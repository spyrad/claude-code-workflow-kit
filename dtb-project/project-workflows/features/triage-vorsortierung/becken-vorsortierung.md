# Becken-Vorsortierung (Probelauf 2026-10-16)

> Vorschlag von 3 lesenden Agenten, nichts entschieden. Entscheidung per `/dtb:idea-triage`.
> Spalte **Deine Entscheidung**: leer = Vorschlag angenommen; nur Abweichungen eintragen (Messsatz für INBOX #99).

## Bilanz

| Vorschlag | Anzahl |
|-----------|--------|
| Befördern | 51 |
| Verwerfen (erledigt / überholt / Dublette / falsches Repo) | 16 |
| Unklar (Frage an dich) | 6 |
| **Summe** | **73** |

## Bündel (gemeinsam zuschneiden)

1. **Handoff-Regel im Checkpoint:** #86, #90, #118, #121, #132 (+ #35)
2. **`dtb:archive`:** #87, #94, #129, #130
3. **`task.md`-Schiene:** #90, #92, #124
4. **`pane-start`-Kleinkram:** #89, #115, #124, #126
5. **Worktree-Hand-off-Empfang:** #123, #128, #131
6. **Überwachungs-Tick:** #104, #116, #127
7. **`kit-sync`:** #31, #51, #55, #82, #108, #109
8. **`feature-discover`:** #18, #32, #47
9. **Zustand ohne Pfleger:** #52, #53
10. **Nachträge statt eigener Ideen:** #103, #106 → INBOX #99 · #46, #58 → INBOX #100

## Prozesslücken (vom Probelauf aufgedeckt)

- **Lektionen im Becken:** #77, #79, #80 sind Lektionen. `dtb:idea-triage` kennt keinen Ausgang nach `lessons.md`.
- **`lessons.md` lückenhaft:** L22–L34 fehlen in der versionierten Datei (per Grep bestätigt).

## teil1

| # | Vorschlag | Grund (1 Satz, Deutsch) | Beleg | Sicherheit | Deine Entscheidung |
|---|-----------|-------------------------|-------|------------|---|
| 136 | Verwerfen: falsches Repo | Der Befund betrifft das Logging der Sprachausgabe, und die liegt seit 2026-09-11 in einem eigenen Repo (Ziel: github.com/spyrad/claude-code-tts); im Kit gibt es weder `speak.log` noch edge-tts. | INBOX-BEFUNDE.md:55 (#91, `bcdbf2e` im TTS-Repo); `grep -rl "speak.log\|edge-tts" skills agents output-styles` ohne Treffer | hoch |  |
| 132 | Befördern | Die Handoff-Regel kennt nur Geplant / In Arbeit / Fertig zum Testen (+REJECTED); für `Abgenommen` fehlt der Zweig `/dtb:archive`, ebenso der Merge-Hinweis im Pane-Fall. | skills/dtb-workflow-checkpoint/SKILL.md:246-252 | hoch |  |
| 131 | Befördern (#114 hier einfalten) | Empfangsschritt 4 zieht triviale globale Updates wie den INBOX-Link „direkt in diesem Lauf“ nach, auch vor dem Merge; §8.1 wertet einen Worktree nicht als Beleg, die Sichten zeigen dann „Change fehlt“. | skills/dtb-workflow-checkpoint/SKILL.md:392-394; DERIVED_STATE_RULES.md:438-458 | hoch |  |
| 130 | Befördern (mit #94 zusammen) | 4e entfernt nur Zeilen und setzt keine Vorlagen-Zeile „Kein aktives Feature.“, wenn die Tabelle leer wird. | skills/dtb-archive/SKILL.md:196-204 vs. skills/dtb-workflow-checkpoint/SKILL.md:201 | hoch |  |
| 129 | Befördern | Die Übersicht führt mitzuarchivierende INBOX-Zeilen als eigenen Block neben den Change-Ordnern, und die Abschlussfrage nennt weder Art noch Anzahl. | skills/dtb-archive/SKILL.md:110-125 | hoch |  |
| 128 | Befördern | Beide Skills behaupten weiter, der Block erreiche die Session „von selbst als Eingabe“; dass der Mensch den Checkpoint selbst auslösen muss, steht nirgends. | skills/dtb-pane-start/SKILL.md:271-272, :333-336; skills/dtb-worker/SKILL.md:352-353, :367, :418 | mittel |  |
| 127 | Befördern | `dtb:workflow-resume` erwähnt weder Tick noch `/loop`, also gibt es nach einem Neustart kein erneutes Angebot. | `grep -n "tick\|/loop" skills/dtb-workflow-resume/SKILL.md` ohne Treffer | hoch |  |
| 126 | Befördern | Weder Vorbedingungen noch Begrüßungstext von pane-start (und worker) erwähnen fehlende Abhängigkeiten wie `node_modules` im frischen Worktree. | `grep "node_modules\|npm install\|package.json"` in skills/dtb-pane-start + dtb-worker ohne Treffer | hoch |  |
| 125 | Befördern | Der Skill kennt nur kein Argument, `YYYY-MM-DD` und `woche`; bei anderen Argumenten fragt er nach. Das ist ein Fach-Wunsch, gehört also in die INBOX. | skills/dtb-session-summary/SKILL.md:23, :56-62 | hoch |  |
| 124 | Befördern | Die Startbefehl-Tabelle in 1b hat keine Zeile für `task.md` (und auch keine für `bug.md`). | skills/dtb-pane-start/SKILL.md:149-158 | hoch |  |
| 123 | Befördern | Die Sende-Seite baut den Hand-off-Block weiterhin „aus dem Sitzungskontext“; nur die Prüfseite im Worker nutzt `git diff --stat`. | skills/dtb-workflow-checkpoint/SKILL.md:55; skills/dtb-worker/SKILL.md:441 | hoch |  |
| 122 | Befördern | Check 4 erlaubt nur fünf Dateinamen; es fehlen `review.md` und die Belegdateien, dazu auch `worker-report.md` und `fast-draft.md`, die laut Kit-CLAUDE.md legitim sind. | skills/dtb-project-health/SKILL.md:172-173 | hoch |  |
| 121 | Befördern (mit #118/#132/#86 zuschneiden) | Die Handoff-Regel leitet „In Arbeit“ blind auf `/dtb:implement` ab; eine Sperrmarke für Schritte gibt es im Kit gar nicht, sie ist PKP-Praxis. Vor der Regel muss also eine Konvention entstehen. | skills/dtb-workflow-checkpoint/SKILL.md:246-247; kein `⛔`/„gesperrt“ in DERIVED_STATE_RULES.md | mittel |  |
| 120 | Befördern | Beide Matrizen haben für RETHINK weiter nur eine Zeile ohne Begründung. | skills/dtb-plan-review/SKILL.md:217-222; DERIVED_STATE_RULES.md:355-360 | hoch |  |
| 119 | Befördern | idea-triage beschreibt nur die Selbstanlage des Beckens; eine Regel für den Erst-Umzug mit Statusfilter fehlt kitweit. Der Mensch muss klären, ob noch Bestandsprojekte zu migrieren sind. | skills/dtb-idea-triage/SKILL.md:79-114; kein Migrations-Treffer in skills/ | mittel |  |
| 118 | Befördern (mit #121/#132/#86 zuschneiden) | Der Widerspruch besteht weiter: Die Handoff-Regel schickt bei Y/Y + REJECTED zu `/dtb:implement`, implement bricht bei voll abgehaktem Progress ab, und impl-review bildet den Scope nur aus Progress-SHAs. | skills/dtb-workflow-checkpoint/SKILL.md:248-249; skills/dtb-implement/SKILL.md:85; skills/dtb-impl-review/SKILL.md:75-97, :329 | hoch |  |
| 117 | Befördern | „Bereit? Sage Los“ steht noch im Skill; Station 2 hat es bewusst aus dem Scope genommen und als offenen Punkt vermerkt, der Teil „in Station 2 mitziehen“ ist also überholt. Zu entscheiden bleibt nur noch streichen oder lassen. | skills/dtb-workflow-resume/SKILL.md:229; archive/rueckfragen-defaults/plan.md:41, :322 | hoch |  |
| 116 | Befördern | Der Tick meldet `done` ausdrücklich „als Änderung“, eine Ausnahme für den reinen Wechsel `done`↔`idle` gibt es nicht. | skills/dtb-worker/SKILL.md:356-362, :371 | hoch |  |
| 115 | Befördern | 1a kennt nur „rein numerisch“, `#57` landet im Slug-Zweig; ein Abstreifen des `#` gibt es weder hier noch in feature-discover oder task. | skills/dtb-pane-start/SKILL.md:123-133 | hoch |  |
| 114 | Verwerfen: Dublette #131 | Gleicher Gegenstand (globale Nachträge vor dem Merge → „Change fehlt“); #131 ist der spätere, konkretere Befund mit beiden Zuschnitt-Optionen. | INBOX-BEFUNDE.md:26 vs. :43; skills/dtb-workflow-checkpoint/SKILL.md:392-394 | hoch |  |
| 109 | Befördern | Der Skill nennt drei Modi, legt aber keinen Default für den Aufruf ohne Argument fest. | skills/dtb-kit-sync/SKILL.md:9, :21-23 (kein Treffer „ohne Argument“/„kein Argument“) | hoch |  |
| 108 | Befördern | Der Skill-Ordner enthält nur `SKILL.md`, ein mitgeliefertes Skript gibt es nicht; nur `kithash` ist festgelegt, die Vergleichsschleife (Schritte 3-5) bleibt Prosa und wird improvisiert. | skills/dtb-kit-sync/ (nur SKILL.md); SKILL.md:89, :130-148 | hoch |  |
| 106 | Befördern (als Korrektur-Nachtrag in INBOX #99, keine eigene Idee) | #99 Punkt (2) nennt die Station-1-Erhebung weiterhin als Eval-Set, die Korrektur steht nur im Session-Log; der Teil zu #57 ist überholt, weil #57 umgesetzt und archiviert ist. | INBOX.md:18 („das Eval-Set dafür ist genau die Erhebung aus Station 1“); project-changelog/2026-09/2026-09-28.md:19 | mittel |  |
| 104 | Befördern | Bei `idle` liest der Tick die Pane nie, `herdr pane read` läuft nur bei `blocked`; unabgeschickte Eingaben bleiben also unsichtbar. | skills/dtb-worker/SKILL.md:337, :369 | hoch |  |
| 103 | Unklar | Das ist ein Architektur-Vorschlag (Jev-Schattenbetrieb) zu #99, kein Mangel. Der Mensch muss entscheiden, ob Schattenbetrieb der gewählte Weg für #99 ist und ob er als Nachtrag in #99 oder als eigene Idee geführt wird. | INBOX.md:18 (#99 ohne „Schatten“); project-changelog/2026-09/2026-09-28.md:19 | mittel |  |

**Auffälligkeiten Teil 1**
- #118, #121 und #132 sind drei fehlende Zweige derselben Handoff-Regel (checkpoint SKILL.md:244-252), zusammen mit #86. Ein Change.
- #131 und #114 sind ein Gegenstand; #128 berührt dieselbe Empfangsseite des Worktree-Hand-offs.
- #129, #130 und #94 betreffen alle `dtb:archive` (Schritt 3 und 4e). Ein Change.
- `task.md`-Familie: #124 gehört zu #90 und #92 (Task-Schiene fehlt in implement, resume, pane-start).
- #106 und #103 sind Ergänzungen zu INBOX #99. #104 und #116 betreffen beide die Meldungsregel des Ticks.

## teil2

| # | Vorschlag | Grund (1 Satz, Deutsch) | Beleg | Sicherheit | Deine Entscheidung |
|---|-----------|-------------------------|-------|------------|---|
| 102 | Verwerfen: erledigt | Der Beleg wurde in #97 verbraucht: Feature `ueberwachungs-tick` ist abgenommen und zitiert #102 als Grund für den 15-min-Takt. | `archive/ueberwachungs-tick/spec.md:17`, `archive/ueberwachungs-tick/plan.md:181`, `skills/dtb-worker/SKILL.md:390`, `ARCHIVE_LOG.md:100-101` | hoch |  |
| 101 | Befördern | `.env` fehlt weiter in der Kit-`.gitignore` (`git check-ignore .env` gibt nichts zurück); `project-init` legt gar keine `.gitignore` an, nur eine Lese-Sperre für `.env` in `settings.json`. | `.gitignore` (gesamte Datei, kein `.env`), `settings.json:16-17`, `skills/dtb-project-init/SKILL.md:375` | hoch |  |
| 96 | Verwerfen: überholt | Die Bezugsidee #57 ist abgeschlossen: Die Erhebung fand 0 von 8 echten Nein, und die Frage wurde zur stillen Anzeige mit Testordner-Ausnahme. | `archive/rueckfragen-erhebung/erhebung.md:65`, `skills/CLAUDE.md:326`, `ARCHIVE_LOG.md:104-106` | hoch |  |
| 94 | Befördern | Teilweise behoben: `## Offene Aufgaben` bleibt jetzt bewusst für den Checkpoint stehen, der `## Handoff`-Block wird in 4e aber weiter nicht genannt (nur pauschal „sonstige Referenzen“, das gab es schon beim Befund). | `skills/dtb-archive/SKILL.md:199-204` (blame: 199-201 `350f017` vor dem Befund, 202-204 `e97b002`) | mittel |  |
| 93 | Befördern | In der Zusammenfassung von Schritt 4 fehlt weiter eine Zeile für übersprungene Ideen. | `skills/dtb-idea-review/SKILL.md:112`, `:193-207` | hoch |  |
| 92 | Befördern | Schritt 4 von workflow-resume prüft für „In Arbeit“ weiter nur `plan.md` `## Progress`; `task.md` erscheint nur im Worktree-Block. | `skills/dtb-workflow-resume/SKILL.md:128-129`, `:159-160` (vgl. `:104`) | hoch |  |
| 91 | Verwerfen: erledigt | Die Entscheidung ist umgesetzt: #41 ist mit Verweis auf das eigene Repo archiviert, und die drei veralteten Installer-Dateien gibt es nicht mehr. | `ARCHIVE_LOG.md:94`; `ls` auf `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1` und `build-installer.ps1` meldet: nicht vorhanden | hoch |  |
| 90 | Befördern | `dtb:implement` erwähnt `task.md` nirgends, und die Handoff-Regel im Checkpoint hat keinen Zweig für Aufgaben. | `skills/dtb-implement/SKILL.md` (Grep „task“: 0 Treffer), `skills/dtb-workflow-checkpoint/SKILL.md:246-250` | hoch |  |
| 89 | Befördern | Beide Mängel bestehen noch: In `consumes` fehlt `DERIVED_STATE_RULES.md`, und dort steht „Zwei bewusste Abweichungen“ über einer dreizeiligen Tabelle. | `skills/dtb-pane-start/SKILL.md:18`, `:252-259` | hoch |  |
| 88 | Befördern | Die Stage-Tabelle kennt weiter 8 Stages, während die Frontmatter 10 nutzt (`capture`, `execution` je 2 Skills); `useMaxWidth` fehlt in `mermaid.initialize`. | `skills/dtb-pipeline-graph/SKILL.md:36`, `:83-92`, `:143-154`; Grep `^  stage:` über alle Skills | hoch |  |
| 87 | Befördern | Kandidat ist weiter jede `Ausgearbeitet`-Zeile, deren verlinkte Datei existiert; ob der verlinkte Change selbst archivierbar ist, wird nicht geprüft. | `skills/dtb-archive/SKILL.md:71-78`, `DERIVED_STATE_RULES.md` §8.1 (`:438-448`) | hoch |  |
| 86 | Befördern | Die Handoff-Regel kennt bei Y/Y mit `review.md` nur den Fall REJECTED → implement; ein vollständig triagiertes, nicht abgelehntes Review fällt auf den Fallback. | `skills/dtb-workflow-checkpoint/SKILL.md:246-252` | hoch |  |
| 85 | Verwerfen: überholt | Durch #91 entschieden: Die Sprachausgabe ist ein eigenes Repo und kein Kit-Baustein, #41 ist archiviert. | `ARCHIVE_LOG.md:94`; Befund #91 (Zeile 55) | hoch |  |
| 84 | Verwerfen: erledigt | Das Becken hat einen eigenen Ausgang (die Triage entfernt jede Zeile beim Befördern und Verwerfen), und gegen das Wachstum gibt es die Becken-Erinnerung im Checkpoint; nur ein ausdrücklicher Absichtssatz in archive fehlt. | `skills/dtb-idea-triage/SKILL.md:283`, `:307`, `skills/dtb-workflow-checkpoint/SKILL.md:254-257` | mittel |  |
| 83 | Befördern | Die INBOX kennt weiter vier Werte; „nebenbei umgesetzt“ wird nur als ungeregelte Notiz („Verworfen (umgesetzt …)“) geführt, das ist für Lese-Skills nicht unterscheidbar. | `skills/CLAUDE.md` Statustabelle (Zeile `INBOX.md entries`), `skills/dtb-project-health/SKILL.md:103`, `ARCHIVE_LOG.md:87-88` | mittel |  |
| 77 | Unklar | Das ist eine Lektion, keine Idee; in `lessons.md` steht keine passende, und die Triage hat keinen Ausgang zu den Lektionen. Frage an den Menschen: per `/dtb:lesson` übernehmen oder verwerfen? | Grep `lessons.md` (kein Treffer), `skills/dtb-idea-triage/SKILL.md` (kein Lektions-Ausgang) | mittel |  |
| 78 | Verwerfen: erledigt | Der Anlassfall ist behoben (die Bedingung steht jetzt wortgleich), und die allgemeine Regel steht als Mechanik-Regel „Spiegel mitziehen und per Grep auf den neuen Wortlaut verifizieren“. | `skills/dtb-no-loss-check/SKILL.md:328`, `skills/CLAUDE.md:575-580` | mittel |  |
| 79 | Unklar | Werkzeug-Lektion ohne Entsprechung in `lessons.md` (L38 behandelt nur Heredocs, nicht Python-String-Literale). Frage an den Menschen: als Lektion erfassen oder verwerfen? | `lessons.md` L38 (Zeile 34) | mittel |  |
| 80 | Unklar | Werkzeug-Lektion (Arbeitsverzeichnis bleibt über Bash-Aufrufe erhalten), nicht abgedeckt; die Mechanik-Regel „Bash-Bloecke sind eigene Shells“ behandelt nur Variablen. Frage an den Menschen: als Lektion erfassen oder verwerfen? | `skills/CLAUDE.md:546-556`, `lessons.md` (kein Treffer) | mittel |  |
| 81 | Verwerfen: erledigt | Die Migration ist als Aufgabe `inbox-becken-migration` erledigt und archiviert (27 Funde migriert). | `ARCHIVE_LOG.md:90` (`daf7e24`, `badc097`), `archive/inbox-becken-migration/task.md` | hoch |  |
| 82 | Befördern | `agents/CLAUDE.md` fällt weiter unter das Klasse-A-Muster und liegt tatsächlich installiert in `~/.claude/agents/CLAUDE.md` und im Lock. | `skills/dtb-kit-sync/SKILL.md:75`; `ls ~/.claude/agents/`; `~/.claude/dtb-lock.json` enthält `agents/CLAUDE.md` | hoch |  |
| 75 | Verwerfen: überholt | Der Checkpoint schreibt die Ideen aus „Kann warten“ seit dem Becken-Umbau selbst ins Becken, Folgeläufe filtern sie über Stufe 2; offen bleibt nur ein Restfall (eigenständige Läufe ohne Checkpoint, Nicht-Ideen-Funde). | `skills/dtb-workflow-checkpoint/SKILL.md:282`, `:292`, `skills/dtb-no-loss-check/SKILL.md:420-441` | mittel |  |
| 70 | Befördern | Teilweise behoben: Zeile #54 hat jetzt korrekt 5 freie Pipes, und Becken und Triage prüfen die Spaltenzahl; `idea`, `task` und `bug-report` nennen die Feld-Hygiene aber weiter nicht, und für `INBOX.md` fehlt der Spalten-Check. | Grep „Pipe/Feld-Hygiene“ in `skills/dtb-{idea,task,bug-report}/SKILL.md`: 0 Treffer; `skills/dtb-project-health/SKILL.md:102-108`; `skills/dtb-idea-triage/SKILL.md:281` | hoch |  |
| 69 | Unklar | Alle fünf Capture-Skills stehen weiter auf `true`, aber der Schmerz ist weitgehend über die Sammelvorlage im Checkpoint aufgefangen, und `dtb:idea` muss für die Zwei-Becken-Regel auf `true` bleiben. Frage an den Menschen: Reicht die Sammelvorlage, oder sollen `lesson` und `open-question` trotzdem für das Modell geöffnet werden? | `skills/dtb-{idea,lesson,task,bug-report,open-question}/SKILL.md` Frontmatter; `skills/CLAUDE.md` Zwei-Becken-Regel; `archive/checkpoint-verlustfunde/discovery.md:79` | mittel | Verwerfen: erledigt — 2026-10-16 umgesetzt (`lesson` + `open-question` modell-aufrufbar) |

**Auffälligkeiten Teil 2**
- Handoff-Regel im Checkpoint (`:246-252`): #86 und #90 hier, dazu #118, #121, #132. Zusammen zuschneiden.
- `dtb:archive`: #87 und #94 hier, dazu #129 und #130.
- `task.md` unsichtbar: #90 (implement), #92 (resume), #124 (pane-start 1b).
- `pane-start`-Kleinkram bündeln: #89 mit #115, #124, #126.
- #77, #79, #80 sind Lektionen im Becken; die Triage hat keinen Weg nach `lessons.md` — Prozesslücke, einmal grundsätzlich entscheiden.

## teil3

| # | Vorschlag | Grund (1 Satz, Deutsch) | Beleg | Sicherheit | Deine Entscheidung |
|---|-----------|-------------------------|-------|------------|---|
| 66 | Verwerfen: überholt | Die Kennzahl „Kit-Stand“ war eine freihändige Kontextzeile dieses Projekts, das Checkpoint-Template hat sie nie vorgegeben, und seit dem 2026-08-14 steht sie nicht mehr im Statusdokument. | `skills/dtb-workflow-checkpoint/SKILL.md:209-210`; `669519d`; entfernt in `08fa791` | hoch |  |
| 64 | Verwerfen: erledigt | `lessons.md` ist seit 2026-09-07 versioniert, damit reist der Bestand mit dem Repo. | `f75979d`; `.gitignore` Negation `!dtb-project/project-rules/lessons.md` | hoch |  |
| 63 | Befördern | Eine Konvention für feste Maschinen-Kennungen fehlt, relative Namen („Arbeitsrechner“, „Zweitrechner“) sind noch in Gebrauch. | `skills/CLAUDE.md` ohne Treffer; WORKFLOW_STATUS Offene Aufgaben; `lessons.md:77` (L81) | mittel |  |
| 62 | Befördern | Der Ort der Minimal-Notiz bei hartem Worker-Stopp ist nicht festgelegt. | `skills/dtb-worker/SKILL.md:556-558` | hoch |  |
| 61 | Befördern | Die Lektionen-Tabelle ist unsortiert (8 vor 7, 17→12), `dtb:lesson` sagt nur „nächste laufende Nummer“, nicht max+1; „ans Tabellenende“ steht schon drin. | `lessons.md`; `skills/dtb-lesson/SKILL.md:188`, `:191` | hoch |  |
| 60 | Unklar | Ob der Ausfall am Harness (Command-Loader) oder am Kit liegt, ist nie geklärt; bis 2026-08-16 vier Belege, danach keiner. Frage: Harness-Fehler als Workaround-Doku führen oder verwerfen? | `2026-08/2026-08-09.md:63`; `2026-08/2026-08-16.md:177` | mittel |  |
| 59 | Befördern | Die Spalte „Vorab-Frage“ wird nur bei `teilweise` gefüllt, bei `nein` steht nur eine Begründung. | `skills/dtb-worker/SKILL.md:81-84`, `:98`, `:108-109` | mittel |  |
| 58 | Verwerfen: Dublette #100 | Fall (2) ist erledigt; Fall (1) (`greenfield-prd.after: null` trotz `opportunity-map.next`) fällt unter #100 („Pipeline-Kanten ohne Gegenstück“). Fall (1) als Beleg an #100 hängen. | `acb405e`; `skills/dtb-greenfield-prd/SKILL.md:13`; `INBOX.md:17` | mittel |  |
| 56 | Befördern | Der Pfad des Session-Logs hängt am heutigen Datum, eine Regel für Sitzungen über Mitternacht fehlt. | `skills/dtb-workflow-checkpoint/SKILL.md:118` | hoch |  |
| 55 | Befördern | `kit-sync` hat keinen Klassen-Lesemodus, `skills/CLAUDE.md` trägt keinen Hinweis „kein verteiltes Artefakt“. | `skills/dtb-kit-sync/SKILL.md:9` | mittel |  |
| 54 | Befördern | Die Regel zu Negativ-Kriterien deckt nur den Ort ab, nicht den Inhalt; eine Positiv-Gegenprobe ist nirgends verankert. | `skills/CLAUDE.md:610-620`; `skills/dtb-impl-plan/SKILL.md` ohne Treffer | hoch |  |
| 53 | Befördern | Das Feld `**Status:**` in `bug.md` hat keinen Pfleger; `feature-start` verweist selbst auf #53 als offen. Die „falsche Zusage“ in `bug-report` ist korrigiert. | `skills/dtb-workflow-checkpoint/SKILL.md:14`, `:475`; `skills/dtb-bug-report/SKILL.md:159`, `:209-211`; `skills/dtb-feature-start/SKILL.md:87-90` | hoch |  |
| 52 | Befördern | Die Sektion „Laufende Arbeit“ wird von drei Skills gelesen, aber von keinem Template erzeugt. | `skills/dtb-workflow-resume/SKILL.md:130`, `:238`, `:277`; `skills/dtb-workflow-status/SKILL.md:88`; `skills/dtb-project-health/SKILL.md:312` | hoch |  |
| 51 | Befördern | Weder `impl-review` noch `commit-and-push` weisen auf den fälligen `kit-sync` bei Klasse-A-Dateien hin. | Grep in beiden Skills = 0 | hoch |  |
| 47 | Befördern | Der Codebase-Scan liegt vor der Scope-Klärung, und der Zwischenstand wird unter `<slug>` gespeichert, bevor der Slug feststeht. | `skills/dtb-feature-discover/SKILL.md:63`, `:97-104`, `:165` | hoch |  |
| 46 | Verwerfen: Dublette #100 | Zwei echte Kanten sind behoben; die vier Rest-Kanten und die Konventionsfrage fallen unter #100. Fragen (a)/(b) als Zuschnitt-Input an #100 hängen. | `a79c218`; Frontmatter `workflow-next`/`meeting-agenda`; `INBOX.md:17` | mittel |  |
| 44 | Verwerfen: erledigt | DSR §8 macht „Ausgearbeitet, Change fehlt“ in `workflow-next` und `workflow-status` sichtbar, mit `/dtb:task {N}` als nächstem Schritt. | `DERIVED_STATE_RULES.md:452-470`; `skills/dtb-workflow-next/SKILL.md:38-45`, `:74`; `c2176d9`/`b60105f` | hoch |  |
| 35 | Befördern | Teilweise behoben (Remote-Achse im Resume, `review.md`-Zweig); ein SHA-Anker für die Gültigkeit und die Achse HEAD ↔ Checkpoint-Stand fehlen. | `skills/dtb-workflow-resume/SKILL.md:142-147`, `:309-312`; `skills/dtb-workflow-checkpoint/SKILL.md:239`, `:244-252` | mittel |  |
| 34 | Verwerfen: erledigt | Die Entscheidung ist revidiert, `lessons.md` ist seit 2026-09-07 versioniert. | `f75979d`; `.gitignore`-Kommentar „Revision … INBOX #34“ | hoch |  |
| 32 | Befördern | Schritt 2 nennt kein Aufnahmekriterium, für externe Vorbilder gibt es keinen eigenen Abschnitt. | `skills/dtb-feature-discover/SKILL.md:86-89` | hoch |  |
| 31 | Befördern | Ein Lock-Eintrag, dessen Repo-Pfad existiert, der aber kein Klasse-A-Muster trifft, fällt durch jedes Raster. | `skills/dtb-kit-sync/SKILL.md:130-131`, `:145-147` | mittel |  |
| 23 | Befördern | Multi-Repo wird über die Zahl der `config.repos`-Einträge definiert, nicht über den Git-Toplevel. | `DERIVED_STATE_RULES.md:145-148`; `skills/dtb-implement/SKILL.md:224` | hoch |  |
| 22 | Befördern | Für Seeds gibt es keine Skew-Meldung, die Spiegel-Hinweise verweisen ausdrücklich auf #22 als offen. | `skills/dtb-project-health/SKILL.md:258`; `skills/dtb-kit-sync/SKILL.md:265`; `DERIVED_STATE_RULES.md:435`, `:482` | hoch |  |
| 18 | Befördern | `feature-discover` liest keine `ROADMAP.md`: `consumes` nennt sie nicht, Schritt 1 sucht nur in der INBOX. | `skills/dtb-feature-discover/SKILL.md:31-36` | hoch |  |

**Auffälligkeiten Teil 3**
- Im versionierten `lessons.md` fehlen **L22 bis L34** (eingecheckt 1-21, 35, 36 in `f75979d`) — von der Hauptsession per Grep bestätigt.
- #47 und #32 betreffen denselben Abschnitt `## Betroffene Module` in `feature-discover` (dazu #18).
- kit-sync-Familie: #31, #55, #51, #82, #108, #109.
- „Zustand ohne Pfleger“: #52 und #53 gemeinsam entscheiden.
- #63 (Ort) und #56 (Zeit) sind dieselbe Klasse „relative Bezeichnung“. #46/#58 bei Verwerfen als Belege in #100 nachtragen.

