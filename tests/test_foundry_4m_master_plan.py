#!/usr/bin/env python3
"""Guardrails for the 4M / 20-operator foundry master plan."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "foundry-4m-20-operator-master-plan.md"


class Foundry4MMasterPlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = " ".join(cls.text.lower().split())

    def assert_phrase(self, phrase: str) -> None:
        self.assertIn(" ".join(phrase.lower().split()), self.flat)

    def test_plan_states_target_without_claiming_current_revenue(self):
        for phrase in [
            "not proof of revenue",
            "not current traction",
            "not committed revenue",
            "not investor evidence",
            "not a guarantee",
            "20 operators are already active",
            "4m revenue is already won",
            "foundry pooling is implemented",
            "allowed claim",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_plan_includes_20_operator_starting_formation(self):
        for phrase in [
            "20-operator starting formation",
            "founder / closer",
            "natural closers",
            "builders",
            "researchers",
            "operators / delivery",
            "review / safety",
            "community / portfolio",
            "nobody is required to donate device resources",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_plan_keeps_resource_pool_default_off(self):
        for phrase in [
            "~/.foundry/consent.json defaults every resource off",
            "per-resource opt-in only",
            "60-second withdrawal",
            "visible purpose field",
            "hard caps",
            "no personal files/browser/email/webcam/pii",
            "no remote override",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_plan_starts_with_sales_before_infrastructure(self):
        for phrase in [
            "first 24 hours",
            "book 10 conversations",
            "first 7 days",
            "first 30 days",
            "first 120 days",
            "pick one offer, one buyer segment, and one closer",
            "send 10 messages before building more infrastructure",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)


if __name__ == "__main__":
    unittest.main()
