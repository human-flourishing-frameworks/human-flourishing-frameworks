import os
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
        'running': True,
        'node_id': engine.node_id,
        'stats': engine.consensus.get_statistics()
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
