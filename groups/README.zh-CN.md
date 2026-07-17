# PrismCat 抓取内容整理
> 生成时间见文件修改时间；来源：`http://<prismcat-host>:8080` 的全部日志。
> 共 234 条日志，去重后 9 组 (system+tools) 组合。

| # | 来源 | 哈希 | system 大小 | 工具数 | 请求数 | 文件夹 |
|---|------|------|------------|--------|--------|--------|
| 1 | ccd-desktop | a5fb6def | 27001 | 0 | 1 | 01-ccd-desktop-a5fb6def |
| 2 | ccd-desktop | 3eec97da | 11445 | 58 | 58 | 02-ccd-desktop-3eec97da |
| 3 | ccd-desktop | 0dc1ed0b | 11445 | 58 | 4 | 03-ccd-desktop-0dc1ed0b |
| 4 | ccd-desktop | a55f3160 | 11441 | 58 | 1 | 04-ccd-desktop-a55f3160 |
| 5 | token-probe | d813ea35 | 0 | 1 | 18 | 05-token-probe-d813ea35 |
| 6 | token-probe | abd8d3b7 | 0 | 19 | 9 | 06-token-probe-abd8d3b7 |
| 7 | no-system | 3eb41622 | 0 | 0 | 123 | 07-no-system-3eb41622 |
| 8 | token-probe | 93caae64 | 0 | 28 | 5 | 08-token-probe-93caae64 |
| 9 | token-probe | 59b2704e | 0 | 11 | 9 | 09-token-probe-59b2704e |

## 中文版文档（*-zh.md）

每组目录下的 `*-zh.md` 是对应英文文档的简体中文翻译（散文已翻译，代码块、JSON schema、
工具名、参数名保持英文原文）：

- `system-prompt-zh.md` — 系统提示词译文
- `tools-zh.md` — 工具定义译文
- `skills-zh.md` / `sample-message-zh.md` — skill 相关内容 / 消息样本译文

说明：
- 03、04 组的内容与 02 组仅差版本戳/模型 ID 字符串（`cc_version=2.1.209.74d`、`claude-fable-5[1m]`），
  其中文译文由 02 组译文复制并替换版本戳生成。
- 05–09 组为 Claude Code 的 token 计数探针（`max_tokens=1`），无系统提示词，
  其 tools-zh.md 是探针携带的工具集定义译文。
