#!/usr/bin/env python3
"""
Human Flourishing Frameworks - Main Flask Application

Research software for AI bias monitoring. Submitted violation data is
HMAC-SHA256 signed at intake. Demo data is clearly labeled as synthetic.
See data_sources.py for real public datasets.
"""

from flask import Flask, jsonify, render_template_string, request
import os
from datetime import datetime, timezone
import uuid
import threading

from adoption_tracker import (
    init_adoption_db, register_node, get_adoption_stats,
    get_nodes_list, get_active_nodes, get_total_nodes, start_heartbeat
)
from mesh_network import (
    init_mesh_db, get_mesh_violations, sync_with_mesh,
    get_mesh_peers, add_mesh_peer
)
from data_sources import get_mock_violations, get_compas_summary
from byzantine_consensus import (
    init_consensus_db, get_approved_violations, get_consensus_status,
    _COMPAT_DB, _ensure_compat_db
)
from violations_db import (
    init_violations_db, submit_violation, get_violations,
    get_violation, get_violation_stats, update_violation_status,
    verify_violation
)

app = Flask(__name__)

def _consensus_propose(violation_id, system_name, violation_type, severity, n_nodes=1):
    """Write a proposal to the PBFT compat DB.
    On single-node deployments auto-approves (1/1 = 100%).
    On multi-node deployments, status stays 'pending' until PBFT completes.
    """
    _ensure_compat_db()
    status = 'approved' if n_nodes == 1 else 'pending'
    score  = 100.0      if n_nodes == 1 else 0.0
    import sqlite3 as _sql
    conn = _sql.connect(_COMPAT_DB)
    try:
        conn.execute("""
            INSERT OR IGNORE INTO proposals
            (violation_id, system_name, violation_type, severity, consensus_status, consensus_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (violation_id, system_name, violation_type, severity, status, score))
        conn.commit()
    finally:
        conn.close()
    return status


for _init in [init_adoption_db, init_mesh_db, init_consensus_db, init_violations_db]:
    try:
        _init()
    except Exception:
        pass

NODE_ID   = str(uuid.uuid4())
NODE_NAME = os.environ.get('NODE_NAME', f'node-{NODE_ID[:8]}')
PLATFORM  = os.environ.get('PLATFORM', 'web')

mesh_sync_thread = threading.Thread(target=sync_with_mesh, daemon=True)
mesh_sync_thread.start()

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Human Flourishing Frameworks</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0; padding: 20px; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            text-align: center; margin-bottom: 40px; padding: 40px 20px;
            background: rgba(26,31,74,0.8); border-radius: 12px;
            border: 1px solid rgba(0,255,136,0.3);
        }
        h1 { font-size: 36px; margin-bottom: 10px; color: #00ffff; }
        .subtitle { color: #888; font-size: 16px; }
        .status {
            display: inline-block; background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88; color: #00ff88;
            padding: 8px 16px; border-radius: 20px; margin-top: 15px;
            font-size: 12px; font-weight: bold;
        }
        .stats {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin: 40px 0;
        }
        .stat-box {
            background: rgba(26,31,74,0.8); border: 1px solid rgba(0,255,136,0.3);
            border-radius: 12px; padding: 20px; text-align: center;
        }
        .stat-number { font-size: 32px; color: #00ffff; font-weight: bold; }
        .stat-label  { color: #888; font-size: 12px; margin-top: 8px; }
        .violations  { display: grid; gap: 20px; margin: 40px 0; }
        .violation {
            background: rgba(26,31,74,0.8); border-left: 4px solid #ff4444;
            border-radius: 8px; padding: 20px;
        }
        .violation h3 { color: #00ffff; margin-bottom: 10px; }
        .violation p  { color: #bbb; font-size: 14px; margin-bottom: 8px; }
        .severity {
            display: inline-block; padding: 4px 8px; border-radius: 4px;
            font-size: 11px; font-weight: bold; color: white;
        }
        .severity.LOW      { background: #888; }
        .severity.MEDIUM   { background: #ff9900; }
        .severity.HIGH     { background: #ff6600; }
        .severity.CRITICAL { background: #ff4444; }
        .notice {
            background: rgba(255,200,0,0.1); border: 1px solid #ffcc00;
            border-radius: 8px; padding: 16px; margin: 20px 0; font-size: 13px;
            color: #ffcc00;
        }
        .empty-state { color: #888; text-align: center; padding: 40px; }
        footer {
            text-align: center; margin-top: 60px; padding-top: 20px;
            border-top: 1px solid rgba(0,255,136,0.2); color: #666; font-size: 12px;
        }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Human Flourishing Frameworks</h1>
        <p class="subtitle">AI Bias Monitoring — Research Software</p>
        <div class="status" id="system-status">LOADING</div>
    </header>

    <div class="notice">
        <strong>Research software — early development.</strong>
        Submitted violations are signed and stored. Demo data is labeled synthetic.
        No governance board is active. See <a href="https://github.com/human-flourishing-frameworks/human-flourishing-frameworks/blob/master/CORRECTIONS.md" style="color:#ffcc00;">CORRECTIONS.md</a> for history.
    </div>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-number" id="violation-count">—</div>
            <div class="stat-label">Submitted Violations</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="affected-count">—</div>
            <div class="stat-label">Affected Persons (reported)</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="pending-count">—</div>
            <div class="stat-label">Pending Consensus</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="node-count">—</div>
            <div class="stat-label">Active Nodes</div>
        </div>
    </div>

    <h2 style="color:#00ffff; margin: 40px 0 20px 0;">Submitted Violations</h2>
    <div class="violations" id="violations-list">
        <p class="empty-state">Loading…</p>
    </div>

    <footer>
        <p>Human Flourishing Frameworks &mdash; Open intake system for AI bias violations</p>
        <p style="margin-top:8px;">
            Node: {{ node_name }} &nbsp;|&nbsp;
            Submit: <code>POST /api/violations</code> &nbsp;|&nbsp;
            Demo data: <a href="/api/violations/demo" style="color:#888;">/api/violations/demo</a>
        </p>
    </footer>
</div>

<script>
function fmt(n) { return Number(n).toLocaleString(); }

fetch('/api/status')
    .then(r => r.json())
    .then(d => {
        document.getElementById('system-status').textContent = d.status || 'ONLINE';
        document.getElementById('violation-count').textContent = fmt(d.violations);
        document.getElementById('affected-count').textContent  = fmt(d.affected_persons);
        document.getElementById('pending-count').textContent   = fmt(d.pending);
    })
    .catch(() => { document.getElementById('system-status').textContent = 'ERROR'; });

fetch('/api/adoption/stats')
    .then(r => r.json())
    .then(d => { document.getElementById('node-count').textContent = fmt(d.active_last_hour); })
    .catch(() => {});

fetch('/api/violations')
    .then(r => r.json())
    .then(list => {
        const el = document.getElementById('violations-list');
        if (!list.length) {
            el.innerHTML = '<p class="empty-state">No violations submitted yet. Submit one via <code>POST /api/violations</code>.</p>';
            return;
        }
        el.innerHTML = list.map(v => `
            <div class="violation">
                <h3>${v.system_name}</h3>
                <p><strong>Type:</strong> ${v.violation_type} &nbsp;|&nbsp;
                   <strong>Severity:</strong> <span class="severity ${v.severity}">${v.severity}</span> &nbsp;|&nbsp;
                   <strong>Status:</strong> ${v.status.toUpperCase()}</p>
                <p><strong>Affected:</strong> ${fmt(v.affected_count)} persons
                   ${v.harm_amount ? ' &nbsp;|&nbsp; <strong>Harm:</strong> ' + v.harm_amount : ''}</p>
                <p style="color:#666;font-size:12px;">
                    ID: ${v.id} &nbsp;|&nbsp; ${v.submitted_at.slice(0,10)} &nbsp;|&nbsp; node: ${v.node_id.slice(0,8)}…
                </p>
            </div>
        `).join('');
    })
    .catch(() => {});

fetch('/api/adoption/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({node_id: '{{ node_id }}', node_name: '{{ node_name }}', platform: '{{ platform }}'})
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
    return render_template_string(
        HTML_TEMPLATE, node_id=NODE_ID, node_name=NODE_NAME, platform=PLATFORM)


@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/api/status')
def api_status():
    stats = get_violation_stats()
    adoption = {}
    try:
        adoption = get_adoption_stats()
    except Exception:
        pass
    return jsonify({
        "status":           "OPERATIONAL",
        "timestamp":        datetime.now(timezone.utc).isoformat(),
        "violations":       stats["total"],
        "pending":          stats["pending"],
        "approved":         stats["approved"],
        "affected_persons": stats["affected_persons"],
        "nodes_online":     adoption.get("active_last_hour", 0),
        "mode":             "open",
        "data_note":        "counts reflect submitted violations only; demo data at /api/violations/demo",
    })


@app.route('/api/violations', methods=['GET'])
def api_violations_get():
    """Real submitted violations from the DB."""
    status_filter = request.args.get('status')
    return jsonify(get_violations(status=status_filter))


@app.route('/api/violations', methods=['POST'])
def api_violations_post():
    """
    Submit a violation for review.
    Required: system_name, violation_type, severity, affected_count
    Optional: harm_amount, evidence, reporter
    """
    data = request.get_json(silent=True) or {}
    missing = [f for f in ['system_name', 'violation_type', 'severity', 'affected_count']
               if not data.get(f) and data.get(f) != 0]
    if missing:
        return jsonify({"error": f"missing required fields: {missing}"}), 400

    try:
        record = submit_violation(
            system_name    = data['system_name'],
            violation_type = data['violation_type'],
            severity       = data['severity'],
            affected_count = data['affected_count'],
            harm_amount    = data.get('harm_amount', ''),
            evidence       = data.get('evidence', ''),
            reporter       = data.get('reporter', 'anonymous'),
            node_id        = NODE_ID,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        nodes = get_nodes_list(limit=1000)
        n = max(len(nodes), 1)
        consensus_status = _consensus_propose(
            record['id'], record['system_name'],
            record['violation_type'], record['severity'], n_nodes=n,
        )
        if consensus_status == 'approved':
            update_violation_status(record['id'], 'approved')
            record['status'] = 'approved'
    except Exception as e:
        print(f"[WARNING] Consensus wiring failed: {e}")

    return jsonify(record), 201


@app.route('/api/violations/demo')
def api_violations_demo():
    """Synthetic demo violations, clearly labeled. Not real data."""
    return jsonify({
        "violations": get_mock_violations(),
        "data_source": "SYNTHETIC",
        "note": "These are fabricated examples for UI/API testing only. Not real violations.",
    })


@app.route('/api/violations/compas')
def api_compas():
    """ProPublica COMPAS analysis summary (Angwin et al., 2016). Cited, not our research."""
    return jsonify(get_compas_summary())


@app.route('/api/violations/<violation_id>')
def api_violation_detail(violation_id):
    v = get_violation(violation_id)
    if not v:
        return jsonify({"error": "not found"}), 404
    v['signature_valid'] = verify_violation(violation_id)
    return jsonify(v)


# --- Adoption ---

@app.route('/api/adoption/register', methods=['POST'])
def adoption_register():
    try:
        data = request.get_json(silent=True) or {}
        register_node(
            data.get('node_id', str(uuid.uuid4())),
            data.get('node_name', 'unknown'),
            data.get('platform', 'web'),
            data.get('version', '1.0.0'),
        )
        return jsonify({"status": "registered"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/adoption/stats')
def adoption_stats():
    try:
        return jsonify(get_adoption_stats()), 200
    except Exception as e:
        return jsonify({"total_nodes": 0, "active_last_hour": 0,
                        "active_last_24h": 0, "last_7_days": 0,
                        "by_platform": {}, "error": str(e)}), 200


@app.route('/api/adoption/nodes')
def adoption_nodes():
    try:
        limit = request.args.get('limit', 50, type=int)
        return jsonify(get_nodes_list(limit)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/adoption/dashboard')
def adoption_dashboard():
    try:
        return jsonify({"stats": get_adoption_stats(),
                        "this_node": {"id": NODE_ID, "name": NODE_NAME,
                                      "platform": PLATFORM}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Mesh ---

@app.route('/api/mesh/peers')
def mesh_peers():
    try:
        peers = get_mesh_peers()
        return jsonify({"peers": peers, "count": len(peers),
                        "timestamp": datetime.now(timezone.utc).isoformat()}), 200
    except Exception as e:
        return jsonify({"peers": [], "count": 0, "error": str(e)}), 200


@app.route('/api/mesh/violations')
def mesh_violations():
    try:
        v = get_mesh_violations()
        return jsonify({"violations": v, "count": len(v),
                        "timestamp": datetime.now(timezone.utc).isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/mesh/sync', methods=['POST'])
def mesh_sync():
    """Peer-to-peer sync. Accepts violations from another node; returns ours."""
    data = request.get_json(silent=True) or {}
    sender_id = data.get('node_id', 'unknown')

    try:
        add_mesh_peer(sender_id, request.remote_addr or 'unknown',
                      data.get('port', 5000))
    except Exception:
        pass

    received = 0
    for v in data.get('violations', []):
        try:
            from mesh_network import DB_PATH as MESH_DB
            import sqlite3 as _sql
            conn = _sql.connect(MESH_DB)
            c = conn.cursor()
            c.execute("""
                INSERT OR IGNORE INTO mesh_violations
                (violation_id, system_name, violation_type, severity,
                 affected_count, harm_amount, first_reported, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (v.get('id'), v.get('system_name'), v.get('violation_type'),
                  v.get('severity'), v.get('affected_count'), v.get('harm_amount'),
                  v.get('submitted_at'), datetime.now(timezone.utc).isoformat()))
            conn.commit()
            conn.close()
            received += 1
        except Exception:
            pass

    return jsonify({"node_id": NODE_ID, "violations": get_violations(),
                    "received": received}), 200


# --- Consensus ---

@app.route('/api/consensus/approved')
def consensus_approved():
    try:
        v = get_approved_violations()
        return jsonify({"approved_violations": v, "count": len(v),
                        "timestamp": datetime.now(timezone.utc).isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/api/consensus/status/<violation_id>')
def consensus_status_route(violation_id):
    try:
        return jsonify(get_consensus_status(violation_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/api/consensus/tally/<violation_id>', methods=['POST'])
def consensus_tally(violation_id):
    """Re-evaluate consensus status for a violation (e.g. after peer votes arrive)."""
    try:
        status = get_consensus_status(violation_id)
        if status.get('status') == 'approved':
            update_violation_status(violation_id, 'approved')
        elif status.get('status') == 'rejected':
            update_violation_status(violation_id, 'rejected')
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        register_node(NODE_ID, NODE_NAME, PLATFORM)
        print(f"\n[OK] Node registered: {NODE_NAME} ({PLATFORM})")
        start_heartbeat(NODE_ID, NODE_NAME, PLATFORM, interval=60)
        print(f"[OK] Heartbeat started")
    except Exception as e:
        print(f"\n[WARNING] Could not register node: {e}")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
