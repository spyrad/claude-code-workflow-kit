# Review-Snapshot: open-question
Scope: skills/dtb-open-question/SKILL.md, CLAUDE.md · Geprueft bis: `edc1de4` · Datum: 2026-07-19
Gesamt-Verdikt: REJECTED
Aufloesung 2026-07-19: alle 9 Findings FIXED (Triage 9 Fixed · 0 Lesson · 0 Skipped).
Re-Distribution via kit-sync ausstehend — F1 war blocking im bereits verteilten Skill.

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
SKILL.md Schritt 2a — Kopf verlangt „erstes Token = vorhandener Ordner → Ziel", Abbruch-Bullet sagt
„Ordner fehlt → abbrechen". Widerspruch: Token ohne Ordner-Match (Normalfall Frage ohne Slug) hat
keinen expliziten Durchfall zu 2b → woertlich gelesen bricht der haeufigste Pfad ab.
Fix: 2a-Bedingung explizit machen (Token = vorhandener nicht-leerer Ordner → Override; sonst ganzes
Argument = Frage → 2b); „Ordner fehlt"-Abbruch nur fuer tatsaechlich gegebenen, aber ungueltigen Slug.
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Mittel] — torvalds/non-blocking
SKILL.md Schritt 5.1/5.2 — „Footer als Anker, unmittelbar davor einfuegen" platziert die Zeile unter
einem abschliessenden `---`, abgetrennt vom Bullet-Block.
Fix: Footer / naechste `##` / EOF nur als End-Grenze der Sektion, nie als Einfuege-Punkt; immer nach
der letzten echten Inhaltszeile (letzter Bullet), oberhalb eines abschliessenden `---`.
Decision: FIXED

### F3 — Plan Adherence — [S:Mittel × I:Niedrig] — SHA-Check
plan.md Progress 3.1 — geflippt ohne SHA-Beleg, obwohl Commit `edc1de4` existiert (Rueckschreibung
entfiel, weil p3.1 ueber commit-and-push lief).
Fix: `edc1de4` an Progress-Zeile 3.1 nachtragen.
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig] — principled/non-blocking
SKILL.md Schritt 4.2 — Duplikat-Check liest nur die Zieldatei; Frage frueher in discovery.md + jetzt
spec.md → dieselbe offene Frage doppelt (Fach-Agenda §6.3 ist dateiunabhaengig).
Fix: exakten Vergleich ueber beide `## Offene Punkte` (spec.md + discovery.md) fuehren.
Decision: FIXED

### F5 — Safety & Quality — [S:Niedrig × I:Mittel] — principled/non-blocking
SKILL.md Schritt 2a/1 — positional-markerlose Slug-Erkennung: Fragewort, das mit einem Slug
kollidiert, wird stillschweigend als Slug „gestohlen".
Fix: in Variante-B-Bestaetigung den interpretierten Slug explizit ausweisen.
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/non-blocking
Gate-Konvention (skills/CLAUDE.md) — schreibender Skill mit zwingendem Ablage-Ort + Redirect, aber
nicht in der Hard-Gate-Tabelle / nicht in dokumentierter Fit-Check-Form.
Fix: in Gate-Tabelle aufnehmen ODER als bewusst ausgenommen vermerken (Capture-Tool wie /dtb:idea).
Decision: FIXED (als bewusst ausgenommen vermerkt)

### F7 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit
SKILL.md Frontmatter — allowed-tools gewaehrt Write, Skill legt aber nie eine Datei an.
Fix: auf `Read, Glob, Grep, Edit` reduzieren.
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
SKILL.md Z. 29/73/114 — `DERIVED_STATE_RULES.md` ohne `{config.paths.rules}/`-Praefix.
Fix: an allen 3 Stellen vereinheitlichen.
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit
SKILL.md — interne Marker lecken: „(Variante c/B)" in Ueberschriften + „#25" im user-sichtbaren
Ausgabe-Block.
Fix: Ueberschriften entjargonisieren; „#25" aus der User-Meldung entfernen.
Decision: FIXED

## Info
1 Workflow-Artefakt im Diff (plan.md), bekannt — nicht bewertet. discovery/spec.md = Feature-Definition.
