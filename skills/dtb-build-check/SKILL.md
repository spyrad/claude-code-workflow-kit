---
name: dtb:build-check
description: >-
  Use when: "deploy ready", "deploy check", "alle Repos pruefen",
  "Release-Check", "Build check". Stand-alone multi-repo deploy-readiness
  check (tests + builds across all configured repos) run before a
  deploy/release — NOT part of the per-feature loop (phase verification
  lives in dtb:implement).
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [workflow.config.yaml]
  produces: []
---

# DTB Build-Check (Deploy-Readiness)

Stand-alone Sammel-Check ueber alle konfigurierten Repos — **vor Deploy/Release**, auf Zuruf.
Er ist bewusst NICHT Teil des Feature-Loops: Die Verifikation je Phase leistet das
Phasen-Ende-Ritual von `dtb:implement` (Verifikations-Gate, §2). Dieser Skill beantwortet
die andere Frage: „Sind ALLE Repos zusammen gerade deploy-faehig?"

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

> **Hinweis (frueherer Event-Konsistenz-Check):** Der FastWS-spezifische Backend↔Frontend-
> Event-Abgleich ist kein Kit-Bestandteil mehr — er war projektspezifisch (pkp). Wer ihn
> braucht, verankert ihn als Projekt-Rule (`project-rules/`), z.B. als Checkliste
> „Events Backend↔Frontend abgleichen vor Deploy".

### Schritt 3: Report

```markdown
# Build-Check Report
**Datum:** {DD.MM.YYYY HH:MM}

## Ergebnis-Uebersicht

| Repo | Check | Status | Details |
|------|-------|--------|---------|
| {repo.name} | Tests | {PASS/FAIL/SKIP} | {Details} |
| {repo.name} | Build | {PASS/FAIL/SKIP} | {Details} |

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

- `/dtb:implement` - Verifikation je Phase (Feature-Loop — dort, nicht hier)
- `/dtb:repo-sync` - Git-Status aller Repos
- `/dtb:workflow-checkpoint` - Session-Ende
- `/dtb:workflow-status` - Pipeline-Status

---

Fuehre jetzt den Deploy-Readiness-Check durch und erstelle den Report.
