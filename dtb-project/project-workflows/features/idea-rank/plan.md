# Implementierungsplan: idea-rank

**Erstellt:** 2026-09-17
**Feature-Spec:** `features/idea-rank/spec.md`
**Geschaetzte Dauer:** ca. 2-3 Stunden
**Status:** Reviewed (plan-review 2026-09-17: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill `dtb:idea-rank` bauen | ca. 1,5 h | Geplant |
| Phase 2 | Einbindung ins Kit + Probelauf | ca. 1 h | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-idea-rank/SKILL.md` | Existiert nicht (Neubau) |
| `skills/dtb-meeting-agenda/SKILL.md` | Vorbild einer Read-only-Sicht: `disable-model-invocation: false`, `allowed-tools: Read, Glob, Grep`, `produces: []` |
| `skills/dtb-idea-review/SKILL.md` | `pipeline.after: [dtb:idea, dtb:idea-triage]` (Zeile 11) — Gegenkante fehlt |
| `skills/dtb-idea-triage/SKILL.md` | Schreibender Becken-Skill; bleibt unangetastet |
| `CLAUDE.md` | Kategorie „Idea management" nennt `idea`, `idea-review`, `idea-triage` |
| `skills/CLAUDE.md` | Zeile 380: Read-only-Sichten-Liste (`workflow-next`, …, `meeting-agenda`, …) |
| `README.md` | Tabelle „Skills Overview" ab Zeile 65, `idea-review` in Zeile 71 |
| `dtb-project/project-workflows/INBOX.md` | 7 Eintraege mit Status `Offen` (#95, #57, #45, #39, #33, #27, #15) — Probelauf-Basis |

---

## Phase 1: Skill `dtb:idea-rank` bauen

### Ziel
Eine vollstaendige, rein lesende `SKILL.md`, die offene Inbox-Ideen in vier Toepfe rankt und eine Reihenfolge empfiehlt.

### Schritte

#### Schritt 1.1: Frontmatter und Geruest
- **Zweck:** Skill auffindbar und korrekt in die Pipeline eingeordnet
- **Dateien:** `skills/dtb-idea-rank/SKILL.md` (neu)
- **Input:** Vorbild `skills/dtb-meeting-agenda/SKILL.md`, spec.md Scope
- **Output:** Frontmatter (`name: dtb:idea-rank`, `description` mit Ausloese-Phrasen ohne „Triage"/„Becken" und ausdruecklicher Abgrenzung zu `dtb:idea-triage`, `disable-model-invocation: false`, `argument-hint: "[Ideen-Nummern]"`, `allowed-tools: Read, Glob, Grep`, `pipeline: stage: idea, after: null, next: [dtb:idea-review], consumes: [INBOX.md, BACKLOG.md, features/*/spec.md, features/*/plan.md, workflow.config.yaml], produces: []`), Einleitung mit Abgrenzung, Schritt 0 Config laden

#### Schritt 1.2: Bewertungs- und Topf-Logik + Ausgabeformat
- **Zweck:** Kern des Skills — reproduzierbare Zuordnung statt Bauchgefuehl
- **Dateien:** `skills/dtb-idea-rank/SKILL.md`
- **Input:** Toepfe aus INBOX #33, Changelog-Triagen 2026-07-30/2026-08-08 als Muster, Lektion #10 (Ersetzungsprobe statt Quote)
- **Output:** Abschnitte: Inbox laden (Status `Offen`, optionale Nummern-Teilmenge), Querbelege lesen (laufende Changes, BACKLOG), Stufen Aufwand klein/mittel/gross + Nutzen niedrig/mittel/hoch mit 1-Satz-Begruendung, Zuordnungsregel je Topf inkl. Grenzfall-Regel (Vorrang: blockiert vor allem anderen; grosser Aufwand → eigener Fokus; sonst Aufwand/Nutzen-Matrix), Abhaengigkeits-Erkennung, festes Report-Template (Kopf mit Datum + Anzahl, vier Topf-Abschnitte, Abhaengigkeiten, Reihenfolge, `→ /dtb:idea-review`)

#### Schritt 1.3: Randfaelle und Schlussregeln
- **Zweck:** Leere/abweichende Eingaben sauber behandeln, Schreibverbot festhalten
- **Dateien:** `skills/dtb-idea-rank/SKILL.md`
- **Input:** Randfaelle aus discovery.md
- **Output:** Behandlung: Inbox fehlt/leer, keine `Offen`-Eintraege, unbekannte/nicht-offene Nummern im Argument, `In Arbeit`-Ideen nur als Blocker-Kontext, Teil-Routing-Vermerk (Lektion #19), Becken ausgeschlossen (§6.4); Abschnitt „Wichtig" (rein lesend, keine Ablage, jeder Lauf neu) und „Verwandte Skills"

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-idea-rank/SKILL.md` vollstaendig

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f skills/dtb-idea-rank/SKILL.md`
- [ ] `grep -c "^name: dtb:idea-rank$" skills/dtb-idea-rank/SKILL.md` = 1
- [ ] `grep -c "^  produces: \[\]$" skills/dtb-idea-rank/SKILL.md` = 1
- [ ] `grep -E "^allowed-tools:" skills/dtb-idea-rank/SKILL.md` enthaelt weder `Write` noch `Edit` noch `Bash`
- [ ] Alle vier Topf-Namen im Skill, je ein eigener Grep >= 1: `grep -c "Quick Wins"`, `grep -c "strategisch wertvoll"`, `grep -c "wartend/blockiert"`, `grep -c "braucht eigenen Fokus"` (jeweils auf `skills/dtb-idea-rank/SKILL.md`)
- [ ] Becken-Ausschluss verankert: `grep -c "INBOX-BEFUNDE.md" skills/dtb-idea-rank/SKILL.md` >= 1

#### Manual
- [ ] Zuordnungsregel fuer Grenzfaelle ist eindeutig (zwei Leser kaemen zum selben Topf)

---

## Phase 2: Einbindung ins Kit + Probelauf

### Ziel
Der Skill ist in allen Uebersichten eingetragen, die Pipeline-Kante ist beidseitig, und ein Lauf gegen die echte Inbox erfuellt die Success Criteria.

### Schritte

#### Schritt 2.1: CLAUDE.md und skills/CLAUDE.md
- **Zweck:** Kit-Dokumentation und Worktree-Kategorie aktuell
- **Dateien:** `CLAUDE.md`, `skills/CLAUDE.md`
- **Input:** Formulierungsmuster der Nachbar-Eintraege
- **Output:** `idea-rank` in Kategorie „Idea management" (mit Abgrenzung zu `idea-triage`), `idea-rank` in der Read-only-Sichten-Zeile

#### Schritt 2.2: README und idea-review-Gegenkante
- **Zweck:** Oeffentliche Skill-Tabelle und Pipeline-Graph konsistent
- **Dateien:** `README.md`, `skills/dtb-idea-review/SKILL.md`
- **Input:** Tabelle „Skills Overview", Frontmatter idea-review
- **Output:** Tabellenzeile `/dtb:idea-rank` nach `/dtb:idea-review`; `after: [dtb:idea, dtb:idea-triage, dtb:idea-rank]`; repo-weiter Grep auf weitere Skill-Listen (Lektion #3), Befunde nachziehen oder begruendet auslassen — bekannter Kandidat: `skills/dtb-workflow-status/SKILL.md` (Einstiegs-Tabelle, Zeile „Idee bewerten → `/dtb:idea-review`")

#### Schritt 2.3: Probelauf gegen die aktuelle Inbox
- **Zweck:** Wirkung belegen, nicht nur Text pruefen (Lektion #14)
- **Dateien:** `features/idea-rank/plan.md` — Pruefprotokoll als Abschnitt `## Probelauf 2026-MM-DD` am Planende (Lektion #20; bewusst nicht `review.md`: die Datei gehoert `dtb:impl-review` und wird dort als Snapshot ueberschrieben)
- **Input:** fertiger Skill, `INBOX.md` (7 offene Ideen). Lauf mit der Repo-Fassung `skills/dtb-idea-rank/SKILL.md` (Datei lesen und befolgen), nicht mit einer installierten Kopie — `~/.claude/skills/` kennt den Skill erst nach Merge + `dtb:kit-sync`, und kit-sync zieht von GitHub (Lektion #39)
- **Output:** Report des Laufs; `INBOX.md` unveraendert (git diff); Protokoll mit Zuordnung je Idee und Auffaelligkeiten

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Eintraege in `CLAUDE.md`, `skills/CLAUDE.md`, `README.md`
- [ ] Gegenkante in `skills/dtb-idea-review/SKILL.md`
- [ ] Probelauf-Protokoll

### Checkpoint-Kriterien

#### Automated
- [ ] Kategorie-Zeile: `grep "^- \*\*Idea management\*\*" CLAUDE.md | grep -c "\`idea-rank\`"` = 1
- [ ] Read-only-Zeile: `grep "^| \*\*Read-only-Sichten\*\*" skills/CLAUDE.md | grep -c "idea-rank"` = 1
- [ ] `grep -c "^| \`/dtb:idea-rank\`" README.md` = 1
- [ ] `grep -E "^  after:" skills/dtb-idea-review/SKILL.md | grep -c "dtb:idea-rank"` = 1
- [ ] `grep -c "^## Probelauf" dtb-project/project-workflows/features/idea-rank/plan.md` >= 1
- [ ] Inbox unveraendert: `git diff --exit-code -- dtb-project/project-workflows/INBOX.md` → Exit 0
- [ ] Kein Becken-Eintrag im Report: Nummern aus `INBOX-BEFUNDE.md` (`^| {N} |`) minus Nummern aus `INBOX.md` bilden → Liste nicht leer (Gate, Lektion #7), dann jede Nummer als `#{N}\b` im `## Probelauf`-Abschnitt von `plan.md` suchen → 0 Treffer

#### Manual
- [ ] Probelauf-Report gelesen: jede offene Idee genau einmal zugeordnet, Begruendungen tragen, Reihenfolge nachvollziehbar

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger | eigener Skill / Modus von idea-review | eigener Skill | Name 2026-09-17 entschieden; keine Vermischung lesend/schreibend |
| Persistenz | Chat-only / Datei | Chat-only | Rangliste veraltet schnell; per Veto-Vorlage bestaetigt 2026-09-17 |
| Bewertungsquellen | nur Inbox / + features+BACKLOG / + Changelog | Inbox + features + BACKLOG | Blocker erkennbar, Lauf bleibt schnell; per Veto-Vorlage bestaetigt 2026-09-17 |
| Bewertungsskala | Zahlen / grobe Stufen | grobe Stufen | Lektion #10 (keine Schein-Messbarkeit) |
| Pipeline-Einordnung | monitoring ohne Kanten / idea mit `next: idea-review` | `stage: idea`, `next: [dtb:idea-review]` | Vorstufe des Reviews sichtbar im Graph; per Veto-Vorlage bestaetigt 2026-09-17 |
| Ausloesung | nur manuell / auch natuerlich-sprachlich | natuerlich-sprachlich | Read-only-Sichten sind gefahrlos (Vorbild meeting-agenda) |
| Regel-Reihenfolge Topf-Zuordnung | Aufwand vor Nutzen / Nutzen niedrig vor Aufwand gross | Nutzen niedrig vor Aufwand gross | Eine Idee ohne belegten Bedarf wartet auf Anlass, auch wenn sie gross ist (Praxis 2026-07-30); weicht von der Vorrang-Kette in Schritt 1.2 ab — Manual-Gate Phase 1 bestaetigt 2026-09-17, nachgetragen aus impl-review Lauf 2 |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Frontmatter und Geruest — `fedfac6`
- [x] 1.2 Topf-Logik und Ausgabeformat — `fedfac6`
- [x] 1.3 Randfaelle und Schlussregeln — `fedfac6`
- [x] 2.1 CLAUDE.md und skills/CLAUDE.md — `3563fce`
- [x] 2.2 README und idea-review-Gegenkante — `3563fce`
- [x] 2.3 Probelauf gegen die Inbox — `3563fce`

---

## Umsetzung

Umsetzung mit `/dtb:implement idea-rank` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/idea-rank/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

## Probelauf 2026-09-17

**Lauf:** Repo-Fassung `skills/dtb-idea-rank/SKILL.md`, gelesen und befolgt im Worktree `pane-idea-rank`; ohne
Argument. Quellen: `INBOX.md` (7 × `Offen`, 0 × `In Arbeit`), `BACKLOG.md` (alle Tabellen leer), `features/*/`
(nur `idea-rank`). Becken nicht gelesen. Zwei Durchgaenge: Lauf 1 gegen Stand `fedfac6`, Lauf 2 nach der
Regel-Korrektur in 4.2 (vor dem Abschnittstausch im impl-review: 4.3) (Mismatch-Entscheid 2026-09-17, Option 1a).

| Idee | Aufwand | Nutzen | Regel (4.4) | Topf |
|------|---------|--------|-------------|------|
| #33 | mittel | hoch | 5 | strategisch wertvoll |
| #95 | gross | hoch | 3 | braucht eigenen Fokus |
| #57 | gross | mittel | 3 | braucht eigenen Fokus |
| #27 | klein | niedrig | 2 (+ ↪ Verweis ausserhalb der Inbox) | wartend/blockiert |
| #45 | gross | niedrig | 2 | wartend/blockiert |
| #39 | gross | niedrig | 2 | wartend/blockiert |
| #15 | gross | niedrig | 2 | wartend/blockiert |

Jede der 7 Ideen genau einmal zugeordnet. Quick Wins leer. Reihenfolge: #33 → #95 → #57; danach #27, #45, #39,
#15 bei Anlass. Abhaengigkeiten: keine erkannt.

**Auffaelligkeiten:**

1. **Lauf 1 — Verweis ins Becken als Blocker gefuehrt (behoben).** #27 nennt eine Reihenfolge-Abhaengigkeit zu
   einer Nummer, die nicht in `INBOX.md` steht. Lauf 1 fuehrte sie nach der alten Regel in 4.2 (vor dem Abschnittstausch im impl-review: 4.3) als Blocker „Stand
   unklar" und als Abhaengigkeit — tatsaechlich ist es ein nie befoerderter Becken-Eintrag (Altbestand). Das
   Automated-Kriterium „kein Becken-Eintrag im Report" schlug an. Ursache: Der Skill darf das Becken nicht lesen,
   kann Becken-Nummern also nicht von archivierten Ideen unterscheiden. Korrektur: Verweise ausserhalb der Inbox
   erzeugen keine Abhaengigkeit, die Nummer wird nicht uebernommen, die Zeile traegt einen `↪`-Hinweis. Topf von
   #27 unveraendert (Regel 2 greift ohnehin).
2. **#33 wird als offen gerankt, obwohl er in diesem Worktree bearbeitet wird.** Der `In Arbeit`-Flip ist per
   Teil-Guard auf den Hand-off verschoben — der Skill sieht korrekt den Inbox-Stand. Kein Skill-Fehler; derselbe
   Befund wie #95 Punkt (4) (Worktree-Fortschritt unsichtbar bis Merge).
3. **#15 nennt sich selbst „braucht zusammenhaengenden Fokus", landet aber in wartend/blockiert.** Regel 2 (Nutzen
   niedrig) greift vor Regel 3 — regelkonform und begruendet (schwacher Nutzungsfrequenz-Test laut Text).
4. **Stufen-Grenzfaelle entschieden per Vorsichtsregel:** #39 Aufwand mittel/gross → gross; #15 Nutzen
   mittel/niedrig → niedrig.
5. **Repo-weiter Grep (2.2, Lektion #3): zwei Kandidaten bewusst ausgelassen.**
   `skills/dtb-workflow-status/SKILL.md` — die Tabelle „Beteiligte Skills & Agents" fuehrt nur Uebergaenge der
   Hauptpipeline; `idea-triage` steht dort ebenfalls nicht, eine optionale Lese-Vorstufe gehoert nicht hinein.
   `skills/dtb-pipeline-graph/SKILL.md` Zeile 199 — Textzeile der Hauptpipeline, ebenfalls ohne optionale
   Vorstufen. (Nachgetragen aus impl-review 2026-09-17, Befund F6.)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-17)
