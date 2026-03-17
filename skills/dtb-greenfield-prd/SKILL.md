---
name: dtb:greenfield-prd
description: >-
  Use when: "PRD zeigen", "Anforderungen", "MVP requirements",
  "Product Requirements". Reads and summarizes the Product Requirements
  Document (PRD-MVP.md) for greenfield projects.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: greenfield
  after: null
  next: dtb:greenfield-roadmap
  consumes: [PRD-MVP.md]
  produces: []
---

# Greenfield PRD

Liest ein Product Requirements Document und fasst die MVP-Anforderungen zusammen. Geeignet fuer Projekte in der Planungsphase.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root fuer den Projektnamen.

Falls nicht vorhanden: Frage den Projektnamen ab.

## Aufgabe

Lade das PRD aus `dtb-project/project-strategy/PRD-MVP.md` und erstelle eine uebersichtliche Zusammenfassung der Anforderungen.

## Schritt 1: PRD laden

Lies die folgende Datei:
- **dtb-project/project-strategy/PRD-MVP.md** - Product Requirements Document

## Schritt 2: Anforderungen extrahieren

Identifiziere und kategorisiere:
- **Must-Have Features** (MVP-kritisch)
- **Should-Have Features** (wichtig, aber nicht kritisch)
- **Nice-to-Have Features** (optional)
- **User Stories** mit Akzeptanzkriterien
- **Nicht-funktionale Anforderungen** (Performance, Security, etc.)

## Schritt 3: PRD-Report erstellen

Erstelle einen strukturierten Report in diesem Format:

```markdown
# PRD-Uebersicht: {config.project_name} MVP
**Stand:** {DD.MM.YYYY}

---

## Produkt-Vision

### Elevator Pitch
[1-2 Saetze: Was ist das Produkt und fuer wen?]

### Erfolgskriterien
- [Kriterium 1]
- [Kriterium 2]
- [Kriterium 3]

---

## Zielgruppen

| Persona | Beduerfnis | Hauptnutzen |
|---------|------------|-------------|
| [Persona 1] | [Was braucht sie?] | [Was bekommt sie?] |
| [Persona 2] | [Was braucht sie?] | [Was bekommt sie?] |

---

## Feature-Uebersicht

### Must-Have (MVP)

| Feature | Beschreibung | Status |
|---------|--------------|--------|
| [Feature 1] | [Kurzbeschreibung] | [Implementiert/Offen] |
| [Feature 2] | [Kurzbeschreibung] | [Implementiert/Offen] |
| [Feature 3] | [Kurzbeschreibung] | [Implementiert/Offen] |

### Should-Have

| Feature | Beschreibung | Prioritaet |
|---------|--------------|------------|
| [Feature 1] | [Kurzbeschreibung] | [Hoch/Mittel] |
| [Feature 2] | [Kurzbeschreibung] | [Hoch/Mittel] |

### Nice-to-Have

| Feature | Beschreibung |
|---------|--------------|
| [Feature 1] | [Kurzbeschreibung] |
| [Feature 2] | [Kurzbeschreibung] |

---

## User Stories (Top 5)

### US-1: [Titel]
**Als** [Rolle]
**moechte ich** [Aktion]
**damit** [Nutzen]

**Akzeptanzkriterien:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

### US-2: [Titel]
...

---

## Nicht-funktionale Anforderungen

### Performance
- [Anforderung 1]
- [Anforderung 2]

### Sicherheit
- [Anforderung 1]
- [Anforderung 2]

### Usability
- [Anforderung 1]
- [Anforderung 2]

---

## Abgrenzung (Out of Scope)

Folgendes ist NICHT Teil des MVP:
- [Feature/Funktion 1]
- [Feature/Funktion 2]
- [Feature/Funktion 3]

---

## Abhaengigkeiten

| Abhaengigkeit | Typ | Status |
|---------------|-----|--------|
| [System 1] | Extern | [Verfuegbar/Ausstehend] |
| [System 2] | Intern | [Verfuegbar/Ausstehend] |

---

## Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| [Risiko 1] | [Hoch/Mittel/Niedrig] | [Hoch/Mittel/Niedrig] | [Massnahme] |
| [Risiko 2] | [Hoch/Mittel/Niedrig] | [Hoch/Mittel/Niedrig] | [Massnahme] |

---

## MVP-Checkliste

### Muss vor Release fertig sein:
- [ ] [Feature/Task 1]
- [ ] [Feature/Task 2]
- [ ] [Feature/Task 3]
- [ ] [Feature/Task 4]
- [ ] [Feature/Task 5]

---

*Quelle: dtb-project/project-strategy/PRD-MVP.md*
```

## Richtlinien

- **Priorisiert**: Klare Unterscheidung Must/Should/Nice-to-Have
- **Messbar**: Konkrete Akzeptanzkriterien
- **Deutsch**: Alle Texte auf Deutsch
- **Aktuell**: Status der Features aktualisieren
- **Actionable**: Klare naechste Schritte erkennbar

## Verwendung

Nutze diesen Command:
- Vor Sprint-Planung
- Bei Feature-Diskussionen
- Zur Priorisierung von Tasks
- Beim Review des Projekt-Fortschritts

## Verwandte Commands

- `/dtb:greenfield-roadmap` - Zeitliche Planung
- `/dtb:workflow-resume` - Aktueller Workflow-Fortschritt

---

Lies jetzt das PRD und erstelle den Report.
