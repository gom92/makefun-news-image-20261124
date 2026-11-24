#!/usr/bin/env python3
"""Render the front page for make.fun news-image-20261124.

Draws a 1024x1024 newspaper front page summing up Tuesday 24 November
2026 with Pillow. All text is drawn by Pillow (AI image tools garble
text); the two editorial illustrations in ../assets/ are AI-generated
and carry no text.

Run:  python3 tools/render_frontpage.py
Out:  entry.png  (1024x1024, must stay under 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)      # newsprint off-white
INK = (18, 18, 18)           # near-black
RULE = (18, 18, 18)
ACCENT = (158, 27, 24)       # deep newspaper red
MUTED = (90, 86, 78)

FONT_CANDIDATES = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
    "serif_italic": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
}


def font(kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_image(path, w, h):
    """Open, centre-crop to the target aspect, resize to (w, h)."""
    im = Image.open(path).convert("RGB")
    tw, th = w, h
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    MX = 28                      # side margin
    CW = W - 2 * MX              # content width

    # ---- Masthead -----------------------------------------------------
    mast = font("serif_bold", 66)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 14), title, font=mast, fill=INK)
    d.line([(MX, 96), (W - MX, 96)], fill=RULE, width=3)
    d.line([(MX, 101), (W - MX, 101)], fill=RULE, width=1)
    small = font("sans_bold", 15)
    d.text((MX, 110), "TUESDAY, 24 NOVEMBER 2026", font=small, fill=INK)
    right = "THE DAY'S NEWS IN ONE PAGE"
    d.text((W - MX - d.textlength(right, font=small), 110),
           right, font=small, fill=INK)
    d.line([(MX, 134), (W - MX, 134)], fill=RULE, width=2)

    # ---- Lead story: NATO AWACS to Poland -----------------------------
    LX, LW = MX, 640
    LY = 148
    awacs = fit_image(
        os.path.join(ASSETS,
                     "media-generation-awacs-lead-0-9ca43ab1-dd78-47b8-b2fd-215180b194a8.webp"),
        LW, 272)
    page.paste(awacs, (LX, LY))
    d.rectangle([LX, LY, LX + LW - 1, LY + 272], outline=RULE, width=1)
    y = LY + 272 + 12
    y = draw_lines(d, wrap(d, "NATO SENDS AWACS TO POLAND",
                           font("serif_bold", 40), LW),
                   LX, y, font("serif_bold", 40), leading=46)
    y += 6
    y = draw_lines(d, wrap(d, "Three Russian Kh-101 cruise missiles came down "
                           "on Polish soil on Friday. The alliance holds "
                           "Moscow fully responsible and is weighing more "
                           "defences on its eastern flank.",
                           font("serif", 19), LW),
                   LX, y, font("serif", 19), leading=24)
    y += 6
    d.text((LX, y), "Illustration: an AWACS radar aircraft on patrol.",
           font=font("serif_italic", 14), fill=MUTED)

    # ---- Right column: Ukraine sinks Russian warship ------------------
    RX, RW = 692, W - MX - 692
    warship = fit_image(
        os.path.join(ASSETS,
                     "media-generation-warship-libya-0-17ad341d-c891-44a1-b0bb-74879d18f566.webp"),
        RW, 186)
    page.paste(warship, (RX, LY))
    d.rectangle([RX, LY, RX + RW - 1, LY + 186], outline=RULE, width=1)
    y = LY + 186 + 12
    y = draw_lines(d, wrap(d, "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
                           font("serif_bold", 27), RW),
                   RX, y, font("serif_bold", 27), leading=32)
    y += 6
    y = draw_lines(d, wrap(d, "Kyiv says maritime drones sank the corvette "
                           "Merkury in Benghazi on Sunday — the war reaching "
                           "far beyond Europe.",
                           font("serif", 17), RW),
                   RX, y, font("serif", 17), leading=22)
    # "By the numbers" box fills the rest of the right column.
    # Single-line items only: the box must end before the briefs rule at y=656.
    by = max(y + 16, 516)
    d.line([(RX, by), (RX + RW, by)], fill=RULE, width=1)
    d.text((RX, by + 8), "BY THE NUMBERS", font=font("sans_bold", 13),
           fill=ACCENT)
    ny = by + 30
    num_f = font("serif_bold", 15)
    txt_f = font("serif", 13)
    for num, txt in [("3", "Russian Kh-101 missiles hit Poland"),
                     ("74", "lashes for Iran's singer and team"),
                     ("1,600+", "Delta flights delayed by outage")]:
        d.text((RX, ny), num, font=num_f, fill=INK)
        nw = d.textlength(num, font=num_f)
        d.text((RX + nw + 8, ny + 1), txt, font=txt_f, fill=INK)
        ny += 26
    # vertical divider between the two top stories
    d.line([(680, LY), (680, 640)], fill=(150, 145, 132), width=1)

    # ---- Briefs strip ---------------------------------------------------
    d.line([(MX, 656), (W - MX, 656)], fill=RULE, width=2)
    briefs = [
        ("MIDDLE EAST", "Iran flogs singer and her team",
         "Parastoo Ahmadi and four colleagues get 74 lashes each over a virtual concert."),
        ("AMERICA", "Trump halts Army detonation in Iowa",
         "The president orders a pause on destroying a toxic stockpile of lead azide."),
        ("MARKETS", "Nvidia brings back Jensen Huang",
         "Shares jump about 30% as the board reinstates its chief 11 days after he resigned."),
        ("CLIMATE", "COP31 collapse sparks blame game",
         "Australia faces calls for its minister to quit as Pacific nations voice despair."),
        ("UKRAINE", "Odesa left dark after Russian strikes",
         "The port city loses power, heat and water in the latest bombardment."),
        ("SPORT", "Verstappen wins Las Vegas GP",
         "His third win there in four years, edging Norris by 0.639 seconds in a chaotic race."),
    ]
    col_w = (CW - 24) // 2
    row_h = 106
    for i, (kicker, head, deck) in enumerate(briefs):
        col, row = i % 2, i // 2
        bx = MX + col * (col_w + 24)
        by = 672 + row * row_h
        d.text((bx, by), kicker, font=font("sans_bold", 13), fill=ACCENT)
        y = by + 20
        y = draw_lines(d, wrap(d, head, font("serif_bold", 19), col_w),
                       bx, y, font("serif_bold", 19), leading=23)
        y += 2
        draw_lines(d, wrap(d, deck, font("serif", 14), col_w),
                   bx, y, font("serif", 14), leading=18)
        if col == 0:
            d.line([(MX + col_w + 12, by), (MX + col_w + 12, by + row_h - 14)],
                   fill=(200, 194, 180), width=1)

    # ---- Footer ---------------------------------------------------------
    d.line([(MX, 992), (W - MX, 992)], fill=RULE, width=1)
    foot = "Six stories that defined Tuesday  •  The World Today  •  24 November 2026"
    ff = font("sans", 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1000), foot,
           font=ff, fill=MUTED)

    page.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {page.size[0]}x{page.size[1]}, {size} bytes "
          f"({size / 1024:.0f} KiB, limit 1024 KiB)")


if __name__ == "__main__":
    main()
