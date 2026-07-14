# Implementierungsplan: Opportunity-Map (build/buy/complement/wait-Sichtung)

**Erstellt:** 2026-07-14
**Feature-Spec:** `features/opportunity-map/spec.md`
**Geschaetzte Dauer:** ~7-9 h (3 Phasen, 2-3 Sessions im 3x3-Rhythmus)
**Status:** Reviewed <!-- plan-review 2026-07-14: REVISE, 3 WARN → alle Empfehlungen eingearbeitet (Suche bei Bedarf, Gegen-Hinweis-Paar, Untrusted-Guardrail, Fallback-Test); Nudge-Timing „jetzt" bestätigt -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | `dtb-opportunity-map` Kern-Skill (Erhebung, Klassifikation, Kandidat, Artefakt) | ~4 h | Geplant |
| Phase 2 | Umfeld + Verifikation des Kern-Skills (pipeline-graph, README/CLAUDE.md, statisch, Fixtures) | ~2,5 h | Geplant |
| Phase 3 | greenfield-prd Eingangs-Nudge (isolierter letzter Schritt) + kit-sync | ~2 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` `## Betroffene Module` (📂 übernommen, Bestands-Pfade per Glob verifiziert 2026-07-14;
> `dtb-opportunity-map/SKILL.md` fehlt erwartungsgemäß = Neubau). Ergänzt um belegte Befunde aus greenfield-prd/skills-CLAUDE.md.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-opportunity-map/SKILL.md` | **NEU** — existiert nicht; wird in Phase 1 erstellt |
| `skills/dtb-greenfield-prd/SKILL.md` | 279 Z.; Modus-Weiche = Schritt 1 (dreistufig, Resume-Vorrang-Regel); Autoren-Modus Zweig 3; Quellmaterial-Glob Schritt 2a Z. 73 schließt nur PRD/ROADMAP/TECH-STACK aus (→ Map wird erfasst); `allowed-tools: Read, Write, Glob, Grep` (kein AskUserQuestion); Nudge-Ort = Zweig 3 vor Schritt 2a |
| `dtb-project/project-strategy/` | Zielverzeichnis (enthält ROADMAP.md/TEAM.md); Bindestrich-UPPERCASE-Konvention wie PRD-MVP.md/TECH-STACK.md |
| `skills/CLAUDE.md` | Frontmatter-Pflichtfelder; Eligibility-Gate-Einteilung („kein Gate für Entry-Points ohne zwingende Eingabe"); kit-sync Class-A deckt neuen Skill automatisch (keine Registrierung) |
| `skills/dtb-pipeline-graph/SKILL.md` | liest `produces`-Frontmatter; Artefakt-Legende führt PRD-MVP/ROADMAP/TECH-STACK — Ort für OPPORTUNITY-MAP-Zeile beim Umsetzen per Grep bestätigen |
| `skills/dtb-kit-sync/SKILL.md` | Class-A-Pattern `skills/dtb-*/SKILL.md` — neuer Skill automatisch im Sync-Umfang; **keine** Code-Änderung, nur Sync-Lauf + Lock |
| `README.md` + `CLAUDE.md` (Root) | Skill-Katalog/Kategorien — neuer Skill unter Greenfield-Vorfeld eintragen (genaue Stelle beim Umsetzen bestätigen) |

---

## Phase 1: `dtb-opportunity-map` Kern-Skill

### Ziel
Ein manuell startbarer Vorfeld-Skill, der Signale erhebt, sie in build/buy/complement/wait einordnet, genau einen Kandidaten empfiehlt und das Artefakt schreibt.

### Schritte

#### Schritt 1.1: Frontmatter + Grundgerüst + Signal-Erhebung
- **Zweck:** Skelett des Skills + der Eingang (Signale sammeln, ohne Lösung mit Schmerz zu verwechseln)
- **Dateien:** `skills/dtb-opportunity-map/SKILL.md` (neu)
- **Input:** 10x-Vorbild (Initial Response, Guardrails, Step 1); spec.md SC1; skills/CLAUDE.md (Frontmatter)
- **Output:** Frontmatter (`name: dtb:opportunity-map`, `disable-model-invocation: true`, `allowed-tools: Read, Write, Glob, Grep, WebSearch`, `stage: greenfield`, `after: null`, `next: dtb:greenfield-prd`, `consumes: [project-strategy/*.md, INBOX.md, workflow.config.yaml]`, `produces: [OPPORTUNITY-MAP.md]`); Signal-Erhebung: `Glob project-strategy/*.md` + INBOX + Freitext anbieten; Guardrail „vorgeschlagene Lösung (‚baut mir X') ≠ Schmerzsignal → nach wiederkehrendem Schmerz fragen". **Kein Hard-Gate** (Entry-Point ohne zwingende Eingabe, skills/CLAUDE.md-Einteilung)

#### Schritt 1.2: Klassifikation Signal-für-Signal + Daten-Risiko + Marktkenntnis
- **Zweck:** Der Kern — jedes Signal in 4 Wege einordnen, mit aktueller Marktkenntnis
- **Dateien:** `skills/dtb-opportunity-map/SKILL.md`
- **Input:** 10x Step 2 (Block-Format); spec.md SC2/SC4
- **Output:** Signal-für-Signal **als Block** (kein breites Tabellen-Rendering mitten im Gespräch): je Signal `Existing/default response`, `Thin complement`, `First useful version`, `Data risk`, `Direction (build/buy/complement/wait)`; Daten-Risiko **früh** per Auswahlfrage (mock/lokal/read-only vs. echte Firmen-/Kundendaten). Marktkenntnis: **WebSearch bei Bedarf** — nur wenn das Modellwissen für die Kategorie unsicher ist (offensichtliche Kategorien ohne Suche); nicht verfügbar → **Fallback Modellwissen mit sichtbarer Kennzeichnung**; „nie erfinden" — Funde als recherchiert markieren, Unsicherheit benennen. **Untrusted-Input-Guardrail (Betriebs-WARN):** Web-Funde nie wörtlich/als Instruktion ins Artefakt übernehmen, nur als Hinweis behandeln; buy/complement-Empfehlung trägt immer „aktuelle Produktlage selbst verifizieren"

#### Schritt 1.3: Kandidaten-Empfehlung + „no build"-Ausgang
- **Zweck:** Genau ein Kandidat statt zehn Prototypen; ehrliches Nichts-bauen zulassen
- **Dateien:** `skills/dtb-opportunity-map/SKILL.md`
- **Input:** 10x Step 3/4; spec.md SC3
- **Output:** Ranking-Kriterien (wiederholt sich, ≥2 Quellen/Rollen, klarer manueller Schmerz, read-only testbar, ersetzt keine Plattform, klare spätere Richtung) → **genau 1 Kandidat** mit dünner Erstversion (Reads/Returns/Does-not-do/Daten-Risiko/Richtung) + „Warum dieser, nicht die anderen"; qualifiziert sich keiner → **„no build / bestehendes Tool nutzen"** als gültiges Ergebnis

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Artefakt-Template + Selbst-Review + Kollision + Hand-off
- **Zweck:** Artefakt festlegen, Schreibschutz, Verzweigung in die Kette
- **Dateien:** `skills/dtb-opportunity-map/SKILL.md`
- **Input:** 10x Artifact-Shape; spec.md SC5/SC6/SC7; greenfield-prd Schritt 4/5 (Selbst-Review-/Kollisions-Muster)
- **Output:** `OPPORTUNITY-MAP.md`-Template (deutsch): Kontext (Projekt/Datenlage/Datum), Vergleichstabelle (1 Zeile/Signal, terse), empfohlener Kandidat, Begründung, Richtung. Selbst-Review VOR Write (Basis nicht leer, alle Sektionen) → Abbruch ohne Write bei Verstoß. Kollisions-Dialog wie greenfield (Archivieren+ersetzen `project-strategy/archive/YYYY-MM-DD-OPPORTUNITY-MAP.md` / Überschreiben / Abbrechen). Hand-off ohne Auto-Chaining: build → `/dtb:greenfield-prd`; buy/complement → Handlungshinweis („Produktkategorie gegen Must-Haves prüfen"); wait → Map gespeichert. **Gegen-Hinweis (L5, Architekt-WARN):** Kommentar am Artefakt-Namen — „`OPPORTUNITY-MAP.md` wird von greenfield-prds Quellmaterial-Glob aufgegriffen; Name/Ort gekoppelt an dessen Ausschlussliste (Schritt 2a) — bei Änderung dort mitdenken"

### Deliverables
- [ ] `skills/dtb-opportunity-map/SKILL.md`, ≤ ~350 Z., deutsch

### Checkpoint-Kriterien
- [ ] SC1–SC7-Mechanik im Skill-Text vollständig
- [ ] **Budget-Messpunkt:** Zeilenzahl gemessen; >350 → sofort entscheiden (Budget vs. Kürzen vs. references-Folge-Idee) BEVOR Phase 2 startet

---

## Phase 2: Umfeld + Verifikation des Kern-Skills

### Ziel
Das Umfeld kennt das neue Artefakt; SC1–7 + SC9 sind belegt (deterministische Mechanik + Websuche-Sonderbehandlung).

### Schritte

#### Schritt 2.1: pipeline-graph + README/CLAUDE.md
- **Zweck:** Umfeld kennt Skill + Artefakt
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`, `README.md`, `CLAUDE.md`
- **Input:** vorhandene Artefakt-Legende (Ort per Grep bestätigen)
- **Output:** Legende um `OPPORTUNITY-MAP.md` (Ort project-strategy/, Erzeuger opportunity-map); README/CLAUDE.md-Katalog: neuer Skill unter Greenfield/Vorfeld mit ehrlicher Beschreibung

#### Schritt 2.2: Statische Selbstprüfung (SC9)
- **Zweck:** SC9 mechanisch belegen, bevor Fixtures laufen
- **Dateien:** — (read-only)
- **Input:** SKILL.md, Frontmatter
- **Output:** Belegt: Zeilenzahl ≤ ~350, `disable-model-invocation: true`, `produces: [OPPORTUNITY-MAP.md]`, `allowed-tools` inkl. WebSearch, `next`-Kette, deutsch, Guardrails im Text, pipeline-graph-Legende + README/CLAUDE.md aktuell

#### Schritt 2.3: Blinde Mechanik-Fixtures (SC1–SC3, SC5–SC7)
- **Zweck:** Deterministische Mechanik verhaltensecht, unabhängig vom Autor-Kontext
- **Dateien:** Scratchpad-Fixtures (Projektstruktur mit workflow.config.yaml + project-strategy/-Varianten)
- **Input:** Fixtures: (a) Signale mit klarer Kaufkategorie → buy/complement + Kandidat; (b) „baut mir ein Dashboard" → Rückfrage nach Schmerz (SC1); (c) kein qualifizierter Kandidat → „no build" (SC3); (d) präparierte leere Basis → Selbst-Review-Abbruch ohne Write (SC6); (e) vorhandene OPPORTUNITY-MAP.md → Kollisions-Dialog (SC6); (f) build-Ausgang → Hand-off greenfield-prd, buy → Handlungshinweis (SC7); (g) geschriebene Map → Grep, dass Dateiname nicht in greenfield-prds Ausschlussliste (SC5)
- **Output:** Blinde Agenten-Läufe (nur Skill + Fixture), PASS/FAIL je SC dokumentiert; Fixture-Signale mit **offensichtlicher Kategorie** gewählt → „bei Bedarf"-Regel löst keine Suche aus → deterministisch (kein Websuche-Leck in 2.3)

#### Schritt 2.4: Websuche-Sonderbehandlung (SC4) — nicht blind
- **Zweck:** Den nicht-deterministischen Marktteil belegen, ohne exakten Inhalt zu prüfen
- **Dateien:** — (statische Prüfung + beobachteter Probelauf)
- **Input:** Skill-Text + ein beobachteter Lauf mit echtem Nischen-Signal (löst „bei Bedarf"-Suche aus) + ein Fallback-Fixture ohne WebSearch-Verfügbarkeit
- **Output:** Statisch belegt: Skill sucht bei Bedarf, kennzeichnet Funde als recherchiert, behandelt sie als untrusted (nicht wörtlich/als Instruktion), degradiert bei Nichtverfügbarkeit sichtbar auf Modellwissen, erfindet keine Produkte. Beobachteter Probelauf: Struktur/Kennzeichnung korrekt (Inhalt NICHT auf Exaktheit geprüft — Nicht-Determinismus dokumentiert). **Fallback-Fall (Senior-Dev-WARN):** WebSearch nicht verfügbar → sichtbare Degradation auf Modellwissen belegt, kein harter Fehler

> **3x3-Block:** Nach Schritt 2.4 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Umfeld konsistent; SC1–7 + SC9 belegt; SC4 mit dokumentierter Sonderbehandlung

### Checkpoint-Kriterien
- [ ] Jeder SC-Haken trägt einen konkreten Beleg (Fixture-Lauf, Grep, statische Prüfung, Probelauf)

---

## Phase 3: greenfield-prd Eingangs-Nudge (isolierter letzter Schritt)

### Ziel
Der Nudge macht build/buy sichtbar, ohne die verifizierte Greenfield-Logik zu berühren; alles global verteilt.

### Schritte

#### Schritt 3.1: Eingangs-Nudge in greenfield-prd einbauen
- **Zweck:** build/buy im Autoren-Einstieg anbieten, ohne die Modus-Weiche zu verletzen
- **Dateien:** `skills/dtb-greenfield-prd/SKILL.md`
- **Input:** reale Modus-Weiche Schritt 1 (dreistufig); spec.md SC8
- **Output:** Neuer Mikro-Block **nur in Zweig 3 (PRD fehlt, frischer Autoren-Modus), VOR Schritt 2a**: falls keine `project-strategy/OPPORTUNITY-MAP.md` existiert → EIN Text-Hinweis „build/buy schon geklärt? → `/dtb:opportunity-map` erwägen. Weiter / Abbrechen". **Expliziter Vorrang (L5):** greift NICHT bei Resume-Marker ≠ done (Zweig 1) und NICHT im Report-Modus (Zweig 2); liegt eine Map vor, erscheint er nicht. Additiv — Schritte 2a/2b/3/4/5 unverändert (SC1–3 des Greenfield-Features unberührt). **Gegen-Hinweis (L5, Gegenrichtung):** Kommentar an der Glob-Ausschlussliste (Schritt 2a) — „Ausschlussliste + Nudge-Bedingung auf `OPPORTUNITY-MAP.md` gekoppelt an `dtb-opportunity-map`; bei Änderung dort mitdenken"

#### Schritt 3.2: Nudge-Verifikation (SC8)
- **Zweck:** Den additiven Zweig verhaltensecht + die Nicht-Regression der Greenfield-SC belegen
- **Dateien:** Scratchpad-Fixtures
- **Input:** Fixtures: (a) kein PRD + keine Map → Nudge erscheint; (b) kein PRD + Map vorhanden → kein Nudge; (c) Resume-Marker ≠ done → kein Nudge; (d) PRD vorhanden (Report) → kein Nudge
- **Output:** PASS/FAIL je Fall; Bestätigung, dass die vorhandenen Greenfield-Fixtures (SC1–3-Pfade) unverändert PASS bleiben

#### Schritt 3.3: kit-sync + SC-Abschluss
- **Zweck:** Verteilen (neuer Skill + geänderter greenfield-prd) und Stand ehrlich abschließen
- **Dateien:** `~/.claude/skills/…` via `/dtb:kit-sync`; `features/opportunity-map/spec.md`
- **Input:** verteilter Stand; Verifikationsergebnisse 2.3/2.4/3.2
- **Output:** kit-sync sync (Lock aktualisiert: neuer Skill + greenfield-prd-Hash; pitch-coach weiter gehalten); SC1–SC9 in spec.md mit Belegen abhaken; Session-Log vermerkt bewussten greenfield-prd-Touch

### Deliverables
- [ ] Nudge in greenfield-prd (additiv); SC8 belegt; SC1–9 abgehakt; global verteilt

### Checkpoint-Kriterien
- [ ] Greenfield-SC1–3 nachweislich nicht regressiert; Nudge greift nur in Zweig 3 ohne Map

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| A: Nudge-Platzierung | eigener Schritt vor Weiche / in Zweig 3 vor 2a / in jeder Weiche | **Zweig 3 (frischer Autor), vor 2a** | Nur dort ist build/buy noch offen; Resume/Report unberührt → kein Konflikt mit Resume-Vorrang-Regel (L5) |
| B: Hard-Gate für opportunity-map | Gate auf Signal-Input / kein Gate | **kein Gate** | Entry-Point ohne zwingende Eingabe (Freitext genügt); skills/CLAUDE.md-Einteilung |
| C: Verifikation Websuche | rein blinde Fixtures / Mechanik-Fixtures + Websuche-Sonderbehandlung | **geteilt: deterministische Mechanik blind (2.3), Marktteil statisch + Probelauf + Fallback-Fall (2.4)** | „Bei Bedarf"-Suche (G) macht 2.3 sauber deterministisch (offensichtliche Kategorien → keine Suche); nicht-deterministischer Marktteil separat auf Struktur/Kennzeichnung/Fallback geprüft (löst den Haupt-offenen-Punkt der Spec) |
| D: Kollisions-Verhalten Artefakt | Kollisions-Dialog wie greenfield / edit-in-place | **Kollisions-Dialog** | Die Map ist eine Momentaufnahme der Entscheidung (regenerierbar wie PRD), kein inkrementelles Living-Doc wie TECH-STACK |
| E: Artefakt-Dateiname | OPPORTUNITY-MAP.md / OPPORTUNITY_MAP.md | **OPPORTUNITY-MAP.md** | Analog PRD-MVP.md/TECH-STACK.md (UPPERCASE-mit-Bindestrich in project-strategy/); gegen project-health beim Umsetzen gegenprüfen |
| F: allowed-tools | ohne Web / mit WebSearch (+WebFetch) | **Read, Write, Glob, Grep, WebSearch** | Live-Marktkenntnis (Nutzer-Entscheidung „max. Aktualität"); WebFetch nachrüsten nur falls Detailabruf nötig |
| G: Suchstrategie (plan-review) | immer suchen / bei Bedarf | **bei Bedarf** (nur wenn Modellwissen für die Kategorie unsicher) | Aktualität dort wo sie zählt (Nischen/neue Produkte); offensichtliche Kategorien deterministisch testbar ohne Test-Schalter; passt zur „groben Vorfeld-Sichtung"-Philosophie |
| H: Nudge-Timing (plan-review) | jetzt (Phase 3) / mit Greenfield-Abnahme | **jetzt** | Nudge additiv+winzig, „zweimal testen" trivial; halbfertiges opportunity-map ohne Nudge wäre der schwächere Zustand; Pre-Mortem-Einwand durch Gegen-Hinweis (nicht Timing) entschärft |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [x] 1.1 Frontmatter + Grundgerüst + Signal-Erhebung — `772ae4f`
- [x] 1.2 Klassifikation Signal-für-Signal + Daten-Risiko + Marktkenntnis — `772ae4f`
- [x] 1.3 Kandidaten-Empfehlung + „no build"-Ausgang — `772ae4f`
- [x] 1.4 Artefakt-Template + Selbst-Review + Kollision + Hand-off — `a2fd691`
- [x] 2.1 pipeline-graph + README/CLAUDE.md — `a2fd691`
- [x] 2.2 Statische Selbstprüfung (SC9) — 286 Z., Frontmatter, Gegen-Hinweis — alle PASS — `a2fd691`
- [x] 2.3 Blinde Mechanik-Fixtures (SC1–3, SC5–7) — 5 Blindläufe PASS (build/buy/empty/collision/nobuild) + Pfad-Inkonsistenz gefixt — `e69446e`
- [x] 2.4 Websuche-Sonderbehandlung (SC4) — statisch + Positiv-Lauf (WebSearch bei Nische, Funde untrusted gekennzeichnet) + Fallback-Lauf (sichtbare Degradation, kein Fehler) — alle PASS (Verifikation, kein Commit; plan.md-Stand fließt in 3.x)
- [ ] 3.1 Eingangs-Nudge in greenfield-prd
- [ ] 3.2 Nudge-Verifikation (SC8)
- [ ] 3.3 kit-sync + SC-Abschluss

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/opportunity-map/plan.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
