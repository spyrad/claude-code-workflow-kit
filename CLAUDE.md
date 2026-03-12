# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Claude Code workflow toolkit** — a collection of slash commands, frameworks, and templates that extend Claude Code's capabilities for structured development workflows. It is not a runnable application; it contains markdown-based prompts and configuration files.

The primary language for commands and documentation is **German**. The memory framework (`frameworks/claude-code-memory-framework/`) documentation is in **Polish** (third-party inclusion). Code, file names, and technical terms remain in English.

## How This Repo Is Used

This is a **distribution repository**, not a standalone project. Users copy parts into their own projects:
- `commands/dtb/` → target project's `.claude/commands/dtb/`
- `frameworks/` templates → target project's `memory/` directory
- `settings.json` → target project's `.claude/settings.json`

There are no build steps, tests, or runtime dependencies. The `context7` plugin is enabled in settings.json.

## DTB Command System

The `/dtb:*` commands form a German-language workflow system for managing development sessions.

### Command Workflow Lifecycle

Commands are designed to work together in a session lifecycle:
1. **Start/Resume**: `workflow-resume` reads `WORKFLOW_STATUS.md` to restore context
2. **Work**: Use `feature-plan`, `debug-plan`, `code-review`, `build-check` during development
3. **Save**: `workflow-checkpoint` writes a session log AND overwrites `WORKFLOW_STATUS.md`
4. **Next session**: `workflow-resume` picks up where checkpoint left off

### Command Categories

- **Session lifecycle**: `workflow-checkpoint`, `workflow-status`, `workflow-resume`
- **Project documentation**: `analyze-project` (brownfield onboarding), `project-architecture`, `project-context`, `project-prd`, `project-roadmap`, `project-glossary`
- **Development**: `feature-plan`, `debug-plan`, `code-review`, `build-check`, `backlog`
- **Utilities**: `repo-sync`, `unstuck` (session recovery)

### Output Locations (in target project)

- `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` — Session logs (appended per session)
- `dtb-project/project-workflows/WORKFLOW_STATUS.md` — Status dashboard (overwritten each update, max 60-80 lines)
- `dtb-project/project-workflows/FEATURE_*.md` — Feature specs (UPPER_SNAKE_CASE naming)

## Memory Framework

The `frameworks/claude-code-memory-framework/` provides templates for three patterns:

1. **Autonomy rules** (`autonomy-rules.md`) — Four-level permission taxonomy: ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE
2. **Pitfalls file** (`pitfalls.md`) — Institutional knowledge about non-obvious technical issues, grouped by technology
3. **Memory size management** — Keep MEMORY.md under 150 lines (hard cutoff at 200); use one-line summaries with pointers to topic files

## Conventions When Editing Commands

- Command files are markdown with embedded template blocks (fenced code blocks showing output format)
- Templates use `[PLACEHOLDER]` syntax for values to be filled at runtime
- File paths in commands use forward slashes and are relative to the target project root
- Dates always use `YYYY-MM-DD` format, never relative terms
- WORKFLOW_STATUS.md: 1-line summaries with links only, no detail tables — details belong in session logs or test reports
