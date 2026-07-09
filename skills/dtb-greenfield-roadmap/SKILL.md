---
name: dtb:greenfield-roadmap
description: >-
  Use when: "Roadmap zeigen", "Projekt-Roadmap", "Meilensteine",
  "Fortschritt". Creates a roadmap overview for greenfield projects
  by reading strategic docs and showing phases, milestones, and progress.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: greenfield
  after: dtb:greenfield-prd
  next: null
  consumes: [ROADMAP.md, PRD-MVP.md]
  produces: []
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

**Vertikale Slices statt Schicht-Phasen:** Fasse jede Phase als durchgaengigen Slice, der
End-to-End Nutzerwert liefert (nicht „erst alle Datenschicht, dann alle Oberflaeche"). Pruefe je
Phase: Liefert sie fuer sich genommen etwas Nutzbares? Rein technische Schicht-Phasen ohne
sichtbaren Wert markieren.

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

## Foundations

Grundbausteine, die selbst keinen direkten Nutzerwert liefern, aber Slices erst ermoeglichen
(z.B. Persistenz, Auth-Grundlage, Deploy-Pfad). Jede Foundation nennt, was sie freischaltet:

| Foundation | Status | Schaltet frei |
|------------|--------|---------------|
| [Baustein] | [Abgeschlossen / In Arbeit / Geplant] | [Slice(s), die darauf aufbauen] |

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

## Schritt 4: Selbst-Review (vor Ausgabe)

Pruefe die erzeugte Roadmap gegen diese Checkliste; markiere Verstoesse sichtbar im Report,
statt sie zu verschweigen (read-only — nichts wird geaendert, nur gemeldet):

- [ ] Jede Phase ist ein vertikaler Slice mit sichtbarem Nutzerwert (rein technische Schicht-Phase markiert)
- [ ] Jede Foundation nennt, welche Slice(s) sie freischaltet
- [ ] Abhaengigkeiten sind konsistent (keine Phase haengt an einer spaeteren)
- [ ] Status-Angaben decken sich mit den Deliverable-Checkboxen
- [ ] Naechste Schritte sind konkret und einer Phase/Foundation zuordenbar

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
