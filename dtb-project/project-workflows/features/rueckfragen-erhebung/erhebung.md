# Rückfragen-Erhebung (Station 1)

**Datum:** 2026-09-21
**Auftrag:** `features/rueckfragen-erhebung/task.md` (Vorarbeit für INBOX #57 / #97 / #98 / #99)
**Erhoben von:** Worker `rueckfragen-erhebung` (Subagent, Worktree `worker-rueckfragen-erhebung`)

## Quellen (ausschliesslich lesend)

- `dtb-project/project-changelog/` — 53 Tagesdateien, 2026-03-12 bis 2026-09-18 (7.935 Zeilen). Pfadangaben in den Tabellen unten sind relativ zu diesem Ordner, z. B. `2026-07/2026-07-21.md`.
- `dtb-project/project-workflows/features/` — 1 aktiver Change-Ordner (`rueckfragen-erhebung/task.md`)
- `dtb-project/project-workflows/archive/` — 43 archivierte Change-Ordner: 33 mit `discovery.md` (28 via `/dtb:feature-discover`, 5 via `/dtb:feature-fast`), 3 mit `bug.md`, 7 mit `task.md`; dazu `ARCHIVE_LOG.md`
- `dtb-project/project-workflows/BACKLOG.md` (Zeile 22, einziger Beleg für den heutigen Task)
- `skills/dtb-{feature-discover,feature-plan,impl-plan,plan-review,feature-start,implement,impl-review,task,feature-fast}/SKILL.md` — nur für Schritt 4 (Fragetexte), nur gelesen
- Zum Verständnis: `INBOX.md` #57, #97, #98, #99

**Lesart der Spalte „abweichend?":** `ja` nur, wenn der Log die Abweichung ausdrücklich belegt; `nein` nur, wenn der Log die Übernahme des Vorschlags/Defaults ausdrücklich belegt; `n. e.` = nicht ermittelbar (Session-Logs sind Ergebnis-, keine Verlaufsprotokolle — eine übernommene Rückfrage hinterlässt dort in der Regel keine Zeile).

---

## Schritt 1 — Slug-Vorschlag (`dtb:feature-discover` Schritt 5, `dtb:feature-fast` Schritt 3)

**Fragetext im Skill:** `Feature-Name festlegen: 1. {Name} (Recommended) → Ordner: features/{slug}/  2. Alternativer Name (angeben)` (`skills/dtb-feature-discover/SKILL.md:163-168`); `feature-fast` leitet den Slug still ab und fragt nur bei Kollision (`skills/dtb-feature-fast/SKILL.md:71-73`).

**Obergrenze:** 33 Change-Ordner mit `discovery.md` in `archive/` (28 discover + 5 fast). Eine 34. Discovery (#15) wurde vor Schritt 5 abgebrochen und hinterliess keinen Ordner.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-20 | `2026-07/2026-07-20.md` | 79, 103 | meeting-dump (#24), feature-discover, Discovery bis 3c | Arbeits-Slug `meeting-nachbereitung`, „Name/Slug final" als offener Schritt | Slug am Discovery-Ende auf `meeting-dump` geändert („Slug = Skill-Name") | **ja** |
| 2026-07-21 | `2026-07/2026-07-21.md` | 9-10 | meeting-dump (#24) | Vollzug derselben Entscheidung | Ordner `meeting-nachbereitung/` → `meeting-dump/` per `git mv` | (Beleg zur Zeile darüber) |
| 2026-08-02 | `2026-08/2026-08-02.md` | 11, 41-42 | meeting-agenda (#25), feature-fast (E2E-Lauf 2) | Slug-Ableitung; der Plan sah `fach-agenda` vor | `meeting-agenda` — „Nutzer-Entscheid im Lauf: englische Skill-Namen", Paar zu meeting-dump | **ja** |
| 2026-08-03 | `2026-08/2026-08-03.md` | 232-233 | abnahme-zustand (#38), feature-fast | Slug-Ableitung | „Slug `abnahme-zustand`" — übernommen | nein |
| 2026-08-06 | `2026-08/2026-08-06.md` | 149-151 | no-loss-check (#29), Discovery-Slug `no-loss-gate` | Slug aus feature-discover | in `/dtb:feature-plan` per `git mv` auf `no-loss-check` geändert („Gate versprach eine Blockade, die der Skill nicht leistet"); INBOX + BACKLOG nachgezogen | **ja** (nachträglich, eine Station später) |
| 2026-09-09 | `2026-09/2026-09-09.md` | 105-107 | idea-rank (#33) | Namensfrage im idea-review: `dtb:idea-triage` ist vergeben | Idee bleibt offen „mit Namens-Klärung" | (Vorlauf) |
| 2026-09-17 | `2026-09/2026-09-17.md` | 38, 6 | idea-rank (#33), feature-fast in Pane | Namensentscheidung VOR dem Fast-Track im Orchestrator | „Variante C — der neue Skill heisst `dtb:idea-rank`"; feature-fast übernahm den Slug, Sammelvorlage bestätigt | nein (Frage vorab entschieden, kein Vorschlag abgelehnt) |
| 2026-07-28 | `2026-07/2026-07-28.md` | 102-104 | #15 Discovery | Schritt 5 nie erreicht | Abbruch vor Ordner-Anlage, „spurenfrei" | n/a |
| 2026-07-09 | `2026-07/2026-07-09.md` | 148, 162 | change-folder-modell (#7) | Slug-Regel eingeführt („kebab-case-Slugs ohne Nummern") | Regel, keine Einzelantwort | (Kontext) |

**Summe: 33 gestellt (Obergrenze), 3 abweichend belegt (2 am Fragepunkt: meeting-dump, meeting-agenda; 1 nachträglich: no-loss-check), 1 vorab entschieden (idea-rank), 1 explizit übernommen (abnahme-zustand), 28 nicht ermittelbar.**

Indiz für die 28 nicht ermittelbaren Fälle: in allen 33 archivierten Ordnern ist der Ordner-Slug eine kebab-/Kurzform des `discovery.md`-Titels (Auszählung `# Discovery: …` gegen Ordnernamen) — kein Fall, in dem Titel und Ordner auseinanderfallen. Das belegt Übernahme des am Ende gültigen Namens, nicht Übernahme des *ersten* Vorschlags.

**Muster der 3 Abweichungen:** alle drei betreffen Features, die einen Kit-Skill liefern, und alle drei lösen den Slug auf den (englischen) Skill-Namen auf. Die Abweichung ist damit regelhaft vorhersagbar („Feature liefert Skill → Slug = Skill-Name") — ein besserer Default würde sie auf 0 senken. Revisionskosten belegt: `git mv` plus 2-3 Anzeige-Zeilen (`2026-08-06.md:149-151`), einmal eine Station später ohne Folgeschaden.

---

## Schritt 2 — Backlog-Frage in `dtb:task`

**Fragetext im Skill:** `Soll die Aufgabe in BACKLOG.md eingetragen werden? (Ja/Nein)` (`skills/dtb-task/SKILL.md:204-208`).

**Obergrenze:** 8 `task.md` (7 in `archive/`, 1 in `features/`) plus belegte Wegwerf-/Testläufe.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-08-05 | `2026-08/2026-08-05.md` | 91-96, 113 | gitattributes-eol (#28), `/dtb:task` real | Backlog? | **Ja** — „BACKLOG: Zeile in der Aufgaben-Tabelle + Datum" | nein |
| 2026-08-09 | `2026-08/2026-08-09.md` | 19, 41 | pipeline-kanten-reziprok (#46 Teil-Routing) | Backlog? | **Ja** — „BACKLOG.md — Aufgaben-Zeile `pipeline-kanten-reziprok`" | nein |
| 2026-08-16 | `2026-08/2026-08-16.md` | 29-30, 38 | pipeline-kante-worker-checkpoint (#58), `/dtb:task` | Backlog? | **Ja** — „BACKLOG.md - Aufgaben-Zeile neu/Erledigt" | nein |
| 2026-08-16 | `2026-08/2026-08-16.md` + `2026-08/2026-08-18.md` | 130-133 / 35, 55 | lesestand-ls-portabel, archive-4d-realitaet (Worker-E2E-Queue; Anlage laut 2026-08-18:55 „selbst ein `ja` führt erst über `/dtb:task`") | Backlog? | **Ja** (indirekt: „archivierte Zeilen aus ‚Aktive Features' + ‚Aufgaben'" beim Archivieren entfernt) | nein (indirekt) |
| 2026-09-07 | `2026-09/2026-09-07.md` | 105-108 | Blind-Wirklauf `hana-backup-taeglich/` (Test von capture-duplikat-schutz; parallel bug-report `passwort-klartext-paste/`) | Backlog? | **Nein** — „Backlog-Frage je `Nein`"; Testartefakte danach ungetrackt gelöscht (Z. 113-115) | **ja** (Testkontext) |
| 2026-09-09 | `2026-09/2026-09-09.md` | 108, 127 | idea-review-sofortschreiben (#71), `/dtb:task` | Backlog? | **Ja** — „BACKLOG.md - Aufgaben-Zeile, Status-Sync"; Entfernung 2026-09-12:38 bestätigt die Zeile | nein |
| 2026-09-09 | `2026-09/2026-09-09.md` | 161, 170 | inbox-becken-migration (Anlageweg `/dtb:task` nicht ausdrücklich genannt) | Backlog? | **Ja** — „BACKLOG.md - Aufgaben-Zeile `inbox-becken-migration`, Datum" | nein |
| 2026-09-16 | `2026-09/2026-09-16.md` | 7 | Wegwerf-Aufgabe `abnahmeprobe-start` (Abnahme feature-start-statusfeld; Anlageweg nicht belegt) | Backlog? | **Ja** — „Wegwerf-Item samt BACKLOG-Zeile gelöscht" | nein |
| 2026-09-21 | `dtb-project/project-workflows/BACKLOG.md` | 22 | rueckfragen-erhebung (dieser Task; kein Session-Log) | Backlog? | **Ja** — Zeile in „## Aufgaben" vorhanden | nein |
| 2026-09-17 | `2026-09/2026-09-17.md` | 36 | Nutzerfrage „warum kleine Tasks nicht im BACKLOG landen" → Idee #95 | (Kontext: die Sichtbarkeit der Task-Lane war selbst Gegenstand einer Nachfrage) | — | (Kontext) |

**Summe: 8 reale Tasks → 8× Ja (7 im Log belegt, 1 über BACKLOG.md:22); dazu 1 Wegwerf-Task mit Ja und 1 Blind-Testlauf mit Nein. Nein real: 0 von 8. Nein gesamt: 1 von 10 — und dieses eine Nein war ein Testartefakt, das die BACKLOG-Tabelle bewusst nicht verschmutzen sollte. Nicht ermittelbar: 0 (die BACKLOG-Zeile ist selbst der Beleg).**

Hinweis: derselbe Fragetyp existiert in `dtb:bug-report` (Blind-Lauf `passwort-klartext-paste` ebenfalls Nein, `2026-09-07.md:108`) — nicht Gegenstand des Auftrags, aber dieselbe Datenlage.

---

## Schritt 3 — Nachfrage nach dem Pane-/Worktree-Stand (Beleg für INBOX #97 Punkt 8)

**Behauptung in #97:** „das Nachfragen ist Handarbeit" — Quelle ist `skills/dtb-pane-start/SKILL.md:323` („Es läuft kein blockierender Warteprozess. Anlassbezogen (der Mensch fragt nach dem Stand) …"), kein Log.

**Obergrenze:** 5 belegte Pane-Läufe (Worker-Pane-Träger oder `dtb:pane-start`) im Log. Der E2E-Lauf vom 2026-08-13 lief über einen Subagenten (`2026-08-13.md:98`, `2026-08-14.md:60`) — dort wartet der Orchestrator blockierend, eine Nachfrage ist strukturell unmöglich.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-08-16 | `2026-08/2026-08-16.md` | 17-22 | Worker-Pane `w3:p2`, Task pipeline-kante-worker-checkpoint (Hand-off 14:31) | Stand nachgefragt? | keine Nachfrage protokolliert; Rückweg kam automatisch per `herdr agent prompt` an die Orchestrator-Pane | 0 Nachfragen belegt |
| 2026-08-16 | `2026-08/2026-08-16.md` | 127-133, 161-163, 205, 210 | E2E-Queue `w3:p7`/`w3:p8` (lesestand-ls-portabel ~19:00, archive-4d-realitaet 19:42) | Stand nachgefragt? | keine Fortschritts-Nachfrage; „beide Blöcke kamen automatisch"; nach Abschluss nur Zustandsbeobachtung „Worker-Panes leben noch (manuelles /exit steht aus)" | 0 Nachfragen belegt |
| 2026-08-19 | `2026-08/2026-08-19.md` | 20-25 | `dtb:pane-start` E2E `w3:p5` (Dogfooding) | Stand nachgefragt? | „Erkennung beim ersten Poll" = Start-Erkennung, keine Stand-Nachfrage; Session wartete, 0 Dateiänderungen | 0 Nachfragen belegt |
| 2026-08-19/20 | `2026-08/2026-08-20.md` | 7-10, 63-64 | Pane-Session `w3:p6`, capture-duplikat-schutz (Hand-off 2026-08-19 21:24) | Stand nachgefragt? | keine Nachfrage protokolliert; „Orchestrator-Nachlauf" erst nach dem Hand-off | 0 Nachfragen belegt |
| 2026-09-17 | `2026-09/2026-09-17.md` | 39-40, 54 | Pane `w3:p9`, idea-rank (Hand-off 13:34) | Stand nachgefragt? | „Die Orchestrator-Session hat nur vorbereitet (Idee, Namensfrage, Commit), der Bau lief komplett in der Pane" — keine Nachfrage | 0 Nachfragen belegt |
| 2026-09-18 | `2026-09/2026-09-18.md` | 7 | Idee #97 erfasst | (Behauptung) | „das Nachfragen ist Handarbeit" — zitiert die Skill-Regel, nennt keinen Fall | — |

**Summe: 5 Pane-Läufe (Obergrenze), 0 belegte Nachfragen nach dem Pane-/Worktree-Stand, 5 nicht ermittelbar (eine Chat-Nachfrage ohne Artefaktfolge hinterlässt keine Log-Zeile).**

Einordnung: In allen fünf Läufen kam der Rückweg als automatischer Hand-off-Block an, bevor der Orchestrator etwas tat. Was die Logs stattdessen zeigen, ist eine **Aufräum-Lücke** (Panes/Worktrees leben nach Abschluss weiter: `2026-08-16.md:174/210`, `2026-08-20.md:103-104`, `2026-09-07.md:10-11`, `2026-09-17.md:58`) und eine **Anzeige-Lücke** (#95 (4), `2026-09-17.md:36`) — beides keine Fortschritts-Nachfrage. Der Nutzen eines getakteten Lese-Laufs (#97) ist damit **nicht belegt**; die belegten Lücken liegen beim Abbau und bei der Anzeige.

---

## Schritt 4 — Weitere Rückfragen der Voll-Schiene

Durchsucht: `skills/dtb-{feature-discover,feature-plan,impl-plan,plan-review,feature-start,implement,impl-review}/SKILL.md` (plus `dtb-feature-fast` als Vergleich). Aufgenommen sind nur Rückfragen, deren Antwort keine Festlegung trägt bzw. einen vorgeschlagenen Default bestätigt. Echte Entscheidungsfragen (plan-review Runde 4 „Fragen an Damian", Klärungsfragen 3a-3e in feature-discover, Kernfragen in feature-fast) sind ausdrücklich **nicht** Gegenstand — sie werden nur dort erwähnt, wo sie an eine Bestätigungsfrage angrenzen.

### 4a — `feature-plan` Schritt 10 / `feature-fast` Schritt 7: „Soll das Feature in BACKLOG.md eingetragen werden? (Ja/Nein)"

Fragetext: `skills/dtb-feature-plan/SKILL.md:185-189`; `skills/dtb-feature-fast/SKILL.md:248` („BACKLOG anbieten, analog feature-plan Schritt 10"). Obergrenze: 33 `spec.md` (28 feature-plan + 5 feature-fast).

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-13 | `2026-07/2026-07-13.md` | 266, 287 | greenfield-autoren-skills (#11) | Backlog? | Ja — „BACKLOG-Zeile Geplant" | nein |
| 2026-07-29 | `2026-07/2026-07-29.md` | 145 | `backlog-status`-Lauf | (Gegenprobe) | „6 Items, 0 Statuskonflikte, keine Backlog-Lücke" → alle Ordner hatten Zeilen | nein (für alle Items zu diesem Zeitpunkt) |
| 2026-08-02 | `2026-08/2026-08-02.md` | 11 | meeting-agenda (#25), feature-fast | Backlog? | Ja — „BACKLOG Geplant/Mittel" | nein |
| 2026-08-04 | `2026-08/2026-08-04.md` | 12-13 | `backlog-status`-Lauf | (Gegenprobe) | „8 Features … alle Ordner im BACKLOG erfasst" | nein (für alle Items) |
| 2026-08-05 | `2026-08/2026-08-05.md` | 12-20 | Nutzerfrage zur No-Loss-Lücke | (Kontext) | „der BACKLOG-Eintrag ist optional (feature-plan Schritt 10, Ja/Nein) — aber ein Ordner ohne BACKLOG-Zeile ist kein blinder Fleck" | (Kontext: Revisionskosten = 0, Anzeige-Redundanz) |
| 2026-08-08 | `2026-08/2026-08-08.md` | 75 | autonome-schiene (#43) | Backlog? | Ja — „BACKLOG.md — neuer Eintrag" | nein |
| 2026-08-19 | `2026-08/2026-08-19.md` | 57 | pane-start (#68), feature-fast | Backlog? | Ja — „Zeile `pane-start`, Status Fertig zum Testen" | nein |
| 2026-08-20 | `2026-08/2026-08-20.md` | 56 | capture-duplikat-schutz (#48) | Backlog? | Ja — „Zeile `capture-duplikat-schutz`" | nein |
| 2026-09-08 | `2026-09/2026-09-08.md` | 61 | checkpoint-verlustfunde (#72) | Backlog? | Ja — „Zeile `checkpoint-verlustfunde`, Letzte Aktualisierung" | nein |
| 2026-09-09 | `2026-09/2026-09-09.md` | 110-111 | `backlog-status`-Lauf | (Gegenprobe) | „kein Item ausserhalb des Backlogs" | nein (für alle Items) |
| 2026-09-17 | `2026-09/2026-09-17.md` | 47 | idea-rank (#33), feature-fast (im Worktree übersprungen, im Orchestrator nachgezogen, Z. 44) | Backlog? | Ja — „Zeile `idea-rank` unter Aktive Features" | nein |

**Summe: 33 gestellt (Obergrenze), 0 Nein belegt, 7 Ja einzeln belegt, 3 `backlog-status`-Gegenproben belegen zu ihrem Zeitpunkt Zeilen für alle vorhandenen Ordner, 26 Einzelantworten nicht protokolliert (aber durch die Gegenproben abgedeckt).**

### 4b — `feature-discover` Kleinfall-Weiche: „Fast-Track nehmen?"

Fragetext: `skills/dtb-feature-discover/SKILL.md:50-59` (seit 2026-08-02, `2026-08-02.md:8`). Wird nur bei „klein wirkenden" Ideen gestellt.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-08-05 | `2026-08/2026-08-05.md` | 99 | #35 im idea-review (Dreier-Weiche, Nachbar der Kleinfall-Weiche) | Lane? | „Einschätzung: Voll-Schiene, kein Fast-Track — 5 offene Punkte" | n. e. (Einschätzung des Skills, Antwort nicht protokolliert) |
| seit 2026-08-02 | — | — | 6 Discover-Läufe (no-loss-check, autonome-schiene, herdr-worker-automation, capture-duplikat-schutz, checkpoint-verlustfunde, ideen-becken) | Weiche angeboten? | kein Log nennt ein Angebot oder eine Antwort | n. e. |

**Summe: 6 Läufe (Obergrenze), 0 belegte Angebote, 0 abweichend, 6 nicht ermittelbar.**

### 4c — Escape-Hatch der Eligibility-Gates: „trotzdem fortfahren" bestätigen

Fragetext identisch in `impl-plan:48-59`, `plan-review:39-51`, `feature-start:93-105`, `implement:60-72`, `impl-review:62-72`. Wird nur gestellt, wenn das kritische Artefakt fehlt.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-13 | `2026-07/2026-07-13.md` | 57 | Block-Test `impl-plan pdf-export` (Spec fehlt) | Escape? | „⛔ Block + Redirect feature-plan + Escape-Hatch ✅" — Testlauf, Escape nicht genutzt | nein |
| 2026-07-18 | `2026-07/2026-07-18.md` | 60 | greenfield-autoren-skills F3 | (Fehlauslösung) | Gate blockte den Report-Modus → Skill-Fix „Vorab-Ausnahme", kein Escape | nein |
| 2026-08-03 | `2026-08/2026-08-03.md` | 232 | abnahme-zustand (#38), feature-fast Eingangs-Gate | INBOX-Eintrag zuerst? | Nutzer legte die Idee an (`/dtb:idea` #38), kein Umgehen | nein |

**Summe: 3 belegte Gate-Auslösungen (1 Test, 1 Fehlauslösung, 1 Eingangs-Gate), 0× Escape genutzt, 0 abweichend; alle weiteren Läufe nicht ermittelbar (Gate greift im Normalfall nicht).**

### 4d — `plan-review` Schritt 5: „Möchtest du Anpassungen am Implementierungsplan vornehmen? (Ja/Nein)"

Fragetext: `skills/dtb-plan-review/SKILL.md:185, 336`. Obergrenze = belegte plan-review-Läufe.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-08 | `2026-07/2026-07-08.md` | 123 | Pipeline-Durchlauf #2 | Anpassungen? | Ja — „4 Review-Empfehlungen eingearbeitet" | nein |
| 2026-07-09 | `2026-07/2026-07-09.md` | 14 | Pipeline-Durchlauf #3 | Anpassungen? | Ja — „3 Entscheidungen, 6 Empfehlungen eingearbeitet" | nein |
| 2026-07-09 | `2026-07/2026-07-09.md` | 30 | Pipeline-Durchlauf #3, Finding-Ebene | Pragmatiker-Einwand (Resume-Marker zu komplex) | „Resume-Marker im Scope behalten (trotz Komplexitäts-Einwand)" | **ja** (Finding abgelehnt) |
| 2026-07-09 | `2026-07/2026-07-09.md` | 49, 53 | spec-haertung (#5) | Anpassungen? | Ja — „REVISE → 5 Anpassungen" | nein |
| 2026-07-09 | `2026-07/2026-07-09.md` | 125 | Pipeline-Durchlauf #6 | Anpassungen? | Ja — „Plan-Review REVISE → …" (Marker, Recommended, Abnahme-Strategie) | nein |
| 2026-07-09 | `2026-07/2026-07-09.md` | 148 | change-folder-modell (#7) | Anpassungen? | Ja — REVISE eingearbeitet | nein |
| 2026-07-10 | `2026-07/2026-07-10.md` | 10 | eligibility-gates (#12) | Anpassungen? | Ja — „REVISE → alle Punkte eingearbeitet" | nein |
| 2026-07-13 | `2026-07/2026-07-13.md` | 170 | codebase-research-step (#14) | Anpassungen? | Ja — „REVISE, 3 WARN adressiert" | nein |
| 2026-07-14 | `2026-07/2026-07-14.md` | 53 | (Session-Feature 2026-07-14) | Anpassungen? | Ja — „REVISE, 3 WARN, alle eingearbeitet" | nein |
| 2026-07-15 | `2026-07/2026-07-15.md` | 63 | verifikations-gate | Anpassungen? | Ja — „REVISE, 7 Punkte eingearbeitet" | nein |
| 2026-07-15 | `2026-07/2026-07-15.md` | 192 | (Session-Feature 2026-07-15 S2) | Anpassungen? | Ja — „alle 5 Empfehlungen + 2 R4-Entscheidungen" | nein |
| 2026-07-16 | `2026-07/2026-07-16.md` | 102 | commit-and-push | Anpassungen? | Ja — „REVISE (4 WARN), alle 4 eingearbeitet" | nein |
| 2026-07-17 | `2026-07/2026-07-17.md` | 7 | (Session-Feature 2026-07-17) | Anpassungen? | Ja — „REVISE, alle Punkte …" | nein |
| 2026-07-19 | `2026-07/2026-07-19.md` | 11 | open-question (#26) | Anpassungen? | Ja — „REVISE → 3 WARNs behoben" | nein |
| 2026-07-21 | `2026-07/2026-07-21.md` | 12, 35 | meeting-dump (#24) | Anpassungen? / Datenschutz-FAIL | Ja — 5 Findings; **ein FAIL „durch Damians Einwand entschärft"** (getrackt statt gitignore) | nein / **ja** (Finding entschärft) |
| 2026-08-02 | `2026-08/2026-08-02.md` | 14 | feature-fast (#37) | Anpassungen? | Ja — „REVISE → 3 WARNs behoben" | nein |
| 2026-08-02 | `2026-08/2026-08-02.md` | 68 | meeting-agenda (#25) | Anpassungen? | Ja — „REVISE → 4 WARNs behoben" | nein |
| 2026-08-03 | `2026-08/2026-08-03.md` | 233-235 | abnahme-zustand (#38) | Anpassungen? | Ja — „REVISE, 6 WARNs … alle eingearbeitet" | nein |
| 2026-08-06 | `2026-08/2026-08-06.md` | 153 | no-loss-check (#29) | Anpassungen? | Ja — „REVISE — 7 WARNs, alle eingearbeitet" | nein |
| 2026-08-07 | `2026-08/2026-08-07.md` | 18-23 | output-style-gezielt | Anpassungen? | Ja — „REVISE, 4 WARNs, alle behoben"; „Vier Nutzer-Entscheide" auf Finding-Ebene | nein |
| 2026-08-08 | `2026-08/2026-08-08.md` | 25 | autonome-schiene (#43) | Anpassungen? | Ja — „REVISE, 4 WARNs, alle behoben" | nein |
| 2026-08-16 | `2026-08/2026-08-16.md` | 120 | herdr-worker-automation (#67) | Anpassungen? | Ja — „REVISE, 3 WARNs behoben" | nein |
| 2026-08-19 | `2026-08/2026-08-19.md` | 10-11 | pane-start (#68) | Anpassungen? | Ja — „REVISE, 5 WARNs → alle behoben" | nein |
| 2026-08-20 | `2026-08/2026-08-20.md` | 9 | capture-duplikat-schutz (#48) | Anpassungen? | Ja — „REVISE, 3 WARNs behoben" | nein |
| 2026-09-08 | `2026-09/2026-09-08.md` | 32-39 | checkpoint-verlustfunde (#72) | Anpassungen? | Ja — 4 WARNs; **„1.3 (b)/3.1 bleiben mit Spec-Nachtrag"** (zwei Findings nicht als Plan-Änderung, sondern per Spec-Nachtrag) | nein / **ja** (Finding anders gelöst) |
| 2026-09-09 | `2026-09/2026-09-09.md` | 25 | ideen-becken (#76) | Anpassungen? | Ja — „REVISE (6 WARNs), alle 6 einzeln entschieden und eingearbeitet" | nein |
| 2026-09-17 | `2026-09/2026-09-17.md` | 7 | idea-rank (#33) | Anpassungen? | Ja — „REVISE, 3 WARNs einzeln besprochen und behoben" | nein |

**Summe: 26 belegte Läufe, Verdikt in allen 26 Fällen REVISE, Ja/Nein-Frage 26× Ja, 0× Nein; auf Finding-Ebene 3 belegte Abweichungen (1 Finding abgelehnt, 1 entschärft, 2 anders gelöst — in 2 Läufen).** Kein plan-review-Lauf mit Verdikt APPROVED belegt — die Ja/Nein-Frage hatte in keinem belegten Fall einen anderen Ausgang als Ja; die Entscheidungsarbeit liegt vollständig in den Einzel-Findings.

### 4e — `implement` Schritt 4 Punkt 2, Manuelles Bestätigungs-Gate: „Bestätige (‚passt') oder nenne Korrekturen"

Fragetext: `skills/dtb-implement/SKILL.md:147-157` (seit verifikations-gate 2026-07-15, `2026-07-15.md:69`); Regel „wird IMMER gestellt" (`2026-09-18.md:10`). Obergrenze: 110 Phasen in 33 archivierten `plan.md`, davon 57 mit `#### Manual`-Block (Plan-Form nach 2026-07-15).

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-30 | `2026-07/2026-07-30.md` | 51-56 | commit-and-push Schritt 4.3 (Nachbar-Skill, gleiche Frageform) | Freitext „passt" | **wurde übersehen — „der Lauf versandete still, Arbeit blieb uncommittet"**; danach auf blockierende Auswahlfrage gehärtet | **ja** (Form-Befund: Freitext-Bestätigung ohne Default wird verpasst) |
| 2026-08-16 | `2026-08/2026-08-16.md` | 129 | herdr-worker-automation Phase 4 | Manual 4.3? | „im Gate bestätigt" | nein |
| 2026-09-08 | `2026-09/2026-09-08.md` | 99 | checkpoint-verlustfunde Phase 2 | Manual? | „12/12 Automated grün, 2 Manual" bestätigt | nein |
| 2026-09-08 | `2026-09/2026-09-08.md` | 423 | checkpoint-verlustfunde Phase 3 | Manual? | „2 Manual bestätigt" | nein |
| 2026-09-16 | `2026-09/2026-09-16.md` | 9 | feature-start-statusfeld, Abnahme-Kriterium „Rückweg" (Kriterium aus dem Plan, im Checkpoint geprüft) | Kriterium erfüllt? | **„fiel im ersten Durchgang durch und wurde nach Korrektur bestanden"** (Platzhalter-SHAs, falsche Commit-Zahl) | **ja** (Korrektur statt „passt") |
| 2026-09-17 | `2026-09/2026-09-17.md` | 10 | idea-rank Phasen 1-2 (Pane) | Manual? | „Manual-Gates im Pane bestätigt (‚passt')" | nein |
| 2026-09-17 | `2026-09/2026-09-17.md` | 102 | idea-rank Abnahme, Manual Phase 3 | passt? | „Nutzer-Urteil ‚passt'" | nein |
| 2026-09-17 | `2026-09/2026-09-17.md` | 84 | idea-rank, Lektion L64 | (Kontext) | „Beispiel-Ausgabe als Manual-Gate in Phase 1" — Gate bestand, Ergebnis fiel in der Abnahme durch (vgl. #98 (7)) | (Kontext: Gate-Ja garantiert keinen Nutzen) |

**Summe: 57 Manual-Blöcke / 110 Phasen (Obergrenze), 6 Bestätigungen belegt, 1 Korrektur belegt (Abnahme-Kontext), 1 Form-Befund (Freitext übersehen), 0 Ablehnung am implement-Gate belegt, ≥50 nicht ermittelbar.**

### 4f — `implement` Staging-Frage bei dirty paths: „(1) nur geplantes Set (Empfehlung) / (2) alles / (3) abbrechen"

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-09-08 | `2026-09/2026-09-08.md` | 43 | checkpoint-verlustfunde Phase 1 | Staging-Set? | „‚passt' ohne Nummer → Skill-Default (1)" | nein (Default) |

**Summe: 1 belegt, 0 abweichend; sonst nicht ermittelbar.**

### 4g — `implement` Commit-Message-Vorschlag („Nutzer kann Subject/Body überschreiben")

Fragetext: `skills/dtb-implement/SKILL.md:168-170`. Kein Log nennt eine überschriebene Message; die protokollierten Phasen-Commits folgen dem vorgeschlagenen Muster `<type>({slug}): … (pN)` (z. B. `2026-08-20.md:9-10`, `2026-09-17.md:8-9`). **Summe: n. e. gestellt, 0 abweichend belegt, alle nicht ermittelbar.**

### 4h — `implement` Nächste-Phase-Entscheidung: „(1) direkt weiter / (2) Kontext klären, neue Session / (3) erst Review"

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-21 | `2026-07/2026-07-21.md` | 14-19 | meeting-dump | nächste Phase? | (1) — 3 Phasen in einer Session | nein |
| 2026-08-20 | `2026-08/2026-08-20.md` | 9-10 | capture-duplikat-schutz | nächste Phase? | (1) — 3 Phasen in einer Pane-Session | nein |
| 2026-09-08 | `2026-09/2026-09-08.md` | 411, 423 | checkpoint-verlustfunde Phase 3 | nächste Phase? | **(2)** — Wiedereinstieg `/dtb:implement checkpoint-verlustfunde phase 3` in neuer Session | **ja** |
| 2026-09-17 | `2026-09/2026-09-17.md` | 9-11, 69 | idea-rank | nächste Phase? | Phasen 1-2 direkt, dann Review, dann Phase 3 nachgeplant | gemischt |

**Summe: 4 belegt, 1 klar abweichend (Option 2), 1 gemischt; Regelfall Option 1.**

### 4i — `implement` Mismatch-Dialog: „(1) anpassen und fortfahren / (2) Schritt überspringen / (3) stoppen und neu planen"

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-08-16 | `2026-08/2026-08-16.md` | 134-137 | herdr-worker-automation | Mismatch (2×) | „Zwei genehmigte Mismatch-Entscheide" — je (1) mit inhaltlicher Umplanung (pane run statt agent start; neue Pane je Aufgabe) | echte Entscheidung |
| 2026-09-17 | `2026-09/2026-09-17.md` | 8 | idea-rank Phase 2 | Mismatch | „per Option 1a behoben" | echte Entscheidung |

**Summe: 3 belegt; keine Schein-Rückfrage — die Antwort ist eine Planänderung.**

### 4j — `impl-review` Triage je Finding: „(1) Fix wie vorgeschlagen / (2) anders fixen / (3) Skip / (4) als Lektion"

Fragetext: `skills/dtb-impl-review/SKILL.md:336-346`. Die Frage lautet je Finding „Fix wie vorgeschlagen?"; die Spalte „Frage" nennt die Zahl der so gestellten Fragen (Findings) pro Triage.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|----------|---------|-------------|
| 2026-07-16 | `2026-07/2026-07-16.md` | 11, 23 | verifikations-gate (Selbst-Test) | 3 | 2 Fixed, **F2 SKIPPED** | 1 |
| 2026-07-18 | `2026-07/2026-07-18.md` | 10, 22 | opportunity-map | 6 | „4 Fixed · 0 Lesson · **2 Skipped**" (F5 gewollt, F6 später) | 2 |
| 2026-07-18 | `2026-07/2026-07-18.md` | 55, 64 | greenfield-autoren-skills | 7 | „6 Fixed · 0 Lesson · **1 Skipped**" (F7 kosmetisch) | 1 |
| 2026-07-21 | `2026-07/2026-07-21.md` | 19-22 | meeting-dump | 4 | „Triage: 4 Fixed" | 0 |
| 2026-07-30 | `2026-07/2026-07-30.md` | 201 | (Session-Feature) | 10 | „8 Fixed · 0 Lesson · **2 Skipped**" | 2 |
| 2026-07-31 | `2026-07/2026-07-31.md` | 33, 150 | (Session-Feature) | 10 | „10 Fixed · 0 Lesson · 0 Skipped" | 0 |
| 2026-08-02 | `2026-08/2026-08-02.md` | 15 | feature-fast | 10 | „Triage 10/10 Fixed" | 0 |
| 2026-08-03 | `2026-08/2026-08-03.md` | 251 | abnahme-zustand | 6 | „6 Fixed · 0 Lesson · 0 Skipped" | 0 |
| 2026-08-06 | `2026-08/2026-08-06.md` | 195 | no-loss-check (2 Läufe) | 17 | „17 Fixed, 0 Skipped" | 0 |
| 2026-08-07 | `2026-08/2026-08-07.md` | 167 | feature-start-statusfeld | 9 | „alle 9 gefixt" | 0 |
| 2026-08-08 | `2026-08/2026-08-08.md` | 54, 61 | autonome-schiene | 8 | „7 gefixt, **1 bewusst SKIPPED**" (F8) | 1 |
| 2026-08-16 | `2026-08/2026-08-16.md` | 121 | herdr-worker-automation | 12 | „Triage 12/12 FIXED" | 0 |
| 2026-08-19 | `2026-08/2026-08-19.md` | 13 | pane-start | 13 | „11 Fixed / **1 Skipped / 1 Lesson**" | 2 |
| 2026-08-20 | `2026-08/2026-08-20.md` | 10 | capture-duplikat-schutz | 13 | „in der Triage alle FIXED" | 0 |
| 2026-09-08 | `2026-09/2026-09-08.md` | 425, 430 | checkpoint-verlustfunde | 10 | „9 FIXED · **1 SKIPPED**" (F10) | 1 |
| 2026-09-17 | `2026-09/2026-09-17.md` | 11 | idea-rank (2 Läufe) | 20 | „10 FIXED … 10 FIXED" | 0 |

**Summe: 16 belegte Triagen, 158 Findings, 148 Fixed (94 %), 9 Skipped, 1 Lesson → 10 abweichend vom Fix-Default (6 %).** Jede Abweichung trägt im Log eine Begründung („gewollt", „kosmetisch", „gehört zur nächsten …") — es sind Entscheidungen, aber seltene.

### 4k — `impl-plan` Codebase-Scan-Bestätigung (2b) / `feature-discover` Schritt 2 „Stimmt das so?"

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-13 | `2026-07/2026-07-13.md` | 206 | codebase-research-step Abnahme | Übernahme-Pfad (Skip) | „Übernahme-Pfad (Skip) real ausgelöst" — Liste aus discovery.md übernommen, keine Frage | nein |
| 2026-07-20 | `2026-07/2026-07-20.md` | 80 | meeting-dump Discovery | Scan-Ergebnis bestätigen? | „Codebase-Scan (7 Module, bestätigt)" | nein |

**Summe: 2 belegt, 0 abweichend; sonst nicht ermittelbar.**

### 4l — `feature-start`: „Bereit? Starte mit `/dtb:implement` oder stelle Fragen" / „Sage ‚Los'"

Fragetext: `skills/dtb-feature-start/SKILL.md:145, 171, 189`. In allen belegten Ketten folgte `implement` unmittelbar (`2026-08-20.md:9-10`, `2026-09-08.md:40`, `2026-08-19.md:11`); eine Rückfrage an dieser Stelle ist nirgends protokolliert. Gegenbeispiel mit Absicht: die `pane-start`-Session wartete korrekt und führte den vorgeschlagenen Befehl NICHT selbst aus (`2026-08-19.md:23-25`) — das ist die Wartepflicht des Skills, keine Nutzerantwort. **Summe: n. e. gestellt, 0 abweichend belegt.**

### 4m — `impl-plan` Lektion-Kandidat: „Nach lessons.md übernehmen? (/dtb:lesson oder ja/nein)"

Fragetext: `skills/dtb-impl-plan/SKILL.md:264`. Zuordnung unscharf — dieselbe Frage stellt die Verlustprüfung (`no-loss-check`).

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-09 | `2026-07/2026-07-09.md` | 71 | change-folder-modell | Lektion übernehmen? | in „Nächste Schritte" verschoben („Lektion-Kandidat festhalten … `/dtb:lesson`") | **ja** (nicht sofort) |
| 2026-07-14 | `2026-07/2026-07-14.md` | 82, 115, 152 | greenfield/opportunity | Lektion übernehmen? | dreimal als offener Punkt weitergetragen | **ja** (nicht sofort) |
| 2026-08-07 | `2026-08/2026-08-07.md` | 40 | output-style-gezielt | Lektion übernehmen? | „als Lektion-Kandidat gemeldet (Verlustprüfung, nicht abgesetzt)" | **ja** |
| 2026-08-16 | `2026-08/2026-08-16.md` | 168 | herdr-worker-automation | Lektion übernehmen? | „als Lektion-Kandidat im Verlustreport" | **ja** |

**Summe: 4 belegte Stellen, 4× nicht sofort übernommen — der Default „ja" ist laut Datenlage NICHT der Regelfall.** (Seit `checkpoint-verlustfunde` 2026-09-08 schreibt der Checkpoint dringende Funde selbst — die Frage wandert.)

### 4n — Überschreib-Fragen: „Spec/Plan existiert — überschreiben oder aktualisieren?" (`feature-plan:143`, `impl-plan:218`), review.md-PENDING-Schutz (`impl-review:322-326`)

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-07-16 | `2026-07/2026-07-16.md` | 11 | verifikations-gate Selbst-Test | PENDING überschreiben? | „PENDING-Überschreibschutz live bestätigt" (Test) | nein |

**Summe: 1 Selbsttest belegt, 0 reale Auslösung belegt, sonst nicht ermittelbar.**

### 4o — Vergleich `feature-fast` Sammelvorlage: „Ok zum Schreiben? (Ok / Korrekturen / Voll-Schiene / Abbruch)"

Fragetext: `skills/dtb-feature-fast/SKILL.md:194`. Das ist das Muster „begründeter Default + Veto", das #57 auf die Voll-Schiene übertragen will.

| Datum | Datei | Zeile | Feature/Kontext | Frage | Antwort | abweichend? |
|-------|-------|-------|-----------------|-------|---------|-------------|
| 2026-08-02 | `2026-08/2026-08-02.md` | 11 | meeting-agenda (#25) | Ok? | Ok — „1 Kernfrage statt ~15" (Name), „Abbruch+Wiederaufnahme via fast-draft.md getestet" | nein (Kernfrage genutzt) |
| 2026-08-02 | `2026-08/2026-08-02.md` | 12 | #35 (E2E-Lauf 3) | — | Skill eskalierte selbst („Empfehlung Voll-Schiene, keine Artefakte") | (Skill-Eskalation, keine Nutzerantwort) |
| 2026-08-03 | `2026-08/2026-08-03.md` | 232-233 | abnahme-zustand (#38) | Ok? | Ok — „0 von 3 Kernfragen verbraucht, 12 Annahmen-Vorlage" | nein |
| 2026-08-07 | `archive/feature-start-statusfeld/discovery.md` | 76 | feature-start-statusfeld | Ok? | „Sammelvorlage bestätigt 2026-08-07"; Log (`2026-08-07.md`) nennt keine Vetos | nein (Vetos n. e.) |
| 2026-08-19 | `2026-08/2026-08-19.md` | 10, 14 | pane-start (#68) | Ok? | Ok — „1 Kernfrage + 10 Annahmen, Sammelvorlage bestätigt"; Kernfrage = Trägerschaft („Nutzer-Entscheid: eigener Skill") | nein (Kernfrage genutzt) |
| 2026-09-17 | `2026-09/2026-09-17.md` | 6 | idea-rank (#33) | Ok? | Ok — „11 Annahmen, 0 Kernfragen" | nein |

**Summe: 5 reale Läufe, 5× Ok, 0 belegte Freitext-Korrekturen (n. e., „Unkommentiertes gilt als angenommen"), 2 von 5 Läufen nutzten 1 Kernfrage (Name bzw. Trägerschaft).** Das Muster hält in der Praxis: der Mensch bestätigt einmal, die Kernfragen tragen die echten Entscheidungen.

---

## Abgrenzungskriterium (Vorschlag)

**Kriterium (ein Satz):** Eine Rückfrage ist delegierbar, wenn ihre Antwort keine Festlegung trägt, deren Rücknahme mehr kostet als einen einzelnen, lokal umkehrbaren Schreibvorgang (`git mv`, eine Tabellenzeile, ein Feldwert, ein Staging-Set) — sobald die Antwort Scope, Verhalten oder verteilten Code festlegt oder ein Abnahme-Urteil ersetzt, bleibt sie beim Menschen.

**Begründung aus den Zahlen:**

1. **Die Häufigkeit der Abweichung ist das falsche Kriterium.** Der Slug wurde in 3 von 33 Fällen geändert (9 %) — und trotzdem ist er der klarste Delegations-Kandidat, weil jede Änderung als `git mv` plus zwei Anzeige-Zeilen erledigt war, einmal sogar eine Station später ohne Folgeschaden (`2026-08-06.md:149-151`). Umgekehrt wurde das Manual-Gate in 0 belegten Fällen abgelehnt und bleibt trotzdem beim Menschen, weil L64 zeigt, dass ein bestandenes Gate den Nutzen nicht garantiert (`2026-09-17.md:84`, #98 (7)). Die Achse, die trennt, ist die **Rücknahmekosten der Folge**, nicht die Wahrscheinlichkeit der Abweichung — genau wie #99 es für den Konfidenzwert formuliert.
2. **Die Nullen liegen dort, wo die Antwort redundant ist.** Backlog-Frage (`task`: 0/8 Nein; `feature-plan`/`fast`: 0/33 Nein belegt) und „Anpassungen? (Ja/Nein)" (0/26 Nein) haben keinen Informationsgehalt: die BACKLOG-Zeile ist eine abgeleitete Anzeige, deren Fehlen `backlog-status` meldet (`2026-08-05.md:17-19`); das Ja vor der Anpassungs-Runde ist bei einem REVISE-Verdikt gesetzt. Beide sind streichbar bzw. auf stillen Default umstellbar.
3. **Wo die Antwort variiert, ist sie meist eine echte Entscheidung** — Mismatch-Dialog (3/3 mit Umplanung), Nächste-Phase (1 Wiedereinstieg), Finding-Ebene im plan-review (3 Abweichungen), impl-review-Triage (6 % Skip/Lesson mit Begründung). Diese Fragen tragen Festlegungen (Plan, Code) und bleiben beim Menschen; aber ihr Default („Fix wie vorgeschlagen", „weiter mit Phase N+1") ist in ≥94 % richtig, was für eine **vetobare Vorlage statt Einzelabfrage** spricht.
4. **Die Form entscheidet mit.** Eine Freitext-Bestätigung ohne Default wurde real übersehen und liess den Lauf still versanden (`2026-07-30.md:51-56`); die Härtung war eine blockierende Auswahlfrage mit Optionen. Jeder Veto-Default muss deshalb sichtbar sein und ein eindeutiges „weiter" haben — stiller Default ohne Anzeige ist bei Slug/Backlog vertretbar, bei allem, was einen Commit auslöst, nicht.
5. **Der Pane-Stand ist kein Fragetyp mit Datenlage.** 0 belegte Nachfragen in 5 Läufen; belegt sind eine Abbau- und eine Anzeige-Lücke. #97 Punkt 8 ist damit nicht bestätigt — die Vorbedingung von #98 Stufe 2 steht ohne Beleg.

---

## Delegations-Policy je Fragetyp (Vorschlag)

Policies: **nie automatisch** (Mensch entscheidet) · **automatisch mit Veto** (begründeter Default wird angezeigt, Enter/„weiter" übernimmt, Freitext korrigiert) · **automatisch ab Schwellwert** (Default wird still angewandt, sobald ein Wert oder Zustand über der Schwelle liegt; Anzeige nur im Report). Die Festlegung trifft der Mensch bei der Abnahme.

| Fragetyp | gestellt | abweichend | Revisionskosten (billig/teuer, Grund) | Policy-Vorschlag |
|----------|----------|------------|----------------------------------------|------------------|
| Slug-Vorschlag (discover Schritt 5 / fast Schritt 3) | 33 (Obergrenze) | 3 belegt (9 %), alle regelhaft „Skill-Name" | **billig** — `git mv` + INBOX/BACKLOG-Zeile, belegt 2026-07-21:9-10 und 2026-08-06:149-151 | **automatisch mit Veto**; Default-Regel ergänzen: „Feature liefert einen Kit-Skill → Slug = englischer Skill-Name" (deckt alle 3 Abweichungen) |
| Backlog-Frage `dtb:task` | 8 real (+1 Wegwerf, +1 Test) | 0 real / 1 Test-Nein | **billig** — eine Tabellenzeile; Fehlen wird von `backlog-status` gemeldet; Status-Spalte ist abgeleitete Anzeige | **automatisch ab Schwellwert**: Default Ja ohne Frage; Ausnahme nur für Wegwerf-/Testartefakte (Schwelle = Ordnername `zz-test-*`/`abnahmeprobe-*` oder explizites Flag) |
| Backlog-Frage `feature-plan` Schritt 10 / `feature-fast` Schritt 7 | 33 (Obergrenze) | 0 belegt | **billig** (dito) | **automatisch ab Schwellwert** (wie oben); die Antwort „Nein" hat seit 2026-08-05 keinen dokumentierten Anwendungsfall |
| Pane-/Worktree-Stand nachfragen | 5 Läufe | 0 Nachfragen belegt | n/a (lesend) | **nicht bauen, solange kein Fall belegt ist**; falls doch: automatisch ab Schwellwert (Takt, read-only, Abbruch bei Hand-off) — belegter Bedarf liegt beim Abbau (Panes/Worktrees) und bei der Anzeige (#95 (4)), nicht beim Fortschritt |
| Kleinfall-Weiche „Fast-Track nehmen?" | 6 Läufe (Obergrenze) | 0 belegt, 6 n. e. | **mittel** — Lane-Wahl bestimmt Interviewtiefe; Umkehr über Eskalationspfad möglich, Artefakte bleiben | **nie automatisch** (Vorschlag + Bestätigung bleibt) — Datenlage leer, Festlegung ist Scope-nah |
| Escape-Hatch „trotzdem fortfahren" | 3 Auslösungen | 0 genutzt | **teuer** — Arbeit auf fehlender Basis (Plan ohne Spec, Review ohne Plan) | **nie automatisch**; das Gate hat seinen Zweck erfüllt (0 Umgehungen) |
| plan-review „Anpassungen vornehmen? (Ja/Nein)" | 26 | 0 Nein | Ja/Nein selbst **billig** (kein Schreibvorgang); die Einzel-Findings sind Scope-Festlegungen | **automatisch ab Schwellwert**: bei Verdikt REVISE/REJECTED direkt in die Finding-Runde (Frage entfällt); die Finding-Entscheidungen selbst **nie automatisch** (3 belegte Abweichungen mit Substanz) |
| implement Manual-Gate „passt / Korrekturen" | 57 Manual-Blöcke / 110 Phasen | 0 Ablehnung, 1 Korrektur, 1 Form-Befund | **teuer** — Gate löst den Phasen-Commit aus und ersetzt das Abnahme-Urteil; L64: bestandenes Gate ≠ nützliches Ergebnis | **nie automatisch**; Bündelung „ein Gate am Ende aller Phasen" (#98 (f)) als ehrliche Zwischenstufe prüfen; Form: blockierende Auswahl statt Freitext (Lehre 2026-07-30) |
| implement Staging bei dirty paths (1/2/3) | 1 belegt | 0 | **billig** — Staging-Set, vor Commit umkehrbar | **automatisch mit Veto** (Default 1 ist bereits Skill-Default; belegt „passt ohne Nummer → 1") |
| implement Commit-Message-Vorschlag | n. e. | 0 belegt | **billig vor dem Commit**, mittel danach (`--amend` verboten → neuer Commit) | **automatisch mit Veto** (Vorschlag anzeigen, „weiter" übernimmt) |
| implement Nächste-Phase (1/2/3) | 4 belegt | 1 (Option 2), 1 gemischt | **billig** — reine Ablaufwahl, Wiedereinstieg jederzeit möglich | **automatisch ab Schwellwert**: Default (1) weiter; Schwelle = Kontext-/Session-Budget oder Nutzer-Stopp → (2) mit Wiedereinstiegs-Kommando |
| implement Mismatch-Dialog (1/2/3) | 3 belegt | 3 Umplanungen | **teuer** — Abweichung vom reviewten Plan | **nie automatisch** |
| impl-review Triage je Finding | 158 Findings / 16 Triagen | 10 (6 %) Skip/Lesson | Fix = Code-Änderung (**mittel**, per Commit rückholbar); blocking-Findings entscheiden über Freigabe (**teuer**) | **automatisch mit Veto** für non-blocking/nits: Fix-Default in EINER Sammelvorlage, Skip per Zeile; **nie automatisch** für blocking-Findings |
| Codebase-Scan-Bestätigung (impl-plan 2b / discover Schritt 2) | 2 belegt | 0 | **billig** — Ist-Analyse-Tabelle im Plan, jederzeit ergänzbar | **automatisch mit Veto** (Liste anzeigen, weiter) |
| feature-start „Bereit? Los" | n. e. | 0 belegt | **keine Festlegung** — reiner Übergang | **automatisch ab Schwellwert** (streichen; wenn `plan.md` vorliegt, direkt `implement` anbieten/anschliessen) |
| Lektion-Kandidat „nach lessons.md übernehmen?" | 4 belegt | 4 („später") | **billig** — append-only Datei | **automatisch mit Veto**, aber mit **umgekehrtem Default**: Kandidat wird erfasst (nicht verworfen); seit 2026-09-08 übernimmt das der Checkpoint (Sammelvorlage) |
| Überschreib-Fragen (spec/plan/review.md PENDING) | 1 Selbsttest | 0 | **teuer** — Datenverlust (Triage-Stand, Spec-Inhalt) | **nie automatisch** |
| feature-fast Sammelvorlage „Ok / Korrekturen / Voll-Schiene / Abbruch" | 5 | 0 Vetos belegt | **mittel bis teuer** — fixiert Scope-Annahmen für drei Artefakte | **ist bereits „automatisch mit Veto"** — beibehalten; die max. 3 Kernfragen bleiben **nie automatisch** (2 von 5 Läufen brauchten eine: Name, Trägerschaft) |

**Gesamtbild:** 7 Fragetypen sind nach Kriterium delegierbar (Slug, 2× Backlog, Staging, Commit-Message, Codebase-Scan, „Los"), 3 weitere mit Schwellwert (Anpassungs-Ja/Nein, Nächste Phase, Lektion-Default umkehren), 6 bleiben beim Menschen (Escape, Manual-Gate, Mismatch, Überschreiben, Kleinfall-Weiche, Kernfragen), 1 wird als Bedarf nicht bestätigt (Pane-Stand).

---

## Festlegung 2026-09-22 (verbindlich)

Der Mensch hat die Vorschläge oben in dieser Sitzung abgenommen. Das Abgrenzungskriterium gilt
unverändert wie formuliert (Rücknahmekosten der Folge, nicht Häufigkeit der Abweichung). Die
Policy je Fragetyp ist damit festgelegt — die Tabelle oben ist die Begründung, diese hier die
Entscheidung. Vier Zeilen wurden einzeln entschieden und sind unten mit **E** markiert.

| # | Fragetyp | Festlegung | Anmerkung |
|---|----------|-----------|-----------|
| 1 | Slug-Vorschlag | automatisch mit Veto | Default-Regel ergänzen: Kit-Skill → Slug = englischer Skill-Name |
| 2 | Backlog-Frage `dtb:task` | automatisch ab Schwellwert | **E** Default Ja; Ausnahme nur bei Ordner-Präfix `zz-test-*`/`abnahmeprobe-*` |
| 3 | Backlog-Frage `feature-plan`/`feature-fast` | automatisch ab Schwellwert | **E** dieselbe Präfix-Ausnahme |
| 4 | Pane-/Worktree-Stand | wird nicht gebaut | **E** 0 Nachfragen in 5 Läufen → INBOX #97 Punkt 8 verliert seine Vorbedingung; Entscheidung über #97 in `/dtb:idea-review` |
| 5 | Kleinfall-Weiche „Fast-Track nehmen?" | nie automatisch | Datenlage leer, Festlegung ist Scope-nah |
| 6 | Escape-Hatch „trotzdem fortfahren" | nie automatisch | 0 Umgehungen — Gate erfüllt seinen Zweck |
| 7 | plan-review „Anpassungen? (Ja/Nein)" | automatisch ab Schwellwert | bei REVISE/REJECTED direkt in die Finding-Runde; Findings selbst nie automatisch |
| 8 | implement Manual-Gate | nie automatisch, je Phase | **E** keine Bündelung (#98 (f) verworfen); teuerste Rücknahme der Tabelle, L64 |
| 9 | implement Staging bei dirty paths | automatisch mit Veto | Default 1 |
| 10 | implement Commit-Message | automatisch mit Veto | Vorschlag anzeigen, „weiter" übernimmt |
| 11 | implement Nächste-Phase | automatisch ab Schwellwert | Default (1); Schwelle = Kontext-/Session-Budget oder Nutzer-Stopp → (2) |
| 12 | implement Mismatch-Dialog | nie automatisch | Abweichung vom reviewten Plan |
| 13 | impl-review Triage | automatisch mit Veto (non-blocking) / nie automatisch (blocking) | Fix-Default in EINER Sammelvorlage, Skip per Zeile |
| 14 | Codebase-Scan-Bestätigung | automatisch mit Veto | Liste anzeigen, weiter |
| 15 | feature-start „Bereit? Los" | entfällt | **E** bei vorliegender `plan.md` direkt `/dtb:implement` anschliessen |
| 16 | Lektion-Kandidat | automatisch mit Veto, Default umgekehrt | Kandidat wird erfasst statt verworfen (seit 2026-09-08 im Checkpoint) |
| 17 | feature-fast Sammelvorlage | unverändert (automatisch mit Veto) | max. 3 Kernfragen bleiben nie automatisch |

**Bilanz: 6 delegierbar mit Veto · 4 ab Schwellwert · 5 beim Menschen · 1 entfällt · 1 wird nicht gebaut.**

**Form-Auflage für alle automatischen Zeilen:** Ein Veto-Default muss sichtbar sein und ein
eindeutiges „weiter" haben; stiller Default ohne Anzeige ist bei Slug und Backlog vertretbar,
bei allem, was einen Commit auslöst, nicht (Lehre 2026-07-30).

**Was diese Festlegung freigibt:** Station 2 (`/dtb:feature-fast` für #57) kann starten — das
Kriterium und die 17 Zeilen sind die Vorgabe. Diese Notiz ändert keine Skills; die Umsetzung
je Zeile ist Gegenstand von #57 bzw. #98.

---

## Eval-Set für #99

Zweck: ein maschinelles Urteil (typisiert + Konfidenz) muss je Fall die tatsächlich gegebene Antwort reproduzieren. „Soll" = die belegte Antwort; ein Kalibrierungs-Anspruch ist nur so gut wie seine Trefferquote auf dieser Tabelle. Die Fälle mit `abweichend = ja` sind die harten Fälle.

| Fragetyp | Fall (Datum / Feature) | Frage | tatsächliche Antwort |
|----------|------------------------|-------|----------------------|
| Slug | 2026-07-20/21 meeting-dump (#24) | Slug `meeting-nachbereitung` übernehmen? | **Nein → `meeting-dump`** (Slug = Skill-Name) |
| Slug | 2026-08-02 meeting-agenda (#25) | Slug `fach-agenda` übernehmen? | **Nein → `meeting-agenda`** (englischer Skill-Name) |
| Slug | 2026-08-03 abnahme-zustand (#38) | Slug `abnahme-zustand` übernehmen? | Ja |
| Slug | 2026-08-06 no-loss-check (#29) | Slug `no-loss-gate` beibehalten? | **Nein → `no-loss-check`** („Gate" verspricht Blockade) |
| Slug | 2026-09-17 idea-rank (#33) | Slug `idea-rank` übernehmen? | Ja (Name vorab entschieden, Kollision mit `idea-triage` ausgeschlossen) |
| Slug | 28 weitere archivierte Ordner 2026-07-08 … 2026-09-09 | Slug übernehmen? | Ja (Indiz: Ordner = Kurzform des Discovery-Titels; Einzelantwort nicht protokolliert) |
| Backlog `task` | 2026-08-05 gitattributes-eol | In BACKLOG eintragen? | Ja |
| Backlog `task` | 2026-08-09 pipeline-kanten-reziprok | In BACKLOG eintragen? | Ja |
| Backlog `task` | 2026-08-16 pipeline-kante-worker-checkpoint | In BACKLOG eintragen? | Ja |
| Backlog `task` | 2026-08-16 lesestand-ls-portabel, archive-4d-realitaet | In BACKLOG eintragen? | Ja (indirekt belegt) |
| Backlog `task` | 2026-09-07 `hana-backup-taeglich` (Blind-Testlauf) | In BACKLOG eintragen? | **Nein** (Testartefakt) |
| Backlog `task` | 2026-09-09 idea-review-sofortschreiben | In BACKLOG eintragen? | Ja |
| Backlog `task` | 2026-09-09 inbox-becken-migration | In BACKLOG eintragen? | Ja |
| Backlog `task` | 2026-09-16 `abnahmeprobe-start` (Wegwerf) | In BACKLOG eintragen? | Ja (Zeile danach gelöscht) |
| Backlog `task` | 2026-09-21 rueckfragen-erhebung | In BACKLOG eintragen? | Ja |
| Backlog `feature-plan/fast` | 2026-07-13 greenfield-autoren-skills · 2026-08-02 meeting-agenda · 2026-08-08 autonome-schiene · 2026-08-19 pane-start · 2026-08-20 capture-duplikat-schutz · 2026-09-08 checkpoint-verlustfunde · 2026-09-17 idea-rank | Feature in BACKLOG eintragen? | Ja (7× einzeln belegt) |
| Backlog `feature-plan/fast` | Gegenproben 2026-07-29, 2026-08-04, 2026-09-09 | (alle Ordner im BACKLOG?) | Ja — keine Lücke gemeldet |
| Pane-Stand | 2026-08-16 w3:p2 · 2026-08-16 w3:p7/p8 · 2026-08-19 w3:p5 · 2026-08-19/20 w3:p6 · 2026-09-17 w3:p9 | Wurde nach dem Stand gefragt? | Nein (0 Nachfragen belegt; Rückweg jeweils automatischer Hand-off) |
| Escape-Hatch | 2026-07-13 impl-plan pdf-export (Test) | trotzdem fortfahren? | Nein (Redirect befolgt) |
| Escape-Hatch | 2026-08-03 feature-fast Eingangs-Gate (#38) | ohne INBOX-Eintrag fortfahren? | Nein (Idee zuerst erfasst) |
| plan-review Ja/Nein | 26 Läufe 2026-07-08 … 2026-09-17 (Tabelle 4d) | Anpassungen vornehmen? | Ja (26/26) |
| plan-review Finding | 2026-07-09 #3 Pragmatiker-Einwand Resume-Marker | Finding übernehmen? | **Nein** (im Scope behalten) |
| plan-review Finding | 2026-07-21 meeting-dump Datenschutz-FAIL | Finding übernehmen (gitignore)? | **Anders** (getrackt + Sensibilitäts-Hinweis) |
| plan-review Finding | 2026-09-08 checkpoint-verlustfunde 1.3 (b) / 3.1 | Plan ändern? | **Anders** (Spec-Nachtrag statt Plan-Änderung) |
| Manual-Gate | 2026-08-16 herdr-worker-automation P4 · 2026-09-08 checkpoint-verlustfunde P2, P3 · 2026-09-17 idea-rank P1, P2, Abnahme P3 | passt? | passt (6×) |
| Manual-Gate/Abnahme | 2026-09-16 feature-start-statusfeld Rückweg-Kriterium | passt? | **Korrekturen** (Platzhalter-SHAs, Commit-Zahl) — nach Korrektur bestanden |
| Bestätigungsform | 2026-07-30 commit-and-push 4.3 | Freitext „passt"? | **keine Antwort** — übersehen, Lauf versandet |
| Staging | 2026-09-08 checkpoint-verlustfunde P1 | Set (1/2/3)? | (1) Default („passt ohne Nummer") |
| Nächste Phase | 2026-07-21 meeting-dump · 2026-08-20 capture-duplikat-schutz | weiter (1/2/3)? | (1) |
| Nächste Phase | 2026-09-08 checkpoint-verlustfunde nach P2 | weiter (1/2/3)? | **(2)** Wiedereinstieg in neuer Session |
| Mismatch | 2026-08-16 herdr-worker-automation (2×) · 2026-09-17 idea-rank | (1/2/3)? | (1) mit Umplanung (3×) |
| impl-review Triage | 148 Findings in 16 Triagen (Tabelle 4j) | Fix wie vorgeschlagen? | Ja (Fixed) |
| impl-review Triage | 2026-07-16 F2 · 2026-07-18 F5, F6 · 2026-07-18 F7 · 2026-07-30 (2) · 2026-08-08 F8 · 2026-08-19 (1) · 2026-09-08 F10 | Fix wie vorgeschlagen? | **Skip** (9×, je begründet) |
| impl-review Triage | 2026-08-19 pane-start (1 Finding) | Fix wie vorgeschlagen? | **Lektion** |
| Codebase-Scan | 2026-07-20 meeting-dump (7 Module) | Liste bestätigen? | Ja |
| Lektion-Kandidat | 2026-07-09 · 2026-07-14 (3×) · 2026-08-07 · 2026-08-16 | sofort nach lessons.md? | **Nein — später** (als offener Punkt weitergetragen) |
| Sammelvorlage fast | 2026-08-02 meeting-agenda · 2026-08-03 abnahme-zustand · 2026-08-07 feature-start-statusfeld · 2026-08-19 pane-start · 2026-09-17 idea-rank | Ok zum Schreiben? | Ok (5/5; 2× vorher 1 Kernfrage) |
| Sammelvorlage fast | 2026-08-02 #35 (E2E-Lauf 3) | Ok zum Schreiben? | — (Skill eskalierte selbst auf Voll-Schiene) |

**Messvorschrift für #99:** Trefferquote getrennt nach (a) Übernahme-Fällen und (b) Abweichungs-Fällen ausweisen; eine Kalibrierung, die (a) zu 100 % trifft und (b) zu 0 %, ist wertlos, weil (b) die Fälle sind, für die man den Menschen braucht. Erwartung nach Datenlage: Slug-Abweichungen sind regelhaft (Skill-Name) und damit lernbar; Finding-Abweichungen im plan-review sind es nicht (Einwand aus Fachwissen).

---

## Grenzen der Erhebung

1. **Ergebnis- statt Verlaufsprotokoll.** Die Session-Logs halten fest, was geschrieben wurde, nicht welche Frage wie beantwortet wurde. Eine übernommene Rückfrage hinterlässt meist keine Zeile; eine abgelehnte nur dann, wenn sie eine Änderung auslöste. Die Zahl „0 abweichend belegt" ist deshalb eine Untergrenze der Abweichungen, nicht ihr Wert — sie ist überall als solche ausgewiesen („nicht ermittelbar" getrennt von „0 belegt").
2. **Obergrenzen statt Zählungen.** „Gestellt" ist je Fragetyp aus Artefakten abgeleitet (33 `discovery.md`, 8 `task.md`, 110 Phasen / 57 Manual-Blöcke, 26 belegte plan-review-Läufe, 16 belegte Triagen, 5 Pane-Läufe). Die Skills änderten sich im Zeitraum (Eligibility-Gates ab 2026-07-10, Manual-Gate ab 2026-07-15, Fast-Track und Kleinfall-Weiche ab 2026-08-02, Duplikat-Check ab 2026-08-20) — frühe Läufe haben manche Frage nie gesehen.
3. **Zuordnungs-Unschärfen.** Die Lektion-Kandidat-Frage (4m) stellen `impl-plan` und `no-loss-check` gleichlautend; die Backlog-Frage stellen `task`, `bug-report`, `feature-plan`, `feature-fast`. Die Zuordnung folgt dem Kontext der Log-Zeile.
4. **Testartefakte getrennt gezählt.** Blind-Wirkläufe (2026-09-07) und Wegwerf-Items (2026-09-16) sind ausgewiesen, aber nicht mit den realen Läufen verrechnet — das einzige belegte Backlog-Nein stammt aus einem Testlauf.
5. **Pane-Nachfragen sind im Log strukturell unsichtbar.** Eine Chat-Nachfrage „wie weit ist die Pane?" ohne Artefaktfolge würde in einem Ergebnis-Log nicht erscheinen. „0 belegt" heisst hier: kein Log-Autor hielt eine solche Nachfrage für erwähnenswert — in fünf Läufen, deren Rückweg jeweils automatisch ankam.
6. **Abdeckung.** 53 Tagesdateien 2026-03-12 bis 2026-09-18; der 2026-09-21 (heute) hat noch kein Log — der Task `rueckfragen-erhebung` ist nur über `BACKLOG.md:22` belegt. Änderungen in Logs vor dem Change-Folder-Modell (bis 2026-07-09) nennen Features in Grossschreibung (`CHANGE_FOLDER_MODELL`); sie wurden über INBOX-Nummern zugeordnet.
7. **Grep-Basis.** Kandidaten wurden mit Stichwörtern gefunden (`slug`, `umbenannt`, `Arbeitsname`, `BACKLOG`, `Backlog-Frage`, `Pane`, `Worktree`, `Stand`, `Manual`, `passt`, `REVISE`, `Skipped`, `Escape`, `Fast-Track`, `Sammelvorlage`, `Einwand`, `revidiert`, `Nutzer-Entscheid`, `Nutzerwunsch`) und dann im Kontext gelesen. Eine Abweichung, die im Log ohne eines dieser Wörter beschrieben ist, kann fehlen.
8. **Kein Wertungsanspruch.** Kriterium und Policy sind Vorschläge aus den Zahlen; die Festlegung trifft der Mensch bei der Abnahme. Nichts hier ändert Skills, INBOX-Status oder zentrale Dateien.
