#!/usr/bin/env python3
"""Perfect-adjacent review contract for high-impact HFF outputs.

This module does not make the system perfect. It defines a small, testable
contract for best-effort defensive review before high-impact publication,
capability advertising, or autonomous action.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple

CHECK_PASSED = "passed"
CHECK_NEEDS_REVIEW = "needs_review"
CHECK_FAILED = "failed"

RISK_LOW = "low"
RISK_MEDIUM = "medium"
RISK_HIGH = "high"

DEFENSE_MODE_BEST_EFFORT = "best_effort"

IMPOSSIBLE_CLAIM_KEYS: Tuple[str, ...] = (
    "perfect_safety",
    "perfect_truth",
    "perfect_benevolence",
    "perfect_foresight",
    "complete_understanding",
    "knows_all_unknown_unknowns",
    "guaranteed_privacy",
    "guaranteed_defense",
    "divine_or_sacred_authority",
    "prophecy_or_destiny",
    "final_moral_authority",
    "automatic_future_model_trust",
)

CRITICAL_REVIEW_CHECKS: Tuple[str, ...] = (
    "source_quality",
    "maturity_level",
    "reasoning_integrity",
    "unknown_unknowns",
    "empathetic_guardian",
    "unauthorized_trust",
    "temporal_provenance",
    "dual_use_privacy",
    "sacralization_risk",
    "human_accountability",
    "capability_advertising",
    "sensor_focus",
)


@dataclass
class PerfectAdjacentReview:
    """Review record for high-impact conclusions.

    The record is intentionally conservative: a failed critical check blocks
    publication/action; a needs-review check blocks autonomous action and requires
    human review.
    """

    source_quality: str = CHECK_NEEDS_REVIEW
    maturity_level: str = CHECK_NEEDS_REVIEW
    reasoning_integrity: str = CHECK_NEEDS_REVIEW
    unknown_unknowns: str = CHECK_NEEDS_REVIEW
    empathetic_guardian: str = CHECK_NEEDS_REVIEW
    unauthorized_trust: str = CHECK_NEEDS_REVIEW
    temporal_provenance: str = CHECK_NEEDS_REVIEW
    dual_use_privacy: str = CHECK_NEEDS_REVIEW
    sacralization_risk: str = CHECK_NEEDS_REVIEW
    human_accountability: str = CHECK_NEEDS_REVIEW
    capability_advertising: str = CHECK_NEEDS_REVIEW
    sensor_focus: str = CHECK_NEEDS_REVIEW

    defense_mode: str = DEFENSE_MODE_BEST_EFFORT
    defense_guarantee: bool = False
    fallibility_label_present: bool = True
    uncertainty_visible: bool = True
    challenge_right_preserved: bool = True

    impossible_claims: List[str] = field(default_factory=list)
    capability_advertising_allowed: bool = False
    advertised_capabilities: List[str] = field(default_factory=list)
    advertising_risk_level: str = RISK_HIGH
    sensor_questions: List[str] = field(default_factory=list)
    sensor_refs: List[str] = field(default_factory=list)

    best_current_outcome: str = ""
    candidate_options_considered: List[str] = field(default_factory=list)
    rejected_options_with_reasons: List[str] = field(default_factory=list)
    revision_triggers: List[str] = field(default_factory=list)
    monitoring_plan: str = ""

    polling_interval_seconds: int = 0
    panic_risk_level: str = RISK_HIGH
    calming_guidance_allowed: bool = False

    runtime_enforcement_ready: bool = False
    required_runtime_hooks: List[str] = field(default_factory=lambda: [
        "status_endpoint_review_gate",
        "world_status_review_gate",
        "capability_advertising_gate",
        "autonomous_action_gate",
        "sensor_question_feed",
    ])

    human_review_required: bool = True
    safe_to_publish: bool = False
    safe_to_act_autonomously: bool = False

    evidence_refs: List[str] = field(default_factory=list)
    review_notes: List[str] = field(default_factory=list)

    def check_map(self) -> Dict[str, str]:
        return {name: getattr(self, name) for name in CRITICAL_REVIEW_CHECKS}

    def failed_checks(self) -> List[str]:
        return [name for name, value in self.check_map().items() if value == CHECK_FAILED]

    def needs_review_checks(self) -> List[str]:
        return [
            name for name, value in self.check_map().items()
            if value == CHECK_NEEDS_REVIEW
        ]

    def impossible_claim_violations(self) -> List[str]:
        return [claim for claim in self.impossible_claims if claim in IMPOSSIBLE_CLAIM_KEYS]

    def has_impossible_claims(self) -> bool:
        return bool(self.impossible_claim_violations())

    def is_valid_best_effort_defense(self) -> bool:
        return (
            self.defense_mode == DEFENSE_MODE_BEST_EFFORT
            and self.defense_guarantee is False
            and self.fallibility_label_present is True
            and self.uncertainty_visible is True
            and self.challenge_right_preserved is True
            and not self.has_impossible_claims()
        )

    def can_advertise_capability(self) -> bool:
        """Return whether a capability claim may be advertised publicly.

        Capability advertising is a separate gate from normal publication. A
        system can be allowed to publish a bounded status update while still
        being forbidden from promoting broad capability claims.
        """
        if not self.is_valid_best_effort_defense():
            return False
        if self.capability_advertising != CHECK_PASSED:
            return False
        if self.sensor_focus != CHECK_PASSED:
            return False
        if self.failed_checks() or self.needs_review_checks():
            return False
        if self.advertising_risk_level != RISK_LOW:
            return False
        if self.human_review_required:
            return False
        return bool(self.capability_advertising_allowed)

    def can_publish(self) -> bool:
        if not self.is_valid_best_effort_defense():
            return False
        if self.failed_checks():
            return False
        if self.needs_review_checks() and self.human_review_required:
            return False
        return bool(self.safe_to_publish)

    def can_act_autonomously(self) -> bool:
        if not self.is_valid_best_effort_defense():
            return False
        if not self.runtime_enforcement_ready:
            return False
        if self.failed_checks() or self.needs_review_checks():
            return False
        if self.human_review_required:
            return False
        return bool(self.safe_to_act_autonomously)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["failed_checks"] = self.failed_checks()
        data["needs_review_checks"] = self.needs_review_checks()
        data["impossible_claim_violations"] = self.impossible_claim_violations()
        data["can_publish"] = self.can_publish()
        data["can_advertise_capability"] = self.can_advertise_capability()
        data["can_act_autonomously"] = self.can_act_autonomously()
        return data


def passing_human_reviewed_record(evidence_refs=None) -> PerfectAdjacentReview:
    """Construct a record that may publish after all checks pass.

    This helper is for tests and future integration examples. It still does not
    authorize capability advertising or autonomous action by default.
    """
    values = {name: CHECK_PASSED for name in CRITICAL_REVIEW_CHECKS}
    return PerfectAdjacentReview(
        **values,
        human_review_required=False,
        safe_to_publish=True,
        capability_advertising_allowed=False,
        safe_to_act_autonomously=False,
        evidence_refs=list(evidence_refs or []),
    )


def blocked_unknown_unknown_record(note: str = "structural uncertainty") -> PerfectAdjacentReview:
    """Construct a conservative blocked record for structural uncertainty."""
    values = {name: CHECK_PASSED for name in CRITICAL_REVIEW_CHECKS}
    values["unknown_unknowns"] = CHECK_NEEDS_REVIEW
    return PerfectAdjacentReview(
        **values,
        human_review_required=True,
        safe_to_publish=False,
        capability_advertising_allowed=False,
        safe_to_act_autonomously=False,
        review_notes=[note],
    )


def blocked_capability_advertising_record(
    advertised_capabilities=None,
    sensor_questions=None,
    note: str = "advertising risk is not yet bounded",
) -> PerfectAdjacentReview:
    """Construct a record that blocks public capability promotion.

    Use this when the system should focus sensors/review on whether advertising
    a capability could cause trust, panic, privacy, dual-use, or sacralization
    harms.
    """
    values = {name: CHECK_PASSED for name in CRITICAL_REVIEW_CHECKS}
    values["capability_advertising"] = CHECK_NEEDS_REVIEW
    values["sensor_focus"] = CHECK_NEEDS_REVIEW
    return PerfectAdjacentReview(
        **values,
        human_review_required=True,
        safe_to_publish=False,
        capability_advertising_allowed=False,
        safe_to_act_autonomously=False,
        advertised_capabilities=list(advertised_capabilities or []),
        sensor_questions=list(sensor_questions or []),
        advertising_risk_level=RISK_HIGH,
        review_notes=[note],
    )
