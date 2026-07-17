# 工具定义（token-probe / 93caae64）—— 共 28 个

## `mcp__ccd_directory__request_directory`
Request access to a directory on the user's computer that is outside your current working directory. If you know the path, pass it — the user sees and approves it. If you omit `path`, a native folder picker opens. Use this whenever the user asks you to work with files you don't currently have access to.

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
Withdraw a background-task chip you previously created with spawn_task.

Call this when a suggestion you flagged is now stale, superseded, or irrelevant — e.g. you (or the user) already fixed it in this session, or you spawned a better-scoped replacement. To replace a chip: call spawn_task with the new suggestion first, then dismiss the old task_id.

Only chips the user hasn't acted on can be withdrawn. If the user already started or dismissed the task, the result says so and nothing changes — do not retry. Task ids are not persisted across app restarts.

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
Mark the start of a new chapter in this session.

Call this when the work shifts to a meaningfully different phase — e.g. after finishing exploration and starting implementation, after a fix lands and you move to verification, or when the user pivots to an unrelated request. The user sees a divider in the transcript and a floating table of contents for jumping between chapters.

Use sparingly: a chapter should cover a coherent stretch of work, not every tool call. A typical session has 3–8 chapters. Do not mark a chapter for the very first message — the session start is implicit.

The title is a short noun phrase ("Codebase exploration", "Auth bug fix", "Test verification"), not a sentence.

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
Flag an out-of-scope issue for a separate background task.

Call this when you notice something worth fixing that would bloat the current change — dead code, stale docs, missing coverage, a confirmed TODO, or a security issue spotted in passing. Don't flag vague code-smell observations, trivial fixes you can do inline, or low-confidence hunches. A chip appears for the user; one click spins it off into its own session. Your current turn continues uninterrupted.

The prompt must stand alone — include file paths and enough context to act without this conversation.

The result includes a task_id; call dismiss_task with it if the suggestion later becomes stale.

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
Archive a CCD session. Archiving stops the session's process and (by default) cleans up its worktree; the session can still be reopened later from the Archived list. Pass the literal string "self" as session_id to archive this session — the conversation ends after this tool result.

This tool ALWAYS prompts the user for confirmation. Only call it after the user has explicitly agreed to archive a specific session — never speculatively.

If the user often wants sessions archived once their PR merges, suggest enabling the "Auto-archive on PR close" preference in Settings instead of calling this repeatedly.

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
Get detailed metadata for a single CCD session by ID.

Returns the same fields as a list_sessions entry plus creation time, model, worktree/branch info, whether the session is remote, scheduled-task linkage, and agent. Metadata only — no conversation content (use list_events for that). Use this when you have a session_id and want its full configuration without re-listing everything.

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
Read the recent transcript of another CCD session.

Returns a compact plaintext rendering of the target session's user/assistant turns and tool calls, most recent last. Use this to understand what another session has been doing or what it concluded. In managed deployments that restrict workspace folders, this prompts the user for approval.

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
List the user's other CCD sessions (active and optionally archived).

Returns a compact JSON array sorted by most recent activity. The current session is excluded. Use this to answer "what other sessions do I have", to find a session by title/branch/PR, or — after a PR you opened has merged — to locate the corresponding session and offer to archive it via archive_session.

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
Full-text search across the user/assistant messages of other CCD session transcripts.

Returns one hit per matching session with a snippet around the match. Use this to find which session previously discussed a topic, error message, file, or decision.

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
Send a message to another CCD session. The message arrives in the target session as a user turn labelled "From {this session's title}" with a link back here, so the user can see where it came from.

This tool ALWAYS prompts the user for confirmation. Use it to hand off context, ask the other session to pick something up, or relay a finding — not to orchestrate background work.

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
Rename another CCD session.

Use it when the user asks to rename a session, or after a session's scope has clearly changed and the old title is misleading.

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
Click an element by CSS selector (e.g., 'button.primary', '#submit', '[data-testid="btn"]').

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
Get browser console output (log, info, warn, error, debug). Use to check runtime behavior, debug values, or client-side errors. Use 'level' to filter to errors or warnings only.

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
Execute JavaScript in the Browser pane's page for DEBUGGING and INSPECTION only. Use for reading page state, DOM queries, checking variables, navigation, page reload, hover/type/key events. Do NOT use this to implement UI changes the user requests — edit the source code instead. Any DOM modifications via eval are temporary and lost on reload. Wrap multi-step logic in an IIFE.

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
Fill an input, textarea, or select element with a value. For select elements, matches by value or text.

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
Inspect a DOM element by CSS selector. Returns text content, className, tagName, id, computed styles, and bounding box. BEST tool for verifying visual properties like colors, fonts, spacing, and dimensions — more accurate than screenshots.

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
List servers started with preview_start. Returns serverIds for use with other preview_* tools.

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {},
  "type": "object"
}
```

## `mcp__Claude_Browser__preview_logs`
Get server stdout/stderr output. Use to check for build errors, verify server behavior, or read debug output. Use 'level' to filter to errors only, or 'search' to filter for specific text. Use after preview_start.

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
List network requests or inspect a specific response body. Without requestId, lists all requests with URL, method, status, and requestId. With requestId, returns the full response body for that request (useful for inspecting API payloads).

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
Resize the Browser pane viewport to test responsive layouts. Presets: mobile (375x812), tablet (768x1024), desktop (1280x800). Also supports custom dimensions and color scheme emulation for dark mode testing.

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
Take a screenshot of the page. Good for checking layout and general appearance, but DO NOT rely on it for verifying colors, font sizes, or precise styles — use preview_inspect with specific CSS properties instead. Returns a compressed JPEG image.

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
Get an accessibility tree snapshot of the page. Returns exact text content, roles, and element UIDs for use with click/fill/hover. PREFERRED over screenshot for verifying text, element presence, and page structure.

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
Start a dev server by name from .claude/launch.json. If .claude/launch.json doesn't exist, create it first with this format:
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
Set "runtimeExecutable" to the command (e.g. "npm"), "runtimeArgs" to the arguments (e.g. ["run", "dev"]), and "port" to the server port. Only include servers you actually need to preview. Reuses the server if already running. ALWAYS use this instead of Bash for running servers.

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
Stop a server started with preview_start.

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
Create a scheduled task that runs automatically — on a recurring schedule or once at a future moment. Use this when the user asks for something to happen repeatedly ("every day at 6am", "each Monday", "hourly") or at a specific later time ("remind me in 20 minutes", "tomorrow at 3pm"), rather than once right now. Go ahead and call it when the request clearly describes a schedule; if the schedule or task content is ambiguous, confirm the details with the user first — an approval prompt may or may not appear depending on the user's permission settings, so don't rely on it as the confirmation step.

To modify an existing scheduled task's schedule or prompt, use `update_scheduled_task` instead.

The task is stored as {taskId}/SKILL.md in C:\Users\<user>\.claude\scheduled-tasks/. Each run starts fresh with no memory of this conversation, so the prompt must be fully self-contained: include which connectors to use, the output format, and any preferences the user expressed here.

Scheduled tasks run while this app is open. If the app is closed when a task is due, it runs on next launch — tell the user this so they aren't surprised.

**Scheduling options (pick at most one):**
- cronExpression: recurring (daily, weekly, etc.)
- fireAt: one-time — runs once at the given moment, then auto-disables. Never use a cron expression for a one-time task; cron has no one-shot semantics.
- Omit both: "ad-hoc" — can only be started manually

**Recurring (cronExpression):** Cron is evaluated in the user's LOCAL timezone, not UTC. Use local times directly. Format: minute hour dayOfMonth month dayOfWeek
- "0 9 * * *" — Every day at 9:00 AM local time
- "0 9 * * 1-5" — Weekdays at 9:00 AM local time
- "30 8 * * 1" — Every Monday at 8:30 AM local time
- "0 0 1 * *" — First day of every month at midnight local time

**One-time (fireAt):** An ISO 8601 timestamp with timezone offset. The task fires once at that moment (or on next app launch if it was closed), then disables itself.
- "2026-03-05T14:30:00-08:00" — Runs once on March 5 at 2:30 PM … [truncated]

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
Delete an existing scheduled task. taskId must be an exact ID from list_scheduled_tasks.

This removes the task from the scheduler so it will no longer run. The task's SKILL.md file is left on disk so the prompt can be recovered. To pause a task without deleting it, use update_scheduled_task with enabled: false instead.

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
List all scheduled tasks with their current state. Use this to discover existing tasks and their IDs before updating them.

Returns each task's taskId, description, schedule (human-readable), cronExpression, fireAt (ISO timestamp if one-time), enabled state, nextRunAt (ISO timestamp), and lastRunAt (ISO timestamp). Each entry also includes a `path` to the task's SKILL.md — Read it to see the current prompt.

**input_schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {},
  "type": "object"
}
```

## `mcp__scheduled-tasks__update_scheduled_task`
Update an existing scheduled task. taskId must be an exact ID from list_scheduled_tasks. To see the current prompt before editing it, Read the `path` returned by list_scheduled_tasks.

Supports partial updates — only supply the fields you want to change:
- prompt: Replace the instructions Claude executes on each run
- description: Replace the one-line summary shown in the sidebar
- cronExpression: Change or set a recurring schedule (5-field cron string in LOCAL time, not UTC). Clears any one-time fireAt.
- fireAt: Change or set a one-time run (ISO 8601 timestamp with offset, must be in the future). Clears any cron schedule and re-arms the task.
- enabled: Pass false to pause automatic runs, true to resume them
- notifyOnCompletion: Pass true to receive a notification each time the task finishes a run; pass false to stop

**Note on timing:** Recurring tasks apply a small deterministic delay of several minutes at dispatch time to balance server load. One-time tasks fire without delay.

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
