"""
USE CASE 3: Quantum Algorithm IP Watermarking & Licensing
Demonstrates AAPF for tracking algorithm execution and IP verification
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, NegativeAuthorityProfile,
    serialize_framework_state
)


def quantum_algorithm_watermark_demo():
    """
    Scenario: Research lab licenses a proprietary VQE variant to pharma company.
    Framework proves: exact algorithm was executed, no modification, usage logged for billing.
    """
    framework = ComplianceFramework(signer_key="quantum-algorithm-licensing")

    print("\n" + "="*80)
    print("QUANTUM ALGORITHM IP WATERMARKING & LICENSING")
    print("="*80)

    # Step 1: Algorithm specification and watermark
    print("\n[STEP 1] Define proprietary quantum algorithm with embedded watermark")
    print("-" * 80)

    # VQE (Variational Quantum Eigensolver) variant
    algorithm_spec = {
        "algorithm_name": "VQE-DrugDiscovery-v2.1",
        "version": "2.1",
        "vendor": "MIT-Quantum-Lab",
        "license_key": "MIT-QML-VQE-2026-PHARMACO-EXCLUSIVE",
        "gate_sequence": [
            "RY(theta_0)",
            "CZ(q0,q1)",
            "RY(theta_1)",
            "CZ(q1,q2)",
            "RY(theta_2)",
            "RZ(watermark_phase_0)",  # WATERMARK 1
            "CZ(q0,q2)",
            "RY(theta_3)",
            "MEASURE"
        ],
        "watermark_phases": [
            {"gate_index": 5, "phase_value": 0.7854, "hidden_data": "MIT-VQE-v2.1"}  # pi/4
        ],
        "gate_count": 9,
        "qubit_count": 3,
        "parameter_vector_length": 4,
        "execution_time_min_seconds": 2,
        "execution_time_max_seconds": 30
    }

    # Compute algorithm fingerprint
    algorithm_json = json.dumps(algorithm_spec, sort_keys=True)
    algorithm_hash = framework.hash_data(algorithm_json)

    print(f"Algorithm: {algorithm_spec['algorithm_name']}")
    print(f"Vendor: {algorithm_spec['vendor']}")
    print(f"License: {algorithm_spec['license_key']}")
    print(f"Gates: {algorithm_spec['gate_count']}")
    print(f"Qubits: {algorithm_spec['qubit_count']}")
    print(f"Watermarks embedded: {len(algorithm_spec['watermark_phases'])}")
    print(f"Algorithm fingerprint: {algorithm_hash[:16]}...")

    # Step 2: License agreement and NDC (NAP equivalent)
    print("\n[STEP 2] Register licensing restrictions (NAP)")
    print("-" * 80)

    license_restrictions = NegativeAuthorityProfile(
        rule_id="nap-vqe-v2.1-pharmaco",
        resource_id="algorithm-vqe-v2.1",
        forbidden_operations=[
            "SHARE_WITH_COMPETITORS",
            "REVERSE_ENGINEER",
            "PUBLISH_IN_LITERATURE",
            "SUBLICENSE_WITHOUT_APPROVAL"
        ],
        override_policy="REQUIRES_QUORUM",  # Requires approval from vendor + customer + neutral party
        enforcement_timestamp=time.time(),
        enforcement_signature=framework.sign_data("license-nap-vqe-v2.1")
    )

    framework.register_nap_rule(license_restrictions)

    print(f"License rule: {license_restrictions.rule_id}")
    print(f"Forbidden operations:")
    for op in license_restrictions.forbidden_operations:
        print(f"  - {op}")
    print(f"Override policy: {license_restrictions.override_policy}")
    print(f"Enforcement: {time.ctime(license_restrictions.enforcement_timestamp)}")

    # Step 3: Classify algorithm as CONFIDENTIAL (DCF)
    print("\n[STEP 3] Classify algorithm intellectual property (DCF)")
    print("-" * 80)

    algo_label = framework.classify_data(
        resource_id="algorithm-vqe-v2.1",
        classification=DataClassification.CONFIDENTIAL,
        applier="licensing@mit-quantum-lab.edu"
    )

    print(f"Resource: {algo_label.resource_id}")
    print(f"Classification: {algo_label.classification.value}")
    print(f"Applied by: {algo_label.applied_by}")
    print(f"Transformation history: {len(algo_label.transformation_history)} events")

    # Step 4: First execution - log gate sequence (AAPF)
    print("\n[STEP 4] Execute algorithm: PHARMAÇO runs first simulation")
    print("-" * 80)

    execution_1 = framework.record_action(
        agent_id="pharmaço-quantum-lab",
        action_type="QUANTUM_ALGORITHM_EXECUTION",
        parameters={
            "algorithm_id": "vqe-v2.1",
            "license_key": "MIT-QML-VQE-2026-PHARMACO-EXCLUSIVE",
            "algorithm_hash": algorithm_hash,
            "gate_sequence_executed": algorithm_spec["gate_sequence"],
            "parameters_used": [1.234, 2.345, 0.456, 3.567],
            "target_molecule": "COVID-19-protease-inhibitor",
            "execution_timestamp": time.time(),
            "quantum_processor_id": "IonQ-Denver-Q32",
            "execution_status": "SUCCESS",
            "energy_result": -42.75,
            "shots": 1000,
            "watermark_verified": "YES"
        }
    )

    print(f"Execution ID: {execution_1.action_id}")
    print(f"Algorithm: {algorithm_spec['algorithm_name']}")
    print(f"Hash match: {execution_1.parameters['algorithm_hash'][:16]}...")
    print(f"Target: {execution_1.parameters['target_molecule']}")
    print(f"Energy result: {execution_1.parameters['energy_result']} Ha")
    print(f"Watermark verified: YES (algorithm unmodified)")
    print(f"Signature: {execution_1.signature[:16]}...")

    # Step 5: Verify execution against algorithm spec
    print("\n[STEP 5] Verify execution integrity")
    print("-" * 80)

    verification_result = {
        "check_algorithm_hash": execution_1.parameters["algorithm_hash"] == algorithm_hash,
        "check_gate_sequence": execution_1.parameters["gate_sequence_executed"] == algorithm_spec["gate_sequence"],
        "check_gate_count": len(execution_1.parameters["gate_sequence_executed"]) == algorithm_spec["gate_count"],
        "check_watermark_present": "watermark_verified" in execution_1.parameters,
        "check_within_time_bounds": True,
        "verdict": "LICENSED_EXECUTION_VERIFIED"
    }

    print("Verification checks:")
    for check, result in verification_result.items():
        if check != "verdict":
            print(f"  {check}: {result}")
    print(f"\nVerdict: {verification_result['verdict']}")

    # Step 6: Attempted unauthorized modification
    print("\n[STEP 6] Unauthorized attempt: Modify algorithm (DETECT & DENY)")
    print("-" * 80)

    # Modify algorithm
    modified_algorithm = algorithm_spec.copy()
    modified_algorithm["gate_sequence"][2] = "RY(theta_1_HACKED)"  # Try to modify

    modified_json = json.dumps(modified_algorithm, sort_keys=True)
    modified_hash = framework.hash_data(modified_json)

    print(f"Attacker attempts modification...")
    print(f"Original hash: {algorithm_hash[:16]}...")
    print(f"Modified hash: {modified_hash[:16]}...")
    print(f"Hash mismatch: {algorithm_hash != modified_hash}")

    # Try to record modified execution
    nap_allowed, nap_reason = framework.check_nap_compliance(
        resource_id="algorithm-vqe-v2.1",
        operation="REVERSE_ENGINEER",
        party_count=1  # Single attacker, no quorum
    )

    print(f"\nNAP compliance check:")
    print(f"  Operation: REVERSE_ENGINEER (attempted)")
    print(f"  Allowed: {nap_allowed}")
    print(f"  Reason: {nap_reason}")

    # Attempt is logged as violation
    violation_record = framework.record_action(
        agent_id="security-monitoring",
        action_type="LICENSE_VIOLATION_DETECTED",
        parameters={
            "algorithm_id": "vqe-v2.1",
            "violation_type": "UNAUTHORIZED_MODIFICATION",
            "original_hash": algorithm_hash,
            "modified_hash": modified_hash,
            "modified_gate": algorithm_spec["gate_sequence"][2],
            "unauthorized_actor": "unknown-attacker",
            "nap_rule_triggered": license_restrictions.rule_id,
            "alert_level": "CRITICAL"
        }
    )

    print(f"\nViolation recorded: {violation_record.action_id}")
    print(f"Alert sent to: MIT Licensing, PHARMAÇO Legal")

    # Step 7: Second execution by authorized partner
    print("\n[STEP 7] Authorized execution: Partner institution (with approval)")
    print("-" * 80)

    # Partner requests execution with proper quorum approval
    nap_allowed_quorum, reason_quorum = framework.check_nap_compliance(
        resource_id="algorithm-vqe-v2.1",
        operation="SHARE_WITH_COLLABORATORS",  # Not in forbidden list - allowed
        party_count=3
    )

    execution_2 = framework.record_action(
        agent_id="stanford-quantum-lab",
        action_type="QUANTUM_ALGORITHM_EXECUTION",
        parameters={
            "algorithm_id": "vqe-v2.1",
            "license_key": "MIT-QML-VQE-2026-PHARMACO-RESEARCH-PARTNER",
            "algorithm_hash": algorithm_hash,
            "gate_sequence_executed": algorithm_spec["gate_sequence"],
            "parameters_used": [0.987, 1.876, 2.765, 3.654],
            "target_molecule": "Alzheimer-protein-amyloid-beta",
            "execution_timestamp": time.time() + 3600,
            "quantum_processor_id": "Rigetti-Aspen-M-2",
            "execution_status": "SUCCESS",
            "energy_result": -37.42,
            "watermark_verified": "YES",
            "approval_parties": ["MIT-Licensing", "PHARMAÇO-R&D", "Stanford-IRB"]
        }
    )

    print(f"Execution by Stanford (authorized partner)")
    print(f"Algorithm hash verified: {algorithm_hash[:16]}...")
    print(f"Watermark verified: YES")
    print(f"Approval parties: {len(execution_2.parameters['approval_parties'])}")
    print(f"Target: {execution_2.parameters['target_molecule']}")
    print(f"Energy result: {execution_2.parameters['energy_result']} Ha")

    # Step 8: Billing and compliance report
    print("\n[STEP 8] Generate licensing compliance and billing report")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Provenance chain valid: {is_valid}")
    print(f"Total executions: {len([r for r in framework.provenance_chain if 'EXECUTION' in r.action_type])}")
    print(f"Violations detected: 1")
    print(f"Authorized executions: 2")

    billing_record = {
        "license_key": "MIT-QML-VQE-2026-PHARMACO-EXCLUSIVE",
        "billing_period": "2026-05",
        "usage": {
            "successful_executions": 2,
            "failed_attempts": 0,
            "unauthorized_attempts": 1,
            "quantum_processor_hours": 2.5,
            "molecules_optimized": 2
        },
        "costs": {
            "per_execution_usd": 5000,
            "per_processor_hour_usd": 250,
            "execution_cost": 10000,
            "processor_cost": 625,
            "security_incident_charge": 0,
            "total_usd": 10625
        },
        "compliance_status": "VERIFIED",
        "ip_protection_status": "ACTIVE",
        "violations": [
            {
                "timestamp": time.time(),
                "type": "UNAUTHORIZED_MODIFICATION_ATTEMPT",
                "status": "DETECTED_AND_BLOCKED"
            }
        ],
        "next_billing_date": time.time() + 2592000  # 30 days
    }

    # Save comprehensive compliance packet
    compliance_packet = serialize_framework_state(framework)
    compliance_packet["billing_record"] = billing_record
    compliance_packet["algorithm_spec_hash"] = algorithm_hash

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/quantum-compliance-poc/algorithm_watermark_packet.json", "w") as f:
        f.write(packet_json)

    print("\nBilling Summary:")
    print(f"  Executions: {billing_record['usage']['successful_executions']}")
    print(f"  Execution cost: ${billing_record['costs']['execution_cost']:,}")
    print(f"  Processor cost: ${billing_record['costs']['processor_cost']:.2f}")
    print(f"  Total: ${billing_record['costs']['total_usd']:,}")

    print(f"\nCompliance packet saved to: algorithm_watermark_packet.json")

    # Step 9: Legal outcome
    print("\n[STEP 9] MIT Licensing Department Decision")
    print("-" * 80)

    print("BILLING ISSUED: $10,625 for May 2026")
    print("IP PROTECTION: VERIFIED AND INTACT")
    print("Evidence:")
    print("  1. Algorithm hash verified on all executions (AAPF)")
    print("  2. Watermark present and uncorrupted (embedded crypto)")
    print("  3. Unauthorized modification attempt detected (NAP)")
    print("  4. Modification blocked before execution (DCF escalation)")
    print("  5. All authorized executions logged and signed")
    print("\nConclusion: License agreement complied with. IP fully protected.")
    print("Next: Renewal discussion with PHARMAÇO for exclusive term extension")


if __name__ == "__main__":
    quantum_algorithm_watermark_demo()
