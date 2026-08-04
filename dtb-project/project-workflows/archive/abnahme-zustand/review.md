# Review-Snapshot: abnahme-zustand
Scope: DERIVED_STATE_RULES.md, dtb-workflow-next, dtb-backlog-status, dtb-workflow-resume, dtb-archive · Geprueft bis: `c44dffd` · Datum: 2026-08-03
Gesamt-Verdikt: REJECTED (2 blocking) — Stand des Review-Laufs; Triage am 2026-08-03 im selben
Lauf vollstaendig: 6 Fixed · 0 Lesson · 0 Skipped, alle Fixes mechanisch verifiziert (Voll-Kernsatz
je 1x in Kanon + 3 Spiegeln). KEIN Nacharbeits-Auftrag.

Achsen: Plan Adherence PASS (6/6 MATCH) · Scope Discipline PASS · Safety & Quality FAIL ·
Architecture WARNING · Pattern Consistency FAIL · Rules WARNING (deckungsgleich F1/F2)

## Findings

### F1 — Pattern Consistency — [S:Hoch × I:Hoch] — Craft(principled) + Rules
skills/dtb-workflow-next/SKILL.md:77-79/112-113, skills/dtb-backlog-status/SKILL.md:49-50,
skills/dtb-workflow-resume/SKILL.md:93-94 — Kanon deklariert den Kernsatz als „eine Zeile,
Grep-Anker der Kopplung" (Zielzahl 3); in allen drei Spiegeln ist er zeilenumbrochen.
Voll-Satz-Grep = 0 Spiegel-Treffer, Fragment-Grep = 4 (Doppelung in workflow-next). Die
mechanische Spiegel-Verifikation ist ab Geburt funktionsunfaehig. Das Phasen-Gate hatte einen
Teilstring gegrept, nicht den Wortlaut.
Fix: Kernsatz in allen drei Spiegeln auf genau eine physische Zeile ziehen (Ueberlaenge bewusst
akzeptieren), analog Kanon Z.65.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

### F2 — Safety & Quality — [S:Hoch × I:Hoch] — Craft(principled) + Rules
dtb-project/project-rules/DERIVED_STATE_RULES.md:104-105 vs. skills/dtb-workflow-next/SKILL.md:68 —
§1.5 erlaubt explizite Kopf-Zustaende in task.md/bug.md NUR fuer `Pausiert`; die neue
Pipeline-Zeile liest `Abgenommen` aus task.md, der Checkpoint schreibt es dorthin (Sync-Ziel
„spec.md bzw. task.md"), und die Status-Werte-Tabelle in skills/CLAUDE.md kennt `Abgenommen`
fuer task.md nicht. Kanon und Spiegel liefern divergentes Verhalten.
Fix: §1.5-Ausnahmemenge auf „Pausiert, Abgenommen" erweitern + §1.2 Traegerdateien benennen
(spec.md, bei Tasks task.md) + dtb-archive Schritt 2 und skills/CLAUDE.md-Tabelle mitziehen.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

### F3 — Safety & Quality — [S:Mittel × I:Mittel] — Craft(principled)
dtb-project/project-rules/DERIVED_STATE_RULES.md:71-72 — „Feld fehlt oder traegt einen
abgeleiteten Wert → still" ist woertlich zu weit (auch `In Arbeit` bei abgeleitetem „Fertig zum
Testen" waere still — Widerspruch zu §1.3); die Spiegel verkuerzen den Randfall unterschiedlich.
Fix: praezisieren auf „den (mit der Ableitung uebereinstimmenden) Wert; jeder andere
Nicht-`Abgenommen`-Wert faellt unter §1.3" — identisch in die Spiegel uebernehmen.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

### F4 — Architecture — [S:Mittel × I:Mittel] — Craft(torvalds)
skills/dtb-workflow-next/SKILL.md:77-81 + 112-116 — Kernsatz doppelt in derselben Datei; nach
F1-Fix ergaebe der Grep 4 statt versprochener 3. Autarkie rechtfertigt eine Kopie pro Datei,
nicht zwei.
Fix: Schritt-3-Duplikat durch Verweis ersetzen; Zielzahl im Kanon als „1 Treffer je
Spiegel-Datei (3 Dateien)" formulieren.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

### F5 — Architecture — [S:Mittel × I:Niedrig] — Craft(torvalds)
skills/dtb-workflow-resume/SKILL.md:93 — `3b.` ist kein gueltiges Ordered-List-Item; Renderer
brechen die Liste. Keine externen Referenzen auf die Punktnummern (geprueft).
Fix: als regulaeren Punkt 4 einreihen, bisherigen Punkt 4 → 5.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

### F6 — Architecture — [S:Niedrig × I:Niedrig] — Craft(torvalds), nit
skills/dtb-workflow-resume/SKILL.md:95-97 — geforderte Report-Zeile hat keinen Platzhalter in
den drei Fall-Templates (A/B/C), anders als die Git-Sonderzeilen.
Fix: `{Falls abgenommen: "{N} Feature(s) abgenommen — warten auf /dtb:archive"}` in alle drei
Templates aufnehmen.
Decision: FIXED (2026-08-03, Triage im selben Lauf)

## Info
3 Workflow-Artefakte im Diff, bekannt — nicht bewertet (plan.md, BACKLOG.md, INBOX.md);
discovery.md/spec.md als legitime Erhebungsartefakte eingestuft (Buendelung dokumentiert).
