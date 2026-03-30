"""
Agent 5: notion_agent.py
Role: Read design_spec.md, parse the database schema via Claude API,
      create the Notion template page and databases via Notion API,
      add 3 sample records per database, then append the page URL to
      output/publish_summary.txt.

Notion API property types supported:
  title, rich_text, number, select, multi_select, date, checkbox, url
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import anthropic
import requests as _requests
from dotenv import load_dotenv
from notion_client import Client

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

NOTION_API_BASE = "https://api.notion.com/v1"
# Pin to 2022-06-28: notion-client v3 defaults to 2025-09-03 which does not
# return or create database properties correctly.
NOTION_API_VERSION = "2022-06-28"

# Notion property colors for select / multi_select options
_COLORS = ["blue", "green", "orange", "pink", "purple", "red", "yellow", "gray", "brown"]


def _notion_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION,
    }


# ---------------------------------------------------------------------------
# File loaders
# ---------------------------------------------------------------------------

def load_design_spec() -> str:
    path = ROOT / "data" / "design_spec.md"
    if not path.exists():
        raise FileNotFoundError(
            f"design_spec.md not found: {path}\nRun design_agent.py first."
        )
    return path.read_text(encoding="utf-8")


def load_sales_copy() -> dict:
    path = ROOT / "data" / "sales_copy.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Schema extraction via Claude API
# ---------------------------------------------------------------------------

SCHEMA_PROMPT = """\
You are a Notion workspace architect.
Parse the Notion template design specification below and return a JSON object
that describes the page structure and all databases to create.

Rules:
- All names, options, and sample data MUST be in English.
- Each database must have exactly one property with type "title" — this is the main identifier.
- Supported property types: title, rich_text, number, select, multi_select, date, checkbox, url
- Do NOT use: relation, rollup, formula (Notion API requires extra setup for these).
- For select / multi_select include an "options" array of 3-6 English option strings.
- Provide exactly 3 sample_records per database that match the defined properties.
- Keep sample data realistic and relevant to the template theme.

Return ONLY valid JSON — no markdown, no extra text.

Schema:
{{
  "page_title": "string — main page / dashboard title",
  "databases": [
    {{
      "name": "string — database name",
      "description": "string — one-sentence description",
      "properties": [
        {{
          "name": "string",
          "type": "title | rich_text | number | select | multi_select | date | checkbox | url",
          "options": ["option1", "option2"]   // only for select / multi_select
        }}
      ],
      "sample_records": [
        {{ "Property Name": "value", ... }},
        {{ "Property Name": "value", ... }},
        {{ "Property Name": "value", ... }}
      ]
    }}
  ]
}}

## Design specification
{spec}
"""


def _extract_json_object(text: str) -> str:
    """
    Robustly extract the outermost JSON object from arbitrary text.
    Handles code fences (```json ... ```) and plain embedded JSON.
    """
    # 1. Try code fence with closing fence
    m = re.search(r"```(?:json)?\s*(\{[\s\S]+?\})\s*```", text)
    if m:
        return m.group(1).strip()

    # 2. Try code fence without closing fence (truncated response)
    m = re.search(r"```(?:json)?\s*(\{[\s\S]+)", text)
    if m:
        candidate = m.group(1).strip()
        # Try to close unclosed braces
        depth = candidate.count("{") - candidate.count("}")
        if depth > 0:
            candidate += "}" * depth
        return candidate

    # 3. Find the outermost { ... } in plain text
    start = text.find("{")
    if start == -1:
        return text
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    # 4. Fallback: return from first { to end and hope for the best
    return text[start:]


def extract_schema(design_spec: str) -> dict:
    """Use Claude API to parse design_spec.md into a structured Notion schema."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = SCHEMA_PROMPT.format(spec=design_spec)

    print("[notion] Extracting database schema from design spec via Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = message.content[0].text.strip()
    json_str = _extract_json_object(raw_text)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[notion] JSON parse error.\nExtracted:\n{json_str[:800]}")
        raise ValueError(f"Claude returned invalid JSON: {e}") from e


# ---------------------------------------------------------------------------
# Notion property builders
# ---------------------------------------------------------------------------

def build_property_schema(prop: dict) -> dict:
    """Convert a schema property dict to a Notion API property definition."""
    ptype = prop["type"]
    options = prop.get("options", [])

    if ptype == "title":
        return {"title": {}}
    if ptype == "rich_text":
        return {"rich_text": {}}
    if ptype == "number":
        return {"number": {"format": "number"}}
    if ptype == "select":
        return {
            "select": {
                "options": [
                    {"name": o, "color": _COLORS[i % len(_COLORS)]}
                    for i, o in enumerate(options)
                ]
            }
        }
    if ptype == "multi_select":
        return {
            "multi_select": {
                "options": [
                    {"name": o, "color": _COLORS[i % len(_COLORS)]}
                    for i, o in enumerate(options)
                ]
            }
        }
    if ptype == "date":
        return {"date": {}}
    if ptype == "checkbox":
        return {"checkbox": {}}
    if ptype == "url":
        return {"url": {}}
    # Fallback for any unsupported types
    return {"rich_text": {}}


def build_prop_value(ptype: str, value) -> dict | None:
    """Convert a single value to the Notion page property format for the given type."""
    if value is None or value == "":
        return None
    try:
        if ptype == "title":
            return {"title": [{"text": {"content": str(value)}}]}
        if ptype == "rich_text":
            return {"rich_text": [{"text": {"content": str(value)}}]}
        if ptype == "number":
            return {"number": float(value)}
        if ptype == "select":
            return {"select": {"name": str(value)}}
        if ptype == "multi_select":
            items = value if isinstance(value, list) else [value]
            return {"multi_select": [{"name": str(v)} for v in items]}
        if ptype == "date":
            return {"date": {"start": str(value)}}
        if ptype == "checkbox":
            return {"checkbox": bool(value)}
        if ptype == "url":
            return {"url": str(value)}
    except (TypeError, ValueError):
        pass
    return None


# ---------------------------------------------------------------------------
# Notion API operations
# ---------------------------------------------------------------------------

def create_template_page(notion: Client, parent_page_id: str, title: str) -> str:
    """Create the top-level template page and return its page_id."""
    resp = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        children=[
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": (
                                    "Welcome! Duplicate this page to your workspace "
                                    "to start using the template."
                                )
                            },
                        }
                    ],
                    "icon": {"type": "emoji", "emoji": "👋"},
                    "color": "blue_background",
                },
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {},
            },
        ],
    )
    return resp["id"]


def create_database(api_key: str, parent_page_id: str, db_schema: dict) -> str:
    """
    Create a Notion database via REST API (Notion-Version 2022-06-28)
    and return its database_id.
    """
    properties: dict = {}
    title_added = False

    for prop in db_schema["properties"]:
        notion_prop = build_property_schema(prop)
        if prop["type"] == "title":
            if title_added:
                notion_prop = {"rich_text": {}}  # only one title allowed
            else:
                title_added = True
        properties[prop["name"]] = notion_prop

    if not title_added:
        properties = {"Name": {"title": {}}, **properties}

    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": db_schema["name"]}}],
        "properties": properties,
    }
    resp = _requests.post(
        f"{NOTION_API_BASE}/databases",
        headers=_notion_headers(api_key),
        json=body,
        timeout=30,
    )
    data = resp.json()
    if not resp.ok:
        raise RuntimeError(f"Database creation failed: {data.get('message', data)}")
    return data["id"]


def get_database_properties(api_key: str, database_id: str) -> dict[str, str]:
    """
    Retrieve actual property names and types from a Notion database.
    Returns {property_name: notion_type}.
    """
    resp = _requests.get(
        f"{NOTION_API_BASE}/databases/{database_id}",
        headers=_notion_headers(api_key),
        timeout=30,
    )
    data = resp.json()
    if not resp.ok:
        raise RuntimeError(f"Database retrieve failed: {data.get('message', data)}")
    return {name: info["type"] for name, info in data.get("properties", {}).items()}


def add_sample_records(api_key: str, database_id: str, db_schema: dict) -> None:
    """
    Add up to 3 sample records to a Notion database.
    Fetches actual property names from Notion and matches case-insensitively.
    """
    actual_props = get_database_properties(api_key, database_id)
    lower_to_actual = {n.lower(): n for n in actual_props}

    for i, record in enumerate(db_schema.get("sample_records", [])[:3], 1):
        page_props: dict = {}
        for key, value in record.items():
            if key in actual_props:
                actual_name = key
            elif key.lower() in lower_to_actual:
                actual_name = lower_to_actual[key.lower()]
            else:
                continue

            ptype = actual_props[actual_name]
            prop_val = build_prop_value(ptype, value)
            if prop_val is not None:
                page_props[actual_name] = prop_val

        if not page_props:
            print(f"[notion]   WARNING: Sample record {i} skipped (no matching properties).")
            continue

        resp = _requests.post(
            f"{NOTION_API_BASE}/pages",
            headers=_notion_headers(api_key),
            json={"parent": {"database_id": database_id}, "properties": page_props},
            timeout=30,
        )
        if resp.ok:
            print(f"[notion]   Sample record {i} added.")
        else:
            msg = resp.json().get("message", resp.text[:200])
            print(f"[notion]   WARNING: Sample record {i} failed: {msg}")
        time.sleep(0.35)


def page_id_to_url(page_id: str) -> str:
    """Convert a Notion page ID to a public URL."""
    clean_id = page_id.replace("-", "")
    return f"https://www.notion.so/{clean_id}"


# ---------------------------------------------------------------------------
# notion_result.json — read by publish_agent to include Notion URL in summary
# ---------------------------------------------------------------------------

def save_notion_result(result: dict) -> None:
    """Save Notion creation result to data/notion_result.json for publish_agent."""
    out_path = ROOT / "data" / "notion_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[notion] Result saved to {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> dict:
    print("[notion] === Notion template creation started ===")

    notion_api_key = os.getenv("NOTION_API_KEY")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")

    if not notion_api_key:
        raise EnvironmentError("NOTION_API_KEY is not set.")
    if not parent_page_id:
        raise EnvironmentError("NOTION_PARENT_PAGE_ID is not set.")

    # notion_client is used only for page creation (top-level template page).
    # All database operations use requests + Notion-Version 2022-06-28 directly,
    # because notion-client v3 defaults to 2025-09-03 which does not create
    # database properties correctly.
    notion = Client(auth=notion_api_key)

    # 1. Load design spec
    design_spec = load_design_spec()

    # 2. Extract schema via Claude
    schema = extract_schema(design_spec)
    page_title = schema.get("page_title", "Notion Template")
    databases = schema.get("databases", [])

    if not databases:
        raise ValueError("No databases found in the extracted schema.")

    print(f"[notion] Page title : {page_title}")
    print(f"[notion] Databases  : {len(databases)} ({', '.join(d['name'] for d in databases)})")

    # 3. Create top-level template page
    print(f"[notion] Creating template page under parent {parent_page_id}...")
    template_page_id = create_template_page(notion, parent_page_id, page_title)
    page_url = page_id_to_url(template_page_id)
    print(f"[notion] Template page created: {page_url}")

    # 4 & 5. Create each database and add sample records
    created_databases: list[dict] = []
    for db_schema in databases:
        db_name = db_schema["name"]
        print(f"[notion] Creating database: {db_name}...")
        try:
            db_id = create_database(notion_api_key, template_page_id, db_schema)
            print(f"[notion]   Database created (id: {db_id[:8]}...)")
            print(f"[notion]   Adding sample records...")
            add_sample_records(notion_api_key, db_id, db_schema)
            created_databases.append({"name": db_name, "id": db_id})
        except Exception as e:
            print(f"[notion]   ERROR creating '{db_name}': {e}")
        time.sleep(0.5)

    # 6. Note: Notion API does not support enabling "Share to web" programmatically.
    print("[notion] NOTE: To make this page public, open Notion -> Share -> enable 'Share to web'.")

    result = {
        "page_title": page_title,
        "page_id": template_page_id,
        "page_url": page_url,
        "databases_created": len(created_databases),
        "databases": created_databases,
    }

    print(f"[notion] ============================================")
    print(f"[notion]  Template creation complete")
    print(f"[notion]  Title      : {page_title}")
    print(f"[notion]  URL        : {page_url}")
    print(f"[notion]  Databases  : {len(created_databases)}")
    print(f"[notion] ============================================")
    print("[notion] === Notion template creation complete ===")

    # 7. Save result for publish_agent
    save_notion_result(result)

    return result


if __name__ == "__main__":
    run()
