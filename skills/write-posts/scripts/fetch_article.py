#!/usr/bin/env python3
"""
Fetch article content from any URL using requests + BeautifulSoup.
Usage: python fetch_article.py <url> [output_dir]
"""

import sys
import os
import json
import re
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
}

# Tags that typically contain article body text
ARTICLE_TAGS = ["article", "main", "[role='main']", ".post-content", ".article-content",
                ".entry-content", ".post-body", ".article-body", ".story-body"]

# Tags to remove before extracting text
REMOVE_TAGS = ["script", "style", "nav", "footer", "header", "aside",
               "iframe", "noscript", "svg", "form", ".sidebar", ".comments",
               ".advertisement", ".ad", ".social-share", ".related-posts"]


def fetch_url(url: str) -> str:
    """Fetch HTML content from URL."""
    resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def extract_article(html: str, url: str) -> dict:
    """Extract article metadata and content from HTML."""
    parser = "lxml" if "lxml" in sys.modules or _try_import("lxml") else "html.parser"
    soup = BeautifulSoup(html, parser)

    # Remove unwanted elements
    for selector in REMOVE_TAGS:
        for el in soup.select(selector) if selector.startswith((".","[","#")) else soup.find_all(selector):
            el.decompose()

    # Extract title
    title = ""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    # Extract author
    author = ""
    for meta_name in ["author", "article:author", "og:author"]:
        meta = soup.find("meta", attrs={"name": meta_name}) or soup.find("meta", property=meta_name)
        if meta and meta.get("content"):
            author = meta["content"].strip()
            break
    if not author:
        author_el = soup.find(class_=re.compile(r"author", re.I))
        if author_el:
            author = author_el.get_text(strip=True)

    # Extract publish date
    publish_date = ""
    for meta_name in ["article:published_time", "datePublished", "date", "publishedDate"]:
        meta = soup.find("meta", property=meta_name) or soup.find("meta", attrs={"name": meta_name})
        if meta and meta.get("content"):
            publish_date = meta["content"].strip()[:10]
            break
    if not publish_date:
        time_el = soup.find("time")
        if time_el and time_el.get("datetime"):
            publish_date = time_el["datetime"][:10]

    # Extract description
    description = ""
    og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
    if og_desc and og_desc.get("content"):
        description = og_desc["content"].strip()

    # Extract article body
    content = ""
    for selector in ARTICLE_TAGS:
        if selector.startswith((".", "[", "#")):
            article_el = soup.select_one(selector)
        else:
            article_el = soup.find(selector)
        if article_el:
            content = _extract_text(article_el)
            if len(content) > 200:
                break

    # Fallback: use body
    if len(content) < 200:
        body = soup.find("body")
        if body:
            content = _extract_text(body)

    return {
        "url": url,
        "title": title,
        "author": author,
        "publishDate": publish_date,
        "description": description,
        "content": content.strip(),
        "contentLength": len(content.strip()),
    }


def _extract_text(element) -> str:
    """Extract clean text from a BeautifulSoup element, preserving paragraph structure."""
    paragraphs = []
    for el in element.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote"]):
        text = el.get_text(strip=True)
        if text and len(text) > 10:
            prefix = ""
            if el.name and el.name.startswith("h"):
                level = el.name[1]
                prefix = "#" * int(level) + " "
            elif el.name == "li":
                prefix = "- "
            elif el.name == "blockquote":
                prefix = "> "
            paragraphs.append(prefix + text)

    if not paragraphs:
        return element.get_text(separator="\n", strip=True)

    return "\n\n".join(paragraphs)


def _try_import(module_name: str) -> bool:
    """Try to import a module, return True if successful."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_article.py <url> [output_dir]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    # Default output: outputs/posts/<timestamp>
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("outputs", "posts", timestamp)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Fetching article from: {url}", file=sys.stderr)
    html = fetch_url(url)
    print(f"HTML fetched: {len(html)} characters", file=sys.stderr)

    result = extract_article(html, url)
    result["outputDir"] = output_dir

    print(f"Title: {result['title']}", file=sys.stderr)
    print(f"Author: {result['author']}", file=sys.stderr)
    print(f"Content length: {result['contentLength']} characters", file=sys.stderr)

    # Save result
    result_path = os.path.join(output_dir, "article_source.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Print to stdout for Claude Code (force UTF-8 on Windows)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
