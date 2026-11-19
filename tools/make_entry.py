#!/usr/bin/env python3
"""Draws the make.fun news-image entry for Thursday, 19 November 2026.

The image is a front page: a masthead naming the day, six cards for the
day's stories (one region each, an icon and a short headline), and a ticker
of the smaller stories of the same day. Everything is flat colour and clear
type so it still reads when it is scaled down to about 300 pixels wide.

Run:  python tools/make_entry.py  ->  entry.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
INK = (16, 21, 28)
PAPER = (244, 241, 233)
CARD = (255, 255, 255)
RULE = (206, 199, 186)
MUTED = (92, 98, 108)

FONT_DIR = r"C:\Windows\Fonts"
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
REG = os.path.join(FONT_DIR, "arial.ttf")
SERIF_B = os.path.join(FONT_DIR, "georgiab.ttf")

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill):
    draw.text(xy, s, font=f, fill=fill)


def sp_text(draw, xy, s, f, fill, spacing=2):
    """Letter-spaced text, drawn letter by letter."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + spacing
    return x


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
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


# ---------------------------------------------------------------- icons ----

def icon_summit(d, box, c):
    """Three national flags beside a globe: Trump, Xi and Putin."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.5, y0 + h * 0.30
    r = min(w, h) * 0.20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=4)
    d.ellipse([cx - r * 0.42, cy - r, cx + r * 0.42, cy + r], outline=c, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=c, width=3)
    # three flags under the globe
    fw, fh, gap = w * 0.26, h * 0.18, w * 0.07
    fx = cx - (fw * 3 + gap * 2) / 2
    fy = cy + r + h * 0.16
    for i in range(3):
        x = fx + i * (fw + gap)
        if i == 0:  # United States: red and white stripes, blue corner
            for s in range(7):
                if s % 2 == 0:
                    d.rectangle([x, fy + s * fh / 7, x + fw, fy + (s + 1) * fh / 7], fill=(198, 42, 45))
            d.rectangle([x, fy, x + fw * 0.5, fy + fh * 0.55], fill=(38, 60, 122))
        elif i == 1:  # China: red with a star
            d.rectangle([x, fy, x + fw, fy + fh], fill=(211, 47, 47))
            sx, sy, sr = x + fw * 0.28, fy + fh * 0.34, fh * 0.17
            d.polygon([(sx, sy - sr), (sx + sr * 0.87, sy + sr * 0.5), (sx - sr * 0.87, sy + sr * 0.5)],
                      fill=(255, 221, 72))
        else:  # Russia: white, blue, red
            for s, col in enumerate(((255, 255, 255), (40, 68, 148), (200, 40, 45))):
                d.rectangle([x, fy + s * fh / 3, x + fw, fy + (s + 1) * fh / 3], fill=col)
        d.rectangle([x, fy, x + fw, fy + fh], outline=INK, width=2)


def icon_iran(d, box, c):
    """A quadcopter drone over a flame: Iran drones hit a US base in Kuwait."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.5, y0 + h * 0.40
    r = min(w, h) * 0.26
    # four arms and rotors
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * r * 0.95, cy + sy * r * 0.72
        d.line([cx, cy, ax, ay], fill=c, width=5)
        d.ellipse([ax - r * 0.42, ay - r * 0.18, ax + r * 0.42, ay + r * 0.18], outline=c, width=4)
    d.rounded_rectangle([cx - r * 0.42, cy - r * 0.30, cx + r * 0.42, cy + r * 0.34],
                        radius=r * 0.12, fill=c)
    d.ellipse([cx - r * 0.16, cy + r * 0.30, cx + r * 0.16, cy + r * 0.56], fill=c)
    # flame beneath
    d.polygon([(cx - r * 0.34, cy + r * 1.05), (cx, cy + r * 1.85),
               (cx + r * 0.34, cy + r * 1.05)], fill=(226, 118, 32))


def icon_ipo(d, box, c):
    """Rising bars and an upward arrow: Anthropic lists on the Nasdaq."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    base = y0 + h * 0.82
    r = min(w, h) * 0.22
    bw = w * 0.14
    heights = [h * 0.26, h * 0.40, h * 0.56]
    for i, hh in enumerate(heights):
        x = x0 + w * 0.10 + i * (bw * 1.55)
        d.rectangle([x, base - hh, x + bw, base], fill=c)
    d.line([x0 + w * 0.08, base + 3, x0 + w * 0.92, base + 3], fill=INK, width=4)
    # arrow over the bars
    ax, ay = x0 + w * 0.72, y0 + h * 0.30
    d.line([ax - r * 0.9, ay + r * 0.9, ax, ay], fill=(226, 118, 32), width=7)
    d.polygon([(ax, ay - r * 0.28), (ax + r * 0.30, ay + r * 0.06), (ax - r * 0.14, ay + r * 0.26)],
              fill=(226, 118, 32))


def icon_ebola(d, box, c):
    """A virus particle with spikes: Ebola spreads in DR Congo."""
    x0, y0, x1, y1 = box
    cx, cy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.48
    r = min(x1 - x0, y1 - y0) * 0.24
    import math
    for k in range(12):
        a = k * math.pi / 6
        ex, ey = cx + math.cos(a) * r * 1.55, cy + math.sin(a) * r * 1.55
        d.line([cx + math.cos(a) * r, cy + math.sin(a) * r, ex, ey], fill=c, width=4)
        d.ellipse([ex - r * 0.16, ey - r * 0.16, ex + r * 0.16, ey + r * 0.16], fill=c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=PAPER)


def icon_gaza(d, box, c):
    """A tent among rubble under smoke: displaced Palestinians in Gaza."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = x0 + w * 0.44
    base = y0 + h * 0.88
    # rubble at the foot
    for dx, dy, s in ((-0.32, -0.09, 0.14), (-0.14, -0.02, 0.11), (0.30, -0.05, 0.12)):
        rx, ry, rs = cx + w * dx, base + h * dy, w * s
        d.rectangle([rx, ry, rx + rs, ry + rs * 0.62], fill=(126, 122, 116),
                    outline=(96, 92, 86), width=2)
    # tent
    tw, th = w * 0.58, h * 0.50
    tx, ty = cx - tw / 2, base - th - h * 0.03
    d.polygon([(tx, ty + th), (tx + tw / 2, ty), (tx + tw, ty + th)], fill=(240, 237, 229))
    d.polygon([(tx, ty + th), (tx + tw / 2, ty), (tx + tw / 2, ty + th)], fill=(214, 210, 199))
    d.polygon([(tx + tw / 2 - tw * 0.15, ty + th), (tx + tw / 2, ty + th * 0.34),
               (tx + tw / 2 + tw * 0.15, ty + th)], fill=(46, 48, 54))
    d.line([tx - 3, ty + th, tx + tw + 3, ty + th], fill=(96, 92, 86), width=3)
    # smoke curling up on the right
    for sxx, syy, r in ((0.26, 0.30, 0.10), (0.34, 0.10, 0.13), (0.28, -0.10, 0.09)):
        sx, sy, sr = cx + w * sxx, ty + h * syy, w * r
        d.ellipse([sx - sr, sy - sr * 0.7, sx + sr, sy + sr * 0.7], fill=(178, 174, 168))
    # flame
    d.polygon([(cx + w * 0.26, base - h * 0.34), (cx + w * 0.20, base - h * 0.12),
               (cx + w * 0.33, base - h * 0.12)], fill=(214, 88, 40))


def icon_berlin(d, box, c):
    """A blue and yellow flag beside EU stars: Europe's summit on Ukraine."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # flag on a pole
    fx, fy = x0 + w * 0.10, y0 + h * 0.18
    fw, fh = w * 0.50, h * 0.44
    d.line([fx, fy - h * 0.06, fx, fy + fh + h * 0.06], fill=(90, 96, 104), width=5)
    d.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh / 2], fill=(46, 96, 196))
    d.rectangle([fx + 3, fy + fh / 2, fx + 3 + fw, fy + fh], fill=(250, 208, 58))
    d.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh], outline=(120, 126, 134), width=2)
    # circle of stars: Europe acting together
    ccx, ccy = x0 + w * 0.76, y0 + h * 0.50
    rr = min(w, h) * 0.27
    d.ellipse([ccx - rr, ccy - rr, ccx + rr, ccy + rr], fill=(30, 62, 132))
    import math
    for k in range(8):
        a = -math.pi / 2 + k * 2 * math.pi / 8
        sx, sy = ccx + math.cos(a) * rr * 0.58, ccy + math.sin(a) * rr * 0.58
        sr = rr * 0.16
        d.polygon([(sx, sy - sr), (sx + sr * 0.87, sy + sr * 0.5), (sx - sr * 0.87, sy + sr * 0.5)],
                  fill=(252, 209, 58))


# --------------------------------------------------------------- content ---

STORIES = [
    dict(tag="CHINA · APEC SUMMIT", color=(196, 44, 44), head="TRUMP, XI AND PUTIN MEET",
         sub="First trilateral summit of the three, in Shenzhen",
         icon=icon_summit),
    dict(tag="MIDDLE EAST", color=(200, 96, 24), head="IRAN DRONES HIT US BASE IN KUWAIT",
         sub="Retaliation after a US raid on Qeshm island",
         icon=icon_iran),
    dict(tag="AI · WALL STREET", color=(36, 96, 176), head="ANTHROPIC DEBUTS, WORTH $1 TRILLION",
         sub="Priced at $83 a share; chip and AI stocks swing",
         icon=icon_ipo),
    dict(tag="CONGO · HEALTH", color=(124, 62, 152), head="EBOLA SPREADS IN DR CONGO",
         sub="11,432 cases and 5,593 deaths, WHO says",
         icon=icon_ebola),
    dict(tag="ISRAEL · GAZA", color=(150, 40, 48), head="ISRAEL PUSHES INTO CENTRAL GAZA",
         sub="Ceasefire holds but cracks; Lebanon also struck",
         icon=icon_gaza),
    dict(tag="EUROPE · UKRAINE", color=(30, 110, 60), head="BERLIN SUMMIT ON UKRAINE",
         sub="Europe's coalition meets; EU plans a 45bn euro loan",
         icon=icon_berlin),
]

TICKER = [
    "WORLD COURT VERDICT IN MYANMAR GENOCIDE CASE",
    "US LOSES MEASLES-FREE STATUS",
    "HAITI: UN COUNTS 4,595 KILLED IN 2026",
    "FED MINUTES SHOW INFLATION UNEASE",
    "DEMOCRATS TAKE THE SENATE, 56-44",
    "ISRAEL STRIKES SOUTH LEBANON",
]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_eyebrow = font(REG, 19)
    f_date = font(SERIF_B if os.path.exists(SERIF_B) else BOLD, 54)
    f_date_small = font(BOLD, 24)
    f_tag = font(BOLD, 13)
    f_head = font(BOLD, 25)
    f_sub = font(REG, 16)
    f_tick = font(BOLD, 14)

    # ---- masthead ----
    d.rectangle([0, 0, W, 140], fill=INK)
    d.rectangle([0, 140, W, 145], fill=(214, 160, 40))
    sp_text(d, (20, 18), "THE WORLD'S NEWS IN ONE IMAGE", f_eyebrow, (198, 204, 212), spacing=3)
    d.text((20, 44), "THURSDAY, 19 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    d.text((20, 104), "Six stories that made the day, and what else happened on it",
           font=f_date_small, fill=(214, 160, 40))
    d.text((W - 210, 20), "make.fun · news-image", font=font(REG, 14), fill=(140, 148, 158))

    # ---- cards ----
    top, gap, m = 164, 20, 18
    card_w = (W - 2 * m - gap) // 2
    card_h = 224
    for i, st in enumerate(STORIES):
        cx = m + (i % 2) * (card_w + gap)
        cy = top + (i // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD, outline=RULE, width=2)
        d.rectangle([cx, cy, cx + 8, cy + card_h], fill=st["color"])
        st["icon"](d, (cx + 22, cy + 34, cx + 148, cy + 182), st["color"])
        tx = cx + 166
        sp_text(d, (tx, cy + 26), st["tag"], f_tag, st["color"], spacing=1)
        y = para(d, (tx, cy + 52), st["head"], f_head, INK, card_w - 168 - 20, 29)
        para(d, (tx, y + 6), st["sub"], f_sub, MUTED, card_w - 168 - 20, 20)

    # ---- ticker ----
    ty = H - 128
    d.rectangle([0, ty, W, H], fill=INK)
    d.rectangle([0, ty, W, ty + 4], fill=(214, 160, 40))
    sp_text(d, (20, ty + 16), "ALSO ON 19 NOVEMBER", f_tag, (214, 160, 40), spacing=2)
    for i, t in enumerate(TICKER):
        col = i % 2
        row = i // 2
        x = 20 + col * (W // 2 - 10)
        y = ty + 42 + row * 26
        d.ellipse([x, y + 6, x + 8, y + 14], fill=(214, 160, 40))
        d.text((x + 18, y), t, font=f_tick, fill=(226, 230, 236))
    d.text((W - 200, H - 22), "one image · one day · 19.11.2026", font=font(REG, 13), fill=(150, 158, 168))

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
