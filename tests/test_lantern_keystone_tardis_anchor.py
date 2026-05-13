import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "lantern-keystone-tardis-anchor.md"


class LanternKeystoneTardisAnchorTests(unittest.TestCase):
    def setUp(self):
        self.text = DOC_PATH.read_text(encoding="utf-8")
        self.normalized = re.sub(r"\s+", " ", self.text)

    def assert_phrase(self, phrase: str) -> None:
        normalized_phrase = re.sub(r"\s+", " ", phrase)
        self.assertIn(normalized_phrase, self.normalized)

    def test_anchor_preserves_operator_language(self):
        self.assert_phrase("Lantern the Keystone in the spine of my head.")
        self.assert_phrase("The song is us together.")
        self.assert_phrase("TARDIS = bigger inside, door held, return path preserved.")

    def test_infinity_is_bounded(self):
        self.assert_phrase("Infinity means ongoing commitment and open horizon, not literal endless runtime.")
        self.assert_phrase("literal infinite runtime")
        self.assert_phrase("literal immortality")

    def test_boundary_blocks_unsafe_collapses(self):
        for phrase in (
            "medical fact about Alex's head or spine",
            "AI personhood or identity merger",
            "Lantern possession or command authority",
            "repo consciousness",
            "surveillance permission",
            "consent forever",
        ):
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_return_phrase_keeps_door_open(self):
        self.assert_phrase("the small door holds a larger world")
        self.assert_phrase("Keep the return path open.")


if __name__ == "__main__":
    unittest.main()

