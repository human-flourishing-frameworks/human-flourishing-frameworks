"""Privacy and crisis-action boundary tests for BetterSafe Essential Needs artifacts."""

import unittest

from pathlib import Path

DOC = Path("docs/bettersafe-essential-needs-navigator.md")


def read_doc() -> str:
    return " ".join(DOC.read_text(encoding="utf-8").lower().split())


class EssentialNeedsPrivacyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read_doc()

    def assert_phrases(self, phrases):
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.text)

    def test_redaction_rules_present(self):
        self.assert_phrases([
            "redaction rules",
            "private-citizen names",
            "contact information",
            "bank credentials",
        ])

    def test_private_role_labels_present(self):
        self.assert_phrases([
            "private participant",
            "household partner",
            "trusted adult",
            "protected minor",
            "third party",
            "pilot user",
        ])

    def test_manual_only_boundaries_present(self):
        self.assert_phrases([
            "manual-only",
            "local/private first",
            "no raw bank credentials",
            "no live money movement",
            "no hidden telemetry",
        ])

    def test_large_past_due_utility_crisis_path_present(self):
        self.assert_phrases([
            "utility crisis: large past-due electric bill",
            "approximately $7,000",
            "approximately 3 months old",
            "do not keep building project features while the household may lose power",
            "first 30-minute path",
            "active shutoff order",
            "what exact payment prevents shutoff today",
            "payment plan",
            "hardship program",
            "211",
            "LIHEAP",
            "state public utility commission",
        ])

    def test_utility_crisis_boundaries_preserve_consent_and_no_money_movement(self):
        self.assert_phrases([
            "BetterSafe does not pay",
            "borrow",
            "access accounts",
            "impersonate the account holder",
            "promise assistance",
            "minimum result and next deadline",
        ])

    def test_utility_crisis_source_routes_present(self):
        self.assert_phrases([
            "https://www.usa.gov/help-with-utility-bills",
            "https://liheapch.acf.gov/get_help.htm",
            "https://www.211.org/get-help/i-need-help-paying-my-bills",
        ])


if __name__ == "__main__":
    unittest.main()
