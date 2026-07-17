# 分组索引

> 234 条请求，去重后 9 组"系统提示词 + 工具"组合。
> 每组文件夹里有英文原文、中文译文（`*.zh-CN.md`）和基础统计 `meta.json`。
>
> [English index](README.md)

| 文件夹 | 内容 | system 大小 | 工具数 | 请求数 |
|--------|------|------------|--------|--------|
| [title-generation-prompt](title-generation-prompt) | 桌面应用标题生成代理的提示词 | 27001 | 0 | 1 |
| [main-prompt-and-tools](main-prompt-and-tools) | ★ Claude Code 主提示词 + 全部 58 工具 + skills | 11445 | 58 | 58 |
| [main-prompt-build-74d](main-prompt-build-74d) | 同上，来自构建 `2.1.209.74d` | 11445 | 58 | 4 |
| [main-prompt-build-fable5](main-prompt-build-fable5) | 同上，模型 ID 写作 `claude-fable-5` | 11441 | 58 | 1 |
| [probe-skill-tool](probe-skill-tool) | token 探针：仅 Skill 工具 | 0 | 1 | 18 |
| [probe-extended-tools](probe-extended-tools) | token 探针：19 个扩展内置工具 | 0 | 19 | 9 |
| [probe-text-fragments](probe-text-fragments) | token 探针：零散文本片段（无工具） | 0 | 0 | 123 |
| [probe-mcp-tools](probe-mcp-tools) | token 探针：28 个 MCP 工具 | 0 | 28 | 5 |
| [probe-core-tools](probe-core-tools) | token 探针：11 个核心工具 | 0 | 11 | 9 |

## 每组是什么

- **title-generation-prompt** — 桌面应用标题生成进程使用的 27K 字符 Claude Agent SDK
  通用代理提示词；只出现一次，不带工具。
- **main-prompt-and-tools** — Claude Code 主系统提示词 + 全部 58 个工具定义 + skill 块。
  本仓库的核心内容。
- **main-prompt-build-74d / main-prompt-build-fable5** — 主提示词的构建变体：
  内容相同，仅 `cc_version` 构建号 / 模型 ID 字符串不同。
- **probe-skill-tool** — 只携带 **Skill** 工具的探针（其描述随技能加载变化，单独称量）。
- **probe-extended-tools** — 携带 19 个**扩展内置**工具的探针。
- **probe-text-fragments** — 片段探针（无 system、无工具）加少量手工测试请求。
- **probe-mcp-tools** — 携带 28 个 **MCP** 工具的探针。
- **probe-core-tools** — 携带 11 个**核心**工具的探针。

所有探针都用 `max_tokens=1` 来称量输入 token 数——详见
[SUMMARY.zh-CN.md](../SUMMARY.zh-CN.md) 第四节。
