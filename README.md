# Claude Code Internals

**The full system prompts, all 58 tool definitions, and the token-accounting behavior of
Claude Code — documented bilingually.**

[Chinese version](README.zh-CN.md) · [Detailed analysis](SUMMARY.md)

---

## What's inside

| Path | Contents |
|------|----------|
| [SUMMARY.md](SUMMARY.md) | Detailed analysis of every prompt section and all 58 tools |
| [groups/](groups/) | The prompt/tool content, one folder per unique combination |

Each group folder contains the originals in English plus Chinese translations
(`*.zh-CN.md`), and a `meta.json` with basic statistics.

## Key findings

1. **Every request carries ~11.4K chars of system prompt + ~124K chars of tool
   definitions** (58 tools) before a single word of conversation.

2. **~60% of requests are not conversations at all — they are token-counting probes.**
   Claude Code sends `max_tokens=1` requests to weigh every context part
   (core tools / extended tools / MCP tools / Skill / text fragments separately),
   feeding the `/context` breakdown and compaction decisions.

3. **The 58 tools decompose exactly into 11 core + 19 extended + 28 MCP + 1 Skill** —
   the same grouping the probes measure.

4. **The desktop app generates conversation titles with a separate Agent SDK process**
   that loads its own 27K-char system prompt (with the full memory system) and no tools.

5. **Reasoning effort is sent as `output_config.effort` with
   `thinking: {"type": "adaptive"}`** — the newer qualitative replacement for the fixed
   `budget_tokens` thinking budget.

6. **Different client builds send byte-identical prompts** — only the build stamp
   (`cc_version`) and model-ID string differ.

## Why is everything in Anthropic's format?

Claude Code is built by Anthropic on the Anthropic Messages API. Even when you point it
at a different LLM endpoint, **the client still constructs Anthropic-format requests** —
Anthropic system-prompt structure, Anthropic tool definitions, Anthropic `thinking`
fields — and relies on the endpoint (or a gateway in front of it) to translate or accept
that format. So what you see in this repository is determined by the **client**, not by
whichever model ultimately answers: the prompts and tool definitions in `groups/` are
inherently Anthropic-flavored, regardless of backend.

## Repository structure

```
├── README.md / README.zh-CN.md     ← this file (EN) / Chinese version
├── SUMMARY.md / SUMMARY.zh-CN.md   ← detailed analysis (EN) / Chinese version
├── LICENSE                         ← CC-BY-4.0
└── groups/                         ← prompt & tool content
    ├── 01-ccd-desktop-a5fb6def/    ← 27K general-agent prompt (title-gen process)
    ├── 02-ccd-desktop-3eec97da/    ← ★ main prompt + 58 tools + skills
    ├── 03/04-ccd-desktop-*/        ← build variants of 02
    ├── 05-token-probe-*/           ← Skill-tool probe
    ├── 06/08/09-token-probe-*/     ← tool-subset probes
    └── 07-no-system-*/             ← text-fragment probes
```

## Disclaimer & license

- The system prompts and tool definitions are **Anthropic's intellectual property**,
  presented here **for educational research only**. They change across versions
  (from `cc_version=2.1.209`). If Anthropic objects to this repository's presence,
  it will be taken down on request.
- The analysis, summaries, and translations are © the repository author, licensed
  under [CC-BY-4.0](LICENSE).
- Personal paths and identifiers have been replaced with `<placeholders>`.
