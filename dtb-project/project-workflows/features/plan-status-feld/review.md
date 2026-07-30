# Review-Snapshot: plan-status-feld

Scope: 10 Dateien aus 4 Commits (`bdb412e`, `4dd8671`, `789495f`, `bf87fd2`) · Geprueft bis: `bf87fd2` · Datum: 2026-07-30
Gesamt-Verdikt: REJECTED (2 blocking) — **Stand des Reviews**, nicht des Artefakts
Triage abgeschlossen 2026-07-30: **8 Fixed · 0 Lesson · 2 Skipped · 0 PENDING** — beide Blocker
behoben. Die Fixes liegen im Working Tree (noch nicht committet); ein frisches Review nach dem
Commit wuerde das Verdikt neu vergeben.

Achsen: Plan Adherence WARNING (1) · Scope Discipline PASS (0) · Safety & Quality FAIL (5) ·
Architecture WARNING (3) · Pattern Consistency WARNING (3) · Rules uebersprungen (keine Coding-Rules)

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
`dtb-project/project-rules/DERIVED_STATE_RULES.md:282-291` + `:328-332` — §7.1 definiert die
Vermerkform MIT Klammer, §7.3 matcht auf die nackten Werte und wirft sonst „unbekannter
Statuswert". Eine Parse-Regel fehlt. Real: `impl-plan` erzeugt seit diesem Commit
`**Status:** Entwurf <!-- Review-Nachweis … -->` — woertlich gelesen ist jeder frisch erzeugte
Plan ein unbekannter Wert; 5 archivierte Plaene tragen dieselbe Kommentarform.
Fix: In §7.1 ergaenzen: „Gelesen wird ausschliesslich das erste Wort nach `**Status:**`; alles
danach (Klammer-Vermerk, HTML-Kommentar) ist Annotation und wird ignoriert."
Decision: FIXED (2026-07-30, §7.1 Parse-Regel ergaenzt)

### F2 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
`skills/dtb-workflow-next/SKILL.md:98-102` — Konfliktregel nennt als zweiten Ausloeser
„`Reviewed` bei 0/Y ohne je gelaufenes Review". Widerspricht §7.3 (Konflikt = Feld vs. Progress),
widerspricht der eigenen Tabellenzeile (`Reviewed` + 0/Y = legitimes „Start ausstehend") und ist
read-only nicht entscheidbar (keine Review-Historie). Feuert im gesunden Normalfall.
Fix: Klausel „oder `Reviewed` bei 0/Y ohne je gelaufenes Review" streichen.
Decision: FIXED (2026-07-30, Klausel gestrichen)

### F3 — Pattern Consistency — [S:Mittel × I:Mittel] — principled/non-blocking
`skills/dtb-project-health/SKILL.md:118` — prueft „BACKLOG-Status-Spalte oder `**Status:**`-Zeile"
gegen den abgeleiteten Status, Fix-Hinweis `workflow-checkpoint`. Fuer den plan.md-Kopf nach §7
doppelt falsch: Feld ist status-neutral (§7.4), checkpoint schreibt es nicht (§7.2).
Fix: Zeile einschraenken auf `**Status:**`-Zeile in `spec.md`/`task.md` + Hinweis auf §7.4.
Decision: FIXED (2026-07-30, project-health auf spec.md/task.md eingeschraenkt + §7.4-Hinweis)

### F4 — Safety & Quality — [S:Mittel × I:Mittel] — torvalds/non-blocking
`DERIVED_STATE_RULES.md:330` vs `:337-339` — „fehlendes Feld = still" und „Entwurf widerspricht
Progress = ⚠" greifen beim haeufigsten Altbestand (Feld fehlt + teilweise abgehakt) gleichzeitig;
Reihenfolge unspezifiziert.
Fix: „Konfliktmeldung gilt nur fuer ein physisch vorhandenes Feld mit bekanntem Wert; als
`Entwurf` behandelte Leerstellen bleiben still."
Decision: FIXED (2026-07-30, Vorrang der Still-Regel in §7.3 ergaenzt)

### F5 — Architecture — [S:Mittel × I:Niedrig] — torvalds/non-blocking
Wertematrix doppelt (§7.2 ↔ `plan-review` 6.1), Toleranz-Matrix dreifach (§7.3 ↔ workflow-next ↔
workflow-status). Duplikation ist gerechtfertigt (Regel-Datei ist Klasse-B-Seed, Skills muessen
autark sein), aber keine Stelle traegt den im Repo etablierten reziproken
„Wartungs-Hinweis (Format-Kopplung)" (Vorbild: impl-plan ↔ feature-discover, open-question ↔ meeting-dump).
Fix: Reziproke Kopplungs-Hinweise in §7.2/§7.3 und den drei Skills ergaenzen.
Decision: FIXED (2026-07-30, reziproke Wartungs-Hinweise in §7.2/§7.3 + plan-review/workflow-next/workflow-status)

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/non-blocking
`skills/dtb-backlog-status/SKILL.md:43` — dritter Leser des Felds, in §7.3 nicht genannt
(geschlossene Zweier-Liste). Aktuell folgenlos (beide Werte → „Geplant").
Fix: Zeile vom Feldwert entkoppeln („`plan.md` vorhanden + 0 Checkboxen → Geplant").
Decision: FIXED (2026-07-30, backlog-status vom Feldwert entkoppelt)

### F7 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit (taste)
`DERIVED_STATE_RULES.md:328-332` — 5-Zeilen-Matrix traegt nur zwei echte Informationen.
Fix: als „Default + zwei Ausnahmen" formulieren.
Decision: SKIPPED (2026-07-30, Umbau am frisch gesetzten Kanon: dreifacher Nachzug der gespiegelten Matrix, Nutzen rein aesthetisch)

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
Platzhalter uneinheitlich: Kanon `{Datum}`, Spiegel-Matrix `{YYYY-MM-DD}`; `skills/CLAUDE.md`
macht die strengere Form zur Konvention.
Fix: `{Datum}` → `{YYYY-MM-DD}` in §7.1/§7.2.
Decision: FIXED (2026-07-30, {Datum} -> {YYYY-MM-DD}, 6 Stellen)

### F9 — Architecture — [S:Niedrig × I:Niedrig] — torvalds/nit
`skills/dtb-workflow-next/SKILL.md:131` — Erklaertext im Beispiel-Output statt der `{falls …}`-
Konvention; Risiko der woertlichen Ausgabe. Zudem liest „—" beim Label „Impl-Plan" wie
„kein Plan vorhanden".
Fix: `Impl-Plan  {✓ Reviewed | ✓ Entwurf (Review ausstehend)}`, Erklaertext in die Richtlinien.
Decision: FIXED (2026-07-30, Beispiel-Output auf {…}-Konvention umgestellt)

### F10 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
§6 stellt Status-Neutralitaet an zweite Stelle (6.2), §7 ans Ende (7.4) — inkonsistente
Gliederung zweier bewusst paralleler Abschnitte.
Fix: §7.4 als §7.2 einsortieren.
Decision: SKIPPED (2026-07-30, Umsortierung wuerde §7.2/§7.3/§7.4-Verweise in vier Dateien brechen)

---

**Erstellt mit:** `/dtb:impl-review`
