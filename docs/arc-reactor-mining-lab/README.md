# Arc Reactor Mining Lab

Safe multi-coin mining package for operator-owned hardware.

This package is a planning, intake, accounting, and validation kit. It does not
mine by itself, does not store private keys, does not move funds, and does not
reuse Lantern OS wallet ledger balances as crypto balances. The Lantern wallet
ledger is treated as a cash and invoice record only.

## Operator Rules

- Mine only on hardware you own or are explicitly allowed to use.
- Never paste seed phrases, private keys, exchange credentials, or Apple ID
  credentials into miners, scripts, pools, spreadsheets, or reports.
- Use wallet receive addresses only. A miner needs a payout address, not a
  private key.
- Download miners only from official project pages or well-known open-source
  repositories, then verify releases before use.
- Start with short, observed tests and stop immediately for overheating,
  breaker trips, abnormal fan noise, unexpected remote access prompts, or
  unstable power draw.
- Treat profitability as volatile. Recalculate from current network difficulty,
  price, pool fee, stale share rate, actual wall power, and local electricity
  rate before spending money.
- Record every payout and sell-off in the receipt ledger. The ledger is proof
  of process, not proof of market value.

## Package Contents

| Path | Purpose |
|---|---|
| `data/arc-reactor-mining-lab/hardware-intake.csv` | Hardware, power, rate, and readiness intake form. |
| `data/arc-reactor-mining-lab/wallet-matrix.csv` | Coin-by-coin wallet, mining method, and off-ramp status. |
| `data/arc-reactor-mining-lab/profitability-model.csv` | Formula-ready profitability assumptions and model columns. |
| `data/arc-reactor-mining-lab/airdrop-faucet-tracker.csv` | Safe tracker for practice faucets and token claims. |
| `data/arc-reactor-mining-lab/receipt-ledger-template.jsonl` | Append-only mined coin and sell-off ledger example. |
| `data/arc-reactor-mining-lab/sources.csv` | Source register for algorithms, electricity data, and miner docs. |
| `data/arc-reactor-mining-lab/arc_reactor_mining_lab_workbook.xlsx` | Editable workbook with intake, wallet matrix, model, checks, and sources. |
| `configs/arc-reactor-mining-lab/xmrig-config.sample.json` | XMRig placeholder config for Monero-style CPU mining tests. |
| `configs/arc-reactor-mining-lab/kawpowminer.sample.args.txt` | Ravencoin KawPoW placeholder argument file. |
| `configs/arc-reactor-mining-lab/kaspa-asic-intake.sample.csv` | ASIC intake fields for Kaspa or other kHeavyHash machines. |
| `ARC-REACTOR-MINING-LAB-SAFE-MULTI-COIN-PLAN.pdf` | Print-ready package summary and operator checklist. |

## Coin Lanes

| Coin | Algorithm | Best hardware lane | Default decision |
|---|---|---|---|
| Monero (XMR) | RandomX | CPU | Good learning lane; profit depends heavily on power cost and CPU efficiency. |
| Ravencoin (RVN) | KAWPOW | GPU | Valid GPU exercise if the operator already owns suitable GPUs and cooling. |
| Kaspa (KAS) | kHeavyHash | ASIC | Skip unless an operator already owns a compatible ASIC and has cheap power. |

## Inventory Commands

Use these only for local inventory. They do not start miners.

Windows PowerShell:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
```

Linux:

```bash
lscpu
cat /proc/cpuinfo
nvidia-smi
```

## Electricity Formula

Daily electricity cost:

```text
((device_watts + overhead_watts) / 1000) * hours_per_day * kwh_rate_usd
```

Include cooling, fans, network gear, and power supply inefficiency. A simple
starter overhead is 10% to 20% until measured wall power is available.

## Mining Workflow

1. Fill the hardware intake sheet with real CPU/GPU/ASIC names, wattage, and
   local electricity rate.
2. Create receive-only wallet addresses for each coin. Mark every wallet row as
   `Address only`, not private-key-backed.
3. Run a profitability calculator with current network conditions. Save the
   date, URL, and result in the model notes.
4. Run a short miner test only after confirming thermals, pool endpoint, payout
   address, and stop condition.
5. Log accepted hashrate, rejected shares, wall power, temperature, and pool
   payout receipts.
6. Stop or tune any rig that is net-negative unless the explicit goal is a
   bounded education test.
7. If selling a small amount, follow the sell-off checklist and preserve the
   exchange receipt, blockchain transaction ID, and ledger row.

## Truth Boundary

This package is not investment advice, a wallet, custody software, a miner
installer, or a remote-control system. It is a documented lab protocol for
operator-owned hardware and receive-only wallets. All returns are estimates
until verified against pool history, on-chain transactions, exchange receipts,
and actual utility bills.

