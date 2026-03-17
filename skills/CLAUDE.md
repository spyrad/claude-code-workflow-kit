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
  consumes: [ARTIFACT_*.md]   # artifacts read by this skill
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
| `consumes` | list | Artifact patterns this skill reads (e.g. `FEATURE_*.md`, `INBOX.md`) |
| `produces` | list | Artifact patterns this skill writes (e.g. `PLAN_*.md`) |

## Directory & naming conventions

- Each skill lives in `skills/dtb-<name>/SKILL.md`
- Directory names: kebab-case, lowercase
- Template placeholders: `[PLACEHOLDER]` syntax
- File paths: forward slashes, relative to target project root
- Dates: `YYYY-MM-DD`, never relative terms

## Language

- **Frontmatter keys**: English
- **Skill body** (instructions, templates, output): German
- **description field**: German trigger phrases + English summary sentence
