#!/usr/bin/env python3
"""Contract tests for the Lantern local chat app and local backend."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAT_DIR = REPO_ROOT / "apps" / "lantern-local-chat"
SHELL_HTML = CHAT_DIR / "index.html"
RUNTIME_STATE_JS = CHAT_DIR / "runtime-state.js"
GENERATED_RUNTIME_STATE_JS = CHAT_DIR / "runtime-state.generated.js"
ANCHOR_SNAPSHOT = CHAT_DIR / "anchor-snapshot.json"
LOCAL_BACKEND = CHAT_DIR / "local_lantern_server.py"
LAUNCHER = REPO_ROOT / "scripts" / "start_lantern_local_chat.py"
BATCH_LAUNCHER = REPO_ROOT / "scripts" / "start_lantern_local_chat.bat"


class LanternLocalChatShellTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = SHELL_HTML.read_text(encoding="utf-8")
        cls.launcher = LAUNCHER.read_text(encoding="utf-8")
        cls.batch_launcher = BATCH_LAUNCHER.read_text(encoding="utf-8")
        cls.runtime_state = RUNTIME_STATE_JS.read_text(encoding="utf-8")
        cls.backend = LOCAL_BACKEND.read_text(encoding="utf-8")
        cls.anchor_snapshot = ANCHOR_SNAPSHOT.read_text(encoding="utf-8")

    def test_shell_is_chat_first_and_uses_local_backend(self) -> None:
        for phrase in [
            "Message Lantern", "What are we building next?", "+ New chat",
            "thread-list", "message-row", "composer-area", "sendMessage",
            "fetch(field('backendUrl').value + '/chat'", "Checking local backend",
            "Local backend ready", "Thinking locally", "getLanternAnswer",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)
        for phrase in ["Conversation draft", "Add Lantern response", "Repo state paste area", "function lanternReply"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.html)

    def test_shell_preserves_boundaries(self) -> None:
        for phrase in [
            "No direct GPT calls", "Browser sends chat to localhost only",
            "No GPT/API calls", "no browser command execution; no agents; no tunnels; no public writes",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)
        for blocked in ["api.openai", "anthropic", "google.generativeai", "WebSocket", "EventSource", "eval("]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.html)

    def test_runtime_placeholder_and_anchor_snapshot_exist(self) -> None:
        self.assertTrue(RUNTIME_STATE_JS.exists())
        self.assertIn("window.LANTERN_LOCAL_STATE = null", self.runtime_state)
        self.assertIn("runtime-state.generated.js", self.runtime_state)
        anchors = json.loads(self.anchor_snapshot)["anchors"]
        ids = {anchor["id"] for anchor in anchors}
        for expected in ["anchor-taxonomy", "local-chat-shell", "perfect-adjacent-lantern", "degraded-grounding", "resonance-convergence", "essential-needs"]:
            self.assertIn(expected, ids)

    def test_backend_is_local_repo_anchor_engine(self) -> None:
        for phrase in [
            "Local Lantern chat backend", "ThreadingHTTPServer", "127.0.0.1",
            "ANCHOR_SNAPSHOT", "ANCHOR_TAXONOMY", "build_response", "do_POST",
            "do_GET", "/chat", "/healthz",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.backend)
        for blocked in ["openai.ChatCompletion", "from openai", "import openai", "anthropic.Client", "import anthropic", "google.generativeai", "requests.post", "urllib.request.urlopen", "httpx.", "aiohttp."]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.backend)

    def test_launcher_and_batch_contract(self) -> None:
        for phrase in ["LOCAL_BACKEND", "start_backend", "--no-backend", "Backend URL:", "Backend PID:", "Generated runtime state:"]:
            self.assertIn(phrase, self.launcher)
        self.assertIn("@echo off", self.batch_launcher)
        self.assertIn("cd /d", self.batch_launcher)
        self.assertIn("start_lantern_local_chat.py", self.batch_launcher)
        self.assertIn("--batch-state", self.batch_launcher)
        for blocked in ["curl", "Invoke-WebRequest", "powershell", "gh ", "git pull", "git reset", "git clean"]:
            self.assertNotIn(blocked, self.batch_launcher)

    def test_backend_once_smoke_answers_from_anchors(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LOCAL_BACKEND), "--once", "find anchors and summarize current repo state"],
            cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertIn("Lantern local answer", payload["answer"])
        self.assertIn("Sources:", payload["answer"])
        self.assertIn("anchor rule:", payload["answer"])
        self.assertGreaterEqual(len(payload["selectedAnchors"]), 1)

    def test_launcher_print_and_state_only_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LAUNCHER), "--print-only"],
            cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Lantern local chat app", result.stdout)
        self.assertIn("Backend URL:", result.stdout)

        state_result = subprocess.run(
            [sys.executable, str(LAUNCHER), "--state-only"],
            cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(state_result.returncode, 0, state_result.stderr)
        self.assertIn("Generated runtime state:", state_result.stdout)
        generated_runtime_state = GENERATED_RUNTIME_STATE_JS.read_text(encoding="utf-8")
        self.assertIn("window.LANTERN_LOCAL_STATE =", generated_runtime_state)
        self.assertIn("backendUrl", generated_runtime_state)
        self.assertIn("LOCAL_REPO_ANCHOR_BACKEND", generated_runtime_state)
        self.assertIn("window.LANTERN_LOCAL_STATE = null", RUNTIME_STATE_JS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
