#!/usr/bin/env python3
"""BetterSafe Social Services — eligibility matching (local only).

High-stakes care + benefits is a fail-closed domain: it is never acceptable to
emit a confident "you are eligible" when the data needed to decide is missing.
This module evaluates each eligibility rule INDEPENDENTLY and returns a per-rule
evidence trail — [criterion, required, observed, source, status] — and ABSTAINS
(``insufficient_evidence``) on any decisive rule whose inputs are missing, rather
than silently skipping it (the prior ``_score_match`` behaviour) or guessing.

A recommendation is only ``eligible`` when every decisive rule conclusively
PASSES. One failing decisive rule → ``ineligible``. Any abstaining decisive rule
(and no outright failure) → ``insufficient_evidence`` (surfaced to a human),
never ``eligible``.
"""

import logging
import json

logger = logging.getLogger('BetterSafe.SocialServices')

# Per-rule outcomes
PASS = "pass"
FAIL = "fail"
INSUFFICIENT = "insufficient_evidence"

# Overall decisions
ELIGIBLE = "eligible"
INELIGIBLE = "ineligible"
NEEDS_REVIEW = "insufficient_evidence"

# Service-registry column indices (social_services_registry; see bettersafe_db.py)
_COL_ID, _COL_NAME, _COL_CATEGORY, _COL_COUNTY, _COL_CITY = 0, 1, 2, 3, 4
_COL_PHONE, _COL_WEBSITE, _COL_CRITERIA, _COL_PROGRAMS = 5, 6, 7, 8


class SocialServicesEligibility:
    """Match users to eligible social services with an auditable evidence trail."""

    def __init__(self, db, config):
        self.db = db
        self.config = config
        logger.info("Social Services Eligibility initialized")

    # ── public API ────────────────────────────────────────────────────────────
    def find_eligible_services(self, user_profile):
        """Return services the user is conclusively eligible for.

        Each entry carries the full per-rule evidence trail + a confidence score.
        Services that ABSTAIN (insufficient evidence) are excluded here and made
        available separately via :meth:`evaluate_all` so a human can resolve them.
        """
        eligible = []
        for service in self._active_services():
            result = self.evaluate_eligibility(user_profile, service)
            if result['decision'] == ELIGIBLE:
                eligible.append(result)
        logger.info("Found %d conclusively-eligible services for user", len(eligible))
        return eligible

    def evaluate_all(self, user_profile):
        """Evaluate every active service; return the full decision + evidence for
        each, including ineligible and needs-review cases (for a reviewer UI)."""
        return [self.evaluate_eligibility(user_profile, s) for s in self._active_services()]

    def evaluate_eligibility(self, user_profile, service):
        """Evaluate one service and return a citation-bearing decision.

        Returns a dict::

            {
              service_id, service_name, category, phone, website, programs,
              decision: eligible | ineligible | insufficient_evidence,
              confidence: float,                 # share of decisive rules with conclusive evidence
              rules: [ {rule, status, required, observed, source, rationale} ],
              abstentions: [rule, ...],
              summary: str,
            }
        """
        try:
            criteria = json.loads(service[_COL_CRITERIA]) if service[_COL_CRITERIA] else {}
        except (ValueError, TypeError):
            criteria = {}

        source = f"social_services_registry#{service[_COL_ID]} ({service[_COL_NAME]})"
        rules = []

        # Age — lower / upper bounds
        if criteria.get('age_min') is not None:
            rules.append(self._rule_numeric_min(
                'age >= age_min', user_profile.get('age'), criteria['age_min'], source, 'age'))
        if criteria.get('age_max') is not None:
            rules.append(self._rule_numeric_max(
                'age <= age_max', user_profile.get('age'), criteria['age_max'], source, 'age'))

        # Income — only decide against a real threshold; abstain if the registry
        # says income-based but supplies no threshold (we don't invent one).
        if criteria.get('income_based'):
            rules.append(self._rule_income(user_profile, criteria, source))

        # County residency — the service's county is the requirement.
        service_county = service[_COL_COUNTY]
        if service_county:
            rules.append(self._rule_equals(
                'county == service.county', user_profile.get('county'), service_county, source, 'county'))

        # Disability requirement
        if criteria.get('disability_required'):
            rules.append(self._rule_bool(
                'disability required', user_profile.get('disability'), source, 'disability'))

        return self._decide(service, rules, source)

    # ── per-rule evaluators (each returns an evidence dict) ──────────────────────
    @staticmethod
    def _evidence(rule, status, required, observed, source, rationale):
        return {'rule': rule, 'status': status, 'required': required,
                'observed': observed, 'source': source, 'rationale': rationale}

    def _rule_numeric_min(self, rule, observed, required, source, field):
        if observed is None:
            return self._evidence(rule, INSUFFICIENT, f">= {required}", None, source,
                                  f"user profile is missing '{field}' — cannot decide, abstaining")
        ok = observed >= required
        return self._evidence(rule, PASS if ok else FAIL, f">= {required}", observed, source,
                              f"{field}={observed} {'meets' if ok else 'below'} minimum {required}")

    def _rule_numeric_max(self, rule, observed, required, source, field):
        if observed is None:
            return self._evidence(rule, INSUFFICIENT, f"<= {required}", None, source,
                                  f"user profile is missing '{field}' — cannot decide, abstaining")
        ok = observed <= required
        return self._evidence(rule, PASS if ok else FAIL, f"<= {required}", observed, source,
                              f"{field}={observed} {'within' if ok else 'above'} maximum {required}")

    def _rule_equals(self, rule, observed, required, source, field):
        if observed is None:
            return self._evidence(rule, INSUFFICIENT, required, None, source,
                                  f"user profile is missing '{field}' — cannot decide, abstaining")
        ok = observed == required
        return self._evidence(rule, PASS if ok else FAIL, required, observed, source,
                              f"{field}={observed!r} {'matches' if ok else 'does not match'} {required!r}")

    def _rule_bool(self, rule, observed, source, field):
        if observed is None:
            return self._evidence(rule, INSUFFICIENT, True, None, source,
                                  f"user profile is missing '{field}' — cannot decide, abstaining")
        ok = bool(observed)
        return self._evidence(rule, PASS if ok else FAIL, True, observed, source,
                              f"{field}={observed} {'satisfies' if ok else 'fails'} requirement")

    def _rule_income(self, user_profile, criteria, source):
        threshold = criteria.get('income_max')
        observed = user_profile.get('income_annual')
        if threshold is None:
            return self._evidence('income <= income_max', INSUFFICIENT, 'income_max (unset)', observed, source,
                                  "service is income-based but the registry has no income_max threshold — "
                                  "abstaining rather than assuming one")
        if observed is None:
            return self._evidence('income <= income_max', INSUFFICIENT, f"<= {threshold}", None, source,
                                  "user profile is missing 'income_annual' — cannot decide, abstaining")
        ok = observed <= threshold
        return self._evidence('income <= income_max', PASS if ok else FAIL, f"<= {threshold}", observed, source,
                              f"income_annual={observed} {'within' if ok else 'above'} threshold {threshold}")

    # ── aggregation (fail-closed) ───────────────────────────────────────────────
    def _decide(self, service, rules, source):
        statuses = [r['status'] for r in rules]
        abstentions = [r['rule'] for r in rules if r['status'] == INSUFFICIENT]
        passed = sum(1 for s in statuses if s == PASS)
        conclusive = sum(1 for s in statuses if s in (PASS, FAIL))
        total = len(rules)

        if not rules:
            # No criteria to check at all → we cannot assert eligibility.
            decision = NEEDS_REVIEW
            summary = "no eligibility criteria on record — needs human review"
        elif FAIL in statuses:
            decision = INELIGIBLE
            failed = [r['rule'] for r in rules if r['status'] == FAIL]
            summary = f"ineligible — failed: {', '.join(failed)}"
        elif abstentions:
            decision = NEEDS_REVIEW  # fail-closed: never 'eligible' with an open question
            summary = f"insufficient evidence — abstained on: {', '.join(abstentions)}"
        else:
            decision = ELIGIBLE
            summary = f"eligible — all {total} decisive rule(s) passed"

        confidence = round(conclusive / total, 3) if total else 0.0

        try:
            programs = json.loads(service[_COL_PROGRAMS]) if service[_COL_PROGRAMS] else []
        except (ValueError, TypeError):
            programs = []

        return {
            'service_id': service[_COL_ID],
            'service_name': service[_COL_NAME],
            'category': service[_COL_CATEGORY],
            'phone': service[_COL_PHONE],
            'website': service[_COL_WEBSITE],
            'programs': programs,
            'decision': decision,
            'confidence': confidence,
            'match_score': passed,  # backward-compatible: count of passed criteria
            'rules': rules,
            'abstentions': abstentions,
            'summary': summary,
            'source': source,
        }

    # ── helpers / unchanged API ─────────────────────────────────────────────────
    def _active_services(self):
        self.db.cursor.execute('SELECT * FROM social_services_registry WHERE is_active = 1')
        return self.db.cursor.fetchall()

    def get_service_by_id(self, service_id):
        """Get details for a specific service."""
        return self.db.get_by_id('social_services_registry', service_id)

    def get_all_services(self, county=None, category=None):
        """Get all services, optionally filtered."""
        services = self._active_services()
        if county:
            services = [s for s in services if s[_COL_COUNTY] == county]
        if category:
            services = [s for s in services if s[_COL_CATEGORY] == category]
        return services
