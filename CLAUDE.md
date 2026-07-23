# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **Claude Code workflow toolkit** — a collection of skills, agent roles, and templates that extend Claude Code's capabilities for structured development workflows. It is not a runnable application; it contains markdown-based prompts and configuration files.

The primary language for skills and documentation is **German**. Code, file names, and technical terms remain in English.

## How This Repo Is Used

This is a **distribution repository**, not a standalone project. Users copy parts into their own projects:
- `skills/` → target project's `.claude/skills/`
- `agents/` → target project root
- `commands/` → target project's `.claude/commands/`
- `settings.json` → target project's `.claude/settings.json`

There are no build steps, tests, or runtime dependencies. The `context7` plugin is enabled in settings.json.

**Distribution model:** `dtb:kit-sync` installs class-A artifacts (`skills/dtb-*/SKILL.md`,
`agents/*.md`, `commands/dtb-*.md`) globally to `~/.claude/` and records a content hash per
file in `~/.claude/dtb-lock.json` (three-point drift detection repo ↔ lock ↔ copy; source is
this repo on GitHub). Seeds (`settings.json`, `DERIVED_STATE_RULES.md`) are
copied per project by `dtb:project-init` and never drift-checked. `dtb:project-init` writes
its CLAUDE.md block in target projects between `<!-- BEGIN dtb -->…<!-- END dtb -->` sentinel
markers (idempotent updates, user text untouched).

## DTB Skill System

The `/dtb:*` skills form a German-language workflow system for managing development sessions. Skills are the primary delivery format — they support YAML frontmatter with natural language triggers and are auto-detected by Claude Code.

### Skill Workflow Lifecycle

Skills are designed to work together in a session lifecycle:
1. **Start/Resume**: `workflow-resume` derives the active feature from artifacts (PLAN `## Progress`) and reads `WORKFLOW_STATUS.md` for context
2. **Work**: Use `feature-plan`, `debug-plan` for planning; `implement` drives the plan phase by phase (3x3 rhythm + phase-end ritual: checkbox flips are gated by checkpoint criteria, the commit SHA is written back as verification evidence); `impl-review` checks the result across three dimensions (plan drift, craft, rules)
3. **Save**: `workflow-checkpoint` writes a session log AND overwrites `WORKFLOW_STATUS.md` (status block generated from artifacts, context block manual)
4. **Next session**: `workflow-resume` picks up where the progress checkboxes left off — even without a checkpoint

**Derived State principle:** Feature status is never maintained manually — it is derived
from artifact existence and `## Progress` checkboxes in `features/<slug>/plan.md` (single source of truth).
Rules live in `dtb-project/project-rules/DERIVED_STATE_RULES.md`; all read-side skills
(`workflow-next`, `workflow-status`, `workflow-resume`, `backlog-status`) reference that file.
Status fields in BACKLOG.md/`spec.md` are derived displays synced by `workflow-checkpoint`.
On conflict the artifact wins and the mismatch is reported. `IMPL_STATUS_*.md` is abolished.

### Skill Categories

- **Session lifecycle**: `workflow-checkpoint`, `workflow-resume`, `workflow-status`, `workflow-next`, `session-summary` (read-only recap of active session / a given day / last 7 days)
- **Idea management**: `idea` (quick capture), `idea-review` (triage)
- **Feature workflow**: `feature-discover` (requirements gathering), `feature-plan` (with inbox integration), `impl-plan`, `plan-review`, `feature-start`, `implement` (drives the plan phase by phase, enforces the verification gate at each phase end)
- **Bug workflow**: `bug-report` (quick capture with severity), `debug-plan` (root-cause analysis + fix strategy)
- **Project setup**: `project-init`, `project-health`, `project-team`
- **Greenfield**: `opportunity-map` (Vorfeld: build/buy/complement/wait-Sichtung → `OPPORTUNITY-MAP.md`, Hand-off zu `greenfield-prd` bei „build"), `greenfield-prd` (Autor: PRD-Interview → `PRD-MVP.md`, oder Report-Modus), `greenfield-roadmap` (Autor: Stack-Besprechung → `TECH-STACK.md` + Lean-Interview → `ROADMAP.md` mit Change-IDs, oder Report-Modus)
- **Maintenance**: `archive` (move completed/discarded items to archive), `kit-sync` (install/update installed kit copies under `~/.claude/` via lock-based drift detection — see below)
- **Development**: `impl-review` (feature-end review across plan drift, craft, rules — the former rules-only review, now retired), `backlog-status`, `repo-sync`, `build-check` (stand-alone deploy-readiness check across all repos — not part of the feature loop), `commit-and-push` (guided routine commit+push; groups paths by their real git root via `rev-parse --show-toplevel`, not `config.repos` — monorepo/poly-repo/single safe; hard safety rules, never `--force`/`--no-verify`/`--amend`)
- **Knowledge management**: `docs-extract` (scan input/ folder, extract facts from documents into thematic MDs), `lesson` (capture a reusable lesson append-only into `project-rules/lessons.md`, read as a prior by impl-plan/debug-plan/plan-review/impl-review — replaces the dead `pitfalls.md` concept), `open-question` (active capture: appends a subject-matter question `- [ ] [Fach] {Frage}` §6-conform to the active feature's `## Offene Punkte` — Variante-c target routing + Variante-B confirm; the capture tool for the Fach-Frage convention #13, later read by the Fach-Agenda #25)
- **Documentation**: `pipeline-graph` (generate interactive HTML overview of entire skill pipeline from frontmatter)

### Agent Roles

Reusable agent definitions in `agents/` are referenced by skills (e.g. `dtb:plan-review`):
- `architekt.md` — Technical reviewer (feasibility, dependencies, risks)
- `pragmatiker.md` — Scope guardian (MVP cut, effort-value, prioritization)
- `senior-dev.md` — Implementation reviewer (time estimates, test strategy, code-level feasibility)

### Personas — not hosted here

The kit does **not** host personas. Personas (role definitions that work *with the human over an
event* — a pitch, a kick-off — as opposed to agent roles, which work *on a code artifact*) live in
the dedicated `oma-personas` repository. What the kit carries instead are **distillates**: e.g.
`dtb:impl-review` embeds the `principled` and `torvalds` reviewer lenses inline in its Craft
sub-agent prompt, as evaluation criteria without voice or persona identity.

### Commands

Slash-command definitions in `commands/` (`commands/dtb-<name>.md`) activate a workflow shortcut.
They use YAML frontmatter (`description`) and may pull files into context via `@`-references.
Currently the kit ships no command — the directory and the `commands/dtb-*.md` class-A pattern in
`dtb:kit-sync` remain in place, so a newly added command is distributed automatically.

### Output Locations (in target project)

- `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` — Session logs (appended per session)
- `dtb-project/project-workflows/WORKFLOW_STATUS.md` — Status dashboard (overwritten each update, max 60-80 lines)
- `dtb-project/project-workflows/features/<slug>/` — **Change-Folder-Modell:** one folder per change (kebab-case slug), fixed filenames inside — `discovery.md`, `spec.md`, `plan.md`, optional `bug.md`/`task.md`. Replaces the former flat `FEATURE_*.md`/`PLAN_*.md`/`DISCOVERY_*.md`/`BUG_*.md`/`TASK_*.md` files paired by name. Status is derived from files present in the folder + `## Progress` in `plan.md` (see `DERIVED_STATE_RULES.md`)
- `dtb-project/project-workflows/INBOX.md` — Idea inbox (managed by `dtb:idea` and `dtb:idea-review`); stays a flat per-project file (not a change folder)
- `dtb-project/project-workflows/archive/<slug>/` — Archived changes (whole folder moved via `git mv`, or filesystem move + backup in non-git projects), plus archive log
- `dtb-project/project-rules/` — Coding-Richtlinien pro Bereich/Technologie (generiert + manuell gepflegt)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — Zentrale Statusableitungs-Regeln (Kit-Bestandteil, von project-init verteilt; einzige versionierte Datei in project-rules/)
- `dtb-project/project-rules/lessons.md` — Append-only Lektionen-Sammlung (Laufzeit-Artefakt, angelegt von `dtb:lesson`; Prior für impl-plan/debug-plan/plan-review/impl-review; keine Coding-Rule)
- `dtb-project/project-rules/UI.md` — UI-/Design-Guideline (eine der Bereichs-Regeln, generiert von `dtb:generate-rules ui`; von `dtb:impl-review` als Review-Dimension geprüft). Bei etablierter Design-Sprache die maßgebliche Referenz; ihre Token-Assets liegen in `project-design/`
- `dtb-project/project-design/` — Importierbare Design-Assets (Design-Tokens als `*.css`/`*.json`, ggf. weitere), referenziert von `project-rules/UI.md`. Assets, kein Markdown-/Regel-Bucket; von `dtb:project-init` angelegt, leer wenn das Projekt keine geteilten Design-Assets hat
- `dtb-project/project-infrastructure/input/` — Drop-Zone für Infra-Dokumente (PDFs, Configs, Exports)
- `dtb-project/project-infrastructure/*.md` — Extrahierte Infra-Fakten (UPPER_SNAKE_CASE, generiert von `dtb:docs-extract`)
- `dtb-project/project-requirements/input/` — Drop-Zone für Anforderungs-Dokumente
- `dtb-project/project-strategy/input/` — Drop-Zone für Strategie-Dokumente
- `integrations/<vendor-name>/input/` — Drop-Zone für Vendor-/Integrations-Dokumente

## Conventions When Editing Skills

- Skill files are markdown with YAML frontmatter (`name`, `description`, `disable-model-invocation`, optional `argument-hint`, `allowed-tools`)
- Each skill lives in its own directory: `skills/dtb-<name>/SKILL.md`
- Templates use `[PLACEHOLDER]` syntax for values to be filled at runtime
- File paths in skills use forward slashes and are relative to the target project root
- Dates always use `YYYY-MM-DD` format, never relative terms
- WORKFLOW_STATUS.md: 1-line summaries with links only, no detail tables — details belong in session logs or test reports; status block is generated from artifacts (fixed template, placeholders only), context block is manual
- `plan.md` must contain a `## Progress` section (one checkbox per step N.M; flips are gated by the phase's checkpoint criteria, the commit SHA is written back at the phase-end commit as verification evidence) — format in `dtb-project/project-rules/DERIVED_STATE_RULES.md` §2
- Status is derived, never trusted from fields: read-side skills derive from artifacts and report conflicts (artifact wins)
- Spec size limits: `spec.md` and `plan.md` max 500 lines each (longer specs degrade AI processing quality)
- Pipeline metadata in frontmatter: `stage`, `after`, `next`, `consumes`, `produces`
- `workflow-status` reads pipeline frontmatter to auto-generate the flow visualization
- `dtb:impl-review` reads rules from `{config.paths.rules}/` as one of its three review dimensions
- Fach-Fragen fürs Meeting werden als `- [ ] [Fach] {Frage}` in `## Offene Punkte` erfasst (status-neutral — zählt NICHT für die Statusableitung) — Regel: `dtb-project/project-rules/DERIVED_STATE_RULES.md` §6
