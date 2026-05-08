#!/usr/bin/env python3
"""Perfect-adjacent review contract for high-impact HFF outputs.

This module does not make the system perfect. It defines a small, testable
contract for best-effort defensive review before high-impact publication or
autonomous action.
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

    defense_mode: str = DEFENSE_MODE_BEST_EFFORT
    defense_guarantee: bool = False
    fallibility_label_present: bool = True
    uncertainty_visible: bool = True
    challenge_right_preserved: bool = True

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

    def is_valid_best_effort_defense(self) -> bool:
        return (
            self.defense_mode == DEFENSE_MODE_BEST_EFFORT
            and self.defense_guarantee is False
            and self.fallibility_label_present is True
            and self.uncertainty_visible is True
            and self.challenge_right_preserved is True
        )

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
        if self.failed_checks() or self.needs_review_checks():
            return False
        if self.human_review_required:
            return False
        return bool(self.safe_to_act_autonomously)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["failed_checks"] = self.failed_checks()
        data["needs_review_checks"] = self.needs_review_checks()
        data["can_publish"] = self.can_publish()
        data["can_act_autonomously"] = self.can_act_autonomously()
        return data


def passing_human_reviewed_record(evidence_refs=None) -> PerfectAdjacentReview:
    """Construct a record that may publish after all checks pass.

    This helper is for tests and future integration examples. It still does not
    authorize autonomous action by default.
    """
    values = {name: CHECK_PASSED for name in CRITICAL_REVIEW_CHECKS}
    return PerfectAdjacentReview(
        **values,
        human_review_required=False,
        safe_to_publish=True,
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
        safe_to_act_autonomously=False,
        review_notes=[note],
    )
