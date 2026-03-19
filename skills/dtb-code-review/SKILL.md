---
name: dtb:code-review
description: >-
  Use when: "Code Review", "Code pruefen", "Review gegen Richtlinien",
  "Rules Check", "Coding Standards pruefen". Reviews recent code changes
  against project-specific coding rules from project-rules/.
disable-model-invocation: true
argument-hint: "[Dateien oder 'last-commit' oder 'staged']"
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: development
  after: dtb:build-check
  next: dtb:workflow-checkpoint
  consumes: [project-rules/*.md, CLAUDE.md, workflow.config.yaml]
  produces: []
---

# DTB Code-Review

Pruefe aktuelle Code-Aenderungen gegen die projekt-spezifischen Coding-Richtlinien aus `project-rules/`.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden. Bitte zuerst /dtb:project-init ausfuehren.
```
→ Abbruch.

### Schritt 2: Rules laden

Lies alle `*.md`-Dateien aus `{config.paths.rules}/`.

Falls keine Rules vorhanden:
```
Keine Richtlinien gefunden in {config.paths.rules}/.
Erstelle welche mit /dtb:generate-rules.
```
→ Abbruch.

### Schritt 3: CLAUDE.md laden

Lies die Root-CLAUDE.md und relevante Sub-CLAUDE.md Dateien fuer Architektur-Kontext, Gotchas und Conventions.

### Schritt 4: Scope bestimmen

Bestimme welche Dateien geprueft werden sollen:

- Argument `staged` → `git diff --cached --name-only` + `git diff --cached`
- Argument `last-commit` → `git diff HEAD~1 --name-only` + `git diff HEAD~1`
- Argument mit Dateinamen → diese Dateien direkt lesen
- Kein Argument → `git diff --name-only` + `git diff` (unstaged + staged)

Falls keine Aenderungen gefunden:
```
Keine Aenderungen gefunden. Gib einen Scope an: staged, last-commit, oder Dateinamen.
```
→ Abbruch.

### Schritt 5: Review durchfuehren

Fuer jede geaenderte Datei:

1. **Relevante Rules ermitteln:**
   - Backend-Datei (z.B. `.py`, `.go`, `src/api/`) → `BACKEND.md` Rules
   - Frontend-Datei (z.B. `.tsx`, `.vue`, `src/components/`) → `FRONTEND.md` Rules
   - Test-Datei (z.B. `*_test.*`, `*.spec.*`) → `TESTING.md` Rules
   - `ALLGEMEIN.md` Rules immer mitpruefen
   - CLAUDE.md Konventionen immer mitpruefen
2. **Datei-Inhalt lesen** (geaenderte Version)
3. **Gegen jede relevante Regel pruefen — in dieser Prioritaetsreihenfolge:**
   1. **Logik-Fehler und Bugs** — Falsches Verhalten, fehlende Faelle, Race Conditions
   2. **Sicherheitsluecken** — Injection, fehlende Validierung, exponierte Secrets
   3. **Performance-Probleme** — N+1 Queries, unnoetige Re-Renders, fehlende Indizes
   4. **Wartbarkeit** — Architektur-Patterns, Don'ts, Error-Handling, Namenskonventionen
   5. **Code-Style und Konsistenz** — Formatierung, Test-Konventionen (niedrigste Prio)

   Nur signifikante Findings reporten die eine Aktion erfordern. Kosmetische Hinweise weglassen.

### Schritt 6: Report erstellen

Erstelle den Report als Konsolen-Output (keine Datei schreiben):

```markdown
# Code Review: {Scope}
**Datum:** YYYY-MM-DD
**Geprueft gegen:** {Liste der Rules-Dateien}
**Dateien:** {Anzahl} geaenderte Dateien

---

## Ergebnis

| Datei | Status | Verstoesse | Details |
|-------|--------|------------|---------|
| {pfad} | ✅/⚠️/❌ | {N} | {Kurzbeschreibung} |

## Verstoesse

### {pfad/zur/datei.ext}

1. **[Prio {1-5}: Kategorie]** Zeile {N}: {Beschreibung}
   → Regel: {Zitat aus Rules-Datei}
   → Empfehlung: {Konkreter Fix}

Sortiere Verstoesse nach Prioritaet (1 = Logik/Bugs zuerst, 5 = Style zuletzt).

## Zusammenfassung

✅ {N} Dateien konform | ⚠️ {N} Warnungen | ❌ {N} Verstoesse

{Falls Verstoesse: "Empfohlene Aktion: Verstoesse beheben vor Commit/Checkpoint"}
{Falls alles OK: "Alle Aenderungen entsprechen den Projekt-Richtlinien."}
```

---

## Richtlinien

- **Read-Only:** Keine Dateien aendern — nur reporten
- **Spezifisch:** Immer Zeilennummer + konkrete Regel referenzieren
- **Actionable:** Bei jedem Verstoss eine konkrete Fix-Empfehlung
- **Relevant:** Nur Rules pruefen die zum Bereich der geaenderten Datei passen
- **Deutsch:** Alle Texte auf Deutsch
- **Keine generischen Regeln:** Nur gegen projekt-spezifische Rules aus `project-rules/` pruefen, nicht gegen allgemeine Best Practices

## Verwandte Skills

- `/dtb:generate-rules` — Richtlinien generieren
- `/dtb:build-check` — Build/Test-Checks (Vorgaenger)
- `/dtb:workflow-checkpoint` — Session-Ende (Nachfolger)
- `/dtb:project-health` — Prueft Rules-Konsistenz

---

Fuehre jetzt das Code-Review durch und erstelle den Report.
