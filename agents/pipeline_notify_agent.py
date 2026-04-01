"""
Agent: pipeline_notify_agent.py
Role: After the 06:00 pipeline, send an email with all Gumroad registration
      content ready to copy-paste (Description, Content field, basic info).
"""

import json
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT))
from log_utils import system_log

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sales_copy() -> dict:
    path = ROOT / "data" / "sales_copy.json"
    if not path.exists():
        raise FileNotFoundError(f"sales_copy.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_notion_result() -> dict:
    path = ROOT / "data" / "notion_result.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_latest_product() -> dict:
    path = ROOT / "data" / "latest_product.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def build_gumroad_description(sales_copy: dict) -> str:
    """
    Build a plain-text Gumroad Description that pastes cleanly
    without markdown artifacts.
    """
    lines = []

    # Main description
    lines.append(sales_copy.get("description", ""))
    lines.append("")

    # What's included
    lines.append("--------------------------------------------------")
    lines.append("WHAT'S INCLUDED")
    lines.append("--------------------------------------------------")
    for f in sales_copy.get("features", []):
        lines.append(f"- {f}")
    lines.append("")

    # FAQ
    faq = sales_copy.get("faq", [])
    if faq:
        lines.append("--------------------------------------------------")
        lines.append("FAQ")
        lines.append("--------------------------------------------------")
        for item in faq:
            lines.append(f"Q: {item['q']}")
            lines.append(f"A: {item['a']}")
            lines.append("")

    return "\n".join(lines).strip()


def build_gumroad_content(sales_copy: dict, notion_result: dict) -> str:
    """
    Build the Gumroad 'Content' field text (shown to buyers after purchase).
    Uses the public Notion URL if available.
    """
    notion_url = notion_result.get("page_url", "")
    # Prefer a known public notion.site URL from latest_product if stored
    latest = load_latest_product()
    # notion_url stays as-is (user will update to public URL via update_gumroad_url / Share to web)

    title = sales_copy.get("title", "Notion Template")

    lines = [
        "Thank you for your purchase! 🎉",
        "",
        "Click the link below to access your Notion template:",
        "",
        notion_url if notion_url else "(Add your public Notion Share link here)",
        "",
        "How to duplicate:",
        "",
        "1. Click the link above",
        "2. Click \"Duplicate\" in the top right corner",
        "3. The template will be added to your Notion workspace",
        "4. Start using it right away!",
        "",
        "If you have any questions, contact me via Gumroad messaging.",
        "I'll respond within 2 business days.",
    ]
    return "\n".join(lines)


def build_summary_line(sales_copy: dict) -> str:
    features = sales_copy.get("features", [])
    f1 = features[0].rstrip(".") if features else ""
    f2 = features[1].rstrip(".") if len(features) > 1 else ""
    if f1 and f2:
        return f"You'll get {f1.lower()}, and {f2.lower()}."
    elif f1:
        return f"You'll get {f1.lower()}."
    return "You'll get everything you need in Notion."


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------

def send_pipeline_email(sales_copy: dict, notion_result: dict) -> None:
    gmail_address = os.getenv("GMAIL_ADDRESS", "").strip()
    app_password  = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_address:
        raise EnvironmentError("GMAIL_ADDRESS is not set in .env")
    if not app_password:
        raise EnvironmentError("GMAIL_APP_PASSWORD is not set in .env")

    title     = sales_copy.get("title", "")
    price     = sales_copy.get("price", {}).get("usd", "")
    today     = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    notion_url = notion_result.get("page_url", "(not available)")

    description = build_gumroad_description(sales_copy)
    content     = build_gumroad_content(sales_copy, notion_result)
    summary     = build_summary_line(sales_copy)

    sep = "=" * 60

    body = f"""\
Pipeline complete for {today}. Gumroad registration content is below.

{sep}
PRODUCT INFO
{sep}
Title : {title}
Price : ${price}
Notion: {notion_url}

NOTE: The Notion URL above is private. Before setting it in Gumroad Content,
enable "Share to web" in Notion and replace with the public notion.site link.

{sep}
GUMROAD — Description field
(Copy everything between the dashes and paste into the Description box)
{sep}
{description}
{sep}

{sep}
GUMROAD — Summary field (1-2 sentences below the title)
{sep}
{summary}
{sep}

{sep}
GUMROAD — Content field (shown to buyers after purchase)
{sep}
{content}
{sep}

{sep}
NEXT STEPS
{sep}
1. Open https://app.gumroad.com/products/new (or edit existing product)
2. Paste Description, Summary, and Content from above
3. Enable "Share to web" in Notion → copy public URL → update Content field
4. Upload thumbnail: output/thumbnail.png (1200x630 for Cover)
5. Run: python update_gumroad_url.py https://takasoccerfan.gumroad.com/l/XXXXX
6. git add -f data/latest_product.json && git commit -m "update gumroad url" && git push
{sep}
"""

    subject = f"[Pipeline] New product ready: {title} ({today})"
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"]    = gmail_address
    msg["To"]      = gmail_address

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmail_address, app_password)
        smtp.sendmail(gmail_address, gmail_address, msg.as_string())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> dict:
    print("[pipeline_notify] === Pipeline notification started ===")
    system_log("pipeline_notify_agent", "started", "Pipeline notification started")

    sales_copy    = load_sales_copy()
    notion_result = load_notion_result()

    title = sales_copy.get("title", "")
    print(f"[pipeline_notify] Product: {title}")

    send_pipeline_email(sales_copy, notion_result)

    print("[pipeline_notify] Email sent successfully.")
    system_log("pipeline_notify_agent", "success", f"Pipeline notification email sent: {title}")
    print("[pipeline_notify] === Pipeline notification complete ===")

    return {"status": "sent", "title": title}


if __name__ == "__main__":
    run()
