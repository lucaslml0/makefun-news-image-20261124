#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

One 1024x1024 PNG newspaper front page summarising the day's world
news in six stories, drawn entirely with Pillow primitives. No network,
no downloaded assets, no external images.

Run:  python3 draw_entry.py            (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
PAPER = (245, 239, 225)      # newsprint cream
INK = (20, 20, 20)           # near-black
RED = (158, 27, 27)          # masthead accent / kickers
MUTED = (90, 83, 72)         # grey-brown for source lines
RULE = (20, 20, 20)
SOFT = (226, 216, 196)       # light panel
BLUE = (38, 84, 124)
GREEN = (46, 125, 50)
ORANGE = (214, 96, 20)
GOLD = (176, 132, 30)

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = os.path.join(FN, "NotoSerif-Black.ttf")
SERIF_BOLD = os.path.join(FN, "NotoSerif-Bold.ttf")
SERIF = os.path.join(FN, "NotoSerif-Regular.ttf")
SANS_BOLD = os.path.join(FN, "NotoSans-Bold.ttf")
SANS = os.path.join(FN, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text helpers
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_chart(d, x, y, w, h):
    """Rising bar chart with an arrow (Nvidia / markets)."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 244, 233), outline=INK, width=2)
    bars = [0.28, 0.38, 0.34, 0.52, 0.46, 0.66, 0.60, 0.86]
    bw = w // 12
    base = y + h - 26
    for i, f in enumerate(bars):
        bx = x + 10 + i * (bw + 4)
        bh = int((h - 52) * f)
        d.rectangle([bx, base - bh, bx + bw, base], fill=GREEN)
    d.line([(x + 8, base - int((h - 52) * 0.30)),
            (x + w - 8, base - int((h - 52) * 0.88))],
           fill=RED, width=4)
    d.polygon([(x + w - 8, base - int((h - 52) * 0.88)),
               (x + w - 26, base - int((h - 52) * 0.88) + 2),
               (x + w - 10, base - int((h - 52) * 0.88) - 14)],
              fill=RED)
    d.text((x + 10, y + h - 22), "NVDA  +31%",
           font=font(SANS_BOLD, 17), fill=INK)


def icon_globe(d, x, y, w, h):
    """Globe with a warning sun (climate talks)."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244), outline=INK, width=2)
    cx, cy, r = x + w // 2 - 8, y + h // 2 + 4, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 214),
              outline=BLUE, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=2)
    d.ellipse([cx - 22, cy - 18, cx - 2, cy + 2], fill=GREEN)   # land blob
    d.ellipse([cx + 2, cy + 6, cx + 20, cy + 24], fill=GREEN)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    sx, sy = x + w - 26, y + 18
    d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=GOLD)
    for a in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line([(sx + dx * 12, sy + dy * 12), (sx + dx * 17, sy + dy * 17)],
               fill=GOLD, width=2)


def icon_flame(d, x, y, w, h):
    """Flame over a factory roof (Indonesia fire)."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 232, 214), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 + 14
    d.polygon([(cx - 30, cy + 18), (cx - 26, cy - 6), (cx - 12, cy - 26),
               (cx - 2, cy - 44), (cx + 8, cy - 22), (cx + 22, cy - 30),
               (cx + 18, cy - 8), (cx + 30, cy + 18)],
              fill=ORANGE)
    d.polygon([(cx - 12, cy + 18), (cx - 8, cy - 2), (cx + 2, cy - 14),
               (cx + 10, cy + 2), (cx + 13, cy + 18)], fill=(240, 196, 40))
    d.rectangle([x + 12, y + h - 22, x + w - 12, y + h - 12], fill=INK)


def icon_ship(d, x, y, w, h):
    """Cargo ship on waves with smoke (Sparta II)."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244), outline=INK, width=2)
    cx = x + w // 2
    d.ellipse([cx - 26, y + 8, cx - 12, y + 22], fill=MUTED)
    d.ellipse([cx - 16, y + 2, cx - 2, y + 16], fill=MUTED)
    d.ellipse([cx - 6, y + 10, cx + 8, y + 24], fill=MUTED)
    d.polygon([(x + 12, y + h - 34), (x + w - 12, y + h - 34),
               (x + w - 26, y + h - 16), (x + 26, y + h - 16)], fill=INK)
    d.rectangle([x + 20, y + h - 52, x + 34, y + h - 34], fill=RED)
    d.rectangle([x + 38, y + h - 52, x + 52, y + h - 34], fill=GOLD)
    d.rectangle([x + 56, y + h - 52, x + 70, y + h - 34], fill=BLUE)
    d.rectangle([x + w - 34, y + h - 58, x + w - 18, y + h - 34], fill=(240, 240, 240),
                outline=INK, width=1)
    for wy in (y + h - 12, y + h - 6):
        d.line([(x + 8, wy), (x + w - 8, wy)], fill=BLUE, width=2)


def icon_train(d, x, y, w, h):
    """Front of a train on rails (India-Nepal link)."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 236, 244), outline=INK, width=2)
    tx, ty, tw, th = x + 14, y + 16, w - 28, 46
    d.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8,
                        fill=RED, outline=INK, width=2)
    d.rectangle([tx + 10, ty + 10, tx + tw // 2 - 6, ty + 28],
                fill=(200, 225, 245), outline=INK, width=1)
    d.rectangle([tx + tw // 2 + 6, ty + 10, tx + tw - 10, ty + 28],
                fill=(200, 225, 245), outline=INK, width=1)
    d.ellipse([tx + tw // 2 - 6, ty + 34, tx + tw // 2 + 6, ty + 46],
              fill=GOLD, outline=INK, width=1)
    d.line([(x + 16, y + h - 16), (x + w - 16, y + h - 16)], fill=INK, width=3)
    d.line([(x + 22, y + h - 10), (x + w - 22, y + h - 10)], fill=INK, width=3)
    for sx in (x + 26, x + w // 2, x + w - 26):
        d.line([(sx, y + h - 16), (sx, y + h - 10)], fill=INK, width=2)


def icon_aid(d, x, y, w, h):
    """Aid box with a cross above a wave (Gaza aid)."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 232), outline=INK, width=2)
    bx, by, bw, bh = x + 18, y + 14, w - 36, 44
    d.rectangle([bx, by, bx + bw, by + bh], fill=(214, 178, 120),
                outline=INK, width=2)
    d.rectangle([bx, by, bx + bw, by + 10], fill=(190, 150, 96),
                outline=INK, width=1)
    cx, cy = bx + bw // 2, by + bh // 2 + 4
    d.rectangle([cx - 4, cy - 12, cx + 4, cy + 12], fill=RED)
    d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=RED)
    for wy, ww in ((y + h - 26, w - 24), (y + h - 16, w - 40)):
        xs = x + (w - ww) // 2
        d.arc([xs, wy - 8, xs + ww, wy + 8], 0, 180, fill=BLUE, width=3)


ICONS = {
    "chart": icon_chart,
    "globe": icon_globe,
    "flame": icon_flame,
    "ship": icon_ship,
    "train": icon_train,
    "aid": icon_aid,
}


# ---------------------------------------------------------------- page
def draw():
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    MX = 34                      # side margin
    RX = W - MX                  # right edge of content

    # ---- masthead ----
    f_mast = font(SERIF_BLACK, 62)
    d.text((W // 2, 24), "THE WORLD TODAY", font=f_mast, fill=INK,
           anchor="ma")
    d.text((MX, 96), "WORLD EDITION", font=font(SANS_BOLD, 15), fill=MUTED)
    d.text((RX, 96), "SIX STORIES · ONE DAY", font=font(SANS_BOLD, 15),
           fill=MUTED, anchor="ra")
    hrule(d, MX, RX, 122, 2)
    f_date = font(SERIF_BOLD, 26)
    d.text((W // 2, 130), "TUESDAY, 24 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    hrule(d, MX, RX, 166, 3)
    hrule(d, MX, RX, 171, 1)

    # ---- lead story: Nvidia ----
    y = 180
    d.text((MX, y), "MARKETS  ·  TECHNOLOGY", font=font(SANS_BOLD, 15),
           fill=RED)
    y += 20
    y = para(d, MX, y, "Huang returns to Nvidia as shares soar 31%",
             font(SERIF_BOLD, 36), 664, 38, max_lines=2)
    y += 6
    y = para(d, MX, y,
             "Eleven days after resigning in scandal, co-founder Jensen "
             "Huang is back as chief executive. Nvidia jumped 31% and the "
             "Nasdaq rose 6.5%.",
             font(SANS, 17), 664, 20, max_lines=2)
    d.text((MX, 322), "Source: Reuters", font=font(SANS, 13), fill=MUTED)
    icon_chart(d, 716, 184, 274, 140)
    hrule(d, MX, RX, 344, 2)

    # ---- grid of four stories, two columns x two rows ----
    stories = [
        ("CLIMATE  ·  ANTALYA", "Climate talks collapse with no deal",
         "COP31 ended without agreement after 194 nations split over "
         "fossil fuels \u2014 the longest climate summit ever.",
         "Source: CNN", "globe"),
        ("DISASTER  ·  INDONESIA", "24 killed in Indonesian factory fire",
         "A blaze tore through a candy factory in Banten; about 30 workers "
         "are still missing as rescuers search the wreckage.",
         "Source: Reuters", "flame"),
        ("WAR AT SEA  ·  BALTIC", "Drone-hit Russian ship reaches port",
         "The cargo ship Sparta II, set ablaze by drones in the Gulf of "
         "Finland, arrived in St Petersburg under tow. Its 16 crew are safe.",
         "Source: Reuters", "ship"),
        ("DIPLOMACY  ·  SOUTH ASIA", "New train links Ayodhya and Janakpur",
         "India and Nepal flagged off the weekly Saryu-Kamala Express; "
         "the first train reaches Janakpur today.",
         "Source: ANI", "train"),
    ]
    col_w = 466
    cols = [MX, MX + col_w + 24]
    rows = [360, 574]
    cell_h = 200
    for i, (kick, head, body, src, icon) in enumerate(stories):
        cx = cols[i % 2]
        cy = rows[i // 2]
        d.text((cx, cy), kick, font=font(SANS_BOLD, 14), fill=RED)
        ty = cy + 22
        ty = para(d, cx, ty, head, font(SERIF_BOLD, 26),
                  col_w - 100, 31, max_lines=2)
        ty += 4
        para(d, cx, ty, body, font(SANS, 17), col_w - 100, 22,
             max_lines=3)
        d.text((cx, cy + cell_h - 18), src, font=font(SANS, 13),
               fill=MUTED)
        ICONS[icon](d, cx + col_w - 88, cy + 22, 88, 88)
        if i % 2 == 0:
            d.line([(cx + col_w + 12, cy + 4),
                    (cx + col_w + 12, cy + cell_h - 4)], fill=SOFT, width=2)
    hrule(d, MX, RX, 556, 1, fill=SOFT)
    hrule(d, MX, RX, 790, 2)

    # ---- bottom strip: Gaza aid ----
    y = 806
    icon_aid(d, MX, y + 6, 120, 120)
    tx = MX + 140
    d.text((tx, y), "MIDDLE EAST  ·  GAZA", font=font(SANS_BOLD, 15),
           fill=RED)
    y2 = para(d, tx, y + 24,
              "Four nations urge Israel to open Gaza aid routes",
              font(SERIF_BOLD, 28), RX - tx, 34, max_lines=1)
    para(d, tx, y2 + 4,
         "Australia, Canada, Italy and Britain jointly called for immediate, "
         "unrestricted aid access to Gaza, where flooding has added to the "
         "suffering of Palestinians.",
         font(SANS, 18), RX - tx, 23, max_lines=2)
    d.text((tx, 912), "Source: The Paris Eye", font=font(SANS, 13),
           fill=MUTED)

    # ---- footer ----
    hrule(d, MX, RX, 948, 1)
    d.text((W // 2, 960),
           "Compiled from reports by Reuters, CNN, The Paris Eye and "
           "ANI  \u00b7  Drawn with Python + Pillow",
           font=font(SANS, 13), fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = draw()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
