---
name: dtb:project-team
description: >-
  Use when: "Team erfassen", "Projektteam", "Team dokumentieren",
  "TEAM.md erstellen". Captures the project team and saves it
  to dtb-project/project-strategy/TEAM.md.
disable-model-invocation: true
allowed-tools: Read, Write
pipeline:
  stage: setup
  after: dtb:project-init
  next: null
  consumes: [workflow.config.yaml]
  produces: [TEAM.md]
---

# DTB Projekt-Team

Du erfasst das Projektteam und speicherst es in `dtb-project/project-strategy/TEAM.md`.

---

## Schritt 0: Pruefen

Lies `dtb-project/project-strategy/TEAM.md`.

- Falls die Datei **bereits existiert und ausgefuellt** ist: Zeige den aktuellen Inhalt und frage ob ein Update gewuenscht ist (neues Mitglied, Rolle geaendert, jemand entfernt).
- Falls die Datei **nicht existiert**: Fahre mit Schritt 1 fort.

---

## Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root fuer den Projektnamen.

Falls nicht vorhanden: Frage den Projektnamen ab.

---

## Schritt 2: Interview

Stelle die folgenden Fragen **gebuendelt in einem Block**:

```
Projektteam erfassen:

Fuer jedes Teammitglied bitte angeben:
- Name
- Rolle (z.B. Entwickler, Product Owner, Infrastruktur)
- Bereich/Abteilung
- Fokus (Hauptaufgaben im Projekt)

Kommunikation:
- Hauptkanal (z.B. Slack, Teams, Discord)
- Regelmaessige Meetings (z.B. Daily, Weekly)
```

---

## Schritt 3: TEAM.md schreiben

Erstelle `dtb-project/project-strategy/TEAM.md`:

```markdown
# Projektteam {project_name}

## Kernteam

| Name | Rolle | Bereich | Fokus |
|------|-------|---------|-------|
| {Name} | {Rolle} | {Bereich} | {Fokus} |

## Kommunikation

- **Hauptkanal:** {Kanal}
- **{Meeting-Typ}:** {Teilnehmer} - {Rhythmus}
```

**Regeln:**
- Eine Zeile pro Person, kompakt
- Fokus beschreibt die Rolle **im Projekt**, nicht die generelle Stellenbeschreibung
- Kommunikation nur auflisten was tatsaechlich existiert

---

## Schritt 4: Bestaetigung

```
Team dokumentiert: dtb-project/project-strategy/TEAM.md

{Anzahl} Teammitglieder erfasst.
Hauptkanal: {Kanal}
```

---

## Richtlinien

- **Einmalig erfasst, selten aktualisiert**: Bei Aenderungen erneut aufrufen
- **Kompakt**: Max 20-30 Zeilen, keine ausfuehrlichen Beschreibungen
- **Deutsch**: Alle Texte auf Deutsch
