# Review-Snapshot: feature-start-statusfeld
Scope: skills/dtb-feature-start/SKILL.md, skills/CLAUDE.md, skills/dtb-implement/SKILL.md · Geprueft bis: `4047ea3` · Datum: 2026-08-07
Gesamt-Verdikt: REJECTED -> alle 9 Findings in der Triage 2026-08-07 behoben (1 blocking, 4 non-blocking, 4 nits; Plan Adherence 5/5 MATCH, 0 EXTRA, Rules uebersprungen). Triage-Bilanz: 9 Fixed, 0 Lesson, 0 Skipped. F3 und F6 wurden mit dem F1-Fix miterledigt (gemeinsamer Blockquote). Nachlese Lektion 13: der F1-Fix machte Kriterium P1-3 (grep WORKFLOW_STATUS in Schritt 4 = 0) rot, weil er den Dateinamen erklaerend nannte; geloest durch die im selben Kasten etablierte Umschreibung "Uebersichtsdatei". Nach Abschluss der Triage alle 11 Phasen-Kriterien erneut ausgefuehrt: gruen.

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled, BLOCKING
skills/dtb-feature-start/SKILL.md:80 + :189 — Behaupten „einziger Pfleger der Anzeigen ist dtb:workflow-checkpoint" fuer drei Ziele inkl. `bug.md`; der Checkpoint pflegt `bug.md` nachweislich nicht (produces Z. 14, Sync-Schritt Z. 218). Dieselbe Fehlerklasse, gegen die das Feature gebaut wurde — im selben Commit entfernt und neu eingesetzt.
Fix: Pfleger auf belegte Ziele einschraenken (BACKLOG.md, WORKFLOW_STATUS.md, spec.md/task.md) und die `bug.md`-Luecke mit Verweis auf INBOX #53 benennen.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch] — principled, non-blocking
skills/dtb-feature-start/SKILL.md:10 — `allowed-tools: Read, Edit`, aber Schritt 2 (Z. 39/41) scannt `features/*/bug.md` und `features/*/task.md` per Glob. Schwesterskills deklarieren das (workflow-next, backlog-status, impl-plan). Nebenbefund: `## Rueckweg` im Plan nennt `Write` als Fehlermodus — real fehlt `Glob`.
Fix: `allowed-tools: Read, Glob, Edit`.
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel] — principled, non-blocking
skills/dtb-feature-start/SKILL.md:78-79 — „haengt allein an `## Progress` bzw. der Checkliste" erzaehlt den Kanon falsch nach: §1.1 leitet auch aus Artefakt-Existenz ab, §1.5 trennt Offen/Analysiert ueber den Debug-Plan, nicht ueber Checkboxen.
Fix: „folgt der Ableitung aus vorhandenen Artefakten und der Checkliste (§1.1/§1.5)".
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel] — principled, non-blocking
skills/CLAUDE.md:105 + skills/dtb-plan-review/SKILL.md:47 — Nennen `feature-start` als Alternativ-Erzeuger fuer ein FEHLENDES plan.md; genau dann verweigert der Skill selbst (Hard-Gate). Vorbestehend, steht aber jetzt zwei Zeilen neben seiner Korrektur. Gegenprobe Phase 2 hat gegen die falsche Frage geprueft.
Fix: `feature-start` als Alternativ-Erzeuger streichen — nur `impl-plan` erzeugt plan.md.
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Niedrig] — principled, non-blocking
skills/dtb-feature-start/SKILL.md:7-8 gegen :16 — `produces` nennt plan.md, die `description` verschweigt jede Schreibwirkung („Status displays remain untouched"). Ursache: eigenes Checkpoint-Kriterium (plan.md:75) verbietet deutsche Schreib-Woerter im Frontmatter.
Fix: englischen Halbsatz ergaenzen: „…and may add a missing `## Progress` section to its plan."
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Mittel] — principled, nit
skills/dtb-feature-start/SKILL.md:77 + :189 — Beleg „(Kanon §1.3)" traegt die Aussage nur halb: §1.3 sagt „beim naechsten schreibenden Skill oder manuell"; Exklusivitaet steht nur fuer `Abgenommen` (§1.2).
Fix: „der im Kanon vorgesehene schreibende Skill ist `dtb:workflow-checkpoint` (§1.3)".
Decision: FIXED

### F7 — Architecture — [S:Niedrig × I:Mittel] — torvalds, non-blocking
skills/dtb-feature-start/SKILL.md:75, 77-82, 102-103, 119, 144, 170, 189 — Dieselbe Tatsache an sieben Stellen; Skill netto +2 Zeilen bei acht entfernten Anweisungen. Blockquote und Z. 189 sind ein Duplikat-Paar und driften bereits gemeinsam falsch (F1).
Fix: Z. 189 auf Zeiger eindampfen, Wiederholung Z. 102-103 streichen; Blockquote bleibt (beantwortet die Maintainer-Frage).
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig] — torvalds, nit
skills/dtb-feature-start/SKILL.md:117, 142, 168 — Ueberschrift „gestartet", Zeile darunter dementiert („unveraendert").
Fix: „# Feature geladen: {Name}" + „**Status:** Geplant (wechselt mit dem ersten abgehakten Schritt)".
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig] — torvalds, nit
skills/dtb-feature-start/SKILL.md:73 gegen :113 — „Kontext laden" vs. „Kontext zeigen" unterscheiden sich in einem Verb.
Fix: Schritt 4 auf „Artefakte lesen" umbenennen.
Decision: FIXED
