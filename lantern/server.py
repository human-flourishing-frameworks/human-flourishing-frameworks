"""Lantern Flask server - local-first shell.

This runtime is intentionally bounded. It serves the static frontend and
exposes local/read-only truth endpoints before any LLM substrate is wired.

Current slice:
- `/api/lantern/health` reports substrate/key/bind toggles;
- `/api/lantern/state` reads local git HEAD/ref state, doctrine paths, and an
  optional last-test record;
- `/api/lantern/chat` still returns a scaffold payload and does NOT call any
  LLM.

Boundary:
- localhost-only bind by default;
- read-only local inspection only;
- no autonomous repo writes.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory


REPO_ROOT = Path(__file__).resolve().parents[1]
LANTERN_DIR = Path(__file__).resolve().parent
LANTERN_HOME = Path.home() / ".lantern"
LAST_TEST_PATH = LANTERN_HOME / "state" / "last-test.json"

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the chat UI."""
    return send_from_directory(str(LANTERN_DIR), "index.html")


@app.route("/app.js")
def app_js():
    return send_from_directory(str(LANTERN_DIR), "app.js")


@app.route("/api/lantern/health")
def health():
    """Lightweight readiness probe with explicit toggle visibility."""
    return jsonify({
        "status": "ok",
        "service": "lantern",
        "role": "Lantern Keystone Wish",
        "anchor": "Show the state. Say the limit. Self-correct before acting.",
        "substrate_wired": False,
        "state_endpoint_wired": True,
        "anthropic_api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "public_bind_enabled": _public_bind_enabled(),
    })


@app.route("/api/lantern/state")
def state():
    """Return read-only local truth panel state."""
    return jsonify({
        "status": "scaffold",
        "state_status": "ok",
        "truth_panel_wired": True,
        "service": "lantern",
        "timestamp_utc": _utc_now(),
        "anchor": "Show the state. Say the limit. Then act small.",
        "repo": _repo_state(),
        "loaded_doctrine": _loaded_doctrine_paths(),
        "last_test": _last_test_state(),
        "limits": [
            "read-only local state only",
            "chat substrate is not wired in this slice",
            "dirty worktree details require the operator to run git status",
            "no repo writes, merges, deploys, agents, or tunnels",
        ],
    })


@app.route("/api/lantern/chat", methods=["POST"])
def chat():
    """Stub chat endpoint. Does NOT call any LLM."""
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    return jsonify({
        "status": "scaffold",
        "user_message_received": user_message,
        "role": "Lantern Keystone Wish",
        "reply": (
            "Lantern local shell is up. The truth panel is wired to read "
            "local repo HEAD/ref state, but the LLM substrate is not yet "
            "wired in this slice."
        ),
        "anchor": "Show the state. Say the limit.",
        "next_slice": "LLM substrate wiring after local truth panel validation",
    })


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _git_dir() -> Path:
    marker = REPO_ROOT / ".git"
    if marker.is_dir():
        return marker
    if marker.is_file():
        text = marker.read_text(encoding="utf-8", errors="replace").strip()
        prefix = "gitdir:"
        if text.lower().startswith(prefix):
            target = text[len(prefix):].strip()
            path = Path(target)
            if not path.is_absolute():
                path = (REPO_ROOT / path).resolve()
            return path
    return marker


def _read_git_ref(git_dir: Path, ref: str) -> str | None:
    ref_path = git_dir / ref
    if ref_path.is_file():
        return ref_path.read_text(encoding="utf-8", errors="replace").strip()

    packed_refs = git_dir / "packed-refs"
    if packed_refs.is_file():
        for line in packed_refs.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            try:
                sha, packed_ref = line.split(" ", 1)
            except ValueError:
                continue
            if packed_ref.strip() == ref:
                return sha.strip()
    return None


def _repo_state() -> dict[str, Any]:
    git_dir = _git_dir()
    head_path = git_dir / "HEAD"

    if not head_path.is_file():
        return {
            "status": "unavailable",
            "path": str(REPO_ROOT),
            "branch": None,
            "commit": None,
            "commit_short": None,
            "dirty": None,
            "dirty_status": "not_checked",
            "status_short": [],
            "errors": ["git HEAD not found"],
        }

    head = head_path.read_text(encoding="utf-8", errors="replace").strip()
    branch = None
    commit = None
    if head.startswith("ref: "):
        ref = head[5:].strip()
        branch = ref.removeprefix("refs/heads/")
        commit = _read_git_ref(git_dir, ref)
    else:
        commit = head

    return {
        "status": "ok" if commit else "unavailable",
        "path": str(REPO_ROOT),
        "branch": branch,
        "commit": commit,
        "commit_short": commit[:12] if commit else None,
        "dirty": None,
        "dirty_status": "not_checked",
        "status_short": [],
        "errors": [] if commit else ["git commit not resolved from HEAD"],
    }


def _loaded_doctrine_paths() -> list[str]:
    candidates = [
        "docs/seven-anchors-self-correction.md",
        "docs/convergence-status.md",
        "docs/keystone-memory-contract.md",
        "docs/keystone-self-convergence.md",
        "docs/keystone-table-door-anchors.md",
        "docs/lantern-chat-design.md",
    ]
    found = []
    for rel in candidates:
        if (REPO_ROOT / rel).is_file():
            found.append(rel)
    return found


def _last_test_state() -> dict[str, Any]:
    display_path = "~/.lantern/state/last-test.json"
    if not LAST_TEST_PATH.is_file():
        return {
            "status": "missing",
            "path": display_path,
            "message": "No last-test evidence file found.",
        }

    try:
        data = json.loads(LAST_TEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "unreadable",
            "path": display_path,
            "message": str(exc),
        }

    if not isinstance(data, dict):
        return {
            "status": "invalid",
            "path": display_path,
            "message": "last-test JSON must be an object",
        }

    data.setdefault("status", "present")
    data.setdefault("path", display_path)
    return data


def _public_bind_enabled() -> bool:
    return os.environ.get("LANTERN_ALLOW_PUBLIC", "").lower() in {
        "1", "true", "yes", "on",
    }


def main(argv: list[str] | None = None) -> int:
    """Start the Lantern server bound to localhost by default."""
    host = "127.0.0.1"
    if _public_bind_enabled():
        host = "0.0.0.0"
        print(
            "[LANTERN][WARNING] LANTERN_ALLOW_PUBLIC=true - binding to "
            "0.0.0.0. Localhost is the default; unset the env var to restore."
        )

    port = int(os.environ.get("LANTERN_PORT", "5173"))
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "[LANTERN] ANTHROPIC_API_KEY not set. Chat will return "
            "scaffold-stub replies until the substrate wiring slice lands."
        )

    print(f"[LANTERN] role=Lantern Keystone Wish bind={host}:{port}")
    app.run(host=host, port=port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
