# Discovery: Herdr-App-Umstellung
<!-- resume: done -->

**Erstellt:** 2026-11-12
**Idee-Referenz:** Inbox #200 — "Kit auf die Herdr-App umstellen (`herdr-app` + `hc`/herdr-core statt `herdr`-CLI)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-worker/SKILL.md | Pane-Träger komplett (42 Treffer): Traeger-Weiche, Pane-Auftrag, Pane-Ausfuehrung, Rueckweg „Warten ohne Warten" + Ueberwachungs-Tick, Stop-Hook |
| skills/dtb-pane-start/SKILL.md | Herdr-Gate (hart), Herdr-Mechanik per Referenz auf den Worker, Begrüßung per `herdr agent prompt` (19 Treffer) |
| skills/dtb-workflow-resume/SKILL.md | Schritt 2a Pane-Uebergabe: Orchestrator-Adresse per `herdr agent get` (8 Treffer) |
| skills/dtb-workflow-checkpoint/SKILL.md | Worktree-Hand-off: Transport des Hand-off-Blocks (1 Treffer) |
| skills/CLAUDE.md | Orchestrator-Muster: Pane-Worker, Transport „Herdr-Session-Kommunikation" (2 Treffer) |
| CLAUDE.md | Kit-Beschreibung worker/pane-start/resume mit Herdr-Bezug (2 Treffer) |
| dtb-project/project-rules/lessons.md | 11 Herdr-Lektionen (u. a. 69, 87, 95, 119–124, 127) auf Gültigkeit für `hc` prüfen |
| dtb-project/project-workflows/INBOX-BEFUNDE.md | 12 Herdr-Befunde: erledigt oder verändert durch die Umstellung? |

---

## Anforderungen

### Scope
**Enthalten:**
- Alle Herdr-Stellen in `dtb:worker` (Pane-Träger), `dtb:pane-start` und `dtb:workflow-resume` (Schritt 2a) laufen über `hc` (herdr-core) bzw. `herdr-app`; die alte `herdr`-CLI fällt komplett weg
- Hand-off-Transport (`dtb:workflow-checkpoint`) und Kit-Doku (`skills/CLAUDE.md`, `CLAUDE.md`) nachziehen
- Herdr-Lektionen in `lessons.md` auf Gültigkeit für `hc` prüfen
- **Stop-Hook und Ueberwachungs-Tick direkt mit umbauen:** ersetzen durch die eingebaute Rückmeldung von `hc` (blocked/error/exit an den Auftraggeber) und `hc wait --children` — Entscheidung 2026-11-12

**Nicht enthalten:**
- Parallelbetrieb beider Systeme (`herdr`-CLI und App)
- Neue `hc`-Fähigkeiten nutzen, die das Kit heute nicht hat (andere Rechner, Vorlagen/Templates)
- Subagenten-Träger von `dtb:worker` (nutzt kein Herdr)

### Gewuenschtes Verhalten
- **Sichtbare Tabs:** jeder Worker und jeder `pane-start`-Arbeitsplatz erscheint als eigener Tab in der Herdr-App, benannt nach dem Slug (`herdr-app do tab.new …`) — kein unsichtbares `hc`-Terminal; Entscheidung 2026-11-12 (wie heute die sichtbaren Panes, Eingreifen per Klick)
- **Rückmeldung von selbst:** Worker-Meldungen kommen als Nachricht in die Orchestrator-Session, ohne `/loop`-Abfrage
- **Bleibt gleich:** Begrüßungstext mit Wartepflicht (`pane-start`), Hand-off-Block, Übergabe-Notiz mit `/clear` + `workflow-resume`, Freigabe und Abnahme durch den Menschen

### Randfaelle
- **Session läuft nicht in der App** (`HC_TERMINAL_ID` fehlt): harter Abbruch mit Hinweis, wie die Session in der App gestartet wird — wie das heutige Herdr-Gate
- **Erster Auftrag kommt nicht an** (`first_message.sent: false`, z. B. Vertrauens-Dialog beim Claude-Start): erst den Bildschirm lesen (`hc read`), nie blind erneut senden (laut `hc --skill`)
- **Worker wartet auf Rückfrage** (Status `blocked`): der Orchestrator meldet es dem Menschen und antwortet nie selbst; kein `hc send --force`
- **Mensch tippt gerade im Ziel-Tab:** `hc` hält die Nachricht zurück (Draft-Wartezeit, max. 60 s) — löst vermutlich die Lektionen zu Zustellung-beim-Tippen ab (ungeprüft)
- **App-Fenster wird geschlossen:** Terminals laufen weiter (herdr-core hält sie), Worker arbeiten zu Ende

### Einschraenkungen
- **Windows zuerst:** muss auf dem Windows-Rechner des Menschen laufen (Git Bash + PowerShell); andere Systeme werden nicht eigens geprüft
- **Probe vor dem Umbau (Pflicht):** ein kurzer Test in der App belegt drei Punkte, bevor ein Skill umgebaut wird — (1) `HC_TERMINAL_ID` ist in App-Terminals gesetzt, (2) eine `hc send`-Nachricht kommt in einer Claude-Session an, (3) `hc` meldet das Ende eines Workers von selbst an den Auftraggeber
- **Versionsstand:** `hc` 0.1.20 ist jung, Befehle können sich ändern — der Plan nennt die geprüfte Version
- **Kit-Regeln bleiben:** Startsequenz nur einmal im Worker (`pane-start` per Referenz, nie Kopie); Worker pushen nie; Autonomie nur zwischen Freigabe und Abnahme
- **Kern nicht anfassen:** das Kit führt nie `hc server stop`/`restart` aus (träfe alle Terminals des Menschen)

### Integrationspunkte
- **Im Kit:** die vier Skills der Scan-Liste plus ihre Querverweise — `pane-start` prüft per Struktur-Check feste Abschnitts-Anker im Worker (u. a. Tick-Anker); umbenannte oder entfallende Abschnitte → Checks mitziehen
- **Verteilung:** nach dem Umbau bringt `dtb:kit-sync` die neuen Skills nach `~/.claude/`; bis dahin laufen dort die alten
- **Nach außen:** `hc` (herdr-core) und `herdr-app` müssen installiert und im PATH sein — ob beide in einem App-Terminal direkt aufrufbar sind, klärt die Probe
- **Alte `herdr`-CLI:** wird vom Kit nicht mehr genutzt; Deinstallation entscheidet der Mensch, kein Teil des Features
- **Claude-Integration:** die alte CLI brauchte `herdr integration install claude` für die Status-Erkennung; ob die App Vergleichbares braucht, ist offen → Probe

---

## Abhaengigkeiten

- **Überschneidung (kein Konflikt):** `checkpoint-schneller` und `checkpoint-ohne-rueckfragen` (beide „Fertig zum Testen") ändern ebenfalls `skills/dtb-workflow-checkpoint/SKILL.md` — dieses Feature berührt dort nur die Transport-Zeile im Worktree-Hand-off
- **Nachfolger:** INBOX #98 (Autopilot für die Voll-Schiene) und #182 (autonome Kette bis vor den Merge) bauen auf der Pane-Mechanik auf — erst nach diesem Feature planen

---

## Offene Punkte

- Probe (siehe Einschränkungen): Ist `HC_TERMINAL_ID` in App-Terminals gesetzt? Kommt `hc send` in einer Claude-Session an? Meldet `hc` das Worker-Ende von selbst?
- Sind `hc` und `herdr-app` in einem App-Terminal direkt aufrufbar (PATH)?
- Braucht die App eine Claude-Integration für die Status-Erkennung (Gegenstück zu `herdr integration install claude`)?
- Welche der 11 Herdr-Lektionen in `lessons.md` gelten für `hc` weiter, welche werden ausgemustert (`dtb:lesson-curate`)?
- Welche der 12 Herdr-Befunde in `INBOX-BEFUNDE.md` erledigt die Umstellung?
- Ersetzt die eingebaute `hc`-Rückmeldung den Stop-Hook vollständig, oder bleibt ein Rest (z. B. Turn-Ende ohne Terminal-Ende)?

---

**Erstellt mit:** `/dtb:feature-discover`
