# Implementierungsplan: DERIVED_STATE

**Erstellt:** 2026-07-06
**Feature-Spec:** `features/FEATURE_DERIVED_STATE.md`
**Geschaetzte Dauer:** 3-4 Sessions
**Status:** Abgeschlossen (alle 16 Schritte umgesetzt, Success Criteria abgenommen 2026-07-06)

> **Dogfooding:** Dieser Plan enthaelt bereits die `## Progress`-Sektion, die er selbst einfuehrt. Die Umsetzung hakt dort ab (mit Commit-SHA) — kein IMPL_STATUS_DERIVED_STATE.md.

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Fundament: zentrale Ableitungsregel | ~1h | Geplant |
| Phase 2 | Schreibseite: impl-plan + feature-start | ~1h | Geplant |
| Phase 3 | Leseseite: 4 Lese-Skills umstellen | ~1-2h | Geplant |
| Phase 4 | Dashboard & Lifecycle: 8 Skills + Vorlagen | ~1-2h | Geplant |
| Phase 5 | Doku & Konsistenz: kit-weite Verifikation | ~1h | Geplant |

---

## Phase 1: Fundament — zentrale Ableitungsregel

### Ziel
Eine Referenzdatei definiert Ableitungsregel und Progress-Format, bevor irgendein Skill angefasst wird. Alle spaeteren Phasen bauen darauf auf.

### Schritte

#### Schritt 1.1: Referenzdatei DERIVED_STATE_RULES.md anlegen
- **Zweck:** Single Source fuer die Ableitungslogik — verhindert Logik-Drift zwischen den 4 Lese-Skills. Standort `project-rules/` (Review-Entscheidung): existierende Kategorie, projekt-relativ aufloesbar, wird von project-init ohnehin verteilt — kein Nicht-Skill-Verzeichnis im Skill-Baum
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (neu; Kit-Instanz = Dogfood + Vorlage fuer project-init)
- **Input:** Randfaelle + Ableitungsregeln aus `DISCOVERY_DERIVED_STATE.md`
- **Output:** Regelwerk: Artefakt-Existenz → Pipeline-Stage; Checkbox-Zaehlung → Fortschritt; Konfliktregel (Artefakt gewinnt, Widerspruch melden); Fallbacks fuer Altbestand (kein Progress / IMPL_STATUS vorhanden / 0 Checkboxen); TASK_*/BUG_*-Sonderregel (Checkliste in der Datei)

#### Schritt 1.2: Progress-Sektion-Format spezifizieren
- **Zweck:** Einheitliche Syntax, die alle Skills gleich parsen
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (ergaenzen)
- **Input:** UX-Muster aus Discovery (Checkbox-Konvention, SHA als Inline-Code)
- **Output:** Format-Spec: `- [x] 2.1 Kurzname — \`SHA\`` (SHA optional), 1 Zeile pro Schritt, Nummerierung = Plan-Schritte, max ~30 Zeilen pro Progress-Sektion; SHA-Regel fuer gebuendelte Commits: ein Commit darf mehrere Checkboxen belegen (gleiche SHA an mehreren Zeilen zulaessig)

#### Schritt 1.3: Statusmodell-Mapping definieren
- **Zweck:** Abgeleitete Zustaende muessen auf die bestehende Status-Legende abbilden (BACKLOG bleibt lesbar)
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (ergaenzen)
- **Input:** Status-Legende aus BACKLOG.md-Vorlage
- **Output:** Mapping-Tabelle: keine Artefakte→Idee; DISCOVERY→In Discovery; FEATURE ohne PLAN→Spez. erstellt; PLAN 0% →Geplant; PLAN teilweise→In Arbeit; PLAN 100%→Fertig zum Testen; Abnahme/Archiv→explizit via `/dtb:archive`

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `dtb-project/project-rules/DERIVED_STATE_RULES.md` vollstaendig (Regeln + Format + Mapping)

### Checkpoint-Kriterien
- [ ] Alle 11 Randfaelle aus der Discovery sind in den Regeln abgedeckt
- [ ] Kein Randfall fuehrt zu Abbruch — immer definierter Fallback

---

## Phase 2: Schreibseite — Statusquelle erzeugen

### Ziel
`impl-plan` erzeugt die Progress-Sektion, `feature-start` pflegt sie. IMPL_STATUS_*.md wird nirgendwo mehr erzeugt.

### Schritte

#### Schritt 2.1: impl-plan umbauen
- **Zweck:** Progress-Sektion wird Pflichtteil jedes neuen Plans; IMPL_STATUS-Konzept entfernen
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`
- **Input:** Format-Spec aus 1.2
- **Output:** PLAN-Template mit `## Progress`; IMPL_STATUS-Block ersetzt durch Handoff via Progress-Sektion; Frontmatter `produces: [PLAN_*.md]`

#### Schritt 2.2: feature-start umbauen
- **Zweck:** Abhaken (+ SHA) wird expliziter Pflichtschritt im Implementierungs-Loop — Mitigation fuer das Checkbox-Hygiene-Risiko
- **Dateien:** `skills/dtb-feature-start/SKILL.md`
- **Input:** Format-Spec aus 1.2
- **Output:** Implementierungs-Loop: nach jedem Schritt Checkbox + SHA in PLAN_*.md; Kontextverlust-Handoff ueber Progress-Sektion statt IMPL_STATUS; Frontmatter ohne IMPL_STATUS_*.md

#### Schritt 2.3: Schreibseite verifizieren
- **Zweck:** Sicherstellen, dass die Erzeugungsseite konsistent ist, bevor die Leseseite umgestellt wird
- **Dateien:** keine (Verifikation)
- **Input:** Grep ueber `skills/`
- **Output:** `IMPL_STATUS` hat in skills/ nur noch 0 Treffer (bzw. dokumentierte Alt-Referenz in Fallback-Regel); Progress-Format in beiden Skills identisch zur Referenzdatei

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] impl-plan + feature-start erzeugen/pflegen Progress statt IMPL_STATUS

### Checkpoint-Kriterien
- [ ] Kit-weit keine IMPL_STATUS-Erzeugung mehr (Success Criterion 1 der Spec, Teil 1)

---

## Phase 3: Leseseite — Status ableiten

### Ziel
Die 4 Lese-Skills leiten Status aus Artefakten ab und referenzieren die zentrale Regel-Datei.

### Schritte

#### Schritt 3.0: Test-Fixtures anlegen
- **Zweck:** Checkpoint-Kriterien der Phase 3 real pruefbar machen (Review-Empfehlung) — ohne Fixtures gibt es nichts abzuleiten
- **Dateien:** Scratchpad-Verzeichnis (Fixture-Set, nach Abnahme geloescht)
- **Input:** Format-Spec + Mapping aus Phase 1
- **Output:** Dummy-Artefakte in 4 Zustaenden: (a) FEATURE ohne PLAN, (b) PLAN 0% abgehakt, (c) PLAN 2/5 abgehakt, (d) PLAN 100% + widersprechendes BACKLOG-Feld; dazu 1 Alt-Artefakt (PLAN ohne Progress + IMPL_STATUS-Datei) fuer die Fallback-Pruefung

#### Schritt 3.1: workflow-next umstellen
- **Zweck:** Naechster Schritt aus Artefakt-Existenz + Checkboxen statt BACKLOG-Feldern
- **Dateien:** `skills/dtb-workflow-next/SKILL.md`
- **Input:** DERIVED_STATE_RULES.md
- **Output:** Skill liest PLAN-Progress, leitet naechsten offenen Schritt ab; referenziert Regel-Datei statt eigener Logik

#### Schritt 3.2: workflow-resume umstellen
- **Zweck:** Aktive Features aus Artefakten erkennen; Widersprueche melden
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md`
- **Input:** DERIVED_STATE_RULES.md
- **Output:** "In Arbeit" = abgeleitet (PLAN teilweise abgehakt); Konfliktmeldung bei Widerspruch zu BACKLOG-Feld; Report-Format aeusserlich unveraendert

#### Schritt 3.3: workflow-status + backlog-status umstellen
- **Zweck:** Pipeline-/Queue-Ansicht und Backlog-Uebersicht aus derselben Regel speisen
- **Dateien:** `skills/dtb-workflow-status/SKILL.md`, `skills/dtb-backlog-status/SKILL.md`
- **Input:** DERIVED_STATE_RULES.md, Mapping aus 1.3
- **Output:** Beide Skills leiten Stage/Status ab; backlog-status zeigt abgeleiteten Status neben manueller Prio

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 4 Lese-Skills referenzieren DERIVED_STATE_RULES.md

### Checkpoint-Kriterien
- [x] Test-Szenario (Fixture c): PLAN mit 2/5 Checkboxen, KEIN Checkpoint gelaufen → workflow-next/-resume nennen korrekt Schritt 3 (Success Criterion 3) — 2026-07-06, unabhaengiger Agent
- [x] Widerspruchs-Szenario (Fixture d): BACKLOG sagt "Geplant", PLAN ist abgehakt → Report meldet Konflikt, Artefakt gewinnt (Success Criterion 4) — 2026-07-06
- [x] Fallback-Szenario (Alt-Fixture): PLAN ohne Progress + IMPL_STATUS → "Fortschritt unbekannt" + Nachruest-Angebot, kein Abbruch (Success Criterion 5) — 2026-07-06
- [ ] Ergebnisse als kurzes Testprotokoll im Session-Log dokumentiert (Szenario → erwartet → beobachtet) — beim naechsten /dtb:workflow-checkpoint

---

## Phase 4: Dashboard & Lifecycle

### Ziel
WORKFLOW_STATUS.md wird generiert; Lifecycle-Skills und Vorlagen folgen dem neuen Modell.

### Schritte

#### Schritt 4.1: workflow-checkpoint umbauen
- **Zweck:** Status-Teil des Dashboards generieren statt formulieren; Session-Log bleibt Prosa
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** DERIVED_STATE_RULES.md, Mapping aus 1.3
- **Output:** WORKFLOW_STATUS.md-Template: generierter Statusblock (aus Artefakten) + manueller Kontextblock (Blocker, Notizen); Session-Log unveraendert. Generierungs-Anweisung woertlich im Skill vorgeben: festes Template mit definierten Feldern, die nur befuellt werden — keine freie Formulierung (Review-Empfehlung gegen Drift durch die Hintertuer)

#### Schritt 4.2: BACKLOG-Vorlage + Eintrags-Skills anpassen
- **Zweck:** Status-Spalte wird abgeleitete Anzeige; Prio/Ideen bleiben manuell
- **Dateien:** `dtb-project/project-workflows/BACKLOG.md` (Vorlage), `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-task/SKILL.md`, `skills/dtb-bug-report/SKILL.md`
- **Input:** Mapping aus 1.3
- **Output:** Vorlage kennzeichnet Status-Spalte als generiert; Eintrags-Skills setzen initialen abgeleiteten Status, pflegen ihn aber nicht weiter

#### Schritt 4.3: archive, project-init, project-health, plan-review anpassen
- **Zweck:** Restliche Lifecycle-/QS-Skills auf das neue Modell ziehen
- **Dateien:** `skills/dtb-archive/SKILL.md`, `skills/dtb-project-init/SKILL.md`, `skills/dtb-project-health/SKILL.md`, `skills/dtb-plan-review/SKILL.md`
- **Input:** DERIVED_STATE_RULES.md
- **Output:** archive: Abschluss bleibt explizite Nutzer-Entscheidung (100% Checkboxen ≠ auto-archiviert); project-init: neue Vorlagen; project-health: Drift-Checks ersetzt durch Derived-State-Checks (verwaiste Paare, Commits ohne Checkbox, IMPL_STATUS-Altlasten); plan-review: prueft Progress-Sektion auf Format-Konformitaet

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] WORKFLOW_STATUS.md-Vorlage mit generiertem Statusblock
- [ ] 8 Lifecycle-/QS-Dateien angepasst

### Checkpoint-Kriterien
- [ ] WORKFLOW_STATUS.md-Template enthaelt keine handgepflegten Statusaussagen mehr (Success Criterion 6, Teil 1)
- [ ] project-health erkennt die 3 neuen Inkonsistenz-Klassen

---

## Phase 5: Doku & Konsistenz

### Ziel
Kit-weite Doku und Pipeline-Metadaten stimmen mit dem neuen Modell ueberein; Success Criteria final verifiziert.

### Schritte

#### Schritt 5.1: Doku aktualisieren
- **Zweck:** CLAUDE.md/README beschreiben das neue Statusmodell und dtb-shared/
- **Dateien:** `CLAUDE.md`, `README.md`, `skills/CLAUDE.md`
- **Input:** Ergebnisse Phasen 1-4
- **Output:** Output-Locations ohne IMPL_STATUS, mit `project-rules/DERIVED_STATE_RULES.md`; Konventions-Abschnitt erklaert Derived State + Progress-Format

#### Schritt 5.2: Pipeline-Frontmatter kit-weit pruefen
- **Zweck:** `consumes`/`produces` aller 28 Skills konsistent (Grundlage fuer pipeline-graph)
- **Dateien:** alle betroffenen `skills/dtb-*/SKILL.md`
- **Input:** Grep `IMPL_STATUS|PLAN_\*|WORKFLOW_STATUS` ueber skills/
- **Output:** IMPL_STATUS_*.md kit-weit 0 Treffer (ausser Fallback-Doku in Regel-Datei); DERIVED_STATE_RULES.md in consumes der 4 Lese-Skills (Success Criteria 1+2+6)

#### Schritt 5.3: pipeline-graph regenerieren + Abnahme
- **Zweck:** Visueller Beleg, dass die neuen Kanten ohne Nacharbeit erscheinen
- **Dateien:** `dtb-project/claude-code-workflow-kit.html` (generiert)
- **Input:** aktualisierte Frontmatter
- **Output:** Neue Pipeline-Uebersicht; Abgleich aller 7 Success Criteria aus der Spec (Success Criterion 7); Fixtures aus 3.0 loeschen

> **3x3-Block:** Nach Schritt 5.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Doku + Frontmatter konsistent, Pipeline-Graph regeneriert

### Checkpoint-Kriterien
- [ ] Alle 7 Success Criteria aus FEATURE_DERIVED_STATE.md abgehakt

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Ort der Ableitungsregel | eigene Referenzdatei / skills/CLAUDE.md / dupliziert | eigene Referenzdatei (`skills/dtb-shared/`) | Eine Quelle, versionierbar, bei Distribution mitkopierbar (entschieden in feature-plan) |
| BACKLOG-Statusfeld | abgeleitete Anzeige / entfernen / BACKLOG abschaffen | abgeleitete Anzeige | Geringste UX-Aenderung, kein Pflege-Zwang (entschieden in feature-plan) |
| SHA-Rueckschreibung | Pflicht / optional | optional | Doku-Schritte haben keinen Commit; SHA ist Beleg, keine Buerokratie |
| Standort Regel-Datei | `project-rules/` / `skills/dtb-shared/` / beides | `project-rules/` | Existierende Kategorie, projekt-relativ aufloesbar, von project-init verteilt; kein Nicht-Skill-Verzeichnis im Skill-Baum (Plan-Review 2026-07-06) |
| Umfangs-Schnitt | alles in einem Zug / MVP Phase 1-3 + TASK | alles in einem Zug | Kein Zwischenzustand mit zwei Statusmodellen; Progress-Sektion macht Unterbrechungen resumebar (Plan-Review 2026-07-06) |
| Teststrategie Phase 3 | Fixtures + Protokoll / nur manuell | Fixtures + Testprotokoll | Schritt 3.0 liefert Fixtures; Abnahme der Success Criteria braucht Beleg statt Erinnerung (Plan-Review 2026-07-06) |
| Umgang mit IMPL_STATUS-Altlasten in Zielprojekten | ignorieren / project-health warnt | project-health warnt | Rueckwaertskompatibel lesen, aktiv auf Migration hinweisen |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand. Abhaken nach jedem Schritt, Commit-SHA als Beleg (optional bei Doku-Schritten).

- [x] 1.1 Referenzdatei DERIVED_STATE_RULES.md anlegen — `e127284`
- [x] 1.2 Progress-Sektion-Format spezifizieren — `e127284`
- [x] 1.3 Statusmodell-Mapping definieren — `e127284`
- [x] 2.1 impl-plan umbauen — `cdf7f31`
- [x] 2.2 feature-start umbauen — `cdf7f31`
- [x] 2.3 Schreibseite verifizieren — `cdf7f31`
- [x] 3.0 Test-Fixtures anlegen
- [x] 3.1 workflow-next umstellen — `a6c2828`
- [x] 3.2 workflow-resume umstellen — `a6c2828`
- [x] 3.3 workflow-status + backlog-status umstellen — `40d88d9`
- [x] 4.1 workflow-checkpoint umbauen — `669519d`
- [x] 4.2 BACKLOG-Vorlage + Eintrags-Skills anpassen — `4b18df8`
- [x] 4.3 archive, project-init, project-health, plan-review anpassen — `4b18df8`
- [x] 5.1 Doku aktualisieren — `51d3d92`
- [x] 5.2 Pipeline-Frontmatter kit-weit pruefen — `fb23c06`
- [x] 5.3 pipeline-graph regenerieren + Abnahme — `fb23c06`

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Fasse kurz zusammen was erledigt wurde
3. Beschreibe die naechsten 3 Schritte
4. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion oben ist der Wiedereinstiegspunkt — in neuer Konversation `PLAN_DERIVED_STATE.md` laden, erster nicht abgehakter Schritt ist der naechste. (Dogfooding: kein IMPL_STATUS_*.md fuer dieses Feature.)

---

**Erstellt mit:** `/dtb:impl-plan`
