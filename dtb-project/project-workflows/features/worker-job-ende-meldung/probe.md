# Proben: Worker-Job-Ende-Meldung

**Datum:** 2026-11-06
**Umgebung:** Claude Code 2.1.318, Windows 10, Herdr 0.9.0-preview.2026-09-08; Orchestrator = Pane `w3:pR`
**Ablage der Wegwerf-Dateien:** Scratchpad `probe1/` (Settings, Mini-Hooks, Logs) — nicht versioniert

---

## Probe 1: Registrierung

**Frage:** Feuert ein Stop-Hook aus `claude --settings {datei}`, und in welcher Shell laeuft der Hook-Befehl?

| Lauf | Start | Ergebnis |
|------|-------|----------|
| 1a | `claude -p … --settings settings.json` aus dem Bash-Tool | feuert; Befehl lief in **Windows PowerShell 5.1** (`$0` leer, `%COMSPEC%` unexpandiert, `>>` schrieb UTF-16) |
| 1b | wie 1a, PowerShell-Befehl mit `[Console]::In.ReadToEnd()` | feuert; Payload-Felder: `session_id`, `transcript_path`, `cwd`, `prompt_id`, `permission_mode`, `effort`, `hook_event_name: Stop`, `stop_hook_active`, `last_assistant_message`, `background_tasks`, `session_crons` |
| 1c | interaktiv in frischer Herdr-Pane (`herdr pane run {pane} "claude --settings …"`) | feuert, aber Befehl lief in **Git Bash** (`/usr/bin/bash: -c: … syntax error near unexpected token`) — derselbe PowerShell-Befehl scheitert dort |
| 1d | Befehl `powershell -NoProfile -ExecutionPolicy Bypass -File "{pfad}/hook.ps1"`, `-p` und interaktiv | feuert in beiden Modi, Skript laeuft jeweils unter PS 5.1, Payload kommt an (627 bzw. 762 Zeichen), keine Fehlermeldung in der Pane |

`/hooks` listet Hooks aus `--settings` NICHT (zeigte nur `[User]`/`[Plugin]`) — trotzdem feuern sie.
Die Shell fuer Hook-Befehle wechselt je nach Startweg; nur ein shell-neutraler Befehl
(`powershell -File "{skript}"` — keine Variablen, keine Operatoren im Befehl) laeuft ueberall.

**Ergebnis:** Registrierung pro Session per `--settings` funktioniert. Hook-Befehl = Aufruf eines
`.ps1` per `powershell -NoProfile -ExecutionPolicy Bypass -File "{pfad}"`.

---

## Probe 2: Nebeneinander

**Frage:** Laufen globale Stop-Hooks und der `--settings`-Hook nebeneinander?

- Session mit `--settings` zeigte waehrend des Turn-Endes `running Stop hooks… 1/3` — drei Stop-Hooks:
  `[User]` (Sprachausgabe, `~/.claude/settings.json`), `[Plugin]` (codex) und der `--settings`-Hook
- `/hooks` in derselben Session listet den `[User]`-Stop-Hook weiterhin
- Die Sprachausgabe selbst war abgeschaltet (`~/.claude/tts-off`) und schrieb deshalb keine Logzeile

**Ergebnis:** Zusammenfuehrung, keine Ersetzung — der Worker-Hook laeuft zusaetzlich.

---

## Probe 3: Zustellung

**Frage:** Was passiert mit `herdr agent prompt`, wenn die Ziel-Session (a) mitten im Turn steckt,
(b) in ihrer Eingabezeile schon Text steht?

| Fall | Beobachtung |
|------|-------------|
| (a) Turn laeuft (lange Textgenerierung, Status `working`) | Zustellung Exit 0; Text landet in der Warteschlange von Claude Code („Press up to edit queued messages"), wird nach dem Turn als eigene Eingabe verarbeitet — kein Verlust, kein Einschub |
| (b) Eingabezeile enthaelt `halb getippte Frage des Menschen` | Zustellung haengt den Text an und schickt ab: `halb getippte Frage des MenschenWORKER-STOP (dtb) — mensch-tippt` — der Entwurf des Menschen geht vorzeitig mit raus |
| Adresse existiert nicht (`w3:zz`) | `herdr agent prompt` Exit 1 |

**Ergebnis:** (a) unkritisch. (b) ist eine bekannte Grenze von `herdr agent prompt` — sie gilt heute
schon fuer den Hand-off-Block, den das Worker-Modell auf demselben Weg schickt. Folge fuer den Plan:
den Anker `WORKER-STOP (dtb) — {slug}` irgendwo in der Eingabe erkennen (nicht nur am Zeilenanfang)
und einen Vorspann als Entwurf des Menschen zurueckzeigen. Exit ≠ 0 bei falscher Adresse → das
Skript muss den Exit-Code abfangen (Hook-Exit immer 0).

---

## Probe 4: Zeichen

**Frage:** Kommt `—` aus PowerShell 5.1 ueber `herdr agent prompt` unverfaelscht an?

- Testskript (ASCII-Quelltext, Gedankenstrich per `[char]0x2014`) → Pane zeigte
  `WORKER-STOP (dtb) — zeichen-probe` korrekt

**Ergebnis:** Unicode bleibt (gleicher Stil wie `WORKTREE-HANDOFF (dtb) — …`).

---

## Abnahme

**Aufbau (2026-11-06 15:21):** Orchestrator = diese Pane `w3:pR`, Wegwerf-Worker = Pane `w3:pV`
(per `herdr pane split` neu angelegt, cwd = dieser Arbeitsplatz). Signal-Einrichtung woertlich aus
der Repo-Fassung (`#### Hinweg: Start-Sequenz`) mit `{slug}` = `worker-job-ende-meldung`,
`{orchestrator-pane}` = `w3:pR` → `HOOK-OK …/.git/worktrees/pane-worker-job-ende-meldung/dtb-worker-hook.json`;
Start per `herdr pane run w3:pV "claude --settings '…'"`, Erkennung `idle` nach < 90 s.
Ausgangsstand `git status --porcelain`: 3 Zeilen (plan.md, discovery.md, spec.md).
Hash `~/.claude/settings.json` vorher: `f7a5b663…3a51369`.

### 3.1 Wirklauf ohne und mit Hand-off

**Lauf 1 — ohne Hand-off.** Auftrag: „nichts schreiben, genau ein Satz, KEINEN Hand-off-Block".
Worker antwortete `Auftrag gelesen, ich warte.` (done 15:21). In dieser Pane kam als eigene Eingabe an:

```
WORKER-STOP (dtb) — worker-job-ende-meldung
```

Reaktion nach Ausgang (d): kein `WORKTREE-HANDOFF (dtb) — Quelle: worker-job-ende-meldung` in dieser
Session → Stand selbst gelesen (Kommandos wie Tick-Pruefpunkt 2), einmal `herdr pane read w3:pV`
(Hinweis: Default-Quelle zeigte nur den leeren Eingabebereich, erst `--source recent --lines 80`
lieferte die Antwort), Meldung:

```
⚠ worker-job-ende-meldung: Worker hat aufgehoert ohne Hand-off — wartet er auf eine Antwort oder hat er den Block vergessen?
   Stand: +2 Commits · 3 uncommitted · Progress 7/10
   Letzte Antwort: „Auftrag gelesen, ich warte." (done 15:21)
   → du entscheidest: antworten · Block anfordern · liegen lassen
```

**Lauf 2 — Nachfassen mit Block („Block anfordern").** Auftrag an `w3:pV`: genau einen Bash-Befehl
`herdr agent prompt w3:pR "WORKTREE-HANDOFF (dtb) — Quelle: worker-job-ende-meldung (Test) …"`.
Reihenfolge der Eingaben in dieser Pane — erst der Block, dann das Signal (Block geht im Turn raus,
Signal erst beim Turn-Ende):

```
WORKTREE-HANDOFF (dtb) — Quelle: worker-job-ende-meldung (Test)
Erledigt:
- Abnahme-Probe 3.1, nichts geschrieben
```
```
WORKER-STOP (dtb) — worker-job-ende-meldung
```

Reaktion nach Ausgang (d), Block da:

```
✅ worker-job-ende-meldung: Turn beendet, Hand-off liegt vor · +2 Commits · 4 uncommitted · Progress 7/10
```

(4 uncommitted = Ausgangsstand + diese `probe.md`.) Mehrfach-Stopp belegt: jeder Turn-Ende schickt
ein eigenes Signal, beide wurden je einmal ausgewertet. Nebenbefund: der Worker bemerkte von selbst,
dass die Orchestrator-Pane im selben Worktree arbeitet, und bat um Pruefung — im Wirklauf (eigener
`worker-{slug}`-Worktree) tritt das nicht auf.

### 3.2 Randfaelle im Wirklauf

| Fall | Vorgehen | Beobachtung |
|------|----------|-------------|
| Orchestrator weg | Signal-Einrichtung woertlich mit `{orchestrator-pane}` = `w3:zz` (existiert nicht) → `HOOK-OK`; Skript ueberschrieben, laufende Session `w3:pV` liest es beim naechsten Stop neu; Auftrag „ein Satz" | Worker antwortete `Turn ohne Orchestrator.` (done 15:23), Status `done`, **keine Hook-Fehlermeldung** in der Pane, hier kam nichts an; danach Einrichtung erneut mit `w3:pR` (fuer 3.3) |
| Ungueltiger Slug (Fehlerweg) | Einrichtung mit `{slug}` = `Ungueltig_Slug` | `HOOK-FEHLT ungueltiger Slug`, vorhandene Dateien unberuehrt (Abbruch vor dem Schreiben); Warnzeile laut Skill: `⚠ Signal-Hook fuer Ungueltig_Slug nicht eingerichtet (ungueltiger Slug) — Worker startet ohne Ende-Signal, Netz ist der Ueberwachungs-Tick`; Start dann ohne `--settings` (naechste Zeile) |
| pane-start ohne Hook | zweite Wegwerf-Pane `w3:pW`, Start nur `claude` (= Startbefehl von `dtb:pane-start` und Fehlerweg); Auftrag „ein Satz" | Antwort `Turn ohne Hook.` (done 15:24); 20 s Nachlauf — **keine Signalzeile** hier |
| Globale Einstellungen | `sha256sum ~/.claude/settings.json` vor 3.1 und nach 3.2 | beide `f7a5b663…3a51369` — unveraendert |

### 3.3 Tick-Probe

**Anpassung am Ablauf:** Die Lage „Signal ohne Block" aus 3.1 (Lauf 1) war durch den Test-Block aus
Lauf 2 ueberholt — ein Tick haette die Pane wegen „Hand-off eingetroffen" beendet. Deshalb: Tick-
Fenster beginnt nach 3.2 mit einer Ausgangszeile, danach ein neuer Worker-Turn ohne Block, dann die
zwei Laeufe aus dem Plan. Pruefliste woertlich aus der Repo-Fassung (`#### Rueckweg: Ueberwachungs-Tick`),
Schleifen-Form (Meldungsregel „nur bei Aenderung"), von Hand ausgefuehrt.

Schritt 0 fand den Worktree `pane-worker-job-ende-meldung` und ZWEI Panes mit passendem `cwd`
(`w3:pR` = diese Orchestrator-Pane, `w3:pV` = Worker) — Artefakt der Simulation (Orchestrator im
selben Worktree); beobachtet wurde `w3:pV`. Im Betrieb sitzt der Orchestrator im Haupt-Checkout.

| Tick | Lage | Ausgabe |
|------|------|---------|
| 1 (Ausgang) | nach 3.2, kein Signal seit Fenster-Beginn | `🔭 worker-job-ende-meldung (w3:pV): done · +2 Commits, zuletzt 2026-11-06 · 4 uncommitted · Progress 9/10` |
| — | Worker-Turn „ein Satz, KEIN Hand-off-Block" → hier eingetroffen: `WORKER-STOP (dtb) — worker-job-ende-meldung` | — |
| 2 | Signal seit Tick 1, kein Hand-off seit Tick 1 (Pruefpunkt 3) | `🔭 worker-job-ende-meldung (w3:pV): done · ⚠ gestoppt ohne Hand-off · +2 Commits, zuletzt 2026-11-06 · 4 uncommitted · Progress 9/10` |
| 3 | keine Aenderung, kein neues Signal | keine Zeile |

`gestoppt ohne Hand-off` erscheint genau einmal; die Pane blieb beobachtet.

**Aufraeumen:** `herdr pane close w3:pW` (nach 3.2) und `herdr pane close w3:pV`; `herdr pane list`
zeigt keine der beiden mehr. `dtb-worker-hook.ps1`/`.json` aus
`.git/worktrees/pane-worker-job-ende-meldung/` entfernt (0 Treffer danach).
