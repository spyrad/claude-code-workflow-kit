# Implementierungsplan: Skill-Lint

**Erstellt:** 2026-11-26
**Feature-Spec:** `features/skill-lint/spec.md`
**Geschaetzte Dauer:** ca. 4–5 h
**Status:** Reviewed (plan-review 2026-11-26: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Prüfskript, Selbsttest, Bestand grün | ca. 3 h | Geplant |
| Phase 2 | CI-Lauf, Check-8-Einbindung, Doku | ca. 1,5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` + Probelauf über 45 Skills am 2026-11-26.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `scripts/` | existiert nicht (Neubau) |
| `.github/workflows/` | nur `notify-site.yml` (Push auf master, Site-Deploy) — bleibt unberührt |
| `skills/dtb-*/SKILL.md` (45) | `name` = Verzeichnis, `Use when:`-Präfix, Listenform, Stage im 10er-Enum: fehlerfrei; Beschreibungen der 10 modellaufrufbaren Skills ≤ 338 Zeichen |
| `skills/dtb-feature-plan/SKILL.md:11`, `skills/dtb-feature-discover/SKILL.md:10`, `skills/dtb-open-question/SKILL.md:10` | `allowed-tools` ohne `Bash`, obwohl alle drei den `**Teil-Guard (Worktree):**`-Anker tragen (#195; open-question per plan-review 2026-11-26 gefunden, Anker Zeile 74); das Wort „Bash" kommt im Body nicht vor. In `dtb-feature-plan:251` und `dtb-feature-fast:250` steht der Anker eingerückt |
| 7 Kanten | einseitig: feature-plan.next→plan-review, lesson-curate.after←lesson, meeting-dump.next→workflow-next, meeting-dump.after←meeting-agenda, open-question.next→workflow-next, open-question.next→meeting-agenda, opportunity-map.next→greenfield-prd |
| `skills/dtb-project-health/SKILL.md` Check 8 | Modell-Sicht über `.claude/skills/dtb-*`; Einstufung FEHLER (name/description, Kanten-Ziel, Zyklen) / WARNUNG (übrige Pflichtfelder, verwaiste consumes, Werkzeuge) |
| `skills/CLAUDE.md` | Frontmatter-Block nennt 10 Stages, Pipeline-Tabelle nur 8 (`capture`, `execution` fehlen) |
| `CLAUDE.md` (Root):19 | „There are no build steps, tests, or runtime dependencies." |

---

## Phase 1: Prüfskript, Selbsttest, Bestand grün

### Ziel
Ein lokal lauffähiges Prüfskript mit Selbsttest, das über den heutigen Bestand ohne FEHLER läuft.

### Schritte

#### Schritt 1.1: Prüfskript
- **Zweck:** Die eindeutigen Regeln aus `skills/CLAUDE.md` mechanisch prüfen
- **Dateien:** `scripts/lint-skills.py` (neu)
- **Input:** Regeln aus `skills/CLAUDE.md` → „Frontmatter (Pflichtfelder)", Einstufung aus Check 8
- **Output:** Skript mit Argument Repo-Root (Default: Elternordner von `scripts/`); prüft je
  `skills/dtb-*/`: `SKILL.md` vorhanden, Frontmatter als gültiges YAML (PyYAML; fehlt es →
  Meldung mit `pip install pyyaml`, Exit 2), CRLF normalisiert. FEHLER: `name`/`description`
  fehlt, `name` ≠ `dtb:` + Verzeichnis ohne `dtb-`, Beschreibung beginnt nicht mit `Use when:`,
  `after`/`next` weder Liste noch null, Kanten-Ziel ohne Skill, `stage` nicht im 10er-Enum,
  gefaltete Beschreibung > 350 Zeichen bei `disable-model-invocation: false`, ```` ```bash ````-Block
  oder Zeile `## Worktree-Guard` bzw. Zeile mit `**Teil-Guard (Worktree):**` (führende
  Leerzeichen erlaubt — in `dtb-feature-plan`/`dtb-feature-fast` eingerückt) ohne `Bash` in
  `allowed-tools`, einseitige Kante ohne Eintrag in der Ausnahmeliste `EDGE_EXCEPTIONS`
  (Tupel Quelle, Feld, Ziel, Grund). WARNUNG: `disable-model-invocation`/`allowed-tools`/
  `pipeline` fehlt. Ausgabe je Befund eine Zeile `{FEHLER|WARNUNG} {skill}: {regel} — {detail}`,
  Schlusszeile mit Zählern; Exit 1 bei ≥ 1 FEHLER, sonst 0. `sys.dont_write_bytecode = True`

#### Schritt 1.2: Selbsttest mit Fixtures
- **Zweck:** Belegen, dass jede Regel anschlägt und ein sauberer Skill grün bleibt
- **Dateien:** `scripts/tests/test_lint_skills.py` (neu), `.gitignore` (Zeile `__pycache__/`).
  Keine eingecheckten Fixtures: der Test erzeugt je Fehlerklasse ein Mini-Repo zur Laufzeit in
  `tempfile.TemporaryDirectory()` (Grundgerüst + gezielte Abweichung, dazu ein grünes) — keine
  `dtb:`-Dateien im Baum, CRLF exakt geschrieben statt von Git umgeschrieben (plan-review 2026-11-26)
- **Input:** Regelliste aus 1.1
- **Output:** `unittest`-Tests, die das Skript je Fixture aufrufen und Exit-Code plus erwartete
  Befundzeile prüfen; eine Fixture mit CRLF-Zeilenenden (binär geschrieben); eine mit gefalteter Beschreibung knapp
  unter und knapp über 350 Zeichen; eine mit eingerücktem `**Teil-Guard (Worktree):**`-Anker
  ohne `Bash` (der #195-Fall)

#### Schritt 1.3: Bestand bereinigen
- **Zweck:** Der erste CI-Lauf soll grün sein
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-feature-discover/SKILL.md`,
  `skills/dtb-open-question/SKILL.md` (`Bash` in `allowed-tools`, #195); je nach Kanten-Entscheidung die betroffenen Skills aus der
  Ist-Analyse bzw. `EDGE_EXCEPTIONS` in `scripts/lint-skills.py`
- **Input:** Lint-Lauf über den Bestand; Kanten-Tendenz aus `discovery.md` → `## Offene Punkte`
- **Output:** Die 7 Kanten werden dem Menschen als eine Liste vorgelegt (je Kante Vorschlag:
  Gegenkante oder Ausnahme mit Grund) und nach seiner Entscheidung umgesetzt; danach Lint-Lauf
  ohne FEHLER. Vor dem Umhängen einer Kante repo-weit nach den Skill-Namen greppen (Lektion L3)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `scripts/lint-skills.py`
- [ ] `scripts/tests/test_lint_skills.py` (Fixtures zur Laufzeit)
- [ ] Bestand ohne FEHLER

### Checkpoint-Kriterien

#### Automated
- [ ] `python -m unittest discover -s scripts/tests` endet mit Exit 0
- [ ] `python scripts/lint-skills.py` über den Repo-Root endet mit Exit 0, Schlusszeile meldet 0 FEHLER
- [ ] `grep -n '^allowed-tools:.*Bash' skills/dtb-feature-plan/SKILL.md skills/dtb-feature-discover/SKILL.md skills/dtb-open-question/SKILL.md` liefert 3 Treffer
- [ ] `git status --porcelain` zeigt kein `__pycache__`

#### Manual
- [ ] Jede der 7 Kanten-Entscheidungen ist vom Menschen bestätigt (Gegenkante oder Ausnahme mit Grund)

---

## Phase 2: CI-Lauf, Check-8-Einbindung, Doku

### Ziel
Das Skript läuft bei jedem Push und Pull Request; Check 8 und die Doku kennen es.

### Schritte

#### Schritt 2.1: CI-Workflow
- **Zweck:** Prüfung unabhängig von Aufmerksamkeit
- **Dateien:** `.github/workflows/lint-skills.yml` (neu)
- **Input:** Aufrufe aus Phase 1
- **Output:** Workflow `on: push` (alle Branches) + `pull_request`, `permissions: contents: read`,
  `ubuntu-latest`, `actions/checkout@v4`, Python per `actions/setup-python@v5`,
  `pip install pyyaml==6.0.1` (lokal geprüfte Version), dann Selbsttest, dann Lint; keine
  Secrets; keine Fehler-Unterdrückung (`continue-on-error`, `|| true`), damit ein Fehler-Exit
  den Lauf rot macht. `notify-site.yml` unverändert

#### Schritt 2.2: Check 8 nutzt das Skript
- **Zweck:** Modell-Sicht und Skript nicht doppelt pflegen
- **Dateien:** `skills/dtb-project-health/SKILL.md` (Check 8)
- **Input:** Befundformat aus 1.1
- **Output:** Absatz am Anfang von Check 8: liegt `scripts/lint-skills.py` im Projekt-Root, ihn
  ausführen und seine Befunde für die abgedeckten Regeln übernehmen; die Modell-Sicht prüft dann
  nur noch, was das Skript nicht abdeckt (verwaiste `consumes`, Zyklen). Fehlt das Skript →
  unverändert wie heute. `allowed-tools` enthält `Bash` bereits

#### Schritt 2.3: Doku-Nachzug
- **Zweck:** Doku darf Skript und CI nicht verschweigen
- **Dateien:** `CLAUDE.md` (Root, Zeile „no build steps, tests"), `skills/CLAUDE.md`
  (Frontmatter-Abschnitt: Verweis aufs Skript als Prüfinstanz, Regel-Änderungen im selben Zug
  ins Skript; Pipeline-Tabelle: `stage`-Zeile auf 10 Werte)
- **Input:** Ergebnis 2.1/2.2
- **Output:** Root-`CLAUDE.md` nennt `python scripts/lint-skills.py` und den CI-Lauf;
  `skills/CLAUDE.md` angeglichen

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `.github/workflows/lint-skills.yml`
- [ ] Check 8 mit Skript-Aufruf
- [ ] Doku angeglichen

### Checkpoint-Kriterien

#### Automated
- [ ] `python -c "import yaml; d=yaml.safe_load(open('.github/workflows/lint-skills.yml')); print(sorted(d[True].keys()))"` zeigt `pull_request` und `push`
- [ ] `grep -n -E 'continue-on-error|\|\| *true' .github/workflows/lint-skills.yml` liefert 0 Treffer (ein Fehler-Exit wird nicht geschluckt — Spec: „wird rot, sobald ein FEHLER auftritt")
- [ ] `grep -c 'scripts/lint-skills.py' skills/dtb-project-health/SKILL.md` ≥ 1, und zwar innerhalb der Sektion `#### Check 8` (Lektion L2: auf die Wirkstelle ankern)
- [ ] `grep -n 'no build steps, tests' CLAUDE.md` liefert 0 Treffer in der Sektion `## How This Repo Is Used` (Wirkstelle)
- [ ] In `skills/CLAUDE.md` nennt die `stage`-Zeile der Pipeline-Tabelle `capture` und `execution`
- [ ] `python scripts/lint-skills.py` endet weiter mit Exit 0
- [ ] `git diff master...HEAD --stat -- .github/workflows/notify-site.yml` ist leer

#### Manual
- [ ] Der erste CI-Lauf auf GitHub nach dem Push ist grün (Lauf-Link im Session-Log)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Zielort | nur Kit + CI / auch Zielprojekte / Check 8 unberührt | nur Kit + CI, Check 8 nutzt das Skript bei Vorhandensein | Kernfrage beantwortet 2026-11-26; kit-sync verteilt kein `scripts/` |
| YAML-Lesen | PyYAML / eigener Parser | PyYAML | gefaltete Beschreibungen und Flow-Listen ohne eigenen Parser; per Veto-Vorlage bestaetigt 2026-11-26 |
| Aufruf | `python` / `python -I` | `python` ohne `-I` | `-I` blendet die User-site-packages aus, PyYAML fehlt dann (Probelauf 2026-11-26) |
| Einstufung | eigene / wie Check 8 | wie Check 8, ergänzt um Präfix, Stage, Länge, Gegenkante als FEHLER | keine neue Einstufung erfinden; per Veto-Vorlage bestaetigt 2026-11-26 |
| Ausnahmen für Kanten | eigene Datei / Liste im Skript | Liste im Skript mit Grund je Eintrag | sichtbar am Prüfort, keine weitere Datei |
| Versionen im CI | offen / Major-Tag / Commit-SHA | PyYAML exakt (`==6.0.1`), offizielle Actions mit Major-Tag (`checkout@v4`, `setup-python@v5`) | öffentliches Repo, aber nur Leserechte und keine Secrets — SHA-Pin unverhältnismäßig; Updates bewusst nachziehen (plan-review 2026-11-26) |
| Werkzeug-Regel | Stichwort „Bash" / feste Anker | ```` ```bash ````-Block oder Guard-Anker-Zeile | #195 ist am Stichwort nicht erkennbar (Teil-Guard per Verweis) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Prüfskript
- [x] 1.2 Selbsttest mit Fixtures
- [x] 1.3 Bestand bereinigen
- [ ] 2.1 CI-Workflow
- [ ] 2.2 Check 8 nutzt das Skript
- [ ] 2.3 Doku-Nachzug

---

## Umsetzung

Umsetzung mit `/dtb:implement Skill-Lint` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/skill-lint/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
