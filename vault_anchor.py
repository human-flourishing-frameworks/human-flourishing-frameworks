#!/usr/bin/env python3
"""vault_anchor.py — external time-anchoring for the verifiable memory vault.

The local Ed25519 + Merkle + hash-chain in ``cryptographic_proof.py`` proves
*internal consistency* — that a set of records hashes to a given root and that the
audit chain is unbroken. It does **not** prove a record *existed at a past date*:
whoever holds the data could recompute a consistent chain after the fact.

This module adds the missing external grounding:

  1. **TransparencyLog** — an append-only, hash-chained log of Merkle roots you
     publish periodically (commit it, push to object storage, email it to
     yourself). Once a root is published, any record provably included under that
     root provably existed by the publication time. This is the CT-style
     (RFC 6962-shaped) building block, kept dependency-free and offline-verifiable.

  2. **rfc3161_timestamp()** — requests an RFC 3161 trusted timestamp token for a
     root from a third-party TSA, giving a cryptographic *existed-before* proof
     that doesn't rely on you. It is wired but **degrades gracefully**: if the
     ``rfc3161ng`` package isn't installed or no TSA URL is configured, it returns
     a ``skipped`` status instead of failing — install + configure to enable.

Honest scope: this is tamper-EVIDENT + externally-anchored, not tamper-PROOF.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from cryptographic_proof import MerkleTree

_ZERO = "0" * 64
_DEFAULT_LOG = os.environ.get("TRANSPARENCY_LOG_PATH", "./data/transparency-log.jsonl")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Transparency log: append-only, hash-chained Merkle-root publication
# ---------------------------------------------------------------------------
class TransparencyLog:
    """Append-only JSONL log of Merkle roots, hash-chained for tamper-evidence.

    Each line: ``{seq, root, count, ts, prev_anchor, anchor_hash}`` where
    ``anchor_hash = sha256(prev_anchor || root || count || ts)``. The file is the
    artifact you publish externally; its hash chain lets anyone detect editing or
    reordering of past anchors.
    """

    def __init__(self, path: str = _DEFAULT_LOG) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def _entries(self) -> List[dict]:
        if not os.path.exists(self.path):
            return []
        out = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    def _last_anchor(self) -> str:
        entries = self._entries()
        return entries[-1]["anchor_hash"] if entries else _ZERO

    def append(self, root: str, count: int, ts: Optional[str] = None) -> dict:
        """Publish a Merkle ``root`` (covering ``count`` records) to the log."""
        ts = ts or _now_iso()
        prev = self._last_anchor()
        seq = len(self._entries())
        anchor_hash = _sha256(f"{prev}{root}{count}{ts}".encode("utf-8"))
        entry = {"seq": seq, "root": root, "count": count, "ts": ts,
                 "prev_anchor": prev, "anchor_hash": anchor_hash}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def verify_chain(self) -> Tuple[bool, int]:
        """Recompute the chain; return ``(is_valid, entries_checked)``."""
        prev = _ZERO
        entries = self._entries()
        for i, e in enumerate(entries):
            if e.get("prev_anchor") != prev:
                return False, i
            expected = _sha256(f"{prev}{e['root']}{e['count']}{e['ts']}".encode("utf-8"))
            if e.get("anchor_hash") != expected:
                return False, i
            prev = e["anchor_hash"]
        return True, len(entries)

    def find_root(self, root: str) -> Optional[dict]:
        """Return the (earliest) log entry that published ``root``, if any."""
        for e in self._entries():
            if e["root"] == root:
                return e
        return None


# ---------------------------------------------------------------------------
# RFC 3161 trusted timestamp (wired, degrades gracefully)
# ---------------------------------------------------------------------------
def rfc3161_timestamp(digest_hex: str, tsa_url: Optional[str] = None) -> dict:
    """Request an RFC 3161 timestamp token for ``digest_hex`` from a TSA.

    Returns ``{"status": "ok", "tsa", "token_hex"}`` on success, or
    ``{"status": "skipped", "reason", "install"?}`` when ``rfc3161ng`` is absent,
    no TSA is configured, or the request fails — so callers never crash on the
    optional external dependency.
    """
    tsa_url = tsa_url or os.environ.get("RFC3161_TSA_URL")
    if not tsa_url:
        return {"status": "skipped", "reason": "no TSA configured (set RFC3161_TSA_URL or pass tsa_url=)"}
    try:
        import rfc3161ng  # type: ignore
    except ImportError:
        return {"status": "skipped", "reason": "rfc3161ng not installed", "install": "pip install rfc3161ng"}
    try:
        tsa = rfc3161ng.RemoteTimestamper(tsa_url, hashname="sha256")
        token = tsa(digest=bytes.fromhex(digest_hex))
        return {"status": "ok", "tsa": tsa_url, "token_hex": token.hex()}
    except Exception as e:  # network down, TSA error, malformed response
        return {"status": "skipped", "reason": f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------------
# Anchoring + inclusion verification
# ---------------------------------------------------------------------------
@dataclass
class Anchor:
    root: str
    count: int
    seq: int
    ts: str
    anchor_hash: str
    timestamp_token: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"root": self.root, "count": self.count, "seq": self.seq, "ts": self.ts,
                "anchor_hash": self.anchor_hash, "timestamp_token": self.timestamp_token}


def anchor_records(records: List[dict], log: Optional[TransparencyLog] = None,
                   ts: Optional[str] = None, tsa_url: Optional[str] = None) -> Anchor:
    """Build a Merkle root over ``records``, publish it to the transparency log,
    and attempt an RFC 3161 timestamp. Returns the resulting :class:`Anchor`."""
    tree = MerkleTree(records)
    root = tree.root
    log = log or TransparencyLog()
    entry = log.append(root, len(records), ts=ts)
    token = rfc3161_timestamp(root, tsa_url=tsa_url)
    return Anchor(root=root, count=len(records), seq=entry["seq"], ts=entry["ts"],
                  anchor_hash=entry["anchor_hash"], timestamp_token=token)


def verify_existence(record: dict, records: List[dict], log: TransparencyLog) -> dict:
    """Prove ``record`` existed by the time its covering root was published.

    Returns ``{"included": bool, "published": bool, "existed_by": ts|None,
    "root": str}``: ``included`` = Merkle inclusion proof verifies; ``published``
    = that root appears in the transparency log; ``existed_by`` = the log ts.
    """
    tree = MerkleTree(records)
    target = _sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    try:
        index = tree.leaves.index(target)
    except ValueError:
        return {"included": False, "published": False, "existed_by": None, "root": tree.root}
    proof = tree.get_proof(index)
    included = MerkleTree.verify_proof(record, proof, tree.root)
    entry = log.find_root(tree.root)
    return {"included": included, "published": entry is not None,
            "existed_by": entry["ts"] if entry else None, "root": tree.root}


if __name__ == "__main__":
    recs = [{"event": "memory", "i": i} for i in range(5)]
    tl = TransparencyLog(path="./data/transparency-log-selftest.jsonl")
    a = anchor_records(recs, log=tl, ts="2026-06-30T00:00:00+00:00")
    ok, n = tl.verify_chain()
    res = verify_existence(recs[2], recs, tl)
    print(f"[OK] anchored root={a.root[:16]}… seq={a.seq} ts={a.ts}")
    print(f"[OK] transparency chain valid={ok} ({n} anchors)")
    print(f"[OK] inclusion proof: {res}")
    print(f"[i ] rfc3161: {a.timestamp_token}")
