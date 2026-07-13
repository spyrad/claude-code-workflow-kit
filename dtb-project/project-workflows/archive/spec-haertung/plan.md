# Implementierungsplan: SPEC_HAERTUNG

**Erstellt:** 2026-07-09
**Feature-Spec:** `features/FEATURE_SPEC_HAERTUNG.md`
**Geschaetzte Dauer:** ~1 Session
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Baustein B — „nie erfinden → Offene Punkte" | kurz | Geplant |
| Phase 2 | Baustein A — Technical-Leak-Lint (7 Kategorien, Hard-Block+Override) | mittel | Geplant |
| Phase 3 | Abnahme (Fixture) + Sync | kurz | Geplant |

---

## Phase 1: Baustein B — „nie erfinden → Offene Punkte"

> **Eigenständiger Zwischen-Meilenstein** (Review-Entscheidung 2026-07-09, Punkt 1a): Phase 1
> ist für sich abnehmbar/nutzbar — der sichere Gewinn (Offene Punkte) hängt nicht am Lint-Risiko
> aus Phase 2. Bei Bedarf kann nach Phase 1 zwischen-abgenommen werden.

### Ziel
`feature-plan` parkt fehlendes Wissen als explizite Frage in `## Offene Punkte` statt es zu erfinden; `[TODO: …]` wird vollständig abgelöst, Benennung einheitlich mit `feature-discover`.

### Schritte

#### Schritt 1.1: `## Offene Punkte` ins FEATURE-Template
- **Zweck:** Der Abschnitt muss fester Bestandteil jeder erzeugten Spec werden
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (Template-Block, Zeilen ~39–94)
- **Input:** Vorbild-Benennung aus `feature-discover` (`## Offene Punkte`)
- **Output:** Template enthält `## Offene Punkte` (vor „Erstellt mit"); Konvention „— keine —" bei fehlenden Lücken dokumentiert

#### Schritt 1.2: „nie erfinden"-Regel ersetzt `[TODO: …]`
- **Zweck:** Die Anweisung darf nicht mehr zum Platzhalter-Erfinden verleiten
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (Ausführungs-Schritt 6, Zeile ~139)
- **Input:** bestehende Regel „Bei fehlenden Infos: Nutze Platzhalter `[TODO: ...]`"
- **Output:** ersetzt durch „Fehlt Information: NICHT plausibel füllen → als konkrete Frage in `## Offene Punkte`"; keine `[TODO]`-Erwähnung mehr im Skill

#### Schritt 1.3: Benennungs-Konsistenz verifizieren
- **Zweck:** Kein Drift zwischen `feature-plan` und `feature-discover`
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`, Abgleich gegen `skills/dtb-feature-discover/SKILL.md`
- **Input:** beide Skill-Dateien
- **Output:** identische Abschnittsbenennung `## Offene Punkte` bestätigt (Grep, still bei Erfolg)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] FEATURE-Template mit `## Offene Punkte`
- [ ] `[TODO]`-Muster entfernt

### Checkpoint-Kriterien
- [ ] Kein `[TODO`-Vorkommen mehr in `feature-plan/SKILL.md`
- [ ] Benennung deckt sich mit `feature-discover`

---

## Phase 2: Baustein A — Technical-Leak-Lint

### Ziel
`feature-plan` prüft den Spec-Text vor dem Write auf 7 Leck-Kategorien und bricht bei Treffer ab (Hard-Block), mit begründetem Override.

### Schritte

#### Schritt 2.1: Lint-Kategorien-Block definieren ⚠ schwerster Schritt
- **Zweck:** Die 7 Kategorien maschinell anwendbar + fehlalarm-arm formulieren (löst Offenen Punkt „exakte Wortlaute"). **Kern der Feinarbeit** — treffsichere Muster, die nicht bei jedem Fachwort feuern (Senior-Dev-Warnung Review); hier steckt der größte Aufwand der Phase
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (neuer Abschnitt, kompakt)
- **Input:** 7 Kategorien aus FEATURE-Spec (Vendor, ORM/Query, Transport, Impl-Verben, Datenstrukturen, Framework/Lib, Datei/Klasse)
- **Output:** kompakte Liste, je Kategorie 1 Leck-Beispiel + lösungsneutrale Alternative + kurze Abgrenzung legitimer Fachbegriffe. **Eng gefasste Meta-Spec-Ausnahme** (Review-Entscheidung 2b): Wenn der Spec-Gegenstand selbst ein Code-/Config-/Skill-Artefakt ist (betroffene Module = Skill-/Code-Dateien), sind Referenzen *auf dieses Artefakt* legitim — inkl. aus `DISCOVERY_*.md` geerbter technischer Angaben; technische Details über *andere*, nicht-gegenständliche Lösungen bleiben Lecks. Ausnahme bewusst schmal halten (Aufblähungs-Spannung)

#### Schritt 2.2: Lint als Pre-Write-Gate einbauen
- **Zweck:** Prüfung muss unmittelbar vor dem Speichern greifen und blocken
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (neuer Schritt zwischen Ausführungs-Schritt 6 und 7 „Speichere")
- **Input:** Kategorien-Block aus 2.1
- **Output:** Gate mit Melde-Format `❌ Technical-Leak-Lint: N Lecks, Write abgebrochen` inkl. Zeile + Kategorie + Umformulierungs-Hinweis pro Fund; kein Write bei Treffer

#### Schritt 2.3: Override mit Begründung + Markierung
- **Zweck:** Legitime Fachbegriffe (z.B. „Export nach SAP") bewusst zulassen, ohne Lint zu entwerten
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (im Gate-Abschnitt)
- **Input:** Melde-Format aus 2.2
- **Output:** Override-Pfad dokumentiert (Begründungspflicht). **Sichtbarkeit (Review-Entscheidung 4b):** überstimmte Stelle wird in der erzeugten Spec mit knappem HTML-Kommentar markiert, z.B. `<!-- Lint-Override: SAP ist fachliche Anforderung -->` — Begründung bleibt dauerhaft nachvollziehbar (für Leser/plan-review)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Kategorien-Block + Pre-Write-Gate im Skill
- [ ] Override-Pfad dokumentiert

### Checkpoint-Kriterien
- [ ] Gate steht vor dem Save-Schritt
- [ ] `feature-plan` bleibt kompakt (< ~280 Zeilen)

---

## Phase 3: Abnahme (Fixture) + Sync

### Ziel
Nachweis, dass Lint + Offene Punkte wortlautkonform greifen; geänderter Skill global synchronisiert.

### Schritte

#### Schritt 3.1: Fixture-Set + isolierte Doppel-Abnahme
- **Zweck:** Heuristik-Determinismus belegen, nicht nur einen Einzelfall (Review-Entscheidung 3b; kein Selbst-Bestätigen)
- **Dateien:** Scratchpad-Fixture-Set mit **3 Spec-Varianten** — (1) klare Lecks, (2) Wissenslücken, (3) gegenständliche Meta-Spec (testet die Ausnahme aus 2.1); Abnahme durch **unabhängigen Agenten** (nicht der Umsetzer)
- **Input:** finaler `feature-plan/SKILL.md`
- **Output:** Protokoll: jede Variante **2× gelaufen**, bestanden nur bei konsistentem Urteil beider Läufe (Leck geblockt mit Zeile/Kategorie · Lücke → `## Offene Punkte` · Ausnahme greift · Override + Markierung funktioniert). Zwischen-Läufen schwankende Fälle = Finding für 3.2

#### Schritt 3.2: Findings beheben + Zeilen-Budget prüfen
- **Zweck:** Mehrdeutigkeiten der Abnahme nachschärfen, Aufblähung vermeiden
- **Dateien:** `skills/dtb-feature-plan/SKILL.md`
- **Input:** Abnahme-Findings aus 3.1
- **Output:** Nachschärfungen eingearbeitet; Zeilenzahl im Budget bestätigt

#### Schritt 3.3: kit-sync
- **Zweck:** Installierte globale Kopie auf Repo-Stand bringen
- **Dateien:** `~/.claude/skills/dtb-feature-plan/SKILL.md`, `~/.claude/dtb-lock.json`
- **Input:** committeter Skill-Stand (siehe `dtb:kit-sync`)
- **Output:** kit-sync check → sync; Lock aktualisiert, Kopie synchron

> **3x3-Block:** Nach Schritt 3.3 → Feature „Fertig zum Testen", Abnahme-Entscheidung einholen

### Deliverables
- [ ] Bestandenes Abnahme-Protokoll
- [ ] Lock aktualisiert, Kopie synchron

### Checkpoint-Kriterien
- [ ] Alle Success Criteria der FEATURE-Spec erfüllt
- [ ] kit-sync meldet feature-plan synchron

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Lint-Verhalten | Hard-Block / Warn / Hard-Block+Override | Hard-Block+Override | Diskussion Discovery — streng, aber nicht bevormundend |
| Kategorien-Umfang | 4 / 7 / später | 7 | Diskussion Discovery — umfassender Schutz |
| Offene-Punkte-Benennung | dt. / engl. | „## Offene Punkte" (dt.) | Einheitlich mit `feature-discover` |
| Override-Sichtbarkeit | im Dialog / in Spec markiert | In Spec markiert (HTML-Kommentar) | Review 4b — Begründung bleibt dauerhaft nachvollziehbar |
| Meta-Spec-Fehlalarm | Ausnahme-Regel / nur Override | Eng gefasste Ausnahme | Review 2b — Skill-Specs in diesem Repo sind Normalfall, nicht Rand |
| A/B-Bündelung | zusammen / getrennt | Zusammen, Phase 1 als Zwischen-Meilenstein | Review 1a — kleiner Umfang, Risiko-Entkopplung ohne Feature-Split |
| Abnahme-Design | 1 Lauf / mehrere Läufe | 3 Varianten × 2 Läufe, unabh. Agent | Review 3b — Heuristik-Determinismus belegen |
| Lint-Umsetzung | Prompt-Heuristik / externes Tool | Prompt-Heuristik | feature-plan hat kein Bash; keine neue Dependency |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [x] 1.1 Offene-Punkte ins Template — `e81965a`
- [x] 1.2 „nie erfinden" ersetzt [TODO] — `e81965a`
- [x] 1.3 Benennungs-Konsistenz — `e81965a`
- [x] 2.1 Lint-Kategorien-Block — `33e6bf4`
- [x] 2.2 Pre-Write-Gate — `33e6bf4`
- [x] 2.3 Override mit Begründung — `33e6bf4`
- [x] 3.1 Fixture + isolierte Abnahme — Scratchpad `spec-haertung-fixtures/` (kein Commit); unabh. Agent, 3 Varianten × 2 Läufe, gesamt PASS + 6 Ambiguitäten
- [x] 3.2 Findings beheben + Zeilen-Budget — `f18f281` (238 Z. < 280)
- [x] 3.3 kit-sync — feature-plan global übernommen (Lock `hash ff0d688`, `sourceCommit 7554e8d`); pitch-coach bewusst übersprungen (INBOX #8/#10)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_SPEC_HAERTUNG.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
