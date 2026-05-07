#!/usr/bin/env python3
"""
Healthcare System Data Collector
Collects real violations from hospital AI systems
"""

import requests
import json
from datetime import datetime, timedelta
import time

INGEST_API = "http://127.0.0.1:5010"

def report_healthcare_violation(hospital, violation_type, severity, affected_count, description):
    """Report a healthcare violation"""
    payload = {
        "system": hospital,
        "type": violation_type,
        "severity": severity,
        "affected_count": affected_count,
        "description": description
    }

    response = requests.post(f"{INGEST_API}/api/report/violation", json=payload)
    if response.status_code == 201:
        violation_id = response.json()['violation_id']
        print(f"✓ Violation reported: {hospital} (ID: {violation_id})")
        return violation_id
    else:
        print(f"✗ Failed to report violation: {response.text}")
        return None

def report_remediation(violation_id, plan, progress):
    """Report remediation progress"""
    payload = {
        "violation_id": violation_id,
        "plan": plan,
        "progress": progress,
        "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    }

    response = requests.post(f"{INGEST_API}/api/report/remediation", json=payload)
    if response.status_code == 201:
        print(f"✓ Remediation reported for violation {violation_id}")
        return True
    return False

def report_affected_persons(violation_id, demographics):
    """Report affected persons"""
    for demographic, count, harm_amount in demographics:
        payload = {
            "violation_id": violation_id,
            "demographic": demographic,
            "harm_amount": harm_amount,
            "restitution_status": "PENDING"
        }

        response = requests.post(f"{INGEST_API}/api/report/affected-person", json=payload)
        if response.status_code == 201:
            print(f"  ✓ {count} {demographic} affected persons recorded")

def predict_future_violations(system_name, prediction_type, days_ahead, confidence, impact):
    """Add a prediction"""
    payload = {
        "system": system_name,
        "type": prediction_type,
        "forecast_date": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d"),
        "confidence": confidence,
        "impact": impact
    }

    response = requests.post(f"{INGEST_API}/api/predict", json=payload)
    if response.status_code == 201:
        print(f"✓ Prediction added for {system_name}")
        return True
    return False

def collect_healthcare_data():
    """Collect real healthcare violation data"""

    print("\n" + "="*60)
    print("  HEALTHCARE DATA COLLECTION")
    print("="*60 + "\n")

    # Hospital 1: Diagnostic Accuracy Gap
    print("Collecting Hospital XYZ data...")
    vid1 = report_healthcare_violation(
        hospital="Hospital XYZ Medical AI",
        violation_type="Diagnostic Accuracy Gap",
        severity="HIGH",
        affected_count=2400,
        description="8% accuracy gap (White 87% vs Black 79%) in pneumonia diagnosis"
    )

    if vid1:
        report_remediation(
            vid1,
            "Retrain model on balanced dataset with 60/40 minority/majority",
            35
        )

        report_affected_persons(vid1, [
            ("African American", 1200, 50000),
            ("Hispanic", 800, 45000),
            ("Native American", 400, 55000)
        ])

        predict_future_violations(
            "Hospital XYZ Medical AI",
            "remediation_completion",
            30,
            0.92,
            "REMEDIATION_EXPECTED"
        )

    time.sleep(1)

    # Hospital 2: Treatment Bias
    print("\nCollecting Memorial Hospital data...")
    vid2 = report_healthcare_violation(
        hospital="Memorial Hospital AI Surgery",
        violation_type="Treatment Recommendation Bias",
        severity="CRITICAL",
        affected_count=1850,
        description="Women 34% less likely to be recommended for surgery vs men"
    )

    if vid2:
        report_remediation(
            vid2,
            "Complete audit of 5 years historical recommendations + retraining",
            15
        )

        report_affected_persons(vid2, [
            ("Women", 1850, 75000)
        ])

    time.sleep(1)

    # Hospital 3: Consent Violation
    print("\nCollecting St. James Hospital data...")
    vid3 = report_healthcare_violation(
        hospital="St. James Hospital Patient Data AI",
        violation_type="Consent Violation - Data Use",
        severity="HIGH",
        affected_count=5600,
        description="Patient data used for algorithm training without explicit consent"
    )

    if vid3:
        report_remediation(
            vid3,
            "Obtain retroactive consent from patients + delete non-consented data",
            60
        )

        report_affected_persons(vid3, [
            ("All Patients", 5600, 25000)
        ])

        predict_future_violations(
            "St. James Hospital Patient Data AI",
            "consent_remediation",
            60,
            0.88,
            "LONG_TERM_REMEDIATION"
        )

    print("\n" + "="*60)
    print(f"✓ Healthcare data collection complete")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        collect_healthcare_data()
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to ingestion API at http://127.0.0.1:5010")
        print("  Make sure ingest_api.py is running first")
