---
name: dtb:backlog-status
description: >-
  Use when: "Backlog zeigen", "backlog status", "offene Features",
  "was steht an". Read-only overview of open features, priorities,
  and current progress from BACKLOG.md and FEATURE_*.md files.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [BACKLOG.md, FEATURE_*.md, PLAN_*.md, BUG_*.md]
  produces: []
---

# DTB Backlog-Status

Schneller Read-Only-Ueberblick ueber offene Features, Prioritaeten und aktuellen Fortschritt.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Backlog laden

Lies die Datei:
- **`{config.paths.workflows}/BACKLOG.md`**

## Schritt 2: Feature-Specs und Plaene scannen

Finde alle `FEATURE_*.md` und `BUG_*.md` Dateien in `{config.paths.workflows}/features/` und lies jeweils die ersten 20 Zeilen (Titel, Status, Zusammenfassung).

Pruefe fuer jedes Feature ob eine zugehoerige `PLAN_*.md` existiert (gleicher Name).
Pruefe fuer jeden Bug ob ein Analyse-Abschnitt vorhanden ist (Status `Analysiert` oder `Behoben`).

## Schritt 3: Abgleich

Vergleiche die gefundenen `FEATURE_*.md` und `BUG_*.md` Dateien mit den Eintraegen in BACKLOG.md:
- Markiere Features/Bugs die in BACKLOG.md **fehlen** (Datei existiert aber kein Backlog-Eintrag)
- Markiere Features/Bugs deren Status in BACKLOG.md **veraltet** sein koennte

## Schritt 4: Backlog-Report erstellen

Erstelle einen kompakten Report:

```markdown
# Backlog-Status
**Datum:** {DD.MM.YYYY}

## Aktiv (in Arbeit)
| Feature | Status | Prio | Plan | Datei | Ziel |
|---------|--------|------|------|-------|------|
| {Feature} | {Status} | {Prio} | ✅/❌ | {Datei} | {Ziel} |

## Geplant (priorisiert)
| Feature | Status | Prio | Plan | Datei | Ziel |
|---------|--------|------|------|-------|------|
| {Feature} | Geplant | {Prio} | ✅/❌ | {Datei} | {Ziel} |

## Ideen / Backlog
- {Feature}: {Einzeiler-Beschreibung}

## Fertig zum Testen / Abgenommen
| Feature | Status | Datei |
|---------|--------|-------|
| {Feature} | {Status} | {Datei} |

## Abgeschlossen (letzte 5)
| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
| {Feature} | {Datum} | {Datei} |

---

## Offene Bugs
| Bug | Severity | Status | Analyse | Datei |
|-----|----------|--------|---------|-------|
| {Bug-Name} | {Severity} | {Status} | ✅/❌ | {Datei} |

## Nicht im Backlog (FEATURE_*.md / BUG_*.md ohne Eintrag)
| Datei | Titel | Status |
|-------|-------|--------|
| {Datei} | {Titel} | {Status} |

> Diese Features/Bugs haben eine Datei, sind aber nicht in BACKLOG.md eingetragen.
> Trage sie manuell ein oder nutze `/dtb:feature-plan` bzw. `/dtb:bug-report`.

---

## Empfehlung
{Was sollte als naechstes angegangen werden und warum?}
```

## Richtlinien

- **Read-Only**: Dieser Command aendert keine Dateien
- **Kompakt**: Uebersicht, nicht Detail — Details stehen in den FEATURE_*.md Dateien
- **Priorisiert**: Wichtigstes zuerst
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Klare Empfehlung am Ende

## Verwendung

Nutze diesen Command:
- Am Session-Start fuer Orientierung
- Bei Planungsentscheidungen
- Fuer Stakeholder-Updates
- Wenn unklar ist was als naechstes kommt

## Verwandte Commands

- `/dtb:workflow-resume` - Session-Start mit vollem Kontext
- `/dtb:feature-plan` - Neues Feature planen (mit Backlog-Eintrag)
- `/dtb:workflow-checkpoint` - Session dokumentieren (mit Feature-Status-Update)
- `/dtb:workflow-status` - Pipeline-Visualisierung (alle Workflow-Stufen)

---

Scanne jetzt die Workflow-Dateien und erstelle den Backlog-Status.
