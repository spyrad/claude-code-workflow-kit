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
  after: [dtb:implement]
  next: [dtb:workflow-checkpoint]
  consumes: [project-rules/*.md, CLAUDE.md, workflow.config.yaml]  # lessons.md separat als Prior (aus Rules-Glob ausgeschlossen)
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

Lies alle `*.md`-Dateien aus `{config.paths.rules}/` — **ausser `lessons.md`**. Diese Datei ist
keine Coding-Regel, sondern eine Lektionen-Sammlung und wird in Schritt 2b separat als Prior gelesen.

Falls keine Rules vorhanden:
```
Keine Richtlinien gefunden in {config.paths.rules}/.
Erstelle welche mit /dtb:generate-rules.
```
→ Abbruch.

### Schritt 2b: Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`) — **separat
vom Rules-Glob** aus Schritt 2.

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `code-review` oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen beim Review still an (zusaetzlich zu den Coding-Rules)
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei nach dem Filter behaltene Lektionen mit gegensaetzlicher `Rule` — z.B. „immer X" vs. „nie X" zum selben Gegenstand):
  beide zeigen und den Widerspruch melden — nicht selbst aufloesen

### Schritt 3: CLAUDE.md laden

Lies die Root-CLAUDE.md und relevante Sub-CLAUDE.md Dateien fuer Architektur-Kontext, Gotchas und Conventions.
Fehlt eine CLAUDE.md → diesen Schritt still ueberspringen (kein Abbruch).

### Schritt 4: Scope bestimmen

**Zuerst: Wiederaufnahme-Check — hat Vorrang vor der Scope-Ableitung.** Enthaelt der Chat einen
`dtb-review-resume`-Marker (YAML-Block aus einem frueheren Report, vom Nutzer eingefuegt —
mehrzeilig, passt nicht ins Argument), ist dies eine **Wiederaufnahme**. Der Marker gewinnt gegen
alle folgenden Scope-Regeln — auch bei leerem `git diff HEAD` und auch ohne Argument. Gehe dann
NICHT in die Ableitung unten und melde NICHT „Keine Aenderungen gefunden":
1. `sha` mit `git rev-parse HEAD` vergleichen — bei Abweichung:
   `⚠ Stand geaendert ({alt} → {neu}) — frisches Review empfohlen. Fortfahren? (Ja/Nein)`
2. Scope aus dem `scope`-Feld uebernehmen; weicht der beim Aufruf angegebene Scope davon ab →
   `⚠ Scope geaendert ({alt} → {neu}) — frisches Review empfohlen. Fortfahren? (Ja/Nein)`
3. Findings unter `triagiert` ueberspringen (Identitaet: Datei + Zeile + Kategorie — NIE ueber
   laufende Report-Nummern matchen); `offen`-Findings erneut pruefen und zeigen. Der Cap gilt
   erneut: durch Triage frei gewordene Plaetze fuellen sich mit bisher nicht triagierten
   Findings (Nachruecken); `nicht_triagiert` wird entsprechend frisch ermittelt

**Sonst (kein `dtb-review-resume`-Marker im Chat):** Scope aus Argument/Diff ableiten —
bestimme welche Dateien geprueft werden sollen:

- Argument `staged` → `git diff --cached --name-only` + `git diff --cached`
- Argument `last-commit` → `git diff HEAD~1 --name-only` + `git diff HEAD~1`
- Argument mit Dateinamen → diese Dateien direkt lesen
- Kein Argument → `git diff HEAD --name-only` + `git diff HEAD` (unstaged + staged)

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
3. **Gegen jede relevante Regel pruefen — Kategorien:**
   - **Logik-Fehler und Bugs** — Falsches Verhalten, fehlende Faelle, Race Conditions
   - **Sicherheitsluecken** — Injection, fehlende Validierung, exponierte Secrets
   - **Performance-Probleme** — N+1 Queries, unnoetige Re-Renders, fehlende Indizes
   - **Wartbarkeit** — Architektur-Patterns, Don'ts, Error-Handling, Namenskonventionen
   - **Code-Style und Konsistenz** — Formatierung, Test-Konventionen

   Nur signifikante Findings reporten die eine Aktion erfordern. Kosmetische Hinweise weglassen.
4. **Jedes Finding auf zwei Achsen einstufen** (Doppelachse — ersetzt die alte Prio 1-5;
   die Kategorie bleibt als Label erhalten, steuert aber nicht mehr allein die Reihenfolge):
   - **Severity** (Schwere des Problems selbst): Hoch = falsches Verhalten, Sicherheitsluecke,
     Datenverlust; Mittel = Performance-/Wartbarkeitsproblem mit realen Folgen; Niedrig =
     Stil/Konsistenz mit Handlungsbedarf
   - **Impact** (Reichweite und Folgekosten): Hoch = betrifft mehrere Module oder alle Aufrufer;
     Mittel = auf Datei/Komponente begrenzt; Niedrig = lokale Einzelstelle

### Schritt 6: Report erstellen

Erstelle den Report als Konsolen-Output (keine Datei schreiben).

**Zaehl- und Status-Regeln:** Warnung = Finding mit S:Niedrig; Verstoss = Finding mit
S:Hoch oder S:Mittel. Datei-Status: ✅ = keine Findings, ⚠️ = nur Warnungen,
❌ = mindestens ein Verstoss.

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

1. **[S:{Hoch|Mittel|Niedrig} × I:{Hoch|Mittel|Niedrig} | {Kategorie}]** Zeile {N}: {Beschreibung}
   → Regel: {Zitat aus Rules-Datei}
   → Option: {Konkreter Fix} — Tradeoff: {Kosten/Nebenwirkung} — Confidence: {Hoch|Mittel|Niedrig}

Sortiere Findings global nach Severity, bei Gleichstand nach Impact — Severity dominiert
(S:Hoch×I:Niedrig kommt VOR S:Mittel×I:Hoch); Anzeige gruppiert nach Datei.
**Cap: maximal 10 Findings im Report** (die Top 10 der globalen Sortierung). Gibt es mehr,
folgt darunter genau eine Zeile:
`{N} weitere Findings unterhalb des Caps (erneut ausfuehren nach Behebung)`

## Zusammenfassung

✅ {N} Dateien konform | ⚠️ {N} Warnungen | ❌ {N} Verstoesse (ALLE Findings, auch unterhalb des Caps)

{Falls Verstoesse: "Empfohlene Aktion: Verstoesse beheben vor Commit/Checkpoint"}
{Falls alles OK: "Alle Aenderungen entsprechen den Projekt-Richtlinien."}
```

### Schritt 6b: Resume-Marker ausgeben

Falls der Report Findings enthaelt, beende ihn mit einem kopierbaren Marker-Block
(bei 0 Findings entfaellt der Marker):

```yaml
dtb-review-resume:
  scope: {staged | last-commit | Dateiliste}
  sha: {git rev-parse HEAD}
  offen:
    - {datei}:{zeile} [{Kategorie}]
  triagiert: []
  nicht_triagiert: {N}   # Findings unterhalb des Caps — zaehlen NIE als "offen"
```

- Initial stehen alle gezeigten Findings unter `offen`, `triagiert` ist leer
- Kollidieren zwei Findings in Datei + Zeile + Kategorie: ein unterscheidendes Stichwort
  anhaengen (`{datei}:{zeile} [{Kategorie}] {Stichwort}`)
- Wird die Triage im Chat unterbrochen: Marker aktualisiert erneut ausgeben —
  besprochene/behobene/verworfene Findings wandern nach `triagiert`
- Hinweis unter dem Block: `Wiederaufnahme: /dtb:code-review aufrufen und diesen Block in den Chat einfuegen.`

---

## Richtlinien

- **Read-Only:** Keine Dateien aendern — nur reporten
- **Spezifisch:** Immer Zeilennummer + konkrete Regel referenzieren
- **Actionable:** Bei jedem Verstoss genau EINE Fix-Option mit Tradeoff und Confidence (nicht mehrere — Report-Laenge)
- **Relevant:** Nur Rules pruefen die zum Bereich der geaenderten Datei passen
- **Deutsch:** Alle Texte auf Deutsch
- **Keine generischen Regeln:** Nur gegen projekt-spezifische Rules aus `project-rules/` pruefen, nicht gegen allgemeine Best Practices

## Lektion-Kandidat erkennen (Vorschlager)

Wenn dir waehrend des Reviews eine nicht-offensichtliche, wiederverwendbare Erkenntnis auffaellt
(Trigger-Frage: „Wuerde ich denselben Fehler nochmal machen, wenn das nur im Session-Log stuende?"),
schlage sie zur Aufnahme vor — **nie stiller Auto-Write**:
```
💡 Lektion-Kandidat: "{knappe Regel}". Nach lessons.md uebernehmen? (/dtb:lesson oder ja/nein)
```
Bei „ja": den Text an `/dtb:lesson` uebergeben.

## Verwandte Skills

- `/dtb:generate-rules` — Richtlinien generieren
- `/dtb:implement` — Umsetzungs-Loop mit Phasen-Ende-Ritual (Vorgaenger)
- `/dtb:workflow-checkpoint` — Session-Ende (Nachfolger)
- `/dtb:project-health` — Prueft Rules-Konsistenz
- `/dtb:lesson` — Lektion festhalten (Prior-Quelle)

---

Fuehre jetzt das Code-Review durch und erstelle den Report.
