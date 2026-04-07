# Claude Code Workflow Kit

> A collection of slash commands, frameworks, and templates that extend Claude Code
> with structured development workflows.

## What's Inside

- **Skills** (`/dtb:*`) — German-language workflow system for session management,
  project documentation, feature planning, idea capture, and code review
- **Agent Roles** — Reusable agent definitions (Architekt, Pragmatiker, Senior Dev) for structured reviews
- **Memory Framework** — Production-tested patterns for managing Claude Code's persistent
  memory (autonomy rules, pitfalls tracking, memory size management)
- **Project Settings** — Pre-configured permissions and plugin setup

## Installation

### Minimal (Skills + Agents)

```bash
# 1. Skills in dein Projekt kopieren
cp -r skills/* <dein-projekt>/.claude/skills/

# 2. Agenten-Rollen kopieren
cp -r agents/ <dein-projekt>/agents/

# 3. In deinem Projekt Claude Code starten und initialisieren
cd <dein-projekt>
# /dtb:project-init ausfuehren — befuellt workflow.config.yaml und legt dtb-project/ an
```

### Vollstaendig (mit Memory Framework + Settings)

```bash
# 1-2: Wie oben

# 3. Memory Framework Templates kopieren
cp frameworks/claude-code-memory-framework/templates/* <dein-projekt>/memory/

# 4. Settings uebernehmen (oder manuell in bestehende settings.json mergen)
cp settings.json <dein-projekt>/.claude/settings.json

# 5. Initialisieren
cd <dein-projekt>
# /dtb:project-init ausfuehren
```

### Nach der Installation

- Skills werden von Claude Code automatisch erkannt
- Aufruf per Slash-Command (`/dtb:idea`) oder natuerliche Sprache ("Session speichern")
- `/dtb:project-init` ist der erste Schritt — danach sind alle anderen Skills einsatzbereit

## Skills Overview

| Skill | Purpose |
|-------|---------|
| `/dtb:workflow-checkpoint` | Log session progress + update status dashboard |
| `/dtb:workflow-resume` | Resume after a break |
| `/dtb:idea` | Quick-capture an idea into the inbox |
| `/dtb:idea-review` | Review and triage open ideas |
| `/dtb:bug-report` | Capture bug report with severity and reproduction steps |
| `/dtb:debug-plan` | Root-cause analysis and fix strategy for an existing bug |
| `/dtb:feature-discover` | Analyze idea, scan codebase, gather requirements before spec writing |
| `/dtb:feature-plan` | Create structured feature specifications (with inbox integration) |
| `/dtb:feature-start` | Start a planned feature from the backlog |
| `/dtb:impl-plan` | Create implementation plan from feature spec |
| `/dtb:plan-review` | Structured review with Architekt, Pragmatiker + Senior Dev agents |
| `/dtb:build-check` | Build verification |
| `/dtb:code-review` | Review code changes against project-specific rules |
| `/dtb:generate-rules` | Generate coding rules/guidelines from codebase analysis |
| `/dtb:workflow-status` | Pipeline visualization and queue analysis |
| `/dtb:workflow-next` | Show next concrete action per active feature |
| `/dtb:backlog-status` | Backlog overview |
| `/dtb:archive` | Archive completed/discarded items from workflow files |
| `/dtb:repo-sync` | Repository synchronization |
| `/dtb:project-init` | Initialize DTB workflow in a project |
| `/dtb:project-health` | Project linting and consistency checks |
| `/dtb:project-team` | Team documentation |
| `/dtb:greenfield-prd` | Generate product requirements for new projects |
| `/dtb:greenfield-roadmap` | Create project roadmap for new projects |
| `/dtb:docs-extract` | Scan input/ folder, extract facts from PDFs/docs, create thematic MDs |
| `/dtb:pipeline-docs` | Generate interactive HTML overview of entire skill pipeline |

## Memory Framework

The included [Claude Code Memory Framework](frameworks/claude-code-memory-framework/)
provides templates for:

- **Autonomy Rules** — 4-level permission model (ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE)
- **Pitfalls File** — Institutional knowledge about non-obvious technical issues
- **Memory Management** — Keep MEMORY.md lean (<150 lines) with topic file pointers

## Project Structure

```
skills/                # Skill definitions (primary — auto-detected by Claude Code)
agents/                # Reusable agent role definitions
frameworks/            # Memory framework with templates
workflow.config.yaml   # Project-specific config (template — filled by /dtb:project-init)
settings.json          # Claude Code project settings
CLAUDE.md              # Project instructions for Claude Code
```

## Note

- Skills and documentation are in **German**; code and file names are in English
- Skills are markdown-based prompt templates with YAML frontmatter, not executable code
- Skills support natural language triggers (e.g. "Session speichern" activates `dtb:workflow-checkpoint`)
- Generated session data goes to `dtb-project/` (gitignored)

## License

MIT
