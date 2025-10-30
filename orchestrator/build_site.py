#!/usr/bin/env python3
import os, re, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "site" / "posts"
INDEX = ROOT / "site" / "index.html"

def md_to_html(md_text):
    # extremely basic Markdown to HTML (headers + paragraphs + blockquotes + links)
    html = md_text
    html = re.sub(r'^# (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^\*Published: (.+)\*$', r'<div class="meta">Published: \1</div>', html, flags=re.MULTILINE)
    html = re.sub(r'^\> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    html = re.sub(r'\n\n([^<\n][^\n]+)\n\n', r'\n<p>\1</p>\n', html)
    html = re.sub(r'\[(.+?)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', html)
    html = html.replace("\n", "\n")
    return html

def build_listing():
    posts = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    items = []
    for p in posts[:10]:
        md = p.read_text(encoding="utf-8")
        title = re.search(r'^# (.+)$', md, flags=re.MULTILINE)
        title = title.group(1) if title else p.stem
        html = md_to_html(md)
        items.append(f'<article class="post">{html}</article>')
    listing = "\n".join(items) if items else "<p>No posts yet.</p>"
    return listing

def inject_into_index(listing_html):
    html = INDEX.read_text(encoding="utf-8")
    new_html = re.sub(r'(<section id="latest">).*?(</section>)', r'\1' + listing_html + r'\2', html, flags=re.DOTALL)
    INDEX.write_text(new_html, encoding="utf-8")

def main():
    listing = build_listing()
    inject_into_index(listing)

if __name__ == "__main__":
    main()
