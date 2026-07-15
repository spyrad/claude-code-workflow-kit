# Implementierungsplan: Verifikations-Gate

**Erstellt:** 2026-07-15
**Feature-Spec:** `features/verifikations-gate/spec.md`
**Geschaetzte Dauer:** 3-4 Sessions
**Status:** Reviewed <!-- plan-review 2026-07-15: REVISE → 7 Punkte eingearbeitet -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Regel-Fundament: §2-Härtung in DERIVED_STATE_RULES | 0.5 Session | Geplant |
| Phase 2 | impl-plan: Automated/Manual-Kriterien + 3x3-Verweis | 0.5 Session | Geplant |
| Phase 3 | dtb:implement — Treiber-Skill mit Phasen-Ende-Ritual | 1-1.5 Sessions | Geplant |
| Phase 4 | Pipeline-Umbau: feature-start, build-check, code-review, workflow-checkpoint | 1 Session | Geplant |
| Phase 5 | Konsistenz-Sweep + Success-Criteria-Abgleich | 0.5 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (8 Module, Pfade verifiziert 2026-07-15) + Grep-Sweep `build-check`.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §2.7 „nach jedem Schritt sofort abhaken" + SHA-Beleg beim Abhaken — widerspricht dem Ziel-Ritual (Flip mid-phase ohne SHA, SHA beim Phasen-Commit) |
| `skills/dtb-implement/SKILL.md` | Existiert nicht (Neubau) |
| `skills/dtb-feature-start/SKILL.md` | `next: [dtb:build-check]` (Z. 14); Schritt 5 + „Wichtig" beschreiben 3x3 und Checkbox-Pflicht („sofort … mit Commit-SHA als Beleg") |
| `skills/dtb-build-check/SKILL.md` | Dünner Config-Wrapper (test_command/build_command je Repo) + FastWS-Event-Konsistenz-Check; `stage: development`, in der Feature-Pipeline |
| `skills/dtb-impl-plan/SKILL.md` | Template hat `### Checkpoint-Kriterien` pro Phase (Z. 148), aber ohne Automated/Manual-Trennung; Template enthält `## 3x3 Umsetzungsrhythmus`-Sektion |
| `skills/dtb-code-review/SKILL.md` | `after: [dtb:build-check]` (Z. 12) + Querverweis Z. 210 |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 2.3: „Abgenommen (getestet & freigegeben)" als nachweisfreie Auswahloption; Schritt 2.1 referenziert „Checkbox-Pflicht aus dtb:feature-start" |
| `skills/CLAUDE.md` | Hard-Gate-Tabelle v1 ohne implement; Pipeline-Konventionen |
| Weitere `build-check`-Referenzen (Grep) | Root-`CLAUDE.md` (Z. 38, 58), `dtb-pipeline-graph` (Beispiel-Ketten Z. 197-198), `dtb-project-health` (Z. 360), `dtb-workflow-status` (Z. 86, 176, 182, 204), `dtb-repo-sync` (Z. 88) |

**Inventur alte Wortlaute (1.3, Grep 2026-07-15)** — jede Fundstelle mit liefernder Phase:

| Fundstelle | Alter Wortlaut | Liefernde Phase |
|------------|----------------|-----------------|
| `skills/dtb-impl-plan/SKILL.md:164` | „sofort abhaken; Commit-SHA als Beleg" (Template-Blockquote) | 2.1 |
| `skills/dtb-impl-plan/SKILL.md:178` | „ab (Commit-SHA als Beleg)" (3x3-Sektion) | 2.3 |
| `skills/dtb-impl-plan/SKILL.md:228` | „SHA-Beleg kommt erst beim Abhaken dazu" (Anweisung 6) | 2.2 |
| `skills/dtb-feature-start/SKILL.md:133` | „ab (Commit-SHA als Beleg)" (3x3) | 4.1 |
| `skills/dtb-feature-start/SKILL.md:197` | „Nach JEDEM umgesetzten Schritt sofort … mit Commit-SHA als Beleg" | 4.1 |
| `skills/dtb-workflow-checkpoint/SKILL.md:187` | „Checkbox-Pflicht aus dtb:feature-start" | 4.3 |
| Root-`CLAUDE.md:38` | „check off … (with commit SHA) after each implemented step" | 4.5 |
| Root-`CLAUDE.md:107` | „commit SHA as evidence when checked" | 4.5 |
| `skills/CLAUDE.md:54` | „commit SHA as evidence" (Artifact-Tabelle) | 4.5 |
| `features/verifikations-gate/plan.md` (Progress-Blockquote) | „sofort abhaken; Commit-SHA als Beleg" | **1.3 (erledigt)** |

---

## Phase 1: Regel-Fundament (§2-Härtung)

### Ziel
`DERIVED_STATE_RULES.md` §2 trägt das Verifikations-Gate als Regel (Hybrid-Teil b), bevor der Skill existiert — widerspruchsfrei zu allen bestehenden Wortlauten.

### Schritte

#### Schritt 1.1: §2 Flip-Bedingung härten
- **Zweck:** Checkbox-Flip an grüne Checkpoint-Kriterien der Phase koppeln (Kern der Idee #19)
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** Spec Success Criteria 2, 10x-Vorbild „Verification Approach"
- **Output:** Neue Regel in §2: eine Checkbox darf erst geflippt werden, wenn die Checkpoint-Kriterien ihrer Phase (Automated) grün sind; Begriffe Automated/Manual eingeführt

#### Schritt 1.2: §2 SHA-Timing neu fassen + Multi-Repo-SHA-Regel
- **Zweck:** Mid-phase-Flip ohne SHA als gültigen Zwischenzustand definieren; SHA-Nachtrag beim Phasen-Commit (SHA = Verifikations-Beleg); Multi-Repo-Lücke schließen (Review-Empfehlung 2)
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** heutiges §2 Regel 3+7, 10x-Ritual Schritt 8-9, Review-Frage Senior Dev (2)
- **Output:** §2 Regeln 3/7 ersetzt; SHA-Format unverändert (` — ` + Inline-Code, 7 Zeichen); NEU: SHA pro Progress-Zeile stammt aus dem Repo des jeweiligen Schritts, mehrere SHAs pro Phase zulässig; bei Multi-Repo-Projekten optionales Repo-Präfix (`— repo-name@a1b2c3d`) — Format-Detail hier final entscheiden, Single-Repo bleibt unverändert

#### Schritt 1.3: Inventur alte Wortlaute + Plan-Header-Fix
- **Zweck:** Alle „sofort mit SHA abhaken"-Stellen erfassen (Risiko 5 der Spec) — OHNE Edits an Stellen, die Phase 2/4 strukturell ersetzen (kein Churn; Review-Empfehlung 5)
- **Dateien:** Inventur-Liste (nur dieser Plan, Sektion `## Ist-Analyse` ergänzen); Edit NUR am Progress-Blockquote von `features/verifikations-gate/plan.md` (Challenger-Befund 2: eigener Plan folgt ab jetzt neuem §2)
- **Input:** Grep „sofort" / „Commit-SHA als Beleg" über skills/ + CLAUDE.md
- **Output:** Fundliste mit Zuordnung (impl-plan-Stellen → 2.1/2.3, feature-start → 4.1, skills/CLAUDE.md → 4.5); eigener Progress-Blockquote §2-konform
- **Hinweis:** Zwischen Phase 1 und 4 tragen einzelne Skills bewusst noch alten Wortlaut — Abgleich-Kriterium liegt im Regressions-Sweep (5.1), nicht hier

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Gehärtetes §2 mit Flip-Bedingung + neuem SHA-Timing + Multi-Repo-SHA-Regel
- [ ] Inventur-Liste alter Wortlaute mit Phasen-Zuordnung; eigener Plan-Header konsistent

### Checkpoint-Kriterien

#### Automated
- [ ] §2 enthält die Begriffe „Automated", „Manual", die Flip-Bedingung und die Multi-Repo-SHA-Regel
- [ ] Progress-Blockquote dieses Plans enthält nicht mehr „sofort … Commit-SHA als Beleg" (alter Wortlaut)

#### Manual
- [ ] Neues §2 laut gelesen: kein Widerspruch zwischen Regel 3 (SHA optional), neuer Flip-Bedingung und SHA-Timing
- [ ] Inventur-Liste vollständig: jede Fundstelle hat eine liefernde Phase (2/4/5)

---

## Phase 2: impl-plan — Automated/Manual-Kriterien

### Ziel
`dtb:impl-plan` erzeugt Pläne, deren Checkpoint-Kriterien das Gate bedienen können (Skill prüft Automated, Mensch bestätigt Manual).

### Schritte

#### Schritt 2.1: Template-Sektion Checkpoint-Kriterien unterteilen
- **Zweck:** Das Gate braucht maschinell prüfbare vs. menschlich zu bestätigende Kriterien getrennt
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (Template)
- **Input:** 10x-Progress-Format (`#### Manual`-Subsections)
- **Output:** `### Checkpoint-Kriterien` mit Unterüberschriften `#### Automated` / `#### Manual` (Manual optional, wenn nichts manuell zu prüfen ist)

#### Schritt 2.2: Ausführungs-Anweisungen ergänzen
- **Zweck:** Kriterien müssen prüfbar formuliert sein, sonst ist das Gate leer
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (Abschnitt „Wichtig", Punkt 6)
- **Input:** Spec Success Criterion 3
- **Output:** Anweisung: jede Phase ≥1 Automated-Kriterium (konkret prüfbar: Kommando, Grep, Datei-Existenz); Manual nur für echte menschliche Urteile

#### Schritt 2.3: 3x3-Template-Sektion durch Verweis ersetzen
- **Zweck:** 3x3-Konsolidierung Teil 1 (Entscheidung T2) — Template-Sektion wird Kurzverweis auf `dtb:implement`
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (Template `## 3x3 Umsetzungsrhythmus`)
- **Input:** Entscheidung T2
- **Output:** Kompakte Sektion `## Umsetzung` (Verweis: „Umsetzung mit `/dtb:implement` — 3x3-Rhythmus + Phasen-Ende-Ritual, Wiedereinstieg über `## Progress`")

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] impl-plan-Template mit Automated/Manual-Kriterien und Umsetzungs-Verweis

### Checkpoint-Kriterien

#### Automated
- [ ] Template enthält `#### Automated` und `#### Manual` unter `### Checkpoint-Kriterien`
- [ ] Template enthält keine eigenständige 3x3-Beschreibung mehr (nur Verweis)

#### Manual
- [ ] Trockenlauf im Kopf: Aus einer Beispiel-Spec ließe sich ein Plan mit prüfbaren Automated-Kriterien erzeugen

---

## Phase 3: dtb:implement — Treiber-Skill

### Ziel
Der neue Skill treibt einen Plan phasenweise und erzwingt das Verifikations-Gate am Phasen-Ende (Hybrid-Teil a) — die eine Quelle für den 3x3-Rhythmus.

### Schritte

#### Schritt 3.1: Skill-Gerüst + Frontmatter
- **Zweck:** Skill existiert mit korrekter Pipeline-Position und Konventionen
- **Dateien:** `skills/dtb-implement/SKILL.md` (NEU)
- **Input:** skills/CLAUDE.md Frontmatter-Konventionen, Entscheidung T4
- **Output:** Frontmatter (`stage: implementation`, `after: [dtb:feature-start]`, `next: [dtb:code-review]`, `consumes: [features/*/plan.md, features/*/spec.md, project-rules/DERIVED_STATE_RULES.md, workflow.config.yaml]`, `produces: [features/*/plan.md]`, `disable-model-invocation: true`, `argument-hint`); Grundstruktur (Config laden, Slug ermitteln)

#### Schritt 3.2: Einstieg, Hard-Gate, Wiedereinstieg
- **Zweck:** Konstruktive Weigerung ohne Plan; abgeleiteter Einstieg statt Sidecar
- **Dateien:** `skills/dtb-implement/SKILL.md`
- **Input:** Eligibility-Gate-Konvention (skills/CLAUDE.md), §1.4-Fallbacks
- **Output:** Hard-Gate (kein `plan.md` → Redirect `/dtb:impl-plan` + Escape-Hatch); Archiv-Weigerung (`archive/<slug>/` → „neuen Change starten"); `plan.md` ohne `## Progress` → Nachrüstung anbieten; Einstieg = erster nicht abgehakter Progress-Schritt (optional `phase N`-Argument); **Alt-Plan-Fallback** (Review-Empfehlung 1, konsistent mit §1.4 „kein Fallback führt zum Abbruch"): Checkpoint-Kriterien fehlen oder sind nicht Automated/Manual-geteilt → ALLE Kriterien als Manual behandeln (Gate bleibt, Mensch bestätigt) + Nachrüstung anbieten — das Gate läuft nie leer durch

#### Schritt 3.3: Umsetzungs-Loop (3x3 als eine Quelle)
- **Zweck:** Der Loop, den feature-start heute nur ankündigt, wird hier ausgeführt
- **Dateien:** `skills/dtb-implement/SKILL.md`
- **Input:** 3x3-Beschreibung aus feature-start/impl-plan (kanonische Fassung hierher), 10x „Implementation Philosophy"
- **Output:** 3x3-Rhythmus (max. 3 Schritte → Zusammenfassung → Feedback); Flip mid-phase ohne SHA; Mismatch-Handling (stoppen, Erwartet/Gefunden/Warum zeigen, fragen: anpassen / überspringen / neu planen); Phase-Blöcke read-only, nur `## Progress` wird mutiert

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Phasen-Ende-Ritual
- **Zweck:** Das eigentliche Verifikations-Gate — SHA wird Verifikations-Beleg
- **Dateien:** `skills/dtb-implement/SKILL.md`
- **Input:** 10x-Ritual (Schritte 1-11), gehärtetes §2 (Phase 1), Entscheidung T3-Schnittstelle
- **Output:** Sequenz: (1) Automated-Kriterien der Phase prüfen — rot → fixen, nicht weiter (Alt-Plan-Fallback aus 3.2: ungeteilte/fehlende Kriterien → alle als Manual); (2) manuelles Gate: Manual-Kriterien listen, auf Bestätigung warten; (3) berührte Dateien explizit stagen (kein `git add -A`), fremde dirty paths melden + fragen; (4) Commit (nie `--force`/`--no-verify`/`--amend`) — **shell-agnostisch** (Review-Empfehlung 3): Bash-heredoc als Standard, ein Satz Hinweis für PowerShell-Kontexte (Here-String `@'…'@`); (5) Kurz-SHA in alle in der Phase geflippten Progress-Zeilen (` — ` + Inline-Code, Multi-Repo-Regel aus 1.2; leerer Diff → Zeilen bleiben SHA-los, Hinweis)

#### Schritt 3.5: Multi-Repo + Abschluss-Verhalten
- **Zweck:** DTB-Besonderheit gegenüber 10x (config.repos) und sauberes Ende
- **Dateien:** `skills/dtb-implement/SKILL.md`
- **Input:** `workflow.config.yaml` repos-Schema, Spec „Nicht enthalten" (kein Autonomie-Modus)
- **Output:** Checks/Commit im Repo des jeweiligen Schritts (bei einem Repo: still); nach letzter Phase: Rest-Scan auf offene Checkboxen + Hinweis auf `/dtb:workflow-checkpoint`; Abgrenzungs-Hinweise zu #20/#21 als Kommentar

> **3x3-Block:** Nach Schritt 3.5 (2er-Block) → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-implement/SKILL.md` vollständig (Gerüst, Gates, Loop, Ritual, Multi-Repo)

### Checkpoint-Kriterien

#### Automated
- [ ] Frontmatter vollständig + konventionskonform (name/description/pipeline nach skills/CLAUDE.md)
- [ ] SKILL.md enthält: Hard-Gate-Block, Archiv-Weigerung, Mismatch-Block, Ritual-Sequenz mit SHA-Rückschreibung
- [ ] Grep: keine verbotenen Git-Flags als Anweisung (`--force`, `--no-verify`, `--amend` nur in Verbotsform)

#### Manual
- [ ] Ritual-Trockenlauf: Phasen-Ende an einem fiktiven 2-Schritte-Beispiel durchgespielt — Reihenfolge und Gate-Stopps fühlen sich schlank an (Risiko 4: eine Bestätigung pro Phase)

---

## Phase 4: Pipeline-Umbau + Nachbar-Skills

### Ziel
Die Pipeline führt über `implement`; build-check ist entkernt und neu positioniert; die Abnahme verlangt einen Beleg.

> **Selbst-Test (Review-Empfehlung 4):** Phase 4 und 5 dieses Plans werden MIT dem in Phase 3
> gebauten `dtb:implement` umgesetzt (Repo-Kopie `skills/dtb-implement/SKILL.md` direkt befolgen —
> keine Distribution nötig). Echter Testlauf statt Trockenlauf: inkl. Phasen-Ende-Ritual,
> SHA-Rückschreibung und — via bewusst herbeigeführtem Test — dem Alt-Plan-Fallback.
> Erkenntnisse fließen als Fixes in Phase 5 bzw. als Lektion-Kandidaten.

### Schritte

#### Schritt 4.1: feature-start umbauen
- **Zweck:** Übergabe an implement statt an das übersprungene build-check
- **Dateien:** `skills/dtb-feature-start/SKILL.md`
- **Input:** Entscheidung T2/T4
- **Output:** `next: [dtb:implement]`; Schritt 5 + „Wichtig": 3x3-Vollbeschreibung durch Kurzverweis auf `dtb:implement` ersetzt; Abschluss-Zeile „Bereit? → `/dtb:implement {slug}`"

#### Schritt 4.2: build-check entkernen/neu positionieren
- **Zweck:** Verifikation wohnt jetzt im Loop; Restfunktion bewusst verorten (Entscheidung T1)
- **Dateien:** `skills/dtb-build-check/SKILL.md`
- **Input:** Entscheidung T1
- **Output:** Neupositionierung als Stand-alone Multi-Repo-„deploy-ready"-Check: `stage: monitoring`, `after: null`, `next: null`; Beschreibung geschärft (Sammel-Check vor Deploy/Release, NICHT Teil des Feature-Loops); Event-Konsistenz-Check (Schritt 3) entfernt, im Skill-Text als Projekt-Rule-Kandidat erwähnt

#### Schritt 4.3: code-review + workflow-checkpoint Verweise umziehen
- **Zweck:** Keine toten Pipeline-Kanten
- **Dateien:** `skills/dtb-code-review/SKILL.md`, `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Grep-Befund (Ist-Analyse)
- **Output:** code-review `after: [dtb:implement]` + Querverweis Z. 210 angepasst; workflow-checkpoint Schritt 2.1: „Checkbox-Pflicht aus dtb:implement" (statt feature-start)

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

#### Schritt 4.4: Abnahme-Härtung in workflow-checkpoint
- **Zweck:** „Fertig zum Testen" → „Abgenommen" verlangt einen Beleg (letzter Teil der Gate-Lücke)
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 2.3)
- **Input:** Entscheidung T3
- **Output:** Bei Wahl „Abgenommen": Rückfrage nach Beleg — offene Manual-Kriterien aus dem Plan listen („Diese manuellen Prüfungen sind offen/bestätigt?"), 1-Zeilen-Beleg in den Session-Log; ohne Antwort bleibt „Fertig zum Testen"

#### Schritt 4.5: Doku- und Übersichts-Stellen aktualisieren
- **Zweck:** Grep-Befund abarbeiten — Übersichten dürfen build-check nicht mehr als Pipeline-Schritt führen
- **Dateien:** Root-`CLAUDE.md` (Z. 38, 58), `skills/CLAUDE.md` (Hard-Gate-Tabelle + implement-Zeile, Pipeline-Beschreibung), `skills/dtb-pipeline-graph/SKILL.md` (Beispiel-Ketten Z. 197-198), `skills/dtb-workflow-status/SKILL.md` (Z. 86, 176, 182, 204), `skills/dtb-project-health/SKILL.md` (Z. 360), `skills/dtb-repo-sync/SKILL.md` (Z. 88)
- **Input:** Ist-Analyse Grep-Zeilen
- **Output:** Ketten zeigen `feature-start → implement → code-review`; Hard-Gate-Tabelle: implement | `features/*/plan.md` | Redirect `impl-plan`; workflow-status-Aktionen zeigen auf `/dtb:implement`; build-check-Verweise nur noch als Deploy-Check

### Deliverables
- [ ] Konsistente Pipeline über implement, build-check neu positioniert, Abnahme mit Beleg-Rückfrage

### Checkpoint-Kriterien

#### Automated
- [ ] Grep `build-check` über `skills/` + `CLAUDE.md`: kein Treffer mehr in Pipeline-Ketten/`after`/`next` (nur noch Deploy-Check-Kontext + eigener Skill)
- [ ] Grep `dtb:implement`: feature-start.next, code-review.after, Hard-Gate-Tabelle, pipeline-graph-Ketten vorhanden

#### Manual
- [ ] Abnahme-Rückfrage-Dialog einmal durchgespielt (Wahl „Abgenommen" mit und ohne Beleg)

---

## Phase 5: Konsistenz-Sweep + Abgleich

### Ziel
Nichts zeigt mehr auf alte Zustände; jedes Success Criterion der Spec ist belegt.

### Schritte

#### Schritt 5.1: Repo-weiter Konsistenz-Sweep
- **Zweck:** Reste finden, die die Greps der Phasen nicht abdeckten
- **Dateien:** alle `skills/*/SKILL.md`, `commands/`, `agents/`, beide `CLAUDE.md`
- **Input:** Inventur-Liste aus 1.3, Greps: „3x3" (nur noch eine Vollbeschreibung), „sofort" + „SHA", „build-check", „Fertig zum Testen"
- **Output:** Fundliste abgearbeitet oder als bewusst-belassen dokumentiert; **hier gilt das aus Phase 1 verschobene Kriterium:** Grep „sofort abhaken"/„sofort die Checkbox" über `skills/` + `dtb-project/project-rules/` liefert nur noch §2-konforme Stellen (alle Inventur-Stellen von 2.1/2.3/4.1/4.5 geliefert)

#### Schritt 5.2: Success-Criteria-Abgleich + Seed-Hinweis
- **Zweck:** Spec-Abnahmegrundlage schaffen; Risiko 2 (Seed erreicht Bestandsprojekte nicht) dokumentieren
- **Dateien:** `features/verifikations-gate/spec.md` (Abgleich-Notiz unter Success Criteria zulässig als Kommentar), Session-Log via `/dtb:workflow-checkpoint`
- **Input:** Spec Success Criteria 1-9
- **Output:** Jedes SC mit Beleg (Datei/Grep) gemappt; Hinweis dokumentiert: Bestandsprojekte erhalten §2-Härtung erst durch manuelles Update/`project-init` (bewusst akzeptiert; aktive Seed-Skew-Meldung ist INBOX #22, nicht Teil dieses Features); Verteilung der Klasse-A-Artefakte via `/dtb:kit-sync`

> **3x3-Block:** Nach Schritt 5.2 (2er-Block) → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Sweep-Ergebnis dokumentiert, SC1-9 belegt

### Checkpoint-Kriterien

#### Automated
- [ ] Alle Phase-1-bis-4-Greps erneut grün (Regression)
- [ ] Wortlaut-Grep (aus Phase 1 verschoben): keine „sofort … mit SHA"-Altbestände mehr in `skills/` + `dtb-project/project-rules/`

#### Manual
- [ ] SC-Mapping gelesen: kein Kriterium ohne Beleg
- [ ] Selbst-Test-Erkenntnisse aus Phase 4/5 dokumentiert (Session-Log oder Lektion)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| T1: build-check-Restfunktionen | A: Skill streichen; B: Neupositionierung als Stand-alone Deploy-Check (Event-Check raus); C: unverändert lassen | B (bestätigt 2026-07-15, plan-review) | Multi-Repo-„deploy-ready" ist für pkp real nützlich, gehört aber nicht in den Feature-Loop; FastWS-Event-Check ist projektspezifisch → Projekt-Rule-Kandidat, kein Kit-Skill |
| T2: 3x3-Quelle | A: implement; B: feature-start behält Volltext; C: DERIVED_STATE_RULES | A (Vorschlag) | Der Skill, der den Loop AUSFÜHRT, trägt seine Beschreibung; feature-start/impl-plan-Template verweisen nur — ein Ort, kein Drift |
| T3: Beleg-Rückfrage „Abgenommen" | A: Freitext-Beleg; B: offene Manual-Kriterien des Plans listen + bestätigen lassen, 1-Zeilen-Beleg in Session-Log | B (Vorschlag) | Nutzt die in Phase 2 geschaffene Manual-Struktur; konkreter als Freitext, leichter als eigenes Artefakt |
| T4: Pipeline-Position implement | A: after feature-start, next code-review; B: implement ersetzt feature-start | A | feature-start bleibt Auswahl-/Aktivierungs-Skill (Backlog→In Arbeit), implement ist der Umsetzungs-Treiber — getrennte Verantwortungen |
| T5: SHA-Timing in §2 | A: heutiges „sofort mit SHA"; B: Flip ohne SHA mid-phase, SHA beim Phasen-Commit | B | SHA soll Verifikation belegen, nicht bloß Commits; ein Commit pro Phase entspricht dem Ritual (10x-Vorbild) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 §2 Flip-Bedingung härten
- [x] 1.2 §2 SHA-Timing neu fassen
- [x] 1.3 Inventur alte Wortlaute + Plan-Header-Fix
- [ ] 2.1 Checkpoint-Kriterien Automated/Manual
- [ ] 2.2 Anweisungen: prüfbare Kriterien
- [ ] 2.3 3x3-Template-Sektion → Verweis
- [ ] 3.1 implement: Gerüst + Frontmatter
- [ ] 3.2 implement: Einstieg + Hard-Gate + Wiedereinstieg
- [ ] 3.3 implement: Umsetzungs-Loop (3x3-Quelle)
- [ ] 3.4 implement: Phasen-Ende-Ritual
- [ ] 3.5 implement: Multi-Repo + Abschluss
- [ ] 4.1 feature-start umbauen
- [ ] 4.2 build-check entkernen/neu positionieren
- [ ] 4.3 code-review + checkpoint Verweise
- [ ] 4.4 Abnahme-Härtung workflow-checkpoint
- [ ] 4.5 Doku-/Übersichts-Stellen
- [ ] 5.1 Konsistenz-Sweep
- [ ] 5.2 SC-Abgleich + Seed-Hinweis

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/verifikations-gate/plan.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

> Hinweis: Ab Phase 1 dieses Plans gilt das gehärtete §2 (Flip-Bedingung + SHA-Timing) auch für
> die Umsetzung DIESES Plans — der Plan verifiziert sich ab dann selbst nach der neuen Regel.

---

**Erstellt mit:** `/dtb:impl-plan`
