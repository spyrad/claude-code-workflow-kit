# Review-Snapshot: meeting-dump
Scope: skills/dtb-meeting-dump/SKILL.md, DERIVED_STATE_RULES.md (§6), skills/dtb-open-question/SKILL.md · Geprüft bis: `05c1ca7` · Datum: 2026-07-21
Gesamt-Verdikt (Review-Zeitpunkt): REJECTED (1 blocking)
Triage-Abschluss 2026-07-21: 4 Fixed · 0 Lesson · 0 Skipped — blocking F1 behoben, Verdikt nach Fix: APPROVED-fähig

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Mittel] — Craft/principled, blocking
skills/dtb-meeting-dump/SKILL.md (Schritt 5.3) vs. DERIVED_STATE_RULES.md §6.1 — §6.1 verlangt „je Meeting einer" für Zwischenstände; der Rückschreib-Pfad hängt `→ Zwischenstand:` akkumulierend OHNE Duplikat-Schutz an. Doppel-Lauf mit gleichem Dump am selben Tag läuft trotz Beleg-Warnung weiter; Zwischenstand-Fragen bleiben `[ ]`, werden re-gematcht → zweite identische `→ Zwischenstand: … (Meeting {selbes Datum})`-Zeile. open-question Schritt 4.2 hat den Exact-Text-Duplikat-Schutz, meeting-dump nicht.
Fix: In Schritt 5.3 vor dem Anhängen überspringen/warnen, wenn im Frage-Block bereits eine `→ Zwischenstand:`-Zeile mit demselben `(Meeting {Datum})`-Marker steht (analog open-question Duplikat-Schutz).
Decision: FIXED — Duplikat-Schutz in Schritt 5.3 ergänzt

### F2 — Architecture — [S:Niedrig × I:Niedrig] — Craft/torvalds, non-blocking
skills/dtb-open-question/SKILL.md:171 — Footer `**Erstellt mit:** /dtb:impl-plan → /dtb:implement` ist ein Copy-Paste-Rest; jeder andere Skill nennt sein eigenes Kommando. Vorbestehend, aber in angefasster Datei aufgefallen.
Fix: Zeile 171 → `**Erstellt mit:** /dtb:open-question`.
Decision: FIXED — Footer korrigiert

### F3 — Pattern Consistency — [S:Niedrig × I:Niedrig] — Craft/principled, non-blocking
skills/dtb-meeting-dump/SKILL.md — kein Hard-Gate (degradiert sauber via Schritt 3.4), aber ohne Begründung; open-question hat den expliziten „Kein formales Eligibility-Gate (bewusst)"-Vermerk. Risiko: späterer Maintainer schraubt unnötiges Gate an.
Fix: Einzeiler ergänzen (Muster open-question), dass meeting-dump bewusst kein Hard-Gate hat.
Decision: FIXED — „Kein formales Eligibility-Gate (bewusst)"-Vermerk ergänzt

### F4 — Pattern Consistency — [S:Niedrig × I:Niedrig] — Craft/principled, nit
skills/dtb-meeting-dump/SKILL.md:16 — `consumes` listet `project-meetings/*.md` nicht, obwohl Schritt 2 die Tagesdatei zum Doppel-Lauf-Schutz liest. workflow-status/pipeline-graph generieren aus Frontmatter → ungenaue Kante.
Fix: `project-meetings/*.md` in `consumes` ergänzen.
Decision: FIXED — consumes ergänzt
