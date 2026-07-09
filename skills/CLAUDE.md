# Skills — Contributor Guide

## Frontmatter (Pflichtfelder)

Every skill file must have YAML frontmatter with these fields:

```yaml
---
name: dtb:<skill-name>
description: >-
  Use when: "<trigger phrases>". <English summary of what the skill does>.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash   # subset as needed
pipeline:
  stage: idea | planning | implementation | development | session | monitoring | setup | greenfield
  after: dtb:<predecessor>    # or null
  next: dtb:<successor>       # or null
  consumes: [ARTIFACT_*.md]   # artifacts read by this skill (FEATURE_*, PLAN_*, BUG_*, etc.)
  produces: [ARTIFACT_*.md]   # artifacts written by this skill
---
```

### Field details

- **name**: `dtb:<kebab-case-name>` — must match directory name without `dtb-` prefix
- **description**: starts with `Use when:` trigger phrases (German), ends with English summary
- **disable-model-invocation**: `true` unless the skill should be auto-triggered by the model
- **allowed-tools**: comma-separated list of tools the skill is permitted to use
- **pipeline**: declares where the skill sits in the workflow pipeline (see below)

### Pipeline block

| Field | Type | Description |
|-------|------|-------------|
| `stage` | enum | Workflow phase: `idea`, `planning`, `implementation`, `development`, `session`, `monitoring`, `setup`, `greenfield` |
| `after` | string/null | Predecessor skill (`dtb:<name>`) or `null` if entry point |
| `next` | string/null | Successor skill (`dtb:<name>`) or `null` if terminal |
| `consumes` | list | Artifact patterns this skill reads (e.g. `features/*/spec.md`, `INBOX.md`) |
| `produces` | list | Artifact patterns this skill writes (e.g. `features/*/plan.md`) |

### Artifact status values (Derived State)

Status is **derived from artifacts**, not maintained in fields — rules in
`dtb-project/project-rules/DERIVED_STATE_RULES.md` (single source; read-side skills must
reference it instead of implementing their own logic). Status fields/columns are derived
displays synced by `dtb:workflow-checkpoint`. `IMPL_STATUS_*.md` is abolished.

Changes live in `features/<slug>/` folders (kebab-case slug, fixed filenames). Status derives from
which files are present + `plan.md` `## Progress` (see `DERIVED_STATE_RULES.md`).

| File in `features/<slug>/` | Status values (derivation source) |
|----------------------------|-----------------------------------|
| `spec.md` | Derived: Spezifiziert, Geplant, In Arbeit, Fertig zum Testen (from `plan.md` `## Progress` checkboxes). Explicit only: Abgenommen, Abgeschlossen, Pausiert |
| `plan.md` | Entwurf, Reviewed (first 10 lines); progress via mandatory `## Progress` section (one checkbox per step N.M, commit SHA as evidence) |
| `bug.md` | Derived from `## Fix-Schritte` checklist: Offen, Analysiert, In Arbeit, Behoben |
| `task.md` | Derived from `## Schritte` checklist: Offen, In Arbeit, Erledigt |
| `INBOX.md` entries | Offen, In Arbeit, Ausgearbeitet, Verworfen (maintained by idea skills) |

## Directory & naming conventions

- Each skill lives in `skills/dtb-<name>/SKILL.md`
- Directory names: kebab-case, lowercase
- Template placeholders: `[PLACEHOLDER]` syntax
- File paths: forward slashes, relative to target project root
- Dates: `YYYY-MM-DD`, never relative terms
- `project-rules/` files use UPPER_SNAKE_CASE (e.g. `FRONTEND.md`, `BACKEND.md`)
- **Change folders:** `features/<slug>/` with kebab-case slug (derived from the feature name, no running numbers) and fixed filenames `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md` — slug rules in `DERIVED_STATE_RULES.md` §4

## Distribution (kit-sync)

Skills are distributed to `~/.claude/skills/` by `dtb:kit-sync` (modes: check/sync/install).
A lock file `~/.claude/dtb-lock.json` records source, ref, and a content hash per artifact
(three-point drift detection: repo ↔ lock ↔ installed copy; hashing normalizes line endings).

- **Class A (`mode: synced`, drift-checked):** `skills/dtb-*/SKILL.md`, `agents/*.md`,
  `commands/dtb-*.md` — a NEW skill is covered automatically by the pattern, no registration needed
- **Class B (`mode: seed`, copied once, never drift-checked):** `frameworks/` templates,
  `settings.json`, `DERIVED_STATE_RULES.md` (distributed per project by `dtb:project-init`)
- Not distributed in v1: `personas/` (source cleanup pending, see INBOX #8)

Lock schema and fixed command sequences live in `skills/dtb-kit-sync/SKILL.md` — do not
duplicate that logic in other skills; reference it (like `dtb:project-health` check 11 does).

## Language

- **Frontmatter keys**: English
- **Skill body** (instructions, templates, output): German
- **description field**: German trigger phrases + English summary sentence
