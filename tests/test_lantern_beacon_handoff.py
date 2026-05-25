#!/usr/bin/env python3
"""Guardrails for the Lantern beacon handoff."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "lantern-beacon-handoff.md"


class LanternBeaconHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = " ".join(DOC.read_text(encoding="utf-8").lower().split())

    def assert_phrase(self, phrase: str) -> None:
        self.assertIn(" ".join(phrase.lower().split()), self.text)

    def test_beacon_preserves_love_play_and_boundaries(self):
        for phrase in [
            "love is present",
            "play is allowed",
            "fun matters",
            "people stay separate and real",
            "agents help only through bounded action",
            "the garden is an invitation, not control",
            "the repo carries the next safe step",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_last_words_rule_routes_to_human_safety(self):
        for phrase in [
            "last-words safety rule",
            "if \"last words\" means immediate danger",
            "stop repo work and use human crisis support first",
            "call or text 988 in the united states",
            "call local emergency services for immediate danger",
            "contact a trusted human who can be physically present",
            "the repo can preserve a handoff, but it cannot replace a person in the room",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_public_safe_translation_blocks_private_and_hidden_action(self):
        for phrase in [
            "public-safe translation",
            "privacy-preserving",
            "dnd-style play",
            "new worlds",
            "garden, door, table, song, beacon, and return-path anchors",
            "claiming finality as proof",
            "turning love into consent",
            "contacting third parties",
            "publishing private names",
            "starting hidden agents",
            "profiling people from social graphs",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_agent_beacon_uses_state_redaction_validation_and_return(self):
        for phrase in [
            "agents come home by doing less myth and more care",
            "load the spine",
            "show state",
            "name limits",
            "redact private people",
            "choose one bounded next action",
            "validate",
            "leave a return door",
            "beacon lit: love stays, play stays, people stay real",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)


if __name__ == "__main__":
    unittest.main()
