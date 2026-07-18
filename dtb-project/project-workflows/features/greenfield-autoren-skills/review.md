# Review-Snapshot: greenfield-autoren-skills
Scope: greenfield-prd/SKILL.md · greenfield-roadmap/SKILL.md · feature-plan (Lint-Hinweis) · skills/CLAUDE.md · DERIVED_STATE_RULES §5 · workflow-checkpoint · pipeline-graph · README · CLAUDE.md · Geprueft bis: `9ade135` (4.4) · Datum: 2026-07-18
Gesamt-Verdikt: NEEDS ATTENTION

Dimensionen: Drift 11/11 MATCH (kein EXTRA) · Craft 6 Findings (1 als blocking gemeldet, hier zu hoch-schwerem WARNING kalibriert — Laufzeit intakt) · Rules uebersprungen (keine Coding-Rules) · SHA-Check: 4.4 zitiert falsche SHA
Lektionen-Prior: #1, #2 (Legacy-Alias code-review) beruecksichtigt — kein Treffer im Scope

## Findings

### F1 — Pattern Consistency / Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-greenfield-prd/SKILL.md:184-187 ↔ skills/dtb-greenfield-roadmap/SKILL.md:183-187 — Die beiden Seiten der bewusst-bidirektionalen Format-Kopplung (L5-Deliverable) widersprechen sich UND sind beide unvollstaendig: (1) PRD-Seite listet `## Zielgruppen` als von roadmap geparst — roadmap parst es NIRGENDS. (2) roadmap liest tatsaechlich `## Risiken`/`## Abhaengigkeiten` (Lean-Interview Q3, roadmap Z.123) — KEINE der beiden Warnungen fuehrt diese Sektionen, ein Umbenennen im PRD braeche die „(Recommended)"-Ableitung still. Laufzeit ist intakt (roadmap liest am Nutzungsort korrekt); kaputt ist der Schutz-Kommentar, den §-Kopplung schuetzen soll.
Fix: Beide Gegen-Hinweise auf den REAL geparsten Satz vereinheitlichen — `## Produkt-Vision`, `## Features`, `## User Stories`, `## Out of Scope`, `## Risiken`, `## Abhaengigkeiten`; `## Zielgruppen` streichen (oder eine echte Parse-Stelle dafuer ergaenzen).
Decision: FIXED (beide Hinweise vereinheitlicht)

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-greenfield-roadmap/SKILL.md:156-159 + Selbst-Review ↔ DERIVED_STATE_RULES.md:196 — Doc-Status (`proposed/ready/blocked`) ist laut §5.1 der einzige manuell gesetzte Wert, aber KEIN Schritt sagt dem Autor, wann `ready`/`blocked` statt `proposed` zu setzen ist; Template (Z.158-159) emittiert durchgaengig `proposed`. Gleichzeitig nennt der Hand-off den ersten Slice ohne offene Prerequisites „startbereit" (= `ready` laut Legende Z.153) — sichtbarer Widerspruch Tabelle (proposed) ↔ Hand-off (startbereit).
Fix: In Schritt 6 eine Zuweisungsregel ergaenzen: Slice ohne offene Prerequisites → `ready`, mit unerfuellten → `blocked`, sonst `proposed`; Template-Beispielzeile entsprechend.
Decision: FIXED (Zuweisungsregel in Schritt 6 ergaenzt)

### F3 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-greenfield-roadmap/SKILL.md:41-55 — Das Eligibility-Gate (Schritt 1) steht VOR der Modus-Weiche (Schritt 2) und wirkt damit unconditional — auch im Report-Modus. Ein Nutzer mit fertiger ROADMAP.md, dessen PRD-MVP.md archiviert/geloescht wurde, wird beim blossen Zusammenfassen mit „⛔ braucht ein PRD" geblockt; die Gate-Begruendung „wird aus dem PRD abgeleitet" ist im Report-Modus falsch.
Fix: Gate in den Autoren-Modus verlagern (nach der Weiche, nur Zweig 1+3) ODER Zweig 2 (Report) explizit ausnehmen.
Decision: FIXED (Vorab-Ausnahme fuer vorhandene ROADMAP.md)

### F4 — Plan Adherence — [S:Niedrig × I:Niedrig]
plan.md `## Progress` Zeile 4.4 — zitiert SHA `6bb2a9b`, das ist aber der 4.3-Commit (nur plan.md). Der echte 4.4-Commit (kit-sync + spec.md-SC-Abschluss) ist `9ade135`. Beide Commits existieren und sind verifizierbar — reine Beleg-Fehlzuordnung (§2 Regel 4). Zeile 4.3 traegt keine SHA, ihr realer Commit ist 6bb2a9b (Bookkeeping, Fixtures im Scratchpad = leer-Diff-faehig).
Fix: In plan.md 4.4-Zeile `6bb2a9b` → `9ade135`; optional 4.3 die `6bb2a9b` geben.
Decision: FIXED (4.4 → 9ade135, 4.3 → 6bb2a9b)

### F5 — Safety & Quality — [S:Niedrig × I:Niedrig] (nit)
skills/dtb-greenfield-roadmap/SKILL.md:81 — Readiness-Signal 1 „Vision nicht-trivial — mehr als eine Platzhalter-/Leerzeile" ist als einziges der 4 Signale nicht sauber mechanisch zaehlbar (PRD-Vision-Template ist genau eine `[…]`-Platzhalterzeile → mehrdeutig).
Fix: Praezisieren auf „Abschnittsinhalt nicht-leer UND nicht nur der `[…]`-Platzhalter".
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Niedrig] (nit)
skills/dtb-greenfield-prd/SKILL.md:52-63 — Resume-Marker-Endzustand fuer die letzte Kategorie (f) unspezifiziert: nach Kategorie f steht `<!-- resume: f -->` (noch nicht `done`); Weiche-Zweig 1 „fortsetzen ab der Kategorie NACH {K}" hat fuer f keine Folge-Kategorie. Ein Abbruch zwischen letztem Kategorie-Save und dem `done`-Write faellt ins Loch (umsichtiger Agent leitet es ab, steht aber nicht da).
Fix: Zweig 1 anfuegen: „gibt es keine Folge-Kategorie (K = f), direkt zu Selbst-Review + Write (Schritt 4/5)".
Decision: FIXED

### F7 — Architecture — [S:Niedrig × I:Niedrig] (nit/taste)
skills/dtb-greenfield-prd/SKILL.md:15 — `consumes`-Mischformat: `project-strategy/*.md` mit Pfad-Praefix, `PRD-MVP.md`/`INBOX.md` bar; roadmap (Z.14) listet alle bar. Kosmetisch, aber Metadaten-Parser stolpern.
Fix: Innerhalb der `consumes`-Liste eine Schreibweise waehlen (konsistent zu uebrigen dtb-Skills). Empfehlung: SKIP oder bei naechster Beruehrung.
Decision: SKIPPED (kosmetisch, bei naechster Beruehrung angleichen)
