#!/usr/bin/env python3
"""Draws the make.fun news-image entry for Thursday, 19 November 2026.

The page is a news front page: a masthead that names the day, a band of the
day's numbers by region, three hero stories with a drawing each, a grid of
numbered stories with a small drawing each, a map of where the day happened,
a list of the smaller stories of the same day, and a date check at the foot.
Flat colour and one clear type scale keep it readable at about 300 pixels.

Every fact on the page was reported on 19 November 2026, or happened on it.

Run:  python tools/make_entry.py  ->  entry.png
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 233)
INK = (20, 24, 29)
RED = (176, 42, 36)
MUTED = (98, 98, 98)
RULE = (198, 190, 176)
WHITE = (255, 255, 255)
NAVY = (18, 30, 56)
LAND = (226, 210, 173)

FONT_DIR = r"C:\Windows\Fonts"
DISPLAY = os.path.join(FONT_DIR, "georgiab.ttf")
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
REG = os.path.join(FONT_DIR, "arial.ttf")
ITALIC = os.path.join(FONT_DIR, "ariali.ttf")

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")

REGION = {
    "AMERICAS": (38, 88, 158),
    "THE AMERICAS": (38, 88, 158),
    "EUROPE": (36, 108, 70),
    "MIDDLE EAST": (190, 84, 40),
    "AFRICA": (140, 60, 150),
    "ASIA-PACIFIC": (182, 46, 46),
    "WORLD": (72, 72, 82),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def sp_text(draw, xy, s, f, fill, spacing=2, right=None):
    """Letter-spaced text, drawn letter by letter; aligned to `right` when given."""
    x, y = xy
    if right is not None:
        width = sum(draw.textlength(ch, font=f) + spacing for ch in s) - spacing
        x = right - width
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + spacing
    return x


def wrap(draw, s, f, max_w):
    lines, cur = [], ""
    for wd in s.split():
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, s, f, fill, max_w, leading):
    x, y = xy
    for ln in wrap(draw, s, f, max_w):
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def rule(draw, y, x0=24, x1=1000, color=RULE, width=2):
    draw.rectangle([x0, y, x1, y + width], fill=color)


# ---------------------------------------------------------------- flags ----

def flag_us(d, x, y, w, h):
    for s in range(7):
        if s % 2 == 0:
            d.rectangle([x, y + s * h / 7, x + w, y + (s + 1) * h / 7], fill=(190, 40, 44))
    d.rectangle([x, y, x + w * 0.46, y + h * 0.54], fill=(40, 62, 126))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(209, 45, 45))
    sx, sy, sr = x + w * 0.26, y + h * 0.28, h * 0.14
    d.polygon([(sx, sy - sr), (sx + sr * 0.9, sy + sr * 0.55), (sx - sr * 0.9, sy + sr * 0.55)],
              fill=(252, 222, 72))


def flag_ru(d, x, y, w, h):
    for s, col in enumerate(((238, 238, 238), (44, 70, 148), (199, 42, 48))):
        d.rectangle([x, y + s * h / 3, x + w, y + (s + 1) * h / 3], fill=col)


def flag_ua(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 2], fill=(46, 96, 196))
    d.rectangle([x, y + h / 2, x + w, y + h], fill=(250, 208, 58))


# -------------------------------------------------------- illustrations ----

def ill_summit(d, x, y, w, h):
    """A night skyline with the three leaders' flags above it."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 48))
    for i in range(9):
        bw = w * (0.07 + 0.02 * ((i * 7) % 3))
        bh = h * (0.28 + 0.12 * ((i * 5) % 4))
        bx = x + w * 0.04 + i * w * 0.108
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(44, 52, 78))
        for r in range(3):
            for c in range(2):
                if (i + r + c) % 3:
                    d.rectangle([bx + 4 + c * bw * 0.42, y + h - bh + 6 + r * 9,
                                 bx + 4 + c * bw * 0.42 + 3, y + h - bh + 6 + r * 9 + 4],
                                fill=(238, 206, 120))
    fw, fh = w * 0.15, h * 0.20
    fy = y + h * 0.13
    for i, flag in enumerate((flag_us, flag_cn, flag_ru)):
        fx = x + w * 0.30 + i * w * 0.19
        d.line([fx, fy, fx, fy + fh + 4], fill=(150, 150, 160), width=2)
        flag(d, fx + 1, fy, fw, fh)


def ill_gulf(d, x, y, w, h):
    """Drones over a lit base at night, with a strike flash."""
    d.rectangle([x, y, x + w, y + h], fill=(22, 26, 40))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(16, 18, 26))
    for i in range(7):
        bx = x + w * 0.06 + i * w * 0.13
        d.rectangle([bx, y + h * 0.52, bx + w * 0.08, y + h * 0.72], fill=(38, 42, 56))
        for r in range(3):
            d.rectangle([bx + 5, y + h * 0.56 + r * 11, bx + 9, y + h * 0.56 + r * 11 + 5],
                        fill=(240, 200, 110))
    d.polygon([(x + w * 0.74, y + h * 0.44), (x + w * 0.66, y + h * 0.72),
               (x + w * 0.84, y + h * 0.72)], fill=(226, 128, 40))
    cx, cy, r = x + w * 0.30, y + h * 0.28, w * 0.035
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * r * 1.5, cy + sy * r * 1.1
            d.line([cx, cy, ax, ay], fill=(210, 210, 216), width=2)
            d.ellipse([ax - r * 0.7, ay - r * 0.25, ax + r * 0.7, ay + r * 0.25], fill=(210, 210, 216))
    d.rounded_rectangle([cx - r * 0.7, cy - r * 0.5, cx + r * 0.7, cy + r * 0.6],
                        radius=r * 0.2, fill=(210, 210, 216))


def ill_market(d, x, y, w, h):
    """A chart with the Anthropic ticker on the wall."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 236, 228))
    for i in range(6):
        d.line([x, y + h * (0.25 + i * 0.13), x + w, y + h * (0.25 + i * 0.13)],
               fill=(212, 222, 212), width=1)
    bars = (0.34, 0.50, 0.68)
    bw = w * 0.10
    for i, frac in enumerate(bars):
        bh = h * frac
        bx = x + w * 0.08 + i * bw * 1.6
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(58, 104, 168))
    pts = [(x + w * 0.44, y + h * 0.72), (x + w * 0.58, y + h * 0.58),
           (x + w * 0.70, y + h * 0.44), (x + w * 0.86, y + h * 0.20)]
    d.line(pts, fill=(198, 52, 44), width=5)
    d.polygon([(pts[-1][0], pts[-1][1] - 2), (pts[-1][0] + 12, pts[-1][1] + 4),
               (pts[-1][0] - 4, pts[-1][1] + 12)], fill=(198, 52, 44))
    d.text((x + w * 0.05, y + 6), "ANT", font=font(BOLD, 21), fill=(24, 30, 40))
    d.text((x + w * 0.05, y + 32), "$83 a share", font=font(REG, 12), fill=(52, 58, 66))


# -------------------------------------------------------- small drawings ----

def sm_scales(d, x, y, s, c=INK):
    cx, top, base = x + s * 0.5, y + s * 0.18, y + s * 0.80
    d.line([cx, top, cx, base], fill=c, width=3)
    d.line([cx - s * 0.32, top + s * 0.14, cx + s * 0.32, top + s * 0.14], fill=c, width=3)
    d.rectangle([cx - s * 0.24, base, cx + s * 0.24, base + s * 0.07], fill=c)
    for sx in (-1, 1):
        bx = cx + sx * s * 0.32
        d.line([bx, top + s * 0.14, bx, top + s * 0.38], fill=c, width=2)
        d.polygon([(bx - s * 0.12, top + s * 0.38), (bx + s * 0.12, top + s * 0.38),
                   (bx, top + s * 0.54)], fill=(196, 150, 60))


def sm_bridge(d, x, y, s, c=INK):
    w = s * 0.86
    x0 = x + (s - w) / 2
    y0, y1 = y + s * 0.28, y + s * 0.72
    d.rectangle([x0, y0, x0 + w, y0 + 5], fill=c)
    for i in range(5):
        px = x0 + i * (w / 5) + w / 10
        d.line([px, y0, px, y1], fill=(128, 126, 120), width=3)
    d.rectangle([x0, y1, x0 + w, y1 + 5], fill=c)
    d.rectangle([x0 + w * 0.42, y0, x0 + w * 0.60, y1], fill=PAPER)
    d.line([x0 + w * 0.42, y0, x0 + w * 0.36, y0 + s * 0.20], fill=RED, width=4)


def sm_tent(d, x, y, s, c=INK):
    base = y + s * 0.82
    tw, th = s * 0.58, s * 0.46
    tx, ty = x + s * 0.21, base - th
    d.polygon([(tx, ty + th), (tx + tw / 2, ty), (tx + tw, ty + th)], fill=(232, 228, 214))
    d.polygon([(tx + tw / 2 - tw * 0.15, ty + th), (tx + tw / 2, ty + th * 0.34),
               (tx + tw / 2 + tw * 0.15, ty + th)], fill=(52, 54, 60))
    d.line([tx - 2, ty + th, tx + tw + 2, ty + th], fill=(112, 108, 100), width=3)


def sm_house(d, x, y, s, c=INK):
    bx, by = x + s * 0.18, y + s * 0.46
    d.polygon([(bx, by), (bx + s * 0.30, by - s * 0.24), (bx + s * 0.60, by)], fill=(206, 92, 74))
    d.rectangle([bx, by, bx + s * 0.60, y + s * 0.80], fill=(232, 226, 208))
    d.rectangle([bx + s * 0.22, by + s * 0.16, bx + s * 0.38, y + s * 0.80], fill=(70, 70, 76))
    d.line([bx + s * 0.30, by - s * 0.24, bx + s * 0.30, by - s * 0.40], fill=(120, 116, 108), width=3)


def sm_controller(d, x, y, s, c=(36, 108, 70)):
    cx, cy = x + s * 0.5, y + s * 0.52
    w, h = s * 0.76, s * 0.40
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h * 0.45, fill=c)
    d.rectangle([cx - w * 0.26, cy - h * 0.28, cx - w * 0.19, cy + h * 0.08], fill=PAPER)
    d.rectangle([cx - w * 0.31, cy - h * 0.15, cx - w * 0.14, cy + h * 0.02], fill=PAPER)
    for dx, dy in ((w * 0.18, -h * 0.20), (w * 0.27, -h * 0.03),
                   (w * 0.27, h * 0.17), (w * 0.18, h * 0.32)):
        d.ellipse([cx + dx - s * 0.03, cy + dy - s * 0.03,
                   cx + dx + s * 0.03, cy + dy + s * 0.03], fill=(232, 232, 224))


def sm_frame(d, x, y, s, c=(150, 60, 40)):
    fw, fh = s * 0.58, s * 0.44
    fx, fy = x + s * 0.21, y + s * 0.16
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(247, 241, 223), outline=INK, width=2)
    d.polygon([(fx + fw * 0.10, fy + fh * 0.84), (fx + fw * 0.36, fy + fh * 0.34),
               (fx + fw * 0.54, fy + fh * 0.68), (fx + fw * 0.70, fy + fh * 0.44),
               (fx + fw * 0.92, fy + fh * 0.84)], fill=c)
    d.rectangle([fx + fw * 0.06, fy + fh * 0.12, fx + fw * 0.22, fy + fh * 0.30], fill=(226, 196, 92))


def sm_stars(d, x, y, s, c=(30, 62, 132)):
    cx, cy, r = x + s * 0.5, y + s * 0.5, s * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for k in range(8):
        a = -math.pi / 2 + k * 2 * math.pi / 8
        sx, sy = cx + math.cos(a) * r * 0.58, cy + math.sin(a) * r * 0.58
        sr = r * 0.15
        d.polygon([(sx, sy - sr), (sx + sr * 0.9, sy + sr * 0.5), (sx - sr * 0.9, sy + sr * 0.5)],
                  fill=(252, 209, 58))


def sm_storm(d, x, y, s, c=(46, 104, 172)):
    cx, cy = x + s * 0.5, y + s * 0.48
    r = s * 0.28
    d.ellipse([cx - r * 1.3, cy - r * 0.9, cx + r * 1.3, cy + r * 0.5], fill=(146, 170, 200))
    for i in range(3):
        d.ellipse([cx - r * 1.2 + i * r * 0.9, cy - r * 0.7 + (i % 2) * r * 0.3,
                   cx - r * 0.4 + i * r * 0.9, cy + r * 0.4 + (i % 2) * r * 0.3],
                  fill=(176, 196, 218))
    d.ellipse([cx + r * 0.2, cy - r * 0.8, cx + r * 1.2, cy - r * 0.1], fill=(176, 196, 218))
    d.polygon([(cx - r * 0.1, cy + r * 0.1), (cx - r * 0.42, cy + r * 0.8),
               (cx + r * 0.12, cy + r * 0.8), (cx - r * 0.08, cy + r * 1.35)], fill=c)


def sm_island(d, x, y, s, c=INK):
    d.rectangle([x, y + s * 0.62, x + s, y + s * 0.92], fill=(62, 116, 166))
    d.polygon([(x + s * 0.28, y + s * 0.62), (x + s * 0.46, y + s * 0.20),
               (x + s * 0.64, y + s * 0.62)], fill=(96, 132, 84))
    d.polygon([(x + s * 0.52, y + s * 0.34), (x + s * 0.72, y + s * 0.56),
               (x + s * 0.56, y + s * 0.58)], fill=(122, 158, 102))
    d.rectangle([x + s * 0.44, y + s * 0.48, x + s * 0.54, y + s * 0.62], fill=(206, 200, 184))


def sm_capitol(d, x, y, s, c=INK):
    d.polygon([(x + s * 0.14, y + s * 0.34), (x + s * 0.5, y + s * 0.14),
               (x + s * 0.86, y + s * 0.34)], fill=(196, 196, 190))
    for i in range(4):
        cx = x + s * 0.22 + i * s * 0.18
        d.rectangle([cx, y + s * 0.38, cx + s * 0.10, y + s * 0.72], fill=(232, 230, 224))
    d.rectangle([x + s * 0.12, y + s * 0.74, x + s * 0.88, y + s * 0.84], fill=c)


def sm_virus(d, x, y, s, c=(140, 60, 150)):
    cx, cy, r = x + s * 0.5, y + s * 0.5, s * 0.22
    for k in range(10):
        a = k * math.pi / 5
        ex, ey = cx + math.cos(a) * r * 1.5, cy + math.sin(a) * r * 1.5
        d.line([cx + math.cos(a) * r, cy + math.sin(a) * r, ex, ey], fill=c, width=3)
        d.ellipse([ex - r * 0.15, ey - r * 0.15, ex + r * 0.15, ey + r * 0.15], fill=c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=PAPER)


def sm_flags(d, x, y, s, c=INK):
    fw, fh = s * 0.30, s * 0.20
    for i, flag in enumerate((flag_us, flag_cn, flag_ru)):
        fx = x + s * 0.08 + i * s * 0.32
        d.line([fx, y + s * 0.24, fx, y + s * 0.84], fill=(120, 118, 112), width=2)
        flag(d, fx + 1, y + s * 0.26, fw, fh)


# ------------------------------------------------------------------ map ----

WORLD = [
    [(-165, 68), (-125, 70), (-95, 72), (-80, 68), (-60, 60), (-52, 48), (-65, 44), (-70, 40),
     (-75, 28), (-81, 25), (-84, 30), (-90, 29), (-97, 26), (-105, 22), (-115, 30),
     (-124, 40), (-124, 48), (-135, 58)],
    [(-45, 83), (-20, 78), (-22, 70), (-40, 60), (-55, 65), (-60, 75)],
    [(-78, 8), (-60, 10), (-50, 2), (-35, -6), (-38, -18), (-48, -25), (-55, -40), (-65, -53),
     (-72, -50), (-75, -35), (-71, -18), (-78, -2)],
    [(-17, 21), (-5, 32), (10, 37), (20, 33), (32, 31), (35, 20), (43, 12), (51, 12), (48, 2),
     (41, -12), (35, -24), (26, -34), (18, -34), (12, -18), (9, -1), (-2, 5), (-12, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (6, 54), (10, 58), (20, 60), (25, 66), (32, 70), (45, 68),
     (55, 68), (48, 55), (42, 48), (38, 45), (30, 45), (26, 40), (20, 40), (14, 38), (12, 45),
     (4, 43)],
    [(30, 68), (50, 72), (70, 75), (90, 76), (110, 73), (130, 70), (150, 69), (165, 62),
     (162, 52), (145, 45), (130, 42), (122, 38), (121, 30), (110, 22), (107, 10), (100, 5),
     (98, 16), (92, 22), (88, 21), (80, 15), (77, 8), (73, 18), (68, 24), (60, 26), (52, 30),
     (45, 38), (35, 47), (30, 46), (33, 56), (40, 62)],
    [(113, -22), (122, -14), (135, -12), (145, -15), (152, -25), (146, -39), (135, -35),
     (127, -32), (115, -34)],
    [(46, -13), (50, -24), (45, -26), (44, -18)],
    [(130, 32), (138, 35), (142, 42), (145, 44), (140, 38), (133, 34)],
]

PLACES = [
    ("SHENZHEN", 114, 22), ("KUWAIT", 47, 29), ("NEW YORK", -74, 41), ("THE HAGUE", 4, 52),
    ("CRIMEA", 36, 45), ("GAZA", 34, 31), ("BEIRUT", 35, 35), ("BERLIN", 13, 52),
    ("ANTALYA", 30, 37), ("ODISHA", 85, 20), ("HAITI", -72, 18), ("CONGO", 15, -4),
    ("CARACAS", -66, 10), ("WASHINGTON", -77, 39), ("BRASILIA", -48, -16),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(1, 6):
        d.line([x + w * i / 6, y, x + w * i / 6, y + h], fill=(32, 46, 76), width=1)
    for i in range(1, 3):
        d.line([x, y + h * i / 3, x + w, y + h * i / 3], fill=(32, 46, 76), width=1)

    def project(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)

    for poly in WORLD:
        d.polygon([project(lo, la) for lo, la in poly], fill=LAND)
    for name, lon, lat in PLACES:
        px, py = project(lon, lat)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(198, 42, 38), outline=WHITE, width=1)
    sp_text(d, (x + 8, y + 6), "WHERE IT HAPPENED", font(BOLD, 10), WHITE, spacing=2)
    legend = ", ".join(p[0] for p in PLACES)
    para(d, (x + 8, y + h - 34), legend, font(REG, 10), (196, 206, 224), w - 16, 12)


# --------------------------------------------------------------- content ---

REGION_COUNT = [("MIDDLE EAST", 8), ("THE AMERICAS", 8), ("EUROPE", 4), ("WORLD", 4),
                ("ASIA-PACIFIC", 3), ("AFRICA", 3)]

STATS = [
    ("AMERICAS", "56-44", "Democrats take the Senate"),
    ("EUROPE", "€45bn", "new EU loan for Ukraine"),
    ("MIDDLE EAST", "$92", "Brent crude, a barrel"),
    ("AFRICA", "11,432", "Ebola cases in DR Congo"),
    ("ASIA-PACIFIC", "3", "leaders meet in Shenzhen"),
    ("WORLD", "25.9bn km", "Voyager 1: one light-day"),
]

HEROES = [
    dict(region="ASIA-PACIFIC", n=1, kick="SHENZHEN · APEC SUMMIT",
         head="Trump, Xi and Putin hold their first three-way summit",
         body="At APEC in Shenzhen: arms control, Ukraine and Iran on the table.",
         art=ill_summit),
    dict(region="MIDDLE EAST", n=2, kick="GULF · KUWAIT",
         head="Iran's drones hit a US base in Kuwait",
         body="Ali Al-Salem base hit; Kuwait intercepts; Brent climbs to $92.",
         art=ill_gulf),
    dict(region="AMERICAS", n=3, kick="NASDAQ · MARKETS",
         head="Anthropic debuts at $83 a share, a $1 trillion AI listing",
         body="An $81bn offering, and the most watched first day on the market.",
         art=ill_market),
]

GRID = [
    ("WORLD", "The world's top court delivers its judgment in the Myanmar-Rohingya case", sm_scales),
    ("EUROPE", "The Kerch bridge is hit a third time in four days; rail traffic stops", sm_bridge),
    ("MIDDLE EAST", "Israeli forces push west of the Yellow Line as Gaza's ceasefire cracks", sm_tent),
    ("MIDDLE EAST", "Air strikes hit towns in south Lebanon and homes are pulled down", sm_house),
    ("WORLD", "GTA VI arrives to a record $1.65bn of pre-orders", sm_controller),
    ("WORLD", "Van Gogh's 'Chestnut Trees in Blossom' sells for a record $190.4m", sm_frame),
    ("EUROPE", "Europe's coalition of the willing meets in Berlin on Ukraine", sm_stars),
    ("ASIA-PACIFIC", "Cyclone Akvan closes on the Andhra Pradesh and Odisha coasts", sm_storm),
    ("AFRICA", "Haiti: the UN counts 4,595 killed in armed violence this year", sm_island),
    ("AMERICAS", "Democrats take the Senate 56-44 as the House picks Jeffries", sm_capitol),
    ("AFRICA", "Ebola reaches Watsa: 11,432 cases and 5,593 deaths, WHO says", sm_virus),
    ("AMERICAS", "Washington and Caracas agree to re-establish military ties", sm_flags),
]

BRIEFS = [
    "COP31 talks: 21 items unresolved",
    "Fed minutes: more rate rises eyed",
    "The US loses its measles-free status",
    "Yemen bans the Houthis as terrorists",
    "Three tankers hit by mines near Hormuz",
    "OPEC+ sets output on 29 November",
    "Ebola vaccines to be trialled in Congo",
    "The UK sends long-range missiles to Ukraine",
    "Ottawa and Delhi eye a defence pact",
    "Brazil's 5x2 workweek becomes law",
    "Syria's churches condemn the attacks",
    "Colombia's unions take to the streets",
    "The Panama Canal keeps 32 daily transits",
    "UN: a quarter of women cannot say no",
    "Nvidia falls after its leadership change",
    "Gaza's Board of Peace blames both sides",
]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_eyebrow = font(BOLD, 13)
    f_date = font(DISPLAY, 42)
    f_sub = font(ITALIC, 15)
    f_reg = font(BOLD, 11)
    f_num = font(BOLD, 26)
    f_lab = font(REG, 11)
    f_kick = font(BOLD, 12)
    f_hero_h = font(BOLD, 18)
    f_hero_b = font(REG, 13)
    f_gh = font(BOLD, 13)
    f_gn = font(BOLD, 10)
    f_brief_b = font(REG, 11)
    f_foot = font(REG, 12)

    # ---- masthead ----
    sp_text(d, (24, 10), "THE WORLD IN ONE IMAGE", f_eyebrow, RED, spacing=3)
    d.text((1000 - d.textlength("ONE PAGE · 31 STORIES", font=f_foot), 11),
           "ONE PAGE · 31 STORIES", font=f_foot, fill=MUTED)
    d.text((24, 28), "Thursday 19 November 2026", font=f_date, fill=INK)
    rule(d, 76, 24, 1000, INK, 3)
    d.text((24, 84), "Three leaders meet in Shenzhen · Iran's drones hit a US base in Kuwait · The "
                     "biggest IPO ever debuts · A court delivers a genocide verdict",
           font=f_sub, fill=RED)
    rule(d, 108, 24, 1000, RULE, 2)

    # ---- how the day's news is spread ----
    y0 = 114
    cellw = (1000 - 24) // 6
    for i, (region, count) in enumerate(REGION_COUNT):
        x = 24 + i * cellw
        col = REGION[region]
        d.rectangle([x, y0, x + cellw - 4, y0 + 18], fill=col)
        sp_text(d, (x + 6, y0 + 3), region, f_reg, WHITE, spacing=1)
        d.text((x + cellw - 30, y0 + 22), str(count), font=font(BOLD, 17), fill=INK)
    rule(d, y0 + 46, 24, 1000, RULE, 1)

    # ---- the day in numbers ----
    y1 = 172
    for i, (region, number, label) in enumerate(STATS):
        x = 24 + i * cellw
        col = REGION[region]
        d.rectangle([x, y1, x + cellw - 4, y1 + 18], fill=col)
        sp_text(d, (x + 6, y1 + 3), region, f_reg, WHITE, spacing=1)
        d.text((x + 2, y1 + 24), number, font=f_num, fill=INK)
        para(d, (x + 2, y1 + 54), label, f_lab, MUTED, cellw - 16, 13)
    rule(d, y1 + 84, 24, 1000, INK, 2)

    # ---- hero stories ----
    hy = 272
    hw = (1000 - 24 - 16) // 3
    for i, hero in enumerate(HEROES):
        x = 24 + i * (hw + 8)
        col = REGION[hero["region"]]
        d.rectangle([x, hy, x + hw, hy + 184], fill=WHITE, outline=RULE, width=2)
        hero["art"](d, x + 1, hy + 1, hw - 2, 74)
        d.rectangle([x + 1, hy + 75, x + hw - 1, hy + 78], fill=col)
        sp_text(d, (x + 12, hy + 86), f'{hero["n"]} · {hero["kick"]}', f_kick, col, spacing=1)
        yy = para(d, (x + 12, hy + 102), hero["head"], f_hero_h, INK, hw - 24, 20)
        para(d, (x + 12, yy + 4), hero["body"], f_hero_b, MUTED, hw - 24, 15)

    # ---- numbered story grid ----
    gy = 464
    gw = (1000 - 24 - 30) // 4
    gh = 96
    for i, (region, head, art) in enumerate(GRID):
        x = 24 + (i % 4) * (gw + 10)
        y = gy + (i // 4) * (gh + 4)
        col = REGION[region]
        d.rectangle([x, y, x + gw, y + gh], fill=WHITE, outline=RULE, width=2)
        d.rectangle([x + 1, y + 1, x + gw - 1, y + 5], fill=col)
        art(d, x + 8, y + 10, 34, 34)
        d.ellipse([x + 48, y + 12, x + 64, y + 28], fill=col)
        num = str(i + 4)
        d.text((x + 56 - d.textlength(num, font=f_gn) / 2, y + 15), num, font=f_gn, fill=WHITE)
        sp_text(d, (x + 72, y + 14), region, f_gn, col, spacing=1)
        para(d, (x + 10, y + 50), head, f_gh, INK, gw - 20, 14)

    # ---- map and the rest of the day ----
    my = 766
    d.rectangle([24, my, 24 + 468, my + 168], fill=NAVY)
    draw_map(d, 24, my, 468, 168)
    bx = 508
    sp_text(d, (bx, my + 4), "ALSO ON THURSDAY 19 NOVEMBER", f_kick, INK, spacing=2)
    rule(d, my + 22, bx, 1000, RULE, 1)
    for i, txt in enumerate(BRIEFS):
        col = i % 2
        x = bx + col * 250
        y = my + 30 + (i // 2) * 17
        d.text((x, y), str(i + 16).rjust(2, "0"), font=font(BOLD, 10), fill=RED)
        d.text((x + 22, y), txt, font=f_brief_b, fill=(70, 70, 74))

    # ---- foot ----
    fy = 946
    rule(d, fy, 24, 1000, INK, 2)
    d.text((24, fy + 10), "DATE CHECK", font=font(BOLD, 11), fill=RED)
    d.text((24, fy + 26), "Every story here happened, or was first reported, on Thursday "
                          "19 November 2026.", font=f_foot, fill=INK)
    d.text((24, fy + 43), "Sources: Reuters, AP, BBC, Xinhua, The Hindu, UN News, WHO, NASA, "
                          "Sotheby's, the ICJ.", font=f_foot, fill=MUTED)
    right = "One image · one day · 19.11.2026"
    d.text((1000 - d.textlength(right, font=f_foot), fy + 43), right, font=f_foot, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
