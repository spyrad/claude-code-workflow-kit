# Implementierungsplan: Ueberwachungs-Tick

**Erstellt:** 2026-09-24
**Feature-Spec:** `features/ueberwachungs-tick/spec.md`
**Geschaetzte Dauer:** ~3 h (Phase 1 ~1,5 h, Phase 2 ~1,5 h; der Wirklauf 2.3 erstreckt sich ueber die Pane-Laufzeit)
**Status:** Reviewed (plan-review 2026-09-24: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Tick bauen: Beispiel-Meldung, Quelle in dtb:worker, Angebot + Struktur-Check in dtb:pane-start | ~1,5 h | Geplant |
| Phase 2 | Anbindung Worker-Traeger, Doku, Konsistenz-Sweep, Wirklauf | ~1,5 h | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-worker/SKILL.md` | Herdr-Kommando-Regel: Kommandos nur in `### Pane-Auftrag` und `### Pane-Ausfuehrung` (Z. 180-186). `#### Rueckweg: Warten ohne Warten` (Z. 279-294): anlassbezogen per `herdr agent get`, Ausgaenge (a) Hand-off, (b) `blocked`, (c) `max_minutes` ohne Auto-Stopp. Start-Sequenz endet mit "KEIN blockierendes Warten" (Z. 276-277). `consumes` ohne DSR (Z. 22); `allowed-tools` mit Bash (Z. 17) |
| `skills/dtb-pane-start/SKILL.md` | Struktur-Check mit 2 Ankern `### Pane-Ausfuehrung`/`### Pane-Auftrag`, Statuszeile "2/2 Anker" (Z. 205-211). "Nach der Zustellung ... KEIN blockierendes Warten" (Z. 262-264). `## Rueckweg und Abschluss`: "Es laeuft kein blockierender Warteprozess. Anlassbezogen (der Mensch fragt ..." (Z. 323-326). Genau 2 Herdr-Zeilen (Z. 177, Z. 296). `allowed-tools` mit Bash (Z. 13) |
| `CLAUDE.md` | Katalogzeile "Autonomous execution" (Z. 58) beschreibt worker + pane-start ohne Ueberwachung |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §10.2 Zeilenformat (Stand, uncommitted, Fortschritt), §10.4 erlaubte Lese-Kommandos. Klasse-B-Seed — fehlt in Bestandsprojekten mit altem Seed (#22); deshalb spiegeln workflow-next/-resume/backlog-status §10 inline, Wartungs-Hinweis nennt diese 3 Spiegel (Grep-Anker `In Worktrees`) |

---

## Phase 1: Tick bauen

### Ziel
Der Ueberwachungs-Tick existiert an genau einer Stelle (`dtb:worker` → `### Pane-Ausfuehrung`),
seine Meldungsform ist an echten Daten abgenommen, und `dtb:pane-start` bietet ihn nach der
Zustellung per Verweis an und sichert die Quelle per Struktur-Check.

### Schritte

#### Schritt 1.1: Beispiel-Tick-Meldung aus echten Daten (Form-Abnahme, L64)
- **Zweck:** Meldungsform am echten Nutzen pruefen, BEVOR Regeln ausgeschrieben werden
- **Dateien:** keine Repo-Datei; **Ablageort:** die abgenommene Form wird in 1.2 woertlich als
  `Meldungsform`-Block der neuen Untersektion uebernommen; Abnahme-Vermerk im Hand-off
- **Input:** die Orchestrator-Pane (nicht diese Arbeits-Pane — sie zeigt waehrend der Arbeit
  dauerhaft `working`; Adresse aus `herdr pane list`); Pruefliste von Hand ausgefuehrt:
  `herdr agent get`, Worktree-Stand dieses Worktrees (Format DSR §10.2), Hand-off ja/nein.
  Zusaetzlich belegen, was `herdr agent get` auf eine NICHT mehr vorhandene Pane liefert
  (Exit-Code/Antwort) — Erkennungsmerkmal fuer "Pane weg"
- **Output:** drei Beispiel-Meldungen in Zielform — (1) Aenderung, (2) Ende mit Grund,
  (3) Rueckfall-Antwort auf "Stand?" — plus der Angebots-Block; im Chat vom Menschen abgenommen;
  belegtes "Pane weg"-Merkmal fliesst in 1.2

#### Schritt 1.2: Untersektion `#### Rueckweg: Ueberwachungs-Tick` in dtb:worker
- **Zweck:** die eine Quelle fuer Pruefliste, Kommandos, Meldungsregel, Selbstende, Angebot
- **Dateien:** `skills/dtb-worker/SKILL.md` (neue Untersektion in `### Pane-Ausfuehrung`, direkt
  nach `#### Rueckweg: Warten ohne Warten`; Kopplungs-Hinweis der Sektion Z. 223-227 nennt
  pane-start zusaetzlich als Leser dieser Untersektion)
- **Input:** abgenommene Form aus 1.1; discovery.md `### Gewuenschtes Verhalten` / `### Randfaelle`
- **Output:** Untersektion mit: Pruefliste (3 Signale; Worktree-Stand **autark inline** —
  Commits vor dem Hauptbranch per `git rev-list --count`, uncommitted per
  `git -C {pfad} status --porcelain`, Fortschritt X/Y aus `plan.md`/`task.md` im Worktree-Pfad —
  mit Kopplungs-Hinweis "Format gespiegelt aus DSR §10.2, Aenderung dort → hier mitziehen";
  nur Lese-Kommandos aus §10.4), Parameter `{pane-id}`/`{branch}` (`feature/{slug}` bzw.
  `task/{slug}`), **Mehr-Pane-Fall:** EIN Tick prueft alle Panes des Laufs (eine Meldung je
  geaenderter Pane, Selbstende erst, wenn die letzte beendet ist), Meldungsregel
  (Vergleich gegen letzte Tick-Meldung im Verlauf, keine Zustandsdatei; Randfall: nach
  Kontext-Komprimierung ist eine Doppelmeldung moeglich und harmlos), Selbstende (Hand-off /
  Pane weg nach dem in 1.1 belegten Merkmal), Nur-melden-Faelle (`blocked`, `max_minutes`, `unknown` nie als Ende),
  Harness-Neutralitaet + Rueckfall "Stand?" (keine `/loop`-Existenzabfrage), Meldungsform,
  Angebots-Vorlage (`/loop 15m …` + Kostenhinweis + Rueckfall-Zeile; nie selbst starten)

#### Schritt 1.3: dtb:pane-start bietet an und sichert die Quelle
- **Zweck:** interaktive Arbeitsplaetze bekommen den Tick, ohne eine zweite Kommando-Quelle
- **Dateien:** `skills/dtb-pane-start/SKILL.md` — Struktur-Check: 3. Anker
  `#### Rueckweg: Ueberwachungs-Tick` in die Ankertabelle, Statuszeile 2/2 → 3/3, Fehlerpfad-Text
  pruefen (L42: Bedingung und Zaehlgroesse im selben Zug); "Nach der Zustellung": Angebot per
  Verweis auf die worker-Vorlage (Branch `feature/{slug}`); `## Rueckweg und Abschluss`:
  "anlassbezogen oder getaktet (Tick)"
- **Input:** Untersektion aus 1.2
- **Output:** pane-start ohne neue Herdr-Kommandozeile (weiterhin genau 2)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `#### Rueckweg: Ueberwachungs-Tick` in `skills/dtb-worker/SKILL.md`
- [ ] Angebot + Struktur-Check 3/3 in `skills/dtb-pane-start/SKILL.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "^#### Rueckweg: Ueberwachungs-Tick" skills/dtb-worker/SKILL.md` = 1
- [ ] In der Untersektion (`awk '/^#### Rueckweg: Ueberwachungs-Tick/,/^#### Rueckweg: Branch-Verifikation/' skills/dtb-worker/SKILL.md`) je ≥ 1 Treffer fuer `herdr agent get`, `rev-list --count`, `status --porcelain`, `§10`, `Stand?`, `/loop 15m`
- [ ] Reihenfolge: Zeilennummer von `^#### Rueckweg: Warten ohne Warten` < `^#### Rueckweg: Ueberwachungs-Tick` < `^#### Rueckweg: Branch-Verifikation` (per `grep -n`)
- [ ] Struktur-Check-Tabelle in pane-start traegt den Anker: `awk '/^## Struktur-Check/,/^## Herdr-Mechanik/' skills/dtb-pane-start/SKILL.md | grep -c "Rueckweg: Ueberwachungs-Tick"` ≥ 1 und dieselbe Sektion enthaelt `3/3 Anker` = 1, `2/2 Anker` = 0
- [ ] Keine neue Herdr-Kommandozeile in pane-start: `grep -c "herdr agent\|herdr pane" skills/dtb-pane-start/SKILL.md` = 2
- [ ] Alt-Satz an der Wirkstelle entfernt (L8, geliefert von 1.3): `grep -c "Es laeuft kein blockierender Warteprozess. Anlassbezogen" skills/dtb-pane-start/SKILL.md` = 0

#### Manual
- [ ] Beispiel-Meldungen und Angebots-Block aus 1.1 vom Menschen abgenommen (Form hilft beim Ueberwachen)
- [ ] Text-Review der Untersektion: Pruefliste schreibt nichts, Selbstende und Nur-melden-Faelle widerspruchsfrei zu den Ausgaengen (a)-(c) von "Warten ohne Warten" (L14)

---

## Phase 2: Anbindung, Doku, Wirklauf

### Ziel
Der Worker-Traeger nutzt den Tick selbst, die Doku kennt ihn, keine Alt-Formulierung widerspricht
ihm, und ein echter Lauf belegt Stille, Meldung und Selbstende.

### Schritte

#### Schritt 2.1: Worker-Traeger bindet den Tick an
- **Zweck:** zweiter Traeger nutzt dieselbe Quelle
- **Dateien:** `skills/dtb-worker/SKILL.md` — `#### Rueckweg: Warten ohne Warten`: "anlassbezogen"
  → "anlassbezogen oder getaktet (naechste Untersektion)"; Satz nach der Start-Sequenz (Z. 276-277):
  Angebot gemaess Vorlage (Branch `task/{slug}`); Frontmatter `consumes` +
  `project-rules/DERIVED_STATE_RULES.md` (L44); `allowed-tools` pruefen (L75 — Bash vorhanden)
- **Input:** Untersektion aus 1.2
- **Output:** worker-Rueckweg verweist auf den Tick; Frontmatter nachgezogen

#### Schritt 2.2: Doku + Konsistenz-Sweep
- **Zweck:** keine Stelle behauptet mehr "nur anlassbezogen" (L3: repo-weit nach Skill-Namen greppen)
- **Dateien:** `CLAUDE.md` (Katalogzeile Z. 58: worker + pane-start um den Tick ergaenzen);
  `dtb-project/project-rules/DERIVED_STATE_RULES.md` §10 Wartungs-Hinweis: `dtb:worker`
  (`#### Rueckweg: Ueberwachungs-Tick`) als 4. Spiegel eintragen (Seed-Aenderung — erreicht
  Bestandsprojekte nicht automatisch, deshalb ist der Tick selbst autark); Sweep ueber `skills/`,
  `CLAUDE.md`, `skills/CLAUDE.md` auf "anlassbezogen", "blockierend", "pane-start";
  `skills/CLAUDE.md` bleibt unberuehrt, sofern der Sweep keinen Widerspruch findet (sonst Fund
  melden, nicht still aendern)
- **Input:** Phase-1-Stand + 2.1
- **Output:** Doku aktuell; Sweep-Ergebnis im Hand-off (Ablageort, L20)

#### Schritt 2.3: Wirklauf gegen Wegwerf-Pane (Repo-Fassung, L74)
- **Zweck:** Stille, Meldung, Blockade und Selbstende am echten Lauf belegen; offene Frage der
  Spec klaeren
- **Dateien:** keine Repo-Datei; **Ablageort:** der Mensch traegt das Ergebnis aus der
  Orchestrator-Pane in diese Arbeits-Session zurueck → Hand-off-Block (Abschnitt
  "Entscheidungen/Befunde") → Session-Log des Orchestrators
- **Input:** Der Mensch tippt in der Orchestrator-Pane `/loop` (ein per `herdr agent prompt`
  zugestellter Slash-Befehl kaeme nur als Text an — L69/L77), Pruefliste aus der
  WORKTREE-Fassung `.dtb-worktrees/pane-ueberwachungs-tick/skills/dtb-worker/SKILL.md` (nicht die
  installierte Kopie). Beobachtet wird eine **Wegwerf-Pane**, die der Lauf selbst oeffnet und
  schliesst (L57), gerichtet auf diesen Worktree; Takt fuer den Test verkuerzt (z. B. `/loop 2m`)
- **Output:** Beleg ueber ≥ 3 Ticks: mindestens ein stiller Tick, eine gemeldete Aenderung
  (Commit in diesem Worktree), eine gemeldete Blockade (in der Wegwerf-Pane provozierter
  Rechte-Dialog → `blocked`), Selbstende "Pane weg" nach dem Schliessen der Wegwerf-Pane;
  Antwort auf "festes Intervall selbst beendbar?". Das Selbstende "Hand-off eingetroffen" ist per
  Text-Review (Phase-1-Manual) abgedeckt und wird beim echten Session-Ende im Orchestrator-Log
  bestaetigt — es tritt erst NACH dem Hand-off dieser Session ein

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] worker-Rueckweg + Angebot + `consumes` nachgezogen
- [ ] `CLAUDE.md` aktualisiert, Sweep-Ergebnis dokumentiert
- [ ] DSR §10 Wartungs-Hinweis nennt worker als 4. Spiegel
- [ ] Wirklauf-Beleg im Hand-off

### Checkpoint-Kriterien

#### Automated
- [ ] `awk '/^#### Rueckweg: Warten ohne Warten/,/^#### Rueckweg: Ueberwachungs-Tick/' skills/dtb-worker/SKILL.md | grep -c "getaktet"` ≥ 1
- [ ] `sed -n '1,25p' skills/dtb-worker/SKILL.md | grep -c "consumes:.*DERIVED_STATE_RULES"` = 1
- [ ] `grep -c "Ueberwachungs-Tick" CLAUDE.md` ≥ 1
- [ ] DSR-Spiegelliste nachgezogen: `awk '/^## 10\./,/^### 10\.1/' dtb-project/project-rules/DERIVED_STATE_RULES.md | grep -c "dtb:worker"` ≥ 2 (Einleitung nennt worker schon einmal; der Wartungs-Hinweis fuegt ihn als Spiegel hinzu)

#### Manual
- [ ] Wirklauf 2.3 erbracht: stiller Tick, gemeldete Aenderung, gemeldete Blockade, Selbstende "Pane weg" mit Grund — Beleg vom Menschen zurueckgetragen und im Hand-off
- [ ] Nachlauf nach Merge bekannt: Klasse-A-Dateien geaendert → Commit → Push → `/dtb:kit-sync sync` (L39)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Ort der Pruefliste | A worker `### Pane-Ausfuehrung` / B Regeln in pane-start, Kommandos in worker / C alles in pane-start | A | Herdr-Kommando-Regel (worker Z. 180-186); pane-start reicht Herdr-Mechanik schon heute an worker weiter (per Veto-Vorlage bestaetigt 2026-09-24) |
| Vergleichsbasis "nur bei Aenderung" | Zustandsdatei / letzte Tick-Meldung im Verlauf | Verlauf | Eine Datei waere eine Zustandsaussage ohne Pfleger |
| Signal Fortschritt | Laufzeit-Verweis DSR §10.2 / autark inline + Spiegel-Eintrag in §10 | autark inline | DSR ist Klasse-B-Seed, §10 fehlt in Bestandsprojekten (#22); gleiches Muster wie die 3 Sicht-Spiegel (plan-review 2026-09-24) |
| Mehr-Pane-Warteschlange | ein Loop je Pane / ein Tick fuer alle Panes des Laufs | ein Tick fuer alle | Kosten je Takt einmal statt N-mal; Selbstende erst nach der letzten Pane (plan-review 2026-09-24) |
| Wirklauf-Objekt | diese Arbeits-Pane / Wegwerf-Pane | Wegwerf-Pane | Selbstende "Pane weg" vor dem Hand-off belegbar, 2.3 in dieser Session abhakbar (L57, plan-review 2026-09-24) |
| Takt-Vorschlag | fest 15 min / selbstgetaktet | fest 15 min | Beleg #102 (7 Ticks, 3 echte Eingriffe) |
| Selbstende-Gruende | Hand-off / Pane weg / blocked / max_minutes | nur Hand-off + Pane weg | `blocked`/`max_minutes`: Mensch entscheidet, wie heutige Ausgaenge (b)/(c) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Beispiel-Tick-Meldung — `083ee1c`
- [x] 1.2 worker-Untersektion Tick — `083ee1c`
- [x] 1.3 pane-start Angebot + Struktur-Check — `083ee1c`
- [x] 2.1 worker-Anbindung
- [x] 2.2 Doku + Sweep
- [x] 2.3 Wirklauf

---

## Umsetzung

Umsetzung mit `/dtb:implement ueberwachungs-tick` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/ueberwachungs-tick/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-24)
