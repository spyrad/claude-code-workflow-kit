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
  consumes: [features/*/spec.md]   # artifacts read by this skill (features/*/{spec,plan,bug,task}.md, etc.)
  produces: [features/*/plan.md]   # artifacts written by this skill
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

## Eligibility-Gates

A **schreibender Skill mit zwingender Eingabe** prüft am Eingang, ob sein kritisches Eingabe-Artefakt
existiert. Fehlt es, verweigert er konstruktiv statt auf falscher Basis weiterzuarbeiten, und verweist
auf den Skill, der das Artefakt erzeugt. Vorbild: die Test-zuerst-Weigerung von 10x-tdd.

### Einteilungsregel (welcher Skill bekommt ein Gate)

> Ein Skill bekommt ein **Hard-Gate**, wenn er eine **zwingende Eingabe** braucht (ohne die sein
> Output sinnlos/falsch wäre). Das Kriterium ist **NICHT** `produces` ≠ leer (mehrere Skills
> schreiben nur, ohne eigenes `produces`-Artefakt) und **NICHT** die Position in `consumes`
> (die Reihenfolge ist kein verlässlicher Indikator). Das kritische Artefakt wird **pro Skill
> explizit** benannt — nie positional aus `consumes` abgeleitet.

Read-only-Skills, Entry-Points (`consumes: []`) und Skills ohne zwingende Eingabe bekommen kein
Hard-Gate. Git-Gates (Git-Zustand statt Artefakt) und Soft-Gates (nur empfohlene Eingabe) sind
ein geplantes Folge-Feature — diese Konvention trägt sie bereits.

### Fit-Check + Redirect (Mechanik)

1. **Fit-Check:** existiert das explizit benannte kritische Artefakt am **slug-spezifischen Pfad**
   `features/{slug}/<artefakt>` (z.B. `features/{slug}/spec.md`)? **Nicht** den `*`-Wildcard
   (`features/*/spec.md`) prüfen — der träfe ein fremdes Feature und erzeugte ein False Negative.
   Ja → Skill läuft normal. Nein → Gate greift.
2. **Redirect-Ableitung** (fehlendes Artefakt → erzeugender Skill), Reihenfolge:
   1. **Selbst-Ausschluss:** den aktuellen Skill aus den Erzeugern streichen (viele Skills führen
      ein Artefakt in `produces`, weil sie es nur *aktualisieren*, nicht erstellen).
   2. **`after`-Match bevorzugen:** bleibt mehr als ein Erzeuger, den nennen, der im `after` des
      aktuellen Skills steht (der Pipeline-Vorgänger/Ersteller) — als empfohlenes Erstziel voran.
   3. **verbleibende nennen:** weitere Erzeuger als Alternative anhängen; ist keiner ableitbar →
      ehrliche Meldung ohne erfundenes Ziel (nie raten).
3. **Meldeblock:** kurzer Block (Muster wie `feature-discover` Schritt 1), der (a) das fehlende
   Artefakt + den **geprüften Pfad** ausgibt, (b) den/die Redirect-Befehl(e) nennt, (c) eine
   **Escape-Hatch** anbietet (bewusster Fortfahren-Weg gegen Fehlalarm — der Nutzer muss ihn
   explizit wählen, kein stilles Durchrutschen).
4. **Nicht-Git-Projekt:** ein späterer Git-Zustand-Check (Folge-Feature) wird still übersprungen.

### Verbindliche Hard-Gate-Zuordnung (v1)

Frontmatter-verifiziert 2026-07-10 (`produces`-Rückwärtssuche per Grep belegt):

| Skill | Kritisches Artefakt | Redirect (nach Selbst-Ausschluss + `after`-Match) |
|-------|---------------------|----------------------------------------------------|
| `impl-plan` | `features/*/spec.md` | `feature-plan` (`workflow-checkpoint` nur Status-Updater) |
| `plan-review` | `features/*/plan.md` | `impl-plan` voran, `feature-start` als Alternative |
| `feature-start` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss) |
| `debug-plan` | `features/*/bug.md` | `bug-report` (nach Selbst-Ausschluss; `debug-plan` nur Fix-Updater) |
| `archive` | archivierbare Kandidaten vorhanden | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu archivieren" (nativ in Schritt 3) |
| `migrate-change-folders` | flache Alt-Dateien (`features/*.md`) | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu migrieren" (nativ in Schritt 1) |

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
