# Claude Code Internals（内部机制剖析）

**Claude Code 每次请求到底发了什么：完整的系统提示词、全部 58 个工具定义、
以及它的 token 统计行为——来自真实流量抓包，中英双语整理。**

[English README](README.md) · [详细解读](SUMMARY.zh-CN.md) · [Detailed analysis](SUMMARY.md)

---

## 内容一览

| 路径 | 内容 |
|------|------|
| [SUMMARY.zh-CN.md](SUMMARY.zh-CN.md) | 中文版详细解读（提示词逐章 + 58 个工具逐个） |
| [SUMMARY.md](SUMMARY.md) | 英文版详细解读 |
| [groups/](groups/) | 原始抓取内容，每组"提示词+工具组合"一个文件夹 |
| [extract_prompts.py](extract_prompts.py) | 提取脚本——可以对着你自己的 PrismCat 实例复现 |

每个组的文件夹里都有英文原文 + 中文译文（`*.zh-CN.md`），以及抓取元数据 `meta.json`。

## 核心发现

1. **每次请求都携带约 11.4K 字符系统提示词 + 约 124K 字符工具定义（58 个工具）**，
   这还没算一字对话内容。
2. **约 60% 的请求不是对话，而是 token 计数探针**——Claude Code 发送 `max_tokens=1`
   的请求分别称量上下文的每个部分（核心工具/扩展工具/MCP 工具/Skill/文本片段），
   用于 `/context` 构成分析和对话压缩决策。
3. **58 个工具恰好 = 11 核心 + 19 扩展 + 28 MCP + 1 Skill**，与探针测量分组完全对应。
4. **桌面应用生成会话标题时会单独派生一个 Agent SDK 进程**，加载它自己的
   27K 字符系统提示词（含完整记忆系统），不带任何工具。
5. **思考强度以 `output_config.effort` + `thinking: {"type": "adaptive"}` 传递**——
   旧的固定 `budget_tokens` 预算的新式定性替代。
6. **不同构建版本的客户端发送的提示词逐字相同**——只有构建号（`cc_version`）
   和模型 ID 字符串不同。

## 抓取方法

全部流量由自托管透明代理 [PrismCat](https://github.com/paopaoandlingyia/PrismCat)
抓取（部署在家庭 NAS 上）：

```
Claude Code → 本地供应商切换代理 → PrismCat（记录全部流量）→ LLM 端点
```

PrismCat 只需修改客户端的 `base_url`，即可把完整请求/响应（含 SSE 流）记录到本地
数据库，完全不修改请求——你看到的就是客户端实际发送的内容。本仓库的
`extract_prompts.py` 可以对任何 PrismCat 实例复现整个提取过程（分组、去重、生成文档）。

## 目录结构

```
├── README.md / README.zh-CN.md     ← 本文件（英/中）
├── SUMMARY.md / SUMMARY.zh-CN.md   ← 详细解读（英/中）
├── LICENSE                         ← CC-BY-4.0
├── extract_prompts.py              ← 提取脚本
└── groups/                         ← 原始抓取
    ├── 01-ccd-desktop-a5fb6def/    ← 27K 通用代理提示词（标题生成进程）
    ├── 02-ccd-desktop-3eec97da/    ← ★ 主提示词 + 58 工具 + skills
    ├── 03/04-ccd-desktop-*/        ← 02 的构建变体
    ├── 05-token-probe-*/           ← Skill 工具探针
    ├── 06/08/09-token-probe-*/     ← 工具子集探针
    └── 07-no-system-*/             ← 文本片段探针
```

## 声明与许可

- 抓取的系统提示词与工具定义属于 **Anthropic 的知识产权**，来自作者自己的客户端流量，
  **仅供学习研究**；内容随版本变化（抓取自 `cc_version=2.1.209`）。如 Anthropic
  认为本仓库不妥，将应要求下架。
- 本文档的解读、总结、翻译与提取脚本 © 仓库作者，以 [CC-BY-4.0](LICENSE) 授权。
- 抓取内容中的个人路径与标识已替换为 `<占位符>`。
