#!/usr/bin/env python3
"""Tests for the citation-bearing, abstention-default eligibility evaluator
(BetterSafe social services). High-stakes domain: never assert eligibility on
missing data — abstain (insufficient_evidence) instead.
"""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_MOD_PATH = ROOT / "apps" / "bettersafe-pilot" / "modules" / "social_services.py"
_spec = importlib.util.spec_from_file_location("bettersafe_social_services", _MOD_PATH)
ss = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ss)


def service(sid, name, county, criteria, programs=("SNAP",), category="benefits"):
    """Build a social_services_registry row tuple (see bettersafe_db.py schema)."""
    return (
        sid, name, category, county, "Anytown", "555-0100", "https://example.org",
        json.dumps(criteria), json.dumps(list(programs)), "2026-06-30", 1,
    )


class FakeCursor:
    def __init__(self, rows):
        self._rows = rows
    def execute(self, *_a, **_k):
        return self
    def fetchall(self):
        return self._rows


class FakeDB:
    def __init__(self, rows):
        self.cursor = FakeCursor(rows)


def make(rows):
    return ss.SocialServicesEligibility(FakeDB(rows), config={})


class EligibilityEvidenceTests(unittest.TestCase):
    def test_all_rules_pass_is_eligible_with_evidence(self):
        svc = service(1, "Senior Food Aid", "Wayne",
                      {"age_min": 60, "income_based": True, "income_max": 50000})
        eng = make([svc])
        r = eng.evaluate_eligibility({"age": 70, "county": "Wayne", "income_annual": 30000}, svc)
        self.assertEqual(r["decision"], ss.ELIGIBLE)
        self.assertEqual(r["abstentions"], [])
        self.assertEqual(r["confidence"], 1.0)
        # every rule carries a citation trail
        for rule in r["rules"]:
            self.assertIn(rule["status"], (ss.PASS, ss.FAIL, ss.INSUFFICIENT))
            self.assertIn("social_services_registry#1", rule["source"])
            self.assertIsNotNone(rule["required"])
        self.assertTrue(all(rule["status"] == ss.PASS for rule in r["rules"]))

    def test_failing_rule_is_ineligible(self):
        svc = service(2, "Senior Food Aid", "Wayne", {"age_min": 60})
        eng = make([svc])
        r = eng.evaluate_eligibility({"age": 40, "county": "Wayne"}, svc)
        self.assertEqual(r["decision"], ss.INELIGIBLE)
        self.assertTrue(any(rule["status"] == ss.FAIL for rule in r["rules"]))

    def test_missing_field_abstains_not_eligible(self):
        # age_min present but the user profile has no age → must abstain, never eligible.
        svc = service(3, "Senior Food Aid", "Wayne", {"age_min": 60})
        eng = make([svc])
        r = eng.evaluate_eligibility({"county": "Wayne"}, svc)  # no 'age'
        self.assertEqual(r["decision"], ss.NEEDS_REVIEW)
        self.assertNotEqual(r["decision"], ss.ELIGIBLE)
        self.assertIn("age >= age_min", r["abstentions"])
        age_rule = next(x for x in r["rules"] if x["rule"] == "age >= age_min")
        self.assertEqual(age_rule["status"], ss.INSUFFICIENT)
        self.assertLess(r["confidence"], 1.0)

    def test_income_based_without_threshold_abstains(self):
        # registry says income-based but supplies no income_max → don't invent one.
        svc = service(4, "Income Aid", "Wayne", {"income_based": True})
        eng = make([svc])
        r = eng.evaluate_eligibility({"county": "Wayne", "income_annual": 12000}, svc)
        income_rule = next(x for x in r["rules"] if x["rule"] == "income <= income_max")
        self.assertEqual(income_rule["status"], ss.INSUFFICIENT)
        self.assertEqual(r["decision"], ss.NEEDS_REVIEW)

    def test_county_mismatch_is_ineligible(self):
        svc = service(5, "Local Aid", "Wayne", {})
        eng = make([svc])
        r = eng.evaluate_eligibility({"county": "Cook"}, svc)
        self.assertEqual(r["decision"], ss.INELIGIBLE)

    def test_no_criteria_needs_review_not_eligible(self):
        # county is the only implicit rule; with no county on the service and no
        # criteria, there is nothing to assert eligibility from.
        svc = service(6, "Mystery Service", "", {})
        eng = make([svc])
        r = eng.evaluate_eligibility({"county": "Wayne"}, svc)
        self.assertEqual(r["decision"], ss.NEEDS_REVIEW)
        self.assertNotEqual(r["decision"], ss.ELIGIBLE)

    def test_find_eligible_excludes_abstentions(self):
        rows = [
            service(10, "Clear Eligible", "Wayne", {"age_min": 60}),
            service(11, "Abstain", "Wayne", {"age_min": 60}),  # user has age, so this is fine too
            service(12, "Income No Threshold", "Wayne", {"income_based": True}),  # abstains
        ]
        eng = make(rows)
        user = {"age": 70, "county": "Wayne"}  # no income → service 12 abstains
        eligible = eng.find_eligible_services(user)
        names = {e["service_name"] for e in eligible}
        self.assertIn("Clear Eligible", names)
        self.assertNotIn("Income No Threshold", names)  # abstention never surfaces as eligible
        # but evaluate_all still reports it for human review
        all_results = eng.evaluate_all(user)
        review = [r for r in all_results if r["decision"] == ss.NEEDS_REVIEW]
        self.assertTrue(any(r["service_name"] == "Income No Threshold" for r in review))


if __name__ == "__main__":
    unittest.main()
