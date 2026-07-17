# 工具定义（token-probe / 93caae64）—— 共 28 个

## `mcp__ccd_directory__request_directory`
请求访问用户计算机上位于你当前工作目录之外的某个目录。如果你知道路径，直接传入——用户会看到并批准它。如果省略 `path`，会打开一个原生文件夹选择器。每当用户要求你处理你当前无权访问的文件时，就使用此工具。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "path": {
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session__dismiss_task`
撤回你之前用 spawn_task 创建的后台任务卡片。

当你之前标记的建议已经过时、被取代或不再相关时调用此工具——例如你（或用户）已经在本会话中修复了它，或者你 spawn 了一个范围更合适的替代任务。要替换一张卡片：先用新建议调用 spawn_task，然后再 dismiss 旧的 task_id。

只有用户尚未采取行动的卡片才能被撤回。如果用户已经启动或关闭了该任务，结果会说明这一点且不会有任何变化——不要重试。任务 id 不会在应用重启后保留。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "reason": {
      "type": "string"
    },
    "task_id": {
      "description": "The task_id returned by the spawn_task call that created the chip.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session__mark_chapter`
标记本会话中一个新章节的开始。

当工作转入一个明显不同的阶段时调用此工具——例如探索结束、开始实现之后，修复落地、转入验证之后，或者用户转向一个无关请求时。用户会在 transcript 中看到一个分隔线，以及一个用于在章节间跳转的浮动目录。

谨慎使用：一个章节应覆盖一段连贯的工作，而不是每次工具调用都标记。一个典型会话有 3–8 个章节。不要为第一条消息标记章节——会话的开始是隐含的。

标题是简短的名词短语（"Codebase exploration"、"Auth bug fix"、"Test verification"），而不是句子。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "summary": {
      "type": "string"
    },
    "title": {
      "description": "Short noun-phrase title for the chapter (under 40 chars). Shown in the table of contents.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session__spawn_task`
将一个超出当前范围的问题标记为单独的后台任务。

当你注意到某些值得修复、但会膨胀当前改动的东西时调用此工具——死代码、过时的文档、缺失的测试覆盖、已确认的 TODO，或顺手发现的安全问题。不要标记模糊的代码异味观察、可以顺手内联完成的琐碎修复，或低置信度的猜测。用户会看到一张卡片；一键即可将其拆分为独立的会话。你当前的回合不受中断地继续。

prompt 必须能独立成立——包含文件路径和足够的上下文，使脱离本次对话也能执行。

结果中包含一个 task_id；如果该建议后来过时了，用它调用 dismiss_task。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "cwd": {
      "type": "string"
    },
    "prompt": {
      "description": "The initial message for the spawned session. Self-contained — include file paths and enough context to act without this conversation. Not shown directly in the UI.",
      "type": "string"
    },
    "title": {
      "description": "Under 60 chars. Imperative action phrase (start with a verb), e.g. \"Fix stale README badge\", \"Remove dead config option\". Shown as the chip label and the spawned session title.",
      "type": "string"
    },
    "tldr": {
      "description": "1-2 sentence plain-English summary of what the spawned session will do and why. Shown to the user in a tooltip — keep it readable, no file paths or code.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__archive_session`
归档一个 CCD 会话。归档会停止该会话的进程并（默认）清理其 worktree；之后仍可从 Archived 列表重新打开该会话。传入字面字符串 "self" 作为 session_id 可归档本会话——对话在此工具结果之后结束。

此工具总是向用户请求确认。只有在用户明确同意归档某个特定会话之后才调用——绝不要臆测调用。

如果用户经常希望在 PR 合并后归档会话，建议他们在 Settings 中启用 "Auto-archive on PR close" 偏好，而不是反复调用此工具。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "reason": {
      "type": "string"
    },
    "session_id": {
      "description": "The sessionId of the session to archive (from list_sessions / search_session_transcripts), or the literal string \"self\" to archive this session (ends the conversation).",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__get_session`
按 ID 获取单个 CCD 会话的详细元数据。

返回与 list_sessions 条目相同的字段，外加创建时间、模型、worktree/branch 信息、会话是否为远程、计划任务关联以及 agent。仅元数据——不含对话内容（对话内容请用 list_events）。当你已有 session_id、想获取其完整配置而不想重新列出所有会话时使用此工具。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "session_id": {
      "description": "The sessionId to look up (from list_sessions / search_session_transcripts). Must not be the current session.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__list_events`
读取另一个 CCD 会话的近期 transcript。

返回目标会话的用户/助手回合和工具调用的紧凑纯文本呈现，最新的排在最后。用于了解另一个会话一直在做什么或得出了什么结论。在限制工作区文件夹的托管部署中，这会向用户请求批准。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "before_uuid": {
      "type": "string"
    },
    "limit": {
      "type": "number"
    },
    "session_id": {
      "description": "The sessionId whose transcript to read (from list_sessions / search_session_transcripts). Must not be the current session.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__list_sessions`
列出用户的其他 CCD 会话（活动的，以及可选的已归档会话）。

返回按最近活动排序的紧凑 JSON 数组。当前会话被排除在外。用于回答"我还有哪些其他会话"、按标题/分支/PR 查找某个会话，或者——在你打开的 PR 合并之后——找到对应的会话并通过 archive_session 提议归档它。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "include_archived": {
      "type": "boolean"
    },
    "limit": {
      "type": "number"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__search_session_transcripts`
在其他 CCD 会话 transcript 的用户/助手消息中进行全文搜索。

每个匹配的会话返回一条命中结果，并附带匹配处周围的片段。用于查找哪个会话之前讨论过某个主题、错误消息、文件或决策。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "include_archived": {
      "type": "boolean"
    },
    "limit": {
      "type": "number"
    },
    "query": {
      "description": "Search string (min 2 chars). Substring match, case-insensitive.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__send_message`
向另一个 CCD 会话发送消息。消息以标注为 "From {this session's title}" 的用户回合形式到达目标会话，并附带指回此处的链接，以便用户能看到消息来源。

此工具总是向用户请求确认。用它来交接上下文、请另一个会话接手某件事，或转达某个发现——而不是用来编排后台工作。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "message": {
      "description": "The message body to deliver to the target session.",
      "type": "string"
    },
    "session_id": {
      "description": "The sessionId of the target session (from list_sessions / search_session_transcripts). Must not be the current session.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__ccd_session_mgmt__set_session_title`
重命名另一个 CCD 会话。

当用户要求重命名某个会话时使用，或在某个会话的范围已明显变化、旧标题具有误导性之后使用。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "session_id": {
      "description": "The sessionId of the session to rename (from list_sessions / search_session_transcripts). Must not be the current session.",
      "type": "string"
    },
    "title": {
      "description": "New title for the session.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_click`
通过 CSS 选择器点击一个元素（例如 'button.primary'、'#submit'、'[data-testid="btn"]'）。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "doubleClick": {
      "type": "boolean"
    },
    "selector": {
      "description": "CSS selector for the element to click",
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_console_logs`
获取浏览器控制台输出（log、info、warn、error、debug）。用于检查运行时行为、调试值或客户端错误。使用 'level' 可只过滤出错误或警告。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "level": {
      "enum": [
        "all",
        "error",
        "warn"
      ],
      "type": "string"
    },
    "lines": {
      "type": "number"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_eval`
在 Browser 窗格的页面中执行 JavaScript，仅用于调试和检查。用于读取页面状态、DOM 查询、检查变量、导航、页面重载、hover/type/key 事件。不要用它来实现用户请求的 UI 改动——应改为编辑源代码。通过 eval 做的任何 DOM 修改都是临时的，重载后即丢失。多步逻辑请包裹在 IIFE 中。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "expression": {
      "description": "JavaScript expression to evaluate in the page context. Return values are serialized as JSON.",
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_fill`
向 input、textarea 或 select 元素填入一个值。对于 select 元素，按 value 或文本匹配。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "selector": {
      "description": "CSS selector for the input element",
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    },
    "value": {
      "description": "Value to fill",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_inspect`
通过 CSS 选择器检查一个 DOM 元素。返回文本内容、className、tagName、id、计算样式和边界框。这是验证颜色、字体、间距和尺寸等视觉属性的最佳工具——比截图更准确。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "selector": {
      "description": "CSS selector (e.g., '.button', '#header')",
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    },
    "styles": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_list`
列出通过 preview_start 启动的服务器。返回 serverId，供其他 preview_* 工具使用。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {},
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_logs`
获取服务器 stdout/stderr 输出。用于检查构建错误、验证服务器行为或阅读调试输出。使用 'level' 只过滤错误，或使用 'search' 过滤特定文本。在 preview_start 之后使用。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "level": {
      "enum": [
        "all",
        "error"
      ],
      "type": "string"
    },
    "lines": {
      "type": "number"
    },
    "search": {
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_network`
列出网络请求或检查某个特定响应体。不带 requestId 时，列出所有请求的 URL、方法、状态和 requestId。带 requestId 时，返回该请求的完整响应体（适用于检查 API 负载）。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "filter": {
      "enum": [
        "all",
        "failed"
      ],
      "type": "string"
    },
    "requestId": {
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_resize`
调整 Browser 窗格视口大小以测试响应式布局。预设：mobile (375x812)、tablet (768x1024)、desktop (1280x800)。也支持自定义尺寸和用于深色模式测试的配色方案模拟。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "colorScheme": {
      "enum": [
        "light",
        "dark"
      ],
      "type": "string"
    },
    "height": {
      "type": "number"
    },
    "preset": {
      "enum": [
        "mobile",
        "tablet",
        "desktop"
      ],
      "type": "string"
    },
    "serverId": {
      "description": "Server ID",
      "type": "string"
    },
    "width": {
      "type": "number"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_screenshot`
对页面截图。适合检查布局和整体外观，但不要依赖它验证颜色、字号或精确样式——改用 preview_inspect 并指定具体的 CSS 属性。返回压缩后的 JPEG 图像。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_snapshot`
获取页面的无障碍树快照。返回精确的文本内容、角色和元素 UID，供 click/fill/hover 使用。在验证文本、元素存在性和页面结构时优先于截图使用。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "serverId": {
      "description": "Server ID",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_start`
按名称从 .claude/launch.json 启动一个开发服务器。如果 .claude/launch.json 不存在，先按以下格式创建它：
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "<unique-name>",
      "runtimeExecutable": "<command>",
      "runtimeArgs": ["<args>"],
      "port": <port>
    }
  ]
}
将 "runtimeExecutable" 设为命令（例如 "npm"），"runtimeArgs" 设为参数（例如 ["run", "dev"]），"port" 设为服务器端口。只包含你确实需要预览的服务器。如果服务器已在运行则复用它。运行服务器时总是使用此工具而不是 Bash。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "name": {
      "description": "Server name from .claude/launch.json.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_stop`
停止一个通过 preview_start 启动的服务器。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "serverId": {
      "description": "Server ID to stop",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `mcp__scheduled-tasks__create_scheduled_task`
创建一个自动运行的计划任务——按周期计划运行，或在未来某个时刻运行一次。当用户要求某件事重复发生（"每天早上 6 点"、"每周一"、"每小时"）或在某个特定的稍后时间发生（"20 分钟后提醒我"、"明天下午 3 点"），而不是立即执行一次时，使用此工具。当请求明确描述了计划时，直接调用即可；如果计划或任务内容含糊，先与用户确认细节——根据用户的权限设置，批准提示可能出现也可能不出现，所以不要依赖它作为确认步骤。

要修改现有计划任务的计划或 prompt，改用 `update_scheduled_task`。

任务以 {taskId}/SKILL.md 的形式存储在 C:\Users\<user>\.claude\scheduled-tasks/ 中。每次运行都是全新开始，没有本次对话的记忆，因此 prompt 必须完全自包含：包括使用哪些连接器、输出格式，以及用户在此表达的任何偏好。

计划任务在此应用打开期间运行。如果任务到期时应用已关闭，它会在下次启动时运行——告诉用户这一点，以免他们感到意外。

**计划选项（最多选一种）：**
- cronExpression：周期性（每天、每周等）
- fireAt：一次性——在给定时刻运行一次，然后自动禁用。绝不要对一次性任务使用 cron 表达式；cron 没有一次性语义。
- 两者都省略："ad-hoc"——只能手动启动

**周期性（cronExpression）：** Cron 按用户的本地时区求值，而不是 UTC。直接使用本地时间。格式：minute hour dayOfMonth month dayOfWeek
- "0 9 * * *" — 每天本地时间上午 9:00
- "0 9 * * 1-5" — 工作日本地时间上午 9:00
- "30 8 * * 1" — 每周一本地时间上午 8:30
- "0 0 1 * *" — 每月第一天本地时间午夜

**一次性（fireAt）：** 带时区偏移的 ISO 8601 时间戳。任务在该时刻触发一次（如果应用当时已关闭，则在下次启动时触发），然后自行禁用。
- "2026-03-05T14:30:00-08:00" — 在 3 月 5 日下午 2:30 运行一次……[截断]

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "cronExpression": {
      "description": "Standard 5-field cron expression for recurring runs, in LOCAL time (not UTC). For example, '0 9 * * *' means 9am daily in the user's local timezone. Mutually exclusive with fireAt.",
      "type": "string"
    },
    "description": {
      "description": "A short one-line description of what this task does (used in skill frontmatter).",
      "type": "string"
    },
    "fireAt": {
      "description": "ISO 8601 timestamp with timezone offset for a one-time run (e.g. '2026-03-05T14:30:00-08:00'). Mutually exclusive with cronExpression. Must be in the future. Task auto-disables after firing.",
      "type": "string"
    },
    "notifyOnCompletion": {
      "description": "When true (default), this session receives a notification each time the task finishes a run. Pass false to opt out.",
      "type": "boolean"
    },
    "prompt": {
      "description": "The full task prompt/instructions that will be executed each time the task runs. Write this as a complete prompt describing what Claude should do.",
      "type": "string"
    },
    "taskId": {
      "description": "Kebab-case identifier for the task (e.g., 'check-inbox', 'daily-standup'). Used as the directory name and storage key. Auto-sanitized as a safety net.",
      "type": "string"
    }
  },
  "required": [
    "taskId",
    "prompt",
    "description"
  ],
  "type": "object"
}
```

## `mcp__scheduled-tasks__delete_scheduled_task`
删除一个现有的计划任务。taskId 必须是来自 list_scheduled_tasks 的精确 ID。

这会从调度器中移除该任务，使其不再运行。任务的 SKILL.md 文件保留在磁盘上，因此 prompt 可以恢复。要暂停任务而不删除它，改用 update_scheduled_task 并设置 enabled: false。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "taskId": {
      "description": "The exact ID of the task to delete (from list_scheduled_tasks).",
      "type": "string"
    }
  },
  "required": [
    "taskId"
  ],
  "type": "object"
}
```

## `mcp__scheduled-tasks__list_scheduled_tasks`
列出所有计划任务及其当前状态。在更新任务之前，用此工具发现现有任务及其 ID。

返回每个任务的 taskId、description、计划（人类可读）、cronExpression、fireAt（一次性任务的 ISO 时间戳）、enabled 状态、nextRunAt（ISO 时间戳）和 lastRunAt（ISO 时间戳）。每个条目还包含指向该任务 SKILL.md 的 `path`——Read 它以查看当前 prompt。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {},
  "type": "object"
}
```

## `mcp__scheduled-tasks__update_scheduled_task`
更新一个现有的计划任务。taskId 必须是来自 list_scheduled_tasks 的精确 ID。要在编辑前查看当前 prompt，Read list_scheduled_tasks 返回的 `path`。

支持部分更新——只提供你想更改的字段：
- prompt：替换 Claude 每次运行时执行的指令
- description：替换侧边栏中显示的一行摘要
- cronExpression：更改或设置周期计划（5 字段 cron 字符串，本地时间，非 UTC）。清除任何一次性 fireAt。
- fireAt：更改或设置一次性运行（带偏移的 ISO 8601 时间戳，必须在未来）。清除任何 cron 计划并重新武装任务。
- enabled：传 false 暂停自动运行，传 true 恢复
- notifyOnCompletion：传 true 让本会话在任务每次完成运行时收到通知；传 false 停止通知

**关于时序的说明：** 周期性任务在派发时会施加几分钟的确定性小延迟，以平衡服务器负载。一次性任务无延迟触发。

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "cronExpression": {
      "description": "New 5-field cron expression for recurring runs in LOCAL time (not UTC). For example, '0 9 * * *' means 9am in the user's local timezone. Mutually exclusive with fireAt.",
      "type": "string"
    },
    "description": {
      "description": "New one-line description for the task.",
      "type": "string"
    },
    "enabled": {
      "description": "Set to false to pause automatic runs, true to resume. Does not affect manual runs.",
      "type": "boolean"
    },
    "fireAt": {
      "description": "New ISO 8601 timestamp with timezone offset for a one-time run. Mutually exclusive with cronExpression. Must be in the future. Re-arms and auto-enables the task.",
      "type": "string"
    },
    "notifyOnCompletion": {
      "description": "Pass true to have this session notified each time the task finishes a run (replaces any prior subscriber). Pass false to clear the subscription.",
      "type": "boolean"
    },
    "prompt": {
      "description": "New prompt/instructions to replace the current ones.",
      "type": "string"
    },
    "taskId": {
      "description": "The exact ID of the task to update (from list_scheduled_tasks).",
      "type": "string"
    }
  },
  "required": [
    "taskId"
  ],
  "type": "object"
}
```
