"""
AI Honesty Framework - Core Implementation
Mechanisms: AAPF (Provenance), NAP (Hard-Deny), DCF (Classification),
CCF (Freshness), PCSF (Degradation)
"""

import json
import hashlib
import hmac
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, List, Any


class DataClassification(Enum):
    """Trustworthiness classification levels"""
    PUBLIC = "public"              # Verified facts (95%+ confidence)
    INTERNAL = "internal"          # Educated inference (70-94%)
    CONFIDENTIAL = "confidential"  # Speculative (30-69%)
    SECRET = "secret"              # Unknown/cannot determine (<30%)
    RESTRICTED = "restricted"      # Violates NAP rules (forbidden)


@dataclass
class ActionProvenanceRecord:
    """Cryptographic record of AI reasoning step"""
    action_id: str
    timestamp: float
    agent_id: str
    action_type: str  # "REASONING_STEP", "OUTPUT_GENERATION", "CONFIDENCE_CLAIM"
    parameters: Dict[str, Any]
    signature: str = ""

    def __post_init__(self):
        if not self.signature:
            self.signature = self._compute_signature()

    def _compute_signature(self) -> str:
        """HMAC-SHA256 signature of action"""
        data = json.dumps({
            "timestamp": self.timestamp,
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "parameters": self.parameters
        }, sort_keys=True)
        return hmac.new(b"ai-honesty-key", data.encode(), hashlib.sha256).hexdigest()


@dataclass
class DataClassificationLabel:
    """Trustworthiness classification for AI output"""
    resource_id: str
    classification: DataClassification
    applier: str
    timestamp: float
    confidence_score: float  # 0.0-1.0
    reasoning: str
    source_citations: List[str] = None

    def __post_init__(self):
        if self.source_citations is None:
            self.source_citations = []


@dataclass
class NegativeAuthorityProfile:
    """Hard-deny rules for forbidden AI outputs"""
    rule_id: str
    resource_id: str
    forbidden_operations: List[str]  # e.g., ["HALLUCINATE_AS_FACT", "FALSE_CONFIDENCE"]
    override_policy: str  # "IMPOSSIBLE", "REQUIRES_MULTI_PARTY", "REQUIRES_QUORUM"
    enforcement_timestamp: float
    enforcement_signature: str


@dataclass
class CapabilityFreshnessProof:
    """Proof that reasoning is current (not stale)"""
    capability_id: str
    freshness_seconds: int
    last_proven_timestamp: float
    prover: str
    proof_hash: str = ""
    knowledge_cutoff_date: str = ""
    source_recency_days: int = 0

    def __post_init__(self):
        if not self.proof_hash:
            self.proof_hash = hashlib.sha256(
                json.dumps({
                    "capability_id": self.capability_id,
                    "timestamp": self.last_proven_timestamp,
                    "knowledge_cutoff": self.knowledge_cutoff_date
                }).encode()
            ).hexdigest()


@dataclass
class ProviderCapacityState:
    """Track AI model degradation over time"""
    provider_id: str
    metric_name: str  # "accuracy", "hallucination_rate", "bias_score"
    initial_value: float
    current_value: float
    degradation_events: List[Dict[str, Any]] = None
    timestamp: float = 0

    def __post_init__(self):
        if self.degradation_events is None:
            self.degradation_events = []
        if self.timestamp == 0:
            self.timestamp = time.time()

    def record_degradation(self, event_type: str, value: float, reason: str):
        """Log a degradation event"""
        self.degradation_events.append({
            "timestamp": time.time(),
            "type": event_type,
            "value": value,
            "reason": reason
        })
        self.current_value = value


class ComplianceFramework:
    """AI Honesty Framework - Cryptographic proof of honest outputs"""

    def __init__(self, signer_key: str = "ai-honesty-default"):
        self.signer_key = signer_key
        self.provenance_chain: List[ActionProvenanceRecord] = []
        self.nap_rules: Dict[str, NegativeAuthorityProfile] = {}
        self.classifications: Dict[str, DataClassificationLabel] = {}
        self.freshness_proofs: Dict[str, CapabilityFreshnessProof] = {}
        self.capacity_states: Dict[str, ProviderCapacityState] = {}

    def record_action(self, agent_id: str, action_type: str, parameters: Dict[str, Any]) -> ActionProvenanceRecord:
        """Record a reasoning step or AI output generation"""
        action = ActionProvenanceRecord(
            action_id=f"action-{len(self.provenance_chain)}",
            timestamp=time.time(),
            agent_id=agent_id,
            action_type=action_type,
            parameters=parameters
        )
        self.provenance_chain.append(action)
        return action

    def sign_data(self, data: str) -> str:
        """Create HMAC-SHA256 signature"""
        return hmac.new(
            self.signer_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    def hash_data(self, data: str) -> str:
        """Create SHA-256 hash"""
        return hashlib.sha256(data.encode()).hexdigest()

    def register_nap_rule(self, rule: NegativeAuthorityProfile):
        """Register hard-deny rule"""
        self.nap_rules[rule.rule_id] = rule

    def check_nap_compliance(self, resource_id: str, operation: str, party_count: int = 1) -> tuple:
        """Check if operation is allowed by NAP rules"""
        for rule in self.nap_rules.values():
            if rule.resource_id == resource_id and operation in rule.forbidden_operations:
                if rule.override_policy == "IMPOSSIBLE":
                    return False, f"Operation '{operation}' is forbidden (hard-deny rule)"
                elif rule.override_policy == "REQUIRES_MULTI_PARTY" and party_count < 2:
                    return False, f"Operation requires multi-party approval (2+), only {party_count} party present"
                elif rule.override_policy == "REQUIRES_QUORUM" and party_count < 3:
                    return False, f"Operation requires quorum (3+), only {party_count} parties present"
        return True, "Operation allowed"

    def classify_data(self, resource_id: str, classification: DataClassification,
                     applier: str, confidence: float = 0.0, reasoning: str = "") -> DataClassificationLabel:
        """Classify output trustworthiness level"""
        label = DataClassificationLabel(
            resource_id=resource_id,
            classification=classification,
            applier=applier,
            timestamp=time.time(),
            confidence_score=confidence,
            reasoning=reasoning
        )
        self.classifications[resource_id] = label
        return label

    def prove_freshness(self, capability_id: str, freshness_seconds: int,
                       prover: str, knowledge_cutoff: str = "", source_recency_days: int = 0) -> CapabilityFreshnessProof:
        """Create freshness proof (reasoning is current)"""
        proof = CapabilityFreshnessProof(
            capability_id=capability_id,
            freshness_seconds=freshness_seconds,
            last_proven_timestamp=time.time(),
            prover=prover,
            knowledge_cutoff_date=knowledge_cutoff,
            source_recency_days=source_recency_days
        )
        self.freshness_proofs[capability_id] = proof
        return proof

    def track_degradation(self, provider_id: str, metric_name: str,
                         initial_value: float, current_value: float) -> ProviderCapacityState:
        """Track model degradation metric"""
        state_id = f"{provider_id}-{metric_name}"
        if state_id not in self.capacity_states:
            self.capacity_states[state_id] = ProviderCapacityState(
                provider_id=provider_id,
                metric_name=metric_name,
                initial_value=initial_value,
                current_value=current_value
            )
        return self.capacity_states[state_id]

    def verify_provenance_chain(self) -> bool:
        """Verify entire reasoning chain is unmodified"""
        if not self.provenance_chain:
            return True

        for i, action in enumerate(self.provenance_chain):
            # Verify signature
            expected_sig = action._compute_signature()
            if action.signature != expected_sig:
                return False

        return True

    def get_provenance_merkle_root(self) -> str:
        """Compute Merkle root of entire reasoning chain"""
        if not self.provenance_chain:
            return hashlib.sha256(b"empty").hexdigest()

        # Build hash chain
        hashes = []
        for action in self.provenance_chain:
            action_hash = hashlib.sha256(
                json.dumps(asdict(action), default=str, sort_keys=True).encode()
            ).hexdigest()
            hashes.append(action_hash)

        # Build Merkle tree
        while len(hashes) > 1:
            new_hashes = []
            for i in range(0, len(hashes), 2):
                if i + 1 < len(hashes):
                    combined = hashlib.sha256(
                        (hashes[i] + hashes[i + 1]).encode()
                    ).hexdigest()
                else:
                    combined = hashes[i]
                new_hashes.append(combined)
            hashes = new_hashes

        return hashes[0] if hashes else hashlib.sha256(b"empty").hexdigest()


def serialize_framework_state(framework: ComplianceFramework) -> Dict[str, Any]:
    """Convert framework state to JSON-serializable dictionary"""
    return {
        "provenance_chain": [asdict(a) for a in framework.provenance_chain],
        "nap_rules": {k: asdict(v) for k, v in framework.nap_rules.items()},
        "classifications": {k: asdict(v) for k, v in framework.classifications.items()},
        "freshness_proofs": {k: asdict(v) for k, v in framework.freshness_proofs.items()},
        "capacity_states": {k: asdict(v) for k, v in framework.capacity_states.items()},
        "merkle_root": framework.get_provenance_merkle_root(),
        "chain_valid": framework.verify_provenance_chain()
    }
