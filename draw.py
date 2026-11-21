#!/usr/bin/env python3
"""Draw a fresh front page for 21 November 2026 — THE WORLD TODAY, new edition.

A different composition from the first entry: the Shenzhen summit leads,
with the world-court ruling and the market sell-off stacked in a right-hand
sidebar, and the Kyiv barrage plus the cancer-pill trial in a bottom band.
Every story was reported on Saturday 21 November 2026, verified against
several news sources (see README.md).

Run:  python3 draw.py
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width
LEAD_W = 600                # lead column width
SIDE_X = M + LEAD_W + 28    # sidebar x
SIDE_W = W - M - SIDE_X     # sidebar width

PAPER = (246, 241, 231)
INK = (22, 21, 19)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREY = (90, 86, 78)
GOLD = (212, 175, 55)
NAVY = (16, 32, 64)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns lines that fit inside max_w."""
    out, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def lines(d, text_lines, x, y, font, fill, leading=None):
    """Draw text lines from (x, y); return the y just below the block."""
    if leading is None:
        leading = int(font.size * 1.22)
    for ln in text_lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def hrule(d, x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def blend(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1):
        d.line([(x0, yy), (x1, yy)],
               fill=blend(top, bottom, (yy - y0) / max(1, y1 - y0)))


def draw_shenzhen(d, box):
    """Dusk over Shenzhen: tapered tower, skyline, three summit flags."""
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    panel = Image.new("RGB", (pw, ph), (0, 0, 0))
    pd = ImageDraw.Draw(panel)
    rng = random.Random(20261121)
    vgrad(pd, (0, 0, pw, ph), (26, 30, 78), (216, 118, 64))
    # low sun
    pd.ellipse([pw - 150, 14, pw - 106, 58], fill=(255, 226, 160))
    pd.ellipse([pw - 144, 20, pw - 112, 52], fill=(255, 240, 200))
    # stars fading in at the top
    for _ in range(40):
        sx, sy = rng.randint(4, pw - 4), rng.randint(4, 46)
        r = rng.choice([1, 1, 2])
        pd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 238, 250))
    base = ph - 46
    # tapered Ping An-style tower, left of centre
    tx = 96
    pd.polygon([(tx, 26), (tx + 26, 26), (tx + 34, base), (tx - 8, base)],
               fill=(14, 14, 30))
    pd.line([(tx + 13, 8), (tx + 13, 26)], fill=(14, 14, 30), width=3)
    for wy in range(38, base - 6, 14):
        pd.rectangle([tx + 4, wy, tx + 22, wy + 3], fill=(255, 209, 102))
    # the rest of the skyline
    x = 150
    while x < pw:
        bw = rng.randint(30, 58)
        bh = rng.randint(44, 108)
        pd.rectangle([x, base - bh, min(x + bw, pw), base], fill=(14, 14, 30))
        for _ in range(bh // 16):
            wx = rng.randint(x + 4, min(x + bw - 6, pw - 6))
            wy = rng.randint(base - bh + 6, base - 8)
            pd.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 209, 102))
        x += bw + rng.randint(3, 10)
    # ground band
    pd.rectangle([0, base, pw, ph], fill=(20, 18, 34))
    # three flags on poles, in front of the skyline
    def flag(px, kind):
        pd.line([(px, 52), (px, base)], fill=(220, 220, 210), width=3)
        fx, fy, fw, fh = px + 3, 56, 62, 38
        if kind == "us":
            for i in range(7):
                pd.rectangle([fx, fy + i * 6, fx + fw, fy + (i + 1) * 6],
                             fill=(178, 34, 52) if i % 2 == 0 else (245, 245, 240))
            pd.rectangle([fx, fy, fx + 26, fy + 20], fill=(28, 44, 96))
            for sy in (fy + 5, fy + 11, fy + 17):
                for sx in (fx + 5, fx + 13, fx + 21):
                    pd.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        elif kind == "cn":
            pd.rectangle([fx, fy, fx + fw, fy + fh], fill=(206, 32, 40))
            pd.ellipse([fx + 8, fy + 7, fx + 20, fy + 19], fill=(255, 222, 80))
            for (sx, sy) in [(fx + 26, fy + 6), (fx + 32, fy + 12),
                             (fx + 30, fy + 20), (fx + 24, fy + 16)]:
                pd.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 222, 80))
        else:
            pd.rectangle([fx, fy, fx + fw, fy + 13], fill=(245, 245, 240))
            pd.rectangle([fx, fy + 13, fx + fw, fy + 26], fill=(28, 70, 170))
            pd.rectangle([fx, fy + 26, fx + fw, fy + fh], fill=(206, 32, 40))
    flag(36, "us")
    flag(268, "cn")
    flag(500, "ru")
    # caption strip
    pd.rectangle([0, ph - 24, pw, ph], fill=(14, 14, 30))
    pd.text((10, ph - 21), "SHENZHEN, CHINA — THE FIRST THREE-WAY SUMMIT",
            font=fnt(SANS_B, 13), fill=(255, 255, 255))
    d._image.paste(panel, (x0, y0))


def draw_scales(d, box):
    """Scales of justice on navy: the world court in The Hague."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=NAVY)
    cx, cy = x0 + 62, y0 + 42
    # post, beam, pans
    d.line([(cx, cy - 26), (cx, cy + 26)], fill=GOLD, width=4)
    d.line([(cx - 34, cy - 22), (cx + 34, cy - 22)], fill=GOLD, width=4)
    d.ellipse([cx - 4, cy - 30, cx + 4, cy - 22], fill=GOLD)
    for sgn in (-1, 1):
        px = cx + sgn * 34
        d.line([(px, cy - 22), (px - 12, cy + 2)], fill=GOLD, width=2)
        d.line([(px, cy - 22), (px + 12, cy + 2)], fill=GOLD, width=2)
        d.arc([px - 12, cy - 2, px + 12, cy + 14], 0, 180, fill=GOLD, width=3)
    d.line([(cx - 16, cy + 26), (cx + 16, cy + 26)], fill=GOLD, width=4)
    d.text((x0 + 118, y0 + 22), "WORLD", font=fnt(SANS_B, 26), fill=(255, 255, 255))
    d.text((x0 + 118, y0 + 50), "COURT", font=fnt(SANS_B, 26), fill=(255, 255, 255))
    d.text((x1 - 10, y1 - 20), "THE HAGUE", font=fnt(SANS_B, 11),
           fill=(170, 185, 210), anchor="ra")


def draw_candles(d, box):
    """Falling candlesticks: the day's market rout, in red."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 253, 246))
    for gy in range(y0 + 14, y1 - 6, 16):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(232, 228, 218), width=1)
    # six candles, each lower than the last (kept clear of the footline
    # and of the -3.7% label at the right)
    closes = [12, 18, 16, 26, 32, 40]
    cw, gap = 22, 10
    x = x0 + 12
    for i, cl in enumerate(closes):
        top = y0 + cl
        bot = top + 14
        d.line([(x + cw // 2, top - 6), (x + cw // 2, bot + 6)], fill=RED, width=2)
        d.rectangle([x, top, x + cw, bot], fill=RED)
        x += cw + gap
    d.text((x1 - 96, y0 + 6), "-3.7%", font=fnt(SANS_B, 30), fill=RED)
    d.text((x1 - 96, y0 + 42), "S&P 500", font=fnt(SANS_B, 14), fill=INK)
    d.text((x0 + 12, y1 - 20), "NASDAQ -5.3%  •  NIKKEI -5.1%",
           font=fnt(SANS_B, 13), fill=GREY)


def draw_map(d, box):
    """Abstract map: a burst over Kyiv, an arrow into Poland."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 38, 66))
    for gx in range(x0 + 40, x1, 40):
        d.line([(gx, y0), (gx, y1)], fill=(38, 56, 88), width=1)
    for gy in range(y0 + 20, y1, 20):
        d.line([(x0, gy), (x1, gy)], fill=(38, 56, 88), width=1)
    # landmass hint
    d.polygon([(x0 + 30, y1 - 8), (x0 + 120, y0 + 18), (x0 + 260, y0 + 8),
               (x0 + 380, y0 + 30), (x1 - 20, y0 + 44), (x1 - 8, y1 - 8)],
              fill=(52, 74, 106))
    # Kyiv burst
    kx, ky = x0 + 250, y0 + 52
    for r, col in [(26, (232, 110, 30)), (17, (245, 165, 55)), (9, (255, 215, 110))]:
        d.ellipse([kx - r, ky - r, kx + r, ky + r], fill=col)
    d.text((kx, ky - 40), "KYIV", font=fnt(SANS_B, 15), fill=(255, 255, 255),
           anchor="ma")
    # arrow into Poland
    px, py = x0 + 96, y0 + 30
    d.line([(kx - 30, ky - 12), (px + 18, py + 8)], fill=(255, 214, 120), width=3)
    d.polygon([(px + 18, py + 8), (px + 2, py + 2), (px + 6, py + 16)],
              fill=(255, 214, 120))
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255))
    d.text((px, py - 24), "POLAND", font=fnt(SANS_B, 15), fill=(255, 255, 255),
           anchor="ma")
    d.text((x1 - 10, y1 - 20), "2 MISSILES LAND IN POLAND",
           font=fnt(SANS_B, 11), fill=(180, 195, 220), anchor="ra")


def draw_pill(d, box):
    """A capsule and a '1 in 12' badge: the pancreatic-cancer trial."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 244, 238))
    # capsule, diagonal, two halves: teal left, white right
    cx, cy = x0 + 120, y0 + 44
    d.rectangle([cx - 30, cy - 22, cx + 74, cy + 22], fill=(255, 255, 255))
    d.ellipse([cx + 52, cy - 22, cx + 96, cy + 22], fill=(255, 255, 255))
    d.rectangle([cx - 74, cy - 22, cx - 30, cy + 22], fill=TEAL)
    d.ellipse([cx - 96, cy - 22, cx - 52, cy + 22], fill=TEAL)
    d.ellipse([cx - 96, cy - 22, cx + 96, cy + 22], outline=INK, width=2)
    d.line([(cx - 30, cy - 22), (cx - 30, cy + 22)], fill=INK, width=2)
    # molecule dots
    for (mx, my, r) in [(x0 + 250, y0 + 16, 5), (x0 + 286, y0 + 30, 4),
                        (x0 + 262, y0 + 62, 4), (x0 + 300, y0 + 70, 3)]:
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=TEAL)
    d.line([(x0 + 250, y0 + 16), (x0 + 286, y0 + 30)], fill=TEAL, width=2)
    d.line([(x0 + 286, y0 + 30), (x0 + 262, y0 + 62)], fill=TEAL, width=2)
    # badge
    bx, by = x1 - 62, y0 + 42
    d.ellipse([bx - 34, by - 34, bx + 34, by + 34], fill=NAVY)
    d.text((bx, by - 14), "1 IN 12", font=fnt(SANS_B, 15), fill=(255, 255, 255),
           anchor="ma")
    d.text((bx, by + 4), "PATIENTS", font=fnt(SANS_B, 10), fill=(255, 255, 255),
           anchor="ma")


def side_story(d, x, y, w, panel, kicker, headline, deck):
    """A sidebar story: small panel, kicker, headline, deck. Returns end y."""
    box = (x, y, x + w, y + 84)
    panel(d, box)
    d.rectangle(box, outline=INK, width=1)
    yy = y + 92
    yy = lines(d, [kicker], x, yy, fnt(SANS_B, 13), RED, leading=16)
    yy = lines(d, wrap(d, headline, fnt(SANS_B, 22), w), x, yy + 2,
               fnt(SANS_B, 22), INK, leading=25)
    return lines(d, wrap(d, deck, fnt(SANS, 15), w), x, yy + 2,
                 fnt(SANS, 15), INK, leading=18)


def band_story(d, x, y, w, panel, kicker, headline, deck):
    """A bottom-band story: panel, kicker, headline, deck. Returns end y."""
    box = (x, y, x + w, y + 84)
    panel(d, box)
    d.rectangle(box, outline=INK, width=1)
    yy = y + 92
    yy = lines(d, [kicker], x, yy, fnt(SANS_B, 13), RED, leading=16)
    yy = lines(d, wrap(d, headline, fnt(SANS_B, 23), w), x, yy + 2,
               fnt(SANS_B, 23), INK, leading=27)
    return lines(d, wrap(d, deck, fnt(SANS, 16), w), x, yy + 2,
                 fnt(SANS, 16), INK, leading=19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    d.text((W // 2, 34), "THE WORLD TODAY", font=fnt(SERIF_B, 74), fill=INK,
           anchor="ma")
    hrule(d, M, W - M, 122)
    d.text((M, 130), "SATURDAY, 21 NOVEMBER 2026", font=fnt(SANS_B, 21), fill=INK)
    tag = "THE WORLD IN ONE PAGE"
    tw = d.textlength(tag, font=fnt(SANS, 18))
    d.text((W - M - tw, 132), tag, font=fnt(SANS, 18), fill=GREY)
    hrule(d, M, W - M, 158, width=3)

    # ---- lead column: the Shenzhen summit ----
    y = 170
    y = lines(d, ["DIPLOMACY — SHENZHEN"], M, y, fnt(SANS_B, 19), RED,
              leading=23)
    y = lines(d, ["TRUMP DEFENDS TIES TO", "PUTIN AND XI AFTER",
                  "SHENZHEN SUMMIT"], M, y + 4, fnt(SANS_B, 38), INK,
              leading=44)
    lead_box = (M, y + 8, M + LEAD_W, y + 8 + 182)
    draw_shenzhen(d, lead_box)
    d.rectangle(lead_box, outline=INK, width=1)
    y = y + 8 + 182 + 8
    lead_end = lines(d, wrap(d, "The first three-way meeting of the US, Chinese "
                                "and Russian leaders ends in a four-point peace "
                                "declaration — silent on Ukraine.",
                             fnt(SANS, 20), LEAD_W), M, y, fnt(SANS, 20), INK,
                     leading=24)

    # ---- sidebar: the court ruling, then the markets ----
    d.line([(SIDE_X - 14, 170), (SIDE_X - 14, lead_end)], fill=INK, width=1)
    sy = 170
    sy = side_story(d, SIDE_X, sy, SIDE_W, draw_scales, "JUSTICE — THE HAGUE",
                    "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
                    "The court holds a state responsible for genocide for the "
                    "first time.")
    sy = side_story(d, SIDE_X, sy + 20, SIDE_W, draw_candles,
                    "MARKETS — NEW YORK",
                    "AI RALLY UNWINDS AS STOCKS SLIDE INTO CORRECTION",
                    "S&P 500 falls 3.7% as chip shares tumble; Nasdaq down 5.3%.")

    # ---- bottom band: Kyiv, then the cancer trial ----
    zone_end = max(lead_end, sy)
    hrule(d, M, W - M, zone_end + 12, width=2)
    band_y = zone_end + 26
    col_w = (CW - 28) // 2
    left_end = band_story(d, M, band_y, col_w, draw_map, "WAR IN EUROPE",
                          "RUSSIA'S BARRAGE HITS KYIV; MISSILES LAND IN POLAND",
                          "400+ drones and 110 missiles overnight; at least "
                          "eight killed. NATO condemns the falls on Polish soil.")
    right_end = band_story(d, M + col_w + 28, band_y, col_w, draw_pill,
                           "HEALTH — LONDON",
                           "PILL MAKES TUMOURS UNDETECTABLE IN 1 IN 12",
                           "Trial of daraxonrasib shows major progress against "
                           "pancreatic cancer.")
    band_end = max(left_end, right_end)

    # ---- in-brief strip ----
    hrule(d, M, W - M, band_end + 12, width=2)
    by = band_end + 20
    label = "IN BRIEF:  "
    d.text((M, by), label, font=fnt(SANS_B, 15), fill=INK)
    lx = M + d.textlength(label, font=fnt(SANS_B, 15))
    brief = ("FBI crime database reportedly hacked  •  Quake shakes Peru  •  "
             "COP31 deadlocked in Antalya  •  Trump pardons Pete Rose  •  "
             "Storm kills 3 in southern Brazil")
    lines(d, wrap(d, brief, fnt(SANS, 15), W - M - lx), lx, by, fnt(SANS, 15),
          INK, leading=19)

    # footer
    hrule(d, M, W - M, 946)
    foot = "THE WORLD IN ONE PAGE — SATURDAY 21 NOVEMBER 2026"
    fw = d.textlength(foot, font=fnt(SANS, 14))
    d.text(((W - fw) // 2, 956), foot, font=fnt(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
