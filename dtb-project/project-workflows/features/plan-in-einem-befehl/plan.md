# Implementierungsplan: Plan in einem Befehl

**Erstellt:** 2026-11-09
**Feature-Spec:** `features/plan-in-einem-befehl/spec.md`
**Geschaetzte Dauer:** ca. 2–3 h
**Status:** Reviewed (plan-review 2026-11-09: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | feature-plan umbauen (Referenz-Ausführung von impl-plan, Stopp-Weiche, Frontmatter) | ca. 1–1,5 h | Geplant |
| Phase 2 | Doku nachziehen, Probelauf, Konsistenz-Sweep | ca. 1–1,5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` `## Betroffene Module` (alle Pfade per Glob verifiziert 2026-11-09).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-feature-plan/SKILL.md` | 275 Zeilen; Frontmatter `next: [dtb:impl-plan]`, `produces` ohne `features/*/plan.md`, `argument-hint: "[Feature-Name]"`; Ausführung Schritte 1–11, Spec gespeichert in Schritt 8, INBOX/BACKLOG in 9/10 (Teil-Guard), Abschluss in 11 nennt impl-plan → plan-review → feature-start; Anker `## Template fuer spec.md` und `## Technical-Leak-Lint` werden von feature-fast gelesen |
| `skills/dtb-impl-plan/SKILL.md` | 284 Zeilen; Sektionen `## Lektionen als Prior lesen`, `## Eligibility-Gate`, `## Codebase-Research (Ist-Analyse)`, `## Template fuer plan.md` (Wartungs-Hinweis für feature-fast), `## Wichtig - Anweisungen fuer die Ausfuehrung`, `## Lektion-Kandidat erkennen`; gleiche Werkzeuge wie feature-plan |
| `CLAUDE.md` | Zeile 39 (Lebenszyklus „Work") und Zeile 54 („Feature workflow") führen feature-plan und impl-plan als getrennte Schritte |
| `README.md` | Zeile 76: `/dtb:feature-plan` — „Create structured feature specifications (with inbox integration)" |
| `skills/dtb-feature-discover/SKILL.md` | Zeile 278: `Naechster Schritt: /dtb:feature-plan {Feature-Name}` |

---

## Phase 1: feature-plan umbauen

### Ziel
`dtb:feature-plan` erzeugt nach der Spec den Implementierungsplan durch Referenz-Ausführung von `dtb:impl-plan`, abgesichert per Struktur-Check, mit Stopp-Weiche „nur spec.md" und Abschluss je Ausgang.

### Schritte

#### Schritt 1.1: Stopp-Weiche und Frontmatter
- **Zweck:** Aufrufform und maschinell gelesene Pipeline-Wahrheit festlegen (Lektion 44)
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`
- **Input:** Spec (Scope), Discovery (Gewünschtes Verhalten)
- **Output:** `argument-hint: "[Feature-Name] [nur-spec]"`; `next: [dtb:plan-review, dtb:impl-plan]`; `consumes` + `project-rules/lessons.md`, `project-rules/DERIVED_STATE_RULES.md`; `produces` + `features/*/plan.md`; `description` um den Plan-Teil ergänzt; Einleitung + `## Aufgabe` nennen beide Ausgänge; Stopp-Regel: Argument `nur-spec` oder ausdrücklicher Wunsch „nur spec" im Aufruftext → nach der Spec enden; ohne Angabe läuft der Plan immer mit, keine Rückfrage

#### Schritt 1.2: Neuer Ausführungsschritt „Implementierungsplan mitlaufen lassen"
- **Zweck:** Kern des Features — Referenz-Ausführung statt Kopie
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`
- **Input:** Muster `dtb:feature-fast` Schritt 2 (Struktur-Check, zwei getrennte Fehlerpfade)
- **Output:** neuer Punkt `8a.` direkt nach Punkt 8 „Speichere die Datei" (vor INBOX/BACKLOG) — bewusst ohne Neunummerierung, damit die Verweise auf Punkt 9/10/11 (feature-plan intern, `dtb:feature-fast` „analog feature-plan Schritt 10", `skills/CLAUDE.md` Zeile Z3) gültig bleiben; enthält: (a) Stopp-Weiche; (b) Struktur-Check vor der ersten Nutzung (Lektion 89) auf alle fünf genutzten Anker `## Lektionen als Prior lesen`, `## Codebase-Research (Ist-Analyse)`, `## Template fuer plan.md`, `## Wichtig - Anweisungen fuer die Ausfuehrung`, `## Lektion-Kandidat erkennen (Vorschlager)` (Eligibility-Gate ist im selben Lauf erfüllt und wird nicht genutzt, daher kein Anker) — Auflösung installierte Kopie, sonst Repo-Fallback; Pfad 1 „Datei fehlt" → kit-sync-Hinweis, Pfad 2 „Anker fehlt" → Drift-Meldung; beide: Spec bleibt gültig, Plan-Teil entfällt, Abschluss mit `→ Weiter mit: /dtb:impl-plan {Name}`; (c) Ausführung: die impl-plan-Abschnitte per Name (nie per Punktnummer) mit demselben Slug anwenden — `## Lektionen als Prior lesen`, `## Codebase-Research (Ist-Analyse)`, aus `## Wichtig - Anweisungen fuer die Ausfuehrung` alles ausser der Slug-Ermittlung und der eigenen Bestätigung (Planerstellung nach `## Template fuer plan.md`), `## Lektion-Kandidat erkennen (Vorschlager)`; das Eligibility-Gate ist im selben Lauf erfüllt und entfällt still; Überschreib-Frage bei vorhandenem `plan.md` bleibt; `plan.md` behält die impl-plan-Fusszeile

#### Schritt 1.3: Backlog-Status, Abschluss je Ausgang, Wartungs-Hinweise in impl-plan
- **Zweck:** Anzeige und Abschluss passen zum tatsächlichen Ergebnis; Kopplung an der Quelle sichtbar
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-impl-plan/SKILL.md`
- **Input:** `DERIVED_STATE_RULES.md` (Spec + Plan, 0 Haken = Geplant)
- **Output:** BACKLOG-Schritt: Status `Geplant` bei Durchlauf, `Spezifiziert` bei Stopp oder ausgefallenem Plan-Teil (Anzeige-Zeile `→ in BACKLOG.md eingetragen (Status: {Status})`); Abschluss mit zwei Varianten — Durchlauf: beide Pfade + `Naechster Schritt: /dtb:plan-review {Feature-Name}`; nur Spec: `Naechster Schritt: /dtb:impl-plan {Feature-Name}`; in `dtb-impl-plan/SKILL.md` an den fünf Anker-Sektionen je ein Wartungs-Hinweis mit dem Wortlaut „von `dtb:feature-plan` per Referenz ausgefuehrt"

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-feature-plan/SKILL.md` mit Stopp-Weiche, Referenz-Schritt, Backlog-Status je Ausgang und zwei Abschluss-Varianten
- [ ] `skills/dtb-impl-plan/SKILL.md` mit fünf Wartungs-Hinweisen für den zweiten Referenz-Leser

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE "^  next: \[dtb:plan-review, dtb:impl-plan\]" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] `grep -cE "^  produces: .*features/\*/plan\.md" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] `grep -cE "^  consumes: .*project-rules/lessons\.md" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] `grep -cE "^argument-hint: .*nur-spec" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] Die fünf Struktur-Anker stehen woertlich im neuen Schritt: je `grep -cF` auf `"## Lektionen als Prior lesen"`, `"## Codebase-Research (Ist-Analyse)"`, `"## Template fuer plan.md"`, `"## Wichtig - Anweisungen fuer die Ausfuehrung"`, `"## Lektion-Kandidat erkennen (Vorschlager)"` in `skills/dtb-feature-plan/SKILL.md` ≥ 1 — und dieselben fünf Anker per `grep -c "^…"` in `skills/dtb-impl-plan/SKILL.md` je = 1 (Quelle unverändert)
- [ ] Nummern stabil: in `skills/dtb-feature-plan/SKILL.md` je = 1 für `grep -cE "^8a\. "`, `grep -cE "^9\. \*\*Inbox-Status aktualisieren"`, `grep -cE "^10\. \*\*Backlog-Eintrag"`, `grep -cE "^11\. \*\*Bestaetige"`; Fremdverweise unverändert: `grep -c "analog feature-plan Schritt 10" skills/dtb-feature-fast/SKILL.md` = 1 und `grep -c "^| 3 | \`feature-plan\` Schritt 10" skills/CLAUDE.md` = 1
- [ ] `grep -c "Naechster Schritt: /dtb:plan-review" skills/dtb-feature-plan/SKILL.md` = 1 und `grep -c "Naechster Schritt: /dtb:impl-plan" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] `grep -c "von \`dtb:feature-plan\` per Referenz ausgefuehrt" skills/dtb-impl-plan/SKILL.md` = 5
- [ ] feature-fast-Anker in feature-plan unverändert: `grep -c "^## Template fuer spec.md" skills/dtb-feature-plan/SKILL.md` = 1 und `grep -c "^## Technical-Leak-Lint" skills/dtb-feature-plan/SKILL.md` = 1
- [ ] impl-plan bekommt nur Hinweis-Zeilen (Beleg für „impl-plan allein unverändert"): `git diff $(git merge-base master HEAD) -- skills/dtb-impl-plan/SKILL.md | grep -E "^[-+]" | grep -vE "^(\+\+\+|---) " | grep -vcE "^\+(>|$)"` = 0 (Leerzeilen um neue Hinweis-Blöcke zulässig — angepasst per Mismatch-Entscheid 2026-11-09)
- [ ] Backlog-Zweig kennt beide Ausgänge: `awk '/^10\. \*\*Backlog-Eintrag/,/^11\. /' skills/dtb-feature-plan/SKILL.md | grep -c "Geplant"` ≥ 1 und dasselbe mit `"Spezifiziert"` ≥ 1
- [ ] `allowed-tools` beider Skills unverändert: `git diff $(git merge-base master HEAD) -- skills/dtb-feature-plan/SKILL.md skills/dtb-impl-plan/SKILL.md | grep -c "^[-+]allowed-tools"` = 0 (Lektion 85)

---

## Phase 2: Doku, Probelauf, Konsistenz-Sweep

### Ziel
Kit-Doku beschreibt den neuen Ablauf, beide Ausgänge sind an einem Wegwerf-Ordner belegt, und kein Verweis im Repo behauptet mehr zwei Pflicht-Befehle.

### Schritte

#### Schritt 2.1: Doku und Verweise nachziehen
- **Zweck:** Doku folgt dem Verhalten (Lektion 3: repo-weit nach dem Skill-Namen greppen)
- **Dateien:** `CLAUDE.md` (Lebenszyklus „Work", Kategorie „Feature workflow"), `README.md` (Zeile `/dtb:feature-plan`), `skills/dtb-feature-discover/SKILL.md` (Abschlusszeile: Hinweis „erzeugt spec.md und plan.md")
- **Input:** repo-weiter Grep `feature-plan` über `skills/`, `agents/`, `CLAUDE.md`, `README.md`
- **Output:** angepasste Stellen; Fundliste des Greps mit Entscheidung je Treffer (ändern / bleibt richtig) in `features/plan-in-einem-befehl/probelauf.md` unter `## Verweis-Sweep`

#### Schritt 2.2: Probelauf an Wegwerf-Ordnern
- **Zweck:** beide Ausgänge real belegen, gegen die Repo-Fassung (Lektion 74)
- **Dateien:** `features/plan-in-einem-befehl/probelauf.md` (Ablage); temporär `features/zz-test-plan-durchlauf/`, `features/zz-test-plan-nur-spec/`
- **Input:** `skills/dtb-feature-plan/SKILL.md` (Repo-Fassung lesen und befolgen) mit einem kleinen Schein-Feature aus dem Chat
- **Output:** Lauf A (Durchlauf) erzeugt `spec.md` + `plan.md` (📚-Zeile, Ist-Analyse, `## Progress`, `**Status:** Entwurf`, Fusszeile impl-plan, Abschluss mit plan-review); Lauf B (`nur-spec`) erzeugt nur `spec.md`, Abschluss mit impl-plan; Befund je Lauf unter `## Probelauf` in `probelauf.md`, inklusive Nähte-Prüfung (genau eine 📚-Zeile, genau eine Abschlussmeldung) und dem ausdrücklichen Vermerk „Backlog-Zweig im Worktree nicht ausführbar (Teil-Guard + Testordner) — bei der Abnahme im Haupt-Checkout sichtbar"; danach beide Wegwerf-Ordner gelöscht (Lektion 57)

#### Schritt 2.3: Konsistenz-Sweep
- **Zweck:** Kopplungen mechanisch belegen
- **Dateien:** `features/plan-in-einem-befehl/probelauf.md` (Ablage unter `## Konsistenz`)
- **Input:** Anker-Greps von feature-fast (Schritt 2) und feature-plan (neuer Schritt) gegen die Repo-Fassungen
- **Output:** Tabelle Anker → Fundzahl; alle = 1

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Doku-Stellen in `CLAUDE.md`, `README.md`, `skills/dtb-feature-discover/SKILL.md`
- [ ] `features/plan-in-einem-befehl/probelauf.md` mit `## Verweis-Sweep`, `## Probelauf`, `## Konsistenz`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE "^\| \`/dtb:feature-plan\` .*plan\.md" README.md` = 1
- [ ] `grep -cE "^- \*\*Feature workflow\*\*:.*feature-plan.*impl-plan.*per reference" CLAUDE.md` = 1
- [ ] `grep -cE "^Naechster Schritt: /dtb:feature-plan .*plan\.md" skills/dtb-feature-discover/SKILL.md` = 1
- [ ] `grep -cE "^## (Verweis-Sweep|Probelauf|Konsistenz)$" dtb-project/project-workflows/features/plan-in-einem-befehl/probelauf.md` = 3
- [ ] Wegwerf-Ordner entfernt: `ls dtb-project/project-workflows/features/ | grep -c "^zz-test-plan-"` = 0
- [ ] feature-fast-Struktur-Check weiter grün: `grep -c "^## Schritt 6" skills/dtb-feature-discover/SKILL.md`, `grep -c "^## Template fuer spec.md" skills/dtb-feature-plan/SKILL.md`, `grep -c "^## Template fuer plan.md" skills/dtb-impl-plan/SKILL.md` je = 1

#### Manual
- [ ] Der Mensch liest den Befund von Lauf A und B in `probelauf.md` und bestätigt: der Plan aus Lauf A ist von einem Einzel-Lauf von `impl-plan` nicht zu unterscheiden, der Lauf stellte keine zusätzliche Rückfrage, und es gibt keine sichtbaren Nähte (genau eine 📚-Zeile, genau eine Abschlussmeldung)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Zusammenlegen vs. Referenz | Skills verschmelzen / Referenz-Ausführung | Referenz | Beide Skills werden je von ~15 anderen referenziert; Muster in feature-fast erprobt (INBOX #178, geklärt 2026-10-30) |
| Stopp-Mechanik | Argument / Rückfrage nach der Spec | Argument `nur-spec` (auch Wunsch im Aufruftext) | Eine Rückfrage würde die Kette nicht verkürzen; per Veto-Vorlage bestätigt 2026-11-09 |
| Struktur-Check fehlgeschlagen | ganzen Lauf abbrechen / nur Plan-Teil entfallen lassen | nur Plan-Teil | Spec ist zu diesem Zeitpunkt korrekt gespeichert; Abbruch des Ganzen würde fertige Arbeit verwerfen |
| Position des neuen Schritts | nach dem Abschluss / direkt nach dem Speichern der Spec | direkt nach dem Speichern, als Punkt `8a` | BACKLOG-Status hängt vom Ausgang ab und wird danach geschrieben; `8a` statt Neunummerierung hält sieben Verweise in drei Dateien gültig (plan-review 2026-11-09) |
| Fusszeile von plan.md | impl-plan / feature-plan | impl-plan | Inhalt soll unverändert bleiben (INBOX-Fertig-Kriterium) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Stopp-Weiche und Frontmatter
- [x] 1.2 Referenz-Schritt impl-plan
- [x] 1.3 Backlog-Status, Abschluss, Wartungs-Hinweise
- [ ] 2.1 Doku und Verweise
- [ ] 2.2 Probelauf
- [ ] 2.3 Konsistenz-Sweep

---

## Umsetzung

Umsetzung mit `/dtb:implement Plan in einem Befehl` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/plan-in-einem-befehl/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)
