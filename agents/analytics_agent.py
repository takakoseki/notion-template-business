"""
Agent: analytics_agent.py
Role: Fetch recent tweet metrics via Tweepy and analyze performance using Claude API.
      Saves results to data/twitter_analytics.json and data/analytics_report.json.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import anthropic
import tweepy
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT))
from log_utils import system_log

ANALYTICS_PATH = ROOT / "data" / "twitter_analytics.json"
REPORT_PATH    = ROOT / "data" / "analytics_report.json"

_EMPTY_REPORT = {
    "best_performing_type": None,
    "high_engagement_patterns": [],
    "recommended_style": "general",
    "writing_tips": [],
    "summary": "No tweet data available yet.",
}


# ---------------------------------------------------------------------------
# Fetch metrics
# ---------------------------------------------------------------------------

def fetch_tweet_metrics() -> list[dict]:
    """Fetch up to 30 recent tweets with public metrics via OAuth 1.0a."""
    required = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing credentials: {', '.join(missing)}")

    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )

    me = client.get_me()
    user_id = me.data.id

    response = client.get_users_tweets(
        id=user_id,
        max_results=30,
        tweet_fields=["public_metrics", "created_at", "text"],
    )

    if not response.data:
        return []

    tweets = []
    for tweet in response.data:
        m = tweet.public_metrics or {}
        tweets.append({
            "id": str(tweet.id),
            "text": tweet.text,
            "created_at": str(tweet.created_at),
            "likes": m.get("like_count", 0),
            "retweets": m.get("retweet_count", 0),
            "replies": m.get("reply_count", 0),
            "quotes": m.get("quote_count", 0),
        })

    return tweets


# ---------------------------------------------------------------------------
# Claude analysis
# ---------------------------------------------------------------------------

def analyze_with_claude(tweets: list[dict]) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)
    tweets_text = json.dumps(tweets, ensure_ascii=False, indent=2)

    prompt = f"""\
Analyze the following recent tweets and their engagement metrics for a Notion template product account.

Tweets (JSON):
{tweets_text}

Provide:
1. Best performing tweet type among: tips / question / product / before_after / new_product
2. Common patterns in high-engagement tweets (2-3 bullet points)
3. Recommended posting style for the next tweet (1 sentence)
4. Specific writing tips based on the data (2-3 bullet points)
5. One-sentence summary of findings

Output ONLY valid JSON with these exact keys:
{{
  "best_performing_type": "...",
  "high_engagement_patterns": ["...", "..."],
  "recommended_style": "...",
  "writing_tips": ["...", "..."],
  "summary": "..."
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()
    m = re.search(r"\{[\s\S]+\}", text)
    return json.loads(m.group(0) if m else text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> dict:
    print("[analytics] === Analytics started ===")
    system_log("analytics_agent", "started", "Analytics job started")

    # Step 1: Fetch tweet metrics
    tweets: list[dict] = []
    try:
        tweets = fetch_tweet_metrics()
        print(f"[analytics] Fetched {len(tweets)} tweets.")
        system_log("analytics_agent", "info", f"Fetched {len(tweets)} tweets")
    except Exception as e:
        print(f"[analytics] WARNING: Could not fetch tweet metrics: {e}")
        print("[analytics] Proceeding with empty data.")
        system_log("analytics_agent", "warning", f"Metrics fetch failed: {e}")

    # Save raw analytics
    analytics_data = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "tweet_count": len(tweets),
        "tweets": tweets,
    }
    ANALYTICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ANALYTICS_PATH.write_text(
        json.dumps(analytics_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Step 2: Analyze with Claude
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tweet_count": len(tweets),
        **_EMPTY_REPORT,
    }

    if tweets:
        try:
            analysis = analyze_with_claude(tweets)
            report.update(analysis)
            report["generated_at"] = datetime.now(timezone.utc).isoformat()
            report["tweet_count"] = len(tweets)
            print(f"[analytics] Analysis: {report.get('summary', '-')}")
            system_log("analytics_agent", "success", report.get("summary", ""))
        except Exception as e:
            print(f"[analytics] WARNING: Claude analysis failed: {e}")
            system_log("analytics_agent", "warning", f"Claude analysis failed: {e}")
    else:
        print("[analytics] No tweets to analyze. Using default report.")

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[analytics] Report saved: {REPORT_PATH}")
    print("[analytics] === Analytics complete ===")

    return report


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run()
