---
name: dtb:greenfield-roadmap
description: >-
  Use when: "Roadmap zeigen", "Projekt-Roadmap", "Meilensteine",
  "Fortschritt". Creates a roadmap overview for greenfield projects
  by reading strategic docs and showing phases, milestones, and progress.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
---

# Greenfield Roadmap

Erstelle eine Roadmap-Uebersicht fuer ein Projekt in der Aufbauphase (Greenfield). Liest strategische Docs und zeigt Phasen, Meilensteine und Fortschritt.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root fuer den Projektnamen.

Falls nicht vorhanden: Frage den Projektnamen ab.

## Aufgabe

Lade die Roadmap aus dem Projekt und erstelle eine visuelle Uebersicht des Projekt-Fortschritts.

## Schritt 1: Roadmap laden

Lies die folgenden Dateien:
- **dtb-project/project-strategy/ROADMAP.md** - Strategische Roadmap
- **dtb-project/project-strategy/PRD-MVP.md** - MVP-Anforderungen (fuer Status-Abgleich)

## Schritt 2: Fortschritt analysieren

Fuer jeden Meilenstein/Phase:
- Identifiziere geplante Deliverables
- Pruefe aktuellen Status (falls dokumentiert)
- Erkenne Abhaengigkeiten zwischen Phasen

## Schritt 3: Roadmap-Report erstellen

```markdown
# Roadmap: {config.project_name}
**Stand:** {DD.MM.YYYY}

---

## Vision

[1-2 Saetze: Langfristige Vision des Projekts]

---

## Phasen-Uebersicht

```
Phase 1        Phase 2        Phase 3        Phase 4
[MVP]          [Erweiterung]  [Optimierung]  [Skalierung]
   |              |              |              |
   v              v              v              v
[==========]  [====------]  [----------]  [----------]
  100%           40%            0%             0%
```

---

## Phase 1: [Name]

**Status:** [Abgeschlossen / In Arbeit / Geplant]
**Zeitraum:** [Startdatum] - [Enddatum]

### Ziele
- [Ziel 1]
- [Ziel 2]

### Deliverables
- [x] [Deliverable 1]
- [x] [Deliverable 2]
- [ ] [Deliverable 3]

### Ergebnis
[Was wurde erreicht? Lessons Learned?]

---

## Phase 2: [Name]

**Status:** [Abgeschlossen / In Arbeit / Geplant]
**Zeitraum:** [Startdatum] - [Enddatum]

### Ziele
- [Ziel 1]
- [Ziel 2]

### Deliverables
- [x] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### Aktuelle Arbeit
[Was wird gerade implementiert?]

### Blocker
- [Blocker 1, falls vorhanden]

---

## Phase 3: [Name]

**Status:** Geplant

### Geplante Ziele
- [Ziel 1]
- [Ziel 2]

### Voraussetzungen
- [Was muss vorher abgeschlossen sein?]

---

## Meilensteine

| Meilenstein | Datum | Status | Beschreibung |
|-------------|-------|--------|--------------|
| MVP Release | [Datum] | [Status] | [Beschreibung] |
| [Meilenstein 2] | [Datum] | [Status] | [Beschreibung] |
| [Meilenstein 3] | [Datum] | [Status] | [Beschreibung] |

---

## Abhaengigkeiten

```
Phase 1 ──────> Phase 2 ──────> Phase 3
    │               │
    │               └──> [Abhaengigkeit]
    │
    └──> [Externe Abhaengigkeit]
```

---

## Risiken fuer Timeline

| Risiko | Impact | Wahrscheinlichkeit | Mitigation |
|--------|--------|-------------------|------------|
| [Risiko 1] | [Hoch/Mittel] | [Hoch/Mittel] | [Massnahme] |
| [Risiko 2] | [Hoch/Mittel] | [Hoch/Mittel] | [Massnahme] |

---

## Naechste Schritte

### Kurzfristig (diese Woche)
- [ ] [Task 1]
- [ ] [Task 2]

### Mittelfristig (dieser Monat)
- [ ] [Task 1]
- [ ] [Task 2]

### Langfristig (dieses Quartal)
- [ ] [Task 1]
- [ ] [Task 2]

---

## Ressourcen & Kapazitaet

| Bereich | Verfuegbar | Benoetigt | Gap |
|---------|------------|-----------|-----|
| Entwicklung | [X] | [Y] | [Differenz] |
| Design | [X] | [Y] | [Differenz] |
| Testing | [X] | [Y] | [Differenz] |

---

*Quelle: dtb-project/project-strategy/ROADMAP.md*
```

## Richtlinien

- **Visuell**: Fortschrittsbalken und Diagramme
- **Aktuell**: Realistischer Status-Abgleich
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Klare naechste Schritte
- **Ehrlich**: Risiken und Blocker transparent machen

## Verwendung

Nutze diesen Command:
- Bei Sprint-Planung
- Fuer Stakeholder-Updates
- Zur Priorisierung von Features
- Bei Ressourcen-Diskussionen

## Verwandte Commands

- `/dtb:greenfield-prd` - Detaillierte Anforderungen
- `/dtb:workflow-resume` - Aktueller Workflow-Fortschritt

---

Lies jetzt die Roadmap und erstelle den Report.
