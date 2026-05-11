import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BetterSafeDataCenterAnchorTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def assert_contains_phrase(self, text: str, phrase: str) -> None:
        normalized_text = re.sub(r"\s+", " ", text)
        normalized_phrase = re.sub(r"\s+", " ", phrase)
        self.assertIn(normalized_phrase, normalized_text)

    def test_anchor_locks_physical_infrastructure_truth(self):
        doc = self.read("docs/bettersafe-data-center-physical-infrastructure-anchor.md")
        required_phrases = [
            "Digital systems are not weightless.",
            "servers",
            "storage systems",
            "fiber connections",
            "cooling systems",
            "backup power",
            "buildings",
            "land",
            "electricity",
            "water or cooling resources",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assert_contains_phrase(doc, phrase)

    def test_anchor_requires_data_minimization_and_non_computer_paths(self):
        doc = self.read("docs/bettersafe-data-center-physical-infrastructure-anchor.md")
        required_phrases = [
            "data goes somewhere",
            "storage has cost",
            "network access is unequal",
            "data minimization",
            "offline-capable checklists where practical",
            "no-computer paths for public benefits, documents, voting, care, and access work",
            "small evidence records instead of broad private-data consolidation",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assert_contains_phrase(doc, phrase)

    def test_anchor_blocks_over_collection_and_cloud_abstraction(self):
        doc = self.read("docs/bettersafe-data-center-physical-infrastructure-anchor.md")
        required_phrases = [
            "collecting data because it might be useful later",
            "hiding physical infrastructure cost behind cloud language",
            "assuming every participant can use online-only systems",
            "claiming public blockchain makes private data safe",
            "building features that require raw personal histories by default",
            "turning every interaction into a durable record",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assert_contains_phrase(doc, phrase)

    def test_anchor_has_feature_review_checklist(self):
        doc = self.read("docs/bettersafe-data-center-physical-infrastructure-anchor.md")
        required_phrases = [
            "What data does this create?",
            "Is the data private, identifying, high-impact, or linkable?",
            "Can the same goal be met with less data?",
            "Can the user proceed without a computer or stable internet?",
            "Can the evidence be kept local or minimal?",
            "Does the feature create a public-chain, permanent, or hard-to-delete record?",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assert_contains_phrase(doc, phrase)

    def test_anchor_preserves_scope_boundary(self):
        doc = self.read("docs/bettersafe-data-center-physical-infrastructure-anchor.md")
        required_phrases = [
            "This anchor does not claim the screenshot is a complete technical assessment of data centers.",
            "digital systems depend on physical infrastructure",
            "minimize private data",
            "preserve non-computer paths",
            "real-world resource and access costs",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assert_contains_phrase(doc, phrase)


if __name__ == "__main__":
    unittest.main()
