"""
Agent 5: publish_agent.py
Role: Read sales_copy.json and output/thumbnail.png, attempt to register the
      product on Gumroad via API (draft), and output a manual-registration
      summary to output/publish_summary.txt if the API is unavailable.
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

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

GUMROAD_API_BASE = "https://api.gumroad.com/v2"


def load_notion_result() -> dict:
    """Load Notion creation result if notion_agent has already run."""
    path = ROOT / "data" / "notion_result.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_sales_copy() -> dict:
    path = ROOT / "data" / "sales_copy.json"
    if not path.exists():
        raise FileNotFoundError(
            f"sales_copy.json not found: {path}\nRun copy_agent.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_full_description(sales_copy: dict) -> str:
    """Assemble the full Gumroad product description."""
    description = sales_copy["description"]
    features = "\n".join(f"* {f}" for f in sales_copy["features"])
    faq_lines = []
    for item in sales_copy["faq"]:
        faq_lines.append(f"**{item['q']}**\n{item['a']}")
    faq_text = "\n\n".join(faq_lines)
    return (
        f"{description}\n\n"
        f"## What's included\n{features}\n\n"
        f"## FAQ\n{faq_text}"
    )


def try_create_gumroad_product(sales_copy: dict, access_token: str) -> dict | None:
    """
    Attempt to create a Gumroad product via API (draft).
    Returns None if the endpoint is unavailable instead of raising.
    """
    price_cents = int(float(sales_copy["price"]["usd"]) * 100)
    payload = {
        "access_token": access_token,
        "name": sales_copy["title"],
        "description": build_full_description(sales_copy),
        "price": price_cents,
        "published": "false",
        "type": "digital",
    }
    try:
        resp = requests.post(f"{GUMROAD_API_BASE}/products", data=payload, timeout=30)
        if resp.status_code == 404:
            return None  # endpoint deprecated
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            return None
        return data["product"]
    except requests.HTTPError:
        return None


def upload_thumbnail(product_id: str, thumbnail_path: Path, access_token: str) -> None:
    """Upload a thumbnail image to a Gumroad product."""
    if not thumbnail_path.exists():
        print(f"[publish] WARNING: Thumbnail not found: {thumbnail_path}")
        return

    with open(thumbnail_path, "rb") as f:
        files = {"cover_image": ("thumbnail.png", f, "image/png")}
        data = {"access_token": access_token}
        resp = requests.put(
            f"{GUMROAD_API_BASE}/products/{product_id}",
            data=data,
            files=files,
            timeout=60,
        )

    try:
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            print(f"[publish] WARNING: Thumbnail upload failed: {result.get('message')}")
        else:
            print("[publish] Thumbnail uploaded successfully.")
    except requests.HTTPError as e:
        print(f"[publish] WARNING: Thumbnail upload error: {e}")


def build_summary_line(sales_copy: dict) -> str:
    """Generate a 1-2 sentence Gumroad Summary field starting with 'You'll get...'"""
    features = sales_copy["features"]
    f1 = features[0].rstrip(".") if features else ""
    f2 = features[1].rstrip(".") if len(features) > 1 else ""
    if f1 and f2:
        return f"You'll get {f1.lower()}, and {f2.lower()}."
    elif f1:
        return f"You'll get {f1.lower()}."
    return "You'll get everything you need to build lasting habits in Notion."


def save_publish_summary(sales_copy: dict, thumbnail_path: Path, notion_result: dict | None = None) -> Path:
    """Save a manual Gumroad registration summary to output/publish_summary.txt."""
    full_desc = build_full_description(sales_copy)
    features = sales_copy["features"]
    faq = sales_copy["faq"]
    square_path = thumbnail_path.parent / "thumbnail_square.png"

    detail1_items = "\n".join(f"  * {f}" for f in features)

    detail2_qa = ""
    if len(faq) >= 2:
        detail2_qa = (
            f"  Q: {faq[0]['q']}\n"
            f"  A: {faq[0]['a']}\n\n"
            f"  Q: {faq[1]['q']}\n"
            f"  A: {faq[1]['a']}"
        )
    elif faq:
        detail2_qa = f"  Q: {faq[0]['q']}\n  A: {faq[0]['a']}"

    detail3_qa = ""
    if len(faq) >= 3:
        detail3_qa = (
            f"  Q: {faq[2]['q']}\n"
            f"  A: {faq[2]['a']}\n\n"
            "  Support: After purchase, reach out via Gumroad's messaging feature "
            "and I'll respond within 2 business days."
        )

    lines = [
        "=" * 60,
        "  Gumroad Manual Registration Summary",
        "=" * 60,
        "",
        "[Product Title]",
        f"  {sales_copy['title']}",
        "",
        "[Price]",
        f"  ${sales_copy['price']['usd']}",
        "",
        "[Description — paste into Gumroad Description field]",
        "-" * 40,
        full_desc,
        "-" * 40,
        "",
        "[Gumroad Summary field]",
        "-" * 40,
        build_summary_line(sales_copy),
        "-" * 40,
        "",
        "[Gumroad Additional Details]",
        "-" * 40,
        "Detail 1 Title: What's Included",
        detail1_items,
        "",
        "Detail 2 Title: Frequently Asked Questions",
        detail2_qa,
        "",
        "Detail 3 Title: More Questions & Support",
        detail3_qa,
        "-" * 40,
        "",
        "[Notion Template Link]",
        *(
            [
                f"  Page  : {notion_result.get('page_title', '')}",
                f"  URL   : {notion_result.get('page_url', '')}",
                "  NOTE  : Enable 'Share to web' in Notion to get the public link.",
            ]
            if notion_result and notion_result.get("page_url")
            else [
                "  * Add the shareable Notion link here after publishing the template",
                "  (e.g. https://your-workspace.notion.site/xxxxxxxx)",
            ]
        ),
        "",
        "[Thumbnail Image Paths]",
        f"  Landscape (1200x630) : {thumbnail_path}",
        f"  Square   (1200x1200) : {square_path}",
        "",
        "[Registration Steps]",
        "  1. Open https://app.gumroad.com/products/new",
        "  2. Copy and paste the title, price, and description above",
        "  3. Paste the Summary field text into the Summary box",
        "  4. Add Detail 1-3 under Additional Details",
        "  5. Add the Notion template link to the product file or description",
        "  6. Upload the thumbnail image (landscape or square)",
        "  7. Review all details and publish",
        "",
        "=" * 60,
    ]
    summary_text = "\n".join(lines)

    out_path = thumbnail_path.parent / "publish_summary.txt"
    out_path.write_text(summary_text, encoding="utf-8")
    return out_path


def run() -> dict:
    print("[publish] === Gumroad publish started ===")

    access_token = os.getenv("GUMROAD_ACCESS_TOKEN")
    if not access_token:
        raise EnvironmentError("GUMROAD_ACCESS_TOKEN is not set.")

    sales_copy = load_sales_copy()
    notion_result = load_notion_result()
    thumbnail_path = ROOT / "output" / "thumbnail.png"

    print(f"[publish] Product : {sales_copy['title']}")
    print(f"[publish] Price   : ${sales_copy['price']['usd']}")

    product = try_create_gumroad_product(sales_copy, access_token)

    if product:
        product_id = product["id"]
        product_url = product.get("short_url") or product.get("url", "")
        upload_thumbnail(product_id, thumbnail_path, access_token)
        result = {
            "product_id": product_id,
            "product_url": product_url,
            "name": product.get("name"),
            "price_usd": sales_copy["price"]["usd"],
            "status": "draft (registered via API)",
        }
        print(f"[publish] ============================================")
        print(f"[publish]  Product registered (draft)")
        print(f"[publish]  Title  : {result['name']}")
        print(f"[publish]  Price  : ${result['price_usd']}")
        print(f"[publish]  URL    : {product_url}")
        print(f"[publish]  Review and publish from Gumroad dashboard.")
        print(f"[publish] ============================================")
    else:
        print("[publish] INFO: Gumroad product creation API is unavailable. Generating manual summary.")
        summary_path = save_publish_summary(sales_copy, thumbnail_path, notion_result)
        result = {
            "product_id": None,
            "product_url": "https://app.gumroad.com/products/new",
            "name": sales_copy["title"],
            "price_usd": sales_copy["price"]["usd"],
            "status": "manual_required",
            "summary_path": str(summary_path),
        }
        print(f"[publish] ============================================")
        print(f"[publish]  Manual summary saved")
        print(f"[publish]  File      : {summary_path}")
        print(f"[publish]  Title     : {result['name']}")
        print(f"[publish]  Price     : ${result['price_usd']}")
        print(f"[publish]  Register  : https://app.gumroad.com/products/new")
        print(f"[publish]  Thumbnail : {thumbnail_path}")
        print(f"[publish] ============================================")

    print("[publish] === Gumroad publish complete ===")
    return result


if __name__ == "__main__":
    run()
