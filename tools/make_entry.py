#!/usr/bin/env python3
"""Draws the make.fun news-image entry for Thursday, 19 November 2026.

The page is a news front page: a masthead that names the day, a band of the
day's numbers by region, three hero stories with a drawing each, a grid of
numbered stories, a list of the smaller stories of the same day, and a date
check at the foot. Flat colour and one clear type scale keep it readable when
it is scaled down to about 300 pixels wide.

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

FONT_DIR = r"C:\Windows\Fonts"
DISPLAY = os.path.join(FONT_DIR, "georgiab.ttf")
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
REG = os.path.join(FONT_DIR, "arial.ttf")
ITALIC = os.path.join(FONT_DIR, "ariali.ttf")

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")

REGION = {
    "AMERICAS": (38, 88, 158),
    "EUROPE": (36, 108, 70),
    "MENA": (190, 84, 40),
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
    bars = (0.22, 0.34, 0.48)
    bw = w * 0.10
    for i, bh in enumerate(bars):
        bx = x + w * 0.08 + i * bw * 1.6
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(58, 104, 168))
    pts = [(x + w * 0.44, y + h * 0.72), (x + w * 0.58, y + h * 0.58),
           (x + w * 0.70, y + h * 0.44), (x + w * 0.86, y + h * 0.20)]
    d.line(pts, fill=(198, 52, 44), width=5)
    d.polygon([(pts[-1][0], pts[-1][1] - 2), (pts[-1][0] + 12, pts[-1][1] + 4),
               (pts[-1][0] - 4, pts[-1][1] + 12)], fill=(198, 52, 44))
    d.text((x + w * 0.05, y + 8), "ANT", font=font(BOLD, 22), fill=(24, 30, 40))
    d.text((x + w * 0.05, y + 36), "$83 a share", font=font(REG, 13), fill=(52, 58, 66))


# ---------------------------------------------------------------- icons ----

def icon_drone(d, x, y, s, color=RED):
    cx, cy = x + s * 0.5, y + s * 0.44
    r = s * 0.26
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * r * 0.92, cy + sy * r * 0.68
        d.line([cx, cy, ax, ay], fill=color, width=6)
        d.ellipse([ax - r * 0.42, ay - r * 0.16, ax + r * 0.42, ay + r * 0.16], fill=color)
    d.rounded_rectangle([cx - r * 0.40, cy - r * 0.26, cx + r * 0.40, cy + r * 0.34],
                        radius=r * 0.12, fill=color)
    d.polygon([(cx - r * 0.30, cy + r * 0.90), (cx, cy + r * 1.60), (cx + r * 0.30, cy + r * 0.90)],
              fill=(214, 118, 30))


def icon_bridge(d, x, y, s, color=INK):
    w = s * 0.9
    x0 = x + (s - w) / 2
    y0 = y + s * 0.26
    y1 = y + s * 0.74
    d.rectangle([x0, y0, x0 + w, y0 + 8], fill=color)
    for i in range(5):
        px = x0 + i * (w / 5) + w / 10
        d.line([px, y0, px, y1], fill=(124, 122, 116), width=4)
    d.rectangle([x0, y1, x0 + w, y1 + 7], fill=color)
    d.rectangle([x0 + w * 0.40, y0, x0 + w * 0.62, y1], fill=PAPER)
    d.line([x0 + w * 0.40, y0, x0 + w * 0.33, y0 + s * 0.22], fill=RED, width=5)
    d.line([x0 + w * 0.62, y0, x0 + w * 0.70, y0 + s * 0.30], fill=RED, width=5)


def icon_scales(d, x, y, s, color=INK):
    cx = x + s * 0.5
    base = y + s * 0.80
    top = y + s * 0.20
    d.line([cx, top, cx, base], fill=color, width=5)
    d.line([cx - s * 0.34, top + s * 0.14, cx + s * 0.34, top + s * 0.14], fill=color, width=5)
    d.rectangle([cx - s * 0.26, base, cx + s * 0.26, base + s * 0.07], fill=color)
    for sx in (-1, 1):
        bx = cx + sx * s * 0.34
        d.line([bx, top + s * 0.14, bx, top + s * 0.40], fill=color, width=3)
        d.polygon([(bx - s * 0.14, top + s * 0.40), (bx + s * 0.14, top + s * 0.40),
                   (bx, top + s * 0.58)], fill=(196, 150, 60))


def icon_controller(d, x, y, s, color=(36, 108, 70)):
    cx, cy = x + s * 0.5, y + s * 0.52
    w, h = s * 0.78, s * 0.42
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h * 0.45, fill=color)
    d.rectangle([cx - w * 0.26, cy - h * 0.30, cx - w * 0.18, cy + h * 0.10], fill=PAPER)
    d.rectangle([cx - w * 0.31, cy - h * 0.17, cx - w * 0.13, cy + h * 0.03], fill=PAPER)
    for dx, dy in ((w * 0.18, -h * 0.22), (w * 0.28, -h * 0.04),
                   (w * 0.28, h * 0.18), (w * 0.18, h * 0.34)):
        d.ellipse([cx + dx - s * 0.035, cy + dy - s * 0.035,
                   cx + dx + s * 0.035, cy + dy + s * 0.035], fill=(228, 228, 220))


def icon_frame(d, x, y, s, color=(150, 60, 40)):
    fw, fh = s * 0.62, s * 0.50
    fx, fy = x + s * 0.19, y + s * 0.13
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(247, 241, 223), outline=INK, width=3)
    d.polygon([(fx + fw * 0.10, fy + fh * 0.84), (fx + fw * 0.36, fy + fh * 0.34),
               (fx + fw * 0.54, fy + fh * 0.68), (fx + fw * 0.70, fy + fh * 0.44),
               (fx + fw * 0.92, fy + fh * 0.84)], fill=color)
    d.rectangle([fx + fw * 0.06, fy + fh * 0.14, fx + fw * 0.22, fy + fh * 0.32], fill=(226, 196, 92))
    d.line([fx + fw * 0.50, fy + fh, fx + fw * 0.44, y + s * 0.92], fill=INK, width=4)
    d.line([fx + fw * 0.52, fy + fh, fx + fw * 0.60, y + s * 0.92], fill=INK, width=4)
    d.rectangle([fx + fw * 0.28, y + s * 0.88, fx + fw * 0.76, y + s * 0.94], fill=INK)


def icon_sun(d, x, y, s, color=(206, 140, 40)):
    cx, cy = x + s * 0.5, y + s * 0.5
    r = s * 0.22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for i in range(8):
        a = i * math.pi / 4
        d.line([cx + math.cos(a) * r * 1.35, cy + math.sin(a) * r * 1.35,
                cx + math.cos(a) * r * 1.85, cy + math.sin(a) * r * 1.85], fill=color, width=4)


# --------------------------------------------------------------- content ---

STATS = [
    ("AMERICAS", "56-44", "Democrats take the Senate"),
    ("EUROPE", "€45bn", "new EU loan for Ukraine"),
    ("MENA", "$92", "Brent crude, a barrel"),
    ("AFRICA", "11,432", "Ebola cases in DR Congo"),
    ("ASIA-PACIFIC", "3", "leaders meet in Shenzhen"),
    ("WORLD", "25.9bn km", "Voyager 1: one light-day"),
]

HEROES = [
    dict(region="ASIA-PACIFIC", n=1, kick="SHENZHEN · APEC SUMMIT",
         head="Trump, Xi and Putin hold their first three-way summit",
         body="At APEC in Shenzhen: arms control, Ukraine and Iran on the table.",
         art=ill_summit),
    dict(region="MENA", n=2, kick="GULF · KUWAIT",
         head="Iran's drones hit a US base in Kuwait",
         body="Ali Al-Salem base hit; Kuwait intercepts; Brent climbs to $92.",
         art=ill_gulf),
    dict(region="AMERICAS", n=3, kick="NASDAQ · MARKETS",
         head="Anthropic debuts at $83 a share, a $1 trillion AI listing",
         body="An $81bn offering, and the most watched first day on the market.",
         art=ill_market),
]

GRID = [
    ("WORLD", "The world's top court delivers its judgment in the Myanmar-Rohingya case"),
    ("EUROPE", "The Kerch bridge is hit a third time in four days; rail traffic stops"),
    ("MENA", "Israeli forces push west of the Yellow Line as Gaza's ceasefire cracks"),
    ("MENA", "Air strikes hit towns in south Lebanon and homes are pulled down"),
    ("WORLD", "GTA VI arrives to a record $1.65bn of pre-orders"),
    ("WORLD", "Van Gogh's 'Chestnut Trees in Blossom' sells for a record $190.4m"),
    ("EUROPE", "Europe's coalition of the willing meets in Berlin on Ukraine"),
    ("ASIA-PACIFIC", "Cyclone Akvan closes on the Andhra Pradesh and Odisha coasts"),
    ("AFRICA", "Haiti: the UN counts 4,595 killed in armed violence this year"),
    ("AMERICAS", "Democrats take the Senate 56-44 as the House picks Jeffries"),
    ("AFRICA", "Ebola reaches Watsa: 11,432 cases and 5,593 deaths, WHO says"),
    ("AMERICAS", "Washington and Caracas agree to re-establish military ties"),
]

BRIEFS = [
    "COP31 in Antalya: 21 items unresolved as new climate texts land",
    "Fed minutes show inflation unease and a case for further rate rises",
    "The US loses its measles-free status; an eighth death in Pennsylvania",
    "Yemen's presidency declares the Houthis a terrorist organisation",
    "Three oil tankers disabled by mines near the Strait of Hormuz",
    "Brent falls for a fourth week; OPEC+ sets output on 29 November",
    "Congo's Ebola vaccine trials begin next week as the virus spreads",
    "The UK brings long-range cruise missiles to Ukraine",
    "Paris and Ottawa near a defence pact during Modi's December visit",
    "Brasilia's 5x2 workweek is signed into law",
    "Syria's church leaders condemn attacks on Christian communities",
    "Colombia's unions march against the government",
    "The Panama Canal expects 32 daily transits in the dry season",
    "The UN: one in four women worldwide cannot refuse sex in marriage",
    "Nvidia falls after its leadership change, ending an AI rally",
    "Israel and Hamas are both blamed by the Board of Peace for Gaza's impasse",
]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_eyebrow = font(BOLD, 14)
    f_date = font(DISPLAY, 44)
    f_sub = font(ITALIC, 16)
    f_reg = font(BOLD, 11)
    f_num = font(BOLD, 28)
    f_lab = font(REG, 11)
    f_kick = font(BOLD, 12)
    f_hero_h = font(BOLD, 19)
    f_hero_b = font(REG, 13)
    f_gh = font(BOLD, 14)
    f_gn = font(BOLD, 11)
    f_brief_h = font(BOLD, 12)
    f_brief_b = font(REG, 12)
    f_foot = font(REG, 12)

    # ---- masthead ----
    sp_text(d, (24, 12), "THE WORLD IN ONE IMAGE", f_eyebrow, RED, spacing=3)
    d.text((1000 - d.textlength("ONE PAGE · 31 STORIES", font=f_foot), 13),
           "ONE PAGE · 31 STORIES", font=f_foot, fill=MUTED)
    d.text((24, 32), "Thursday 19 November 2026", font=f_date, fill=INK)
    rule(d, 82, 24, 1000, INK, 3)
    d.text((24, 92), "Three leaders meet in Shenzhen · Iran's drones hit a US base in Kuwait · "
                     "The biggest IPO ever debuts · A court delivers a genocide verdict",
           font=f_sub, fill=RED)
    rule(d, 118, 24, 1000, RULE, 2)

    # ---- the day in numbers, by region ----
    y0 = 128
    cellw = (1000 - 24) // 6
    for i, (region, number, label) in enumerate(STATS):
        x = 24 + i * cellw
        col = REGION[region]
        d.rectangle([x, y0, x + cellw - 4, y0 + 20], fill=col)
        sp_text(d, (x + 6, y0 + 4), region, f_reg, WHITE, spacing=1)
        d.text((x + 2, y0 + 26), number, font=f_num, fill=INK)
        para(d, (x + 2, y0 + 58), label, f_lab, MUTED, cellw - 16, 14)
    rule(d, y0 + 92, 24, 1000, INK, 2)

    # ---- hero stories ----
    hy = 226
    hw = (1000 - 24 - 16) // 3
    for i, hero in enumerate(HEROES):
        x = 24 + i * (hw + 8)
        col = REGION[hero["region"]]
        d.rectangle([x, hy, x + hw, hy + 210], fill=WHITE, outline=RULE, width=2)
        hero["art"](d, x + 1, hy + 1, hw - 2, 84)
        d.rectangle([x + 1, hy + 85, x + hw - 1, hy + 88], fill=col)
        sp_text(d, (x + 12, hy + 96), f'{hero["n"]} · {hero["kick"]}', f_kick, col, spacing=1)
        yy = para(d, (x + 12, hy + 112), hero["head"], f_hero_h, INK, hw - 24, 21)
        para(d, (x + 12, yy + 4), hero["body"], f_hero_b, MUTED, hw - 24, 16)

    # ---- numbered story grid ----
    gy = 444
    gw = (1000 - 24 - 30) // 4
    gh = 100
    for i, (region, head) in enumerate(GRID):
        x = 24 + (i % 4) * (gw + 10)
        y = gy + (i // 4) * (gh + 8)
        col = REGION[region]
        d.rectangle([x, y, x + gw, y + gh], fill=WHITE, outline=RULE, width=2)
        d.rectangle([x + 1, y + 1, x + gw - 1, y + 5], fill=col)
        d.ellipse([x + 10, y + 12, x + 28, y + 30], fill=col)
        num = str(i + 4)
        d.text((x + 19 - d.textlength(num, font=f_gn) / 2, y + 16), num, font=f_gn, fill=WHITE)
        sp_text(d, (x + 36, y + 14), region, f_gn, col, spacing=1)
        para(d, (x + 10, y + 38), head, f_gh, INK, gw - 20, 16)

    # ---- also on the day ----
    by = 748
    rule(d, by, 24, 1000, INK, 2)
    sp_text(d, (24, by + 8), "ALSO ON THURSDAY 19 NOVEMBER", f_kick, INK, spacing=2)
    for i, txt in enumerate(BRIEFS):
        x = 24 + (i % 2) * 494
        y = by + 32 + (i // 2) * 21
        d.text((x, y - 1), str(i + 16).rjust(2, "0"), font=font(BOLD, 10), fill=RED)
        d.text((x + 24, y), txt, font=f_brief_b, fill=(70, 70, 74))

    # ---- foot ----
    fy = 952
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
