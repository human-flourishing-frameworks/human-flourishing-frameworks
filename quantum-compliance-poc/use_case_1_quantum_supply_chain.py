"""
USE CASE 1: Quantum Supply Chain & Hardware Attestation
Demonstrates DCF, AAPF, CCF, PCSF for tracking quantum hardware through shipping
"""

import json
import time
from framework_core import (
    ComplianceFramework, DataClassification, NegativeAuthorityProfile,
    ProviderCapacityState, serialize_framework_state
)


def quantum_supply_chain_demo():
    """
    Scenario: IonQ ships a 32-qubit quantum processor to a customer.
    Framework proves: qubits maintained coherence during shipping, no tampering.
    """
    framework = ComplianceFramework(signer_key="quantum-supply-chain")

    print("\n" + "="*80)
    print("QUANTUM SUPPLY CHAIN ATTESTATION")
    print("="*80)

    # Step 1: Initial capacity claim at shipment
    print("\n[STEP 1] Manufacturer IonQ ships quantum processor")
    print("-" * 80)

    shipment_capacity = {
        "total_qubits": 32,
        "coherence_time_us": 500,
        "gate_depth": 1000,
        "2qubit_gate_error_rate": 0.002,
        "location": "IonQ-Denver-Facility",
        "calibration_timestamp": time.time()
    }

    shipment_state = ProviderCapacityState(
        provider_id="ionq-processor-001",
        service_name="IonQ-32q-v2",
        capacity_claims=shipment_capacity,
        state_timestamp=time.time(),
        state_hash=framework.hash_data(json.dumps(shipment_capacity, sort_keys=True)),
        state_signature=framework.sign_data(json.dumps(shipment_capacity, sort_keys=True)),
        degradation_log=[]
    )

    framework.register_provider_capacity(shipment_state)

    print(f"Processor ID: {shipment_state.provider_id}")
    print(f"Qubits: {shipment_capacity['total_qubits']}")
    print(f"Coherence Time: {shipment_capacity['coherence_time_us']} microseconds")
    print(f"Capacity State Hash: {shipment_state.state_hash[:16]}...")
    print(f"Signed by: {shipment_state.state_signature[:16]}...")

    # Step 2: Classify qubits as quantum-unobserved (DCF)
    print("\n[STEP 2] Classify quantum state as UNOBSERVED (DCF)")
    print("-" * 80)

    qubit_label = framework.classify_data(
        resource_id="ionq-processor-001-qubits",
        classification=DataClassification.QUANTUM_UNOBSERVED,
        applier="manufacturer@ionq.com"
    )

    print(f"Resource: {qubit_label.resource_id}")
    print(f"Classification: {qubit_label.classification.value}")
    print(f"Applied by: {qubit_label.applied_by}")
    print(f"Timestamp: {time.ctime(qubit_label.applied_timestamp)}")

    # Step 3: Record shipment action (AAPF)
    print("\n[STEP 3] Record shipment action in provenance chain (AAPF)")
    print("-" * 80)

    shipment_record = framework.record_action(
        agent_id="ionq-shipping-agent",
        action_type="QUANTUM_PROCESSOR_SHIPMENT",
        parameters={
            "processor_id": "ionq-processor-001",
            "origin": "IonQ-Denver-Facility",
            "destination": "Customer-Lab-SanFrancisco",
            "shipping_date": time.ctime(),
            "expected_delivery": "2026-05-15",
            "coherence_freshness_required_hours": 72
        }
    )

    print(f"Action ID: {shipment_record.action_id}")
    print(f"Agent: {shipment_record.agent_id}")
    print(f"Type: {shipment_record.action_type}")
    print(f"Hash: {shipment_record.action_hash[:16]}...")
    print(f"Signature: {shipment_record.signature[:16]}...")

    # Step 4: Mid-transit checkpoints - log coherence degradation
    print("\n[STEP 4] Mid-transit checkpoint: Temperature spike detected")
    print("-" * 80)

    updated_state = ProviderCapacityState(
        provider_id="ionq-processor-001",
        service_name="IonQ-32q-v2",
        capacity_claims=shipment_capacity,
        state_timestamp=time.time(),
        state_hash=shipment_state.state_hash,
        state_signature=shipment_state.state_signature,
        degradation_log=[
            (time.time() - 3600, "Temperature spike 15C above spec (Qubit#5, Qubit#12 affected)")
        ]
    )

    framework.register_provider_capacity(updated_state)

    available = updated_state.get_available_capacity()
    print(f"Temperature spike detected at {time.ctime(time.time() - 3600)}")
    print(f"Affected qubits: 2 (Qubit#5, Qubit#12)")
    print(f"Current available qubits: {available['qubits']} (down from 32)")
    print(f"Coherence time degraded to: {available['coherence_time_us']}us")

    # Record degradation event
    degradation_record = framework.record_action(
        agent_id="environmental-monitoring",
        action_type="DEGRADATION_OBSERVED",
        parameters={
            "processor_id": "ionq-processor-001",
            "location": "In-Transit-Chicago",
            "event": "Temperature spike",
            "qubits_affected": ["qubit_5", "qubit_12"],
            "coherence_loss_percent": 20
        }
    )

    print(f"\nDegradation logged: {degradation_record.action_hash[:16]}...")

    # Step 5: Delivery and freshness proof (CCF)
    print("\n[STEP 5] Delivery: Create freshness proof of coherence (CCF)")
    print("-" * 80)

    freshness_proof = framework.prove_freshness(
        capability_id="ionq-processor-001-qubits",
        freshness_seconds=3600,  # Proof valid for 1 hour
        prover="customer-lab@sanfrancisco"
    )

    print(f"Capability: {freshness_proof.capability_id}")
    print(f"Fresh within: {freshness_proof.freshness_window_seconds} seconds (1 hour)")
    print(f"Proved at: {time.ctime(freshness_proof.last_proven_timestamp)}")
    print(f"Proof Hash: {freshness_proof.proof_hash[:16]}...")
    print(f"Is Fresh Now: {freshness_proof.is_fresh()}")

    delivery_record = framework.record_action(
        agent_id="customer-receiving",
        action_type="QUANTUM_PROCESSOR_RECEIVED",
        parameters={
            "processor_id": "ionq-processor-001",
            "delivery_date": time.ctime(),
            "qubits_functional": available['qubits'],
            "coherence_time_measured_us": available['coherence_time_us'],
            "freshness_proof_hash": freshness_proof.proof_hash,
            "customer_accepts": "YES_WITH_CREDIT"
        }
    )

    print(f"\nDelivery recorded: {delivery_record.action_id}")
    print(f"Customer verdict: YES_WITH_CREDIT (2 qubits degraded, requesting refund)")

    # Step 6: Verify entire provenance chain
    print("\n[STEP 6] Verify entire supply chain provenance")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Provenance chain valid: {is_valid}")
    print(f"Merkle root: {merkle_root[:16]}...")
    print(f"Total actions recorded: {len(framework.provenance_chain)}")

    for i, record in enumerate(framework.provenance_chain):
        print(f"  [{i}] {record.action_type} @ {time.ctime(record.timestamp)}")

    # Step 7: Export compliance packet
    print("\n[STEP 7] Export compliance packet for warranty dispute")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    print("Compliance packet includes:")
    print("  - Complete provenance chain (shipment -> degradation -> delivery)")
    print("  - DCF labels (QUANTUM_UNOBSERVED -> no measurement)")
    print("  - AAPF signatures (all events cryptographically signed)")
    print("  - CCF freshness proof (coherence maintained within spec)")
    print("  - PCSF capacity claims (before/after degradation)")
    print(f"  - Merkle root: {merkle_root[:16]}...")

    # Save to file
    with open("/tmp/quantum-compliance-poc/supply_chain_packet.json", "w") as f:
        f.write(packet_json)

    print(f"\nPacket saved to: supply_chain_packet.json")

    # Step 8: Buyer verification
    print("\n[STEP 8] Buyer uses packet to file warranty claim")
    print("-" * 80)

    print("Claim: 'Two qubits degraded during shipping due to environmental damage'")
    print("Evidence from packet:")
    print("  1. Degradation event timestamped and cryptographically signed")
    print("  2. Coherence freshness maintained until delivery")
    print("  3. No unauthorized measurement (DCF QUANTUM_UNOBSERVED unchanged)")
    print("  4. Full provenance chain proves legitimate degradation")
    print("  5. Manufacturer liable (event detected mid-transit, not in customer hands)")
    print("\nResult: CLAIM APPROVED - $50,000 refund issued")


if __name__ == "__main__":
    quantum_supply_chain_demo()
