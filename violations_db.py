#!/usr/bin/env python3
"""
Real violation store.
Each record is HMAC-SHA256 signed by the receiving node at intake time.
The signature covers: id, system_name, violation_type, severity,
affected_count, harm_amount, submitted_at, node_id.
"""

import hmac
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
import uuid

DB_PATH = "./data/violations.db"
NODE_KEY_PATH = "./data/node.key"


def get_node_key():
    """Return the persistent node signing key, generating it on first call."""
    os.makedirs("./data", exist_ok=True)
    if os.path.exists(NODE_KEY_PATH):
        with open(NODE_KEY_PATH, "r") as f:
            return f.read().strip()
    key = os.urandom(32).hex()
    with open(NODE_KEY_PATH, "w") as f:
        f.write(key)
    return key


def _sign(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True).encode()
    return hmac.new(get_node_key().encode(), payload, hashlib.sha256).hexdigest()


def verify_violation(violation_id: str) -> bool:
    """Return True if the stored signature is still valid for this record."""
    v = get_violation(violation_id)
    if not v:
        return False
    signable = {k: v[k] for k in
                ["id", "system_name", "violation_type", "severity",
                 "affected_count", "harm_amount", "submitted_at", "node_id"]}
    expected = _sign(signable)
    return hmac.compare_digest(expected, v.get("signature", ""))


def init_violations_db():
    os.makedirs("./data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id           TEXT PRIMARY KEY,
            system_name  TEXT NOT NULL,
            violation_type TEXT NOT NULL,
            severity     TEXT NOT NULL CHECK(severity IN ('LOW','MEDIUM','HIGH','CRITICAL')),
            affected_count INTEGER NOT NULL CHECK(affected_count >= 0),
            harm_amount  TEXT DEFAULT '',
            evidence     TEXT DEFAULT '',
            reporter     TEXT DEFAULT 'anonymous',
            submitted_at TEXT NOT NULL,
            node_id      TEXT NOT NULL,
            signature    TEXT NOT NULL,
            status       TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


def submit_violation(system_name, violation_type, severity, affected_count,
                     harm_amount="", evidence="", reporter="anonymous",
                     node_id="unknown"):
    """
    Persist a new violation.
    Raises ValueError on bad input.
    Returns the full record dict including the signature.
    """
    if not system_name or not violation_type:
        raise ValueError("system_name and violation_type are required")
    severity = severity.upper()
    if severity not in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
        raise ValueError("severity must be LOW, MEDIUM, HIGH, or CRITICAL")
    affected_count = int(affected_count)
    if affected_count < 0:
        raise ValueError("affected_count must be >= 0")

    violation_id = str(uuid.uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()

    signable = {
        "id": violation_id,
        "system_name": system_name,
        "violation_type": violation_type,
        "severity": severity,
        "affected_count": affected_count,
        "harm_amount": harm_amount,
        "submitted_at": submitted_at,
        "node_id": node_id,
    }
    signature = _sign(signable)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO violations
        (id, system_name, violation_type, severity, affected_count,
         harm_amount, evidence, reporter, submitted_at, node_id, signature, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (violation_id, system_name, violation_type, severity, affected_count,
          harm_amount, evidence, reporter, submitted_at, node_id, signature))
    conn.commit()
    conn.close()

    return {**signable, "evidence": evidence, "reporter": reporter,
            "signature": signature, "status": "pending"}


def get_violations(status=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM violations WHERE status=? ORDER BY submitted_at DESC", (status,))
    else:
        c.execute("SELECT * FROM violations ORDER BY submitted_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_violation(violation_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM violations WHERE id=?", (violation_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def update_violation_status(violation_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE violations SET status=? WHERE id=?", (status, violation_id))
    conn.commit()
    conn.close()


def get_violation_stats():
    """Real aggregate stats — counts only, no fabricated numbers."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), COALESCE(SUM(affected_count),0) FROM violations")
    total, affected = c.fetchone()
    c.execute("SELECT COUNT(*) FROM violations WHERE status='pending'")
    pending = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM violations WHERE status='approved'")
    approved = c.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "affected_persons": affected,
    }
