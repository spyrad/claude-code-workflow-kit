# Review-Snapshot: fachfragen-erfassung
Scope: CLAUDE.md, DERIVED_STATE_RULES.md (§6), feature-discover/SKILL.md, feature-plan/SKILL.md · Geprueft bis: `96084b4` · Datum: 2026-07-17
Gesamt-Verdikt: NEEDS ATTENTION

## Findings

### F1 — Safety & Quality — [S:Mittel × I:Mittel]
DERIVED_STATE_RULES.md §6.1/§6.3 — Fall „untagged mit Checkbox" (`- [ ] normaler Punkt`) undefiniert; saehe in der Agenda-Ansicht wie eine offene Fach-Frage aus, obwohl der `[Fach]`-Scanner sie ignoriert.
Fix: explizit festhalten „nur `[Fach]`-Fragen sind statusfaehig (tragen `[ ]`); untagged Punkte bleiben reine Bullets OHNE Checkbox".
Decision: FIXED

### F2 — Safety & Quality — [S:Niedrig × I:Mittel]
DERIVED_STATE_RULES.md §6.1 — Prosa „`[Fach]` steht unmittelbar nach der Checkbox" widerspricht dem Beispiel `- [ ] [Fach] …` (ein Leerzeichen).
Fix: Kanonform pinnen „`- [ ] [Fach] <Frage>` (je ein Leerzeichen zwischen Checkbox, Tag, Frage)", „unmittelbar" streichen.
Decision: FIXED

### F3 — Architecture — [S:Niedrig × I:Niedrig]
DERIVED_STATE_RULES.md §6.3 + feature-plan/SKILL.md — „drei Faelle" erzeugen nur zwei Renderings (a+b untagged, c getaggt); parallele (a)/(b)/(c)-Auflistung suggeriert drei Markups.
Fix: „Zwei Renderings, drei Intents: getaggt `[Fach]` (c) vs. untagged Bullet (a+b, syntaktisch identisch)".
Decision: FIXED

### F4 — Architecture — [S:Niedrig × I:Niedrig]
feature-discover/SKILL.md + feature-plan/SKILL.md — Template-Platzhalter enthaelt Meta-Selbstkommentar („diese Zeile ist selbsterklaerend, der Verweis nur der Kanon-Ort") — Rauschen.
Fix: auf Handlungsanweisung + Kanon-Referenz kuerzen, Selbstkommentar streichen.
Decision: FIXED

### F5 — Safety & Quality — [S:Niedrig × I:Niedrig]
DERIVED_STATE_RULES.md §6.3 — `[Stakeholder]` nennt ein nicht existentes Token; mischt Kanon mit Roadmap.
Fix: in eine Ausblick-Zeile verschieben oder streichen (Feature-Log traegt die Historie).
Decision: FIXED
