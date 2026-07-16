# Implementierungsplan: impl-review

**Erstellt:** 2026-07-15
**Feature-Spec:** `features/impl-review/spec.md`
**Geschaetzte Dauer:** 6.5-8.5h (2 Sessions)
**Status:** Reviewed <!-- plan-review 2026-07-15: REVISE, 5 Empfehlungen + 2 R4-Entscheidungen eingearbeitet -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Neuer Skill `dtb:impl-review` (Gates, 3 Sub-Agents, Report, Persistenz, Triage) | 4-5h | Geplant |
| Phase 2 | Pipeline-Umverdrahtung (implement, checkpoint, workflow-status, pipeline-graph) | 0.5-1h | Geplant |
| Phase 3 | Abloesung `code-review` + Begleit-Doku (lesson, generate-rules, CLAUDE.md ×2, Regeln) | 1h | Geplant |
| Phase 4 | Sweep + Selbst-Test + SC-Abgleich | 1-1.5h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Pfade per Stichprobe verifiziert 2026-07-15). Zeilennummern = Ist-Stand.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-impl-review/SKILL.md` | Ziel-Artefakt — existiert noch nicht (Neubau) |
| `skills/dtb-code-review/SKILL.md` | 217 Zeilen; Rules-Check + Lessons-Prior (2b) + Severity×Impact + Cap 10 + Chat-Marker-Resume (6b) — Substanz wird eingefaltet, Datei entfernt |
| `skills/dtb-implement/SKILL.md` | `next: [dtb:code-review]` (Z.15); Ritual Punkt 11 Option „(3) erst Review" (Z.189); Schritt-5-Abschluss (Z.202); Abgrenzungs-Notiz nennt #20 (Z.217f); Verwandte Skills (Z.225) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | `after: [dtb:code-review]` (Z.11); Handoff-Block-Erzeuger (Empfangsseite: workflow-resume) |
| `skills/dtb-pipeline-graph/SKILL.md` | Beispiel-Flow-Zeilen mit `code-review` (Z.197-198) |
| `skills/dtb-workflow-status/SKILL.md` | Checkliste-Zeile „Code-Review durchgefuehrt" (Z.87) |
| `skills/dtb-lesson/SKILL.md` | `Applies-to`-Vokabular erlaubt `code-review` (Z.77); Header-/Hinweis-Texte Z.22, 51, 118 |
| `skills/dtb-generate-rules/SKILL.md` | 2 Verweise „code-review nutzt diese Rules" (Z.137, 153) |
| `CLAUDE.md` (Kit-Root) | 5 Stellen (Z.38, 58, 59, 92, 112) |
| `skills/CLAUDE.md` | Eligibility-Gate-Tabelle ohne impl-review-Eintrag; Frontmatter-/Distributions-Konventionen |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Datei-Tabelle des Change-Folder-Modells (Z.15-22) ohne `review.md`; §2 liefert SHA-Semantik (Konsum-Basis fuer Diff-Scope) |
| `oma-personas/persona-{principled,torvalds}-reviewer/COGNITIVE.md` | Destillat-Quellen (je §1 Kerndenken + §3 Entscheidungsfilter) — Nur-Lese, wird NICHT kopiert |

---

## Phase 1: Neuer Skill `dtb:impl-review`

### Ziel
`skills/dtb-impl-review/SKILL.md` existiert vollstaendig: Eingangs-Gates, Scope-Aufloesung ueber
Progress-SHAs, 3 Sub-Agents (Drift/Craft/Rules), Report mit 6 Verdikt-Achsen, review.md-Persistenz
mit PENDING-Resume, interaktive Triage.

### Schritte

#### Schritt 1.1: Frontmatter + Eingangs-Gates
- **Zweck:** Skill-Skelett regelkonform anlegen (Konventionen: `skills/CLAUDE.md`)
- **Dateien:** `skills/dtb-impl-review/SKILL.md` (neu)
- **Input:** Frontmatter-Konventionen; Gate-Muster aus `dtb-implement` (Hard-Gate + Archiv-Weigerung)
- **Output:** Frontmatter (`name: dtb:impl-review`, Use-when-Description, `argument-hint: "[Feature-Name oder Slug] [phase N]"`, `allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion`, pipeline: `stage: development`, `after: [dtb:implement]`, `next: [dtb:workflow-checkpoint]`, `consumes: [features/*/plan.md, features/*/spec.md, project-rules/*.md, project-rules/lessons.md, workflow.config.yaml]`, `produces: [features/*/review.md]`); Schritt 0 Config; Eligibility-Hard-Gate (kritisches Artefakt `features/{slug}/plan.md`, Redirect `/dtb:impl-plan`, Escape-Hatch); Archiv-Weigerung ohne Escape-Hatch (Muster `dtb-implement` Schritt 1.2)

#### Schritt 1.2: Scope-Aufloesung + Diff-Scope aus Progress-SHAs
- **Zweck:** Review-Gegenstand exakt bestimmen — ohne Datums-Heuristik
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** `DERIVED_STATE_RULES.md` §2 Regel 4+5 (SHA-Timing, Multi-Repo-Praefix)
- **Output:** Abschnitt: Slug + optionales `phase N` aufloesen; Plan + Spec laden; SHAs aus `## Progress` sammeln (dedupliziert, Repo-Praefixe aufloesen) → Commit-Menge → `git show`/`git diff` Dateiliste; Randfaelle: `## Progress` fehlt → melden + Nachruestung anbieten; geflippte Zeilen ohne SHA → als Scope-Luecke ausweisen (Detail in 1.4); keine SHA ermittelbar → ehrlich melden, Scope erfragen — nie raten; **Workflow-Artefakt-Ausnahme (Review-Empfehlung 3):** Aenderungen an Workflow-Artefakten (`features/{slug}/plan.md` — SHA-Rueckschreibung landet systematisch im Folge-/Checkpoint-Commit, `review.md`, `WORKFLOW_STATUS.md`, `BACKLOG.md`, `INBOX.md`, `project-changelog/**`) sind erwartete Pipeline-Nebenprodukte: aus dem Drift-Vergleich ausgenommen, im Report genau 1 Info-Zeile („{N} Workflow-Artefakte im Diff, bekannt — nicht bewertet"), nie DRIFT/EXTRA

#### Schritt 1.3: Lessons-Prior mit Legacy-Alias
- **Zweck:** Bestehende Lektionen wirken sofort weiter — ohne Datenmigration
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** Prior-Muster aus `dtb-code-review` Schritt 2b
- **Output:** Prior-Abschnitt: filtert `Applies-to` auf `impl-review`, `code-review` (Legacy-Alias, nur Lese-Seite) oder `alle`; `📚 {N} Lektion(en) beruecksichtigt`; Konflikt-Regel (zeigen, nicht aufloesen); fehlt/leer → still ueberspringen

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Sub-Agent 1 — Drift (mechanisch)
- **Zweck:** Plan↔Code-Abgleich + Gate-Beleg-Pruefung, ohne Geschmacksurteil
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** 10x-Vorbild Agent 1 (Verdikte MATCH/DRIFT/MISSING/EXTRA); §2-SHA-Semantik
- **Output:** Agent-Prompt-Block (Typ general-purpose; Kontext: „Schritte"-Texte der gepruef­ten Phasen + Diff-Dateiliste — NICHT alle Quelldateien in den Hauptkontext): pro geplantem Schritt Datei lesen, Intent vergleichen, Verdikt; ungeplante Aenderungen (EXTRA) flaggen; Pflicht-Zeile im Agent-Prompt: „Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren; du bewertest Code-Stand, nicht Testergebnisse" (Review-Empfehlung 2, belegt Spec-SC3); **SHA-Vollstaendigkeits-Check** (laeuft mechanisch im Hauptkontext, Ergebnis wird Dimension-1-Finding): geflippte Progress-Zeile ohne SHA ausserhalb der Leer-Diff-Ausnahme (§2 R4) → Hinweis „Gate nicht durchlaufen?"

#### Schritt 1.5: Sub-Agent 2 — Craft (beide Linsen-Destillate)
- **Zweck:** Handwerks-Urteil mit den zwei destillierten Reviewer-Linsen (Modell C)
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** `oma-personas/persona-principled-reviewer/COGNITIVE.md` §1+§3; `persona-torvalds-reviewer/COGNITIVE.md` §1+§3 (Nur-Lese-Quellen; Entwuerfe aus Discovery-Session)
- **Output:** EIN Agent-Prompt-Block mit zwei Linsen-Abschnitten (~8 Zeilen je, ohne Stimme/Tonfall/Risiken): **principled** (Konsistenz ueber Distanz, Prinzip-/Detail-Treue, Zeilen-Referenz + verletztes Prinzip, blocking/non-blocking/nit-Label) + **torvalds** (Abstraktions-Rechtfertigung ≥2 reale Konsumenten, Sonderfall-Eleganz, Maintainer-Lens, Kontrakt-Bruch = Blocker, Performance nur im kritischen Pfad, Geschmack als nit/taste); jedes Finding traegt sein Linsen-Label; Pflicht-Zeile im Agent-Prompt: „Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren" (Review-Empfehlung 2)

#### Schritt 1.6: Sub-Agent 3 — Rules (Regel-Abgleich)
- **Zweck:** Heutigen `code-review` als Dimension 3 einfalten
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** `dtb-code-review` Schritte 2+5 (Rules-Glob exkl. `lessons.md`, Bereichs-Zuordnung)
- **Output:** Agent-Prompt-Block: Rules aus `{config.paths.rules}/` laden (**ohne `lessons.md` und ohne `DERIVED_STATE_RULES.md`** — Status-Regelwerk, keine Coding-Rule; Review-Empfehlung 1, behebt geerbte code-review-Schwaeche), Bereichs-Zuordnung (Backend/Frontend/Test/Allgemein), nur signifikante Verstoesse mit Regel-Zitat; Pflicht-Zeile im Agent-Prompt: „Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren" (Review-Empfehlung 2); **fehlen Rules → Dimension still ueberspringen** mit 1 Statuszeile (kein Abbruch — Unterschied zu heute)

> **3x3-Block:** Nach Schritt 1.6 → Zusammenfassung + Feedback einholen

#### Schritt 1.7: Report — 6 Verdikt-Achsen
- **Zweck:** Lesbare Verdichtung der 3 Agent-Ergebnisse
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** 10x-Verdikt-Modell; Kit-Stil (Markdown, deutsch)
- **Output:** Report-Template (Markdown-Tabellen, kein Box-Drawing — Entscheidung s.u.): Achsen-Tabelle Plan Adherence · Scope Discipline · Safety & Quality · Architecture · Pattern Consistency · Rules (je PASS/WARNING/FAIL + Findings-Zahl); Gesamt-Verdikt APPROVED / NEEDS ATTENTION / REJECTED; Findings mit ID (F1…), Severity×Impact (Doppelachse wie heute), Dimension, Linsen-/Agent-Herkunft, Fundstelle, genau 1 Fix-Option (2 nur bei echtem Tradeoff, eine als Empfehlung markiert); global sortiert Severity vor Impact, **Cap 10** + 1 Zeile Rest-Zaehler

#### Schritt 1.8: review.md-Persistenz + PENDING-Schutz
- **Zweck:** Triage-Stand lebt im Artefakt, nicht im Chat
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** 10x-Report-Persistenz (`Decision: PENDING`); Change-Folder-Modell (fixe Dateinamen)
- **Output:** Abschnitt: bei ≥1 Finding nach der Dreiwahl „Triage jetzt / Speichern & spaeter / Nur speichern" → `features/{slug}/review.md` schreiben (Header: Scope, Datum, geprueft-bis-SHA; pro Finding `Decision: PENDING`); **0 Findings → keine Datei**, nur Konsolen-Verdikt; Ueberschreib-Schutz: existiert review.md mit PENDING-Eintraegen → warnen + bestaetigen lassen; Resume: Aufruf bei vorhandener review.md bietet Weiter-Triage der PENDING-Findings an

#### Schritt 1.9: Triage-Loop + Lektion-Anschluss
- **Zweck:** Findings entscheidbar machen — Fix, Skip oder Lektion
- **Dateien:** `skills/dtb-impl-review/SKILL.md`
- **Input:** 10x-Triage (AskUserQuestion, Pre-Fill-Lesson-Flow); `/dtb:lesson`-Schnittstelle
- **Output:** Triage-Abschnitt: pro Finding (Severity-Reihenfolge) AskUserQuestion mit Fix anwenden / anders fixen / Skip / als Lektion erfassen; Fix nur nach expliziter Wahl (Vorschau vor Edit); Lektion: Context/Problem aus Finding vorbefuellen → `/dtb:lesson`-Uebergabe, danach Pflicht-Rueckfrage „Fix trotzdem anwenden?"; jede Entscheidung aktualisiert `Decision:` in review.md; Abschluss-Summary (Fixed/Lesson/Skipped); kein Commit (Verweis auf Nutzer bzw. kuenftig #21)

### Deliverables
- [ ] `skills/dtb-impl-review/SKILL.md` vollstaendig (Gates → Scope → Prior → 3 Agents → Report → Persistenz → Triage)

### Checkpoint-Kriterien

#### Automated
- [ ] Datei existiert: `skills/dtb-impl-review/SKILL.md`
- [ ] Grep Frontmatter: `name: dtb:impl-review` ∧ `Agent` und `AskUserQuestion` in der allowed-tools-Zeile ∧ `after: [dtb:implement]` ∧ `produces: [features/*/review.md]`
- [ ] Grep im SKILL.md: beide Linsen-Marker („principled" ∧ „torvalds"), alle 6 Achsen-Namen, `Decision: PENDING`, `MATCH`/`DRIFT`/`MISSING`/`EXTRA`
- [ ] Grep im SKILL.md: Legacy-Alias-Zeile (`code-review` im Lessons-Prior-Abschnitt, markiert „Legacy")
- [ ] Grep im SKILL.md: Kommando-Verbots-Zeile („Nur lesen — keine Kommandos") in allen 3 Agent-Prompt-Bloecken (≥3 Fundstellen)

#### Manual
- [ ] Linsen-Destillate tragen Review-Substanz (Kerndenken + Filter), keine Stimme/Tonfall-Anteile
- [ ] Report-/Triage-Fluss liest sich schluessig und kompakt (Kit-Stil, deutsch)

---

## Phase 2: Pipeline-Umverdrahtung

### Ziel
Alle 3 Vorschlags-Stellen zeigen auf `impl-review`; Pipeline-Frontmatter konsistent — kein
Zeitfenster mit widerspruechlichen Nachfolger-Zeigern.

### Schritte

#### Schritt 2.1: `dtb-implement` umbiegen
- **Zweck:** Vorschlags-Stellen 1+2 (nach letzter Phase; Ritual Punkt 11)
- **Dateien:** `skills/dtb-implement/SKILL.md`
- **Input:** Ist-Befunde Z.15/189/202/217f/225
- **Output:** `next: [dtb:impl-review]`; Punkt 11 Option „(3) erst Review (`/dtb:impl-review`)"; Schritt-5-Abschluss empfiehlt `/dtb:impl-review` VOR dem Checkpoint-Verweis; Abgrenzungs-Notiz aktualisiert (code-review-Satz raus, #20 als umgesetzt); Verwandte Skills: `code-review`-Zeile → `impl-review`

#### Schritt 2.2: `dtb-workflow-checkpoint` umbiegen (Vorschlags-Stelle 3)
- **Zweck:** Der Vorschlag ueberlebt den Session-Bruch (Handoff → Status-Datei → resume)
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Ist-Befund Z.11; Handoff-Block-Mechanik des Skills
- **Output:** `after: [dtb:impl-review]`; Handoff-Regel ergaenzt (zweistufig, R4-Entscheidung): Feature „Fertig zum Testen" ∧ keine `features/{slug}/review.md` → `**Naechster Befehl:** /dtb:impl-review {slug}`; existiert `review.md` mit Gesamt-Verdikt REJECTED → `**Naechster Befehl:** /dtb:implement {slug}` (Rueckweg zur Nacharbeit, danach frisches Review)

#### Schritt 2.3: Uebersichts-Skills nachziehen
- **Zweck:** Lektion 3 — Uebersichts-Skills referenzieren ausserhalb der Frontmatter
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`, `skills/dtb-workflow-status/SKILL.md`
- **Input:** Ist-Befunde Z.197-198 bzw. Z.87
- **Output:** Flow-Beispielzeilen und Checklisten-Zeile nennen `impl-review` statt `code-review`

### Deliverables
- [ ] 4 Skills konsistent auf `impl-review` verdrahtet

### Checkpoint-Kriterien

#### Automated
- [ ] Grep `next: [dtb:impl-review]` in `skills/dtb-implement/SKILL.md` ∧ `after: [dtb:impl-review]` in `skills/dtb-workflow-checkpoint/SKILL.md` (Frontmatter-Anker)
- [ ] Grep `dtb:code-review` in den 4 Dateien dieser Phase → 0 Treffer
- [ ] Grep `/dtb:impl-review` in `dtb-implement` ≥ 2 Fundstellen (Punkt 11 + Schritt 5)

---

## Phase 3: Abloesung `code-review` + Begleit-Doku

### Ziel
`code-review` existiert nicht mehr im Repo; Vokabular, Gate-Tabelle, Regeln und beide CLAUDE.md
sind nachgezogen.

### Schritte

#### Schritt 3.1: `dtb-lesson` + `dtb-generate-rules` nachziehen
- **Zweck:** Schreib-Vokabular wechselt; Rules-Konsument heisst jetzt impl-review
- **Dateien:** `skills/dtb-lesson/SKILL.md`, `skills/dtb-generate-rules/SKILL.md`
- **Input:** Ist-Befunde (lesson Z.22/51/77/118; generate-rules Z.137/153)
- **Output:** lesson: erlaubte `Applies-to`-Werte = `impl-plan, debug-plan, plan-review, impl-review, alle` + 1 Hinweis „`code-review` (Legacy) wird lesend weiter akzeptiert, nicht neu vergeben"; Header-/Vorschlag-Texte auf impl-review; generate-rules: beide Verweise auf `/dtb:impl-review`

#### Schritt 3.2: Kit-CLAUDE.md + skills/CLAUDE.md nachziehen
- **Zweck:** Doku beschreibt die neue Pipeline; Gate-Konvention kennt impl-review
- **Dateien:** `CLAUDE.md`, `skills/CLAUDE.md`
- **Input:** Ist-Befunde (5 Stellen; Gate-Tabelle)
- **Output:** CLAUDE.md: Workflow-Satz, Kategorien-Zeile, lessons-Prior-Listen (×2), Rules-Konsument → impl-review; skills/CLAUDE.md: Gate-Tabellen-Eintrag `impl-review | features/*/plan.md | impl-plan (nach Selbst-Ausschluss; zusaetzlich harte Archiv-Weigerung)`

#### Schritt 3.3: DERIVED_STATE_RULES — review.md status-neutral
- **Zweck:** Neue Ordner-Datei darf die Ableitung nicht kippen
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** Datei-Tabelle Z.15-22; §1.1
- **Output:** `review.md`-Zeile in der Datei-Tabelle („Review-Report, status-neutral — zaehlt NICHT fuer die Ableitung nach 1.1") + Fussnote „ergaenzt mit Feature impl-review, 2026-07-15"; Hinweis im Commit/Session-Log: Seed-Aenderung erreicht Bestandsprojekte nicht automatisch (INBOX #22, dort loesen)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: `skills/dtb-code-review/` entfernen
- **Zweck:** Abloesung vollziehen — erst jetzt, nachdem alle Zeiger umgebogen sind
- **Dateien:** `skills/dtb-code-review/SKILL.md` (git rm)
- **Input:** Phasen 1-3 abgeschlossen (kein aktiver Verweis mehr)
- **Output:** Ordner entfernt; installierte Kopien meldet `dtb:kit-sync check` als „verwaist" (Entfernen mit Bestaetigung — Mechanik existiert, S1 2026-07-15 verifiziert)

### Deliverables
- [ ] `code-review` restlos abgeloest (Skill weg, Doku/Vokabular/Regeln nachgezogen)

### Checkpoint-Kriterien

#### Automated
- [ ] Glob `skills/dtb-code-review/**` → 0 Treffer
- [ ] Grep `impl-review` in der `Erlaubte Werte`-Zeile von `dtb-lesson` ∧ Legacy-Hinweis vorhanden
- [ ] Grep `review.md` in der Datei-Tabelle von `DERIVED_STATE_RULES.md`
- [ ] Grep `impl-review` in der Gate-Tabelle von `skills/CLAUDE.md` ∧ kein `code-review` mehr in `CLAUDE.md` (Kit-Root)

---

## Phase 4: Sweep + Selbst-Test + SC-Abgleich

### Ziel
Kein vergessener aktiver Verweis; der Skill funktioniert auf einem echten Feature; alle
Spec-Kriterien belegt.

### Schritte

#### Schritt 4.1: Konsistenz-Sweep (praezise geankert)
- **Zweck:** Risiko „vergessene Referenz" mechanisch ausschliessen (Lektion 2: Anker statt Stichwort)
- **Dateien:** keine (read-only)
- **Input:** Sweep-Definition: `dtb:code-review|dtb-code-review` ueber `skills/**`, `agents/**`, `commands/**`, `CLAUDE.md`, `skills/CLAUDE.md`
- **Output:** 0 unzulaessige Treffer. Zulaessig sind NUR Zeilen mit explizitem „Legacy"-Kontext (Alias in `dtb-impl-review`, Hinweis in `dtb-lesson`). Historie bleibt bewusst unangetastet: `INBOX.md`, `project-changelog/**`, `archive/**`, `features/impl-review/**`, `WORKFLOW_STATUS.md`-Meilensteine

#### Schritt 4.2: Selbst-Test auf echtem Feature
- **Zweck:** Der Skill beweist sich am eigenen Repo (Spec-SC 10)
- **Dateien:** ggf. `features/verifikations-gate/review.md` (Testlauf-Artefakt)
- **Input:** `/dtb:impl-review verifikations-gate` — 18/18 umgesetzt, SHAs vorhanden (ideale Testbasis fuer Diff-Scope aus Progress-SHAs)
- **Output:** Report mit 6 Achsen-Verdikten; Drift-Verdikte nachvollziehbar; bei nicht ermittelbarem Teil-Scope ehrliche Meldung statt Erfindung; Triage-Anlauf (mind. 1 Finding durchspielen oder 0-Findings-Pfad belegen); **Zweittest PENDING-Schutz (Review-Empfehlung 4):** bei Findings Triage bewusst NICHT abschliessen (≥1 PENDING stehen lassen) → zweiter Aufruf direkt danach → erwartet: Warnung + Bestaetigungs-Frage statt stillem Ueberschreiben; bei 0 Findings entfaellt der Zweittest ehrlich als „nicht ausloesbar" (Vermerk in 4.3, nicht uebersprungen)

#### Schritt 4.3: SC-Abgleich + offene Punkte schliessen
- **Zweck:** Spec-Erfuellung explizit belegen
- **Dateien:** `features/impl-review/spec.md` (nur Abgleich, kein Umbau)
- **Input:** 10 Success Criteria der Spec; Testlauf-Ergebnis aus 4.2
- **Output:** Punkt-fuer-Punkt-Abgleich (Beleg je Kriterium); die 3 „Offenen Punkte" der Spec als entschieden dokumentiert (Layout: Markdown; produces: ja; Destillate: final); Abweichungen als Mismatch melden, nicht still anpassen; **Abnahme-Hinweis (R4-Entscheidung):** nach Phase 4 ist der Status „Fertig zum Testen" — „Abgenommen" erst nach erstem echten Einsatz im Zielprojekt (pkp), wie beim Verifikations-Gate

### Deliverables
- [ ] Sweep gruen, Selbst-Test-Report vorhanden, SC-Abgleich dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] Sweep-Grep (Anker wie 4.1) → 0 unzulaessige Treffer
- [ ] Selbst-Test hat einen Report erzeugt (Konsole; bei Findings zusaetzlich `features/verifikations-gate/review.md`)

#### Manual
- [ ] Selbst-Test-Report plausibel: Verdikte nachvollziehbar, Craft-Findings substanziell (kein Geschmacks-Noise), keine Erfindungen
- [ ] SC-Abgleich: alle 10 Spec-Kriterien mit Beleg gruen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Report-Layout | Box-Drawing (10x) / Markdown-Tabellen (Kit) | Markdown | Kit-Konsistenz (alle dtb-Reports sind Markdown); Box-Drawing bricht bei Umbruch/Rendering; loest offenen Spec-Punkt |
| Craft-Agent-Schnitt | 1 Agent mit 2 Linsen / 2 getrennte Agents | 1 Agent, 2 Linsen-Abschnitte | Ein kohaerenter Craft-Befund, halbe Agent-Kosten; Linsen-Label pro Finding erhaelt die Blickwinkel-Trennung |
| Sub-Agent-Typ | general-purpose / Spezial-Typ | general-purpose | 10x-Vorbild; keine Spezial-Agents im Kit-Kontext verfuegbar |
| `produces`-Eintrag | mit / ohne `features/*/review.md` | mit | pipeline-graph/workflow-status lesen Frontmatter; review.md ist echtes Output-Artefakt; loest offenen Spec-Punkt |
| Entfernungs-Zeitpunkt code-review | frueh (Phase 1) / spaet (Phase 3 Ende) | spaet (3.4) | Kein Zeitfenster, in dem die Pipeline auf einen geloeschten Skill zeigt |
| Rules-Glob-Ausschluss | nur lessons.md / + DERIVED_STATE_RULES.md | + DERIVED_STATE_RULES.md | Status-Regelwerk ist keine Coding-Rule; verhindert Schein-Findings (plan-review Empfehlung 1) |
| REJECTED-Handoff | immer impl-review / Rueckweg | Rueckweg (`/dtb:implement`) | Nacharbeit vor erneutem Review; Verdikt steuert den Handoff (R4 Architekt) |
| Abnahme-Kriterium | Selbst-Test genuegt / Realeinsatz | Realeinsatz (pkp) | Konsistent zum Verifikations-Gate; Selbst-Test belegt nur „Fertig zum Testen" (R4 Pragmatiker) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Frontmatter + Eingangs-Gates — `fb0310d`
- [x] 1.2 Scope-Aufloesung + Diff-Scope aus SHAs — `fb0310d`
- [x] 1.3 Lessons-Prior mit Legacy-Alias — `fb0310d`
- [x] 1.4 Sub-Agent Drift + SHA-Check — `fb0310d`
- [x] 1.5 Sub-Agent Craft (2 Linsen-Destillate) — `fb0310d`
- [x] 1.6 Sub-Agent Rules (still ueberspringbar) — `fb0310d`
- [x] 1.7 Report mit 6 Verdikt-Achsen — `fb0310d`
- [x] 1.8 review.md-Persistenz + PENDING-Schutz — `fb0310d`
- [x] 1.9 Triage-Loop + Lektion-Anschluss — `fb0310d`
- [x] 2.1 implement umbiegen (2 Vorschlags-Stellen)
- [x] 2.2 workflow-checkpoint umbiegen (Handoff)
- [x] 2.3 pipeline-graph + workflow-status nachziehen
- [ ] 3.1 lesson-Vokabular + generate-rules
- [ ] 3.2 CLAUDE.md ×2 nachziehen
- [ ] 3.3 DERIVED_STATE_RULES: review.md neutral
- [ ] 3.4 code-review entfernen (git rm)
- [ ] 4.1 Konsistenz-Sweep (geankert)
- [ ] 4.2 Selbst-Test auf verifikations-gate
- [ ] 4.3 SC-Abgleich + offene Punkte

---

## Umsetzung

Umsetzung mit `/dtb:implement impl-review` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/impl-review/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
