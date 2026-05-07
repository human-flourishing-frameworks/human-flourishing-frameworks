#!/usr/bin/env python3
"""
Prediction Engine
Analyzes historical violations and generates forecasts
"""

import sqlite3
from datetime import datetime, timedelta
import numpy as np

DB_PATH = r'C:\nodes\data.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def analyze_violations():
    """Analyze stored violations and generate predictions"""

    print("\n" + "="*60)
    print("  PREDICTION ENGINE - ANALYZING HISTORICAL DATA")
    print("="*60 + "\n")

    conn = get_db()
    c = conn.cursor()

    # Get all violations
    c.execute('SELECT * FROM violations ORDER BY detected_at')
    violations = [dict(row) for row in c.fetchall()]

    print(f"Analyzing {len(violations)} violations...\n")

    if len(violations) == 0:
        print("No violations to analyze yet.")
        conn.close()
        return

    # Analyze by system
    systems = {}
    for v in violations:
        system = v['system_name']
        if system not in systems:
            systems[system] = []
        systems[system].append(v)

    print("="*60)
    print("  SYSTEM ANALYSIS")
    print("="*60)

    for system_name, sys_violations in systems.items():
        print(f"\n{system_name}:")
        print(f"  Total violations: {len(sys_violations)}")

        # Calculate severity trend
        severities = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
        severity_scores = [severities.get(v['severity'], 1) for v in sys_violations]

        if len(severity_scores) > 1:
            # Simple trend analysis
            x = np.arange(len(severity_scores))
            trend = np.polyfit(x, severity_scores, 1)

            print(f"  Trend: {'WORSENING' if trend[0] > 0.1 else 'IMPROVING' if trend[0] < -0.1 else 'STABLE'}")
            print(f"  Affected persons: {sum(v['affected_count'] for v in sys_violations):,}")

            # Generate prediction
            if trend[0] > 0.2:
                prediction = "ESCALATING - Expect more violations within 30 days"
                confidence = 0.85
                impact = "CRITICAL"
            elif trend[0] > 0.05:
                prediction = "CONCERNING TREND - Monitor for further violations"
                confidence = 0.75
                impact = "HIGH"
            else:
                prediction = "STABLE OR IMPROVING - Continue current remediation efforts"
                confidence = 0.80
                impact = "MEDIUM"

            print(f"  Forecast: {prediction}")
            print(f"  Confidence: {confidence:.0%}")

    print("\n" + "="*60)
    print("  REMEDIATION PROGRESS")
    print("="*60 + "\n")

    c.execute('SELECT v.system_name, r.progress_percent FROM violations v LEFT JOIN remediations r ON v.id = r.violation_id')
    remediation_data = c.fetchall()

    if remediation_data:
        for system, progress in remediation_data:
            if progress is not None:
                print(f"{system}: {progress}% complete")

    print("\n" + "="*60)
    print("  AFFECTED PERSONS ANALYSIS")
    print("="*60 + "\n")

    c.execute('''
        SELECT ap.demographic, COUNT(*) as count, SUM(ap.harm_amount) as total_harm
        FROM affected_persons ap
        GROUP BY ap.demographic
        ORDER BY total_harm DESC
    ''')

    affected_summary = c.fetchall()
    total_harm = sum(row['total_harm'] or 0 for row in affected_summary)

    print(f"Total affected persons groups: {len(affected_summary)}")
    print(f"Total quantified harm: ${total_harm:,.0f}\n")

    for row in affected_summary:
        demographic = row['demographic']
        count = row['count']
        harm = row['total_harm'] or 0
        print(f"  {demographic}: {count} affected, ${harm:,.0f} total harm")

    print("\n" + "="*60)
    print("  FORWARD PREDICTIONS")
    print("="*60 + "\n")

    c.execute('SELECT * FROM predictions ORDER BY forecast_date')
    predictions = [dict(row) for row in c.fetchall()]

    if predictions:
        print(f"Total predictions on file: {len(predictions)}\n")
        for p in predictions[:10]:  # Show first 10
            forecast = datetime.strptime(p['forecast_date'], '%Y-%m-%d').strftime('%B %d, %Y')
            print(f"  {p['system_name']}")
            print(f"    Type: {p['prediction_type']}")
            print(f"    Forecast: {forecast}")
            print(f"    Confidence: {p['confidence_score']:.0%}")
            print(f"    Impact: {p['predicted_impact']}\n")

    conn.close()

    print("="*60)
    print("✓ Prediction analysis complete")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        analyze_violations()
    except FileNotFoundError:
        print("✗ Database not found. Run ingest_api.py first to create it.")
    except Exception as e:
        print(f"✗ Error: {e}")
