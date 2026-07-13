# Implementierungsplan: Greenfield-Autoren-Skills

**Erstellt:** 2026-07-13
**Feature-Spec:** `features/greenfield-autoren-skills/spec.md`
**Geschaetzte Dauer:** ~12-14 h (4 Phasen, 2-3 Sessions im 3x3-Rhythmus)
**Status:** Reviewed <!-- plan-review 2026-07-13: REVISE, 3 WARN → alle 5 Empfehlungen eingearbeitet -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | greenfield-prd → Autor (Interview, Template, Lint, Kollision) | ~3,5 h | Geplant |
| Phase 2 | greenfield-roadmap → Autor (Gate, Stack-Besprechung, Lean-Interview, Slices) | ~4 h | Geplant |
| Phase 3 | Derived-State-Integration (§5 + workflow-checkpoint-Sync) | ~1 h | Geplant |
| Phase 4 | Umfeld, statische Prüfung, blinde Fixtures, kit-sync (zweistufige Abnahme) | ~3,5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` `## Betroffene Module` (📂 übernommen, 8 Pfade per Glob verifiziert 2026-07-13);
> ergänzt um 2 Dateien aus den verifizierten Integrationspunkten der Discovery (3e).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-greenfield-prd/SKILL.md` | 198 Z., read-only-Report (`produces: []`, `disable-model-invocation: false`); Report-Template mit verschachtelten Code-Fences; liest `project-strategy/PRD-MVP.md` |
| `skills/dtb-greenfield-roadmap/SKILL.md` | 235 Z., read-only; hat bereits vertikale Slices/Foundations-mit-Unlocks/Selbst-Review-Checkliste (skill-10x Block 3) — wird zum Autoren-Template weiterentwickelt; kein Fallback bei fehlender ROADMAP.md; Template führt `Zeitraum`-Felder + Ressourcen-Tabelle (entfallen) |
| `skills/dtb-pipeline-graph/SKILL.md` | Artefakt-Legende Z. ~264-269 führt PRD-MVP.md/ROADMAP.md mit Ort; TECH-STACK.md fehlt; liest `produces`-Frontmatter |
| `skills/dtb-workflow-status/SKILL.md` | Liest Pipeline-Frontmatter (stage/after/next) für Flow-Visualisierung; sonst unberührt |
| `skills/dtb-project-health/SKILL.md` | Check Z. ~142: UPPER_SNAKE_CASE nur „direkt in" `project-strategy/` — `archive/`-Unterordner kollidiert nicht |
| `skills/dtb-docs-extract/SKILL.md` | Schreibt thematische UPPER_SNAKE_CASE-MDs nach `project-strategy/` — Quellmaterial fürs PRD-Interview (nur lesen, kein Edit an docs-extract) |
| `skills/CLAUDE.md` | Frontmatter-Pflichtfelder, Eligibility-Gate-Konvention + Hard-Gate-Tabelle (v1) — Roadmap-Gate auf PRD-MVP.md dort nachtragen |
| `README.md` (+ Root-`CLAUDE.md`) | README Z. 97-98 verspricht bereits „Generate product requirements/roadmap" — Beschreibungen werden nach dem Umbau ehrlich |
| `skills/dtb-workflow-checkpoint/SKILL.md` (aus 3e) | Schritt 2 „Status ableiten & Anzeige-Felder synchronisieren" = Sync-Stelle; `consumes`/`produces` um ROADMAP.md erweitern |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` (aus 3e) | §3 Anzeige-Muster (Vorbild für §5), §4 Slug-Regeln (Change-ID-Ableitung + Kollisions-Abbruch); endet bei §4 → neuer §5 |

---

## Phase 1: greenfield-prd → Autor

### Ziel
`greenfield-prd` wird Zwei-Modus-Skill: Report-Modus (PRD existiert) bleibt, Autoren-Modus (PRD fehlt) führt das gründliche Interview und generiert ein technikfreies `PRD-MVP.md`.

### Schritte

#### Schritt 1.1: Modus-Weiche + Frontmatter + Quellmaterial
- **Zweck:** Grundgerüst des Umbaus; Skill entscheidet am Eingang, welcher Modus läuft
- **Dateien:** `skills/dtb-greenfield-prd/SKILL.md`
- **Input:** discovery.md (Scope), heutige SKILL.md
- **Output:** Frontmatter (`disable-model-invocation: true`, `produces: [PRD-MVP.md]`, description mit neuen Triggern); **dreistufige Weiche mit explizitem Vorrang-Satz** (plan-review Empf. 1, L5): (1) `PRD-MVP.md` mit `<!-- resume: … -->`-Marker ≠ `done` → **Interview fortsetzen — hat Vorrang vor der Existenz-Regel**; (2) PRD vorhanden ohne Marker/`done` → Report-Modus (bestehende Schritte 1-3, gestraffte Code-Fences); expliziter Neuerzeugungs-Wunsch → Kollisions-Dialog (1.4); (3) PRD fehlt → Autoren-Modus neu. Kein vierter Zweig (kein Auto-Wiederöffnen bei hohlem PRD). Autoren-Modus beginnt mit Quellmaterial-Angebot: Glob `project-strategy/*.md` (ohne PRD/ROADMAP/TECH-STACK) + INBOX-Ideen einlesen, Funde anbieten

#### Schritt 1.2: Interview-Phasen + Resume-Marker + Thin-Input-Warnung
- **Zweck:** Das gründliche, unterbrechbare Produkt-Interview (Kern des Autoren-Modus)
- **Dateien:** `skills/dtb-greenfield-prd/SKILL.md`
- **Input:** 10x-shape als Konzeptions-Vorbild; Resume-Muster aus feature-discover
- **Output:** Interview-Kategorien (Entscheidung B): (a) Vision/Problem, (b) Zielgruppen/Personas, (c) Feature-Priorisierung Must/Should/Nice, (d) User Stories + Akzeptanzkriterien, (e) NFRs, (f) Scope-Abgrenzung/Out-of-Scope. Nach jeder Kategorie Entwurf mit `<!-- resume: {Kategorie} -->` in `PRD-MVP.md` speichern; Wiedereinstieg ohne Doppelfragen. Thin-Input-Warnung: liefert eine Kategorie fast nichts, fehlendes Signal + Konsequenz konkret benennen, „Trotzdem weiter" erlaubt

#### Schritt 1.3: PRD-Template + „Nie erfinden"-Hard-Rule
- **Zweck:** Das erzeugte Artefakt strukturell festlegen — kompatibel zum Report-Modus
- **Dateien:** `skills/dtb-greenfield-prd/SKILL.md`
- **Input:** heutiges Report-Format (Entscheidung A: Strukturkontinuität)
- **Output:** PRD-MVP.md-Template (deutsch, technikfrei): Vision/Erfolgskriterien, Zielgruppen, Must/Should/Nice, User Stories, NFRs, Out of Scope, Abhängigkeiten, Risiken + NEU `## Open Questions`. Hard-Rule im Skill-Text: fehlende Inhalte landen wörtlich als nummerierte Open Questions — nie plausibel auffüllen. Gegen-Hinweis Format-Kopplung: „Sektionsnamen werden von greenfield-roadmap geparst"

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Selbst-Review + Kollisions-Dialog + Hand-off
- **Zweck:** Schreibschutz-Mechanik: nichts Fehlerhaftes landet auf Platte, Historie bleibt erhalten
- **Dateien:** `skills/dtb-greenfield-prd/SKILL.md`, `skills/dtb-feature-plan/SKILL.md` (nur Gegen-Hinweis)
- **Input:** Leak-Lint-Kategorien aus feature-plan (7 Kategorien, bewusste Kopie), Archivkonvention aus discovery
- **Output:** Selbst-Review VOR Write: Struktur-Check (alle Template-Sektionen, Reihenfolge) + Technical-Leak-Lint mit konstruktivem Redirect „gehört in TECH-STACK.md" → Verstoß = Abbruch ohne Write, konkreter Befund. Kollisions-Dialog bei explizitem Neuerzeugen: „Archivieren + ersetzen (Recommended) / Überschreiben / Abbrechen", Archiv `project-strategy/archive/YYYY-MM-DD-PRD-MVP.md` (Zweitlauf `-2`), Ordner lazy, Nicht-Git = einfacher Move. Hand-off: Empfehlung `/dtb:greenfield-roadmap`, kein Auto-Chaining. Lint-Kopie beidseitig markieren (plan-review Empf. 5): Gegen-Hinweis in `feature-plan` („Kategorien-Kopie in greenfield-prd — bei Änderung mitdenken") + Gegenrichtung in greenfield-prd

### Deliverables
- [ ] `skills/dtb-greenfield-prd/SKILL.md` als Zwei-Modus-Autor, ≤ ~350 Z.

### Checkpoint-Kriterien
- [ ] SC1/SC2/SC3-Mechanik im Skill-Text vollständig (Interview+Resume, Report+Kollision, Quellmaterial+Lint)
- [ ] **Budget-Messpunkt (plan-review Empf. 3):** Zeilenzahl `greenfield-prd` gemessen; >350 → SOFORT entscheiden (Budget erhöhen vs. kürzen vs. Folge-Idee kit-sync-references), BEVOR Phase 2 nach demselben Muster gebaut wird

---

## Phase 2: greenfield-roadmap → Autor

### Ziel
`greenfield-roadmap` wird Autor: Gate auf PRD, Stack-Besprechung → TECH-STACK.md, Lean-Interview, vertikale Slices mit Change-IDs, ROADMAP.md mit abgeleiteter Statusspalte.

### Schritte

#### Schritt 2.1: Frontmatter + Eligibility-Gate + Readiness-Check
- **Zweck:** Sauberer Eingang: ohne PRD kein Roadmap-Lauf, hohles PRD wird benannt
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`, `skills/CLAUDE.md` (Hard-Gate-Tabelle ergänzen)
- **Input:** Gate-Muster aus skills/CLAUDE.md; Readiness-Heuristik (Entscheidung C)
- **Output:** Frontmatter (`disable-model-invocation: true`, `produces: [ROADMAP.md, TECH-STACK.md]`, `next: [dtb:feature-discover]`); Hard-Gate: `project-strategy/PRD-MVP.md` fehlt → ⛔ Redirect `/dtb:greenfield-prd` + Escape-Hatch. Readiness-Check (4 Signale à 1 Punkt: Vision nicht-trivial ∧ ≥1 User Story ∧ ≥1 Must-Have-Feature ∧ Out-of-Scope befüllt; Schwelle ≥3): darunter Warnung mit fehlenden Signalen + „Trotzdem fortfahren"-Escape

#### Schritt 2.2: Stack-Besprechung → TECH-STACK.md
- **Zweck:** Der schlanke Ersatz für 10x-Glied 3 — Stack-Entscheidungen bekommen ein Zuhause, das PRD bleibt technikfrei
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** discovery (Zuschnitt 1)
- **Output:** Schritt im Skill: `TECH-STACK.md` vorhanden → Skip-Zeile `📂 TECH-STACK.md vorhanden → Besprechung übersprungen` + konsumieren; fehlt → kompakte Besprechung (Team-Skills, Sprach-/Framework-Präferenzen, Avoid-List, Deployment-Ziel; 4-6 Fragen) → Living Doc `project-strategy/TECH-STACK.md` (edit-in-place, kein Archivdialog — Entscheidung D)

#### Schritt 2.3: Lean-Interview + Slice-Zerlegung
- **Zweck:** Das Herzstück: PRD → sequenzierte vertikale Slices
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** 10x-roadmap Step 5/6 als Vorbild (stark komprimiert); DERIVED_STATE_RULES §4
- **Output:** Lean-Interview: max. 3 Ankerfragen (Hauptziel, North-Star-Slice, Top-Blocker), jede mit „(Recommended)" aus Artefakt-Zitat + 1-2 begründeten Alternativen; Investment-Schwerpunkte abgeleitet, nicht erfragt. Zerlegung: vertikale Slices („Nutzer kann …", jede Schicht), Foundations nur mit benanntem Unlocks; Prerequisites-Graph statt Zeitschätzung; externe Termine als Constraints erlaubt; Change-ID je Item §4-konform (kebab-case, Kollisions-Abbruch)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: ROADMAP-Template + Selbst-Review + Kollision + Hand-off
- **Zweck:** Artefakt-Format + Schreibschutz + Brücke in die Change-Pipeline
- **Dateien:** `skills/dtb-greenfield-roadmap/SKILL.md`
- **Input:** bestehende Slices/Foundations/Selbst-Review-Teile (skill-10x Block 3) als Basis
- **Output:** ROADMAP.md-Template: Vision-Recap, At-a-glance-Tabelle (ID, Change-ID, Outcome, Prerequisites, Status), Foundations/Slices-Blöcke, externe Termine, `## Open Roadmap Questions`; Status-Vokabular einheitlich englisch `proposed / ready / blocked / in-progress / done` (Entscheidung F) mit einer Legenden-Zeile, die die 5 Werte einmal deutsch erklärt; Statusspalte mit Hinweis „abgeleitete Anzeige — nicht manuell pflegen (DERIVED_STATE_RULES §5)"; `Zeitraum`-Felder + Ressourcen-Tabelle entfernt. Selbst-Review VOR Write (Sektionen, jeder Slice mit PRD-Bezug, Change-ID-Eindeutigkeit, kein Slice ohne Outcome) → Verstoß = Abbruch. Kollisions-Dialog wie 1.4 (ROADMAP-Variante). Hand-off: genau EIN Befehl `/dtb:feature-discover <change-id>` mit 1-Zeilen-Begründung; Gegen-Hinweis Format-Kopplung Richtung PRD-Template

### Deliverables
- [ ] `skills/dtb-greenfield-roadmap/SKILL.md` als Autor, ≤ ~350 Z.
- [ ] `skills/CLAUDE.md` Hard-Gate-Tabelle um Roadmap-Gate ergänzt

### Checkpoint-Kriterien
- [ ] SC4/SC5/SC6-Mechanik im Skill-Text vollständig (Gate+Readiness, Stack-Besprechung+Skip, Lean-Interview+Slices+Hand-off)

---

## Phase 3: Derived-State-Integration

### Ziel
Roadmap-Status ohne Drift: Ableitungsregel zentral definiert, Sync-Stelle verdrahtet.

### Schritte

#### Schritt 3.1: DERIVED_STATE_RULES.md §5 „Roadmap-Ableitung"
- **Zweck:** Zentrale Regel (Single Source), auf die Skill-Texte nur verweisen
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** §3 (Anzeige-Muster) als Vorlage; discovery 3d
- **Output:** Neuer §5: Change-ID = Feature-Slug (§4); Ableitungstabelle (kein Ordner → Doc-Status `proposed`/`ready`/`blocked` gilt; `features/<slug>/` existiert → `in-progress`; `archive/<slug>/` → `done`) — Vokabular einheitlich englisch (Entscheidung F); Statusspalte = abgeleitete Anzeige; Konfliktregel §1.3 gilt analog

#### Schritt 3.2: workflow-checkpoint um ROADMAP-Sync erweitern
- **Zweck:** Die Schreib-Seite der Ableitung — gleiche Mechanik wie BACKLOG-Spalte
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** dortiger Schritt 2 (bestehende Sync-Liste)
- **Output:** Schritt 2 ergänzt: „Falls `project-strategy/ROADMAP.md` existiert: Statusspalte nach §5 synchronisieren" (sonst still überspringen); Frontmatter `consumes`/`produces` um ROADMAP.md erweitert. Minimal-invasiv, keine weiteren Checkpoint-Änderungen

### Deliverables
- [ ] §5 in DERIVED_STATE_RULES.md; workflow-checkpoint synct ROADMAP-Spalte

### Checkpoint-Kriterien
- [ ] SC8-Mechanik vollständig (Regel + Sync-Stelle, nur-wenn-existiert)

---

## Phase 4: Umfeld + Verifikation

### Ziel
Konsistentes Umfeld, belegte Success Criteria (statisch + blinde Fixtures); Abschluss bei „Fertig zum Testen" (zweistufige Abnahme, Entscheidung G).

### Schritte

#### Schritt 4.1: pipeline-graph + README/CLAUDE.md
- **Zweck:** Umfeld kennt die neuen Artefakte und ehrlichen Beschreibungen
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`, `README.md`, `CLAUDE.md`
- **Input:** Artefakt-Legende (Z. ~264-269)
- **Output:** Legende + TECH-STACK.md; README/CLAUDE.md-Beschreibungen der beiden Skills aktualisiert (Autoren-Verhalten, Zwei-Modus)

#### Schritt 4.2: Statische Selbstprüfung
- **Zweck:** SC9 mechanisch belegen, bevor Agenten laufen
- **Dateien:** — (read-only Prüfung)
- **Input:** beide SKILL.md, Frontmatter, Gegen-Hinweise
- **Output:** Belegt: Zeilenzahlen ≤ ~350, `disable-model-invocation: true`, `produces` korrekt, `next`-Kette, Gegen-Hinweise beidseitig, Hard-Gate-Tabelle aktuell, project-health-Konformität (UPPER_SNAKE_CASE)

#### Schritt 4.3: Blinde Fixture-Läufe (SC1-SC8)
- **Zweck:** Verhaltensecht verifizieren, unabhängig vom Autor-Kontext
- **Dateien:** Scratchpad-Fixtures (Projektstruktur mit workflow.config.yaml + project-strategy/-Varianten)
- **Input:** Fixtures: (a) leer → Interview SC1; (b) PRD vorhanden → Report + Kollisions-Dialog SC2; (c) Strategie-MDs + INBOX → Quellmaterial SC3; (d) kein PRD → Roadmap-Gate SC4; (e) hohles PRD → Readiness SC4; (f) TECH-STACK vorhanden/fehlt → SC5; (g) PRD gut → Slices/Lean-Interview SC6; (h) präparierter Leak/Struktur-Verstoß → Abbruch SC7; (i) archive/<slug>-Fixture + Checkpoint → SC8
- **Output:** Blinde Agenten-Läufe (nur Skill + Fixture, kein Feature-Kontext), PASS/FAIL je SC dokumentiert; Negativ-Kontrollen inklusive (kein Fehlalarm)

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

#### Schritt 4.4: kit-sync + SC-Abschluss (zweistufige Abnahme)
- **Zweck:** Verteilen und Feature-Stand ehrlich abschließen (plan-review Empf. 4: kein künstlicher Praxistest — der wäre nur die zehnte Fixture)
- **Dateien:** `~/.claude/skills/…` via `/dtb:kit-sync`; `features/greenfield-autoren-skills/spec.md`
- **Input:** verteilter Stand, Fixture-Ergebnisse aus 4.3
- **Output:** kit-sync sync (Lock aktualisiert, pitch-coach weiter gehalten); SC-Boxen in spec.md mit Fixture-/Grep-Belegen abhaken. **Zweistufige Abnahme (Nutzer-Entscheidung 2026-07-13):** Feature endet hier bei „Fertig zum Testen" — die echte Abnahme (L5) erfolgt erst beim ersten realen Greenfield-Vorhaben (PRD-Interview → TECH-STACK → ROADMAP an echtem Projekt); bis dahin bleibt es unabgenommen im Backlog, Hinweis dazu in spec.md-Statuskommentar

### Deliverables
- [ ] Umfeld konsistent; SC1-SC9 belegt abgehakt; global verteilt

### Checkpoint-Kriterien
- [ ] Jeder SC-Haken trägt einen konkreten Beleg (Fixture-Lauf, Grep, Praxistest)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| A: PRD-Template-Struktur | neu nach 10x-Schema / am heutigen Report-Format angelehnt | Report-Format + `## Open Questions` | Strukturkontinuität: Report-Modus liest dieselben Sektionen, keine zwei PRD-Dialekte |
| B: Interview-Kategorien | frei / 10x-shape 1:1 / 6 Kategorien ans Template gespiegelt | 6 Kategorien (Vision, Zielgruppen, Features, Stories, NFRs, Scope) | Interview-Output = Template-Sektionen, nichts Erhobenes ohne Zielort |
| C: Readiness-Heuristik | LLM-Einschätzung / mechanische Signale | 4 Signale à 1 Punkt, Schwelle ≥3 | Mechanisch prüfbar, blind testbar; Muster aus Codebase-Research-Kriterium bewährt |
| D: TECH-STACK.md-Kollision | Archivdialog wie PRD / edit-in-place | edit-in-place | Living Doc mit inkrementellen Änderungen; nur PRD/ROADMAP werden „ganz regeneriert" |
| E: Leak-Lint-Quelle | eigene Kategorien / 7 Kategorien aus feature-plan wiederverwenden | wiederverwenden (angepasstes Redirect-Ziel TECH-STACK.md) | Ein Lint-Vokabular im Kit; bewusste Kopie, beidseitig mit Gegen-Hinweis markiert (kein Import-Mechanismus) |
| F: §5-/Roadmap-Status-Vokabular | englisch `in-progress` / deutsche Anzeigewerte | englisch `proposed/ready/blocked/in-progress/done` + deutsche Legenden-Zeile | Ein Wortschatz, grep-bar, konsistent zu S-NN/F-NN; BACKLOG-Legende (deutsch) bleibt eigenständig (plan-review Challenger 2) |
| G: Abnahme-Pfad | Praxistest an erfundenem Projekt / zweistufig | zweistufig: Fixtures → Fertig zum Testen; Abnahme erst beim ersten realen Greenfield-Lauf | Kein Zielprojekt ist Greenfield; erfundenes Projekt = verkleidete Fixture, unterliefe L5 (Nutzer-Entscheidung) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [ ] 1.1 Modus-Weiche + Frontmatter + Quellmaterial
- [ ] 1.2 Interview-Phasen + Resume-Marker + Thin-Input
- [ ] 1.3 PRD-Template + Nie-erfinden-Hard-Rule
- [ ] 1.4 Selbst-Review + Kollision + Hand-off (prd)
- [ ] 2.1 Frontmatter + Gate + Readiness (roadmap)
- [ ] 2.2 Stack-Besprechung → TECH-STACK.md
- [ ] 2.3 Lean-Interview + Slice-Zerlegung
- [ ] 2.4 ROADMAP-Template + Selbst-Review + Kollision + Hand-off
- [ ] 3.1 DERIVED_STATE_RULES.md §5
- [ ] 3.2 workflow-checkpoint ROADMAP-Sync
- [ ] 4.1 pipeline-graph + README/CLAUDE.md
- [ ] 4.2 Statische Selbstprüfung
- [ ] 4.3 Blinde Fixture-Läufe SC1-SC8
- [ ] 4.4 kit-sync + SC-Abschluss (zweistufige Abnahme)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/greenfield-autoren-skills/plan.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
