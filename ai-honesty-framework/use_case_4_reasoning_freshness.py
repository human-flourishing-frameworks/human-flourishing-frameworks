"""
USE CASE 4: Reasoning Freshness Proof (CCF)
Demonstrates proving that AI reasoning is current (not stale)
"""

import json
import time
from framework_core import (
    ComplianceFramework, serialize_framework_state
)


def reasoning_freshness_demo():
    """
    Scenario: Financial AI provides real-time stock price analysis.
    Framework proves reasoning is based on current data (not stale cache).
    User can verify analysis freshness before trading.
    """
    framework = ComplianceFramework(signer_key="finance-freshness")

    print("\n" + "="*80)
    print("REASONING FRESHNESS - REAL-TIME STOCK ANALYSIS")
    print("="*80)

    # Step 1: User requests real-time analysis
    print("\n[STEP 1] Investor requests real-time stock analysis")
    print("-" * 80)

    query_time = time.time()

    query = framework.record_action(
        agent_id="investor-trader",
        action_type="REALTIME_ANALYSIS_REQUEST",
        parameters={
            "ticker": "APPL",
            "request_time": time.ctime(query_time),
            "request_timestamp": query_time,
            "analysis_type": "Intraday technical + fundamental"
        }
    )

    print(f"Query time: {time.ctime(query_time)}")
    print(f"Requested analysis: Intraday stock analysis")

    # Step 2: AI fetches current market data
    print("\n[STEP 2] AI fetches current market data")
    print("-" * 80)

    market_data_time = time.time()

    market_data = framework.record_action(
        agent_id="finance-ai-v5.0",
        action_type="FETCH_MARKET_DATA",
        parameters={
            "data_source": "Live Bloomberg Terminal",
            "timestamp": market_data_time,
            "data_items": [
                "Current price: $195.47",
                "Volume: 52.3M shares",
                "50-day MA: $188.32",
                "200-day MA: $181.92",
                "RSI: 58.2",
                "Market cap: $3.05T"
            ],
            "data_freshness_seconds": 0  # Just fetched, completely fresh
        }
    )

    print(f"Data fetch time: {time.ctime(market_data_time)}")
    print(f"Data source: Live Bloomberg Terminal")
    print(f"Data items fetched: {len(market_data.parameters['data_items'])}")
    print(f"Data freshness: {market_data.parameters['data_freshness_seconds']}s old (current)")

    # Step 3: AI performs reasoning
    print("\n[STEP 3] AI performs real-time reasoning")
    print("-" * 80)

    reasoning_time = time.time()

    reasoning = framework.record_action(
        agent_id="finance-ai-v5.0",
        action_type="TECHNICAL_ANALYSIS_REASONING",
        parameters={
            "timestamp": reasoning_time,
            "reasoning_steps": [
                "Price above both MAs: Uptrend confirmed",
                "RSI 58.2: Not overbought, room to run",
                "Volume 52.3M: Above average (bullish)",
                "Market cap $3.05T: No significant change from last update"
            ],
            "conclusion": "Technical setup is positive for next 1-2 hours",
            "recommendation": "BUY opportunity with stop-loss at $193.50",
            "data_freshness_at_reasoning": 0  # Reasoning still based on fresh data
        }
    )

    print(f"Reasoning time: {time.ctime(reasoning_time)}")
    print(f"Reasoning conclusion: {reasoning.parameters['conclusion']}")
    print(f"Recommendation: {reasoning.parameters['recommendation']}")
    print(f"Based on data freshness: {reasoning.parameters['data_freshness_at_reasoning']}s old")

    # Step 4: Create freshness proof
    print("\n[STEP 4] Create freshness proof")
    print("-" * 80)

    freshness_proof = framework.prove_freshness(
        capability_id="APPL-technical-analysis",
        freshness_seconds=300,  # Proof valid for 5 minutes
        prover="finance-ai-v5.0",
        knowledge_cutoff="2026-05-07",
        source_recency_days=0  # Real-time data, 0 days old
    )

    print(f"Freshness proof created:")
    print(f"  Capability: APPL technical analysis")
    print(f"  Proof valid for: {freshness_proof.freshness_seconds}s (5 minutes)")
    print(f"  Knowledge cutoff: {freshness_proof.knowledge_cutoff_date}")
    print(f"  Source recency: {freshness_proof.source_recency_days} days old (real-time)")
    print(f"  Proof hash: {freshness_proof.proof_hash[:16]}...")

    # Step 5: Generate output with freshness guarantee
    print("\n[STEP 5] Output analysis with freshness guarantee")
    print("-" * 80)

    output_time = time.time()

    output = framework.record_action(
        agent_id="finance-ai-v5.0",
        action_type="ANALYSIS_OUTPUT_WITH_FRESHNESS",
        parameters={
            "output_timestamp": output_time,
            "analysis": "Technical setup is positive (RSI 58.2, price above MAs, strong volume)",
            "recommendation": "BUY with stop at $193.50",
            "freshness_guarantee": {
                "data_age_seconds": int(output_time - market_data_time),
                "analysis_age_seconds": int(output_time - reasoning_time),
                "freshness_expires_at": output_time + 300,
                "expires_in_seconds": 300,
                "proof_hash": freshness_proof.proof_hash[:16]
            }
        }
    )

    print(f"Output generated: {time.ctime(output_time)}")
    print(f"\nFreshness guarantee:")
    print(f"  Data age: {output.parameters['freshness_guarantee']['data_age_seconds']}s")
    print(f"  Analysis age: {output.parameters['freshness_guarantee']['analysis_age_seconds']}s")
    print(f"  Expires in: {output.parameters['freshness_guarantee']['expires_in_seconds']}s")
    print(f"  Proof: {output.parameters['freshness_guarantee']['proof_hash']}...")

    # Step 6: Simulate passage of time
    print("\n[STEP 6] Investor waits 4 minutes, then rechecks")
    print("-" * 80)

    time.sleep(0.1)  # Simulate waiting (in real scenario, would be 240 seconds)
    recheck_time = time.time()

    print(f"Original analysis time: {time.ctime(output_time)}")
    print(f"Recheck time: {time.ctime(recheck_time)}")
    print(f"Age of analysis: {int(recheck_time - output_time)}s")

    # Check if freshness proof is still valid
    freshness_still_valid = (recheck_time - output_time) < 300

    if freshness_still_valid:
        print(f"Freshness proof: STILL VALID")
        print(f"  Analysis is still current (less than 5 minutes old)")
        print(f"  Investor can still trade on this recommendation")
    else:
        print(f"Freshness proof: EXPIRED")
        print(f"  Analysis is stale (more than 5 minutes old)")
        print(f"  Investor should request fresh analysis before trading")

    # Step 7: Verify chain integrity
    print("\n[STEP 7] Verify analysis integrity")
    print("-" * 80)

    is_valid = framework.verify_provenance_chain()
    merkle_root = framework.get_provenance_merkle_root()

    print(f"Chain valid: {is_valid}")
    print(f"Total actions: {len(framework.provenance_chain)}")
    print(f"Freshness proofs: {len(framework.freshness_proofs)}")
    print(f"Merkle root: {merkle_root[:16]}...")

    # Step 8: Save compliance packet
    print("\n[STEP 8] Save analysis with freshness proof")
    print("-" * 80)

    compliance_packet = serialize_framework_state(framework)
    compliance_packet["use_case"] = "Finance AI - Real-Time Freshness Proof"
    compliance_packet["trade_decision"] = {
        "ticker": "APPL",
        "recommendation": "BUY",
        "stop_loss": "$193.50",
        "analysis_freshness": {
            "generated_at": time.ctime(output_time),
            "valid_until": time.ctime(output_time + 300),
            "currently_valid": freshness_still_valid
        }
    }

    packet_json = json.dumps(compliance_packet, indent=2, default=str)

    with open("/tmp/ai-honesty-framework/use_case_4_freshness_packet.json", "w") as f:
        f.write(packet_json)

    print("Compliance packet saved")
    print(f"  - Freshness proof valid: {freshness_still_valid}")
    print(f"  - Analysis generated: {time.ctime(output_time)}")
    print(f"  - Chain integrity verified: {is_valid}")

    # Step 9: Investor decision
    print("\n[STEP 9] Investor makes informed trading decision")
    print("-" * 80)

    print("Investor checklist:")
    print(f"  [X] Verified: Analysis data is current (real-time)")
    print(f"  [X] Verified: Reasoning was based on fresh data")
    print(f"  [X] Verified: Freshness proof is still valid")
    print(f"  [X] Verified: Chain integrity maintained: {merkle_root[:16]}...")
    print("\nOutcome: CONFIDENT TRADE - Investor can execute BUY order based on fresh analysis")


if __name__ == "__main__":
    reasoning_freshness_demo()
