"""
Agent 1: research_agent.py
Role: Research trending Notion template themes from Reddit and ProductHunt,
      score the top 5, and save results to data/research_result.json
"""

import json
import os
import random
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import praw
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


# ---------------------------------------------------------------------------
# Reddit
# ---------------------------------------------------------------------------

def fetch_reddit_posts() -> list[dict]:
    """Fetch hot posts from r/Notion and r/productivity from the past 30 days."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "notion-template-bot/1.0")

    if not client_id or not client_secret:
        print("[research] WARNING: Reddit credentials not set. Skipping.")
        return []

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    subreddits = ["Notion", "productivity"]
    cutoff = time.time() - 30 * 24 * 3600
    results = []

    for sub_name in subreddits:
        try:
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.hot(limit=200):
                if post.created_utc < cutoff:
                    continue
                if "template" not in post.title.lower() and "template" not in (post.selftext or "").lower():
                    continue
                results.append({
                    "source": "reddit",
                    "subreddit": sub_name,
                    "title": post.title,
                    "score": post.score,
                    "url": f"https://www.reddit.com{post.permalink}",
                    "created_utc": post.created_utc,
                })
            count = sum(1 for r in results if r.get("subreddit") == sub_name)
            print(f"[research] Reddit r/{sub_name}: {count} posts fetched")
        except Exception as e:
            print(f"[research] Reddit r/{sub_name} fetch error: {e}")

    return results


# ---------------------------------------------------------------------------
# ProductHunt
# ---------------------------------------------------------------------------

def fetch_producthunt_posts() -> list[dict]:
    """Search ProductHunt GraphQL API for Notion template posts."""
    token = os.getenv("PRODUCTHUNT_DEVELOPER_TOKEN") or os.getenv("PRODUCTHUNT_API_KEY")
    if not token:
        print("[research] WARNING: ProductHunt API key not set. Skipping.")
        return []

    query = """
    query {
      posts(first: 50, topic: "notion") {
        edges {
          node {
            name
            tagline
            votesCount
            url
            createdAt
          }
        }
      }
    }
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        resp = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query},
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        edges = data.get("data", {}).get("posts", {}).get("edges", [])
    except Exception as e:
        print(f"[research] ProductHunt API error: {e}")
        return []

    results = []
    for edge in edges:
        node = edge["node"]
        name = node.get("name", "")
        tagline = node.get("tagline", "")
        if "template" not in name.lower() and "template" not in tagline.lower():
            continue
        results.append({
            "source": "producthunt",
            "title": f"{name} - {tagline}",
            "score": node.get("votesCount", 0),
            "url": node.get("url", ""),
            "created_utc": None,
        })

    print(f"[research] ProductHunt: {len(results)} posts fetched")
    return results


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

THEME_KEYWORDS: dict[str, list[str]] = {
    "Project Management": ["project", "task", "kanban", "roadmap", "sprint", "agile", "milestone"],
    "Personal Finance": ["finance", "budget", "expense", "money", "investment", "saving", "debt"],
    "Content Creator": ["content", "social media", "youtube", "blog", "creator", "editorial", "posting"],
    "Job Search / Career": ["job", "career", "resume", "cv", "interview", "hiring", "application"],
    "Study / Learning": ["study", "learning", "notes", "course", "student", "education", "reading"],
    "Habit Tracker": ["habit", "routine", "daily", "tracker", "goal", "streak"],
    "CRM / Sales": ["crm", "sales", "client", "lead", "pipeline", "deal", "customer"],
    "Life OS / Second Brain": ["life os", "second brain", "pkm", "zettelkasten", "knowledge", "dashboard"],
    "Meeting Notes": ["meeting", "minutes", "agenda", "action item", "standup"],
    "Travel Planner": ["travel", "trip", "itinerary", "vacation", "packing"],
}


def score_themes(posts: list[dict]) -> list[dict]:
    """Aggregate posts by theme and return the top 5 ranked by total score."""
    theme_scores: dict[str, dict] = defaultdict(lambda: {"total_score": 0, "post_count": 0, "top_posts": []})

    for post in posts:
        text = (post["title"] + " ").lower()
        for theme, keywords in THEME_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                ts = theme_scores[theme]
                ts["total_score"] += post["score"]
                ts["post_count"] += 1
                ts["top_posts"].append({"title": post["title"], "score": post["score"], "url": post["url"]})

    ranked = sorted(
        [{"theme": t, **v} for t, v in theme_scores.items()],
        key=lambda x: x["total_score"],
        reverse=True,
    )

    top5 = []
    for item in ranked[:5]:
        item["top_posts"] = sorted(item["top_posts"], key=lambda p: p["score"], reverse=True)[:5]
        top5.append(item)

    return top5


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> dict:
    print("[research] === Research started ===")

    reddit_posts = fetch_reddit_posts()
    ph_posts = fetch_producthunt_posts()
    all_posts = reddit_posts + ph_posts

    if not all_posts:
        print("[research] No live data. Using fallback dataset.")
        all_posts = [
            {"source": "fallback", "title": "Best Notion project management template", "score": 500, "url": ""},
            {"source": "fallback", "title": "Notion personal finance tracker template", "score": 430, "url": ""},
            {"source": "fallback", "title": "Content creator dashboard notion template", "score": 380, "url": ""},
            {"source": "fallback", "title": "Notion habit tracker template", "score": 320, "url": ""},
            {"source": "fallback", "title": "Life OS second brain notion template", "score": 290, "url": ""},
        ]

    top5 = score_themes(all_posts)

    # Supplement with fallback themes if fewer than 5 results.
    # Shuffle fallback list so the same theme is not always chosen first.
    if len(top5) < 5:
        fallback_themes = [
            {"theme": "Habit Tracker",        "total_score": 100, "post_count": 1, "top_posts": []},
            {"theme": "Project Management",   "total_score":  90, "post_count": 1, "top_posts": []},
            {"theme": "Personal Finance",     "total_score":  80, "post_count": 1, "top_posts": []},
            {"theme": "Content Creator",      "total_score":  70, "post_count": 1, "top_posts": []},
            {"theme": "Study / Learning",     "total_score":  60, "post_count": 1, "top_posts": []},
            {"theme": "Job Search / Career",  "total_score":  50, "post_count": 1, "top_posts": []},
            {"theme": "CRM / Sales",          "total_score":  40, "post_count": 1, "top_posts": []},
            {"theme": "Life OS / Second Brain","total_score": 30, "post_count": 1, "top_posts": []},
            {"theme": "Meeting Notes",        "total_score":  20, "post_count": 1, "top_posts": []},
            {"theme": "Travel Planner",       "total_score":  10, "post_count": 1, "top_posts": []},
        ]
        random.shuffle(fallback_themes)
        existing_themes = {t["theme"] for t in top5}
        for fb in fallback_themes:
            if fb["theme"] not in existing_themes and len(top5) < 5:
                top5.append(fb)
        print(f"[research] Supplemented with fallback themes. Total: {len(top5)}")

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_posts_analyzed": len(all_posts),
        "top5_themes": top5,
    }

    output_path = ROOT / "data" / "research_result.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[research] Top 5 themes:")
    for i, t in enumerate(top5, 1):
        print(f"  {i}. {t['theme']} (score: {t['total_score']}, posts: {t['post_count']})")
    print(f"[research] Results saved to {output_path}")
    print("[research] === Research complete ===")

    return result


if __name__ == "__main__":
    run()
