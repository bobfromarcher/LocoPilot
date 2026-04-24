"""
research_agent.py — Browse Hacker News top stories and summarize them.

Uses LocoPilot's /browser/browse_and_read endpoint to fetch and read
the HN front page, then prints the top 5 story titles.
"""

import requests

LOCOPILOT = "http://127.0.0.1:8264"


def fetch_hacker_news() -> str:
    """Browse Hacker News and return the page content."""
    resp = requests.post(
        f"{LOCOPILOT}/browser/browse_and_read",
        json={"url": "https://news.ycombinator.com"},
    )
    resp.raise_for_status()
    data = resp.json()
    # browse_and_read returns the page text in its response
    return data.get("text", data.get("content", ""))


def parse_top_stories(text: str, limit: int = 5) -> list[str]:
    """Extract top story titles from HN page text.

    HN titles appear as numbered lines like '1. Some Title' or as
    standalone lines after rank numbers. We split on newlines and
    look for lines that match typical HN title patterns.
    """
    import re

    titles = []
    # Match lines starting with a rank number (e.g. "1. Title here")
    for line in text.splitlines():
        match = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if match:
            titles.append(match.group(1).strip())
        if len(titles) >= limit:
            break

    # Fallback: if regex didn't find enough, grab non-empty lines
    if not titles:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        titles = lines[:limit]

    return titles


def main():
    print("Fetching Hacker News front page...")
    page_text = fetch_hacker_news()

    stories = parse_top_stories(page_text, limit=5)

    print("\n=== Top 5 Hacker News Stories ===\n")
    for i, title in enumerate(stories, 1):
        print(f"  {i}. {title}")
    print()


if __name__ == "__main__":
    main()
