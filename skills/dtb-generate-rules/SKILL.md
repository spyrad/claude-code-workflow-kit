---
name: dtb:generate-rules
description: >-
  Use when: "Regeln generieren", "generate rules", "Richtlinien erstellen",
  "Coding Guidelines", "Rules for AI". Analyzes the existing codebase and
  generates coding rules/guidelines per area or technology.
disable-model-invocation: true
argument-hint: "[Bereich: frontend|backend|ui|prompts|testing|allgemein oder 'alle']"
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: setup
  after: [dtb:project-init]
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

Ermittle den Bereich aus dem Argument. Standard-Bereiche:

| Bereich | Datei | Fokus |
|---------|-------|-------|
| `backend` | `BACKEND.md` | API-Design, Services, Datenbank, Authentifizierung, Error-Handling |
| `frontend` | `FRONTEND.md` | Komponenten-Struktur, State-Management, Routing, Data-Fetching |
| `ui` | `UI.md` | Design-System, Styling, Responsiveness, Accessibility, Komponenten-API |
| `prompts` | `PROMPTS.md` | Prompt-Patterns, System-Prompts, LLM-Integration, Output-Formate |
| `testing` | `TESTING.md` | Test-Strategie, Naming, Mocking, Fixtures, Coverage-Ziele |
| `allgemein` | `ALLGEMEIN.md` | Projektweite Regeln: Git, Commits, Ordnerstruktur, Sprache, Tooling |

Argument `alle` → generiere alle 6 Standard-Bereiche nacheinander (jeweils nur wenn relevant fuer das Projekt).

Falls kein Argument: Zeige die Tabelle und frage welchen Bereich (oder `alle`).

### Schritt 3: Codebase analysieren

1. **CLAUDE.md lesen** — Root und Sub-CLAUDE.md fuer bestehende Konventionen
2. **Repo-Verzeichnisse scannen** — Nutze `config.repos` um die relevanten Pfade zu finden
3. **Bestehende Linter/Formatter pruefen** — `.eslintrc`, `prettier`, `ruff.toml`, `pyproject.toml`, etc.
4. **Bereichsspezifisch scannen:**

**Backend:** API-Routes, Service-Layer, DB-Zugriffe, Middleware, Error-Responses, Auth-Patterns
**Frontend:** Komponenten-Architektur, Hooks, State-Management, Router-Struktur, Data-Fetching
**UI:** Styling-Ansatz (CSS Modules, Tailwind, styled-components), Design-Tokens, Breakpoints, Accessibility-Patterns
**Prompts:** System-Prompts, Prompt-Templates, LLM-Aufrufe, Output-Parsing, Fallback-Strategien
**Testing:** Test-Runner, Naming (`*.test.*` vs `*.spec.*`), Mocking-Ansatz, Fixtures, Coverage-Config
**Allgemein:** Git-Workflow, Commit-Konventionen, Ordnerstruktur, Sprach-Mix, Import-Reihenfolge, Env-Handling

### Schritt 4: Bestehende Rules pruefen

Pruefe ob bereits eine Datei fuer diesen Bereich existiert unter `{config.paths.rules}/`:

- Falls **ja**: Zeige den bestehenden Inhalt und frage: "Ueberschreiben oder ergaenzen?"
- Falls **nein**: Fahre mit Schritt 5 fort

### Schritt 5: Rules-Datei generieren

Erstelle die Rules-Datei nach dem passenden bereichsspezifischen Template:

**Gemeinsamer Header (alle Bereiche):**

```markdown
# Coding Rules: [Bereich]

**Generiert:** [YYYY-MM-DD]
**Basis:** [Welche Dateien/Patterns analysiert]
**Manuell angepasst:** Nein

---
```

**Bereichsspezifische Sektionen:**

**BACKEND.md:**
`## API-Konventionen` · `## Service-Layer` · `## Datenbank-Zugriffe` · `## Error-Handling` · `## Auth-Patterns` · `## Do's` · `## Don'ts`

**FRONTEND.md:**
`## Komponenten-Struktur` · `## State-Management` · `## Data-Fetching` · `## Routing` · `## Naming` · `## Do's` · `## Don'ts`

**UI.md:**
`## Design-System` · `## Styling-Konventionen` · `## Responsive-Breakpoints` · `## Accessibility` · `## Komponenten-API` · `## Do's` · `## Don'ts`

**PROMPTS.md:**
`## Prompt-Patterns` · `## System-Prompts` · `## Output-Formate` · `## LLM-Aufrufe` · `## Fallback-Strategien` · `## Do's` · `## Don'ts`

**TESTING.md:**
`## Test-Strategie` · `## Naming & Struktur` · `## Mocking` · `## Fixtures & Testdaten` · `## Coverage-Ziele` · `## Do's` · `## Don'ts`

**ALLGEMEIN.md:**
`## Ordnerstruktur` · `## Git & Commits` · `## Import-Konventionen` · `## Sprache & Naming` · `## Env & Config` · `## Do's` · `## Don'ts`

**Gemeinsamer Footer (alle Bereiche):**

```markdown
---

*Generiert mit `/dtb:generate-rules`. Manuell anpassen und ergaenzen.*
```

Jede Sektion enthaelt knappe Regeln im Format: `- Regel — Begruendung (Beispiel: pfad/zur/datei)`

### Schritt 6: Speichern

Speichere die Datei unter `{config.paths.rules}/{BEREICH}.md` (UPPER_SNAKE_CASE: `BACKEND.md`, `FRONTEND.md`, `UI.md`, `PROMPTS.md`, `TESTING.md`, `ALLGEMEIN.md`).

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
- /dtb:impl-review nutzt diese Rules automatisch (als Rules-Dimension)
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

- `/dtb:impl-review` — Prueft Code gegen diese Rules (als eine seiner drei Review-Dimensionen)
- `/dtb:project-init` — Erstinitialisierung (legt `project-rules/` an)
- `/dtb:project-health` — Prueft Rules-Konsistenz (Check 10)

---

Analysiere jetzt die Codebase und generiere die Rules fuer den angegebenen Bereich.
