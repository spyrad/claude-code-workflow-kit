# Review-Snapshot: output-style-gezielt
Scope: output-styles/dtb-gezielt.md, skills/dtb-kit-sync/SKILL.md, skills/CLAUDE.md, CLAUDE.md, skills/dtb-project-health/SKILL.md, output-styles/dtb-test.md (Wegwerf, netto entfernt) · Geprueft bis: `845e356` (+ `0784a58` fuer 3.1) · Datum: 2026-08-07
Gesamt-Verdikt: NEEDS ATTENTION -> alle 9 Findings in der Triage 2026-08-07 behoben (0 blocking, 4 non-blocking, 5 nits; Plan Adherence 7/7 MATCH, 0 EXTRA, Rules uebersprungen). Triage-Bilanz: 9 Fixed, 0 Lesson, 0 Skipped. F7 wurde mit dem F1-Edit miterledigt (gemeinsame Zeile). Nachlese zur Nachbarschafts-Regel (Lektion 12): der F8-Fix senkte das Phase-2-Kriterium grep -c "output-styles/dtb-\*" >= 2 auf 1; nachgebessert, wieder 2.

## Findings

### F1 — Safety & Quality — [S:Mittel × I:Mittel] — principled, non-blocking
skills/dtb-project-health/SKILL.md:247-248 — Bei korruptem Lock meldet Check 12 „✅ kein Output-Style installiert" — nicht belegbarer Fakt (Ueberclaim).
Fix: Zeilentext auf Evidenz reduzieren: „kein Output-Style im Lock nachweisbar (Lock-Zustand: siehe Kit-Drift)".
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Mittel] — torvalds, non-blocking
skills/dtb-project-health/SKILL.md:330 — Report verspricht `{name}: aktiv`, Check misst nur „outputStyle gesetzt"; bei fremdem Style-Wert meldet der Report falsch.
Fix: Report-Zeile aufs Gemessene reduzieren: `✅ outputStyle gesetzt ({wert})`.
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel] — principled, non-blocking
output-styles/dtb-gezielt.md:9-13 vs. 19 — Praezedenz-Luecke: Leitsatz verlangt Orientierung je Antwort, Regel 3 verbietet Wiederholung aus dem Verlauf.
Fix: Regel 3 ergaenzen: „…bereits steht — die Orientierung (1–3) ist davon ausgenommen".
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig] — principled, non-blocking (Bestand)
skills/dtb-kit-sync/SKILL.md:271 — „prueft Drift als Check 5" stale; Kit-Drift ist Check 11.
Fix: „Check 5" → „Check 11".
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled, nit
skills/dtb-project-health/SKILL.md:13 — consumes mischt Notationen (dtb-lock.json ohne, ~/.claude/settings.json mit Prefix).
Fix: `dtb-lock.json` → `~/.claude/dtb-lock.json`.
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled, nit
skills/dtb-project-health/SKILL.md:239 — Check 12 als einziger Check von `---`-Trennern eingefasst.
Fix: Trenner vor Check 12 entfernen.
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled, nit
skills/dtb-project-health/SKILL.md:247 — Check prueft `output-styles/*`, Klassen-Muster ist `output-styles/dtb-*.md`.
Fix: im Check-Text `output-styles/dtb-*` schreiben.
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig] — torvalds, nit (taste)
skills/dtb-kit-sync/SKILL.md:150-151 — „bewusst deckungsgleich"-Klammer lenkt auf unerklaerte agents/-Asymmetrie.
Fix: Klammer generalisieren oder streichen.
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig] — torvalds, nit (taste)
output-styles/dtb-gezielt.md:3,17 — „kurz, knapp, einfach" Dreifach-Synonym, zweimal.
Fix: auf „aufs Wichtigste reduziert, nicht weggelassen" kuerzen.
Decision: FIXED
