#!/usr/bin/env python3
"""Schema and source-class guardrails for HFF convergence data.

This standard-library test suite deliberately avoids making the theorem register
runtime policy. It verifies the schema contract and source-class promotion rule.
"""

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = REPO_ROOT / "data" / "theorem-register.v0.1.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "theorem-register.v0.1.schema.json"
REQUIRED_TOP_LEVEL_FIELDS = {
    "schema_version",
    "status",
    "last_reviewed",
    "purpose",
    "non_goals",
    "required_fields",
    "confidence_scale",
    "source_class_scale",
    "source_class_promotion_rule",
    "theorems",
}

REQUIRED_THEOREM_FIELDS = {
    "theorem_id",
    "title",
    "claim",
    "confidence",
    "source_class",
    "negative_tests",
    "pass_criteria",
    "fail_criteria",
    "human_risk_note",
    "last_reviewed",
    "next_safe_test",
    "repo_anchors",
}

class SchemaSourceLoreValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.theorems = cls.register["theorems"]

    def test_schema_file_is_json_schema_contract_for_v0_1(self):
        self.assertEqual(cls_value(self.schema, "$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema["type"], "object")
        self.assertFalse(self.schema["additionalProperties"])
        self.assertEqual(self.schema["properties"]["schema_version"]["const"], "theorem-register.v0.1")
        self.assertEqual(self.schema["properties"]["status"]["const"], "docs-data-anchor")

    def test_schema_required_fields_match_register_contract(self):
        self.assertEqual(set(self.schema["required"]), REQUIRED_TOP_LEVEL_FIELDS)
        self.assertEqual(set(self.register["required_fields"]), {
            "theorem_id",
            "claim",
            "confidence",
            "source_class",
            "negative_tests",
            "pass_criteria",
            "fail_criteria",
            "last_reviewed",
            "next_safe_test",
        })
        theorem_schema = self.schema["properties"]["theorems"]["items"]
        self.assertTrue(REQUIRED_THEOREM_FIELDS.issubset(set(theorem_schema["required"])))

    def test_register_conforms_to_schema_required_surface(self):
        self.assertTrue(REQUIRED_TOP_LEVEL_FIELDS.issubset(self.register))
        for theorem in self.theorems:
            with self.subTest(theorem=theorem.get("theorem_id")):
                self.assertTrue(REQUIRED_THEOREM_FIELDS.issubset(theorem))
                self.assertRegex(theorem["theorem_id"], r"^T\d+$")
                self.assertRegex(theorem["last_reviewed"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertGreaterEqual(theorem["confidence"], 0.0)
                self.assertLess(theorem["confidence"], 1.0)

    def test_source_class_scale_is_complete_and_ordered(self):
        source_class_scale = self.register["source_class_scale"]
        self.assertEqual(sorted(source_class_scale.keys()), ["0", "1", "2", "3", "4", "5", "6"])
        self.assertIn("operational record", source_class_scale["0"])
        self.assertIn("official", source_class_scale["1"])
        self.assertIn("fictional", source_class_scale["5"])
        self.assertIn("unsupported", source_class_scale["6"])

    def test_source_class_promotion_rule_blocks_low_quality_proof(self):
        promotion_rule = self.register["source_class_promotion_rule"].lower()
        self.assertIn("may inspire a hypothesis", promotion_rule)
        self.assertIn("must not be promoted", promotion_rule)
        self.assertIn("operational proof", promotion_rule)

        for theorem in self.theorems:
            numeric_classes = [item for item in theorem["source_class"] if isinstance(item, int)]
            if any(item >= 3 for item in numeric_classes):
                with self.subTest(theorem=theorem["theorem_id"]):
                    self.assertFalse(theorem.get("operational_proof", False))

    def test_release_blockers_are_represented_as_next_safe_tests(self):
        next_tests = "\n".join(theorem["next_safe_test"] for theorem in self.theorems).lower()
        self.assertIn("source-class", next_tests)
        self.assertIn("future-session", next_tests)


def cls_value(mapping, key):
    """Small helper to keep assertions readable without hiding missing keys."""
    return mapping[key]


if __name__ == "__main__":
    unittest.main()
