"""
archive_daily.py
Copy today's pipeline output files to dated copies (JST).

Files archived:
  data/research_result.json  → data/research_result_YYYYMMDD.json
  data/design_spec.md        → data/design_spec_YYYYMMDD.md
  data/sales_copy.json       → data/sales_copy_YYYYMMDD.json
  data/notion_result.json    → data/notion_result_YYYYMMDD.json
  data/latest_product.json   → data/latest_product_YYYYMMDD.json
  output/thumbnail.png       → output/thumbnail_YYYYMMDD.png
  output/thumbnail_square.png→ output/thumbnail_square_YYYYMMDD.png

Usage:
    python archive_daily.py
"""

import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JST  = timezone(timedelta(hours=9))


def run() -> list[str]:
    date_str = datetime.now(JST).strftime("%Y%m%d")

    targets = [
        (ROOT / "data"   / "research_result.json",    ROOT / "data"   / f"research_result_{date_str}.json"),
        (ROOT / "data"   / "design_spec.md",           ROOT / "data"   / f"design_spec_{date_str}.md"),
        (ROOT / "data"   / "sales_copy.json",          ROOT / "data"   / f"sales_copy_{date_str}.json"),
        (ROOT / "data"   / "notion_result.json",       ROOT / "data"   / f"notion_result_{date_str}.json"),
        (ROOT / "data"   / "latest_product.json",      ROOT / "data"   / f"latest_product_{date_str}.json"),
        (ROOT / "output" / "thumbnail.png",            ROOT / "output" / f"thumbnail_{date_str}.png"),
        (ROOT / "output" / "thumbnail_square.png",     ROOT / "output" / f"thumbnail_square_{date_str}.png"),
    ]

    archived = []
    for src, dst in targets:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"[archive] {src.name} → {dst.name}")
            archived.append(str(dst))
        else:
            print(f"[archive] SKIP (not found): {src.name}")

    print(f"[archive] {len(archived)} file(s) archived for {date_str}.")
    return archived


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    run()
