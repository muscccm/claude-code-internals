# 工具定义（probe-skill-tool）—— 共 1 个

## `Skill`
在主对话中执行一个 skill

当用户要求你执行任务时，检查是否有可用的 skill 与之匹配。Skill 提供专门的能力和领域知识。

当用户提到 "slash command" 或 "/<something>" 时，他们指的就是 skill。使用此工具来调用它。

如何调用：
- 将 `skill` 设为可用 skill 的精确名称（不带前导斜杠）。对于插件命名空间下的 skill，使用完全限定的 `plugin:skill` 形式。
- 设置 `args` 以传递可选参数。
- 有些 skill 限定于某个目录：其名称带有目录前缀（例如 `apps/web:deploy`），且其描述说明了它适用于哪个目录。当一个 skill 名称同时存在限定版和非限定版时，根据你正在处理的文件来选择：如果文件位于某个限定版的目录之下，调用该限定版（最具体的目录优先）；否则调用非限定版。

重要：
- 可用 skill 列在对话中的 system-reminder 消息里
- 只调用出现在该列表中的 skill，或用户在消息中明确输入为 `/<name>` 的 skill。绝不要凭训练数据猜测或编造 skill 名称；否则不要调用此工具
- 当某个 skill 与用户的请求匹配时，这是一个阻塞性要求：在生成关于该任务的任何其他响应之前，先调用相关的 Skill 工具
- 绝不要在不实际调用此工具的情况下提及某个 skill
- 不要调用已经在运行的 skill
- 不要将此工具用于内置 CLI 命令（如 /help、/clear 等）
- 如果你在当前对话回合中看到 <command-name> 标签，说明该 skill 已经被加载——直接按照其指令执行，而不是再次调用此工具

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "args": {
      "description": "Optional arguments for the skill",
      "type": "string"
    },
    "skill": {
      "description": "The name of a skill from the available-skills list. Do not guess names.",
      "type": "string"
    }
  },
  "required": [
    "skill"
  ],
  "type": "object"
}
```
