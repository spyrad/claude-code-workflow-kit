# Implementierungsplan: Review-Härtung

**Erstellt:** 2026-07-08
**Feature-Spec:** `features/FEATURE_REVIEW_HAERTUNG.md`
**Geschätzte Dauer:** 3 Phasen (ca. 6–8 h Session-Zeit)
**Status:** Reviewed <!-- plan-review 2026-07-08: 6 Empfehlungen eingearbeitet, 3 Entscheidungen von Damian -->

---

## Phasen-Übersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | plan-review-Härtung: Grounding, Challenger-Pass, Dimensions-Verdikte | ~2,5 h | Geplant |
| Phase 2 | code-review-Härtung: Doppelachse, Cap, Fix-Optionen, Resume-Marker | ~2 h | Geplant |
| Phase 3 | Fixtures, isolierte Abnahme (2 Läufe), Verteilung | ~2,5 h | Geplant |

---

## Phase 1: plan-review-Härtung

### Ziel
`skills/dtb-plan-review/SKILL.md` prüft Pläne mechanisch (Grounding + Challenger-Pass) BEVOR die Agenten diskutieren, und liefert am Ende eine verbindliche Verdikt-Matrix mit deterministischem Gesamt-Verdikt.

### Schritte

#### Schritt 1.1: Grounding-Schritt einbauen
- **Zweck:** Codebase-Behauptungen des Plans verifizieren statt glauben (Baustein 2, SC1/SC4)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Ist-Struktur des Skills (Schritte 0–2c), Discovery-Verhaltensregeln
- **Output:** Neuer Schritt 2d „Grounding": extrahiere prüfbare Referenzen aus dem Plan (Datei-Pfade, Funktions-/Sektions-Namen, Struktur-Behauptungen), verifiziere per Glob/Grep. Still bei Erfolg (`🔎 Grounding: N Referenzen geprüft, alle gefunden`), Abweichungen einzeln (`⚠ Plan referenziert X — nicht gefunden`), leer-Fall (`🔎 Grounding: keine prüfbaren Referenzen`). Unsichere Checks (dynamisch/implizit) nur als Hinweis, nie als FAIL-Treiber. Befunde fließen als Input in Runde 2

#### Schritt 1.2: Challenger-Pass einbauen
- **Zweck:** Mechanische Konsistenz-Prüfung: Widersprüche zwischen Plan-Schritten, Promise-Gaps (Baustein 1, SC2)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Schritt 1.1 (gleicher Skill-Bereich, ein Umbau-Guss)
- **Output:** Schritt 2e „Challenger-Pass": (a) Promise-Gap-Check — jede Zusage im Plan-Text (Deliverables, „wird ergänzt", Checkpoint-Kriterien) muss einem Schritt N.M zuordenbar sein; (b) Widerspruchs-Check — Schritte, die sich gegenseitig aufheben oder dieselbe Datei inkompatibel ändern. Befunde als nummerierte Liste, fließen in Runde 2. Abgrenzung zur Challenge-Runde (Runde 3 = Perspektiv-Kritik) im Skill-Text explizit

#### Schritt 1.3: Verdikt-Liste + Aggregations-Regel
- **Zweck:** Verbindliches, deterministisches Review-Ergebnis (Baustein 3, SC3)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Bestehende Review-Zusammenfassungs-Tabelle (8 Aspekte), Dimensions-Zuordnung (siehe Technische Entscheidungen)
- **Output:** Review-Zusammenfassung erweitert: Verdikt-Zuordnungsliste (Zeile = Dimension, mit zuständigem Agent und Verdikt PASS/WARN/FAIL — jeder Agent bewertet NUR seine eigenen Dimensionen) + **Einspruchs-Regel:** Sieht ein Agent ein Problem in einer fremden Dimension, wird es als eigene Einspruchs-Zeile unter der Liste vermerkt (`Einspruch {Agent} zu {Dimension}: {1 Satz}`) und zählt wie ein WARN der Dimension (bei belegtem Schwerwiegend-Fall: wie FAIL — der zuständige Agent bestätigt oder entkräftet in einem Satz). Gesamt-Verdikt-Zeile mit fester Regel (alle PASS → SOUND; ≥1 WARN, kein FAIL → REVISE; ≥1 FAIL → RETHINK). Verdikte erst NACH Runde 3 vergeben (im Skill-Text verankert), keine Verdikte in den Runden. Betriebs-Wächter-Dimension nur bei Aktivierung Teil der Liste

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Agenten-Dateien um Verdikt-Pflicht ergänzen
- **Zweck:** Agenten kennen ihre Bewertungs-Dimensionen und die Verdikt-Semantik (PASS = keine Bedenken, WARN = behebbar im Plan, FAIL = Dimension kaputt)
- **Dateien:** `agents/architekt.md`, `agents/pragmatiker.md`, `agents/senior-dev.md`, `agents/betriebs-waechter.md`
- **Input:** Dimensions-Zuordnung aus 1.3
- **Output:** Je 1–2 Zeilen pro Agent (Verdikt-Pflicht + zugeordnete Dimensionen); Rollenbeschreibung und Challenge-Techniken unangetastet. Aggregations-Regel bleibt allein im Skill (keine Duplizierung)

### Deliverables
- [ ] plan-review mit Schritten 2d (Grounding) + 2e (Challenger-Pass) + Verdikt-Matrix im Output-Format
- [ ] 4 Agenten-Dateien mit Verdikt-Pflicht

### Checkpoint-Kriterien
- [ ] Schritte 2b (Prior) und 2c (Betriebs-Wächter) textlich unverändert
- [ ] Skill bleibt unter ~280 Zeilen (Aufblähungs-Risiko aus Spec)
- [ ] Matrix funktioniert bei 3 UND 4 aktiven Agenten

---

## Phase 2: code-review-Härtung

### Ziel
`skills/dtb-code-review/SKILL.md` priorisiert Findings über zwei Achsen, cappt bei 10, liefert pro Finding Fix-Optionen mit Tradeoff/Confidence und macht die Triage per Resume-Marker wiederaufnehmbar.

### Schritte

#### Schritt 2.1: Severity×Impact-Doppelachse
- **Zweck:** Zweidimensionale Priorisierung statt einachsiger Prio 1–5 (Baustein 4, SC5)
- **Dateien:** `skills/dtb-code-review/SKILL.md`
- **Input:** Bestehende Prio-Logik (Schritt 5.3 + Report-Format), Skalen-Definition (siehe Technische Entscheidungen)
- **Output:** Finding-Format `[S:{Hoch|Mittel|Niedrig} × I:{Hoch|Mittel|Niedrig}]` ersetzt `[Prio 1–5]`; Sortier-Rangfolge definiert (S vor I); bestehende 5 Prüf-Kategorien bleiben als Kategorien erhalten, steuern aber nicht mehr allein die Reihenfolge

#### Schritt 2.2: Findings-Cap 10 + Überlauf-Zeile
- **Zweck:** Fokus auf die wichtigsten Findings, Reports bleiben handhabbar (Baustein 4, SC5)
- **Dateien:** `skills/dtb-code-review/SKILL.md`
- **Input:** Sortierung aus 2.1
- **Output:** Report zeigt max. 10 Findings (nach S×I-Rang); darunter genau eine Zeile `{N} weitere Findings unterhalb des Caps (erneut ausführen nach Behebung)`; Zusammenfassungszähler zählt weiterhin ALLE Findings

#### Schritt 2.3: Fix-Optionen mit Tradeoff + Confidence
- **Zweck:** Jedes Finding wird actionable mit bewerteten Lösungswegen (Baustein 4, SC6)
- **Dateien:** `skills/dtb-code-review/SKILL.md`
- **Input:** Finding-Format aus 2.1
- **Output:** Pro Finding genau EINE Fix-Option (Entscheidung Damian, dämpft Report-Länge), eine Zeile: `Option: {Fix} — Tradeoff: {Kosten/Nebenwirkung} — Confidence: {Hoch|Mittel|Niedrig}`; ersetzt die bisherige einzeilige „Empfehlung"

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Resume-Marker
- **Zweck:** Abgebrochene Review-Triage wiederaufnehmbar machen (Baustein 5, SC7)
- **Dateien:** `skills/dtb-code-review/SKILL.md`
- **Input:** Marker-Format (siehe Technische Entscheidungen), Commit-SHA via `git rev-parse HEAD`
- **Output:** (a) Report endet mit kopierbarem Marker-Block; **Finding-Identität inhaltlich** (Datei + Zeile + Kategorie), NICHT über laufende Report-Nummern — die sind zwischen Läufen instabil; (b) **Übergabe-Mechanik:** Marker wird nach dem Skill-Aufruf in den Chat eingefügt (mehrzeiliger Block passt nicht ins einzeilige Argument); Skill-Text beschreibt das explizit; (c) **Cap-Interaktion:** Findings unterhalb des Caps gelten als „nicht triagiert" und stehen im Marker als eigener Zähler — nie als „offen"; (d) SHA-Abweichung → `⚠ Stand geändert ({alt} → {neu}) — frisches Review empfohlen. Fortfahren? (Ja/Nein)`; (e) **Scope-Wechsel:** weicht der Scope beim Wiederaufnehmen vom `scope`-Feld des Markers ab → gleiche Warnung + Rückfrage. Kein Datei-Artefakt, kein neues `produces`

### Deliverables
- [ ] code-review mit Doppelachse, Cap 10, Fix-Optionen und Resume-Marker (Ausgabe + Wiederaufnahme)

### Checkpoint-Kriterien
- [ ] Schritt 2b (Prior) und Lektion-Kandidat-Vorschlager textlich unverändert
- [ ] Read-only-Garantie bleibt (keine Datei geschrieben, Marker nur Konsolen-Output)

---

## Phase 3: Fixtures, Abnahme, Verteilung

### Ziel
Beide gehärteten Skills bestehen eine isolierte Fixture-Abnahme durch unabhängige Agenten in zwei getrennten Läufen (SC1–SC8); danach globale Verteilung per kit-sync.

### Schritte

#### Schritt 3.1: Fixture-Set erstellen
- **Zweck:** Reproduzierbare Testbasis für alle Success Criteria
- **Dateien:** Scratchpad/Fixture-Verzeichnis (außerhalb des Repos, nicht committet)
- **Input:** SC1–SC8 aus der Feature-Spec
- **Output:** (a) **Fixture-Mini-Codebase** (kleiner kontrollierter Datei-Bestand, auf den alle Fixture-Referenzen zeigen — Grounding prüft NIE gegen das live-Repo, sonst nicht reproduzierbar); (b) Fixture-Plan mit 1 Fake-Referenz, 1 Widerspruch, 1 Promise-Gap, echten Referenzen auf die Mini-Codebase; (c) Fixture-Plan ohne prüfbare Referenzen; (d) **Compliance-Fixture:** bewusst schwacher Plan, der nachweislich RETHINK erzeugen muss (testet die Verdikt-Regel gegen Aufweichung, nicht nur das Format); (e) Fixture-Diff mit >10 Verstößen unterschiedlicher S×I-Kombinationen; (f) zwei Abnahme-Anleitungen mit Erwartungswerten pro Szenario (inkl. Regressions-Szenarien 2b/2c und 3-vs-4-Agenten-Fall)

#### Schritt 3.2: Isolierte Abnahme durch unabhängige Agenten (2 Läufe)
- **Zweck:** Verifikation ohne Session-Kenntnis (SC9, Muster DERIVED_STATE/LESSON_LOOP); **zwei getrennte Läufe** (Lauf A: plan-review-Szenarien, Lauf B: code-review-Szenarien) — ein Kombi-Lauf für beide Skills riskiert Kontext-Überlauf des Abnahme-Agenten
- **Dateien:** keine (read-only-Läufe der Agenten gegen die Fixtures)
- **Input:** Fixture-Set + die zwei Abnahme-Anleitungen aus 3.1
- **Output:** Zwei Testprotokolle (Szenario / Erwartet / Beobachtet / Ergebnis); Findings-Liste bei Abweichungen

#### Schritt 3.3: Findings beheben + kit-sync
- **Zweck:** Abnahme-Findings einarbeiten, dann globale Verteilung (SC10)
- **Dateien:** betroffene SKILL.md/agents-Dateien; `~/.claude/` (außerhalb des Repos)
- **Input:** Testprotokolle aus 3.2
- **Output:** Findings behoben (ggf. Wiederholung des betroffenen Szenarios); `/dtb:kit-sync check` → `sync`: beide Skills + 4 Agenten global aktualisiert, Lock auf neuem Stand; `dtb-pitch-coach` bleibt übersprungen (INBOX #8)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Zwei bestandene Abnahme-Testprotokolle (Lauf A: plan-review, Lauf B: code-review)
- [ ] Lock-Datei auf neuem Stand, installierte Kopien synchron

### Checkpoint-Kriterien
- [ ] Alle SC1–SC8 im Protokoll ✅
- [ ] kit-sync check meldet: alle Klasse-A-Artefakte synchron (außer bewusstem pitch-coach-Skip)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begründung |
|-------|----------|-------------|-------------|
| Position Grounding/Challenger | A: vor Agenten-Diskussion (2d/2e), B: eigene Runde nach Runde 2 | A | Befunde sind Input für die Diskussion — Agenten sollen auf verifizierten Fakten argumentieren, nicht parallel dazu |
| Verdikt-Dimensionen | A: bestehende 8 Zusammenfassungs-Aspekte den Agenten zuordnen, B: neue Dimensionen definieren | A | Keine neuen Konzepte: Architekt = Machbarkeit + Abhängigkeiten; Pragmatiker = Scope/MVP + Spec-Deckung; Senior Dev = Reihenfolge + Zeitschätzungen + Teststrategie; Betriebs-Wächter = Betrieb & Härtung (falls aktiv) |
| Verdikt-Gefäß | A: jeder Agent NUR eigene Dimensionen (Zuordnungsliste + Einspruchs-Regel), B: alle Agenten alle Dimensionen (echte Matrix) | A (Damian, Review 2026-07-08) | Schlank statt 24–32 Verdikte; Quer-Befunde behalten via Einspruchs-Zeile ein Gefäß |
| Severity/Impact-Skalen | A: je 3-stufig (Hoch/Mittel/Niedrig), B: numerisch 1–5 × 1–5 | A | Konsistent mit Risiko-Tabellen des Kits; 9 Kombinationen reichen für Cap-Sortierung |
| Sortier-Rangfolge S×I | A: Severity dominiert (S:Hoch×I:Niedrig vor S:Mittel×I:Hoch), B: Produkt-Score | A | Schwere Einzelfehler dürfen nicht hinter breite Kleinigkeiten rutschen; deterministisch ohne Rechnen |
| Resume-Marker-Format | A: YAML-Block, B: einzeiliger Token | A | Lesbar + kopierbar; Felder: `scope`, `sha`, `offen`/`triagiert` (Finding-Identität: Datei + Zeile + Kategorie, KEINE laufenden Nummern), `nicht_triagiert: {N}` (Cap-Überlauf); Übergabe durch Einfügen in den Chat |
| Resume-Marker im Scope | A: behalten, B: auf spätere Iteration verschieben | A (Damian, Review 2026-07-08) | Bewusste Entscheidung trotz Komplexitäts-Einwand des Pragmatikers; Dämpfung: genau 1 Fix-Option pro Finding |
| Fixture-Ablage | A: Scratchpad (nicht committet), B: `tests/fixtures/` im Repo | A | Kit hat keine Test-Infrastruktur; Muster der früheren Abnahmen (DERIVED_STATE/LESSON_LOOP) |

---

## Progress

> Single Source of Truth für den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [x] 1.1 Grounding-Schritt (plan-review 2d) — `e1b2860`
- [x] 1.2 Challenger-Pass (plan-review 2e) — `e1b2860`
- [x] 1.3 Verdikt-Liste + Aggregations-Regel — `e1b2860`
- [x] 1.4 Agenten-Dateien Verdikt-Pflicht — `15c9be4`
- [x] 2.1 Severity×Impact-Doppelachse — `15c9be4`
- [x] 2.2 Findings-Cap 10 + Überlauf-Zeile — `15c9be4`
- [x] 2.3 Fix-Optionen mit Tradeoff/Confidence — `754b848`
- [x] 2.4 Resume-Marker — `754b848`
- [x] 3.1 Fixture-Set erstellen — (Scratchpad `review-haertung-fixtures/`, kein Commit)
- [x] 3.2 Isolierte Abnahme (2 Läufe, unabhängige Agenten) — Lauf A 6/6, Lauf B 8/8, keine FAILs
- [x] 3.3 Findings beheben + kit-sync — Nachschärfungen `0d9aff6`; kit-sync Lock→`971e16a` (6 Updates, pitch-coach übersprungen)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist für die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die nächsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_REVIEW_HAERTUNG.md` laden; der erste nicht abgehakte Schritt ist der nächste.
Erkenntnisse/Abweichungen gehören in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
