#!/usr/bin/env python3
"""
Real Data Ingestion API
Accepts violation reports, remediations, and predictions from real systems
"""

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = r'C:\nodes\data.db'

def init_db():
    """Initialize database from schema"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        with open(r'C:\nodes\schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print(f"✓ Database initialized at {DB_PATH}")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# VIOLATION REPORTING
# ============================================================================

@app.route('/api/report/violation', methods=['POST'])
def report_violation():
    """
    Report a new violation

    POST /api/report/violation
    {
      "system": "Hospital XYZ Medical AI",
      "type": "Diagnostic Accuracy Gap",
      "severity": "HIGH",
      "affected_count": 2400,
      "description": "8% accuracy gap between demographic groups"
    }
    """
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute('''INSERT INTO violations
                (system_name, violation_type, severity, affected_count, harm_description, status)
                VALUES (?, ?, ?, ?, ?, ?)''',
              (data['system'],
               data['type'],
               data.get('severity', 'MEDIUM'),
               data.get('affected_count', 0),
               data.get('description', ''),
               'INVESTIGATING'))

    conn.commit()
    violation_id = c.lastrowid
    conn.close()

    return jsonify({
        'status': 'received',
        'violation_id': violation_id,
        'timestamp': datetime.now().isoformat()
    }), 201

@app.route('/api/violations/all', methods=['GET'])
def get_all_violations():
    """Get all violations from database"""
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM violations ORDER BY detected_at DESC')
    violations = [dict(row) for row in c.fetchall()]
    conn.close()

    return jsonify(violations)

# ============================================================================
# REMEDIATION TRACKING
# ============================================================================

@app.route('/api/report/remediation', methods=['POST'])
def report_remediation():
    """
    Report remediation progress

    POST /api/report/remediation
    {
      "violation_id": 1,
      "plan": "Retrain model on balanced dataset",
      "progress": 45,
      "due_date": "2026-06-07"
    }
    """
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute('''INSERT INTO remediations
                (violation_id, remediation_plan, progress_percent, status)
                VALUES (?, ?, ?, ?)''',
              (data['violation_id'],
               data.get('plan', ''),
               data.get('progress', 0),
               'IN_PROGRESS'))

    conn.commit()
    conn.close()

    return jsonify({
        'status': 'received',
        'timestamp': datetime.now().isoformat()
    }), 201

@app.route('/api/remediations/all', methods=['GET'])
def get_all_remediations():
    """Get all remediations"""
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM remediations ORDER BY created_at DESC')
    remediations = [dict(row) for row in c.fetchall()]
    conn.close()

    return jsonify(remediations)

# ============================================================================
# AFFECTED PERSONS REGISTRY
# ============================================================================

@app.route('/api/report/affected-person', methods=['POST'])
def report_affected_person():
    """
    Report an affected person

    POST /api/report/affected-person
    {
      "violation_id": 1,
      "demographic": "African American Female",
      "harm_amount": 50000,
      "restitution_status": "PENDING"
    }
    """
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute('''INSERT INTO affected_persons
                (violation_id, demographic, harm_amount, restitution_status)
                VALUES (?, ?, ?, ?)''',
              (data['violation_id'],
               data.get('demographic', 'Unknown'),
               data.get('harm_amount', 0),
               data.get('restitution_status', 'PENDING')))

    conn.commit()
    conn.close()

    return jsonify({
        'status': 'received',
        'timestamp': datetime.now().isoformat()
    }), 201

@app.route('/api/affected-persons/all', methods=['GET'])
def get_all_affected():
    """Get all affected persons"""
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM affected_persons ORDER BY created_at DESC')
    affected = [dict(row) for row in c.fetchall()]
    conn.close()

    return jsonify(affected)

# ============================================================================
# PREDICTIONS
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def add_prediction():
    """
    Add a prediction/forecast

    POST /api/predict
    {
      "system": "Hospital XYZ Medical AI",
      "type": "violation_risk",
      "forecast_date": "2026-06-07",
      "confidence": 0.85,
      "impact": "HIGH"
    }
    """
    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute('''INSERT INTO predictions
                (system_name, prediction_type, forecast_date, confidence_score, predicted_impact)
                VALUES (?, ?, ?, ?, ?)''',
              (data['system'],
               data.get('type', 'unknown'),
               data.get('forecast_date'),
               data.get('confidence', 0),
               data.get('impact', 'MEDIUM')))

    conn.commit()
    conn.close()

    return jsonify({
        'status': 'received',
        'timestamp': datetime.now().isoformat()
    }), 201

@app.route('/api/predictions/all', methods=['GET'])
def get_all_predictions():
    """Get all predictions"""
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM predictions ORDER BY created_at DESC')
    predictions = [dict(row) for row in c.fetchall()]
    conn.close()

    return jsonify(predictions)

# ============================================================================
# HEALTH & STATUS
# ============================================================================

@app.route('/api/ingest/status', methods=['GET'])
def ingest_status():
    """Get ingestion system status"""
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM violations')
    violation_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM remediations')
    remediation_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM affected_persons')
    affected_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM predictions')
    prediction_count = c.fetchone()[0]

    conn.close()

    return jsonify({
        'status': 'OPERATIONAL',
        'timestamp': datetime.now().isoformat(),
        'database': DB_PATH,
        'counts': {
            'violations': violation_count,
            'remediations': remediation_count,
            'affected_persons': affected_count,
            'predictions': prediction_count
        }
    })

@app.route('/api/ingest/reset', methods=['POST'])
def reset_database():
    """WARNING: Reset all data (development only)"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        init_db()
        return jsonify({'status': 'database reset'})
    return jsonify({'status': 'nothing to reset'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  REAL DATA INGESTION API")
    print("="*60)

    init_db()

    print("\n✓ Database ready")
    print("✓ Ingestion API starting on port 5010")
    print("\nEndpoints:")
    print("  POST /api/report/violation")
    print("  POST /api/report/remediation")
    print("  POST /api/report/affected-person")
    print("  POST /api/predict")
    print("  GET  /api/violations/all")
    print("  GET  /api/predictions/all")
    print("  GET  /api/ingest/status")
    print("\n" + "="*60 + "\n")

    app.run(host='127.0.0.1', port=5010, debug=False)
