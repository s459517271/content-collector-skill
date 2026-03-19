# Content Collector - 社交内容收藏助手

自动收集社交媒体内容 → AI 整理 → 存入飞书多维表格。

## 特性

- 🚀 **多平台支持**：X/Twitter、微信公众号、即刻、Reddit、知乎、Bilibili、Hacker News
- 🎯 **公众号完美抓取**：基于 Scrapling，完美绕过微信反爬
- 🤖 **AI 智能整理**：自动摘要、分类、关键词提取
- 📝 **飞书集成**：存入飞书云空间 + 多维表格
- 🔄 **去重机制**：避免重复收藏

## 快速开始

### 安装

```bash
# 复制到 OpenClaw skills 目录
cp -r content-collector ~/.openclaw/workspace/skills/

# 安装依赖（公众号抓取需要）
pip install scrapling html2text
scrapling install
```

### 配置

```bash
# 设置环境变量
export FEISHU_BITABLE_APP_TOKEN="your_app_token"
export FEISHU_BITABLE_TABLE_ID="your_table_id"
```

或复制 `.env.example` 为 `.env` 并填入配置。

### 使用

直接在对话中发送链接，skill 自动触发：
- X/Twitter 链接
- 微信公众号文章 (`mp.weixin.qq.com`)
- 即刻、Reddit、知乎、Bilibili、Hacker News
- 截图（OCR 识别后提取链接）

## 平台支持

| 平台 | 抓取方式 | 状态 |
|------|---------|------|
| X/Twitter | x-tweet-fetcher | ✅ 完美支持 |
| 微信公众号 | Scrapling | ✅ 完美支持 |
| 即刻 | defuddle | ✅ 支持 |
| Reddit | defuddle | ✅ 支持 |
| 知乎 | defuddle | ✅ 支持 |
| Bilibili | defuddle | ✅ 支持（标题/描述）|
| Hacker News | defuddle | ✅ 支持 |

## 多维表格字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 标题 | 文本 | 内容标题 |
| 来源 | 文本 | 作者/平台 |
| 分类 | 单选 | 分类标签 |
| 原文链接 | 超链接 | 原始链接 |
| 摘要内容 | 文本 | AI 生成的摘要 |
| 原文文件 | 超链接 | 飞书云空间 .md 文件 |
| 记录时间 | 创建时间 | 自动记录 |

## 目录结构

```
content-collector/
├── SKILL.md              # 主文件
├── scripts/              # 辅助脚本
│   ├── extract_content.py    # 平台检测
│   ├── deduplicate.py        # URL 去重
│   └── ...
└── references/           # 参考文档
    ├── platforms.md          # 平台映射
    └── feishu_config.md      # 飞书配置
```

---

## 作者与维护

**作者**: vigor  
**公众号**: 懂点儿AI  
**制作过程**: [从零打造 AI 内容收藏助手](https://mp.weixin.qq.com/s/hw4uKk-9ezaJlDpL1nEUuA)

---

## License

MIT