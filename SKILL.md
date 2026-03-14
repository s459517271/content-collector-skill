---
name: content-collector
description: "自动收集社交媒体内容（X/Twitter、即刻、公众号等）并整理成结构化笔记存入飞书文档。当用户发送链接或截图时使用此技能。支持每日定时提醒查看收藏内容。"
version: "1.1.0"
---

# Content Collector - 社交内容收藏助手

自动收集社交媒体精彩内容，AI 整理后存入飞书文档，每日定时提醒查看。

## 触发条件

当用户发送以下内容时自动触发：
- **链接**：X/Twitter、即刻、微信公众号、论坛帖子等
- **图片**：截图（自动 OCR 识别）
- **混合**：链接 + 截图

## 工作流程

```
用户发送链接/图片 → 检查去重 → 爬取内容 → AI 整理 → 存入飞书 → 每日提醒
```

### Step 1: 去重检查

**检查方式**：
1. **本地缓存**：检查 `.cache/collected_urls.json`
2. **文档检查**：检查飞书文档中是否已存在该链接
3. **URL 标准化**：去除追踪参数（utm_source、fbclid 等）

**脚本**：
```bash
python3 scripts/deduplicate.py "<url>" [doc_content_file]
```

### Step 2: 内容提取

**检测链接类型**：
- `x.com` / `twitter.com` → 使用 x-tweet-fetcher
- `mp.weixin.qq.com` → scripts/extract_weixin.py
- `m.okjike.com` / `web.okjike.com` → scripts/extract_jike.py
- `reddit.com` → scripts/extract_reddit.py
- 其他 → 通用 web_fetch

**检测图片**：
- OCR 识别文字内容 → scripts/ocr_image.py
- 提取其中的链接

### Step 3: 内容整理

**结构化信息**：
- 原文内容（完整保留）
- AI 摘要（3-5 句话）
- 作者/来源
- 发布时间
- 互动数据（点赞/转发/评论）
- 关键词标签
- 收藏理由

### Step 4: 存入飞书

**文档位置**：`社交内容收藏 - 每日精选`

**格式**：
```markdown
### {序号}. {标题}

| 属性 | 内容 |
|:---|:---|
| **作者** | {作者} |
| **平台** | {平台} |
| **发布时间** | {时间} |
| **原文链接** | [查看原帖]({url}) |
| **互动数据** | 👍 {likes} | 🔄 {retweets} | 💾 {bookmarks} | 👁️ {views} |

**原文内容**：
> {原文}

**AI 摘要**：
{摘要}

**关键词**：{关键词}

**为什么收藏**：
{收藏理由}

---
```

### Step 5: 每日提醒

**时间**：每天 18:00
**内容**：
- 当日收藏数量
- 内容标题列表
- 飞书文档链接
- 建议阅读提示

## 脚本使用

### 去重检查

```bash
python3 scripts/deduplicate.py "https://x.com/..."
```

### 提取 Twitter/X 内容

```bash
python3 scripts/extract_content.py --url "https://x.com/..."
```

### 提取即刻内容

```bash
python3 scripts/extract_jike.py "https://m.okjike.com/..."
```

### 提取公众号内容

```bash
python3 scripts/extract_weixin.py "https://mp.weixin.qq.com/..."
```

### 提取 Reddit 内容

```bash
python3 scripts/extract_reddit.py "https://reddit.com/r/..."
```

### 图片 OCR 识别

```bash
python3 scripts/ocr_image.py /path/to/image.png
```

### 格式化并追加到飞书

```bash
python3 scripts/append_to_feishu.py '<json_content>'
```

## 配置

**飞书文档 Token**：首次使用时创建文档，后续追加到同一文档

**Cron 任务**：自动创建每日 18:00 提醒
```bash
openclaw cron create \
  --name "daily-content-reminder" \
  --cron "0 18 * * *" \
  --message "📚 今日内容收藏提醒..." \
  --channel feishu
```

## 支持的来源

| 平台 | 支持程度 | 备注 |
|:---|:---|:---|
| X/Twitter | ✅ 完整 | 使用 x-tweet-fetcher |
| 即刻 | ✅ 完整 | scripts/extract_jike.py |
| 微信公众号 | ✅ 完整 | scripts/extract_weixin.py |
| Reddit | ✅ 完整 | scripts/extract_reddit.py + JSON API |
| Hacker News | ✅ 完整 | 使用 hn-api |
| 知乎 | ⚠️ 部分 | web_fetch |
| Bilibili | ⚠️ 部分 | web_fetch |
| 其他论坛 | ⚠️ 部分 | 视具体情况 |

## 去重机制

### URL 标准化

去除以下追踪参数：
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- `fbclid`, `gclid`
- `ref`, `source`

### 缓存存储

```
.cache/collected_urls.json
{
  "https://x.com/user/status/123": {
    "original_url": "https://x.com/...",
    "date": "2026-03-14T10:00:00",
    "metadata": {...}
  }
}
```

## OCR 支持

### 本地 OCR（可选）

```bash
# 安装依赖
pip install pytesseract pillow
apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### 云端 OCR

- 腾讯云数据万象 CI OCR
- 飞书内置 OCR

## 输出示例

见 `references/example-output.md`

## 依赖

- Python 3.8+
- x-tweet-fetcher skill
- feishu-doc skill
- web_fetch tool
- pytesseract (可选，用于本地 OCR)

## 更新日志

### v1.1.0 (2026-03-14)
- ✅ 添加去重机制（本地缓存 + 文档检查）
- ✅ 支持更多平台（即刻、公众号、Reddit 专用提取器）
- ✅ 添加图片 OCR 识别脚本
- ✅ 优化飞书文档格式（自动序号、互动数据格式化）

### v1.0.0 (2026-03-14)
- 初始版本
- 支持 X/Twitter、即刻、微信公众号
- 每日定时提醒

---

*由 OpenClaw 自动生成 | 版本 1.1.0*
