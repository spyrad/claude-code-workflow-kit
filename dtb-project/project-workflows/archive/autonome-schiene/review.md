# Review-Snapshot: autonome-schiene
Scope: skills/dtb-worker/SKILL.md, skills/CLAUDE.md, CLAUDE.md, DERIVED_STATE_RULES.md, workflow.config.yaml, skills/dtb-project-init/SKILL.md, .gitattributes, features/gitattributes-eol/{task,worker-report}.md · Geprueft bis: `166595c` · Datum: 2026-08-08
Gesamt-Verdikt: REJECTED (1 blocking, 4 non-blocking, 3 nits)
Triage-Bilanz 2026-08-08: 7 FIXED · 1 SKIPPED (F8, bewusst) · 0 PENDING — alle Findings entschieden

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
skills/dtb-worker/SKILL.md:163 vs. 158-159 vs. skills/CLAUDE.md:120 — Schreibziel-Widerspruch im kritischsten Kontrakt: „keine Schreibzugriffe ausserhalb des eigenen Worktrees" vs. Rechenschafts-Pflicht `task.md`/`worker-report.md` (liegen im Haupt-Repo-Change-Ordner); der Kanon liest sich als ZWEI Schreibziele. Ein woertlich parsender Worker bekommt zwei verschiedene Antworten.
Fix: Genau eine Regel, in beiden Dateien identisch — Worktree-only + Zusatz „Report/Checkboxen erreichen das Haupt-Repo erst mit der Abnahme" (entspricht dem realen Erstlauf-Verhalten); Schritt-9-Link entsprechend praezisieren.
Decision: FIXED (2026-08-08 — SKILL.md Auftrag + Schritt 9, skills/CLAUDE.md Kanon)

### F2 — Architecture — [S:Mittel × I:Hoch] — torvalds/non-blocking
skills/dtb-worker/SKILL.md:197 — Ausgangs-Vokabular deckt den haeufigsten Fall nicht: Tasks mit Commit-Schritten oder Fremd-Maschinen-Schritten koennen strukturell nie „gruen" werden; der erste Realbetrieb musste „teilweise" umdeuten.
Fix: Verbots-gesperrte/unerreichbare Schritte bei der Freigabe als „beim Menschen" ausklammern; „gruen" = alle Worker-erreichbaren Schritte gruen (Report weist Ausgeklammertes aus).
Decision: FIXED (2026-08-08 — Schritt 5 Punkt 2b + Ausgang-Definition Schritt 8)

### F3 — Safety & Quality — [S:Mittel × I:Mittel] — principled/non-blocking
skills/dtb-worker/SKILL.md:141, 198 — Worktree-Lebenszyklus: `{tmp}` nirgends gebunden (Session-Scratchpad garantiert „liegt dort bis zur Abnahme" nicht ueber Sessions); `git worktree remove` fehlt in Schritt 9 (verwaiste Registrierungen akkumulieren).
Fix: `{tmp}` als bis zur Abnahme stabilen Ort definieren + Aufraeum-Zeile in Schritt 9.
Decision: FIXED (2026-08-08 — .dtb-worktrees/ neben dem Repo + worktree-remove-Zeile)

### F4 — Pattern Consistency — [S:Mittel × I:Mittel] — principled/non-blocking (auch Drift-Befund)
skills/dtb-worker/SKILL.md:17 vs. skills/CLAUDE.md:15 — `stage: execution` nicht im dokumentierten Enum (Praezedenz: `capture` fehlt ebenfalls); `workflow-status`/`project-health` lesen das Feld.
Fix: Enum in skills/CLAUDE.md um `execution` (+ `capture`) ergaenzen.
Decision: FIXED (2026-08-08 — beide Werte ergaenzt, Alt-Drift capture mitgeschlossen)

### F5 — Pattern Consistency — [S:Mittel × I:Mittel] — principled/non-blocking
skills/dtb-worker/SKILL.md:18 vs. skills/dtb-task/SKILL.md:14 — Pipeline-Kanten einseitig: `worker.after: [dtb:task, dtb:idea-review]`, aber `dtb-task.next: null` und `idea-review.next` kennt worker nicht (exakt die #46-Fehlerklasse, am Tag der Einfuehrung).
Fix: `dtb-task` auf `next: [dtb:worker]`; `dtb:idea-review` aus `worker.after` streichen (INBOX ist nur Scan-Quelle in consumes).
Decision: FIXED (2026-08-08 — beide Kanten beidseitig; Achtung: dtb-task ist Klasse A, Nachlauf-Sync noetig)

### F6 — Architecture — [S:Niedrig × I:Mittel] — torvalds/nit
skills/dtb-worker/SKILL.md:189 vs. 125-128 — „Report VOR dem Ende, egal mit welchem Ausgang" gilt fuer harte Stopps (Task-Verwaltung, Kollisionsregel) nicht — der Worker wird beendet, bevor er schreibt.
Fix: Auf selbst-beendete Laeufe einschraenken; bei harten Stopps „Diff ohne Report" bzw. Orchestrator-Minimalnotiz.
Decision: FIXED (2026-08-08 — Schritt-8-Einleitung)

### F7 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit (taste)
skills/dtb-worker/SKILL.md:69-72 — Vier-Zeilen-Andock-Blockquote fuer einen Konsumenten (#33), den es noch nicht gibt.
Fix: Auf eine Zeile kuerzen.
Decision: FIXED (2026-08-08)

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
features/gitattributes-eol/task.md:5 — `**Status:** Offen` bei 5/6 abgehakten Schritten; die Datei wurde bei der Abnahme ohnehin editiert, das Anzeige-Feld haette mitziehen koennen (naechster Checkpoint synct sonst).
Fix: Zeile auf abgeleiteten Anzeige-Wert setzen.
Decision: SKIPPED (2026-08-08 — bewusst dem Pfleger workflow-checkpoint ueberlassen, keine Doppel-Schreiberei nach dem #50-Prinzip)
