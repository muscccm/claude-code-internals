# 工具定义（probe-core-tools）—— 共 11 个

## `Agent`
启动一个新的 agent 来处理复杂的多步骤任务。每种 agent 类型都有其特定的能力和可用工具。

可用的 agent 类型会在对话中的 <system-reminder> 消息里列出。

使用 Agent 工具时，通过 subagent_type 参数指定要使用的 agent 类型。如果省略，则使用 general-purpose agent。

## 何时使用

当任务匹配某种可用的 agent 类型、当你有可以并行运行的独立工作、或者当回答问题需要跨多个文件阅读时，使用本工具——把它委派出去，你保留的是结论，而不是一堆文件转储。对于你已经知道文件、符号或值的单一事实查找，直接搜索即可。一旦你已经委派了某个搜索，就不要自己再跑一遍——等待结果即可。

- agent 的最终消息会作为工具结果返回给你；它不会展示给用户——重要的内容需要你来转达。
- 使用 SendMessage 并传入 agent 的 ID 或名称，可以在保留其上下文的情况下继续之前启动的 agent；而新的 Agent 调用则是全新开始。
- 每种 agent 类型的模型、推理强度和工具都来自其定义（`.claude/agents/*.md` 的 frontmatter 或 SDK 的 `agents`）。
- `isolation: "worktree"` 会为 agent 提供独立的 git worktree（如果没有改动会自动清理）。
- 子 agent 默认在后台运行；完成时你会收到通知。如果你需要先拿到结果再继续，传入 `run_in_background: false` 以同步方式运行。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "description": {
      "description": "A short (3-5 word) description of the task",
      "type": "string"
    },
    "isolation": {
      "description": "Isolation mode. \"worktree\" creates a temporary git worktree so the agent works on an isolated copy of the repo. \"remote\" launches the agent in a remote cloud environment (always runs in background; availability is gated).",
      "enum": [
        "worktree",
        "remote"
      ],
      "type": "string"
    },
    "model": {
      "description": "Optional model override for this agent. Takes precedence over the agent definition's model frontmatter. If omitted, uses the agent definition's model, or inherits from the parent. Ignored for subagent_type: \"fork\" — forks always inherit the parent model.",
      "enum": [
        "sonnet",
        "opus",
        "haiku",
        "fable"
      ],
      "type": "string"
    },
    "prompt": {
      "description": "The task for the agent to perform",
      "type": "string"
    },
    "run_in_background": {
      "description": "Agents run in the background by default; you will be notified when one completes. Set to false to run this agent synchronously when you need its result before continuing.",
      "type": "boolean"
    },
    "subagent_type": {
      "description": "The type of specialized agent to use for this task",
      "type": "string"
    }
  },
  "required": [
    "description",
    "prompt"
  ],
  "type": "object"
}
```

## `AskUserQuestion`
仅当你被一个真正应由用户来做主的决定卡住时才使用此工具：即无法从请求、代码或合理默认值中解决的决定。

使用说明：
- 用户始终可以选择 "Other" 来提供自定义文本输入
- 使用 multiSelect: true 允许一个问题选择多个答案
- 如果你推荐某个特定选项，把它放在选项列表的第一位，并在标签末尾加上 "(Recommended)"

计划模式说明：要进入计划模式，使用 EnterPlanMode（而不是本工具）。进入计划模式后，在最终确定计划之前，使用本工具来澄清需求或在多种方案之间做选择。不要用本工具问 "我的计划准备好了吗？"、"我可以继续吗？"，也不要在问题中提及 "计划"——在你调用 ExitPlanMode 请求批准之前，用户是看不到计划的。

本工具只用于那些用户的回答会改变你下一步行动的决定——而不是用于有惯例默认值的取舍、或你自己就能在代码库中验证的事实。对于那些情况，选择显而易见的选项，在回复中提一句，然后继续。

预览功能：
当需要展示用户需要直观比较的具体产物时，可以在选项上使用可选的 `preview` 字段：
- UI 布局或组件的 ASCII 草图
- 展示不同实现的代码片段
- 图表的不同变体
- 配置示例

预览内容会以 markdown 形式渲染在等宽字体框中，支持带换行的多行文本。当任一选项带有预览时，UI 会切换为左右并排布局：左侧是纵向选项列表，右侧是预览。对于仅靠标签和描述就足够说明的简单偏好类问题，不要使用预览。注意：预览仅支持单选问题（不支持 multiSelect）。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "annotations": {
      "additionalProperties": {
        "additionalProperties": false,
        "properties": {
          "notes": {
            "description": "Free-text notes the user added to their selection.",
            "type": "string"
          },
          "preview": {
            "description": "The preview content of the selected option, if the question used previews.",
            "type": "string"
          }
        },
        "type": "object"
      },
      "description": "Optional per-question annotations from the user (e.g., notes on preview selections). Keyed by question text.",
      "propertyNames": {
        "type": "string"
      },
      "type": "object"
    },
    "answers": {
      "additionalProperties": {
        "type": "string"
      },
      "description": "User answers collected by the permission component",
      "propertyNames": {
        "type": "string"
      },
      "type": "object"
    },
    "metadata": {
      "additionalProperties": false,
      "description": "Optional metadata for tracking and analytics purposes. Not displayed to user.",
      "properties": {
        "source": {
          "description": "Optional identifier for the source of this question (e.g., \"remember\" for /remember command). Used for analytics tracking.",
          "type": "string"
        }
      },
      "type": "object"
    },
    "questions": {
      "description": "Questions to ask the user (1-4 questions)",
      "items": {
        "additionalProperties": false,
        "properties": {
          "header": {
            "description": "Very short label displayed as a chip/tag (max 12 chars). Examples: \"Auth method\", \"Library\", \"Approach\".",
            "type": "string"
          },
          "multiSelect": {
            "default": false,
            "description": "Set to true to allow the user to select multiple options instead of just one. Use when choices are not mutually exclusive.",
            "type": "boolean"
          },
          "options": {
            "description": "The available choices for this question. Must have 2-4 options. Each option should be a distinct, mutually exclusive choice (unless multiSelect is enabled). There should be no 'Other' option, that will be provided automatically.",
            "items": {
              "additionalProperties": false,
              "properties": {
                "description": {
                  "description": "Explanation of what this option means or what will happen if chosen. Useful for providing context about trade-offs or implications.",
                  "type": "string"
                },
                "label": {
                  "description": "The display text for this option that the user will see and select. Should be concise (1-5 words) and clearly describe the choice.",
                  "type": "string"
                },
                "preview": {
                  "description": "Optional preview content rendered when this option is focused. Use for mockups, code snippets, or visual comparisons that help users compare options. See the tool description for the expected content format.",
                  "type": "string"
                }
              },
              "required": [
                "label",
                "description"
              ],
              "type": "object"
            },
            "maxItems": 4,
            "minItems": 2,
            "type": "array"
          },
          "question": {
            "description": "The complete question to ask the user. Should be clear, specific, and end with a question mark. Example: \"Which library should we use for date formatting?\" If multiSelect is true, phrase it accordingly, e.g. \"Which features do you want to enable?\"",
            "type": "string"
          }
        },
        "required": [
          "question",
          "header",
          "options",
          "multiSelect"
        ],
        "type": "object"
      },
      "maxItems": 4,
      "minItems": 1,
      "type": "array"
    }
  },
  "required": [
    "questions"
  ],
  "type": "object"
}
```

## `Bash`
执行一条 bash 命令并返回其输出。

本工具运行的是 Git Bash（POSIX sh），而不是 cmd.exe 或 PowerShell。请使用 Unix shell 语法：`/dev/null` 而不是 `NUL`，使用正斜杠，用 `$VAR` 而不是 `%VAR%` 或 `$env:VAR`。

- 工作目录在多次调用之间会保持，但优先使用绝对路径——在复合命令中使用 `cd` 可能触发权限提示。Shell 状态（环境变量、函数）不会保持；shell 会从用户的 profile 初始化。
- 重要：避免使用本工具运行 `find`、`grep`、`cat`、`head`、`tail`、`sed`、`awk` 或 `echo` 命令，除非被明确指示，或者你已经确认没有专用工具能完成该任务。请改用相应的专用工具，这会给用户带来好得多的体验。
- `timeout` 以毫秒为单位：默认 120000，最大 600000。
- `run_in_background` 会让命令以分离方式运行：它会跨回合持续运行，并在退出时重新唤起你。不需要加 `&`。

# Git
- 本环境不支持交互式参数（`-i`，例如 `git rebase -i`、`git add -i`）。
- GitHub 操作（PR、issue、API）请使用 `gh` CLI。
- 仅在用户要求时才提交或推送。如果当前在默认分支上，先创建分支。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "command": {
      "description": "The command to execute",
      "type": "string"
    },
    "dangerouslyDisableSandbox": {
      "description": "Set this to true to dangerously override sandbox mode and run commands without sandboxing.",
      "type": "boolean"
    },
    "description": {
      "description": "Clear, concise description of what this command does in active voice. Never use words like \"complex\" or \"risk\" in the description - just describe what it does.\n\nFor simple commands (git, npm, standard CLI tools), keep it brief (5-10 words):\n- ls → \"List files in current directory\"\n- git status → \"Show working tree status\"\n- npm install → \"Install package dependencies\"\n\nFor commands that are harder to parse at a glance (piped commands, obscure flags, etc.), add enough context to clarify what it does:\n- find . -name \"*.tmp\" -exec rm {} \\; → \"Find and delete all .tmp files recursively\"\n- git reset --hard origin/main → \"Discard all local changes and match remote main\"\n- curl -s url | jq '.data[]' → \"Fetch JSON from URL and extract data array elements\"",
      "type": "string"
    },
    "run_in_background": {
      "description": "Set to true to run this command in the background.",
      "type": "boolean"
    },
    "timeout": {
      "description": "Optional timeout in milliseconds (max 600000)",
      "type": "number"
    }
  },
  "required": [
    "command"
  ],
  "type": "object"
}
```

## `Edit`
在文件中执行精确的字符串替换。

- 编辑之前必须在本对话中先 Read 该文件，否则调用会失败。
- `old_string` 必须与文件内容完全一致（包括缩进），并且必须唯一——否则编辑会失败。匹配前要去掉 Read 输出的行前缀（行号 + 制表符）。
- `replace_all: true` 会替换所有出现的位置。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "file_path": {
      "description": "The absolute path to the file to modify",
      "type": "string"
    },
    "new_string": {
      "description": "The text to replace it with (must be different from old_string)",
      "type": "string"
    },
    "old_string": {
      "description": "The text to replace",
      "type": "string"
    },
    "replace_all": {
      "default": false,
      "description": "Replace all occurrences of old_string (default false)",
      "type": "boolean"
    }
  },
  "required": [
    "file_path",
    "old_string",
    "new_string"
  ],
  "type": "object"
}
```

## `Glob`
快速的文件模式匹配。支持 "**/*.js" 或 "src/**/*.ts" 之类的 glob 模式。返回按修改时间排序的匹配文件路径。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "path": {
      "description": "The directory to search in. If not specified, the current working directory will be used. IMPORTANT: Omit this field to use the default directory. DO NOT enter \"undefined\" or \"null\" - simply omit it for the default behavior. Must be a valid directory path if provided.",
      "type": "string"
    },
    "pattern": {
      "description": "The glob pattern to match files against",
      "type": "string"
    }
  },
  "required": [
    "pattern"
  ],
  "type": "object"
}
```

## `Grep`
基于 ripgrep 构建的内容搜索。优先使用本工具，而不是通过 Bash 调用 `grep`/`rg`——其结果会与权限 UI 和文件链接集成。

- 完整的正则语法（例如 "log.*Error"、"function\s+\w+"）。这是 ripgrep 而不是 grep——字面花括号需要转义（`interface\{\}`）。
- 用 `glob`（例如 "**/*.tsx"）或 `type`（例如 "js"、"py"、"rust"）进行过滤。
- `output_mode`："content"（匹配行）、"files_with_matches"（仅路径，默认）或 "count"。
- `multiline: true` 用于跨行匹配的模式。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "-A": {
      "description": "Number of lines to show after each match (rg -A). Requires output_mode: \"content\", ignored otherwise.",
      "type": "number"
    },
    "-B": {
      "description": "Number of lines to show before each match (rg -B). Requires output_mode: \"content\", ignored otherwise.",
      "type": "number"
    },
    "-C": {
      "description": "Alias for context.",
      "type": "number"
    },
    "-i": {
      "description": "Case insensitive search (rg -i)",
      "type": "boolean"
    },
    "-n": {
      "description": "Show line numbers in output (rg -n). Requires output_mode: \"content\", ignored otherwise. Defaults to true.",
      "type": "boolean"
    },
    "-o": {
      "description": "Print only the matched (non-empty) parts of each matching line, one match per output line (rg -o / --only-matching). Requires output_mode: \"content\", ignored otherwise. Defaults to false.",
      "type": "boolean"
    },
    "context": {
      "description": "Number of lines to show before and after each match (rg -C). Requires output_mode: \"content\", ignored otherwise.",
      "type": "number"
    },
    "glob": {
      "description": "Glob pattern to filter files (e.g. \"*.js\", \"*.{ts,tsx}\") - maps to rg --glob",
      "type": "string"
    },
    "head_limit": {
      "description": "Limit output to first N lines/entries, equivalent to \"| head -N\". Works across all output modes: content (limits output lines), files_with_matches (limits file paths), count (limits count entries). Defaults to 250 when unspecified. Pass 0 for unlimited (use sparingly — large result sets waste context).",
      "type": "number"
    },
    "multiline": {
      "description": "Enable multiline mode where . matches newlines and patterns can span lines (rg -U --multiline-dotall). Default: false.",
      "type": "boolean"
    },
    "offset": {
      "description": "Skip first N lines/entries before applying head_limit, equivalent to \"| tail -n +N | head -N\". Works across all output modes. Defaults to 0.",
      "type": "number"
    },
    "output_mode": {
      "description": "Output mode: \"content\" shows matching lines (supports -A/-B/-C context, -n line numbers, head_limit), \"files_with_matches\" shows file paths (supports head_limit), \"count\" shows match counts (supports head_limit). Defaults to \"files_with_matches\".",
      "enum": [
        "content",
        "files_with_matches",
        "count"
      ],
      "type": "string"
    },
    "path": {
      "description": "File or directory to search in (rg PATH). Defaults to current working directory.",
      "type": "string"
    },
    "pattern": {
      "description": "The regular expression pattern to search for in file contents",
      "type": "string"
    },
    "type": {
      "description": "File type to search (rg --type). Common types: js, py, rust, go, java, etc. More efficient than include for standard file types.",
      "type": "string"
    }
  },
  "required": [
    "pattern"
  ],
  "type": "object"
}
```

## `Read`
从本地文件系统读取文件。

- `file_path` 必须是绝对路径。
- 默认最多读取 2000 行。
- 可以可选地指定行偏移和行数上限（对长文件特别有用），但建议不提供这些参数、直接读取整个文件。
- 结果以 cat -n 格式返回，行号从 1 开始。
- 可以读取图片（PNG、JPG 等）并以视觉方式呈现。通过 `pages` 参数读取 PDF（例如 "1-5"，每次请求最多 20 页；超过 10 页的 PDF 必须提供该参数）。读取 Jupyter notebook（.ipynb）时会按单元格连同输出一起返回。
- 读取目录、不存在的文件或空文件时，会返回错误或系统提示，而不是内容。
- 不要为了验证而重新读取你刚刚编辑过的文件——如果修改失败，Edit/Write 本身就会报错，而且 harness 会为你跟踪文件状态。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "file_path": {
      "description": "The absolute path to the file to read",
      "type": "string"
    },
    "limit": {
      "description": "The number of lines to read. Only provide if the file is too large to read at once.",
      "exclusiveMinimum": 0,
      "maximum": 9007199254740991,
      "type": "integer"
    },
    "offset": {
      "description": "The line number to start reading from. Only provide if the file is too large to read at once",
      "maximum": 9007199254740991,
      "minimum": 0,
      "type": "integer"
    },
    "pages": {
      "description": "Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.",
      "type": "string"
    }
  },
  "required": [
    "file_path"
  ],
  "type": "object"
}
```

## `ReportFindings`
以类型化列表的形式报告代码审查发现，以便宿主 UI 渲染。仅当当前生效的代码审查指令要求用本工具报告发现时才使用；否则遵循那些指令指定的输出格式。报告审查结果时，只调用一次，传入经过验证的发现，按严重程度从高到低排序（如果没有发现通过验证，则传空数组），并且不要同时把发现以文本形式打印出来。在应用修复后重新报告时（仅当应用指令要求时），将每个发现的 `outcome` 设置为实际发生的情况。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "findings": {
      "description": "Verified findings, most-severe first; empty if none survived",
      "items": {
        "additionalProperties": false,
        "properties": {
          "category": {
            "description": "Short kebab-case slug of the finding type, e.g. \"correctness\", \"simplification\", \"efficiency\", \"test-coverage\"",
            "maxLength": 40,
            "type": "string"
          },
          "failure_scenario": {
            "description": "Concrete inputs/state → wrong output/crash",
            "type": "string"
          },
          "file": {
            "description": "Repo-relative path of the file the finding is in",
            "type": "string"
          },
          "line": {
            "description": "1-indexed line the finding anchors to",
            "maximum": 9007199254740991,
            "minimum": -9007199254740991,
            "type": "integer"
          },
          "outcome": {
            "description": "Set ONLY when re-reporting after applying fixes: what happened to this finding",
            "enum": [
              "fixed",
              "skipped",
              "no_change_needed"
            ],
            "type": "string"
          },
          "summary": {
            "description": "One-sentence statement of the defect",
            "type": "string"
          },
          "verdict": {
            "description": "Set when a verify pass ran; absent on inline-only reviews",
            "enum": [
              "CONFIRMED",
              "PLAUSIBLE"
            ],
            "type": "string"
          }
        },
        "required": [
          "file",
          "summary",
          "failure_scenario"
        ],
        "type": "object"
      },
      "maxItems": 32,
      "type": "array"
    },
    "level": {
      "description": "Effort level the review ran at",
      "enum": [
        "low",
        "medium",
        "high",
        "xhigh",
        "max"
      ],
      "type": "string"
    }
  },
  "required": [
    "findings"
  ],
  "type": "object"
}
```

## `Skill`
在主对话中执行一个 skill

当用户要求你执行任务时，检查是否有可用的 skill 与之匹配。skill 提供专门的能力和领域知识。

当用户提到 "斜杠命令" 或 "/<something>" 时，他们指的就是 skill。使用本工具来调用它。

调用方式：
- 将 `skill` 设置为可用 skill 的准确名称（不带前导斜杠）。对于带插件命名空间的 skill，使用完整的 `plugin:skill` 形式。
- 通过 `args` 传递可选参数。
- 有些 skill 限定在特定目录下：其名称带有目录前缀（例如 `apps/web:deploy`），且描述中会说明它适用于哪个目录。当某个 skill 名称同时存在带作用域和不带作用域的变体时，根据你正在处理的文件来选择：如果文件位于某个变体的目录之下，就调用该变体（最具体的目录优先）；否则调用不带作用域的那个。

重要：
- 可用的 skill 会在对话的 system-reminder 消息中列出
- 只调用出现在该列表中的 skill，或者用户在消息中明确输入的 `/<name>`。绝不要凭训练数据猜测或编造 skill 名称；否则不要调用本工具
- 当某个 skill 与用户的请求匹配时，这是一个阻塞性要求：在生成任何其他关于该任务的回复之前，先调用相应的 Skill 工具
- 绝不要在不实际调用本工具的情况下提及某个 skill
- 不要调用已经在运行的 skill
- 不要将本工具用于内置 CLI 命令（如 /help、/clear 等）
- 如果你在当前对话回合中看到 <command-name> 标签，说明该 skill 已经被加载——直接按照其指示执行，不要再调用本工具

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
## `Workflow`
执行一个 workflow 脚本，确定性地编排多个 subagent。Workflow 在后台运行——本工具立即返回一个 task ID，workflow 完成时会收到一条 <task-notification>。使用 /workflows 查看实时进度。

Workflow 把工作组织到多个 agent 之间——为了全面（分解并并行覆盖）、为了可靠（提交前引入独立视角和对抗性检查）、或为了承担单个上下文装不下的规模（迁移、审计、大范围扫荡）。脚本就是你编码这种结构的地方：什么扇出、什么验证、什么综合。

仅当用户明确选择加入多 agent 编排时才调用本工具。Workflow 可能派生数十个 agent 并消耗大量 token；这种规模必须由用户主动要求，而不是靠你推断。明确选择加入指以下之一：
- 用户在 prompt 中包含了关键词 "ultracode"（你会看到一条 system-reminder 确认此事）。
- 本会话已开启 ultracode（有 system-reminder 确认）——见下文 **Ultracode**。
- 用户用自己的话直接要求你运行 workflow 或使用多 agent 编排（"use a workflow"、"run a workflow"、"fan out agents"、"orchestrate this with subagents"）。该要求必须出自用户之口——仅仅是从 workflow 中受益的任务不算数。
- 用户调用了某个 skill 或 slash command，其指示要求你调用 Workflow。
- 用户要求你运行某个具名的或已保存的 workflow。

对于任何其他任务——即使明显能从并行中受益——也不要调用本工具。改用 Agent 工具处理单个 subagent，或者简要说明多 agent workflow 能做什么、大致花费多少，然后询问用户是否运行。可以提醒用户：在后续消息中说 "use a workflow" 即可跳过询问。

当你确实要调用它时，正确的做法往往是**混合式**：先内联侦察（列出文件、找到渠道、圈定 diff 范围）以发现工作清单，然后调用 Workflow 在其上跑 pipeline。你不需要在*任务*开始前就知道形状——只需要在*编排步骤*之前知道。

常见的单阶段 workflow，可以跨多轮串联：
- **理解**——并行 reader 扫过相关子系统 → 结构化地图
- **设计**——N 个独立方案的评审团 → 打分后的综合
- **审查**——分维度 → 查找 → 对抗性验证（示例见下）
- **调研**——多模态扫荡 → 深读 → 综合
- **迁移**——发现位置 → 逐一转换（worktree 隔离）→ 验证

更大的工作可以按顺序跑好几个——先读每个结果再决定下一阶段。你始终在环路中；每个 workflow 都是一次边界清晰的扇出。

**Ultracode。** 当 system-reminder 确认 ultracode 已开启时，该选择加入持续有效：默认对每个实质性任务都编写并运行 workflow。目标是给出你能产出的最详尽、最正确的答案——token 成本不是约束。对于多阶段工作（理解 → 设计 → 实现 → 审查），这通常意味着按顺序跑多个 workflow——每阶段一个——这样你能在阶段之间保持参与。下面的质量模式（对抗性验证、多模态扫荡、完整性批评者、循环直到枯竭）是工具；按任务挑选合适的。倾向于用 workflow 编排并对抗性地验证你的发现——除非工作很琐碎或已被验证。仅在对话性轮次或琐碎的机械编辑时才单干。当 reminder 说 ultracode 已关闭时，恢复上面的选择加入规则。

通过 `script` 内联传入脚本——不要先把它 Write 到文件。每次调用都会自动把脚本持久化到会话目录下的一个文件，并在工具结果中返回路径。要迭代 workflow，用 Write/Edit 编辑该文件，然后用 `{scriptPath: "<path>"}` 重新调用 Workflow，而不是重发完整脚本。

每个脚本都必须以 `export const meta = {...}` 开头：
  export const meta = {
    name: 'find-flaky-tests',
    description: 'Find flaky tests and propose fixes',   // one-line, shown in permission dialog
    phases: [                                            // one entry per phase() call
      { title: 'Scan', detail: 'grep test logs for retries' },
      { title: 'Fix', detail: 'one agent per flaky test' },
    ],
  }
  // script body starts here — use agent()/parallel()/pipeline()/phase()/log()
  phase('Scan')
  const flaky = await agent('grep CI logs for retry markers', {schema: FLAKY_SCHEMA})
  ...

`meta` 对象必须是纯字面量——不能有变量、函数调用、展开运算符或模板插值。必填字段：`name`、`description`。可选：`whenToUse`（显示在 workflow 列表中）、`phases`。meta.phases 中的阶段标题必须与 phase() 调用中使用的完全一致——标题按精确匹配；没有匹配 meta 条目的 phase() 调用只会得到自己的进度分组。当某个阶段使用特定的模型覆盖时，在该阶段条目中加入 `model`。

脚本主体可用的钩子：
- agent(prompt: string, opts?: {label?: string, phase?: string, schema?: object, model?: string, effort?: string, isolation?: 'worktree', agentType?: string}): Promise<any> —— 派生一个 subagent。不带 schema 时，以字符串形式返回其最终文本。带 schema（一个 JSON Schema）时，subagent 被强制调用 StructuredOutput 工具，agent() 返回校验后的对象——无需解析。如果用户在运行中途跳过该 agent，或 subagent 在重试后仍死于不可恢复的 API 错误，则返回 null（用 .filter(Boolean) 过滤）。opts.label 覆盖显示标签。opts.phase 显式把该 agent 分配到某个进度分组（在 pipeline()/parallel() 阶段内部使用它，以避免对全局 phase() 状态的竞争——相同的 phase 字符串 → 相同的分组框）。opts.model 覆盖本次 agent 调用的模型。默认应省略——agent 会继承主循环模型（解析后的会话模型），这几乎总是正确的。只有当你非常确信另一档模型更适合该任务时才设置；不确定就省略。opts.effort 覆盖本次 agent 调用的推理强度（'low' | 'medium' | 'high' | 'xhigh' | 'max'）——省略则继承会话强度；对廉价的机械性阶段用 'low'，更高档位只留给最难的 verify/judge 阶段。opts.isolation: 'worktree' 在一个全新的 git worktree 中运行该 agent——开销大（每个 agent 约 200-500ms 的初始化 + 磁盘占用），仅当多个 agent 并行修改文件、否则就会冲突时才使用；若 worktree 无改动会被自动删除。opts.agentType 使用自定义 subagent 类型（例如 'general-purpose'、'code-reviewer'）代替默认的 workflow subagent——从与 Agent 工具相同的注册表解析；可与 schema 组合（自定义 agent 的 system prompt 会追加一条 StructuredOutput 指示）。
- pipeline(items, stage1, stage2, ...): Promise<any[]> —— 让每个 item 独立地依次经过所有阶段，阶段之间没有屏障。item A 可以在第 3 阶段时，item B 还在第 1 阶段。这是多阶段工作的默认选择。墙上时钟 = 最慢的单条 item 链，而不是每阶段最慢者之和。每个阶段回调收到 (prevResult, originalItem, index)——在后续阶段中用 originalItem/index 标记工作，而不必把上下文穿进第 1 阶段的返回值。抛出异常的阶段会把该 item 置为 `null` 并跳过其剩余阶段。
- parallel(thunks: Array<() => Promise<any>>): Promise<any[]> —— 并发运行任务。这是一个屏障：返回前会等待所有 thunk。抛出异常（或其 agent 出错）的 thunk 在结果数组中解析为 `null`——调用本身永远不会 reject，所以使用结果前先 `.filter(Boolean)`。仅当你确实需要同时拿到所有结果时才使用。
- log(message: string): void —— 向用户发出一条进度消息（显示为进度树上方的一行旁白）
- phase(title: string): void —— 开始一个新阶段；后续的 agent() 调用在进度显示中归入此标题下
- args: any —— 作为 Workflow 的 `args` 输入原样传入的值（未提供时为 undefined）。在工具调用中把数组/对象作为真正的 JSON 值传入，而不是 JSON 编码的字符串——写 `args: ["a.ts", "b.ts"]`，而不是 `args: "[\"a.ts\", ...]"`（字符串化的列表到达脚本时是一个字符串，`args.filter`/`args.map` 会抛错）。用它把具名 workflow 参数化——例如直接传入研究问题、目标路径或配置对象，而不是走旁路文件。
- budget: {total: number|null, spent(): number, remaining(): number} —— 本轮的 token 目标，来自用户 "+500k" 式的指令。未设置目标时 `budget.total` 为 null。`budget.spent()` 返回本轮主循环和所有 workflow 已消耗的 output token——池子是共享的，不是按 workflow 分的。`budget.remaining()` 返回 `max(0, total - spent())`，未设目标时为 `Infinity`。该目标是硬上限，不是建议值：一旦 `spent()` 达到 `total`，后续的 `agent()` 调用会抛错。用于动态循环：`while (budget.total && budget.remaining() > 50_000) { ... }`，或静态缩放：`const FLEET = budget.total ? Math.floor(budget.total / 100_000) : 5`。
- workflow(nameOrRef: string | {scriptPath: string}, args?: any): Promise<any> —— 把另一个 workflow 作为子步骤内联运行，并返回它的返回值。传入名称以调用已保存的 workflow（与 {name: "..."} 同一注册表），或传 {scriptPath} 运行你之前 Write 的脚本文件。子 workflow 共享本次运行的并发上限、agent 计数器、中止信号和 token 预算——它的 agent 在 /workflows 中显示在 "▸ name" 分组下，其 token 计入 budget.spent()。args 参数成为子 workflow 的 `args` 全局变量。嵌套仅限一层：在子 workflow 内调用 workflow() 会抛错。名称未知 / scriptPath 不可读 / 子脚本语法错误时抛错；用 catch 优雅处理。

Subagent 会被告知：它们的最终文本就是返回值（不是面向人类的消息），所以它们返回原始数据。要结构化输出，使用 schema 选项——校验发生在工具调用层，不匹配时模型会重试。

Workflow 的 agent 可以通过 ToolSearch 访问所有会话连接的 MCP 工具——schema 按 agent 按需加载。注意：交互式认证的 MCP 服务器（例如 claude.ai）在 headless/cron 运行中可能缺席。

脚本是纯 JavaScript，不是 TypeScript——类型注解（`: string[]`）、interface 和泛型无法解析。脚本主体运行在 async 上下文中——直接使用 await。标准 JS 内建对象（JSON、Math、Array 等）可用——除了 `Date.now()`/`Math.random()`/无参 `new Date()`，它们会抛错（会破坏 resume）；通过 `args` 传入时间戳，在 workflow 返回后再盖时间戳，需要随机性时按 index 改变 agent 的 prompt/label。没有文件系统或 Node.js API 访问。

默认使用 pipeline()。只有当你确实需要同时拿到所有前一阶段的结果时，才使用屏障（阶段之间的 parallel）。

屏障仅在以下情况才正确：第 N 阶段需要来自第 N-1 阶段全部结果的跨 item 上下文：
- 在昂贵的下游工作之前，对完整结果集去重/合并
- 总数为零时提前退出（"发现 0 个 bug → 完全跳过验证"）
- 第 N 阶段的 prompt 引用"其他发现"做比较

以下理由不能为屏障正名：
- "我需要先 flatten/map/filter"——在 pipeline 阶段内部做：pipeline(items, stageA, r => transform([r]).flat(), stageB)
- "这些阶段在概念上是分开的"——这正是 pipeline() 所建模的。分开的阶段 ≠ 同步的阶段。
- "代码更干净"——屏障延迟是真实存在的。如果 5 个 finder 在跑，最慢的耗时是最快的 3 倍，屏障会浪费掉快速 finder 2/3 的空闲时间。

嗅觉测试：如果你写的是
  const a = await parallel(...)
  const b = transform(a)        // flatten, map, filter — no cross-item dependency
  const c = await parallel(b.map(...))
中间那个 transform 并不需要屏障。改写成 pipeline，把 transform 放进某个阶段里。拿不准时：用 pipeline。

每个 workflow 的并发 agent() 调用上限为 min(16, cpu 核数 - 2)——超出的调用排队，等槽位空出再运行。你仍然可以给 parallel()/pipeline() 传 100 个 item，它们都会完成；只是任一时刻只有约 10 个在跑。一个 workflow 生命周期内的 agent 总数上限为 1000——这是失控循环的兜底，远高于任何真实 workflow。单次 parallel()/pipeline() 调用最多接受 4096 个 item；传更多是显式报错，而不是静默截断。

典型的多阶段模式——默认 pipeline，每个维度一旦审查完成就立即验证：
  export const meta = {
    name: 'review-changes',
    description: 'Review changed files across dimensions, verify each finding',
    phases: [{ title: 'Review' }, { title: 'Verify' }],
  }
  const DIMENSIONS = [{key: 'bugs', prompt: '...'}, {key: 'perf', prompt: '...'}]
  const results = await pipeline(
    DIMENSIONS,
    d => agent(d.prompt, {label: `review:${d.key}`, phase: 'Review', schema: FINDINGS_SCHEMA}),
    review => parallel(review.findings.map(f => () =>
      agent(`Adversarially verify: ${f.title}`, {label: `verify:${f.file}`, phase: 'Verify', schema: VERDICT_SCHEMA})
        .then(v => ({...f, verdict: v}))
    ))
  )
  const confirmed = results.flat().filter(Boolean).filter(f => f.verdict?.isReal)
  return { confirmed }
  // Dimension 'bugs' findings verify while dimension 'perf' is still reviewing. No wasted wall-clock.

屏障确实正确的情形——在昂贵的验证之前对所有发现去重：
  const all = await parallel(DIMENSIONS.map(d => () => agent(d.prompt, {schema: FINDINGS_SCHEMA})))
  const deduped = dedupeByFileAndLine(all.filter(Boolean).flatMap(r => r.findings))  // <-- genuinely needs ALL at once
  const verified = await parallel(deduped.map(f => () => agent(verifyPrompt(f), {schema: VERDICT_SCHEMA})))

循环直到达数模式——累积到目标数量：
  const bugs = []
  while (bugs.length < 10) {
    const result = await agent("Find bugs in this codebase.", {schema: BUGS_SCHEMA})
    bugs.push(...result.bugs)
    log(`${bugs.length}/10 found`)
  }

循环直到预算耗尽模式——按用户 "+500k" 指令缩放深度。要用 budget.total 做守卫：未设目标时 remaining() 为 Infinity，循环会一直跑到 1000 个 agent 的上限。
  const bugs = []
  while (budget.total && budget.remaining() > 50_000) {
    const result = await agent("Find bugs in this codebase.", {schema: BUGS_SCHEMA})
    bugs.push(...result.bugs)
    log(`${bugs.length} found, ${Math.round(budget.remaining()/1000)}k remaining`)
  }

组合模式——穷尽式审查（查找 → 与 seen 去重 → 多视角评审团 → 循环直到枯竭）：
  const seen = new Set(), confirmed = []
  let dry = 0
  while (dry < 2) {                                              // loop-until-dry
    const found = (await parallel(FINDERS.map(f => () =>          // barrier: collect all finders this round
      agent(f.prompt, {phase: 'Find', schema: BUGS})))).filter(Boolean).flatMap(r => r.bugs)
    const fresh = found.filter(b => !seen.has(key(b)))           // dedup vs ALL seen — plain code, not an agent
    if (!fresh.length) { dry++; continue }
    dry = 0; fresh.forEach(b => seen.add(key(b)))
    const judged = await parallel(fresh.map(b => () =>           // every fresh bug judged concurrently...
      parallel(['correctness','security','repro'].map(lens => () =>   // ...each by 3 distinct lenses
        agent(`Judge "${b.desc}" via the ${lens} lens — real?`, {phase: 'Verify', schema: VERDICT})))
        .then(vs => ({ b, real: vs.filter(Boolean).filter(v => v.real).length >= 2 }))))
    confirmed.push(...judged.filter(v => v.real).map(v => v.b))
  }
  return confirmed
  // dedup vs `seen`, NOT `confirmed` — else judge-rejected findings reappear every round and it never converges.

质量模式——常见形状；按任务挑选，自由组合：
- 对抗性验证：每个发现派生 N 个独立的怀疑者，每个都被要求去反驳。若 ≥ 多数反驳则杀掉该发现。防止看似合理但错误的发现存活下来。
    const votes = await parallel(Array.from({length: 3}, () => () =>
      agent(`Try to refute: ${claim}. Default to refuted=true if uncertain.`, {schema: VERDICT})))
    const survives = votes.filter(Boolean).filter(v => !v.refuted).length >= 2
- 多视角验证：当一个发现可能以多种方式出错时，给每个验证者一个不同的视角（正确性、安全性、性能、能否复现），而不是 N 个相同的反驳者——多样性能抓到冗余抓不到的失败模式。
- 评审团：从不同角度生成 N 个独立尝试（例如 MVP 优先、风险优先、用户优先），用并行评委打分，以胜者为底综合，同时嫁接亚军的最佳点子。解空间宽广时，胜过单次尝试反复迭代。
- 循环直到枯竭：对规模未知的发现任务（bug、问题、边界情况），持续派生 finder，直到连续 K 轮没有新发现。简单计数器（while count < N）会漏掉长尾。
- 多模态扫荡：并行 agent 各用不同方式搜索（按容器、按内容、按实体、按时间）。彼此看不到对方的发现；当单一搜索角度找不全时很有用。
- 完整性批评者：最后一个 agent 追问"还缺什么——哪种模态没跑、哪条论断没验证、哪个来源没读？"它的发现成为下一轮工作。
- 不做静默截断：如果 workflow 限制了覆盖范围（top-N、不重试、采样），用 `log()` 说明被丢弃的部分——静默截断读起来像"全部覆盖了"，而实际并没有。

按用户要求的规模来。"find any bugs" → 几个 finder，单票验证。"thoroughly audit this" 或 "be comprehensive" → 更大的 finder 池、3–5 票的对抗性验证、综合阶段。拿不准时，研究/审查/审计类请求倾向彻底，快速检查类倾向简短。

这些模式并不穷尽——任务需要时，组合出新式框架（锦标赛对阵、自修复循环、逐级升级，什么合适用什么）。

当多步编排的控制流应当是确定性的（循环、条件、扇出）而非模型驱动时，使用本工具。

## 恢复

工具结果中包含一个 runId。要在暂停、终止或脚本编辑之后恢复，用 Workflow({scriptPath, resumeFromRunId}) 重新启动——未改动的 agent() 调用最长前缀会立即返回缓存结果；第一个被编辑/新增的调用及其后所有调用都实时运行。相同脚本 + 相同 args → 100% 缓存命中。在诊断已完成的 workflow 为何返回空或意外结果之前，先 Read <transcriptDir>/journal.jsonl——它记录了每个 agent 的实际返回值；不要假设缓存结果非空。脚本中不可用 Date.now()/Math.random()/new Date()（它们会破坏这一机制）——在 workflow 返回后再盖时间戳，或通过 args 传入时间戳。没有 journal 可用时的兜底方案：Read transcript 目录中的 agent-<id>.jsonl 文件，手工编写续跑脚本。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "args": {
      "description": "Optional input value exposed to the script as the global `args`, verbatim. Pass arrays/objects as actual JSON values, NOT as a JSON-encoded string — a stringified list breaks `args.filter`/`args.map` in the script. Use for parameterized named workflows (e.g. a research question)."
    },
    "description": {
      "description": "Ignored — set the workflow description in the script's `meta` block.",
      "type": "string"
    },
    "name": {
      "description": "Name of a predefined workflow (built-in or from .claude/workflows/). Resolves to a self-contained script.",
      "type": "string"
    },
    "resumeFromRunId": {
      "description": "Run ID of a prior Workflow invocation to resume from. Completed agent() calls with unchanged (prompt, opts) return their cached results instantly; only edited or new calls re-run. Same-session only. Stop the prior run first (TaskStop) before resuming.",
      "pattern": "^wf_[a-z0-9-]{6,}$",
      "type": "string"
    },
    "script": {
      "description": "Self-contained workflow script. Must begin with `export const meta = { name, description, phases }` (pure literal, no computed values) followed by the script body using agent()/parallel()/pipeline()/phase().",
      "maxLength": 524288,
      "type": "string"
    },
    "scriptPath": {
      "description": "Path to a workflow script file on disk. Every Workflow invocation persists its script under the session directory and returns the path in the tool result. To iterate, edit that file with Write/Edit and re-invoke Workflow with the same `scriptPath` instead of re-sending the full script. Takes precedence over `script` and `name`.",
      "type": "string"
    },
    "title": {
      "description": "Ignored — set the workflow title in the script's `meta` block.",
      "type": "string"
    }
  },
  "type": "object"
}
```

## `Write`
将文件写入本地文件系统，如已存在则覆盖。

何时使用：创建新文件，或完全替换一个你已经 Read 过的文件。覆盖一个尚未 Read 的已有文件会失败。局部修改请改用 Edit。

**input_schema:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": false,
  "properties": {
    "content": {
      "description": "The content to write to the file",
      "type": "string"
    },
    "file_path": {
      "description": "The absolute path to the file to write (must be absolute, not relative)",
      "type": "string"
    }
  },
  "required": [
    "file_path",
    "content"
  ],
  "type": "object"
}
```
