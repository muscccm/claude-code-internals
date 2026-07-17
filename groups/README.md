# Groups Index

> 234 requests deduplicated into 9 unique (system prompt + tools) combinations.
> Each folder holds the English originals, Chinese translations (`*.zh-CN.md`),
> and a `meta.json` with basic statistics.
>
> [中文索引](README.zh-CN.md)

| Folder | What it is | System size | Tools | Requests |
|--------|-----------|-------------|-------|----------|
| [title-generation-prompt](title-generation-prompt) | The desktop app's title-generation agent prompt | 27001 | 0 | 1 |
| [main-prompt-and-tools](main-prompt-and-tools) | ★ The main Claude Code prompt + all 58 tools + skills | 11445 | 58 | 58 |
| [main-prompt-build-74d](main-prompt-build-74d) | Same as main, from build `2.1.209.74d` | 11445 | 58 | 4 |
| [main-prompt-build-fable5](main-prompt-build-fable5) | Same as main, model ID written `claude-fable-5` | 11441 | 58 | 1 |
| [probe-skill-tool](probe-skill-tool) | Token probe: Skill tool only | 0 | 1 | 18 |
| [probe-extended-tools](probe-extended-tools) | Token probe: 19 extended built-in tools | 0 | 19 | 9 |
| [probe-text-fragments](probe-text-fragments) | Token probe: loose text fragments (no tools) | 0 | 0 | 123 |
| [probe-mcp-tools](probe-mcp-tools) | Token probe: 28 MCP tools | 0 | 28 | 5 |
| [probe-core-tools](probe-core-tools) | Token probe: 11 core tools | 0 | 11 | 9 |

## What each group is

- **title-generation-prompt** — The 27K-char Claude Agent SDK general-agent prompt used by
  the desktop app's title-generation process; seen once, no tools.
- **main-prompt-and-tools** — The main Claude Code system prompt + all 58 tool
  definitions + skill blocks. The primary artifact of this repository.
- **main-prompt-build-74d / main-prompt-build-fable5** — Build variants of the main
  prompt: identical content, only the `cc_version` build stamp / model-ID string differs.
- **probe-skill-tool** — Probe carrying only the **Skill** tool (its description changes
  as skills load, so it is weighed separately).
- **probe-extended-tools** — Probe carrying the 19 **extended built-in** tools.
- **probe-text-fragments** — Fragment probes (no system, no tools) plus a few manual
  test requests.
- **probe-mcp-tools** — Probe carrying the 28 **MCP** tools.
- **probe-core-tools** — Probe carrying the 11 **core** tools.

All probes use `max_tokens=1` to weigh input token counts — see
[SUMMARY.md](../SUMMARY.md) section 4.
