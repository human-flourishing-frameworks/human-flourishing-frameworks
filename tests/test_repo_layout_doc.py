"""Test that repo layout documentation contains key phrases."""

import unittest
from pathlib import Path


class TestRepoLayoutDoc(unittest.TestCase):
    def test_repo_layout_doc_exists(self):
        """docs/repo-layout.md should exist."""
        doc_path = Path(__file__).parent.parent / "docs" / "repo-layout.md"
        self.assertTrue(doc_path.exists(), "docs/repo-layout.md should exist")

    def test_repo_layout_doc_contains_key_phrases(self):
        """docs/repo-layout.md should contain key structural phrases."""
        doc_path = Path(__file__).parent.parent / "docs" / "repo-layout.md"
        content = doc_path.read_text()

        required_phrases = [
            "Top-Level Modules",
            "Namespaced Packages",
            "src/bettersafe/",
            "tests/__init__.py",
            "PYTHONPATH=src",
            "pip install -e .",
        ]

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content, f"docs/repo-layout.md should contain '{phrase}'")


if __name__ == "__main__":
    unittest.main()
