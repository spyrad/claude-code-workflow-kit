# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Claude Code workflow toolkit** — a collection of skills, agent roles, frameworks, and templates that extend Claude Code's capabilities for structured development workflows. It is not a runnable application; it contains markdown-based prompts and configuration files.

The primary language for skills and documentation is **German**. The memory framework (`frameworks/claude-code-memory-framework/`) documentation is in **Polish** (third-party inclusion). Code, file names, and technical terms remain in English.

## How This Repo Is Used

This is a **distribution repository**, not a standalone project. Users copy parts into their own projects:
- `skills/` → target project's `.claude/skills/`
- `agents/` → target project root
- `personas/` → target project's `.claude/personas/`
- `commands/` → target project's `.claude/commands/`
- `frameworks/` templates → target project's `memory/` directory
- `settings.json` → target project's `.claude/settings.json`

There are no build steps, tests, or runtime dependencies. The `context7` plugin is enabled in settings.json.

**Distribution model:** `dtb:kit-sync` installs class-A artifacts (`skills/dtb-*/SKILL.md`,
`agents/*.md`, `commands/dtb-*.md`) globally to `~/.claude/` and records a content hash per
file in `~/.claude/dtb-lock.json` (three-point drift detection repo ↔ lock ↔ copy; source is
this repo on GitHub). Seeds (`frameworks/`, `settings.json`, `DERIVED_STATE_RULES.md`) are
copied per project by `dtb:project-init` and never drift-checked. `dtb:project-init` writes
its CLAUDE.md block in target projects between `<!-- BEGIN dtb -->…<!-- END dtb -->` sentinel
markers (idempotent updates, user text untouched).

## DTB Skill System

The `/dtb:*` skills form a German-language workflow system for managing development sessions. Skills are the primary delivery format — they support YAML frontmatter with natural language triggers and are auto-detected by Claude Code.

### Skill Workflow Lifecycle

Skills are designed to work together in a session lifecycle:
1. **Start/Resume**: `workflow-resume` derives the active feature from artifacts (PLAN `## Progress`) and reads `WORKFLOW_STATUS.md` for context
2. **Work**: Use `feature-plan`, `debug-plan`, `code-review`, `build-check` during development; check off `## Progress` boxes (with commit SHA) after each implemented step
3. **Save**: `workflow-checkpoint` writes a session log AND overwrites `WORKFLOW_STATUS.md` (status block generated from artifacts, context block manual)
4. **Next session**: `workflow-resume` picks up where the progress checkboxes left off — even without a checkpoint

**Derived State principle:** Feature status is never maintained manually — it is derived
from artifact existence and `## Progress` checkboxes in `PLAN_*.md` (single source of truth).
Rules live in `dtb-project/project-rules/DERIVED_STATE_RULES.md`; all read-side skills
(`workflow-next`, `workflow-status`, `workflow-resume`, `backlog-status`) reference that file.
Status fields in BACKLOG.md/FEATURE_*.md are derived displays synced by `workflow-checkpoint`.
On conflict the artifact wins and the mismatch is reported. `IMPL_STATUS_*.md` is abolished.

### Skill Categories

- **Session lifecycle**: `workflow-checkpoint`, `workflow-resume`, `workflow-status`, `workflow-next`, `session-summary` (read-only recap of active session / a given day / last 7 days)
- **Idea management**: `idea` (quick capture), `idea-review` (triage)
- **Feature workflow**: `feature-discover` (requirements gathering), `feature-plan` (with inbox integration), `impl-plan`, `plan-review`, `feature-start`
- **Bug workflow**: `bug-report` (quick capture with severity), `debug-plan` (root-cause analysis + fix strategy)
- **Project setup**: `project-init`, `project-health`, `project-team`
- **Greenfield**: `greenfield-prd`, `greenfield-roadmap`
- **Maintenance**: `archive` (move completed/discarded items to archive), `kit-sync` (install/update installed kit copies under `~/.claude/` via lock-based drift detection — see below)
- **Development**: `build-check`, `code-review`, `backlog-status`, `repo-sync`
- **Knowledge management**: `docs-extract` (scan input/ folder, extract facts from documents into thematic MDs), `lesson` (capture a reusable lesson append-only into `project-rules/lessons.md`, read as a prior by impl-plan/debug-plan/plan-review/code-review — replaces the dead `pitfalls.md` concept)
- **Documentation**: `pipeline-graph` (generate interactive HTML overview of entire skill pipeline from frontmatter)

### Agent Roles

Reusable agent definitions in `agents/` are referenced by skills (e.g. `dtb:plan-review`):
- `architekt.md` — Technical reviewer (feasibility, dependencies, risks)
- `pragmatiker.md` — Scope guardian (MVP cut, effort-value, prioritization)
- `senior-dev.md` — Implementation reviewer (time estimates, test strategy, code-level feasibility)

### Personas

Personas in `personas/` differ from agent roles: agent roles work **on a code artifact** (a review), personas work **with the human over an event** (a pitch, a kick-off). Each persona lives in its own directory (`personas/dtb-<name>/`) with:
- `COGNITIVE.md` — core thinking, voice, decision filters, known risks
- `README.md` — when to use / when not to use, activation examples, relationship to other personas
- `cognitive/` — optional context overlays (planned)
- `input/` — optional source documents (empty if the persona was constructed in dialogue)

Current persona: `dtb-stakeholder-pitch-coach` — coaching for business-stakeholder pitches with a commitment goal (pilot, beta, budget). **Coach-only by design**: delivers structure, talking points, and rationale — never read-aloud scripts.

### Commands

Slash-command definitions in `commands/` (`commands/dtb-<name>.md`) activate a persona or workflow shortcut. They use YAML frontmatter (`description`) and `@`-references to pull persona files into context. Example: `/dtb-pitch-coach` activates the `dtb-stakeholder-pitch-coach` persona with its hard coach-only rule.

### Output Locations (in target project)

- `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` — Session logs (appended per session)
- `dtb-project/project-workflows/WORKFLOW_STATUS.md` — Status dashboard (overwritten each update, max 60-80 lines)
- `dtb-project/project-workflows/features/DISCOVERY_*.md` — Discovery docs (requirements gathering before spec writing)
- `dtb-project/project-workflows/features/FEATURE_*.md` — Feature specs (UPPER_SNAKE_CASE naming)
- `dtb-project/project-workflows/features/BUG_*.md` — Bug reports (UPPER_SNAKE_CASE naming, same directory as features)
- `dtb-project/project-workflows/features/TASK_*.md` — Operational/infrastructure tasks (UPPER_SNAKE_CASE naming, lightweight checklists)
- `dtb-project/project-workflows/features/PLAN_*.md` — Implementation plans (paired with FEATURE_*.md by name)
- `dtb-project/project-workflows/INBOX.md` — Idea inbox (managed by `dtb:idea` and `dtb:idea-review`)
- `dtb-project/project-workflows/archive/` — Archived items: completed features, discarded ideas, archive log
- `dtb-project/project-rules/` — Coding-Richtlinien pro Bereich/Technologie (generiert + manuell gepflegt)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — Zentrale Statusableitungs-Regeln (Kit-Bestandteil, von project-init verteilt; einzige versionierte Datei in project-rules/)
- `dtb-project/project-rules/lessons.md` — Append-only Lektionen-Sammlung (Laufzeit-Artefakt, angelegt von `dtb:lesson`; Prior für impl-plan/debug-plan/plan-review/code-review; keine Coding-Rule)
- `dtb-project/project-infrastructure/input/` — Drop-Zone für Infra-Dokumente (PDFs, Configs, Exports)
- `dtb-project/project-infrastructure/*.md` — Extrahierte Infra-Fakten (UPPER_SNAKE_CASE, generiert von `dtb:docs-extract`)
- `dtb-project/project-requirements/input/` — Drop-Zone für Anforderungs-Dokumente
- `dtb-project/project-strategy/input/` — Drop-Zone für Strategie-Dokumente
- `integrations/<vendor-name>/input/` — Drop-Zone für Vendor-/Integrations-Dokumente

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
- WORKFLOW_STATUS.md: 1-line summaries with links only, no detail tables — details belong in session logs or test reports; status block is generated from artifacts (fixed template, placeholders only), context block is manual
- PLAN_*.md must contain a `## Progress` section (one checkbox per step N.M, commit SHA as evidence when checked) — format in `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- Status is derived, never trusted from fields: read-side skills derive from artifacts and report conflicts (artifact wins)
- Spec size limits: `FEATURE_*.md` and `PLAN_*.md` max 500 lines each (longer specs degrade AI processing quality)
- Pipeline metadata in frontmatter: `stage`, `after`, `next`, `consumes`, `produces`
- `workflow-status` reads pipeline frontmatter to auto-generate the flow visualization
- `dtb:code-review` reads rules from `{config.paths.rules}/` to validate implementations
