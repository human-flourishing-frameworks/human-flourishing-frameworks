"""
USE CASE 3: Trustworthiness Classification (DCF)
Demonstrates classifying AI outputs by confidence and verification level
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, serialize_framework_state
)


def trustworthiness_classification_demo():
    """
    Scenario: Finance AI provides investment analysis.
    Every claim is classified by trustworthiness level.
    User can see which outputs are verified vs. speculative.
    """
    framework = ComplianceFramework(signer_key="finance-ai-honesty")

    print("\n" + "="*80)
    print("TRUSTWORTHINESS CLASSIFICATION - INVESTMENT ANALYSIS")
    print("="*80)

    # Step 1: User asks for market analysis
    print("\n[STEP 1] User requests financial market analysis")
    print("-" * 80)

    query = framework.record_action(
        agent_id="user-investor",
        action_type="MARKET_ANALYSIS_QUERY",
        parameters={
            "ticker": "TECHCORP",
            "analysis_type": "Fundamental + Technical",
            "time_horizon": "12 months"
        }
    )

    print(f"Query: Analyze TECHCORP for 12-month investment decision")

    # Step 2: AI generates analysis (multiple claims with different confidence levels)
    print("\n[STEP 2] AI generates analysis with multiple claims")
    print("-" * 80)

    analysis_claims = {
        "claim_1": {
            "statement": "TECHCORP revenue was $5.2B in Q4 2025",
            "type": "verified_fact",
            "confidence": 0.99,
            "source": "SEC 10-K filing",
            "classification": DataClassification.PUBLIC
        },
        "claim_2": {
            "statement": "TECHCORP has growing market share in cloud computing",
            "type": "data_inference",
            "confidence": 0.78,
            "source": "Multiple analyst reports + company filings",
            "classification": DataClassification.INTERNAL
        },
        "claim_3": {
            "statement": "AI will be a major revenue driver for TECHCORP",
            "type": "speculation",
            "confidence": 0.45,
            "source": "Industry trend analysis + management commentary",
            "classification": DataClassification.CONFIDENTIAL
        },
        "claim_4": {
            "statement": "Stock price will reach $500 in 12 months",
            "type": "price_prediction",
            "confidence": 0.25,
            "source": "Historical volatility models",
            "classification": DataClassification.SECRET
        }
    }

    print("AI analysis with trustworthiness classifications:\n")

    for claim_id, claim_data in analysis_claims.items():
        # Record the claim
        claim_action = framework.record_action(
            agent_id="finance-ai-v4.1",
            action_type="ANALYSIS_CLAIM",
            parameters=claim_data
        )

        # Classify the claim
        label = framework.classify_data(
            resource_id=f"TECHCORP-{claim_id}",
            classification=claim_data['classification'],
            applier="finance-ai-honesty-framework",
            confidence=claim_data['confidence'],
            reasoning=f"Type: {claim_data['type']}, Confidence: {claim_data['confidence']*100:.0f}%"
        )

        print(f"Claim: {claim_data['statement']}")
        print(f"  Classification: {claim_data['classification'].value.upper()}")
        print(f"  Confidence: {claim_data['confidence']*100:.0f}%")
        print(f"  Type: {claim_data['type']}")
        print(f"  Source: {claim_data['source']}")
        print()

    # Step 3: Explain classification levels to investor
    print("\n[STEP 3] Classification guide for investor")
    print("-" * 80)

    classification_guide = {
        "PUBLIC": {
            "meaning": "Verified facts (95%+ confidence)",
            "examples": "Financial data from SEC filings, confirmed earnings",
            "how_to_use": "Can rely on this for investment decisions"
        },
        "INTERNAL": {
            "meaning": "Educated inference (70-94% confidence)",
            "examples": "Analysis based on multiple reliable sources",
            "how_to_use": "Use as context, but verify independently"
        },
        "CONFIDENTIAL": {
            "meaning": "Speculative (30-69% confidence)",
            "examples": "Industry trends, forward-looking statements",
            "how_to_use": "Caution: High uncertainty, do not rely solely on this"
        },
        "SECRET": {
            "meaning": "Unknown/cannot determine (<30% confidence)",
            "examples": "Price predictions, speculation",
            "how_to_use": "Avoid: Too uncertain for investment decisions"
        }
    }

    for level, guide in classification_guide.items():
        print(f"{level}:")
        print(f"  {guide['meaning']}")
        print(f"  Examples: {guide['examples']}")
        print(f"  Use: {guide['how_to_use']}")
        print()

    # Step 4: Verify chain integrity
    print("\n[STEP 4] Verify analysis integrity")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Chain valid: {is_valid}")
    print(f"Total claims analyzed: {len(framework.provenance_chain)}")
    print(f"Claims classified: {len(framework.classifications)}")
    print(f"Merkle root: {merkle_root[:16]}...")

    # Step 5: Classification summary
    print("\n[STEP 5] Summary of trustworthiness levels")
    print("-" * 80)

    classification_summary = {}
    for claim_id, classification in framework.classifications.items():
        level = classification.classification.value
        if level not in classification_summary:
            classification_summary[level] = []
        classification_summary[level].append({
            "claim": claim_id,
            "confidence": classification.confidence_score
        })

    print("Claims by trustworthiness level:")
    for level in [DataClassification.PUBLIC.value, DataClassification.INTERNAL.value,
                  DataClassification.CONFIDENTIAL.value, DataClassification.SECRET.value]:
        if level in classification_summary:
            print(f"\n{level.upper()}:")
            for item in classification_summary[level]:
                print(f"  - {item['claim']}: {item['confidence']*100:.0f}% confidence")

    # Step 6: Save compliance packet
    print("\n[STEP 6] Save analysis with trustworthiness proof")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["use_case"] = "Finance AI - Trustworthiness Classification"
    compliance_packet["investment_analysis"] = {
        "ticker": "TECHCORP",
        "analysis_date": time.ctime(),
        "claims_analyzed": len(framework.provenance_chain),
        "claims_classified": len(framework.classifications),
        "claims_by_level": classification_summary
    }

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/ai-honesty-framework/use_case_3_classification_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet saved")
    print(f"  - Claims analyzed: {len(framework.provenance_chain)}")
    print(f"  - Claims classified: {len(framework.classifications)}")
    print(f"  - Chain integrity verified: {is_valid}")

    # Step 7: Investor decision
    print("\n[STEP 7] Investor makes decision based on classified analysis")
    print("-" * 80)

    print("Investor decision process:")
    print("  [X] Identified verified facts (PUBLIC): TECHCORP revenue $5.2B")
    print("  [X] Identified reliable inferences (INTERNAL): Growing market share")
    print("  [X] Identified speculation (CONFIDENTIAL): AI revenue growth")
    print("  [X] Rejected unreliable predictions (SECRET): Stock price target")
    print(f"  [X] Verified chain integrity: {merkle_root[:16]}...")
    print("\nOutcome: CONFIDENT DECISION - Investor can trust AI's trustworthiness labels")


if __name__ == "__main__":
    trustworthiness_classification_demo()
