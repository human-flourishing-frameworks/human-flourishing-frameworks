#!/usr/bin/env python3
"""Contract tests for the Lantern local chat shell."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHELL_HTML = REPO_ROOT / "apps" / "lantern-local-chat" / "index.html"
RUNTIME_STATE_JS = REPO_ROOT / "apps" / "lantern-local-chat" / "runtime-state.js"
LAUNCHER = REPO_ROOT / "scripts" / "start_lantern_local_chat.py"
BATCH_LAUNCHER = REPO_ROOT / "scripts" / "start_lantern_local_chat.bat"


class LanternLocalChatShellTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = SHELL_HTML.read_text(encoding="utf-8")
        cls.launcher = LAUNCHER.read_text(encoding="utf-8")
        cls.batch_launcher = BATCH_LAUNCHER.read_text(encoding="utf-8")
        cls.runtime_state = RUNTIME_STATE_JS.read_text(encoding="utf-8")

    def test_shell_exists_and_declares_local_lantern_surface(self) -> None:
        self.assertTrue(SHELL_HTML.exists())
        self.assertIn("Lantern Local Chat Shell", self.html)
        self.assertIn("Local-first operator interface", self.html)
        self.assertIn("Lantern-style bounded support", self.html)
        self.assertIn("not GPT execution", self.html)
        self.assertIn("not a hosted LLM endpoint", self.html)
        self.assertIn("not autonomous authority", self.html)

    def test_shell_has_required_issue_142_panels(self) -> None:
        for phrase in [
            "Conversation draft",
            "Repo state",
            "git status --short",
            "Latest handoff packet",
            "Shell default",
            "Grounding mode",
            "Anchors in force",
            "Batch mode",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)

    def test_shell_preserves_local_first_no_executor_boundary(self) -> None:
        for phrase in [
            "Commands stay copy-only",
            "does not execute shell commands",
            "No command execution",
            "No command execution from browser, no GPT calls, no agents, no tunnels, no sensors, no public writes",
            "no GPT calls; no command execution from browser; no hidden telemetry; no public writes; no autonomous action",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)

    def test_shell_uses_generated_runtime_state_without_fetching(self) -> None:
        self.assertIn('script src="runtime-state.js"', self.html)
        self.assertIn("window.LANTERN_LOCAL_STATE", self.html)
        self.assertIn("FULL_REPO_GROUNDED_FROM_LOCAL_BATCH", self.html)
        self.assertIn("Batch state loaded", self.html)
        for phrase in ["fetch(", "XMLHttpRequest", "WebSocket", "EventSource"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.html)

    def test_shell_does_not_contain_browser_execution_primitives(self) -> None:
        blocked = [
            "child_process",
            "powershell.exe",
            "cmd.exe /c",
            "Start-Process",
            "exec(",
            "eval(",
        ]
        for phrase in blocked:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.html)

    def test_shell_uses_local_storage_only_for_draft_state(self) -> None:
        self.assertIn("localStorage", self.html)
        self.assertIn("lantern-local-chat-shell-v1", self.html)
        self.assertIn("Clear local draft", self.html)
        self.assertNotIn("sessionStorage", self.html)

    def test_launcher_exists_and_writes_read_only_state_snapshot(self) -> None:
        self.assertTrue(LAUNCHER.exists())
        self.assertIn("Open the Lantern local chat shell", self.launcher)
        self.assertIn("write_runtime_state", self.launcher)
        self.assertIn("RUNTIME_STATE_JS", self.launcher)
        self.assertIn("git", self.launcher)
        self.assertIn("status", self.launcher)
        self.assertIn("branch", self.launcher)
        self.assertIn("rev-parse", self.launcher)
        self.assertIn("no GPT calls", self.launcher)
        self.assertIn("no command execution, no agents, no tunnels, no public writes", self.launcher)
        for blocked in [
            "Flask(",
            "app.run",
            "requests.",
            "http.server",
            "openai",
            "anthropic",
            "google.generativeai",
        ]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.launcher)

    def test_batch_launcher_is_cmd_safe_and_local_only(self) -> None:
        self.assertTrue(BATCH_LAUNCHER.exists())
        self.assertIn("@echo off", self.batch_launcher)
        self.assertIn("cd /d", self.batch_launcher)
        self.assertIn("start_lantern_local_chat.py", self.batch_launcher)
        self.assertIn("--batch-state", self.batch_launcher)
        self.assertIn("No GPT calls", self.batch_launcher)
        for blocked in ["curl", "Invoke-WebRequest", "powershell", "gh ", "git pull", "git reset", "git clean"]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.batch_launcher)

    def test_runtime_state_placeholder_is_non_networked(self) -> None:
        self.assertTrue(RUNTIME_STATE_JS.exists())
        self.assertIn("window.LANTERN_LOCAL_STATE = null", self.runtime_state)
        self.assertIn("No GPT call", self.runtime_state)
        self.assertNotIn("fetch(", self.runtime_state)
        self.assertNotIn("XMLHttpRequest", self.runtime_state)

    def test_launcher_print_only_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LAUNCHER), "--print-only"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Lantern local chat shell", result.stdout)
        self.assertIn("file://", result.stdout)
        self.assertIn("Runtime state:", result.stdout)
        self.assertIn("no GPT calls", result.stdout)

    def test_launcher_state_only_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LAUNCHER), "--state-only"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Runtime state:", result.stdout)
        runtime_state = RUNTIME_STATE_JS.read_text(encoding="utf-8")
        self.assertIn("window.LANTERN_LOCAL_STATE =", runtime_state)
        self.assertIn("gitStatusShort", runtime_state)
        self.assertIn("no GPT call", runtime_state.lower())


if __name__ == "__main__":
    unittest.main()
