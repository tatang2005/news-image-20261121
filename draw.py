#!/usr/bin/env python3
"""Render the "Civil Atlas" front page for Saturday 21 November 2026.

The page is a broadsheet-style newspaper front page drawn entirely with
Pillow primitives: a masthead, one lead panel, four grid panels, one
full-width bottom panel and a black ticker strip along the foot of the
page.  Everything is laid out from fixed coordinates and the drawing
uses no randomness, no clock and no network, so two runs of this file
produce byte-identical PNG files.

Usage:  python3 draw.py [output-path]     (default: entry.png)
"""

import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

WIDTH = 1024
HEIGHT = 1024
MARGIN = 26
CONTENT_W = WIDTH - 2 * MARGIN

PAPER = (248, 244, 233)
PANEL_BG = (255, 253, 246)
INK = (26, 26, 26)
FAINT = (90, 84, 70)
RULE = (150, 140, 115)
BAR_DARK = (34, 37, 42)
BAR_RED = (156, 28, 28)
BAR_GREEN = (46, 107, 52)
BAR_GOLD = (138, 90, 18)
BAR_PLUM = (74, 54, 112)
WHITE = (255, 255, 255)
TICKER_BG = (12, 12, 12)
TICKER_RED = (178, 30, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = load("DejaVuSerif-Bold.ttf", 68)
F_DATE = load("DejaVuSans-Bold.ttf", 17)
F_TAG = load("DejaVuSans.ttf", 13)
F_LEAD_HEAD = load("DejaVuSans-Bold.ttf", 34)
F_HEAD = load("DejaVuSans-Bold.ttf", 21)
F_BODY = load("DejaVuSans.ttf", 14)
F_BAR = load("DejaVuSans-Bold.ttf", 12)
F_TICK_LABEL = load("DejaVuSans-Bold.ttf", 15)
F_TICK = load("DejaVuSans.ttf", 14)

# ---------------------------------------------------------------- helpers


def wrap(draw, text, font, max_width):
    """Split text into lines that each fit inside max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, font, colour, max_width, line_height):
    """Draw wrapped text starting at (x, y); return the y just below it."""
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=colour)
        y += line_height
    return y


def panel(draw, x, y, w, h, bar_colour, section, number,
          headline, body, head_font, head_line_height, body_max_lines,
          body_line_height=20):
    """Draw one story panel: header bar, headline, body copy."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE, width=1)

    # header bar with the section name on the left, story number right
    draw.rectangle([x, y, x + w, y + 24], fill=bar_colour)
    draw.text((x + 10, y + 5), section, font=F_BAR, fill=WHITE)
    label = "No. %d" % number
    draw.text((x + w - 10 - draw.textlength(label, font=F_BAR), y + 5),
              label, font=F_BAR, fill=WHITE)

    inner_x = x + 13
    inner_w = w - 26
    cy = y + 24 + 8
    cy = draw_text_block(draw, inner_x, cy, headline, head_font, INK,
                         inner_w, head_line_height)
    cy += 3
    lines = wrap(draw, body, F_BODY, inner_w)[:body_max_lines]
    for line in lines:
        draw.text((inner_x, cy), line, font=F_BODY, fill=INK)
        cy += body_line_height
    return cy


# ---------------------------------------------------------------- content

LEAD = (
    "EUROPE",
    "Russian Missiles Land in Poland",
    "Two Russian missiles and a jet-powered drone came down in "
    "south-eastern Poland during the massive overnight strike on "
    "Ukraine. PM Donald Tusk called it a likely \u201cintentional "
    "provocation\u201d; NATO chief Mark Rutte called it a \u201cgrave "
    "violation\u201d of Polish airspace. No injuries were reported.",
)

STORIES = [
    (
        "UKRAINE",
        "Kyiv Pounded in Massive Strike",
        "Russia fired more than 400 drones and 110 missiles, some with "
        "cluster warheads, across Ukraine. At least nine civilians were "
        "killed, three Kyiv bridges shut and power was knocked out. "
        "Zelensky called it one of the most massive strikes of the war.",
    ),
    (
        "CLIMATE",
        "COP31 Deadlocked in Overtime",
        "The UN climate talks in Antalya slipped past their Friday "
        "close into the weekend with no deal. The latest draft drops "
        "every mention of fossil fuels and the $120bn adaptation "
        "target; a third draft was promised for Saturday.",
    ),
    (
        "WASHINGTON",
        "Trump: Iran Must Take a \u2018Real Deal\u2019",
        "Trump said Iran wants an agreement but refuses terms he can "
        "accept, demanding a \u201creal deal\u201d. US envoys met Qatari "
        "mediators in Berlin while Washington kept its naval blockade "
        "and economic pressure on Tehran.",
    ),
    (
        "ENERGY",
        "Tankers Ablaze off Hormuz",
        "Iran\u2019s army said two oil tankers caught fire after "
        "striking mines in the waters off Hormuz, the chokepoint "
        "strait at the centre of the US\u2013Iran confrontation. The "
        "IEA warned there is \u201cno going back\u201d from the energy "
        "shock.",
    ),
]

BOTTOM_STORY = (
    "TECHNOLOGY",
    "Nvidia Probed over China Chips",
    "California\u2019s attorney general has subpoenaed Nvidia amid "
    "worries over how its AI chips reached China, while a House "
    "committee reported the US approved sales of nearly 900,000 AI "
    "chips to China within six months \u2014 fuelling the fight over "
    "export controls and the future of the AI race.",
)

TICKER_ITEMS = [
    "EU approves \u20ac1 billion in military aid for Ukraine",
    "Italy\u2019s workers and students walk out in a mass strike over "
    "living costs",
    "Myanmar rejects the ICJ genocide ruling as Malaysia agrees to "
    "shelter 10,000 Rohingya",
]

# ---------------------------------------------------------------- page


def masthead(draw):
    # newspaper name, centred
    name = "CIVIL ATLAS"
    w = draw.textlength(name, font=F_TITLE)
    draw.text(((WIDTH - w) / 2, 30), name, font=F_TITLE, fill=INK)

    tag = "THE WORLD IN ONE DAY  \u00b7  ALL THE NEWS ON A SINGLE PAGE"
    w = draw.textlength(tag, font=F_TAG)
    draw.text(((WIDTH - w) / 2, 108), tag, font=F_TAG, fill=FAINT)

    draw.line([MARGIN, 132, WIDTH - MARGIN, 132], fill=INK, width=3)
    draw.line([MARGIN, 138, WIDTH - MARGIN, 138], fill=INK, width=1)

    date = "SATURDAY, 21 NOVEMBER 2026"
    draw.text((MARGIN, 146), date, font=F_DATE, fill=INK)
    right = "LATE CITY EDITION"
    w = draw.textlength(right, font=F_DATE)
    draw.text((WIDTH - MARGIN - w, 146), right, font=F_DATE, fill=INK)

    draw.line([MARGIN, 172, WIDTH - MARGIN, 172], fill=RULE, width=1)


def ticker(draw):
    top = 906
    draw.rectangle([MARGIN, top, WIDTH - MARGIN, HEIGHT - MARGIN],
                   fill=TICKER_BG)
    # red label block on the left
    draw.rectangle([MARGIN, top, MARGIN + 118, HEIGHT - MARGIN],
                   fill=TICKER_RED)
    label = "LATE"
    w = draw.textlength(label, font=F_TICK_LABEL)
    draw.text((MARGIN + (118 - w) / 2, top + 22), label,
              font=F_TICK_LABEL, fill=WHITE)
    label = "WIRE"
    w = draw.textlength(label, font=F_TICK_LABEL)
    draw.text((MARGIN + (118 - w) / 2, top + 44), label,
              font=F_TICK_LABEL, fill=WHITE)

    text = "  \u2022  ".join(TICKER_ITEMS)
    draw_text_block(draw, MARGIN + 138, top + 24, text, F_TICK, WHITE,
                    WIDTH - MARGIN - (MARGIN + 138) - 14, 24)


def build():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, WIDTH - 9, HEIGHT - 9], outline=RULE, width=2)

    masthead(draw)

    # lead story, full width
    panel(draw, MARGIN, 184, CONTENT_W, 142, BAR_RED,
          LEAD[0], 1, LEAD[1], LEAD[2], F_LEAD_HEAD, 42, 4)

    # four stories in a two-by-two grid
    col_w = (CONTENT_W - 14) // 2
    row_h = 192
    positions = [
        (MARGIN, 340),
        (MARGIN + col_w + 14, 340),
        (MARGIN, 546),
        (MARGIN + col_w + 14, 546),
    ]
    bar_colours = [BAR_DARK, BAR_GREEN, BAR_DARK, BAR_GOLD]
    for idx, (story, (px, py), colour) in enumerate(
            zip(STORIES, positions, bar_colours)):
        panel(draw, px, py, col_w, row_h, colour,
              story[0], idx + 2, story[1], story[2], F_HEAD, 26, 5)

    # closing story, full width above the ticker
    panel(draw, MARGIN, 752, CONTENT_W, 140, BAR_PLUM,
          BOTTOM_STORY[0], 6, BOTTOM_STORY[1], BOTTOM_STORY[2],
          F_HEAD, 26, 3)

    ticker(draw)
    return img


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out_path, format="PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
