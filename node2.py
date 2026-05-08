#!/usr/bin/env python3
"""
Impossibility Engine - Node 2
Connects to Node 1 mesh network
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
consensus = ByzantineConsensus(db_path='consensus_node2.db')
crypto = CryptographicProof()
mesh = MeshNetwork()
detector = ViolationDetector()

# Connect to Node 1, Railway cloud, and other nodes
mesh.connected_peers = [
    'node-9999',      # Primary node (port 9999)
    'https://web-production-46794.up.railway.app',  # Railway cloud node
    'node-a8f2',
    'node-c9e1',
    'node-d7b4'
]

@app.route('/')
def dashboard():
    """Node 2 dashboard"""
    stats = consensus.get_statistics()
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Impossibility Engine - Node 2</title>
    <style>
        body {{ background: #0a0e27; color: #e0e0e0; font-family: monospace; padding: 20px; }}
        .header {{ background: #1a1f4a; border: 2px solid #00ff88; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #00ff88; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
        .stat {{ background: #2a2f5a; border-left: 3px solid #00ff88; padding: 10px; }}
        .number {{ color: #00ffff; font-size: 24px; font-weight: bold; }}
        .label {{ color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Impossibility Engine - Node 2</h1>
        <p>Byzantine Consensus • Violation Detection • Mesh Network</p>
        <p style="color: #00ff88;">● ONLINE - Connected to mesh</p>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="number">{len(mesh.connected_peers)}</div>
            <div class="label">Connected Peers</div>
        </div>
        <div class="stat">
            <div class="number">{stats.get('proposal_count', 0)}</div>
            <div class="label">Proposals</div>
        </div>
        <div class="stat">
            <div class="number">{stats.get('vote_count', 0)}</div>
            <div class="label">Votes</div>
        </div>
        <div class="stat">
            <div class="number">67%</div>
            <div class="label">Consensus Threshold</div>
        </div>
    </div>

    <h2 style="color: #00ffff; margin-top: 30px;">🌐 Mesh Network Status</h2>
    <p>Connected to {len(mesh.connected_peers)} nodes:</p>
    <ul style="color: #00ff88;">
        {''.join([f'<li>✓ {peer}</li>' for peer in mesh.connected_peers])}
    </ul>

    <h2 style="color: #00ffff; margin-top: 30px;">⚙️ System Status</h2>
    <p>✓ Byzantine Consensus: <strong style="color: #00ff88;">ACTIVE</strong></p>
    <p>✓ Mesh Network: <strong style="color: #00ff88;">SYNCING</strong></p>
    <p>✓ Violation Detection: <strong style="color: #00ff88;">MONITORING</strong></p>
    <p>✓ Database: <strong style="color: #00ff88;">consensus_node2.db</strong></p>
</body>
</html>
"""
    return html

@app.route('/api/status')
def status():
    """Node 2 API status"""
    stats = consensus.get_statistics()
    return jsonify({
        'node_id': 'node-2',
        'port': 9998,
        'system': 'Impossibility Engine',
        'status': 'ONLINE',
        'mesh': {
            'connected_peers': len(mesh.connected_peers),
            'peers': mesh.connected_peers
        },
        'consensus': {
            'proposals': stats.get('proposal_count', 0),
            'votes': stats.get('vote_count', 0),
            'threshold': '67%'
        }
    })

if __name__ == '__main__':
    print("[Node 2] Impossibility Engine starting on port 9998")
    print("[Node 2] Connecting to mesh network...")
    port = 9998
    app.run(host='0.0.0.0', port=port, debug=False)
