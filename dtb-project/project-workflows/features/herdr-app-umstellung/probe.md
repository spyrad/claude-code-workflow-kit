# Probe: Herdr-App-Umstellung

**Stand:** 2026-11-12 · hc 0.1.20 · herdr-app 0.1.15 · Windows 11, Git Bash und PowerShell 5.1
**Ort:** Claude-Session in einem Terminal der Herdr-App, Arbeitsverzeichnis = Haupt-Checkout,
Zweig `feature/herdr-app-umstellung`.
**Quellen der Kommandos:** `hc --skill`, `herdr-app --skill`, `hc <befehl> --help`,
`herdr-app commands` (alle am 2026-11-12 gelesen).

Jede Zeile ist ein Beleg aus einem tatsächlich gefahrenen Kommando. Was nicht gefahren wurde,
steht als **ungeprüft** da.

---

## Probe 1: Umgebung und Adressen

| # | Punkt | Kommando | Ergebnis |
|---|-------|----------|----------|
| 1.1 | Eigene Adresse gesetzt | `env \| grep -E '^(HC_\|HERDR_)'` (Git Bash) | `HC_TERMINAL_ID=t13`, `HC_SCOPE=0-95ff…`, `HC_TERMINAL_SOCKET=\\.\pipe\herdr-core-damia-default.sock`; keine `HERDR_*`-Variable gesetzt |
| 1.2 | Adresse in PowerShell | `$env:HC_TERMINAL_ID` | `t13` |
| 1.3 | Werkzeuge im PATH (Git Bash) | `command -v hc herdr-app` | `/c/Users/…/AppData/Local/Programs/herdr-core/hc`, `…/Programs/herdr-app/herdr-app` — beide gefunden, Exit 0 |
| 1.4 | Werkzeuge im PATH (PowerShell) | `(Get-Command hc).Source`, `(Get-Command herdr-app).Source` | `…\herdr-core\hc.exe`, `…\herdr-app\herdr-app.exe` — beide gefunden |
| 1.5 | Alte CLI liegt ebenfalls im PATH | `command -v herdr` | `…/.herdr/packages/standalone/releases/0.9.4-preview…/herdr` — ein Gate auf „`herdr` vorhanden" unterscheidet die Systeme also nicht |
| 1.6 | Versionen | `hc --version`, `herdr-app --version` | `hc 0.1.20`, `herdr-app 0.1.15` |
| 1.7 | Terminal-Liste | `hc ls` (gepiped → JSON) | `{"hidden_finished":5,"terminals":[{"address":"t13","agent":"claude-code","cwd":"C:\\…\\claude-code-workflow-kit","state":"live","status":"working","turn":39,"where":"claude-code-workflow-kit / 1"}, …]}` — Felder je Terminal: `address`, `agent`, `cwd`, `state`, `status` (fehlt bei reinen Shells), `turn`, `where` |
| 1.8 | Arbeitsverzeichnis-Feld | `hc ls`, `hc get t13` | `cwd` = Startordner (laut Anleitung); der aktuelle Ordner steht in `hc get` unter `foreground.cwd` |
| 1.9 | Ein Terminal im Detail | `hc get t13` | u. a. `parent: null`, `name: null`, `notify: true`, `keep: true`, `status: {app: "claude-code", state: "working", msg: …}`, `labels: {herdr.space: "sp8835…", herdr.tab: "tb94d4…", where: …}` |
| 1.10 | Zuordnung Terminal ↔ Tab/Pane | `herdr-app ls` | `spaces[].tabs[].terminals[]` mit `terminal: "t13"`, `pane: "pa7913…"`, `status`, `app`, `name`; Tab-ID `tb94d4…` und Space-ID `sp8835…` sind dieselben Werte wie die Labels `herdr.tab`/`herdr.space` in `hc get` |
| 1.11 | Claude Code wird erkannt | `hc ls` | `agent: "claude-code"` und ein `status` (`working`/`done`) für jede Claude-Session — ohne dass in dieser Session eine Integration eingerichtet wurde (Herkunft der Statusmeldung: siehe Probe 3) |
| 1.12 | Ordner des Space ≠ Projektordner | `herdr-app ls` | Space `claude-code-workflow-kit` trägt `folder: …\oma-my-new-web-page` — der Ordner eines neuen Tabs darf nie dem Vorgabewert überlassen werden, er muss ausdrücklich mitgegeben werden |
| 1.13 | Gegenprobe außerhalb der App | `echo $env:HC_TERMINAL_ID` in einem Terminal außerhalb der App | leer — vom Menschen am 2026-11-12 in einem Terminal außerhalb der App gefahren (aus dieser Session nicht fahrbar, jeder Kindprozess erbt die Variable) |

**Urteil Probe 1:** Die Adresse ist gesetzt, beide Werkzeuge sind aus beiden Shells direkt
aufrufbar, Claude Code wird samt Status erkannt. Das Adress-Schema ist die Terminal-ID (`t13`);
ein Name ist optional und bei von Hand geöffneten Tabs leer (`name: null`).

---

## Probe 2: Start, Sichtbarkeit, Zustellung

Wegwerf-Worktree `../zz-test-hc-probe` (Zweig `zz-test-hc-probe`), nach der Probe entfernt.
Test-Terminals: `t15` (Variante A), `t17` (Variante B), `t18` (zweiter Worker für Probe 3).

### Variante A — `herdr-app do tab.new`

Kommando (Git Bash, Auftrag als Variable mit echtem Zeilenumbruch):
`herdr-app do tab.new --name "zz-test-hc-probe-a" --space {space-id} --folder "{worktree}" --argv '["claude"]' --task "$T"`

| # | Punkt | Ergebnis |
|---|-------|----------|
| 2.A1 | Antwort | `{"space": "sp8835…", "tab": "tb7330…", "terminal": "t15"}`, Exit 0 |
| 2.A2 | Sichtbarer, benannter Tab | ja — `herdr-app ls` zeigt Tab `zz-test-hc-probe-a` mit `t15` |
| 2.A3 | Kind des Orchestrators | **nein** — `hc get t15` → `parent: null`, `die_with_parent: false`; `name: null` (der Tab hat den Namen, das Terminal nicht) |
| 2.A4 | Erster Auftrag kommt an | ja, aber als Programm-Argument, nicht als Nachricht: `argv = ['powershell.exe', '-NoExit', '-Command', "& 'claude' '…'"]`; `first_message: null` |
| 2.A5 | Zweizeiliger Auftrag | beide Zeilen kamen an |
| 2.A6 | Anführungszeichen im Auftrag | **gehen verloren und kürzen den Auftrag** — gesendet `… hc send t13 "PROBE-A angekommen, Zeile 2 gelesen" - danach warte …`, angekommen `… hc send t13 PROBE-A` (alles ab dem ersten Leerzeichen innerhalb der Anführungszeichen fehlt) |
| 2.A7 | Session-Ende | Claude läuft in einer PowerShell-Hülle (`-NoExit`): endet Claude, bleibt das Terminal als Shell stehen |

### Variante B — `hc run --bg` mit Fenster-Label

Kommando: `hc run --bg --json --name zz-test-hc-probe-b --cwd "{worktree}" --label herdr.space={space-id} claude "$T"`

| # | Punkt | Ergebnis |
|---|-------|----------|
| 2.B1 | Antwort | `{"address":"t17","agent":"claude","cwd":"…\\zz-test-hc-probe","name":"zz-test-hc-probe-b","parent":"t13","state":"live","turn":0}`, Exit 0 |
| 2.B2 | Kind des Orchestrators | **ja** — `parent: t13`, `die_with_parent: true`, `notify: true` |
| 2.B3 | Sichtbarer Tab | ja — durch das Label `herdr.space` legt die App von selbst einen Tab an; ohne Label bliebe der Worker unsichtbar (laut `herdr-app --skill`) |
| 2.B4 | Tab-Name | der Tab heißt zunächst nach seiner Nummer (`3`); `herdr-app do tab.rename --id {tab-id} --name zz-test-hc-probe-b` → `{"ok": true}`. Die Tab-ID steht in `herdr-app ls` beim Terminal. Der Terminal-Name (`--name`) ist sofort gesetzt und erscheint im Absender-Tag |
| 2.B5 | Erster Auftrag kommt an | ja, als Programm-Argument (`argv = ['claude', '…']`), samt Anführungszeichen unverändert |
| 2.B6 | Mehrzeiliger Auftrag als EIN Argument | **scheitert** — `spawn_failed`: `claude.CMD is a batch file: it can't take an argument with a line break`, Exit 1 (unter Windows ist `claude` eine Batch-Hülle von npm) |
| 2.B7 | `first_message.sent` | **gibt es bei diesem Startweg nicht** — `first_message: null` in Startantwort und `hc get`; das Feld gehört laut Anleitung zu Vorlagen-Starts (`hc templates`). Beleg für die Zustellung ist stattdessen `hc get` (`turn`/`status`) bzw. der Bildschirm |
| 2.B8 | Vertrauens-Dialog | trat nicht auf (Worktree neben dem Haupt-Checkout) — Verhalten bei einem Dialog **ungeprüft** |

### Senden an eine laufende Session (`hc send`)

| # | Punkt | Kommando | Ergebnis |
|---|-------|----------|----------|
| 2.S1 | Form beim Empfänger | `hc send t17 "…"` | kommt als `<hc from="t13">…</hc>` an; Antwort `{"started":true,"status":"done","turn":1}` |
| 2.S2 | Mehrzeilig | `hc send --wait t17 "$T"` (zwei Zeilen) | beide Zeilen in EINER Eingabe angekommen; `--wait` kehrt mit `wait.status: done` zurück |
| 2.S3 | Slash-Befehl aus Git Bash | `hc send t17 "/context"` | Pfad-Umschreibung greift: angekommen ist `C:/Program Files/Git/context` (L95 gilt weiter) |
| 2.S4 | Slash-Befehl ohne Umschreibung | `MSYS_NO_PATHCONV=1 hc send t17 "/context"` | Text unverändert, aber **nicht als Befehl ausgeführt** — er steckt im Tag `<hc from="t13">/context</hc>` und ist für Claude Code gewöhnlicher Text. Slash-Befehle lassen sich per `hc send` nicht auslösen |
| 2.S5 | Senden bei offenem Auswahldialog im Ziel | `hc send t17 "…"` bei `status: blocked` | abgewiesen: `{"error":{"kind":"blocked","message":"t17 is blocked (question)","hint":"typing would answer its dialog; … or --force"}}`, Exit 9 — der Dialog wird nicht beantwortet (L123 ist durch das Werkzeug abgedeckt) |
| 2.S6 | Senden in einen Entwurf | sieben Tasten per `hc keys t17 E N T W U R F`, dann `hc send` | sofort zugestellt (0 s), Entwurf und Nachricht in EINER Eingabe: `entwurf<hc from="t13">…</hc>` — Text vor dem Tag ist der Entwurf (L122 gilt in dieser Form weiter). Die Wartezeit von bis zu 60 s gilt laut Anleitung für Tasten eines Menschen; mit echtem Tippen **ungeprüft** |

**Urteil Probe 2:** Nur Variante B liefert alle drei Dinge zugleich (sichtbarer Tab, Kind des
Orchestrators, erster Auftrag) — mit zwei Zusätzen: der Tab wird danach umbenannt, und der
erste Auftrag muss einzeilig sein. Variante A fällt aus: kein Elternbezug (also keine Meldungen
von selbst) und Verlust von Anführungszeichen. Die Prüfung `first_message.sent` aus der
Befehls-Zuordnung des Plans entfällt für diesen Startweg.

---

## Probe 3: Rückmeldung ohne Hook und ohne Takt

| # | Fall | Ergebnis |
|---|------|----------|
| 3.1 | Meldet Claude Code einen Status? | ja — `hc get` zeigt `status: {app: "claude-code", state: working / done / blocked / idle, msg: …}`, bei `blocked` zusätzlich `kind: question`. In drei frisch gestarteten Sessions ohne eigenes Zutun; woher die Meldung kommt, ist nicht geklärt (in `~/.claude/settings.json` steht nur der Hook der alten CLI) |
| 3.2 | (i) Turn-Ende ohne Terminal-Ende | **keine Meldung von selbst** — über sieben Turn-Enden von `t17` kam beim Orchestrator nichts an. Sichtbar wird das Turn-Ende nur über `hc wait` oder `hc get` (`status: done`, `turn` erhöht) |
| 3.3 | (ii) Rückfrage-Dialog | Meldung von selbst: `<hc>t17 zz-test-hc-probe-b is blocked (question). See: hc read t17</hc>` |
| 3.4 | (iii) Session-Ende (Strg+C, zweimal) | Meldung von selbst: `<hc>t17 zz-test-hc-probe-b exited (exit 0). Read: hc read t17</hc>`; `hc get` → `state: finished`, `exit_code: 0` |
| 3.5 | (iv) Tab geschlossen (`herdr-app do tab.close --id … --confirmed true`) | Meldung von selbst: `<hc>t18 zz-test-hc-probe-c exited (exit 1). Read: hc read t18</hc>`; `hc get` → `state: finished`, `reason: killed` |
| 3.6 | Form der Meldungen | eigene Nachricht eines Workers: `<hc from="t17 zz-test-hc-probe-b">Text</hc>` (ohne Terminal-Namen nur `from="t15"`); Meldung des Werkzeugs selbst: `<hc>…</hc>` ohne `from`. Beide treffen als Eingabe in der laufenden Runde des Orchestrators ein |
| 3.7 | `hc wait --children any` | kehrt nach 4 s zurück: `{"children":[{"terminal":"t17","status":"done","turn":7,…}],"reason":"children"}`. `hc wait {t}` kehrt mit `reason: message` zurück, sobald das Ziel selbst eine Nachricht schickt, und mit `reason: status` beim Zustandswechsel |
| 3.8 | (v) Meldung trifft ein, während beim Orchestrator ein Auswahldialog offen ist | das Senden wird **abgewiesen**: beim Absender Exit 9, `t13 is blocked (question)`. Der Dialog wird nicht beantwortet — die Nachricht kommt aber auch nicht an und wird nicht nachgeliefert |
| 3.9 | (vi) Meldung trifft ein, während der Mensch beim Orchestrator tippt | **ungeprüft** — braucht echtes Tippen des Menschen (siehe 2.S6) |
| 3.10 | App-Fenster geschlossen | **ungeprüft** — aus der Session heraus nicht fahrbar, ohne das Fenster des Menschen zu schließen |

**Urteil Probe 3:** Rückfrage, Session-Ende und geschlossener Tab erreichen den Orchestrator
von selbst — dafür braucht es weder Stop-Hook noch Takt. Zwei Reste bleiben:

1. **Turn-Ende ohne Hand-off** wird nicht gemeldet (3.2). Der alte Stop-Hook deckte genau das
   ab. Ersatz ohne Hook: der Orchestrator hält die Runde mit `hc wait --children any` offen
   (kehrt beim Turn-Ende zurück) oder prüft auf Zuruf.
2. **Ein Hand-off, der auf einen offenen Dialog beim Orchestrator trifft, geht verloren** (3.8):
   der Worker bekommt Exit 9. Der Dialog ist damit geschützt (die Kernannahme kippt nicht),
   aber der Auftrag an den Worker braucht eine Regel für diesen Fall — Block zusätzlich in eine
   Datei schreiben und das Senden wiederholen bzw. den Fehlschlag sichtbar stehen lassen.

---

## Eigenprüfung Phase 2

**Stand:** 2026-11-12 · Gegenstand: `skills/dtb-worker/SKILL.md` auf dem Arbeitszweig
(Repo-Fassung, nicht die installierte Kopie). Jeder Bash-Block wurde aus der Skill-Datei
herausgelöst (Zeile der öffnenden Code-Marke), von der Listen-Einrückung befreit, mit
Platzhaltern gefüllt und einzeln in einer frischen Shell gefahren. Test-Arbeitsplatz:
Worktree `.dtb-worktrees/worker-zz-test-hc-eigen`, Zweig `task/zz-test-hc-eigen`, Terminals
`t1b` und `t1c` — alles wieder entfernt.

### Blöcke

| # | Block (Abschnitt) | Ergebnis |
|---|-------------------|----------|
| E1 | Gate (`### Traeger-Weiche`) | in der App `APP-OK t13`; mit geleerter Variable `APP-FEHLT` |
| E2 | Fremde Session (`#### Hinweg: Vorbedingungen`) | erste Fassung fand nichts, auch nicht in der Positivprobe — der Pfadvergleich scheiterte an doppelten Schrägstrichen (`c://users//…`). Korrigiert auf `sed 's#[\\][\\]*#/#g'`; danach: eigene Adresse `t13` → leer, als fremde Adresse `t99` → `t13` |
| E3 | Auftragsdatei schreiben (`#### Hinweg: Start-Sequenz`, Schritt 2) | `AUFTRAG-OK …/.git/worktrees/worker-zz-test-hc-eigen/dtb-auftrag.md`; mehrzeiliger Text mit Anführungszeichen unverändert in der Datei |
| E4 | Tab starten, benennen, Zustellung prüfen (Schritt 3), erste Fassung | `START-OK t1b …`, aber `TAB-NAME-FEHLT` und `ZUSTAND idle`: der Tab erschien erst kurz nach dem Start im Fenster, und die Session stand beim Abfragen noch auf `idle`. Der Bildschirm (`hc read --lines 0 t1b`) zeigte die angekommene Startzeile und eine arbeitende Session |
| E5 | derselbe Block, korrigiert (Schleife: höchstens 90 s, alle 5 s) | `START-OK t1c zz-test-hc-eigen 2026-11-12 12:53`, `TAB-OK tb1d23…`, `ZUSTAND working`, Dauer 5 s; `herdr-app ls` zeigt Tab und Terminal mit dem Namen `zz-test-hc-eigen` |
| E6 | Stand-Prüfung, Prüfpunkt 1 (`#### Rueckweg: Stand-Pruefung`) | `ADRESSE t1b`, `ZUSTAND live done`, `HANDOFF-DATEI …/dtb-handoff.md`; unbekannter Slug → `TERMINAL-WEG zz-gibt-es-nicht` |
| E7 | Tab schließen (`#### Abschluss`, Punkt 4) | `TAB-ZU tb3a48…`, `ENTFERNT t1b`; die App meldete danach von selbst `<hc>t1b zz-test-hc-eigen exited (exit 1)…</hc>` |
| E8 | Übergabe-Notiz-Block (`#### Abschluss`, vor Punkt 1) | unverändert übernommen, enthält kein Kommando von `hc`/`herdr-app` — nicht erneut gefahren |

### Ablauf am Stück (beide Läufe)

- Die Startzeile `Lies die Datei …/dtb-auftrag.md vollstaendig und fuehre den Auftrag darin aus.`
  kam an; der Worker las die Datei aus dem Git-Verwaltungsordner ohne Rückfrage (diese Sessions
  laufen im Modus „auto"; andere Berechtigungs-Modi **ungeprüft**).
- Der Worker schrieb den Block in `dtb-handoff.md` und sendete ihn mit
  `hc send t13 "$(cat '…/dtb-handoff.md')"`. Angekommen ist er vollständig, vier Zeilen, mit
  Anführungszeichen: `<hc from="t1b zz-test-hc-eigen">WORKTREE-HANDOFF (dtb) — Quelle: …</hc>`.
- Adressen können Buchstaben tragen (`t1b`, `t1c`) — kein Muster auf „t + Ziffern" verwenden.

### Kommandos im Skill gegen die Belege

| Kommando im Skill | Beleg |
|-------------------|-------|
| `command -v hc`, `command -v herdr-app`, `$HC_TERMINAL_ID` | Probe 1.1–1.4, E1 |
| `hc get "$HC_TERMINAL_ID"` → Label `herdr.space` | Probe 1.9, E4/E5 |
| `hc run --bg --json --name … --cwd … --label herdr.space=… claude "…"` | Probe 2.B1–2.B5, E4/E5 |
| `herdr-app ls` (Tab-Kennung zum Terminal) und `herdr-app do tab.rename --id … --name …` | Probe 2.B4, E5 |
| `hc ls`, `hc ls --all` (flache Einträge mit `name`, `state`, `status`) | Probe 1.7, E2, E6 |
| `hc read --lines 0 {adresse}` | Probe 2 und 3, E4 |
| `hc send {adresse} "…"`, auch mehrzeilig und aus einer Datei | Probe 2.S1, 2.S2, Ablauf oben |
| `herdr-app do tab.close --id … --confirmed true`, `hc rm {adresse}` | Probe 3.5, E7 |
| `hc get {orchestrator}` nur über den Exit-Code (0 vorhanden, 3 nicht gefunden) | gefahren am 2026-11-12: unbekannter Name → Exit 3, beendetes Terminal → Exit 0, entferntes → Exit 3 |
| `MSYS_NO_PATHCONV=1` vor Text mit führendem `/` | Probe 2.S3, 2.S4 |

**Im Skill beschrieben, aber ungeprüft** (gehen in die Abnahme, Schritt 4.1):

- Wiederholung des Hand-offs nach Exit 9 durch den Worker selbst (die Abweisung ist belegt,
  Probe 3.8; das Wiederholen und der Ausgang „Hand-off aus der Datei gelesen" nicht)
- die Zeile `WORKER-MELDUNG (dtb) — …` bei einem Aufhören ohne Hand-off
- Start-Dialog (Vertrauensfrage) und der Hinweis „Status-Erkennung fehlt auf diesem Rechner"
- alle `START-FEHLT`- und `AUFTRAG-FEHLT`-Zweige außer dem Normalfall
- der volle Auftragstext der Vorlage mit einer echten `task.md` (hier lief ein gekürzter Testauftrag)

**Unverändert:** Subagenten-Träger und Listen-Lauf — der Abschnitt ab
`### Schritt 6: Worker starten` ist gleich dem Stand vor dem Umbau (113 Zeilen auf beiden
Seiten, kein Unterschied). Zeilenzahl der Datei: 741 → 740.

## Kopplungs-Sweep

Gefahren 2026-11-12 nach Plan-Schritt 3.4, über die Endfassung der Phasen 2 und 3. Jede
Zeile: Muster, Zielzahl, Ergebnis.

| Spiegel | Muster | Zielzahl | Ergebnis |
|---|---|---|---|
| Rückweg-Zeile (Hand-off aus der Datei senden) | `hc send {orchestrator} "$(cat '{handoff-datei}')"` | 3 — Worker-Vorlage, Begrüßungstext von `pane-start`, `workflow-resume` 2a | 3 ✅ (Worker Z. 251, pane-start Z. 334, resume Z. 121) |
| Nennung der Rückweg-Zeile im Kopplungs-Hinweis des Workers und die `WORKER-MELDUNG`-Zeile | `hc send {orchestrator` | 2 weitere Treffer, beide im Worker, begründet | 2 ✅ (Z. 202 Hinweis, Z. 259 Meldung ohne Hand-off — kein Spiegel) |
| Wiederholungs-Regel bei abgewiesenem Senden | `Exit 9` | 3 Anwender-Stellen + 1 Erklärung im Worker | 4 ✅ |
| Struktur-Check-Anker 1 | `^### Pane-Ausfuehrung` im Worker | 1 | 1 ✅ |
| Struktur-Check-Anker 2 | `^### Pane-Auftrag` im Worker | 1 | 1 ✅ |
| Struktur-Check-Anker 3 | `^#### Rueckweg: Stand-Pruefung` im Worker | 1 | 1 ✅ |
| Gate-Block | `APP-OK $HC_TERMINAL_ID` | 2 — Worker `### Traeger-Weiche`, pane-start `## Herdr-Gate (hart)` | 2 ✅ |
| Warnzeile „fremde Session" | `Weitere Session im Haupt-Checkout gefunden ({adresse})` | 2 — Worker, pane-start | 2 ✅ |
| Notiz-Feld | `^Orchestrator: {` in `workflow-checkpoint` | 1 | 1 ✅ (`{terminal-id \| —}`) |
| Ausgabeformen | `^## Pane-Uebergabe` in `workflow-resume` | 3 | 3 ✅ |

Die Anker wurden zeilenende-normalisiert (`tr -d '\r'`) und am Zeilenanfang verankert
gezählt; die Worker-Datei hatte dabei 745 Zeilen (Seite gefüllt, kein Werkzeug-Fehlschlag).

**Gegenprobe zum Leser-Scan** (dieselben Muster wie in `sichtung.md`: `Ueberwachungs-Tick`,
`WORKER-STOP`, `HERDR_`, Kommando-Formen der alten CLI, dazu `claude --settings`, `/loop 15m`,
`Orchestrator-Pane`, `pane-id`) über das ganze Repo außer `dtb-project/project-changelog/`,
`archive/` und den Feature-Ordnern:

| Fundort | Treffer | Urteil |
|---|---|---|
| `skills/`, `CLAUDE.md`, `skills/CLAUDE.md`, `DERIVED_STATE_RULES.md`, `README.md` | 0 | bereinigt |
| `dtb-project/project-rules/lessons.md` | 13 Zeilen | begründet — Erfahrungswissen zur alten CLI; Urteil je Lektion steht in `sichtung.md`, die Ausmusterung läuft über `dtb:lesson-curate` |
| `dtb-project/project-workflows/INBOX-BEFUNDE.md` | 18 Zeilen | begründet — Befunde zum alten Unterbau; Urteil in `sichtung.md`, Abgang über `dtb:idea-triage` |
| `dtb-project/project-workflows/INBOX.md` | 2 Zeilen (#200, #98) | begründet — die Idee dieser Umstellung selbst und eine ältere Idee, die den alten Begriff im Text trägt |
| `dtb-project/project-dashboard.html` | 1 Zeile | begründet — erzeugte, unversionierte Seite; sie spiegelt den Text der INBOX und wird beim nächsten Checkpoint neu geschrieben |

**Über den Plan hinaus mitgezogen (Phase 3):** die Begrüßung von `pane-start` schreibt den
Hand-off wie der Worker zuerst in die Datei im Git-Verwaltungsordner; die Vorbedingung „fremde
Session im Haupt-Checkout" läuft in `pane-start` per Referenz aus dem Worker (nach dem
Struktur-Check); im Worker zwei Kopplungs-Hinweise auf diese Leser und der Satz, dass „steht
still ohne Meldung" nur für `worker-`-Arbeitsplätze gilt.

**Unverändert:** Subagenten-Träger und Listen-Lauf des Workers (Vergleich ab
`### Schritt 6: Worker starten` gegen den Stand vor dem Umbau: kein Unterschied).
Zeilenzahlen: Worker 741 → 745, pane-start 354 → 379, resume 410 → 414.

**Ungeprüft bis zur Abnahme (Plan-Phase 4):** die Start-Sequenz mit Begrüßungstext und der
abweichenden Startzeile; der Rückweg aus einem interaktiven Tab über die Hand-off-Datei;
`workflow-resume` 2a mit einer echten Übergabe-Notiz im neuen Adress-Schema.

## Abnahme 4.1: Worker-Lauf mit Pane-Träger

Geladen: skills/dtb-worker/SKILL.md (Repo-Fassung des Arbeitszweigs, Stand `c188566`; kein Slash-Befehl getippt)

Gefahren 2026-11-12, 13:47–14:05, vom Orchestrator `t13` (hc 0.1.20, herdr-app 0.1.15). Freigabe
durch den Menschen im Chat („weiter mit Phase 4"). Wegwerf-Aufgabe `zz-test-hc-worker`
(`task.md`, drei Schritte, committet als `cd638c2`).

| Punkt | Ergebnis | Beleg |
|---|---|---|
| Gate | ✅ | `APP-OK t13` |
| Vorbedingungen | ✅ | `task.md` committet; keine fremde Session im Haupt-Checkout (Block ohne Ausgabe) |
| Auftragsdatei | ✅ | `AUFTRAG-OK …/.git/worktrees/worker-zz-test-hc-worker/dtb-auftrag.md` |
| Start, eigener Tab mit dem Slug als Namen | ✅ | `START-OK t1d zz-test-hc-worker 2026-11-12 13:48`, `TAB-OK tbbb94d6…` |
| Auftrag kam an | ✅ | `ZUSTAND working`; erste Zeile in `ergebnis.md` um 13:49:10 |
| Worker committet auf `task/zz-test-hc-worker` | ✅ | `96b4874`, nicht gepusht |
| Hand-off-Block erreicht den Orchestrator von selbst | ✅ | Block im Tag `<hc from="t1d zz-test-hc-worker">` um 13:51, Kopfzeile vollständig |
| Hand-off-Datei | ✅ | `dtb-handoff.md` im Git-Verwaltungsordner, erste Zeile = Kopfzeile |
| Branch-Verifikation | ✅ grün | Commit vorhanden, `git diff --stat` = genau die zwei Dateien des Blocks, 0 uncommitted |
| Senden trifft auf einen offenen Dialog beim Orchestrator (Probe 3.8) | ✅ | eigene Testmeldung: Versuche 1–3 mit Exit 9 abgewiesen (Dialog blieb unberührt), Versuch 4 kam an — geprüft an einer `WORKER-MELDUNG`, nicht am Hand-off selbst |
| Meldung trifft ein, während der Mensch tippt (Probe 3.9) | ✅ | Eingabe kam als `abc <hc from="t1d …">…</hc>` an: der Entwurf wird VOR das Tag gehängt und mit abgeschickt; der Orchestrator wertete ihn als Entwurf, nicht als Auftrag |
| Worker arbeitet bei geschlossenem App-Fenster zu Ende (Probe 3.10) | ◐ teilweise | Orchestrator-Session, Worker-Terminal und laufender Warte-Timer überlebten das Schließen; die Zeile in der Datei entstand aber erst nach dem Wiederöffnen (14:02:55) — echte Arbeit bei geschlossenem Fenster nicht gesehen |
| Korrektur an den laufenden Worker | ✅ | fünfmal `hc send t1d "…"`, jeweils `{"started":true,…}`; der Text kam beim Worker als `<hc from="t13">…</hc>` an |
| Angebot „Tab schließen", Schließen, Entfernen | ✅ | Ein-Wort-Bestätigung des Menschen, `TAB-ZU tbbb94d6…`, `ENTFERNT t1d` |
| Ende-Meldung ohne Hook und ohne `/loop` | ✅ | `<hc>t1d zz-test-hc-worker exited (exit 1). Read: hc read t1d</hc>` traf von selbst ein, wenige Sekunden nach dem Schließen |
| Aufräumen | ✅ | Worktree und Branch `task/zz-test-hc-worker` entfernt, Ordner `features/zz-test-hc-worker/` per `git rm` gelöscht |

**Befunde:**

1. **Wartezeit im Hintergrund = Turn-Ende ohne Meldung.** Die Umgebung blockt ein alleinstehendes
   `sleep` im Vordergrund; der Worker ließ es im Hintergrund laufen, beendete seinen Zug und
   wurde nach Ablauf von selbst fortgesetzt. In dieser Zeit stand er auf `done`, mit `1 shell`
   in der Fußzeile, ohne Meldung an den Orchestrator. Folge: `done` ohne Hand-off heißt nicht
   „hat aufgehört". Nachgearbeitet: die Stand-Prüfung im Worker liest vor der Warnung „steht
   still" den Bildschirm und meldet bei laufender Hintergrund-Shell stattdessen
   „wartet auf eigenen Hintergrund-Befehl".
2. **„höchstens dreimal" war zweideutig.** Der Worker las es als drei Wiederholungen nach dem
   ersten Versuch (vier Versuche). Nachgearbeitet: Wortlaut an allen drei Stellen
   (Worker-Vorlage, Begrüßung von `pane-start`, `workflow-resume` 2a) auf „höchstens drei
   Wiederholungen, also vier Versuche insgesamt".
3. **`hc send` an einen Worker auf `done` startet sofort eine neue Runde** (`"started":true`) —
   der Weg „Korrektur senden" trägt auch nach dem Hand-off.
4. **Der Mensch braucht je Test genau eine Anweisung.** Der erste Versuch, drei Handgriffe in
   einem Dialog zu bündeln, scheiterte; einzeln liefen alle Tests.

Beleg der Nacharbeit (Befunde 1 und 2): Sie liegt im Checkpoint-Commit `860f493`, nicht im
Phasen-Commit `851b4b9`. Der Hinweis zum Hintergrund-Befehl (Befund 1) ist nach dem Einbau in
keinem Abnahme-Lauf erneut gefahren; die Wiederholungs-Regel (Befund 2) lief in „Abnahme 4.2".

**Ungeprüft geblieben:** Hand-off (statt Testmeldung) trifft auf einen offenen Dialog und wird
aus der Datei gelesen (Ausgang (f)); Arbeit des Workers während das Fenster wirklich
geschlossen ist; Vertrauens-Dialog beim Start (der Ordner war schon vertraut); `TAB-NAME-FEHLT`,
`START-FEHLT`, `HC-FEHLT`. — Die ersten beiden Punkte sind in „Abnahme 4.2" nachgeholt.

## Abnahme 4.2: `pane-start` und Session-Wechsel

Geladen: skills/dtb-pane-start/SKILL.md (Repo-Fassung des Arbeitszweigs, Struktur-Check gegen skills/dtb-worker/SKILL.md im Projekt-Root; kein Slash-Befehl getippt)
Geladen: {worktree}/skills/dtb-workflow-checkpoint/SKILL.md und {worktree}/skills/dtb-workflow-resume/SKILL.md (im Tab, per Satz statt Slash-Befehl)

Gefahren 2026-11-12, 14:18–15:10, vom Orchestrator `t13` (hc 0.1.20, herdr-app 0.1.15). Freigabe
durch den Menschen im Chat („weiter"). Wegwerf-Change `zz-test-hc-pane` (nur `discovery.md`,
committet als `01d92a3`), Worktree `.dtb-worktrees/pane-zz-test-hc-pane` auf
`feature/zz-test-hc-pane`.

| Punkt | Ergebnis | Beleg |
|---|---|---|
| Guard, Gate | ✅ | `HAUPT-CHECKOUT`, `APP-OK t13` |
| Vorbedingungen 1–3 | ✅ | Change-Ordner committet, Branch frei, Worktree-Pfad frei |
| Struktur-Check | ✅ | 3/3 Anker (`^### Pane-Ausfuehrung`, `^### Pane-Auftrag`, `^#### Rueckweg: Stand-Pruefung`) je 1 Treffer |
| Vorbedingung 4 (fremde Session, per Referenz aus dem Worker) | ✅ | keine Ausgabe; Positivprobe ohne Ausschluss fand `t13` (L130) |
| Begrüßungsdatei | ✅ | `AUFTRAG-OK …/.git/worktrees/pane-zz-test-hc-pane/dtb-auftrag.md` |
| Eigener Tab, Claude gestartet | ✅ | `START-OK t1f zz-test-hc-pane 2026-11-12 14:18`, `TAB-OK tb849bf2…`, `ZUSTAND working`; `hc ls`: `"parent":"t13"` |
| Begrüßung zugestellt, Session wartet | ✅ | Bildschirm 14:18: Begrüßung mit Arbeitsplatz, Vorschlag `/dtb:feature-plan zz-test-hc-pane`, Orchestrator `t13`, „Ich führe den Befehl nicht selbst aus"; 0 Änderungen im Worktree |
| Arbeit im Tab | ✅ | auf Eingabe des Menschen `ergebnis.md` angelegt und als `0aab604` committet |
| Checkpoint „Wechsel" | ✅ | Notiz `dtb-session-uebergabe.md` mit `## Wechsel 2026-11-12 14:24`, `Orchestrator: t13`; nichts an den Orchestrator gesendet |
| `/clear` | ✅ | Terminal blieb `live` (`idle`), keine Ende-Meldung beim Orchestrator |
| `workflow-resume` findet die Notiz und prüft die Adresse | ✅ | Bericht: `Orchestrator: t13 (erreichbar)`, Rückweg-Zeile `hc send t13 "$(cat '…/dtb-handoff.md')"`, eigener Change als Item, `herdr-app-umstellung` nur als Zeile „Weitere aktive Features im Repo" |
| Checkpoint „Ende" liefert EINEN Block | ✅ | Notiz-Marker `## Ende-Block erzeugt 2026-11-12 14:32`; Hand-off-Datei, Kopfzeile `WORKTREE-HANDOFF (dtb) — Quelle: zz-test-hc-pane @ feature/zz-test-hc-pane, 2026-11-12 14:32`, „Wechsel" und „Ende" kumuliert |
| Hand-off trifft auf einen offenen Dialog (Rest aus 4.1) | ✅ | Orchestrator hielt eine Auswahlfrage 3 min offen: vier Versuche mit Exit 9 („t13 is blocked (question)"), danach Stopp ohne `--force`, Meldung an den Menschen im Tab; Stand-Prüfung meldete `HANDOFF-DATEI`, der Orchestrator las den Block aus der Datei (Ausgang (f)). Später sendete die Session auf „senden" des Menschen erneut — Exit 0, Inhalt gleich der Datei, kein zweiter Block übernommen |
| Arbeit bei geschlossenem App-Fenster (Rest aus 4.1) | ✅ | `zeit2.txt`: 8 Zeitstempel 15:05:46–15:09:18; Protokoll des Orchestrators: `herdr-app status` scheitert ab 15:06:17 (Fenster zu), `t1f` dabei durchgehend `working` — 7 Zeilen entstanden bei geschlossenem Fenster; die Fertig-Meldung des Tabs kam beim Orchestrator an, während das Fenster noch zu war |
| Branch-Stand | ✅ | `+1 Commits` vor dem Arbeitszweig, `git diff --stat` = genau `ergebnis.md`, 0 uncommitted (vor dem Fenster-Test) |

**Befunde:**

1. **Getippter Slash-Befehl lädt die alte Kopie.** Der Mensch tippte im Tab `/dtb-workflow-checkpoint`
   — geladen wurde `~/.claude/`, wie die Lade-Regel vorhersagt. Der Aufruf wurde vor der Weiche
   verworfen und mit der Repo-Fassung wiederholt. Inhaltlich weicht die alte Kopie bei
   „Wechsel" nur im Wortlaut ab (Diff installiert ↔ Repo). Gilt bis zum `kit-sync` nach dem Merge.
2. **`herdr-app status` zeigt, ob das Fenster offen ist.** Ein erster Fenster-Test scheiterte,
   weil „das Fenster" nicht eindeutig war (der Mensch fragte „welches Fenster"); erst „das ganze
   Fenster der Herdr-App, X oben rechts" wurde verstanden. Der Befehl scheitert bei geschlossenem
   Fenster und eignet sich als Beleg (`herdr-app ls` dagegen nennt kein Fenster-Feld).
3. **Exit 9 gilt auch für die eigene Auswahlfrage des Orchestrators** (`blocked (question)`), nicht
   nur für Berechtigungs-Dialoge.

**Ungeprüft geblieben:** Vertrauens-Dialog beim Start (Ordner schon vertraut); `TAB-NAME-FEHLT`,
`START-FEHLT`.

## Abnahme 4.3: Gate außerhalb der App und Aufräumen

Geladen: skills/dtb-pane-start/SKILL.md, skills/dtb-worker/SKILL.md, skills/dtb-workflow-resume/SKILL.md (Repo-Fassung, in einer Claude-Session in Windows Terminal/PowerShell außerhalb der Herdr-App; Gate-Blöcke per Satz statt Slash-Befehl)

Gefahren 2026-11-12, 15:15–15:25. Die Session außerhalb der App hatte `$HC_TERMINAL_ID` leer,
`hc` und `herdr-app` lagen aber im PATH — das Gate hängt also wirklich an der eigenen
Terminal-Adresse, nicht an den Werkzeugen.

| Punkt | Ergebnis | Beleg |
|---|---|---|
| `dtb:pane-start` bricht hart ab und nennt den Weg in die App | ✅ | `APP-FEHLT`, ⛔-Meldung mit „die Herdr-App oeffnen …" und dem Befehl `/dtb:pane-start zz-test-hc-pane` zum erneuten Absetzen |
| Pane-Träger von `dtb:worker` bricht hart ab, keine stille Degradierung | ✅ | `APP-FEHLT`, ⛔-Meldung „Pane-Modus braucht die Herdr-App …", Subagent nur als genannte Alternative |
| `workflow-resume` 2a läuft außerhalb der App still weiter | ✅ | `APP-AUS`, `hc get` nicht aufgerufen, keine Warnzeile, `Orchestrator: t13 (ungeprueft)`, Rückweg-Zeile trotzdem gebaut |
| Gegenfälle in der App | ✅ | `APP-OK t13` (4.1, 4.2), `(erreichbar)` (4.2); `NICHT-ERREICHBAR` nur in der Probe (Phase 1) |
| Tab geschlossen und entfernt (Angebot nach der Abnahme, ein Wort) | ✅ | Bestätigung „ja", `TAB-ZU tb849bf2…`, `STATE finished`, `ENTFERNT t1f` |
| `git worktree list` zeigt nur den Haupt-Checkout | ✅ | eine Zeile (`feature/herdr-app-umstellung`) |
| kein `zz-test-`-Ordner, kein `task/zz-test-*`/`feature/zz-test-*`-Branch | ✅ | Zählung je 0; `feature/zz-test-hc-pane` mit `-D` gelöscht (war `0aab604`, Wegwerf), Ordner per `git rm` |

Nicht angefasst: `.dtb-worktrees/pane-sdd-geschichte-blog` (fremder Ordner, in `git worktree list`
dieses Repos nicht verlinkt).

→ Nach Merge und Push: /dtb:kit-sync sync (erst pushen, dann syncen — L39); bis dahin laufen unter ~/.claude/ die alten Skills
