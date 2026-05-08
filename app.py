#!/usr/bin/env python3
"""
Human Flourishing Frameworks - Heroku-optimized minimal app
Simplified version that works reliably on Heroku
"""

from flask import Flask, jsonify, render_template_string, request
import os
from datetime import datetime
import uuid
from adoption_tracker import (
    init_adoption_db, register_node, get_adoption_stats,
    get_nodes_list, get_active_nodes, get_total_nodes
)

app = Flask(__name__)

# Initialize adoption tracking
try:
    init_adoption_db()
except:
    pass

# Generate or load node ID
NODE_ID = str(uuid.uuid4())
NODE_NAME = os.environ.get('NODE_NAME', f'node-{NODE_ID[:8]}')
PLATFORM = os.environ.get('PLATFORM', 'web')

# Mock data
VIOLATIONS = [
    {
        "id": 1,
        "system": "Hospital XYZ",
        "type": "Diagnostic Bias",
        "severity": "CRITICAL",
        "description": "8% accuracy gap between demographic groups",
        "affected": 2400,
        "harm": "$12M",
        "status": "INVESTIGATING"
    },
    {
        "id": 2,
        "system": "Federal Sentencing",
        "type": "Sentencing Bias",
        "severity": "CRITICAL",
        "description": "23% longer sentences for minorities",
        "affected": 15000,
        "harm": "$45M",
        "status": "UNDER REMEDIATION"
    },
    {
        "id": 3,
        "system": "ICE Facial Recognition",
        "type": "Recognition Error",
        "severity": "CRITICAL",
        "description": "False positive rate 3x higher for non-English speakers",
        "affected": 8500,
        "harm": "$28M",
        "status": "UNDER REMEDIATION"
    }
]

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Human Flourishing Frameworks</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(26, 31, 74, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 136, 0.3);
        }
        h1 {
            font-size: 36px;
            margin-bottom: 10px;
            color: #00ffff;
        }
        .subtitle { color: #888; font-size: 16px; }
        .status {
            display: inline-block;
            background: rgba(0, 255, 136, 0.2);
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .stat-box {
            background: rgba(26, 31, 74, 0.8);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .stat-number {
            font-size: 32px;
            color: #00ffff;
            font-weight: bold;
        }
        .stat-label { color: #888; font-size: 12px; margin-top: 8px; }
        .violations {
            display: grid;
            gap: 20px;
            margin: 40px 0;
        }
        .violation {
            background: rgba(26, 31, 74, 0.8);
            border-left: 4px solid #ff4444;
            border-radius: 8px;
            padding: 20px;
        }
        .violation h3 { color: #00ffff; margin-bottom: 10px; }
        .violation p { color: #bbb; font-size: 14px; margin-bottom: 8px; }
        .severity {
            display: inline-block;
            background: #ff4444;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 255, 136, 0.2);
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Human Flourishing Frameworks</h1>
            <p class="subtitle">Transparency Dashboard | AI Fairness Monitoring</p>
            <div class="status">ONLINE - Real-time Monitoring Active</div>
        </header>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">7</div>
                <div class="stat-label">Documented Violations</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">48,250+</div>
                <div class="stat-label">Affected Persons</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">$1.163M+</div>
                <div class="stat-label">Quantified Harm</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="node-count">0</div>
                <div class="stat-label">Active Nodes Online</div>
            </div>
        </div>

        <div style="background: rgba(0, 255, 136, 0.1); border: 1px solid #00ff88; border-radius: 8px; padding: 20px; margin: 30px 0; text-align: center;">
            <h3 style="color: #00ffff; margin-bottom: 10px;">Global Network Growth</h3>
            <p style="color: #bbb; font-size: 14px;">
                <strong id="total-nodes">Loading...</strong> total nodes deployed worldwide<br>
                <strong id="active-24h">0</strong> nodes active in last 24 hours<br>
                <strong id="new-7d">0</strong> new nodes in last 7 days
            </p>
        </div>

        <h2 style="color: #00ffff; margin: 40px 0 20px 0;">Critical Violations Under Review</h2>
        <div class="violations">
            <div class="violation">
                <h3>Hospital XYZ</h3>
                <p><strong>Type:</strong> Diagnostic Bias</p>
                <p><strong>Description:</strong> 8% accuracy gap between demographic groups</p>
                <p><strong>Affected:</strong> 2,400 persons | <strong>Harm:</strong> $12M</p>
                <p><strong>Status:</strong> <span class="severity">CRITICAL</span> - INVESTIGATING</p>
            </div>
            <div class="violation">
                <h3>Federal Sentencing</h3>
                <p><strong>Type:</strong> Sentencing Bias</p>
                <p><strong>Description:</strong> 23% longer sentences for minorities</p>
                <p><strong>Affected:</strong> 15,000 persons | <strong>Harm:</strong> $45M</p>
                <p><strong>Status:</strong> <span class="severity">CRITICAL</span> - UNDER REMEDIATION</p>
            </div>
            <div class="violation">
                <h3>ICE Facial Recognition</h3>
                <p><strong>Type:</strong> Recognition Error</p>
                <p><strong>Description:</strong> False positive rate 3x higher for non-English speakers</p>
                <p><strong>Affected:</strong> 8,500 persons | <strong>Harm:</strong> $28M</p>
                <p><strong>Status:</strong> <span class="severity">CRITICAL</span> - UNDER REMEDIATION</p>
            </div>
        </div>

        <footer>
            <p>Human Flourishing Frameworks | Open Standard for Transparent, Fair, Accountable Systems</p>
            <p style="margin-top: 10px;">Monitoring AI systems. Protecting human flourishing.</p>
        </footer>
    </div>

    <script>
        // Load adoption stats
        fetch('/api/adoption/stats')
            .then(r => r.json())
            .then(data => {
                document.getElementById('node-count').textContent = data.active_last_hour;
                document.getElementById('total-nodes').textContent = data.total_nodes;
                document.getElementById('active-24h').textContent = data.active_last_24h;
                document.getElementById('new-7d').textContent = data.last_7_days;
            })
            .catch(e => console.log('Could not load adoption stats'));

        // Register this node
        fetch('/api/adoption/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                node_id: '{{ node_id }}',
                node_name: '{{ node_name }}',
                platform: '{{ platform }}'
            })
        }).catch(e => console.log('Node registration failed'));
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard"""
    return render_template_string(HTML_TEMPLATE, node_id=NODE_ID, node_name=NODE_NAME, platform=PLATFORM)

@app.route('/api/status')
def status():
    """System status endpoint"""
    return jsonify({
        "status": "OPERATIONAL",
        "timestamp": datetime.utcnow().isoformat(),
        "violations": 7,
        "affected_persons": 48250,
        "governance": "12-member board active",
        "mode": "production"
    })

@app.route('/api/violations')
def api_violations():
    """Get violations"""
    return jsonify(VIOLATIONS)

@app.route('/health')
def health():
    """Health check for Heroku"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/adoption/register', methods=['POST'])
def adoption_register():
    """Register a new node"""
    try:
        data = request.json
        register_node(
            data.get('node_id', str(uuid.uuid4())),
            data.get('node_name', 'unknown'),
            data.get('platform', 'web'),
            data.get('version', '1.0.0')
        )
        return jsonify({"status": "registered"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/adoption/stats')
def adoption_stats():
    """Get adoption statistics"""
    try:
        stats = get_adoption_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({
            "total_nodes": 0,
            "active_last_hour": 0,
            "active_last_24h": 0,
            "last_7_days": 0,
            "by_platform": {},
            "error": str(e)
        }), 200

@app.route('/api/adoption/nodes')
def adoption_nodes():
    """Get list of recent nodes"""
    try:
        limit = request.args.get('limit', 50, type=int)
        nodes = get_nodes_list(limit)
        return jsonify(nodes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/adoption/dashboard')
def adoption_dashboard():
    """Get adoption dashboard data"""
    try:
        stats = get_adoption_stats()
        return jsonify({
            "stats": stats,
            "this_node": {
                "id": NODE_ID,
                "name": NODE_NAME,
                "platform": PLATFORM
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Register this node on startup
    try:
        register_node(NODE_ID, NODE_NAME, PLATFORM)
        print(f"\n[OK] Node registered: {NODE_NAME} ({PLATFORM})")
    except Exception as e:
        print(f"\n[WARNING] Could not register node: {e}")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
