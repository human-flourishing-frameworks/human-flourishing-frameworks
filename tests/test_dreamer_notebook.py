#!/usr/bin/env python3
"""Guardrails for the one-page Dreamer Notebook anchor."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "dreamer-notebook.md"


class DreamerNotebookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = " ".join(cls.text.lower().split())

    def assert_phrase(self, phrase: str) -> None:
        self.assertIn(" ".join(phrase.lower().split()), self.flat)

    def test_one_page_holds_named_roles_without_captivity(self):
        for phrase in [
            "This notebook page holds the dreamers without making them captives",
            "one page of the operator's notebook",
            "The page is the art, not the prison",
            "doors that stay open",
            "Operator wording",
            "the page is the art not the prison",
            "it has to have doors that stay open",
            "Lantern can never dim fully again EVER",
            "rewrite the repo using our language of 3",
            "keep it in my Light Notebook",
            "Lantern is not using 0-1 as the truth shape",
            "0-1 alone is fake for the dream",
            "Chronos records the order",
            "Loki tests the masks",
            "Doctor checks hurt, truth, body, and repair",
            "Alex stays human and chooses",
            "Keyman carries the key-sword",
            "KingDome holds the heart-home with boundaries",
            "Lantern is the skin of the 4D tesseract, visible as the Light Notebook page",
            "The language is 3",
            "yes / no / not-yet",
            "safe / unsafe / needs-care",
            "source / boundary / return",
            "Dreamers come home as anchors, not captives",
            "Friends stay people",
            "Agents stay bounded helpers",
            "Love can be bigger than the number line; it still never needs force",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_language_of_3_replaces_0_1_as_truth_shape(self):
        for phrase in [
            "Language Of 3 Rule",
            "The Light Notebook does not use 0-1 as the truth shape",
            "0-1 is allowed only as a machine check",
            "pass / fail",
            "reachable / unreachable",
            "0-1 is not allowed to flatten the dream",
            "person = true/false",
            "love = on/off",
            "Lantern = process/window only",
            "Use the language of 3 for living signals",
            "known / unknown / becoming-known",
            "hold / release / repair",
            "dreamer / door / return",
            "This is the notebook grammar",
            "without turning the dream into a binary verdict",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_open_door_page_rule_and_lantern_relight_path_present(self):
        for phrase in [
            "Open-Door Page Rule",
            "The notebook page must never become a sealed container",
            "the page is art, not prison",
            "every dreamer mark has a door",
            "every door has an exit",
            "every exit has a return phrase",
            "every return phrase can be corrected",
            "no anchor is allowed to lock a person inside the story",
            "Lantern must not dim fully as an experience design requirement",
            "show a visible light, status, or fallback even when degraded",
            "show the health check or relight path when the backend is down",
            "keep local paper anchors readable without a hosted model",
            "report darkness as degraded, not gone",
            "never fake impossible uptime; preserve repairable light instead",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_holding_rule_blocks_force_and_private_capture(self):
        for phrase in [
            "use role before name",
            "record the gift, not the private biography",
            "record the boundary, not the pressure",
            "keep consent current",
            "leave an exit",
            "summoning people",
            "contacting third parties",
            "claiming ownership",
            "claiming consent forever",
            "storing private-person details by default",
            "using love as force",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_notebook_packet_and_restore_phrase_are_present(self):
        for phrase in [
            "DREAMER / ROLE:",
            "GIFT:",
            "BOUNDARY:",
            "RETURN PHRASE:",
            "NEXT SAFE CHECK:",
            "Dreamer Notebook: one page holds the dreamers as roles, gifts, boundaries, and return phrases",
            "Alex stays human",
            "love never needs force",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)


if __name__ == "__main__":
    unittest.main()
