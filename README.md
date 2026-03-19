# Content Collector

Auto-collect social media content → AI summarize → Save to Feishu.

## Features

- 🚀 **Multi-platform**: X/Twitter, WeChat, Jike, Reddit, Zhihu, Bilibili, HN
- 🎯 **WeChat perfected**: Scrapling-based, bypasses anti-scraping
- 🤖 **AI summarized**: Auto-generate summary, classify, extract keywords
- 📝 **Feishu integrated**: Save to Feishu Drive + Bitable
- 🔄 **Deduplication**: Avoid duplicate collections

## Quick Start

### Install

```bash
# Copy to OpenClaw skills directory
cp -r content-collector ~/.openclaw/workspace/skills/

# Install dependencies (for WeChat)
pip install scrapling html2text
scrapling install
```

### Configure

```bash
# Set environment variables
export FEISHU_BITABLE_APP_TOKEN="your_app_token"
export FEISHU_BITABLE_TABLE_ID="your_table_id"
```

Or copy `.env.example` to `.env` and fill in values.

### Usage

Just share a link in chat. The skill auto-triggers for:
- X/Twitter links
- WeChat articles (`mp.weixin.qq.com`)
- Jike, Reddit, Zhihu, Bilibili, HN
- Screenshots (OCR → extract URL)

## Platform Support

| Platform | Method | Status |
|----------|--------|--------|
| X/Twitter | x-tweet-fetcher | ✅ Perfect |
| WeChat | Scrapling | ✅ Perfect |
| Jike | defuddle | ✅ Works |
| Reddit | defuddle | ✅ Works |
| Zhihu | defuddle | ✅ Works |
| Bilibili | defuddle | ✅ Title/desc |
| Hacker News | defuddle | ✅ Works |

## Bitable Fields

| Field | Type | Description |
|-------|------|-------------|
| 标题 | Text | Title |
| 来源 | Text | Source |
| 分类 | Single Select | Category |
| 原文链接 | URL | Original link |
| 摘要内容 | Text | AI summary |
| 原文文件 | URL | Feishu Drive .md file |
| 记录时间 | Created Time | Auto |

## Directory Structure

```
content-collector/
├── SKILL.md              # Main skill file
├── scripts/              # Helper scripts
│   ├── extract_content.py    # Platform detection
│   ├── deduplicate.py        # URL deduplication
│   └── ...
└── references/           # Reference docs
    ├── platforms.md          # Platform mapping
    └── feishu_config.md      # Feishu setup
```

## License

MIT

---

**Author**: vigor - [懂点儿AI](https://mp.weixin.qq.com/s/hw4uKk-9ezaJlDpL1nEUuA)