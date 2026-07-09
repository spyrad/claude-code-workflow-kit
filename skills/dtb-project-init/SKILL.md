---
name: dtb:project-init
description: >-
  Use when: "Projekt initialisieren", "project init", "DTB einrichten",
  "workflow.config.yaml erstellen". One-time project initialization that
  creates workflow.config.yaml and the directory structure.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
pipeline:
  stage: setup
  after: null
  next: [dtb:generate-rules, dtb:project-team, dtb:workflow-resume]
  consumes: []
  produces: [workflow.config.yaml, CLAUDE.md, WORKFLOW_STATUS.md, BACKLOG.md, project-rules/DERIVED_STATE_RULES.md]
---

# DTB Projekt-Initialisierung

Du fuehrst die einmalige Projekt-Initialisierung durch. Ziel: Die Datei `workflow.config.yaml` im Projekt-Root erstellen und die Verzeichnisstruktur anlegen.

---

## Schritt 0: Pruefen

Lies `workflow.config.yaml` im Projekt-Root.

- Falls die Datei **bereits existiert und ausgefuellt** ist: Zeige den aktuellen Inhalt und frage ob ein Update gewuenscht ist.
- Falls die Datei **nicht existiert**: Fahre mit Schritt 1 fort.

**Kit-Installation pruefen (Ebenen-Trennung):** project-init arbeitet auf der
**Projekt-Ebene** und kopiert KEINE globalen Kit-Dateien (Skills, Agents, Commands) —
das ist Sache von `/dtb:kit-sync` (Maschinen-Ebene, einmal pro Rechner).

```bash
ls "$HOME/.claude/dtb-lock.json" 2>/dev/null
```

- Lock fehlt → Hinweis (kein Abbruch): `Kit ist ohne Lock installiert. Empfehlung:
  einmalig /dtb:kit-sync install ausfuehren (adoptiert den vorhandenen Bestand).`
- Lock vorhanden → weiter ohne Meldung. Kein Netzwerk-Check hier — Drift prueft
  `/dtb:kit-sync check` bzw. `/dtb:project-health`.

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
  rules: "dtb-project/project-rules"

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
├── project-rules/
├── project-workflows/
│   └── features/
├── project-strategy/
│   └── input/
├── project-testing/
├── project-infrastructure/
│   └── input/
├── project-requirements/
│   └── input/
└── integrations/
    └── vendor-x/
        └── input/
```

Lege in jedem `input/`-Ordner eine `.gitkeep`-Datei an damit die Verzeichnisse im Git versioniert werden.

Lege in `integrations/vendor-x/input/` zusaetzlich eine `README.md` an:

```markdown
# Integrations

Dieses Verzeichnis enthaelt Dokumente zu externen Integrationen und Vendor-APIs.

## Struktur

Fuer jede Integration einen eigenen Unterordner anlegen:

```
integrations/
└── <vendor-name>/
    └── input/    ← Rohdokumente (PDFs, Specs, Exports)
```

Verzeichnis `vendor-x/` umbenennen oder als Vorlage nutzen.
```

### CLAUDE.md mit Sentinel-Markern

Der DTB-Abschnitt in der Ziel-CLAUDE.md steht zwischen **Sentinel-Markern** —
nur dieser Block gehoert dem Kit und darf bei spaeteren project-init-Laeufen oder
Kit-Updates ersetzt werden. Alles ausserhalb der Marker ist Nutzertext und wird
NIEMALS angefasst.

**Update-Logik (idempotent):**
1. CLAUDE.md existiert nicht → komplett aus dem Template unten erstellen
2. CLAUDE.md existiert MIT Markern → NUR den Inhalt zwischen
   `<!-- BEGIN dtb -->` und `<!-- END dtb -->` durch den aktuellen DTB-Block ersetzen
3. CLAUDE.md existiert OHNE Marker → DTB-Block (inkl. Marker) ans Dateiende anhaengen;
   falls ein alter unmarkierter DTB-/Workflow-Abschnitt erkennbar ist: einmalige
   Migration anbieten (alten Abschnitt entfernen, markierten Block uebernehmen) —
   nur mit Bestaetigung

**CLAUDE.md (Template fuer Neuanlage):**
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

<!-- BEGIN dtb -->
## DTB Workflow

Dieses Projekt nutzt das DTB-Workflow-Kit (`workflow.config.yaml` ist die Config).

- **Session-Lifecycle:** `/dtb:workflow-resume` (Start), `/dtb:workflow-checkpoint` (Ende)
- **Artefakte:** `{paths.workflows}/features/<slug>/` (ein Ordner pro Change mit fixen
  Dateinamen `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md`),
  `{paths.workflows}/BACKLOG.md`, `{paths.changelog}/`
- **Derived State:** Status wird aus Artefakten abgeleitet (`## Progress`-Checkboxen
  in `plan.md`), nie manuell gepflegt — Regeln: `{paths.rules}/DERIVED_STATE_RULES.md`
- **Naechster Schritt unklar?** `/dtb:workflow-next`
<!-- END dtb -->
```

Der Block zwischen den Markern ist der **DTB-Block** — beim Anhaengen an bestehende
CLAUDE.md (Fall 3) nur diesen Block inkl. Marker verwenden, `{paths.*}` aus der
workflow.config.yaml einsetzen.

Erstelle eine leere `WORKFLOW_STATUS.md` und `BACKLOG.md` falls sie nicht existieren.

**Regel-Datei verteilen (Seed):** Kopiere `DERIVED_STATE_RULES.md` (zentrale Statusableitungs-Regeln,
Quelle: Kit-Repo `dtb-project/project-rules/DERIVED_STATE_RULES.md`) nach
`{config.paths.rules}/DERIVED_STATE_RULES.md` im Zielprojekt — die Lese-Skills
(workflow-next/-status/-resume, backlog-status) und workflow-checkpoint referenzieren sie.
Die Datei ist ein **Seed** (Klasse B im Sinne von `dtb:kit-sync`): projektlokal,
nicht vom globalen Drift-Check erfasst.

**WORKFLOW_STATUS.md:**
```markdown
# Workflow-Status: {project_name}

**Letztes Update:** [YYYY-MM-DD]
**Letzter Session-Log:** -

---

## Status (generiert aus Artefakten — nicht manuell editieren)

Kein aktives Feature.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | Projekt initialisiert — erstes Feature planen |

---

## Session-Resume

Fuer neue Session: `/dtb:workflow-resume`
```

**BACKLOG.md:**
```markdown
# Feature Backlog

**Letzte Aktualisierung:** [YYYY-MM-DD]

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

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
- /dtb:pipeline-graph — Pipeline-Uebersicht als HTML generieren
```

---

## Richtlinien

- **Einmalig**: Dieser Command wird pro Projekt nur einmal ausgefuehrt
- **Automatisch erkennen**: So viel wie moeglich aus dem Repository ableiten
- **Gebuendelt fragen**: Alle Fragen in einem Block, nicht einzeln
- **Deutsch**: Alle Texte auf Deutsch
- **workflow.config.yaml ist Single Source of Truth**: Alle Commands lesen von dort
