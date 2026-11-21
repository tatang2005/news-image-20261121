"""draw.py -- renders the front page for news-image-20261121.

A 1024x1024 newspaper front page, "The Daily Wire", summing up the
world news of Saturday 21 November 2026 in six illustrated panels plus
a three-item ticker strip along the bottom.

Everything is drawn with Pillow primitives (lines, polygons, ellipses,
text) from fixed coordinates and fixed data, so the output is fully
deterministic: the same input always produces the same pixels.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- fonts

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start_size, max_width, min_size=10):
    """Largest font (<= start_size) whose text fits inside max_width."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, min_size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, path, size, fill, max_width, line_gap,
                 max_lines=None):
    """Draw wrapped text, shrinking the font until it fits max_lines."""
    while True:
        f = font(path, size)
        lines = wrap(draw, text, f, max_width)
        if max_lines is None or len(lines) <= max_lines or size <= 11:
            break
        size -= 1
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += size + line_gap
    return y


# ---------------------------------------------------------------- palette

PAPER = (246, 241, 227)
PANEL_BG = (255, 253, 244)
INK = (20, 18, 14)
FAINT = (110, 102, 88)
RED = (176, 32, 32)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- icons
# Each icon draws inside the box (x0, y0, x1, y1) on a tinted ground.


def icon_missile_poland(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # Polish flag: white over red.
    d.rectangle([x0, y0, x1, y0 + h // 2], fill=(250, 250, 246))
    d.rectangle([x0, y0 + h // 2, x1, y1], fill=(206, 42, 54))
    # Missile silhouette diving from top-left to bottom-right.
    body = [(x0 + 18, y0 + 12), (x0 + 44, y0 + 20), (x1 - 22, y1 - 34),
            (x1 - 34, y1 - 16), (x0 + 30, y0 + 44)]
    d.polygon(body, fill=(38, 38, 44))
    # Nose cone.
    d.polygon([(x1 - 22, y1 - 34), (x1 - 6, y1 - 8), (x1 - 34, y1 - 16)],
              fill=(16, 16, 20))
    # Fins near the tail.
    d.polygon([(x0 + 26, y0 + 34), (x0 + 6, y0 + 52), (x0 + 38, y0 + 48)],
              fill=(16, 16, 20))
    d.polygon([(x0 + 40, y0 + 22), (x0 + 52, y0 + 4), (x0 + 52, y0 + 34)],
              fill=(16, 16, 20))
    # Exhaust flame.
    d.polygon([(x0 + 18, y0 + 12), (x0 + 2, y0 + 2), (x0 + 30, y0 + 26)],
              fill=(240, 140, 30))
    d.polygon([(x0 + 22, y0 + 16), (x0 + 12, y0 + 8), (x0 + 30, y0 + 26)],
              fill=(250, 200, 60))


def icon_bridge_blast(d, box):
    x0, y0, x1, y1 = box
    mid_y = y0 + (y1 - y0) * 2 // 3
    # Explosion starburst above the bridge.
    cx, cy = (x0 + x1) // 2, y0 + 34
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 30 if i % 2 == 0 else 13
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(232, 116, 22))
    pts2 = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 18 if i % 2 == 0 else 8
        pts2.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts2, fill=(250, 196, 60))
    # Smoke puffs.
    for (sx, sy, r) in [(x0 + 26, y0 + 20, 11), (x1 - 28, y0 + 16, 9),
                        (x1 - 46, y0 + 30, 7)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 146, 138))
    # Bridge towers and deck.
    d.rectangle([x0 + 16, mid_y - 34, x0 + 24, mid_y + 22], fill=INK)
    d.rectangle([x1 - 24, mid_y - 34, x1 - 16, mid_y + 22], fill=INK)
    d.rectangle([x0 + 6, mid_y, x1 - 6, mid_y + 7], fill=INK)
    # Suspension cables.
    d.line([x0 + 20, mid_y - 34, cx, mid_y - 2], fill=INK, width=2)
    d.line([cx, mid_y - 2, x1 - 20, mid_y - 34], fill=INK, width=2)
    # Broken span in the middle: jagged gap.
    d.polygon([(cx - 16, mid_y - 1), (cx - 4, mid_y + 8), (cx + 6, mid_y - 1),
               (cx + 16, mid_y + 9), (cx + 16, mid_y + 14), (cx - 16, mid_y + 14)],
              fill=PANEL_BG)
    # Water below.
    for i, wy in enumerate(range(mid_y + 26, y1 - 8, 10)):
        off = 8 if i % 2 else 0
        for wx in range(x0 + 12 + off, x1 - 24, 30):
            d.arc([wx, wy, wx + 18, wy + 8], 0, 180, fill=(70, 110, 160),
                  width=2)


def icon_globe_thermo(d, box):
    x0, y0, x1, y1 = box
    cx, cy, r = x0 + 48, (y0 + y1) // 2, 40
    # Globe.
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 90, 150),
              width=3)
    d.ellipse([cx - 15, cy - r, cx + 15, cy + r], outline=(30, 90, 150),
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(30, 90, 150), width=2)
    d.line([cx - r + 6, cy - 22, cx + r - 6, cy - 22], fill=(30, 90, 150),
           width=1)
    d.line([cx - r + 6, cy + 22, cx + r - 6, cy + 22], fill=(30, 90, 150),
           width=1)
    # Continents (rough green blobs).
    green = (52, 140, 74)
    d.ellipse([cx - 30, cy - 26, cx - 8, cy - 8], fill=green)
    d.ellipse([cx + 4, cy - 18, cx + 28, cy + 2], fill=green)
    d.ellipse([cx - 12, cy + 8, cx + 10, cy + 28], fill=green)
    # Thermometer on the right, mercury high.
    tx = x1 - 30
    d.rounded_rectangle([tx - 6, y0 + 12, tx + 6, y1 - 26], 6,
                        outline=INK, width=3)
    d.ellipse([tx - 13, y1 - 40, tx + 13, y1 - 14], outline=INK, width=3,
              fill=RED)
    d.rectangle([tx - 3, y0 + 22, tx + 3, y1 - 28], fill=RED)
    for ty in range(y0 + 20, y1 - 34, 14):
        d.line([tx + 8, ty, tx + 14, ty], fill=INK, width=2)


def icon_deal_doc(d, box):
    x0, y0, x1, y1 = box
    # Document sheet.
    dx0, dy0, dx1, dy1 = x0 + 26, y0 + 10, x1 - 26, y1 - 10
    d.rectangle([dx0, dy0, dx1, dy1], fill=WHITE, outline=INK, width=3)
    # Folded corner.
    d.polygon([(dx1 - 18, dy0), (dx1, dy0 + 18), (dx1 - 18, dy0 + 18)],
              fill=(210, 205, 190), outline=INK)
    # Text lines on the sheet.
    for i, ly in enumerate(range(dy0 + 18, dy1 - 30, 13)):
        end = dx1 - 14 if i % 3 else dx1 - 30
        d.line([dx0 + 12, ly, end, ly], fill=(120, 116, 106), width=3)
    # Big red X over the document: no deal.
    d.line([dx0 + 8, dy0 + 8, dx1 - 8, dy1 - 8], fill=RED, width=9)
    d.line([dx1 - 8, dy0 + 8, dx0 + 8, dy1 - 8], fill=RED, width=9)


def icon_tanker_fire(d, box):
    x0, y0, x1, y1 = box
    deck_y = y0 + 66
    # Flames above the deck.
    flame = [(x0 + 42, deck_y), (x0 + 48, deck_y - 38), (x0 + 58, deck_y - 10),
             (x0 + 66, deck_y - 46), (x0 + 76, deck_y - 8), (x0 + 86, deck_y)]
    d.polygon(flame, fill=(232, 116, 22))
    flame2 = [(x0 + 54, deck_y), (x0 + 62, deck_y - 24), (x0 + 72, deck_y)]
    d.polygon(flame2, fill=(250, 200, 60))
    # Smoke.
    for (sx, sy, r) in [(x0 + 84, y0 + 14, 10), (x0 + 98, y0 + 8, 7)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 146, 138))
    # Containers on deck.
    cols = [(52, 140, 74), (176, 32, 32), (30, 90, 150)]
    for i, c in enumerate(cols):
        d.rectangle([x0 + 18 + i * 30, deck_y - 14, x0 + 44 + i * 30, deck_y],
                    fill=c, outline=INK, width=1)
    # Bridge tower.
    d.rectangle([x1 - 26, deck_y - 26, x1 - 12, deck_y], fill=(90, 90, 96),
                outline=INK, width=1)
    # Hull.
    d.polygon([(x0 + 8, deck_y), (x1 - 8, deck_y), (x1 - 20, deck_y + 18),
               (x0 + 20, deck_y + 18)], fill=(38, 38, 44))
    d.rectangle([x0 + 8, deck_y, x1 - 8, deck_y + 4], fill=RED)
    # Sea waves.
    for i, wy in enumerate(range(deck_y + 26, y1 - 6, 9)):
        off = 8 if i % 2 else 0
        for wx in range(x0 + 10 + off, x1 - 26, 30):
            d.arc([wx, wy, wx + 18, wy + 8], 0, 180, fill=(70, 110, 160),
                  width=2)


def icon_chip(d, box):
    x0, y0, x1, y1 = box
    bx0, by0, bx1, by1 = x0 + 26, y0 + 26, x1 - 26, y1 - 26
    # Pins on all four sides.
    for px in range(bx0 + 10, bx1 - 6, 16):
        d.rectangle([px, by0 - 12, px + 6, by0], fill=(90, 90, 96))
        d.rectangle([px, by1, px + 6, by1 + 12], fill=(90, 90, 96))
    for py in range(by0 + 10, by1 - 6, 16):
        d.rectangle([bx0 - 12, py, bx0, py + 6], fill=(90, 90, 96))
        d.rectangle([bx1, py, bx1 + 12, py + 6], fill=(90, 90, 96))
    # Chip body and core.
    d.rounded_rectangle([bx0, by0, bx1, by1], 8, fill=(38, 38, 44))
    d.rounded_rectangle([bx0 + 12, by0 + 12, bx1 - 12, by1 - 12], 5,
                        outline=(120, 200, 90), width=3)
    f = fit_font(d, "AI", SANS_BOLD, 34, bx1 - bx0 - 30)
    tw = d.textlength("AI", font=f)
    d.text(((bx0 + bx1 - tw) / 2, (by0 + by1) / 2 - 19), "AI", font=f,
           fill=(180, 240, 150))


# ---------------------------------------------------------------- content

STORIES = [
    {
        "kicker": "NATO · POLAND",
        "accent": (176, 32, 32),
        "tint": (250, 236, 232),
        "icon": icon_missile_poland,
        "headline": "RUSSIAN MISSILES LAND IN POLAND",
        "summary": "Two missiles and a drone fell on NATO soil in the "
                   "giant strike on Ukraine. PM Tusk called it a "
                   "provocation; nobody was hurt.",
    },
    {
        "kicker": "UKRAINE · WAR",
        "accent": (194, 94, 16),
        "tint": (252, 240, 226),
        "icon": icon_bridge_blast,
        "headline": "KYIV POUNDED IN MASSIVE STRIKE",
        "summary": "Russia fired 400+ drones and 110 missiles, killing "
                   "at least nine, crippling Kyiv's bridges and cutting "
                   "power across Ukraine.",
    },
    {
        "kicker": "CLIMATE · COP31",
        "accent": (30, 110, 78),
        "tint": (232, 246, 236),
        "icon": icon_globe_thermo,
        "headline": "COP31 DEADLOCKED IN OVERTIME",
        "summary": "Antalya's climate talks ran into the weekend with "
                   "no deal: the latest draft drops every mention of "
                   "fossil fuels.",
    },
    {
        "kicker": "IRAN · DIPLOMACY",
        "accent": (29, 58, 110),
        "tint": (232, 238, 250),
        "icon": icon_deal_doc,
        "headline": "TRUMP: IRAN MUST TAKE A 'REAL DEAL'",
        "summary": "Trump says Tehran wants a deal but not one he can "
                   "accept. Envoys met Qatari mediators in Berlin as "
                   "the blockade grinds on.",
    },
    {
        "kicker": "HORMUZ · ENERGY",
        "accent": (176, 32, 32),
        "tint": (250, 236, 232),
        "icon": icon_tanker_fire,
        "headline": "TANKERS ABLAZE OFF HORMUZ",
        "summary": "Two oil tankers burst into flames after striking "
                   "mines off Hormuz, Iran's army says, amid the "
                   "US-Iran standoff at sea.",
    },
    {
        "kicker": "TECH · AI CHIPS",
        "accent": (91, 42, 134),
        "tint": (242, 236, 250),
        "icon": icon_chip,
        "headline": "NVIDIA PROBED OVER CHINA CHIPS",
        "summary": "California's attorney general subpoenas Nvidia over "
                   "China chip sales; a House panel counts 900K AI chip "
                   "approvals in six months.",
    },
]

TICKER = [
    "EU approves €1 billion more in military aid for Ukraine",
    "Italy: workers and students walk out over living costs",
    "Myanmar rejects ICJ verdict; Malaysia to take 10,000 Rohingya",
]

# ---------------------------------------------------------------- layout

SIZE = 1024
MARGIN = 30


def draw_masthead(d):
    # Top hairline with edition marks.
    d.line([MARGIN, 42, SIZE - MARGIN, 42], fill=INK, width=2)
    small = font(SANS_BOLD, 15)
    d.text((MARGIN + 2, 50), "VOL. V — No. 321", font=small, fill=FAINT)
    right = "ONE IMAGE · ONE DAY"
    d.text((SIZE - MARGIN - 2 - d.textlength(right, font=small), 50),
           right, font=small, fill=FAINT)
    # Newspaper name.
    name = "THE DAILY WIRE"
    f = fit_font(d, name, SERIF_BOLD, 96, SIZE - 2 * MARGIN - 40)
    tw = d.textlength(name, font=f)
    d.text(((SIZE - tw) / 2, 66), name, font=f, fill=INK)
    # Thick-thin rules under the name.
    d.rectangle([MARGIN, 158, SIZE - MARGIN, 163], fill=INK)
    d.line([MARGIN, 168, SIZE - MARGIN, 168], fill=INK, width=1)
    # Date line.
    date = "SATURDAY · 21 NOVEMBER 2026"
    f = fit_font(d, date, SANS_BOLD, 30, 620)
    tw = d.textlength(date, font=f)
    d.text(((SIZE - tw) / 2, 176), date, font=f, fill=RED)
    tag = "All the day's world news, drawn on a single page"
    f = font(SERIF_ITALIC, 18)
    tw = d.textlength(tag, font=f)
    d.text(((SIZE - tw) / 2, 210), tag, font=f, fill=FAINT)
    return 236


def draw_panel(d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)
    # Icon box, top-left.
    ib = (x + 14, y + 16, x + 132, y + 134)
    d.rectangle(ib, fill=story["tint"], outline=INK, width=2)
    story["icon"](d, ib)
    # Text column to the right of the icon.
    tx = x + 148
    tw = x + w - tx - 12
    kick_f = font(SANS_BOLD, 15)
    d.text((tx, y + 14), story["kicker"], font=kick_f, fill=story["accent"])
    hy = draw_wrapped(d, (tx, y + 36), story["headline"], SANS_BOLD, 26,
                      INK, tw, 4, max_lines=3)
    draw_wrapped(d, (tx, hy + 6), story["summary"], SANS, 18, INK, tw, 5,
                 max_lines=4)
    # Thin rule + dateline under the icon.
    d.line([x + 14, y + h - 25, x + w - 14, y + h - 25], fill=FAINT, width=1)
    foot = font(SERIF_ITALIC, 14)
    d.text((x + 14, y + h - 19), "The Daily Wire — wire reports",
           font=foot, fill=FAINT)


def draw_ticker(d, y):
    x0, x1 = MARGIN, SIZE - MARGIN
    d.rectangle([x0, y, x1, y + 62], fill=INK)
    label = "LATE WIRE"
    lf = font(SANS_BOLD, 16)
    lw = d.textlength(label, font=lf)
    d.rectangle([x0 + 10, y + 10, x0 + 22 + lw, y + 40], fill=RED)
    d.text((x0 + 16, y + 17), label, font=lf, fill=WHITE)
    col_x = x0 + 36 + lw
    col_w = (x1 - col_x - 10) // 3
    for i, item in enumerate(TICKER):
        cx = col_x + i * col_w
        if i:
            d.line([cx - 8, y + 10, cx - 8, y + 52], fill=(90, 86, 76),
                   width=1)
        draw_wrapped(d, (cx, y + 11), item, SANS_BOLD, 16, WHITE,
                     col_w - 12, 4, max_lines=2)


def render():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # Page frame: double border.
    d.rectangle([16, 16, SIZE - 16, SIZE - 16], outline=INK, width=3)
    d.rectangle([24, 24, SIZE - 24, SIZE - 24], outline=INK, width=1)
    top = draw_masthead(d)
    # Panel grid: 2 columns x 3 rows.
    ticker_y = 934
    area_h = ticker_y - 14 - top
    gap = 12
    row_h = (area_h - 2 * gap) // 3
    col_w = (SIZE - 2 * MARGIN - gap) // 2
    for idx, story in enumerate(STORIES):
        r, c = divmod(idx, 2)
        x = MARGIN + c * (col_w + gap)
        y = top + r * (row_h + gap)
        draw_panel(d, x, y, col_w, row_h, story)
    draw_ticker(d, ticker_y)
    return img


if __name__ == "__main__":
    render().save("entry.png")
