"""
Agent: twitter_agent.py
Role: Generate a promotional tweet draft using Claude API and save to data/twitter_draft.txt.

Tweet types (selected randomly per run):
  1. product      — highlight one feature + Gumroad link
  2. tips         — useful habit tip + template link
  3. before_after — contrast format showing transformation
  4. question     — engagement question + template link
  5. new_product  — new product announcement (only when gumroad_url is set in latest_product.json)

Additional context fed to Claude:
  - Past 30 post texts (deduplication)
  - Analytics report (style recommendations)
"""

import json
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import anthropic
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT))
from log_utils import system_log

TWEET_MAX_CHARS = 280
_URL_T_CO_LEN   = 23  # Twitter wraps all URLs to 23 chars

_HASHTAG_SETS = {
    "product":     "#Notion #ProductivityTools #NotionTemplate",
    "tips":        "#HabitTracker #Notion #Productivity",
    "before_after":"#Notion #HabitTracker",
    "question":    "#Notion #Productivity",
    "new_product": "#Notion #NewRelease #ProductivityTools",
}

TWEET_PROMPTS: dict[str, str] = {
    "product": """\
Write a single promotional tweet for a Notion template product.
Rules:
- Highlight ONE specific feature from the features list below.
- End with: {url}
- Add hashtags on the last line: {hashtags}
- Total tweet length (including URL counted as 23 chars and hashtags) must be ≤ 280 characters.
- Write in a friendly, engaging tone. English only. No emojis unless they enhance readability.
- Output only the tweet text, nothing else.

Product title: {title}
Features:
{features}
{extra_context}""",

    "tips": """\
Write a single tweet sharing ONE practical, actionable tip about habit tracking or building daily routines.
Rules:
- The tip must be genuinely useful and specific (not generic advice).
- After the tip, add: I built a Notion template to help with exactly this → {url}
- Add hashtags on the last line: {hashtags}
- Total tweet length (URL counted as 23 chars) must be ≤ 280 characters.
- English only. No emojis.
- Output only the tweet text, nothing else.

Context (use for inspiration, don't copy directly):
Product title: {title}
Features: {features}
{extra_context}""",

    "before_after": """\
Write a single tweet using a before/after contrast format showing the transformation
a user experiences from using a habit-tracking Notion template.
Rules:
- Use the format: "Before: ... / After: ..." or similar contrast structure.
- Keep it relatable and specific.
- Include the product URL: {url}
- Add hashtags on the last line: {hashtags}
- Total tweet length (URL counted as 23 chars) must be ≤ 280 characters.
- English only. No emojis.
- Output only the tweet text, nothing else.

Product title: {title}
Description: {description}
{extra_context}""",

    "question": """\
Write a single engagement-focused tweet asking a question about habit tracking or productivity.
Rules:
- Ask ONE concise, relatable question that encourages replies.
- After the question, add: I built a Notion template to solve this → {url}
- Add hashtags on the last line: {hashtags}
- Total tweet length (URL counted as 23 chars) must be ≤ 280 characters.
- English only. No emojis.
- Output only the tweet text, nothing else.

Context:
Product title: {title}
{extra_context}""",

    "new_product": """\
Write a single tweet announcing a newly released Notion template.
Rules:
- Start with exactly: "New template just dropped!"
- Mention the product name and ONE key feature in one sentence.
- End with the product URL: {url}
- Add hashtags on the last line: {hashtags}
- Total tweet length (URL counted as 23 chars) must be ≤ 280 characters.
- English only. No emojis.
- Output only the tweet text, nothing else.

Product name: {title}
Key features:
{features}
{extra_context}""",
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sales_copy() -> dict:
    path = ROOT / "data" / "sales_copy.json"
    if not path.exists():
        raise FileNotFoundError(
            f"sales_copy.json not found: {path}\nRun copy_agent.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_gumroad_url() -> str:
    """
    Resolve the Gumroad product URL in priority order:
      1. GUMROAD_PRODUCT_URL in .env
      2. gumroad_url in data/latest_product.json
      3. First https://....gumroad.com/l/... URL in publish_summary.txt
      4. Placeholder string
    """
    env_url = os.getenv("GUMROAD_PRODUCT_URL", "").strip()
    if env_url:
        return env_url

    latest_path = ROOT / "data" / "latest_product.json"
    if latest_path.exists():
        try:
            data = json.loads(latest_path.read_text(encoding="utf-8"))
            url = data.get("gumroad_url", "").strip()
            if url:
                return url
        except Exception:
            pass

    summary_path = ROOT / "output" / "publish_summary.txt"
    if summary_path.exists():
        text = summary_path.read_text(encoding="utf-8")
        m = re.search(r"https://[a-z]+\.gumroad\.com/l/\S+", text)
        if m:
            return m.group(0).rstrip(")")

    return "https://gumroad.com/l/your-product"


def load_latest_product() -> dict | None:
    path = ROOT / "data" / "latest_product.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_past_posts(n: int = 30) -> list[str]:
    path = ROOT / "data" / "twitter_log.json"
    if not path.exists():
        return []
    try:
        log = json.loads(path.read_text(encoding="utf-8"))
        return [entry["tweet_text"] for entry in log[-n:] if "tweet_text" in entry]
    except Exception:
        return []


def load_analytics_report() -> dict | None:
    path = ROOT / "data" / "analytics_report.json"
    if not path.exists():
        return None
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        # Only use if it contains actual analysis (not the empty default)
        if report.get("tweet_count", 0) > 0:
            return report
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Tweet generation
# ---------------------------------------------------------------------------

def _count_tweet_length(text: str, url: str) -> int:
    return len(text.replace(url, "x" * _URL_T_CO_LEN))


def _build_extra_context(past_posts: list[str], analytics: dict | None) -> str:
    parts = []

    if past_posts:
        recent = "\n".join(f"- {p[:80]}..." if len(p) > 80 else f"- {p}"
                           for p in past_posts[-30:])
        parts.append(f"Do not repeat these recent posts:\n{recent}")

    if analytics:
        tips = "\n".join(f"- {t}" for t in analytics.get("writing_tips", []))
        parts.append(
            f"Based on this performance analysis, generate a post that follows "
            f"the best performing style:\n"
            f"Summary: {analytics.get('summary', '')}\n"
            f"Recommended style: {analytics.get('recommended_style', '')}\n"
            f"Writing tips:\n{tips}"
        )

    return ("\n\n" + "\n\n".join(parts)) if parts else ""


def generate_tweet(
    sales_copy: dict,
    url: str,
    tweet_type: str,
    past_posts: list[str] | None = None,
    analytics: dict | None = None,
) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)

    features_text  = "\n".join(f"- {f}" for f in sales_copy.get("features", []))
    hashtags       = _HASHTAG_SETS[tweet_type]
    extra_context  = _build_extra_context(past_posts or [], analytics)

    prompt = TWEET_PROMPTS[tweet_type].format(
        title=sales_copy.get("title", ""),
        description=sales_copy.get("description", ""),
        features=features_text,
        url=url,
        hashtags=hashtags,
        extra_context=extra_context,
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    tweet = message.content[0].text.strip()

    # Safety trim
    if _count_tweet_length(tweet, url) > TWEET_MAX_CHARS:
        lines = tweet.splitlines()
        hashtag_line = lines[-1] if lines[-1].startswith("#") else ""
        body_lines   = lines[:-1] if hashtag_line else lines
        body         = " ".join(body_lines).strip()
        max_body     = TWEET_MAX_CHARS - _URL_T_CO_LEN - 1 - len(hashtag_line) - 2
        if len(body) > max_body:
            body = body[:max_body - 1].rsplit(" ", 1)[0] + "…"
        tweet = f"{body}\n{hashtag_line}".strip()

    return tweet


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def load_log() -> list:
    path = ROOT / "data" / "twitter_log.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def append_log(entry: dict) -> None:
    log = load_log()
    log.append(entry)
    path = ROOT / "data" / "twitter_log.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> dict:
    print("[twitter] === Tweet draft generation started ===")
    system_log("twitter_agent", "started", "Tweet draft generation started")

    sales_copy     = load_sales_copy()
    latest_product = load_latest_product()
    past_posts     = load_past_posts(30)
    analytics      = load_analytics_report()

    # Determine available tweet types
    available_types = list(TWEET_PROMPTS.keys())
    has_new_product = (
        latest_product is not None
        and bool(latest_product.get("gumroad_url", "").strip())
    )
    if not has_new_product:
        available_types = [t for t in available_types if t != "new_product"]

    tweet_type = random.choice(available_types)

    # URL: new_product uses latest_product gumroad_url; others use general URL
    if tweet_type == "new_product" and has_new_product:
        url = latest_product["gumroad_url"]
        # Merge latest_product info into sales_copy for richer context
        if latest_product.get("title"):
            sales_copy = {**sales_copy, "title": latest_product["title"]}
    else:
        url = load_gumroad_url()

    print(f"[twitter] Tweet type  : {tweet_type}")
    print(f"[twitter] Product URL : {url}")
    print(f"[twitter] Past posts  : {len(past_posts)} loaded for dedup")
    print(f"[twitter] Analytics   : {'loaded' if analytics else 'not available'}")
    print("[twitter] Generating tweet via Claude API...")

    tweet_text    = generate_tweet(sales_copy, url, tweet_type, past_posts, analytics)
    estimated_len = _count_tweet_length(tweet_text, url)

    print(f"[twitter] Tweet ({estimated_len} chars):")
    print("-" * 40)
    print(tweet_text)
    print("-" * 40)

    log_entry: dict = {
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "tweet_type":      tweet_type,
        "tweet_text":      tweet_text,
        "estimated_chars": estimated_len,
        "url":             url,
        "status":          "draft",
    }

    # Save draft
    draft_path = ROOT / "data" / "twitter_draft.txt"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(tweet_text, encoding="utf-8")

    append_log(log_entry)
    system_log("twitter_agent", "success", f"Draft saved — type: {tweet_type}, chars: {estimated_len}")

    print(f"[twitter] Draft saved: {draft_path}")
    print("[twitter] ============================================")
    print(f"[twitter]  Type    : {tweet_type}")
    print(f"[twitter]  Chars   : {estimated_len}")
    print("[twitter] ============================================")
    print("[twitter] Copy the draft above and post it manually on X.")
    print("[twitter] === Draft generation complete ===")

    return log_entry


if __name__ == "__main__":
    run()
