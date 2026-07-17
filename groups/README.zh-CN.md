# 分组索引

> 234 条请求，去重后 9 组"系统提示词 + 工具"组合。
> 每组文件夹里有英文原文、中文译文（`*.zh-CN.md`）和基础统计 `meta.json`。
>
> [English index](README.md)

| # | 来源 | 哈希 | system 大小 | 工具数 | 请求数 | 文件夹 |
|---|------|------|------------|--------|--------|--------|
| 1 | ccd-desktop | a5fb6def | 27001 | 0 | 1 | [01-ccd-desktop-a5fb6def](01-ccd-desktop-a5fb6def) |
| 2 | ccd-desktop | 3eec97da | 11445 | 58 | 58 | [02-ccd-desktop-3eec97da](02-ccd-desktop-3eec97da) |
| 3 | ccd-desktop | 0dc1ed0b | 11445 | 58 | 4 | [03-ccd-desktop-0dc1ed0b](03-ccd-desktop-0dc1ed0b) |
| 4 | ccd-desktop | a55f3160 | 11441 | 58 | 1 | [04-ccd-desktop-a55f3160](04-ccd-desktop-a55f3160) |
| 5 | token-probe | d813ea35 | 0 | 1 | 18 | [05-token-probe-d813ea35](05-token-probe-d813ea35) |
| 6 | token-probe | abd8d3b7 | 0 | 19 | 9 | [06-token-probe-abd8d3b7](06-token-probe-abd8d3b7) |
| 7 | no-system | 3eb41622 | 0 | 0 | 123 | [07-no-system-3eb41622](07-no-system-3eb41622) |
| 8 | token-probe | 93caae64 | 0 | 28 | 5 | [08-token-probe-93caae64](08-token-probe-93caae64) |
| 9 | token-probe | 59b2704e | 0 | 11 | 9 | [09-token-probe-59b2704e](09-token-probe-59b2704e) |

## 每组是什么

- **01** — 桌面应用标题生成进程使用的 27K 字符 Claude Agent SDK 通用代理提示词；
  只出现一次，不带工具。
- **02** — Claude Code 主系统提示词 + 全部 58 个工具定义 + skill 块。
  本仓库的核心内容。
- **03 / 04** — 02 的构建变体：内容相同，仅 `cc_version` 构建号 / 模型 ID 字符串不同。
- **05** — 只携带 **Skill** 工具的 token 计数探针（其描述随技能加载变化，单独称量）。
- **06** — 携带 19 个**扩展内置**工具的探针。
- **07** — 片段探针（无 system、无工具）加少量手工测试请求。
- **08** — 携带 28 个 **MCP** 工具的探针。
- **09** — 携带 11 个**核心**工具的探针。

所有探针都用 `max_tokens=1` 来称量输入 token 数——详见
[SUMMARY.zh-CN.md](../SUMMARY.zh-CN.md) 第四节。
