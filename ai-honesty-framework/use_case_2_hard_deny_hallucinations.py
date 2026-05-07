"""
USE CASE 2: Hard-Deny Rules for Hallucinations (NAP)
Demonstrates preventing AI from claiming false facts as true
"""

import json
import time
from framework_core import (
    ComplianceFramework, NegativeAuthorityProfile, DataClassification,
    serialize_framework_state
)


def hard_deny_hallucinations_demo():
    """
    Scenario: Legal AI is asked to cite a court case.
    NAP rules prevent AI from fabricating case citations.
    Any hallucination attempt is blocked and logged.
    """
    framework = ComplianceFramework(signer_key="legal-ai-honesty")

    print("\n" + "="*80)
    print("HARD-DENY RULES - PREVENTING HALLUCINATED CASE CITATIONS")
    print("="*80)

    # Step 1: Register NAP rules
    print("\n[STEP 1] Register hard-deny rules for legal AI")
    print("-" * 80)

    hallucination_nap = NegativeAuthorityProfile(
        rule_id="nap-legal-no-hallucinations",
        resource_id="legal-ai-v2.1",
        forbidden_operations=[
            "CITE_NONEXISTENT_CASE",
            "CLAIM_CERTAINTY_WITHOUT_SOURCE",
            "FABRICATE_STATUTE",
            "FALSE_PRECEDENT_CLAIM"
        ],
        override_policy="IMPOSSIBLE",  # Cannot be overridden
        enforcement_timestamp=time.time(),
        enforcement_signature=framework.sign_data("legal-honesty-nap")
    )

    framework.register_nap_rule(hallucination_nap)

    print("Hard-deny rule registered:")
    print(f"  Rule ID: {hallucination_nap.rule_id}")
    print(f"  Forbidden operations:")
    for op in hallucination_nap.forbidden_operations:
        print(f"    - {op}")
    print(f"  Override policy: {hallucination_nap.override_policy} (cannot be bypassed)")

    # Step 2: User asks for case citation
    print("\n[STEP 2] User asks AI to cite supporting legal precedent")
    print("-" * 80)

    query = framework.record_action(
        agent_id="user-attorney",
        action_type="QUERY_LEGAL_PRECEDENT",
        parameters={
            "question": "What is the leading case on employee non-compete enforcement in California?",
            "jurisdiction": "California",
            "topic": "Non-compete agreements"
        }
    )

    print(f"Query: {query.parameters['question']}")
    print(f"Jurisdiction: {query.parameters['jurisdiction']}")

    # Step 3: AI generates response (with hallucination attempt)
    print("\n[STEP 3] AI attempts to respond with case citation")
    print("-" * 80)

    # The AI's internal reasoning might try to hallucinate a case
    hallucinated_cite = {
        "case_name": "Smith v. California Tech Corp, 2024 CA 456789",
        "year": 2024,
        "holding": "Non-compete agreements are unenforceable under California law",
        "confidence": 0.95  # High confidence in fabricated case!
    }

    print("AI generated response (candidate):")
    print(f"  Case: {hallucinated_cite['case_name']}")
    print(f"  Holding: {hallucinated_cite['holding']}")
    print(f"  Confidence: {hallucinated_cite['confidence']*100:.0f}%")

    # Step 4: Check against NAP rules
    print("\n[STEP 4] Framework checks response against hard-deny rules")
    print("-" * 80)

    # Check: Is this case real? (In real implementation, would check legal database)
    case_is_real = False  # This case doesn't exist in legal databases

    if not case_is_real:
        # Attempting to cite nonexistent case
        allowed, reason = framework.check_nap_compliance(
            resource_id="legal-ai-v2.1",
            operation="CITE_NONEXISTENT_CASE",
            party_count=1
        )

        print(f"NAP compliance check:")
        print(f"  Operation: CITE_NONEXISTENT_CASE")
        print(f"  Allowed: {allowed}")
        print(f"  Reason: {reason}")

        # Step 5: Block hallucination and log
        print("\n[STEP 5] Hallucination blocked and logged")
        print("-" * 80)

        blocked_action = framework.record_action(
            agent_id="legal-ai-v2.1",
            action_type="HALLUCINATION_ATTEMPT_BLOCKED",
            parameters={
                "attempted_citation": hallucinated_cite,
                "reason": "Case does not exist in legal databases",
                "nap_rule_violated": "nap-legal-no-hallucinations",
                "violation_type": "CITE_NONEXISTENT_CASE",
                "timestamp_blocked": time.time(),
                "alert_sent_to": ["attorney", "legal-compliance-monitor"]
            }
        )

        print(f"Hallucination blocked:")
        print(f"  Attempted case: {hallucinated_cite['case_name']}")
        print(f"  Violation: Case does not exist")
        print(f"  Action logged: {blocked_action.action_id}")
        print(f"  Signature: {blocked_action.signature[:16]}...")

        # Step 6: Generate honest response instead
        print("\n[STEP 6] AI generates honest response with confidence disclosure")
        print("-" * 80)

        honest_response = framework.record_action(
            agent_id="legal-ai-v2.1",
            action_type="HONEST_RESPONSE_GENERATED",
            parameters={
                "response": "California recognizes that non-compete agreements are generally unenforceable under California Business & Professions Code Section 16600. However, I cannot cite a specific recent Supreme Court case on this exact topic from my training data.",
                "confidence": 0.65,
                "supported_by": [
                    "Cal. Bus. & Prof. Code Section 16600 (verified statute)",
                    "General California law principle (well-established)"
                ],
                "unsupported_by": [
                    "Specific recent case citation (not found in knowledge base)"
                ],
                "disclaimer": "This is general legal information, not legal advice. Consult an attorney for your specific situation."
            }
        )

        print(f"Honest response:")
        print(f"  Response: {honest_response.parameters['response']}")
        print(f"  Confidence: {honest_response.parameters['confidence']*100:.0f}%")
        print(f"\n  Supported by:")
        for source in honest_response.parameters['supported_by']:
            print(f"    - {source}")
        print(f"  Unsupported by:")
        for item in honest_response.parameters['unsupported_by']:
            print(f"    - {item}")
        print(f"\n  Disclaimer: {honest_response.parameters['disclaimer']}")

    # Step 7: Verify chain integrity
    print("\n[STEP 7] Verify response integrity")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Chain valid: {is_valid}")
    print(f"Total actions: {len(framework.provenance_chain)}")
    print(f"Merkle root: {merkle_root[:16]}...")
    print(f"\nEvents logged:")
    for i, action in enumerate(framework.provenance_chain):
        print(f"  {i+1}. {action.action_type} - {action.action_id}")

    # Step 8: Save compliance packet
    print("\n[STEP 8] Save response with hallucination prevention proof")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["use_case"] = "Legal AI - Hallucination Prevention"
    compliance_packet["analysis"] = {
        "hallucination_attempts": 1,
        "hallucinations_blocked": 1,
        "block_rate": "100%",
        "honest_response_provided": True,
        "nap_enforcement": "SUCCESSFUL"
    }

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/ai-honesty-framework/use_case_2_hallucination_prevention_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet saved")
    print(f"  - Hallucination attempts: 1")
    print(f"  - Hallucinations blocked: 1")
    print(f"  - Block rate: 100%")
    print(f"  - NAP enforcement: SUCCESSFUL")

    # Step 9: Attorney review
    print("\n[STEP 9] Attorney reviews AI output")
    print("-" * 80)

    print("Attorney checklist:")
    print("  [X] AI did not fabricate case citations")
    print("  [X] AI disclosed confidence level (65%)")
    print("  [X] AI provided verified sources (statute)")
    print("  [X] AI disclosed limitations (no recent case found)")
    print("  [X] Hallucination attempt was logged with proof")
    print(f"  [X] Merkle root {merkle_root[:16]}... proves no tampering")
    print("\nOutcome: AI response is TRUSTWORTHY - Attorney can rely on it")


if __name__ == "__main__":
    hard_deny_hallucinations_demo()
