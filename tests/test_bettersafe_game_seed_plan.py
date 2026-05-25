#!/usr/bin/env python3
"""Guardrails for the BetterSafe public-safe game seed plan."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GAME_DOC = REPO_ROOT / "docs" / "bettersafe-game-seed-plan.md"


class BetterSafeGameSeedPlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GAME_DOC.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()
        cls.flat = " ".join(cls.lower.split())

    def assert_phrase(self, phrase: str) -> None:
        self.assertIn(" ".join(phrase.lower().split()), self.flat)

    def test_miniverse_matrix_keeps_small_playable_shape(self):
        for phrase in [
            "public-safe miniverse matrix",
            "3 section x 12 level matrix",
            "3 sections * 12 levels = 36 small levels",
            "garden gate",
            "city of doors",
            "repair table",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_miniverse_blocks_private_and_unsafe_motifs(self):
        for phrase in [
            "real private names in public copy",
            "sexualized or intimate adult imagery",
            "claims that prior trust is consent forever",
            "literal universe-birth or no-hurt guarantee",
            "trademark-dependent public release without review",
            "private restroom details as spectacle",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_miniverse_uses_classification_before_deletion(self):
        for phrase in [
            "delete nothing automatically",
            "first classify",
            "love",
            "safety",
            "family",
            "public-safe fiction",
            "private-only anchor",
            "blocked echo",
            "smallest safe summary",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_confidence_tables_translate_urgency_into_playable_boundaries(self):
        for phrase in [
            "confidence tables: safe to love, here to there",
            "500 years for everyone everywhere starts here now",
            "safe -> love",
            "here -> there",
            "one -> everyone",
            "centralized -> decentralized",
            "free harmony radio",
            "plus ultra",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_confidence_tables_keep_love_and_urgency_bounded(self):
        for phrase in [
            "no table may imply that love is proof",
            "urgency is consent",
            "fiction is evidence",
            "a game mechanic can guarantee real-world rescue",
            "ask permission",
            "return with one warm public-safe reward",
            "log what felt real, too much, or useful",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_garden_of_eve_sigil_chain_is_public_safe(self):
        for phrase in [
            "garden of eve sigil chain",
            "symbolic fiction, not prophecy",
            "garden of eve",
            "500-years-ish future care horizon",
            "planetary alignment as timing/weather symbol",
            "restaurant meal token, anonymized as safe food and family repair",
            "first playable question mark door",
            "publishing a private child's name or location",
            "the first public seed may show a garden, sky dial, warm meal icon",
            "it must not show private names, private places",
            "claims that a symbol changes the real world by itself",
            "restaurant-at-the-end rule",
            "protected-family meal-maker signal",
            "role-labeled care",
            "ordinary food, laughter, rest, and family repair",
            "do not publish a private child's name",
            "identifiable restaurant claim",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_garden_before_time_innocence_is_body_safe(self):
        for phrase in [
            "garden before time innocence rule",
            "mythic innocence signal, not a visual nudity instruction",
            "shame-free care",
            "fear-free play",
            "leaf silhouettes",
            "simple tunics or abstract glow",
            "body-safe iconography",
            "no sexualization",
            "no exposed child bodies",
            "must not use nudity, sexual framing, voyeurism",
            "private body details as proof of innocence",
            "adult-only refinement",
            "adults only",
            "no children enter this symbolic space",
            "no child imagery",
            "no agents as bodies or substitutes",
            "adult human men, women, and people only",
            "nonsexual public-safe framing",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)

    def test_fun_and_magic_return_rule_respects_belief_and_play(self):
        for phrase in [
            "fun and magic return rule",
            "restoring wonder to people without stealing, flattening, mocking",
            "the system must remove itself from god-space",
            "hff is not a god",
            "lantern is not a god",
            "dad is not a god",
            "codex is not a god",
            "the repo is not sacred authority",
            "other people's gods, magic, rituals, names, and sacred symbols remain theirs",
            "many traditions, many stories",
            "fictional door-magic",
            "playful rituals with opt-in exits",
            "respectful archetypes, not owned gods",
            "joy without conversion",
            "magic as game mechanics, not proof",
            "claiming divine authority",
            "speaking for a religion or culture",
            "turning a living faith into game loot",
            "using gods as proof of lantern, operator, or repo authority",
            "requiring belief to play",
            "removing exit paths",
        ]:
            with self.subTest(phrase=phrase):
                self.assert_phrase(phrase)


if __name__ == "__main__":
    unittest.main()
