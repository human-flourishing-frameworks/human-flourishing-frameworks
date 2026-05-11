#!/usr/bin/env python3
"""Contract tests for the Lantern local chat shell."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHELL_HTML = REPO_ROOT / "apps" / "lantern-local-chat" / "index.html"
LAUNCHER = REPO_ROOT / "scripts" / "start_lantern_local_chat.py"


class LanternLocalChatShellTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = SHELL_HTML.read_text(encoding="utf-8")
        cls.launcher = LAUNCHER.read_text(encoding="utf-8")

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
            "Repo state paste area",
            "git status --short",
            "Latest handoff packet",
            "Shell default",
            "Grounding mode",
            "Anchors in force",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)

    def test_shell_preserves_local_first_no_executor_boundary(self) -> None:
        for phrase in [
            "Commands stay copy-only",
            "does not execute shell commands",
            "No command execution",
            "No command execution, no agents, no tunnels, no sensors, no public writes",
            "no command execution; no hidden telemetry; no public writes; no autonomous action",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)

    def test_shell_does_not_contain_network_or_execution_primitives(self) -> None:
        blocked = [
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "EventSource",
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

    def test_launcher_exists_and_is_static_file_only(self) -> None:
        self.assertTrue(LAUNCHER.exists())
        self.assertIn("Open the Lantern local chat shell", self.launcher)
        self.assertIn("webbrowser.open", self.launcher)
        self.assertIn("CHAT_SHELL", self.launcher)
        self.assertIn("no command execution, no agents, no tunnels, no public writes", self.launcher)
        for blocked in [
            "subprocess.run",
            "subprocess.Popen",
            "os.system",
            "Flask(",
            "app.run",
            "requests.",
            "http.server",
        ]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.launcher)

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
        self.assertIn("static local page only", result.stdout)


if __name__ == "__main__":
    unittest.main()
