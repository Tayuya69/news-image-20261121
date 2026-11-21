#!/usr/bin/env python3
"""Draw the front page for 21 November 2026 and write entry.png beside this file.

A newspaper front page: masthead with the date, one lead story with a drawn
night scene over Kyiv, and four smaller stories (markets, climate, cyber,
disaster) each with its own drawn panel, plus an in-brief strip.
Every story was reported on Saturday 21 November 2026.

Run:  python3 draw.py
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width

PAPER = (246, 241, 231)
INK = (22, 21, 19)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREY = (90, 86, 78)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, lines, x, y, fnt, fill, leading=None, align="left"):
    """Draw lines starting at (x, y); returns the y just below the block."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            d.text((x + CW // 2, y), line, font=fnt, fill=fill, anchor="ma")
        else:
            d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1):
        d.line([(x0, yy), (x1, yy)], fill=lerp(top, bottom, (yy - y0) / max(1, y1 - y0)))


def draw_kyiv(d, box):
    """Night over Kyiv: skyline, explosions, missile trails, bridge.

    Rendered into its own panel image in local coordinates, then pasted.
    """
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    panel = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    rng = random.Random(20261121)
    for yy in range(ph):
        pd.line([(0, yy), (pw, yy)], fill=lerp((10, 26, 51), (38, 74, 110), yy / max(1, ph)))
    for _ in range(70):
        sx, sy = rng.randint(4, pw - 4), rng.randint(4, 90)
        r = rng.choice([1, 1, 2])
        pd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(230, 235, 245, 255))
    pd.ellipse([pw - 90, 18, pw - 46, 62], fill=(226, 228, 210, 255))
    pd.ellipse([pw - 84, 22, pw - 52, 58], fill=(245, 244, 230, 255))
    # missile trails converging on the bursts
    for (ax, ay, bx, by) in [(90, 8, 300, 72), (660, 6, 520, 62), (860, 14, 720, 72)]:
        pts = []
        for t in range(0, 21):
            f = t / 20
            pts.append((ax + (bx - ax) * f, ay + (by - ay) * f - 26 * (f * (1 - f)) * 4))
        pd.line(pts, fill=(255, 214, 120, 255), width=3)
        pd.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 240, 180, 255))
    # skyline silhouette with lit windows
    base = ph - 34
    x = 0
    while x < pw:
        bw = rng.randint(28, 64)
        bh = rng.randint(40, 120)
        pd.rectangle([x, base - bh, min(x + bw, pw), base + 34], fill=(8, 12, 20, 255))
        for _ in range(bh // 14):
            wx, wy = rng.randint(x + 4, min(x + bw - 6, pw - 6)), rng.randint(base - bh + 6, base - 8)
            pd.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 209, 102, 255))
        x += bw + rng.randint(2, 10)
    # explosion fireballs in front of the rooftops (solid rings: the panel is RGB)
    for (cx, cy, r) in [(300, 72, 46), (520, 62, 38), (720, 72, 52)]:
        pd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 110, 30, 255))
        pd.ellipse([cx - int(r * 0.68), cy - int(r * 0.68),
                    cx + int(r * 0.68), cy + int(r * 0.68)], fill=(245, 165, 55, 255))
        pd.ellipse([cx - int(r * 0.38), cy - int(r * 0.38),
                    cx + int(r * 0.38), cy + int(r * 0.38)], fill=(255, 215, 110, 255))
    # bridge over the river
    pd.line([(60, base + 30), (pw - 60, base + 30)], fill=(8, 12, 20, 255), width=5)
    for bx in range(90, pw - 90, 90):
        pd.line([(bx, base + 30), (bx, base + 2)], fill=(8, 12, 20, 255), width=3)
    pd.arc([60, base - 6, pw - 60, base + 66], 180, 360, fill=(8, 12, 20, 255), width=4)
    pd.rectangle([0, base + 30, pw, ph], fill=(16, 34, 58, 255))
    for ex in (300, 520, 720):
        pd.line([(ex - 26, ph - 12), (ex + 26, ph - 12)], fill=(255, 170, 60, 255), width=2)
    d._image.paste(panel.convert("RGB"), (x0, y0))


def draw_markets(d, box):
    """Falling red chart with the day's closes."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 253, 246))
    for gy in range(y0 + 16, y1 - 8, 18):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(232, 228, 218), width=1)
    pts = [(x0 + 14, y0 + 14), (x0 + 70, y0 + 22), (x0 + 115, y0 + 18),
           (x0 + 165, y0 + 40), (x0 + 210, y0 + 34), (x0 + 260, y0 + 58),
           (x0 + 300, y0 + 52), (x0 + 330, y0 + 74)]
    poly = pts + [(x0 + 330, y1 - 10), (x0 + 14, y1 - 10)]
    d.polygon(poly, fill=(246, 213, 213))
    d.line(pts, fill=RED, width=4)
    d.ellipse([x0 + 326, y0 + 70, x0 + 334, y0 + 78], fill=RED)
    f_big = font(SANS_B, 30)
    d.text((x1 - 118, y0 + 8), "-3.7%", font=f_big, fill=RED)
    f_sm = font(SANS_B, 14)
    d.text((x1 - 118, y0 + 44), "S&P 500", font=f_sm, fill=INK)
    d.text((x0 + 12, y1 - 22), "NASDAQ -5.3%  •  NIKKEI -5.1%", font=f_sm, fill=GREY)


def draw_cop31(d, box):
    """Globe and rising sun over Antalya."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (13, 110, 102), (23, 150, 128))
    cx, cy, r = x0 + 62, y0 + 46, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 190))
    d.ellipse([cx - 24, cy - 20, cx - 2, cy - 2], fill=(64, 160, 90))
    d.ellipse([cx + 2, cy + 4, cx + 26, cy + 22], fill=(64, 160, 90))
    d.ellipse([cx - 8, cy - 28, cx + 12, cy - 12], fill=(64, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    import math
    sx, sy = x0 + 398, y0 + 22
    d.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(255, 214, 120))
    for ang in range(0, 360, 45):
        d.line([(sx, sy), (sx + int(20 * math.cos(math.radians(ang))),
                            sy + int(20 * math.sin(math.radians(ang))))],
               fill=(255, 214, 120), width=3)
    f_big = font(SANS_B, 30)
    d.text((x0 + 128, y0 + 22), "COP31", font=f_big, fill=(255, 255, 255))
    f_sm = font(SANS_B, 14)
    d.text((x0 + 128, y0 + 58), "ANTALYA, TURKEY", font=f_sm, fill=(220, 240, 235))


def draw_fbi(d, box):
    """Shield and code: a reported breach of the FBI's crime database."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(22, 35, 63))
    rng = random.Random(7)
    f_code = font(SANS, 11)
    for _ in range(46):
        bx, by = rng.randint(x0 + 6, x1 - 20), rng.randint(y0 + 4, y1 - 12)
        d.text((bx, by), rng.choice(["0", "1"]), font=f_code, fill=(70, 95, 130))
    cx, cy = x0 + 66, y0 + 46
    shield = [(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 34, cy + 2),
              (cx, cy + 34), (cx - 34, cy + 2)]
    d.polygon(shield, outline=(212, 175, 55), width=3)
    d.polygon([(cx - 28, cy - 24), (cx + 28, cy - 24), (cx + 28, cy + 1),
               (cx, cy + 28), (cx - 28, cy + 1)], fill=(212, 175, 55))
    f_big = font(SANS_B, 24)
    d.text((cx, cy - 8), "FBI", font=f_big, fill=(22, 35, 63), anchor="ma")
    f_sm = font(SANS_B, 14)
    d.text((x0 + 122, y0 + 30), "BREACH", font=font(SANS_B, 26), fill=(255, 255, 255))
    d.text((x0 + 122, y0 + 60), "REPORTED", font=f_sm, fill=(180, 195, 220))


def draw_peru(d, box):
    """Andes peaks and a seismograph trace."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (232, 220, 195), (214, 196, 154))
    d.polygon([(x0, y1), (x0 + 110, y0 + 22), (x0 + 220, y1)], fill=(138, 109, 75))
    d.polygon([(x0 + 110, y0 + 22), (x0 + 128, y0 + 40), (x0 + 92, y0 + 40)], fill=(255, 255, 255))
    d.polygon([(x0 + 150, y1), (x0 + 280, y0 + 8), (x0 + 400, y1)], fill=(107, 79, 51))
    d.polygon([(x0 + 280, y0 + 8), (x0 + 300, y0 + 28), (x0 + 260, y0 + 28)], fill=(255, 255, 255))
    d.polygon([(x0 + 330, y1), (x0 + 430, y0 + 30), (x1, y1)], fill=(78, 58, 38))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(255, 253, 246))
    pts = []
    x, y = x0 + 8, y1 - 13
    pts.append((x, y))
    import math
    for i in range(1, 60):
        x = x0 + 8 + i * 6
        amp = 9 if 22 < i < 40 else 2
        y = y1 - 13 + int(amp * math.sin(i * 1.7))
        pts.append((x, y))
    d.line(pts, fill=RED, width=2)
    f_big = font(SANS_B, 30)
    d.rectangle([x1 - 96, y0 + 4, x1 - 6, y0 + 62], fill=(255, 253, 246),
                outline=(122, 30, 30), width=2)
    d.text((x1 - 51, y0 + 8), "6.9", font=f_big, fill=(122, 30, 30), anchor="ma")
    d.text((x1 - 51, y0 + 42), "MAGNITUDE", font=font(SANS_B, 11), fill=INK, anchor="ma")


def story(d, x, y, w, kicker, headline, deck, panel):
    """One secondary story: drawn panel, kicker, headline, deck."""
    box = (x, y, x + w, y + 84)
    panel(d, box)
    d.rectangle(box, outline=INK, width=1)
    yy = y + 92
    yy = text_lines(d, [kicker], x, yy, font(SANS_B, 13), RED, leading=16)
    yy = text_lines(d, wrap(d, headline, font(SANS_B, 24), w), x, yy + 2,
                    font(SANS_B, 24), INK, leading=27)
    text_lines(d, wrap(d, deck, font(SANS, 17), w), x, yy + 2,
               font(SANS, 17), INK, leading=20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    f_name = font(SERIF_B, 74)
    d.text((W // 2, 34), "THE WORLD TODAY", font=f_name, fill=INK, anchor="ma")
    rule(d, M, W - M, 122)
    f_date = font(SANS_B, 21)
    d.text((M, 130), "SATURDAY, 21 NOVEMBER 2026", font=f_date, fill=INK)
    f_tag = font(SANS, 18)
    tw = d.textlength("THE WORLD IN ONE PAGE", font=f_tag)
    d.text((W - M - tw, 132), "THE WORLD IN ONE PAGE", font=f_tag, fill=GREY)
    rule(d, M, W - M, 158, width=3)

    # lead story
    y = 168
    y = text_lines(d, ["WAR IN EUROPE"], M, y, font(SANS_B, 20), RED, leading=24)
    y = text_lines(d, ["RUSSIA'S BIGGEST BARRAGE", "HITS KYIV — MISSILES LAND IN POLAND"],
                   M, y + 2, font(SANS_B, 40), INK, leading=46)
    vis_y = y + 8
    lead_box = (M, vis_y, W - M, vis_y + 190)
    draw_kyiv(d, lead_box)
    d.rectangle(lead_box, outline=INK, width=1)
    y = vis_y + 190 + 10
    y = text_lines(d, wrap(d, "More than 400 drones and 110 missiles fired at Ukraine overnight; "
                              "at least eight killed in Kyiv. Warsaw calls the falls on its soil "
                              "a deliberate provocation.",
                           font(SANS, 21), CW), M, y, font(SANS, 21), INK, leading=25)
    rule(d, M, W - M, y + 8, width=2)

    # rows of two stories
    row_y = y + 20
    col_w = (CW - 36) // 2
    story(d, M, row_y, col_w, "MARKETS",
          "AI SELL-OFF DRAGS STOCKS INTO CORRECTION",
          "S&P 500 falls 3.7% as chip shares tumble; Nasdaq down 5.3%, Nikkei 5.1%.",
          draw_markets)
    story(d, M + col_w + 36, row_y, col_w, "CLIMATE — ANTALYA",
          "COP31 DEADLOCKED OVER FOSSIL FUELS",
          "Climate talks run past their deadline as nearly 200 nations fail to agree.",
          draw_cop31)
    row_y += 206
    story(d, M, row_y, col_w, "CYBER — UNITED STATES",
          "FBI CRIME DATABASE REPORTEDLY HACKED",
          "Hack reported as US computer outages continue.",
          draw_fbi)
    story(d, M + col_w + 36, row_y, col_w, "DISASTER — PERU",
          "6.9 QUAKE SHAKES PERU'S ANDES",
          "Tremor felt in Lima; no casualties reported.",
          draw_peru)

    # in-brief strip
    by = row_y + 196
    rule(d, M, W - M, by, width=2)
    f_brief_b = font(SANS_B, 15)
    f_brief = font(SANS, 15)
    label = "IN BRIEF:  "
    d.text((M, by + 8), label, font=f_brief_b, fill=INK)
    lx = M + d.textlength(label, font=f_brief_b)
    brief = ("UK–EU sign post-Brexit deals  •  Palisades fire arsonist convicted  •  "
             "Bayer pays $7.25bn over Roundup")
    d.text((lx, by + 8), brief, font=f_brief, fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
