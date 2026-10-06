# Review-Snapshot: rueckfragen-defaults
Scope: skills/CLAUDE.md, CLAUDE.md, 13× skills/dtb-*/SKILL.md (bug-report, debug-plan, feature-discover, feature-fast, feature-plan, feature-start, impl-plan, impl-review, implement, lesson, no-loss-check, plan-review, task) · Geprueft bis: `2a7ba6b` · Datum: 2026-10-01
Gesamt-Verdikt: NEEDS ATTENTION (0 blocking; Plan Adherence + Scope Discipline PASS, Rules uebersprungen)
Triage 2026-10-01 (neue Sammelliste, Durchgang 1 leer): 10 Fixed · 0 Lesson · 0 Skipped

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings

### F1 — Architecture — [S:Mittel × I:Mittel] — Craft/torvalds
skills/dtb-impl-plan/SKILL.md:264-269, skills/dtb-debug-plan/SKILL.md:185-190 — Lektion-Kandidat lebt nur im Verlauf; Worktree-Hand-off (Sendeseite workflow-checkpoint) kennt die Regel nicht, bei komprimiertem Verlauf/ohne Checkpoint geht er verloren.
Fix: Kandidat als status-neutrale Zeile `Lektion-Kandidat: …` im geschriebenen Artefakt (plan.md/bug.md) ablegen; no-loss-check liest diese Zeilen als Quelle; Worktree-Sonderregel entfaellt.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel] — Craft/principled + Drift-EXTRA
skills/dtb-implement/SKILL.md:165-176 — „Abbrechen" am Staging-/Commit-Knopf undefiniert; Phase geflippt ohne SHA, Wiedereinstieg springt in Phase N+1.
Fix: Abbrechen = Stopp, Index unveraendert, Zeile `⚠ Phase {N} ohne Phasen-Commit — Wiedereinstieg: /dtb:implement {slug} phase {N}`.
Decision: FIXED

### F3 — Architecture — [S:Mittel × I:Mittel] — Craft/torvalds
skills/dtb-implement/SKILL.md:203-204 — nach „passt" kein Entscheidungsmoment mehr fuer Stopp/Review; Option „erst Review" faktisch weg.
Fix: dritte Gate-Option `passt — Commit, dann Stopp`.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel] — Craft/principled
skills/dtb-impl-review/SKILL.md:310-319 vs. :340-342 — Abgrenzung braucht Achsen-Verdikte, Snapshot speichert sie nicht → beim Resume nicht ableitbar.
Fix: Tabelle `## Verdikt-Achsen` ins Snapshot-Template von Schritt 8.
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Niedrig] — Craft/principled
skills/dtb-no-loss-check/SKILL.md:90-94 — „faellt nur durch Treffer in lessons.md weg" widerspricht Randfall 3.
Fix: „…oder durch eine Verwerfung im Verlauf (Randfall 3)".
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Niedrig] — Craft/principled
skills/dtb-feature-start/SKILL.md:196 — „eine Frage" gilt als Start → Rueckfrage loest Code-Aenderung aus.
Fix: „Befehl oder ‚weiter' startet; eine Frage wird beantwortet, ohne zu starten."
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Mittel] — Craft/principled
skills/dtb-impl-review/SKILL.md:268 vs. :340 — Findings mit zwei Fix-Optionen landen in der Sammelliste, „Alle uebernehmen" entscheidet den Tradeoff still.
Fix: Einzel-Finding = S:Hoch ODER FAIL-Achse ODER zwei Fix-Optionen.
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig] — Craft/principled + Drift 2.2
skills/dtb-task/SKILL.md:211, dtb-bug-report:195, dtb-feature-plan:187, dtb-feature-fast:256 — Position der Backlog-Zeile inkonsistent („endet mit" vs. folgende Bestaetigung; feature-fast ohne Platzhalter).
Fix: Platzhalter `{Backlog-Zeile}` ins abschliessende Bestaetigungs-Template aller 4 Skills, „endet mit …" streichen.
Decision: FIXED

### F9 — Safety & Quality — [S:Niedrig × I:Niedrig] — Craft/principled
skills/dtb-implement/SKILL.md:175-176 — „Message aendern … dann committen" ohne erneute Anzeige.
Fix: geaenderte Message zeigen und Knopf erneut stellen.
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig] — Craft/principled
skills/dtb-implement/SKILL.md:199 — Schwelle zaehlt nur Phasen mit Commit.
Fix: „2 Phasen mit durchlaufenem Ritual (mit oder ohne Commit)".
Decision: FIXED

3 weitere Findings unterhalb des Caps (feature-start Fix-Schritt-Nummer bei Wiederaufnahme; feature-fast leerer Altordner nach Ordner-Korrektur; beispielausgaben.md Spiegel-Soll 3→4) — erneut ausfuehren nach Behebung.
