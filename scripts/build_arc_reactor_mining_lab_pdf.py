from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "arc-reactor-mining-lab"
OUTPUT = ROOT / "ARC-REACTOR-MINING-LAB-SAFE-MULTI-COIN-PLAN.pdf"


class Rule(Flowable):
    def __init__(self, color: colors.Color = colors.HexColor("#0F766E"), height: int = 2):
        super().__init__()
        self.color = color
        self.height = height

    def wrap(self, width: float, height: float) -> tuple[float, float]:
        self.width = width
        return width, self.height + 8

    def draw(self) -> None:
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.height)
        self.canv.line(0, self.height, self.width, self.height)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, style), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
    )


def table(data: list[list[str]], col_widths: list[float] | None = None) -> Table:
    tbl = Table(data, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12343B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tbl


def source_table(styles: dict[str, ParagraphStyle]) -> Table:
    rows = read_csv("sources.csv")
    data = [["Source", "Used for", "URL"]]
    for row in rows:
        data.append(
            [
                row["title"],
                row["used_for"],
                f'<a href="{row["url"]}">{row["url"]}</a>',
            ]
        )
    return table(
        [[p(cell, styles["TableCell"]) for cell in row] for row in data],
        [1.55 * inch, 2.25 * inch, 2.65 * inch],
    )


def draw_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(doc.leftMargin, 0.45 * inch, "Arc Reactor Mining Lab - operator-owned hardware only")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build() -> None:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=29,
            textColor=colors.HexColor("#12343B"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["BodyText"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#334155"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#0F766E"),
            spaceBefore=14,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallBody",
            parent=styles["BodyText"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["BodyText"],
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor("#0F172A"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Callout",
            parent=styles["BodyText"],
            fontSize=10,
            leading=13,
            leftIndent=10,
            rightIndent=10,
            borderColor=colors.HexColor("#0F766E"),
            borderWidth=0.8,
            borderPadding=8,
            backColor=colors.HexColor("#ECFDF5"),
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=8,
            spaceAfter=10,
        )
    )

    story: list[Flowable] = []
    story.append(Spacer(1, 0.35 * inch))
    story.append(p("Arc Reactor Mining Lab", styles["TitleCenter"]))
    story.append(
        p(
            "Safe multi-coin mining plan for operator-owned hardware, receive-only wallets, "
            "and auditable expense tracking.",
            styles["Subtitle"],
        )
    )
    story.append(Rule())
    story.append(
        p(
            "<b>No private keys. No brute force. No hidden mining. No Lantern cash-ledger reuse as crypto balance.</b> "
            "This package documents how to test CPU, GPU, and ASIC mining lanes without giving any tool custody over funds.",
            styles["Callout"],
        )
    )
    story.append(
        table(
            [
                ["Deliverable", "File"],
                ["Operator guide", "docs/arc-reactor-mining-lab/README.md"],
                ["Workbook", "data/arc-reactor-mining-lab/arc_reactor_mining_lab_workbook.xlsx"],
                ["Templates", "data/arc-reactor-mining-lab/*.csv and receipt-ledger-template.jsonl"],
                ["Sample configs", "configs/arc-reactor-mining-lab/"],
                ["Validation", "scripts/validate_arc_reactor_mining_lab.py"],
            ],
            [2.0 * inch, 4.2 * inch],
        )
    )

    story.append(p("Executive Decision", styles["Section"]))
    story.append(
        bullets(
            [
                "Use Monero as the CPU learning lane, because RandomX is CPU-optimized and discourages specialized hardware.",
                "Use Ravencoin as the GPU learning lane only if the operator already owns GPUs and can manage heat.",
                "Treat Kaspa as ASIC-only for this lab. Do not buy an ASIC from static estimates; model already-owned hardware first.",
                "Use current calculators and actual wall power for every run. This document deliberately avoids fixed profit promises.",
            ],
            styles["SmallBody"],
        )
    )

    story.append(PageBreak())
    story.append(p("Safety Model", styles["Section"]))
    story.append(
        p(
            "The lab separates wallet accounting from mining execution. Miners are configured with receive addresses only. "
            "The local Lantern-style ledger records receipts and off-ramp events after they happen; it is not a crypto wallet, "
            "custodian, balance oracle, or private-key store.",
            styles["SmallBody"],
        )
    )
    story.append(
        table(
            [
                ["Boundary", "Allowed", "Not allowed"],
                ["Wallets", "Receive addresses and public transaction IDs", "Seed phrases, private keys, exchange passwords"],
                ["Hardware", "Owned CPU/GPU/ASIC devices with measured wall power", "Unapproved computers, cloud abuse, covert usage"],
                ["Software", "Official/open-source miners and documented pool configs", "Malware, key extraction, brute forcing"],
                ["Accounting", "Append-only receipt rows and exchange receipts", "Invented balances or unverified cash claims"],
            ],
            [1.2 * inch, 2.5 * inch, 2.7 * inch],
        )
    )

    story.append(p("Hardware Intake", styles["Section"]))
    story.append(
        p(
            "Inventory begins with CPU/GPU/ASIC identity, hashrate, power draw, wall measurement, operating hours, electricity "
            "rate, and cooling readiness. The workbook includes formulas for power cost so the operator can adjust assumptions "
            "without editing code.",
            styles["SmallBody"],
        )
    )
    hardware_rows = read_csv("hardware-intake.csv")
    hardware_data = [["Device", "Type", "Lane", "Watts", "Hours", "kWh rate", "Notes"]]
    for row in hardware_rows:
        hardware_data.append(
            [
                row["device_id"],
                row["device_type"],
                row["algorithm_lane"],
                row["tdp_watts"],
                row["hours_per_day"],
                row["kwh_rate_usd"],
                row["notes"],
            ]
        )
    story.append(table(hardware_data, [0.7 * inch, 0.6 * inch, 1.0 * inch, 0.6 * inch, 0.6 * inch, 0.7 * inch, 2.6 * inch]))

    story.append(PageBreak())
    story.append(p("Coin Lanes", styles["Section"]))
    wallet_rows = read_csv("wallet-matrix.csv")
    lane_data = [["Coin", "Algorithm", "Hardware", "Pool or Mode", "Default posture"]]
    posture = {
        "XMR": "Good learning lane; profit depends on power.",
        "RVN": "GPU test lane; heat and tuning matter.",
        "KAS": "ASIC-only; skip without owned compatible machine.",
        "ETC": "Optional GPU comparison lane.",
        "BTC": "Reference only for home labs.",
    }
    for row in wallet_rows:
        lane_data.append(
            [
                row["coin"],
                row["algorithm"],
                row["hardware_lane"],
                row["pool_or_mode"],
                posture.get(row["ticker"], row["notes"]),
            ]
        )
    story.append(table(lane_data, [1.1 * inch, 1.0 * inch, 0.9 * inch, 1.6 * inch, 2.0 * inch]))

    story.append(p("Profitability Logic", styles["Section"]))
    story.append(
        p(
            "Gross revenue equals current expected coin per day multiplied by current coin price. Power cost equals adjusted "
            "watts divided by 1000, multiplied by hours per day and local kWh rate. Net estimate subtracts power cost and pool fee. "
            "All live hashrate, reward, and price fields must be refreshed before each decision.",
            styles["SmallBody"],
        )
    )
    story.append(
        table(
            [
                ["Metric", "Formula"],
                ["Gross revenue", "gross_coin_per_day * coin_price_usd"],
                ["Power cost", "((device_watts * (1 + overhead_pct)) / 1000) * hours_per_day * kwh_rate_usd"],
                ["Pool fee", "gross_revenue_usd * pool_fee_pct"],
                ["Net estimate", "gross_revenue_usd - power_cost_usd - pool_fee_usd"],
            ],
            [1.5 * inch, 4.8 * inch],
        )
    )

    story.append(PageBreak())
    story.append(p("Operating Workflow", styles["Section"]))
    story.append(
        bullets(
            [
                "Fill hardware intake from local inventory commands and actual utility rate.",
                "Create receive-only wallet addresses and update the wallet matrix.",
                "Refresh calculator outputs, price, difficulty, pool fee, and measured power.",
                "Run a short observed test with a known stop condition.",
                "Record accepted/rejected shares, temperature, wall power, payout, and transaction IDs.",
                "Append sell-off rows only after actual conversion receipts exist.",
            ],
            styles["SmallBody"],
        )
    )
    story.append(p("Sell-Off Controls", styles["Section"]))
    story.append(
        p(
            "The sell-off path is deliberately small and auditable: confirm ownership, verify exchange support for the exact network, "
            "send a test transfer when practical, record transaction IDs, wait for confirmations, and update project cash only after "
            "settlement.",
            styles["SmallBody"],
        )
    )
    story.append(
        table(
            [
                ["Step", "Evidence to keep"],
                ["Pre-transfer", "Wallet balance, source address, exchange deposit network"],
                ["Broadcast", "Transaction ID, timestamp, amount, fee"],
                ["Exchange", "Deposit confirmation, order ID, gross proceeds, fees"],
                ["Ledger", "Append-only receipt row and correction row if needed"],
            ],
            [1.4 * inch, 4.9 * inch],
        )
    )

    story.append(PageBreak())
    story.append(p("Source Register", styles["Section"]))
    story.append(
        p(
            "Sources were refreshed on 2026-05-29 for algorithm and electricity context. Live profitability must still be recalculated "
            "at run time because price, difficulty, pool luck, fees, and wall power move continuously.",
            styles["SmallBody"],
        )
    )
    story.append(source_table(styles))

    story.append(PageBreak())
    story.append(p("Final Operator Checklist", styles["Section"]))
    story.append(
        bullets(
            [
                "Every wallet row has receive-address status, not private-key material.",
                "Every device has owner, location, breaker/circuit, cooling status, and measured or conservative wattage.",
                "Every mining run has a stop condition for heat, power, or negative expected value.",
                "Every payout has a pool receipt or transaction ID.",
                "Every conversion has exchange receipt evidence before any USD ledger update.",
                "Every profitability claim is timestamped and source-linked.",
            ],
            styles["SmallBody"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch,
        title="Arc Reactor Mining Lab Safe Multi-Coin Plan",
        author="Codex",
    )
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()

