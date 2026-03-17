---
name: dtb:generate-rules
description: >-
  Use when: "Regeln generieren", "generate rules", "Richtlinien erstellen",
  "Coding Guidelines", "Rules for AI". Analyzes the existing codebase and
  generates coding rules/guidelines per area or technology.
disable-model-invocation: true
argument-hint: "[Bereich: frontend|backend|testing|allgemein]"
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: setup
  after: dtb:project-init
  next: null
  consumes: [workflow.config.yaml, CLAUDE.md]
  produces: [project-rules/*.md]
---

# DTB Rules generieren

Analysiere die bestehende Codebase und generiere Coding-Richtlinien fuer einen bestimmten Bereich oder eine Technologie.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden. Bitte zuerst /dtb:project-init ausfuehren.
```
→ Abbruch.

Ermittle den Rules-Pfad aus `config.paths.rules` (Standard: `dtb-project/project-rules`).

### Schritt 2: Bereich ermitteln

Ermittle den Bereich aus dem Argument oder frage nach:

- `frontend` — Frontend-Code (React, Vue, Angular, CSS, etc.)
- `backend` — Backend-Code (API, Services, Datenbank, etc.)
- `testing` — Test-Konventionen und -Patterns
- `allgemein` — Projektweite Regeln
- Oder technologie-spezifisch (z.B. `python`, `typescript`, `go`)

Falls kein Argument: Frage den Nutzer welchen Bereich er abdecken moechte.

### Schritt 3: Codebase analysieren

1. **CLAUDE.md lesen** — Root und Sub-CLAUDE.md fuer bestehende Konventionen
2. **Repo-Verzeichnisse scannen** — Nutze `config.repos` um die relevanten Pfade zu finden
3. **Patterns erkennen:**
   - Naming-Konventionen (Dateien, Variablen, Funktionen, Klassen)
   - Error-Handling-Patterns
   - Import-Struktur und -Reihenfolge
   - Ordnerstruktur und Modul-Organisation
   - Test-Patterns und -Konventionen
   - Konfigurationsansaetze
4. **Bestehende Linter/Formatter pruefen** — `.eslintrc`, `prettier`, `ruff.toml`, `pyproject.toml`, etc.

### Schritt 4: Bestehende Rules pruefen

Pruefe ob bereits eine Datei fuer diesen Bereich existiert unter `{config.paths.rules}/`:

- Falls **ja**: Zeige den bestehenden Inhalt und frage: "Ueberschreiben oder ergaenzen?"
- Falls **nein**: Fahre mit Schritt 5 fort

### Schritt 5: Rules-Datei generieren

Erstelle die Rules-Datei nach folgendem Template:

```markdown
# Coding Rules: [Bereich]

**Generiert:** [YYYY-MM-DD]
**Basis:** [Welche Dateien/Patterns analysiert]
**Manuell angepasst:** Nein

---

## Namenskonventionen

- [Konvention 1]
- [Konvention 2]

## Architektur-Patterns

- [Pattern 1: Beschreibung + Beispiel-Pfad]

## Do's

- [Regel mit Begruendung]

## Don'ts

- [Anti-Pattern mit Begruendung]

## Error-Handling

- [Konvention]

## Testing

- [Test-Pattern fuer diesen Bereich]

---

*Generiert mit `/dtb:generate-rules`. Manuell anpassen und ergaenzen.*
```

### Schritt 6: Speichern

Speichere die Datei unter `{config.paths.rules}/{BEREICH}.md` (UPPER_SNAKE_CASE, z.B. `FRONTEND.md`, `BACKEND.md`, `TESTING.md`, `ALLGEMEIN.md`).

### Schritt 7: Bestaetigung

```
Rules generiert:

Bereich: {Bereich}
Datei: {Pfad}
Sektionen: {Anzahl}
Analysierte Quellen: {Liste}

Naechste Schritte:
- Rules manuell pruefen und anpassen
- "Manuell angepasst: Nein" auf "Ja" setzen nach Review
- /dtb:code-review nutzt diese Rules automatisch
```

---

## Richtlinien

- **Spezifisch:** Regeln muessen auf dem tatsaechlichen Code basieren, nicht auf generischen Best Practices
- **Beispiele:** Wo moeglich, konkrete Datei-Pfade als Beispiel referenzieren
- **Begruendungen:** Jede Regel sollte ein "warum" haben
- **Kompakt:** Max 60-80 Zeilen pro Rules-Datei
- **Deutsch:** Alle Texte auf Deutsch
- **UPPER_SNAKE_CASE:** Dateinamen immer in UPPER_SNAKE_CASE

## Verwandte Skills

- `/dtb:code-review` — Prueft Code gegen diese Rules
- `/dtb:project-init` — Erstinitialisierung (legt `project-rules/` an)
- `/dtb:project-health` — Prueft Rules-Konsistenz (Check 10)

---

Analysiere jetzt die Codebase und generiere die Rules fuer den angegebenen Bereich.
