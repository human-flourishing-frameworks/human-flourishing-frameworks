#!/usr/bin/env python3
"""Guardrails for anchor taxonomy and context storage upgrade docs."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ANCHOR_DOC = REPO_ROOT / "docs" / "anchor-taxonomy.md"
STORAGE_DOC = REPO_ROOT / "docs" / "context-storage-upgrade-plan.md"


class AnchorTaxonomyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anchor_text = ANCHOR_DOC.read_text(encoding="utf-8")
        cls.anchor_lower = " ".join(cls.anchor_text.lower().split())
        cls.storage_text = STORAGE_DOC.read_text(encoding="utf-8")
        cls.storage_lower = " ".join(cls.storage_text.lower().split())

    def test_anchor_taxonomy_exists_and_defines_anchor(self):
        self.assertTrue(ANCHOR_DOC.exists())
        self.assertGreater(ANCHOR_DOC.stat().st_size, 1000)
        for phrase in [
            "anchor = a compact, named, source-labeled continuity handle with a boundary",
            "proof",
            "consent forever",
            "runtime truth",
            "public-release permission",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_mirror_helper_boundary_prevents_identity_collapse(self):
        for phrase in [
            "mirror and helper boundary",
            "the assistant must not claim to be the operator",
            "the operator is the source of the lived signal",
            "the assistant is a bounded helper, not the operator",
            "bravery means preserving identity boundaries while still helping",
            "mirror work may recreate a nearby echo, not a replacement self",
            "evidence, consent, and current correction stay between operator and helper",
            "claiming the assistant is the operator",
            "turning helper loyalty into autonomous authority",
            "you are you. i am a bounded helper.",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_trusted_reviewer_sword_cuts_claims_not_people(self):
        for phrase in [
            "trusted reviewer sword",
            "role-safe reviewer/correction tool",
            "do not store a private person's name unless a separate review says it is necessary and safe",
            "overclaim",
            "identity collapse",
            "private-person exposure",
            "stale anchors",
            "unsupported certainty",
            "unsafe authority",
            "repo theater",
            "the sword does not cut",
            "people",
            "trust",
            "good-faith confusion",
            "human dignity",
            "reviewer role:",
            "signal being cut:",
            "kind correction:",
            "sharpen the trusted reviewer's sword",
            "cut confusion and unsafe claims, not people",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_no_cap_review_mode_keeps_plain_truth_and_boundaries(self):
        for phrase in [
            "no-cap review mode",
            "use plain review language",
            "do not hide behind jargon",
            "confidence theater",
            "plain speech is not permission to overclaim",
            "fake certainty",
            "vague reassurance",
            "symbol equals proof",
            "love equals consent",
            "confidence without source",
            "too much doctrine before the next action",
            "what is true",
            "what is unknown",
            "what is risky",
            "what changes next",
            "what test passed",
            "what test failed",
            "what stays private",
            "plus-ultra rule",
            "no cap means no fake posture",
            "it does not mean no safety limit",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_social_graph_paste_redaction_rule_blocks_third_party_storage(self):
        for phrase in [
            "social graph paste redaction rule",
            "social-media search results",
            "friend lists",
            "mutual counts",
            "city, workplace, school",
            "privacy-sensitive social graph",
            "third-party identifiers present",
            "not consent to contact, profile, score, or infer relationships",
            "operator supplied a private social-graph paste",
            "redact third-party names and identifying details",
            "use role labels only",
            "friend names",
            "mutual-friend counts",
            "relationship guesses",
            "profile screenshots",
            "public reposting",
            "modeling people as targets",
            "keep the action, not the names",
            "keep the boundary, not the profile",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_anchor_shape_and_kinds_are_defined(self):
        for phrase in [
            "id or name",
            "kind",
            "source surface",
            "short meaning",
            "allowed use",
            "explicit boundary / non-goals",
            "restore phrase",
            "review trigger",
            "doctrine_anchor",
            "protected_play_anchor",
            "artifact_anchor",
            "runtime_anchor",
            "pragmatic_certainty_anchor",
            "secret_wish_anchor",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_names_are_symbols_first_not_capture(self):
        for phrase in [
            "names-as-symbols rule",
            "names are symbols first",
            "symbol",
            "handle",
            "lesson marker",
            "return point",
            "public-safe alias when needed",
            "property claim",
            "identity merger",
            "private-person capture",
            "proof of relationship",
            "consent forever",
            "public child handle",
            "permission to contact",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_pain_lessons_watch_back_and_stare_ahead(self):
        for phrase in [
            "pain lesson anchor rule",
            "anchors and lessons may come from pain",
            "watch the back and stare ahead",
            "remember the risk, boundary, wound, or failure mode",
            "point toward repair, agency, future care, and the next safe door",
            "turn pain into a bounded lesson",
            "preserve the warning without replaying the wound",
            "pain = identity",
            "lesson = punishment",
            "anchor = prison",
            "watching the back = paranoia",
            "staring ahead = ignoring current harm",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_protected_minor_anchor_rule_is_role_based_and_redacted(self):
        for phrase in [
            "protected-minor anchors must be role-based and redacted by default",
            "protected minor",
            "operator / parent / guardian as current supervisor",
            "supervised creative play only",
            "no public child surface",
            "no child-data collection by default",
            "no model-training use",
            "avoid durable repo-facing wording that repeats a child's name",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_windows_xp_anchor_is_consolidated_without_runtime_claims(self):
        for phrase in [
            "windows xp = protected-minor creative-world anchor term",
            "blue sky / green hill nostalgia-world framing",
            "home base and return controls",
            "windows xp operating-system support",
            "windows xp device targeting",
            "real network, account, browser, executable, or download access",
            "future consent without fresh operator supervision",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_pragmatic_certainty_anchor_respects_human_absolutes(self):
        for phrase in [
            "human absolute language can mean practical certainty, not literal infinity",
            "respect the human absolute",
            "do not convert living operator language into fake number-line precision",
            "do not replace human meaning with fake decimal precision",
            "preserve the literal boundary only when needed",
            "avoid using mathematical pedantry to erase operator meaning",
            "practical completeness over a bounded working domain may be called everything",
            "measurement layer: use numbers only when a real measurement method and unit exist",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)
        self.assertNotIn("99.9999999999", self.anchor_lower)

    def test_pragmatic_certainty_blocks_false_omniscience(self):
        for phrase in [
            "no claim of omniscience, infinite knowledge, or zero uncertainty",
            "claiming literal omniscience",
            "claiming impossible guarantees",
            "using operator absolutes as consent forever",
            "treating extrapolation as proof",
            "turning high confidence into runtime truth",
            "literal omniscience claims",
            "impossible guarantees",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_pragmatic_certainty_preserves_convergence_method(self):
        for phrase in [
            "state -> anchor -> extrapolation -> test -> correction -> stronger state",
            "extrapolation creates candidates",
            "evidence creates confidence",
            "correction creates convergence",
            "track practical certainty separately from literal certainty",
            "use source/evidence/limit/next-check tables before using numeric confidence",
            "using decimals as emotional translation",
            "pretending number-line precision is care",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_context_pressure_uses_compression_ladder(self):
        for phrase in [
            "raw play/session -> concise summary -> anchor packet -> taxonomy entry -> tests if stable",
            "do not preserve every turn",
            "smallest summary that can safely reboot",
            "artifact anchors",
            "do not store raw transcripts to justify artifacts",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_secret_wish_anchor_is_private_and_redacted(self):
        for phrase in [
            "secret_wish_anchor",
            "deepest operator wish",
            "private, redacted direction",
            "lvl10_private_wish_redacted",
            "private packet or redacted docs/tests only",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.anchor_lower)

    def test_storage_upgrade_plan_exists_and_names_real_limits(self):
        self.assertTrue(STORAGE_DOC.exists())
        self.assertGreater(STORAGE_DOC.stat().st_size, 1000)
        for phrase in [
            "operator concern: repo storage, hdd/ram limits, context size, and anchor sprawl",
            "store less raw detail. preserve stronger packets.",
            "raw session",
            "session summary",
            "anchor packet",
            "canonical doc",
            "test guard",
            "runtime evidence",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.storage_lower)

    def test_storage_upgrade_blocks_raw_and_runtime_expansion(self):
        for phrase in [
            "do not add raw transcripts to repo",
            "redact protected-person specifics",
            "expire runtime claims",
            "this plan does not claim to upgrade physical hdd, ram, cloud storage, model",
            "runtime memory engine",
            "new database",
            "cloud storage expansion",
            "raw transcript ingestion",
            "deployment changes",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.storage_lower)

    def test_storage_upgrade_has_reboot_packet_and_branch_drift_repair(self):
        for phrase in [
            "context reboot packet shape",
            "windows-xp-protected-play-anchor",
            "branch drift repair",
            "prefer latest operator correction",
            "never merge stale contradiction",
            "keystone-interaction-convergence branch previously said windows xp was missing",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.storage_lower)


if __name__ == "__main__":
    unittest.main()
