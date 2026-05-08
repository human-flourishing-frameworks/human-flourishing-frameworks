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
from agent_system import (
    AutonomousAgentSystem,
    ViolationDetectionAgent,
    CryptographicVerificationAgent,
    ByzantineConsensusAgent,
    AutonomousEscalationAgent,
    ImmutableAuditAgent,
    SystemHealthAgent,
    NetworkDiscoveryAgent,
    IMMUTABLE_RULES,
)
from cryptographic_proof import generate_keypair, load_keypair, save_keypair

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
# Autonomous agent system — node keypair + initialization
# ---------------------------------------------------------------------------
_NODE_KEY_DIR = os.path.join(os.path.dirname(__file__), "data")
_NODE_KEY_PRIV = os.path.join(_NODE_KEY_DIR, "node_key.pem")
_NODE_KEY_PUB = os.path.join(_NODE_KEY_DIR, "node_key_pub.pem")

try:
    _node_private, _node_public = load_keypair(_NODE_KEY_PRIV, _NODE_KEY_PUB)
except Exception:
    _node_private, _node_public = generate_keypair()
    try:
        save_keypair(_node_private, _node_public, _NODE_KEY_PRIV, _NODE_KEY_PUB)
    except Exception:
        pass  # keys stay in memory only

_PEER_URLS = [
    u.strip() for u in os.environ.get("PEER_URLS", "").split(",") if u.strip()
]

autonomous_system = AutonomousAgentSystem(
    private_key=_node_private,
    public_key=_node_public,
    peer_urls=_PEER_URLS,
    node_id=NODE_ID,
)

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
            <div class="stat-box" style="border-color: rgba(255, 136, 0, 0.5);">
                <div class="stat-number" style="color: #ff8800;" id="agent-count">7</div>
                <div class="stat-label">Autonomous Agents</div>
            </div>
            <div class="stat-box" style="border-color: rgba(255, 136, 0, 0.5);">
                <div class="stat-number" style="color: #ff8800;" id="pending-escalations">0</div>
                <div class="stat-label">Pending Escalations</div>
            </div>
            <div class="stat-box" style="border-color: rgba(255, 136, 0, 0.5);">
                <div class="stat-number" style="color: #ff8800;" id="audit-entries">0</div>
                <div class="stat-label">Audit Entries</div>
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

        <h2 style="color: #ff8800; margin: 40px 0 20px 0;">Autonomous Governance</h2>
        <div class="demo-banner" style="border-color: #ff8800; background: rgba(255, 136, 0, 0.1); color: #ff8800;">
            <strong>ALGORITHMIC GOVERNANCE</strong> &mdash; 7 autonomous agents coordinate
            through PBFT consensus. No human board, no discretion. Escalations are
            irreversible after a 24-hour lock period. Consensus threshold is derived from
            PBFT quorum (2f+1), not hardcoded.
        </div>
        <div class="stats" id="autonomous-agents-grid">
            <!-- populated by JS -->
        </div>
        <div id="autonomous-escalations" style="margin: 20px 0;">
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

        // Load autonomous system status
        fetch('/api/autonomous/status')
            .then(r => r.json())
            .then(data => {
                const agents = data.agents || [];
                document.getElementById('agent-count').textContent = agents.length;

                const queue = data.escalation_queue || {};
                document.getElementById('pending-escalations').textContent = queue.total || 0;

                const audit = data.audit_chain || {};
                document.getElementById('audit-entries').textContent = audit.entries_checked || 0;

                const grid = document.getElementById('autonomous-agents-grid');
                agents.forEach(a => {
                    const box = document.createElement('div');
                    box.className = 'stat-box';
                    box.style.borderColor = 'rgba(255, 136, 0, 0.4)';
                    box.innerHTML = `
                        <div class="stat-number" style="font-size: 16px; color: #ff8800;">${a.agent}</div>
                        <div class="stat-label">${a.description || ''}</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #00ff88;">${a.status || 'active'}</div>
                    `;
                    grid.appendChild(box);
                });
            })
            .catch(() => {});

        // Load escalations
        fetch('/api/autonomous/escalations')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('autonomous-escalations');
                const escalations = data.escalations || [];
                if (escalations.length === 0) return;

                let html = '<h3 style="color: #ff8800; margin-bottom: 10px;">Recent Escalations</h3>';
                escalations.slice(0, 5).forEach(e => {
                    const statusColor = e.status === 'executed' ? '#00ff88' : '#ffcc00';
                    html += `
                        <div class="violation" style="border-left-color: #ff8800; margin-bottom: 10px;">
                            <h3 style="font-size: 14px;">${e.violation_id}</h3>
                            <p><strong>Status:</strong> <span style="color: ${statusColor};">${e.status}</span></p>
                            <p><strong>Lock time:</strong> ${e.lock_time}</p>
                            <p><strong>Execute time:</strong> ${e.execute_time}</p>
                        </div>
                    `;
                });
                container.innerHTML = html;
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
# Autonomous agent system endpoints
# ---------------------------------------------------------------------------


@app.route('/api/autonomous/submit', methods=['POST'])
def autonomous_submit():
    """Submit violation evidence for autonomous processing.

    Runs the full pipeline: Detect -> Verify -> Consensus -> Lock -> Escalate.
    Evidence must include 'accuracy_gap' (float), 'system_name' (str),
    and 'description' (str).
    """
    try:
        evidence = request.json
        if not evidence:
            return jsonify({"error": "JSON body required"}), 400
        result = autonomous_system.submit_evidence(evidence)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/autonomous/status')
def autonomous_status():
    """Current autonomous system status: agents, rules, escalation queue."""
    try:
        status = autonomous_system.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/autonomous/escalations')
def autonomous_escalations():
    """List locked, pending, and executed escalations."""
    try:
        limit = request.args.get('limit', 50, type=int)
        escalations = autonomous_system.autonomous_escalation.get_all_escalations(limit)
        pending = autonomous_system.autonomous_escalation.check_pending()
        return jsonify({
            "escalations": escalations,
            "pending_execution": pending,
            "total": len(escalations),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/autonomous/audit')
def autonomous_audit():
    """Audit trail entries from the immutable log."""
    try:
        limit = request.args.get('limit', 100, type=int)
        entries = autonomous_system.immutable_audit.get_entries(limit)
        chain = autonomous_system.immutable_audit.verify_chain()
        return jsonify({
            "entries": entries,
            "chain_valid": chain["chain_valid"],
            "entries_checked": chain["entries_checked"],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/autonomous/rules')
def autonomous_rules():
    """Return IMMUTABLE_RULES for full transparency."""
    try:
        return jsonify(autonomous_system.get_rules()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
