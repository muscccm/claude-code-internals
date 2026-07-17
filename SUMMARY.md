# Claude Code Internals — Detailed Analysis

> A detailed look at Claude Code's prompts and tools, based on 234 requests from
> `cc_version=2.1.209` (2026-07-17). For the original content see the per-group
> folders (`*.zh-CN.md` files are the Chinese translations). This document explains
> **what every prompt section and every tool actually does**.
>
> [中文版本](SUMMARY.zh-CN.md)

---

## 1. The main Claude Code system prompt (groups 02/03/04, ~11.4K chars)

This prompt is attached verbatim to every real conversation request. It answers three
questions: who the model is, what tools it has, and what rules it works by.
Section by section:

### 1.1 Identity & safety red lines

- `You are Claude Code, Anthropic's official CLI for Claude, running within the Claude Agent SDK.`
  — declares this is not a chatbot but a **coding agent that operates the machine**.
- The safety clause explicitly permits authorized security testing / CTF / education;
  **refuses** destructive techniques, DoS attacks, mass targeting, supply-chain compromise,
  and malicious detection evasion. Dual-use tools (C2 frameworks, credential testing,
  exploit development) require a clear authorization context.

### 1.2 Harness (how output is rendered)

Tells the model how its words reach the user:

- Plain text is rendered as GitHub-flavored markdown — so headings, tables, and code fences are usable;
- Tool-call details are not shown to the user by default, so **important conclusions must be
  written into the final text message**, not left inside tool calls;
- Code references use the `file_path:line_number` format because it is clickable in the terminal;
- Prefer dedicated tools over shell equivalents (e.g. Grep over `bash grep`) because the
  permission UI renders them better;
- Independent tool calls should be issued in parallel within one reply.

### 1.3 Communicating with the user (tone rules)

- **Lead with the outcome**: the first sentence answers "what happened / what did you find";
- Complete sentences, no abbreviation chains or `A → B → fail` arrows;
- Calibrate to the user's expertise;
- Use they/them for anyone whose pronouns are unknown;
- **Confirm before hard-to-reverse or outward-facing actions** (sending data to external
  services may be cached/indexed; look before deleting);
- Report faithfully: if tests fail, say so with output; if a step was skipped, say that.

### 1.4 Memory (persistent file-based memory)

- A fixed memory directory, one markdown file per fact, with frontmatter (name/description/type);
- Four types: **user** (who the user is), **feedback** (corrections, with the *why*),
  **project** (ongoing work; relative dates must become absolute), **reference** (external links);
- `MEMORY.md` is the index loaded every session — one line per memory, never full content;
- Explicitly **not** to be saved: code structure, git history, anything CLAUDE.md already records;
- Memories cross-link with `[[name]]`.

### 1.5 Environment (per-request injection)

- Working directory, git-repo flag, platform, shell, OS version;
- Current model ID (`claude-fable-5[1m]`), knowledge cutoff, latest-model list
  (so the model knows which model it is);
- Current date, used for time-sensitive searches.

### 1.6 Context management

When the conversation grows long it is automatically summarized and continued —
the model is told **not to wrap up early** and not to re-derive settled decisions.

### 1.7 Autonomous-operation rules (a key chapter)

- The user is **not watching in real time**; asking "Shall I…?" only blocks the work —
  reversible actions that follow from the request should just be done;
- Stop only for destructive actions or genuine scope changes;
- **Exception**: when the user is describing a problem or thinking out loud, the deliverable
  is your assessment — report findings and stop; don't fix until asked;
- Before ending the turn, check the last paragraph: if it's a plan or a promise
  ("I'll…"), do that work now.

### 1.8 Session-specific guidance

`/skill-name` invocations go through the Skill tool, restricted to the listed available skills.

### 1.9 Build variants (groups 03/04)

Byte-identical to 02 except: 03 carries build stamp `cc_version=2.1.209.74d` (02 has `89f`);
04 writes the model ID as `claude-fable-5` (02 writes `claude-fable-5[1m]`).
**Different client builds send identical prompt content** — only metadata differs.

---

## 2. All 58 tools, one by one (group 02, tools.md)

Tool definitions (name + description + JSON Schema) are sent verbatim with every request,
totalling ~124K characters. 58 tools = 11 core + 19 extended + 28 MCP + 1 Skill —
matching the token-probe groups exactly.

### 2.1 Core built-ins (11, probe group 09)

| Tool | What it does |
|------|--------------|
| **Agent** | Spawns a subagent for complex multi-step tasks. Subagents have their own context window, run in the background, and report back conclusions. Supports git-worktree isolation (parallel file edits without conflicts) and remote runs |
| **AskUserQuestion** | Pops a structured multiple-choice dialog when genuinely blocked on a user decision (2–4 options, multi-select, ASCII previews). Conventional defaults must NOT be asked about |
| **Bash** | Runs shell commands (Git Bash here). Timeouts up to 10 min, background execution with exit notification |
| **Edit** | Exact-string-replacement file editing. Requires a prior Read; `old_string` must match uniquely |
| **Glob** | Finds files by name pattern (e.g. `**/*.ts`), sorted by mtime |
| **Grep** | ripgrep-based content search: regex, context lines, type filters, multiline |
| **Read** | Reads files: 2000 lines of text by default; images visually; PDFs by page range; notebooks by cell |
| **ReportFindings** | Code-review findings reporter: severity-ranked, structured, rendered by the host UI |
| **Skill** | Invokes a skill (slash command). A **blocking requirement**: a matching skill must be invoked before answering |
| **Workflow** | Multi-agent orchestration engine: a JS script deterministically fans out dozens of subagents (pipelines, adversarial verification, judge panels), with token budgets and resume. Gated behind explicit user opt-in |
| **Write** | Creates or fully overwrites a file (partial changes go through Edit) |

### 2.2 Extended built-ins (19, probe group 06)

| Tool | What it does |
|------|--------------|
| **CronCreate / CronDelete / CronList** | Scheduled prompts: fires a prompt to Claude on a cron expression ("every weekday at 9am, check the inbox"). Durable jobs survive restarts; recurring jobs auto-expire after 7 days |
| **DesignSync** | Syncs claude.ai design-system projects: read remote files, lock a write plan (`finalize_plan`), upload/delete files, register component preview cards |
| **EnterPlanMode / ExitPlanMode** | Plan mode: explore the codebase and design an implementation plan first; code only after user approval |
| **EnterWorktree / ExitWorktree** | git worktree isolation: work on a separate branch/directory, keep or discard on exit |
| **NotebookEdit** | Replaces/inserts/deletes a single Jupyter cell |
| **ScheduleWakeup** | Self-scheduling for `/loop` dynamic mode: pick a delay and wake up for the next iteration. The delay choice considers the 5-minute prompt-cache window |
| **SendMessage** | Messages another named subagent to continue collaboration |
| **TaskCreate / TaskGet / TaskList / TaskUpdate / TaskStop** | The task-list system: break work into tasks with status (pending/in_progress/completed) and dependencies (blocks/blockedBy); TaskStop kills runaway background tasks |
| **WebFetch** | Fetches a URL as markdown, then answers a given prompt with a small fast model. No authenticated pages |
| **WebSearch** | Web search (US-only), domain filters supported |

### 2.3 MCP tools (28, probe group 08)

MCP (Model Context Protocol) tools are provided by external services, in three bundles:

**ccd session helpers (3)** — provided by the Claude desktop app:

| Tool | What it does |
|------|--------------|
| `mcp__ccd_directory__request_directory` | Requests access to a directory outside the workspace (native folder picker) |
| `mcp__ccd_session__mark_chapter` | Marks a chapter boundary in the session timeline ("Exploration" → "Fix" → "Verification") for navigation |
| `mcp__ccd_session__spawn_task` / `dismiss_task` | Files an out-of-scope issue as a UI chip the user can spin off into its own session; `dismiss_task` withdraws stale chips |

**ccd session management (7)** — manages the user's other sessions:

| Tool | What it does |
|------|--------------|
| `list_sessions` / `get_session` | Lists / inspects other sessions' metadata (title, branch, PR, model, age) |
| `list_events` / `search_session_transcripts` | Reads another session's transcript / full-text-searches all session histories ("which session discussed X?") |
| `send_message` | Sends a message into another session (handoff; user-confirmed) |
| `set_session_title` | Renames a session |
| `archive_session` | Archives a session (stops its process, cleans the worktree, restorable) |

**Browser preview (14, `mcp__Claude_Browser__preview_*`)** — front-end dev & debugging:

| Tool | What it does |
|------|--------------|
| `preview_start` / `preview_stop` / `preview_list` | Starts / stops / lists dev servers from `.claude/launch.json` |
| `preview_screenshot` / `preview_snapshot` | Screenshot for layout / accessibility tree for exact text & structure (preferred for verification) |
| `preview_inspect` | Reads an element's computed styles (exact colors, fonts, spacing) |
| `preview_click` / `preview_fill` | Clicks elements / fills forms |
| `preview_eval` | Evaluates JS in the page (debugging/inspection only — never to implement changes) |
| `preview_console_logs` / `preview_logs` / `preview_network` | Browser console / server stdout / network requests |
| `preview_resize` | Resizes the viewport for responsive testing, with dark-mode emulation |

**Scheduled tasks (4, `mcp__scheduled-tasks__*`)** — tasks that run while the app is open:

| Tool | What it does |
|------|--------------|
| `create_scheduled_task` | Creates a scheduled task: recurring cron or one-shot `fireAt`. The prompt must be fully self-contained (each run is a fresh session with no memory of this conversation) |
| `update_scheduled_task` | Edits a task's prompt / schedule / enabled state |
| `list_scheduled_tasks` / `delete_scheduled_task` | Lists tasks (with next-run times) / deletes them |

### 2.4 The Skill tool (its own probe group, 05)

The entry point for "skills" — predefined capability packs (instructions + resources).
Its description embeds the current available-skills list, so **its size changes as skills
come and go**. That is why Claude Code weighs it separately — probe group 05 contains
this single tool.

---

## 3. The Claude Agent SDK general-agent prompt (group 01, 27K chars)

Seen exactly once, with no tools attached. It opens with
"You are a Claude agent, built on Anthropic's Claude Agent SDK" (note: not "Claude Code").
Its Environment section shows a working directory of
`…\AppData\Local\Claude-3p\title-gen\title-gen-<id>\` — **this is a standalone Agent SDK
process the desktop app spawns to auto-generate conversation titles**, run once per new
chat, which is why it appears once and needs no tools. Chapters:

| Section | What it does |
|---------|--------------|
| System | The agent's positioning and behavioral boundaries |
| Doing tasks | Task methodology: decomposition, verification, what "done" means |
| Executing actions with care | The caution list: which actions are hard to reverse (deleting data, external requests, shared state) and how to confirm them |
| Using your tools | Tool discipline: dedicated tools first, parallel calls, failure handling |
| Tone and style / Text output | Tone and formatting rules (similar to group 02, more detailed) |
| auto memory | The **full memory specification**, far more detailed than group 02's: worked examples per memory type; an explicit "do not save" list; a verify-before-citing rule (if a memory names a file, check it exists; if it names a function, grep for it); the boundary between memory and other persistence (CLAUDE.md, comments, docs) |
| Environment | This group's shell is `cmd.exe` (group 02 uses bash) — a **different session/shell configuration** |
| Context management | Context compaction explained |

**Relationship to group 02**: same skeleton (one agent philosophy); 01 targets
"general single-shot agent tasks", 02 targets "Claude Code coding sessions".
The discovery here: the desktop app's **conversation titles are model-generated too**,
by a process that first loads a full system prompt plus the memory system.

---

## 4. Token-counting probes (groups 05–09, ~60% of all requests)

### How they work

```
Request:  max_tokens=1 + the content to measure
Response: usage.input_tokens = the content's exact token count
```

Letting the model emit just 1 token (near-zero cost) reveals **the exact input token
count** from the usage field — the API itself acts as a scale.

### Why measure in groups

Claude Code's `/context` command shows a context breakdown (system prompt X tokens,
tools Y tokens, history Z tokens, free space left). To produce that breakdown it must
**weigh each part separately**:

| Probe group | What it weighs |
|-------------|----------------|
| 09 (11 tools) | Token cost of the core tool set |
| 06 (19 tools) | Token cost of the extended tool set |
| 08 (28 tools) | Token cost of the MCP tool set |
| 05 (1 tool) | The Skill tool (dynamic description — re-weighed often) |
| 07 (123 reqs) | Loose text fragments: session-guidance reminders and other dynamically injected blocks |

### Group 07 addendum

Most of its 123 requests are the fragment probes above (`max_tokens=1`); a few
`max_tokens=16` ones are manual test requests (user-agent `curl/8.21.0`).

---

## 5. How skills are injected (skills.md)

Skill content is **not in the tool definitions** — it rides the message stream as
system-reminders:

- When a session starts or the skill list changes, an "available skills" reminder block
  (name + description + when-to-use) is inserted into the messages;
- Typing `/skill-name` → Skill tool call → the skill's full instructions return as the tool result;
- skills.md preserves the captured reminder blocks (one per group 02/03/04, varying
  slightly as the session progresses).

---

## 6. Anatomy of one real conversation request

One request from this session (~300KB), field by field:

| Field | Content | Size |
|-------|---------|------|
| `system` | The main system prompt analyzed in section 1 | 11.4K chars |
| `tools` | The 58 tool definitions analyzed in section 2 | 124K chars |
| `messages` | Full conversation history (user turns, assistant turns, every tool call and result) | The bulk — grows with the conversation |
| `model` / `max_tokens` / `stream` | The client-configured model name / 64000 / true | — |
| `thinking` + `output_config` | `{"type":"adaptive"}` (adaptive thinking) + `{"effort":"max"}` (reasoning-effort level) | — |
| `metadata.user_id` | A JSON string with device ID + session ID | — |

That is why every request is hundreds of KB: **prompt + tool definitions are fixed
overhead; conversation history is growing overhead** — and the reason the token probes
keep measuring context size.
