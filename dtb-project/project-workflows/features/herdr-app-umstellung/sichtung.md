# Sichtung: Lektionen, Befunde und Leser

**Stand:** 2026-11-12 · Grundlage: `probe.md` (hc 0.1.20, herdr-app 0.1.15)

Urteil je Zeile: **gilt weiter** (unverändert gültig) · **gilt angepasst** (Kern bleibt, Kommando
oder Form ändert sich) · **überholt** (Anlass fällt mit der alten `herdr`-CLI weg).
Diese Datei ändert nichts an `lessons.md` oder am Befund-Becken — die Ausmusterung läuft später
über `dtb:lesson-curate` bzw. `dtb:idea-triage`.

**Mengenprobe:** 19 Lektionen + 12 Befunde = 31 Zeilen. Eingangsmenge gegengezählt: 19 Treffer
auf die Lektions-Nummern der Ist-Analyse in `lessons.md`; 12 Zeilen mit „herdr" (ohne
Groß-/Kleinschreibung) in `INBOX-BEFUNDE.md`.

## Lektionen

| Quelle | Kern | Urteil | Beleg |
|--------|------|--------|-------|
| L64 | Bei Sicht-Skills eine Beispiel-Ausgabe früh vom Nutzer abnehmen lassen | gilt weiter | kein Herdr-Wirkbezug, die Pane war nur der Ort des Anlasses |
| L67 | Settings-Änderungen nur in einem frisch gestarteten Prozess prüfen, nie per `/clear` | gilt weiter | unabhängig vom Unterbau; „neue Pane" heißt künftig „neuer Tab" |
| L69 | Ein als Text angekommener Slash-Befehl feuert den Skill nicht; hat der Mensch ihn erkennbar abgesetzt, SKILL.md lesen und ausführen | gilt weiter | Probe 2.S4: per `hc send` kommt ein Slash-Befehl als Text im Tag an und wird nicht ausgeführt |
| L77 | Eine per Hand-off zugestellte Checkpoint-Aufforderung ist kein Befehl des Menschen — der Mensch tippt selbst | gilt weiter | Probe 2.S4 und 3.6: Zugestelltes ist Text im `<hc from=…>`-Tag |
| L79 | Kurze Takte nur ohne Menschen-Wartezeit; unabgeschickte Eingabe in der wartenden Pane erkennen | gilt angepasst | der Takt-Teil hängt an der Tick-Entscheidung (1.5); die unabgeschickte Eingabe bleibt möglich und ist per `hc read --lines 0 {t}` sichtbar (Probe 2.S6) |
| L86 | Einstellungsfenster in einer Herdr-Pane schließt nicht per Esc — rohes Escape per `herdr pane send-text` | überholt | das Kommando gehört zur alten CLI; in der App schloss `hc keys {t} esc` einen Auswahldialog (Probe 2, nach 2.S5). Das Einstellungsfenster selbst wurde nicht nachgestellt |
| L87 | Pane-Status nie per Regex über ein flaches JSON-Objekt lesen | gilt angepasst | das Erkennungs-Warten entfällt (Probe 2.B5: Auftrag reist mit dem Start); der Kern bleibt: auch `hc get` liefert verschachteltes JSON (Probe 1.9) — mit einem Parser lesen oder nur den Exit-Code werten |
| L91 | Regex und Python-Logik als Skriptdatei, nie inline oder im Heredoc | gilt weiter | am 2026-11-12 erneut eingetreten: ein Heredoc mit Anführungszeichen brach beim Schreiben von `probe.md` |
| L93 | Ableitungen aus `review.md` auf `^Decision: PENDING` stützen | gilt weiter | kein Herdr-Wirkbezug |
| L94 | Heredocs in Skill-Texten mit eindeutiger Endmarke und ohne Einrückung | gilt weiter | kein Herdr-Wirkbezug |
| L95 | Slash-Befehle aus Git Bash mit `MSYS_NO_PATHCONV=1` senden | gilt angepasst | Probe 2.S3: die Pfad-Umschreibung greift auch bei `hc send`; Probe 2.S4: ein Slash-Befehl wird per `hc send` aber gar nicht ausgeführt. Neue Regel: keine Slash-Befehle per `hc send`; Text mit führendem `/` trotzdem mit `MSYS_NO_PATHCONV=1` |
| L96 | Mehrstufige Pane-Abnahmen fährt der Orchestrator, der Mensch entscheidet nur Abnahme oder Abbruch | gilt angepasst | Transport ist `hc send` (Probe 2.S1); weil Slash-Befehle so nicht auslösbar sind (2.S4), nennt der Auftrag die Skill-Datei — deckt sich mit der Lade-Regel in Phase 4 |
| L97 | Befunde eines Abnahme-Laufs vor der Abnahme zuordnen | gilt weiter | kein Herdr-Wirkbezug |
| L119 | Nach `herdr update` die neue Version mit vollem Pfad aufrufen | überholt | betrifft Aktualisierung und Integration der alten CLI. Für `hc` nicht nachgestellt; laut `hc --skill` erhalten neue Windows-Terminals einen aufgefrischten PATH |
| L120 | Hook-Befehle shell-neutral als `powershell -File` schreiben | gilt angepasst | allgemeine Hook-Regel bleibt gültig; im Worker ohne Anwendung, sobald der Stop-Hook entfällt (Entscheidung 1.5) |
| L122 | Eine automatische Nachricht hängt sich an einen halb getippten Entwurf — den Anker irgendwo in der Eingabe erkennen | gilt angepasst | Probe 2.S6: dieselbe Form, `entwurf<hc from="t13">…</hc>`; der Anker ist jetzt das Tag. Die Wartezeit bei echtem Tippen ist ungeprüft |
| L123 | Automatisches Senden beantwortet einen offenen Auswahldialog — vorher die Fußzeile prüfen | überholt | Probe 2.S5 und 3.8: `hc send` weist ab (Exit 9, `blocked (question)`), die Fußzeilen-Prüfung entfällt. Neue Folge: die abgewiesene Nachricht kommt nicht an und braucht eine Wiederholungs-Regel |
| L124 | Für die letzte Antwort `pane read --source recent --lines N`, für Fußzeilen `--source visible` | gilt angepasst | `hc read --lines N {t}` bzw. `--lines 0` für den Bildschirm (Probe 2); laut `hc --skill` liefert ein Verlaufs-Lesen bei `working`/`blocked`/`error` nur den Bildschirm |
| L127 | Hängt die Erkennung auf `working`, die Integrations-Version prüfen | überholt | betrifft die Integration der alten CLI; in der App meldeten drei frische Sessions ihren Status ohne Zutun (Probe 3.1) |

## Befunde

| Quelle | Kern | Urteil | Beleg |
|--------|------|--------|-------|
| #197 | Tick sieht nicht, wenn eine Pane auf den Menschen wartet, Herdr aber `working` meldet | gilt angepasst | die Statusquelle ist jetzt `hc` (Probe 3.1); ob dort dieselbe Fehlmeldung auftritt, ist ungeprüft. Form der Prüfung laut Tick-Entscheidung (1.5) |
| #191 | Herdr-Kanon im Worker gegen Herdr 0.9.4 prüfen | überholt | die Kommandos der alten CLI entfallen ganz (Phase 2) |
| #190 | „Korrektur senden" an eine laufende Pane dokumentieren | gilt angepasst | `hc send` an eine arbeitende Session wird zugestellt und trifft in der laufenden Runde ein (Probe 3.6); bei offenem Dialog Exit 9 (2.S5) |
| #168 | Skills setzen eigene Lektionen nicht um — darunter `herdr agent prompt` ohne `MSYS_NO_PATHCONV` | gilt angepasst | der Herdr-Teil wird mit dem Umbau neu geschrieben (Urteil zu L95); die übrigen Teile des Befunds sind unberührt |
| #163 | `blocked` vor der Blockade-Zeile am Pane-Inhalt gegenprüfen | gilt angepasst | `hc` liefert bei `blocked` die Art (`kind: question`) und meldet von selbst (Probe 3.3); eine Fehlmeldung `blocked` ohne Dialog ist unter `hc` ungeprüft — das Gegenlesen per `hc read --lines 0` bleibt sinnvoll |
| #161 | `pane run "claude"` nur wiederholen, wenn keine Claude-Session läuft | überholt | der Start läuft in einem Zug ohne Wiederholung (Probe 2.B1, 2.B5) |
| #157 | Pane bleibt `working`, solange Hintergrund-Agenten laufen — Erkennung auf den Prompt stützen | überholt | das Erkennungs-Warten entfällt, der erste Auftrag reist mit dem Start (Probe 2.B5) |
| #144 | Erkennungs-Warten auf `idle` läuft ins Leere | überholt | wie #157 |
| #128 | Ein zugestellter Hand-off führt den vorangestellten Checkpoint-Befehl nicht aus — den Menschen-Schritt ausdrücklich nennen | gilt weiter | Probe 2.S4 und 3.6 |
| #116 | Tick meldet den Wechsel `done`↔`idle` als Änderung | gilt angepasst | `hc` kennt beide Zustände ebenfalls (Probe 3.1, nach Esc `idle`, nach einem Turn `done`); ob die Regel gebraucht wird, hängt an der Tick-Entscheidung (1.5) |
| #104 | Tick soll eine unabgeschickte Eingabe erkennen | gilt angepasst | wie L79: per `hc read --lines 0 {t}` lesbar; Ort der Prüfung laut Tick-Entscheidung |
| #58 | Zwei halbseitige Pipeline-Kanten (Scan-Befund) | gilt weiter | kein Herdr-Wirkbezug — „Herdr" steht dort nur im Erledigt-Vermerk eines Teilfalls |

## Leser-Scan

Muster: `Ueberwachungs-Tick`, `WORKER-STOP`, `HERDR_`, `herdr ` und die Skill-Namen
`dtb:worker` / `dtb:pane-start`, über das ganze Repo außer `dtb-project/project-changelog/`,
`archive/` und den Feature-Ordnern. Treffer je Datei (Zeilen):

| Fundstelle | Treffer | Urteil |
|------------|---------|--------|
| `skills/dtb-worker/SKILL.md` | 62 (davon Tick 11, WORKER-STOP 6, `HERDR_` 8, Kommando-Formen 26) | im Plan abgedeckt (Schritte 2.1–2.6) |
| `skills/dtb-pane-start/SKILL.md` | 33 (Tick 5, WORKER-STOP 1, `HERDR_` 6, Kommando-Formen 2) | im Plan abgedeckt (Schritt 3.1) |
| `skills/dtb-workflow-resume/SKILL.md` | 6 (Tick 1, `HERDR_` 1, Kommando-Formen 3) | im Plan abgedeckt (Schritt 3.2) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 4 — nur die Skill-Namen (Frontmatter `after`, Worktree-Anlage, Verweis auf `#### Abschluss`, Kit-Sonderfall) | kein Handlungsbedarf an diesen vier Zeilen; die fünf Adress-Stellen ohne Mustertreffer sind im Plan abgedeckt (Schritt 3.2) |
| `skills/CLAUDE.md` | 6 (Autonomie-Regel, Abgrenzung pane-start, Absatz „Pane-Worker") | im Plan abgedeckt (Schritt 3.3) |
| `CLAUDE.md` | 2 (Absätze „Autonomous execution" und Change-Folder-Modell) | im Plan abgedeckt (Schritt 3.3); der zweite Treffer nennt nur `worker-report.md` — kein Handlungsbedarf |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | 3 (§1 `worker-report.md`, §10 Einleitung, §10 Gegen-Hinweis auf den Tick-Anker) | im Plan abgedeckt (Schritt 2.5, nur der Gegen-Hinweis); die zwei anderen nennen nur Skill-Namen |
| `skills/dtb-idea-rank/SKILL.md` | 4 — Verweis auf das Eignungs-Raster von `dtb:worker` | kein Handlungsbedarf (Raster liegt im Sicht-Modus, der unverändert bleibt) |
| `skills/dtb-project-init/SKILL.md`, `workflow.config.yaml` | 3 + 2 — `worker:`-Block (Versuche, Minuten) | kein Handlungsbedarf (Deckelung bleibt) |
| `skills/dtb-project-dashboard/SKILL.md` | 1 — Muster-Verweis auf den „Struktur-Check" von pane-start | kein Handlungsbedarf (Abschnitts-Titel bleibt, Schritt 3.1) |
| `skills/dtb-task`, `dtb-idea-review`, `dtb-feature-fast`, `dtb-feature-discover` (je `SKILL.md`) | je 1 — Pipeline-Frontmatter `next`/`after` | kein Handlungsbedarf (Skill-Namen bleiben) |
| `dtb-project/project-rules/lessons.md`, `INBOX-BEFUNDE.md`, `INBOX.md`, `WORKFLOW_STATUS.md` | 13 + 33 + 4 + 2 | Daten, keine Leser — Urteil in den Tabellen oben; Ausmusterung über `dtb:lesson-curate` / `dtb:idea-triage` |
| `dtb-project/claude-code-workflow-kit.html`, `dtb-project/project-dashboard.html` | 11 + 2 | erzeugte Seiten (`dtb:pipeline-graph`, `dtb:project-dashboard`) — entstehen beim nächsten Lauf neu, nicht von Hand ändern |
| `README.md` | 0 | kein Handlungsbedarf |

Außerhalb des Repos, nur zur Kenntnis: `~/.claude/settings.json` trägt weiter den Hook der alten
CLI (`hooks/herdr-agent-state.ps1`). Er gehört zur Installation der alten CLI — deren Abbau ist
laut Spec nicht Teil dieses Features.

**Ergebnis:** keine Fundstelle außerhalb des Plans. Plan-Ergänzungen entstehen nicht aus dem
Leser-Scan, sondern aus der Probe (siehe `probe.md`, Urteile zu Probe 2 und 3).
