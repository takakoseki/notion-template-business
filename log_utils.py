"""
log_utils.py
Shared utility for writing entries to data/system_log.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def system_log(agent: str, status: str, message: str, data: dict = None) -> None:
    """Append one entry to data/system_log.json."""
    log_path = ROOT / "data" / "system_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "status": status,
        "message": message,
    }
    if data:
        entry["data"] = data

    logs: list = []
    if log_path.exists():
        try:
            logs = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            logs = []

    logs.append(entry)
    log_path.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")
