"""
USE CASE 5: Model Degradation Tracking (PCSF)
Demonstrates detecting and logging AI model quality drift over time
"""

import json
import time
from framework_core import (
    ComplianceFramework, serialize_framework_state
)


def model_degradation_demo():
    """
    Scenario: Criminal justice AI is used for recidivism prediction.
    Framework tracks if model accuracy degrades over time.
    System detects if demographic bias increases (fairness degradation).
    """
    framework = ComplianceFramework(signer_key="criminal-justice-fairness")

    print("\n" + "="*80)
    print("MODEL DEGRADATION TRACKING - CRIMINAL JUSTICE FAIRNESS")
    print("="*80)

    # Step 1: Establish baseline model performance
    print("\n[STEP 1] Establish baseline model performance at deployment")
    print("-" * 80)

    baseline_action = framework.record_action(
        agent_id="criminal-justice-ai-v1.0",
        action_type="MODEL_BASELINE_ESTABLISHED",
        parameters={
            "model_version": "1.0",
            "training_date": "2025-01-15",
            "test_set_size": 50000,
            "baseline_metrics": {
                "overall_accuracy": 0.876,
                "accuracy_african_american": 0.849,
                "accuracy_caucasian": 0.893,
                "accuracy_hispanic": 0.861,
                "fairness_metric": "3.3% accuracy gap (acceptable)"
            }
        }
    )

    print("Model baseline established:")
    print("  Overall accuracy: 87.6%")
    print("  African American: 84.9%")
    print("  Caucasian: 89.3%")
    print("  Hispanic: 86.1%")
    print("  Fairness gap: 3.3% (within acceptable range)")

    # Track baseline metrics
    accuracy_tracker = framework.track_degradation(
        provider_id="criminal-justice-ai-v1.0",
        metric_name="overall_accuracy",
        initial_value=0.876,
        current_value=0.876
    )

    fairness_tracker = framework.track_degradation(
        provider_id="criminal-justice-ai-v1.0",
        metric_name="accuracy_fairness_gap",
        initial_value=0.033,  # 3.3% as decimal
        current_value=0.033
    )

    # Step 2: Monthly monitoring - month 3 (stable)
    print("\n[STEP 2] Month 3 check - Performance stable")
    print("-" * 80)

    month_3_check = framework.record_action(
        agent_id="criminal-justice-ai-monitor",
        action_type="MONTHLY_PERFORMANCE_CHECK",
        parameters={
            "month": 3,
            "overall_accuracy": 0.874,
            "accuracy_african_american": 0.848,
            "accuracy_caucasian": 0.891,
            "accuracy_hispanic": 0.860,
            "fairness_gap": 0.035,
            "status": "STABLE"
        }
    )

    accuracy_tracker.current_value = 0.874
    fairness_tracker.current_value = 0.035

    print(f"Month 3: Overall accuracy 87.4% (down 0.2% - within normal variance)")
    print(f"         Fairness gap: 3.5% (still acceptable)")

    # Step 3: Monthly monitoring - month 6 (drift detected)
    print("\n[STEP 3] Month 6 check - DEGRADATION DETECTED")
    print("-" * 80)

    month_6_check = framework.record_action(
        agent_id="criminal-justice-ai-monitor",
        action_type="MONTHLY_PERFORMANCE_CHECK",
        parameters={
            "month": 6,
            "overall_accuracy": 0.851,
            "accuracy_african_american": 0.798,
            "accuracy_caucasian": 0.889,
            "accuracy_hispanic": 0.832,
            "fairness_gap": 0.091,
            "status": "DEGRADATION_ALERT"
        }
    )

    # Record degradation
    accuracy_tracker.record_degradation(
        event_type="ACCURACY_DROP",
        value=0.851,
        reason="Overall accuracy dropped from 87.6% to 85.1% (down 2.5%)"
    )

    fairness_tracker.record_degradation(
        event_type="FAIRNESS_DEGRADATION",
        value=0.091,
        reason="Accuracy gap widened from 3.3% to 9.1% (concerning drift toward demographic bias)"
    )

    print("DEGRADATION DETECTED:")
    print(f"  Overall accuracy: 85.1% (down 2.5% from baseline)")
    print(f"  African American accuracy: 79.8% (down 5.1% - CRITICAL)")
    print(f"  Caucasian accuracy: 88.9% (stable)")
    print(f"  Hispanic accuracy: 83.2% (down 2.9%)")
    print(f"  Fairness gap: 9.1% (up 5.8% - CRITICAL)")
    print(f"\n  Alert: Model is becoming biased against African American defendants!")

    # Step 4: Investigation and remediation
    print("\n[STEP 4] Investigate degradation and plan remediation")
    print("-" * 80)

    investigation = framework.record_action(
        agent_id="criminal-justice-audit-team",
        action_type="DEGRADATION_INVESTIGATION",
        parameters={
            "root_cause_analysis": [
                "Fine-tuning on recent local jurisdiction data",
                "New jurisdiction has different demographic distribution",
                "Model overfitted to majority demographic in new data"
            ],
            "recommended_actions": [
                "Halt use of model for African American defendants pending review",
                "Retrain on balanced demographic data",
                "Add fairness constraints to model objective",
                "Implement stricter demographic parity monitoring"
            ],
            "urgency": "CRITICAL",
            "legal_impact": "Model usage violates fairness requirements - potential litigation risk"
        }
    )

    print("Investigation findings:")
    for cause in investigation.parameters['root_cause_analysis']:
        print(f"  - {cause}")

    print("\nRecommended actions:")
    for action in investigation.parameters['recommended_actions']:
        print(f"  - {action}")

    print(f"\nLegal impact: {investigation.parameters['legal_impact']}")

    # Step 5: Record remediation action
    print("\n[STEP 5] Implement remediation")
    print("-" * 80)

    remediation = framework.record_action(
        agent_id="criminal-justice-ai-team",
        action_type="MODEL_REMEDIATION_IMPLEMENTED",
        parameters={
            "old_model_version": "1.0",
            "new_model_version": "1.1",
            "retraining_approach": "Balanced demographic stratification",
            "fairness_constraints": "Demographic parity enforced (accuracy gap < 2%)",
            "post_remediation_metrics": {
                "overall_accuracy": 0.869,
                "accuracy_african_american": 0.862,
                "accuracy_caucasian": 0.874,
                "accuracy_hispanic": 0.859,
                "fairness_gap": 0.012
            }
        }
    )

    accuracy_tracker.record_degradation(
        event_type="MODEL_RETRAINED",
        value=0.869,
        reason="Retraining with fairness constraints improved accuracy gap from 9.1% to 1.2%"
    )

    fairness_tracker.record_degradation(
        event_type="FAIRNESS_RESTORED",
        value=0.012,
        reason="Fairness gap reduced to 1.2% (within acceptable range)"
    )

    print("Model version 1.1 deployed with:")
    print(f"  New overall accuracy: 86.9% (recovered most loss)")
    print(f"  African American accuracy: 86.2% (restored fairness)")
    print(f"  New fairness gap: 1.2% (restored to acceptable range)")

    # Step 6: Verify degradation tracking
    print("\n[STEP 6] Verify degradation tracking and audit trail")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Chain valid: {is_valid}")
    print(f"Total monitoring events: {len(framework.provenance_chain)}")
    print(f"Degradation metrics tracked: {len(framework.capacity_states)}")

    print(f"\nDegradation events logged:")
    print(f"  Accuracy tracker: {len(accuracy_tracker.degradation_events)} events")
    for event in accuracy_tracker.degradation_events:
        print(f"    - {event['type']}: {event['reason']}")

    print(f"\n  Fairness tracker: {len(fairness_tracker.degradation_events)} events")
    for event in fairness_tracker.degradation_events:
        print(f"    - {event['type']}: {event['reason']}")

    # Step 7: Compliance documentation
    print("\n[STEP 7] Generate compliance documentation")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["use_case"] = "Criminal Justice AI - Degradation & Fairness Tracking"
    compliance_packet["degradation_analysis"] = {
        "initial_accuracy": 0.876,
        "peak_degradation": {
            "accuracy": 0.851,
            "fairness_gap": 0.091,
            "month_detected": 6
        },
        "post_remediation": {
            "accuracy": 0.869,
            "fairness_gap": 0.012,
            "status": "RESTORED"
        },
        "legal_defensibility": "FULL - Complete audit trail proves degradation was detected and remediated"
    }

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/ai-honesty-framework/use_case_5_degradation_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet saved")
    print(f"  - Tracking period: 6 months")
    print(f"  - Degradation detected and logged: YES")
    print(f"  - Remediation implemented: YES")
    print(f"  - Legal defensibility: FULL")

    # Step 8: Court/audit verification
    print("\n[STEP 8] Court/audit can verify fairness compliance")
    print("-" * 80)

    print("Audit checklist:")
    print("  [X] Model baseline established at deployment")
    print("  [X] Monthly monitoring performed and logged")
    print("  [X] Degradation detected automatically at month 6")
    print("  [X] Investigation documented")
    print("  [X] Root cause identified")
    print("  [X] Remediation implemented")
    print("  [X] Fairness restored")
    print(f"  [X] Complete audit trail immutable: {merkle_root[:16]}...")
    print("\nOutcome: COMPLIANT - Criminal justice agency can defend model fairness in court")


if __name__ == "__main__":
    model_degradation_demo()
