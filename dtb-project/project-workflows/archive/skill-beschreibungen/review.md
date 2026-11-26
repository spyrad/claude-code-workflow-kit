# Review-Snapshot: skill-beschreibungen
Scope: skills/CLAUDE.md + 7 skills/dtb-*/SKILL.md (description-Felder) · Geprueft bis: `0bc7190` · Datum: 2026-11-26
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | PASS |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Plan Adherence — [S:Mittel × I:Mittel]
skills/dtb-session-summary/SKILL.md:8-9 — Zwei gestrichene Details stehen nicht im Body (Proaktiv-Hinweis; Ausschluss „git diff, git log, application log"); „summarizing documents" deckt git diff/git log nicht ab. Plan verlangte „anhalten und nachfragen", stattdessen nur im Abnahme-Beleg offengelegt und dort als „verdichtet" bezeichnet.
Fix: Not-for-Satz „… or summarizing documents, diffs or git logs", Zweck-Satz straffen („this session, one day or 7 days"); Abnahme-Beleg korrigieren.
Decision: FIXED

### F2 — Plan Adherence — [S:Mittel × I:Mittel]
skills/dtb-no-loss-check/SKILL.md:7-8 — Auslösebedingung verschoben: „when a session ends without a checkpoint" ist im Auslösemoment nicht wissbar (vorher: „appears to be ending").
Fix: „Use proactively when a session seems to be ending or the topic shifts."
Decision: FIXED

### F3 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:7-8 — Abgrenzung nicht gegenseitig (workflow-status/backlog-status nennen dashboard nicht, dashboard nennt workflow-status nicht); dashboard teilt zwei Fälle in einer Klammer.
Fix: „Not for a chat answer (that is dtb:workflow-next, dtb:workflow-status or dtb:backlog-status)." + Vermerk im Abnahme-Beleg.
Decision: FIXED

### F4 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/CLAUDE.md:27 — Regel erlaubt genau einen Zweck-Satz; no-loss-check trägt zusätzlich den geplanten Proaktiv-Satz.
Fix: optionalen Platz „optionally one `Use proactively when …` sentence for skills the model should start unprompted" in :27 und in der Template-Zeile :12.
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/CLAUDE.md:27 — „Mode, column and output details belong in the body" ist uneingeschränkt; lesson, open-question, meeting-agenda und workflow-status verstoßen ab Tag 1.
Fix: eingrenzen auf „details that do not distinguish the skill from a neighbour belong in the body".
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/CLAUDE.md:27 — Not-for-Fall ohne Skill-Verweis (session-summary „summarizing documents") ist in der Regel nicht vorgesehen.
Fix: Halbsatz „a case no kit skill covers is named without the parenthesis".
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-next/SKILL.md:5-6 (auch no-loss-check, project-dashboard) — Zweck-Satz-Einleitung uneinheitlich („Read-only: …" vs. „Read-only <Nomen> …"); workflow-next ist ein Fragment.
Fix: die drei Doppelpunkt-Formen auf „Read-only <Nomen> …" umstellen.
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-session-summary/SKILL.md:6-7 — ausgefranster Zeilenumbruch nach Edit („"session summary". Read-only").
Fix: Block auf übliche Breite neu umbrechen (mit F1).
Decision: FIXED
