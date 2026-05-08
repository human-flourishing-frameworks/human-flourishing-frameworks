#!/usr/bin/env python3
"""
Human Flourishing Frameworks - Main Flask Application

Research software for AI bias monitoring. Violation data shown is synthetic
unless explicitly labeled with a real citation. See data_sources.py for
details on mock vs. real datasets.
"""

from flask import Flask, jsonify, render_template_string, request
import math
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
from seed_data import ALL_SEED_MEASUREMENTS
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
from sensors import Measurement, SensorRegistry
from world_model import WorldModel, Intervention

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
# World model — Bayesian belief tracking + sensor framework
# ---------------------------------------------------------------------------
_world_sensor_registry = SensorRegistry()
world_model = WorldModel(
    sensors=_world_sensor_registry,
    db_path=os.path.join(os.path.dirname(__file__), "data", "world_model.db"),
)

# ---------------------------------------------------------------------------
# Bootstrap — seed the world model with REAL data only
# ---------------------------------------------------------------------------
# The world model starts empty. Without initial observations it has no beliefs
# and nothing to show. This bootstrap feeds published, cited, real-world
# findings into the sensor→world_model pipeline so the system has something
# true to reason about from the moment it starts.
#
# NO mock data enters the world model. Mock violations stay in the demo UI
# where they are clearly labeled synthetic.
# ---------------------------------------------------------------------------


def _bootstrap_world_model() -> None:
    """Seed the world model with observations from peer-reviewed research.

    Draws from seed_data.py which contains measurements from 30+ published
    sources covering humans (health, autonomy, fairness, opportunity),
    animals (health, safety, comfort, natural_behavior), and ecosystems
    (biodiversity, stability, resilience).

    Every measurement comes from peer-reviewed or publicly audited research.
    No mock data enters the world model. Each carries honest uncertainty.
    See seed_data.py for full source citations and methodology notes.
    """
    # Skip if the model already has beliefs (persistence across restarts)
    if world_model.beliefs:
        return

    bootstrap_measurements = ALL_SEED_MEASUREMENTS

    updates = world_model.update(bootstrap_measurements)
    print(f"[BOOTSTRAP] Seeded {len(updates)} beliefs from real published data")
    for u in updates:
        print(
            f"  - {u['entity']}: posterior={u['posterior']:.3f}, "
            f"uncertainty={u['uncertainty']:.3f}"
        )


_bootstrap_world_model()

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

        <h2 style="color: #00ff88; margin: 40px 0 20px 0;">World Model</h2>
        <div class="demo-banner" style="border-color: #00ff88; background: rgba(0, 255, 136, 0.1); color: #00ff88;">
            <strong>BAYESIAN WORLD MODEL</strong> &mdash; Tracks probabilistic beliefs
            about outcomes across all domains and scopes. The model is always wrong
            somewhere &mdash; uncertainty is a first-class concept, not an afterthought.
            Every number below carries error bars.
        </div>
        <div class="stats" id="world-model-stats">
            <div class="stat-box" style="border-color: rgba(0, 255, 136, 0.4);">
                <div class="stat-number" style="color: #00ff88;" id="wm-belief-count">0</div>
                <div class="stat-label">Beliefs Tracked</div>
            </div>
            <div class="stat-box" style="border-color: rgba(0, 255, 136, 0.4);">
                <div class="stat-number" style="color: #00ff88;" id="wm-sensor-count">0</div>
                <div class="stat-label">Sensors Active</div>
            </div>
            <div class="stat-box" style="border-color: rgba(0, 255, 136, 0.4);">
                <div class="stat-number" style="color: #00ff88;" id="wm-avg-uncertainty">--</div>
                <div class="stat-label">Avg Uncertainty</div>
            </div>
            <div class="stat-box" style="border-color: rgba(0, 255, 136, 0.4);">
                <div class="stat-number" style="color: #00ff88;" id="wm-corrections">0</div>
                <div class="stat-label">Self-Corrections</div>
            </div>
        </div>
        <div id="world-model-flourishing" style="margin: 20px 0;"></div>
        <div id="world-model-discoveries" style="margin: 20px 0;"></div>

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

        // Load world model status
        fetch('/api/world/status')
            .then(r => r.json())
            .then(data => {
                document.getElementById('wm-belief-count').textContent = data.belief_count || 0;
                document.getElementById('wm-sensor-count').textContent = data.sensor_count || 0;
                document.getElementById('wm-avg-uncertainty').textContent =
                    data.average_uncertainty !== undefined
                        ? (data.average_uncertainty * 100).toFixed(0) + '%'
                        : '--';
                document.getElementById('wm-corrections').textContent = data.corrections_count || 0;

                // Render flourishing scores
                const scores = data.flourishing_scores || {};
                const fContainer = document.getElementById('world-model-flourishing');
                const scopes = Object.keys(scores);
                if (scopes.length > 0) {
                    let html = '<h3 style="color: #00ff88; margin-bottom: 10px;">Flourishing Scores by Scope</h3>';
                    html += '<div class="stats">';
                    scopes.forEach(scope => {
                        const s = scores[scope];
                        const pct = (s.score * 100).toFixed(0);
                        const unc = (s.uncertainty * 100).toFixed(0);
                        html += `
                            <div class="stat-box" style="border-color: rgba(0, 255, 136, 0.3);">
                                <div class="stat-number" style="font-size: 20px; color: #00ff88;">${pct}%</div>
                                <div class="stat-label">${scope}</div>
                                <div style="margin-top: 6px; font-size: 11px; color: #888;">
                                    &plusmn;${unc}% uncertainty
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    fContainer.innerHTML = html;
                }
            })
            .catch(() => {});

        // Load world model discoveries
        fetch('/api/world/discover')
            .then(r => r.json())
            .then(data => {
                const discoveries = data.discoveries || [];
                const container = document.getElementById('world-model-discoveries');
                if (discoveries.length === 0) return;

                let html = '<h3 style="color: #00ff88; margin-bottom: 10px;">Discovered Patterns</h3>';
                discoveries.slice(0, 5).forEach(d => {
                    const sevColor = d.severity === 'actionable' ? '#ffcc00'
                                   : d.severity === 'interesting' ? '#00ffff'
                                   : '#888';
                    html += `
                        <div class="violation" style="border-left-color: #00ff88; margin-bottom: 10px;">
                            <h3 style="font-size: 14px; color: ${sevColor};">${d.type}</h3>
                            <p>${d.description}</p>
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
# World model endpoints
# ---------------------------------------------------------------------------


@app.route('/api/world/status')
def world_status():
    """World model status: belief count, sensor count, last update, flourishing.

    The model is always wrong somewhere. The 'average_uncertainty' field
    tells you roughly how wrong -- higher means more ignorant. This is
    honest self-assessment, not false modesty.
    """
    try:
        status = world_model.status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/beliefs')
def world_beliefs():
    """Current beliefs, paginated and filterable by domain/scope.

    Each belief includes its uncertainty -- the most important number
    after the posterior itself. A posterior of 0.8 with uncertainty 0.6
    is NOT a confident belief.

    Query params:
        domain: filter by domain (e.g., 'healthcare')
        scope: filter by scope (e.g., 'humans')
        page: page number (default 1)
        per_page: items per page (default 50, max 200)
    """
    try:
        domain = request.args.get('domain')
        scope = request.args.get('scope')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 200)

        all_beliefs = list(world_model.beliefs.values())

        if domain:
            all_beliefs = [b for b in all_beliefs if b.domain == domain]
        if scope:
            all_beliefs = [b for b in all_beliefs if b.scope == scope]

        # Sort by last_updated descending
        all_beliefs.sort(key=lambda b: b.last_updated, reverse=True)

        total = len(all_beliefs)
        start = (page - 1) * per_page
        end = start + per_page
        page_beliefs = all_beliefs[start:end]

        return jsonify({
            "beliefs": [b.to_dict() for b in page_beliefs],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 0,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/belief/<path:entity>')
def world_belief_detail(entity):
    """Detailed belief for one entity, including full history.

    The history shows how the model's belief has evolved over time.
    Large swings in the posterior indicate either contradictory evidence
    or a genuinely volatile phenomenon. Steady convergence indicates
    the model is learning something stable.
    """
    try:
        belief = world_model.query(entity)
        if belief is None:
            return jsonify({
                "error": "not_found",
                "entity": entity,
                "message": (
                    "no belief exists for this entity. the model has not "
                    "observed it yet. this does not mean it does not exist "
                    "-- only that no sensor has measured it."
                ),
            }), 404

        history = world_model.get_history(entity)

        return jsonify({
            "belief": belief.to_dict(),
            "history": history,
            "evidence_count": len(belief.evidence),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/observe', methods=['POST'])
def world_observe():
    """Submit new sensor measurements for Bayesian update.

    Accepts a list of measurements. Each measurement must include at
    minimum: value, uncertainty, confidence_interval, source, and scope.

    The model updates its beliefs based on these measurements. More
    certain measurements (lower uncertainty) shift beliefs more.

    Request body:
    {
        "measurements": [
            {
                "value": 0.73,
                "uncertainty": 0.15,
                "confidence_interval": [0.65, 0.81],
                "source": "hospital_xyz_records",
                "scope": "healthcare:hospital_xyz",
                "methodology": "administrative_records",
                "sample_size": 500,
                "confounders": ["income_not_controlled"],
                "missing": ["rural_patients_excluded"]
            }
        ]
    }
    """
    try:
        data = request.json
        if not data or "measurements" not in data:
            return jsonify({
                "error": "request must include 'measurements' array",
            }), 400

        raw_measurements = data["measurements"]
        if not isinstance(raw_measurements, list):
            return jsonify({"error": "'measurements' must be an array"}), 400

        measurements = []
        errors = []
        for i, raw in enumerate(raw_measurements):
            try:
                m = Measurement.from_dict(raw)
                measurements.append(m)
            except Exception as e:
                errors.append({"index": i, "error": str(e)})

        if not measurements:
            return jsonify({
                "error": "no valid measurements in request",
                "parse_errors": errors,
            }), 400

        updates = world_model.update(measurements)

        return jsonify({
            "updates": updates,
            "measurements_processed": len(measurements),
            "parse_errors": errors,
            "disclaimer": (
                "beliefs have been updated. the model is now slightly less "
                "wrong than before (probably). check uncertainty values."
            ),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/predict/<path:entity>')
def world_predict(entity):
    """What interventions could improve this entity's flourishing?

    Returns a list of hypothetical interventions with predicted effects.
    Every prediction includes uncertainty bounds and caveats. These are
    suggestions based on current beliefs, not prescriptions.

    Query params:
        action: specific action to evaluate (default: 'improve')
    """
    try:
        action = request.args.get('action', 'improve')
        interventions = world_model.counterfactual(entity, action)

        predictions = []
        for intervention in interventions:
            prediction = world_model.predict(intervention)
            predictions.append(prediction.to_dict())

        return jsonify({
            "entity": entity,
            "predictions": predictions,
            "disclaimer": (
                "these are speculative predictions, not guarantees. "
                "correlation does not imply causation. second-order "
                "effects are especially uncertain."
            ),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/flourishing')
def world_flourishing():
    """Aggregate flourishing scores by scope.

    Returns flourishing scores for all scopes the model knows about.
    Each score includes uncertainty -- a score of 70% with 40% uncertainty
    means flourishing could plausibly be anywhere from 30% to 100%.

    Query params:
        scope: specific scope to query (returns all if not specified)
    """
    try:
        specific_scope = request.args.get('scope')

        if specific_scope:
            score = world_model.flourishing_score(specific_scope)
            metric = world_model.get_flourishing_metric(specific_scope)
            return jsonify({
                "scope": specific_scope,
                "score": score.to_dict(),
                "components": metric.to_dict()["components"],
                "disclaimer": (
                    "flourishing is a value-laden concept. these components "
                    "and weights reflect choices, not objective truths."
                ),
            }), 200

        # All scopes
        scopes = list(set(
            b.scope for b in world_model.beliefs.values()
        ))
        # Also include explicitly configured flourishing metrics
        scopes = list(set(
            scopes + list(world_model._flourishing_metrics.keys())
        ))

        results = {}
        for scope in scopes:
            try:
                score = world_model.flourishing_score(scope)
                results[scope] = score.to_dict()
            except Exception:
                pass

        return jsonify({
            "flourishing_by_scope": results,
            "scopes_measured": len(results),
            "disclaimer": (
                "flourishing metrics are approximations. unmeasured dimensions "
                "(joy, meaning, beauty) are invisible to this model."
            ),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/corrections')
def world_corrections():
    """Every time the model self-corrected.

    A correction happens when new evidence significantly shifts a belief
    (more than 5% change in posterior). Frequent corrections mean the
    model is learning. No corrections could mean the model is stagnant
    or not receiving new data.

    Query params:
        limit: max corrections to return (default 100)
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        corrections = world_model.correction_log[:limit]

        return jsonify({
            "corrections": corrections,
            "total": len(world_model.correction_log),
            "returned": len(corrections),
            "disclaimer": (
                "corrections are a feature, not a bug. a model that never "
                "corrects itself is not learning."
            ),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/world/discover')
def world_discover():
    """Anomalies and discovered patterns in current beliefs.

    The model looks for:
    - Outlier beliefs (posteriors far from priors with low uncertainty)
    - Measurement gaps (clusters of high-uncertainty beliefs)
    - Stale beliefs (not updated recently)
    - Correlated beliefs (entities moving together, suggesting shared causes)

    These are hypotheses to investigate, not conclusions.
    """
    try:
        discoveries = world_model.discover()
        return jsonify({
            "discoveries": discoveries,
            "count": len(discoveries),
            "disclaimer": (
                "patterns found here are exploratory, not causal. "
                "the model finds correlations, not causes."
            ),
        }), 200
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
