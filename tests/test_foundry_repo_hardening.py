import unittest
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


if __name__ == "__main__":
    unittest.main()
