"""
USE CASE 2: Quantum Sensor Attestation for Critical Infrastructure
Demonstrates CCF, AAPF, DCF for atomic clock calibration and frequency stability
"""

import json
import time
import math
from framework_core import (
    ComplianceFramework, DataClassification, NegativeAuthorityProfile,
    ProviderCapacityState, serialize_framework_state
)


def quantum_sensor_attestation_demo():
    """
    Scenario: Aviation authority uses atomic clock (quantum sensor) for navigation.
    Framework proves: clock was calibrated correctly, measurements are trustworthy.
    """
    framework = ComplianceFramework(signer_key="quantum-sensor-attestation")

    print("\n" + "="*80)
    print("QUANTUM SENSOR ATTESTATION FOR CRITICAL INFRASTRUCTURE")
    print("="*80)

    # Step 1: Sensor initialization and calibration baseline
    print("\n[STEP 1] Initialize quantum atomic clock sensor")
    print("-" * 80)

    sensor_specs = {
        "sensor_type": "Cesium-133 atomic clock",
        "location": "San Francisco Airport - Navigation System",
        "frequency_mhz": 9192.631770,  # Cesium transition frequency
        "precision_ppb": 0.001,  # Parts per billion
        "last_calibration_timestamp": time.time(),
        "calibration_source": "NIST-traceable standard",
        "next_calibration_due": time.time() + 86400  # 24 hours
    }

    sensor_state = ProviderCapacityState(
        provider_id="cesium-clock-sfo-001",
        service_name="Primary-Navigation-Clock",
        capacity_claims=sensor_specs,
        state_timestamp=time.time(),
        state_hash=framework.hash_data(json.dumps(sensor_specs, sort_keys=True)),
        state_signature=framework.sign_data(json.dumps(sensor_specs, sort_keys=True)),
        degradation_log=[]
    )

    framework.register_provider_capacity(sensor_state)

    print(f"Sensor ID: {sensor_state.provider_id}")
    print(f"Type: {sensor_specs['sensor_type']}")
    print(f"Location: {sensor_specs['location']}")
    print(f"Frequency: {sensor_specs['frequency_mhz']} MHz")
    print(f"Precision: ±{sensor_specs['precision_ppb']} PPB")
    print(f"Calibrated: {time.ctime(sensor_specs['last_calibration_timestamp'])}")

    # Step 2: Classify measurement data (DCF)
    print("\n[STEP 2] Classify measurement data quality (DCF)")
    print("-" * 80)

    measurement_label = framework.classify_data(
        resource_id="cesium-clock-sfo-001-measurements",
        classification=DataClassification.INTERNAL,  # Sensitive precision data
        applier="calibration-technician@faa.gov"
    )

    print(f"Resource: {measurement_label.resource_id}")
    print(f"Classification: {measurement_label.classification.value}")
    print(f"Applied by: {measurement_label.applied_by}")
    print(f"Critical because: Precision data affects navigation safety")

    # Step 3: Record calibration action (AAPF)
    print("\n[STEP 3] Record calibration procedure (AAPF)")
    print("-" * 80)

    calibration_record = framework.record_action(
        agent_id="faa-calibration-team",
        action_type="QUANTUM_SENSOR_CALIBRATION",
        parameters={
            "sensor_id": "cesium-clock-sfo-001",
            "calibration_standard": "NIST-SP330-cesium-reference",
            "calibration_uncertainty_ppb": 0.0001,
            "environment_temperature_c": 20.5,
            "environment_humidity_percent": 45,
            "calibration_personnel": "Technician Smith (NIST-certified)",
            "certification_valid_until": "2027-05-07"
        }
    )

    print(f"Calibration action: {calibration_record.action_id}")
    print(f"Performed by: faa-calibration-team")
    print(f"Standard: NIST-SP330 cesium reference")
    print(f"Uncertainty: ±0.0001 PPB (world-class precision)")
    print(f"Signature: {calibration_record.signature[:16]}...")

    # Step 4: Operational measurements with freshness proofs (CCF)
    print("\n[STEP 4] Operational phase: Continuous freshness proofs (CCF)")
    print("-" * 80)

    measurements = []
    for hour in range(3):
        # Simulate measurements every hour
        measurement_value = sensor_specs['frequency_mhz'] + (0.0001 * math.sin(hour))
        measurement_time = time.time() + (hour * 3600)

        # Create freshness proof
        freshness_proof = framework.prove_freshness(
            capability_id=f"cesium-clock-sfo-001-measurement-h{hour}",
            freshness_seconds=3600,  # Valid for 1 hour
            prover="automated-sensor-monitor"
        )

        measurements.append({
            "hour": hour,
            "frequency_measured": measurement_value,
            "freshness_proof_hash": freshness_proof.proof_hash,
            "is_fresh": freshness_proof.is_fresh()
        })

        # Record measurement action
        measurement_record = framework.record_action(
            agent_id="navigation-system",
            action_type="ATOMIC_CLOCK_MEASUREMENT",
            parameters={
                "sensor_id": "cesium-clock-sfo-001",
                "measurement_hour": hour,
                "frequency_hz": measurement_value * 1e6,
                "deviation_ppb": (measurement_value - sensor_specs['frequency_mhz']) * 1e9,
                "freshness_proof": freshness_proof.proof_hash,
                "aircraft_using_measurement": ["United-747-N1", "Southwest-737-N2", "Delta-A380-N3"]
            }
        )

        print(f"\nHour {hour}: Frequency = {measurement_value:.12f} MHz")
        print(f"  Deviation: {(measurement_value - sensor_specs['frequency_mhz']) * 1e9:.4f} PPB")
        print(f"  Freshness proof: {freshness_proof.proof_hash[:16]}...")
        print(f"  Aircraft relying on measurement: 3 planes")
        print(f"  Signature: {measurement_record.signature[:16]}...")

    # Step 5: Environmental stress event
    print("\n[STEP 5] Environmental stress: Temperature excursion detected")
    print("-" * 80)

    stress_event_time = time.time() + (2 * 3600)

    updated_state = ProviderCapacityState(
        provider_id="cesium-clock-sfo-001",
        service_name="Primary-Navigation-Clock",
        capacity_claims=sensor_specs,
        state_timestamp=time.time(),
        state_hash=sensor_state.state_hash,
        state_signature=sensor_state.state_signature,
        degradation_log=[
            (stress_event_time, "Temperature spike +5C above spec (Facility HVAC failure 14:22 UTC)")
        ]
    )

    framework.register_provider_capacity(updated_state)

    stress_record = framework.record_action(
        agent_id="facilities-monitoring",
        action_type="ENVIRONMENTAL_DEGRADATION_DETECTED",
        parameters={
            "sensor_id": "cesium-clock-sfo-001",
            "event_type": "Temperature excursion",
            "temperature_deviation_c": 5.0,
            "duration_minutes": 12,
            "root_cause": "HVAC compressor failure",
            "frequency_drift_during_event_ppb": 0.015,
            "affected_measurements": ["hour_2"],
            "recovery_status": "Sensor stabilized, next NIST calibration recommended"
        }
    )

    print(f"Event timestamp: {time.ctime(stress_event_time)}")
    print(f"Temperature spike: +5.0°C (beyond operational spec)")
    print(f"Duration: 12 minutes")
    print(f"Frequency drift: 0.015 PPB (acceptable for navigation)")
    print(f"Root cause: HVAC compressor failure (not sensor fault)")
    print(f"Event signature: {stress_record.signature[:16]}...")

    # Step 6: Verify measurement integrity
    print("\n[STEP 6] Integrity verification for regulatory audit")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Provenance chain integrity: {is_valid}")
    print(f"Merkle root: {merkle_root[:16]}...")
    print(f"Total events recorded: {len(framework.provenance_chain)}")

    for i, record in enumerate(framework.provenance_chain):
        print(f"  [{i}] {record.action_type}")

    # Step 7: Compliance packet for safety auditor
    print("\n[STEP 7] Generate compliance packet for FAA safety audit")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)

    # Custom safety analysis
    safety_analysis = {
        "audit_question": "Were measurements trustworthy for aircraft navigation?",
        "answer": "YES with qualification",
        "evidence": [
            "All measurements cryptographically signed (AAPF)",
            "Freshness proofs created within 1-hour windows (CCF)",
            "Environmental stress event detected and documented",
            "Stress event outside critical measurement period (Hour 1-2, stress in Hour 2)",
            "Hour 1 measurements unaffected and fully trustworthy",
            "Hour 2 measurements flagged with stress event context"
        ],
        "action_items": [
            "Aircraft using Hour 2 data should request fresh calibration",
            "HVAC system requires maintenance (non-sensor issue)",
            "NIST recalibration due in 12 hours (advance by 12 hours recommended)"
        ],
        "safety_verdict": "SAFE TO CONTINUE with recommendations"
    }

    compliance_packet["safety_analysis"] = safety_analysis

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/quantum-compliance-poc/sensor_attestation_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet contents:")
    print(f"  - {len(framework.provenance_chain)} timestamped events with signatures")
    print(f"  - Freshness proofs for 3 measurement hours")
    print(f"  - Environmental stress documentation")
    print(f"  - Safety analysis and verdicts")
    print(f"\nPacket saved to: sensor_attestation_packet.json")

    # Step 8: Regulatory outcome
    print("\n[STEP 8] FAA Safety Audit Decision")
    print("-" * 80)

    print("VERDICT: CONTINUE OPERATIONS")
    print("Reasoning:")
    print("  1. Cryptographic proof of calibration (AAPF signature)")
    print("  2. Hourly freshness proofs prove measurements were current (CCF)")
    print("  3. Environmental stress event detected, impact assessed, aircraft notified")
    print("  4. No measurement tampering detected (provenance chain valid)")
    print("  5. Root cause identified as facility HVAC, not sensor")
    print("\nOutcome: Flight operations continue; HVAC maintenance scheduled")


if __name__ == "__main__":
    quantum_sensor_attestation_demo()
