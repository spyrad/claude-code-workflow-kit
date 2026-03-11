# Claude Code Workflow Kit

> A collection of slash commands, frameworks, and templates that extend Claude Code
> with structured development workflows.

## What's Inside

- **16 Slash Commands** (`/dtb:*`) — German-language workflow system for session management,
  project documentation, feature planning, debugging, and code review
- **Memory Framework** — Production-tested patterns for managing Claude Code's persistent
  memory (autonomy rules, pitfalls tracking, memory size management)
- **Project Settings** — Pre-configured permissions and plugin setup

## Quick Start

1. Clone this repo into your project (or copy the parts you need):
   ```bash
   git clone https://github.com/SpyraD/claude-code-workflow-kit.git
   ```
2. Copy `commands/dtb/` to your project's `.claude/commands/dtb/`
3. Use commands via `/dtb:<name>` in Claude Code

## Commands Overview

| Command | Purpose |
|---------|---------|
| `/dtb:workflow-checkpoint` | Log session progress + update status dashboard |
| `/dtb:workflow-status` | Show current workflow state |
| `/dtb:workflow-resume` | Resume after a break |
| `/dtb:analyze-project` | Onboard into an existing (brownfield) project |
| `/dtb:feature-plan` | Create structured feature specifications |
| `/dtb:debug-plan` | Systematic debugging strategy |
| `/dtb:code-review` | Structured code review |
| `/dtb:build-check` | Build verification |
| `/dtb:project-architecture` | Document project architecture |
| `/dtb:project-context` | Capture project context |
| `/dtb:project-prd` | Generate product requirements |
| `/dtb:project-roadmap` | Create project roadmap |
| `/dtb:project-glossary` | Build project glossary |
| `/dtb:backlog` | Backlog overview |
| `/dtb:repo-sync` | Repository synchronization |
| `/dtb:unstuck` | Session recovery when stuck |

## Memory Framework

The included [Claude Code Memory Framework](frameworks/claude-code-memory-framework/)
provides templates for:

- **Autonomy Rules** — 4-level permission model (ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE)
- **Pitfalls File** — Institutional knowledge about non-obvious technical issues
- **Memory Management** — Keep MEMORY.md lean (<150 lines) with topic file pointers

## Project Structure

```
commands/dtb/          # Slash commands (markdown prompt templates)
frameworks/            # Memory framework with templates
agents/                # Custom agent definitions (extensible)
plugins/               # Plugin configurations (extensible)
skills/                # Skill definitions (extensible)
settings.json          # Claude Code project settings
CLAUDE.md              # Project instructions for Claude Code
```

## Note

- Commands and documentation are in **German**; code and file names are in English
- Commands are markdown-based prompt templates, not executable code
- Generated session data goes to `dtb-project/` (gitignored)

## License

MIT
