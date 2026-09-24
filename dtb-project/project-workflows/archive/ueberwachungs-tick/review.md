# Review-Snapshot: ueberwachungs-tick
Scope: skills/dtb-worker/SKILL.md, skills/dtb-pane-start/SKILL.md, CLAUDE.md, DERIVED_STATE_RULES.md (+3 Workflow-Artefakte) · Geprueft bis: `3918193` · Datum: 2026-09-24
Gesamt-Verdikt: REJECTED (1 blocking)

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-worker/SKILL.md:351+393 — Ausgang "Hand-off eingetroffen" schickt beide Traeger in die Branch-Verifikation (hart task/{slug}, Merge-Angebot); bei pane-start ist der Hand-off nur Session-Ende (Rueckweg = /dtb:workflow-checkpoint, Merge ausdruecklich nicht dort, pane-start:333-337).
Fix: Ausgangszeile + Ende-Meldung (2) nach Traeger splitten — worker → Branch-Verifikation, pane-start → nur /dtb:workflow-checkpoint.
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:278-280, :321-322 — Warteschlange erzeugt Panes nacheinander; feste Pane-Liste im Loop-Befehl veraltet, Selbstende greift vor Ende der Warteschlange.
Fix: (Empfehlung) Panes je Tick ableiten (herdr agent list, cwd unter .dtb-worktrees/(worker|pane)-*, Branch/Pfad aus git worktree list) — oder kleiner: je neue Pane ein neues Angebot, das den alten Loop ersetzt.
Decision: FIXED (Panes je Tick abgeleitet — Schritt 0 der Pruefliste; Selbstende beachtet offene Warteschlange; Angebot ohne Pane-Liste, entfaellt bei laufendem Tick; CLAUDE.md nachgezogen)

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:376 + pane-start:263-265 — Loop-Befehl ohne {slug}/{worktree-pfad}/Quellpfad; feature/{slug} als Muster statt tatsaechlich angelegtem Branch (1c.2).
Fix: Loop-Zeile mit allen vier Parametern (Ist-Werte aus der Start-Sequenz) + Pfad ~/.claude/skills/dtb-worker/SKILL.md.
Decision: FIXED (durch F2 — Quellpfad in der Loop-Zeile, Parameter ermittelt der Tick selbst, pane-start nennt den tatsaechlich angelegten Branch)

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-pane-start/SKILL.md:202-212 — Anker-Grep ohne Zeilenanfang; neuer Anker 6x in worker (5x Prosa/Vorlage) → Struktur-Check meldet nach Umbenennung falsch 3/3.
Fix: Anker-Grep fuer alle drei Anker zeilenanfang-verankert vorschreiben (nach CR-Normalisierung).
Decision: FIXED (je Anker genau 1 Treffer belegt)

### F5 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:341-345, :386-397 — Vergleichsbasis unvollstaendig: (1b) ohne Stand-Felder, Erst-Tick-Form offen, Commit-Feld in (1) ohne Pfeil.
Fix: Jede Tick-Zeile traegt alle Felder, nur geaenderte als alt → neu; Erst-Tick = Form (1) ohne Pfeile.
Decision: FIXED (Meldungsregel + Formen (1)/(1b); Stand-Feld jetzt "+{n} Commits, zuletzt …")

### F6 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-worker/SKILL.md:295 — "(naechster Abschnitt)" zeigt seit dem Einschub auf den Tick.
Fix: Titel #### Rueckweg: Branch-Verifikation nennen.
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:353, :327 — blocked: Tick verweist nur auf pane read, (b)/(c) lesen; done ohne Ausgang.
Fix: bei blocked Pane einmal lesen + Auszug; unknown-Zeile auf done/unknown erweitern.
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:357-360 — Selbstende ohne Mechanismus und ohne Lauf-Ende-Vorlage.
Fix: Meldungsform (4) "Lauf-Ende" — Claude Code: geplanten Loop-Job loeschen (belegt: CronDelete im Wirklauf 2026-09-24); sonst nichts zu tun.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:330-336 vs. DSR §10.2 — Spiegel ohne Stage-Rueckfall, Stand-Format abweichend.
Fix: Stage-Rueckfall + Stand-Format "+{n} Commits, zuletzt YYYY-MM-DD" woertlich aus §10.2.
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-worker/SKILL.md:290-292 — Startzeit fuer max_minutes "aus dem Verlauf" unsicher (keine Zeitstempel, Komprimierung).
Fix: Startzeit bei Zustellung per date ermitteln, in der Loop-Zeile mitgeben.
Decision: FIXED (Startzeit per date in der Angebots-Kopfzeile, die immer erscheint)

4 weitere Findings unterhalb des Caps (2x EXTRA begruendet: consumes features/*/plan.md, Zeitfeld-Einschub; nit: consumes DERIVED_STATE_RULES.md entgegen "autark"; nit: pane-start:234 "beiden Sektionen" → drei) — erneut ausfuehren nach Behebung.
