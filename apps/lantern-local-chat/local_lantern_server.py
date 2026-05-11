#!/usr/bin/env python3
"""Local Lantern chat backend.

This is a localhost-only, repo-grounded response service for the Lantern desktop
chat app. It intentionally avoids OpenAI/GPT/API calls and external network
requests. It reads local repo files and anchor snapshots, then returns bounded
Lantern responses with source labels and limits.
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[2]
CHAT_DIR = REPO_ROOT / "apps" / "lantern-local-chat"
ANCHOR_SNAPSHOT = CHAT_DIR / "anchor-snapshot.json"
ANCHOR_TAXONOMY = REPO_ROOT / "docs" / "anchor-taxonomy.md"

BLOCKED_NETWORK_TERMS = (
    "openai",
    "anthropic",
    "google.generativeai",
    "requests.",
    "urllib.request",
    "httpx",
    "aiohttp",
)


def _run_git(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def read_repo_state() -> dict[str, Any]:
    status_code, status_out, status_err = _run_git(["status", "--short"])
    branch_code, branch_out, branch_err = _run_git(["branch", "--show-current"])
    commit_code, commit_out, commit_err = _run_git(["rev-parse", "HEAD"])
    errors = [err for err in (status_err, branch_err, commit_err) if err]
    clean = status_code == 0 and branch_code == 0 and commit_code == 0 and not status_out.strip()
    return {
        "repoPath": str(REPO_ROOT),
        "branch": branch_out if branch_code == 0 else "UNKNOWN",
        "commit": commit_out if commit_code == 0 else "UNKNOWN",
        "gitStatusShort": status_out if status_code == 0 else "UNAVAILABLE",
        "isClean": clean,
        "errors": errors,
        "groundingMode": "LOCAL_REPO_ANCHOR_BACKEND" if not errors else "UNAVAILABLE_OR_DEGRADED",
    }


def load_anchors() -> list[dict[str, Any]]:
    if not ANCHOR_SNAPSHOT.exists():
        return []
    data = json.loads(ANCHOR_SNAPSHOT.read_text(encoding="utf-8"))
    anchors = data.get("anchors", [])
    if isinstance(anchors, list):
        return [a for a in anchors if isinstance(a, dict)]
    return []


def read_anchor_taxonomy_summary() -> str:
    if not ANCHOR_TAXONOMY.exists():
        return "Anchor taxonomy unavailable."
    text = ANCHOR_TAXONOMY.read_text(encoding="utf-8")
    key = "Anchor = a compact, named, source-labeled continuity handle with a boundary."
    if key in text:
        return key
    return "Anchors are compact continuity handles with boundaries."


def select_anchors(message: str, anchors: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    lowered = message.lower()
    scored: list[tuple[int, dict[str, Any]]] = []
    for anchor in anchors:
        haystack = " ".join(str(anchor.get(k, "")) for k in ("id", "kind", "name", "short_meaning", "allowed_use", "restore_phrase")).lower()
        score = 0
        for token in set(lowered.replace("/", " ").replace("-", " ").split()):
            if len(token) >= 4 and token in haystack:
                score += 1
        if score == 0 and any(word in lowered for word in ("anchor", "repo", "state", "lantern", "app", "debt", "money", "hike", "discord")):
            if anchor.get("id") in {"anchor-taxonomy", "local-chat-shell", "perfect-adjacent-lantern", "degraded-grounding"}:
                score = 1
        if score > 0:
            scored.append((score, anchor))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return [anchor for _, anchor in scored[:limit]]


def classify_intent(message: str) -> str:
    text = message.lower()
    if any(term in text for term in ("ready", "status", "state", "repo", "dirty", "commit", "branch")):
        return "state"
    if any(term in text for term in ("anchor", "restore", "hff", "framework")):
        return "anchors"
    if any(term in text for term in ("money", "debt", "paycheck", "gig", "trade", "job")):
        return "essential_needs"
    if any(term in text for term in ("hike", "appalachian", "waru", "friend")):
        return "hike"
    if any(term in text for term in ("app", "desktop", "chat", "quality", "gate", "brave")):
        return "app"
    return "general"


def build_response(message: str) -> dict[str, Any]:
    repo_state = read_repo_state()
    anchors = load_anchors()
    selected = select_anchors(message, anchors)
    intent = classify_intent(message)
    taxonomy = read_anchor_taxonomy_summary()

    source_lines = [
        "source: local_lantern_server.py",
        f"repo: {repo_state['repoPath']}",
        f"branch: {repo_state['branch']}",
        f"commit: {str(repo_state['commit'])[:12]}",
        f"grounding: {repo_state['groundingMode']}",
        f"anchor rule: {taxonomy}",
    ]
    for anchor in selected:
        source_lines.append(f"anchor: {anchor.get('id')} ({anchor.get('source_surface')})")

    if intent == "state":
        body = [
            "Current local state is the first truth surface.",
            f"Repo path: {repo_state['repoPath']}",
            f"Branch: {repo_state['branch']}",
            f"Commit: {repo_state['commit']}",
            "Git status: " + (repo_state['gitStatusShort'] or "clean"),
            "Next move: only call the app ready after the backend chat path answers from local repo/anchor state and tests pass.",
        ]
    elif intent == "anchors":
        body = ["Anchors loaded locally:"]
        for anchor in selected or anchors[:5]:
            body.append(f"- {anchor.get('name')}: {anchor.get('restore_phrase')}")
        body.append("Use anchors as return handles, not authority.")
    elif intent == "essential_needs":
        body = [
            "Debt rescue should use dated cash flow, holds, reduced costs, and service income before speculative upside.",
            "Highest-confidence stack: stable paycheck, bill negotiation, small service gigs, then productized Discord/local workflow setup.",
            "Rejected for debt rescue: trading, gambling, HFT, or cash-for-risk under pressure.",
            "False-confidence check: project hope is not current income until money arrives.",
        ]
    elif intent == "hike":
        body = [
            "The hike remains a consent-first wish, not a lock.",
            "Use gentle friend language first: would this still sound fun, how many days, camping/cabin/day hikes, no pressure.",
            "Keep stricter route/weather/gear checks internal until people actually opt in.",
        ]
    elif intent == "app":
        body = [
            "Quality gate: a typed message must produce a repo/anchor-grounded answer through localhost, not canned browser text.",
            "This backend is that missing path: /chat reads local repo state and anchor snapshots, then returns a bounded answer.",
            "The browser remains a chat UI; the local backend does the repo/anchor response work.",
        ]
    else:
        body = [
            "I can answer from local repo state and the anchor snapshot now.",
            "Ask for anchors, repo state, app readiness, debt plan, hike planning, or the next bounded change.",
            "I will label grounding and avoid pretending this is a direct GPT/API response.",
        ]

    limits = [
        "No direct GPT/API calls.",
        "No external network requests.",
        "No browser command execution.",
        "No agents, tunnels, sensors, public writes, payments, or account actions.",
        "Local files and git state can still be stale if the repo is not pulled.",
    ]

    text = "\n".join([
        "Lantern local answer",
        "",
        *body,
        "",
        "Sources:",
        *source_lines,
        "",
        "Limits:",
        *[f"- {item}" for item in limits],
    ])

    return {
        "ok": True,
        "answer": text,
        "repoState": repo_state,
        "selectedAnchors": selected,
        "intent": intent,
        "sources": source_lines,
        "limits": limits,
    }


class LanternHandler(BaseHTTPRequestHandler):
    server_version = "LocalLantern/0.1"

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_json(200, {"ok": True})

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/healthz":
            self._send_json(200, {"ok": True, "service": "local-lantern", "repoState": read_repo_state()})
            return
        if path == "/anchors":
            self._send_json(200, {"ok": True, "anchors": load_anchors()})
            return
        self._send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/chat":
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw) if raw else {}
            message = str(data.get("message", "")).strip()
            if not message:
                self._send_json(400, {"ok": False, "error": "message is required"})
                return
            self._send_json(200, build_response(message))
        except Exception as exc:  # pragma: no cover - defensive server boundary
            self._send_json(500, {"ok": False, "error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        # Keep the desktop app quiet unless launched directly for debugging.
        return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Lantern backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--once", default="", help="Return one local Lantern answer without starting the server.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.once:
        print(json.dumps(build_response(args.once), indent=2))
        return 0
    server = ThreadingHTTPServer((args.host, args.port), LanternHandler)
    print(f"Local Lantern backend listening on http://{args.host}:{args.port}")
    print("Boundary: localhost only; no GPT/API calls; no external network requests.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
