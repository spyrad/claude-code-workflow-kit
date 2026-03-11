# DTB Backlog-Uebersicht

Schneller Ueberblick ueber offene Features, Prioritaeten und aktuellen Fortschritt.

## Aufgabe

Scanne alle relevanten Workflow-Dateien und erstelle eine kompakte Feature/Backlog-Uebersicht.

## Schritt 1: Backlog laden

Lies die Datei:
- **dtb-project/project-workflows/BACKLOG.md**

## Schritt 2: Feature-Specs scannen

Finde alle `FEATURE_*.md` Dateien in `dtb-project/project-workflows/` und lies jeweils die ersten 20 Zeilen (Titel, Status, Zusammenfassung).

## Schritt 3: Aktuellen Status laden

Lies die Datei:
- **dtb-project/project-workflows/WORKFLOW_STATUS.md** (Abschnitt "Offene Aufgaben" und "Laufende Arbeit")

## Schritt 4: Backlog-Report erstellen

Erstelle einen kompakten Report:

```markdown
# Backlog-Uebersicht
**Datum:** {DD.MM.YYYY}

## Aktiv (in Arbeit)
| Feature | Status | Naechster Schritt |
|---------|--------|-------------------|
| {Feature} | {Status} | {Aktion} |

## Geplant (priorisiert)
| Feature | Prioritaet | Abhaengigkeiten |
|---------|------------|-----------------|
| {Feature} | {Hoch/Mittel} | {Deps oder Keine} |

## Backlog (ungeplant)
- {Feature}: {Einzeiler-Beschreibung}

## Abgeschlossen (letzte 5)
- {Feature}: {Ergebnis}

---

## Feature-Specs vorhanden
| Datei | Titel | Status |
|-------|-------|--------|
| FEATURE_{NAME}.md | {Titel} | {Status} |

---

## Empfehlung
{Was sollte als naechstes angegangen werden und warum?}
```

## Richtlinien

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
- `/dtb:feature-plan` - Neues Feature planen
- `/dtb:workflow-status` - Aktueller Workflow-Fortschritt

---

Scanne jetzt die Workflow-Dateien und erstelle die Backlog-Uebersicht.
