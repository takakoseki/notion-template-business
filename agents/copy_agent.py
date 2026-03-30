"""
Agent 3: copy_agent.py
Role: Read design_spec.md, generate English-only sales copy via Claude API,
      and save results to data/sales_copy.json

sales_copy.json structure (English only, flat):
  title       - product title string
  description - product description string
  features    - list of feature strings
  faq         - list of {q, a} dicts
  price       - {usd: float}
"""

import json
import os
import re
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


def load_design_spec() -> str:
    path = ROOT / "data" / "design_spec.md"
    if not path.exists():
        raise FileNotFoundError(
            f"design_spec.md not found: {path}\nRun design_agent.py first."
        )
    return path.read_text(encoding="utf-8")


def generate_sales_copy(design_spec: str) -> dict:
    """Generate English-only sales copy using Claude API and return as a dict."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a Notion template sales copywriter.
Based on the design specification below, generate Gumroad sales page copy.
All output must be in English only. Do not include any Japanese text.

## Template Design Specification
{design_spec}

## Output format
Output ONLY valid JSON matching the structure below. Do not include any text outside the JSON.

{{
  "title": "Product title (under 60 characters, compelling)",
  "description": "Product description (around 200 words, highlight benefits and use cases clearly)",
  "features": [
    "Feature 1 (one sentence, specific benefit)",
    "Feature 2 (one sentence, specific benefit)",
    "Feature 3 (one sentence, specific benefit)",
    "Feature 4 (one sentence, specific benefit)",
    "Feature 5 (one sentence, specific benefit)"
  ],
  "faq": [
    {{"q": "Question 1", "a": "Answer 1 (2-3 sentences)"}},
    {{"q": "Question 2", "a": "Answer 2 (2-3 sentences)"}},
    {{"q": "Question 3", "a": "Answer 3 (2-3 sentences)"}}
  ],
  "price": {{
    "usd": 13
  }}
}}
"""

    print("[copy] Requesting sales copy from Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    json_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if json_match:
        raw = json_match.group(1)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[copy] JSON parse error. Raw response:\n{raw[:500]}")
        raise ValueError(f"Claude API response is not valid JSON: {e}") from e


def run() -> dict:
    print("[copy] === Sales copy generation started ===")

    design_spec = load_design_spec()
    sales_copy = generate_sales_copy(design_spec)

    output_path = ROOT / "data" / "sales_copy.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(sales_copy, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[copy] Title   : {sales_copy['title']}")
    print(f"[copy] Price   : ${sales_copy['price']['usd']}")
    print(f"[copy] Sales copy saved to {output_path}")
    print("[copy] === Sales copy generation complete ===")

    return sales_copy


if __name__ == "__main__":
    run()
