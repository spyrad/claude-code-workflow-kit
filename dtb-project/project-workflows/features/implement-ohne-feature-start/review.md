# Review-Snapshot: implement-ohne-feature-start
Scope: 12 Dateien (skills/dtb-implement, dtb-feature-start, dtb-plan-review, dtb-impl-plan, dtb-workflow-{next,checkpoint,status,resume}, dtb-pipeline-graph, skills/CLAUDE.md, README.md, CLAUDE.md) · Geprueft bis: `d5c592d` · Datum: 2026-11-10
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-feature-start/SKILL.md:13 — `next: [dtb:implement]` ist falsch: Bugs/Aufgaben enden mit `→ Weiter mit: Fix-Schritt {N}`/`Schritt {N}`, implement wuerde ohne plan.md am Gate scheitern; pipeline-graph:200/206 behauptet den Weg ausdruecklich.
Fix: `next: [dtb:workflow-checkpoint]`; pipeline-graph Bug-Kette `bug-report → debug-plan → feature-start → workflow-checkpoint → workflow-resume`, Annotation umschreiben.
Decision: FIXED

### F2 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:438 — Handoff schickt „Geplant" (0/Y) pauschal zu implement; workflow-next trennt Entwurf → plan-review und Reviewed → implement.
Fix: Regel splitten: `Entwurf` 0/Y → `/dtb:plan-review {NAME}`, `Reviewed` 0/Y → `/dtb:implement {NAME}`.
Decision: FIXED

### F3 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-implement/SKILL.md:53-56,75-76 — Altplan ohne `## Progress` erscheint nicht in der Auswahl; als einziger Plan fuehrt die Leer-Meldung faelschlich zu „Plan fehlt".
Fix: Plaene mit 0 Checkbox-Zeilen als Gruppe „Progress fehlt" aufnehmen; Wahl fuehrt in die Nachruestung (Schritt 2 Punkt 2).
Decision: FIXED

### F4 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-implement/SKILL.md:57-59 — Review-Stand liest „erstes Wort" statt der Toleranz-Regel §7.3 (Altwert → „In", fehlend → `—` statt `Entwurf`).
Fix: Review-Stand nach §7.3 ableiten (Altwerte → Reviewed, fehlend/unbekannt → Entwurf).
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/CLAUDE.md:105-106 — Gate-Tabelle: „impl-plan (einziger Erzeuger)" falsch (feature-plan, feature-fast erzeugen plan.md); „plan-review erstellt keinen Plan" widerspricht `produces: [features/*/plan.md]`.
Fix: „impl-plan (feature-plan fuehrt es per Referenz aus, feature-fast gebuendelt)"; „plan-review schreibt nur das Kopf-Statusfeld".
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-implement/SKILL.md:71-72 — neue Textzeile `weiter = uebernehmen` fehlt in der Zuordnungstabelle der Rueckfragen-Defaults (skills/CLAUDE.md).
Fix: Zeile J ergaenzen: `implement` Schritt 1 — Auswahl, genau ein Kandidat → Textzeile.
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-implement/SKILL.md:49-52 — Argument nur `phase N` ist ungeregelt; woertlich wird `phase-2` zum Slug.
Fix: „auch wenn das Argument nur `phase N` ist → Auswahl, Phase merken".
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-pipeline-graph/SKILL.md:187 — „plan-review ← 2 Vorgaenger" mehrdeutig (mit der feature-plan-Kante 3).
Fix: „plan-review ← 2 `after`-Eintraege".
Decision: FIXED
