# Implementierungsplan: SKILL_10X_OPTIMIERUNGEN

**Erstellt:** 2026-07-09
**Feature-Spec:** `features/FEATURE_SKILL_10X_OPTIMIERUNGEN.md`
**Geschaetzte Dauer:** ~6-9 h (5 Bloecke + Abnahme)
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | project-health: A/B, WARN-CONTINUE, Fixes | ~1 h | Geplant |
| Phase 2 | debug-plan: Evidenz-Tabelle + Framing-Ergebnis | ~45 min | Geplant |
| Phase 3 | greenfield-roadmap: Slices, Unlocks, Selbst-Review (read-only) | ~1 h | Geplant |
| Phase 4 | feature-discover: Checkpoint-Frontmatter + Recommended | ~45 min | Geplant |
| Phase 5 | checkpoint/resume: Handoff-Block (beidseitig) | ~1 h | Geplant |
| Phase 6 | Abnahme + kit-sync | ~2-3 h | Geplant |

**Reihenfolge:** aufsteigend nach Blast-Radius — erst die drei Report-Bloecke (in sich
geschlossen), dann die zwei Session-Bloecke (feature-discover, checkpoint/resume koppeln).
Alle Bloecke sind technisch unabhaengig und einzeln abnehmbar.

---

## Phase 1: project-health (Block 1)

### Ziel
Health-Report priorisiert Befunde und bricht bei Einzel-Check-Fehlern nicht ab.
Reine Ausgabe-Struktur — `produces: []` bleibt (kein Write).

### Schritte

#### Schritt 1.1: Befund-Kategorisierung A/B
- **Zweck:** Befunde in „A jetzt / B spaeter" trennen, damit der Report handlungsleitend wird
- **Dateien:** `skills/dtb-project-health/SKILL.md`
- **Input:** bestehende Check-Ausgabe-Sektion
- **Output:** Report-Format mit zwei Kategorien; A = blockierend/inkonsistent, B = kosmetisch/spaeter

#### Schritt 1.2: WARN-AND-CONTINUE
- **Zweck:** ein fehlgeschlagener Einzel-Check darf den Gesamt-Report nicht abbrechen
- **Dateien:** `skills/dtb-project-health/SKILL.md`
- **Input:** Ablauf der Einzel-Checks
- **Output:** Regel „Einzel-Check-Fehler → WARN im Report, weiterlaufen"; Fehlerzeile als WARN gelistet

#### Schritt 1.3: Fixes mit Kommando + Aufwand
- **Zweck:** jeder Befund bekommt eine konkrete Behebung statt nur einer Diagnose
- **Dateien:** `skills/dtb-project-health/SKILL.md`
- **Input:** Befund-Liste
- **Output:** pro Befund `Fix: {Kommando/Aktion}` + `Aufwand: {klein/mittel/gross}`; Zeilenzahl < 500 gepruft

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] project-health mit A/B-Kategorien, WARN-CONTINUE, Fix+Aufwand pro Befund

### Checkpoint-Kriterien
- [ ] Skill <= 500 Zeilen, Frontmatter unveraendert (`produces: []`)
- [ ] Kein Write eingefuehrt (bleibt Report-only)

---

## Phase 2: debug-plan (Block 2)

### Ziel
Hypothesen werden nach Evidenzstaerke gefuehrt; „Framing war korrekt" ist ein valides Endergebnis.

### Schritte

#### Schritt 2.1: Hypothesen-Tabelle mit Evidenzstaerke
- **Zweck:** Root-Cause-Hypothesen nachvollziehbar gewichten
- **Dateien:** `skills/dtb-debug-plan/SKILL.md`
- **Input:** bestehende Root-Cause-Sektion
- **Output:** Tabelle Hypothese | Evidenz | Staerke (STRONG/WEAK/NONE) | naechster Test

#### Schritt 2.2: „Framing war korrekt" als valides Ergebnis
- **Zweck:** kein Zwang, eine Hypothese zu bestaetigen — Ausgang „Problem-Framing falsch/schon geloest" zulassen
- **Dateien:** `skills/dtb-debug-plan/SKILL.md`
- **Input:** Abschluss-/Ergebnis-Sektion
- **Output:** explizite Ergebnis-Option, wenn keine Hypothese STRONG erreicht

> **3x3-Block:** Nach Schritt 2.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] debug-plan mit Evidenz-Tabelle + Framing-Ergebnis-Option

### Checkpoint-Kriterien
- [ ] Skill <= 500 Zeilen, Frontmatter unveraendert
- [ ] Bestehender Write-Ablauf (`produces: BUG_*.md`) unangetastet

---

## Phase 3: greenfield-roadmap (Block 3, read-only)

### Ziel
Roadmap-Uebersicht zeigt vertikale Slices + Foundations mit Unlocks und prueft sich selbst.
Bleibt **read-only** (`produces: []`) — kollisionsfrei zu Idee #11.

### Schritte

#### Schritt 3.1: Vertikale Slices
- **Zweck:** Roadmap nach durchgaengigen Slices statt reiner Schicht-Phasen darstellen
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** bestehende Phasen-Ausgabe
- **Output:** Ausgabe-Format „vertikale Slices" in der Uebersicht

#### Schritt 3.2: Foundations mit Unlocks-Feld
- **Zweck:** Grundbausteine sichtbar machen, die weitere Slices freischalten
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** Slice-Ausgabe
- **Output:** Foundations-Block mit Feld „schaltet frei: {Slices}"

#### Schritt 3.3: Selbst-Review-Checkliste
- **Zweck:** Roadmap-Ausgabe gegen Qualitaetskriterien pruefen, bevor sie gezeigt wird
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** fertige Ausgabe
- **Output:** kurze Selbst-Review-Checkliste im Skill (z.B. „jede Slice liefert Nutzerwert?")

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] greenfield-roadmap mit Slices, Unlocks-Feld, Selbst-Review

### Checkpoint-Kriterien
- [ ] Skill <= 500 Zeilen, `produces: []` unveraendert (keine Write-Faehigkeit ergaenzt)

---

## Phase 4: feature-discover (Block 4)

### Ziel
Discovery ist wiederaufnehmbar (Checkpoint-Frontmatter) und nutzt das „(Recommended)"-Muster.

### Schritte

#### Schritt 4.1: Resume-Marker (leichtgewichtig, resumebar)
- **Zweck:** eine unterbrochene Discovery kann in neuer Session weiterlaufen
- **Dateien:** `skills/dtb-feature-discover/SKILL.md`
- **Input:** DISCOVERY_*.md-Ausgabe (Skill hat Write, `produces: DISCOVERY_*.md`)
- **Output:** **HTML-Kommentar-Marker** (`<!-- resume: {zuletzt beantwortete Klaerungs-Kategorie} -->`) statt YAML-Frontmatter, damit project-health/pipeline-graph den DISCOVERY-Konsum nicht fehlinterpretieren (Review-Entscheidung 2026-07-09); Wiedereinstiegs-Regel im Skill

#### Schritt 4.2: „(Recommended)"-Muster an Auswahlpunkten
- **Zweck:** die realen Auswahlpunkte bekommen einen markierten Default
- **Dateien:** `skills/dtb-feature-discover/SKILL.md`
- **Input:** die tatsaechlichen Auswahlstellen (Feature-Name-Vorschlag Schritt 5, Scope-Schnitt) — NICHT die offenen Klaerungsfragen (3a-3e bleiben Freitext)
- **Output:** Konvention „empfohlener Default markiert" nur an diesen Stellen (Review-Grounding 2026-07-09: Skill nutzt sonst keine Optionslisten)

> **3x3-Block:** Nach Schritt 4.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] feature-discover resumebar + Recommended-Muster

### Checkpoint-Kriterien
- [ ] Skill <= 500 Zeilen, Frontmatter-Schema (Pipeline-Felder) unveraendert
- [ ] Resume-Marker als HTML-Kommentar (kein YAML) — von project-health/pipeline-graph nachweislich ignoriert
- [ ] „(Recommended)"-Muster nur an Auswahlpunkten, offene Klaerungsfragen unveraendert

---

## Phase 5: checkpoint/resume Handoff (Block 5)

### Ziel
checkpoint erzeugt einen Handoff (naechster Befehl + /clear-Hinweis); resume nimmt ihn
konsistent auf. **checkpoint schreibt** (hat Write), **resume liest nur** (kein Write) —
Trennung strikt einhalten.

### Schritte

#### Schritt 5.1: Handoff-Block in checkpoint (Sende-Seite)
- **Zweck:** am Session-Ende einen klaren Wiedereinstieg hinterlassen
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** abgeleiteter naechster Schritt (aus `## Progress`/Pipeline)
- **Output:** Handoff-Abschnitt (naechster Befehl + `/clear`-Hinweis) in WORKFLOW_STATUS/session-log; Fallback ohne erfundene Empfehlung, wenn nichts ableitbar

#### Schritt 5.2: Handoff-Aufnahme in resume (Empfangs-Seite)
- **Zweck:** den Handoff beim Fortsetzen zeigen — ohne Write
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md`
- **Input:** von checkpoint geschriebener Handoff-Abschnitt
- **Output:** resume liest und zeigt den Handoff im Resume-Report; Format beidseitig referenziert/konsistent

> **3x3-Block:** Nach Schritt 5.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] checkpoint schreibt Handoff, resume zeigt ihn konsistent

### Checkpoint-Kriterien
- [ ] beide Skills <= 500 Zeilen, Frontmatter unveraendert
- [ ] resume bleibt ohne Write (`allowed-tools: Read, Bash`); Handoff-Format auf beiden Seiten deckungsgleich

---

## Phase 6: Abnahme + kit-sync

### Ziel
Alle Bloecke verifiziert, Budgets/Frontmatter konsistent, gehaertete Skills global aktiv.

### Schritte

#### Schritt 6.1: Budget- + Frontmatter-Konsistenz-Check
- **Zweck:** Regressionen und Budget-Ueberschreitungen ausschliessen
- **Dateien:** alle sechs SKILL.md
- **Input:** finaler Stand
- **Output:** Zeilenzahl < 500 je Datei bestaetigt; Pipeline-Frontmatter unveraendert; `produces: []` bei project-health/greenfield-roadmap intakt

#### Schritt 6.2: Abnahme pro Block
- **Zweck:** Verhalten wortlautkonform bestaetigen
- **Dateien:** Fixtures/Scratchpad
- **Input:** festgelegte Strategie — Report-Bloecke 1-3 via **Fixture** durch unabhaengigen Agenten (Praezedenz SPEC/REVIEW_HAERTUNG), Session-Bloecke 4-5 via **Praxiserprobung** (echtes feature-discover bzw. checkpoint→resume-Zyklus)
- **Output:** Abnahme-Ergebnis je Block dokumentiert; Findings nachgeschaerft

#### Schritt 6.3: kit-sync
- **Zweck:** globale Kopien aktualisieren
- **Dateien:** `~/.claude/` (via `/dtb:kit-sync`)
- **Input:** gepushter Stand
- **Output:** Lock aktualisiert, R=L=K verifiziert

> **3x3-Block:** Nach Schritt 6.3 → Abschluss + Feedback

### Deliverables
- [ ] Alle Bloecke abgenommen, global synchronisiert

### Checkpoint-Kriterien
- [ ] Kein Skill > 500 Zeilen; kein Frontmatter-Bruch
- [ ] Lock valides JSON, R=L=K

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Scope-Schnitt | 1 Feature / je Skill / nach Zweck | 1 Feature | Nutzer-Wahl 2026-07-09; Aenderungen gleichartig |
| roadmap-Rolle | read-only / Autoren-Skill | read-only | kollisionsfrei zu #11; Write = eigenes Feature |
| Handoff-Schreibrichtung | checkpoint schreibt / resume schreibt | checkpoint schreibt, resume liest | L1-Grounding: resume hat kein Write (`Read, Bash`) |
| Abnahme-Strategie | Fixture (wie SPEC/REVIEW) / Praxiserprobung | Report-Bloecke 1-3 Fixture, Session-Bloecke 4-5 Praxis | Review-Entscheidung 2026-07-09; Report-Verhalten fixture-pruefbar, Session-Verhalten nur im echten Zyklus |
| Discovery-Resume-Marker | YAML-Frontmatter / HTML-Kommentar | HTML-Kommentar | project-health konsumiert DISCOVERY_*.md — Kommentar wird nachweislich ignoriert (Review-Entscheidung) |
| „(Recommended)" in feature-discover | alle Fragen / nur Auswahlpunkte | nur Auswahlpunkte | Grounding: Klaerungsfragen sind Freitext, kein Optionsformat |
| Umsetzungs-Reihenfolge | frei | Report → Session | aufsteigender Blast-Radius; Session-Bloecke koppeln |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg.

- [x] 1.1 project-health A/B-Kategorisierung — `f9feef4`
- [x] 1.2 project-health WARN-AND-CONTINUE — `f9feef4`
- [x] 1.3 project-health Fixes mit Kommando/Aufwand — `f9feef4`
- [x] 2.1 debug-plan Hypothesen-Tabelle Evidenzstaerke — `06751ec`
- [x] 2.2 debug-plan „Framing war korrekt"-Ergebnis — `06751ec`
- [x] 3.1 greenfield-roadmap vertikale Slices — `06751ec`
- [x] 3.2 greenfield-roadmap Foundations/Unlocks — `37819f2`
- [x] 3.3 greenfield-roadmap Selbst-Review-Checkliste — `37819f2`
- [x] 4.1 feature-discover Resume-Marker (HTML-Kommentar) — `37819f2`
- [x] 4.2 feature-discover „(Recommended)" an Auswahlpunkten — `12f396c`
- [x] 5.1 checkpoint Handoff-Block (Sende-Seite) — `12f396c`
- [x] 5.2 resume Handoff-Aufnahme (Empfangs-Seite) — `12f396c`
- [ ] 6.1 Budget-/Frontmatter-Konsistenz-Check
- [ ] 6.2 Abnahme pro Block
- [ ] 6.3 kit-sync

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_SKILL_10X_OPTIMIERUNGEN.md` laden; der erste nicht abgehakte Schritt ist
der naechste. Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
