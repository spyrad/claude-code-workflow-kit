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
  produces: [workflow.config.yaml, CLAUDE.md, WORKFLOW_STATUS.md, BACKLOG.md, project-rules/DERIVED_STATE_RULES.md, .claude/settings.json]
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
├── project-design/
├── project-infrastructure/
│   └── input/
├── project-requirements/
│   └── input/
└── integrations/
    └── vendor-x/
        └── input/
```

**Zusaetzlich auf Projektwurzel-Ebene** (NICHT unter `dtb-project/`):

```
.claude/          ← Ziel des settings.json-Seeds (Schritt 4, Abschnitt „Seeds verteilen")
```

```bash
mkdir -p .claude
```

Lege eine `.gitkeep`-Datei an in **jedem `input/`-Ordner** sowie in `project-changelog/`,
`project-testing/` und `project-workflows/features/` — diese drei bleiben nach der
Initialisierung leer und waeren in Git sonst unversioniert. (`project-design/` bekommt
stattdessen eine README, s.u.; `.claude/` erhaelt mit `settings.json` sofort Inhalt.)

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

Lege in `project-design/` eine `README.md` an (hält das leere Verzeichnis im Git und erklaert die Konvention):

```markdown
# Project Design

Importierbare Design-Assets dieses Projekts — z.B. Design-Tokens (`*.css`, `*.json`),
die der Frontend-Code importiert.

## Konvention

- Die **Design-Guideline** (visuelle Sprache, Regeln, Do's/Don'ts) lebt als
  `project-rules/UI.md` — dort prueft `dtb:impl-review` sie gegen die Umsetzung.
- **Hier** liegen die zugehoerigen **Assets** (Tokens etc.), die `UI.md` referenziert.
  Assets, keine Regeln — daher eigener Bucket, nicht `project-rules/`.

Leer lassen, falls das Projekt keine geteilten Design-Assets hat.
```

### CLAUDE.md mit Sentinel-Markern

**Zielort:** `CLAUDE.md` im **Projekt-Root** (neben `workflow.config.yaml`) — dort erwartet
Claude Code die Projekt-Anweisungen.

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

**Status-Dateien anlegen:** Erstelle `{config.paths.workflows}/WORKFLOW_STATUS.md` und
`{config.paths.workflows}/BACKLOG.md` mit den Vorlagen weiter unten, falls sie nicht existieren.
**Nicht** in den Projekt-Root schreiben — dort liegen nur `workflow.config.yaml` (Schritt 3)
und `CLAUDE.md`. Verzeichnis vorher sicherstellen:

```bash
mkdir -p "{config.paths.workflows}"   # konkreten Pfad aus der Config einsetzen
```

Genau dort erwarten sie alle Lese-Skills (`workflow-resume`, `workflow-next`, `workflow-status`,
`backlog-status`, `project-health`, `feature-start`, `archive`) und `workflow-checkpoint`. Eine
Kopie im Projekt-Root wird von keinem Skill gelesen und veraltet still.

### Seeds verteilen (Klasse B)

Klasse-B-Seeds sind projektlokal und werden **nicht** vom globalen Drift-Check erfasst;
`dtb:kit-sync` kopiert sie ausdrücklich NICHT (dort Abschnitt „Artefakt-Klassen": `settings.json`
als Klasse B „projektlokal (via project-init)", `DERIVED_STATE_RULES.md` als „Seed via
project-init") — sie sind Sache dieses Skills. **Alle** Seeds der Klasse verteilen, nicht nur den erstbesten:

| Seed | Quelle im Kit-Repo | Ziel im Projekt | Bei bereits vorhandener Datei |
|------|--------------------|-----------------|-------------------------------|
| `DERIVED_STATE_RULES.md` | `dtb-project/project-rules/DERIVED_STATE_RULES.md` | `{config.paths.rules}/DERIVED_STATE_RULES.md` | **überschreiben** — zentrale Regel, muss aktuell sein |
| `settings.json` | `settings.json` (Repo-Root) | `.claude/settings.json` | **NIE überschreiben** — trägt projekteigene permissions/hooks |

> ⚠ **Mechanisch kopieren, nie aus dem Gedächtnis rekonstruieren.** In einer Zielprojekt-Session
> ist das Kit-Repo nicht der cwd — ein relativer Pfad ist nicht auflösbar. Die Quelle deshalb
> **absolut** über `~/.claude/dtb-lock.json` → `localPath` bestimmen und per `cp` byte-genau kopieren.
> Wird die Quelle nicht gefunden, den betroffenen Seed **überspringen** (ehrliche Meldung), statt
> die Datei aus dem Gedächtnis nachzuschreiben (führt sonst zu einer veralteten Regel-Datei bzw.
> einer erfundenen Settings-Datei).

**Schritt A — Quelle einmal auflösen (gilt für beide Seeds):**

```bash
LOCK="$HOME/.claude/dtb-lock.json"
KIT="$(grep -o '"localPath"[[:space:]]*:[[:space:]]*"[^"]*"' "$LOCK" 2>/dev/null | sed -E 's/.*"localPath"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

if [ ! -f "$LOCK" ]; then
  echo "FEHLER: Kein Lock unter $LOCK — Kit-Quelle unbekannt."
  echo "        → einmalig /dtb:kit-sync install ausfuehren, danach project-init erneut."
  echo "        Beide Seeds werden uebersprungen (nichts erfinden)."
elif [ -z "$KIT" ]; then
  echo "FEHLER: Lock vorhanden, aber ohne 'localPath' — der Pfad zum Kit-Klon fehlt."
  echo "        → Kit-Repo-Pfad beim Nutzer erfragen und hier als KIT einsetzen,"
  echo "          oder localPath im Lock nachtragen. Beide Seeds bis dahin uebersprungen."
elif [ ! -d "$KIT" ]; then
  echo "FEHLER: localPath zeigt auf ein nicht vorhandenes Verzeichnis: $KIT"
  echo "        (typisch nach Rechnerwechsel — der Lock stammt von einer anderen Maschine)"
  echo "        → korrekten Pfad erfragen oder /dtb:kit-sync install erneut ausfuehren."
else
  echo "Seed-Quelle: $KIT"
fi
```

Nur wenn `$KIT` ein existierendes Verzeichnis ist, weiter mit B und C — sonst beide Seeds
überspringen und den Nutzer auf manuelles Kopieren hinweisen. Nie improvisieren.

**Schritt B — Seed 1: `DERIVED_STATE_RULES.md`** (die Lese-Skills workflow-next/-status/-resume,
backlog-status und workflow-checkpoint referenzieren sie):

```bash
SRC="$KIT/dtb-project/project-rules/DERIVED_STATE_RULES.md"
DST="{config.paths.rules}/DERIVED_STATE_RULES.md"   # konkreten Pfad aus der Config einsetzen

if [ -f "$SRC" ]; then
  mkdir -p "$(dirname "$DST")"
  cp "$SRC" "$DST"
  # Hash-Verifikation Quelle <-> Ziel
  if [ "$(git hash-object "$SRC")" = "$(git hash-object "$DST")" ]; then
    echo "Seed OK: DERIVED_STATE_RULES.md kopiert (hashgleich zur Kit-Quelle)."
  else
    echo "WARN: Seed kopiert, aber Hash weicht ab — Quelle/Ziel pruefen: $SRC"
  fi
else
  echo "FEHLER: Regel-Datei nicht gefunden. Erwartet: $SRC"
  echo "        → manuell aus dem Kit-Repo kopieren; NICHT aus dem Gedaechtnis erzeugen."
fi
```

**Schritt C — Seed 2: `settings.json`** → `.claude/settings.json` (Permissions inkl.
Deny-Liste für `.env`/`secrets/**`, aktivierte Plugins, `effortLevel`):

> ⚠ **Existierende Datei niemals überschreiben.** Anders als die Regel-Datei ist
> `.claude/settings.json` im Zielprojekt oft **schon vorhanden und projekteigen** (permissions,
> hooks, env). Ein `cp` darüber zerstört die Projekt-Konfiguration. Deshalb: nur anlegen, wenn
> sie fehlt — sonst melden und den Nutzer entscheiden lassen.

```bash
SRC="$KIT/settings.json"
DST=".claude/settings.json"

if [ ! -f "$SRC" ]; then
  echo "FEHLER: Settings-Seed nicht gefunden. Erwartet: $SRC"
elif [ -f "$DST" ]; then
  echo "UEBERSPRUNGEN: $DST existiert bereits — projekteigene Konfiguration bleibt unangetastet."
  echo "               Kit-Vorlage zum Vergleich: $SRC"
  diff "$SRC" "$DST" || true    # nur Anzeige; NICHT automatisch mergen
else
  mkdir -p .claude
  cp "$SRC" "$DST"
  if [ "$(git hash-object "$SRC")" = "$(git hash-object "$DST")" ]; then
    echo "Seed OK: settings.json kopiert (hashgleich zur Kit-Quelle)."
  else
    echo "WARN: Seed kopiert, aber Hash weicht ab — Quelle/Ziel pruefen: $SRC"
  fi
fi
```

Bei Unterschieden zu einer bestehenden Datei: den Diff zeigen und fragen, ob einzelne Blöcke
übernommen werden sollen — **nie automatisch mergen**. Der Seed ist ein Startpunkt, kein Zwang:
er aktiviert u.a. das `context7`-Plugin und setzt `effortLevel` — beides darf das Projekt
anders entscheiden.

**WORKFLOW_STATUS.md** → Zielpfad `{config.paths.workflows}/WORKFLOW_STATUS.md`:
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

**BACKLOG.md** → Zielpfad `{config.paths.workflows}/BACKLOG.md`:
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
