"""
Agent 4: thumbnail_agent.py
Role: Read title and features from sales_copy.json, generate an HTML thumbnail
      via Jinja2, convert it to a 1200x630px PNG with Playwright, and save to
      output/thumbnail.png
"""

import json
import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from jinja2 import Environment, BaseLoader

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1200" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      width: 1200px;
      height: 630px;
      font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .container {
      width: 1100px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .badge {
      display: inline-block;
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 20px;
      padding: 6px 18px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      width: fit-content;
    }

    .title {
      font-size: {{ title_font_size }}px;
      font-weight: 800;
      line-height: 1.15;
      background: linear-gradient(90deg, #fff 0%, #c5b4e3 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .features {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .feature {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-size: 18px;
      line-height: 1.4;
      color: rgba(255,255,255,0.85);
    }

    .feature-icon {
      flex-shrink: 0;
      width: 22px;
      height: 22px;
      background: linear-gradient(135deg, #a78bfa, #60a5fa);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      color: white;
      margin-top: 2px;
    }

    .footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .notion-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
      color: rgba(255,255,255,0.6);
      font-weight: 600;
    }

    .notion-icon {
      width: 30px;
      height: 30px;
      background: white;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      font-weight: 900;
      color: #000;
    }

    .price-tag {
      background: linear-gradient(135deg, #a78bfa, #60a5fa);
      border-radius: 12px;
      padding: 8px 22px;
      font-size: 18px;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div style="position:absolute;top:-120px;right:-120px;width:500px;height:500px;border-radius:50%;background:#a78bfa;opacity:0.08;"></div>
  <div style="position:absolute;bottom:-80px;left:-80px;width:350px;height:350px;border-radius:50%;background:#60a5fa;opacity:0.08;"></div>

  <div class="container">
    <div class="badge">✦ Notion Template</div>

    <div class="title">{{ title }}</div>

    <div class="features">
      {% for f in features %}
      <div class="feature">
        <div class="feature-icon">{{ loop.index }}</div>
        <span>{{ f }}</span>
      </div>
      {% endfor %}
    </div>

    <div class="footer">
      <div class="notion-logo">
        <div class="notion-icon">N</div>
        Notion Template
      </div>
      <div class="price-tag">${{ price }}</div>
    </div>
  </div>
</body>
</html>
"""


def load_sales_copy() -> dict:
    path = ROOT / "data" / "sales_copy.json"
    if not path.exists():
        raise FileNotFoundError(
            f"sales_copy.json not found: {path}\nRun copy_agent.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def render_html(sales_copy: dict) -> str:
    """Render the HTML thumbnail using Jinja2."""
    title = sales_copy["title"]
    features = sales_copy["features"]
    price_usd = sales_copy["price"]["usd"]

    title_len = len(title)
    if title_len <= 30:
        font_size = 64
    elif title_len <= 50:
        font_size = 52
    else:
        font_size = 44

    env = Environment(loader=BaseLoader())
    tmpl = env.from_string(HTML_TEMPLATE)
    return tmpl.render(
        title=title,
        features=features[:3],
        price=price_usd,
        title_font_size=font_size,
    )


def html_to_png(html_content: str, output_path: Path) -> None:
    """Convert HTML to a 1200x630px PNG using Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "playwright is not installed.\n"
            "Run: pip install playwright && playwright install chromium"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        page.set_content(html_content, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(output_path), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()


def run() -> dict:
    print("[thumbnail] === Thumbnail generation started ===")

    sales_copy = load_sales_copy()
    html_content = render_html(sales_copy)

    html_path = ROOT / "output" / "thumbnail.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[thumbnail] HTML saved to {html_path}")

    output_path = ROOT / "output" / "thumbnail.png"
    print("[thumbnail] Converting to PNG with Playwright...")
    html_to_png(html_content, output_path)

    print(f"[thumbnail] Thumbnail saved to {output_path} (1200x630px)")

    # Generate square version (1200x1200) for social media / Gumroad
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("resize_square", ROOT / "resize_square.py")
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _mod.main()
    print("[thumbnail] Square thumbnail saved (1200x1200px)")

    print("[thumbnail] === Thumbnail generation complete ===")

    return {"output_path": str(output_path)}


if __name__ == "__main__":
    run()
