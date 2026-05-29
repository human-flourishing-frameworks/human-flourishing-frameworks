from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "arc-reactor-mining-lab"
CONFIG_DIR = ROOT / "configs" / "arc-reactor-mining-lab"
DOC_DIR = ROOT / "docs" / "arc-reactor-mining-lab"
PDF_PATH = ROOT / "ARC-REACTOR-MINING-LAB-SAFE-MULTI-COIN-PLAN.pdf"
WORKBOOK_PATH = DATA_DIR / "arc_reactor_mining_lab_workbook.xlsx"


EXPECTED_CSV_HEADERS = {
    "hardware-intake.csv": [
        "device_id",
        "owner",
        "site",
        "device_type",
        "make_model",
        "algorithm_lane",
        "hashrate_input",
        "hashrate_unit",
        "tdp_watts",
        "measured_wall_watts",
        "hours_per_day",
        "kwh_rate_usd",
        "overhead_pct",
        "cooling_status",
        "breaker_circuit",
        "notes",
    ],
    "wallet-matrix.csv": [
        "coin",
        "ticker",
        "network",
        "algorithm",
        "hardware_lane",
        "wallet_software",
        "address_status",
        "receive_address",
        "pool_or_mode",
        "off_ramp_status",
        "notes",
    ],
    "profitability-model.csv": [
        "scenario_id",
        "coin",
        "ticker",
        "hashrate",
        "hashrate_unit",
        "gross_coin_per_day",
        "coin_price_usd",
        "pool_fee_pct",
        "device_watts",
        "overhead_pct",
        "hours_per_day",
        "kwh_rate_usd",
        "gross_revenue_usd_formula",
        "power_cost_usd_formula",
        "pool_fee_usd_formula",
        "net_usd_formula",
        "refresh_required",
        "notes",
    ],
    "airdrop-faucet-tracker.csv": [
        "item_id",
        "coin_or_network",
        "type",
        "url",
        "status",
        "wallet_required",
        "kyc_required",
        "risk_notes",
        "last_checked",
        "operator_notes",
    ],
    "sources.csv": [
        "source_id",
        "title",
        "url",
        "source_type",
        "used_for",
        "as_of",
        "notes",
    ],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    expected = EXPECTED_CSV_HEADERS[path.name]
    if reader.fieldnames != expected:
        raise AssertionError(f"{path.name} header mismatch: {reader.fieldnames}")
    if not rows:
        raise AssertionError(f"{path.name} has no data rows")
    return rows


def validate_jsonl(path: Path) -> None:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise AssertionError(f"{path.name}:{line_number} blank JSONL line")
            payload = json.loads(line)
            if "event_type" not in payload or "coin" not in payload:
                raise AssertionError(f"{path.name}:{line_number} missing core fields")
            forbidden_keys = {"private_key", "private_keys", "seed_phrase", "seed", "mnemonic"}
            if forbidden_keys.intersection(payload.keys()):
                raise AssertionError(f"{path.name}:{line_number} contains forbidden secret field")


def main() -> None:
    for relative in [
        DOC_DIR / "README.md",
        DOC_DIR / "SELL-OFF-CHECKLIST.md",
        CONFIG_DIR / "xmrig-config.sample.json",
        CONFIG_DIR / "kawpowminer.sample.args.txt",
        CONFIG_DIR / "kaspa-asic-intake.sample.csv",
    ]:
        if not relative.exists() or relative.stat().st_size < 100:
            raise AssertionError(f"Missing or tiny artifact: {relative}")

    for csv_name in EXPECTED_CSV_HEADERS:
        read_csv(DATA_DIR / csv_name)

    validate_jsonl(DATA_DIR / "receipt-ledger-template.jsonl")

    xmrig = json.loads((CONFIG_DIR / "xmrig-config.sample.json").read_text(encoding="utf-8"))
    pool = xmrig["pools"][0]
    if "YOUR_XMR_RECEIVE_ADDRESS_ONLY" not in pool["user"]:
        raise AssertionError("XMRig sample must keep receive-address placeholder")
    if pool.get("tls") is not True:
        raise AssertionError("XMRig sample should default to TLS")

    for artifact in [PDF_PATH, WORKBOOK_PATH]:
        if not artifact.exists() or artifact.stat().st_size < 5000:
            raise AssertionError(f"Missing or tiny generated artifact: {artifact}")

    try:
        import pypdf
    except Exception:
        pypdf = None
    if pypdf is not None:
        reader = pypdf.PdfReader(str(PDF_PATH))
        if len(reader.pages) < 4:
            raise AssertionError("PDF should be more than a thin cover sheet")
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        for phrase in ["No private keys", "Monero", "Ravencoin", "Kaspa", "Electricity"]:
            if phrase not in text:
                raise AssertionError(f"PDF missing phrase: {phrase}")

    print("ARC_REACTOR_MINING_LAB_VALIDATION_OK")


if __name__ == "__main__":
    main()
