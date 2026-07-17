# Claude Code Internals（内部机制剖析）

**Claude Code 的完整系统提示词、全部 58 个工具定义、以及 token 统计行为——
中英双语文档。**

[English version](README.md) · [详细解读](SUMMARY.zh-CN.md)

---

## 内容一览

| 路径 | 内容 |
|------|------|
| [SUMMARY.zh-CN.md](SUMMARY.zh-CN.md) | 中文版详细解读（提示词逐章 + 58 个工具逐个） |
| [SUMMARY.md](SUMMARY.md) | 英文版详细解读 |
| [groups/](groups/) | 提示词与工具内容，每个唯一组合一个文件夹 |

每个组的文件夹里都有英文原文 + 中文译文（`*.zh-CN.md`），以及基础统计 `meta.json`。

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

## 为什么全是 Anthropic 格式？

Claude Code 是 Anthropic 基于 Anthropic Messages API 构建的。即使你把它指向其他
LLM 端点，**客户端构造的仍然是 Anthropic 格式的请求**——Anthropic 的系统提示词结构、
Anthropic 的工具定义、Anthropic 的 `thinking` 字段——然后依赖端点（或其前面的网关）
来翻译或接受这种格式。所以本仓库里的内容是由**客户端**决定的，与最终回答的模型无关：
`groups/` 里的提示词和工具定义天然就是 Anthropic 风格的。

## 目录结构

```
├── README.md / README.zh-CN.md     ← 本文件（英/中）
├── SUMMARY.md / SUMMARY.zh-CN.md   ← 详细解读（英/中）
├── LICENSE                         ← CC-BY-4.0
└── groups/                         ← 提示词与工具内容
    ├── 01-ccd-desktop-a5fb6def/    ← 27K 通用代理提示词（标题生成进程）
    ├── 02-ccd-desktop-3eec97da/    ← ★ 主提示词 + 58 工具 + skills
    ├── 03/04-ccd-desktop-*/        ← 02 的构建变体
    ├── 05-token-probe-*/           ← Skill 工具探针
    ├── 06/08/09-token-probe-*/     ← 工具子集探针
    └── 07-no-system-*/             ← 文本片段探针
```

## 声明与许可

- 系统提示词与工具定义属于 **Anthropic 的知识产权**，**仅供学习研究**；
  内容随版本变化（来自 `cc_version=2.1.209`）。如 Anthropic 认为本仓库不妥，
  将应要求下架。
- 本仓库的解读、总结与翻译 © 仓库作者，以 [CC-BY-4.0](LICENSE) 授权。
- 内容中的个人路径与标识已替换为 `<占位符>`。
