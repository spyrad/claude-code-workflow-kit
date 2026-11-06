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

— folgt in Phase 3 —
