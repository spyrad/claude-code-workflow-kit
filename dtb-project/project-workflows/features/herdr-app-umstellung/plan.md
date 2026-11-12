# Implementierungsplan: Herdr-App-Umstellung

**Erstellt:** 2026-11-12
**Feature-Spec:** `features/herdr-app-umstellung/spec.md`
**Geschaetzte Dauer:** ca. 9 Stunden (4 Phasen)
**Status:** Reviewed (plan-review 2026-11-12: REVISE → 5 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Probe in der App + Sichtung der Lektionen/Befunde + Entscheidungen | 2,5–3 h | Geplant |
| Phase 2 | `dtb:worker` umbauen (die eine Quelle der Kommandos) | 2,5–3 h | Geplant |
| Phase 3 | Folge-Skills (`pane-start`, `workflow-resume`, `workflow-checkpoint`) + Doku | 1,5–2 h | Geplant |
| Phase 4 | Abnahme-Wirklaeufe in der App | 1–1,5 h | Geplant |

**Ausfuehrungsort:** Phase 1 und Phase 4 brauchen eine Claude-Session, die IN der Herdr-App
laeuft (Terminal der App). Phase 2 und 3 sind reine Textarbeit und ortsunabhaengig.
**Arbeitszweig:** `feature/herdr-app-umstellung`, von Hand im Haupt-Checkout angelegt
(`git switch -c`) — `dtb:pane-start` steht fuer dieses Feature nicht zur Verfuegung (es ist
selbst Gegenstand des Umbaus).
**Probelaeufe** immer gegen die Repo-Fassung `skills/…/SKILL.md`, nie gegen `~/.claude/` (L74).

---

## Ist-Analyse

> Quelle: `discovery.md` (8 Module, Pfade verifiziert 2026-11-12), ergaenzt um die beim Planen
> gelesenen Sektionen.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-worker/SKILL.md | 741 Zeilen. Herdr nur im Pane-Traeger: `### Traeger-Weiche` (Gate `HERDR_ENV`/`HERDR_PANE_ID`), `### Pane-Auftrag` (Vorlage, Rueckweg-Zeile `herdr agent prompt`), `### Pane-Ausfuehrung` mit `#### Hinweg: Vorbedingungen`, `#### Hinweg: Start-Sequenz` (4 Kommandos + Signal-Einrichtung: Stop-Hook als PowerShell-Skript im Git-Verwaltungsordner, `claude --settings`), `#### Rueckweg: Warten ohne Warten` (Ausgaenge a–d, d = `WORKER-STOP`), `#### Rueckweg: Ueberwachungs-Tick` (Pruefliste, `/loop 15m`-Angebot, Meldungsformen), `#### Rueckweg: Branch-Verifikation` (herdr-frei). Frontmatter-`description` nennt „visible Herdr session" |
| skills/dtb-pane-start/SKILL.md | 354 Zeilen. `## Herdr-Gate (hart)`, Vorbedingung 1c.4 (`herdr agent list`), `## Struktur-Check` (3/3 Anker im Worker: `### Pane-Auftrag`, `### Pane-Ausfuehrung`, `#### Rueckweg: Ueberwachungs-Tick`), `## Herdr-Mechanik` (vier bewusste Abweichungen, u. a. Startbefehl OHNE `--settings`), Begruessungstext mit Rueckweg-Zeile, Tick-Angebot im Abschluss |
| skills/dtb-workflow-resume/SKILL.md | Schritt 2a: Adress-Pruefung per Bash-Block (`HERDR_ENV` + `herdr agent get`, Ausgaben `ERREICHBAR`/`NICHT-ERREICHBAR`/`HERDR-AUS`), Rueckweg-Zeile, Kopplungs-Hinweis „Herdr-Kanon"; drei `## Pane-Uebergabe`-Ausgabeformen |
| skills/dtb-workflow-checkpoint/SKILL.md | Fuenf Stellen mit Orchestrator-Adresse (Stand 2026-11-12): Transport-Zeile im Worktree-Hand-off („Herdr-Session-Kommunikation an die Orchestrator-Pane", Z. 170); Lesen des juengsten `Orchestrator:`-Werts aus der Notiz (Z. 70); Rueckfrage `Orchestrator-Pane? · weiter = ohne …` samt Vorbelegung aus der Notiz (Z. 97–98); Notiz-Format `Orchestrator: {pane-id oder —}` (Z. 258). Nur die erste nennt Herdr woertlich — die anderen vier tragen das alte Adress-Schema still mit |
| skills/CLAUDE.md | Orchestrator-Muster: Transport-Beispiel und Absatz „Pane-Worker" |
| CLAUDE.md | Zwei Beschreibungs-Absaetze (Session lifecycle, Autonomous execution) mit Herdr-, Stop-Hook- und Tick-Bezug |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §10 traegt den Gegen-Hinweis auf `#### Rueckweg: Ueberwachungs-Tick` (Spiegel Signal 2) — betroffen, falls der Anker umbenannt wird |
| dtb-project/project-rules/lessons.md | 19 Lektionen mit Herdr-/Pane-Bezug (64, 67, 69, 77, 79, 86, 87, 91, 93–97, 119, 120, 122–124, 127) — Sichtung in Schritt 1.4 |
| dtb-project/project-workflows/INBOX-BEFUNDE.md | 12 Zeilen mit Herdr-Bezug — Sichtung in Schritt 1.4 |

**Befehls-Zuordnung (Quelle: `hc --skill`, `herdr-app --skill`, hc 0.1.20 — ungeprueft bis Phase 1):**

| Alt (`herdr`-CLI) | Neu |
|---|---|
| Gate `HERDR_ENV=1` + `command -v herdr` + `$HERDR_PANE_ID` | `$HC_TERMINAL_ID` nicht leer + `command -v hc` + `command -v herdr-app` |
| `herdr agent list` / `herdr pane list` | `hc ls` (JSON beim Pipen) |
| `herdr agent get {pane}` | `hc get {t}` (Exit 3 = nicht gefunden, 11 = beendet) |
| `herdr agent prompt {pane} "…"` | `hc send {t} "…"` |
| `herdr pane read … --source recent --lines 80` | `hc read --lines 80 {t}`; nur Bildschirm: `--lines 0` |
| `pane split` + `pane run "claude"` + Erkennungs-Warten + `agent prompt` | Start mit erstem Auftrag in einem Zug: `hc run --bg --name {slug} --cwd {worktree} --label herdr.space={space-id} claude "{eine Zeile}"`, danach `herdr-app do tab.rename --id {tab-id} --name {slug}`; Beleg der Zustellung ueber `hc get` (kein `first_message.sent` bei diesem Startweg) — belegt in `probe.md` Probe 2 |
| Stop-Hook `WORKER-STOP` + `/loop`-Tick | eingebaute Meldungen `<hc>… is blocked / exited …</hc>` + eigene Meldung des Workers `<hc from="…">` + Pruefung auf Zuruf — belegt in `probe.md` Probe 3 |

---

## Phase 1: Probe, Sichtung, Entscheidungen

### Ziel
Belegen, dass die Annahmen aus den Anleitungen in der Praxis tragen, bevor ein Skill geaendert
wird — und die offenen technischen Entscheidungen auf dieser Grundlage treffen.

### Schritte

#### Schritt 1.0: Planungsstand sichern, Arbeitszweig anlegen
- **Zweck:** Der Umbau startet von einem committeten Stand auf einem eigenen Zweig (kein Schritt ausser diesem legt ihn an)
- **Dateien:** keine inhaltliche Aenderung — Commit von `features/herdr-app-umstellung/{discovery,spec,plan}.md`, `INBOX.md`, `BACKLOG.md` auf `master`; danach `git switch -c feature/herdr-app-umstellung`
- **Input:** reviewter Plan (Kopf-Statusfeld `Reviewed`)
- **Output:** `git status --short` leer; `git branch --show-current` = `feature/herdr-app-umstellung`; alle weiteren Schritte laufen auf diesem Zweig. Vorbereitungsschritt — zaehlt nicht in den 3x3-Rhythmus

#### Schritt 1.1: Umgebung und Adressen
- **Zweck:** Gate-Bedingung und Adress-Schema belegen
- **Dateien:** `features/herdr-app-umstellung/probe.md` (neu; Ablageort aller Probe-Ergebnisse, L20)
- **Input:** Claude-Session in einem Terminal der Herdr-App, Arbeitsverzeichnis = Haupt-Checkout
- **Output:** Abschnitt „Probe 1": Wert von `$HC_TERMINAL_ID`; weitere `HC_*`-Variablen; `command -v hc herdr-app` aus Git Bash UND PowerShell; Versionen; Ausschnitt `hc ls` und `herdr-app ls` (Zuordnung Terminal-ID ↔ Tab/Pane-ID, Feld fuer das Arbeitsverzeichnis); Gegenprobe ausserhalb der App (Variable leer)

#### Schritt 1.2: Start, Sichtbarkeit, Zustellung
- **Zweck:** Den einen Startweg finden, der drei Dinge zugleich liefert: sichtbarer, benannter Tab · Terminal gilt als Kind des Orchestrators · erster Auftrag kommt an
- **Dateien:** `probe.md`
- **Input:** Wegwerf-Worktree `zz-test-hc-probe` (eigener Branch, nach der Probe entfernt — L57)
- **Output:** Abschnitt „Probe 2", je Variante ein Ergebnis mit Belegzeile:
  (A) `herdr-app do tab.new --name … --argv '["claude"]' --task "…"` — Elternbezug per `hc get` pruefen;
  (B) `hc run --bg --name … --cwd … claude "…"` und danach im Tab zeigen (`herdr-app commands` → passender Befehl);
  dazu: `first_message.sent`, Verhalten beim Vertrauens-Dialog, mehrzeiliger Auftrag als EIN Argument, `hc send` mit Slash-Befehl aus Git Bash (Pfad-Umschreibung, L95), Senden waehrend im Ziel ein Auswahldialog offen ist (L123) und waehrend dort ein Entwurf steht (L122)

#### Schritt 1.3: Rueckmeldung ohne Hook und ohne Takt
- **Zweck:** Klaeren, ob Stop-Hook und Ueberwachungs-Tick entfallen koennen
- **Dateien:** `probe.md`
- **Input:** der Wegwerf-Worker aus 1.2
- **Output:** Abschnitt „Probe 3": Welche Meldung erreicht den Orchestrator von selbst bei (i) Turn-Ende ohne Terminal-Ende, (ii) Rueckfrage-Dialog (`blocked`), (iii) Session-Ende, (iv) Tab geschlossen? In welcher Form (Tag `<hc from=…>`)? Meldet Claude Code ueberhaupt einen Status (`hc get` → `idle`/`working`/`done`) oder braucht es eine Integration? Verhalten von `hc wait --children any`. Verhalten bei geschlossenem App-Fenster. **Empfangsseite Orchestrator (Pflicht):** (v) eine Worker-Meldung trifft ein, waehrend beim Orchestrator ein Auswahldialog offen ist — beantwortet sie den Dialog? (vi) eine Worker-Meldung trifft ein, waehrend der Mensch dort tippt — wird sie zurueckgehalten, angehaengt oder mit abgeschickt? Urteil: Hook entfaellt ganz / Rest bleibt (welcher). **Beantwortet eine Meldung in (v) den Dialog, gilt „Stop-Hook entfaellt ganz" als nicht tragfaehig** — der Dialog-Schutz des alten Hooks braucht dann einen Ersatz, der in 1.5 benannt wird

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Lektionen und Befunde sichten
- **Zweck:** Erfahrungswissen nicht verlieren und nicht ungeprueft weitertragen
- **Dateien:** `features/herdr-app-umstellung/sichtung.md` (neu)
- **Input:** 19 Lektionen und 12 Befund-Zeilen aus der Ist-Analyse, Probe-Ergebnisse
- **Output:** Tabelle `| Quelle | Kern | Urteil (gilt weiter / gilt angepasst / ueberholt) | Beleg (Probe-Abschnitt oder Begruendung) |`; Mengenprobe: Zeilenzahl = Eingangsmenge (L90). Keine Aenderung an `lessons.md` oder am Becken — die Ausmusterung laeuft spaeter ueber `dtb:lesson-curate` / `dtb:idea-triage`. **Dazu der repo-weite Leser-Scan (L3, vor dem Umbau statt danach):** Grep nach `Ueberwachungs-Tick`, `WORKER-STOP`, `HERDR_`, `herdr ` und den Skill-Namen `dtb:worker`/`dtb:pane-start` ueber das ganze Repo ausser `dtb-project/project-changelog/`, `archive/` und den Feature-Ordnern → Abschnitt „Leser-Scan" in `sichtung.md`: jede Fundstelle mit Urteil „im Plan abgedeckt (Schritt N.M)" oder „fehlt"; ein „fehlt" fuehrt in 1.5 zu einer Plan-Ergaenzung

#### Schritt 1.5: Entscheidungen festschreiben
- **Zweck:** Phase 2 und 3 auf Belege stellen
- **Dateien:** `plan.md` (Tabelle „Technische Entscheidungen": jede Zeile „Offen" → Entscheidung mit Verweis auf den Probe-Abschnitt), `spec.md` (`## Offene Punkte` nachfuehren)
- **Input:** `probe.md`, `sichtung.md`
- **Output:** keine Zeile der Entscheidungstabelle steht mehr auf „Offen". **Abweichungs-Regel:** Faellt eine Entscheidung anders aus als der Vorschlag in der Tabelle (oder meldet der Leser-Scan ein „fehlt"), werden die betroffenen Schritte der Phasen 2–4 im selben Zug angepasst und dem Menschen als Aenderungsliste zur kurzen Bestaetigung gezeigt — kein neues Review. **Kippt eine Kernannahme** (keine Adresse, keine Zustellung, oder eine Meldung beantwortet einen offenen Dialog am Orchestrator ohne tragfaehigen Ersatzschutz) → Stopp, Befund melden, Plan ueberarbeiten und `/dtb:plan-review` erneut fahren statt umbauen

### Deliverables
- [ ] `probe.md` mit drei Probe-Abschnitten und je Punkt einer Belegzeile
- [ ] `sichtung.md` mit Urteil je Lektion und Befund
- [ ] Entscheidungstabelle im Plan ohne „Offen"

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f dtb-project/project-workflows/features/herdr-app-umstellung/probe.md` und `grep -cE '^## Probe [123]' …/probe.md` = 3
- [ ] `grep -cE '^\| *(L[0-9]+|#[0-9]+) ' …/sichtung.md` = 31 (19 Lektionen + 12 Befunde; Zahl beim Sichten gegen eine Stichprobe der Zeilen pruefen, L17)
- [ ] `sed -n '/^## Technische Entscheidungen/,/^## Progress/p' …/plan.md | grep -c '| Offen'` = 0
- [ ] `git worktree list | grep -c zz-test-hc-probe` = 0 (Wegwerf-Worktree entfernt)
- [ ] `git branch --show-current` = `feature/herdr-app-umstellung`
- [ ] `grep -c '^## Leser-Scan' …/sichtung.md` = 1 und darin `grep -c '| fehlt'` = 0 nach Schritt 1.5 (jede fehlende Stelle ist in den Plan aufgenommen)

#### Manual
- [ ] Der Mensch bestaetigt die Entscheidungstabelle (vor allem: Stop-Hook entfaellt ganz oder bleibt ein Rest; Tab nach der Abnahme)

---

## Phase 2: `dtb:worker` umbauen

### Ziel
Der Pane-Traeger laeuft vollstaendig ueber `hc`/`herdr-app`. Der Worker bleibt die EINE Quelle
aller Kommandos; Sektions-Titel bleiben stabil, soweit die Entscheidung aus 1.5 nichts anderes sagt.

### Schritte

#### Schritt 2.1: Gate, Traeger-Weiche, Frontmatter
- **Zweck:** Einstieg und Selbstbeschreibung umstellen
- **Dateien:** `skills/dtb-worker/SKILL.md` (`### Traeger-Weiche`, Frontmatter `description`)
- **Input:** Gate-Bedingung aus Probe 1
- **Output:** Gate auf `$HC_TERMINAL_ID` + `hc` + `herdr-app`; ⛔-Meldung nennt den Weg „Session in der Herdr-App starten"; `description` ohne „Herdr session"-Altform; `allowed-tools` gegen die neuen Kommandos geprueft (L75 — alles laeuft ueber Bash, erwartet: unveraendert)

#### Schritt 2.2: Pane-Auftrag und Vorbedingungen
- **Zweck:** Auftragstext und Rueckkanal umstellen
- **Dateien:** `skills/dtb-worker/SKILL.md` (`### Pane-Auftrag`, `#### Hinweg: Vorbedingungen`)
- **Input:** Adress-Schema aus Probe 1, Zustell-Befunde aus Probe 2
- **Output:** Orchestrator-Adresse aus `$HC_TERMINAL_ID`; Rueckweg-Zeile `hc send {orchestrator} "<der komplette Block>"`; Syntax-Stand mit Datum UND geprüfter hc-Version; Kopplungs-Hinweis (deklarierte Ausnahmen 1 und 2) auf die neuen Kommandos; Vorbedingung 2 („fremde Session im Haupt-Checkout") ueber `hc ls`. **Ergaenzt nach 1.5:** (a) Meldepflicht — der Worker meldet das Ende JEDES Turns selbst per `hc send` (ein Turn-Ende meldet die App nicht, Probe 3.2); (b) Hand-off-Datei — der Worker schreibt den Block zusaetzlich in eine Datei im Git-Verwaltungsordner des Worktrees und wiederholt das Senden, wenn `hc send` mit Exit 9 abweist (offener Dialog beim Orchestrator, Probe 3.8); nie `--force`; (c) keine Slash-Befehle im zugestellten Text als Ausloeser (Probe 2.S4), Text mit fuehrendem `/` aus Git Bash mit `MSYS_NO_PATHCONV=1` (2.S3)

#### Schritt 2.3: Start-Sequenz
- **Zweck:** Worker-Arbeitsplatz als sichtbaren, benannten Tab starten
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Hinweg: Start-Sequenz`)
- **Input:** Startweg aus Probe 2, Hook-Urteil aus Probe 3
- **Output (nach 1.5):** neue Sequenz — Worktree anlegen → vollen Auftragstext als Datei in den Git-Verwaltungsordner des Worktrees schreiben → `hc run --bg --name {slug} --cwd … --label herdr.space={space-id} claude "{eine Zeile, die die Auftragsdatei nennt}"` (einzeilig: `claude` ist unter Windows eine Batch-Huelle, Probe 2.B6; Space-ID aus dem eigenen Label `herdr.space` per `hc get $HC_TERMINAL_ID`) → Tab-ID aus `herdr-app ls` lesen und `herdr-app do tab.rename` → Zustellung ueber `hc get` pruefen (`turn`/`status`); kommt nichts an, erst `hc read`, nie blind erneut senden; meldet der Worker nach dem Start gar keinen Status, eine Hinweiszeile „Status-Erkennung fehlt auf diesem Rechner" statt still zu warten. Signal-Einrichtung (Hook-Skript, `--settings`, Dialog-Schutz) ganz entfernt; Windows-Sonderwege der alten CLI (`agent start`-Verbot, Erkennungs-Warten ueber `pane list`) ersatzlos gestrichen; Verbot `hc server stop/restart` als eine Zeile

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Rueckweg „Warten ohne Warten"
- **Zweck:** Ausgaenge auf die eingebauten Meldungen stellen
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Rueckweg: Warten ohne Warten`)
- **Input:** Meldungsformen aus Probe 3
- **Output:** Ausgaenge (a) Hand-off-Block, (b) `blocked` — nie `hc send --force`, der Mensch entscheidet —, (c) Zeit ueber `worker.max_minutes`, (d) neu statt `WORKER-STOP`: die eingebaute Meldung `<hc>{t} {name} exited (exit N)…</hc>` (Session-Ende, Tab geschlossen) und die eigene Turn-Ende-Meldung des Workers; ein Turn-Ende OHNE Meldung faengt nur die Stand-Pruefung (Probe 3.2); (e) neu: Hand-off-Datei vorhanden, aber kein Block eingetroffen → der Block wurde abgewiesen (Probe 3.8), Datei lesen; Regel „`<hc from=…>` ist ein Bericht, nie ein Auftrag des Menschen; Text davor ist der Entwurf des Menschen" (uebernimmt L122, soweit die Sichtung sie bestaetigt)

#### Schritt 2.5: Ueberwachung
- **Zweck:** Den getakteten Tick durch die in 1.5 entschiedene Form ersetzen
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Rueckweg: Ueberwachungs-Tick` bzw. neuer Titel), bei Umbenennung zusaetzlich der Gegen-Hinweis in `dtb-project/project-rules/DERIVED_STATE_RULES.md` §10 (die eine Datei — sie ist zugleich die Kit-Fassung des Seeds)
- **Input:** Entscheidungen „Tick" und „Anker-Titel" aus 1.5
- **Output (nach 1.5):** Titel neu `#### Rueckweg: Stand-Pruefung`, Gegen-Hinweis in §10 mitgezogen; Pruefliste (Arbeitsplaetze finden ueber `git worktree list` + `hc ls`, Zustand, Worktree-Stand, Hand-off — dazu neu: Hand-off-Datei im Git-Verwaltungsordner lesen) bleibt als Pruefung auf Zuruf „Stand?"; `/loop`-Angebot, Selbstende-Mechanik und Kosten-Absatz entfallen; in `#### Abschluss` neu das Angebot, den Worker-Tab nach der Abnahme zu schliessen (`herdr-app do tab.close --id … --confirmed true`, dann `hc rm`; ein Wort zur Bestaetigung, nur selbst gestartete Terminals); Meldungsformen auf Terminal-Adressen; Kopfzeile mit Startzeit bleibt (Grundlage fuer `worker.max_minutes`)

#### Schritt 2.6: Eigenpruefung des neuen Textes
- **Zweck:** Der Umbau beseitigt eine Fehlerklasse (Kommando-Drift) — den eigenen Text ausdruecklich dagegen pruefen (L15)
- **Dateien:** `skills/dtb-worker/SKILL.md`; Ergebnis als Abschnitt „Eigenpruefung Phase 2" in `probe.md` (Ablageort, L20)
- **Input:** fertiger Text aus 2.1–2.5
- **Output:** jedes `hc`-/`herdr-app`-Kommando im Skill steht woertlich so in `probe.md` oder ist dort als ungeprueft markiert; jeder Bash-Block einzeln in frischer Shell ausgefuehrt (Mechanik-Regel „eigene Shells"); Listen-Lauf (Schritt 7 des Skills) und Subagenten-Traeger unveraendert

### Deliverables
- [ ] `skills/dtb-worker/SKILL.md` ohne Kommandos der alten CLI im Pane-Traeger
- [ ] Abschnitt „Eigenpruefung Phase 2" in `probe.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE 'herdr (agent|pane|integration) [a-z-]+' skills/dtb-worker/SKILL.md` = 0 (Kommando-Formen; Abschaffungs-Notizen nennen die alte CLI nur als „alte `herdr`-CLI", nie in Kommando-Form — L116)
- [ ] `grep -cE 'HERDR_(ENV|PANE_ID)' skills/dtb-worker/SKILL.md` = 0
- [ ] `grep -cE '^### (Traeger-Weiche|Pane-Auftrag|Pane-Ausfuehrung)' skills/dtb-worker/SKILL.md` = 3 (Anker stabil)
- [ ] `grep -c 'HC_TERMINAL_ID' skills/dtb-worker/SKILL.md` ≥ 2 (Gate + Auftrag)
- [ ] Nach 1.5: `grep -c '^#### Rueckweg: Stand-Pruefung' skills/dtb-worker/SKILL.md` = 1 und `grep -cE 'Ueberwachungs-Tick|WORKER-STOP|claude --settings' skills/dtb-worker/SKILL.md` = 0; `grep -c 'Ueberwachungs-Tick' dtb-project/project-rules/DERIVED_STATE_RULES.md` = 0
- [ ] Subagenten-Traeger und Listen-Lauf unberuehrt — der Abschnitt ab `### Schritt 6: Worker starten` bis Dateiende ist gleich dem Stand vor dem Umbau (gegen den merge-base, L85): `diff <(git show "$(git merge-base master HEAD)":skills/dtb-worker/SKILL.md | sed -n '/^### Schritt 6: Worker starten/,$p') <(sed -n '/^### Schritt 6: Worker starten/,$p' skills/dtb-worker/SKILL.md)` liefert keine Ausgabe; Gegenprobe: beide Seiten haben mehr als 0 Zeilen (Werkzeug-Fehlschlag ist kein Befund)

#### Manual
- [ ] Der Mensch liest die neue Start-Sequenz und den Rueckweg einmal gegen `probe.md` (stimmen Ablauf und Meldungen mit dem Erlebten ueberein?)

---

## Phase 3: Folge-Skills und Doku

### Ziel
Alle Leser und Spiegel des Workers nachziehen; Kopplungen mechanisch verifizieren.

### Schritte

#### Schritt 3.1: `dtb:pane-start`
- **Zweck:** Interaktiven Arbeitsplatz auf den neuen Unterbau stellen
- **Dateien:** `skills/dtb-pane-start/SKILL.md` (`## Herdr-Gate (hart)`, 1c Vorbedingung 4, `## Struktur-Check`, `## Herdr-Mechanik`, Begruessungstext, `## Rueckweg und Abschluss`, Frontmatter `description`)
- **Input:** Worker-Fassung aus Phase 2
- **Output:** Gate wie im Worker; Struktur-Check-Anker = die Titel, die Phase 2 hinterlaesst (Zahl im Text „N/N" passend); die vier bewussten Abweichungen neu formuliert (die Abweichung „Startbefehl OHNE Signal-Einrichtung" entfaellt, wenn der Hook entfaellt); Rueckweg-Zeile im Begruessungstext spiegelt die Vorlage; Wartepflicht und Begruessungs-Inhalt unveraendert. **Nach 1.5:** der Tick-Anker heisst `#### Rueckweg: Stand-Pruefung`, das `/loop`-Angebot im Abschluss wird zum Hinweis auf „Stand?"; die Begruessung reist wie der Worker-Auftrag als Datei plus EINE Startzeile (Start-Sequenz per Referenz); der vorgeschlagene Startbefehl bleibt ein Vorschlag, den der Mensch tippt (per `hc send` waere er ohnehin nicht ausloesbar, Probe 2.S4)

#### Schritt 3.2: `dtb:workflow-resume` und `dtb:workflow-checkpoint`
- **Zweck:** Pane-Uebergabe und Hand-off-Transport nachziehen
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md` (Schritt 2a: Bash-Block der Adress-Pruefung, Rueckweg-Zeile, Kopplungs-Hinweis), `skills/dtb-workflow-checkpoint/SKILL.md` (alle fuenf Stellen mit Orchestrator-Adresse laut Ist-Analyse: Transport-Zeile, Lesen des `Orchestrator:`-Werts, Rueckfrage `Orchestrator-Pane?` mit Vorbelegung, Notiz-Format — Zeilennummern vor dem Aendern frisch nachlesen, L60)
- **Input:** Adress-Schema aus Probe 1
- **Output:** Adress-Pruefung per `hc get` (nur der Exit-Code zaehlt), Ausgaben `ERREICHBAR`/`NICHT-ERREICHBAR` und eine umbenannte Aus-Marke statt `HERDR-AUS`; alte Uebergabe-Notizen mit Adressen im alten Schema → `NICHT-ERREICHBAR` (kein Sonderfall); Bash-Block einzeln in frischer Shell getestet

#### Schritt 3.3: Doku
- **Zweck:** Autoren-Doku und Kit-Beschreibung stimmen mit den Skills
- **Dateien:** `skills/CLAUDE.md` (Orchestrator-Muster: Transport-Beispiel, Absatz „Pane-Worker"; Autonomie-Regel nur falls beruehrt), `CLAUDE.md` (Absaetze „Session lifecycle" und „Autonomous execution": Stop-Hook, Tick, Herdr-Gate)
- **Input:** Endfassung der Skills
- **Output:** keine Beschreibung nennt mehr Stop-Hook, `claude --settings`, `HERDR_ENV=1` oder `/loop 15m` als geltenden Stand

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Kopplungs-Sweep
- **Zweck:** Spiegel mechanisch verifizieren statt dem Fliesstext zu glauben (Kopplungsregel `skills/CLAUDE.md`; L3: repo-weit greppen)
- **Dateien:** alle Dateien aus Phase 2 und 3; Ergebnis als Abschnitt „Kopplungs-Sweep" in `probe.md`
- **Input:** Endfassung
- **Output:** Trefferlisten mit Zielzahl: Rueckweg-Zeile `hc send {orchestrator` in Worker, pane-start, resume (Zielzahl = Zahl der Spiegel); jeder Struktur-Check-Anker von pane-start existiert genau einmal im Worker (mit dem Grep-Werkzeug und `^`-Anker gefahren, L113); repo-weiter Grep (Gegenprobe zum Leser-Scan aus 1.4, dieselben Muster) nach `Ueberwachungs-Tick`, `WORKER-STOP`, `HERDR_` ausserhalb von `dtb-project/project-changelog/`, `archive/` und den Feature-Ordnern → jede Fundstelle begruendet oder bereinigt

### Deliverables
- [ ] Vier Skills und zwei Doku-Dateien auf dem neuen Stand
- [ ] Abschnitt „Kopplungs-Sweep" in `probe.md` mit Zielzahlen

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE 'herdr (agent|pane|integration) [a-z-]+|HERDR_(ENV|PANE_ID)' ` je Datei = 0 fuer `skills/dtb-pane-start/SKILL.md`, `skills/dtb-workflow-resume/SKILL.md`, `skills/dtb-workflow-checkpoint/SKILL.md`
- [ ] Jeder im `## Struktur-Check` von pane-start genannte Anker steht genau einmal im Worker — am Zeilenanfang verankert, OHNE `$`-Anker (die Titel tragen Zusaetze; Form wie im Struktur-Check selbst): `tr -d '\r' < skills/dtb-worker/SKILL.md | grep -c '^{Anker}'` = 1
- [ ] `grep -c '^## Pane-Uebergabe' skills/dtb-workflow-resume/SKILL.md` = 3 (Ausgabeformen unveraendert vorhanden)
- [ ] Checkpoint-Seite vollstaendig: `grep -c '^Orchestrator: {pane-id' skills/dtb-workflow-checkpoint/SKILL.md` = 0 und `grep -c 'Orchestrator-Pane?' skills/dtb-workflow-checkpoint/SKILL.md` = 0 (Notiz-Format und Rueckfrage tragen das neue Adress-Schema); `grep -c '^Orchestrator: {' skills/dtb-workflow-checkpoint/SKILL.md` = 1 (das Feld selbst bleibt)
- [ ] `grep -cE 'claude --settings|HERDR_ENV=1|/loop 15m' CLAUDE.md` = 0
- [ ] Nach 1.5: `grep -c 'Ueberwachungs-Tick' skills/dtb-pane-start/SKILL.md` = 0

> Hinweis ohne Sperrwirkung: der Umbau soll kuerzen, nicht aufblaehen (Ausgangswerte: worker 741,
> pane-start 354, resume 410 Zeilen) — die Zeilenzahl wird im Phasen-Bericht genannt, ist aber
> kein Kriterium.

#### Manual
- [ ] Der Mensch liest den neuen Begruessungstext von `pane-start` und die ⛔-Gate-Meldung (verstaendlich, nennt den Weg in die App)

---

## Phase 4: Abnahme-Wirklaeufe in der App

### Ziel
Die Success Criteria der Spec an echten Laeufen belegen — gefahren vom Orchestrator, der Mensch
schaut zu und entscheidet nur Abnahme oder Abbruch (L96). Befunde werden VOR der Abnahme
zugeordnet: nacharbeiten oder als eigene Idee auslagern (L97).

**Lade-Regel (verbindlich fuer alle Schritte dieser Phase):** Ein getippter Slash-Befehl laedt
die installierte ALTE Kopie aus `~/.claude/`. Deshalb wird vor der Abnahme nichts installiert
und kein Slash-Befehl fuer die umgebauten Skills getippt — stattdessen:
- Der Orchestrator liest die Repo-Datei des Arbeitszweigs (`skills/dtb-worker/SKILL.md` bzw.
  `skills/dtb-pane-start/SKILL.md`) und fuehrt deren Ablauf aus; der Mensch gibt den Start frei
  (die Freigabe ersetzt den getippten Befehl, die Autonomie-Regel bleibt gewahrt)
- Der Struktur-Check von `pane-start` wird gegen `skills/dtb-worker/SKILL.md` im Projekt-Root
  gefahren (seine Aufloesung bevorzugt sonst die installierte Kopie)
- `workflow-resume` und der Checkpoint „Wechsel"/„Ende" im Tab: der Auftrag nennt ausdruecklich
  die Datei im Worktree (`{worktree-pfad}/skills/dtb-workflow-resume/SKILL.md` bzw.
  `…/dtb-workflow-checkpoint/SKILL.md`) — der Worktree entsteht aus dem Arbeitszweig und traegt
  die neue Fassung
- Jeder Abnahme-Abschnitt in `probe.md` haelt in einer Zeile `Geladen: {Pfad}` fest, welche
  Datei gelaufen ist

### Schritte

#### Schritt 4.1: Worker-Lauf mit Pane-Traeger
- **Zweck:** Hinweg und Rueckweg am Stueck
- **Dateien:** Wegwerf-Aufgabe `features/zz-test-hc-worker/task.md` (vom Lauf selbst erzeugt und vorher committet, L18/L57); Protokoll als Abschnitt „Abnahme 4.1" in `probe.md`
- **Input:** Orchestrator-Session in der App, Repo-Fassung des Skills
- **Output:** eigener Tab mit dem Slug als Namen · Auftrag kam an · Worker committet auf `task/zz-test-hc-worker` · Hand-off-Block erreicht den Orchestrator · Ende-Meldung ohne Hook und ohne `/loop` · Branch-Verifikation gruen; danach Worktree, Branch und Wegwerf-Ordner entfernt. **Nach 1.5 zusaetzlich** (in der Probe ungeprueft bzw. neu): Hand-off trifft auf einen offenen Dialog beim Orchestrator → Datei vorhanden, Senden wiederholt, Block kommt an (3.8) · eine Meldung trifft ein, waehrend der Mensch beim Orchestrator tippt (3.9) · der Worker arbeitet bei geschlossenem App-Fenster zu Ende (3.10) · Angebot „Tab schliessen" nach der Abnahme

#### Schritt 4.2: `pane-start` und Session-Wechsel
- **Zweck:** Interaktiven Weg und Uebergabe-Notiz belegen
- **Dateien:** Protokoll „Abnahme 4.2" in `probe.md`
- **Input:** Wegwerf-Change `zz-test-hc-pane`
- **Output:** eigener Tab · Claude gestartet · Begruessung zugestellt · Session wartet (fuehrt den vorgeschlagenen Befehl nicht selbst aus) · im Tab: Checkpoint „Wechsel" → `/clear` → `workflow-resume` findet die Notiz und meldet die Orchestrator-Adresse als erreichbar · Checkpoint „Ende" liefert EINEN Hand-off-Block beim Orchestrator

#### Schritt 4.3: Gate ausserhalb der App und Aufraeumen
- **Zweck:** Negativfall und sauberer Endzustand
- **Dateien:** Protokoll „Abnahme 4.3" in `probe.md`
- **Input:** eine Session ausserhalb der App (normales Terminal)
- **Output:** `dtb:pane-start` und der Pane-Traeger brechen hart ab und nennen den Weg in die App; `workflow-resume` 2a laeuft ausserhalb der App still weiter (`ungeprueft`); `git worktree list` zeigt nur den Haupt-Checkout; kein `zz-test-`-Ordner, kein `task/zz-test-*`-Branch mehr. Der Abschnitt „Abnahme 4.3" endet mit der festen Zeile `→ Nach Merge und Push: /dtb:kit-sync sync (erst pushen, dann syncen — L39); bis dahin laufen unter ~/.claude/ die alten Skills` — und der Orchestrator gibt dieselbe Zeile im Chat aus

### Deliverables
- [ ] Drei Abnahme-Abschnitte in `probe.md`, je Success Criterion der Spec eine Belegzeile
- [ ] `kit-sync`-Zeile am Ende von „Abnahme 4.3" (geliefert von Schritt 4.3)

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE '^## Abnahme 4\.[123]' …/probe.md` = 3
- [ ] `grep -c '^Geladen: ' …/probe.md` ≥ 3 (Lade-Regel belegt) und `grep -c '^→ Nach Merge und Push: /dtb:kit-sync' …/probe.md` = 1
- [ ] `git worktree list | wc -l` = 1 und `git branch --list 'task/zz-test-*' 'feature/zz-test-*' | wc -l` = 0
- [ ] `ls dtb-project/project-workflows/features | grep -c '^zz-test-'` = 0

#### Manual
- [ ] Der Mensch hat beide Wirklaeufe im App-Fenster gesehen und bestaetigt: Tabs sichtbar und benannt, Meldungen kamen von selbst, kein Eingriff noetig ausser den vorgesehenen Entscheidungen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Altsystem | (A) ganz ersetzen, (B) beide parallel | A | Entscheidung des Menschen 2026-11-12 (Discovery) |
| Sichtbarkeit | (A) eigener Tab je Arbeitsplatz, (B) unsichtbares Terminal | A | Entscheidung des Menschen 2026-11-12 |
| Gate-Bedingung | (A) `$HC_TERMINAL_ID` + `hc` + `herdr-app` im PATH, (B) nur `hc` | A | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 1 (1.1–1.4 in der App gesetzt und aufrufbar, 1.13 außerhalb leer); `herdr-app` wird für das Umbenennen des Tabs gebraucht (2.B4) |
| Startweg (Tab + Kind-Beziehung + erster Auftrag) | (A) `herdr-app do tab.new … --task`, (B) `hc run --bg …` und danach im Tab zeigen | B | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 2: nur `hc run --bg --name … --cwd … --label herdr.space={id} claude "…"` liefert Kind-Beziehung (2.B2), sichtbaren Tab (2.B3) und ersten Auftrag (2.B5); danach `herdr-app do tab.rename` (2.B4). Folgen: erster Auftrag einzeilig (2.B6) — der volle Auftragstext liegt als Datei im Git-Verwaltungsordner des Worktrees, die eine Zeile nennt sie; `first_message.sent` entfaellt als Pruefung (2.B7), Beleg ist `hc get`/Bildschirm. Variante A scheidet aus (2.A3, 2.A6) |
| Stop-Hook | (A) entfaellt ganz, (B) Rest bleibt fuer „Turn-Ende ohne Terminal-Ende" | A | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 3: Rueckfrage, Session-Ende und geschlossener Tab melden sich von selbst (3.3–3.5); der Dialog-Schutz ist durch `hc send` abgedeckt (2.S5, 3.8 — Exit 9 statt Antwort). Zwei Reste ohne Hook geloest: (1) Turn-Ende ohne Hand-off wird nicht gemeldet (3.2) → Meldepflicht des Workers per `hc send` im Auftrag, Auffangnetz ist die Pruefung auf Zuruf; (2) ein abgewiesener Hand-off (3.8) → Block zusaetzlich als Datei im Git-Verwaltungsordner, Senden wiederholen, die Pruefung auf Zuruf liest die Datei |
| Ueberwachungs-Tick | (A) getakteter Lauf entfaellt, Pruefliste bleibt auf Zuruf „Stand?", (B) `/loop` bleibt als Netz | A | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 3 (3.3–3.5 Meldungen von selbst, 3.7 `hc wait --children any`). Die Pruefliste bleibt als Pruefung auf Zuruf und ist das Auffangnetz fuer die zwei Reste der Hook-Entscheidung (liest zusaetzlich die Hand-off-Datei); `/loop`-Angebot, Selbstende-Mechanik und Kosten-Absatz entfallen |
| Anker-Titel `#### Rueckweg: Ueberwachungs-Tick` | (A) behalten, (B) umbenennen (z. B. „Stand-Pruefung") und Spiegel mitziehen (pane-start, DSR §10) | B | Entscheidung des Menschen 2026-11-12 — neuer Titel `#### Rueckweg: Stand-Pruefung` (folgt der Tick-Entscheidung: ohne Takt ist der alte Titel irrefuehrend). Spiegel im selben Zug: Struktur-Check und Angebot in `dtb:pane-start` (Schritt 3.1), Gegen-Hinweis in `DERIVED_STATE_RULES.md` §10 (Schritt 2.5); Leser laut `sichtung.md` → Leser-Scan |
| Orchestrator-Adresse in Auftrag und Uebergabe-Notiz | (A) Terminal-ID (`t7`), (B) vergebener Name | A | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 1 (1.1 `$HC_TERMINAL_ID`, 1.9 `name: null` bei von Hand geoeffneten Tabs); ein Name laesst sich nachtraeglich nicht vergeben (`hc --help`: kein Befehl dafuer, nur `run --name`). Ob die ID einen Neustart des Kerns ueberlebt, ist ungeprueft — eine veraltete Adresse faellt in den bestehenden Weg `NICHT-ERREICHBAR` (Schritt 3.2) |
| Claude-Integration fuer die Status-Erkennung | (A) nicht noetig, (B) noetig → Vorbedingung im Gate oder Hinweis | A | Entscheidung des Menschen 2026-11-12 — `probe.md` Probe 3 (3.1: drei frische Sessions melden ihren Status ohne Zutun). Herkunft der Meldung ungeklaert, belegt nur auf diesem Rechner → keine Gate-Vorbedingung, aber eine Hinweiszeile in der Start-Sequenz (Schritt 2.3): meldet ein Worker nach dem Start keinen Status, das sichtbar sagen statt still zu warten |
| Tab nach der Abnahme | (A) der Mensch schliesst, (B) der Orchestrator bietet `hc kill` + `hc rm` an | B | Entscheidung des Menschen 2026-11-12 — Angebot nach der Abnahme, ein Wort zur Bestaetigung; nie von selbst, nie vor der Abnahme, nur selbst gestartete Terminals. Belegte Form: `herdr-app do tab.close --id {tab-id} --confirmed true`, danach `hc rm {t}` (`probe.md` 3.5 und Aufraeumen der Probe) |
| Versions-Hinweis | (A) Syntax-Stand mit Datum + hc-Version an den zwei Kommando-Orten, (B) Versions-Pruefung zur Laufzeit | A | bestehendes Muster („Syntax-Stand 2026-08-16"); eine Laufzeit-Pruefung waere neuer Umfang |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.0 Planungsstand sichern, Arbeitszweig anlegen
- [x] 1.1 Umgebung und Adressen
- [x] 1.2 Start, Sichtbarkeit, Zustellung
- [x] 1.3 Rueckmeldung ohne Hook und Takt
- [x] 1.4 Lektionen und Befunde sichten
- [x] 1.5 Entscheidungen festschreiben
- [ ] 2.1 Gate, Traeger-Weiche, Frontmatter
- [ ] 2.2 Pane-Auftrag und Vorbedingungen
- [ ] 2.3 Start-Sequenz
- [ ] 2.4 Rueckweg Warten ohne Warten
- [ ] 2.5 Ueberwachung
- [ ] 2.6 Eigenpruefung des neuen Textes
- [ ] 3.1 pane-start
- [ ] 3.2 workflow-resume und workflow-checkpoint
- [ ] 3.3 Doku
- [ ] 3.4 Kopplungs-Sweep
- [ ] 4.1 Worker-Lauf mit Pane-Traeger
- [ ] 4.2 pane-start und Session-Wechsel
- [ ] 4.3 Gate ausserhalb der App und Aufraeumen

---

## Umsetzung

Umsetzung mit `/dtb:implement Herdr-App-Umstellung` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/herdr-app-umstellung/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
