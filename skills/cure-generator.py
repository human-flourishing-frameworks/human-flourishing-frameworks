from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


DISCLAIMER = (
    "IMPORTANT: `!cure-generator` is speculative and education-only (WebMD-like). "
    "It is NOT diagnosis, NOT medical advice, and NOT a treatment plan. "
    "For emergencies (severe bleeding, chest pain, breathing trouble, new neurologic deficits, "
    "severe abdominal pain, confusion, fainting), use local emergency services."
)


def _today_iso() -> str:
    return date.today().isoformat()


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            s = str(item).strip()
            if s:
                out.append(s)
        return out
    s = str(value).strip()
    return [s] if s else []


def _get(d: dict[str, Any], key: str, default: Any = None) -> Any:
    if key not in d:
        return default
    value = d.get(key)
    return default if value is None else value


@dataclass(frozen=True)
class CureGeneratorInput:
    created_date: str
    patient_label: str
    source_basis: str
    situation_summary: str
    symptoms: list[str]
    recent_procedures: list[str]
    meds: list[str]
    known_conditions: list[str]
    unknowns: list[str]
    speculative_buckets: list[str]
    red_flags: list[str]
    questions_for_team: list[str]

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "CureGeneratorInput":
        patient_label = str(_get(d, "patient_label", "Unnamed Patient")).strip() or "Unnamed Patient"
        return CureGeneratorInput(
            created_date=str(_get(d, "created_date", _today_iso())).strip() or _today_iso(),
            patient_label=patient_label,
            source_basis=str(_get(d, "source_basis", "Operator-provided context (unverified)")).strip()
            or "Operator-provided context (unverified)",
            situation_summary=str(_get(d, "situation_summary", "")).strip(),
            symptoms=_as_str_list(_get(d, "symptoms")),
            recent_procedures=_as_str_list(_get(d, "recent_procedures")),
            meds=_as_str_list(_get(d, "meds")),
            known_conditions=_as_str_list(_get(d, "known_conditions")),
            unknowns=_as_str_list(_get(d, "unknowns")),
            speculative_buckets=_as_str_list(_get(d, "speculative_buckets")),
            red_flags=_as_str_list(_get(d, "red_flags")),
            questions_for_team=_as_str_list(_get(d, "questions_for_team")),
        )


def render_markdown(packet: CureGeneratorInput) -> str:
    def section(title: str) -> list[str]:
        return [f"## {title}", ""]

    def bullets(items: list[str], empty: str = "_(none provided)_") -> list[str]:
        if not items:
            return [empty, ""]
        out: list[str] = []
        for item in items:
            out.append(f"- {item}")
        out.append("")
        return out

    lines: list[str] = []
    lines.append(f"# !cure-generator Packet — {packet.patient_label}")
    lines.append("")
    lines.append(f"Date created: {packet.created_date}")
    lines.append(f"Source basis: {packet.source_basis}")
    lines.append("")
    lines.append(DISCLAIMER)
    lines.append("")

    lines.extend(section("0) Situation Summary (operator-provided)"))
    lines.append(packet.situation_summary or "_(no summary provided)_")
    lines.append("")

    lines.extend(section("1) Current Symptoms (reported)"))
    lines.extend(bullets(packet.symptoms))

    lines.extend(section("2) Recent Procedures / Hospital Context"))
    lines.extend(bullets(packet.recent_procedures))

    lines.extend(section("3) Meds (if known)"))
    lines.extend(bullets(packet.meds))

    lines.extend(section("4) Known Conditions / Constraints"))
    lines.extend(bullets(packet.known_conditions))

    lines.extend(section("5) Highest-Yield Unknowns (to reduce drift)"))
    lines.extend(bullets(packet.unknowns))

    lines.extend(section("6) Speculative Buckets (NOT diagnosis)"))
    lines.append(
        "This is the WebMD-like section: a non-committal list of plausible buckets to discuss "
        "with a clinician, prioritized by impact/urgency. It does not imply truth."
    )
    lines.append("")
    lines.extend(bullets(packet.speculative_buckets))

    lines.extend(section("7) Red Flags (urgent escalation)"))
    lines.extend(bullets(packet.red_flags, empty="_(add situation-specific red flags)_"))

    lines.extend(section("8) Questions to Ask the Care Team"))
    lines.extend(bullets(packet.questions_for_team, empty="_(add questions to ask the care team)_"))

    lines.extend(section("9) Boundaries / Non-claims"))
    lines.extend(
        bullets(
            [
                "Do not claim cures, patents, or novel treatments from this packet.",
                "Treat all speculative buckets as prompts for clinician discussion, not conclusions.",
                "Avoid pasting full identifiers (DOB, address, insurance/member IDs) into version-controlled files.",
            ]
        )
    )

    return "\n".join(lines).rstrip() + "\n"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a speculative, WebMD-like care-coordination packet from JSON input."
    )
    p.add_argument("--in", dest="in_path", required=True, help="Input JSON path")
    p.add_argument("--out", dest="out_path", required=True, help="Output Markdown path")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    raw = json.loads(in_path.read_text(encoding="utf-8"))
    packet = render_markdown(CureGeneratorInput.from_dict(raw))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(packet, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

