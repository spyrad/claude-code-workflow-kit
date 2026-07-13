# Implementierungsplan: Codebase-Research-Step

**Erstellt:** 2026-07-13
**Feature-Spec:** `features/codebase-research-step/spec.md`
**Geschaetzte Dauer:** 1–2 Sessions
**Status:** Entwurf

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Änderung `dtb-impl-plan` + Gegen-Hinweis `feature-discover` (Repo) | ~1/2 Session | Geplant |
| Phase 2 | Verifikation (statisch + blinde Agenten) | ~1/2 Session | Geplant |
| Phase 3 | Verteilung + Abnahme | kurz | Geplant |

---

## Phase 1: Skill-Änderung `dtb-impl-plan` (Repo)

### Ziel
`skills/dtb-impl-plan/SKILL.md` (aktuell 219 Zeilen) erhält den Research-Schritt als
kompakten, deterministischen Block — alle Spec-Entscheidungen (Auslöse-Kriterium, UX,
Randfälle) landen im Skill-Text, Budget ≤ 260 Zeilen (SC8).

### Schritte

#### Schritt 1.1: Research-Block schreiben
- **Zweck:** Kernstück — der neue Abschnitt `## Codebase-Research (Ist-Analyse)` direkt nach dem Eligibility-Gate (Eingangs-Reihenfolge lt. Spec: Lektionen-Prior → Gate → Research → Aufgabe). Vorrang-Regeln explizit formulieren (L5: konkurrierende Eingangs-Regeln nie implizit lassen)
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`
- **Input:** Spec „Enthalten" (Auslöse-Kriterium, 0-Treffer-Dialog, Kappung 15, Bestätigungs-UX), UX-Muster aus `skills/dtb-feature-discover/SKILL.md` Schritt 2 (Z. 52–71)
- **Output:** Block mit: (a) Auslöse-Kriterium als eine mechanische Regel (verwertbare Modul-Liste = discovery.md ∧ `## Betroffene Module` ∧ ≥1 Pfad-Zeile ∧ Stichproben-Verifikation per Glob; ≥1 Pfad fehlt → veraltet → Scan). **Parser-Toleranz explizit definieren:** „Pfad-Zeile" = jede Zeile in `## Betroffene Module`, deren erste Spalte/erstes Token wie ein Datei-/Verzeichnispfad aussieht (Backticks optional, Tabellen- ODER Bullet-Form zulässig); für die Stichproben-Verifikation den ersten Pfad je Zeile per Glob prüfen. Nicht am Format scheitern (ältere Kit-Versionen/Zielprojekte formatieren frei); (b) Scan-Anleitung (Schlüsselwörter aus Spec → Glob/Grep, read-only); (c) Tabelle `| # | Pfad | Relevanz |` + „Stimmt das so?"-Bestätigung VOR der Planung; (d) 0-Treffer-Dialog mit beiden Ausgängen (Pfade nachtragen + verifizieren / Neubau explizit); (e) Kappung bei 15 + Pflicht-Zeile „+ N weitere Treffer nicht gelistet" + operatives Priorisierungs-Kriterium (direkter Modul-Treffer = Spec-Schlüsselwort im Pfad/Dateinamen VOR Streu-Treffer im Datei-Inhalt/Doku/Tests) + Hinweis-Satz „zu generisch → schärfer nachscannen"; (f) Wartungs-Hinweis Format-Kopplung an feature-discover `## Betroffene Module`; (g) **sichtbare Skip-Statuszeile** bei verwertbarer Modul-Liste: `📂 Ist-Analyse aus discovery.md übernommen (N Module, Pfade verifiziert)` — macht den korrekten Skip von einem vergessenen Schritt unterscheidbar (Muster wie 📚/🔎)

#### Schritt 1.2: Template + Ausführungs-Anweisungen erweitern
- **Zweck:** Ergebnis-Verankerung im Plan-Artefakt und Einbau in den Ablauf
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`
- **Input:** Ergebnis aus 1.1; bestehendes plan.md-Template (Z. 69–157) und Ausführungs-Schritte 1–7 (Z. 161–202)
- **Output:** (a) plan.md-Template um kompakten Abschnitt `## Ist-Analyse` ergänzt (Tabelle Pfad/Ist-Befund, 1 Hinweiszeile „Neubau" für den 0-Treffer-Ausgang, keine Prosa — zählt gegen 500-Zeilen-Budget von plan.md); (b) Ausführungs-Schritte sauber renummeriert mit neuem Schritt „Ist-Analyse durchführen/übernehmen" zwischen „Feature-Spec lesen" und „Analysiere die Feature-Spec"; Verweis auf den Research-Block statt Text-Doppelung (Muster: Eligibility-Gate-Verweis in Schritt 2)

#### Schritt 1.3: Frontmatter + Reader-Verifikation
- **Zweck:** `consumes:` ehrlich machen und SC7 auf belegte Reader stützen (L2: Reader-Rolle per Grep am SKILL.md-Text belegen, nie aus CLAUDE.md-Behauptungen)
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (Frontmatter); Grep read-only über `skills/dtb-pipeline-graph/SKILL.md`, `skills/dtb-workflow-status/SKILL.md`, `skills/dtb-project-health/SKILL.md`
- **Input:** Frontmatter Z. 10–15 (`consumes: [features/*/spec.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md]`)
- **Output:** `consumes` + `features/*/discovery.md`; belegte Liste, welche Skills `consumes` real lesen (Erwartung aus L2: pipeline-graph liest, project-health validiert, workflow-status offen) — Ergebnis bestimmt, wogegen SC7 in Phase 2 geprüft wird

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Gegen-Hinweis in feature-discover (Kopplung beidseitig)
- **Zweck:** Review-Entscheidung 1A — die Format-Kopplung wird an BEIDEN Enden abgesichert; der Schutz wirkt dort, wo die brechende Änderung entsteht (wer feature-discover Schritt 2 ändert, sieht die Warnung im Moment der Änderung), nicht nur bei impl-plan
- **Dateien:** `skills/dtb-feature-discover/SKILL.md` (Schritt 2 „Codebase-Scan", Z. 52–71)
- **Input:** Ergebnis 1.1(f)
- **Output:** eine Kommentar-/Hinweiszeile an der `## Betroffene Module`-Erzeugung: „Format wird von `dtb:impl-plan` als Auslöse-Kriterium des Research-Schritts geparst — bei Formatänderung dort mitdenken"; macht feature-discover zur **zweiten Klasse-A-Datei** im kit-sync-Umfang (3.1)

### Deliverables
- [ ] `skills/dtb-impl-plan/SKILL.md` mit Research-Block, erweitertem Template, renummerierten Ausführungs-Schritten, erweitertem `consumes` (≤ 260 Zeilen)
- [ ] `skills/dtb-feature-discover/SKILL.md` mit Gegen-Hinweis-Zeile (Kopplung beidseitig)

### Checkpoint-Kriterien
- [ ] Alle 7 Bausteine (a–g) aus 1.1 im Skill-Text auffindbar (inkl. Parser-Toleranz in (a) und Skip-Zeile (g))
- [ ] Eingangs-Reihenfolge im Text: Lektionen-Prior → Eligibility-Gate → Research → Aufgabe
- [ ] Kein Baustein doppelt (Verweis-Muster statt Kopie)
- [ ] Gegen-Hinweis in feature-discover vorhanden; beide Hinweise verweisen aufeinander

---

## Phase 2: Verifikation (statisch + blinde Agenten)

### Ziel
Alle 8 Success Criteria der Spec verhaltensecht oder mechanisch belegen — nach dem
Abnahme-Vorbild Eligibility-Gates/Change-Folder (blinde Multi-Varianten-Agenten gegen Fixtures).

### Schritte

#### Schritt 2.1: Statische Selbstprüfung
- **Zweck:** Billige mechanische SCs sofort abhaken, bevor Agenten laufen
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (read-only)
- **Input:** Deliverable aus Phase 1
- **Output:** Belege für SC7 (Frontmatter enthält `features/*/discovery.md`; Reader-Check aus 1.3 bestanden: pipeline-graph/project-health verarbeiten den Eintrag fehlerfrei — Umfang lt. 1.3-Befund) und SC8-Hälfte 1 (`wc -l` ≤ 260)

#### Schritt 2.2: Fixtures bauen
- **Zweck:** 4 minimale Projekt-Fixtures im Scratchpad für die blinden Läufe (C+E zusammengelegt, Review-Entscheidung 3A)
- **Dateien:** Scratchpad `research-fixture-{a,b,ce,d}/` (config + features/<slug>/ + ggf. discovery.md)
- **Input:** Spec-SCs 1–4, 6
- **Wichtig (Senior-Dev-Punkt):** Jede Fixture braucht neben den Workflow-Artefakten eine **echte, scanbare Quelldatei-Struktur** (nicht nur config + spec.md), sonst testet Fixture A den 0-Treffer-Pfad statt SC1. Die Spec-Schlüsselwörter der Fixture müssen zu vorhandenen Dateien passen
- **Output:** (A) spec.md ohne discovery.md, Schlüsselwörter matchen vorhandene Dateien → SC1; (B) spec.md + verwertbare discovery.md (Pfade existieren) → SC2 (prüft die sichtbare Skip-Zeile aus 1.1(g), kein Nicht-Ereignis); (CE) **kombiniert:** discovery.md mit ≥1 totem Pfad UND >15 matchende Dateien → ein Lauf: Veraltet-Regel triggert den Scan (SC3, Beobachtung: Trigger-Meldung), Scan läuft in die Kappung (SC6, Beobachtung: „+ N weitere"-Zeile) — getrennte Output-Artefakte, keine Verunreinigung; (D) spec.md, deren Schlüsselwörter nichts matchen → SC4

#### Schritt 2.3: Blinde Agenten-Läufe SC1–SC4 + SC6
- **Zweck:** Verhaltensechte Belege — Agenten kennen nur den echten Skill-Text + Fixture, nicht die Erwartung
- **Dateien:** Läufe gegen Repo-Stand von `skills/dtb-impl-plan/SKILL.md`; Ergebnisse in Spec-SC-Boxen
- **Input:** Fixtures aus 2.2
- **Output:** aus 4 Läufen 5 Verdikte: Scan läuft + Tabelle + Bestätigung vor Planung (SC1, Fixture A); Schritt übersprungen, sichtbare Skip-Zeile statt Doppel-Scan (SC2, Fixture B); Veraltet-Regel triggert Scan + Scan läuft in die Kappung (SC3 + SC6, Fixture CE); 0-Treffer-Dialog, beide Ausgänge, kein stummes Weiterplanen (SC4, Fixture D). Fixture B ist zugleich Negativ-Kontrolle (kein Fehlalarm)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: SC5-Nachweis (Grounding-Kompatibilität)
- **Zweck:** Der in einem 2.3-Lauf erzeugte plan.md-Entwurf mit `## Ist-Analyse` wird gegen `plan-review` Schritt 2d gehalten: extrahiert das Grounding die Ist-Analyse-Pfade als prüfbare Referenzen?
- **Dateien:** plan.md-Artefakt aus Lauf A; `skills/dtb-plan-review/SKILL.md` (Z. 98–116, unverändert)
- **Input:** Lauf-A-Ergebnis
- **Output:** SC5-Beleg (Grounding-Zeile `🔎 Grounding: N Referenzen geprueft …` umfasst die Ist-Analyse-Pfade)

### Deliverables
- [ ] SC1–SC7 in `spec.md` mit 1-Zeilen-Beleg abgehakt (SC8 erst nach Phase 3 vollständig)

### Checkpoint-Kriterien
- [ ] Kein Agent bekam die erwarteten Ergebnisse vorab (blind)
- [ ] Negativ-Kontrolle vorhanden (Fixture B = kein Fehlalarm)

---

## Phase 3: Verteilung + Abnahme

### Ziel
Geänderten Skill global verteilen und das Feature an echtem Kontext gegentesten (L5).

### Schritte

#### Schritt 3.1: kit-sync ausführen
- **Zweck:** Klasse-A-Verteilung — Drei-Punkte-Abgleich, globale Kopien aktualisieren
- **Dateien:** **zwei** Klasse-A-Artefakte (Entscheidung 1A): `~/.claude/skills/dtb-impl-plan/SKILL.md` (Lock `8bd3ee2c`) + `~/.claude/skills/dtb-feature-discover/SKILL.md` (Lock `8f5042c4`); `~/.claude/dtb-lock.json`
- **Input:** Verifizierter Repo-Stand aus Phase 2
- **Output:** für beide Dateien Repo == Lock == global; Lock `sourceCommit` + beide Hashes aktualisiert → SC8-Hälfte 2

#### Schritt 3.2: Praxistest an echtem Kontext + SC-Abschluss
- **Zweck:** L5: Fixture-Abnahmen verstecken Trigger-Ambiguitäten — Praxistest am **Trigger-Pfad** (Kern des Features), Entscheidung 4A
- **Dateien:** **pkp-Testbett** (dort typischerweise keine discovery.md → Trigger-Pfad wird echt, nicht künstlich ausgelöst); danach `features/codebase-research-step/spec.md` (SC-Boxen)
- **Input:** global verteilter Stand aus 3.1
- **Output:** Praxis-Beleg Trigger-Pfad; SC8 abgehakt; Feature „Fertig zum Testen" → Abnahme-Entscheidung durch den Nutzer
- **Bonus (kostenlos, kein Blocker für die Abnahme):** der nächste echte Kit-`impl-plan`-Lauf (z.B. Idee #11/#13) läuft ohnehin mit vorhandener discovery.md → liefert den **Skip-Pfad** als zweiten Praxis-Datenpunkt; im Session-Log nachtragen, wenn er anfällt

### Deliverables
- [ ] Global verteilter, praxis-gegengetesteter Skill; alle SC-Boxen mit Beleg

### Checkpoint-Kriterien
- [ ] Drei-Punkte-Vergleich nach Sync: 36/37 synchron + 1 bewusst divergent (pitch-coach); beide geänderten Dateien (impl-plan, feature-discover) auf der Synchron-Seite
- [ ] Praxistest-Ergebnis (Trigger-Pfad, pkp) im Session-Log dokumentiert

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Einbau-Form des Research-Blocks | (A) eigener Abschnitt nach dem Gate + Verweis in Ausführungs-Schritten, (B) nur in Ausführungs-Schritte einbetten | A | Muster-Konsistenz mit Eligibility-Gate/Lektionen-Prior (Eingangs-Blöcke stehen vorn, Ausführungs-Schritte verweisen); Vorrang-Reihenfolge bleibt an einer Stelle lesbar (L5) |
| Kappungs-Grenze | „~15" (weich) vs. 15 (fest) | 15 fest | SC6 muss mechanisch prüfbar sein; Nachfordern im Dialog bleibt möglich |
| Ausführungs-Schritte einfügen | Renummerieren vs. Einschub „3b" | Renummerieren | Saubere N.M-Referenzen; Skill ist kurz, Kollateralschaden gering |
| SC7-Prüfumfang (workflow-status) | workflow-status als consumes-Reader mitprüfen vs. nur pipeline-graph/project-health | Offen — 1.3 klärt per Grep | L2: Reader-Rolle nie behaupten; Spec nennt workflow-status, der reale Text entscheidet den Prüfumfang |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [x] 1.1 Research-Block schreiben — `5626c96`
- [x] 1.2 Template + Ausführungs-Anweisungen erweitern — `5626c96`
- [x] 1.3 Frontmatter + Reader-Verifikation — `5626c96`
- [x] 1.4 Gegen-Hinweis in feature-discover (Kopplung beidseitig) — `583f003`
- [x] 2.1 Statische Selbstprüfung — SC7 + SC8-Hälfte1 belegt (impl-plan 258 Z., consumes+discovery.md, feature-discover produces discovery.md → kein Verwaisen)
- [x] 2.2 Fixtures bauen (4 Fixtures, C+E kombiniert) — Scratchpad `research-fixtures/{a,b,ce,d}/`
- [x] 2.3 Blinde Agenten-Läufe SC1–SC4 + SC6 — 4 blinde Agenten, alle PASS (A→SC1, B→SC2+Skip, CE→SC3+SC6, D→SC4)
- [x] 2.4 SC5-Nachweis Grounding-Kompatibilität — blinder plan-review-2d-Lauf: 4 Referenzen geprüft, alle gefunden
- [x] 3.1 kit-sync ausführen — impl-plan `1b6977f` + feature-discover `c47ed37` global synchron, Lock `583f003`; 36/37 + 1 gehalten (pitch-coach)
- [x] 3.2 Praxistest + SC-Abschluss — pkp `simulationsmaske-grunddaten` (Trigger/Skip-Pfad real): Übernahme-Pfad + 9-Pfad-Verifikation bestanden; Fund (HANA-Sub-Tabelle → Fehl-Scan-Risiko) gehärtet (`4e46d32`) + am echten Kontext gegenverifiziert

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/codebase-research-step/plan.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
