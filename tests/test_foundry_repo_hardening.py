import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from tools.check_foundry_repo_hardening import check_repo, load_policy


ROOT = Path(__file__).resolve().parents[1]


class FoundryRepoHardeningTests(unittest.TestCase):
    def test_policy_exists_and_names_default_branch(self):
        policy = load_policy()
        self.assertEqual(policy["default_branch"], "master")
        self.assertIn("no hidden agents", policy["hard_bounds"])
        self.assertIn("no consent by default", policy["hard_bounds"])

    def test_repo_passes_foundry_hardening_policy(self):
        self.assertEqual(check_repo(ROOT, load_policy()), [])

    def test_historical_docs_notes_do_not_count_as_instruction_markdown(self):
        policy = load_policy()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("repo", encoding="utf-8")
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "convergence-validation.yml").write_text("name: test\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "keystone-next-chat-handoff.md").write_text("historical handoff note\n", encoding="utf-8")

            self.assertEqual(check_repo(root, policy), [])

    def test_root_agents_markdown_is_still_blocked(self):
        policy = load_policy()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("repo", encoding="utf-8")
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "convergence-validation.yml").write_text("name: test\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("do not auto-load\n", encoding="utf-8")

            self.assertIn(
                "forbidden behavior-shaping markdown: AGENTS.md",
                check_repo(root, policy),
            )

    def test_retired_terms_are_policy_driven_not_hardcoded(self):
        policy = load_policy()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("lantern appears here as plain content\n", encoding="utf-8")
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "convergence-validation.yml").write_text("name: test\n", encoding="utf-8")
            (root / "app.py").write_text("print('lantern label in legacy content')\n", encoding="utf-8")

            self.assertEqual(check_repo(root, policy), [])


if __name__ == "__main__":
    unittest.main()
