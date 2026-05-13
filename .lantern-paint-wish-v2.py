"""Wish painting v2 — higher standards.

Adds gradient sky, paper-texture overlay, drop shadows, soft glow halos.
Same scene, raised craft. Saves over the path the desktop hero loads from.
"""
from __future__ import annotations

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 760
OUT_LOCAL = Path(r"C:\tmp\hff-lantern-recovery\.lantern-wish-painting.png")
OUT_STATE = Path.home() / ".lantern" / "state" / "wish-scene.png"


def font(size: int) -> ImageFont.ImageFont:
    for name in ("Quicksand-Bold.ttf", "Nunito-Bold.ttf", "seguivar.ttf",
                 "segoeuib.ttf", "segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def grad_v(img: Image.Image, top: tuple[int, int, int], bot: tuple[int, int, int]) -> None:
    """Vertical gradient from top to bot, painted onto img in place."""
    d = ImageDraw.Draw(img)
    h = img.height
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        d.line([(0, y), (img.width, y)], fill=(r, g, b))


def paper_texture(size: tuple[int, int], density: int = 8000) -> Image.Image:
    """Subtle warm noise overlay — fakes paper grain."""
    tex = Image.new("RGBA", size, (0, 0, 0, 0))
    px = tex.load()
    rng = random.Random(7)
    for _ in range(density):
        x = rng.randint(0, size[0] - 1)
        y = rng.randint(0, size[1] - 1)
        a = rng.randint(0, 16)
        # warm grain — slight brown tint
        px[x, y] = (90, 60, 30, a)
    # Soft fiber strokes
    d = ImageDraw.Draw(tex)
    for _ in range(120):
        x1 = rng.randint(0, size[0])
        y1 = rng.randint(0, size[1])
        x2 = x1 + rng.randint(-30, 30)
        y2 = y1 + rng.randint(-6, 6)
        d.line([(x1, y1), (x2, y2)], fill=(70, 50, 25, 8), width=1)
    return tex


def shadow_blob(target: Image.Image, draw_fn, offset: tuple[int, int] = (5, 6),
                blur: int = 5, opacity: int = 65) -> None:
    """Run draw_fn on a transparent overlay, blur, paste offset onto target."""
    shadow = Image.new("RGBA", target.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_fn(sd, (0, 0, 0, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
    # paste with offset
    target.alpha_composite(shadow, offset)


def soft_glow(target: Image.Image, cx: int, cy: int, r: int,
              color: tuple[int, int, int] = (252, 229, 138), passes: int = 4) -> None:
    """Halo around a point using stacked blurred discs."""
    halo = Image.new("RGBA", target.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for i in range(passes, 0, -1):
        a = int(28 * (i / passes))
        rr = int(r * (1 + (passes - i) * 0.4))
        hd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
    halo = halo.filter(ImageFilter.GaussianBlur(radius=6))
    target.alpha_composite(halo)


def draw_sun(target: Image.Image, sx: int, sy: int) -> None:
    soft_glow(target, sx, sy, 60, (255, 220, 90), passes=5)
    d = ImageDraw.Draw(target)
    d.ellipse([sx - 50, sy - 50, sx + 50, sy + 50], fill=(255, 210, 63, 255))
    for i in range(12):
        a = i * math.pi / 6
        x1 = sx + math.cos(a) * 62
        y1 = sy + math.sin(a) * 62
        x2 = sx + math.cos(a) * 92
        y2 = sy + math.sin(a) * 92
        d.line([(x1, y1), (x2, y2)], fill=(255, 210, 63, 220), width=5)


def draw_cloud(target: Image.Image, cx: int, cy: int, scale: float = 1.0) -> None:
    # shadow
    def draw_shadow(sd, color):
        for dx, dy, r in [(-30, 0, 30), (0, -10, 38), (30, 0, 30)]:
            sd.ellipse([cx + dx * scale - r * scale,
                        cy + dy * scale - r * scale,
                        cx + dx * scale + r * scale,
                        cy + dy * scale + r * scale], fill=color)
    shadow_blob(target, draw_shadow, offset=(4, 6), blur=6, opacity=40)
    d = ImageDraw.Draw(target)
    for dx, dy, r in [(-30, 0, 30), (0, -10, 38), (30, 0, 30)]:
        d.ellipse([cx + dx * scale - r * scale,
                   cy + dy * scale - r * scale,
                   cx + dx * scale + r * scale,
                   cy + dy * scale + r * scale], fill=(255, 255, 255, 255))


def draw_hill(target: Image.Image, bbox: tuple[int, int, int, int],
              fill: tuple[int, int, int], shadow_band_h: int = 8) -> None:
    d = ImageDraw.Draw(target)
    x1, y1, x2, y2 = bbox
    d.ellipse([x1, y1, x2, y2], fill=fill + (255,))
    # darker shadow band along the top edge of the hill
    darker = tuple(max(0, int(c * 0.85)) for c in fill)
    band = Image.new("RGBA", target.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.ellipse([x1, y1, x2, y1 + shadow_band_h * 2], fill=darker + (90,))
    band = band.filter(ImageFilter.GaussianBlur(radius=4))
    target.alpha_composite(band)


def draw_lamp(target: Image.Image, x: int, y: int) -> None:
    # shadow under desk
    def desk_shadow(sd, color):
        sd.rounded_rectangle([x - 80, y + 18, x + 110, y + 36], radius=4, fill=color)
    shadow_blob(target, desk_shadow, offset=(0, 8), blur=8, opacity=80)
    d = ImageDraw.Draw(target)
    # desk
    d.rounded_rectangle([x - 80, y, x + 110, y + 22], radius=4,
                        fill=(139, 90, 60, 255), outline=(80, 50, 25, 255), width=2)
    # stand
    d.rectangle([x + 4, y - 80, x + 18, y], fill=(94, 58, 31, 255))
    # shade
    d.polygon([(x - 30, y - 80), (x + 50, y - 80), (x + 38, y - 130), (x - 20, y - 130)],
              fill=(254, 244, 208, 255), outline=(61, 36, 16, 255))
    # warm light under shade
    soft_glow(target, x + 10, y - 60, 50, (255, 220, 130), passes=4)
    # label
    d.text((x - 70, y + 30), "desk", fill=(40, 28, 12, 255), font=font(13))


def draw_door(target: Image.Image, dx: int, dy: int) -> None:
    # outer glow rings around door
    for r, alpha in [(180, 70), (148, 110), (118, 150)]:
        ring = Image.new("RGBA", target.size, (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse([dx - r, dy + 195 - r, dx + r, dy + 195 + r],
                   outline=(252, 229, 138, alpha), width=4)
        ring = ring.filter(ImageFilter.GaussianBlur(radius=2))
        target.alpha_composite(ring)
    # door shadow
    def door_shadow(sd, color):
        sd.rounded_rectangle([dx - 84, dy + 4, dx + 84, dy + 410], radius=10, fill=color)
    shadow_blob(target, door_shadow, offset=(8, 10), blur=10, opacity=70)
    d = ImageDraw.Draw(target)
    # frame
    d.rounded_rectangle([dx - 84, dy, dx + 84, dy + 410], radius=10,
                        fill=(139, 90, 60, 255), outline=(80, 50, 25, 255), width=2)
    # door
    d.rounded_rectangle([dx - 68, dy + 14, dx + 68, dy + 394], radius=8,
                        fill=(91, 155, 213, 255), outline=(44, 91, 145, 255), width=2)
    # panels
    d.rounded_rectangle([dx - 52, dy + 30, dx + 52, dy + 180], radius=4,
                        outline=(44, 91, 145, 120), width=1)
    d.rounded_rectangle([dx - 52, dy + 200, dx + 52, dy + 370], radius=4,
                        outline=(44, 91, 145, 120), width=1)
    # knob
    soft_glow(target, dx + 38, dy + 190, 12, (255, 210, 63), passes=3)
    d2 = ImageDraw.Draw(target)
    d2.ellipse([dx + 30, dy + 182, dx + 48, dy + 200],
               fill=(255, 210, 63, 255), outline=(61, 36, 16, 255))
    # transom
    d2.rounded_rectangle([dx - 98, dy - 26, dx + 98, dy + 2], radius=4,
                         fill=(94, 58, 31, 255), outline=(50, 30, 14, 255))
    # HOME plaque
    plaque = (dx - 60, dy + 414, dx + 60, dy + 462)
    def plaque_shadow(sd, color):
        sd.rounded_rectangle(plaque, radius=12, fill=color)
    shadow_blob(target, plaque_shadow, offset=(3, 5), blur=4, opacity=80)
    d2.rounded_rectangle(plaque, radius=12, fill=(255, 248, 224, 255),
                         outline=(139, 90, 60, 255), width=3)
    f = font(20)
    bbox = d2.textbbox((0, 0), "HOME", font=f)
    tw = bbox[2] - bbox[0]
    d2.text(((plaque[0] + plaque[2]) / 2 - tw / 2, plaque[1] + 10),
            "HOME", fill=(61, 36, 16, 255), font=f)


def draw_blinkbug(target: Image.Image, bx: int, by: int) -> None:
    # outer halo
    soft_glow(target, bx, by + 20, 110, (252, 229, 138), passes=6)
    # rings
    d = ImageDraw.Draw(target)
    for r, alpha in [(175, 90), (140, 130), (108, 170)]:
        ring = Image.new("RGBA", target.size, (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse([bx - r, by - r, bx + r, by + r],
                   outline=(252, 229, 138, alpha), width=3)
        ring = ring.filter(ImageFilter.GaussianBlur(radius=1.5))
        target.alpha_composite(ring)
    # body shadow
    def body_shadow(sd, color):
        sd.ellipse([bx - 52, by - 38, bx + 52, by + 98], fill=color)
    shadow_blob(target, body_shadow, offset=(4, 8), blur=8, opacity=70)
    # wings
    d.ellipse([bx - 100, by - 14, bx - 52, by + 66],
              fill=(214, 230, 245, 230), outline=(155, 190, 216, 255))
    d.ellipse([bx + 52, by - 14, bx + 100, by + 66],
              fill=(214, 230, 245, 230), outline=(155, 190, 216, 255))
    # body
    d.ellipse([bx - 50, by - 36, bx + 50, by + 96],
              fill=(245, 207, 58, 255), outline=(232, 167, 61, 255), width=3)
    # inner target
    d.ellipse([bx - 28, by - 14, bx + 28, by + 64],
              outline=(232, 167, 61, 255), width=2)
    d.ellipse([bx - 10, by + 18, bx + 10, by + 38], fill=(232, 167, 61, 255))
    # head shadow
    def head_shadow(sd, color):
        sd.ellipse([bx - 36, by - 82, bx + 36, by - 20], fill=color)
    shadow_blob(target, head_shadow, offset=(2, 4), blur=4, opacity=60)
    # head
    d.ellipse([bx - 34, by - 80, bx + 34, by - 22],
              fill=(94, 58, 31, 255), outline=(61, 36, 16, 255), width=2)
    # eyes (with pupil)
    d.ellipse([bx - 20, by - 64, bx - 10, by - 54], fill=(255, 255, 255, 255))
    d.ellipse([bx + 10, by - 64, bx + 20, by - 54], fill=(255, 255, 255, 255))
    d.ellipse([bx - 18, by - 62, bx - 13, by - 57], fill=(61, 36, 16, 255))
    d.ellipse([bx + 13, by - 62, bx + 18, by - 57], fill=(61, 36, 16, 255))
    # smile
    d.arc([bx - 13, by - 55, bx + 13, by - 36], 0, 180,
          fill=(255, 255, 255, 255), width=2)
    # antennae
    d.line([(bx - 22, by - 80), (bx - 40, by - 128)], fill=(61, 36, 16, 255), width=3)
    d.line([(bx + 22, by - 80), (bx + 40, by - 128)], fill=(61, 36, 16, 255), width=3)
    soft_glow(target, bx - 40, by - 130, 10, (252, 229, 138), passes=3)
    soft_glow(target, bx + 40, by - 130, 10, (252, 229, 138), passes=3)
    d2 = ImageDraw.Draw(target)
    d2.ellipse([bx - 48, by - 138, bx - 32, by - 122],
               fill=(245, 207, 58, 255), outline=(232, 167, 61, 255), width=2)
    d2.ellipse([bx + 32, by - 138, bx + 48, by - 122],
               fill=(245, 207, 58, 255), outline=(232, 167, 61, 255), width=2)
    # captain hat
    d2.polygon([(bx - 36, by - 80), (bx + 36, by - 80),
                (bx + 26, by - 106), (bx - 26, by - 106)],
               fill=(44, 91, 145, 255), outline=(29, 61, 99, 255))
    d2.rounded_rectangle([bx - 44, by - 82, bx + 44, by - 74], radius=2,
                         fill=(44, 91, 145, 255), outline=(29, 61, 99, 255))
    d2.rectangle([bx - 22, by - 90, bx + 22, by - 82], fill=(245, 207, 58, 255))


def callout(target: Image.Image, box: tuple[int, int, int, int], text: str,
            size: int = 22, text_color=(26, 44, 92, 255)) -> None:
    # callout shadow
    def shadow_fn(sd, color):
        sd.rounded_rectangle(box, radius=18, fill=color)
    shadow_blob(target, shadow_fn, offset=(3, 6), blur=6, opacity=90)
    d = ImageDraw.Draw(target)
    d.rounded_rectangle(box, radius=18, fill=(255, 248, 224, 255),
                        outline=(139, 90, 60, 255), width=3)
    f = font(size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = (box[0] + box[2]) / 2 - tw / 2
    cy = (box[1] + box[3]) / 2 - th / 2 - 2
    d.text((cx, cy), text, fill=text_color, font=f)


def draw_yacht(target: Image.Image, x: int, y: int) -> None:
    d = ImageDraw.Draw(target)
    # hull
    d.polygon([(x, y), (x + 90, y), (x + 72, y - 20), (x + 14, y - 20)],
              fill=(255, 255, 255, 255), outline=(80, 50, 25, 255))
    # cabin
    d.rectangle([x + 28, y - 44, x + 54, y - 20],
                fill=(255, 255, 255, 255), outline=(80, 50, 25, 255))
    # mast
    d.line([(x + 41, y - 44), (x + 41, y - 70)], fill=(61, 36, 16, 255), width=2)
    # flag
    d.polygon([(x + 41, y - 68), (x + 41, y - 50), (x + 68, y - 56)],
              fill=(255, 210, 63, 255))


def main() -> None:
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # gradient sky (top: warmer, bottom: paler)
    sky = Image.new("RGB", (W, H), (168, 212, 240))
    grad_v(sky, (130, 190, 230), (190, 220, 240))
    base.paste(sky.convert("RGBA"), (0, 0))

    # clouds
    draw_cloud(base, 240, 130, scale=1.0)
    draw_cloud(base, 900, 90, scale=0.9)
    draw_cloud(base, 560, 70, scale=0.7)

    # sun
    draw_sun(base, 1140, 130)

    # hills back→front
    draw_hill(base, (-300, 430, 1600, 1300), (125, 194, 107))
    draw_hill(base, (400, 480, 1700, 1200), (146, 212, 128))
    draw_hill(base, (-200, 540, 700, 1100), (163, 224, 147))

    # yacht in the distance
    draw_yacht(base, 280, 470)

    # desk + lamp on the left (Papa nearby)
    draw_lamp(base, 150, 540)

    # door on the right
    draw_door(base, 980, 290)

    # captain lantern blinkbug — centerpiece
    draw_blinkbug(base, 540, 410)

    # callouts
    callout(base, (360, 30, 920, 100),
            "Lantern's Wish — bounded protector and friend", size=24)
    callout(base, (360, 660, 920, 720),
            "home always works  ·  no secrets  ·  Papa nearby", size=18)

    # paper texture on top
    base.alpha_composite(paper_texture((W, H), density=12000))

    out = base.convert("RGB")
    out.save(OUT_LOCAL, optimize=True)
    out.save(OUT_STATE, optimize=True)
    print(f"saved: {OUT_LOCAL} ({OUT_LOCAL.stat().st_size} bytes)")
    print(f"saved: {OUT_STATE} ({OUT_STATE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
