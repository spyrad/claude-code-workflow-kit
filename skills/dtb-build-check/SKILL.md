---
name: dtb:build-check
description: >-
  Use when: "Build check", "Tests laufen lassen", "Build pruefen",
  "deploy ready". Runs structured build/test checks across all
  configured repos and reports results.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: development
  after: [dtb:feature-start]
  next: [dtb:code-review]
  consumes: [workflow.config.yaml]
  produces: []
---

# DTB Build-Check

Strukturierter Build/Test-Check ueber alle konfigurierten Repos.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden. Erstelle eine Config mit repos-Eintraegen inkl. test_command/build_command.
```

### Schritt 2: Tests & Builds ausfuehren

Fuer jeden Eintrag in `config.repos`:

**Falls `repo.test_command` gesetzt:**
```bash
cd {repo.path} && {repo.test_command}
```
Erfasse: Anzahl Tests, Passed, Failed, Errors.

**Falls `repo.build_command` gesetzt:**
```bash
cd {repo.path} && {repo.build_command}
```
Erfasse: Fehler, Build-Erfolg, Bundle-Groesse.

### Schritt 3: Event-Konsistenz (optional)

Falls mehrere Repos mit type "python" + "typescript" vorhanden:
1. Lies alle Event-Namen aus Backend-Routes (Pattern: `@fastws.post("EVENT_*")`)
2. Lies alle Events aus Frontend Event-Liste
3. Vergleiche: Fehlende/Verwaiste Events?

### Schritt 4: Report

```markdown
# Build-Check Report
**Datum:** {DD.MM.YYYY HH:MM}

## Ergebnis-Uebersicht

| Repo | Check | Status | Details |
|------|-------|--------|---------|
| {repo.name} | Tests | {PASS/FAIL/SKIP} | {Details} |
| {repo.name} | Build | {PASS/FAIL/SKIP} | {Details} |
| Cross-Repo | Events | {PASS/WARN/SKIP} | {Details} |

## Gesamt-Status: {DEPLOY-READY / NICHT READY}

## Fehler-Details (falls vorhanden)

### {repo.name}
{Fehlermeldungen oder "Alle Checks bestanden"}

## Empfehlung
{Konkreter naechster Schritt}
```

## Richtlinien

- **Ausfuehren, nicht nur beschreiben**: Tests und Builds tatsaechlich laufen lassen
- **Fehler-Fokus**: Bei Erfolg kurz, bei Fehlern detailliert
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Bei Fehlern konkrete Fix-Empfehlungen

## Verwandte Commands

- `/dtb:repo-sync` - Git-Status aller Repos
- `/dtb:workflow-checkpoint` - Session-Ende
- `/dtb:workflow-status` - Pipeline-Status

---

Fuehre jetzt den Build-Check durch und erstelle den Report.
