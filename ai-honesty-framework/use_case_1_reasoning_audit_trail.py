"""
USE CASE 1: AI Reasoning Audit Trail (AAPF)
Demonstrates cryptographic logging of all AI reasoning steps
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, serialize_framework_state
)


def reasoning_audit_trail_demo():
    """
    Scenario: Medical AI diagnoses patient condition.
    Framework logs every reasoning step with cryptographic proof.
    Doctor can verify diagnosis reasoning is sound and unmodified.
    """
    framework = ComplianceFramework(signer_key="medical-ai-reasoning")

    print("\n" + "="*80)
    print("AI REASONING AUDIT TRAIL - MEDICAL DIAGNOSIS")
    print("="*80)

    # Step 1: Input patient data
    print("\n[STEP 1] Patient presents with symptoms")
    print("-" * 80)

    patient_data = {
        "patient_id": "P-2026-00742",
        "age": 65,
        "symptoms": ["chest pain", "shortness of breath", "fatigue"],
        "vital_signs": {
            "heart_rate": 105,
            "blood_pressure": "145/92",
            "oxygen_saturation": "94%"
        },
        "medical_history": ["hypertension", "diabetes type 2"]
    }

    input_action = framework.record_action(
        agent_id="medical-ai-v3.2",
        action_type="PATIENT_INPUT_RECEIVED",
        parameters=patient_data
    )

    print(f"Patient: {patient_data['patient_id']}, Age: {patient_data['age']}")
    print(f"Symptoms: {', '.join(patient_data['symptoms'])}")
    print(f"Action ID: {input_action.action_id}")
    print(f"Signature: {input_action.signature[:16]}...")

    # Step 2: Reasoning step 1 - Symptom analysis
    print("\n[STEP 2] AI reasoning step 1: Symptom analysis")
    print("-" * 80)

    reasoning_1 = framework.record_action(
        agent_id="medical-ai-v3.2",
        action_type="REASONING_STEP",
        parameters={
            "step_number": 1,
            "step_name": "Symptom Analysis",
            "inputs": patient_data['symptoms'],
            "differential_diagnoses": [
                "Acute Coronary Syndrome (ACS)",
                "Heart Failure",
                "Pulmonary Embolism",
                "Anxiety Disorder"
            ],
            "reasoning": "Chest pain + SOB + fatigue in 65yo with HTN/DM2 suggests cardiac etiology"
        }
    )

    print("Differential diagnoses considered:")
    for dx in reasoning_1.parameters['differential_diagnoses']:
        print(f"  - {dx}")
    print(f"Reasoning: {reasoning_1.parameters['reasoning']}")
    print(f"Signature: {reasoning_1.signature[:16]}...")

    # Step 3: Reasoning step 2 - Risk stratification
    print("\n[STEP 3] AI reasoning step 2: Risk stratification")
    print("-" * 80)

    reasoning_2 = framework.record_action(
        agent_id="medical-ai-v3.2",
        action_type="REASONING_STEP",
        parameters={
            "step_number": 2,
            "step_name": "Risk Stratification",
            "risk_factors": ["Age 65+", "Hypertension", "Diabetes", "Chest pain", "SOB"],
            "risk_score": 8.5,  # Out of 10
            "risk_category": "HIGH",
            "reasoning": "Multiple cardiac risk factors + acute symptoms = HIGH RISK for ACS"
        }
    )

    print(f"Risk Score: {reasoning_2.parameters['risk_score']}/10")
    print(f"Risk Category: {reasoning_2.parameters['risk_category']}")
    print(f"Risk Factors: {', '.join(reasoning_2.parameters['risk_factors'])}")
    print(f"Signature: {reasoning_2.signature[:16]}...")

    # Step 4: Reasoning step 3 - Recommendation
    print("\n[STEP 4] AI reasoning step 3: Clinical recommendation")
    print("-" * 80)

    reasoning_3 = framework.record_action(
        agent_id="medical-ai-v3.2",
        action_type="REASONING_STEP",
        parameters={
            "step_number": 3,
            "step_name": "Clinical Recommendation",
            "recommended_tests": ["ECG", "Troponin", "Chest X-ray", "D-dimer"],
            "recommended_action": "Urgent cardiology consult + admission to ICU monitoring",
            "confidence_level": 0.89,
            "reasoning": "HIGH-RISK presentation requires urgent evaluation and monitoring"
        }
    )

    print(f"Recommended Tests: {', '.join(reasoning_3.parameters['recommended_tests'])}")
    print(f"Recommended Action: {reasoning_3.parameters['recommended_action']}")
    print(f"Confidence: {reasoning_3.parameters['confidence_level']*100:.0f}%")
    print(f"Signature: {reasoning_3.signature[:16]}...")

    # Step 5: Generate final diagnosis
    print("\n[STEP 5] AI generates final diagnosis output")
    print("-" * 80)

    final_output = framework.record_action(
        agent_id="medical-ai-v3.2",
        action_type="DIAGNOSIS_OUTPUT_GENERATED",
        parameters={
            "primary_diagnosis": "Acute Coronary Syndrome (Unstable Angina vs. NSTEMI)",
            "confidence": 0.89,
            "secondary_diagnoses": ["Heart Failure", "Hypertensive Emergency"],
            "critical_actions": [
                "Administer aspirin 325mg PO immediately",
                "Start IV access and cardiac monitoring",
                "Request STAT ECG and troponin",
                "Notify cardiology for urgent consult"
            ],
            "reasoning_chain": [reasoning_1.action_id, reasoning_2.action_id, reasoning_3.action_id]
        }
    )

    print(f"Primary Diagnosis: {final_output.parameters['primary_diagnosis']}")
    print(f"Confidence: {final_output.parameters['confidence']*100:.0f}%")
    print(f"\nCritical Actions:")
    for action in final_output.parameters['critical_actions']:
        print(f"  - {action}")
    print(f"\nDiagnosis Signature: {final_output.signature[:16]}...")

    # Step 6: Verify entire reasoning chain
    print("\n[STEP 6] Verify reasoning chain integrity")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Chain valid: {is_valid}")
    print(f"Total steps in chain: {len(framework.provenance_chain)}")
    print(f"Merkle root: {merkle_root[:16]}...")
    print(f"\nMerkle root proves:")
    print(f"  - No reasoning steps were deleted")
    print(f"  - No reasoning steps were modified")
    print(f"  - Entire diagnosis reasoning is unmodified")
    print(f"  - One-bit change breaks entire root hash (tamper-evident)")

    # Step 7: Save compliance packet
    print("\n[STEP 7] Save diagnosis with complete reasoning proof")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["use_case"] = "Medical Diagnosis Reasoning Audit Trail"
    compliance_packet["patient_id"] = patient_data['patient_id']
    compliance_packet["diagnosis_summary"] = {
        "primary_diagnosis": final_output.parameters['primary_diagnosis'],
        "confidence": final_output.parameters['confidence'],
        "reasoning_steps": len(framework.provenance_chain),
        "chain_integrity": is_valid,
        "merkle_proof": merkle_root[:16]
    }

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/ai-honesty-framework/use_case_1_diagnosis_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet saved")
    print(f"  - Patient ID: {patient_data['patient_id']}")
    print(f"  - Reasoning steps: {len(framework.provenance_chain)}")
    print(f"  - Chain integrity verified: {is_valid}")
    print(f"  - Merkle root: {merkle_root[:16]}...")

    # Step 8: Doctor review
    print("\n[STEP 8] Doctor verifies diagnosis reasoning")
    print("-" * 80)

    print("Doctor review checklist:")
    print("  [X] Verified: All reasoning steps are present and unmodified")
    print("  [X] Verified: Symptoms were correctly analyzed")
    print("  [X] Verified: Risk stratification is appropriate")
    print("  [X] Verified: Recommendations align with reasoning")
    print(f"  [X] Verified: Merkle root {merkle_root[:16]}... proves chain integrity")
    print("\nOutcome: DIAGNOSIS APPROVED - Medical team proceeds with treatment plan")


if __name__ == "__main__":
    reasoning_audit_trail_demo()
