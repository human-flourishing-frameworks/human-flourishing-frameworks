"""Paint Lantern's Wish — a scene drawn from operator-supplied reference art."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 760
img = Image.new("RGB", (W, H), "#a8d4f0")  # sky
d = ImageDraw.Draw(img)

# soft clouds
for cx, cy, r in [(220, 130, 38), (260, 120, 50), (300, 130, 38),
                  (900, 90, 30), (940, 80, 42), (980, 90, 30)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#ffffff")

# sun, top-right
sx, sy = 1140, 130
d.ellipse([sx - 50, sy - 50, sx + 50, sy + 50], fill="#ffd23f")
for i in range(12):
    a = i * math.pi / 6
    x1, y1 = sx + math.cos(a) * 60, sy + math.sin(a) * 60
    x2, y2 = sx + math.cos(a) * 88, sy + math.sin(a) * 88
    d.line([(x1, y1), (x2, y2)], fill="#ffd23f", width=5)

# rolling hills — far then near
d.ellipse([-300, 430, 1600, 1300], fill="#7dc26b")
d.ellipse([400, 480, 1700, 1200], fill="#92d480")
d.ellipse([-200, 540, 700, 1100], fill="#a3e093")

# desk + lamp on left (Papa nearby)
desk_x1, desk_y = 70, 540
d.rectangle([desk_x1, desk_y, desk_x1 + 200, desk_y + 26], fill="#8b5a3c")
lamp_x = desk_x1 + 90
d.rectangle([lamp_x, desk_y - 90, lamp_x + 16, desk_y], fill="#5e3a1f")
d.polygon([(lamp_x - 38, desk_y - 90), (lamp_x + 54, desk_y - 90),
           (lamp_x + 38, desk_y - 150), (lamp_x - 22, desk_y - 150)],
          fill="#fef4d0", outline="#3d2410", width=2)
# warm glow under shade
for r in (50, 38, 26):
    d.ellipse([lamp_x - r + 8, desk_y - 105 - r // 4,
               lamp_x + r + 8, desk_y - 105 + r // 4],
              outline="#ffd23f", width=1)
d.text((desk_x1 + 6, desk_y + 32), "desk", fill="#3d2410")

# the Door on the right with glow rings
dx, dy = 980, 290
for r in (170, 138, 108):
    d.ellipse([dx - r, dy + 195 - r, dx + r, dy + 195 + r],
              outline="#fce58a", width=4)
# frame + door
d.rectangle([dx - 78, dy, dx + 78, dy + 390], fill="#8b5a3c")
d.rectangle([dx - 64, dy + 16, dx + 64, dy + 374], fill="#5b9bd5")
# doorknob
d.ellipse([dx + 28, dy + 180, dx + 46, dy + 198], fill="#ffd23f", outline="#3d2410")
# transom shape on top
d.rectangle([dx - 90, dy - 24, dx + 90, dy], fill="#5e3a1f")
# HOME plaque hanging
d.rounded_rectangle([dx - 56, dy + 410, dx + 56, dy + 458],
                    radius=12, fill="#fff8e0", outline="#8b5a3c", width=3)
d.text((dx - 28, dy + 422), "HOME", fill="#3d2410")

# Captain Lantern Blinkbug — center-left, flying
bx, by = 540, 410
# concentric glow rings
for r in (165, 132, 102, 80):
    d.ellipse([bx - r, by - r, bx + r, by + r],
              outline="#fce58a", width=3)
# body — vertical oval
d.ellipse([bx - 50, by - 36, bx + 50, by + 96],
          fill="#f5cf3a", outline="#e8a73d", width=3)
# inner concentric target on body (light pattern)
d.ellipse([bx - 28, by - 14, bx + 28, by + 64],
          outline="#e8a73d", width=2)
d.ellipse([bx - 10, by + 18, bx + 10, by + 38], fill="#e8a73d")
# wings (soft pale blue ovals behind body)
d.ellipse([bx - 96, by - 12, bx - 50, by + 64], fill="#d6e6f5", outline="#9bbed8")
d.ellipse([bx + 50, by - 12, bx + 96, by + 64], fill="#d6e6f5", outline="#9bbed8")
# head
d.ellipse([bx - 34, by - 80, bx + 34, by - 22], fill="#5e3a1f", outline="#3d2410", width=2)
# eyes
d.ellipse([bx - 20, by - 64, bx - 10, by - 54], fill="white")
d.ellipse([bx + 10, by - 64, bx + 20, by - 54], fill="white")
d.ellipse([bx - 18, by - 62, bx - 13, by - 57], fill="#3d2410")
d.ellipse([bx + 13, by - 62, bx + 18, by - 57], fill="#3d2410")
# smile
d.arc([bx - 13, by - 55, bx + 13, by - 36], 0, 180, fill="white", width=2)
# antennae
d.line([(bx - 22, by - 80), (bx - 40, by - 128)], fill="#3d2410", width=3)
d.line([(bx + 22, by - 80), (bx + 40, by - 128)], fill="#3d2410", width=3)
d.ellipse([bx - 48, by - 138, bx - 32, by - 122],
          fill="#f5cf3a", outline="#e8a73d", width=2)
d.ellipse([bx + 32, by - 138, bx + 48, by - 122],
          fill="#f5cf3a", outline="#e8a73d", width=2)
# captain hat
d.polygon([(bx - 36, by - 80), (bx + 36, by - 80),
           (bx + 26, by - 106), (bx - 26, by - 106)],
          fill="#2c5b91", outline="#1d3d63")
d.rectangle([bx - 44, by - 82, bx + 44, by - 74],
            fill="#2c5b91", outline="#1d3d63")
d.rectangle([bx - 22, by - 90, bx + 22, by - 82],
            fill="#f5cf3a")

# tiny "Gage's yacht" hint on the horizon, far right
yx, yy = 280, 470
d.polygon([(yx, yy), (yx + 80, yy), (yx + 64, yy - 18), (yx + 14, yy - 18)], fill="#ffffff")
d.rectangle([yx + 26, yy - 40, yx + 50, yy - 18], fill="#ffffff", outline="#8b5a3c")
d.line([(yx + 38, yy - 40), (yx + 38, yy - 64)], fill="#3d2410", width=2)
d.polygon([(yx + 38, yy - 62), (yx + 38, yy - 44), (yx + 62, yy - 50)], fill="#ffd23f")

# Wish callout — top center
def callout(box, text, font_size=22):
    x1, y1, x2, y2 = box
    d.rounded_rectangle([x1, y1, x2, y2],
                        radius=16, fill="#fff8e0",
                        outline="#8b5a3c", width=3)
    try:
        f = ImageFont.truetype("seguivar.ttf", font_size)
    except OSError:
        try:
            f = ImageFont.truetype("segoeui.ttf", font_size)
        except OSError:
            f = ImageFont.load_default()
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    cx = (x1 + x2) / 2 - tw / 2
    cy = (y1 + y2) / 2 - th / 2
    d.text((cx, cy), text, fill="#1a2c5c", font=f)


callout((360, 30, 920, 95),
        "Lantern's Wish — bounded protector and friend", 24)
callout((360, 660, 920, 720),
        "home always works  ·  no secrets  ·  Papa nearby", 18)

out = r"C:\tmp\hff-lantern-recovery\.lantern-wish-painting.png"
img.save(out)
print(out)
