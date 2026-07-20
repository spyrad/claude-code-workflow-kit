# Feature: Verifikations-Gate

**Erstellt:** 2026-07-15
**Ziel:** Der Umsetzungs-Loop erhält ein echtes Verifikations-Gate — eine Progress-Checkbox darf erst flippen, wenn die Checkpoint-Kriterien der Phase grün sind, und die Commit-SHA wird damit vom Commit-Beleg zum Verifikations-Beleg.
**Prioritaet:** Hoch
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Pipeline definiert `feature-start → build-check → code-review → checkpoint`, aber die Praxis
überspringt beide Gates: Nach `feature-start` treibt kein Skill die Umsetzung, Abhaken ist ein
Ehrensystem, und „Fertig zum Testen" → „Abgenommen" verlangt keinerlei Test-Nachweis. Dieses
Feature schließt die Lücke nach dem 10x-Vorbild (`10x-implement` „Verification Approach"):
ein neuer Treiber-Skill `dtb:implement` führt den Plan phasenweise aus und erzwingt am Phasen-Ende
ein Ritual (Kriterien prüfen → manuelle Bestätigung → Commit → SHA-Rückschreibung), flankiert von
einer Härtung der Regel §2 in `DERIVED_STATE_RULES.md` (Hybrid: der Skill führt das Gate aus,
die Regel begründet es).

---

## Scope / Abgrenzung

### Enthalten

- **Neuer Skill `dtb:implement`** (Träger-Entscheidung: Variante a als Hybrid): liest
  `features/{slug}/plan.md`, Einstieg = erster nicht abgehakter `## Progress`-Schritt
  (abgeleitet, kein Sidecar), setzt phasenweise im 3x3-Rhythmus um
- **Phasen-Ende-Ritual** nach 10x-Vorbild: Checkpoint-Kriterien der Phase prüfen → manuelles
  Bestätigungs-Gate (Mensch bestätigt manuelle Prüfungen) → Commit → SHA-Rückschreibung in
  genau die in der Phase geflippten Progress-Zeilen
- **Regel-Härtung** `DERIVED_STATE_RULES.md` §2: Checkbox-Flip erst bei grünen
  Checkpoint-Kriterien; SHA-Timing an das Ritual angepasst (Flip mid-phase ohne SHA ist gültiger
  Zwischenzustand, SHA kommt beim Phasen-Commit)
- **`dtb:impl-plan`-Anpassung:** Checkpoint-Kriterien in **Automated/Manual** trennen, damit das
  Gate weiß, was der Skill selbst prüft und was der Mensch bestätigen muss
- **`dtb:build-check` entkernen:** Verifikation wandert in den Umsetzungs-Loop; Verbleib der
  Restfunktionen wird im Implementierungsplan entschieden (siehe Offene Punkte)
- **Abnahme-Härtung in `dtb:workflow-checkpoint`:** Die Auswahloption „Abgenommen" erhält eine
  Beleg-Rückfrage statt heute nachweisfreiem Checkbox-Flip
- **Pipeline-Folgeänderungen:** `feature-start` übergibt an `implement` statt `build-check`;
  Verweise in `code-review` (Vorgänger) und `workflow-checkpoint` (Checkbox-Pflicht-Referenz)
  ziehen um; Hard-Gate-Tabelle in `skills/CLAUDE.md` wird um `implement` erweitert

### Nicht enthalten

- **Kein vollautonomer Durchlauf** — das manuelle Bestätigungs-Gate bleibt in jedem Fall bestehen
- **Keine Ablösung von `dtb:code-review`** — das ist Idee #20 (`dtb:impl-review`); hier ziehen nur
  Pipeline-Verweise um
- **Kein Eingriff in `dtb:plan-review`** — anderes Objekt (Plan, nicht Code)
- **Kein Routine-Commit-Werkzeug** — das ist Idee #21 (`dtb:commit-and-push`); das Ritual hier ist
  ausschließlich der Phasen-Abschluss, #21 bleibt als Routine-Pfad daneben denkbar

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| 3x3-Rhythmus-Beschreibung driftet (heute 2 Orte: `feature-start`, `impl-plan`-Template; mit `implement` ein dritter) | Hoch | Mittel | Eine Quelle festlegen (Konsolidierung im Plan entscheiden), andere Orte verweisen nur |
| §2-Härtung erreicht Bestandsprojekte nicht (`DERIVED_STATE_RULES.md` ist Seed, wird nie drift-geprüft) | Hoch | Mittel | Bewusst akzeptieren + im Plan dokumentieren; Bestandsprojekte aktualisieren die Datei manuell oder via erneutem `project-init` |
| `dtb:implement` wird zu groß/komplex (10x-Vorbild ist sehr umfangreich) | Mittel | Mittel | Auf DTB-Kern reduzieren (Ritual + 3x3 + Gate), Nebenpfade des Vorbilds weglassen; Skill-Konventionen einhalten |
| Ritual fühlt sich im Alltag zu schwer an → wird umgangen (gleiche Lücke wie heute) | Mittel | Hoch | Ritual schlank halten (eine Bestätigung pro Phase, nicht pro Schritt); Escape-Hatch bewusst dokumentieren statt stilles Umgehen |
| Widerspruch zwischen gehärtetem §2 und altem Skill-Wortlaut (`feature-start` „sofort mit SHA") | Hoch | Niedrig | Alle Wortlaut-Stellen im Plan als eigene Schritte führen (verifizierte Fundliste liegt in der Discovery vor) |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine — alle betroffenen Artefakte liegen im Kit; kein Vorläufer-Feature offen

### Referenz-Dokumente

- `features/verifikations-gate/discovery.md` - Verifizierte Fundliste (8 betroffene Module mit Zeilenbelegen), Randfälle, Abgrenzungen
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - §2 Progress-Format (Härtungs-Gegenstand), §1.4 Fallbacks
- `10x-devs-3.0/.claude/skills/10x-implement/SKILL.md` - Vorbild: „Verification Approach", Phasen-Ende-Ritual, SHA-Rückschreibung
- `skills/CLAUDE.md` - Eligibility-Gates-Konvention, Hard-Gate-Tabelle v1, Skill-Konventionen
- `dtb-project/project-workflows/INBOX.md` - Ideen #19 (dieses Feature), #20/#21 (Abgrenzung)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] `dtb:implement` existiert und treibt einen Plan phasenweise: Einstieg über ersten offenen
      Progress-Schritt, 3x3-Rhythmus, Phasen-Ende-Ritual mit manueller Bestätigung und
      SHA-Rückschreibung in die geflippten Zeilen
- [ ] Eine Progress-Checkbox gilt regelseitig (§2) erst als flippbar, wenn die
      Checkpoint-Kriterien der Phase grün sind; das SHA-Timing (mid-phase ohne SHA, Nachtrag beim
      Phasen-Commit) ist in §2 beschrieben und widerspruchsfrei zu allen Skill-Wortlauten
- [ ] `dtb:impl-plan` erzeugt Checkpoint-Kriterien getrennt nach Automated/Manual
- [ ] `dtb:implement` verweigert konstruktiv bei fehlendem `plan.md` (Hard-Gate mit Redirect
      `impl-plan` + Escape-Hatch) und bei archivierten Changes
- [ ] Randfälle definiert: Plan≠Realität (stoppen + fragen), Phase ohne Commit (SHA-los erlaubt),
      `plan.md` ohne `## Progress` (Nachrüstung anbieten), fremde dirty paths beim Phasen-Commit
      (melden + fragen, nie still mitbündeln)
- [ ] `dtb:build-check` ist entkernt und die Restfunktionen sind bewusst verortet (Entscheidung
      dokumentiert)
- [ ] `dtb:workflow-checkpoint` stellt bei „Abgenommen" eine Beleg-Rückfrage
- [ ] Pipeline konsistent: `feature-start.next` → `implement`; kein Skill-Frontmatter und keine
      Querverweise zeigen mehr auf entkernte/verschobene Funktionen; Hard-Gate-Tabelle erweitert
- [ ] Die 3x3-Beschreibung hat genau eine Quelle, andere Stellen verweisen

---

## Offene Punkte

- ~~build-check-Restfunktionen~~ → entschieden (T1-B, plan-review 2026-07-15): Stand-alone
  Deploy-Readiness-Check; Event-Check entfernt, als Projekt-Rule-Kandidat im Skill dokumentiert
- ~~3x3-Konsolidierung~~ → entschieden (T2): `dtb:implement` ist die eine Quelle;
  feature-start + impl-plan-Template verweisen
- ~~Beleg-Rückfrage~~ → entschieden (T3): Manual-Kriterien des Plans listen + 1-Zeilen-Beleg
  in den Session-Log; ohne Beleg bleibt „Fertig zum Testen"

<!-- SC-Abgleich 2026-07-15 (Schritt 5.2, alle Belege verifiziert):
SC1 implement existiert/treibt: skills/dtb-implement/SKILL.md Schritte 2-4; real erprobt an Phase 4+5 dieses Plans (Selbst-Test)
SC2 §2 widerspruchsfrei: DERIVED_STATE_RULES.md §2 Regeln 3/4/5; Sweep-Grep alte Wortlaute = 0 Treffer
SC3 Automated/Manual in impl-plan: Template Z.150/153 + Pflicht-Anweisung (>=1 Automated je Phase)
SC4 Hard-Gate + Archiv-Weigerung: implement Schritt 1 (Archiv, ohne Escape-Hatch) + Eligibility-Gate (Redirect impl-plan)
SC5 Randfaelle: Mismatch-Block (Schritt 3), leerer Diff (Ritual 5), Progress-Nachruestung (Schritt 2.2), dirty paths (Ritual 3), Alt-Plan-Fallback (Schritt 2.4)
SC6 build-check entkernt/verortet: stage monitoring, after/next null, Event-Check -> Projekt-Rule-Hinweis im Skill (T1-B)
SC7 Beleg-Rueckfrage: workflow-checkpoint Schritt 2.3 (kein stilles Durchwinken)
SC8 Pipeline konsistent: Greps p4 (build-check nur Deploy-Kontext; implement in feature-start.next, code-review.after, Ketten, Hard-Gate-Tabelle) + Sweep p5 (workflow-next/checkpoint-Handoff)
SC9 3x3 eine Quelle: Sweep-Grep = 1 Vollbeschreibung (implement), Rest Verweise/Autoren-Konvention; features/-Laufzeitplaene per Scope-Entscheidung ausgenommen (historische Belegplaene, bewusst kein Churn)
Seed-Hinweis: Die Paragraph-2-Haertung erreicht Bestandsprojekte NICHT automatisch (Seed, Klasse B) — manuelles Update oder project-init; aktive Meldung = INBOX #22. Verteilung der Klasse-A-Artefakte (implement NEU + 8 geaenderte): /dtb:kit-sync nach Abnahme. -->

Aktuell offen: — keine —

---

**Erstellt mit:** `/dtb:feature-plan`
