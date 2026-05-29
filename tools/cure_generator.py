from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from typing import Any


DISCLAIMER = (
    "IMPORTANT: This is a speculative, education-only care-coordination packet "
    "(WebMD-like). It is NOT diagnosis, NOT medical advice, and NOT a treatment plan. "
    "For emergencies (severe bleeding, chest pain, breathing trouble, new neurologic "
    "deficits, severe abdominal pain, confusion, fainting), use local emergency services."
)


def _today_iso() -> str:
    return date.today().isoformat()


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value).strip()] if str(value).strip() else []


def _get(obj: dict[str, Any], key: str, default: Any = None) -> Any:
    if key not in obj:
        return default
    value = obj.get(key)
    return default if value is None else value


@dataclass(frozen=True)
class CureInput:
    created_date: str
    patient_label: str
    source_basis: str
    situation_summary: str
    symptoms: list[str]
    recent_procedures: list[str]
    meds: list[str]
    known_conditions: list[str]
    unknowns: list[str]
    red_flags: list[str]
    questions_for_team: list[str]
    speculative_buckets: list[str]

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "CureInput":
        created_date = str(_get(d, "created_date", _today_iso()))
        patient_label = str(_get(d, "patient_label", "Unnamed Patient")).strip() or "Unnamed Patient"
        source_basis = str(_get(d, "source_basis", "Operator-provided context (unverified)")).strip()
        situation_summary = str(_get(d, "situation_summary", "")).strip()

        symptoms = _as_str_list(_get(d, "symptoms"))
        recent_procedures = _as_str_list(_get(d, "recent_procedures"))
        meds = _as_str_list(_get(d, "meds"))
        known_conditions = _as_str_list(_get(d, "known_conditions"))
        unknowns = _as_str_list(_get(d, "unknowns"))

        red_flags = _as_str_list(_get(d, "red_flags"))
        questions_for_team = _as_str_list(_get(d, "questions_for_team"))
        speculative_buckets = _as_str_list(_get(d, "speculative_buckets"))

        return CureInput(
            created_date=created_date,
            patient_label=patient_label,
            source_basis=source_basis,
            situation_summary=situation_summary,
            symptoms=symptoms,
            recent_procedures=recent_procedures,
            meds=meds,
            known_conditions=known_conditions,
            unknowns=unknowns,
            red_flags=red_flags,
            questions_for_team=questions_for_team,
            speculative_buckets=speculative_buckets,
        )


def render_packet(data: CureInput) -> str:
    lines: list[str] = []
    lines.append(f"# !cure-generator Packet — {data.patient_label}")
    lines.append("")
    lines.append(f"Date created: {data.created_date}")
    lines.append(f"Source basis: {data.source_basis}")
    lines.append("")
    lines.append(DISCLAIMER)
    lines.append("")

    def section(title: str) -> None:
        lines.append(f"## {title}")
        lines.append("")

    def bullets(items: list[str], empty: str = "_(none provided)_") -> None:
        if not items:
            lines.append(empty)
            lines.append("")
            return
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    section("0) Situation Summary (operator-provided)")
    lines.append(data.situation_summary or "_(no summary provided)_")
    lines.append("")

    section("1) Current Symptoms (reported)")
    bullets(data.symptoms)

    section("2) Recent Procedures / Hospital Context")
    bullets(data.recent_procedures)

    section("3) Meds (if known)")
    bullets(data.meds)

    section("4) Known Conditions / Constraints")
    bullets(data.known_conditions)

    section("5) Highest-Yield Unknowns (to reduce drift)")
    bullets(data.unknowns)

    section("6) Speculative Buckets (NOT diagnosis)")
    lines.append(
        "This is the WebMD-like section: a *non-committal* list of plausible buckets "
        "to discuss with a clinician, prioritized by impact/urgency. It does not imply truth."
    )
    lines.append("")
    bullets(data.speculative_buckets)

    section("7) Red Flags (urgent escalation)")
    bullets(data.red_flags, empty="_(add red flags for this situation)_")

    section("8) Questions to Ask the Care Team")
    bullets(data.questions_for_team, empty="_(add questions to ask the care team)_")

    section("9) Notes / Boundaries")
    bullets(
        [
            "Do not claim cures, patents, or novel treatments from this packet.",
            "If new labs/imaging/diagnoses arrive, regenerate and replace this packet.",
            "Keep identifiers minimal; avoid pasting full DOB/SSN/address/insurance IDs into version-controlled files.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a speculative care-coordination packet from JSON input.")
    p.add_argument("--in", dest="in_path", required=True, help="Input JSON path")
    p.add_argument("--out", dest="out_path", required=True, help="Output Markdown path")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    with open(args.in_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    packet = render_packet(CureInput.from_dict(raw))
    with open(args.out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

