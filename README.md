# write-posts

> A [Claude Code](https://claude.ai/code) skill that turns any article URL into three platform-ready Chinese social media posts — in one command.

---

## What It Does

Paste any article URL. Claude fetches the content, reads it, and writes:

| Output | Platform | Length | Style |
|--------|----------|--------|-------|
| X post | X (Twitter) | ≤ 140 Chinese chars | Sharp, opinionated, one core insight |
| Threads post | Threads | 400–600 chars | Storytelling, conversational, ends with a question |
| Medium article | Medium | 1500–3000 chars | Deep analysis, Markdown, structured |

All three are written in Traditional Chinese, with a strict no-AI-sounding writing guide baked into the prompt.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4 lxml
```

### 2. Install the Skill

Copy the `.claude/` folder into your Claude Code project root:

```
your-project/
├── .claude/
│   └── skills/
│       └── write-posts/
│           └── SKILL.md
├── skills/
│   └── write-posts/
│       ├── scripts/
│       │   └── fetch_article.py
│       └── prompts/
│           └── write-posts.prompt
```

### 3. Run

```bash
/write-posts https://example.com/some-article
```

---

## Output

Files are saved to `outputs/posts/<timestamp>/`:

```
outputs/posts/20260221_143022/
├── article_source.json   ← fetched article metadata + content
├── x_post.md             ← X post
├── threads_post.md       ← Threads post
└── medium_article.md     ← Medium long-form article
```

---

## Writing Quality

The prompt enforces a strict anti-AI-sounding writing guide:

- **Varied sentence length** — short punchy lines mixed with longer ones
- **No mechanical connectors** — no 首先/其次/最後/總之
- **Show, don't tell** — concrete details over abstract summaries
- **Banned phrases** — 值得注意的是、在當今社會、綜上所述, and 16 more
- **Platform tone** — each post sounds native to its platform, not just a resized copy

Each post has a self-check rule before it's considered done:
- X: "Would this get a reply even without the hashtags?"
- Threads: "If I remove any paragraph, would readers notice?"
- Medium: "Can each section heading stand alone as an X post?"

---

## Directory Structure

```
.claude/
  skills/
    write-posts/
      SKILL.md           ← Claude Code skill entrypoint (simplified)

skills/
  write-posts/
    SKILL.md             ← Full workflow definition
    scripts/
      fetch_article.py   ← requests + BeautifulSoup article scraper
    prompts/
      write-posts.prompt ← Writing rules + output format
```

---

## Requirements

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Run scripts |
| Claude Code | AI writing + orchestration |
| requests | HTTP fetch |
| beautifulsoup4 + lxml | HTML parsing |

No API keys required — Claude Code handles all the writing directly.

---

## License

MIT
