"""Lantern Flask server — shell scaffold.

This slice is intentionally inert with respect to LLM calls. It serves
the static frontend and exposes a stub ``/api/lantern/chat`` that returns
a clear "not wired yet" payload. The Anthropic API call lands in a
follow-up PR so this scaffold can be reviewed and run locally without
requiring a key.

Boundary (enforced by ``main()``):
- localhost-only bind by default; public bind requires
  ``LANTERN_ALLOW_PUBLIC=true`` env var which must NEVER be set on the
  Render / Railway production surface;
- no autonomous repo writes;
- no secrets read into the response.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


REPO_ROOT = Path(__file__).resolve().parents[1]
LANTERN_DIR = Path(__file__).resolve().parent

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Serve the chat UI."""
    return send_from_directory(str(LANTERN_DIR), "index.html")


@app.route("/app.js")
def app_js():
    return send_from_directory(str(LANTERN_DIR), "app.js")


# ---------------------------------------------------------------------------
# Health / state stubs
# ---------------------------------------------------------------------------


@app.route("/api/lantern/health")
def health():
    """Lightweight readiness probe with explicit toggle visibility."""
    return jsonify({
        "status": "ok",
        "service": "lantern",
        "role": "Lantern Keystone Wish",
        "anchor": "Show the state. Say the limit. Self-correct before acting.",
        "substrate_wired": False,
        "anthropic_api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "public_bind_enabled": _public_bind_enabled(),
    })


@app.route("/api/lantern/state")
def state():
    """Stub state endpoint. Real implementation lands in slice 2."""
    return jsonify({
        "status": "scaffold",
        "message": (
            "state endpoint not yet wired; will report branch, commit, "
            "open PRs, gate states, and loaded memory files in slice 2"
        ),
        "loaded_doctrine": _loaded_doctrine_paths(),
    })


@app.route("/api/lantern/chat", methods=["POST"])
def chat():
    """Stub chat endpoint.

    Returns a clear "not wired yet" payload so the frontend can be
    exercised before the Anthropic API call lands. Does NOT call any LLM.
    """
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    return jsonify({
        "status": "scaffold",
        "user_message_received": user_message,
        "role": "Lantern Keystone Wish",
        "reply": (
            "Lantern scaffold is up. The LLM substrate is not yet wired "
            "in this slice. Set ANTHROPIC_API_KEY and wait for slice 2 "
            "(the /api/lantern/chat Anthropic call) before expecting "
            "real responses."
        ),
        "anchor": "Show the state. Say the limit.",
        "next_slice": "slice 2: Anthropic API wiring",
    })


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _loaded_doctrine_paths() -> list[str]:
    """Return the doctrine file paths that the real chat endpoint will
    read fresh per call once the substrate is wired."""
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


def _public_bind_enabled() -> bool:
    return os.environ.get("LANTERN_ALLOW_PUBLIC", "").lower() in {
        "1", "true", "yes", "on",
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Start the Lantern server bound to localhost by default."""
    host = "127.0.0.1"
    if _public_bind_enabled():
        # Operator explicitly opted into public bind. This must NEVER be
        # set on the Render / Railway production surface. Print a loud
        # warning so accidental misuse is visible.
        host = "0.0.0.0"
        print(
            "[LANTERN][WARNING] LANTERN_ALLOW_PUBLIC=true — binding to "
            "0.0.0.0. This must not run on the public Render / Railway "
            "surface. Localhost is the default; unset the env var to "
            "restore."
        )

    port = int(os.environ.get("LANTERN_PORT", "5173"))
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "[LANTERN] ANTHROPIC_API_KEY not set. Chat will return "
            "scaffold-stub replies until the key is set AND slice 2 "
            "(API wiring) lands."
        )

    print(f"[LANTERN] role=Lantern Keystone Wish bind={host}:{port}")
    app.run(host=host, port=port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
