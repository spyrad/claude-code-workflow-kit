# Review-Snapshot: capture-duplikat-schutz

Scope: `skills/CLAUDE.md`, `skills/dtb-{idea,task,bug-report,no-loss-check}/SKILL.md`, Change-Artefakte (discovery/spec) · Geprueft bis: `ca38d97` (Progress) — gelesener Stand `09be913` inkl. Triage-Fixes `09365e7`, `e126294` · Datum: 2026-09-07
Gesamt-Verdikt (Zweitlauf): **NEEDS ATTENTION** (kein FAIL, kein blocking)
Nach Triage 2026-09-07: **10 Fixed · 0 Lesson · 0 Skipped** — Fixes liegen uncommittet im Working Tree; ein neues Verdikt erfordert einen erneuten Lauf gegen den committeten Stand.
Erstlauf 2026-08-19: REJECTED, 13 Findings, alle in der Triage FIXED (`09365e7`) — Historie in Git.

Achsen: Plan Adherence WARNING (2) · Scope Discipline WARNING (1) · Safety & Quality WARNING (2) ·
Architecture WARNING (3) · Pattern Consistency WARNING (2) · Rules PASS (STYLE.md ohne Geltungsbereich)
Drift-Bilanz: 10x MATCH, 1x DRIFT (2.4), 0x MISSING, 1x EXTRA, 0 SHA-Luecken. Erstlauf-MISSINGs 3.1-3.3 behoben.

## Findings

### F1 — Pattern Consistency — [S:Mittel × I:Hoch] — Craft/principled
`skills/dtb-no-loss-check/SKILL.md:176-179` vs. `skills/CLAUDE.md:147-149` — Triage-Fix F4 erweiterte den Kanon um den Richtungs-Satz (neue Erfassung bringt mehr mit als der Bestand → keine Dublette); der Spiegel wurde nicht mitgezogen, obwohl der Kopplungs-Hinweis „vollstaendig, keine Verkuerzung" verlangt. Die Zielzahl-Verifikation blieb gruen, weil sie Anker zaehlt, nicht Inhalt (Fehlerklasse L14).
Fix: Richtungs-Satz in den Spiegel-Regelsatz uebernehmen, in Unterdrueckungs-Richtung („Bringt der Kandidat mehr mit als der Bestand → melden").
Decision: FIXED

### F2 — Pattern Consistency — [S:Mittel × I:Mittel] — Craft/principled
`skills/dtb-idea/SKILL.md:86-90` (+ `dtb-task:98-102`, `dtb-bug-report:99-103`) vs. `skills/CLAUDE.md:218-220, 236-242` — F7-Renderregel (je Treffer eine Zeile, `+N weitere`, genau EINE Frage) steht nur im Kanon; die drei Skills tragen Singular-Codeblock + „max. 3 zeigen" — bei 2-3 Treffern zur Laufzeit unspezifiziert. Verletzt die Laufzeit-Autarkie-Invariante.
Fix: Halbsatz in allen drei Treffer-Punkten: „(je Treffer eine Zeile, die Frage genau einmal am Ende)".
Decision: FIXED

### F3 — Plan Adherence — [S:Mittel × I:Mittel] — Drift (2.4 DRIFT)
`plan.md:190-193, 198` — Plan verlangt vier dokumentierte Selbstpruefungs-Nachweise; im Artefakt-Stand nur Nachweis (1) (`2026-08-20.md:23`). (2) project-health-Lauf, (3) Guard-Vergleich gegen `49e1b55`, (4) Aenderungsliste `f971cdd` nirgends protokolliert. Substanz gegeben (Guard byteidentisch, Aenderungsliste 3 Skills + plan.md) — Dokumentationsluecke (L30).
Fix: die drei Nachweise als Kurzprotokoll unter `## Beleg-Protokolle (Phase 3)` in `plan.md` nachtragen, analog 3.1-3.3.
Decision: FIXED

### F4 — Architecture — [S:Niedrig × I:Mittel] — Craft/torvalds
`skills/dtb-idea/SKILL.md:88-89` (+ `task`, `bug-report`) — Pfad „Abbrechen" unspezifiziert (stilles Ende? Ausgabe?); der Guard erhaelt den Text ausdruecklich, der Duplikat-Check wirft ihn kommentarlos weg. `lesson:136-141` hat dieselbe Luecke (Altbestand).
Fix: ein Satz im Kanon-Schema + je Skill: „Abbrechen → eine Zeile `Nicht gespeichert — Bestand: {Fundstelle}`, Skill endet."
Decision: FIXED

### F5 — Scope Discipline — [S:Niedrig × I:Niedrig] — Drift (EXTRA)
`skills/dtb-task/SKILL.md:10`, `skills/dtb-bug-report/SKILL.md:9` — `Bash` in `allowed-tools` ohne Plan-Schritt (Grundlage Triage F1, Uebergabe-Notiz P7). Sachlich richtig, kein Spec-Widerspruch.
Fix: nur Doku — in `plan.md` 2.2/2.3 den Output um „Frontmatter `+Bash`" ergaenzen. Keine Code-Aenderung.
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Niedrig] — Craft/principled (nit)
`skills/dtb-idea/SKILL.md:20` — „einzige Ausnahme: Duplikat-Treffer" — Schritt 1 (Z. 69-71) fragt bei fehlendem Freitext ebenfalls; „einzige" ist woertlich falsch.
Fix: „einzige Ausnahme" → „Ausnahme".
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig] — Craft/principled (nit)
`skills/CLAUDE.md:183-184` — Aufschluesselung der Zielzahl 7 nennt „Einteilungs-/Kopplungsprosa"; der siebte Treffer ist Z. 240 (Laufzeit-Autarkie). Beilaeufige Prosa zaehlt mit (L28).
Fix: „Einteilungs-/Kopplungsprosa" → „Laufzeit-Autarkie-Prosa", Prosa-Treffer als beilaeufig kennzeichnen.
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig] — Craft/torvalds (nit)
`skills/dtb-task/SKILL.md:90-92`, `skills/dtb-bug-report/SKILL.md:89-93` — „Vergleich per Grep gegen Abschnitte" — Grep ist zeilenbasiert, der implizite Lese-Schritt wird nicht genannt.
Fix: „per Grep Kandidaten-Dateien finden, dann den genannten Abschnitt lesen und bewerten".
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig] — Craft/torvalds (nit/taste)
`skills/CLAUDE.md:209` — Slot `{Aehnlicher|Identischer}` ohne Konsumenten (alle drei neuen Skills unscharf). Verteidigbar als Vorgriff auf `open-question`/`meeting-dump` (Z. 254-256).
Fix: als Vorgriff kennzeichnen — oder Slot auf `Aehnlicher` reduzieren und „bei exaktem Vergleich `Identischer`" in die Kopplungsregel-Prosa.
Decision: FIXED

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig] — Drift (nit)
`plan.md:449` (Uebergabe-Notiz P1) — „Protokolle siehe Session-Log" veraltet; sie stehen seit `09365e7` in `plan.md`.
Fix: Verweis auf `## Beleg-Protokolle (Phase 3)` umstellen.
Decision: FIXED

## Info
1 Workflow-Artefakt im Diff (`plan.md`), bekannt — nicht bewertet. `discovery.md`/`spec.md` nur erst-committet bzw. Checkpoint-Status-Sync — kein EXTRA.
