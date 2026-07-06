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
  consumes: [BACKLOG.md, FEATURE_*.md, PLAN_*.md, BUG_*.md, TASK_*.md, project-rules/DERIVED_STATE_RULES.md]
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

Die Status-Spalte ist eine **abgeleitete Anzeige** — verwende sie NICHT als Quelle.
Manuell gepflegt (und damit verbindlich) sind nur Prio und Ziel.

## Schritt 2: Status ableiten

**Ableitungsregel:** verbindliche Regeln in `{config.paths.rules}/DERIVED_STATE_RULES.md`
(Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`). Lies diese Datei zuerst.

Finde alle `FEATURE_*.md`, `BUG_*.md` und `TASK_*.md` Dateien in `{config.paths.workflows}/features/`
und leite den Status pro Item ab:

- **Features:** FEATURE ohne PLAN → Spezifiziert; PLAN `Entwurf`/`Reviewed` + 0 Checkboxen → Geplant;
  `## Progress` teilweise abgehakt → In Arbeit (X/Y); vollstaendig → Fertig zum Testen
- **Bugs:** Analyse-Abschnitt + `## Fix-Schritte`-Checkliste zaehlen (Offen/Analysiert/In Arbeit/Behoben)
- **Tasks:** `## Schritte`-Checkliste zaehlen (Offen/In Arbeit/Erledigt)
- **Fallbacks (Regel-Datei §1.4):** PLAN ohne Progress → "Fortschritt unbekannt"; IMPL_STATUS_*.md
  ignorieren + Migrations-Hinweis; explizit `Pausiert` → als Pausiert zeigen (ueberschreibt Ableitung)

## Schritt 3: Abgleich

Vergleiche die gefundenen Dateien mit den Eintraegen in BACKLOG.md:
- Markiere Features/Bugs/Tasks die in BACKLOG.md **fehlen** (Datei existiert aber kein Backlog-Eintrag)
- **Konflikte melden (Regel-Datei §1.3):** Weicht die BACKLOG-Status-Spalte vom abgeleiteten
  Status ab, gewinnt das Artefakt — 1 Hinweiszeile pro Widerspruch im Report, Feld NICHT
  korrigieren (read-only)

## Schritt 4: Backlog-Report erstellen

Erstelle einen kompakten Report:

```markdown
# Backlog-Status
**Datum:** {DD.MM.YYYY}

## Aktiv (in Arbeit)
| Feature | Status (abgeleitet) | Prio | Fortschritt | Datei | Ziel |
|---------|---------------------|------|-------------|-------|------|
| {Feature} | {abgeleiteter Status} | {Prio} | {X/Y} | {Datei} | {Ziel} |

{Falls Konflikte: ⚠ {Item}: BACKLOG sagt "{Feld}", Artefakte zeigen "{abgeleitet}"}

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

## Offene Aufgaben
| Aufgabe | Prio | Status | Datei |
|---------|------|--------|-------|
| {Aufgaben-Name} | {Prio} | {Status} | {Datei} |

## Nicht im Backlog (FEATURE_*.md / BUG_*.md / TASK_*.md ohne Eintrag)
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
