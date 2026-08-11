# Implementierungsplan: Autonome Schiene (`dtb:worker`)

**Erstellt:** 2026-08-08
**Feature-Spec:** `features/autonome-schiene/spec.md`
**Geschaetzte Dauer:** 3 Phasen (~3 Sessions)
**Status:** Reviewed (plan-review 2026-08-08: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Erkennungs-Sicht (`dtb:worker` Modus 1) | ~1 Session | Geplant |
| Phase 2 | Ausfuehrung (Modus 2: Worker-Auftrag, Liste, Parallelitaet) | ~1 Session | Geplant |
| Phase 3 | Verankerung (Regeln, Spiegel, Erstlauf, Verteilung) | ~1 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (7 Pfade verifiziert, 1 Neubau-Ziel — L5) + 2 Ergaenzungen aus E2/E3.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-worker/SKILL.md | Neubau-Ziel (Klasse A `skills/dtb-*/SKILL.md` — kit-sync verteilt automatisch, keine kit-sync-Aenderung noetig) |
| skills/dtb-task/SKILL.md | Task-Lane endet mit der Erfassung (`task.md ## Schritte`); genau dort setzt Modus 2 an. Wird NICHT geaendert, nur gelesen |
| skills/dtb-implement/SKILL.md | Checkpoint-Kriterien/Verifikations-Gate — Vorbild fuer das Erfolgs-/Abbruchkriterium im Worker-Auftrag. Wird NICHT geaendert |
| skills/dtb-idea-review/SKILL.md | Dreier-Weiche — bleibt im Erstwurf unangetastet (3e-Entscheid), kein Aenderungsziel |
| skills/dtb-workflow-next/SKILL.md, skills/dtb-workflow-checkpoint/SKILL.md | Bleiben im Erstwurf unangetastet (3e-Entscheid); Gegenprobe in 3.3 prueft nur, ob deren Aussagen weiter tragen |
| skills/CLAUDE.md | Traegt die Governance-Konvention (`disable-model-invocation`-Regel Z. 27) und die Skill-Kategorien-Doku — beide bekommen Ergaenzungen |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §1.1 fuehrt `review.md` + `fast-draft.md` als status-neutral (Z. 22-23); `worker-report.md` wird dritter Eintrag; Fusszeile fuehrt die Seed-Skew-Historie (#22) |
| workflow.config.yaml | Kit-eigene Config, Platzhalter unbefuellt; bekommt den `worker:`-Limits-Block |
| skills/dtb-project-init/SKILL.md | Erzeugt `workflow.config.yaml` in Zielprojekten — dessen Config-Template muss den `worker:`-Block mitbekommen (Spiegel-Kopplung) |

---

## Phase 1: Erkennungs-Sicht

### Ziel
`/dtb:worker` ohne Argument liefert die komplette Erkennungs-Sicht ueber die INBOX; die
Freigabe-Mechanik steht. Es wird noch nichts ausgefuehrt.

### Schritte

#### Schritt 1.1: Skill-Geruest + Frontmatter
- **Zweck:** Klasse-A-Artefakt anlegen, Governance ab der ersten Zeile korrekt
- **Dateien:** `skills/dtb-worker/SKILL.md` (neu)
- **Input:** spec.md, Frontmatter-Konventionen aus `skills/CLAUDE.md`
- **Output:** Frontmatter (`name: dtb:worker`, `description` mit Trigger-Phrasen,
  `disable-model-invocation: true`, `argument-hint: "[slug | liste]"`,
  `allowed-tools`, Pipeline-Metadaten: `consumes: [INBOX.md, features/*/task.md,
  workflow.config.yaml]`, `produces: [features/*/worker-report.md, features/*/task.md]`);
  Schritt-0-Config-Block nach Kit-Muster

#### Schritt 1.2: Erkennungs-Sicht (Scan + Urteil)
- **Zweck:** Der Kern von Modus 1 — die Sicht, die der Nutzer vor jeder Freigabe sieht
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** 4 Tauglichkeits-Kriterien (Zielzustand mechanisch verifizierbar; Scope
  geschlossen; keine Fremdwirkung/Spiegel-Kopplung; umkehrbar), INBOX- und
  `task.md`-Formate
- **Output:** Skill-Abschnitt Modus 1: Scan ueber INBOX-Eintraege (`Offen`/`Ausgearbeitet`)
  und `features/*/task.md`; je Eintrag Urteil (ja/teilweise/nein) + 1-Satz-Begruendung;
  Abhaengigkeiten + empfohlene Reihenfolge; **Nebenspalte Vorab-Fragen**; Leerfall
  („kein Eintrag tauglich" → je Eintrag begruenden was fehlt); Hinweis „Idee ohne
  Change-Ordner → erst `/dtb:task`". Scanner-Abschnitt strukturell so schneiden, dass
  ein zweites Bewertungsraster (#33) andocken kann (eigene Unterueberschrift je Raster)

#### Schritt 1.3: Freigabe-Dialog
- **Zweck:** Die Governance-Klammer vorn — nichts laeuft ohne explizite Freigabe
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** 3b-Entscheide (einzeln/Liste), Vorab-Fragen aus 1.2
- **Output:** Freigabe-Schritt: offene Vorab-Fragen der gewaehlten Eintraege werden VOR
  dem Start beantwortet; Wahl „einzelner Eintrag / Liste in vorgeschlagener Reihenfolge";
  Anzeige, welche Listen-Teile parallel laufen wuerden; explizite Bestaetigung als
  Startbedingung. **Stoppweg (plan-review F3):** der Dialog nennt beim Start die
  laufenden Worker und dokumentiert den Abbruch ueber die Task-Verwaltung der Session
  (Worker sind Background-Tasks — listbar und stoppbar); kein eigener Stopp-Mechanismus
  im Erstwurf

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-worker/SKILL.md` mit vollstaendigem Modus 1 (Sicht + Freigabe)

### Checkpoint-Kriterien

#### Automated
- [ ] Datei existiert: `skills/dtb-worker/SKILL.md`
- [ ] `sed -n '1,15p' skills/dtb-worker/SKILL.md | grep -c 'disable-model-invocation: true'` = 1
- [ ] `grep -c 'mechanisch verifizierbar' skills/dtb-worker/SKILL.md` >= 1 (Kriterienkatalog im Sicht-Abschnitt)
- [ ] `grep -c 'Vorab-Frage' skills/dtb-worker/SKILL.md` >= 2 (Nebenspalte + Freigabe-Schritt)
- [ ] `grep -c '/dtb:task' skills/dtb-worker/SKILL.md` >= 1 (Redirect fuer Ideen ohne Change-Ordner)

#### Manual
- [x] Sicht-Format am realen INBOX-Bestand gegengelesen: kompakt, Urteile nachvollziehbar — Laeufe 2026-08-08 (27 Eintraege) und 2026-08-09 (26 Eintraege), Nutzer-Urteil 2026-08-09: bestanden

---

## Phase 2: Ausfuehrung

### Ziel
Modus 2 steht vollstaendig im Skill-Text: Worker-Auftrag, Listen-/Parallel-Logik,
Bericht. Der verdrahtete Traeger ist der Background-Subagent (E4).

### Schritte

#### Schritt 2.1: Worker-Auftrag (Einzel-Task)
- **Zweck:** Der geschlossene Auftrag, den jeder Worker erhaelt — Autonomie nur innerhalb
  dieser Grenzen
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** E1 (strukturelle Trennung), E2 (Deckelung), E4 (Traeger), 3c-Randfaelle
- **Output:** Auftrags-Template im Skill: `## Schritte` aus `task.md` + beantwortete
  Vorab-Fragen + Erfolgskriterien + Deckelung (aus `workflow.config.yaml`, Default
  3 Versuche / 30 Min — Anweisungs-Ebene, kein harter Timer; die Laufzeit wird im
  Bericht ausgewiesen). **Jeder Worker laeuft in einem eigenen Worktree — auch der
  Einzel-Worker (plan-review F1: Worker↔Mensch-Kollision im Arbeitsbaum strukturell
  ausgeschlossen); Ergebnis bleibt als Diff im Worktree bis zur Abnahme.**
  **Vorbedingung vor Start:** Zielbereich clean (`git status`), sonst kein Start.
  Verhaltensregeln im Auftrag: Schreibrechte NUR im eigenen Change-Ordner
  (`## Schritte` abhaken, `worker-report.md`) und im eigenen Worktree; **keine
  Schreibzugriffe ausserhalb des eigenen Worktrees (plan-review F3, Zaun gegen
  praeparierte Eintragstexte)**; niemals committen/pushen; keine zentralen Dateien
  (WORKFLOW_STATUS/INBOX/BACKLOG); bei ungeklaerter Entscheidung Abbruch +
  Rueckmeldung „teilweise" statt Raten; Versuchsschleife intern (pruefen →
  nachbessern → erneut pruefen) bis gruen oder Deckel

#### Schritt 2.2: Listen- und Parallel-Logik
- **Zweck:** Der Listen-Lauf mit dem Parallel-Gate aus der Discovery
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Reihenfolge aus Modus 1, E4 (Worktree nur bei Parallelitaet)
- **Output:** Ablauf-Abschnitt: abhaengige Eintraege sequenziell, unabhaengige mit
  disjunkten Dateien parallel — **ein einheitlicher Ausfuehrungspfad: je Worker immer
  ein Worktree (F1), sequenziell/parallel unterscheiden sich nur in der Anzahl**;
  Degradation ohne Worktree-Faehigkeit (kein Git-Repo) → sequenziell im Arbeitsbaum
  mit Warnhinweis im Freigabe-Dialog („waehrend des Laufs nicht im Repo arbeiten"),
  nie verweigern; Kollisionsregel: zweiter Worker stoppt; „teilweise"-Eintraege
  ueberspringen und am Ende gesammelt melden

#### Schritt 2.3: Bericht + Abschluss-Meldung
- **Zweck:** Rechenschaft pro Task, kompakte Meldung im Chat
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** 3b-Entscheid (voller Bericht pro Task), Statuskonvention (1-Zeilen-Summaries)
- **Output:** `worker-report.md`-Template (was getan / was verifiziert / was aufgefallen /
  Versuchszaehler / **Startzeit, Endzeit, Dauer je Versuch — Laufzeit-Ausweis,
  plan-review F3** / Ausgang: gruen | Deckel erreicht | teilweise | gestoppt) + Regel:
  im Chat nur 1 Sammel-Zeile je Task mit Link; Hinweis auf Abnahme durch den Menschen
  als naechsten Schritt

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Modus 2 vollstaendig in `skills/dtb-worker/SKILL.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'worker-report.md' skills/dtb-worker/SKILL.md` >= 3 (Auftrag, Template, Meldung)
- [ ] `grep -c 'Worktree' skills/dtb-worker/SKILL.md` >= 2 (Parallel-Fall + Degradation)
- [ ] `grep -ci 'niemals committen\|nie committen' skills/dtb-worker/SKILL.md` >= 1 (Verbotsliste im Auftrag)
- [ ] Positiv-Gegenprobe zur Verbotsliste (#54-Muster): `grep -c 'Schritte.*abhaken\|abhaken.*Schritte' skills/dtb-worker/SKILL.md` >= 1 (die erlaubte Schreib-Wirkung bleibt ausdruecklich benannt)
- [ ] `grep -c 'ausserhalb des eigenen Worktrees' skills/dtb-worker/SKILL.md` >= 1 (Zaun in der Verbotsliste, F3)
- [ ] `grep -c 'teilweise' skills/dtb-worker/SKILL.md` >= 3 (Urteil, Abbruchpfad, Listen-Sammlung)

#### Manual
- [x] Auftrags-Template gedanklich gegen `gitattributes-eol` durchgespielt: alle 3c-Randfaelle haben einen definierten Ausgang — Durchgang 2026-08-09 ueber die 6 Randfaelle aus `discovery.md:63-77`, je Fall Fundstelle im Skill belegt (Deckelung Z. 156-159/203 · Abbruch-Verbot Z. 170-171 · Listen-Ueberspringen Schritt 7.3 · Abnahme-Ablehnung Schritt 9 Z. 234-236 · Kollisionsregel Schritt 7.2 · Leerfall Z. 106-107); zusaetzlich der von der Discovery nicht gefuehrte Fall „strukturell unerreichbare Schritte" via F2/Schritt 5.2b. Nutzer-Urteil: bestanden. Nebenbefund → INBOX #62

---

## Phase 3: Verankerung, Erstlauf, Verteilung

### Ziel
Regelwerk und Spiegel konsistent, Verhalten am realen Fall belegt, Kit verteilt.

### Schritte

#### Schritt 3.1: `worker-report.md` status-neutral deklarieren
- **Zweck:** Der Bericht darf die Statusableitung nicht beruehren
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** §1.1-Tabelle (Muster `review.md`/`fast-draft.md`)
- **Output:** Dritte Zeile in der §1.1-Tabelle + Fusszeilen-Eintrag (Datum, Feature);
  Vermerk „siebter Seed-Skew-Fall" als #22-Beleg

#### Schritt 3.2: Governance-Regel + Spiegel + Config
- **Zweck:** Die Autonomie-Regel kanonisieren, alle Spiegel in einem Schritt
- **Dateien:** `skills/CLAUDE.md`, `CLAUDE.md` (Root, Skill-Kategorien),
  `workflow.config.yaml`, `skills/dtb-project-init/SKILL.md`
- **Input:** 3d-Entscheid (Governance), E2 (Limits)
- **Output:** `skills/CLAUDE.md`: Autonomie-Regel („Autonomie nur zwischen expliziter
  Freigabe und Abnahme; Worker schreiben ausschliesslich in ihren eigenen Change-Ordner")
  + `dtb:worker` in der Kategorien-Doku; Root-`CLAUDE.md`-Spiegel; `worker:`-Block
  (`max_attempts: 3`, `max_minutes: 30`) in `workflow.config.yaml` UND im
  Config-Template von `dtb:project-init`

#### Schritt 3.3: Selbstpruefung gegen die eigene Fehlerklasse + Gegenprobe
- **Zweck:** L15/L16 als eigener Schritt — der neue Text behauptet Zustaende (wer
  schreibt was); genau diese Behauptungen pruefen
- **Dateien:** keine (Pruefschritt; Findings fliessen in 3.1/3.2-Dateien zurueck)
- **Input:** Pruefragefrage vorab ausformuliert: „Traegt jede Aussage des neuen Texts
  darueber, wer welche Datei schreibt, nach dem Umbau — und pflegt jeden von
  `dtb:worker` beschriebenen Zustand wirklich ein benannter Schreiber?"
- **Output:** Repo-weiter Grep nach `worker-report`, `dtb:worker`, `Schritte` in
  skills/ + Regel-Datei; jeder Treffer gegen die Pruefragefrage bewertet; Befunde
  behoben oder als Offener Punkt dokumentiert

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Zwischen-Sync + Erstlauf gegen `gitattributes-eol`
- **Zweck:** Verhaltens-Kalibrierung am realen Fall (Spec-Kriterium 8); zugleich wird
  die seit 2026-08-05 offene Aufgabe erledigt. **Zwischen-Sync zuerst (plan-review F2):**
  der Skill wird aus `~/.claude/` aufgerufen — ohne Sync liefe der Erstlauf gegen eine
  nicht existierende Installation (Bootstrap-Muster von `output-style-gezielt`)
- **Dateien:** `features/gitattributes-eol/task.md` (Schritte abgehakt durch Worker),
  `features/gitattributes-eol/worker-report.md` (neu, durch Worker), `.gitattributes`
  (Arbeitsergebnis des Workers)
- **Input:** committeter Stand aus 3.1-3.3; die Scope-Vorab-Frage (Schritt 1 des
  Tasks) wird im Freigabe-Dialog beantwortet
- **Output:** **Teil A:** Commit → Push → `/dtb:kit-sync sync` (installierte Fassung
  vorhanden). **Teil B:** Sicht gezeigt → Vorab-Frage beantwortet → Freigabe →
  Hintergrund-Lauf im Worktree → `worker-report.md` liegt vor → Abnahme-Urteil des
  Nutzers. **Erstlauf = Einzel-Pfad; die Listen-/Parallel-Kalibrierung ist bewusst
  nachgelagert (plan-review F4a, Vermerk in der Spec).** L14 beachten: der Erstlauf
  ist Verhaltens-Kalibrierung, ersetzt NICHT den Text-Review (den liefert `plan-review`
  vorab bzw. `impl-review` danach)

#### Schritt 3.5: Abschluss-Verifikation (Nachlauf)
- **Zweck:** Fixes aus Erstlauf und Selbstpruefung verteilt, Endzustand belegt
  (Lektion-1-Muster: erst nach Sync ist die Phase gruen)
- **Dateien:** keine Repo-Aenderung (Lock + `~/.claude/`-Kopien ausserhalb)
- **Input:** Stand nach 3.4 (inkl. etwaiger Erstlauf-Fixes)
- **Output:** Falls 3.3/3.4 Fixes erzeugt haben: Commit → Push → zweiter
  `/dtb:kit-sync sync`; Abschluss-`check` 0 Abweichungen; `dtb-worker` als neuer
  Klasse-A-Eintrag im Lock verifiziert

### Deliverables
- [ ] Regelwerk + Spiegel konsistent (3.1/3.2), Selbstpruefung dokumentiert (3.3)
- [ ] `features/gitattributes-eol/worker-report.md` aus dem Erstlauf
- [ ] Kit verteilt, Lock enthaelt `dtb-worker`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'worker-report.md' dtb-project/project-rules/DERIVED_STATE_RULES.md` >= 2 (§1.1-Tabelle + Fusszeile)
- [ ] `grep -c 'max_attempts' workflow.config.yaml` = 1 und `grep -c 'max_attempts' skills/dtb-project-init/SKILL.md` >= 1
- [ ] `grep -c 'dtb:worker' skills/CLAUDE.md` >= 2 (Governance-Regel + Kategorien-Doku)
- [ ] Datei existiert: `features/gitattributes-eol/worker-report.md`
- [ ] `git -C . log --oneline -1` zeigt den Phasen-Commit; `/dtb:kit-sync check` meldet 0 Abweichungen

#### Manual
- [x] Abnahme-Urteil zum Erstlauf: Bericht vollstaendig, Arbeitsergebnis akzeptiert oder begruendet abgelehnt — Erstlauf `gitattributes-eol` 2026-08-08 (Ausgang „teilweise", Diff uebernommen, Aufgabe auf 5/6); zweiter Lauf `pipeline-kanten-reziprok` 2026-08-09 gruen nach 1 Versuch, Diff uebernommen (`a79c218`). Nutzer-Urteil 2026-08-09: bestanden
- [x] 3.3-Pruefprotokoll gegengelesen: keine neue „Zustandsaussage ohne Pfleger" — **Protokoll war nie abgelegt worden** (Schritt 3.3 abgehakt mit `a59662b`, Output nirgends niedergeschrieben) → am 2026-08-09 gegen Stand `4d16740` nachgeholt: 8 Treffer aus `worker-report` / `dtb:worker` / `## Schritte` in `skills/` + `DERIVED_STATE_RULES.md` + Root-`CLAUDE.md`, jeder gegen die Pruefragefrage bewertet, alle tragen. Zwei Nebenbefunde: `worker.next` ohne Gegenrichtung (= bekanntes INBOX #58) und der unbestimmte Ort der Minimal-Notiz bei hartem Stopp (`SKILL.md:196-197` → INBOX #62). Beleg-Luecke selbst → Lektion L20. Nutzer-Urteil: bestanden

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| E1 Schreibkoordination | Lock-Datei, Schreib-Queue, strukturelle Trennung | Strukturelle Trennung (c) | Change-Ordner sind per Slug disjunkt — Kollision strukturell unmoeglich statt verwaltet; setzt Single-Writer-Prinzip fort. Worker hakt `## Schritte` im eigenen `task.md` ab |
| E2 Deckelung | fest im Skill vs. Config; Zahlenwahl | `workflow.config.yaml`, Default 3 Versuche / 30 Min pro Task | Projektweit ueberschreibbar; Grenze pro Task, nicht pro Listen-Lauf. Bewusste Schwaeche (plan-review): Zeit-Grenze ist Anweisungs-Ebene, kein harter Timer — Bericht weist Laufzeit aus |
| E3 Skill-Name | dtb:worker, dtb:autonome-schiene, zwei Skills | `dtb:worker`, ein Skill mit zwei Modi | Englisch wie alle Kit-Skills; kit-sync-Vorbild (check/sync); eine Governance-Flaeche |
| E4 Worker-Form | fest verdrahtet vs. Laufzeit-Wahl | Fest: Background-Subagent je Task; **Worktree immer, auch Einzel-Worker (plan-review F1)**; /loop und /schedule draussen | Ein Testpfad, vorhersagbar, reproduzierbare Berichte; Worker↔Mensch-Kollision strukturell ausgeschlossen; ein einziger Ausfuehrungspfad (sequenziell/parallel = nur Anzahl); Wiederholung lebt im Auftrag (Ziel- statt Zeitsteuerung); beleg-getriebener Ausbau moeglich |
| Berichts-Ort | Change-Ordner vs. eigener Baum | `worker-report.md` im Change-Ordner, status-neutral | Dritter Eintrag der §1.1-Familie; kein zweiter Suchort |
| Integrations-Zuschnitt | Weiche-Stufe, workflow-next-Anzeige | Erstwurf ohne Aenderung an idea-review/workflow-next/workflow-checkpoint | Beleg-getrieben nachruesten (3e-Entscheid) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Skill-Geruest + Frontmatter — `a89b064`
- [x] 1.2 Erkennungs-Sicht (Scan + Urteil) — `a89b064`
- [x] 1.3 Freigabe-Dialog — `a89b064`
- [x] 2.1 Worker-Auftrag (Einzel-Task) — `51809fe`
- [x] 2.2 Listen- und Parallel-Logik — `51809fe`
- [x] 2.3 Bericht + Abschluss-Meldung — `51809fe`
- [x] 3.1 worker-report.md status-neutral — `a59662b`
- [x] 3.2 Governance-Regel + Spiegel + Config — `a59662b`
- [x] 3.3 Selbstpruefung + Gegenprobe (L15/L16) — `a59662b`
- [x] 3.4 Zwischen-Sync + Erstlauf gitattributes-eol — `9927fe9`
- [x] 3.5 Abschluss-Verifikation (Nachlauf) — `166595c`

---

## Umsetzung

Umsetzung mit `/dtb:implement autonome-schiene` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/autonome-schiene/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
