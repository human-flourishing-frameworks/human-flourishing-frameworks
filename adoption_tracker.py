#!/usr/bin/env python3
"""
Node Adoption Tracker
Tracks how many nodes are running and reporting in
"""

import json
import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = "./data/adoption.db"

def init_adoption_db():
    """Initialize adoption tracking database"""
    os.makedirs("./data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create nodes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY,
            node_id TEXT UNIQUE,
            node_name TEXT,
            platform TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            version TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Create adoption history (daily snapshots)
    c.execute('''
        CREATE TABLE IF NOT EXISTS adoption_history (
            id INTEGER PRIMARY KEY,
            date DATE UNIQUE,
            node_count INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def register_node(node_id, node_name, platform, version="1.0.0"):
    """Register a new node or update existing"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO nodes (node_id, node_name, platform, version, last_seen)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (node_id, node_name, platform, version))
    except sqlite3.IntegrityError:
        # Node exists, update last_seen
        c.execute('''
            UPDATE nodes 
            SET last_seen = CURRENT_TIMESTAMP, status = 'active'
            WHERE node_id = ?
        ''', (node_id,))
    
    conn.commit()
    conn.close()

def get_active_nodes(minutes=30):
    """Get count of nodes active in last N minutes"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    c.execute('''
        SELECT COUNT(*) FROM nodes 
        WHERE last_seen > ?
    ''', (cutoff_time.isoformat(),))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count

def get_total_nodes():
    """Get total count of all nodes ever registered"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM nodes')
    count = c.fetchone()[0]
    conn.close()
    
    return count

def get_adoption_stats():
    """Get comprehensive adoption statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total nodes
    c.execute('SELECT COUNT(*) FROM nodes')
    total = c.fetchone()[0]
    
    # Active in last hour
    c.execute('''
        SELECT COUNT(*) FROM nodes 
        WHERE last_seen > datetime('now', '-1 hour')
    ''')
    active_1h = c.fetchone()[0]
    
    # Active in last 24 hours
    c.execute('''
        SELECT COUNT(*) FROM nodes 
        WHERE last_seen > datetime('now', '-24 hours')
    ''')
    active_24h = c.fetchone()[0]
    
    # By platform
    c.execute('''
        SELECT platform, COUNT(*) as count 
        FROM nodes 
        GROUP BY platform
        ORDER BY count DESC
    ''')
    by_platform = {row[0]: row[1] for row in c.fetchall()}
    
    # Recent nodes (last 7 days)
    c.execute('''
        SELECT COUNT(*) FROM nodes 
        WHERE first_seen > datetime('now', '-7 days')
    ''')
    last_7d = c.fetchone()[0]
    
    conn.close()
    
    return {
        "total_nodes": total,
        "active_last_hour": active_1h,
        "active_last_24h": active_24h,
        "last_7_days": last_7d,
        "by_platform": by_platform,
        "timestamp": datetime.utcnow().isoformat()
    }

def get_nodes_list(limit=50):
    """Get list of recent nodes"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT node_name, platform, first_seen, last_seen, status
        FROM nodes
        ORDER BY last_seen DESC
        LIMIT ?
    ''', (limit,))
    
    nodes = [
        {
            "name": row[0],
            "platform": row[1],
            "first_seen": row[2],
            "last_seen": row[3],
            "status": row[4]
        }
        for row in c.fetchall()
    ]
    
    conn.close()
    return nodes

if __name__ == "__main__":
    init_adoption_db()
    print("Adoption tracker initialized")
