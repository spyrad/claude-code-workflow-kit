# Feature: Worker-Job-Ende-Meldung

**Erstellt:** 2026-11-06
**Ziel:** Stoppt eine Worker-Pane-Session, erfaehrt der Orchestrator das immer — auch wenn das Worker-Modell den Hand-off-Block vergisst.
**Prioritaet:** Hoch
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

> **Nachgezogen 2026-11-06** auf den gebauten Stand (schlanke Variante aus dem plan-review, Probe-
> Ergebnisse, impl-review-Fixes). Die urspruengliche Fassung (Signalzeile mit Fakten, Transcript-
> Auswertung, Logzeile, kit-sync-Klasse) steht im Git-Verlauf dieser Datei; die Abweichungen sind in
> `plan.md` (Absatz „Schlanke Variante", `## Technische Entscheidungen`) begruendet.

---

## Executive Summary

Im Pane-Traeger von `dtb:worker` haengt die Rueckmeldung bisher allein am Worker-Modell: Es muss den
WORKTREE-HANDOFF-Block am Ende selbst an den Orchestrator schicken. Vergisst es das, kommt keine
Meldung, und erst der optionale Ueberwachungs-Tick sieht spaeter etwas — die einzige Stelle, an der
Arbeit still verloren gehen kann. Ein Stop-Hook in der Worker-Session meldet jetzt jedes Turn-Ende
als reines Signal `WORKER-STOP (dtb) — {slug}`; die Fakten (Commits, uncommitted, Fortschritt) und
den Abgleich „ist der Block eingetroffen?" macht der Orchestrator selbst (Vorbild: Limens
`coordinator-wake`, MEGA.dev s01e04).

---

## Scope / Abgrenzung

### Enthalten
- **Signal beim Turn-Ende** der Worker-Session an die Orchestrator-Pane, mit eigenem Anker und ohne
  Fakten: `WORKER-STOP (dtb) — {slug}`
- **Nur der Pane-Traeger von `dtb:worker`** — der Worker arbeitet seinen Auftrag im Kern in einem
  langen Turn ab, das erste Turn-Ende heisst praktisch „fertig" oder „haengt an einer Rueckfrage"
- **Registrierung nur fuer die Worker-Session:** `claude --settings {datei}`; Settings-Datei und
  Hook-Skript `dtb-worker-hook.ps1` liegen im Git-Verwaltungsordner des Worktrees, globale
  Einstellungen bleiben unberuehrt, beides verschwindet mit dem Worktree
- **Hook-Skript:** shell-neutral aufgerufen (`powershell -NoProfile -ExecutionPolicy Bypass -File`),
  weil Claude Code Hook-Befehle je nach Startweg in PowerShell oder Git Bash ausfuehrt; zwei
  Zustellversuche mit 2 s Pause, endet immer mit Exit 0, Zeitlimit 15 s
- **Dialog-Schutz:** vor dem Senden liest das Skript die sichtbare Fusszeile der Orchestrator-Pane;
  steht dort ein offener Auswahldialog (`Esc to cancel`), wartet es bis zu 10 s und laesst das Signal
  sonst fallen — `herdr agent prompt` wuerde den Dialog sonst als Freitext beantworten
- **Einrichtung mit Pruefung:** Slug und Orchestrator-Adresse werden vor dem Einsetzen geprueft, die
  Settings-Datei per Parse-Lauf; jedes Scheitern → genau eine Warnzeile, Start ohne `--settings`
  (Fehlerweg), der Tick bleibt das Netz
- **Orchestrator-Seite:** Ausgang (d) in `#### Rueckweg: Warten ohne Warten` — Stand selbst lesen;
  Block da → eine Bestaetigungszeile; Block fehlt → Pane einmal lesen und melden („wartet er auf eine
  Antwort oder hat er den Block vergessen?"), der Mensch entscheidet, nichts wird automatisch
  gesendet; Signal vor dem Auftrag → ignorieren; Anker irgendwo in der Eingabe erkennen
- **Ueberwachungs-Tick** wertet das Signal als zusaetzliches Signal: ohne Hand-off einmal
  „gestoppt ohne Hand-off", die Pane bleibt beobachtet
- **Kanon-Pflege:** Herdr-Kommandos bleiben in `### Pane-Ausfuehrung` (keine neue Ausnahme);
  benannte Abweichung in `dtb:pane-start` („nur `claude` starten, keine Signal-Einrichtung")

### Nicht enthalten
- Panes von `dtb:pane-start` (dort arbeitet ein Mensch, ein Turn-Ende-Hook meldete nach jeder
  Antwort; der Rueckweg laeuft dort ueber Checkpoint „Ende")
- Ersatz des WORKTREE-HANDOFF-Blocks — er bleibt der Inhalt, das Signal ist nur der Anstoss
- Fakten in der Signalzeile, Transcript-Auswertung, Logzeile, eigene kit-sync-Artefakt-Klasse
  (plan-review: der Orchestrator liest den Stand ohnehin selbst)
- Eingriff durch den Hook: kein Zwingen zum Senden, kein Stopp, kein Merge, kein Schreiben in den
  Arbeitsbaum
- Erkennen eines Absturzes oder Abbruchs der Session (loest keinen Hook aus) — bleibt beim Tick
- Schutz vor Berechtigungsdialogen beim Orchestrator (im Auto-Modus nicht pruefbar)
- macOS/Linux
- Tick-Pruefliste als Skript und „Korrektur senden" — als eigene neue Ideen ausgegliedert (via Hand-off)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Hooks aus `--settings` greifen nicht | — | Hoch | entkraeftet: Probe 1 (feuert interaktiv und im Print-Modus) |
| Hook-Shell wechselt je Startweg | eingetreten | Hoch | Skript-Aufruf per `powershell -File` ohne Variablen/Operatoren (Probe 1) |
| Signal an einen Orchestrator mitten im Turn | — | Mittel | entkraeftet: wird gepuffert und nach dem Turn verarbeitet (Probe 3a) |
| Signal beantwortet einen offenen Dialog beim Orchestrator | eingetreten | Hoch | Dialog-Schutz im Skript (Probe 5) |
| Halb getippte Eingabe beim Orchestrator geht mit raus | Mittel | Niedrig | Anker irgendwo erkennen, Vorspann als Entwurf zurueckzeigen (Probe 3b) |
| Settings-Datei ungueltig, `HOOK-OK` falsch | Niedrig | Hoch | Parse-Lauf vor `HOOK-OK` |
| Hook haelt die Worker-Session auf | Niedrig | Niedrig | Zeitlimit 15 s; Normalfall 1 s, mit Dialog bis ~11 s |
| Globale Stop-Hooks kollidieren | — | Niedrig | entkraeftet: laufen nebeneinander (Probe 2) |

---

## Dependencies

### Erforderlich vor Start
- [x] Probe: greift ein Stop-Hook aus `claude --settings {datei}` (Claude Code 2.1.318, Windows)? — ja, Probe 1
- [x] Herdr-CLI mit `herdr agent prompt` verfuegbar (Stand: 0.9.0-preview.2026-09-08)

### Referenz-Dokumente
- `dtb-project/project-workflows/features/worker-job-ende-meldung/discovery.md` - Discovery mit allen 16 Entscheidungen
- `dtb-project/project-workflows/features/worker-job-ende-meldung/probe.md` - Proben 1-5 und Abnahme
- `dtb-project/project-workflows/features/worker-job-ende-meldung/review.md` - impl-review mit 10 behobenen Findings
- `skills/dtb-worker/SKILL.md` - Pane-Auftrag, Pane-Ausfuehrung, Ueberwachungs-Tick, Branch-Verifikation
- `skills/dtb-pane-start/SKILL.md` - liest die Worker-Start-Sequenz zur Laufzeit (benannte Abweichungen)
- `skills/dtb-workflow-checkpoint/SKILL.md` - `### Hand-off-Block` (Format, nur Lesequelle)
- `../mega.dev/lessons/s01e04/s01e04-try-today.md` - Limen-Vergleich, Vorbild `coordinator-wake`
- `dtb-project/project-rules/lessons.md` - L95 (Pfadumwandlung in Git Bash), L87 (Herdr-Ausgabe parsen), L79 (Tick-Kosten)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [x] Ein Pane-Worker, der aufhoert OHNE den Hand-off-Block zu senden, erzeugt beim Orchestrator binnen Sekunden das Signal `WORKER-STOP (dtb) — {slug}`; der Orchestrator meldet mit selbst gelesenem Stand (Commits, uncommitted, Fortschritt) — probe.md Abnahme 3.1 Lauf 1
- [x] Ein Pane-Worker, der den Block sendet, erzeugt danach ein Signal, auf das der Orchestrator nur mit einer Bestaetigungszeile reagiert — 3.1 Lauf 2
- [x] Nach einem Nachfassen und erneutem Stopp kommt ein neues Signal und wird erneut ausgewertet — 3.1 Lauf 2
- [x] Ist die Orchestrator-Adresse tot, laeuft die Worker-Session ohne Hook-Fehlermeldung weiter — 3.2
- [x] Scheitert die Einrichtung (z.B. ungueltiger Slug), erscheint genau eine Warnzeile und der Worker startet ohne `--settings` — 3.2
- [x] In einer Pane ohne Hook (Startbefehl von `dtb:pane-start`) entsteht kein Signal — 3.2
- [x] `~/.claude/settings.json` ist nach einem Worker-Lauf unveraendert — 3.2 (Hash vorher/nachher)
- [x] Der Orchestrator reagiert auf ein Signal ohne Block mit genau einer Meldung und schickt nichts automatisch an den Worker — 3.1 Lauf 1
- [x] Der Ueberwachungs-Tick meldet `gestoppt ohne Hand-off` genau einmal und beobachtet die Pane weiter — 3.3
- [x] Ein offener Auswahldialog beim Orchestrator wird vom Signal nicht beantwortet — Probe 5 (5c/5d)

---

## Offene Punkte

- Greift ein Stop-Hook aus `claude --settings {datei}`? → beantwortet: ja (Probe 1)
- Laufen globale Stop-Hooks und der Worker-Hook unabhaengig nebeneinander? → beantwortet: ja, Beleg indirekt (Probe 2)
- Was passiert mit `herdr agent prompt`, wenn die Orchestrator-Session gerade mitten in einem Turn steckt? → beantwortet: Warteschlange, kein Verlust (Probe 3a)
- Kommen Gedankenstrich und Mittelpunkt ueber PowerShell 5.1 → `herdr` unverfaelscht an? → beantwortet: ja (Probe 4)
- Fuer den Hand-off (INBOX gehoert dieser Session nicht): zwei neue Ideen erfassen lassen — Tick-Pruefliste als Skript; „Korrektur senden" dokumentieren → im WORKTREE-HANDOFF vom 2026-11-06 16:30 an den Orchestrator uebergeben

---

**Erstellt mit:** `/dtb:feature-plan` · nachgezogen 2026-11-06 nach Umsetzung und impl-review
