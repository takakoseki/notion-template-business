"""
scheduler.py
Daily automation scheduler for the Notion Template Business system.

Schedule:
  06:00 — analytics_agent → orchestrator (agents 1-5) → save latest_product.json
  09:00 — twitter_agent (draft) → email_agent
  21:00 — twitter_agent (draft) → email_agent

Usage:
    python scheduler.py

Keep this process running (terminal, tmux, or Windows Task Scheduler).
"""

import importlib.util
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import schedule
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT))
from log_utils import system_log

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("scheduler")

ANALYTICS_AGENT_PATH        = ROOT / "agents" / "analytics_agent.py"
TWITTER_AGENT_PATH          = ROOT / "agents" / "twitter_agent.py"
EMAIL_AGENT_PATH            = ROOT / "agents" / "email_agent.py"
PIPELINE_NOTIFY_AGENT_PATH  = ROOT / "agents" / "pipeline_notify_agent.py"

PIPELINE_TIME = "06:00"
POST_TIME_AM  = "09:00"
POST_TIME_PM  = "21:00"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_and_run(name: str, path: Path) -> dict:
    spec   = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run()


def _save_latest_product() -> None:
    """Read sales_copy.json (+ notion_result.json) and write latest_product.json."""
    sales_path  = ROOT / "data" / "sales_copy.json"
    notion_path = ROOT / "data" / "notion_result.json"
    out_path    = ROOT / "data" / "latest_product.json"

    if not sales_path.exists():
        logger.warning("sales_copy.json not found; skipping latest_product.json update.")
        return

    sales = json.loads(sales_path.read_text(encoding="utf-8"))

    notion_url = ""
    if notion_path.exists():
        try:
            notion_data = json.loads(notion_path.read_text(encoding="utf-8"))
            notion_url  = notion_data.get("page_url", "")
        except Exception:
            pass

    # Preserve existing gumroad_url if the file already exists
    existing_gumroad_url = ""
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            existing_gumroad_url = existing.get("gumroad_url", "")
        except Exception:
            pass

    product = {
        "title":       sales.get("title", ""),
        "description": sales.get("description", ""),
        "notion_url":  notion_url,
        "created_at":  datetime.now(timezone.utc).isoformat(),
        "gumroad_url": existing_gumroad_url,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(product, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"latest_product.json saved: {product['title']}")
    system_log("scheduler", "info", f"latest_product.json saved: {product['title']}")


# ---------------------------------------------------------------------------
# 06:00 job: analytics → pipeline (agents 1-5) → save product
# ---------------------------------------------------------------------------

def run_pipeline_job() -> None:
    logger.info("=" * 50)
    logger.info("  06:00 Pipeline job started")
    logger.info("=" * 50)
    system_log("scheduler", "started", "06:00 pipeline job started")

    # Step 1: Analytics
    logger.info(">> Step 1: analytics_agent")
    try:
        _load_and_run("analytics_agent", ANALYTICS_AGENT_PATH)
        logger.info("[OK] analytics_agent complete")
        system_log("scheduler", "success", "analytics_agent complete")
    except Exception as e:
        logger.error(f"[SKIP] analytics_agent failed (continuing): {e}")
        system_log("scheduler", "warning", f"analytics_agent failed: {e}")

    # Step 2: Orchestrator agents 1-5
    logger.info(">> Step 2: orchestrator (agents 1-5)")
    try:
        import importlib.util as ilu
        spec   = ilu.spec_from_file_location("orchestrator", ROOT / "orchestrator.py")
        module = ilu.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(start_from=1, end_at=5)
        logger.info("[OK] orchestrator (1-5) complete")
        system_log("scheduler", "success", "orchestrator agents 1-5 complete")
    except Exception as e:
        logger.error(f"[FAIL] orchestrator failed: {e}")
        system_log("scheduler", "error", f"orchestrator failed: {e}")
        return

    # Step 3: Save latest_product.json
    logger.info(">> Step 3: save latest_product.json")
    try:
        _save_latest_product()
        logger.info("[OK] latest_product.json saved")
    except Exception as e:
        logger.error(f"[SKIP] save latest_product failed (continuing): {e}")
        system_log("scheduler", "warning", f"save latest_product failed: {e}")

    # Step 4: Archive dated copies
    logger.info(">> Step 4: archive dated copies")
    try:
        archive_spec = importlib.util.spec_from_file_location("archive_daily", ROOT / "archive_daily.py")
        archive_mod  = importlib.util.module_from_spec(archive_spec)
        archive_spec.loader.exec_module(archive_mod)
        archive_mod.run()
        logger.info("[OK] Archive complete")
        system_log("scheduler", "success", "Daily archive complete")
    except Exception as e:
        logger.error(f"[SKIP] archive failed (continuing): {e}")
        system_log("scheduler", "warning", f"archive failed: {e}")

    # Step 5: Send pipeline notification email (Gumroad content)
    logger.info(">> Step 5: pipeline notification email")
    try:
        _load_and_run("pipeline_notify_agent", PIPELINE_NOTIFY_AGENT_PATH)
        logger.info("[OK] Pipeline notification email sent")
        system_log("scheduler", "success", "Pipeline notification email sent")
    except Exception as e:
        logger.error(f"[SKIP] pipeline_notify_agent failed (continuing): {e}")
        system_log("scheduler", "warning", f"pipeline_notify_agent failed: {e}")

    logger.info("  06:00 Pipeline job complete")
    logger.info("=" * 50)
    system_log("scheduler", "completed", "06:00 pipeline job complete")


# ---------------------------------------------------------------------------
# 09:00 / 21:00 job: twitter draft → email
# ---------------------------------------------------------------------------

def run_post_job(slot: str) -> None:
    logger.info(f"  {slot} Post job started")
    system_log("scheduler", "started", f"{slot} post job started")

    # Step 1: Generate tweet draft
    try:
        result = _load_and_run("twitter_agent", TWITTER_AGENT_PATH)
        logger.info(f"[OK] Tweet draft — type: {result.get('tweet_type')}, chars: {result.get('estimated_chars')}")
        system_log("scheduler", "success", f"Tweet draft generated — {result.get('tweet_type')}")
    except Exception as e:
        logger.error(f"[FAIL] twitter_agent failed: {e}")
        system_log("scheduler", "error", f"twitter_agent failed: {e}")
        return

    # Step 2: Send via email
    try:
        _load_and_run("email_agent", EMAIL_AGENT_PATH)
        logger.info("[OK] Email sent")
        system_log("scheduler", "success", "Email sent")
    except Exception as e:
        logger.error(f"[SKIP] email_agent failed (draft still saved): {e}")
        system_log("scheduler", "warning", f"email_agent failed: {e}")

    logger.info(f"  {slot} Post job complete")


def run_post_job_am() -> None:
    run_post_job("09:00")


def run_post_job_pm() -> None:
    run_post_job("21:00")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("=" * 60)
    logger.info("  Notion Template Business — Scheduler")
    logger.info("=" * 60)
    logger.info(f"  {PIPELINE_TIME} — analytics + product pipeline (agents 1-5)")
    logger.info(f"  {POST_TIME_AM}  — tweet draft + email")
    logger.info(f"  {POST_TIME_PM}  — tweet draft + email")
    logger.info("  Press Ctrl+C to stop.")
    logger.info("=" * 60)

    schedule.every().day.at(PIPELINE_TIME).do(run_pipeline_job)
    schedule.every().day.at(POST_TIME_AM).do(run_post_job_am)
    schedule.every().day.at(POST_TIME_PM).do(run_post_job_pm)

    for job in schedule.jobs:
        logger.info(f"Scheduled: {job}")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        sys.exit(0)
