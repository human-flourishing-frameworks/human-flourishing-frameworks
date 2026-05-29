import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), "..");
const outputDir = path.join(root, "data", "arc-reactor-mining-lab");
const outputPath = path.join(outputDir, "arc_reactor_mining_lab_workbook.xlsx");

const workbook = Workbook.create();

function sheet(name) {
  const ws = workbook.worksheets.add(name);
  ws.showGridLines = false;
  return ws;
}

function write(ws, range, values) {
  ws.getRange(range).values = values;
}

function formulas(ws, range, values) {
  ws.getRange(range).formulas = values;
}

function styleHeader(ws, range) {
  ws.getRange(range).format = {
    fill: "#12343B",
    font: { bold: true, color: "#FFFFFF" },
  };
}

function styleTitle(ws, range) {
  ws.getRange(range).format = {
    fill: "#0F766E",
    font: { bold: true, color: "#FFFFFF", size: 14 },
  };
}

function setWidths(ws, widths) {
  widths.forEach((width, index) => {
    const letter = String.fromCharCode("A".charCodeAt(0) + index);
    ws.getRange(`${letter}:${letter}`).format.columnWidthPx = width;
  });
}

const cover = workbook.worksheets.getOrAdd("Cover", { renameFirstIfOnlyNewSpreadsheet: true });
cover.showGridLines = false;
write(cover, "A1:H1", [["Arc Reactor Mining Lab", "", "", "", "", "", "", ""]]);
styleTitle(cover, "A1:H1");
write(cover, "A3:B10", [
  ["Workbook purpose", "Operator-owned mining intake, model, tracking, and source audit"],
  ["Status", "Template - fill with current measured values before decisions"],
  ["Safety boundary", "Receive addresses only; no private keys, seed phrases, or hidden mining"],
  ["Default power rate", 0.182],
  ["Default overhead", 0.15],
  ["As-of date", "2026-05-29"],
  ["Model convention", "USD/day unless noted"],
  ["Decision rule", "Run only bounded tests unless refreshed net estimate and safety checks pass"],
]);
cover.getRange("B6:B7").format.font = { color: "#0000FF" };
cover.getRange("B6").format.numberFormat = "$0.000";
cover.getRange("B7").format.numberFormat = "0.0%";
setWidths(cover, [180, 520, 80, 80, 80, 80, 80, 80]);

const hardware = sheet("Hardware Intake");
write(hardware, "A1:P1", [[
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
]]);
write(hardware, "A2:P4", [
  ["cpu-01", "operator", "local", "CPU", "Example 8-core CPU", "RandomX", 0, "H/s", 65, "", 4, 0.182, 0.15, "Unknown", "Unknown", "Replace with measured hashrate after a short test"],
  ["gpu-01", "operator", "local", "GPU", "Example RTX 3070", "KAWPOW", 0, "MH/s", 220, "", 4, 0.182, 0.15, "Unknown", "Unknown", "Use actual wall power when available"],
  ["asic-01", "operator", "local", "ASIC", "Example kHeavyHash ASIC", "kHeavyHash", 0, "TH/s", 3080, "", 0, 0.182, 0.15, "Unknown", "Unknown", "Only model already-owned ASIC hardware"],
]);
styleHeader(hardware, "A1:P1");
hardware.freezePanes.freezeRows(1);
hardware.tables.add("A1:P4", true, "HardwareIntake");
hardware.getRange("G2:G100").format.font = { color: "#0000FF" };
hardware.getRange("J2:M100").format.font = { color: "#0000FF" };
hardware.getRange("L2:L100").format.numberFormat = "$0.000";
hardware.getRange("M2:M100").format.numberFormat = "0.0%";
setWidths(hardware, [95, 95, 95, 90, 180, 120, 110, 90, 85, 120, 95, 95, 95, 120, 120, 310]);

const wallet = sheet("Wallet Matrix");
write(wallet, "A1:K1", [[
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
]]);
write(wallet, "A2:K6", [
  ["Monero", "XMR", "Monero", "RandomX", "CPU", "Official Monero GUI or CLI", "Needed", "", "Pool or P2Pool", "Check exchange support", "Receive address only; never store seed phrase here"],
  ["Ravencoin", "RVN", "Ravencoin", "KAWPOW", "GPU", "Official Ravencoin wallet", "Needed", "", "Public pool", "Check exchange support", "GPU lane only if cooling and wall power are acceptable"],
  ["Kaspa", "KAS", "Kaspa", "kHeavyHash", "ASIC", "Official Kaspa wallet", "Needed", "", "ASIC pool only", "Check exchange support", "Skip unless compatible ASIC and cheap power already exist"],
  ["Ethereum Classic", "ETC", "Ethereum Classic", "Etchash", "GPU", "Official or hardware wallet", "Optional", "", "Public pool", "Check exchange support", "Optional GPU comparison lane"],
  ["Bitcoin", "BTC", "Bitcoin", "SHA-256", "ASIC", "Hardware wallet", "Reference only", "", "Not recommended for home CPU/GPU", "Major exchanges", "Reference lane only"],
]);
styleHeader(wallet, "A1:K1");
wallet.freezePanes.freezeRows(1);
wallet.tables.add("A1:K6", true, "WalletMatrix");
wallet.getRange("H2:H100").format.font = { color: "#0000FF" };
setWidths(wallet, [120, 65, 130, 105, 100, 210, 130, 240, 190, 170, 320]);

const model = sheet("Profit Model");
write(model, "A1:S1", [[
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
  "gross_revenue_usd",
  "power_cost_usd",
  "pool_fee_usd",
  "net_usd",
  "decision",
  "refresh_required",
  "notes",
]]);
write(model, "A2:L4", [
  ["xmr-cpu-example", "Monero", "XMR", 0, "H/s", 0, 0, 0.01, 65, 0.15, 4, 0.182],
  ["rvn-gpu-example", "Ravencoin", "RVN", 0, "MH/s", 0, 0, 0.01, 220, 0.15, 4, 0.182],
  ["kas-asic-example", "Kaspa", "KAS", 0, "TH/s", 0, 0, 0.01, 3080, 0.15, 0, 0.182],
]);
formulas(model, "M2:Q4", [
  ["=F2*G2", "=((I2*(1+J2))/1000)*K2*L2", "=M2*H2", "=M2-N2-O2", '=IF(R2="Yes","Refresh first",IF(P2>0,"Candidate","Do not run"))'],
  ["=F3*G3", "=((I3*(1+J3))/1000)*K3*L3", "=M3*H3", "=M3-N3-O3", '=IF(R3="Yes","Refresh first",IF(P3>0,"Candidate","Do not run"))'],
  ["=F4*G4", "=((I4*(1+J4))/1000)*K4*L4", "=M4*H4", "=M4-N4-O4", '=IF(R4="Yes","Refresh first",IF(P4>0,"Candidate","Do not run"))'],
]);
write(model, "R2:S4", [
  ["Yes", "Enter current calculator output and measured wall power before deciding"],
  ["Yes", "Use current pool estimate and actual GPU tuning values"],
  ["Yes", "Do not buy ASIC from this template; model already-owned hardware"],
]);
styleHeader(model, "A1:S1");
model.freezePanes.freezeRows(1);
model.tables.add("A1:S4", true, "ProfitModel");
model.getRange("D2:L100").format.font = { color: "#0000FF" };
model.getRange("M2:Q100").format.font = { color: "#000000" };
model.getRange("G2:G100").format.numberFormat = "$#,##0.0000";
model.getRange("H2:J100").format.numberFormat = "0.0%";
model.getRange("L2:P100").format.numberFormat = "$#,##0.00;[Red]($#,##0.00);-";
setWidths(model, [150, 110, 65, 90, 95, 120, 110, 95, 95, 95, 95, 95, 115, 115, 100, 100, 110, 115, 320]);

const ledger = sheet("Receipt Ledger");
write(ledger, "A1:L1", [[
  "timestamp_utc",
  "event_type",
  "coin",
  "amount",
  "wallet_address",
  "pool_or_exchange",
  "txid_or_order_id",
  "gross_usd",
  "fee_usd",
  "net_usd",
  "source",
  "notes",
]]);
write(ledger, "A2:L3", [
  ["2026-05-29T00:00:00Z", "mining_payout", "XMR", "0.000000000000", "RECEIVE_ADDRESS_ONLY", "POOL_NAME", "TXID_OR_POOL_RECEIPT", 0, 0, 0, "pool dashboard", "Example only"],
  ["2026-05-29T00:00:00Z", "sell_off", "RVN", "0.00000000", "RECEIVE_ADDRESS_ONLY", "EXCHANGE_NAME", "ORDER_ID", 0, 0, 0, "exchange receipt", "Example only"],
]);
styleHeader(ledger, "A1:L1");
ledger.freezePanes.freezeRows(1);
ledger.tables.add("A1:L3", true, "ReceiptLedger");
ledger.getRange("H2:J100").format.numberFormat = "$#,##0.00;[Red]($#,##0.00);-";
setWidths(ledger, [160, 125, 60, 120, 220, 160, 180, 90, 85, 90, 145, 250]);

const faucets = sheet("Airdrop Faucet Tracker");
write(faucets, "A1:J1", [[
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
]]);
write(faucets, "A2:J4", [
  ["kaspa-testnet", "KAS testnet", "Faucet", "https://faucet.kaspanet.io/", "Unverified", "Yes", "No", "Use only testnet wallet; never enter seed phrase", "2026-05-29", "Verify live URL before use"],
  ["rvn-testnet", "RVN testnet", "Faucet", "https://raven.wiki/wiki/Testnet", "Research", "Yes", "No", "Use official docs and testnet only", "2026-05-29", "Confirm current faucet availability"],
  ["monero-stagenet", "XMR stagenet", "Practice wallet", "https://docs.getmonero.org/infrastructure/networks/", "Research", "Yes", "No", "Practice network only; no market value", "2026-05-29", "Confirm wallet network mode"],
]);
styleHeader(faucets, "A1:J1");
faucets.freezePanes.freezeRows(1);
faucets.tables.add("A1:J4", true, "FaucetTracker");
setWidths(faucets, [140, 140, 115, 260, 100, 120, 100, 260, 115, 240]);

const checks = sheet("Checks");
write(checks, "A1:F1", [["Check", "Actual", "Expected", "Difference", "Status", "Notes"]]);
write(checks, "A2:A7", [
  ["No private key fields"],
  ["Refresh flags"],
  ["Wallet rows"],
  ["Hardware rows"],
  ["Ledger rows"],
  ["Model status"],
]);
write(checks, "C2:C7", [["0"], [">=1"], [">=3"], [">=3"], [">=2"], ["0"]]);
write(checks, "F2:F7", [
  ["Workbook should use receive addresses only"],
  ["At least one model row should force refresh before decision"],
  ["Core coin lanes are present"],
  ["CPU, GPU, and ASIC examples are present"],
  ["Payout and sell-off examples are present"],
  ["All checks should be OK before use"],
]);
formulas(checks, "B2:B7", [
  ['=COUNTIF(\'Receipt Ledger\'!A:L,"*private*")+COUNTIF(\'Wallet Matrix\'!A:K,"*private*")'],
  ['=COUNTIF(\'Profit Model\'!R:R,"Yes")'],
  ["=COUNTA('Wallet Matrix'!A:A)-1"],
  ["=COUNTA('Hardware Intake'!A:A)-1"],
  ["=COUNTA('Receipt Ledger'!A:A)-1"],
  ['=COUNTIF(E2:E6,"Review")'],
]);
formulas(checks, "D2:D7", [["=B2-VALUE(C2)"], [""], [""], [""], [""], ["=B7-VALUE(C7)"]]);
formulas(checks, "E2:E7", [
  ['=IF(D2=0,"OK","Review")'],
  ['=IF(B3>=1,"OK","Review")'],
  ['=IF(B4>=3,"OK","Review")'],
  ['=IF(B5>=3,"OK","Review")'],
  ['=IF(B6>=2,"OK","Review")'],
  ['=IF(B7=0,"OK","Review")'],
]);
styleHeader(checks, "A1:F1");
checks.freezePanes.freezeRows(1);
setWidths(checks, [170, 110, 110, 110, 90, 330]);

const sources = sheet("Sources");
write(sources, "A1:G1", [["source_id", "title", "url", "source_type", "used_for", "as_of", "notes"]]);
write(sources, "A2:G12", [
  ["monero-randomx", "RandomX Moneropedia", "https://web.getmonero.org/resources/moneropedia/randomx.html", "Official docs", "Monero CPU-focused RandomX description", "2026-05-29", "RandomX is CPU-optimized and discourages specialized mining hardware"],
  ["monero-tail", "Monero Tail Emission", "https://www.getmonero.org/resources/moneropedia/tail-emission.html", "Official docs", "Monero tail emission and reward boundary", "2026-05-29", "Rewards stay fixed at 0.6 XMR or less per block after tail emission"],
  ["ravencoin-about", "Ravencoin About", "https://ravencoin.org/about/", "Official project site", "Ravencoin KAWPOW and GPU framing", "2026-05-29", "KAWPOW is derived from ProgPOW and ethhash"],
  ["ravencoin-pools", "Ravencoin Pools", "https://ravencoin.org/pools/", "Official project site", "Ravencoin pool workflow", "2026-05-29", "Create wallet address, then choose mining pool"],
  ["kaspa-home", "Kaspa Home", "https://kaspa.org/", "Official project site", "Kaspa kHeavyHash consensus algorithm", "2026-05-29", "Kaspa uses kHeavyHash for proof of work"],
  ["kaspa-emission", "Kaspa Emission Schedule", "https://kaspa.org/wp-content/uploads/2022/09/KASPA-EMISSION-SCHEDULE.pdf", "Official project PDF", "Kaspa emission schedule", "2026-05-29", "Use for emission reference, not live profitability"],
  ["eia-steo", "EIA Short-Term Energy Outlook Electricity", "https://www.eia.gov/outlooks/steo/report/elec_coal_renew.php", "Government forecast", "US residential electricity price context", "2026-05-29", "EIA reports 18.2 cents/kWh US residential average for 2026"],
  ["eia-electricity-data", "EIA Electricity Data", "https://www.eia.gov/electricity/data.php", "Government data portal", "State and sector electricity refresh path", "2026-05-29", "Use current monthly data before spending"],
  ["xmrig-pool", "XMRig Pool Configuration", "https://xmrig.com/docs/miner/config/pool", "Official miner docs", "XMRig pool config fields", "2026-05-29", "Verify releases and checksums separately"],
  ["xmrig-github", "XMRig GitHub", "https://github.com/xmrig/xmrig", "Open-source repository", "XMRig releases and source review", "2026-05-29", "Official source repository"],
  ["kawpowminer-github", "kawpowminer GitHub", "https://github.com/RavenCommunity/kawpowminer", "Open-source repository", "Ravencoin open-source miner option", "2026-05-29", "Verify maintenance status before use"],
]);
styleHeader(sources, "A1:G1");
sources.freezePanes.freezeRows(1);
sources.tables.add("A1:G12", true, "Sources");
setWidths(sources, [145, 210, 330, 150, 270, 105, 360]);

write(model, "U1:V1", [["Coin", "Net USD"]]);
formulas(model, "U2:V4", [["=B2", "=P2"], ["=B3", "=P3"], ["=B4", "=P4"]]);
const chart = model.charts.add("bar", model.getRange("U1:V4"));
chart.setPosition("A7", "H23");
chart.title = "Illustrative Net USD Before Refresh";
chart.hasLegend = true;
chart.xAxis = { axisType: "textAxis" };
chart.yAxis = { numberFormatCode: "$#,##0" };

const errorScan = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errorScan.ndjson);

await workbook.render({ sheetName: "Cover", autoCrop: "all", scale: 1, format: "png" });
await workbook.render({ sheetName: "Profit Model", autoCrop: "all", scale: 1, format: "png" });
await fs.mkdir(outputDir, { recursive: true });
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
console.log(outputPath);
