# Implementierungsplan: Herdr-Worker-Automation

**Erstellt:** 2026-08-16
**Feature-Spec:** `features/herdr-worker-automation/spec.md`
**Geschaetzte Dauer:** 2-3 Sessions
**Status:** Reviewed (plan-review 2026-08-16: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Fundament: Traeger-Weiche, Auftragstext-Vorlage, Kollisionsregel, Konvention | 0.5-1 Session | Geplant |
| Phase 2 | Hinweg: Gate, Start-Sequenz, Randfall-Verhalten | 0.5 Session | Geplant |
| Phase 3 | Rueckweg: Warte-Logik, Block-Empfang, Branch-Verifikation, Abschluss | 0.5-1 Session | Geplant |
| Phase 4 | Warteschlange + Verteilung + End-to-End-Beleg | 0.5-1 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (5 Module, Pfade am 2026-08-16 per Glob verifiziert).
> **Referenz-SHA (Stand vor Phase 1):** `cef2abc` — Anker fuer das Diff-Kriterium in Phase 3 (notiert von Schritt 1.1).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-worker/SKILL.md | Traeger (entschieden 2026-08-16): Modus-Weiche (Z. 48), Modus 1 Erkennungs-Sicht (Z. 56), Modus 2 Ausfuehrung via Subagent (Z. 134), Worker-Report-Format (Z. 204); Kollisionsregel + Clean-Vorbedingung vorhanden |
| skills/dtb-workflow-checkpoint/SKILL.md | Hand-off-Format (`### Hand-off-Block`) + Empfangsseite (Schritt 1) — bleibt UNVERAENDERT (Success Criterion: Diff = 0) |
| skills/CLAUDE.md | Sektion „Parallele Sessions" (Orchestrator-Muster, Schreibgrenze, Guard-Vorlage) — Pane-Worker als Variante dokumentieren |
| workflow.config.yaml | `worker:`-Block (max_attempts/max_minutes) — max_minutes wird als Timeout-Quelle wiederverwendet; KEIN neuer Key (Entscheidung unten) |
| skills/dtb-project-init/SKILL.md | Seed-Template der Config — nur betroffen, falls doch ein Key kaeme (nach Entscheidung: nicht betroffen, Gegenprobe in 1.3) |
| (extern) ~/.claude/skills/herdr/ | Herdr-CLI-Referenz, Stand 2026-08-16 — nicht Kit-Bestandteil, dokumentiertes Drift-Risiko |

---

## Phase 1: Fundament — Traeger-Weiche, Auftragstext-Vorlage, Kollisionsregel, Konvention

### Ziel
Die EINE Quelle je Baustein steht, bevor Ablauf-Logik entsteht: Traeger-Weiche in
`dtb:worker` (Subagent | Pane), Auftragstext-Vorlage mit Grep-Anker, erweiterte
Kollisionsregel, Konventions-Absatz in `skills/CLAUDE.md`. Verhindert von Anfang an
zwei gepflegte Wortlaute (Spiegel-Kopplungs-Risiko, L14-Muster aus #42).

### Schritte

#### Schritt 1.1: Traeger-Weiche in dtb:worker anlegen
- **Zweck:** Modus 2 (Ausfuehrung) bekommt eine Traeger-Weiche: `subagent` (heutiges Verhalten, Default) | `pane` (neu, nur nach expliziter Wahl bei der Freigabe). Eligibility-Gate des Pane-Traegers: `HERDR_ENV=1` gesetzt UND `herdr` im PATH — sonst Abbruch mit Verweis auf Subagenten-Modus/manuellen Hand-off (keine stille Degradierung)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Modus-2-Struktur (Ist-Analyse), Discovery-Randfall „Kein Herdr"
- **Output:** Weiche mit Gate; Subagenten-Pfad wortgleich erhalten (Positiv-Gegenprobe: bestehende Modus-2-Kernpassagen unveraendert). Beim Start dieses Schritts den **Referenz-SHA** (`git rev-parse --short HEAD`) als Zeile in `## Ist-Analyse` dieses Plans notieren — Anker fuer das Diff-Kriterium in Phase 3 (plan-review 2026-08-16)

#### Schritt 1.2: Auftragstext-Vorlage (die eine Quelle)
- **Zweck:** Vorlage-Block mit Grep-Anker (Sektion `### Pane-Auftrag`), der ALLES traegt, was der Worker wissen muss: Worktree-Pfad, Change-Slug, Orchestrator-Pane-Adresse (`$HERDR_PANE_ID` zur Laufzeit), Schreibgrenzen-Hinweis, Anweisung „Block nach dem Format der installierten `dtb-workflow-checkpoint`-Kopie BAUEN (lesen erlaubt, nicht aufrufen)", Rueckkanal-Anweisung (`herdr agent prompt {orchestrator-pane} "<block woertlich inkl. Kopfzeile>"`). Ausgangspunkt: der real gelaufene Test-Auftrag vom 2026-08-16 (Changelog)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Test-Auftrag 2026-08-16, Hand-off-Format-Verweis
- **Output:** Vorlage mit Platzhaltern `{worktree-pfad}`, `{slug}`, `{orchestrator-pane}`; Herdr-Befehle stehen NUR hier (Drift-Risiko an einem Ort)

#### Schritt 1.3: Kollisionsregel erweitern + Konvention + Config-Gegenprobe
- **Zweck:** (a) Bestehende Kollisionsregel in `dtb:worker` um den Parallel-Fall ergaenzen (eine Quelle): Aufgaben mit gemeinsamen Dateien nie gleichzeitig, die spaetere wartet; (b) `skills/CLAUDE.md` → „Parallele Sessions": Pane-Worker als Variante des Orchestrator-Musters dokumentieren (Verweis auf dtb:worker, kein zweiter Wortlaut); (c) Gegenprobe: workflow.config.yaml und project-init-Seed bleiben unveraendert (kein neuer Key — Entscheidung unten)
- **Dateien:** `skills/dtb-worker/SKILL.md`, `skills/CLAUDE.md`
- **Input:** 1.1, 1.2, bestehende Kollisionsregel
- **Output:** Erweiterte Regel; Konventions-Absatz mit Verweis; belegte Nicht-Aenderung der Config-Dateien

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Traeger-Weiche mit Herdr-Gate in `dtb:worker`
- [ ] `### Pane-Auftrag`-Vorlage (eine Quelle, mit Grep-Anker)
- [ ] Erweiterte Kollisionsregel + Konventions-Verweis in `skills/CLAUDE.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "### Pane-Auftrag" skills/dtb-worker/SKILL.md` = 1 (Vorlage existiert genau einmal)
- [ ] Grep auf `HERDR_ENV` in `skills/dtb-worker/SKILL.md` >= 1 (Gate vorhanden) UND in keinem anderen `skills/dtb-*/SKILL.md` (Grep = 0 dort — Weiche lebt nur im Traeger)
- [ ] Positiv-Gegenprobe (L8/L15): die Modus-2-Kernpassage „Never commits/pushes" bzw. Worker-Report-Anker weiterhin vorhanden (Grep >= 1)
- [ ] `git diff --stat` zeigt KEINE Aenderung an `workflow.config.yaml` und `skills/dtb-project-init/SKILL.md`
- [ ] Verweis-Zeile in `skills/CLAUDE.md` auf den Pane-Traeger (Grep auf „Pane" in der Sektion „Parallele Sessions" >= 1)

---

## Phase 2: Hinweg — Start-Sequenz mit Randfall-Verhalten

### Ziel
Aus einer freigegebenen Aufgabe wird ohne Handarbeit ein arbeitender Pane-Worker —
inklusive der drei entschiedenen Randfaelle (Start-Fehler, fremde Session, L18).

### Schritte

#### Schritt 2.1: Vorbedingungen + Warnpruefung
- **Zweck:** Vor dem Start: (a) L18-Check — Auftragsdatei (`task.md`) committet? Sonst Abbruch mit Hinweis (Worktree aus Commit sieht Uncommittetes nicht); (b) fremde Session im Haupt-Checkout? Agent-Liste + Verzeichnis-Vergleich → genau eine ⚠-Warnung mit Pane-ID, weiterarbeiten (melden statt blockieren; Verzeichnis-Angabe ist stale-anfaellig — belegt 2026-08-16)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** L18, Discovery-Randfall 5
- **Output:** Vorbedingungs-Block im Pane-Pfad

#### Schritt 2.2: Start-Sequenz
- **Zweck:** Die vier Start-Kommandos als EIN dokumentierter Ablauf: `git worktree add {pfad} -b task/{slug}` (**Task-Branch — bewusste Differenz zum detached-Subagenten-Modus**, Entscheidung „Pane-Modus-Artefakte" unten: Merge und Diff-Abnahme brauchen eine Branch-Referenz) → `herdr pane split --current --direction right --cwd {pfad} --no-focus` → `herdr agent start {name} --kind claude --pane {id} -- {dummy-arg}` (Dummy-Argument IMMER — umgeht den belegten PowerShell-Bug; bei Timeout genau 1 Retry mit laengerem Timeout, danach Abbruch mit Meldung + Pane-Inhalt) → `herdr agent prompt {name} "{Pane-Auftrag}"`. Pane-ID aus der split-Antwort lesen, nie raten
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Vorlage aus 1.2, Discovery-Randfall 1
- **Output:** Start-Sequenz im Pane-Pfad; Worker-Name-Schema (`worker-{slug-kurz}`)

#### Schritt 2.3: Trockenlauf Hinweg + Gate-Negativ-Test + Zustellungs-Probe
- **Zweck:** Drei Belege (plan-review 2026-08-16): (a) Sequenz an einer Wegwerf-Aufgabe: Worktree + Pane + Worker entstehen, Auftrag kommt an (Worker bestaetigt Empfang), danach Abbruch und Aufraeumen — noch KEIN Rueckweg (Phase 3); (b) **Gate-Negativ-Test** (SC4): Lauf mit ausgesetztem `HERDR_ENV` → Abbruch mit Verweis auf Subagenten-Modus/manuellen Weg, protokolliert; (c) **Mehrzeilen-Zustellungs-Probe**: ein mehrzeiliger Testblock (inkl. Kopfzeilen-Format) wird per `agent prompt` zugestellt und kommt als EINE Nachricht an (Quoting-Beleg — Unknown Unknown des Reviews). Ablageort des Protokolls (L20): Chat + `### Naechste Schritte`-Notiz im Session-Log der Sitzung
- **Dateien:** keine (Testlauf; Fixture wird entfernt)
- **Input:** 2.1, 2.2
- **Output:** Protokoll im Chat (alle drei Belege), Fixture entfernt

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Pane-Pfad Hinweg komplett (Vorbedingungen → Start-Sequenz → Auftrag)
- [ ] Trockenlauf-Protokoll

### Checkpoint-Kriterien

#### Automated
- [ ] Grep auf `worktree add` UND `pane split` UND `agent start` UND `agent prompt` in `skills/dtb-worker/SKILL.md` je >= 1 (Sequenz vollstaendig dokumentiert)
- [ ] Grep auf das Dummy-Argument-Muster im `agent start`-Kommando der Sequenz (L2: am Kommando verankert, nicht als Prosa)
- [ ] Trockenlauf protokolliert: Pane-ID aus split-Antwort verwendet, Auftrag zugestellt, Fixture entfernt (`git worktree list` zeigt nur den Haupt-Checkout)
- [ ] Gate-Negativ-Test protokolliert: ohne `HERDR_ENV` → Abbruch mit Verweis (SC4-Beleg)
- [ ] Zustellungs-Probe protokolliert: mehrzeiliger Block kam als EINE Nachricht an

---

## Phase 3: Rueckweg — Warten, Empfang, Verifikation, Abschluss

### Ziel
Der Hand-off-Block kommt automatisch an, wird gegen den Branch verifiziert, und der
Abschluss laeuft in der entschiedenen Reihenfolge — ohne Aenderung an
`dtb:workflow-checkpoint`.

### Schritte

#### Schritt 3.1: Warte-Logik (kein aktives Warten)
- **Zweck:** Entschieden (plan-review 2026-08-16): **KEIN blockierender wait-Prozess** — der Push des Workers weckt die Orchestrator-Session von selbst (belegt 2026-08-16). Stattdessen anlassbezogene Pruefung: Bei jedem passenden Anlass (Mensch fragt nach dem Stand, naechste Aufgabe soll zugeteilt werden) prueft der Orchestrator per `herdr agent get {name}` Status + verstrichene Zeit gegen `worker.max_minutes`. Ausgaenge: (a) Block trifft als Prompt ein → weiter 3.2; (b) Status `blocked` → Pane lesen, Zustand melden, Mensch entscheidet; (c) Zeit ueberschritten → Pane lesen, melden, Mensch entscheidet. KEIN Auto-Stopp (umgeht #62)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Discovery-Randfall 2, `worker.max_minutes`
- **Output:** Warte-Block mit drei definierten Ausgaengen, ohne blockierenden Prozess

#### Schritt 3.2: Branch-Verifikation vor dem Checkpoint
- **Zweck:** Eingetroffenen Block pruefen, BEVOR der Mensch `/dtb:workflow-checkpoint` aufruft: Kopfzeile + `Erledigt:` vorhanden; genannter Commit existiert auf dem Task-Branch (`git log master..task/{slug}`); Diff-Dateiliste (`git diff --stat master..task/{slug}`) deckt die `Dateien:`-Eintraege. Abweichung → melden mit Befund, nicht raten; Block trotzdem anzeigen (Entscheidung beim Menschen). Verifikation lebt im Orchestrator-Ablauf von dtb:worker — `dtb:workflow-checkpoint` bleibt unberuehrt
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** Discovery-Randfall 3, reale Verifikation vom 2026-08-16 als Vorlage
- **Output:** Verifikations-Block mit den zwei git-Kommandos; Meldung „Worker {name} fertig — Diff ansehen?" als blockierende Auswahlfrage

#### Schritt 3.3: Abschluss-Sequenz
- **Zweck:** Nach menschlicher Diff-Abnahme (blockierende Auswahlfrage, KEIN Auto-Merge): `git merge --ff-only` (Fallback bei non-ff: melden, Mensch entscheidet) → Hinweis auf `/dtb:workflow-checkpoint` mit dem Block (Empfangsseite) → NACH dem Checkpoint: Worker-Pane beenden lassen, `git worktree remove` + Branch loeschen (entschiedene Reihenfolge: Worktree bleibt bis nach dem Checkpoint als Beweismittel). Kit-sync-Hinweis, falls Klasse-A-Dateien im Diff (#51-Muster)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** 3.2, realer Ablauf 2026-08-16
- **Output:** Abschluss-Sequenz mit Reihenfolge-Begruendung

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Warte-Logik mit drei Ausgaengen
- [ ] Branch-Verifikation (vor Checkpoint, ausserhalb des Checkpoint-Skills)
- [ ] Abschluss-Sequenz in entschiedener Reihenfolge

### Checkpoint-Kriterien

#### Automated
- [ ] Grep auf `agent get` und `max_minutes` im Pane-Pfad von `skills/dtb-worker/SKILL.md` je >= 1 (anlassbezogene Pruefung verankert)
- [ ] Grep auf die zwei Verifikations-Kommandos (`master..task/` -Muster) >= 2 (L2: an den git-Kommandos verankert)
- [ ] `git diff {Referenz-SHA aus 1.1}..HEAD -- skills/dtb-workflow-checkpoint/SKILL.md` = leer (Success Criterion; SHA steht in `## Ist-Analyse`)
- [ ] Kein `--force`/`--no-verify` im gesamten Pane-Pfad (Grep = 0; Sicherheitsregeln)

---

## Phase 4: Warteschlange + Verteilung + End-to-End-Beleg

### Ziel
Mehrere freigegebene Aufgaben laufen nacheinander/parallel korrekt durch; die
installierten Kopien sind aktuell; die Success Criteria sind real belegt.

### Schritte

#### Schritt 4.1: Warteschlange
- **Zweck:** Zuteilungs-Logik im Pane-Pfad: freigegebene Aufgaben in Reihenfolge der Abhaengigkeitsanalyse (Erkennungs-Sicht liefert sie schon); parallele Panes nur fuer Aufgaben ohne gemeinsame Dateien (erweiterte Kollisionsregel aus 1.3); freier Worker bekommt die naechste; Pane-Anzahl kommt aus der Freigabe-Frage (Default 2, kein Config-Key)
- **Dateien:** `skills/dtb-worker/SKILL.md`
- **Input:** 1.3, Erkennungs-Sicht
- **Output:** Warteschlangen-Block im Pane-Pfad

#### Schritt 4.2: Commit, Push, kit-sync
- **Zweck:** Klasse-A-Nachlauf: geaenderte `skills/dtb-worker/SKILL.md` (+ `skills/CLAUDE.md`, Repo-Doku ohne Verteilung) committen, pushen, `/dtb:kit-sync sync`
- **Dateien:** keine neuen (git + sync)
- **Input:** Phasen 1-3 committet
- **Output:** Lock aktuell, Verifikation „alle synchron"

#### Schritt 4.3: End-to-End-Beleg (2 Aufgaben) + Negativ-Test
- **Zweck:** Realer Durchlauf mit **zwei echten kleinen Aufgaben bei einem Worker**
  (plan-review 2026-08-16, SC5-Beleg: die Queue laeuft real — freier Worker bekommt die
  naechste; Aufgaben aus der INBOX waehlen, Muster 2026-08-16): Freigabe → automatischer
  Hinweg → Worker arbeitet → Block kommt automatisch → Verifikation gruen → Abnahme →
  Merge → naechste Aufgabe → … → Checkpoint → Aufraeumen. PLUS Negativ-Test der
  Verifikation (Success Criterion): einen Block mit falscher Commit-Angabe einspeisen →
  Meldung statt Durchwinken. Ablageort (L20): Abnahme-Protokoll im Session-Log
- **Dateien:** keine (Abnahme-Lauf; entstehende Artefakte sind echte Session-Artefakte)
- **Input:** 4.1, 4.2 (installierte Kopien aktuell)
- **Output:** Abnahme-Protokoll im Session-Log (Queue-Durchlauf + Negativ-Test)

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Warteschlangen-Logik
- [ ] Sync-Report „alle synchron"
- [ ] End-to-End-Protokoll inkl. Negativ-Test

### Checkpoint-Kriterien

#### Automated
- [ ] `kit-sync check` nach dem Sync: 0 Abweichungen
- [ ] E2E-Beleg mit 2 Aufgaben: beide Bloecke kamen als Prompt an (Kopfzeilen im Protokoll), Queue-Reihenfolge protokolliert (zweite Aufgabe erst nach Abschluss der ersten), Verifikations-Kommandos je gelaufen
- [ ] Negativ-Test protokolliert: falscher Commit → Meldung (kein Merge-Angebot)

#### Manual
- [ ] End-to-End-Durchlauf abgenommen: Mensch hat genau zwei Beruehrungspunkte erlebt (Freigabe, Diff-Abnahme) — alles dazwischen lief ohne Handgriff

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger | Pane-Modus in dtb:worker / eigener Skill | In dtb:worker (2026-08-16) | Wiederverwendet Erkennungs-Sicht, Freigabe, Kollisionsregel, Config, Report — kein zweiter gepflegter Wortlaut (L14-Muster) |
| Aufraeum-Reihenfolge | Nach Merge sofort / nach Checkpoint | Nach Checkpoint (2026-08-16) | Realer Lauf 2026-08-16 als Vorlage; Worktree bleibt bis zuletzt Beweismittel; Pane muss ohnehin zuerst beendet werden (Windows: Verzeichnis in Benutzung) |
| Kollisionsregel | Bestehende erweitern / eigene Queue-Regel | Bestehende erweitern (2026-08-16) | Eine Quelle in dtb:worker; zwei Regeln zum selben Gegenstand laufen auseinander |
| Rueckweg | Push durch Worker / Pull via agent read | Push (Discovery, belegt) | Alternate Screen verliert gescrollten Text — Pull ist fuer den Hand-off unbrauchbar |
| Checkpoint-Aufruf durch Worker | Skill aufrufen / Format bauen | Format nach installierter Kopie BAUEN | `disable-model-invocation` bleibt unangetastet; formalisiert den real gegangenen Weg |
| Timeout-Quelle | Neuer Key / worker.max_minutes | worker.max_minutes wiederverwenden | Eine Quelle, kein Seed-Skew (#22) |
| Pane-Anzahl | Config-Key / Freigabe-Frage | Freigabe-Frage, Default 2, KEIN Key | Seed-Skew vermeiden; die Zahl ist situativ (Aufgabenlage), kein Projektzustand |
| Herdr-Drift | Laufzeit-Versionscheck / dokumentiertes Risiko | Dokumentiertes Risiko | Discovery 3e; Befehle nur in der Pane-Auftrag-Vorlage → Anpassung an einem Ort |
| Pane-Modus-Artefakte | worker-report.md + Block / nur Block; Task-Branch / detached | Kein worker-report.md, Task-Branch (plan-review 2026-08-16) | Hand-off-Block ersetzt den Report vollstaendig (landet via Empfangsseite im Session-Log — dauerhafter); Task-Branch, weil Merge und Diff-Abnahme eine Branch-Referenz brauchen. Subagenten-Modus bleibt unveraendert detached + worker-report.md — bewusste, dokumentierte Differenz |
| Warte-Mechanik | Hintergrund-wait / kein aktives Warten | Kein aktives Warten (plan-review 2026-08-16) | Der Push weckt die Session ohnehin (belegt); Timeout/blocked anlassbezogen pruefen — kein blockierender Prozess, weniger Mechanik |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Traeger-Weiche + Herdr-Gate — `161367b`
- [x] 1.2 Pane-Auftrag-Vorlage — `161367b`
- [x] 1.3 Kollisionsregel + Konvention + Config-Gegenprobe — `161367b`
- [x] 2.1 Vorbedingungen + Warnpruefung — `766d9a0`
- [x] 2.2 Start-Sequenz — `766d9a0`
- [x] 2.3 Trockenlauf + Gate-Negativ + Zustellungs-Probe — `766d9a0`
- [x] 3.1 Warte-Logik — `e2d1169`
- [x] 3.2 Branch-Verifikation — `e2d1169`
- [x] 3.3 Abschluss-Sequenz — `e2d1169`
- [x] 4.1 Warteschlange — `15a3ec5`
- [x] 4.2 Commit, Push, kit-sync — `15a3ec5`
- [x] 4.3 End-to-End-Beleg (2 Aufgaben) + Negativ-Test — `a625f4b`

---

## Umsetzung

Umsetzung mit `/dtb:implement herdr-worker-automation` — 3x3-Rhythmus und
Phasen-Ende-Ritual (Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine
Quelle). Wiedereinstieg bei Kontextverlust: `features/herdr-worker-automation/plan.md`
laden; der erste nicht abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
