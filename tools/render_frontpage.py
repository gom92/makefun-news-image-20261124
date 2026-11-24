#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261124.

Builds a 1024x1024 newspaper front page summing up Tuesday 24 November
2026, using Pillow for every letter on the page (AI image tools garble
text, so only the two editorial illustrations in ../assets/ are
AI-generated, and they carry no text at all).

Run:  python3 tools/render_frontpage.py
Out:  entry.png  (1024x1024, must stay under 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ASSET_DIR = os.path.join(REPO_ROOT, "assets")
OUTPUT_PATH = os.path.join(REPO_ROOT, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 28
PAPER = (247, 243, 234)  # newsprint off-white
INK = (18, 18, 18)  # near-black
RULE = (18, 18, 18)
ACCENT = (158, 27, 24)  # deep newspaper red
MUTED = (90, 86, 78)

FONT_CANDIDATES = {
    "serif_bold": ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                   "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
    "serif": ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"),
    "serif_italic": ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
                     "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"),
    "sans_bold": ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    "sans": ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
}


def pick_font(style, size):
    for candidate in FONT_CANDIDATES[style]:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(canvas, text, face, max_width):
    """Greedy word wrap; returns the lines that fit inside max_width."""
    wrapped, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                wrapped.append(current)
            current = word
    if current:
        wrapped.append(current)
    return wrapped


def draw_wrapped(canvas, lines, x, y, face, fill=INK, leading=None):
    if leading is None:
        leading = int(face.size * 1.18)
    for line in lines:
        canvas.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def cover_image(path, width, height):
    """Open an image, centre-crop it to the target aspect, resize it."""
    picture = Image.open(path).convert("RGB")
    src_w, src_h = picture.size
    scale = max(width / src_w, height / src_h)
    picture = picture.resize(
        (int(src_w * scale + 0.5), int(src_h * scale + 0.5)), Image.LANCZOS)
    left = (picture.width - width) // 2
    top = (picture.height - height) // 2
    return picture.crop((left, top, left + width, top + height))


def draw_masthead(canvas):
    masthead = pick_font("serif_bold", 66)
    title = "THE WORLD TODAY"
    title_w = canvas.textlength(title, font=masthead)
    canvas.text(((PAGE_W - title_w) / 2, 14), title, font=masthead, fill=INK)
    canvas.line([(MARGIN, 96), (PAGE_W - MARGIN, 96)], fill=RULE, width=3)
    canvas.line([(MARGIN, 101), (PAGE_W - MARGIN, 101)], fill=RULE, width=1)
    small = pick_font("sans_bold", 15)
    canvas.text((MARGIN, 110), "TUESDAY, 24 NOVEMBER 2026", font=small, fill=INK)
    tagline = "THE DAY'S NEWS IN ONE PAGE"
    canvas.text((PAGE_W - MARGIN - canvas.textlength(tagline, font=small), 110),
                tagline, font=small, fill=INK)
    canvas.line([(MARGIN, 134), (PAGE_W - MARGIN, 134)], fill=RULE, width=2)


def draw_lead(canvas, page):
    left, width, top = MARGIN, 640, 148
    lead_art = cover_image(
        os.path.join(ASSET_DIR,
                     "media-generation-awacs-lead-0-9ca43ab1-dd78-47b8-b2fd-215180b194a8.webp"),
        width, 272)
    page.paste(lead_art, (left, top))
    canvas.rectangle([left, top, left + width - 1, top + 272], outline=RULE, width=1)
    y = top + 272 + 12
    head_face = pick_font("serif_bold", 40)
    head = "NATO SENDS AWACS TO POLAND"
    y = draw_wrapped(canvas, wrap_text(canvas, head, head_face, width),
                     left, y, head_face, leading=46)
    y += 6
    deck_face = pick_font("serif", 19)
    deck = ("Three Russian Kh-101 cruise missiles came down on Polish soil "
            "on Friday. The alliance holds Moscow fully responsible and is "
            "weighing more defences on its eastern flank.")
    y = draw_wrapped(canvas, wrap_text(canvas, deck, deck_face, width),
                     left, y, deck_face, leading=24)
    y += 6
    canvas.text((left, y), "Illustration: an AWACS radar aircraft on patrol.",
                font=pick_font("serif_italic", 14), fill=MUTED)


def draw_side(canvas, page):
    left, width, top = 692, PAGE_W - MARGIN - 692, 148
    side_art = cover_image(
        os.path.join(ASSET_DIR,
                     "media-generation-warship-libya-0-17ad341d-c891-44a1-b0bb-74879d18f566.webp"),
        width, 186)
    page.paste(side_art, (left, top))
    canvas.rectangle([left, top, left + width - 1, top + 186], outline=RULE, width=1)
    y = top + 186 + 12
    head_face = pick_font("serif_bold", 27)
    head = "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA"
    y = draw_wrapped(canvas, wrap_text(canvas, head, head_face, width),
                     left, y, head_face, leading=32)
    y += 6
    deck_face = pick_font("serif", 17)
    deck = ("Kyiv says maritime drones sank the corvette Merkury in Benghazi "
            "on Sunday — the war reaching far beyond Europe.")
    y = draw_wrapped(canvas, wrap_text(canvas, deck, deck_face, width),
                     left, y, deck_face, leading=22)
    # The "By the numbers" box fills the rest of the right column.
    # Items are single lines only: the box must end before the briefs
    # rule at y=656.
    box_top = max(y + 16, 516)
    canvas.line([(left, box_top), (left + width, box_top)], fill=RULE, width=1)
    canvas.text((left, box_top + 8), "BY THE NUMBERS",
                font=pick_font("sans_bold", 13), fill=ACCENT)
    row_y = box_top + 30
    num_face = pick_font("serif_bold", 15)
    label_face = pick_font("serif", 13)
    figures = [
        {"value": "3", "label": "Russian Kh-101 missiles hit Poland"},
        {"value": "74", "label": "lashes for Iran's singer and team"},
        {"value": "1,600+", "label": "Delta flights delayed by outage"},
    ]
    for figure in figures:
        canvas.text((left, row_y), figure["value"], font=num_face, fill=INK)
        value_w = canvas.textlength(figure["value"], font=num_face)
        canvas.text((left + value_w + 8, row_y + 1), figure["label"],
                    font=label_face, fill=INK)
        row_y += 26
    # vertical divider between the two top stories
    canvas.line([(680, top), (680, 640)], fill=(150, 145, 132), width=1)


def draw_briefs(canvas):
    content_w = PAGE_W - 2 * MARGIN
    canvas.line([(MARGIN, 656), (PAGE_W - MARGIN, 656)], fill=RULE, width=2)
    briefs = [
        {"tag": "MIDDLE EAST",
         "head": "Iran flogs singer and her team",
         "deck": "Parastoo Ahmadi and four colleagues get 74 lashes each over a virtual concert."},
        {"tag": "AMERICA",
         "head": "Trump halts Army detonation in Iowa",
         "deck": "The president orders a pause on destroying a toxic stockpile of lead azide."},
        {"tag": "MARKETS",
         "head": "Nvidia brings back Jensen Huang",
         "deck": "Shares jump about 30% as the board reinstates its chief 11 days after he resigned."},
        {"tag": "CLIMATE",
         "head": "COP31 collapse sparks blame game",
         "deck": "Australia faces calls for its minister to quit as Pacific nations voice despair."},
        {"tag": "UKRAINE",
         "head": "Odesa left dark after Russian strikes",
         "deck": "The port city loses power, heat and water in the latest bombardment."},
        {"tag": "SPORT",
         "head": "Verstappen wins Las Vegas GP",
         "deck": "His third win there in four years, edging Norris by 0.639 seconds in a chaotic race."},
    ]
    col_w = (content_w - 24) // 2
    row_h = 106
    for index, brief in enumerate(briefs):
        col, row = index % 2, index // 2
        bx = MARGIN + col * (col_w + 24)
        by = 672 + row * row_h
        canvas.text((bx, by), brief["tag"], font=pick_font("sans_bold", 13),
                    fill=ACCENT)
        y = by + 20
        head_face = pick_font("serif_bold", 19)
        y = draw_wrapped(canvas, wrap_text(canvas, brief["head"], head_face, col_w),
                         bx, y, head_face, leading=23)
        y += 2
        deck_face = pick_font("serif", 14)
        draw_wrapped(canvas, wrap_text(canvas, brief["deck"], deck_face, col_w),
                     bx, y, deck_face, leading=18)
        if col == 0:
            canvas.line([(MARGIN + col_w + 12, by),
                         (MARGIN + col_w + 12, by + row_h - 14)],
                        fill=(200, 194, 180), width=1)


def draw_footer(canvas):
    canvas.line([(MARGIN, 992), (PAGE_W - MARGIN, 992)], fill=RULE, width=1)
    foot = "Six stories that defined Tuesday  •  The World Today  •  24 November 2026"
    foot_face = pick_font("sans", 13)
    canvas.text(((PAGE_W - canvas.textlength(foot, font=foot_face)) / 2, 1000),
                foot, font=foot_face, fill=MUTED)


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    canvas = ImageDraw.Draw(page)
    draw_masthead(canvas)
    draw_lead(canvas, page)
    draw_side(canvas, page)
    draw_briefs(canvas)
    draw_footer(canvas)
    page.save(OUTPUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUTPUT_PATH)
    print(f"wrote {OUTPUT_PATH}: {page.size[0]}x{page.size[1]}, {size} bytes "
          f"({size / 1024:.0f} KiB, limit 1024 KiB)")


if __name__ == "__main__":
    main()
