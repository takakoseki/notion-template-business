"""
orchestrator.py
Role: Invoke Agents 1-5 in sequence and manage the overall workflow.

Usage:
    python orchestrator.py
    python orchestrator.py --start-from 3   # Resume from Agent 3
    python orchestrator.py --end-at 3       # Stop after Agent 3
"""

import argparse
import logging
import sys
import time
import traceback
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("orchestrator")


# ---------------------------------------------------------------------------
# Agent runner
# ---------------------------------------------------------------------------

def run_agent(name: str, module_path: str) -> dict:
    """Load and execute the run() function of the specified agent module."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "run"):
        raise AttributeError(f"run() function not found in {module_path}")

    return module.run()


AGENTS = [
    {
        "id": 1,
        "name": "research_agent",
        "label": "Research (trending theme analysis)",
        "path": str(ROOT / "agents" / "research_agent.py"),
    },
    {
        "id": 2,
        "name": "design_agent",
        "label": "Design (template specification generation)",
        "path": str(ROOT / "agents" / "design_agent.py"),
    },
    {
        "id": 3,
        "name": "copy_agent",
        "label": "Copy (sales copy generation)",
        "path": str(ROOT / "agents" / "copy_agent.py"),
    },
    {
        "id": 4,
        "name": "thumbnail_agent",
        "label": "Thumbnail (image generation)",
        "path": str(ROOT / "agents" / "thumbnail_agent.py"),
    },
    {
        "id": 5,
        "name": "notion_agent",
        "label": "Notion (template page and database creation)",
        "path": str(ROOT / "agents" / "notion_agent.py"),
    },
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(start_from: int = 1, end_at: int = 5) -> None:
    logger.info("=" * 60)
    logger.info("  Notion Template Business Automation Orchestrator")
    logger.info("=" * 60)

    results: dict[str, dict] = {}

    agents_to_run = [a for a in AGENTS if a["id"] >= start_from and a["id"] <= end_at]

    if start_from > 1:
        logger.info(f"Resuming from Agent {start_from}.")
    if end_at < 5:
        logger.info(f"Stopping after Agent {end_at}.")

    for agent in agents_to_run:
        agent_id = agent["id"]
        label = agent["label"]

        logger.info("")
        logger.info(f">> Agent {agent_id}: {label}")
        logger.info("-" * 40)

        start_time = time.time()
        try:
            result = run_agent(agent["name"], agent["path"])
            elapsed = time.time() - start_time
            results[agent["name"]] = result
            logger.info(f"[OK] Agent {agent_id} complete ({elapsed:.1f}s)")

        except KeyboardInterrupt:
            logger.error("Interrupted by user.")
            sys.exit(1)

        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"Agent {agent_id} ({label}) failed: {type(e).__name__}: {e}"
            logger.error(f"[FAIL] {error_msg} ({elapsed:.1f}s)")
            logger.debug(traceback.format_exc())
            print("\n" + "=" * 60)
            print("Error details:")
            print(traceback.format_exc())
            print("=" * 60)
            sys.exit(1)

    # Summary
    print("\n")
    logger.info("=" * 60)
    logger.info("  All agents complete")
    logger.info("=" * 60)
    logger.info("Summary")

    if "research_agent" in results:
        themes = results["research_agent"].get("top5_themes", [])
        if themes:
            logger.info(f"  Top theme : {themes[0]['theme']} (score: {themes[0]['total_score']})")

    if "design_agent" in results:
        logger.info(f"  Design spec : {results['design_agent'].get('output_path', 'data/design_spec.md')}")

    if "copy_agent" in results:
        c = results["copy_agent"]
        logger.info(f"  Title  : {c.get('title', '-')}")
        logger.info(f"  Price  : ${c.get('price', {}).get('usd', '-')}")

    if "thumbnail_agent" in results:
        logger.info(f"  Thumbnail : {results['thumbnail_agent'].get('output_path', 'output/thumbnail.png')}")

    if "notion_agent" in results:
        n = results["notion_agent"]
        logger.info(f"  Notion URL  : {n.get('page_url', '-')}")
        logger.info(f"  Databases   : {n.get('databases_created', 0)}")

    logger.info("")
    logger.info("  Next: register the product on Gumroad, then run:")
    logger.info("  python update_gumroad_url.py <url>")
    logger.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Notion Template Business Automation Orchestrator"
    )
    parser.add_argument(
        "--start-from",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5],
        help="Resume from the specified agent number (default: 1)",
    )
    parser.add_argument(
        "--end-at",
        type=int,
        default=5,
        choices=[1, 2, 3, 4, 5],
        help="Stop after the specified agent number (default: 5)",
    )
    args = parser.parse_args()
    main(start_from=args.start_from, end_at=args.end_at)
