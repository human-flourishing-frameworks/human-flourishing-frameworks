#!/usr/bin/env python3
"""
Governance Board Initialization
Sets up the 12-member board and prepares for voting
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = r'C:\nodes\data.db'

def init_governance():
    """Initialize governance board"""

    print("\n" + "="*70)
    print("  GOVERNANCE BOARD INITIALIZATION")
    print("="*70 + "\n")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create governance tables if they don't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS board_members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            affiliation TEXT,
            region TEXT,
            voting_power INTEGER DEFAULT 1,
            appointed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS board_votes (
            id INTEGER PRIMARY KEY,
            violation_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            vote TEXT NOT NULL,
            reasoning TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (violation_id) REFERENCES violations(id),
            FOREIGN KEY (member_id) REFERENCES board_members(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS board_decisions (
            id INTEGER PRIMARY KEY,
            violation_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            vote_count_yes INTEGER,
            vote_count_no INTEGER,
            decision_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            merkle_root TEXT,
            FOREIGN KEY (violation_id) REFERENCES violations(id)
        )
    ''')

    # Add board members
    board_members = [
        ("Dr. Kimberly Washington", "Civil Society - ACLU Representative", "ACLU", "North America", 1),
        ("Dr. James Chen", "Security Researcher - Independent", "Independent", "North America", 1),
        ("Maria Rodriguez", "Technologist - Diverse Tech Background", "Tech Worker Alliance", "Latin America", 1),
        ("Dr. Amara Okonkwo", "Healthcare Ethicist", "Doctors Without Borders", "Africa", 1),
        ("Professor David Kumar", "Academic - Computer Science", "MIT", "North America", 1),
        ("Yuki Tanaka", "Government Observer (non-voting)", "US State Dept", "North America", 0),
        ("Sophie Dubois", "European Regulator Observer", "EU Commission", "Europe", 0),
        ("Carlos Mendez", "Industry Representative - Healthcare", "Mayo Clinic", "North America", 1),
        ("Dr. Rashida Hassan", "Affected Communities Advocate", "Grassroots Coalition", "Africa", 1),
        ("Professor Michael O'Brien", "Law & Policy", "Harvard Law", "North America", 1),
        ("Aisha Patel", "Labor Union Representative", "Service Employees International", "North America", 1),
        ("Dr. Jonas Bergström", "Quantum Computing Researcher", "Swedish Royal Institute", "Europe", 1),
    ]

    # Check if board already initialized
    c.execute('SELECT COUNT(*) FROM board_members')
    if c.fetchone()[0] == 0:
        for name, role, affiliation, region, voting_power in board_members:
            c.execute('''
                INSERT INTO board_members (name, role, affiliation, region, voting_power)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, role, affiliation, region, voting_power))

        conn.commit()
        print(f"✓ Governance board initialized with {len(board_members)} members\n")

        # List members
        c.execute('SELECT id, name, role, region, voting_power FROM board_members ORDER BY id')
        members = c.fetchall()

        print("Board Members:")
        print("="*70)
        voting_count = 0
        for mid, name, role, region, voting_power in members:
            status = "VOTING" if voting_power == 1 else "OBSERVER"
            print(f"  {mid:2d}. {name:30s} | {role:40s} | {status}")
            if voting_power == 1:
                voting_count += 1

        print("="*70)
        print(f"\nTotal voting members: {voting_count}")
        print(f"Quorum requirement: {voting_count // 2 + 1} votes")
        print(f"Decision rule: Simple majority\n")

    else:
        print("✓ Governance board already initialized")
        c.execute('SELECT COUNT(*) FROM board_members WHERE voting_power = 1')
        voting_count = c.fetchone()[0]
        print(f"  Voting members: {voting_count}")

    conn.close()

    # Generate board report
    generate_board_report()

    print("="*70)
    print("✓ Governance system ready")
    print("="*70 + "\n")

def generate_board_report():
    """Generate report of pending decisions"""

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT id, system_name, violation_type, severity, affected_count FROM violations ORDER BY detected_at DESC')
    violations = c.fetchall()

    print("\nVIOLATIONS AWAITING BOARD DECISION:")
    print("-"*70)

    if not violations:
        print("No violations pending board review")
    else:
        for vid, system, vtype, severity, affected in violations:
            print(f"\n  Violation ID {vid}: {system}")
            print(f"    Type: {vtype}")
            print(f"    Severity: {severity}")
            print(f"    Affected: {affected:,} persons")
            print(f"    Status: AWAITING BOARD VOTE")

    conn.close()

if __name__ == '__main__':
    try:
        init_governance()
    except Exception as e:
        print(f"✗ Error: {e}")
