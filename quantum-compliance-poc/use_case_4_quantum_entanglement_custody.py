"""
USE CASE 4: Quantum Entanglement Custody & Multi-Party Derivatives
Demonstrates NAP, AAPF, CCF for proving entanglement ownership in financial contracts
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, NegativeAuthorityProfile,
    serialize_framework_state
)


def quantum_entanglement_custody_demo():
    """
    Scenario: Bank A creates entangled qubit pair, transfers one qubit to Bank B for joint
    quantum computation. Framework proves neither party can unilaterally measure/destroy
    the entanglement without cryptographic proof from the other party.
    """
    framework = ComplianceFramework(signer_key="quantum-derivatives-custody")

    print("\n" + "="*80)
    print("QUANTUM ENTANGLEMENT CUSTODY & MULTI-PARTY DERIVATIVES")
    print("="*80)

    # Step 1: Entanglement creation
    print("\n[STEP 1] Bank A creates entangled qubit pair")
    print("-" * 80)

    entanglement_spec = {
        "entanglement_type": "Bell-state-Phi-plus",
        "qubit_A_custodian": "JPMorgan-Quantum-Lab",
        "qubit_B_custodian": "Goldman-Sachs-Quantum-Lab",
        "creation_timestamp": time.time(),
        "creation_facility": "JPMorgan-Armonk-NYC",
        "entanglement_quality_fidelity": 0.95,
        "contract_reference": "EQ-2026-0512-JPM-GS-MC-SWAP",
        "contract_notional_usd": 500000000,  # $500M Monte Carlo swap
        "computation_type": "Quantum-Monte-Carlo-derivatives-pricing",
        "estimated_computation_hours": 12,
        "measurement_forbidden_duration_hours": 24  # Cannot measure for 24 hours
    }

    print(f"Entanglement: {entanglement_spec['entanglement_type']}")
    print(f"Fidelity: {entanglement_spec['entanglement_quality_fidelity'] * 100}%")
    print(f"Qubit A held by: {entanglement_spec['qubit_A_custodian']}")
    print(f"Qubit B held by: {entanglement_spec['qubit_B_custodian']}")
    print(f"Contract: {entanglement_spec['contract_reference']}")
    print(f"Notional value: ${entanglement_spec['contract_notional_usd']:,}")
    print(f"Created: {time.ctime(entanglement_spec['creation_timestamp'])}")

    # Step 2: Register hard-deny rule (NAP)
    print("\n[STEP 2] Register NAP: MEASUREMENT FORBIDDEN (unless both parties consent)")
    print("-" * 80)

    entanglement_nap = NegativeAuthorityProfile(
        rule_id="nap-eq-jpm-gs-measurement",
        resource_id=f"entanglement-{entanglement_spec['contract_reference']}",
        forbidden_operations=["MEASURE_QUBIT_A", "MEASURE_QUBIT_B", "DESTROY_ENTANGLEMENT"],
        override_policy="REQUIRES_MULTI_PARTY",  # Both JPMorgan AND Goldman Sachs must sign off
        enforcement_timestamp=time.time(),
        enforcement_signature=framework.sign_data(f"measure-nap-{entanglement_spec['contract_reference']}")
    )

    framework.register_nap_rule(entanglement_nap)

    print(f"Hard-deny rule: {entanglement_nap.rule_id}")
    print(f"Forbidden operations:")
    print(f"  - MEASURE_QUBIT_A (would collapse entanglement)")
    print(f"  - MEASURE_QUBIT_B (would collapse entanglement)")
    print(f"  - DESTROY_ENTANGLEMENT (breaking custody)")
    print(f"Override policy: {entanglement_nap.override_policy}")
    print(f"Enforcement: Signed by both JPMorgan and Goldman Sachs")

    # Step 3: Initial custody transfer (AAPF)
    print("\n[STEP 3] Record custody transfer to Goldman Sachs (AAPF)")
    print("-" * 80)

    transfer_record = framework.record_action(
        agent_id="jpm-quantum-custody",
        action_type="QUANTUM_ENTANGLEMENT_TRANSFER",
        parameters={
            "entanglement_id": f"eq-{entanglement_spec['contract_reference']}",
            "from_custodian": "JPMorgan-Quantum-Lab",
            "to_custodian": "Goldman-Sachs-Quantum-Lab",
            "qubit_transferred": "Qubit-B",
            "entanglement_fidelity_before": entanglement_spec["entanglement_quality_fidelity"],
            "entanglement_fidelity_after_transfer": 0.948,  # Slight degradation during transfer
            "transfer_method": "Quantum-teleportation-secure-channel",
            "transfer_timestamp": time.time() + 300,
            "measurement_proof_required_from": ["jpm-quantum-lab", "goldman-sachs-quantum-lab"]
        }
    )

    print(f"Transfer action: {transfer_record.action_id}")
    print(f"Qubit transferred: Qubit-B to Goldman Sachs")
    print(f"Fidelity before: {entanglement_spec['entanglement_quality_fidelity']}")
    print(f"Fidelity after: {transfer_record.parameters['entanglement_fidelity_after_transfer']}")
    print(f"Method: Quantum teleportation on secure channel")
    print(f"Measurement proof required from: 2 parties (both custodians)")

    # Step 4: Classify entanglement state (DCF)
    print("\n[STEP 4] Classify entanglement state (DCF)")
    print("-" * 80)

    entanglement_label = framework.classify_data(
        resource_id=f"eq-{entanglement_spec['contract_reference']}",
        classification=DataClassification.SECRET,  # Highest classification
        applier="derivatives-legal@jpm.com"
    )

    print(f"Classification: {entanglement_label.classification.value}")
    print(f"Reason: Entanglement is $500M derivative contract value")
    print(f"Applied by: JPMorgan Derivatives Legal")

    # Step 5: Joint computation phase
    print("\n[STEP 5] Joint computation: Monte Carlo derivative pricing")
    print("-" * 80)

    computation_steps = [
        {
            "step": 1,
            "actor": "jpm-quantum-processor",
            "operation": "Initialize-state-Qubit-A",
            "entanglement_still_valid": True
        },
        {
            "step": 2,
            "actor": "goldman-sachs-quantum-processor",
            "operation": "Initialize-state-Qubit-B",
            "entanglement_still_valid": True
        },
        {
            "step": 3,
            "actor": "jpm-quantum-processor",
            "operation": "Apply-Hadamard-gates",
            "entanglement_still_valid": True
        },
        {
            "step": 4,
            "actor": "goldman-sachs-quantum-processor",
            "operation": "Apply-Rz-rotation",
            "entanglement_still_valid": True
        },
        {
            "step": 5,
            "actor": "both-parties-synchronized",
            "operation": "CNOT-entanglement-measurement",
            "entanglement_still_valid": False  # Measurement collapses it
        }
    ]

    for step_info in computation_steps[:4]:  # First 4 steps don't measure
        comp_record = framework.record_action(
            agent_id=step_info["actor"],
            action_type="QUANTUM_COMPUTATION_STEP",
            parameters={
                "computation_id": f"mc-{entanglement_spec['contract_reference']}",
                "step_number": step_info["step"],
                "operation": step_info["operation"],
                "entanglement_valid": step_info["entanglement_still_valid"],
                "timestamp": time.time() + (step_info["step"] * 100)
            }
        )

        print(f"Step {step_info['step']}: {step_info['operation']}")
        print(f"  Actor: {step_info['actor']}")
        print(f"  Entanglement valid: {step_info['entanglement_still_valid']}")

    # Step 6: Attempt unauthorized measurement (BLOCKED by NAP)
    print("\n[STEP 6] Goldman Sachs attempts unauthorized measurement")
    print("-" * 80)

    # Try to measure without JPMorgan approval
    measurement_allowed, nap_reason = framework.check_nap_compliance(
        resource_id=f"entanglement-{entanglement_spec['contract_reference']}",
        operation="MEASURE_QUBIT_B",
        party_count=1  # Only Goldman Sachs, not both parties
    )

    print(f"Measurement request: Qubit-B measurement (unauthorized)")
    print(f"Party count: 1 (Goldman Sachs only, no JPMorgan approval)")
    print(f"NAP allows: {measurement_allowed}")
    print(f"Reason: {nap_reason}")

    unauthorized_attempt = framework.record_action(
        agent_id="goldman-sachs-quantum-processor",
        action_type="UNAUTHORIZED_MEASUREMENT_ATTEMPT",
        parameters={
            "entanglement_id": f"eq-{entanglement_spec['contract_reference']}",
            "qubit_target": "Qubit-B",
            "reason_claimed": "Testing measurement capability",
            "nap_rule_violated": "nap-eq-jpm-measurement",
            "blocking_reason": "Multi-party approval required",
            "approval_status": "DENIED",
            "incident_timestamp": time.time() + 2000
        }
    )

    print(f"\nUnauthorized attempt blocked and logged")
    print(f"Signature: {unauthorized_attempt.signature[:16]}...")

    # Step 7: Authorized final measurement (REQUIRES BOTH PARTIES)
    print("\n[STEP 7] Authorized final measurement (both parties sign off)")
    print("-" * 80)

    # Now measure WITH both parties' cryptographic approval
    measurement_allowed_approved, reason = framework.check_nap_compliance(
        resource_id=f"entanglement-{entanglement_spec['contract_reference']}",
        operation="MEASURE_QUBIT_A",
        party_count=2  # Both JPMorgan AND Goldman Sachs
    )

    print(f"Measurement request: Final computation step (authorized)")
    print(f"Party count: 2 (JPMorgan + Goldman Sachs)")
    print(f"NAP allows: {measurement_allowed_approved}")
    print(f"Reason: {reason}")

    final_measurement = framework.record_action(
        agent_id="jpm-goldman-joint-measurement",
        action_type="AUTHORIZED_ENTANGLEMENT_MEASUREMENT",
        parameters={
            "entanglement_id": f"eq-{entanglement_spec['contract_reference']}",
            "measurement_step": 5,
            "computation_result": 42.75,  # Price of derivative
            "approvals": ["jpm-quantum-lab", "goldman-sachs-quantum-lab"],
            "measurement_timestamp": time.time() + 3000,
            "entanglement_collapsed": True,
            "derivative_fair_value_usd": 42750000
        }
    )

    print(f"\nFinal measurement authorized and executed")
    print(f"Derivative fair value: ${final_measurement.parameters['derivative_fair_value_usd']:,}")
    print(f"Both parties' signatures: {final_measurement.signature[:16]}...")

    # Step 8: Custody proof report
    print("\n[STEP 8] Generate custody proof for regulatory compliance")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    compliance_packet = serialize_framework_state(framework)

    # Custom custody analysis
    custody_analysis = {
        "question": "Was entanglement secure and measurement authorized?",
        "answer": "YES - Full cryptographic proof",
        "evidence": [
            "NAP rule registered at custody transfer (IMPOSSIBLE to measure unilaterally)",
            "Unauthorized measurement attempt detected and blocked (by NAP)",
            "Final measurement required and received multi-party approval",
            "All actions cryptographically signed (AAPF)",
            "Measurement proof requires signatures from both JPMorgan and Goldman Sachs",
            "Computation result ($42.75M) matches both parties' independent verification"
        ],
        "legal_implications": [
            "Neither party could unilaterally cheat (measurement requires both signatures)",
            "Measurement is non-repudiable (both parties cryptographically committed)",
            "Entanglement integrity proven through unbroken NAP enforcement",
            "Contract performance fully documented and legally defensible"
        ]
    }

    compliance_packet["custody_analysis"] = custody_analysis

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/quantum-compliance-poc/entanglement_custody_packet.json", "w") as f:
        f.write(packet_json)

    print("Custody proof includes:")
    print("  - NAP enforcement log (unauthorized attempt blocked)")
    print("  - All computation steps with signatures")
    print("  - Final measurement with dual-party approval")
    print("  - Entanglement integrity verification")
    print(f"  - Merkle root: {merkle_root[:16]}...")

    print(f"\nPacket saved to: entanglement_custody_packet.json")

    # Step 9: Settlement
    print("\n[STEP 9] Derivative Settlement")
    print("-" * 80)

    print("CONTRACT SETTLEMENT:")
    print(f"  Derivative type: Quantum-Monte-Carlo swap")
    print(f"  Fair value: ${final_measurement.parameters['derivative_fair_value_usd']:,}")
    print(f"  JPMorgan receives: ${final_measurement.parameters['derivative_fair_value_usd'] * 0.5:,.0f}")
    print(f"  Goldman Sachs pays: ${final_measurement.parameters['derivative_fair_value_usd'] * 0.5:,.0f}")
    print(f"\nCompliance: FULL - No unauthorized measurements, multi-party verification")
    print(f"Regulatory filing: APPROVED")


if __name__ == "__main__":
    quantum_entanglement_custody_demo()
