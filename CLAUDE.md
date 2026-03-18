# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Claude Code workflow toolkit** — a collection of skills, agent roles, frameworks, and templates that extend Claude Code's capabilities for structured development workflows. It is not a runnable application; it contains markdown-based prompts and configuration files.

The primary language for skills and documentation is **German**. The memory framework (`frameworks/claude-code-memory-framework/`) documentation is in **Polish** (third-party inclusion). Code, file names, and technical terms remain in English.

## How This Repo Is Used

This is a **distribution repository**, not a standalone project. Users copy parts into their own projects:
- `skills/` → target project's `.claude/skills/`
- `agents/` → target project root
- `frameworks/` templates → target project's `memory/` directory
- `settings.json` → target project's `.claude/settings.json`

There are no build steps, tests, or runtime dependencies. The `context7` plugin is enabled in settings.json.

## DTB Skill System

The `/dtb:*` skills form a German-language workflow system for managing development sessions. Skills are the primary delivery format — they support YAML frontmatter with natural language triggers and are auto-detected by Claude Code.

### Skill Workflow Lifecycle

Skills are designed to work together in a session lifecycle:
1. **Start/Resume**: `workflow-resume` reads `WORKFLOW_STATUS.md` to restore context
2. **Work**: Use `feature-plan`, `debug-plan`, `code-review`, `build-check` during development
3. **Save**: `workflow-checkpoint` writes a session log AND overwrites `WORKFLOW_STATUS.md`
4. **Next session**: `workflow-resume` picks up where checkpoint left off

### Skill Categories

- **Session lifecycle**: `workflow-checkpoint`, `workflow-resume`, `workflow-status`
- **Idea management**: `idea` (quick capture), `idea-review` (triage)
- **Feature workflow**: `feature-discover` (requirements gathering), `feature-plan` (with inbox integration), `impl-plan`, `plan-review`, `feature-start`
- **Project setup**: `project-init`, `project-health`, `project-team`
- **Greenfield**: `greenfield-prd`, `greenfield-roadmap`
- **Maintenance**: `archive` (move completed/discarded items to archive)
- **Development**: `build-check`, `code-review`, `backlog-status`, `repo-sync`

### Agent Roles

Reusable agent definitions in `agents/` are referenced by skills (e.g. `dtb:plan-review`):
- `architekt.md` — Technical reviewer (feasibility, dependencies, risks)
- `pragmatiker.md` — Scope guardian (MVP cut, effort-value, prioritization)
- `senior-dev.md` — Implementation reviewer (time estimates, test strategy, code-level feasibility)

### Output Locations (in target project)

- `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` — Session logs (appended per session)
- `dtb-project/project-workflows/WORKFLOW_STATUS.md` — Status dashboard (overwritten each update, max 60-80 lines)
- `dtb-project/project-workflows/features/DISCOVERY_*.md` — Discovery docs (requirements gathering before spec writing)
- `dtb-project/project-workflows/features/FEATURE_*.md` — Feature specs (UPPER_SNAKE_CASE naming)
- `dtb-project/project-workflows/features/PLAN_*.md` — Implementation plans (paired with FEATURE_*.md by name)
- `dtb-project/project-workflows/INBOX.md` — Idea inbox (managed by `dtb:idea` and `dtb:idea-review`)
- `dtb-project/project-workflows/archive/` — Archived items: completed features, discarded ideas, archive log
- `dtb-project/project-rules/` — Coding-Richtlinien pro Bereich/Technologie (generiert + manuell gepflegt)

## Memory Framework

The `frameworks/claude-code-memory-framework/` provides templates for three patterns:

1. **Autonomy rules** (`autonomy-rules.md`) — Four-level permission taxonomy: ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE
2. **Pitfalls file** (`pitfalls.md`) — Institutional knowledge about non-obvious technical issues, grouped by technology
3. **Memory size management** — Keep MEMORY.md under 150 lines (hard cutoff at 200); use one-line summaries with pointers to topic files

## Conventions When Editing Skills

- Skill files are markdown with YAML frontmatter (`name`, `description`, `disable-model-invocation`, optional `argument-hint`, `allowed-tools`)
- Each skill lives in its own directory: `skills/dtb-<name>/SKILL.md`
- Templates use `[PLACEHOLDER]` syntax for values to be filled at runtime
- File paths in skills use forward slashes and are relative to the target project root
- Dates always use `YYYY-MM-DD` format, never relative terms
- WORKFLOW_STATUS.md: 1-line summaries with links only, no detail tables — details belong in session logs or test reports
- Pipeline metadata in frontmatter: `stage`, `after`, `next`, `consumes`, `produces`
- `workflow-status` reads pipeline frontmatter to auto-generate the flow visualization
- `dtb:code-review` reads rules from `{config.paths.rules}/` to validate implementations
