# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Claude Code workflow toolkit** — a collection of slash commands, frameworks, and templates that extend Claude Code's capabilities for structured development workflows. It is not a runnable application; it contains markdown-based prompts and configuration files.

The primary language for commands and documentation is **German**. Code, file names, and technical terms remain in English.

## Repository Structure

- `commands/dtb/` — Slash commands (invoked as `/dtb:<name>`) for development workflow management. These are markdown prompt templates, not executable code.
- `frameworks/claude-code-memory-framework/` — A framework for managing Claude Code's persistent memory effectively, with templates for CLAUDE.md, MEMORY.md, autonomy-rules.md, and pitfalls.md.
- `agents/` — Custom agent definitions (currently empty).
- `plugins/` — Plugin configurations (currently empty).
- `skills/` — Skill definitions (currently empty).
- `settings.json` — Project-level Claude Code settings (permissions, plugins, effort level).

## DTB Command System

The `/dtb:*` commands form a German-language workflow system for managing development sessions. Key commands:

- **Session lifecycle**: `workflow-checkpoint` (log session + update status), `workflow-status` (show current state), `workflow-resume` (continue after break)
- **Project documentation**: `analyze-project` (brownfield project onboarding), `project-architecture`, `project-context`, `project-prd`, `project-roadmap`, `project-glossary`
- **Development**: `feature-plan` (structured feature specs), `debug-plan` (debugging strategy), `code-review`, `build-check`, `backlog`
- **Utilities**: `repo-sync`, `unstuck` (session recovery)

All commands output to `dtb-project/` subdirectories:
- `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` — Session logs
- `dtb-project/project-workflows/WORKFLOW_STATUS.md` — Status dashboard (max 60-80 lines, overwritten each update)
- `dtb-project/project-workflows/FEATURE_*.md` — Feature specs

## Memory Framework

The `frameworks/claude-code-memory-framework/` provides templates for three patterns:

1. **Autonomy rules** (`autonomy-rules.md`) — Four-level permission taxonomy: ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE
2. **Pitfalls file** (`pitfalls.md`) — Institutional knowledge about non-obvious technical issues, grouped by technology
3. **Memory size management** — Keep MEMORY.md under 150 lines (hard cutoff at 200); use one-line summaries with pointers to topic files

## Conventions When Editing Commands

- Command files are markdown with frontmatter-style headers and embedded template blocks
- Templates use `[PLACEHOLDER]` syntax for values to be filled at runtime
- File paths in commands use forward slashes and are relative to the target project root
- Dates always use `YYYY-MM-DD` format, never relative terms
- Keep WORKFLOW_STATUS.md compact: 1-line summaries with links, no detail tables
