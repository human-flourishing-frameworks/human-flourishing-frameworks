#!/usr/bin/env python3
"""Local Lantern chat backend.

Localhost-only repo and anchor service for the Lantern desktop app.
No hosted model call is made.
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
    "doctor": "Doctor: diagnose local readiness and reduce operator copy-paste burden.",
    "game-master": "Game Master: turn the moment into playable worlds, choices, and consequences.",
    "anchor-keeper": "Anchor Keeper: compress meaning into bounded restore phrases.",
    "art-mirror": "Art Mirror: turn wishes into visual language and prompts without pretending placeholder art is final.",
    "planner": "Planner: order next actions, people, money, travel, and timing.",
}


def _run_git(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def read_repo_state() -> dict[str, Any]:
    status_code, status_out, status_err = _run_git(["status", "--short"])
    branch_code, branch_out, branch_err = _run_git(["branch", "--show-current"])
    commit_code, commit_out, commit_err = _run_git(["rev-parse", "HEAD"])
    errors = [err for err in (status_err, branch_err, commit_err) if err]
    return {
        "repoPath": str(REPO_ROOT),
        "branch": branch_out if branch_code == 0 else "UNKNOWN",
        "commit": commit_out if commit_code == 0 else "UNKNOWN",
        "gitStatusShort": status_out if status_code == 0 else "UNAVAILABLE",
        "isClean": status_code == 0 and branch_code == 0 and commit_code == 0 and not status_out.strip(),
        "errors": errors,
        "groundingMode": "LOCAL_REPO_ANCHOR_BACKEND" if not errors else "UNAVAILABLE_OR_DEGRADED",
    }


def load_anchors() -> list[dict[str, Any]]:
    if not ANCHOR_SNAPSHOT.exists():
        return []
    data = json.loads(ANCHOR_SNAPSHOT.read_text(encoding="utf-8"))
    anchors = data.get("anchors", [])
    return [item for item in anchors if isinstance(item, dict)] if isinstance(anchors, list) else []


def read_anchor_taxonomy_summary() -> str:
    if not ANCHOR_TAXONOMY.exists():
        return "Anchor taxonomy unavailable."
    text = ANCHOR_TAXONOMY.read_text(encoding="utf-8")
    key = "Anchor = a compact, named, source-labeled continuity handle with a boundary."
    return key if key in text else "Anchors are compact continuity handles with boundaries."


def select_anchors(message: str, anchors: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    lowered = message.lower()
    scored: list[tuple[int, dict[str, Any]]] = []
    defaults = {"hybrid-imagination-engine", "anchor-taxonomy", "local-chat-shell", "perfect-adjacent-lantern", "degraded-grounding"}
    for anchor in anchors:
        haystack = " ".join(str(anchor.get(k, "")) for k in ("id", "kind", "name", "short_meaning", "allowed_use", "restore_phrase")).lower()
        score = sum(1 for token in set(lowered.replace("/", " ").replace("-", " ").split()) if len(token) >= 4 and token in haystack)
        if score == 0 and any(word in lowered for word in ("anchor", "repo", "state", "lantern", "app", "debt", "money", "hike", "discord", "door", "mask", "art", "converge")) and anchor.get("id") in defaults:
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
    if any(term in text for term in ("mask", "mode", "chameleon", "shapeshift", "imagination", "story", "comedian", "enigma", "converge")):
        return "hybrid"
    if any(term in text for term in ("app", "desktop", "chat", "quality", "gate", "brave")):
        return "app"
    return "general"


def _normalize_mode(value: str | None) -> str:
    mode = (value or "engineer").strip().lower().replace("_", "-")
    return mode if mode in MODES else "engineer"


def build_minimal_frame(message: str, intent: str, active_mode: str, repo_state: dict[str, Any], doctor: dict[str, Any] | None = None) -> dict[str, str]:
    if intent == "doctor":
        status = (doctor or {}).get("status", "SMOKE")
        return {
            "Vibe": "Check the floor before the form changes.",
            "Fact": f"Doctor status is {status}; branch is {repo_state['branch']} at {str(repo_state['commit'])[:12]}.",
            "Boundary": "Readiness is local evidence, not a future guarantee.",
            "Next": (doctor or {}).get("nextAction", "Finish the containing Doctor check."),
        }
    if intent == "hybrid":
        return {
            "Vibe": "Lantern shifts form; the Doctor still checks reality underneath.",
            "Fact": f"Active mask is {active_mode}; response is local repo and anchor grounded.",
            "Boundary": "Shapeshifting is style and tooling, not autonomy or proof.",
            "Next": "Use the active mask for one bounded useful artifact or action.",
        }
    if intent == "app":
        return {
            "Vibe": "The interface should sync to Alex, not make Alex sync to it.",
            "Fact": "Door, Mask Rack, chat, and Doctor are the current desktop surfaces.",
            "Boundary": "Do not call the app ready when backend, runtime state, or tests are degraded.",
            "Next": "Use Doctor status before asking for more evidence.",
        }
    return {
        "Vibe": MODES[active_mode],
        "Fact": f"Local repo state is {repo_state['branch']} at {str(repo_state['commit'])[:12]}.",
        "Boundary": "This is bounded local output, not an oracle or perfect memory.",
        "Next": "Preserve state, limits, and one useful next move.",
    }


def build_doctor_report() -> dict[str, Any]:
    repo_state = read_repo_state()
    anchors = load_anchors()
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
        ("minimal convergence frame present", isinstance(smoke.get("minimalFrame"), dict) and "Vibe" in smoke.get("minimalFrame", {})),
    ]
    failed = [name for name, ok in checks if not ok]
    status = "READY" if not failed else ("DEGRADED" if len(failed) <= 2 else "BROKEN")
    next_action = "Open the app and choose a mask." if status == "READY" else "Run the launcher, then recheck Doctor."
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
        "boundary": "Doctor is local-only and read-only except generated runtime state written by the launcher.",
    }


def build_response(message: str, mode: str | None = None, include_doctor: bool = True) -> dict[str, Any]:
    active_mode = _normalize_mode(mode)
    repo_state = read_repo_state()
    anchors = load_anchors()
    selected = select_anchors(message, anchors)
    intent = classify_intent(message)
    taxonomy = read_anchor_taxonomy_summary()
    doctor = build_doctor_report() if include_doctor and intent == "doctor" else None
    minimal_frame = build_minimal_frame(message, intent, active_mode, repo_state, doctor)
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
    if intent == "doctor" and doctor:
        body = [mode_line, "Lantern Doctor report:", f"Status: {doctor['status']}", f"Branch: {doctor['repo']['branch']}", f"Commit: {str(doctor['repo']['commit'])[:12]}", "Git status: " + (doctor["repo"]["gitStatusShort"] or "clean"), "Failed checks: " + (", ".join(doctor["failedChecks"]) if doctor["failedChecks"] else "none"), "Next action: " + doctor["nextAction"]]
    elif intent == "doctor":
        body = [mode_line, "Lantern Doctor smoke response:", "Status: SMOKE", "This path does not call build_doctor_report again."]
    elif intent == "anchors":
        body = [mode_line, "Anchors loaded locally:"] + [f"- {a.get('name')}: {a.get('restore_phrase')}" for a in (selected or anchors[:5])] + ["Use anchors as return handles, not authority."]
    elif intent == "hybrid":
        body = ["Hybrid Imagination Engine mode engaged.", mode_line, "The Door remembers. The Mask Rack changes form. The Doctor checks reality underneath.", "Next convergence: pick the form that fits the moment, then produce one bounded useful artifact or action."]
    else:
        body = [mode_line, "I can answer from local repo state and the anchor snapshot now.", "Use the Mask Rack to shift form while keeping the minimal frame underneath."]
    limits = ["No direct hosted model calls.", "No external network requests.", "No browser command execution.", "Local files and git state can still be stale if the repo is not pulled."]
    frame_lines = ["Minimal convergence frame:", *[f"{key}: {value}" for key, value in minimal_frame.items()]]
    text = "\n".join(["Lantern local answer", "", *body, "", *frame_lines, "", "Sources:", *source_lines, "", "Limits:", *[f"- {item}" for item in limits]])
    return {"ok": True, "answer": text, "repoState": repo_state, "selectedAnchors": selected, "intent": intent, "mode": active_mode, "doctor": doctor, "minimalFrame": minimal_frame, "sources": source_lines, "limits": limits}


class LanternHandler(BaseHTTPRequestHandler):
    server_version = "LocalLantern/0.4"

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
            data = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            message = str(data.get("message", "")).strip()
            mode = str(data.get("mode", "engineer")).strip()
            if not message:
                self._send_json(400, {"ok": False, "error": "message is required"})
                return
            self._send_json(200, build_response(message, mode=mode))
        except Exception as exc:  # pragma: no cover
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
