# Review-Snapshot: parallele-sessions
Scope: skills/CLAUDE.md + 14 SKILL.md + workflow.config.yaml (19 Dateien, 5 Commits) · Geprueft bis: `f91b8d5` · Datum: 2026-08-13
Gesamt-Verdikt: REJECTED (1 blocking)
Triage-Bilanz 2026-08-13: 10 Fixed · 0 Lesson · 0 Skipped — alle Findings inkl. F1 (blocking) behoben; Fixes im Working Tree (Commit ausstehend), Spiegel-Verifikation nach den Fixes gruen (Anker 8/8, Fallback 9/9, Teil-Guard 4, WORKTREE-HANDOFF eindeutig)

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] · blocking
skills/dtb-feature-fast/SKILL.md:244 — Teil-Guard-Nachsatz nennt „Schritt 2/5", der `In Arbeit`-Flip passiert real in Schritt 4 (Z.174) — kaputter Verweis auf dem Unterdrueckungspfad, INBOX-Flip im Worktree bliebe ungeschuetzt.
Fix: Verweis auf „(Schritt 4)" korrigieren + Ein-Zeilen-Hinweis an der Flip-Stelle.
Decision: FIXED

### F2 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/CLAUDE.md:182 vs. 8 Spiegel — Vorlage („woertlich uebernehmen") und ausgerollte Bloecke weichen strukturell ab (Branch-Pruefung gefaltet + widerspruechlich im Durchlass-Bullet, Echo als Prosa statt im Fence) — zwei gepflegte Wortlaute (L14).
Fix: Vorlage praezisieren (Bash-Block + ⛔-Fence byte-identisch, Rahmenprosa gemaess Referenz-Instanz dtb-idea); Branch-Pruefung als eigener Bullet nur im HAUPT-CHECKOUT-Fall.
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
⛔-Meldung (alle 8 Spiegel) zitiert skills/CLAUDE.md — existiert am Einsatzort (installierte Kopien/Zielprojekte) nicht; User-facing Verweis ins Leere.
Fix: Regel statt Pfad in der Meldung („globale Dateien schreibt nur die Orchestrator-Session"); Pfad bleibt in der Skill-Prosa.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-feature-plan/SKILL.md:133 — INBOX-Flip in Schritt 2 ohne Teil-Guard-Anker an der Schreibstelle; Marker sitzt erst bei Schritt 9 (im Fluss NACH dem Schreiben).
Fix: Ein-Zeilen-Hinweis direkt an der Flip-Stelle.
Decision: FIXED

### F5 — Architecture — [S:Mittel × I:Mittel]
dtb-workflow-checkpoint — Namenskollision „Handoff" (Session→Folgesession) vs. „Hand-off" (Worktree→Orchestrator); neue Kopfzeile HANDOFF (dtb) nutzt die Schreibweise des alten Konzepts.
Fix: Kopfzeile WORKTREE-HANDOFF (dtb) + Sektionsname „Worktree-Hand-off", Empfangs-Erkennung anpassen.
Decision: FIXED

### F6 — Architecture — [S:Mittel × I:Mittel]
Guard-Block Zeile 3 (Vorlage + 8 Spiegel) — cd/pwd-Normalisierung ohne Fallback: moeglicher falscher WORKTREE-Abbruch („Haupt-Checkout: .") bzw. stilles fail-open.
Fix: `G=$(cd "$G" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }` (analog C) — Vorlage + 8 Spiegel.
Decision: FIXED

### F7 — Safety & Quality — [S:Mittel × I:Niedrig]
open-question als worktree-faehig klassifiziert, kann per Slug-Override aber fremde Change-Ordner beschreiben — Ausnahme unbenannt.
Fix: Zeile in open-question (Override im Worktree → Hinweis + Hand-off) oder Ausnahme in der Kategorien-Tabelle deklarieren.
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Mittel] · nit
Lesestand-Baustein ohne kanonische Vorlage/Anker in skills/CLAUDE.md (Ueberschriftsebenen differieren ## vs. ###) — gleiche Wartungsklasse wie der Guard, ungleiche Loesung.
Fix: Anker + 3-Schritte-Vorlage in skills/CLAUDE.md deklarieren.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Mittel] · nit
skills/dtb-workflow-resume/SKILL.md:125-127 — Watchliste ohne die in Schritt 2 gelesene Changelog-Tagesdatei (dorthin appended ein paralleler Checkpoint).
Fix: Datei in die Liste aufnehmen.
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig] · nit
„## Worktree-Guard (Schritt 0)" kollidiert mit bestehenden Schritt-0-Sektionen (checkpoint: drei Nullen) — Nummern-Ambiguitaet, F1 ist ein Symptom der Klasse.
Fix: Klammer „(Schritt 0)" streichen (9 Dateien), Anker bleibt ## Worktree-Guard.
Decision: FIXED

## Unterhalb des Caps (nicht triagiert)
- meeting-dump erhaelt uebergebenen Text, bekommt aber bewusst(?) kein Echo — Ausnahme in der Vorlage benennen
- `ls -la --time-style=full-iso` ist GNU-only, `-a` bei benannten Dateien wirkungslos — `ls -l` genuegt, GNU-Annahme benennen

## Widerlegt im Verify
- Drift-Nebenbefund „Backslash-Pfadmuster in workflow-resume Z.127" — Zeile traegt real Forward-Slashes
