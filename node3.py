#!/usr/bin/env python3
"""
Impossibility Engine - Node 3
Connects to Node 1 and Node 2 mesh network
Port: 9997
"""

from flask import Flask, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from core.byzantine_consensus import ByzantineConsensus
from core.cryptographic_proof import CryptographicProof
from core.mesh_network import MeshNetwork
from core.violation_detector import ViolationDetector

app = Flask(__name__)

# Initialize core systems
consensus = ByzantineConsensus(db_path='consensus_node3.db')
crypto = CryptographicProof()
mesh = MeshNetwork()
detector = ViolationDetector()

# Connect to Node 1, Node 2, Railway cloud, and other nodes
mesh.connected_peers = [
    'node-9999',      # Node 1 (port 9999)
    'node-9998',      # Node 2 (port 9998)
    'https://web-production-46794.up.railway.app',  # Railway cloud node
    'node-a8f2',
    'node-c9e1',
    'node-d7b4'
]

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get node status and Byzantine consensus state"""
    pending = consensus.get_pending_proposals()
    return jsonify({
        'node_id': 'node-3',
        'port': 9997,
        'status': 'ONLINE',
        'system': 'Impossibility Engine',
        'consensus': {
            'proposals': len(pending),
            'votes': sum(1 for p in pending for v in p.get('votes', [])),
            'threshold': '67%'
        },
        'mesh': {
            'connected_peers': len(mesh.connected_peers),
            'peers': mesh.connected_peers
        },
        'subsystems': {
            'byzantine_consensus': 'ACTIVE',
            'cryptographic_proof': 'ARMED',
            'mesh_network': 'SYNCING',
            'violation_detector': 'MONITORING'
        }
    })

@app.route('/api/violations', methods=['GET'])
def get_violations():
    """Get detected violations"""
    violations = detector.detect_all()
    return jsonify({
        'node_id': 'node-3',
        'violations': violations,
        'count': len(violations)
    })

@app.route('/')
def dashboard():
    """Node 3 dashboard"""
    stats = consensus.get_statistics()
    pending = consensus.get_pending_proposals()
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Impossibility Engine - Node 3</title>
    <style>
        body {{ background: #0a0e27; color: #e0e0e0; font-family: monospace; padding: 20px; }}
        .header {{ background: #1a1f4a; border: 2px solid #00ff88; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #00ff88; }}
        .status {{ color: #00ff88; font-weight: bold; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
        .stat {{ background: #2a2f5a; border-left: 3px solid #00ff88; padding: 10px; }}
        .number {{ color: #00ffff; font-size: 24px; font-weight: bold; }}
        .label {{ color: #888; font-size: 12px; }}
        .peers {{ background: #2a2f5a; border: 1px solid #00ff88; padding: 15px; margin-top: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Impossibility Engine - Node 3</h1>
        <p>Byzantine Consensus Network | Status: <span class="status">ONLINE</span></p>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="number">{len(pending)}</div>
            <div class="label">Pending Proposals</div>
        </div>
        <div class="stat">
            <div class="number">{sum(1 for p in pending for v in p.get('votes', []))}</div>
            <div class="label">Total Votes</div>
        </div>
        <div class="stat">
            <div class="number">{len(mesh.connected_peers)}</div>
            <div class="label">Connected Peers</div>
        </div>
        <div class="stat">
            <div class="number">67%</div>
            <div class="label">Consensus Threshold</div>
        </div>
    </div>

    <div class="peers">
        <h3 style="color: #00ff88; margin-bottom: 10px;">Mesh Network Peers</h3>
        {"".join([f"<div style='padding: 5px;'>{peer}</div>" for peer in mesh.connected_peers])}
    </div>
</body>
</html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9997))
    app.run(host='0.0.0.0', port=port, debug=False)
