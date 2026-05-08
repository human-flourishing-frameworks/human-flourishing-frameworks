#!/usr/bin/env python3
"""
Human Flourishing Frameworks - Main Flask Application

Research software for AI bias monitoring. Violation data shown is synthetic
unless explicitly labeled with a real citation. See data_sources.py for
details on mock vs. real datasets.
"""

from flask import Flask, jsonify, render_template_string, request
import os
from datetime import datetime
import uuid
import threading

from adoption_tracker import (
    init_adoption_db, register_node, get_adoption_stats,
    get_nodes_list, get_active_nodes, get_total_nodes, start_heartbeat
)
from mesh_network import (
    init_mesh_db, get_mesh_violations, sync_with_mesh
)
from data_sources import get_mock_violations, get_compas_summary

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Database init (safe to call multiple times)
# ---------------------------------------------------------------------------
try:
    init_adoption_db()
except Exception:
    pass

try:
    init_mesh_db()
except Exception:
    pass

# ---------------------------------------------------------------------------
# Node identity
# ---------------------------------------------------------------------------
NODE_ID = str(uuid.uuid4())
NODE_NAME = os.environ.get('NODE_NAME', f'node-{NODE_ID[:8]}')
PLATFORM = os.environ.get('PLATFORM', 'web')

# ---------------------------------------------------------------------------
# Background threads — only heartbeat + mesh sync (no propagation)
# ---------------------------------------------------------------------------
mesh_sync_thread = threading.Thread(target=sync_with_mesh, daemon=True)
mesh_sync_thread.start()

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
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
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }
        .severity-critical { background: #ff4444; }
        .severity-high     { background: #ff8800; }
        .severity-medium   { background: #ffcc00; color: #333; }
        .severity-low      { background: #44bb44; }
        .demo-banner {
            background: rgba(255, 200, 0, 0.15);
            border: 1px solid #ffcc00;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 30px 0 20px 0;
            color: #ffcc00;
            font-size: 14px;
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
            <p class="subtitle">AI Bias Monitoring &mdash; Research Software</p>
            <div class="status" id="status-badge">ONLINE &mdash; <span id="node-count">0</span> node(s) registered</div>
        </header>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number" id="total-nodes">0</div>
                <div class="stat-label">Total Nodes Registered</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="active-nodes">0</div>
                <div class="stat-label">Active Nodes (last hour)</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="violation-count">0</div>
                <div class="stat-label">Demo Violations Loaded</div>
            </div>
        </div>

        <div class="demo-banner">
            <strong>DEMO DATA</strong> &mdash; The violations below are synthetic
            examples for testing. They do not represent real incidents. See
            <code>data_sources.py</code> for real public datasets
            (e.g.&nbsp;ProPublica COMPAS analysis).
        </div>

        <h2 style="color: #00ffff; margin: 20px 0;">Synthetic Violations (Demo)</h2>
        <div class="violations" id="violations-list">
            <!-- populated by JS -->
        </div>

        <footer>
            <p>Human Flourishing Frameworks &mdash; Research Software</p>
            <p style="margin-top: 10px;">
                This is research software. Violation data is synthetic unless labeled otherwise.
            </p>
        </footer>
    </div>

    <script>
        // Load adoption stats
        fetch('/api/adoption/stats')
            .then(r => r.json())
            .then(data => {
                document.getElementById('node-count').textContent = data.active_last_hour || 0;
                document.getElementById('total-nodes').textContent = data.total_nodes || 0;
                document.getElementById('active-nodes').textContent = data.active_last_hour || 0;
            })
            .catch(() => {});

        // Load violations from API (mock data, clearly labeled)
        fetch('/api/violations')
            .then(r => r.json())
            .then(data => {
                const violations = data.violations || [];
                document.getElementById('violation-count').textContent = violations.length;

                const list = document.getElementById('violations-list');
                violations.forEach(v => {
                    const sev = (v.severity || 'medium').toLowerCase();
                    const card = document.createElement('div');
                    card.className = 'violation';
                    card.innerHTML = `
                        <h3>${v.system_name || v.id}</h3>
                        <p><strong>ID:</strong> ${v.id}</p>
                        <p><strong>Description:</strong> ${v.description}</p>
                        <p><strong>Affected (simulated):</strong> ${(v.affected_count || 0).toLocaleString()}</p>
                        <p><strong>Source:</strong> ${v.source}</p>
                        <p><span class="severity severity-${sev}">${sev.toUpperCase()}</span></p>
                    `;
                    list.appendChild(card);
                });
            })
            .catch(() => {});

        // Register this browser as a node
        fetch('/api/adoption/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                node_id: '{{ node_id }}',
                node_name: '{{ node_name }}',
                platform: '{{ platform }}'
            })
        }).catch(() => {});
    </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Main dashboard — renders the HTML template with node identity."""
    return render_template_string(
        HTML_TEMPLATE,
        node_id=NODE_ID,
        node_name=NODE_NAME,
        platform=PLATFORM,
    )


@app.route('/health')
def health():
    """Health check (e.g. for Heroku)."""
    return jsonify({"status": "ok"}), 200


@app.route('/api/status')
def api_status():
    """Honest system status — no fabricated numbers."""
    return jsonify({
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "research",
        "data_source": "mock",
        "node_id": NODE_ID,
        "disclaimer": (
            "This is research software. Violation data shown is synthetic "
            "unless labeled otherwise."
        ),
    })


@app.route('/api/violations')
def api_violations():
    """Return mock violations from data_sources, clearly labeled."""
    violations = get_mock_violations()
    return jsonify({
        "violations": violations,
        "count": len(violations),
        "data_source": "mock",
        "disclaimer": (
            "These violations are synthetic examples for testing. "
            "See data_sources.py for real public datasets."
        ),
    })


@app.route('/api/violations/compas')
def api_compas():
    """Return a summary of the real ProPublica COMPAS analysis."""
    return jsonify(get_compas_summary())


# ---------------------------------------------------------------------------
# Adoption tracker endpoints (real, honest code)
# ---------------------------------------------------------------------------

@app.route('/api/adoption/register', methods=['POST'])
def adoption_register():
    """Register a new node."""
    try:
        data = request.json
        register_node(
            data.get('node_id', str(uuid.uuid4())),
            data.get('node_name', 'unknown'),
            data.get('platform', 'web'),
            data.get('version', '1.0.0'),
        )
        return jsonify({"status": "registered"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/adoption/stats')
def adoption_stats():
    """Get adoption statistics from the local database."""
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
            "error": str(e),
        }), 200


@app.route('/api/adoption/nodes')
def adoption_nodes():
    """Get list of recent nodes."""
    try:
        limit = request.args.get('limit', 50, type=int)
        nodes = get_nodes_list(limit)
        return jsonify(nodes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/adoption/dashboard')
def adoption_dashboard():
    """Get adoption dashboard data."""
    try:
        stats = get_adoption_stats()
        return jsonify({
            "stats": stats,
            "this_node": {
                "id": NODE_ID,
                "name": NODE_NAME,
                "platform": PLATFORM,
            },
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Mesh network endpoints (honest HTTP sync)
# ---------------------------------------------------------------------------

@app.route('/api/mesh/violations')
def mesh_violations():
    """Get violations synced from the mesh network."""
    try:
        violations = get_mesh_violations()
        return jsonify({
            "violations": violations,
            "count": len(violations),
            "timestamp": datetime.utcnow().isoformat(),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Register this node on startup
    try:
        register_node(NODE_ID, NODE_NAME, PLATFORM)
        print(f"\n[OK] Node registered: {NODE_NAME} ({PLATFORM})")

        # Start heartbeat (keeps node visible in adoption tracker)
        start_heartbeat(NODE_ID, NODE_NAME, PLATFORM, interval=60)
        print("[OK] Heartbeat started — syncing every 60 seconds")
    except Exception as e:
        print(f"\n[WARNING] Could not register node: {e}")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
