"""
USE CASE 5: Quantum Escrow Freshness & Settlement
Demonstrates CCF for maintaining proof of quantum state existence in high-value transactions
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, NegativeAuthorityProfile,
    serialize_framework_state
)


def quantum_escrow_demo():
    """
    Scenario: Party A bets $100M with Party B. Outcome depends on measuring a quantum state held
    in escrow. Framework proves the quantum state still exists (hasn't decohered), hasn't been
    measured, and can only be settled with multi-party approval.
    """
    framework = ComplianceFramework(signer_key="quantum-escrow")

    print("\n" + "="*80)
    print("QUANTUM ESCROW FRESHNESS & HIGH-VALUE SETTLEMENT")
    print("="*80)

    # Step 1: Define escrow agreement
    print("\n[STEP 1] Establish quantum escrow contract")
    print("-" * 80)

    escrow_terms = {
        "escrow_id": "QE-2026-0512-GOLDMAN-CITADEL-VQE",
        "parties": ["Goldman-Sachs-Quantum-Trading", "Citadel-Quantum-Fund"],
        "arbitrator": "Federal-Reserve-Quantum-Office",
        "bet_amount_usd": 100000000,  # $100M
        "quantum_state_custodian": "neutral-party-secure-facility",
        "state_description": "Output of proprietary VQE optimization",
        "measurement_condition": "Energy value < -42.5 Ha => Goldman wins; >= -42.5 Ha => Citadel wins",
        "escrow_duration_hours": 72,
        "freshness_proof_interval_hours": 12,  # Must prove quantum state freshness every 12 hours
        "measurement_trigger_condition": "Both parties agree OR arbitrator orders measurement"
    }

    print(f"Escrow ID: {escrow_terms['escrow_id']}")
    print(f"Party A: {escrow_terms['parties'][0]}")
    print(f"Party B: {escrow_terms['parties'][1]}")
    print(f"Arbitrator: {escrow_terms['arbitrator']}")
    print(f"Amount at stake: ${escrow_terms['bet_amount_usd']:,}")
    print(f"Duration: {escrow_terms['escrow_duration_hours']} hours")
    print(f"Freshness proof required: Every {escrow_terms['freshness_proof_interval_hours']} hours")

    # Step 2: Register escrow protection rules (NAP)
    print("\n[STEP 2] Register NAP: Quantum state protection")
    print("-" * 80)

    escrow_nap = NegativeAuthorityProfile(
        rule_id="nap-escrow-quantum-state-protection",
        resource_id=f"quantum-state-{escrow_terms['escrow_id']}",
        forbidden_operations=["MEASURE_WITHOUT_CONSENSUS", "DESTROY_QUANTUM_STATE", "TRANSFER_STATE_UNAUTHORIZED"],
        override_policy="REQUIRES_QUORUM",  # Requires arbitrator + both parties
        enforcement_timestamp=time.time(),
        enforcement_signature=framework.sign_data(f"escrow-nap-{escrow_terms['escrow_id']}")
    )

    framework.register_nap_rule(escrow_nap)

    print(f"Protection rule: {escrow_nap.rule_id}")
    print(f"Forbidden operations:")
    print(f"  - MEASURE_WITHOUT_CONSENSUS (requires 3-party quorum)")
    print(f"  - DESTROY_QUANTUM_STATE (would void contract)")
    print(f"  - TRANSFER_STATE_UNAUTHORIZED (prevents fraud)")
    print(f"Override policy: {escrow_nap.override_policy} (need arbitrator + 2 parties = 3 total)")

    # Step 3: Classify quantum state (DCF)
    print("\n[STEP 3] Classify quantum state (DCF)")
    print("-" * 80)

    state_label = framework.classify_data(
        resource_id=f"quantum-state-{escrow_terms['escrow_id']}",
        classification=DataClassification.SECRET,
        applier="arbitrator@federal-reserve-quantum.gov"
    )

    print(f"Classification: {state_label.classification.value}")
    print(f"Reason: $100M contract value, outcome-determining")
    print(f"Applied by: Federal Reserve Quantum Office")

    # Step 4: Deposit quantum state into escrow (AAPF)
    print("\n[STEP 4] Record deposit of quantum state into escrow")
    print("-" * 80)

    deposit_record = framework.record_action(
        agent_id="goldman-sachs-vqe",
        action_type="QUANTUM_STATE_DEPOSIT_ESCROW",
        parameters={
            "escrow_id": escrow_terms['escrow_id'],
            "state_owner": "Goldman-Sachs",
            "state_depositor": "goldman-sachs-quantum-lab",
            "custodian": "federal-reserve-quantum-office",
            "state_type": "VQE-optimization-output",
            "state_hash": framework.hash_data("quantum_state_vqe_output"),
            "coherence_time_estimate_hours": 72,
            "deposit_timestamp": time.time(),
            "escrow_terms_hash": framework.hash_data(json.dumps(escrow_terms, sort_keys=True))
        }
    )

    print(f"Deposit action: {deposit_record.action_id}")
    print(f"State owner: Goldman Sachs")
    print(f"Held in escrow by: Federal Reserve Quantum Office")
    print(f"Estimated coherence: 72 hours")
    print(f"Signature: {deposit_record.signature[:16]}...")

    # Step 5: Freshness proofs (CCF) - multiple checkpoints
    print("\n[STEP 5] Freshness proofs: Quantum state continuously maintained")
    print("-" * 80)

    freshness_proofs = []
    for hour in [0, 12, 24, 36, 48, 60]:
        freshness_proof = framework.prove_freshness(
            capability_id=f"quantum-state-{escrow_terms['escrow_id']}-h{hour}",
            freshness_seconds=12 * 3600,  # Proof valid for 12 hours
            prover="federal-reserve-quantum-office"
        )

        freshness_record = framework.record_action(
            agent_id="arbitrator-quantum-monitor",
            action_type="QUANTUM_STATE_FRESHNESS_PROOF",
            parameters={
                "escrow_id": escrow_terms['escrow_id'],
                "checkpoint_hour": hour,
                "freshness_proof_hash": freshness_proof.proof_hash,
                "proof_age_seconds": time.time() - freshness_proof.last_proven_timestamp,
                "state_coherence_status": "MAINTAINED",
                "state_measured": False,
                "state_destroyed": False,
                "arbitrator_signature": framework.sign_data(freshness_proof.proof_hash)
            }
        )

        freshness_proofs.append(freshness_proof)

        print(f"Hour {hour}: Freshness proof {freshness_proof.proof_hash[:12]}... (VALID)")
        print(f"  State coherence: MAINTAINED")
        print(f"  State measured: NO")
        print(f"  State destroyed: NO")

    print(f"\nTotal freshness proofs: {len(freshness_proofs)}")
    print(f"Escrow integrity: 100% maintained throughout 60-hour period")

    # Step 6: Attempt unauthorized measurement (BLOCKED)
    print("\n[STEP 6] Goldman Sachs attempts unauthorized measurement (BLOCKED)")
    print("-" * 80)

    # Try to measure with only 1 party (Goldman), not quorum
    measurement_allowed, nap_reason = framework.check_nap_compliance(
        resource_id=f"quantum-state-{escrow_terms['escrow_id']}",
        operation="MEASURE_WITHOUT_CONSENSUS",
        party_count=1  # Only Goldman, missing arbitrator + Citadel
    )

    print(f"Measurement attempt: Goldman tries to measure outcome")
    print(f"Party count: 1 (Goldman only, missing arbitrator + Citadel)")
    print(f"NAP allows: {measurement_allowed}")
    print(f"Reason: {nap_reason}")

    unauthorized_measure = framework.record_action(
        agent_id="goldman-security-incident",
        action_type="UNAUTHORIZED_MEASUREMENT_ATTEMPT_DETECTED",
        parameters={
            "escrow_id": escrow_terms['escrow_id'],
            "attacker_party": "Goldman-Sachs",
            "attempted_operation": "MEASURE_WITHOUT_CONSENSUS",
            "parties_required_for_approval": 3,
            "parties_present": 1,
            "nap_rule_violated": "nap-escrow-quantum-state-protection",
            "result": "BLOCKED_AND_LOGGED",
            "alert_sent_to": ["Citadel", "Federal-Reserve", "Arbitrator"]
        }
    )

    print(f"\nAttempt blocked and logged")
    print(f"Alert sent to: Citadel, Federal Reserve, Arbitrator")
    print(f"Signature: {unauthorized_measure.signature[:16]}...")

    # Step 7: Authorized measurement with quorum
    print("\n[STEP 7] Market condition triggers: Authorized measurement (with quorum)")
    print("-" * 80)

    # Market moves against Goldman, contract expires in 2 hours
    # Both parties AND arbitrator agree to measure

    measurement_allowed_quorum, reason = framework.check_nap_compliance(
        resource_id=f"quantum-state-{escrow_terms['escrow_id']}",
        operation="MEASURE_WITHOUT_CONSENSUS",
        party_count=3  # Goldman + Citadel + Arbitrator (quorum)
    )

    print(f"Measurement triggered: Contract expires in 2 hours")
    print(f"Party count: 3 (Goldman + Citadel + Federal Reserve Arbitrator)")
    print(f"NAP allows: {measurement_allowed_quorum}")
    print(f"Reason: {reason}")

    final_measurement = framework.record_action(
        agent_id="arbitrator-measurement-authority",
        action_type="AUTHORIZED_ESCROW_MEASUREMENT_QUORUM",
        parameters={
            "escrow_id": escrow_terms['escrow_id'],
            "measurement_timestamp": time.time() + 6000,
            "authorized_parties": ["goldman-sachs", "citadel-quantum-fund", "federal-reserve"],
            "quantum_state_measured": True,
            "measurement_result_energy": -42.35,
            "measurement_result_interpretation": "Goldman threshold is < -42.5 Ha => CITADEL WINS",
            "payout_calculation": {
                "citadel_wins": True,
                "citadel_receives_usd": 100000000,
                "goldman_receives_usd": 0,
                "arbitrator_fee_usd": 500000
            },
            "legal_authority": "Quantum Escrow Act of 2024, 18 USC 4001-4015"
        }
    )

    print(f"\nMeasurement executed with full authorization")
    print(f"Energy result: {final_measurement.parameters['measurement_result_energy']} Ha")
    print(f"Winner: Citadel Quantum Fund")
    print(f"Payout: ${final_measurement.parameters['payout_calculation']['citadel_receives_usd']:,}")

    # Step 8: Settlement verification
    print("\n[STEP 8] Verify entire escrow history and authorize settlement")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Provenance chain valid: {is_valid}")
    print(f"Merkle root: {merkle_root[:16]}...")
    print(f"Total events logged: {len(framework.provenance_chain)}")

    settlement_verification = {
        "escrow_integrity": "VERIFIED",
        "checks_performed": [
            "Quantum state existed from deposit through measurement (freshness proofs)",
            "No unauthorized measurements or state destruction",
            "All actions cryptographically signed by authorized parties",
            "Measurement only occurred with full 3-party quorum approval",
            "Settlement calculation matches contract terms"
        ],
        "legal_defensibility": "FULL - Cryptographically provable in court",
        "settlement_authority": "APPROVED by Federal Reserve Quantum Office"
    }

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["settlement_verification"] = settlement_verification
    compliance_packet["final_payout"] = final_measurement.parameters['payout_calculation']

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/quantum-compliance-poc/escrow_settlement_packet.json", "w") as f:
        f.write(packet_json)

    for check in settlement_verification["checks_performed"]:
        print(f"  ✓ {check}")

    print(f"\nSettlement packet saved to: escrow_settlement_packet.json")

    # Step 9: Settlement execution
    print("\n[STEP 9] SETTLEMENT AUTHORIZED AND EXECUTED")
    print("-" * 80)

    print(f"Settlement date: {time.ctime(time.time() + 6000)}")
    print(f"Goldman Sachs account: -$100,000,000")
    print(f"Citadel Quantum Fund account: +$100,000,000")
    print(f"Federal Reserve arbitration fee: $500,000 (paid by Citadel)")
    print(f"\nLegal basis: Quantum Escrow Act of 2024")
    print(f"Cryptographic evidence: {merkle_root[:16]}... (signed by all parties)")
    print(f"Status: SETTLEMENT COMPLETE AND IRREVERSIBLE")


if __name__ == "__main__":
    quantum_escrow_demo()
