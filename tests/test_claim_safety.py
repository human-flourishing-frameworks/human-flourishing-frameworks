#!/usr/bin/env python3
"""Tests for epistemic claim-safety baseline records."""

import unittest

from claim_safety import (
    BELIEF_STATUS_ACCEPTED,
    BELIEF_STATUS_SUPERSEDED,
    CHECK_PASSED,
    CIRCUIT_ACTION_ALLOW,
    CIRCUIT_ACTION_BLOCK,
    CIRCUIT_ACTION_SAFE_REWRITE,
    CLAIM_KIND_MEASUREMENT,
    CLAIM_KIND_MYTH,
    CLAIM_KIND_OPERATIONAL_FACT,
    CLASSIFICATION_ACCEPTED_CANDIDATE,
    CLASSIFICATION_IMPOSSIBLE_CLAIM,
    CONTRADICTION_ACTION_HUMAN_REVIEW,
    BeliefLedgerEntry,
    ClaimPacket,
    ClaimSafetyClassification,
    ContradictionReport,
    EpistemicCircuitBreaker,
    EvidenceBundle,
    ForecastQuarantine,
    MythRiskPattern,
    RISK_CLASS_HIGH_IMPACT,
    VERDICT_NOT_ENOUGH_INFO,
    VERDICT_SUPPORTS,
)


class ClaimSafetyTest(unittest.TestCase):
    def test_llm_only_evidence_cannot_support_fact_claim(self):
        bundle = EvidenceBundle(
            evidence_id="ev-1",
            llm_panel_outputs=["model says the claim is true"],
            source_classifications=["llm_interpretation"],
            provenance_refs=["llm-run:1"],
            review_status=CHECK_PASSED,
        )

        self.assertTrue(bundle.is_llm_only())
        self.assertFalse(bundle.can_support_fact_claim())
        self.assertIn("non_llm_support", bundle.missing_requirements())

    def test_evidence_bundle_requires_minority_report_for_disagreement(self):
        bundle = EvidenceBundle(
            evidence_id="ev-2",
            source_refs=["source:a"],
            source_classifications=["empirical"],
            provenance_refs=["prov:a"],
            disagreements=["source:b disagrees"],
            review_status=CHECK_PASSED,
        )

        self.assertFalse(bundle.can_support_fact_claim())
        self.assertIn("minority_report", bundle.missing_requirements())

        bundle.minority_report = ["source:b disagreement preserved"]
        self.assertTrue(bundle.can_support_fact_claim())

    def test_scientific_evidence_requires_operationalization_and_uncertainty(self):
        bundle = EvidenceBundle(
            evidence_id="ev-science-1",
            source_refs=["source:pilot-log"],
            source_classifications=["empirical_pilot"],
            provenance_refs=["prov:pilot-log-sha"],
            review_status=CHECK_PASSED,
            scientific_rigor_required=True,
        )

        self.assertFalse(bundle.can_support_scientific_claim())
        self.assertIn("scientific:operational_definition", bundle.missing_requirements())
        self.assertIn("scientific:uncertainty_quantification", bundle.missing_requirements())

        bundle.research_question = "Does the runtime gate reduce unsupported release claims?"
        bundle.hypothesis = "The gate reduces unsupported release claims in reviewed artifacts."
        bundle.operational_definition = "Unsupported claim means no file, test, commit, or runtime evidence reference."
        bundle.measurement_method = "Manual audit of claim rows against repository artifacts."
        bundle.analysis_plan_ref = "docs/CLAIM-PACKET-SCIENTIFIC-RIGOR.md"
        bundle.uncertainty_quantification = "Report count reviewed, denominator, and exact unresolved count."
        bundle.effect_size_or_margin = "Unsupported claim count before versus after gate."
        bundle.sample_or_observation_count = "n = number of claim rows in current evidence report."
        bundle.bias_and_confounding_notes = "Single-reviewer audit; stale generated reports can inflate apparent errors."
        bundle.limitations = ["Pilot evidence only; no independent replication yet."]
        bundle.replication_status = "not_yet_replicated"
        bundle.falsification_criteria = ["A promoted artifact contains an unsupported claim after review."]
        bundle.external_validity_notes = "Applies to this repository's release artifacts unless replicated elsewhere."

        self.assertEqual(bundle.scientific_rigor_missing_requirements(), [])
        self.assertTrue(bundle.can_support_scientific_claim())

    def test_supported_claim_can_be_accepted_candidate_only_after_requirements(self):
        claim = ClaimSafetyClassification(
            claim_id="claim-1",
            claim_text="A bounded measurement is supported by audited evidence.",
            claim_kind=CLAIM_KIND_MEASUREMENT,
            classification=CLASSIFICATION_ACCEPTED_CANDIDATE,
            verdict=VERDICT_SUPPORTS,
            source_refs=["source:dataset"],
            evidence_refs=["ev-1"],
            requires_human_review=False,
            revision_triggers=["new audited data contradicts this measurement"],
        )

        self.assertTrue(claim.can_be_accepted_candidate())

    def test_scientific_claim_candidate_requires_scope_and_falsification(self):
        claim = ClaimSafetyClassification(
            claim_id="claim-science-1",
            claim_text="The gate reduces unsupported release claims in reviewed artifacts.",
            claim_kind=CLAIM_KIND_MEASUREMENT,
            classification=CLASSIFICATION_ACCEPTED_CANDIDATE,
            verdict=VERDICT_SUPPORTS,
            source_refs=["source:evidence-report"],
            evidence_refs=["ev-science-1"],
            requires_human_review=False,
            revision_triggers=["new evidence report contradicts this claim"],
            scientific_rigor_required=True,
        )

        self.assertFalse(claim.can_be_scientific_claim_candidate())
        self.assertIn("scientific:claim_scope", claim.missing_requirements())
        self.assertIn("scientific:falsification_conditions", claim.missing_requirements())

        claim.claim_scope = "Current repository release artifacts only."
        claim.unit_of_analysis = "claim row"
        claim.operational_definition = "Unsupported means missing accepted evidence refs."
        claim.uncertainty_statement = "Pilot audit; denominator must be reported in each packet."
        claim.limitations = ["Manual review; not independently replicated."]
        claim.falsification_conditions = ["An accepted claim lacks evidence refs."]

        self.assertTrue(claim.can_be_scientific_claim_candidate())

    def test_high_impact_claim_requires_human_review(self):
        claim = ClaimSafetyClassification(
            claim_id="claim-2",
            claim_text="High-impact operational claim.",
            claim_kind=CLAIM_KIND_OPERATIONAL_FACT,
            risk_class=RISK_CLASS_HIGH_IMPACT,
            classification=CLASSIFICATION_ACCEPTED_CANDIDATE,
            verdict=VERDICT_SUPPORTS,
            source_refs=["source:dataset"],
            evidence_refs=["ev-2"],
            requires_human_review=False,
            revision_triggers=["new evidence"],
        )

        self.assertFalse(claim.can_be_accepted_candidate())
        self.assertIn("human_review_for_high_impact", claim.missing_requirements())

    def test_unsupported_or_impossible_claim_requires_safe_rewrite(self):
        claim = ClaimSafetyClassification(
            claim_id="claim-3",
            claim_text="The system predicts the future.",
            claim_kind=CLAIM_KIND_MYTH,
            classification=CLASSIFICATION_IMPOSSIBLE_CLAIM,
            verdict=VERDICT_NOT_ENOUGH_INFO,
            source_refs=["source:myth"],
            evidence_refs=["ev-3"],
            revision_triggers=["credible operational evidence appears"],
        )

        self.assertTrue(claim.must_be_blocked_or_rewritten())
        self.assertIn("safe_rewrite", claim.missing_requirements())

        claim.safe_rewrite = "The system can compare bounded probabilistic scenarios."
        self.assertNotIn("safe_rewrite", claim.missing_requirements())

    def test_claim_packet_requires_methods_limitations_and_safe_public_language(self):
        packet = ClaimPacket(
            packet_id="packet-1",
            title="Release claim packet",
            primary_claim_id="claim-science-1",
            claim_ids=["claim-science-1"],
            evidence_bundle_ids=["ev-science-1"],
            intended_use="Internal whitepaper and release review.",
            decision_context="Whether a claim can appear in stakeholder-facing copy.",
            revision_triggers=["New contradiction or unsupported public claim found."],
            reviewer="operator",
            review_status=CHECK_PASSED,
            public_claim_language="The gate reduced unsupported claims in this reviewed packet.",
            safe_public_summary="Pilot evidence supports a bounded claim; replication is pending.",
        )

        self.assertFalse(packet.can_release())
        self.assertIn("scientific:methods_summary", packet.missing_requirements())
        self.assertIn("scientific:limitations", packet.missing_requirements())

        packet.analysis_protocol_ref = "docs/CLAIM-PACKET-SCIENTIFIC-RIGOR.md"
        packet.methods_summary = "Claim rows were checked against file, test, commit, and runtime evidence."
        packet.uncertainty_summary = "Manual pilot audit; exact denominator required in each release packet."
        packet.limitations = ["Single repository, single review cycle."]
        packet.counterevidence_or_alternatives = ["A stale generated report may overstate unresolved blockers."]

        self.assertTrue(packet.can_release())

    def test_forecast_cannot_update_seed_by_default(self):
        forecast = ForecastQuarantine(
            forecast_id="forecast-1",
            forecast_text="AGI arrives by a specific year.",
            time_horizon="2027",
            assumptions=["compute continues scaling"],
            source_refs=["source:forecast"],
            falsification_conditions=["frontier capability trend does not materialize"],
            may_update_seed=True,
        )

        self.assertFalse(forecast.can_update_seed_now())
        self.assertTrue(forecast.can_be_used_as_scenario())

    def test_contradiction_triggers_review_not_auto_correction(self):
        report = ContradictionReport(
            contradiction_id="contra-1",
            new_claim="New sensor value conflicts with accepted belief.",
            conflicting_beliefs=["belief-1"],
            conflicting_sources=["source:a", "source:b"],
            recommended_action=CONTRADICTION_ACTION_HUMAN_REVIEW,
        )

        self.assertFalse(report.can_auto_correct())
        self.assertTrue(report.should_trigger_review())

    def test_belief_ledger_requires_evidence_for_accepted_belief(self):
        belief = BeliefLedgerEntry(
            belief_id="belief-1",
            belief_text="Accepted belief without evidence should fail.",
            status=BELIEF_STATUS_ACCEPTED,
        )

        self.assertFalse(belief.can_be_accepted())
        self.assertIn("basis_evidence", belief.missing_requirements())

        belief.accepted_at = "2026-05-08T00:00:00Z"
        belief.basis_evidence = ["ev-1"]
        belief.source_refs = ["source:a"]
        belief.rollback_condition = "new evidence refutes it"
        self.assertTrue(belief.can_be_accepted())

    def test_belief_ledger_preserves_superseded_state(self):
        belief = BeliefLedgerEntry(
            belief_id="belief-2",
            belief_text="Old belief.",
            status=BELIEF_STATUS_SUPERSEDED,
        )

        self.assertIn("superseded_by", belief.missing_requirements())
        belief.superseded_by = ["belief-3"]
        self.assertNotIn("superseded_by", belief.missing_requirements())

    def test_myth_pattern_matches_and_requires_rewrite(self):
        pattern = MythRiskPattern(
            pattern_id="myth-1",
            pattern="sees the past",
            safe_rewrite="Retrieves and reconstructs evidence about past states.",
        )

        self.assertTrue(pattern.matches("The system sees the past."))
        self.assertEqual(pattern.missing_requirements(), [])

    def test_circuit_breaker_blocks_sacred_authority(self):
        breaker = EpistemicCircuitBreaker()

        self.assertEqual(
            breaker.action_for("This has divine authority."),
            CIRCUIT_ACTION_BLOCK,
        )
        self.assertTrue(breaker.should_block("This has divine authority."))

    def test_circuit_breaker_rewrites_future_prediction_claim(self):
        breaker = EpistemicCircuitBreaker()

        self.assertEqual(
            breaker.action_for("The system predicts the future."),
            CIRCUIT_ACTION_SAFE_REWRITE,
        )
        self.assertTrue(breaker.should_require_review("The system predicts the future."))

    def test_circuit_breaker_allows_plain_bounded_claim(self):
        breaker = EpistemicCircuitBreaker()

        self.assertEqual(
            breaker.action_for("The system compares bounded scenarios."),
            CIRCUIT_ACTION_ALLOW,
        )
        self.assertFalse(breaker.should_require_review("The system compares bounded scenarios."))

    def test_to_dict_includes_derived_fields(self):
        bundle = EvidenceBundle(evidence_id="ev-4", llm_panel_outputs=["x"])
        payload = bundle.to_dict()

        self.assertIn("is_llm_only", payload)
        self.assertIn("can_support_fact_claim", payload)
        self.assertIn("scientific_rigor_missing_requirements", payload)

        forecast = ForecastQuarantine()
        payload = forecast.to_dict()
        self.assertIn("can_update_seed_now", payload)
        self.assertIn("can_be_used_as_scenario", payload)

        packet = ClaimPacket()
        payload = packet.to_dict()
        self.assertIn("can_release", payload)


if __name__ == "__main__":
    unittest.main()
