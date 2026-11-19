#!/usr/bin/env python3
"""Draws the make.fun news-image entry for Thursday, 19 November 2026.

The page is a newspaper front page: a masthead naming the day, a red strap
line, a lead story with the three leaders' flags, a grid of the day's other
stories, a strip of the day's numbers, a row of briefs from the rest of the
world, and a late-edition footer. Flat colour and one clear type scale keep
it readable when it is scaled down to about 300 pixels wide.

Every fact on the page comes from reports published on 19 November 2026.

Run:  python tools/make_entry.py  ->  entry.png
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 233)
INK = (20, 24, 29)
RED = (176, 42, 36)
MUTED = (104, 104, 104)
RULE = (196, 188, 174)

FONT_DIR = r"C:\Windows\Fonts"
DISPLAY = os.path.join(FONT_DIR, "georgiab.ttf")
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
REG = os.path.join(FONT_DIR, "arial.ttf")
ITALIC = os.path.join(FONT_DIR, "ariali.ttf")

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def sp_text(draw, xy, s, f, fill, spacing=2):
    """Letter-spaced small caps-ish text, drawn letter by letter."""
    x, y = xy
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
    for k in range(4):
        a = math.radians(20 + k * 30)
        px, py = sx + math.cos(a) * h * 0.26, sy + math.sin(a) * h * 0.26
        pr = h * 0.06
        d.polygon([(px, py - pr), (px + pr * 0.9, py + pr * 0.55), (px - pr * 0.9, py + pr * 0.55)],
                  fill=(252, 222, 72))


def flag_ru(d, x, y, w, h):
    for s, col in enumerate(((238, 238, 238), (44, 70, 148), (199, 42, 48))):
        d.rectangle([x, y + s * h / 3, x + w, y + (s + 1) * h / 3], fill=col)


def flags_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    fw, fh = w * 0.235, h * 0.40
    gap = w * 0.045
    total = fw * 3 + gap * 2
    fx = x + (w - total) / 2
    fy = y + h * 0.20
    flag_us(d, fx, fy, fw, fh)
    flag_cn(d, fx + fw + gap, fy, fw, fh)
    flag_ru(d, fx + 2 * (fw + gap), fy, fw, fh)
    names = ("USA", "CHINA", "RUSSIA")
    small = font(BOLD, 13)
    for i, nm in enumerate(names):
        nx = fx + i * (fw + gap)
        d.text((nx + fw / 2 - d.textlength(nm, font=small) / 2, fy + fh + 10), nm, font=small, fill=INK)
    cap = font(BOLD, 15)
    line = "FIRST TRILATERAL - NO PRECEDENT"
    d.text((x + (w - d.textlength(line, font=cap)) / 2, y + h - 32), line, font=cap, fill=RED)


# ---------------------------------------------------------------- icons ----

def icon_drone(d, x, y, s, color=RED):
    """A quadcopter: the Iranian drones over the US base in Kuwait."""
    cx, cy = x + s * 0.5, y + s * 0.44
    r = s * 0.26
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * r * 0.92, cy + sy * r * 0.68
        d.line([cx, cy, ax, ay], fill=color, width=7)
        d.ellipse([ax - r * 0.42, ay - r * 0.16, ax + r * 0.42, ay + r * 0.16], fill=color)
    d.rounded_rectangle([cx - r * 0.40, cy - r * 0.26, cx + r * 0.40, cy + r * 0.34],
                        radius=r * 0.12, fill=color)
    d.polygon([(cx - r * 0.30, cy + r * 0.90), (cx, cy + r * 1.60), (cx + r * 0.30, cy + r * 0.90)],
              fill=(214, 118, 30))


def icon_bridge(d, x, y, s, color=INK):
    """The Kerch bridge: a span that has been struck."""
    w = s * 0.9
    x0 = x + (s - w) / 2
    y0 = y + s * 0.30
    y1 = y + s * 0.78
    d.rectangle([x0, y0, x0 + w, y0 + 9], fill=color)
    for i in range(5):
        px = x0 + i * (w / 5) + w / 10
        d.line([px, y0, px, y1], fill=(120, 118, 112), width=4)
    d.rectangle([x0, y1, x0 + w, y1 + 8], fill=color)
    # the broken span
    d.rectangle([x0 + w * 0.40, y0, x0 + w * 0.62, y1], fill=PAPER)
    d.line([x0 + w * 0.40, y0, x0 + w * 0.34, y0 + s * 0.22], fill=RED, width=5)
    d.line([x0 + w * 0.62, y0, x0 + w * 0.70, y0 + s * 0.30], fill=RED, width=5)
    d.polygon([(x0 + w * 0.50, y0 - s * 0.08), (x0 + w * 0.56, y0 + s * 0.06),
               (x0 + w * 0.44, y0 + s * 0.06)], fill=RED)


def icon_court(d, x, y, s, color=INK):
    """The world court and its scales."""
    cx = x + s * 0.5
    base = y + s * 0.80
    top = y + s * 0.22
    d.line([cx, top, cx, base], fill=color, width=5)
    d.line([cx - s * 0.34, top + s * 0.14, cx + s * 0.34, top + s * 0.14], fill=color, width=5)
    d.rectangle([cx - s * 0.26, base, cx + s * 0.26, base + s * 0.07], fill=color)
    for sx in (-1, 1):
        bx = cx + sx * s * 0.34
        d.line([bx, top + s * 0.14, bx, top + s * 0.40], fill=color, width=3)
        d.polygon([(bx - s * 0.14, top + s * 0.40), (bx + s * 0.14, top + s * 0.40),
                   (bx, top + s * 0.56)], fill=(196, 150, 60))


def icon_ipo(d, x, y, s, color=(34, 84, 160)):
    """Rising bars and an arrow: Anthropic's Nasdaq debut."""
    base = y + s * 0.80
    bw = s * 0.15
    heights = (s * 0.24, s * 0.38, s * 0.54)
    for i, hh in enumerate(heights):
        bx = x + s * 0.12 + i * bw * 1.5
        d.rectangle([bx, base - hh, bx + bw, base], fill=color)
    d.rectangle([x + s * 0.06, base, x + s * 0.92, base + 6], fill=INK)
    ax, ay = x + s * 0.74, y + s * 0.34
    d.line([ax - s * 0.14, ay + s * 0.16, ax, ay], fill=RED, width=6)
    d.polygon([(ax, ay - s * 0.07), (ax + s * 0.12, ay + s * 0.04), (ax - s * 0.05, ay + s * 0.12)],
              fill=RED)


def icon_game(d, x, y, s, color=(60, 140, 90)):
    """A controller: GTA VI launches today."""
    cx, cy = x + s * 0.5, y + s * 0.52
    w, h = s * 0.76, s * 0.40
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h * 0.45, fill=color)
    d.ellipse([cx - w * 0.30, cy - h * 0.22, cx - w * 0.16, cy - h * 0.08], fill=PAPER)
    d.rectangle([cx - w * 0.21, cy - h * 0.27, cx - w * 0.15, cy + h * 0.07], fill=PAPER)
    for dx, dy in ((w * 0.16, -h * 0.20), (w * 0.26, -h * 0.10), (w * 0.26, h * 0.10), (w * 0.16, h * 0.20)):
        d.ellipse([cx + dx - s * 0.035, cy + dy - s * 0.035, cx + dx + s * 0.035, cy + dy + s * 0.035],
                  fill=(226, 226, 220))


def icon_painting(d, x, y, s, color=(150, 60, 40)):
    """A canvas on an easel: the Van Gogh auction record."""
    fw, fh = s * 0.60, s * 0.48
    fx, fy = x + s * 0.20, y + s * 0.16
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(246, 240, 222), outline=INK, width=3)
    d.polygon([(fx + fw * 0.12, fy + fh * 0.82), (fx + fw * 0.36, fy + fh * 0.36),
               (fx + fw * 0.54, fy + fh * 0.66), (fx + fw * 0.70, fy + fh * 0.44),
               (fx + fw * 0.90, fy + fh * 0.82)], fill=color)
    d.rectangle([fx + fw * 0.06, fy + fh * 0.16, fx + fw * 0.20, fy + fh * 0.34], fill=(226, 196, 92))
    d.line([fx + fw * 0.50, fy + fh, fx + fw * 0.44, y + s * 0.92], fill=INK, width=4)
    d.line([fx + fw * 0.52, fy + fh, fx + fw * 0.60, y + s * 0.92], fill=INK, width=4)
    d.rectangle([fx + fw * 0.30, y + s * 0.88, fx + fw * 0.74, y + s * 0.94], fill=INK)
    d.polygon([(fx + fw * 0.80, fy - s * 0.02), (fx + fw * 0.98, fy + s * 0.10),
               (fx + fw * 0.80, fy + s * 0.16)], fill=RED)


# --------------------------------------------------------------- content ---

LEAD = dict(
    kicker="SHENZHEN · APEC SUMMIT",
    head="THE BIG THREE MEET",
    head2="IN SHENZHEN",
    body=("Trump, Xi and Putin sat down for the first three-way summit of the three, "
          "at the APEC summit in China's tech capital: nuclear arms control, Ukraine and "
          "Iran on the table, with Europe and Ukraine kept out of the room."),
)

STORIES = [
    dict(kicker="GULF ON THE BRINK", head="IRAN DRONES HIT US BASE IN KUWAIT",
         body="Ali Al-Salem base hit after a US raid on Qeshm",
         icon=icon_drone, color=RED),
    dict(kicker="BRIDGE DOWN", head="KERCH BRIDGE HIT A THIRD TIME",
         body="Rail traffic stopped on the Crimea link",
         icon=icon_bridge, color=INK),
    dict(kicker="GENOCIDE VERDICT", head="WORLD COURT RULES ON MYANMAR",
         body="Top court delivers its verdict in the Rohingya case",
         icon=icon_court, color=INK),
    dict(kicker="AI · WALL STREET", head="ANTHROPIC IPO: $1 TRILLION",
         body="The Claude maker starts trading on the Nasdaq today",
         icon=icon_ipo, color=(34, 84, 160)),
    dict(kicker="GAMERS' MIDNIGHT", head="GTA VI LAUNCHES TO A RECORD",
         body="An estimated $1.5bn of pre-orders, the biggest ever",
         icon=icon_game, color=(60, 140, 90)),
    dict(kicker="ART RECORD", head="VAN GOGH FETCHES $190.4M",
         body="'Chestnut Trees in Blossom' sells at Sotheby's",
         icon=icon_painting, color=(150, 60, 40)),
]

NUMBERS = [
    ("3", "leaders in Shenzhen, a first"),
    ("$1.5bn", "GTA VI pre-orders"),
    ("$190m", "Van Gogh auction"),
    ("1", "light-day: Voyager 1"),
    ("4,595", "killed in Haiti this year"),
]

BRIEFS = [
    ("EUROPE", "Berlin coalition summit on Ukraine; the UK pledges long-range missiles, the EU a 45bn euro loan"),
    ("ISRAEL · GAZA", "Israeli forces push into central Gaza; Lebanon is struck again"),
    ("CONGO", "Ebola reaches Watsa: 11,432 cases and 5,593 deaths, WHO says"),
    ("UNITED STATES", "Jeffries is named House Speaker, the first Black one; Democrats take the Senate 56-44"),
    ("INDIA", "Cyclone Akvan closes in on the Andhra Pradesh and Odisha coasts"),
    ("HEALTH", "The US loses its measles-free status as Pennsylvania counts an eighth death"),
]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(DISPLAY, 46)
    f_mast_small = font(REG, 16)
    f_kicker = font(BOLD, 13)
    f_lead = font(BOLD, 42)
    f_lead2 = font(BOLD, 42)
    f_body = font(REG, 15)
    f_card_body = font(REG, 14)
    f_head = font(BOLD, 19)
    f_kick_s = font(BOLD, 12)
    f_num = font(BOLD, 30)
    f_numb = font(REG, 12)
    f_brief_h = font(BOLD, 13)
    f_brief_b = font(REG, 12)
    f_foot = font(REG, 13)

    # ---- masthead ----
    d.text((24, 18), "THE WORLD TODAY", font=f_mast, fill=INK)
    right = "One day, one page"
    d.text((1000 - d.textlength(right, font=f_mast_small), 20), right, font=f_mast_small, fill=MUTED)
    date = "Thursday 19 November 2026"
    d.text((1000 - d.textlength(date, font=font(BOLD, 18)), 42), date, font=font(BOLD, 18), fill=INK)
    rule(d, 84, 24, 1000, INK, 3)

    # ---- strap line ----
    strap = "SHENZHEN SUMMIT · GULF ON FIRE · BRIDGE DOWN · GENOCIDE VERDICT · RECORD IPO · RECORD ART"
    sp_text(d, (24, 94), strap, f_kick_s, RED, spacing=1)
    rule(d, 118, 24, 1000, RULE, 2)

    # ---- lead story ----
    y = 134
    sp_text(d, (24, y), LEAD["kicker"], f_kicker, RED, spacing=2)
    d.text((24, y + 22), LEAD["head"], font=f_lead, fill=INK)
    d.text((24, y + 68), LEAD["head2"], font=f_lead2, fill=INK)
    para(d, (24, y + 126), LEAD["body"], f_body, (60, 62, 66), 600, 20)
    flags_panel(d, 660, y + 10, 340, 170)

    # ---- story grid ----
    gy = 340
    gw = (1000 - 24 - 2 * 20) // 3
    for i, st in enumerate(STORIES):
        cx = 24 + (i % 3) * (gw + 20)
        cy = gy + (i // 3) * 168
        d.rectangle([cx, cy, cx + gw, cy + 152], fill=(255, 255, 255), outline=RULE, width=2)
        st["icon"](d, cx + 16, cy + 22, 66, st["color"])
        sp_text(d, (cx + 100, cy + 20), st["kicker"], f_kick_s, st["color"], spacing=1)
        y2 = para(d, (cx + 100, cy + 40), st["head"], f_head, INK, gw - 116, 22)
        para(d, (cx + 100, y2 + 4), st["body"], f_card_body, MUTED, gw - 116, 16)

    # ---- the day in numbers ----
    ny = 690
    rule(d, ny, 24, 1000, INK, 2)
    sp_text(d, (24, ny + 10), "THE DAY IN NUMBERS", f_kicker, INK, spacing=2)
    ny += 34
    colw = (1000 - 24) // 5
    for i, (n, lab) in enumerate(NUMBERS):
        x = 24 + i * colw
        d.text((x, ny), n, font=f_num, fill=RED)
        para(d, (x, ny + 36), lab, f_numb, MUTED, colw - 24, 15)
        if i:
            d.rectangle([x - 12, ny + 2, x - 10, ny + 52], fill=RULE)
    ny += 76
    rule(d, ny, 24, 1000, INK, 2)

    # ---- briefs from the rest of the world ----
    by = ny + 12
    for i, (tag, txt) in enumerate(BRIEFS):
        cx = 24 + (i % 2) * 498
        cy = by + (i // 2) * 52
        d.ellipse([cx, cy + 5, cx + 9, cy + 14], fill=RED)
        sp_text(d, (cx + 18, cy), tag, f_brief_h, INK, spacing=1)
        para(d, (cx + 18, cy + 17), txt, f_brief_b, MUTED, 456, 15)

    # ---- footer ----
    fy2 = H - 42
    rule(d, fy2, 24, 1000, INK, 2)
    d.text((24, fy2 + 10), "LATE EDITION", font=font(BOLD, 14), fill=RED)
    right = "All the world, one page · 19.11.2026"
    d.text((1000 - d.textlength(right, font=f_foot), fy2 + 11), right, font=f_foot, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
