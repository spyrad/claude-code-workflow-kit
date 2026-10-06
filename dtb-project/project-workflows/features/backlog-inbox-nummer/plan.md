# Implementierungsplan: BACKLOG-Spalte #

**Erstellt:** 2026-10-06
**Feature-Spec:** `features/backlog-inbox-nummer/spec.md`
**Geschaetzte Dauer:** ca. 1,5 h
**Status:** Reviewed (plan-review 2026-10-06: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Vorlage + Zeilen-Schreiber | 45 min | Geplant |
| Phase 2 | Checkpoint-Nachzug, Anzeige, Regel | 45 min | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Modul-Liste per Grep verifiziert 2026-10-06).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-project-init/SKILL.md` | BACKLOG-Vorlage mit vier Tabellenkoepfen `| Feature | Status | …` / `| Aufgabe | Status | …` / `| Feature | Abgeschlossen | Datei |` |
| `skills/dtb-feature-plan/SKILL.md` | Schritt 10 schreibt `| {Feature-Name} | Spezifiziert | {Prio} | features/{slug}/spec.md | {Ziel} |`; Nummer bekannt ueber Inbox-Auswahl (Schritt 2) oder `**Idee-Referenz:**` der discovery.md |
| `skills/dtb-feature-fast/SKILL.md` | Schritt 7 verweist auf feature-plan Schritt 10, Status `Geplant`; Nummer aus Schritt 1 (Eingangs-Gate) |
| `skills/dtb-task/SKILL.md` | Schritt 4 schreibt `| {Aufgaben-Name} | Offen | … | features/{slug}/task.md | … |` und traegt eine Abschnitts-Vorlage "Aufgaben"; Nummer ueber Zahl-Argument (Schritt 1) bzw. Schritt 4b |
| `skills/dtb-bug-report/SKILL.md` | schreibt `| Bug: {Bug-Name} | Offen | {Severity} | features/{slug}/bug.md | … |`; kein INBOX-Bezug |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Sync-Schritt "Synchronisiere die Anzeige-Felder": Status-Spalte BACKLOG, `**Status:**` in spec/task, Datum; consumes INBOX.md + BACKLOG.md, produces BACKLOG.md |
| `skills/dtb-backlog-status/SKILL.md` | Report-Vorlage mit sieben Tabellen — fuenf mit Feature-/Aufgaben-Zeilen (`| Feature | …` viermal, `| Aufgabe | Prio | Status | Datei |`), dazu `| Bug | …` und „Nicht im Backlog" (`| Datei | Titel | Status |`) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §3 "Statusfeld in BACKLOG.md ist abgeleitete Anzeige"; §8 Change-Link-Pflicht |
| `skills/dtb-archive/SKILL.md`, `skills/dtb-project-health/SKILL.md` | unberuehrt — Zugriff ueber Dateipfad/Abschnitt, nicht ueber Spaltenposition |
| Leser-Sweep (Lektion 3, plan-review 2026-10-06) | `grep -rln BACKLOG skills/`: `dtb-feature-start`, `dtb-workflow-next`, `dtb-workflow-resume`, `dtb-workflow-status`, `dtb-idea-rank`, `dtb-project-health`, `dtb-archive` lesen BACKLOG.md ueber Status, Spaltennamen oder Dateipfad — keiner nach Spaltenposition; `dtb-impl-review`, `dtb-pane-start`, `dtb-worker`, `dtb-pipeline-graph` nennen die Datei nur |

---

## Phase 1: Vorlage + Zeilen-Schreiber

### Ziel
Neue Projekte haben die Spalte `#`, und jeder Skill, der eine BACKLOG-Zeile anlegt, fuellt sie
(Nummer oder `—`). Trifft ein Schreiber auf einen alten Kopf ohne `#`, schreibt er im alten
Format — eine einzige Toleranz-Klausel je Schreiber, keine Eigen-Migration.

### Schritte

#### Schritt 1.1: BACKLOG-Vorlage in project-init
- **Zweck:** Neue Projekte starten mit der Spalte
- **Dateien:** `skills/dtb-project-init/SKILL.md`
- **Input:** Vorlage "BACKLOG.md → Zielpfad …"
- **Output:** Alle vier Tabellenkoepfe beginnen mit `| # |`, Trennzeilen um `|---|` ergaenzt; im Erklaer-Kasten der Vorlage ein Halbsatz: `#` = INBOX-Nummer der Idee, `—` ohne Idee, abgeleitete Anzeige

#### Schritt 1.2: feature-plan + feature-fast
- **Zweck:** Feature-Zeilen tragen die Nummer
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-feature-fast/SKILL.md`
- **Input:** feature-plan Schritt 10, feature-fast Schritt 7
- **Output:** feature-plan: Zeilenformat `| {INBOX-Nr oder —} | {Feature-Name} | Spezifiziert | … |` mit Herkunft der Nummer (Inbox-Auswahl in Schritt 2, sonst `**Idee-Referenz:** Inbox #{N}` der discovery.md, sonst `—`) und Toleranz-Klausel (Kopf ohne `#` → altes Format, der Checkpoint zieht nach). feature-fast Schritt 7: ein Satz — Spalte `#` = Nummer aus Schritt 1

#### Schritt 1.3: task + bug-report
- **Zweck:** Aufgaben- und Bug-Zeilen tragen die Spalte
- **Dateien:** `skills/dtb-task/SKILL.md`, `skills/dtb-bug-report/SKILL.md`
- **Input:** task Schritt 4 (Zeile + Abschnitts-Vorlage "Aufgaben"), bug-report Backlog-Eintrag
- **Output:** task: `| {INBOX-Nr oder —} | {Aufgaben-Name} | Offen | … |` (Nummer aus Zahl-Argument bzw. INBOX-Herkunft wie Schritt 4b), Abschnitts-Vorlage mit `| # |`-Kopf; bug-report: `| — | Bug: {Bug-Name} | Offen | … |`; beide mit derselben Toleranz-Klausel wie 1.2

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] BACKLOG-Vorlage mit Spalte `#`
- [ ] Vier Zeilen-Schreiber fuellen die Spalte, tolerant gegen alten Kopf

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -cE '^\| # \| (Feature|Aufgabe) \|' skills/dtb-project-init/SKILL.md` = 4
- [ ] `grep -cE '^\| (Feature|Aufgabe) \| (Status|Abgeschlossen) \|' skills/dtb-project-init/SKILL.md` = 0 (keine alten Koepfe mehr in der Vorlage)
- [ ] `grep -c '| {INBOX-Nr oder —} | {Feature-Name} |' skills/dtb-feature-plan/SKILL.md` >= 1
- [ ] `grep -c '| {INBOX-Nr oder —} | {Aufgaben-Name} |' skills/dtb-task/SKILL.md` >= 2 (Zeile + Abschnitts-Vorlage)
- [ ] `grep -c '| — | Bug: {Bug-Name} |' skills/dtb-bug-report/SKILL.md` >= 1
- [ ] `grep -c 'Spalte `#`' skills/dtb-feature-fast/SKILL.md` >= 1
- [ ] Toleranz-Klausel in allen drei zeilenschreibenden Skills: `grep -l 'Kopf ohne `#`' skills/dtb-feature-plan/SKILL.md skills/dtb-task/SKILL.md skills/dtb-bug-report/SKILL.md` listet 3 Dateien

---

## Phase 2: Checkpoint-Nachzug, Anzeige, Regel

### Ziel
Bestandsprojekte bekommen die Spalte beim naechsten Checkpoint, die Nummer bleibt eine
abgeleitete Anzeige (Quellen: INBOX-Change-Link, dann ARCHIVE_LOG; nie ueberschrieben), und `dtb:backlog-status` zeigt sie.

### Schritte

#### Schritt 2.1: Checkpoint zieht `#` nach
- **Zweck:** Bestandsprojekte erreichen (Lektion 82: Vorlage allein reicht nicht)
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Sync-Schritt "Synchronisiere die Anzeige-Felder", DSR §8
- **Output:** Neuer Spiegelpunkt "Spalte `#` in BACKLOG.md": (a) fehlt die Spalte in einer Tabelle → Kopf, Trennzeile und jede Datenzeile ergaenzen; (b) NUR fehlende oder leere Zellen fuellen, Quellen in dieser Reihenfolge: INBOX-Zeile, deren Change-Link auf den Ordner der Datei-Spalte zeigt → deren Nummer; sonst Eintrag in `archive/ARCHIVE_LOG.md` (`#{N}` + Link auf denselben Ordner) → dessen Nummer; sonst `—`; (c) eine vorhandene Nummer wird NIE ueberschrieben, auch nicht mit `—` — `dtb:archive` verschiebt INBOX-Zeilen `Ausgearbeitet` mit gueltigem Link, waehrend der Change noch aktiv ist, die Quelle kann also verschwinden (plan-review 2026-10-06). Verlinken mehrere INBOX-Zeilen denselben Ordner → kleinste Nummer (Entscheidung plan-review 2026-10-06) und den offenen Punkt in spec.md/discovery.md schliessen; im selben Zug die Nie-Ueberschreiben-Regel in spec.md (Scope-Zeile „fehlende oder abweichende Nummern" → „fehlende Nummern", Risiko-Zeile „der Checkpoint gewinnt") und discovery.md („fehlende/abweichende Werte") nachziehen. Frontmatter pruefen (Lektion 44): consumes INBOX.md + BACKLOG.md, produces BACKLOG.md — bereits vorhanden

#### Schritt 2.2: backlog-status zeigt `#`
- **Zweck:** Nachschlagen per Nummer im Report, nicht nur in der Rohdatei
- **Dateien:** `skills/dtb-backlog-status/SKILL.md`
- **Input:** Report-Vorlage (sieben Tabellen: Aktiv, Geplant, Fertig zum Testen / Abgenommen, Abgeschlossen, Offene Bugs, Offene Aufgaben, Nicht im Backlog)
- **Output:** Die fuenf Tabellen mit Feature- bzw. Aufgaben-Zeilen (Aktiv, Geplant, Fertig zum Testen / Abgenommen, Abgeschlossen, Offene Aufgaben) mit erster Spalte `#`; Offene Bugs (immer `—`) und Nicht im Backlog (keine BACKLOG-Zeile als Quelle) bleiben ohne (plan-review 2026-10-06), Wert aus BACKLOG.md uebernommen (fehlt die Spalte dort → `—`, kein eigenes Ableiten); die Ideen-Liste als `- #{N} {Feature}: …`

#### Schritt 2.3: Regel-Absatz in DSR §3
- **Zweck:** Kanon dokumentieren: `#` ist abgeleitete Anzeige, Quelle INBOX-Change-Link, Pfleger `dtb:workflow-checkpoint`
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** §3 "Statusfeld in BACKLOG.md …", §8
- **Output:** Ein Absatz in §3 — `#` ist abgeleitete Anzeige, wird nur nachgefuellt, nie ueberschrieben (mit Hinweis: Laufzeittext steht inline im Checkpoint, weil die Datei ein Seed ist) + Zeile im Aenderungsverlauf der Datei

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Checkpoint ergaenzt die Spalte `#` und fuellt leere Zellen, ohne vorhandene Nummern zu ueberschreiben
- [ ] backlog-status zeigt die Nummer
- [ ] DSR §3 dokumentiert die Regel

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'Spalte `#`' skills/dtb-workflow-checkpoint/SKILL.md` >= 1 und der Treffer liegt im Sync-Schritt "Synchronisiere die Anzeige-Felder" (Lektion 2: am Zielort verankert)
- [ ] `grep -cE '^\| # \| (Feature|Aufgabe) \|' skills/dtb-backlog-status/SKILL.md` = 5
- [ ] `grep -c 'Spalte `#`' dtb-project/project-rules/DERIVED_STATE_RULES.md` >= 1

#### Manual
- [ ] Trockenlauf gegen die Repo-Fassung (Lektion 74): eine BACKLOG-Datei im alten Format (Testkopie im Scratchpad, eine Zeile mit INBOX-Link, eine ohne, ein Bug) nach der neuen Checkpoint-Regel gedanklich umstellen — Ergebnis: Kopf mit `#`, Nummer bzw. `—` korrekt

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Wer migriert Bestandsprojekte? | A: jeder Schreiber selbst, B: nur der Checkpoint | B | Eine Migrationsstelle statt vier; der Checkpoint pflegt ohnehin die Anzeige-Felder (DSR §1.3) — per Veto-Vorlage bestaetigt 2026-10-06 |
| Spaltenposition | erste Spalte, letzte Spalte | erste | Gleiche Kopfform wie INBOX.md — per Veto-Vorlage bestaetigt 2026-10-06 |
| Zellform | `107`, `#107` | `107` | Wie die `#`-Spalte der INBOX — per Veto-Vorlage bestaetigt 2026-10-06 |
| Regelort | DSR allein, inline im Skill | inline im Checkpoint + Absatz in DSR | DSR ist Seed und erreicht Bestandsprojekte nicht (Lektion 82) |
| Mehrere INBOX-Links auf einen Ordner | kleinste Nummer, alle kommagetrennt | kleinste Nummer | Eine Zelle, ein Wert — die aelteste Idee ist der Ursprung; per plan-review bestaetigt 2026-10-06 |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 BACKLOG-Vorlage project-init — `be76836`
- [x] 1.2 feature-plan + feature-fast — `be76836`
- [x] 1.3 task + bug-report — `be76836`
- [x] 2.1 Checkpoint zieht # nach — `06b8b6e`
- [x] 2.2 backlog-status zeigt # — `06b8b6e`
- [x] 2.3 Regel-Absatz DSR §3 — `06b8b6e`

---

## Umsetzung

Umsetzung mit `/dtb:implement backlog-inbox-nummer` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/backlog-inbox-nummer/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-06)
