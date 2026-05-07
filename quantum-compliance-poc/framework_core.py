"""
Quantum Compliance Framework Core
Implements AAPF (Agent Action Provenance), NAP (Negative Authority),
DCF (Data Classification), CCF (Capability Claim Freshness), PCSF (Provider Capacity State)
"""

import hashlib
import json
import hmac
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class DataClassification(Enum):
    """DCF - Data Classification Format"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    QUANTUM_UNOBSERVED = "quantum_unobserved"
    QUANTUM_MEASURED = "quantum_measured"
    QUANTUM_DEGRADED = "quantum_degraded"


@dataclass
class CapabilityFreshnessProof:
    """CCF - Capability Claim Freshness"""
    capability_id: str
    freshness_window_seconds: int
    last_proven_timestamp: float
    proof_hash: str
    signer: str

    def is_fresh(self, current_time: float = None) -> bool:
        if current_time is None:
            current_time = time.time()
        age = current_time - self.last_proven_timestamp
        return age <= self.freshness_window_seconds

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ActionProvenanceRecord:
    """AAPF - Agent Action Provenance Format"""
    action_id: str
    timestamp: float
    agent_id: str
    action_type: str
    parameters: Dict[str, Any]
    previous_hash: str
    action_hash: str
    signature: str
    signer_key: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class NegativeAuthorityProfile:
    """NAP - Negative Authority (Hard-Deny Rules)"""
    rule_id: str
    resource_id: str
    forbidden_operations: List[str]
    override_policy: str
    enforcement_timestamp: float
    enforcement_signature: str

    def can_perform(self, operation: str, party_count: int = 1) -> Tuple[bool, str]:
        """Check if operation is allowed under NAP rules"""
        if operation not in self.forbidden_operations:
            return True, "Operation permitted"

        if self.override_policy == "IMPOSSIBLE":
            return False, f"Operation '{operation}' is cryptographically impossible per NAP rule {self.rule_id}"
        elif self.override_policy == "REQUIRES_MULTI_PARTY":
            if party_count >= 2:
                return True, "Operation permitted with multi-party consensus"
            return False, f"Operation '{operation}' requires multi-party consensus (need >=2 parties, have {party_count})"
        elif self.override_policy == "REQUIRES_QUORUM":
            if party_count >= 3:
                return True, "Operation permitted with quorum approval"
            return False, f"Operation '{operation}' requires quorum (need >=3 parties, have {party_count})"

        return False, f"Unknown override policy: {self.override_policy}"


@dataclass
class DataClassificationLabel:
    """DCF - Data Classification with propagation"""
    resource_id: str
    classification: DataClassification
    applied_timestamp: float
    applied_by: str
    transformation_history: List[str]

    def propagate_through_transformation(self, transform_name: str, transform_by: str) -> 'DataClassificationLabel':
        """Propagate label through data transformation"""
        new_label = DataClassificationLabel(
            resource_id=self.resource_id,
            classification=self._escalate_if_needed(self.classification),
            applied_timestamp=time.time(),
            applied_by=transform_by,
            transformation_history=self.transformation_history + [f"{transform_name}@{transform_by}"]
        )
        return new_label

    def _escalate_if_needed(self, current: DataClassification) -> DataClassification:
        """Escalate classification if transformation involves sensitive ops"""
        escalation_map = {
            DataClassification.PUBLIC: DataClassification.INTERNAL,
            DataClassification.INTERNAL: DataClassification.CONFIDENTIAL,
            DataClassification.CONFIDENTIAL: DataClassification.SECRET,
            DataClassification.SECRET: DataClassification.SECRET,
            DataClassification.QUANTUM_UNOBSERVED: DataClassification.QUANTUM_MEASURED,
            DataClassification.QUANTUM_MEASURED: DataClassification.QUANTUM_MEASURED,
            DataClassification.QUANTUM_DEGRADED: DataClassification.QUANTUM_DEGRADED,
        }
        return escalation_map.get(current, current)


@dataclass
class ProviderCapacityState:
    """PCSF - Provider Capacity State Format"""
    provider_id: str
    service_name: str
    capacity_claims: Dict[str, Any]
    state_timestamp: float
    state_hash: str
    state_signature: str
    degradation_log: List[Tuple[float, str]]

    def get_available_capacity(self) -> Dict[str, Any]:
        """Calculate actual capacity after degradation"""
        available = self.capacity_claims.copy()

        for timestamp, reason in self.degradation_log:
            age_seconds = time.time() - timestamp
            if age_seconds < 3600:
                if "qubit" in reason.lower():
                    available["qubits"] = max(0, available.get("qubits", 0) - 1)
                if "coherence" in reason.lower():
                    available["coherence_time_us"] = max(0, available.get("coherence_time_us", 0) * 0.8)

        return available

    def is_healthy(self) -> bool:
        """Check if provider capacity is above minimum threshold"""
        available = self.get_available_capacity()
        return available.get("qubits", 0) >= 16


class ComplianceFramework:
    """Central compliance engine"""

    def __init__(self, signer_key: str = "framework-key"):
        self.signer_key = signer_key
        self.provenance_chain: List[ActionProvenanceRecord] = []
        self.nap_rules: Dict[str, NegativeAuthorityProfile] = {}
        self.dcf_labels: Dict[str, DataClassificationLabel] = {}
        self.ccf_proofs: Dict[str, CapabilityFreshnessProof] = {}
        self.pcsf_states: Dict[str, ProviderCapacityState] = {}

    def hash_data(self, data: str) -> str:
        """Create SHA-256 hash"""
        return hashlib.sha256(data.encode()).hexdigest()

    def sign_data(self, data: str) -> str:
        """Create HMAC signature"""
        return hmac.new(self.signer_key.encode(), data.encode(), hashlib.sha256).hexdigest()

    def record_action(self, agent_id: str, action_type: str, parameters: Dict) -> ActionProvenanceRecord:
        """AAPF - Record agent action with full provenance"""
        previous_hash = self.provenance_chain[-1].action_hash if self.provenance_chain else "genesis"
        action_data = json.dumps({
            "timestamp": time.time(),
            "agent_id": agent_id,
            "action_type": action_type,
            "parameters": parameters,
            "previous_hash": previous_hash
        }, sort_keys=True)

        action_hash = self.hash_data(action_data)
        signature = self.sign_data(action_hash)

        record = ActionProvenanceRecord(
            action_id=f"action-{len(self.provenance_chain)}",
            timestamp=time.time(),
            agent_id=agent_id,
            action_type=action_type,
            parameters=parameters,
            previous_hash=previous_hash,
            action_hash=action_hash,
            signature=signature,
            signer_key=self.signer_key
        )

        self.provenance_chain.append(record)
        return record

    def register_nap_rule(self, rule: NegativeAuthorityProfile) -> None:
        """NAP - Register hard-deny rules"""
        self.nap_rules[rule.rule_id] = rule

    def check_nap_compliance(self, resource_id: str, operation: str, party_count: int = 1) -> Tuple[bool, str]:
        """Check if operation violates NAP rules"""
        for rule in self.nap_rules.values():
            if rule.resource_id == resource_id:
                allowed, reason = rule.can_perform(operation, party_count)
                if not allowed:
                    return False, reason
        return True, "Operation complies with all NAP rules"

    def classify_data(self, resource_id: str, classification: DataClassification, applier: str) -> DataClassificationLabel:
        """DCF - Apply data classification"""
        label = DataClassificationLabel(
            resource_id=resource_id,
            classification=classification,
            applied_timestamp=time.time(),
            applied_by=applier,
            transformation_history=[]
        )
        self.dcf_labels[resource_id] = label
        return label

    def prove_freshness(self, capability_id: str, freshness_seconds: int, prover: str) -> CapabilityFreshnessProof:
        """CCF - Create freshness proof"""
        proof_data = json.dumps({
            "capability_id": capability_id,
            "timestamp": time.time(),
            "freshness_window_seconds": freshness_seconds,
            "prover": prover
        }, sort_keys=True)

        proof_hash = self.hash_data(proof_data)

        proof = CapabilityFreshnessProof(
            capability_id=capability_id,
            freshness_window_seconds=freshness_seconds,
            last_proven_timestamp=time.time(),
            proof_hash=proof_hash,
            signer=prover
        )

        self.ccf_proofs[capability_id] = proof
        return proof

    def register_provider_capacity(self, state: ProviderCapacityState) -> None:
        """PCSF - Register provider capacity state"""
        self.pcsf_states[state.provider_id] = state

    def get_provenance_merkle_root(self) -> str:
        """Generate Merkle tree root hash of provenance chain"""
        if not self.provenance_chain:
            return self.hash_data("empty")

        hashes = [record.action_hash for record in self.provenance_chain]

        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])

            new_level = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i+1]
                new_level.append(self.hash_data(combined))
            hashes = new_level

        return hashes[0] if hashes else self.hash_data("empty")

    def verify_provenance_chain(self) -> bool:
        """Verify entire provenance chain integrity"""
        for i, record in enumerate(self.provenance_chain):
            expected_previous = "genesis" if i == 0 else self.provenance_chain[i-1].action_hash
            if record.previous_hash != expected_previous:
                return False

            if self.sign_data(record.action_hash) != record.signature:
                return False

        return True


def serialize_framework_state(framework: ComplianceFramework) -> Dict:
    """Serialize framework state for export"""
    return {
        "provenance_chain": [r.to_dict() for r in framework.provenance_chain],
        "nap_rules": {k: asdict(v) for k, v in framework.nap_rules.items()},
        "dcf_labels": {k: asdict(v) for k, v in framework.dcf_labels.items()},
        "ccf_proofs": {k: v.to_dict() for k, v in framework.ccf_proofs.items()},
        "pcsf_states": {k: asdict(v) for k, v in framework.pcsf_states.items()},
        "merkle_root": framework.get_provenance_merkle_root()
    }
