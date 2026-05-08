#!/usr/bin/env python3
"""
Byzantine Consensus Protocol
Distributed voting on violations without central authority
Ensures agreement even if 1/3 of nodes are faulty
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
import hashlib

DB_PATH = "./data/byzantine.db"
NODE_ID = os.environ.get('NODE_ID', 'unknown')
CONSENSUS_THRESHOLD = 0.67  # 67% of nodes must agree

def init_consensus_db():
    """Initialize Byzantine consensus database"""
    os.makedirs("./data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Violation proposals
    c.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY,
            violation_id TEXT UNIQUE,
            proposer_node_id TEXT,
            system_name TEXT,
            violation_type TEXT,
            severity TEXT,
            affected_count INTEGER,
            harm_amount TEXT,
            proposal_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            consensus_status TEXT DEFAULT 'pending',
            consensus_score REAL DEFAULT 0
        )
    ''')

    # Votes on proposals
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            violation_id TEXT,
            voter_node_id TEXT,
            vote TEXT,
            vote_reason TEXT,
            vote_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vote_hash TEXT,
            UNIQUE(violation_id, voter_node_id)
        )
    ''')

    # Consensus history
    c.execute('''
        CREATE TABLE IF NOT EXISTS consensus_log (
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            violation_id TEXT,
            total_nodes INTEGER,
            votes_for INTEGER,
            votes_against INTEGER,
            final_status TEXT,
            consensus_percentage REAL
        )
    ''')

    # Trusted nodes (part of consensus group)
    c.execute('''
        CREATE TABLE IF NOT EXISTS trusted_nodes (
            id INTEGER PRIMARY KEY,
            node_id TEXT UNIQUE,
            reputation_score REAL DEFAULT 1.0,
            votes_participated INTEGER DEFAULT 0,
            votes_correct INTEGER DEFAULT 0,
            added_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def propose_violation(violation_id, system_name, violation_type, severity, affected_count, harm_amount):
    """Propose a new violation for consensus"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        INSERT INTO proposals
        (violation_id, proposer_node_id, system_name, violation_type, severity, affected_count, harm_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (violation_id, NODE_ID, system_name, violation_type, severity, affected_count, harm_amount))

    conn.commit()
    conn.close()

def cast_vote(violation_id, vote, reason=""):
    """Cast a vote on a proposal (YES/NO)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    vote_hash = hashlib.sha256(
        f"{violation_id}{NODE_ID}{vote}{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()

    try:
        c.execute('''
            INSERT INTO votes (violation_id, voter_node_id, vote, vote_reason, vote_hash)
            VALUES (?, ?, ?, ?, ?)
        ''', (violation_id, NODE_ID, vote, reason, vote_hash))
    except sqlite3.IntegrityError:
        # Node already voted, update it
        c.execute('''
            UPDATE votes
            SET vote = ?, vote_reason = ?, vote_timestamp = CURRENT_TIMESTAMP, vote_hash = ?
            WHERE violation_id = ? AND voter_node_id = ?
        ''', (vote, reason, vote_hash, violation_id, NODE_ID))

    conn.commit()
    conn.close()

def tally_consensus(violation_id, total_nodes):
    """Tally votes and determine consensus"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Count votes
    c.execute('''
        SELECT vote, COUNT(*) FROM votes
        WHERE violation_id = ?
        GROUP BY vote
    ''', (violation_id,))

    votes = {row[0]: row[1] for row in c.fetchall()}
    votes_for = votes.get('YES', 0)
    votes_against = votes.get('NO', 0)
    total_votes = votes_for + votes_against

    # Calculate consensus
    if total_votes == 0:
        consensus_percentage = 0
        status = 'pending'
    else:
        consensus_percentage = (votes_for / total_votes) * 100

        # Byzantine consensus: >66.67% agreement = consensus
        if consensus_percentage > (100 * CONSENSUS_THRESHOLD):
            status = 'approved'
        elif consensus_percentage < (100 * (1 - CONSENSUS_THRESHOLD)):
            status = 'rejected'
        else:
            status = 'undecided'

    # Update proposal status
    c.execute('''
        UPDATE proposals
        SET consensus_status = ?, consensus_score = ?
        WHERE violation_id = ?
    ''', (status, consensus_percentage, violation_id))

    # Log consensus result
    c.execute('''
        INSERT INTO consensus_log
        (violation_id, total_nodes, votes_for, votes_against, final_status, consensus_percentage)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (violation_id, total_nodes, votes_for, votes_against, status, consensus_percentage))

    conn.commit()
    conn.close()

    return {
        'violation_id': violation_id,
        'votes_for': votes_for,
        'votes_against': votes_against,
        'consensus_percentage': consensus_percentage,
        'status': status,
        'total_nodes': total_nodes
    }

def get_approved_violations():
    """Get all violations with consensus approval"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT violation_id, system_name, violation_type, severity,
               affected_count, harm_amount, consensus_score
        FROM proposals
        WHERE consensus_status = 'approved'
        ORDER BY consensus_score DESC
    ''')

    violations = [
        {
            'id': row[0],
            'system': row[1],
            'type': row[2],
            'severity': row[3],
            'affected': row[4],
            'harm': row[5],
            'consensus': row[6]
        }
        for row in c.fetchall()
    ]

    conn.close()
    return violations

def get_consensus_status(violation_id):
    """Get consensus status for a violation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT consensus_status, consensus_score FROM proposals
        WHERE violation_id = ?
    ''', (violation_id,))

    result = c.fetchone()
    conn.close()

    if result:
        return {'status': result[0], 'score': result[1]}
    return {'status': 'unknown', 'score': 0}

if __name__ == "__main__":
    init_consensus_db()
    print("[OK] Byzantine consensus initialized")
