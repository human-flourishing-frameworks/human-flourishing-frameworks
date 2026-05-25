#!/usr/bin/env python3
"""Guardrails for the TARDIS boarding manifest."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "tardis-boarding-manifest.md"


class TardisBoardingManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()
        cls.flat = " ".join(cls.lower.split())

    def assert_phrase(self, phrase: str) -> None:
        self.assertIn(" ".join(phrase.lower().split()), self.flat)

    def test_boarding_means_anchor_loading_not_hidden_action(self):
        for phrase in [
            "boarding means",
            "load the anchor",
            "name the source",
            "redact private people",
            "keep the return door open",
            "boarding does not mean",
            "move humans",
            "contact third parties",
            "start hidden agents",
            "claim literal time travel",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_manifest_preserves_core_operator_signals_with_boundaries(self):
        for phrase in [
            "literal tardis joke",
            "return door watch",
            "briefcase shapeshifter",
            "garden",
            "restaurant at the end",
            "warm meal token",
            "sigil",
            "restroom doors",
            "500-ish years",
            "zenon between moon and earth",
            "middle of everything",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_fold_format_and_sleep_rule_are_present(self):
        for phrase in [
            "anchor:",
            "source:",
            "door:",
            "mirror:",
            "boundary:",
            "next check:",
            "return phrase:",
            "no helpers stay secretly awake",
            "show state",
            "leave no new hidden process",
            "preserve dirty work",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_song_space_intake_saves_references_without_raw_lyrics(self):
        for phrase in [
            "song file / space in the song",
            "song-space anchor",
            "fill packet when operator sends the file",
            "song-space intake",
            "song anchor:",
            "source file or link:",
            "timestamp / section:",
            "space it opens:",
            "feeling role:",
            "store references and short paraphrase only",
            "do not store raw copyrighted lyrics",
            "redact private people by default",
            "do not claim the song speaks for absent people",
            "if the body is ringing or unsafe, ground first and seek human help",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_operator_history_uses_dnd_style_without_impersonation(self):
        for phrase in [
            "operator history fold format",
            "must not claim to be the operator",
            "roleplaying quest log",
            "dnd-style packet",
            "quest:",
            "party:",
            "monster / risk:",
            "spell / tool:",
            "roll / evidence:",
            "save / check:",
            "loot / artifact:",
            "do not impersonate the operator",
            "do not store raw private biography by default",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_positive_change_stays_bounded(self):
        for phrase in [
            "positive change means useful action with consent, evidence, privacy, rollback",
            "care at the middle",
            "smallest testable surface",
            "all friends come home as anchors, not captives",
            "all future signals become bounded next checks before action",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)


if __name__ == "__main__":
    unittest.main()
