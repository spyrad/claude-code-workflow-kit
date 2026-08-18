# Review-Snapshot: herdr-worker-automation
Scope: skills/dtb-worker/SKILL.md, skills/CLAUDE.md (+ 3 Workflow-Artefakte, nicht bewertet) · Geprueft bis: `a625f4b` · Datum: 2026-08-16
Gesamt-Verdikt: REJECTED (3 blocking) — Triage 2026-08-16: 12 Fixed / 0 Lesson / 0 Skipped, alle Findings behoben

Achsen: Plan Adherence PASS (12/12 MATCH, 2 per Mismatch-Entscheid) · Scope Discipline PASS ·
Safety & Quality FAIL · Architecture FAIL · Pattern Consistency WARNING · Rules uebersprungen

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
Frontmatter dtb-worker + Root-CLAUDE.md Worker-Absatz + skills/CLAUDE.md Autonomie-Regel + SKILL.md:195 —
„Niemals committen"-Absolutum an den Raendern nicht nachgezogen; Pane-Traeger committet bewusst (L15/L16-Klasse)
Fix: Autonomie-Regel um Traeger-Klausel qualifizieren; Description + Root-Bullet nachziehen; SKILL.md:195 umformulieren
Decision: FIXED

### F2 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
skills/dtb-worker/SKILL.md Schritt 5 — Freigabe-Dialog erhebt weder Traeger-Wahl noch Pane-Anzahl (zwei Sektionen
delegieren an nicht existentes Dialogelement); Stoppweg-Pflichtzeile fuer Pane-Traeger sachlich falsch
Fix: Schritt 5 Punkt 2 um Traeger-Bestaetigung (+ Anzahl bei pane) erweitern; Stoppweg-Zeile traegerabhaengig
Decision: FIXED

### F3 — Architecture — [S:Hoch × I:Hoch] — torvalds/blocking
skills/dtb-worker/SKILL.md Branch-Verifikation + Queue (3 Stellen) — `master` hartkodiert; in main-Zielprojekten
faellt die Verifikation als Werkzeug-Fehlschlag aus (L7-Familie)
Fix: {default-branch}-Platzhalter aus parallel.default_branch (Fallback: aktueller Branch), am Sektionskopf definiert
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel] — principled/non-blocking
skills/dtb-workflow-checkpoint/SKILL.md (Hand-off-Prosa) — „worktree add {pfad} HEAD … ohne Branch" nur noch fuer
Subagenten-Traeger wahr; bewusst eingefroren (Diff-0-Kriterium), aber nirgends als Nachlauf notiert
Fix: Ein-Satz-Korrektur als Nachlauf-Punkt NACH der Abnahme festhalten (nicht im Diff-0-Fenster)
Decision: FIXED

### F5 — Architecture — [S:Mittel × I:Mittel] — torvalds/non-blocking
skills/dtb-worker/SKILL.md ⛔-Gate, Pane-Auftrag, ⚠-Zeile — Laufzeit-Texte verweisen auf skills/CLAUDE.md,
im Zielprojekt toter Pfad (nicht kit-sync-verteilt)
Fix: Pfad-Verweise aus Laufzeit-Strings streichen (Substanz steht inline); Kanon-Verweise nur Maintainer-Prosa
Decision: FIXED

### F6 — Architecture — [S:Mittel × I:Mittel] — torvalds/non-blocking
skills/dtb-worker/SKILL.md Modus 2 — zwei parallele Pipelines, Zuordnung nur implizit (Schritte 6-9 stillschweigend
subagent-only; Queue restated Kollisionsregel)
Fix: Ueberschriften traeger-markieren; Queue-Restatements auf Verweise auf Schritt 7 eindampfen
Decision: FIXED

### F7 — Pattern Consistency — [S:Mittel × I:Niedrig] — principled/non-blocking
skills/dtb-worker/SKILL.md Traeger-Weiche — Bau-Geruest „wird von Phase 2/3 dieses Features gefuellt" (ist gefuellt,
Referenz adressatenlos im Zielprojekt)
Fix: Parenthese auf „(Ablauf: ### Pane-Ausfuehrung)" kuerzen
Decision: FIXED

### F8 — Pattern Consistency — [S:Mittel × I:Niedrig] — principled/non-blocking
skills/dtb-worker/SKILL.md Branch-Verifikation — Hand-off-Feldnamen dupliziert ohne Kopplungs-Hinweis
Fix: Kopplungs-Zeile „Feldnamen folgen dtb-workflow-checkpoint → ### Hand-off-Block — Aenderung dort → hier nachziehen"
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
Platzhalter-Inkonsistenz {worker.max_attempts} (Pane-Vorlage) vs. {max_attempts} (Subagent-Vorlage)
Fix: auf eine Schreibweise vereinheitlichen
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled/nit
Erkennungs-Warten „genau EIN weiterer Anlauf" ambig (Polling-Budget oder pane run?)
Fix: „bei Ausbleiben genau EIN erneutes herdr pane run mit neuem 90-s-Budget, dann Abbruch"
Decision: FIXED

### F11 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit (unterhalb Cap, mitgefuehrt)
Queue „Start-Sequenz ab Schritt 2" ueberlaedt „Schritt" (Modus 1 hat eigenes Schritt 2)
Fix: „ab Kommando 2 der Start-Sequenz"
Decision: FIXED

### F12 — Pattern Consistency — [S:Niedrig × I:Niedrig] — torvalds/nit-taste (unterhalb Cap, mitgefuehrt)
„Drift wird an einem Ort korrigiert" nach Nennung zweier Orte (Vorlage + Pane-Ausfuehrung)
Fix: ehrlich „an zwei benannten, aufeinander verweisenden Orten"
Decision: FIXED
