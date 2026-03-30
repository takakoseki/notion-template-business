"""
generate_twitter_images.py
Generate Twitter/X profile and banner images using Pillow.

Outputs:
  output/twitter_profile.png  400x400
  output/twitter_banner.png  1500x500
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

# Windows system fonts (tried in order)
FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",   # Segoe UI Bold
    "C:/Windows/Fonts/arialbd.ttf",    # Arial Bold
    "C:/Windows/Fonts/calibrib.ttf",   # Calibri Bold
    "C:/Windows/Fonts/verdanab.ttf",   # Verdana Bold
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    print(f"[warn] No TrueType font found; using default (text may look small)")
    return ImageFont.load_default()


def draw_centered_text(draw, canvas_box, text, font, fill):
    """Draw text centered within canvas_box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = canvas_box
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - w) // 2 - bbox[0]
    y = y0 + (y1 - y0 - h) // 2 - bbox[1]
    draw.text((x, y), text, fill=fill, font=font)


# ---------------------------------------------------------------------------
# Profile image  400x400
# ---------------------------------------------------------------------------

def create_profile() -> None:
    W, H = 400, 400
    img = Image.new("RGB", (W, H), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = load_font(230)
    draw_centered_text(draw, (0, 0, W, H), "T", font, fill=(255, 255, 255))

    out = OUTPUT / "twitter_profile.png"
    img.save(out)
    print(f"Saved: {out}")


# ---------------------------------------------------------------------------
# Banner image  1500x500
# ---------------------------------------------------------------------------

def create_banner() -> None:
    W, H = 1500, 500
    img = Image.new("RGB", (W, H), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_title    = load_font(96)
    font_subtitle = load_font(40)

    # --- Left text block ---
    TEXT_X = 80

    # Measure title to vertically center the text block
    title_text    = "Notion Templates"
    subtitle_text = "Productivity tools for modern life"
    GAP = 24  # gap between title and subtitle

    t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    s_bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    t_h = t_bbox[3] - t_bbox[1]
    s_h = s_bbox[3] - s_bbox[1]
    block_h = t_h + GAP + s_h
    block_y = (H - block_h) // 2

    # Title
    title_y = block_y - t_bbox[1]
    draw.text((TEXT_X, title_y), title_text, fill=(255, 255, 255), font=font_title)

    # Subtitle
    subtitle_y = block_y + t_h + GAP - s_bbox[1]
    draw.text((TEXT_X, subtitle_y), subtitle_text, fill=(160, 160, 160), font=font_subtitle)

    # --- Right icon: Notion-style white rounded square with black "N" ---
    ICON_SIZE = 260
    ICON_X = 1150
    ICON_Y = (H - ICON_SIZE) // 2
    RADIUS = 48

    draw.rounded_rectangle(
        [ICON_X, ICON_Y, ICON_X + ICON_SIZE, ICON_Y + ICON_SIZE],
        radius=RADIUS,
        fill=(255, 255, 255),
    )

    font_icon = load_font(170)
    draw_centered_text(
        draw,
        (ICON_X, ICON_Y, ICON_X + ICON_SIZE, ICON_Y + ICON_SIZE),
        "N",
        font_icon,
        fill=(0, 0, 0),
    )

    out = OUTPUT / "twitter_banner.png"
    img.save(out)
    print(f"Saved: {out}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    create_profile()
    create_banner()
    print("Done.")
