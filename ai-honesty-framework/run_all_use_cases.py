#!/usr/bin/env python3
"""
Master runner for AI Honesty Framework use cases
"""

import sys
import json
import subprocess
from pathlib import Path

def run_all_use_cases():
    """Run all 5 AI honesty use cases"""

    print("\n" + "="*100)
    print("AI HONESTY FRAMEWORK - ALL USE CASES")
    print("="*100)

    use_cases = [
        ("use_case_1_reasoning_audit_trail.py", "Reasoning Audit Trail (AAPF)"),
        ("use_case_2_hard_deny_hallucinations.py", "Hard-Deny Hallucinations (NAP)"),
        ("use_case_3_trustworthiness_classification.py", "Trustworthiness Classification (DCF)"),
        ("use_case_4_reasoning_freshness.py", "Reasoning Freshness (CCF)"),
        ("use_case_5_model_degradation.py", "Model Degradation Tracking (PCSF)"),
    ]

    results = {}

    for script, title in use_cases:
        script_path = Path(script)

        if not script_path.exists():
            print(f"\n[ERROR] {script} not found")
            continue

        print(f"\n\n{'='*100}")
        print(f"RUNNING: {title}")
        print(f"{'='*100}")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=False,
                text=True,
                timeout=30
            )

            results[title] = "SUCCESS" if result.returncode == 0 else "FAILED"

        except subprocess.TimeoutExpired:
            results[title] = "TIMEOUT"
        except Exception as e:
            results[title] = f"ERROR: {str(e)}"

    # Summary report
    print(f"\n\n{'='*100}")
    print("SUMMARY REPORT")
    print(f"{'='*100}\n")

    for title, status in results.items():
        status_symbol = "[OK]" if status == "SUCCESS" else "[FAIL]"
        print(f"{status_symbol} {title}: {status}")

    # Check for generated files
    print(f"\n\n{'='*100}")
    print("GENERATED COMPLIANCE PACKETS")
    print(f"{'='*100}\n")

    packet_files = [
        "use_case_1_diagnosis_packet.json",
        "use_case_2_hallucination_prevention_packet.json",
        "use_case_3_classification_packet.json",
        "use_case_4_freshness_packet.json",
        "use_case_5_degradation_packet.json"
    ]

    for packet_file in packet_files:
        packet_path = Path(packet_file)
        if packet_path.exists():
            size_kb = packet_path.stat().st_size / 1024
            print(f"[OK] {packet_file} ({size_kb:.1f} KB)")

            try:
                with open(packet_path) as f:
                    packet = json.load(f)

                use_case = packet.get("use_case", "unknown")
                chain_length = len(packet.get("provenance_chain", []))
                valid = packet.get("chain_valid", False)

                print(f"     Use case: {use_case}")
                print(f"     Chain length: {chain_length}")
                print(f"     Chain valid: {valid}")

            except Exception as e:
                print(f"     (Could not parse: {e})")
        else:
            print(f"[FAIL] {packet_file} (not found)")

    # Framework capabilities summary
    print(f"\n\n{'='*100}")
    print("FRAMEWORK MECHANISMS DEMONSTRATED")
    print(f"{'='*100}\n")

    mechanisms = {
        "AAPF (Action Provenance)": [
            "Use case 1: Medical diagnosis reasoning audit trail",
            "Use case 2: Hallucination attempt logging",
            "Use case 3: Claim-by-claim reasoning tracking",
            "Use case 4: Real-time analysis reasoning",
            "Use case 5: Degradation monitoring"
        ],
        "NAP (Hard-Deny Rules)": [
            "Use case 2: Prevent hallucinated citations",
            "Use case 3: Prevent false confidence claims",
            "Use case 5: Prevent unfair model usage"
        ],
        "DCF (Classification)": [
            "Use case 1: Classify diagnosis by confidence",
            "Use case 3: Classify claims by trustworthiness (PUBLIC/INTERNAL/CONFIDENTIAL/SECRET)",
            "Use case 4: Classify analysis timeliness"
        ],
        "CCF (Freshness Proof)": [
            "Use case 4: Prove analysis based on real-time data",
            "Use case 4: Time-bounded freshness guarantee"
        ],
        "PCSF (Capacity/Degradation)": [
            "Use case 5: Track accuracy degradation over time",
            "Use case 5: Detect demographic bias drift",
            "Use case 5: Log remediation actions"
        ]
    }

    for mechanism, examples in mechanisms.items():
        print(f"{mechanism}:")
        for example in examples:
            print(f"  - {example}")
        print()

    # Key findings
    print(f"\n{'='*100}")
    print("KEY FINDINGS")
    print(f"{'='*100}\n")

    findings = [
        "1. AI Honesty Framework provides cryptographic proof of honest outputs",
        "   - Every reasoning step is logged and signed (AAPF)",
        "   - Hard-deny rules prevent false claims (NAP)",
        "   - Outputs classified by trustworthiness level (DCF)",
        "   - Analysis freshness is verifiable (CCF)",
        "   - Model quality is continuously tracked (PCSF)",
        "",
        "2. Framework is applicable across multiple AI use cases:",
        "   - Healthcare (diagnosis reasoning, bias detection)",
        "   - Legal (hallucination prevention, citation verification)",
        "   - Finance (confidence classification, real-time analysis)",
        "   - Criminal Justice (fairness monitoring, degradation detection)",
        "",
        "3. Cryptographic proof provides legal defensibility:",
        "   - Merkle root proves chain integrity",
        "   - Signatures prove actions are authentic",
        "   - Complete audit trail is immutable",
        "   - Court-defensible evidence of honest AI operation",
        "",
        "4. Framework enables AI transparency and accountability:",
        "   - Users can verify reasoning quality",
        "   - Regulators can audit AI decision-making",
        "   - Companies can prove fair and honest AI practices",
        "   - Society gains confidence in AI systems"
    ]

    for finding in findings:
        print(finding)

    print(f"\n{'='*100}\n")


if __name__ == "__main__":
    run_all_use_cases()
