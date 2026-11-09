# Discovery: Worker-Job-Ende-Meldung
<!-- resume: done -->

**Erstellt:** 2026-11-06
**Idee-Referenz:** Inbox #175 — "`dtb:worker` Pane-Modus: Job-Ende-Meldung in Code statt im Worker-Modell"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-worker/SKILL.md | Pane-Auftrag, Start-Sequenz (`claude --settings`), „Warten ohne Warten" (neuer Ausgang), Ueberwachungs-Tick (neuer Anker), Branch-Verifikation; einziger Ort fuer Herdr-Kommandos |
| skills/dtb-worker/scripts/ | NEU: Stop-Hook-Skript (PowerShell) |
| skills/dtb-pane-start/SKILL.md | Liest die Start-Sequenz des Workers zur Laufzeit — muss die `--settings`-Ergaenzung bewusst NICHT uebernehmen; Struktur-Check auf Worker-Anker |
| skills/dtb-workflow-checkpoint/SKILL.md | Nur Lesequelle: `### Hand-off-Block` (Format), Uebergabe-Notiz im Git-Verwaltungsordner (Vorbild fuer den Ablageort) |
| skills/dtb-kit-sync/SKILL.md | Neue Artefakt-Klasse `skills/dtb-*/scripts/*` (Verteilung + Drift-Check) |
| skills/CLAUDE.md | Kanon: Herdr-Drift-Regel, Parallele Sessions; ggf. Regel „Code im Kit" |
| CLAUDE.md | Distribution-Model (neue Klasse) und Kategorie-Beschreibung von `worker` |

---

## Anforderungen

### Scope
**Enthalten:**
- Nur Kandidat (A) aus #175: Stop-Hook meldet das Turn-Ende der Worker-Session an die Orchestrator-Pane
- Nur Worker-Pane-Traeger (`dtb:worker`, Traeger `pane`). Grund: der Worker arbeitet seinen Auftrag im Kern in einem langen Turn ab — das erste `Stop` heisst praktisch „fertig" oder „haengt an einer Rueckfrage"
- Der Hook schickt EINE Signalzeile mit eigenem Anker, nur Fakten aus git und `task.md`:
  `WORKER-STOP (dtb) — {slug} @ task/{slug}: +{n} Commits · {k} uncommitted · Schritte X/Y · Hand-off gesendet: ja|nein`
  „Hand-off gesendet" liest der Hook aus dem Transcript der Worker-Session (der Block geht im Turn raus, also vor dem `Stop`)
- Registrierung nur fuer die Worker-Session: Start-Sequenz ruft `claude --settings {datei}`; die Settings-Datei liegt im Git-Verwaltungsordner des Worktrees (wie die Uebergabe-Notiz) — keine Aenderung an `~/.claude/settings.json`, kein Konflikt mit bestehenden globalen Stop-Hooks, verschwindet mit dem Worktree
- Hook-Skript als eigene Datei unter `skills/dtb-worker/scripts/`; `dtb:kit-sync` lernt die Klasse `skills/dtb-*/scripts/*`

**Nicht enthalten:**
- `dtb:pane-start`-Panes (Mensch arbeitet dort; `Stop` feuert nach jeder Antwort → Dauermeldungen; Rueckweg laeuft dort ueber Checkpoint „Ende")
- Ersatz des WORKTREE-HANDOFF-Blocks — der Block bleibt der Inhalt, die Hook-Zeile ist nur das Signal (ein Skript kann „Erledigt"/„Offene Punkte" nicht formulieren)
- Eingriff durch den Hook: kein `decision: block`, kein Stopp, kein Merge, kein Schreiben in den Arbeitsbaum
- Erkennen eines Absturzes/Abbruchs der Session (feuert keinen Hook) — bleibt Aufgabe des Ueberwachungs-Ticks
- Kandidat (B) Tick-Pruefliste als Skript → als eigene neue Idee ausgliedern (via Hand-off)
- Kandidat (C) „Korrektur senden" per `herdr agent prompt` → als eigene neue Idee ausgliedern (via Hand-off); braucht vorab eine Probe, ob Eingaben waehrend eines laufenden Turns ankommen

### Gewuenschtes Verhalten
- Orchestrator empfaengt `WORKER-STOP (dtb)` als neuen Ausgang in `#### Rueckweg: Warten ohne Warten`:
  - `Hand-off gesendet: ja` → Block ist schon da, Branch-Verifikation laeuft wie bisher; zur Signalzeile nur eine kurze Bestaetigungszeile, keine Rueckfrage
  - `Hand-off gesendet: nein` → Orchestrator liest die Pane einmal (`herdr pane read`) und meldet „Worker hat aufgehoert ohne Hand-off — wartet er auf eine Antwort oder hat er den Block vergessen?"; der Mensch entscheidet ueber Nachfassen, nichts wird automatisch geschickt
- Ueberwachungs-Tick wertet die Signalzeile in Pruefpunkt 3 (Hand-off) als zusaetzliches Signal:
  - `ja` → nichts Neues (der Hand-off beendet die Beobachtung schon heute)
  - `nein` → eine Zeile einmal „gestoppt ohne Hand-off"; die Pane bleibt beobachtet (nach Nachfassen arbeitet der Worker weiter)
- Bestehende UX-Muster: Kopfzeilen-Anker wie `WORKTREE-HANDOFF (dtb) — …`; Tick-Meldungsform (eine Zeile je Pane, nur bei Aenderung)

### Randfaelle
- Zustellung scheitert (Orchestrator-Pane weg, `herdr`-Fehler): 2 Versuche, dann eine Logzeile im Git-Verwaltungsordner (Erfolg wie Fehlschlag); der Hook endet IMMER mit Exit 0 — die Worker-Session sieht nie einen Hook-Fehler. Netz bleibt der Ueberwachungs-Tick
- Mehrfacher Stopp (Nachfassen → Worker arbeitet weiter → stoppt erneut): jeder Stopp schickt eine neue Signalzeile mit aktuellem Stand; kein Gedaechtnis, keine Merkdatei (die zweite Meldung „jetzt mit Block" ist die wichtige)
- Wert nicht lesbar (`task.md` fehlt, git-Fehler, Transcript fehlt): trotzdem melden, betroffenes Feld = `?` — die Meldung „gestoppt" kommt immer an
- Zustellbeleg: Exit-Code von `herdr agent prompt` reicht (keine Turn-Beobachtung wie Limen — Hook-Zeitlimit). Probe im Plan: Verhalten, wenn der Orchestrator gerade selbst mitten in einem Turn steckt

### Einschraenkungen
- Sprache: PowerShell, lauffaehig mit Windows PowerShell 5.1 (wie die bestehenden Hooks; JSON ohne Zusatzwerkzeug). macOS/Linux nicht im Scope. Bash verworfen: braucht `jq`, dazu MSYS-Pfadumwandlung bei fuehrendem `/` (Lektion L95)
- Herdr-Drift-Regel: das Skript wird dritte, ausdruecklich benannte Ausnahme neben den zwei bestehenden (Rueckweg-Zeile in `dtb:pane-start`, Schritt 2a in `dtb:workflow-resume`) — Verweis in beide Richtungen zwischen `### Pane-Auftrag`/`### Pane-Ausfuehrung` und dem Skript
- Laufzeit: Hook-Timeout 15 s; 2 Zustellversuche mit 2 s Pause, Normalfall < 5 s. Globale Stop-Hooks (z.B. Sprachausgabe) laufen unabhaengig weiter — Probe im Plan
- Schreibgrenze: der Hook schreibt nur seine Logzeile in den Git-Verwaltungsordner des Worktrees, nie in den Arbeitsbaum oder zentrale Dateien

### Integrationspunkte
- Orchestrator-Adresse und Slug stehen als Parameter im Hook-Befehl der Settings-Datei, die der Orchestrator beim Start schreibt (Adresse aus `$HERDR_PANE_ID`) — das Skript raet nichts, keine Team-Registry
- `dtb:worker` Start-Sequenz: Settings-Datei in den Git-Verwaltungsordner schreiben, `herdr pane run {pane-id} "claude --settings {datei}"`
- `dtb:pane-start` liest die Start-Sequenz zur Laufzeit: neue benannte Abweichung „`--settings` und Hook-Datei nicht uebernehmen, nur `claude` starten" + Gegen-Hinweis in `dtb:worker`
- `dtb:kit-sync`: neue Artefakt-Klasse `skills/dtb-*/scripts/*` → `~/.claude/skills/dtb-*/scripts/*` (synced, Drift-Check)
- Externe Abhaengigkeiten: Herdr-CLI (`herdr agent prompt`), Claude-Code-Hook-Schnittstelle (`Stop`-Payload mit `transcript_path`/`cwd`; `--settings`-Flag)

---

## Abhaengigkeiten

- Bestehende Change-Ordner: `checkpoint-ohne-rueckfragen`, `checkpoint-schneller` — beide aendern nur `dtb:workflow-checkpoint`, das hier nur Lesequelle ist → keine Konflikte
- INBOX #182 (Autonome Kette „Full Stop") nennt #175 als Vorstufe — dieser Change liefert ihr den Baustein „Ende-Meldung in Code"
- Nach dem Merge: Klasse-A-Nachlauf (Commit → Push → `/dtb:kit-sync sync`), jetzt inkl. Skriptdatei

---

## Offene Punkte

- Greifen Hooks aus `claude --settings {datei}`? Erste Probe im Plan; scheitert sie → Rueckfall auf globale Registrierung mit Selbstpruefung im Skript (HERDR_ENV + Worktree-Name `worker-*`)
- Laufen globale Stop-Hooks (Sprachausgabe) und der `--settings`-Hook unabhaengig nebeneinander? Probe im Plan
- Was passiert mit `herdr agent prompt`, wenn die Orchestrator-Session gerade mitten in einem Turn steckt (Warteschlange, Verlust, Einschub)? Probe im Plan
- Fuer den Hand-off (INBOX gehoert dieser Session nicht): zwei neue Ideen aus #175 erfassen lassen — (B) Ueberwachungs-Tick-Pruefliste als Skript statt Modellaufruf; (C) „Korrektur senden" per `herdr agent prompt` dokumentieren, vorab Probe, ob Eingaben waehrend eines laufenden Turns ankommen

---

**Erstellt mit:** `/dtb:feature-discover`
