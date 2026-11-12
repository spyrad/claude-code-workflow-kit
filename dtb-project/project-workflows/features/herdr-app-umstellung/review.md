# Review-Snapshot: herdr-app-umstellung
Scope: 4 Skills (worker, pane-start, workflow-resume, workflow-checkpoint), CLAUDE.md, skills/CLAUDE.md, DERIVED_STATE_RULES.md §10, probe.md/sichtung.md/spec.md · Geprueft bis: `851b4b9` (plus Nacharbeit in `860f493`) · Datum: 2026-11-12
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-worker/SKILL.md:604-609 (und :482) — Der Schliess-Block findet das Terminal allein ueber den Namen (`"name":"$N"` + `tail -1`). Der Name ist nicht eindeutig (Slug auf 32 Zeichen gekuerzt, `pane-{slug}` und `worker-{slug}` gleich benannt, `hc ls --all` mit beendeten Alt-Eintraegen, von Hand gleich benannter Tab). Danach folgen `tab.close --confirmed true` und `hc rm` — die Invariante „nur selbst gestartete Terminals" ist nicht durchgesetzt.
Fix: Im Schliess-Block zusaetzlich auf den Elternbezug filtern (`grep "\"parent\":\"$HC_TERMINAL_ID\""`, Feld belegt in probe.md Abnahme 4.2); bei leerem Ergebnis `TAB-OFFEN (kein von dieser Session gestartetes Terminal — von Hand schliessen)`.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-workflow-resume/SKILL.md:102-103 und :112 — Der Text nennt fuer `hc get` „11 = beendet" und verspricht fuer einen beendeten Orchestrator `NICHT-ERREICHBAR`. Belegt ist (probe.md, Eigenpruefung): beendetes Terminal → Exit 0, nur entferntes → Exit 3. Ein beendeter Orchestrator erscheint also als `(erreichbar)`. Die „11" stammt aus der ungeprueften Plan-Tabelle.
Fix: Z. 102-103 auf „(0 = bekannt — auch ein beendetes Terminal —, 3 = nicht gefunden)"; in Z. 112 „oder beendet" durch „und entfernt" ersetzen; ein Satz: „Exit 0 belegt nur, dass die App das Terminal kennt, nicht dass dort eine Session laeuft."
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:253-256, skills/dtb-pane-start/SKILL.md:336-339, skills/dtb-workflow-resume/SKILL.md:122 — Die Wiederholungs-Regel deckt nur Exit 9. Jeder andere Fehlschlag von `hc send` (Orchestrator entfernt oder beendet) hat keine Anweisung.
Fix: An allen drei Stellen gleich ergaenzen: „Jeder andere Fehler (nicht Exit 9): NICHT wiederholen — aufhoeren; die Datei bleibt liegen." In pane-start und resume zusaetzlich „und dem Menschen sagen".
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:580-584 — Der Abschluss-Zweig `ERZEUGT` kennt nur „Block eingetroffen" oder „im Tab erneut senden"; der neue Ausgang (f) (Hand-off-Datei lesen, Z. 440-444) ist dort nicht nachgezogen.
Fix: Vor dem „Sonst" einfuegen: „… oder die Hand-off-Datei liegt vor (Pruefpunkt 1 der Stand-Pruefung meldet `HANDOFF-DATEI`) → Ausgang (f), ohne Warnung."
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-worker/SKILL.md:433-439 gegen :597-610 — Schliesst der Orchestrator den Tab selbst (Abschluss Punkt 4), meldet die App `exited`; das loest Ausgang (e) mit git-Abfragen aus, waehrend Worktree und Branch gerade entfernt werden. Der selbst verursachte Fall ist nicht deklariert.
Fix: In (e) als ersten Unterpunkt: „**Selbst geschlossen** (Abschluss Punkt 4 lief in dieser Session fuer `{slug}`) → erwartete Meldung, keine Ausgabe, keine git-Abfrage."
Decision: FIXED

### F6 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-worker/SKILL.md:339-346 — Der volle Pane-Auftrag wird per Heredoc geschrieben (lang, Unicode, Backticks, gemischte Anfuehrungszeichen) — Klasse aus Lektion L38 („Lange Inhalte nie inline per Heredoc"). Lief in der Eigenpruefung und in Abnahme 4.1 durch.
Fix: Schritt 2 teilen: (a) Bash-Block ermittelt nur `{G}`, (b) Auftragstext mit dem Write-Werkzeug nach `{G}/dtb-auftrag.md`, (c) die Pruefzeile `AUFTRAG-OK` bleibt als eigener Block.
Decision: SKIPPED — der Fix braeuchte `Write` in `allowed-tools` von Worker und pane-start (bei pane-start gegen „schreibt keine Artefakte"); der Heredoc-Weg lief in Eigenpruefung und Abnahme 4.1 durch, Endmarke am Zeilenanfang (L94)

### F7 — Plan Adherence — [S:Niedrig × I:Mittel]
Commit `860f493` (docs(session)) — Die Nacharbeit aus Abnahme 4.1 (Wiederholungs-Regel an drei Stellen, Hintergrund-Befehl in der Stand-Pruefung) aendert drei Skills in einem Checkpoint-Commit; der Beleg `851b4b9` in `## Progress` enthaelt sie nicht. Planerische Grundlage vorhanden (Phase 4, „nacharbeiten"), kein Scope-Creep. Der Satz zum Hintergrund-Befehl lief nach dem Einbau in keinem Abnahme-Lauf.
Fix: In probe.md unter „Abnahme 4.1 → Befunde" eine Zeile: „Nacharbeit liegt in `860f493` (Checkpoint-Commit), nicht in `851b4b9`; Hintergrund-Befehl-Hinweis nach dem Einbau nicht erneut gefahren."
Decision: FIXED

### F8 — Plan Adherence — [S:Niedrig × I:Mittel]
dtb-project/project-workflows/features/herdr-app-umstellung/spec.md:121-124 — Zwei Fragen stehen noch als „Noch ungeprueft, in die Abnahme verlegt", sind aber in probe.md 4.1/4.2 beantwortet (Meldung waehrend des Tippens; Arbeit bei geschlossenem Fenster).
Fix: Den Absatz durch zwei Ergebniszeilen mit Verweis auf probe.md 4.1/4.2 ersetzen.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:262 — Der Notiz-Kopf sagt „Block an den Orchestrator senden" ohne „erst in die Hand-off-Datei"; alle anderen Stellen nennen die Datei zuerst. Der Kopf ueberlebt als einziger Text das `/clear`.
Fix: „…; den WORKTREE-HANDOFF-Block woertlich und vollstaendig inkl. Kopfzeile erst in die Hand-off-Datei schreiben, dann an den Orchestrator senden".
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:348 — „Den Pfad `{G}` vorher mit derselben ersten Zeile ermitteln": Die erste Zeile des Blocks ist `W="…"`, die Aufloesung steht in Zeile 2 und braucht `$W`. Woertlich ausgefuehrt bleibt der Pfad leer.
Fix: „… mit den ersten beiden Zeilen dieses Blocks plus `echo "$G"` ermitteln".
Decision: FIXED

## Unterhalb des Caps (5, nicht triagiert)
- worker :475-476 gegen :359 — „nie `hc get` per Regex" widerspricht der Start-Sequenz (Label `herdr.space`)
- worker :277-278 — Kopplungs-Hinweis zaehlt drei Abweichungen von pane-start, dort stehen vier (Startzeile fehlt)
- worker :469-473 — Stand-Pruefung nimmt auch detached Subagenten-Worktrees (Altbestand)
- pane-start :286-288, worker :459-460 — Geschichts-Satz „entfallen 2026-11-12" in Laufzeit-Prosa
- plan.md Schritt 2.4 — Plan nennt Ausgaenge a–e, der Worker-Text hat a–f (inhaltlich deckungsgleich)
