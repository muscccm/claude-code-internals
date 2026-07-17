# Groups Index

> 234 requests deduplicated into 9 unique (system prompt + tools) combinations.
> Each group folder holds the English originals, Chinese translations (`*.zh-CN.md`),
> and a `meta.json` with basic statistics.
>
> [Chinese index](README.zh-CN.md)

| # | Label | Hash | System size | Tools | Requests | Folder |
|---|-------|------|-------------|-------|----------|--------|
| 1 | ccd-desktop | a5fb6def | 27001 | 0 | 1 | [01-ccd-desktop-a5fb6def](01-ccd-desktop-a5fb6def) |
| 2 | ccd-desktop | 3eec97da | 11445 | 58 | 58 | [02-ccd-desktop-3eec97da](02-ccd-desktop-3eec97da) |
| 3 | ccd-desktop | 0dc1ed0b | 11445 | 58 | 4 | [03-ccd-desktop-0dc1ed0b](03-ccd-desktop-0dc1ed0b) |
| 4 | ccd-desktop | a55f3160 | 11441 | 58 | 1 | [04-ccd-desktop-a55f3160](04-ccd-desktop-a55f3160) |
| 5 | token-probe | d813ea35 | 0 | 1 | 18 | [05-token-probe-d813ea35](05-token-probe-d813ea35) |
| 6 | token-probe | abd8d3b7 | 0 | 19 | 9 | [06-token-probe-abd8d3b7](06-token-probe-abd8d3b7) |
| 7 | no-system | 3eb41622 | 0 | 0 | 123 | [07-no-system-3eb41622](07-no-system-3eb41622) |
| 8 | token-probe | 93caae64 | 0 | 28 | 5 | [08-token-probe-93caae64](08-token-probe-93caae64) |
| 9 | token-probe | 59b2704e | 0 | 11 | 9 | [09-token-probe-59b2704e](09-token-probe-59b2704e) |

## What each group is

- **01** — The 27K-char Claude Agent SDK general-agent prompt used by the desktop app's
  title-generation process; seen once, no tools.
- **02** — The main Claude Code system prompt + all 58 tool definitions + skill blocks.
  The primary artifact of this repository.
- **03 / 04** — Build variants of 02: identical content, only the `cc_version` build
  stamp / model-ID string differs.
- **05** — Token-counting probe carrying only the **Skill** tool (its description changes
  as skills load, so it is weighed separately).
- **06** — Probe carrying the 19 **extended built-in** tools.
- **07** — Fragment probes (no system, no tools) plus a few manual test requests.
- **08** — Probe carrying the 28 **MCP** tools.
- **09** — Probe carrying the 11 **core** tools.

All probes use `max_tokens=1` to weigh input token counts — see
[SUMMARY.md](../SUMMARY.md) section 4.
