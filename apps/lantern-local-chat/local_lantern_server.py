#!/usr/bin/env python3
"""Local Lantern chat backend.

Localhost-only, repo-grounded response service for the Lantern desktop app.
It intentionally avoids hosted model calls and external network requests. It
reads local repo files and anchor snapshots, returns bounded Lantern responses,
and exposes a Doctor report so the app can validate itself instead of making the
operator act as the permanent copy/paste harness.
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
INDEX_HTML = CHAT_DIR / "index.html"
DOOR_MEMORY_JS = CHAT_DIR / "door-memory.js"
RUNTIME_STATE_JS = CHAT_DIR / "runtime-state.js"
GENERATED_RUNTIME_STATE_JS = CHAT_DIR / "runtime-state.generated.js"

MODES = {
    "engineer": "Engineer: convert the wish into the smallest working system change with validation.",
    "storyteller": "Storyteller: preserve myth, emotion, continuity, and return paths.",
    "comedian": "Comedian: add levity without hiding state or risk.",
    "doctor": "Doctor: diagnose local readiness and reduce operator copy/paste burden.",
    "game-master": "Game Master: turn the moment into playable worlds, choices, and consequences.",
    "anchor-keeper": "Anchor Keeper: compress meaning into bounded restore phrases.",
    "art-mirror": "Art Mirror: turn wishes into visual language and prompts without pretending placeholder art is final.",
    "planner": "Planner: order next actions, people, money, travel, and timing.",
}


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


def select_anchors(message: str, anchors: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    lowered = message.lower()
    scored: list[tuple[int, dict[str, Any]]] = []
    for anchor in anchors:
        haystack = " ".join(str(anchor.get(k, "")) for k in ("id", "kind", "name", "short_meaning", "allowed_use", "restore_phrase")).lower()
        score = 0
        for token in set(lowered.replace("/", " ").replace("-", " ").split()):
            if len(token) >= 4 and token in haystack:
                score += 1
        if score == 0 and any(word in lowered for word in ("anchor", "repo", "state", "lantern", "app", "debt", "money", "hike", "discord", "door", "mask", "art", "converge")):
            if anchor.get("id") in {"hybrid-imagination-engine", "anchor-taxonomy", "local-chat-shell", "perfect-adjacent-lantern", "degraded-grounding"}:
                score = 1
        if score > 0:
            scored.append((score, anchor))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return [anchor for _, anchor in scored[:limit]]


def classify_intent(message: str) -> str:
    text = message.lower()
    if any(term in text for term in ("doctor", "ready", "status", "state", "repo", "dirty", "commit", "branch", "healthz")):
        return "doctor"
    if any(term in text for term in ("anchor", "restore", "hff", "framework")):
        return "anchors"
    if any(term in text for term in ("money", "debt", "paycheck", "gig", "trade", "job")):
        return "essential_needs"
    if any(term in text for term in ("hike", "appalachian", "waru", "friend")):
        return "hike"
    if any(term in text for term in ("mask", "mode", "chameleon", "shapeshift", "imagination", "story", "comedian", "enigma")):
        return "hybrid"
    if any(term in text for term in ("app", "desktop", "chat", "quality", "gate", "brave")):
        return "app"
    return "general"


def _normalize_mode(value: str | None) -> str:
    mode = (value or "engineer").strip().lower().replace("_", "-")
    return mode if mode in MODES else "engineer"


def build_doctor_report() -> dict[str, Any]:
    repo_state = read_repo_state()
    anchors = load_anchors()
    _, ignored_out, _ = _run_git(["check-ignore", "-q", str(GENERATED_RUNTIME_STATE_JS.relative_to(REPO_ROOT))])
    ignored_code, _, _ = _run_git(["check-ignore", "-q", str(GENERATED_RUNTIME_STATE_JS.relative_to(REPO_ROOT))])
    files = {
        "indexHtml": INDEX_HTML.exists(),
        "doorMemoryJs": DOOR_MEMORY_JS.exists(),
        "runtimePlaceholder": RUNTIME_STATE_JS.exists(),
        "generatedRuntimeState": GENERATED_RUNTIME_STATE_JS.exists(),
        "anchorSnapshot": ANCHOR_SNAPSHOT.exists(),
    }
    smoke = build_response("doctor smoke: find anchors and summarize current repo state", mode="doctor", include_doctor=False)
    checks = [
        ("repo clean", repo_state["isClean"]),
        ("anchor snapshot exists", files["anchorSnapshot"]),
        ("door memory exists", files["doorMemoryJs"]),
        ("runtime placeholder exists", files["runtimePlaceholder"]),
        ("generated runtime state ignored by git", ignored_code == 0),
        ("chat smoke builds answer", smoke.get("ok") is True and "Lantern local answer" in smoke.get("answer", "")),
        ("hybrid anchor loaded", any(anchor.get("id") == "hybrid-imagination-engine" for anchor in anchors)),
    ]
    failed = [name for name, ok in checks if not ok]
    status = "READY" if not failed else ("DEGRADED" if len(failed) <= 2 else "BROKEN")
    next_action = "Open the app and choose a mask." if status == "READY" else "Run scripts\\start_lantern_local_chat.bat, then open State > Doctor for the exact failing checks."
    return {
        "ok": True,
        "status": status,
        "repo": repo_state,
        "files": files,
        "generatedRuntimeStateIgnored": ignored_code == 0,
        "anchorsLoaded": len(anchors),
        "modes": sorted(MODES),
        "checks": [{"name": name, "ok": bool(ok)} for name, ok in checks],
        "failedChecks": failed,
        "chatSmoke": {"ok": smoke.get("ok"), "intent": smoke.get("intent"), "mode": smoke.get("mode")},
        "nextAction": next_action,
        "boundary": "Doctor is local-only and read-only except generated runtime state written by the launcher; it performs no GPT/API calls, public writes, payments, agents, tunnels, or sensors.",
    }


def build_response(message: str, mode: str | None = None, include_doctor: bool = True) -> dict[str, Any]:
    active_mode = _normalize_mode(mode)
    repo_state = read_repo_state()
    anchors = load_anchors()
    selected = select_anchors(message, anchors)
    intent = classify_intent(message)
    taxonomy = read_anchor_taxonomy_summary()
    doctor = build_doctor_report() if include_doctor and intent == "doctor" else None

    source_lines = [
        "source: local_lantern_server.py",
        f"mode: {active_mode}",
        f"repo: {repo_state['repoPath']}",
        f"branch: {repo_state['branch']}",
        f"commit: {str(repo_state['commit'])[:12]}",
        f"grounding: {repo_state['groundingMode']}",
        f"anchor rule: {taxonomy}",
    ]
    for anchor in selected:
        source_lines.append(f"anchor: {anchor.get('id')} ({anchor.get('source_surface')})")

    mode_line = MODES[active_mode]
    if intent == "doctor":
        report = doctor or build_doctor_report()
        body = [
            mode_line,
            "Lantern Doctor report:",
            f"Status: {report['status']}",
            f"Branch: {report['repo']['branch']}",
            f"Commit: {str(report['repo']['commit'])[:12]}",
            "Git status: " + (report["repo"]["gitStatusShort"] or "clean"),
            "Failed checks: " + (", ".join(report["failedChecks"]) if report["failedChecks"] else "none"),
            "Next action: " + report["nextAction"],
        ]
    elif intent == "anchors":
        body = [mode_line, "Anchors loaded locally:"]
        for anchor in selected or anchors[:5]:
            body.append(f"- {anchor.get('name')}: {anchor.get('restore_phrase')}")
        body.append("Use anchors as return handles, not authority.")
    elif intent == "essential_needs":
        body = [
            mode_line,
            "Debt rescue should use dated cash flow, holds, reduced costs, and service income before speculative upside.",
            "Highest-confidence stack: stable paycheck, bill negotiation, small service gigs, then productized Discord/local workflow setup.",
            "Rejected for debt rescue: trading, gambling, HFT, or cash-for-risk under pressure.",
            "False-confidence check: project hope is not current income until money arrives.",
        ]
    elif intent == "hike":
        body = [
            mode_line,
            "The hike remains a consent-first wish, not a lock.",
            "Use gentle friend language first: would this still sound fun, how many days, camping/cabin/day hikes, no pressure.",
            "Keep stricter route/weather/gear checks internal until people actually opt in.",
        ]
    elif intent == "hybrid":
        body = [
            "Hybrid Imagination Engine mode engaged.",
            mode_line,
            "The Door remembers. The Mask Rack changes form. The Doctor checks reality underneath.",
            "Next convergence: pick the form that fits the moment, then produce one bounded useful artifact or action.",
        ]
    elif intent == "app":
        body = [
            mode_line,
            "Quality gate: the app should diagnose itself before asking Alex to validate manually.",
            "The visible soul is Door + Mask Rack + Chat; the Doctor stays underneath as readiness state.",
            "Next move: use /doctor for READY / DEGRADED / BROKEN instead of repeated copy/paste loops.",
        ]
    else:
        body = [
            mode_line,
            "I can answer from local repo state and the anchor snapshot now.",
            "Use the Mask Rack to shift form: engineer, storyteller, comedian, doctor, game master, anchor keeper, art mirror, or planner.",
            "I will label grounding and avoid pretending this is a hosted model response.",
        ]

    limits = [
        "No direct hosted model calls.",
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
        "mode": active_mode,
        "doctor": doctor,
        "sources": source_lines,
        "limits": limits,
    }


class LanternHandler(BaseHTTPRequestHandler):
    server_version = "LocalLantern/0.2"

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
        if path == "/doctor":
            self._send_json(200, build_doctor_report())
            return
        if path == "/modes":
            self._send_json(200, {"ok": True, "modes": MODES})
            return
        self._send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path not in {"/chat", "/doctor/run"}:
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        if path == "/doctor/run":
            self._send_json(200, build_doctor_report())
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw) if raw else {}
            message = str(data.get("message", "")).strip()
            mode = str(data.get("mode", "engineer")).strip()
            if not message:
                self._send_json(400, {"ok": False, "error": "message is required"})
                return
            self._send_json(200, build_response(message, mode=mode))
        except Exception as exc:  # pragma: no cover - defensive server boundary
            self._send_json(500, {"ok": False, "error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Lantern backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--once", default="", help="Return one local Lantern answer without starting the server.")
    parser.add_argument("--mode", default="engineer", choices=sorted(MODES))
    parser.add_argument("--doctor", action="store_true", help="Print one Doctor report and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.doctor:
        print(json.dumps(build_doctor_report(), indent=2))
        return 0
    if args.once:
        print(json.dumps(build_response(args.once, mode=args.mode), indent=2))
        return 0
    server = ThreadingHTTPServer((args.host, args.port), LanternHandler)
    print(f"Local Lantern backend listening on http://{args.host}:{args.port}")
    print("Boundary: localhost only; no hosted model calls; no external network requests.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
