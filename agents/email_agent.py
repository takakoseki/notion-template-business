"""
Agent: email_agent.py
Role: Read data/twitter_draft.txt and send it via Gmail SMTP.
"""

import logging
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

logger = logging.getLogger("email_agent")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def load_draft() -> str:
    path = ROOT / "data" / "twitter_draft.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"twitter_draft.txt not found: {path}\nRun twitter_agent.py first."
        )
    return path.read_text(encoding="utf-8").strip()


def send_email(draft_text: str) -> None:
    gmail_address = os.getenv("GMAIL_ADDRESS", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_address:
        raise EnvironmentError("GMAIL_ADDRESS is not set in .env")
    if not app_password:
        raise EnvironmentError("GMAIL_APP_PASSWORD is not set in .env")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"Today's X Post Draft - {today}"
    body = f"""\
Today's post draft is ready. Copy and paste to X.

---

{draft_text}

---
Posted by Notion Template Bot
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = gmail_address

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmail_address, app_password)
        smtp.sendmail(gmail_address, gmail_address, msg.as_string())


def run() -> dict:
    logger.info("[email] === Email send started ===")

    draft_text = load_draft()
    logger.info(f"[email] Draft loaded ({len(draft_text)} chars)")

    send_email(draft_text)

    logger.info("[email] Email sent successfully.")
    logger.info("[email] === Email send complete ===")

    return {"status": "sent"}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run()
