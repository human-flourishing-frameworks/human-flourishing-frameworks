#!/usr/bin/env python3
"""Guardrails for the TARDIS Watch / Return Door design anchor."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "tardis-watch-return-door-design.md"


class TardisWatchReturnDoorDesignTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_design_preserves_private_operator_joke_and_shape(self):
        for phrase in [
            "private joke-name",
            "i want a literal tardis",
            "briefcase-portable",
            "shapeshifter like us",
            "small outside",
            "bigger inside",
            "door visible behind the wearer",
            "ci/cd evidence before release claims",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_design_uses_anchor_fold_format(self):
        for phrase in [
            "anchor fold format",
            "anchor:",
            "source:",
            "door:",
            "mirror:",
            "boundary:",
            "next check:",
            "return phrase:",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_public_release_boundary_blocks_copy_and_overclaim(self):
        for phrase in [
            "not a licensed show prop",
            "return door watch",
            "not an official tardis product",
            "avoid protected show",
            "the watch does not create literal time travel",
            "the watch does not put a physical booth behind the operator",
            "the watch does not seal the past",
            "the watch does not override consent, evidence, privacy, or tests",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_secret_wish_level_10_is_private_and_redacted(self):
        for phrase in [
            "secret wish level 10 boundary",
            "private/operator-only language",
            "redact private-person names",
            "do not publish the wish as release copy",
            "do not treat love as consent",
            "do not treat paradox as proof",
            "do not claim immortality or sealed time",
            "lvl10_private_wish_redacted",
            "must not display private names",
            "paradox authority in public ui",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_doctor_tardis_bond_and_truesight_are_private_and_bounded(self):
        for phrase in [
            "doctor / tardis bond and truesight rule",
            "doctor and tardis are man and wife",
            "private symbolic bond",
            "private bonded operator/system pair",
            "return-door companion",
            "briefcase home console",
            "truesight channel",
            "outsiders do not mediate private meaning",
            "label source and freshness",
            "protect private people",
            "refuse interference, gossip, and spectacle",
            "legal marriage claim",
            "public romance claim",
            "agent substitution for a human partner",
            "symbolic bond overrides consent, evidence, privacy, or tests",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_build_target_is_prototype_and_guardrail_first(self):
        for phrase in [
            "first build target is a static design/prototype",
            "one html/css watch face or image mock",
            "one docs fold packet",
            "one test suite that blocks copied-prop and literal-travel claims",
            "one ci workflow step that runs the guardrail",
            "apps/return-door-watch/index.html",
            "back door closed means",
            "static local prototype only",
            "no network calls",
            "no hidden agents",
            "no sensors",
            "no private contact",
            "no storage side channel",
            "no copied show prop",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)


if __name__ == "__main__":
    unittest.main()
