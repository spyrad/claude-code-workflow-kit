# Review-Snapshot: worker-job-ende-meldung
Scope: CLAUDE.md, skills/dtb-worker/SKILL.md, skills/dtb-pane-start/SKILL.md, features/worker-job-ende-meldung/probe.md · Geprueft bis: `d80ab5d` · Datum: 2026-11-06
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-worker/SKILL.md:297 — `herdr agent prompt` tippt Text + Enter; ungeprueft, ob das Signal bei offenem Auswahldialog des Orchestrators die erste Option (Vorschlag, ggf. Commit) bestaetigt. Der Hook loest bei jedem Turn-Ende aus, ohne Modell dazwischen.
Fix: Probe (Dialog in Wegwerf-Pane + `herdr agent prompt`); trifft es zu, im ps1 vor dem Senden `herdr agent get` pruefen — bei `blocked` innerhalb der 15 s erneut versuchen, sonst Signal fallen lassen (Tick ist das Netz).
Decision: FIXED — Probe 5 bestaetigt (Dialog als Freitext beantwortet; Herdr meldet `done`, nicht `blocked` → Status-Check untauglich). Umgesetzt: Dialog-Check per `herdr pane read --source visible --lines 4` auf `Esc to cancel`, bis 10 s warten, sonst fallen lassen; belegt 5c/5d.

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-worker/SKILL.md:306, 311-313 — JSON mit Skriptpfad per printf ohne Parse-Pruefung; Begruendung „Slug/Adresse geprueft → JSON sicher" passt nicht (im JSON steht nur der Pfad). Ungewoehnlicher Pfad oder fehlendes `powershell` → trotzdem `HOOK-OK`.
Fix: Parse-Lauf (`powershell … ConvertFrom-Json`) vor `HOOK-OK`, Fehlschlag = `HOOK-FEHLT JSON ungueltig` (deckt fehlendes powershell mit ab); Satz 311-313 richtigstellen.
Decision: FIXED — Parse-Lauf vor `HOOK-OK` (`HOOK-FEHLT Settings ungueltig oder kein powershell`), Satz richtiggestellt; gueltig → HOOK-OK, kaputtes JSON → HOOK-FEHLT (geprueft 2026-11-06).

### F3 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:297-311 — Hinweis „Endmarke ohne Einrueckung" steht nach dem Block; eingerueckt kopierte Endmarke → keine Statuszeile, Zustand unbehandelt. `dtb-workflow-checkpoint` loest das mit Hinweis vor dem Block + „Keine Statuszeile zaehlt wie Fehler".
Fix: Muster uebernehmen — Hinweis vor den Block, Regel „Keine Statuszeile zaehlt wie `HOOK-FEHLT`".
Decision: FIXED — Hinweis vor den Block gezogen, Regel „Keine Statuszeile zaehlt wie `HOOK-FEHLT keine Statuszeile`" ergaenzt, Nachsatz entfernt.

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:329, 356, 374, 454 — `herdr pane read` ohne Optionen zeigte in der Abnahme nur den leeren Eingabebereich (probe.md 3.1); „Letzte Antwort" in Ausgang (d) bliebe leer.
Fix: an den vier Kommando-Stellen `herdr pane read {pane-id} --source recent --lines 80`.
Decision: FIXED — vier Kommando-Stellen ergaenzt (Start-Abbruch, Ausgang (b), Ausgang (d), Tick `blocked`); `recent --lines 40/80` zeigte in Probe 5 auch einen offenen Dialog.

### F5 — Plan Adherence — [S:Niedrig × I:Mittel]
plan.md:18-24, 99, 193 — Plantext sagt „Einzeiler, keine Skriptdatei, keine Pfade im JSON"; umgesetzt ist die Skript-Variante (Entscheidung Hook-Shell, Zeile 191).
Fix: die drei Stellen auf die Skript-Variante ziehen (zusammen mit dem spec.md-Nachzug).
Decision: FIXED — Absatz „Schlanke Variante", Output 2.1 und Entscheidungszeilen Hook-Umfang/Settings-Datei auf die Skript-Variante gezogen.

### F6 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:326-328 — zweiter `pane run` bei nicht erkannter, aber laufender Session → Startbefehl wird Prompt → Signal vor dem Auftrag → (d) meldet faelschlich „aufgehoert ohne Hand-off".
Fix: in (d) festhalten: Signal vor Zustellung von Kommando 4 mit einer Hinweiszeile ignorieren.
Decision: FIXED — Unterpunkt „Signal vor dem Auftrag" in Ausgang (d), Zeile `↷ {slug}: Signal vor dem Auftrag — ignoriert`.

### F7 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-worker/SKILL.md:293 — Platzhalter `O="{orchestrator-pane}"` laesst einen Wert abschreiben, der als `$HERDR_PANE_ID` vorliegt.
Fix: `O="$HERDR_PANE_ID"`.
Decision: FIXED — `O="$HERDR_PANE_ID"`, Platzhalterliste auf `{worktree-pfad}`/`{slug}` gekuerzt.

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-worker/SKILL.md:236-237 — Kopplungs-Hinweis nennt 3 der 4 Abweichungen von pane-start (Worktree-Pfad fehlt).
Fix: „Worktree-Pfad `pane-{slug}`" ergaenzen.
Decision: FIXED — Kopplungs-Hinweis nennt vier Abweichungen inkl. Worktree-Pfad `pane-{slug}` und den Ort `## Herdr-Mechanik`.

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-worker/SKILL.md:453, 498-499 — offen, ob „⚠ gestoppt ohne Hand-off" in spaeteren Tick-Zeilen wieder erscheint.
Fix: Satz ergaenzen — Markierung nur in der Tick-Zeile, die das Signal erkannt hat, kein Zustandsfeld.
Decision: FIXED — Tick-Tabelle: Markierung nur in der erkennenden Tick-Zeile, kein Zustand.

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig]
probe.md:33-38 — Mitlaufen des globalen Stop-Hooks nur indirekt belegt (Zaehler „1/3", Sprachausgabe aus).
Fix: in probe.md als indirekten Beleg kennzeichnen.
Decision: FIXED — probe.md Probe 2: Beleg-Staerke „indirekt" plus stuetzender Vergleich aus Probe 5 (1/2 ohne --settings).
