#!/usr/bin/env python3
"""Draw the 24 November 2026 news-image entry: a newspaper front page.

Stdlib-free of any external assets: every pixel is drawn with Pillow
primitives and every word is rendered from local DejaVu fonts, so the
output is deterministic (two runs give byte-identical PNGs).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 244, 232)
INK = (26, 26, 26)
ACCENT = (158, 27, 27)
RULE = (26, 26, 26)
MUTED = (90, 84, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_chip(d, x, y, s):
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                outline=INK, width=3)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                fill=ACCENT)
    for i in range(3):
        t = s * (0.32 + i * 0.18)
        d.line([x + t, y + s * 0.08, x + t, y + s * 0.22], fill=INK, width=3)
        d.line([x + t, y + s * 0.78, x + t, y + s * 0.92], fill=INK, width=3)
        d.line([x + s * 0.08, y + t, x + s * 0.22, y + t], fill=INK, width=3)
        d.line([x + s * 0.78, y + t, x + s * 0.92, y + t], fill=INK, width=3)


def icon_burst(d, x, y, s):
    cx, cy, r1, r2 = x + s / 2, y + s / 2, s * 0.16, s * 0.46
    pts = []
    for i in range(16):
        import math
        ang = math.pi * i / 8
        r = r2 if i % 2 == 0 else r1
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, outline=INK, fill=ACCENT)
    d.ellipse([cx - s * 0.08, cy - s * 0.08, cx + s * 0.08, cy + s * 0.08],
              fill=BG)


def icon_jet(d, x, y, s):
    d.polygon([(x + s * 0.10, y + s * 0.55), (x + s * 0.55, y + s * 0.30),
               (x + s * 0.95, y + s * 0.55), (x + s * 0.55, y + s * 0.62)],
              fill=INK)
    d.polygon([(x + s * 0.45, y + s * 0.55), (x + s * 0.30, y + s * 0.85),
               (x + s * 0.55, y + s * 0.70)], fill=INK)
    d.polygon([(x + s * 0.55, y + s * 0.55), (x + s * 0.75, y + s * 0.88),
               (x + s * 0.62, y + s * 0.62)], fill=INK)


def icon_ship(d, x, y, s):
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.92, y + s * 0.55),
               (x + s * 0.78, y + s * 0.78), (x + s * 0.22, y + s * 0.78)],
              fill=INK)
    d.line([x + s * 0.50, y + s * 0.15, x + s * 0.50, y + s * 0.55],
           fill=INK, width=4)
    d.polygon([(x + s * 0.50, y + s * 0.18), (x + s * 0.82, y + s * 0.38),
               (x + s * 0.50, y + s * 0.38)], fill=ACCENT)
    for i, yy in enumerate((0.86, 0.93)):
        d.arc([x + s * 0.10, y + s * yy, x + s * 0.90, y + s * yy + s * 0.10],
              180, 360, fill=INK, width=3)


def icon_eu(d, x, y, s):
    import math
    cx, cy = x + s / 2, y + s / 2
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        px = cx + s * 0.36 * math.cos(ang)
        py = cy + s * 0.36 * math.sin(ang)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ACCENT)
    d.ellipse([cx - s * 0.10, cy - s * 0.10, cx + s * 0.10, cy + s * 0.10],
              fill=INK)


def icon_gavel(d, x, y, s):
    d.line([x + s * 0.20, y + s * 0.80, x + s * 0.80, y + s * 0.20],
           fill=INK, width=5)
    d.rectangle([x + s * 0.55, y + s * 0.08, x + s * 0.95, y + s * 0.32],
                fill=ACCENT)
    d.rectangle([x + s * 0.05, y + s * 0.68, x + s * 0.45, y + s * 0.92],
                fill=INK)
    d.line([x + s * 0.08, y + s * 0.95, x + s * 0.92, y + s * 0.95],
           fill=INK, width=3)


ICONS = {
    "chip": icon_chip,
    "burst": icon_burst,
    "jet": icon_jet,
    "ship": icon_ship,
    "eu": icon_eu,
    "gavel": icon_gavel,
}

STORIES = [
    dict(kicker="TECHNOLOGY", icon="chip",
         headline="Nvidia Brings Back Jensen Huang as CEO",
         caption="Board reverses course 11 days after his resignation; "
                 "shares jump a third as Trump backs the return."),
    dict(kicker="MIDDLE EAST", icon="burst",
         headline="Iran Hits U.S. Bases in Bahrain Again",
         caption="Third strike in three days as a third American carrier "
                 "group sails into the Gulf."),
    dict(kicker="ASIA", icon="jet",
         headline="Russian Jets Trigger Alert Over South Korea",
         caption="Fighters scramble and Ulleung Island residents are told "
                 "to shelter as jets enter the defence zone."),
    dict(kicker="UKRAINE", icon="ship",
         headline="Ukraine Sinks Russian Warship off Libya",
         caption="Sea drones sink the corvette Merkury in Benghazi and hit "
                 "a cargo ship Kyiv says carried arms."),
    dict(kicker="EUROPE", icon="eu",
         headline="EU Unveils 22nd Sanctions Package",
         caption="Sixty banks face a SWIFT cut-off, plus a ban on Russian "
                 "athletes competing under the EU flag."),
    dict(kicker="TECHNOLOGY", icon="gavel",
         headline="Two U.S. States Sue SpaceX Over Grok",
         caption="Virginia and Oregon say the chatbot turned photos into "
                 "sexual images, including of children."),
]

ALSO = [
    ("Mexico to try 'El Chapo Isidro' at home",
     "Despite a U.S. extradition order, Mexico says it will prosecute "
     "the captured cartel boss first."),
    ("24 dead in Indonesia factory fire",
     "Rescuers still search for about 30 missing after the Banten "
     "candy plant blaze."),
    ("Spain's right on course for majority",
     "Final polls before Sunday's vote put the PP and Vox past "
     "176 seats."),
]

SOURCES = ("Sources: Reuters - Associated Press - The Wall Street Journal - "
           "CNN - Al Jazeera - European Commission - Aju Press - "
           "The Pen PK - Breitbart")


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 34                      # side margin
    cw = W - 2 * mx              # content width
    y = 30

    # ---- masthead ------------------------------------------------------
    f_mast = font(SERIF, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
    y += 78
    f_sub = font(SANS_BOLD, 19)
    left = "TUESDAY, 24 NOVEMBER 2026"
    right = "EDITION No. 328"
    d.text((mx, y), left, font=f_sub, fill=ACCENT)
    rw = d.textlength(right, font=f_sub)
    d.text((W - mx - rw, y), right, font=f_sub, fill=INK)
    y += 30
    d.line([mx, y, W - mx, y], fill=RULE, width=4)
    y += 6
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 16

    # ---- lead story (full width) ---------------------------------------
    lead = STORIES[0]
    f_kick = font(SANS_BOLD, 15)
    f_h1 = font(SERIF, 34)
    f_c1 = font(SANS, 18)
    icon = 108
    d.rectangle([mx, y, mx + icon, y + icon], outline=INK, width=2)
    ICONS[lead["icon"]](d, mx + 4, y + 4, icon - 8)
    tx = mx + icon + 18
    twd = W - mx - tx
    d.text((tx, y + 2), lead["kicker"], font=f_kick, fill=ACCENT)
    hl = wrap(d, lead["headline"], f_h1, twd)
    yy = draw_lines(d, hl, tx, y + 24, f_h1)
    cl = wrap(d, lead["caption"], f_c1, twd)
    draw_lines(d, cl, tx, yy + 2, f_c1)
    y += icon + 16
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 14

    # ---- stories 2-5 in a 2x2 grid --------------------------------------
    gap = 24
    cell_w = (cw - gap) // 2
    f_h2 = font(SERIF, 23)
    f_c2 = font(SANS, 15)
    row_h = 148
    for idx, st in enumerate(STORIES[1:5]):
        col = idx % 2
        row = idx // 2
        cx = mx + col * (cell_w + gap)
        cy = y + row * (row_h + 12)
        d.text((cx, cy), st["kicker"], font=f_kick, fill=ACCENT)
        isz = 62
        d.rectangle([cx, cy + 24, cx + isz, cy + 24 + isz],
                    outline=INK, width=2)
        ICONS[st["icon"]](d, cx + 3, cy + 27, isz - 6)
        tx2 = cx + isz + 12
        tw2 = cx + cell_w - tx2
        hl = wrap(d, st["headline"], f_h2, tw2)
        yy = draw_lines(d, hl, tx2, cy + 24, f_h2)
        cl = wrap(d, st["caption"], f_c2, tw2)
        draw_lines(d, cl, tx2, yy + 2, f_c2)
        if col == 0:
            d.line([cx + cell_w + gap // 2, cy, cx + cell_w + gap // 2,
                    cy + row_h], fill=MUTED, width=1)
    y += 2 * row_h + 12
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 14

    # ---- story 6 (full width band) --------------------------------------
    st = STORIES[5]
    d.text((mx, y), st["kicker"], font=f_kick, fill=ACCENT)
    isz = 62
    d.rectangle([mx, y + 24, mx + isz, y + 24 + isz], outline=INK, width=2)
    ICONS[st["icon"]](d, mx + 3, y + 27, isz - 6)
    tx3 = mx + isz + 14
    tw3 = W - mx - tx3
    hl = wrap(d, st["headline"], f_h2, tw3)
    yy = draw_lines(d, hl, tx3, y + 24, f_h2)
    cl = wrap(d, st["caption"], f_c2, tw3)
    draw_lines(d, cl, tx3, yy + 2, f_c2)
    y += 24 + isz + 14
    d.line([mx, y, W - mx, y], fill=RULE, width=4)
    y += 6
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 14

    # ---- ALSO TODAY strip ----------------------------------------------
    f_also = font(SANS_BOLD, 17)
    d.rectangle([mx, y, W - mx, y + 30], fill=INK)
    d.text((mx + 10, y + 4), "ALSO TODAY", font=f_also, fill=BG)
    y += 42
    col_w = (cw - 2 * gap) // 3
    f_ah = font(SANS_BOLD, 16)
    f_ac = font(SANS, 13)
    for i, (h, c) in enumerate(ALSO):
        ax = mx + i * (col_w + gap)
        hl = wrap(d, h, f_ah, col_w)
        yy = draw_lines(d, hl, ax, y, f_ah)
        cl = wrap(d, c, f_ac, col_w)
        draw_lines(d, cl, ax, yy + 2, f_ac, fill=MUTED)
    y += 96

    # ---- sources footer --------------------------------------------------
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 10
    f_src = font(SANS, 12)
    sl = wrap(d, SOURCES, f_src, cw)
    draw_lines(d, sl, mx, y, f_src, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
