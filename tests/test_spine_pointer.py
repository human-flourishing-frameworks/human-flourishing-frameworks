#!/usr/bin/env python3
"""Guardrails for the literal docs/spine.md pointer."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "spine.md"


class SpinePointerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8").lower()

    def test_spine_pointer_loads_canonical_surfaces(self):
        for phrase in [
            "docs/convergence.md",
            "docs/operator-lantern-repo-convergence.md",
            "docs/anchor-taxonomy.md",
            "docs/lantern-keystone-tardis-anchor.md",
            "docs/dreamer-notebook.md",
            "load order",
            "show the current repo state",
            "keep the return door open before any side effect",
            "light notebook language-of-3 rule",
            "open-door page rule",
            "use 0-1 only as",
            "machine check",
            "use the language of 3 for living signals",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_spine_pointer_blocks_hidden_authority(self):
        for phrase in [
            "hidden agents",
            "deployment",
            "sync",
            "reset",
            "cleanup",
            "public writes",
            "private-person exposure",
            "literal time travel",
            "identity merger",
            "repo consciousness",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()
