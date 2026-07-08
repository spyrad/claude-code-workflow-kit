# Claude Code Workflow Kit

> A collection of slash commands, frameworks, and templates that extend Claude Code
> with structured development workflows.

## What's Inside

- **Skills** (`/dtb:*`) — German-language workflow system for session management,
  project documentation, feature planning, idea capture, and code review
- **Agent Roles** — Reusable agent definitions (Architekt, Pragmatiker, Senior Dev) for structured reviews
- **Personas** — Reusable persona definitions (e.g. `dtb-stakeholder-pitch-coach`) that adopt a
  role to work *with the human over an event* rather than on a code artifact
- **Commands** — Slash-command definitions that activate personas or shortcuts (e.g. `/dtb-pitch-coach`)
- **Memory Framework** — Production-tested patterns for managing Claude Code's persistent
  memory (autonomy rules, pitfalls tracking, memory size management)
- **Project Settings** — Pre-configured permissions and plugin setup

## Installation

### Empfohlen: `/dtb:kit-sync install` (verwaltete Installation)

Das Kit installiert sich selbst und haelt sich aktuell — ueber eine Lock-Datei
(`~/.claude/dtb-lock.json`) mit Content-Hashes pro Artefakt (Drift-Erkennung
Repo ↔ installierte Kopie).

```bash
# 1. Bootstrap: den kit-sync-Skill einmalig manuell installieren
git clone https://github.com/spyrad/claude-code-workflow-kit.git
mkdir -p ~/.claude/skills/dtb-kit-sync
cp claude-code-workflow-kit/skills/dtb-kit-sync/SKILL.md ~/.claude/skills/dtb-kit-sync/

# 2. In Claude Code (beliebiges Verzeichnis):
#    /dtb:kit-sync install
#    → installiert Skills, Agents und Commands global nach ~/.claude/,
#      adoptiert vorhandene Kopien und erzeugt ~/.claude/dtb-lock.json

# 3. Pro Projekt initialisieren:
#    cd <dein-projekt>  →  /dtb:project-init
#    → Scaffolding, workflow.config.yaml, Regel-Datei, CLAUDE.md-Block (Sentinel-Marker)
```

**Updates spaeter:** `/dtb:kit-sync check` (Drift-Report) → `/dtb:kit-sync sync`
(kontrollierter Abgleich; lokal geaenderte Kopien werden nie stillschweigend
ueberschrieben). `/dtb:project-health` meldet Drift nebenbei als eigenen Check.

### Fallback: manuelle Kopie (ohne Lock/Drift-Erkennung)

```bash
# Global (von Claude Code in allen Projekten geladen)
cp -r skills/* ~/.claude/skills/
cp -r agents/* ~/.claude/agents/
cp -r commands/* ~/.claude/commands/

# Optional: Memory Framework Templates + Settings ins Zielprojekt
cp frameworks/claude-code-memory-framework/templates/* <dein-projekt>/memory/
cp settings.json <dein-projekt>/.claude/settings.json

# Pro Projekt initialisieren (verteilt auch die Statusableitungs-Regeln)
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
| `/dtb:session-summary` | Compact recap of work done (active session, a given day, or last 7 days) |
| `/dtb:backlog-status` | Backlog overview |
| `/dtb:archive` | Archive completed/discarded items from workflow files |
| `/dtb:repo-sync` | Git status across configured project repos (not kit distribution) |
| `/dtb:kit-sync` | Install/update kit copies under `~/.claude/` with lock-based drift detection |
| `/dtb:project-init` | Initialize DTB workflow in a project |
| `/dtb:project-health` | Project linting and consistency checks |
| `/dtb:project-team` | Team documentation |
| `/dtb:greenfield-prd` | Generate product requirements for new projects |
| `/dtb:greenfield-roadmap` | Create project roadmap for new projects |
| `/dtb:docs-extract` | Scan input/ folder, extract facts from PDFs/docs, create thematic MDs |
| `/dtb:pipeline-graph` | Generate interactive HTML overview of entire skill pipeline |

## Memory Framework

The included [Claude Code Memory Framework](frameworks/claude-code-memory-framework/)
provides templates for:

- **Autonomy Rules** — 4-level permission model (ALLOWED / REQUIRES APPROVAL / NEVER / ESCALATE)
- **Pitfalls File** — Institutional knowledge about non-obvious technical issues
- **Memory Management** — Keep MEMORY.md lean (<150 lines) with topic file pointers

## Personas & Commands

**Personas** (`personas/`) are role definitions Claude adopts to work *with the human over an
event* (a pitch, a kick-off), as opposed to **agent roles** (`agents/`), which work *on a code
artifact* (a review). Each persona lives in its own directory with a `COGNITIVE.md` (core
thinking, voice, filters, risks) and a `README.md` (when to use, activation examples).

| Persona | Purpose |
|---------|---------|
| `dtb-stakeholder-pitch-coach` | Coaching for business-stakeholder pitches with a commitment goal (pilot, beta, budget). Coach-only — delivers structure and talking points, never read-aloud scripts. |

**Commands** (`commands/`) are slash-command definitions that activate a persona or workflow
shortcut. They use `@`-references to pull persona files into context.

| Command | Activates |
|---------|-----------|
| `/dtb-pitch-coach` | `dtb-stakeholder-pitch-coach` persona (coach-only) |

Install by copying into the target project's `.claude/` directory:

```bash
cp -r personas/ <dein-projekt>/.claude/personas/
cp -r commands/* <dein-projekt>/.claude/commands/
```

## Project Structure

```
skills/                # Skill definitions (primary — auto-detected by Claude Code)
agents/                # Reusable agent role definitions (work on code artifacts)
personas/              # Reusable persona definitions (work with the human over an event)
commands/              # Slash-command definitions (activate personas / shortcuts)
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
- **Derived State:** feature status is derived from artifacts (`## Progress` checkboxes in
  `PLAN_*.md`), not maintained in status fields — rules in
  `dtb-project/project-rules/DERIVED_STATE_RULES.md`

## License

MIT
