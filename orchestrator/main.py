#!/usr/bin/env python3
import os, json, datetime, re, sys, time, textwrap
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Identify the bot so Wikipedia doesn't block it (403 fix)
HEADERS = {
    "User-Agent": "AutopilotKnowledgeEngine/1.0 (+https://github.com/expectations251/ake-autopilot)",
    "Accept": "application/json"
}

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "site" / "posts"
ADS_FILE = ROOT / "house_ads.json"

def load_ads():
    try:
        with open(ADS_FILE, "r") as f:
            data = json.load(f)
        return data.get("ads", [])
    except Exception:
        return []

def pick_ad(ads):
    return ads[0] if ads else None

def fetch_wikipedia_featured(date: datetime.date):
    """Use Wikipedia REST API for 'featured content' of the given date (en)."""
    url = f"https://en.wikipedia.org/api/rest_v1/feed/featured/{date.year}/{date.month:02d}/{date.day:02d}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    title = None
    summary_html = None
    source_url = None
    if "tfa" in data and data["tfa"]:
        tfa = data["tfa"]
        title = tfa.get("titles", {}).get("display")
        summary_html = tfa.get("extract_html")
        source_url = tfa.get("content_urls", {}).get("desktop", {}).get("page")
    elif "news" in data and data["news"]:
        first = data["news"][0]
        title = first.get("story")
        items = [f"<li>{itm.get('titles', {}).get('display', '')}</li>" for itm in first.get("links", [])]
        summary_html = "<p>In the news:</p><ul>" + "".join(items) + "</ul>"
        source_url = "https://en.wikipedia.org/wiki/Portal:Current_events"
    else:
        r = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/random/summary",
            headers=HEADERS, timeout=20
        )
        r.raise_for_status()
        j = r.json()
        title = j.get("title", "Interesting Topic")
        summary_html = j.get("extract_html", j.get("extract", ""))
        source_url = j.get("content_urls", {}).get("desktop", {}).get("page")

    return title, summary_html, source_url

def build_markdown_post(date, title, html, url, ad=None):
    body_md = md(html or "", heading_style="ATX")
    body_md = re.sub(r'\n{3,}', '\n\n', body_md).strip()
    ad_block = ""
    if ad:
        ad_block = f"\n> **{ad['label']}** — {ad['disclosure']} · {ad['url']}\n"
    credit = f"\n— Source: Wikipedia (CC-BY-SA). Original: {url}\n"
    header = f"# {title}\n\n*Published: {date.isoformat()}*\n\n"
    return header + body_md + "\n" + ad_block + credit + "\n"

def write_post(date, title, content):
    safe_title = re.sub(r'[^a-z0-9\-]+', '-', title.lower()).strip('-')[:60] or "daily-post"
    fname = f"{date.isoformat()}-{safe_title}.md"
    path = POSTS_DIR / fname
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def ensure_repo_size_limits():
    MAX = 100 * 1024 * 1024  # 100MB
    for p in ROOT.rglob("*"):
        if p.is_file() and p.stat().st_size > MAX:
            raise RuntimeError(f"File too large for Git: {p} exceeds 100MB.")

def main(once=False):
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    ads = load_ads()
    ad = pick_ad(ads)
    today = datetime.date.today()

    # Try today → yesterday → local fallback (never fails the workflow)
    try:
        title, summary_html, source_url = fetch_wikipedia_featured(today)
    except Exception:
        try:
            y = today - datetime.timedelta(days=1)
            title, summary_html, source_url = fetch_wikipedia_featured(y)
        except Exception:
            title = "Daily Knowledge"
            summary_html = (
                "<p>This starter post proves the autopilot is live. "
                "Future posts will pull from public CC-BY-SA sources automatically.</p>"
            )
            source_url = "https://en.wikipedia.org/wiki/Main_Page"

    content = build_markdown_post(today, title, summary_html, source_url, ad=ad)
    path = write_post(today, title, content)
    ensure_repo_size_limits()
    print(f"Wrote post: {path}")
    return 0

if __name__ == "__main__":
    once = "--once" in sys.argv
    sys.exit(main(once=once))
