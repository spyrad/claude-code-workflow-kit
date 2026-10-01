# Implementierungsplan: Rueckfragen-Defaults

**Erstellt:** 2026-09-30
**Feature-Spec:** `features/rueckfragen-defaults/spec.md`
**Geschaetzte Dauer:** 8–10 h (5 Phasen, 2–3 Sessions)
**Status:** Reviewed (plan-review 2026-09-30: REVISE → 5 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Kanon der Veto-Form + Beispielausgaben (Abnahme vor Ausrollen, L64) | 1 h | Geplant |
| Phase 2 | Anfang der Kette: Backlog ohne Frage, Slug- und Scan-Vorschlag | 1,5 h | Geplant |
| Phase 3 | Plan-/Review-Stellen: plan-review, Lektion-Vormerkung, impl-review-Sammelliste, feature-start | 2,5 h | Geplant |
| Phase 4 | `implement`: Staging, Commit-Message, Manual-Gate-Form, Naechste Phase | 1 h | Geplant |
| Phase 5 | Eigen-Text-Pruefung, Doku, Abnahme-Probelauf | 2,5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Pfade verifiziert 2026-09-30) plus repo-weiter Verweis-Scan (L3). Drei Spiegel kamen im Scan dazu (markiert **neu**).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-feature-discover/SKILL.md | Schritt 2 endet mit „Stimmt das so?…" + Warten (Z14); Schritt 5 Namensvorschlag als Optionsliste mit „(Recommended)" (Z1); Wartungs-Hinweis Format-Kopplung zu impl-plan; Anker `## Schritt 6` von feature-fast gegreppt |
| skills/dtb-feature-fast/SKILL.md | Schritt 3 Punkt 3 „Slug ableiten" (Z1); Schritt 5 Punkt 7 „BACKLOG anbieten (analog feature-plan Schritt 10). Bei Ja: …" (Z3) |
| skills/dtb-task/SKILL.md | `## Schritt 5: Backlog-Eintrag anbieten` — „Soll die Aufgabe in BACKLOG.md eingetragen werden? (Ja/Nein)" (Z2); Voll-Guard: bricht im Worktree hart ab |
| skills/dtb-feature-plan/SKILL.md | Aufgabe Punkt 4 „Frage den Benutzer ob … BACKLOG.md"; Ausfuehrung Punkt 10 „Backlog-Eintrag anbieten" mit Ja/Nein-Zweigen (Z3); Teil-Guard ueberspringt 9+10 im Worktree |
| skills/dtb-bug-report/SKILL.md | `## Schritt 5: Backlog-Eintrag anbieten` — gleiche Ja/Nein-Frage (Zusatz A) |
| skills/dtb-plan-review/SKILL.md | `## Schritt 5: Anpassungen anbieten` + Report-Block endet mit „Moechtest du Anpassungen … (Ja/Nein)"; Schritt 6 (Kopf-Status) haengt am Ausgang von Schritt 5 (Z7) |
| skills/dtb-implement/SKILL.md | Ritual Schritt 4: Punkt 2 Manual-Gate als Freitext „Bestaetige („passt") oder nenne Korrekturen" (Zusatz D); Punkt 3 Staging (1/2/3) (Z9); Punkt 6 Commit-Message-Vorschlag (Z10); Punkt 11 Naechste-Phase (1/2/3) (Z11). `allowed-tools` ohne `AskUserQuestion` |
| skills/dtb-impl-review/SKILL.md | `## Schritt 9: Triage-Loop` — eine Frage je Finding in Severity-Reihenfolge, „nie stiller Auto-Fix" (Z13); `AskUserQuestion` bereits erlaubt |
| skills/dtb-impl-plan/SKILL.md | 2b Scan „Stimmt das so?" (Muster aus discover Schritt 2, Z14); `## Lektion-Kandidat erkennen (Vorschlager)` mit „Nach lessons.md uebernehmen? (… ja/nein)" (Z16) |
| skills/dtb-debug-plan/SKILL.md | `## Lektion-Kandidat erkennen (Vorschlager)` — gleiche Formel (Z16) |
| skills/dtb-feature-start/SKILL.md | Drei Abschluss-Bloecke: Feature „Bereit? Starte mit `/dtb:implement …` oder stelle Fragen.", Bug/Aufgabe „Bereit? Sage "Los" oder stelle Fragen." (Z15, Zusatz E); `disable-model-invocation: true` |
| skills/dtb-lesson/SKILL.md | **neu** — „Zwei Eingangskanaele" Punkt 2 beschreibt den Agent-Vorschlag „…und dich gefragt. Bei ‚ja'…" → Spiegel von Z16 |
| skills/dtb-no-loss-check/SKILL.md | **neu** — Signalklasse „Lektion" kennt keine Vormerk-Zeile; muss sie als sicheren Kandidaten fuehren (Integrationspunkt aus der Discovery) |
| skills/dtb-workflow-resume/SKILL.md | **neu, nicht im Scope** — traegt ebenfalls „Bereit? Sage "Los"" (Zeile 229); nicht Teil der Festlegung → Offener Punkt, keine Aenderung |
| skills/CLAUDE.md | Muster „kanonische Vorlage + Laufzeit-Autarkie" vorhanden (Worktree-Guard, Duplikat-Schutz): installierte Skills sehen `skills/CLAUDE.md` NICHT — Laufzeittext muss inline stehen |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §4 Slug-Ableitung; Klasse-B-Seed (einmal kopiert, nie drift-geprueft) → Aenderungen erreichen Bestandsprojekte nicht |
| CLAUDE.md | Kurzbeschreibungen von feature-start, implement, impl-review in „Skill Categories" |

---

## Phase 1: Kanon der Veto-Form + Beispielausgaben

### Ziel
Die eine Beschreibung der Veto-Form steht, und der Mensch hat sie an echten Beispielen abgenommen, BEVOR elf Skills umgebaut werden (L64: Zielform zuerst zeigen).

### Schritte

#### Schritt 1.1: Kanon-Sektion in `skills/CLAUDE.md`
- **Zweck:** Eine Quelle fuer Form und Zuordnung (Autoren-Doku, Muster Worktree-Guard / Duplikat-Schutz)
- **Dateien:** `skills/CLAUDE.md` — neue Sektion `## Rueckfragen-Defaults (Veto-Form)` nach `## Duplikat-Schutz`
- **Input:** Festlegung 2026-09-22, spec.md
- **Output:** Sektion mit (a) Abgrenzungskriterium (ein Satz, Verweis auf `erhebung.md`); (b) vier Formen mit festem Wortlaut-Anker: **Einzel-Vorschlag Textzeile** (`→ weiter = uebernehmen · oder {Alternative} nennen`), **Einzel-Vorschlag Knopf** (blockierende Auswahl, erste Option = Vorschlag), **Sammelliste** (vorbelegt, „weiter = alle", Nummern streichen), **stiller Default mit Anzeige-Zeile** (`→ …`); (c) Bedienregel „Knopf bei Commit-Folge, sonst Textzeile"; (d) feste Zeilen: Backlog-Anzeige (`→ in BACKLOG.md eingetragen (Status: {Status})`, `→ kein BACKLOG-Eintrag (Testordner)`, `⚠ BACKLOG.md fehlt oder ist unlesbar — kein Eintrag, weiter`), Lektion-Vormerkung (`💡 Lektion-Kandidat vorgemerkt: „{Regel}" → wird beim Checkpoint erfasst`), Testordner-Praefixe; (e) **Zuordnungstabelle** Skill/Stelle → Form (11 Zeilen + Zusaetze A–E), analog „Verbindliche Hard-Gate-Zuordnung"; (f) Laufzeit-Autarkie-Satz: jeder Skill traegt seine Form inline, die Sektion ist nie Laufzeitpfad

#### Schritt 1.2: Beispielausgaben mit echten Daten
- **Zweck:** Abnahme der Zielform vor dem Ausrollen (L64)
- **Dateien:** `features/rueckfragen-defaults/beispielausgaben.md` (neu, status-neutral)
- **Input:** Kanon aus 1.1; echte Daten: Slug dieses Changes, Commit-Stil aus `git log`, ein echtes `review.md` aus `archive/` (z.B. `capture-duplikat-schutz`), ein echter Plan-Review-Verdikt
- **Output:** **4 Ausgaben, eine je Form (Plan-Review 2026-09-30):** (1) Textzeile — Slug-Vorschlag dieses Changes; (2) Knopf — Commit-Message-Vorschlag im Repo-Stil; (3) Sammelliste — aus einem echten `review.md` (≥5 Sammel-Findings + 1 Einzel-Finding nach der S:Hoch/FAIL-Regel); (4) stille Anzeige — Backlog-Zeile (beide Zweige) + Lektion-Vormerkung. Abgenommen wird die Form, nicht jede Stelle

#### Schritt 1.3: Zuordnung gegen Festlegung gegenpruefen
- **Zweck:** Keine Zeile vergessen, keine „nie automatisch"-Zeile beruehrt (Spec-Kriterium 3)
- **Dateien:** `skills/CLAUDE.md` (Zuordnungstabelle), Ergebnis als Fusszeile unter der Tabelle in `beispielausgaben.md`
- **Input:** Festlegungs-Tabelle (17 Zeilen)
- **Output:** Abgleich 17 → 11 umgesetzt + 5 unveraendert (Z5, Z6, Z8-Entscheidung, Z12, Z17) + 1 nicht gebaut (Z4); Zusaetze A–E gelistet

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Kanon-Sektion in `skills/CLAUDE.md`
- [ ] `beispielausgaben.md` mit 4 Ausgaben (eine je Form)

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "^## Rueckfragen-Defaults (Veto-Form)" skills/CLAUDE.md` = 1
- [ ] Zuordnungstabelle in der Sektion hat ≥16 Datenzeilen (11 + A–E): `awk '/^## Rueckfragen-Defaults/,/^## Zwei-Becken/' skills/CLAUDE.md | grep -c "^| [0-9A-E]"` ≥ 16
- [ ] `test -f dtb-project/project-workflows/features/rueckfragen-defaults/beispielausgaben.md`

#### Manual
- [ ] Mensch nimmt die Beispielausgaben ab: Form verstaendlich, „weiter" eindeutig, Knopf-/Textzeilen-Wahl passt

---

## Phase 2: Anfang der Kette — Backlog, Slug, Scan

### Ziel
Die Rueckfragen am Anfang der Kette sind ersetzt: Backlog ohne Frage (4 Skills), Slug- und Scan-Bestaetigung als Textzeilen-Vorschlag.

### Schritte

#### Schritt 2.1: Backlog ohne Frage in `task` und `bug-report`
- **Zweck:** Z2 + Zusatz A
- **Dateien:** `skills/dtb-task/SKILL.md`, `skills/dtb-bug-report/SKILL.md` — je `## Schritt 5`
- **Input:** Kanon-Zeilen aus 1.1
- **Output:** Ueberschrift wird `## Schritt 5: Backlog-Eintrag (ohne Rueckfrage)`; Ja/Nein-Frage und „Bei Nein"-Block entfallen; Testordner-Pruefung (Slug beginnt mit `zz-test-` oder `abnahmeprobe-` → kein Eintrag); Eintrags-Logik unveraendert; Anzeige-Zeile inline; fehlende/unlesbare BACKLOG.md → eine Warnzeile, weiter

#### Schritt 2.2: Backlog ohne Frage in `feature-plan` und `feature-fast`
- **Zweck:** Z3
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (Aufgabe Punkt 4, Ausfuehrung Punkt 10), `skills/dtb-feature-fast/SKILL.md` (Schritt 5 Punkt 7)
- **Input:** wie 2.1
- **Output:** feature-plan Punkt 10 heisst `**Backlog-Eintrag (ohne Rueckfrage):**`, Punkt 4 der Aufgabe entsprechend umformuliert; Testordner-Pruefung und Anzeige-Zeile inline wie 2.1; **fehlende/unlesbare BACKLOG.md → eine Warnzeile, weiter** — in beiden Skills ausgeschrieben, nicht nur verwiesen; Teil-Guard-Texte (feature-plan Schritt 9+10, feature-fast Schritt 6+7 im Worktree ueberspringen) bleiben woertlich; feature-fast Punkt 7 wird `**BACKLOG eintragen** (analog feature-plan Schritt 10)` — Verweis bleibt gueltig, „Bei Ja" entfaellt

#### Schritt 2.3: Slug-Vorschlag mit Veto + allgemeine Namensregel
- **Zweck:** Z1 + Zusatz B
- **Dateien:** `skills/dtb-feature-discover/SKILL.md` (Schritt 5), `skills/dtb-feature-fast/SKILL.md` (Schritt 3 Punkt 3)
- **Input:** Kanon (Einzel-Vorschlag Textzeile)
- **Output:** Vorschlag als Textzeile statt Optionsliste; Namensregel inline: „Liefert das Feature etwas mit festem Namen (Skill, Datei, Befehl), uebernimmt der Slug diesen Namen"; Slug-Kollision bleibt echte Rueckfrage (§4, kein Auto-Suffix); das „(Recommended)"-Muster in discover bleibt nur fuer den Scope-Schnitt; `DERIVED_STATE_RULES.md` bleibt unveraendert (Klasse-B-Seed, siehe Technische Entscheidungen)

#### Schritt 2.4: Scan-Bestaetigung mit Veto in `feature-discover` und `impl-plan`
- **Zweck:** Z14
- **Dateien:** `skills/dtb-feature-discover/SKILL.md` (Schritt 2), `skills/dtb-impl-plan/SKILL.md` (2b)
- **Input:** Kanon (Einzel-Vorschlag Textzeile)
- **Output:** „Stimmt das so? …" + Warten → Textzeile `→ weiter = Liste uebernehmen · oder Pfade nennen, die fehlen/wegfallen`; Tabellenformat `| # | Pfad | Relevanz |` unveraendert (Format-Kopplung zu impl-plan-Pfad-Erkennung bleibt intakt); impl-plan 2b-Musterverweis auf den neuen Wortlaut nachziehen; 0-Treffer-Dialog in impl-plan bleibt echte Frage

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 4 Backlog-Stellen ohne Frage, 2 Slug-Stellen, 2 Scan-Stellen umgestellt

### Checkpoint-Kriterien

#### Automated
- [ ] Alte Fragen an der Wirkstelle weg (L8): `grep -c "in BACKLOG.md eingetragen werden? (Ja/Nein)" skills/dtb-{task,bug-report,feature-plan}/SKILL.md` = 0 je Datei
- [ ] Anzeige-Zeile an allen 4 Stellen: `grep -l "→ in BACKLOG.md eingetragen (Status:" skills/dtb-{task,bug-report,feature-plan,feature-fast}/SKILL.md | wc -l` = 4
- [ ] Testordner-Praefix an allen 4 Stellen: `grep -l "abnahmeprobe-" skills/dtb-{task,bug-report,feature-plan,feature-fast}/SKILL.md | wc -l` = 4
- [ ] Teil-Guards unveraendert: `grep -c "Schritt 9 UND 10 NICHT ausfuehren" skills/dtb-feature-plan/SKILL.md` = 1 und `grep -c "Schritt 6 UND 7 NICHT ausfuehren" skills/dtb-feature-fast/SKILL.md` = 1
- [ ] Warnzeile bei fehlender BACKLOG.md an allen 4 Stellen: `grep -l "BACKLOG.md fehlt" skills/dtb-{task,bug-report,feature-plan,feature-fast}/SKILL.md | wc -l` = 4
- [ ] Anker stabil: `grep -c "^## Schritt 5: Feature-Name / Slug festlegen" skills/dtb-feature-discover/SKILL.md` = 1 und `grep -c "^## Schritt 6" skills/dtb-feature-discover/SKILL.md` = 1
- [ ] `grep -c "Stimmt das so?" skills/dtb-feature-discover/SKILL.md skills/dtb-impl-plan/SKILL.md` = 0 je Datei
- [ ] `git diff --stat -- dtb-project/project-rules/DERIVED_STATE_RULES.md` leer

---

## Phase 3: Plan- und Review-Stellen

### Ziel
plan-review ohne Leer-Frage bei negativem Verdikt, Lektion-Kandidaten werden vorgemerkt statt erfragt, impl-review-Triage als Sammelliste, feature-start ohne „Bereit?".

### Schritte

#### Schritt 3.1: `plan-review` — Direkteinstieg bei REVISE/REJECTED
- **Zweck:** Z7
- **Dateien:** `skills/dtb-plan-review/SKILL.md` (Schritt 5 + Report-Block-Schluss)
- **Input:** Kanon (stiller Default mit Anzeige-Zeile)
- **Output:** Bei REVISE/REJECTED entfaellt die Ja/Nein-Frage; Anzeige `→ Verdikt {X}: direkt in die Finding-Runde`; bei APPROVED bleibt die Frage wie heute (Festlegung nennt nur REVISE/REJECTED); Findings weiterhin einzeln; Schritt-6-Kopplung (Kopf-Status nach Ausgang Schritt 5) bleibt korrekt — Textpassage „Der Block oben endet mit der noch unbeantworteten Frage" fuer den REVISE/REJECTED-Fall anpassen (L42: Bedingung im selben Zug mitziehen)

#### Schritt 3.2: Lektion-Vormerkung statt Rueckfrage
- **Zweck:** Z16 + Zusatz C
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`, `skills/dtb-debug-plan/SKILL.md` (je `## Lektion-Kandidat erkennen`), Spiegel `skills/dtb-lesson/SKILL.md` („Zwei Eingangskanaele" Punkt 2), `skills/dtb-no-loss-check/SKILL.md` (Signalklasse „Lektion")
- **Input:** Kanon-Zeile Lektion-Vormerkung
- **Output:** Rueckfrage entfaellt; feste Vormerk-Zeile inline; „nie stiller Auto-Write in lessons.md" bleibt (erfasst wird erst im Checkpoint mit Sammelvorlage); dtb-lesson Punkt 2 beschreibt den Weg „vorgemerkt → Checkpoint"; no-loss-check fuehrt jede Vormerk-Zeile im Gespraech als sicheren Lektions-Kandidaten (Stufe 1, nicht wegfiltern, ausser bereits in lessons.md)

#### Schritt 3.3: `impl-review` — Sammelliste fuer non-blocking
- **Zweck:** Z13
- **Dateien:** `skills/dtb-impl-review/SKILL.md` (Schritt 9)
- **Input:** Kanon (Sammelliste, Knopf)
- **Output:** **Abgrenzung inline festschreiben (Plan-Review 2026-09-30):** „einzeln" = Finding mit `S:Hoch` ODER aus einer Achse mit Verdikt FAIL; alle anderen = Sammelliste — nutzt die vorhandenen Felder, kein neues Feld im `review.md`-Format. Zwei Durchgaenge: (1) Einzel-Findings wie heute (4 Optionen); (2) alle uebrigen in EINER Liste — je Zeile Befund + geplanter Fix — Knopf „alle uebernehmen / Nummern streichen / einzeln durchgehen"; nur Einzel-Findings → Liste entfaellt (Cap 10 macht einen Gruppierungs-Fall ueberfluessig); „Als Lektion erfassen" fuer non-blocking bleibt ueber „Nummern nennen → Lektion" erreichbar; `Decision:`-Pflege je Finding und Abschluss-Summary unveraendert; „nie stiller Auto-Fix" umformulieren zu „nie ohne sichtbare Liste"

#### Schritt 3.4: `feature-start` ohne „Bereit?"
- **Zweck:** Z15 + Zusatz E
- **Dateien:** `skills/dtb-feature-start/SKILL.md` (drei Abschluss-Bloecke)
- **Input:** Kanon (stiller Default mit Anzeige-Zeile)
- **Output:** Jeder Block endet mit genau EINER Zeile `→ Weiter mit: /dtb:implement {Feature-Name}` (Feature) bzw. dem passenden Einstiegsbefehl (Bug: Fix-Schritte aus `bug.md`; Aufgabe: erster offener Schritt aus `task.md`); kein Selbstaufruf von implement (Sperre bleibt, #98)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] plan-review, impl-plan, debug-plan, lesson, no-loss-check, impl-review, feature-start angepasst

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "Nach lessons.md uebernehmen?" skills/dtb-impl-plan/SKILL.md skills/dtb-debug-plan/SKILL.md` = 0 je Datei
- [ ] `grep -l "Lektion-Kandidat vorgemerkt" skills/dtb-{impl-plan,debug-plan,no-loss-check}/SKILL.md | wc -l` = 3
- [ ] `grep -c "Bereit?" skills/dtb-feature-start/SKILL.md` = 0
- [ ] `grep -c "direkt in die Finding-Runde" skills/dtb-plan-review/SKILL.md` ≥ 1
- [ ] impl-review-Anker stabil: `grep -c "^## Schritt 9: Triage-Loop" skills/dtb-impl-review/SKILL.md` = 1
- [ ] Abgrenzung in Schritt 9 verankert: `awk '/^## Schritt 9: Triage-Loop/,/^## Richtlinien/' skills/dtb-impl-review/SKILL.md | grep -c "S:Hoch"` ≥ 1
- [ ] no-loss-check bleibt read-only: `grep "^allowed-tools" skills/dtb-no-loss-check/SKILL.md` = `Read, Glob, Grep`

#### Manual
- [ ] Mensch liest die neue impl-review-Triage (Schritt 9) gegen die abgenommene Beispielausgabe aus 1.2

---

## Phase 4: `implement`

### Ziel
Staging und Commit-Message als Knopf-Vorschlag, Manual-Gate als blockierende Auswahl, Naechste Phase mit zaehlbarer Schwelle.

### Schritte

#### Schritt 4.1: Staging + Commit-Message als Knopf
- **Zweck:** Z9, Z10
- **Dateien:** `skills/dtb-implement/SKILL.md` (Ritual Punkt 3 und 6), Frontmatter `allowed-tools` (+ `AskUserQuestion`, L75)
- **Input:** Kanon (Einzel-Vorschlag Knopf)
- **Output:** Punkt 3: dirty paths ausserhalb des Sets → Knopf mit erster Option „nur geplantes Set (Vorschlag)", dann „alles stagen", „abbrechen"; Punkt 6: Knopf „Commit mit dieser Message" / „Message aendern"; Sicherheitsregeln Punkt 7 unveraendert (Kopplung zu commit-and-push nicht beruehrt)

#### Schritt 4.2: Manual-Gate als blockierende Auswahl
- **Zweck:** Zusatz D (Entscheidung bleibt beim Menschen, Z8)
- **Dateien:** `skills/dtb-implement/SKILL.md` (Ritual Punkt 2)
- **Input:** Kanon (Knopf); Lehre 2026-07-30
- **Output:** Freitextzeile „Bestaetige („passt") oder nenne Korrekturen" → Knopf „passt — Phasen-Commit" / „Korrekturen"; bei „Korrekturen" Freitext abfragen; weiterhin je Phase, keine Buendelung

#### Schritt 4.3: Naechste Phase mit zaehlbarer Schwelle
- **Zweck:** Z11
- **Dateien:** `skills/dtb-implement/SKILL.md` (Ritual Punkt 11)
- **Input:** Technische Entscheidung „Z11-Schwelle"
- **Output:** Default (1) ohne Frage, Anzeige `→ weiter mit Phase {N+1}`; Schwelle (Ersetzungsprobe-Stil, L10): hat diese Session bereits **2 Phasen** abgeschlossen ODER wurde der Kontext bereits verdichtet → statt weiterzumachen Wiedereinstiegs-Kommando `/dtb:implement {slug} phase {N+1}` ausgeben (2); Nutzer-„Stopp"/„Review" jederzeit → (2) bzw. (3)

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] implement-Ritual mit drei Knoepfen und Schwellenregel

### Checkpoint-Kriterien

#### Automated
- [ ] `grep "^allowed-tools" skills/dtb-implement/SKILL.md | grep -c AskUserQuestion` = 1
- [ ] `grep -c 'Bestaetige („passt") oder nenne Korrekturen' skills/dtb-implement/SKILL.md` = 0
- [ ] Sicherheitsregeln unveraendert: `grep -c "NIE \`--force\`, \`--no-verify\`, \`--amend\`" skills/dtb-implement/SKILL.md` = 1
- [ ] Schwelle benannt: `grep -c "2 Phasen" skills/dtb-implement/SKILL.md` ≥ 1

---

## Phase 5: Eigen-Text-Pruefung, Doku, Abnahme

### Ziel
Der neue Text erzeugt selbst keine neuen Schein-Rueckfragen und keine unsichtbaren Commit-Defaults (L15); Doku stimmt; ein Probelauf gegen die Repo-Fassung belegt das Verhalten (L74).

### Schritte

#### Schritt 5.1: Eigen-Text gegen die Fehlerklasse pruefen
- **Zweck:** L15 + L14 — mechanische Kriterien bezeugen nur Abwesenheit des alten Wortlauts
- **Dateien:** Ergebnis in `features/rueckfragen-defaults/beispielausgaben.md` → Abschnitt `## Eigen-Text-Pruefung`
- **Input:** Diff aller Phasen (`git diff master -- skills/`)
- **Output:** Je geaenderte Stelle drei Fragen beantwortet: Ist der Default sichtbar? Ist „weiter" eindeutig? Loest ein stiller Default einen Commit aus (darf nicht)? Dazu Widerspruchsfreiheit Kanon ↔ Inline-Texte. **Siegel-Check (Plan-Review 2026-09-30):** die Stellen „nie automatisch" sind gegenueber `master` unveraendert — je Paar (Datei, Ankerphrase) Trefferzahl auf `master` = Trefferzahl im Arbeitsbaum: `feature-discover` „Kleinfall-Weiche"; alle Skills „Fehlalarm" (Escape-Hatch, 7 Stellen); `implement` „Mismatch-Handling (Plan ≠ Realitaet)"; `feature-plan` „Soll ich die existierende Spec ueberschreiben oder aktualisieren?"; `impl-plan` „Implementierungsplan existiert bereits. Soll ich ueberschreiben"; `impl-review` „Ueberschreiben / Erst Triage fortsetzen / Abbrechen?"; `feature-fast` „Kernfragen-Budget (max. 3)". Skript per Write-Tool in den Scratchpad (L38), Ergebnis-Tabelle in `## Eigen-Text-Pruefung`

#### Schritt 5.2: Doku nachziehen
- **Zweck:** Kurzbeschreibungen stimmen mit dem Verhalten
- **Dateien:** `CLAUDE.md` (Skill Categories: feature-start, implement, impl-review, Hinweis auf Veto-Form-Kanon)
- **Input:** Phasen 2–4
- **Output:** 3–4 knappe Satzaenderungen; kein neuer Absatz

#### Schritt 5.3: Abnahme-Probelauf im Wegwerf-Clone
- **Zweck:** Spec-Kriterium „Testlauf der Voll-Schiene"; Worktree-Guards verhindern Backlog-Schreiben hier (L21: ortsgebunden zerlegen)
- **Dateien:** Protokoll in `beispielausgaben.md` → Abschnitt `## Abnahme-Probelauf`; Clone im Scratchpad (danach geloescht, L58)
- **Input:** `git clone` des Branches in den Scratchpad (Haupt-Checkout-Situation), Skills aus `skills/…/SKILL.md` dieses Clones gelesen (L74)
- **Output:** Wegwerf-Changes, die der Lauf selbst erzeugt (L57): `probe-rueckfragen` (Aufgabe via task → Backlog-Zeile entsteht, Anzeige-Zeile erscheint) und `zz-test-rueckfragen` (→ kein Eintrag, Testordner-Zeile); Slug-Vorschlag und Scan-Textzeile in feature-discover beobachtet; **Mini-Phase `implement` (Plan-Review 2026-09-30):** Wegwerf-Plan mit einer Phase und einer Test-Datei im Clone, `implement` nach Repo-Fassung durchlaufen — Manual-Gate-Knopf, Staging-Knopf (mit einer bewusst fremden geaenderten Datei), Commit-Knopf, echter Commit im Clone, Naechste-Phase-Anzeige; Eindruck „weniger oder mehr Rueckfragen?" festhalten; Befund je Stelle ✅/❌

> **3x3-Block:** Nach Schritt 5.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Eigen-Text-Pruefung und Abnahme-Protokoll in `beispielausgaben.md`
- [ ] `CLAUDE.md` aktualisiert

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "^## Eigen-Text-Pruefung" dtb-project/project-workflows/features/rueckfragen-defaults/beispielausgaben.md` = 1
- [ ] Spiegel-Zaehlung (Kopplungsregel `skills/CLAUDE.md`): Kanon-Anker je mit Zielzahl — Textzeile `→ weiter =` in discover (2×: Schritt 2 + 5), fast, impl-plan = 3 Dateien; Knopf-Stellen (implement Gate/Staging/Commit, impl-review Sammelliste) = 4 Stellen; `Lektion-Kandidat vorgemerkt` = 3 Dateien; `→ in BACKLOG.md eingetragen (Status:` = 4 Dateien. Abweichung = rot
- [ ] Siegel-Check: alle 7 Anker-Paare mit gleicher Trefferzahl auf `master` und im Arbeitsbaum (0 Abweichungen)
- [ ] `grep -c "^## Abnahme-Probelauf" dtb-project/project-workflows/features/rueckfragen-defaults/beispielausgaben.md` = 1
- [ ] Alle Phase-2–4-Kriterien erneut gruen (L13)
- [ ] Wegwerf-Clone entfernt: Scratchpad-Pfad existiert nicht mehr

#### Manual
- [ ] Mensch nimmt den Probelauf ab: an keiner delegierten Stelle erscheint noch eine Einzelfrage ohne Default
- [ ] Mensch bestaetigt aus der Mini-Phase: die drei Knoepfe hintereinander fuehlen sich wie weniger Rueckfragen an, nicht wie mehr

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Ort der Veto-Form | A: nur zentral in `skills/CLAUDE.md` · B: nur je Skill · C: Kanon zentral + Laufzeit inline | **C** | Installierte Skills sehen `skills/CLAUDE.md` nicht (Laufzeit-Autarkie); Kanon verhindert Auseinanderdriften — bewaehrtes Muster Worktree-Guard/Duplikat-Schutz |
| Ort der Namensregel (Zusatz B) | A: `DERIVED_STATE_RULES.md` §4 · B: inline in discover/fast | **B** | DSR ist Klasse-B-Seed, nie drift-geprueft — Aenderung erreichte Bestandsprojekte nicht; die Regel ist ein Vorschlags-Default, keine Ableitungsregel |
| Z11-Schwelle „Kontext knapp" | A: Modell-Einschaetzung · B: zaehlbar (2 Phasen je Session oder Kontext verdichtet) | **B** | Zaehlbar und nachvollziehbar (L10 Ersetzungsprobe statt Gefuehl); Nutzer-Stopp bleibt Uebersteuerung |
| feature-start „direkt anschliessen" (Z15) | A: implement selbst aufrufen · B: eine Weiter-Zeile mit Befehl | **B** | implement ist gesperrt (`disable-model-invocation`); Selbstaufruf waere Entsperrung = #98 |
| plan-review bei APPROVED | A: Frage auch streichen · B: Frage bleibt | **B** | Festlegung Z7 nennt nur REVISE/REJECTED; bei APPROVED mit WARNs ist das Ja/Nein eine echte Wahl |
| Knopf-Mechanik | blockierende Auswahl (`AskUserQuestion`) | **gesetzt** | impl-review nutzt sie bereits; implement bekommt sie in `allowed-tools` (L75) |
| Abnahme-Ort | A: dieser Worktree · B: Wegwerf-Clone · C: Referenz-Testbett | **B** | Worktree-Guards blockieren Backlog-Schreiben hier; Testbett laeuft auf alter Kit-Version ohne Git |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Kanon-Sektion skills/CLAUDE.md — `30e64ea`
- [x] 1.2 Beispielausgaben — `30e64ea`
- [x] 1.3 Zuordnung gegenpruefen — `30e64ea`
- [x] 2.1 Backlog task + bug-report — `d2e8880`
- [x] 2.2 Backlog feature-plan + feature-fast — `d2e8880`
- [x] 2.3 Slug-Vorschlag + Namensregel — `d2e8880`
- [x] 2.4 Scan-Bestaetigung discover + impl-plan — `d2e8880`
- [x] 3.1 plan-review Direkteinstieg — `a4aedc8`
- [x] 3.2 Lektion-Vormerkung (+ lesson, no-loss-check) — `a4aedc8`
- [x] 3.3 impl-review Sammelliste — `a4aedc8`
- [x] 3.4 feature-start ohne Bereit — `a4aedc8`
- [x] 4.1 Staging + Commit-Message Knopf — `0f1850c`
- [x] 4.2 Manual-Gate Auswahl — `0f1850c`
- [x] 4.3 Naechste Phase Schwelle — `0f1850c`
- [x] 5.1 Eigen-Text-Pruefung — `2a7ba6b`
- [x] 5.2 Doku CLAUDE.md — `2a7ba6b`
- [x] 5.3 Abnahme-Probelauf — `2a7ba6b`

---

## Offene Punkte (Plan)

- `dtb:workflow-resume` traegt ebenfalls „Bereit? Sage "Los"" — nicht Teil der Festlegung; Folge-Idee oder bewusst so lassen?
- #107 (BACKLOG-Spalte „#") beruehrt dieselben vier Backlog-Stellen wie Phase 2 — beim Merge abstimmen
- Prioritaet in `spec.md` noch offen

---

## Umsetzung

Umsetzung mit `/dtb:implement Rueckfragen-Defaults` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/rueckfragen-defaults/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

**Rollout (nach Abschluss, im Haupt-Checkout — nicht in diesem Worktree; Plan-Review 2026-09-30):**
1. Umsetzung + `/dtb:impl-review` abgeschlossen
2. `feature/rueckfragen-defaults` nach `master` mergen
3. `master` pushen — erst dann (L39: `kit-sync` holt den gepushten Stand von `master`, nie HEAD)
4. `/dtb:kit-sync` — ab hier fragen die Skills in allen Projekten nach der neuen Form

**Rueckweg:** Revert-Commit auf `master` → pushen → erneut `/dtb:kit-sync`.

---

**Erstellt mit:** `/dtb:impl-plan`
