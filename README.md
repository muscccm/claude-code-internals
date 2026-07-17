# Claude Code Internals

**The full system prompts, all 58 tool definitions, and the token-accounting behavior of
Claude Code — documented bilingually (English + 中文).**

**Claude Code 的完整系统提示词、全部 58 个工具定义、以及 token 统计行为——
中英双语文档。**

[中文 README](README.zh-CN.md) · [Detailed analysis](SUMMARY.md) · [详细解读](SUMMARY.zh-CN.md)

---

## What's inside / 内容一览

| Path | Contents |
|------|----------|
| [SUMMARY.md](SUMMARY.md) | Detailed English analysis of every prompt section and all 58 tools |
| [SUMMARY.zh-CN.md](SUMMARY.zh-CN.md) | 中文版详细解读（提示词逐章 + 工具逐个） |
| [groups/](groups/) | The prompt/tool captures, one folder per unique combination |

Each group folder contains the originals in English plus Chinese translations
(`*.zh-CN.md`), and a `meta.json` with basic statistics.

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

## Why is everything in Anthropic's format? / 为什么全是 Anthropic 格式？

Claude Code is built by Anthropic on the Anthropic Messages API. Even when you point it
at a different LLM endpoint, **the client still constructs Anthropic-format requests** —
Anthropic system-prompt structure, Anthropic tool definitions, Anthropic `thinking`
fields — and relies on the endpoint (or a gateway in front of it) to translate or accept
that format. So what you see in this repository is determined by the **client**, not by
whichever model ultimately answers: the prompts and tool definitions in `groups/` are
inherently Anthropic-flavored, regardless of backend.

Claude Code 是 Anthropic 基于 Anthropic Messages API 构建的。即使你把它指向其他
LLM 端点，**客户端构造的仍然是 Anthropic 格式的请求**——Anthropic 的系统提示词结构、
Anthropic 的工具定义、Anthropic 的 `thinking` 字段——然后依赖端点（或其前面的网关）
来翻译或接受这种格式。所以本仓库里的内容是由**客户端**决定的，与最终回答的模型无关：
`groups/` 里的提示词和工具定义天然就是 Anthropic 风格的。

## Repository structure / 目录结构

```
├── README.md / README.zh-CN.md     ← this file / 本文
├── SUMMARY.md / SUMMARY.zh-CN.md   ← detailed analysis / 详细解读
├── LICENSE                         ← CC-BY-4.0
└── groups/                         ← prompt & tool captures / 提示词与工具内容
    ├── 01-ccd-desktop-a5fb6def/    ← 27K general-agent prompt (title-gen process)
    ├── 02-ccd-desktop-3eec97da/    ← ★ main prompt + 58 tools + skills
    ├── 03/04-ccd-desktop-*/        ← build variants of 02
    ├── 05-token-probe-*/           ← Skill-tool probe
    ├── 06/08/09-token-probe-*/     ← tool-subset probes
    └── 07-no-system-*/             ← text-fragment probes
```

## Disclaimer & license / 声明与许可

- The system prompts and tool definitions are **Anthropic's intellectual property**,
  presented here **for educational research only**. They change across versions
  (from `cc_version=2.1.209`). If Anthropic objects to this repository's presence,
  it will be taken down on request.
- The analysis, summaries, and translations are © the repository author, licensed
  under [CC-BY-4.0](LICENSE).
- Personal paths and identifiers have been replaced with `<placeholders>`.

- 系统提示词与工具定义属于 **Anthropic 的知识产权**，**仅供学习研究**；
  内容随版本变化（来自 `cc_version=2.1.209`）。如 Anthropic 认为本仓库不妥，
  将应要求下架。
- 本仓库的解读、总结与翻译 © 仓库作者，以 [CC-BY-4.0](LICENSE) 授权。
- 内容中的个人路径与标识已替换为 `<占位符>`。
