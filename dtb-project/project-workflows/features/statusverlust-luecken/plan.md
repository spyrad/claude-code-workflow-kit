# Implementierungsplan: Statusverlust-Luecken schliessen

**Erstellt:** 2026-09-23
**Feature-Spec:** `features/statusverlust-luecken/spec.md`
**Geschaetzte Dauer:** 6,5-7,5 h (4 Phasen)
**Status:** Reviewed (plan-review 2026-09-23: REVISE → 5 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Kanon in `DERIVED_STATE_RULES.md` + Config-Key + Beispielausgaben (Abnahme-Gate) | 1,5 h | Geplant |
| Phase 2 | Task-Lane-Absicherung (1) — Leseseite | 1 h | Geplant |
| Phase 3 | Checkpoint: Abgangsvermerke (2) + Alter (3) | 2,5 h | Geplant |
| Phase 4 | Worktree-Sicht (4) + Aufraeum-Hinweis, Doku, Robustheit, Abnahme | 2 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (14 Module, Pfade verifiziert 2026-09-23) + Nachlese im impl-plan.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-idea-review/SKILL.md` | Z. 162-166: Task-Lane setzt `Ausgearbeitet` + Vermerk „task.md-Link ergaenzt /dtb:task"; Begruendung F2 (2026-08-02) |
| `skills/dtb-task/SKILL.md` | Schritt 4b (Z. 186-198): haengt `→ features/{slug}/task.md` an, zieht `Ausgearbeitet` nach |
| `skills/dtb-archive/SKILL.md` | Schritt 2 (Z. 71): `Ausgearbeitet` pauschal Kandidat; Schutzregel Z. 204 |
| `skills/dtb-project-health/SKILL.md` | Z. 84-86 und 147-148: prueft nur `spec.md`-Link, nicht `task.md`, kein Fall „Link fehlt" |
| `skills/dtb-idea-rank/SKILL.md` | Z. 63: zaehlt nur `Offen`; Z. 150-157: „Ausgearbeitet ohne Change-Link" = nicht pruefbar |
| `skills/dtb-workflow-status/SKILL.md` | Z. 40-42: zaehlt INBOX-Status, nur `Offen`/`In Arbeit` pipeline-relevant; Z. 59 Kopie-Muster #22 |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 470 Zeilen; Log-Template Z. 129-146 (`### Naechste Schritte` mit Checkboxen); Teil 2 Template Z. 206-209 `## Offene Aufgaben`, Datei wird IMMER ueberschrieben |
| `skills/dtb-workflow-next/SKILL.md` | Quellen Z. 36-54 (INBOX nur `In Arbeit`); Pipeline-Tabelle Z. 58-70; Kopie-Muster #22 Z. 50-52; Ausgabe Schritt 4 Z. 133 |
| `skills/dtb-workflow-resume/SKILL.md` | Schritt 3 Git-Status (Z. 48-78, nur `git -C {repo.path}`); Report-Varianten Z. 157-240 mit `## Git` |
| `skills/dtb-backlog-status/SKILL.md` | Report Schritt 4 (Z. 65-122), Abschnitt `## Offene Aufgaben` Z. 105 |
| `skills/dtb-pane-start/SKILL.md` | `.dtb-worktrees/pane-{slug}`, Branch `feature/{slug}` (Z. 254-256) |
| `skills/dtb-worker/SKILL.md` | Pane-Traeger `worker-{slug}` + `task/{slug}` (Z. 257); Subagent `worker-{slug}` detached `HEAD` (Z. 362) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | 434 Zeilen, Abschnitte §1-§7; kein Abschnitt zu Link-Pflicht, Aufgaben-Lebenslauf, Worktree-Stand |
| `skills/dtb-project-init/SKILL.md` | Config-Template Z. 95-115 (Muster `parallel.default_branch` mit Erlaeuterungszeile) |
| `workflow.config.yaml` | Kit-Vorlage; Bloecke `idea_triage`, `worker`, `parallel` |
| `dtb-project/project-workflows/WORKFLOW_STATUS.md` | `## Offene Aufgaben` Z. 27-35: 7 Punkte, kein Datum; 173 Versionen, 0× `[x]` |

---

## Phase 1: Kanon, Config-Key, Beispielausgaben

### Ziel
Die drei Regeln stehen einmal kanonisch in `DERIVED_STATE_RULES.md`; der Config-Key existiert;
der Nutzer hat die Zielform aller neuen Ausgaben an echten Daten abgenommen (L64), bevor Skills
angefasst werden.

### Schritte

#### Schritt 1.1: DSR §8 — Change-Link-Pflicht fuer `Ausgearbeitet`
- **Zweck:** Luecke (1) auf der Leseseite schliessen, ohne die F2-Entscheidung zu revidieren
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (neuer Abschnitt `## 8.`)
- **Input:** Spec (1), Randfaelle (1), L19
- **Output:** Regel: `Ausgearbeitet` gueltig nur mit Link `→ features/{slug}/{spec|task|bug}.md`, dessen
  Ordner existiert, oder Link auf `archive/{slug}/` (= erledigt). Sonst abgeleiteter Zustand
  „Ausgearbeitet, Change fehlt" = offen, naechster Schritt `/dtb:task {N}` bzw. `/dtb:feature-plan`.
  Status-Neutralitaet: kein neuer INBOX-Statuswert (Anzeige-Zustand, kein Feldwert)

#### Schritt 1.2: DSR §9 — Lebenslauf offener Aufgaben
- **Zweck:** Luecken (2)+(3) als EIN Mechanismus definieren (L45: Zaehlbegriff an der Quelle)
- **Dateien:** `DERIVED_STATE_RULES.md` (neuer Abschnitt `## 9.`)
- **Input:** Spec (2)(3), Randfaelle (2)+(3), Technische Entscheidungen T1-T3
- **Output:** Regel mit: fuehrende Liste = `## Offene Aufgaben` in WORKFLOW_STATUS; Zeilenformat
  `- [ ] {Aufgabe} — Kontext: {kurz} (seit YYYY-MM-DD[ · behalten YYYY-MM-DD])`; Vergleichsbasis =
  Datei auf der Platte vor dem Ueberschreiben; semantische Zuordnung + Rueckfrage bei Unsicherheit;
  Abgangsvermerke `erledigt` / `verworfen: {Grund}` / `aufgegangen in …` unter
  `### Aufgaben-Abgaenge` im Session-Log (einfache Aufzaehlung, KEINE Checkboxen); aeltestes Datum
  wird geerbt; ⏳ ab `status.alter_schwelle_tage` seit dem juengeren von `seit`/`behalten`; EINE
  Sammelvorlage, Default „behalten"; Abbruch = alles bleibt; Altbestand `(seit ≤YYYY-MM-DD)`

#### Schritt 1.3: DSR §10 — Worktree-Stand
- **Zweck:** Luecke (4) + Aufraeum-Luecke einmal definieren, die drei Sichten referenzieren/kopieren
- **Dateien:** `DERIVED_STATE_RULES.md` (neuer Abschnitt `## 10.`)
- **Input:** Spec (4), Randfaelle (4), Integrationspunkte (Quellen), T4
- **Output:** Regel mit: Quelle `git worktree list --porcelain` ohne Haupt-Checkout; Zeilenformat
  `{slug} {Art} {branch|detached} {Commit-Stand} {N uncommitted} {Fortschritt}`; Art aus Pfad-Praefix
  (`pane-` interaktiv, `worker-` autonom, sonst `manuell`); Fortschritt: `## Progress` via
  `git show {branch}:…/plan.md` → `## Schritte` aus `task.md` → Stage-Name → „—"; Subagent/detached:
  `worker-report.md` aus dem Worktree-Pfad lesen; `prunable` → „verwaist → `git worktree prune`";
  **frisch** (Branch-Reflog hat nur den Anlage-Eintrag, keine eigenen Commits) → Label `frisch`, nie
  „aufraeumen"; **gemergt** (Branch hatte eigene Commits, alle im Hauptbranch) → „gemergt → aufraeumen" (T10); letzter Commit aelter als Schwelle → ⏳;
  Nicht-Git / keine Zusatz-Worktrees → Block entfaellt still; erlaubte Kommandos nur lesend

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Config-Key `status.alter_schwelle_tage`
- **Zweck:** Schwelle konfigurierbar, Default im Skill bei fehlendem Key (Muster `parallel.default_branch`)
- **Dateien:** `workflow.config.yaml`, `skills/dtb-project-init/SKILL.md` (Template + Erlaeuterungszeile)
- **Input:** T3
- **Output:** Block `status:` mit `alter_schwelle_tage: 7  # §9/§10 — ⏳ ab N Tagen`

#### Schritt 1.5: Beispielausgaben in Zielform (Abnahme-Gate L64)
- **Zweck:** Zielform an echten Daten vom Nutzer abnehmen lassen, bevor Skills umgebaut werden
- **Dateien:** `features/statusverlust-luecken/beispielausgaben.md` (neu, Ablageort nach L20)
- **Input:** aktuelle `WORKFLOW_STATUS.md`, `git worktree list`, INBOX, §8-§10
- **Output:** vier Beispiele mit echten Daten: (a) Worktree-Block, (b) Offene Aufgaben mit `seit`/⏳,
  (c) `### Aufgaben-Abgaenge`-Block, (d) archive-/next-Meldung „Ausgearbeitet, Change fehlt"
  (fuer (d) ein Attrappen-Eintrag, klar als solcher markiert — L57)

### Deliverables
- [ ] DSR §8, §9, §10
- [ ] Config-Key in Kit-Vorlage und project-init-Template
- [ ] `beispielausgaben.md`, vom Nutzer abgenommen

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -nE '^## (8|9|10)\. ' dtb-project/project-rules/DERIVED_STATE_RULES.md` liefert genau 3 Treffer
- [ ] `grep -n 'alter_schwelle_tage' workflow.config.yaml skills/dtb-project-init/SKILL.md` liefert Treffer in beiden Dateien
- [ ] `grep -n 'Aufgaben-Abgaenge' dtb-project/project-rules/DERIVED_STATE_RULES.md` trifft in §9
- [ ] `test -f dtb-project/project-workflows/features/statusverlust-luecken/beispielausgaben.md`

#### Manual
- [ ] Nutzer nimmt die vier Beispielausgaben ab (Form, Laenge, Lesbarkeit)

---

## Phase 2: Task-Lane-Absicherung (1)

### Ziel
Eine Idee `Ausgearbeitet` ohne gueltigen Change-Link wird von keiner Sicht mehr als erledigt
behandelt und von `archive` nicht entsorgt.

### Schritte

#### Schritt 2.1: `dtb:archive` — Sperre + Meldung
- **Zweck:** Der eigentliche Verlustpfad (Archivierung) wird geschlossen
- **Dateien:** `skills/dtb-archive/SKILL.md` (Schritt 2 INBOX, Schritt 3 Uebersicht, Schutzregel Z. 204)
- **Input:** §8
- **Output:** `Ausgearbeitet` nur mit gueltigem Link Kandidat; sonst eigener Block
  „Nicht archiviert — Change fehlt: #{N} → /dtb:task {N}"; operative Kopie §8 + Wartungs-Hinweis (#22)

#### Schritt 2.2: `dtb:project-health` — Link-Pruefung spec/task/bug
- **Zweck:** Konsistenz-Check deckt alle Change-Arten und den fehlenden Link ab
- **Dateien:** `skills/dtb-project-health/SKILL.md` (INBOX → Features, INBOX ↔ Feature-Status)
- **Input:** §8
- **Output:** `Ausgearbeitet` → Link auf `spec.md`/`task.md`/`bug.md` muss existieren; fehlt Link oder
  Ordner → WARNUNG „Change fehlt"; Kopie + Wartungs-Hinweis

#### Schritt 2.3: `workflow-next`, `workflow-status`, `idea-rank` — als offen fuehren
- **Zweck:** Die Idee bleibt in den Sichten sichtbar
- **Dateien:** `skills/dtb-workflow-next/SKILL.md` (Quellen + Pipeline-Tabelle: neue Zeile
  „INBOX `Ausgearbeitet`, Change fehlt → `/dtb:task {N}`"), `skills/dtb-workflow-status/SKILL.md`
  (Zaehlung: „Change fehlt" pipeline-relevant), `skills/dtb-idea-rank/SKILL.md` (Zeile in der Tabelle
  als EINE Hinweiszeile unter der Tabelle „offen, Change fehlt: #{N}" — keine eigene Tabellenzeile,
  Vertrag Z. 63 bleibt (T12); Regel Z. 150-157 abgleichen)
- **Input:** §8
- **Output:** drei Skills mit Kopie + Wartungs-Hinweis

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: `dtb:idea-review` — Vermerk „Link ausstehend"
- **Zweck:** Der Zwischenzustand ist im Vermerk selbst lesbar
- **Dateien:** `skills/dtb-idea-review/SKILL.md` (Task-Lane Z. 162-166)
- **Input:** §8; L3 (repo-weit nach „als Aufgabe geroutet" greppen, alle Leser mitziehen)
- **Output:** Vermerk `→ als Aufgabe geroutet ({Datum}); task.md ausstehend — /dtb:task {N}`;
  F2-Begruendung bleibt unveraendert; `dtb:task` Schritt 4b ersetzt den Vermerk durch den Link

#### Schritt 2.5: Eigenpruefung gegen die Fehlerklasse (L15)
- **Zweck:** Neuer Text wird gegen „Idee verschwindet ohne Change" geprueft, nicht nur per Grep
- **Dateien:** keine Aenderung; Ergebnis in den Session-Log (Ablageort L20)
- **Input:** Wegwerf-Projekt im Scratchpad mit Attrappe `#999 Ausgearbeitet` ohne Link (L57)
- **Output:** Probelauf `archive`/`next`/`project-health` gegen die REPO-Fassung der SKILL.md (nicht
  die installierte Kopie — T8): alle drei melden „Change fehlt", keiner archiviert

### Deliverables
- [ ] Fuenf Skills mit §8-Kopie + Wartungs-Hinweis
- [ ] Probelauf-Ergebnis im Session-Log

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -ln 'Change fehlt' skills/dtb-{archive,project-health,workflow-next,workflow-status,idea-rank}/SKILL.md` liefert 5 Dateien
- [ ] `grep -n 'task.md ausstehend' skills/dtb-idea-review/SKILL.md` trifft im Task-Lane-Block
- [ ] `grep -c 'Kopie ist Absicht' skills/dtb-archive/SKILL.md skills/dtb-project-health/SKILL.md` ≥ 1 je Datei
- [ ] `grep -n 'Aufgabe geroutet' -r skills/` — jeder Treffer ist an das neue Vermerk-Format angepasst (Liste im Log)

#### Manual
- [ ] Probelauf 2.5 im Wegwerf-Projekt bestaetigt: keine Archivierung, drei Meldungen

---

## Phase 3: Checkpoint — Abgangsvermerke (2) + Alter (3)

### Ziel
Kein Punkt verschwindet ohne Vermerk; jeder offene Punkt traegt ein stabiles Datum; Dauerlaeufer
erzwingen genau eine Entscheidung je Schwelle.

### Schritte

#### Schritt 3.1: Schritt 1 — Vergleich vor dem Log-Schreiben
- **Zweck:** Mechanismus (2)+(3) im Checkpoint verankern — der Vergleich laeuft in Schritt 1
  (Informationen sammeln), also VOR Teil 1, weil der Log die Abgaenge schon braucht
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 1: bisherige `WORKFLOW_STATUS.md`
  lesen und zuordnen; Teil 2: Template `## Offene Aufgaben` mit `(seit …)`; Empfangsseite
  Hand-off: uebernommene Offene Punkte bekommen `seit = Hand-off-Datum` (T11))
- **Input:** §9 (kompakte Kopie + Wartungs-Hinweis, Details nur in der DSR)
- **Output:** alte Liste wird gelesen, zugeordnet, neue Liste mit geerbten Daten geschrieben;
  Worktree-Teil-Guard ueberspringt den Vergleich (holt der naechste Orchestrator-Checkpoint nach)

#### Schritt 3.2: Log-Template — `### Aufgaben-Abgaenge`
- **Zweck:** Dauerhafte Spur fuer jeden Abgang im append-only Log
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Teil 1 Format, Z. 129-146)
- **Input:** §9
- **Output:** neuer Abschnitt `### Aufgaben-Abgaenge` (einfache Aufzaehlung, entfaellt bei 0 Abgaengen);
  `### Naechste Schritte` uebernimmt `(seit …)`

#### Schritt 3.3: ⏳-Sammelvorlage
- **Zweck:** Dauerlaeufer einmal zur Entscheidung bringen, ohne Tapete
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** §9, Config-Key (Default 7 bei fehlendem Key)
- **Output:** EINE Vorlage (Default „behalten", Veto je Zeile: erledigen / verwerfen + Grund);
  „behalten" → `· behalten YYYY-MM-DD`; Abbruch → alles unveraendert

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Vertraeglichkeit der Leser
- **Zweck:** Leser von `Offene Aufgaben` / `Naechste Schritte` vertragen `(seit …)` und ⏳
- **Dateien:** `skills/dtb-session-summary/SKILL.md`, `skills/dtb-feature-start/SKILL.md`,
  `skills/dtb-workflow-resume/SKILL.md`, `skills/dtb-backlog-status/SKILL.md` (nur falls noetig)
- **Input:** L3 — `grep -rn 'Offene Aufgaben\|Naechste Schritte' skills/` (14 Dateien laut Scan)
- **Output:** Liste der Leser mit Befund „vertraeglich" / „angepasst" im Session-Log

#### Schritt 3.5: Probe-Checkpoint im Wegwerf-Projekt (Spec-Nutzer-Test)
- **Zweck:** Eigenpruefung gegen die Fehlerklasse „Punkt verschwindet ohne Spur" (L15)
- **Dateien:** keine; Ergebnis in den Session-Log
- **Input:** Wegwerf-Projekt mit `WORKFLOW_STATUS.md`-Attrappe: 1 umformulierter, 2 zusammengelegte,
  1 verworfener, 1 ueberfaelliger Punkt (L57)
- **Output:** korrekte Vermerke, aeltestes Datum geerbt, genau eine ⏳-Vorlage

### Deliverables
- [ ] Checkpoint mit §9-Kopie, `### Aufgaben-Abgaenge`, `(seit …)`, ⏳-Vorlage
- [ ] Leser-Befund + Probe-Ergebnis im Session-Log

### Checkpoint-Kriterien

#### Automated
- [ ] `wc -l < skills/dtb-workflow-checkpoint/SKILL.md` ≤ 510 (Wachstum ≤ +40, T5)
- [ ] `grep -n '### Aufgaben-Abgaenge' skills/dtb-workflow-checkpoint/SKILL.md` trifft im Log-Template
- [ ] `grep -n '(seit YYYY-MM-DD' skills/dtb-workflow-checkpoint/SKILL.md` trifft im Teil-2-Template
- [ ] `grep -n 'alter_schwelle_tage' skills/dtb-workflow-checkpoint/SKILL.md` trifft (Default 7 benannt)
- [ ] `grep -n 'seit = Hand-off-Datum' skills/dtb-workflow-checkpoint/SKILL.md` trifft im Empfangsseiten-Block

#### Manual
- [ ] Probe-Checkpoint 3.5 liefert die erwarteten Vermerke und Daten

---

## Phase 4: Worktree-Sicht (4), Doku, Abnahme

### Ziel
Die drei Lese-Sichten zeigen jeden Zusatz-Worktree mit Stand; gemergte als „aufraeumen" — rein lesend.

### Schritte

#### Schritt 4.1: `dtb:workflow-resume` — Worktree-Stand
- **Zweck:** Beim Wiedereinstieg ist laufende Worktree-Arbeit sichtbar
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md` (nach Schritt 3; Report-Abschnitt `## In Worktrees`)
- **Input:** §10 (operative Kopie + Wartungs-Hinweis)
- **Output:** Lese-Schritt + Report-Block in allen Report-Varianten

#### Schritt 4.2: `dtb:workflow-next` — Block „In Worktrees"
- **Zweck:** Naechste Schritte beruecksichtigen Arbeit ausserhalb des Haupt-Checkouts
- **Dateien:** `skills/dtb-workflow-next/SKILL.md` (Quellen + Schritt 4 Ausgabe)
- **Input:** §10
- **Output:** Block in der Ausgabe ohne Argument; ⏳/„aufraeumen" als naechster Schritt

#### Schritt 4.3: `dtb:backlog-status` — Abschnitt `## In Worktrees`
- **Zweck:** Backlog-Uebersicht zeigt, woran gerade ausserhalb gearbeitet wird
- **Dateien:** `skills/dtb-backlog-status/SKILL.md` (Report Schritt 4)
- **Input:** §10
- **Output:** Abschnitt nach `## Aktiv (in Arbeit)`

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

#### Schritt 4.4: Frontmatter und Doku nachziehen (L44, L3)
- **Zweck:** Maschinell gelesene Wahrheit und Kit-Doku stimmen mit dem neuen Verhalten ueberein
- **Dateien:** Frontmatter `consumes` der geaenderten Skills (nur falls ein neues Artefakt gelesen wird,
  `pipeline-graph`-Vertraeglichkeit pruefen); `CLAUDE.md` (Skill-Beschreibungen checkpoint, next,
  resume, backlog-status, archive); `README.md` falls dort Skill-Verhalten beschrieben ist
- **Input:** Diff der Phasen 1-4
- **Output:** konsistente Frontmatter + Doku

#### Schritt 4.5: Abnahme mit Wegwerf-Worktree (L57)
- **Zweck:** Worktree-Sicht an einem selbst erzeugten Objekt pruefen — alle drei Zustaende getrennt
- **Dateien:** keine dauerhaften; Ergebnis in den Session-Log
- **Input:** Probe-Hauptbranch `probe/haupt` + Probe-Worktree `{scratchpad}/probe-wt` auf Branch
  `probe/statusverlust` (echter Hauptbranch wird nicht angefasst); Hauptbranch-Erkennung fuer den
  Probelauf per `parallel.default_branch: probe/haupt` in einer Wegwerf-Config
- **Output:** Sicht zeigt nacheinander (a) direkt nach Anlage `frisch` (kein „aufraeumen"),
  (b) nach einem Commit + einer uncommitteten Datei Stand + `1 uncommitted`, Art `manuell`,
  (c) nach Merge von `probe/statusverlust` in `probe/haupt` „gemergt → aufraeumen"; Probelauf gegen
  die REPO-Fassung (T8). Danach Probe entfernen (`git worktree remove`, `git branch -D` beider
  Probe-Branches) — nach Bestaetigung durch den Nutzer

#### Schritt 4.6: Kopie ↔ Kanon + Robustheit
- **Zweck:** Drift zwischen operativen Kopien und DSR-Kanon ausschliessen (Spec-Risiko) und die
  Spec-Zusagen „alte DSR-Kopie" / „Nicht-Git-Projekt" belegen
- **Dateien:** keine Aenderung (ausser Nachbesserung bei Fund); Ergebnis in den Session-Log
- **Input:** Kernbegriffe je Abschnitt — §8 `Change fehlt`, §9 `Aufgaben-Abgaenge` + `seit` +
  `alter_schwelle_tage`, §10 `frisch` + `gemergt` + `In Worktrees`; Wegwerf-Kopie des Kits im
  Scratchpad (L57), einmal ohne `.git`, einmal mit DSR-Stand von `master` (ohne §8-§10)
- **Output:** Kernbegriff-Grep je Kopie gruen; Probelauf `workflow-next`/`archive` (Repo-Fassung,
  T8) in beiden Wegwerf-Kopien: Luecken-Schliessung wirkt trotz alter DSR, ohne `.git` kein
  Worktree-Block und kein Fehler

### Deliverables
- [ ] Drei Sichten mit §10-Kopie + Wartungs-Hinweis
- [ ] Frontmatter/Doku konsistent
- [ ] Abnahme-Ergebnis im Session-Log, Probe-Worktree und Probe-Branches entfernt
- [ ] Kopie↔Kanon- und Robustheits-Befund im Session-Log

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -ln 'In Worktrees' skills/dtb-{workflow-resume,workflow-next,backlog-status}/SKILL.md` liefert 3 Dateien
- [ ] `grep -c 'Kopie ist Absicht.*§10' skills/dtb-{workflow-resume,workflow-next,backlog-status}/SKILL.md` ≥ 1 je Datei (neuer Anker, heute 0)
- [ ] Kernbegriff-Grep 4.6: `grep -l 'frisch' skills/dtb-{workflow-resume,workflow-next,backlog-status}/SKILL.md` = 3 und `grep -l 'Aufgaben-Abgaenge' skills/dtb-workflow-checkpoint/SKILL.md` = 1
- [ ] `git worktree list | grep -c probe-wt` = 0 nach Abschluss
- [ ] `grep -nE '^- \*\*Session lifecycle\*\*.*Worktree|backlog-status.*Worktree' CLAUDE.md` trifft (geankert auf die Skill-Beschreibungszeilen)

#### Manual
- [ ] Nutzer bestaetigt die Abnahme 4.5 (alle drei Zustaende korrekt angezeigt)
- [ ] Probelaeufe 4.6 (alte DSR, ohne `.git`) bestaetigt

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| T1 Fuehrende Liste | `## Offene Aufgaben` (WORKFLOW_STATUS) / `### Naechste Schritte` (Log) | Offene Aufgaben | wird weitergetragen; Log-Liste ist Momentaufnahme und uebernimmt `seit` |
| T2 Vergleichsbasis | committete Version / letzter Log / Datei auf der Platte | Datei vor dem Ueberschreiben | braucht kein Git, funktioniert im Nicht-Git-Projekt |
| T3 Schwelle | eine / zwei Schwellen | eine: `status.alter_schwelle_tage: 7` | Aufgaben- und Worktree-Alter meinen dasselbe „liegt zu lange" |
| T4 Hauptbranch | `parallel.default_branch` / master-main-Raten / Haupt-Checkout-Branch | Config-Wert, sonst Branch des ersten `git worktree list`-Eintrags | kein Raten |
| T5 Checkpoint-Groesse | nur Verweis / kompakte Kopie | kompakte Kopie, Wachstum ≤ +40 Zeilen | folgt aus T6; Zeilenlimit-Idee keine Vorbedingung |
| T6 Verteilung der Regeln | Kopie-Muster #22 / Rueckfallregel | Kopie-Muster #22 | Luecken schliessen sich in allen Zielprojekten sofort nach kit-sync |
| T7 Task-Lane | `In Arbeit` bis task.md / `Ausgearbeitet` + Leseseite | `Ausgearbeitet` + Leseseite | F2 (2026-08-02) bleibt gueltig |
| T8 Probelaeufe | installierte Skills / Repo-Fassung | Repo-Fassung der SKILL.md lesen und ausfuehren | `~/.claude/`-Kopien sind bis zum kit-sync nach Merge der alte Stand |
| T9 „behalten"-Frist | Datum ueberschreiben / Zusatzvermerk | `· behalten YYYY-MM-DD` | `seit` bleibt unveraendert (Spec (3)), Frist trotzdem ablesbar |
| T10 frisch vs. gemergt | nur `--merged` / Reflog-Pruefung | Reflog: nur Anlage-Eintrag = `frisch`, eigene Commits alle im Hauptbranch = `gemergt` | `--merged` allein meldet jeden frischen Worktree als „aufraeumen" (plan-review 2026-09-23) |
| T11 `seit` bei Hand-off-Punkten | Hand-off-Datum / Datum der Worktree-Session | Hand-off-Datum | im Hand-off-Block eindeutig vorhanden (Kopfzeile) |
| T12 idea-rank-Anzeige | eigene Tabellenzeile / Hinweiszeile | Hinweiszeile unter der Tabelle | Tabellenvertrag „nur `Offen`" (Z. 63) bleibt |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 DSR §8 Change-Link-Pflicht — `c2176d9`
- [x] 1.2 DSR §9 Lebenslauf offener Aufgaben — `c2176d9`
- [x] 1.3 DSR §10 Worktree-Stand — `c2176d9`
- [x] 1.4 Config-Key alter_schwelle_tage — `c2176d9`
- [x] 1.5 Beispielausgaben (Abnahme-Gate) — `c2176d9`
- [x] 2.1 archive Sperre + Meldung — `b60105f`
- [x] 2.2 project-health Link-Pruefung — `b60105f`
- [x] 2.3 next/status/idea-rank als offen — `b60105f`
- [x] 2.4 idea-review Vermerk — `b60105f`
- [x] 2.5 Eigenpruefung Task-Lane — `b60105f`
- [x] 3.1 Checkpoint Vergleich
- [x] 3.2 Log Aufgaben-Abgaenge
- [x] 3.3 ⏳-Sammelvorlage
- [x] 3.4 Vertraeglichkeit der Leser
- [x] 3.5 Probe-Checkpoint
- [ ] 4.1 resume Worktree-Stand
- [ ] 4.2 next In Worktrees
- [ ] 4.3 backlog-status In Worktrees
- [ ] 4.4 Frontmatter + Doku
- [ ] 4.5 Abnahme Wegwerf-Worktree
- [ ] 4.6 Kopie-Kanon + Robustheit

---

## Umsetzung

Umsetzung mit `/dtb:implement Statusverlust-Luecken schliessen` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/statusverlust-luecken/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
