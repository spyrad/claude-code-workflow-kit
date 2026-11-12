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
