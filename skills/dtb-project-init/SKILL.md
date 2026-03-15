---
name: dtb:project-init
description: >-
  Use when: "Projekt initialisieren", "project init", "DTB einrichten",
  "workflow.config.yaml erstellen". One-time project initialization that
  creates workflow.config.yaml and the directory structure.
disable-model-invocation: true
---

# DTB Projekt-Initialisierung

Du fuehrst die einmalige Projekt-Initialisierung durch. Ziel: Die Datei `workflow.config.yaml` im Projekt-Root erstellen und die Verzeichnisstruktur anlegen.

---

## Schritt 0: Pruefen

Lies `workflow.config.yaml` im Projekt-Root.

- Falls die Datei **bereits existiert und ausgefuellt** ist: Zeige den aktuellen Inhalt und frage ob ein Update gewuenscht ist.
- Falls die Datei **nicht existiert**: Fahre mit Schritt 1 fort.

---

## Schritt 1: Informationen sammeln

Sammle zuerst automatisch was du kannst:

```bash
# Repository-Infos
git remote -v 2>/dev/null
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml Makefile docker-compose.yml 2>/dev/null
```

Lies vorhandene Konfig-Dateien (package.json, pyproject.toml, etc.) um Tech-Stack abzuleiten.

Pruefe ob es ein Mono-Repo mit mehreren Unterprojekten ist:
```bash
ls -d */ 2>/dev/null
```

---

## Schritt 2: Interview

Stelle die folgenden Fragen **gebuendelt in einem Block** — nicht einzeln nacheinander. Zeige dabei was du bereits automatisch erkannt hast, damit der Nutzer nur ergaenzen/korrigieren muss.

```
Projekt-Initialisierung — bitte ergaenze/korrigiere:

1. Projektname: [erkannt oder leer]
2. Namespace (fuer Commands/Pfade): [abgeleitet oder leer]
3. Repos (erkannt):
   - [Repo 1]: Pfad, Typ (python/typescript/go/...), Test-Command, Build-Command
   - [Repo 2]: ...
   (oder "single repo" falls kein Mono-Repo)
4. Sonstiges: [Besonderheiten]
```

---

## Schritt 3: workflow.config.yaml schreiben

Erstelle `workflow.config.yaml` im Projekt-Root mit folgendem Format:

```yaml
project_name: "[Projektname]"
namespace: "[namespace]"

paths:
  workflows: "dtb-project/project-workflows"
  changelog: "dtb-project/project-changelog"

repos:
  - name: "[Repo-Name]"
    path: "[relativer-pfad]"
    type: "[python|typescript|go|rust|...]"
    test_command: "[test command oder null]"
    build_command: "[build command oder null]"
```

**Regeln:**
- `project_name`: Wie der Nutzer es angibt
- `namespace`: Kurzform, lowercase, fuer Pfade und Commands (z.B. "dtb", "myapp")
- `paths`: Immer relativ zum Projekt-Root, Standard ist `dtb-project/project-workflows` und `dtb-project/project-changelog`
- `repos`: Pro Unterprojekt/Repo ein Eintrag. Bei Single-Repo nur ein Eintrag mit `path: "."`
- `test_command` / `build_command`: Konkrete Shell-Commands oder `null` falls nicht vorhanden

---

## Schritt 4: Verzeichnisstruktur anlegen

Erstelle fehlende Verzeichnisse:

```
dtb-project/
├── project-changelog/
├── project-workflows/
│   └── features/
├── project-strategy/
└── project-testing/
```

Erstelle eine `CLAUDE.md` im Projekt-Root falls sie nicht existiert:

**CLAUDE.md:**
```markdown
# CLAUDE.md

<!--
CLAUDE.md Pflege-Richtlinien:
- Diese Datei wird in JEDE Conversation geladen — schlank halten (<150 Zeilen)
- Bei architekturrelevanten Aenderungen (neue Routes, Schemas, Patterns, Configs)
  die betroffene CLAUDE.md im gleichen Commit mitaktualisieren
- Details gehoeren in Sub-CLAUDE.md (pro Repo), nicht hier
- Keine Redundanz: Root verweist auf Sub-CLAUDE.md, dupliziert keine Inhalte
- Sub-CLAUDE.md werden nur geladen wenn im jeweiligen Verzeichnis gearbeitet wird
-->

## Project Context

[1-2 Saetze: Was ist das Projekt?]

## Repository Structure

[Ordner-Baum mit 1-Wort-Beschreibungen]

## Development Commands

[Start, Test, Build Commands pro Repo]

## Architecture Overview

[1-2 Saetze pro Architektur-Aspekt, Verweis auf Sub-CLAUDE.md fuer Details]

## Important Gotchas

[Projekt-spezifische Fallstricke]

## Quick Reference

[Entry Points, kritische Dateien]
```

Erstelle eine leere `WORKFLOW_STATUS.md` und `BACKLOG.md` falls sie nicht existieren:

**WORKFLOW_STATUS.md:**
```markdown
# Workflow-Status: {project_name}

**Letztes Update:** [YYYY-MM-DD]
**Letzter Session-Log:** -

---

## Aktueller Stand

| Kennzahl | Wert |
|----------|------|
| **Laufende Arbeit** | Projekt initialisiert |
| **Naechster Schritt** | Erstes Feature planen |
| **Blocker** | Keine |

---

## Session-Resume

Fuer neue Session: `/dtb:workflow-resume`
```

**BACKLOG.md:**
```markdown
# Feature Backlog

**Letzte Aktualisierung:** [YYYY-MM-DD]

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
```

---

## Schritt 5: Bestaetigung

```
Projekt initialisiert:

Projekt: {project_name}
Config: workflow.config.yaml
Repos: {Anzahl} ({Namen})

Naechste Schritte:
- /dtb:workflow-resume — Workflow starten
- /dtb:feature-plan — Erstes Feature planen
```

---

## Richtlinien

- **Einmalig**: Dieser Command wird pro Projekt nur einmal ausgefuehrt
- **Automatisch erkennen**: So viel wie moeglich aus dem Repository ableiten
- **Gebuendelt fragen**: Alle Fragen in einem Block, nicht einzeln
- **Deutsch**: Alle Texte auf Deutsch
- **workflow.config.yaml ist Single Source of Truth**: Alle Commands lesen von dort
