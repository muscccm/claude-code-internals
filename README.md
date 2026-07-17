# Claude Code Internals

**What Claude Code actually sends with every request: the full system prompts, all 58
tool definitions, and its token-accounting behavior — captured from live traffic and
documented bilingually.**

**Claude Code 每次请求到底发了什么：完整的系统提示词、全部 58 个工具定义、
以及它的 token 统计行为——来自真实流量抓包，中英双语整理。**

[中文 README](README.zh-CN.md) · [Detailed analysis](SUMMARY.md) · [详细解读](SUMMARY.zh-CN.md)

---

## What's inside / 内容一览

| Path | Contents |
|------|----------|
| [SUMMARY.md](SUMMARY.md) | Detailed English analysis of every prompt section and all 58 tools |
| [SUMMARY.zh-CN.md](SUMMARY.zh-CN.md) | 中文版详细解读（提示词逐章 + 工具逐个） |
| [groups/](groups/) | The raw captures, one folder per unique prompt+tools combination |
| [extract_prompts.py](extract_prompts.py) | The extraction script — reproduce this against your own PrismCat instance |

Each group folder contains the originals in English plus Chinese translations
(`*.zh-CN.md`), and a `meta.json` with capture metadata.

## Key findings / 核心发现

1. **Every request carries ~11.4K chars of system prompt + ~124K chars of tool
   definitions** (58 tools) before a single word of conversation.
   每次请求还没算对话内容，就先带上约 11.4K 字符的系统提示词和约 124K 字符的工具定义（58 个工具）。

2. **~60% of requests are not conversations at all — they are token-counting probes.**
   Claude Code sends `max_tokens=1` requests to weigh every context part
   (core tools / extended tools / MCP tools / Skill / text fragments separately),
   feeding the `/context` breakdown and compaction decisions.
   约 60% 的请求根本不是对话，而是 token 计数探针：Claude Code 用 `max_tokens=1`
   的请求分别称量上下文的每个部分，用于 `/context` 构成分析和压缩决策。

3. **The 58 tools decompose exactly into 11 core + 19 extended + 28 MCP + 1 Skill** —
   the same grouping the probes measure.
   58 个工具恰好可以分解为 11 核心 + 19 扩展 + 28 MCP + 1 Skill，与探针的分组完全对应。

4. **The desktop app generates conversation titles with a separate Agent SDK process**
   that loads its own 27K-char system prompt (with the full memory system) and no tools.
   桌面应用生成会话标题时会单独派生一个 Agent SDK 进程，加载它自己的 27K 字符系统提示词
   （含完整记忆系统），不带任何工具。

5. **Reasoning effort is sent as `output_config.effort` with
   `thinking: {"type": "adaptive"}`** — the newer qualitative replacement for the fixed
   `budget_tokens` thinking budget.
   思考强度以 `output_config.effort` + `thinking: {"type": "adaptive"}` 的形式传递——
   这是旧的固定 `budget_tokens` 预算的新式定性替代。

6. **Different client builds send byte-identical prompts** — only the build stamp
   (`cc_version`) and model-ID string differ.
   不同构建版本的客户端发送的提示词逐字相同，只有构建号和模型 ID 字符串不同。

## How this was captured / 抓取方法

All traffic was captured with [PrismCat](https://github.com/paopaoandlingyia/PrismCat),
a self-hosted transparent LLM proxy, deployed on a home NAS:

```
Claude Code → local provider-switching proxy → PrismCat (logging everything) → LLM endpoint
```

PrismCat only requires changing the client's `base_url`; it records full request/response
headers and bodies (including SSE streams) into a local database. No requests were
modified — this is exactly what the client sends. `extract_prompts.py` in this repo
reproduces the extraction (grouping, dedup, doc generation) against any PrismCat instance.

所有流量由自托管透明代理 PrismCat 抓取（部署在家庭 NAS 上）。只需修改客户端的
`base_url`，PrismCat 就会把完整的请求/响应（含 SSE 流）记录到本地数据库，
完全不修改请求——你看到的就是客户端实际发送的内容。仓库里的
`extract_prompts.py` 可以对任何 PrismCat 实例复现整个提取过程。

## Repository structure / 目录结构

```
├── README.md / README.zh-CN.md     ← this file / 本文
├── SUMMARY.md / SUMMARY.zh-CN.md   ← detailed analysis / 详细解读
├── LICENSE                         ← CC-BY-4.0
├── extract_prompts.py              ← extraction script / 提取脚本
└── groups/                         ← raw captures / 原始抓取
    ├── 01-ccd-desktop-a5fb6def/    ← 27K general-agent prompt (title-gen process)
    ├── 02-ccd-desktop-3eec97da/    ← ★ main prompt + 58 tools + skills
    ├── 03/04-ccd-desktop-*/        ← build variants of 02
    ├── 05-token-probe-*/           ← Skill-tool probe
    ├── 06/08/09-token-probe-*/     ← tool-subset probes
    └── 07-no-system-*/             ← text-fragment probes
```

## Disclaimer & license / 声明与许可

- The captured system prompts and tool definitions are **Anthropic's intellectual
  property**, captured from the author's own client traffic **for educational research
  only**. They change across versions (captured from `cc_version=2.1.209`). If Anthropic
  objects to this repository's presence, it will be taken down on request.
- The analysis, summaries, translations, and the extraction script are © the repository
  author, licensed under [CC-BY-4.0](LICENSE).
- Personal paths and identifiers in the captures have been replaced with `<placeholders>`.

- 抓取的系统提示词与工具定义属于 **Anthropic 的知识产权**，来自作者自己的客户端流量，
  **仅供学习研究**；内容随版本变化（抓取自 `cc_version=2.1.209`）。如 Anthropic
  认为本仓库不妥，将应要求下架。
- 本文档的解读、总结、翻译与提取脚本 © 仓库作者，以 [CC-BY-4.0](LICENSE) 授权。
- 抓取内容中的个人路径与标识已替换为 `<占位符>`。
