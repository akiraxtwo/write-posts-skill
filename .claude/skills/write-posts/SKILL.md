---
name: write-posts
description: Fetch article from URL, write X post + Threads post + Medium article in Chinese
argument-hint: <url>
disable-model-invocation: true
---

# Write Posts — 文章轉社群貼文

根據使用者提供的文章 URL，抓取內容後撰寫三種中文社群貼文。

## 執行步驟

### Step 1: 抓取文章
```bash
python skills/write-posts/scripts/fetch_article.py $ARGUMENTS
```
- 抓取網頁內容，提取標題、作者、正文、發布日期
- 輸出 JSON 到 stdout，同時儲存到 `outputs/posts/<timestamp>/article_source.json`

### Step 2: 閱讀文章內容
讀取 Step 1 輸出的 JSON，理解文章的核心論點、關鍵資訊、目標受眾。

### Step 3: 撰寫三種貼文
參照 `skills/write-posts/prompts/write-posts.prompt` 中的規則，撰寫：

1. **X 貼文** — 140 中文字以內，精煉觀點 + hashtag
2. **Threads 貼文** — 400-600 字，故事性敘述 + 互動問題
3. **Medium 深度長文** — 1500-3000 字，完整結構的 Markdown 文章

**必須遵守 prompt 中的「去 AI 味寫作準則」和「禁用詞清單」。**

### Step 4: 儲存結果
將三種貼文分別儲存為 Markdown 檔案，放在 Step 1 建立的輸出目錄中：
```
outputs/posts/<timestamp>/
├── article_source.json
├── x_post.md
├── threads_post.md
└── medium_article.md
```

向使用者展示三種貼文的完整內容和檔案路徑。
