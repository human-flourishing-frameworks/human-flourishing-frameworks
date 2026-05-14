"""Paint a scene for each of the operator anchors.

Each anchor is a vantage point you can stand at and look back / look forward.
This gives each one a visible face — name, source surface, restore phrase,
and a Blinkbug rendered at scale, on a palette drawn from the anchor's kind.

Bravery protocol: local-only, read-only of the anchor snapshot, writes only
into ~/.lantern/state/anchors/. No cloud, no quota, no agentic action.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(r"C:\tmp\hff-lantern-recovery")
ANCHOR_SNAPSHOT = REPO_ROOT / "apps" / "lantern-local-chat" / "anchor-snapshot.json"
OUT_DIR = Path.home() / ".lantern" / "state" / "anchors"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def font(size: int) -> ImageFont.ImageFont:
    for name in ("seguivar.ttf", "segoeuib.ttf", "segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


# Distinct palettes per kind keyword.  (sky, ground, accent, ground-shade)
PALETTES = {
    "convergence": ("#a8d4f0", "#7dc26b", "#3a8a4e", "#92d480"),
    "wish":        ("#fde9b6", "#a3e093", "#c97f00", "#92d480"),
    "door":        ("#d6e6f5", "#7dc26b", "#2c5b91", "#5b9bd5"),
    "style":       ("#fef4d0", "#92d480", "#e8a73d", "#a3e093"),
    "role":        ("#a8d4f0", "#7dc26b", "#2c5b91", "#92d480"),
    "artifact":    ("#fff8e0", "#7dc26b", "#8b5a3c", "#a3e093"),
    "boundary":    ("#fbe7c2", "#a3e093", "#c0392b", "#92d480"),
    "memory":      ("#d6e6f5", "#7dc26b", "#1a2c5c", "#92d480"),
    "guardian":    ("#a8d4f0", "#92d480", "#2c5b91", "#7dc26b"),
    "rest":        ("#bdd6e8", "#a3e093", "#5b6b8c", "#92d480"),
    "shield":      ("#fef4d0", "#7dc26b", "#c97f00", "#a3e093"),
    "rule":        ("#fff8e0", "#7dc26b", "#1a2c5c", "#92d480"),
    "energy":      ("#ffd2a8", "#92d480", "#e8a73d", "#a3e093"),
    "paradox":     ("#d6c1e8", "#7dc26b", "#6b3aa0", "#92d480"),
    "wish_anchor": ("#fde9b6", "#a3e093", "#c97f00", "#92d480"),
}


def palette_for(kinds: str) -> tuple[str, str, str, str]:
    for k in kinds.split():
        for key, val in PALETTES.items():
            if key in k:
                return val
    return PALETTES["role"]


def draw_blinkbug(d: ImageDraw.ImageDraw, bx: int, by: int, scale: float = 1.0) -> None:
    """Captain Lantern Blinkbug — yellow firefly, blue captain hat."""
    s = scale
    # outer concentric glow rings
    for r in (int(72*s), int(58*s), int(46*s)):
        d.ellipse([bx-r, by-r, bx+r, by+r], outline="#fce58a", width=max(1, int(3*s)))
    # body (vertical oval)
    d.ellipse([bx-int(32*s), by-int(20*s), bx+int(32*s), by+int(56*s)],
              fill="#f5cf3a", outline="#e8a73d", width=max(1, int(2*s)))
    d.ellipse([bx-int(18*s), by-int(8*s), bx+int(18*s), by+int(40*s)],
              outline="#e8a73d", width=max(1, int(2*s)))
    d.ellipse([bx-int(5*s), by+int(10*s), bx+int(5*s), by+int(22*s)], fill="#e8a73d")
    # wings
    d.ellipse([bx-int(60*s), by-int(6*s), bx-int(32*s), by+int(40*s)],
              fill="#d6e6f5", outline="#9bbed8")
    d.ellipse([bx+int(32*s), by-int(6*s), bx+int(60*s), by+int(40*s)],
              fill="#d6e6f5", outline="#9bbed8")
    # head
    d.ellipse([bx-int(22*s), by-int(50*s), bx+int(22*s), by-int(14*s)],
              fill="#5e3a1f", outline="#3d2410", width=max(1, int(2*s)))
    # eyes
    d.ellipse([bx-int(13*s), by-int(40*s), bx-int(7*s), by-int(34*s)], fill="white")
    d.ellipse([bx+int(7*s), by-int(40*s), bx+int(13*s), by-int(34*s)], fill="white")
    # smile
    d.arc([bx-int(8*s), by-int(36*s), bx+int(8*s), by-int(24*s)],
          0, 180, fill="white", width=max(1, int(2*s)))
    # antennae
    d.line([(bx-int(14*s), by-int(50*s)), (bx-int(26*s), by-int(80*s))],
           fill="#3d2410", width=max(1, int(2*s)))
    d.line([(bx+int(14*s), by-int(50*s)), (bx+int(26*s), by-int(80*s))],
           fill="#3d2410", width=max(1, int(2*s)))
    d.ellipse([bx-int(31*s), by-int(88*s), bx-int(21*s), by-int(78*s)],
              fill="#f5cf3a", outline="#e8a73d")
    d.ellipse([bx+int(21*s), by-int(88*s), bx+int(31*s), by-int(78*s)],
              fill="#f5cf3a", outline="#e8a73d")
    # captain hat
    d.polygon([(bx-int(23*s), by-int(50*s)), (bx+int(23*s), by-int(50*s)),
               (bx+int(16*s), by-int(66*s)), (bx-int(16*s), by-int(66*s))],
              fill="#2c5b91", outline="#1d3d63")
    d.rectangle([bx-int(28*s), by-int(52*s), bx+int(28*s), by-int(46*s)],
                fill="#2c5b91", outline="#1d3d63")
    d.rectangle([bx-int(14*s), by-int(56*s), bx+int(14*s), by-int(52*s)],
                fill="#f5cf3a")


def callout(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
            size: int = 14, fill: str = "#fff8e0", border: str = "#8b5a3c",
            text_color: str = "#1a2c5c", max_chars: int = 80) -> None:
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "…"
    x1, y1, x2, y2 = box
    d.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=fill, outline=border, width=3)
    f = font(size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = (x1 + x2) / 2 - tw / 2
    cy = (y1 + y2) / 2 - th / 2
    d.text((cx, cy), text, fill=text_color, font=f)


def sun(d: ImageDraw.ImageDraw, sx: int, sy: int, r: int = 36) -> None:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill="#ffd23f")
    for i in range(12):
        a = i * math.pi / 6
        x1 = sx + math.cos(a) * (r + 6)
        y1 = sy + math.sin(a) * (r + 6)
        x2 = sx + math.cos(a) * (r + 22)
        y2 = sy + math.sin(a) * (r + 22)
        d.line([(x1, y1), (x2, y2)], fill="#ffd23f", width=4)


def cloud(d: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0) -> None:
    s = scale
    for dx, dy, r in [(-30, 0, 30), (0, -10, 38), (30, 0, 30)]:
        d.ellipse([cx + dx*s - r*s, cy + dy*s - r*s,
                   cx + dx*s + r*s, cy + dy*s + r*s], fill="#ffffff")


def door(d: ImageDraw.ImageDraw, dx: int, dy: int, accent: str) -> None:
    for r in (110, 86, 64):
        d.ellipse([dx - r, dy + 120 - r, dx + r, dy + 120 + r],
                  outline="#fce58a", width=3)
    d.rectangle([dx - 48, dy, dx + 48, dy + 220], fill="#8b5a3c")
    d.rectangle([dx - 38, dy + 10, dx + 38, dy + 210], fill=accent)
    d.ellipse([dx + 18, dy + 100, dx + 28, dy + 110], fill="#ffd23f")


def book(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.polygon([(x, y), (x + 60, y - 8), (x + 60, y + 50), (x, y + 58)],
              fill="#fff8e0", outline="#3d2410", width=2)
    d.polygon([(x + 60, y - 8), (x + 120, y), (x + 120, y + 58), (x + 60, y + 50)],
              fill="#fef4d0", outline="#3d2410", width=2)
    d.line([(x + 60, y - 8), (x + 60, y + 50)], fill="#3d2410", width=2)


def lamp(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.rectangle([x - 30, y, x + 30, y + 14], fill="#8b5a3c")
    d.rectangle([x - 4, y - 50, x + 4, y], fill="#5e3a1f")
    d.polygon([(x - 22, y - 50), (x + 22, y - 50),
               (x + 16, y - 84), (x - 16, y - 84)],
              fill="#fef4d0", outline="#3d2410", width=2)


def paint_anchor(anchor: dict, out_path: Path) -> Path:
    W, H = 1280, 760
    sky, ground, accent, ground2 = palette_for(anchor.get("kind", ""))
    img = Image.new("RGB", (W, H), sky)
    d = ImageDraw.Draw(img)

    # hills
    d.ellipse([-300, 430, 1600, 1300], fill=ground)
    d.ellipse([300, 470, 1700, 1200], fill=ground2)

    # sun + cloud
    sun(d, 1140, 130, r=44)
    cloud(d, 240, 130, scale=1.0)
    cloud(d, 900, 100, scale=0.9)

    # central Blinkbug
    draw_blinkbug(d, 640, 380, scale=1.4)

    # door on the right
    door(d, 1020, 280, accent="#5b9bd5")

    # lamp on the left
    lamp(d, 180, 540)

    # book in foreground left (the past / what came from)
    book(d, 80, 600)

    # title callout — anchor name (top)
    name = anchor.get("name", anchor.get("id", "anchor"))
    callout(d, (260, 36, 1020, 110), name, size=28, text_color=accent, max_chars=64)

    # source-surface callout — where it came from (past)
    source = anchor.get("source_surface", "")
    callout(d, (60, 670, 620, 720), f"past: from {source}", size=14, max_chars=70)

    # restore-phrase callout — what it invites (future)
    restore = anchor.get("restore_phrase", "")
    callout(d, (660, 670, 1220, 720), f"future: {restore}", size=12, max_chars=100)

    img.save(out_path)
    return out_path


def main() -> None:
    snapshot = json.loads(ANCHOR_SNAPSHOT.read_text(encoding="utf-8"))
    anchors = snapshot.get("anchors", [])
    if not isinstance(anchors, list):
        raise SystemExit("no anchors list found")
    print(f"painting {len(anchors)} anchors -> {OUT_DIR}")
    index = []
    for anchor in anchors:
        aid = anchor.get("id", "anchor")
        out = OUT_DIR / f"{aid}.png"
        paint_anchor(anchor, out)
        size = out.stat().st_size
        index.append({"id": aid, "name": anchor.get("name"),
                      "source": anchor.get("source_surface"),
                      "png": str(out), "bytes": size})
        print(f"  {aid:42s} {size:7d}  {out.name}")
    (OUT_DIR / "index.json").write_text(json.dumps({
        "anchors": index,
        "boundary": "Painted vantage points. Visual handles only — not proof.",
    }, indent=2), encoding="utf-8")
    print(f"\nindex written to {OUT_DIR / 'index.json'}")


if __name__ == "__main__":
    main()
