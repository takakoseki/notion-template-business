"""
Agent 2: design_agent.py
Role: Read the top theme from research_result.json, generate a Notion template
      design specification via Claude API, and save it to data/design_spec.md
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

import anthropic
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def load_research_result() -> dict:
    path = ROOT / "data" / "research_result.json"
    if not path.exists():
        raise FileNotFoundError(
            f"research_result.json not found: {path}\nRun research_agent.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def generate_design_spec(theme: str, top_posts: list[dict]) -> str:
    """Generate a Notion template design specification using Claude API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)

    posts_summary = "\n".join(
        f"- {p['title']} (score: {p['score']})" for p in top_posts[:5]
    )

    prompt = f"""You are an expert Notion template designer.
Create a detailed design specification in Markdown for the Notion template described below.
All output must be written entirely in English.

## Theme
{theme}

## Reference popular posts
{posts_summary}

## Required sections

### 1. Purpose and Target Users
- What problem this template solves
- Primary use cases
- Detailed target user persona

### 2. Notion Database List and Column Definitions
For each database, define:
- Database name
- Purpose / description
- Column name, data type (Text / Number / Select / Multi-select / Date / Checkbox / URL / Relation / Rollup / Formula, etc.), and description

### 3. Page Structure
Describe the hierarchy of pages and where each database lives:
- Top-level page (Dashboard)
- Sub-pages
- Database placement

### 4. Getting-Started Flow (3 Steps)
Explain how a new user begins using the template in exactly 3 clear steps.

Write practical, specific content. All text must be in English.
"""

    print("[design] Requesting design spec from Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def _load_past_themes() -> set[str]:
    """Return the set of all titles already created (from archived sales_copy files)."""
    past: set[str] = set()

    # Collect every archived sales_copy_YYYYMMDD.json
    for path in (ROOT / "data").glob("sales_copy_????????.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            title = data.get("title", "").strip()
            if title:
                past.add(title.lower())
        except Exception:
            pass

    # Also include the current latest_product.json as a safety net
    latest = ROOT / "data" / "latest_product.json"
    if latest.exists():
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            title = data.get("title", "").strip()
            if title:
                past.add(title.lower())
        except Exception:
            pass

    return past


def run() -> dict:
    print("[design] === Design started ===")

    fallback_themes = [
        "Habit Tracker",
        "Project Management",
        "Personal Finance",
        "Content Creator",
        "Study / Learning",
        "Job Search / Career",
        "CRM / Sales",
        "Life OS / Second Brain",
        "Meeting Notes",
        "Travel Planner",
    ]

    past_title = _load_past_themes()

    research = load_research_result()
    top5 = research.get("top5_themes", [])

    # Pick the highest-ranked theme that was NOT used in the last run
    theme_name = None
    top_posts: list[dict] = []

    for candidate in top5:
        name = candidate["theme"]
        # Skip if the previous product title contains this theme's keywords
        if any(word.lower() in pt for word in name.split() for pt in past_title):
            print(f"[design] Skipping '{name}' (same as last product).")
            continue
        theme_name = name
        top_posts = candidate.get("top_posts", [])
        break

    if theme_name is None:
        # All top5 were used — fall back to a theme not in top5
        top5_names = {t["theme"] for t in top5}
        for fb in fallback_themes:
            if fb not in top5_names and not any(
                word.lower() in pt for word in fb.split() for pt in past_title
            ):
                theme_name = fb
                break
        if theme_name is None:
            # Last resort: just pick the top result regardless
            theme_name = top5[0]["theme"] if top5 else fallback_themes[0]
            top_posts = top5[0].get("top_posts", []) if top5 else []
            print(f"[design] WARNING: All themes exhausted. Reusing '{theme_name}'.")

    print(f"[design] Top theme: {theme_name}")

    spec_md = generate_design_spec(theme_name, top_posts)

    header = f"# Notion Template Design Specification\n\n**Theme:** {theme_name}\n\n---\n\n"
    full_content = header + spec_md

    output_path = ROOT / "data" / "design_spec.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_content, encoding="utf-8")

    print(f"[design] Design spec saved to {output_path}")
    print("[design] === Design complete ===")

    return {"theme": theme_name, "output_path": str(output_path)}


if __name__ == "__main__":
    run()
