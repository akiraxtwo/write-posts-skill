# Write Posts Agent

## Metadata

- **Skill Name**: write-posts
- **Version**: 1.0.0
- **Description**: 抓取任意網頁文章內容，Claude Code 自動撰寫三種中文社群貼文：X 推文、Threads 貼文、Medium 深度長文
- **Tags**: article, writing, x, threads, medium, social-media, chinese

## Trigger

`/write-posts <url>`

## Workflow

### Step 1: 抓取文章內容

Run `python skills/write-posts/scripts/fetch_article.py <url>`

- 使用 `requests` + `BeautifulSoup` 抓取網頁
- 提取文章標題、作者、正文、發布日期
- 輸出 JSON 到 stdout + 儲存到 `outputs/posts/<timestamp>/article_source.json`

### Step 2: Claude Code 閱讀文章

Claude Code 讀取 `article_source.json`，理解文章的：

- 核心論點與關鍵資訊
- 目標受眾與語境
- 可引用的數據或觀點

### Step 3: Claude Code 撰寫三種貼文

根據 `prompts/write-posts.prompt` 的規則，產出三種中文貼文：

**X 貼文：**

- 140 中文字以內
- 精煉核心觀點
- 3-5 個 hashtag
- 引發討論的語氣

**Threads 貼文：**

- 約 500 字
- 3-5 段故事性敘述
- 結尾帶互動問題

**Medium 深度長文：**

- 1500-3000 字
- 完整結構：標題 → 引言 → 正文（分小節）→ 結論
- 深度分析 + 延伸思考

### Step 4: 儲存結果

將三種貼文分別儲存為 Markdown 檔案：

```
outputs/posts/<timestamp>/
├── article_source.json    # 原始抓取結果
├── x_post.md              # X 推文
├── threads_post.md        # Threads 貼文
└── medium_article.md      # Medium 長文
```

### Step 4: 生成封面圖 (如果使用 Gemini 3 Pro)

如果當前使用的是 **Gemini 3 Pro** 或其他具備圖片生成能力的模型：

1. 讀取 `imagePrompt` (來自 Step 3 的輸出)
2. 使用 `generate_image` 工具生成圖片
3. 儲存為 `outputs/posts/<timestamp>/cover_image.png`
4. 向用戶展示生成的圖片

> [!NOTE]
> 如果沒有圖片生成能力，請跳過此步驟並告知用戶。

向用戶展示三種貼文內容及檔案路徑。

## Dependencies

- Python 3.10+
- `requests`: HTTP 請求
- `beautifulsoup4`: HTML 解析
- `lxml`: HTML parser backend

## Environment Variables

無需額外 API key — Claude Code 直接處理文章分析和貼文撰寫。
