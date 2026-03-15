---
name: dtb:backlog-status
description: >-
  Use when: "Backlog zeigen", "backlog status", "offene Features",
  "was steht an". Read-only overview of open features, priorities,
  and current progress from BACKLOG.md and FEATURE_*.md files.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# DTB Backlog-Status

Schneller Read-Only-Ueberblick ueber offene Features, Prioritaeten und aktuellen Fortschritt.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Backlog laden

Lies die Datei:
- **`{config.paths.workflows}/BACKLOG.md`**

## Schritt 2: Feature-Specs scannen

Finde alle `FEATURE_*.md` Dateien in `{config.paths.workflows}/features/` und lies jeweils die ersten 20 Zeilen (Titel, Status, Zusammenfassung).

## Schritt 3: Abgleich

Vergleiche die gefundenen `FEATURE_*.md` Dateien mit den Eintraegen in BACKLOG.md:
- Markiere Features die in BACKLOG.md **fehlen** (FEATURE_*.md existiert aber kein Backlog-Eintrag)
- Markiere Features deren Status in BACKLOG.md **veraltet** sein koennte (z.B. FEATURE_*.md sagt "Abgeschlossen" aber BACKLOG sagt "Geplant")

## Schritt 4: Backlog-Report erstellen

Erstelle einen kompakten Report:

```markdown
# Backlog-Status
**Datum:** {DD.MM.YYYY}

## Aktiv (in Arbeit)
| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| {Feature} | {Status} | {Prio} | {Datei} | {Ziel} |

## Geplant (priorisiert)
| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| {Feature} | Geplant | {Prio} | {Datei} | {Ziel} |

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

## Nicht im Backlog (FEATURE_*.md ohne Eintrag)
| Datei | Titel | Status |
|-------|-------|--------|
| {Datei} | {Titel} | {Status} |

> Diese Features haben eine Spec-Datei, sind aber nicht in BACKLOG.md eingetragen.
> Trage sie manuell in BACKLOG.md ein oder nutze `/dtb:feature-plan` beim naechsten Feature-Update.

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

---

Scanne jetzt die Workflow-Dateien und erstelle den Backlog-Status.
