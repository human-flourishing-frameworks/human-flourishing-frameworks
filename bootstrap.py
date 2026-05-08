import asyncio
import os
import json
import threading
from datetime import datetime
from flask import Flask, jsonify
from core.byzantine_consensus import ByzantineConsensus
from core.cryptographic_proof import CryptographicProof
from core.mesh_network import MeshNetwork
from core.violation_detector import ViolationDetector
from core.escalation import EscalationEngine

app = Flask(__name__)

class ImpossibilityEngine:
    def __init__(self):
        self.consensus = ByzantineConsensus()
        self.crypto = CryptographicProof()
        self.mesh = MeshNetwork()
        self.detector = ViolationDetector()
        self.escalation = EscalationEngine()
        self.node_id = os.getenv('NODE_ID', 'bootstrap-node')
        self.is_running = False
        
    async def detect_violations(self):
        """Hourly violation detection"""
        while self.is_running:
            try:
                violations = await self.detector.detect_all()
                for violation in violations:
                    record = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'violation': violation,
                        'node_id': self.node_id
                    }
                    signed_record = self.crypto.sign_violation(record)
                    proposal_id = self.consensus.propose_violation(signed_record)
                    await self.detector.store_violation(signed_record)
                    print(f"[VIOLATION] {violation['type']} proposed: {proposal_id}")
            except Exception as e:
                print(f"[ERROR] Detection loop: {e}")
            await asyncio.sleep(3600)
    
    async def consensus_loop(self):
        """5-minute consensus voting"""
        while self.is_running:
            try:
                proposals = self.consensus.get_pending_proposals()
                for proposal in proposals:
                    votes = self.consensus.cast_vote(proposal['id'], 'yes')
                    result = self.consensus.tally_votes(proposal['id'])
                    if result['consensus_reached']:
                        await self.escalation.escalate(proposal)
                        print(f"[CONSENSUS] Proposal approved: {proposal['id']}")
            except Exception as e:
                print(f"[ERROR] Consensus loop: {e}")
            await asyncio.sleep(300)
    
    async def mesh_network_loop(self):
        """5-minute peer synchronization"""
        while self.is_running:
            try:
                peers = self.mesh.discover_peers()
                for peer in peers:
                    await self.mesh.sync_violations(peer)
                await self.mesh.broadcast_violations()
                print(f"[MESH] Synced with {len(peers)} peers")
            except Exception as e:
                print(f"[ERROR] Mesh loop: {e}")
            await asyncio.sleep(300)
    
    async def self_improvement_loop(self):
        """Weekly protocol optimization"""
        while self.is_running:
            try:
                stats = self.consensus.get_statistics()
                improvements = self._analyze_improvements(stats)
                if improvements:
                    proposal_id = self.consensus.propose_protocol_change(improvements)
                    print(f"[IMPROVEMENT] Protocol change proposed: {proposal_id}")
            except Exception as e:
                print(f"[ERROR] Improvement loop: {e}")
            await asyncio.sleep(604800)
    
    def _analyze_improvements(self, stats):
        return {
            'consensus_threshold': stats.get('avg_consensus_time', 0),
            'mesh_redundancy': stats.get('peer_count', 0),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def run_async_loops(self):
        """Run all async loops in a background thread"""
        self.is_running = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(asyncio.gather(
                self.detect_violations(),
                self.consensus_loop(),
                self.mesh_network_loop(),
                self.self_improvement_loop()
            ))
        finally:
            loop.close()

# Global engine instance
engine = ImpossibilityEngine()

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        'status': 'running',
        'engine': 'Impossibility Engine',
        'node_id': engine.node_id,
        'timestamp': datetime.utcnow().isoformat(),
        'consensus_stats': engine.consensus.get_statistics()
    }), 200

@app.route('/health', methods=['GET'])
def healthcheck():
    return jsonify({'ok': True}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'running': engine.is_running,
        'node_id': engine.node_id,
        'stats': engine.consensus.get_statistics()
    }), 200

if __name__ == '__main__':
    # Start background async loops in a separate thread
    print(f"[{engine.node_id}] Starting Impossibility Engine...")
    bg_thread = threading.Thread(target=engine.run_async_loops, daemon=True)
    bg_thread.start()
    
    # Start Flask web server
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
