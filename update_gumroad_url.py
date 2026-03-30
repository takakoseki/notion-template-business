"""
update_gumroad_url.py
Update the gumroad_url field in data/latest_product.json after manual Gumroad registration.

Usage:
    python update_gumroad_url.py https://takasoccerfan.gumroad.com/l/xxxxx
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python update_gumroad_url.py <gumroad_url>")
        print("Example: python update_gumroad_url.py https://takasoccerfan.gumroad.com/l/xxxxx")
        sys.exit(1)

    url = sys.argv[1].strip()

    if not url.startswith("https://"):
        print(f"[ERROR] URL must start with https://  Got: {url}")
        sys.exit(1)

    path = ROOT / "data" / "latest_product.json"
    if not path.exists():
        print(f"[ERROR] latest_product.json not found: {path}")
        print("        Run the 06:00 pipeline first (orchestrator agents 1-5).")
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    old_url = data.get("gumroad_url", "")
    data["gumroad_url"] = url
    data["gumroad_url_updated_at"] = datetime.now(timezone.utc).isoformat()

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] gumroad_url updated in {path.name}")
    print(f"     Product : {data.get('title', '-')}")
    print(f"     Old URL : {old_url or '(empty)'}")
    print(f"     New URL : {url}")
    print()
    print("Next step: the 09:00 / 21:00 tweet draft will now include this product URL.")


if __name__ == "__main__":
    main()
