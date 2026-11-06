# Implementierungsplan: Worker-Job-Ende-Meldung

**Erstellt:** 2026-11-06
**Feature-Spec:** `features/worker-job-ende-meldung/spec.md`
**Geschaetzte Dauer:** 4-5,5 h
**Status:** Reviewed (plan-review 2026-11-06: REVISE → 7 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Proben (Registrierung, Hook-Shell, Nebeneinander, Zustellung, Zeichen) | 1,5 h | Geplant |
| Phase 2 | Skill-Integration (worker Hinweg/Rueckweg/Tick, pane-start, Doku) | 1,5-2 h | Geplant |
| Phase 3 | Abnahme Ende-zu-Ende aus dieser Pane | 1-2 h | Geplant |

**Schlanke Variante (plan-review 2026-11-06, Empfehlung 1):** Der Hook ist nur ein **Signal** —
ein Einzeiler im Settings-Befehl, der `WORKER-STOP (dtb) — {slug}` an die Orchestrator-Pane
schickt (zweiter Versuch nach 2 s, Exit immer 0). Die Fakten (Commits, uncommitted, Fortschritt)
und den Abgleich „ist der Hand-off-Block hier eingetroffen?" macht der Orchestrator selbst — er
liest den Branch-Stand ohnehin und sieht den Block in seiner eigenen Session. Damit entfallen
Skriptdatei, Transcript-Parsing und die kit-sync-Erweiterung (Discovery-Punkte 2 und 4 revidiert;
Spec-Nachzug siehe `## Offene Punkte`).

---

## Ist-Analyse

> Quelle: `discovery.md` (`## Betroffene Module`), Pfade verifiziert. Durch die schlanke Variante
> entfallen `skills/dtb-worker/scripts/`, `skills/dtb-kit-sync/SKILL.md` und `skills/CLAUDE.md`
> (Distribution) als Aenderungsziele.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-worker/SKILL.md | `#### Hinweg: Start-Sequenz` Kommando 3 startet `herdr pane run {pane-id} "claude"`; `#### Rueckweg: Warten ohne Warten` hat Ausgaenge (a)-(c); Tick-Pruefpunkt 3 erkennt nur `WORKTREE-HANDOFF (dtb)`; Herdr-Kommandos sind in `### Pane-Auftrag` + `### Pane-Ausfuehrung` erlaubt — der Einzeiler lebt in der Start-Sequenz, also KEINE neue Herdr-Ausnahme |
| skills/dtb-pane-start/SKILL.md | `## Herdr-Mechanik` → Tabelle „bewusste Abweichungen" (Branch, Text, Worktree-Pfad; Einleitung sagt „Zwei") — Startbefehl fehlt dort |
| skills/dtb-workflow-checkpoint/SKILL.md | `### Hand-off-Block` (Kopfzeile `WORKTREE-HANDOFF (dtb) — Quelle: …`) — nur Lesequelle |
| CLAUDE.md | Kategorie-Text zu `worker` (Autonomous execution) |

---

## Phase 1: Proben

### Ziel
Die offenen Punkte mit Belegen klaeren, bevor Skill-Text entsteht. Ergebnis entscheidet
Registrierung (pro Session vs. globaler Rueckfall), Form des Einzeilers (welche Shell fuehrt
Hook-Befehle aus) und Zeichenformat.

### Schritte

#### Schritt 1.1: Probe Registrierung per `--settings` und Hook-Shell
- **Zweck:** Feuert ein Stop-Hook aus `claude --settings {datei}` (Claude Code 2.1.318, Windows)? In welcher Shell laeuft der Hook-Befehl (Git Bash, cmd, PowerShell)?
- **Dateien:** `features/worker-job-ende-meldung/probe.md` (neu, Ablageort aller Proben — L20); Wegwerf-Settings im Scratchpad
- **Input:** Mini-Hook, der Shell-Kennung (`echo $0` bzw. `$PSVersionTable`) und Zeitstempel in eine Scratchpad-Datei schreibt; erst `claude -p` (billig), dann interaktiv in einer frischen Herdr-Pane (L67)
- **Output:** `probe.md` → `## Probe 1: Registrierung` (feuert ja/nein, Shell)

#### Schritt 1.2: Probe Nebeneinander mit globalem Stop-Hook
- **Zweck:** Laeuft der globale Sprachausgabe-Hook weiter und der `--settings`-Hook zusaetzlich?
- **Dateien:** `probe.md` → `## Probe 2: Nebeneinander`
- **Input:** Lauf aus 1.1; Spur des globalen Hooks
- **Output:** Beleg beide feuern ja/nein

#### Schritt 1.3: Probe Zustellung und Zeichen
- **Zweck:** (a) `herdr agent prompt` an eine Session mitten im Turn; (b) an eine Pane, in deren Eingabezeile gerade Text steht (Mensch tippt — L79); (c) kommen `—` aus der Hook-Shell unverfaelscht an?
- **Dateien:** `probe.md` → `## Probe 3: Zustellung` (a+b), `## Probe 4: Zeichen` (c)
- **Input:** Wegwerf-Pane mit Claude-Session; (a) langer Auftrag, waehrenddessen zustellen; (b) Text per `herdr pane send-text` in die Eingabezeile legen (nicht abschicken), dann zustellen; Beobachtung je per `herdr pane read`
- **Output:** Belege; Entscheidung Zeichenformat; bei Vermischung in (b) → Gegenmassnahme als Entscheidung nachtragen (z.B. Meldung erst bei leerer Eingabezeile ist NICHT moeglich im Einzeiler → als bekannte Grenze dokumentieren)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `probe.md` mit vier Proben-Abschnitten
- [ ] `## Technische Entscheidungen` nachgetragen (Registrierung, Hook-Shell, Zeichenformat)

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE '^## Probe [1-4]: ' dtb-project/project-workflows/features/worker-job-ende-meldung/probe.md` ergibt 4
- [ ] `grep -E '^\| (Registrierung|Hook-Shell|Zeichenformat) \|' dtb-project/project-workflows/features/worker-job-ende-meldung/plan.md` zeigt in keiner der drei Zeilen die Entscheidung `Offen`

#### Manual
- [ ] Bei „Hook feuert nicht" (1.1): Rueckfall auf globale Registrierung mit dem Menschen bestaetigt, bevor Phase 2 beginnt

---

## Phase 2: Skill-Integration

### Ziel
Worker startet seine Pane-Session mit dem Signal-Hook, Orchestrator und Tick werten das Signal
aus, `pane-start` bleibt hook-frei.

### Schritte

#### Schritt 2.1: `dtb:worker` — Hinweg (Einrichtung + Start)
- **Zweck:** Signal-Hook bei jedem Worker-Pane-Start einrichten
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Hinweg: Start-Sequenz`)
- **Input:** Ergebnis Phase 1
- **Output:** vor Kommando 3 ein Einrichtungsschritt: `{slug}` gegen `^[a-z0-9][a-z0-9-]*$` und `{orchestrator-pane}` gegen das Herdr-Adressformat pruefen; Settings-Datei `{git-dir des Worktrees}/dtb-worker-hook.json` mit genau einem `Stop`-Hook (Einzeiler: Signal, zweiter Versuch nach 2 s, Exit 0; Timeout 15 s) schreiben — nur unkritische Zeichen, keine Pfade im JSON (L66 greift nicht); Kommando 3 wird `herdr pane run {pane-id} "claude --settings {datei}"` (bzw. globaler Rueckfall laut Phase 1). **Fehlerweg** (plan-review Empfehlung 2): scheitert Pruefung oder Schreiben → genau eine Warnzeile `⚠ Signal-Hook fuer {slug} nicht eingerichtet ({Grund}) — Worker startet ohne Ende-Signal, Netz ist der Ueberwachungs-Tick` und Kommando 3 ohne `--settings`; nie still, nie Abbruch

#### Schritt 2.2: `dtb:worker` — Rueckweg Ausgang (d)
- **Zweck:** Orchestrator reagiert auf das Signal mit eigenen Fakten
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Rueckweg: Warten ohne Warten`)
- **Input:** Spec `## Scope` (Verhalten), Tick-Pruefpunkt 2 (Fakten-Kommandos)
- **Output:** Ausgang (d) `WORKER-STOP (dtb) — {slug}`: Orchestrator liest Worktree-Stand wie Tick-Pruefpunkt 2 (Commits, uncommitted, Fortschritt — per Verweis, nicht kopiert) und prueft, ob in dieser Session ein `WORKTREE-HANDOFF (dtb) — Quelle: {slug}`-Block eingetroffen ist. Block da → eine Bestaetigungszeile mit dem Stand, dann Branch-Verifikation wie bisher. Block fehlt → einmal `herdr pane read {pane-id}`, Meldung „Worker hat aufgehoert ohne Hand-off — wartet er auf eine Antwort oder hat er den Block vergessen?" mit Stand, Mensch entscheidet, nichts automatisch senden. Hinweis: ein Auswahldialog des Workers beendet keinen Turn → kein Signal, das deckt Ausgang (b)/Tick (`blocked`)

#### Schritt 2.3: `dtb:worker` — Ueberwachungs-Tick
- **Zweck:** Tick wertet das Signal als zusaetzliches Signal
- **Dateien:** `skills/dtb-worker/SKILL.md` (`#### Rueckweg: Ueberwachungs-Tick`)
- **Input:** Ausgang (d)
- **Output:** Pruefpunkt 3 erkennt zusaetzlich `WORKER-STOP (dtb) — {slug}`; Ausgaenge-Tabelle: Signal ohne Hand-off → einmal `gestoppt ohne Hand-off`, Pane bleibt beobachtet; Signal mit Hand-off → nichts Neues; Meldungsform um eine Beispielzeile ergaenzt

#### Schritt 2.4: `dtb:pane-start`, Abschluss-Hinweis und Doku
- **Zweck:** Pane-start-Panes bleiben hook-frei; Aufraeumen und Beschreibung stimmen
- **Dateien:** `skills/dtb-pane-start/SKILL.md` (`## Herdr-Mechanik`), `skills/dtb-worker/SKILL.md` (`#### Abschluss` Punkt 4, Kopplungs-Hinweis an `### Pane-Ausfuehrung`), `CLAUDE.md` (Kategorie `worker`)
- **Input:** Tabelle „bewusste Abweichungen"
- **Output:** neue Abweichungs-Zeile „Startbefehl: `dtb:worker` richtet den Signal-Hook ein und startet `claude --settings …` — hier KEINE Einrichtung, nur `claude`" mit Begruendung, Einleitung „Zwei bewusste Abweichungen" auf die tatsaechliche Zahl korrigiert; Gegen-Hinweis in `dtb:worker`; `#### Abschluss` Punkt 4: Settings-Datei verschwindet mit `git worktree remove`; `CLAUDE.md` nennt den Signal-Hook in einem Halbsatz

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `dtb:worker` mit Einrichtung, Ausgang (d), Tick-Erweiterung
- [ ] `dtb:pane-start` mit benannter Abweichung
- [ ] `CLAUDE.md` Kategorie-Text nachgezogen

### Checkpoint-Kriterien

#### Automated
- [ ] `claude --settings` steht in `skills/dtb-worker/SKILL.md` nur zwischen den Ankern `^#### Hinweg: Start-Sequenz` und `^#### Rueckweg: Warten ohne Warten` (Zeilennummern per `grep -n` gegen die Anker-Zeilen — L2/L116)
- [ ] `grep -c 'WORKER-STOP (dtb)' skills/dtb-worker/SKILL.md` ≥ 4 (Einrichtung, Ausgang (d), Tick-Pruefpunkt, Meldungsform)
- [ ] `grep -n 'claude --settings' skills/dtb-pane-start/SKILL.md` trifft nur innerhalb `## Herdr-Mechanik`
- [ ] Struktur-Check von `dtb:pane-start` gegen die Repo-Fassung: `^### Pane-Ausfuehrung`, `^### Pane-Auftrag`, `^#### Rueckweg: Ueberwachungs-Tick` je genau 1 (`tr -d '\r' | grep -c`, L74/L89)
- [ ] `grep -n '^allowed-tools' skills/dtb-worker/SKILL.md` enthaelt `Bash` (L75)
- [ ] `grep -c 'Signal-Hook fuer {slug} nicht eingerichtet' skills/dtb-worker/SKILL.md` = 1 (Fehlerweg vorhanden)

---

## Phase 3: Abnahme Ende-zu-Ende

### Ziel
Die Success Criteria an einer echten Claude-Session belegen — aus dieser Pane heraus, ohne
`dtb:worker` zu starten (Worktrees entstehen nur aus dem Haupt-Checkout): diese Pane spielt den
Orchestrator und wendet Ausgang (d) aus der Repo-Fassung an (L74), eine Wegwerf-Pane den Worker
(L57: nur selbst erzeugte Objekte).

### Schritte

#### Schritt 3.1: Wirklauf ohne und mit Hand-off
- **Zweck:** Signal ohne Block, dann nach Nachfassen mit Block — inkl. Mehrfach-Stopp
- **Dateien:** `probe.md` → `## Abnahme`
- **Input:** Wegwerf-Pane, Einrichtung laut 2.1 mit `{orchestrator-pane}` = `$HERDR_PANE_ID`, Worktree = dieser Arbeitsplatz; Wegwerf-Auftrag schreibt NICHTS (nur antworten); Nachfassen mit dem Auftrag, einen Test-Block zu senden
- **Output:** zwei Signale kommen hier an; Reaktion nach Ausgang (d) je einmal protokolliert (ohne Block → Meldung, mit Block → Bestaetigung)

#### Schritt 3.2: Randfaelle im Wirklauf
- **Zweck:** Orchestrator weg; pane-start ohne Hook; globale Einstellungen unberuehrt
- **Dateien:** `probe.md` → `## Abnahme`
- **Input:** Einrichtung mit nicht existierender Orchestrator-Adresse; Einrichtung mit ungueltigem Slug (Fehlerweg); zweite Wegwerf-Pane mit nur `claude`; Hash von `~/.claude/settings.json` vor/nach
- **Output:** Worker-Session laeuft ungestoert weiter (keine Hook-Fehlermeldung im Verlauf); ungueltiger Slug → Warnzeile laut 2.1, Start ohne `--settings`; keine Signalzeile aus der Pane ohne Hook; Hash unveraendert

#### Schritt 3.3: Tick-Probe
- **Zweck:** Erfolgskriterium „Tick meldet `gestoppt ohne Hand-off` genau einmal" belegen
- **Dateien:** `probe.md` → `## Abnahme`
- **Input:** Lage aus 3.1 (Signal ohne Block); Tick-Pruefliste aus der Repo-Fassung zweimal per „Stand?"-Rueckfall ausfuehren
- **Output:** erster Lauf zeigt `gestoppt ohne Hand-off`, zweiter Lauf ohne Aenderung keine Zeile; Wegwerf-Panes danach geschlossen, Settings-Dateien der Probe aus dem Git-Verwaltungsordner entfernt

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `probe.md` → `## Abnahme` mit Belegen zu allen Success Criteria
- [ ] Wegwerf-Panes geschlossen, Probe-Settings entfernt

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'WORKER-STOP (dtb)' dtb-project/project-workflows/features/worker-job-ende-meldung/probe.md` ≥ 2 (beide Signale woertlich eingefuegt)
- [ ] `grep -c 'gestoppt ohne Hand-off' dtb-project/project-workflows/features/worker-job-ende-meldung/probe.md` ≥ 1
- [ ] `git status --porcelain` im Arbeitsplatz vor 3.1 und nach 3.3 identisch, ausser `probe.md` (Wegwerf-Session hat nichts geschrieben)
- [ ] `herdr pane list` zeigt keine Wegwerf-Pane dieses Laufs mehr

#### Manual
- [ ] Mensch bestaetigt: Signal und Orchestrator-Meldung ohne Block sind verstaendlich und loesen die richtige Reaktion aus

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Hook-Umfang | Skript mit Fakten + Transcript, Einzeiler-Signal | Einzeiler-Signal | plan-review Empfehlung 1: Fakten und Hand-off-Abgleich hat der Orchestrator selbst; spart Transcript-Parsing (Zeitlimit-Risiko), Skriptdatei und kit-sync-Klasse |
| Registrierung | `--settings` pro Session, global mit Selbstpruefung | `--settings` pro Session | Probe 1 (1c/1d): feuert interaktiv und im Print-Modus; Probe 2: ergaenzt globale Stop-Hooks |
| Hook-Shell | Git Bash, cmd, PowerShell | shell-neutraler Aufruf `powershell -NoProfile -ExecutionPolicy Bypass -File "{skript}"` | Probe 1: die Hook-Shell wechselt je Startweg (Print-Modus PS 5.1, Herdr-Pane Git Bash) — nur ein Befehl ohne Variablen/Operatoren laeuft ueberall |
| Zeichenformat | Unicode (`—`), ASCII (`-`) | Unicode | Probe 4: `—` kommt aus PS 5.1 ueber Herdr unverfaelscht an |
| Settings-Datei schreiben | Serialisierer, direkte Ausgabe | direkte Ausgabe nach Pruefung von Slug und Adresse | Inhalt nur aus kebab-case-Slug, Pane-Adresse und festem Text — keine Pfade, keine Backslashes |
| Herdr-Ort | neue Ausnahme, Start-Sequenz | Start-Sequenz | `### Pane-Ausfuehrung` ist bereits erlaubter Ort — keine neue Ausnahme |
| Ablage Settings | Arbeitsbaum, Git-Verwaltungsordner | Git-Verwaltungsordner | Wie Uebergabe-Notiz; nicht committbar, verschwindet mit dem Worktree |
| Abnahme-Ort | Wirklauf via `dtb:worker` aus dem Haupt-Checkout, Simulation aus dieser Pane | Simulation aus dieser Pane | Gleicher Code-Pfad (echte Session + Herdr); Worktrees nur aus dem Haupt-Checkout |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Probe Registrierung und Hook-Shell — `45ba7d6`
- [x] 1.2 Probe Nebeneinander mit globalem Stop-Hook — `45ba7d6`
- [x] 1.3 Probe Zustellung und Zeichen — `45ba7d6`
- [x] 2.1 worker Hinweg Einrichtung und Start
- [x] 2.2 worker Rueckweg Ausgang (d)
- [x] 2.3 worker Ueberwachungs-Tick
- [x] 2.4 pane-start, Abschluss-Hinweis und Doku
- [ ] 3.1 Wirklauf ohne und mit Hand-off
- [ ] 3.2 Randfaelle im Wirklauf
- [ ] 3.3 Tick-Probe

---

## Offene Punkte

- Spec-Nachzug: `spec.md` beschreibt noch die Skript-Variante (Signalzeile mit Fakten, Transcript, kit-sync-Klasse, Logzeile) — nach dem Review auf die schlanke Variante ziehen

---

## Umsetzung

Umsetzung mit `/dtb:implement Worker-Job-Ende-Meldung` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/worker-job-ende-meldung/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
