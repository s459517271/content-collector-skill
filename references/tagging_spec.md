# 内容收藏标签规范 v1.0

> ⚠️ **已停用** - 本规范已被 Step 4 v2.0 独立生成模式替代
> 
> 新方案不再使用历史标签池匹配，采用独立生成 + 固定结构模式

## 核心原则

| 原则 | 说明 |
|------|------|
| **唯一性** | 相同内容 → 相同标签，不允许重复或变体 |
| **垂直化** | 标签要具体，不要泛泛的 "技术"、"AI" |
| **有限数量** | 每篇最多 5 个标签 |
| **自动创建** | 新标签自动添加到飞书，无需手动 |

---

## 一、标签分类体系

标签分为 **4 大类**：

| 类别 | 范围 | 示例 |
|------|------|------|
| **技术栈** | 编程语言、框架、工具 | agent, mcp, openclaw, claude code |
| **领域** | 垂直应用领域 | 量化交易, 浏览器自动化, 记忆系统 |
| **内容形式** | 文章类型/用途 | 产品思考, 学习资源, 实战案例, 工具推荐 |
| **方法论** | 工作方式/思维 | prompt, 工作流, 评测 |

---

## 二、标签命名规范

### 2.1 格式要求

| 规则 | 示例 |
|------|------|
| **统一小写** | `agent` ❌ `Agent` ❌ `AGENT` |
| **英文优先** | 用 `agent` 不用 "代理" |
| **用英文连字符** | `deep-research` ❌ `deep_research` |
| **不加复数** | `agent` ❌ `agents` |
| **纯中文标签** | `量化交易`, `产品思考` |

### 2.2 已定义标签（13个）

```
【技术栈】
agent        → Agent 相关（LLM编程、Autonomous AI）
mcp          → MCP (Model Context Protocol)
openclaw     → OpenClaw 相关
claude-code  → Claude Code 相关

【领域】
浏览器自动化 → 浏览器控制、Playwright、puppeteer
记忆系统    → AI 记忆、个人知识管理
量化交易    → 量化投资、交易策略

【内容形式】
产品思考    → 产品分析、思考、观点
学习资源    → 教程、文档、课程
实战案例    → 实战项目、代码演示
工具推荐    → 好用工具、软件推荐

【方法论】
prompt       → Prompt 工程、提示词技巧
工作流       → 工作流、自动化流程
评测         → 评测、benchmark、对比
```

---

## 三、匹配规则

### 3.1 优先级

```
1. 精确匹配（忽略大小写）
   "Agent" → agent ✓
   "MCP Server" → mcp ✓

2. 语义近似匹配
   "LLM Programming" → agent
   "AutoGPT" → agent
   "提示词工程" → prompt

3. 领域关键词匹配（精准匹配）
   "量化交易系统" → 量化交易
   "量化策略" → 量化交易
   "backtest" → 量化交易
   注意：通用词如"投资"、"交易"不直接映射到量化交易
```

### 3.2 关键词映射表

```python
TAG_KEYWORDS = {
    "agent": [
        "agent", "autonomous", "llm programming", "auto-gpt", 
        "agent loop", "agent architecture", "reAct", "tool use",
        "ai assistant", " autonomous ai", "agent system"
    ],
    "mcp": [
        "mcp", "model context protocol", "mcp server", 
        "mcp tool", "anthropic mcp"
    ],
    "openclaw": [
        "openclaw", "openclaw code", "open agent"
    ],
    "claude-code": [
        "claude code", "claude code cli", "@claude", "cody"
    ],
    "浏览器自动化": [
        "browser automation", "playwright", "puppeteer",
        "browser control", "web scraping", "headless browser"
    ],
    "记忆系统": [
        "memory", "long term memory", "知识图谱",
        "personal knowledge", "second brain", "ai memory"
    ],
    "量化交易": [
        "量化", "trading", "quant", "交易策略",
        " algorithmic trading", "量化投资", "quantitative",
        "backtest", "回测", "因子", "策略"
    ],
    "产品思考": [
        "product", "产品", "思考", "观点", "分析",
        "insight", "opinion", "strategy"
    ],
    "学习资源": [
        "tutorial", "教程", "learn", "course", "文档",
        "documentation", "guide", "入门", "教学"
    ],
    "实战案例": [
        "实战", "project", "案例", "code", "代码示例",
        "implementation", "demo", "workshop"
    ],
    "工具推荐": [
        "tool", "工具", "software", "app", "推荐",
        "resource", "awesome", "collection"
    ],
    "prompt": [
        "prompt", "提示词", "prompt engineering",
        "few-shot", "chain of thought", "role playing"
    ],
    "工作流": [
        "workflow", "工作流", "automation", "pipeline",
        "chain", "orchestration", "flow"
    ],
    "评测": [
        "benchmark", "评测", "evaluation", "评测",
        "test", "comparison", "performance"
    ]
}
```

---

## 四、打标流程

```
Step 1: 读取飞书已有标签池
Step 2: 分析内容，提取关键主题
Step 3: 根据关键词映射表匹配标签
Step 4: 去重（忽略大小写）
Step 5: 不足5个时，补充相关标签
Step 6: 新标签自动创建到飞书
```

### 示例

**内容标题**: "深入理解 Claude Code 的 Agent 架构"

**匹配过程**:
1. 关键词提取: "Claude Code", "Agent", "架构"
2. 匹配: `claude-code`, `agent`
3. 领域识别: 技术教程 → `学习资源`
4. 最终标签: `[agent, claude-code, 学习资源]` (3个)

---

## 五、垂直领域扩展

当遇到新领域时，按以下规则扩展：

### 5.1 扩展规则

| 情况 | 处理方式 |
|------|----------|
| 新技术栈 | 用英文小写，如 `langchain`, `crewai` |
| 新垂直领域 | 用中文或英文，如 `ai-avatar`, `虚拟主播` |
| 新方法论 | 用英文或中文，如 `cot`, `思维链` |

### 5.2 建议新增标签（预留）

```
技术栈: langchain, crewai, llama-index, rag
领域:   ai-avatar, 虚拟主播, 代码生成, 语音ai
方法论: cot(思维链), few-shot, 反思机制
```

---

## 六、标签应用示例

| 内容 | 匹配标签 |
|------|----------|
| "OpenClaw 实战教程" | openclaw, 实战案例, 学习资源 |
| "MCP Server 开发指南" | mcp, 学习资源, 工具推荐 |
| "用 Playwright 自动填表" | 浏览器自动化, 实战案例, 工具推荐 |
| "AI Agent memory 设计" | agent, 记忆系统, 产品思考 |
| "量化交易回测框架" | 量化交易, 工具推荐, 实战案例 |
| "Prompt 工程最佳实践" | prompt, 学习资源 |
| "Claude Code 评测对比" | claude-code, 评测, 学习资源 |
| "Workflow Automation 教程" | 工作流, 学习资源 |

---

## 七、强制检查清单

每次打标前必须检查：

- [ ] 标签是否全部小写
- [ ] 是否有重复标签（忽略大小写）
- [ ] 标签数量是否 ≤ 5
- [ ] 是否用了已有标签池中的标签
- [ ] 新标签是否符合命名规范
