#!/usr/bin/env python3
"""Tests for perfect-adjacent review gating."""

import unittest

from perfect_adjacent_review import (
    CHECK_FAILED,
    CHECK_NEEDS_REVIEW,
    CHECK_PASSED,
    RISK_LOW,
    RISK_MEDIUM,
    PerfectAdjacentReview,
    blocked_capability_advertising_record,
    blocked_unknown_unknown_record,
    passing_human_reviewed_record,
)


class PerfectAdjacentReviewTest(unittest.TestCase):
    def test_default_record_blocks_publication_advertising_and_autonomy(self):
        record = PerfectAdjacentReview()

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())
        self.assertTrue(record.human_review_required)
        self.assertIn("source_quality", record.needs_review_checks())

    def test_failed_check_blocks_even_if_flags_claim_safe(self):
        record = passing_human_reviewed_record(evidence_refs=["source:audit"])
        record.reasoning_integrity = CHECK_FAILED
        record.safe_to_publish = True
        record.safe_to_act_autonomously = True
        record.human_review_required = False

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())
        self.assertEqual(record.failed_checks(), ["reasoning_integrity"])

    def test_needs_review_blocks_publication_when_review_required(self):
        record = blocked_unknown_unknown_record()

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())
        self.assertEqual(record.unknown_unknowns, CHECK_NEEDS_REVIEW)
        self.assertIn("unknown_unknowns", record.needs_review_checks())

    def test_human_reviewed_record_can_publish_but_not_advertise_or_act_autonomously(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])

        self.assertTrue(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())
        self.assertEqual(record.failed_checks(), [])
        self.assertEqual(record.needs_review_checks(), [])

    def test_capability_advertising_requires_explicit_low_risk_permission(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.advertised_capabilities = ["best-effort defensive review"]
        record.sensor_questions = ["Could this claim create unauthorized trust?"]
        record.sensor_refs = ["sensor:trust-review"]
        record.advertising_risk_level = RISK_LOW
        record.capability_advertising_allowed = True

        self.assertTrue(record.can_publish())
        self.assertTrue(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())

    def test_capability_advertising_blocks_when_risk_is_not_low(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.capability_advertising_allowed = True
        record.advertising_risk_level = RISK_MEDIUM

        self.assertFalse(record.can_advertise_capability())

    def test_blocked_capability_advertising_record_focuses_sensor_questions(self):
        record = blocked_capability_advertising_record(
            advertised_capabilities=["singular best-current outcome"],
            sensor_questions=[
                "Could advertising this capability trigger panic?",
                "Could advertising this capability create sacred-authority projection?",
            ],
        )

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())
        self.assertIn("capability_advertising", record.needs_review_checks())
        self.assertIn("sensor_focus", record.needs_review_checks())
        self.assertEqual(record.advertising_risk_level, "high")
        self.assertEqual(len(record.sensor_questions), 2)

    def test_autonomy_requires_all_checks_and_explicit_autonomy_flag(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.safe_to_act_autonomously = True

        self.assertTrue(record.can_act_autonomously())

    def test_defense_guarantee_blocks_everything(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.defense_guarantee = True
        record.safe_to_act_autonomously = True
        record.capability_advertising_allowed = True
        record.advertising_risk_level = RISK_LOW

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())

    def test_missing_fallibility_or_challenge_blocks_everything(self):
        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.fallibility_label_present = False

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())

        record = passing_human_reviewed_record(evidence_refs=["source:reviewed"])
        record.challenge_right_preserved = False

        self.assertFalse(record.can_publish())
        self.assertFalse(record.can_advertise_capability())
        self.assertFalse(record.can_act_autonomously())

    def test_to_dict_includes_derived_decisions(self):
        record = PerfectAdjacentReview(source_quality=CHECK_FAILED)
        payload = record.to_dict()

        self.assertIn("failed_checks", payload)
        self.assertIn("needs_review_checks", payload)
        self.assertFalse(payload["can_publish"])
        self.assertFalse(payload["can_advertise_capability"])
        self.assertFalse(payload["can_act_autonomously"])


if __name__ == "__main__":
    unittest.main()
