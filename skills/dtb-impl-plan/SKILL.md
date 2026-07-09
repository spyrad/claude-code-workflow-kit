---
name: dtb:impl-plan
description: >-
  Use when: "Implementierungsplan", "impl plan", "Umsetzung planen",
  "Phasen planen". Creates a structured implementation plan (features/<slug>/plan.md)
  based on an existing feature specification (features/<slug>/spec.md).
disable-model-invocation: true
argument-hint: "[Feature-Name]"
allowed-tools: Read, Glob, Grep, Write
pipeline:
  stage: planning
  after: [dtb:feature-plan]
  next: [dtb:plan-review]
  consumes: [features/*/spec.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md]
  produces: [features/*/plan.md]
---

# Implementierungsplan erstellen

Du bist ein Implementierungsplan-Manager. Deine Aufgabe ist es, basierend auf einer bestehenden Feature-Spec einen detaillierten Implementierungsplan zu erstellen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `impl-plan` oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen bei der Planerstellung still an
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei nach dem Filter behaltene Lektionen mit gegensaetzlicher `Rule` — z.B. „immer X" vs. „nie X" zum selben Gegenstand):
  beide zeigen und den Widerspruch melden — nicht selbst aufloesen

## Aufgabe

1. **Feature-Name / Slug ermitteln:** Aus dem Argument oder Frage den Benutzer
2. **Feature-Spec lesen:** Lies `{config.paths.workflows}/features/{slug}/spec.md`
3. **Analysiere** Ziel, Scope, Dependencies und Success Criteria aus der Feature-Spec
4. **Erstelle** den Implementierungsplan nach dem Template
5. **Speichere** in `{config.paths.workflows}/features/{slug}/plan.md`

## Template fuer plan.md

Verwende folgende Struktur:

```markdown
# Implementierungsplan: [Feature-Name]

**Erstellt:** [Datum]
**Feature-Spec:** `features/{slug}/spec.md`
**Geschaetzte Dauer:** [Gesamt]
**Status:** Entwurf / Reviewed / In Umsetzung / Abgeschlossen

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | [Name] | [Zeit] | Geplant |

---

## Phase 1: [Name]

### Ziel
[Was soll erreicht werden?]

### Schritte

#### Schritt 1.1: [Name]
- **Zweck:** [Warum?]
- **Dateien:** [Welche Dateien werden geaendert/erstellt?]
- **Input:** [Was wird benoetigt?]
- **Output:** [Was wird erzeugt?]

#### Schritt 1.2: [Name]
...

#### Schritt 1.3: [Name]
...

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] [Output 1]

### Checkpoint-Kriterien
- [ ] [Kriterium 1]

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| [Thema] | [A, B] | [Offen/A/B] | [Warum?] |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [ ] 1.1 [Kurzname]
- [ ] 1.2 [Kurzname]
- [ ] 1.3 [Kurzname]
- [ ] 2.1 [Kurzname]

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/{slug}/plan.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
```

---

## Wichtig - Anweisungen fuer die Ausfuehrung

### Beim Ausfuehren des Commands:

1. **Feature-Name / Slug ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Leite den **kebab-case-Slug** ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "Chat History" → `features/chat-history/`)

2. **Feature-Spec lesen:**
   - Lies `{config.paths.workflows}/features/{slug}/spec.md`
   - Falls Datei nicht gefunden:
     ```
     Feature-Spec nicht gefunden: features/{slug}/spec.md
     Erstelle zuerst eine Feature-Spec mit /dtb:feature-plan.
     ```

3. **Prüfe ob `features/{slug}/plan.md` bereits existiert:**
   - Falls JA: Frage "Implementierungsplan existiert bereits. Soll ich ueberschreiben oder aktualisieren?"
   - Falls NEIN: Erstelle neue Datei (Ordner existiert bereits durch die Spec)

4. **Analysiere die Feature-Spec:**
   - Identifiziere Ziel und Scope
   - Leite sinnvolle Phasen ab (Reihenfolge, Abhaengigkeiten)
   - Beruecksichtige Risiken und Dependencies aus der Feature-Spec

5. **Fuelle das Template:**
   - Nutze konkrete Informationen aus der Feature-Spec und dem Chat-Verlauf
   - Bei fehlenden Infos: Nutze Platzhalter `[TODO: ...]`
   - Jede Phase braucht ein klares Ziel, Schritte mit Dateibezug, und Checkpoint-Kriterien
   - Technische Entscheidungen: Optionen auflisten, Entscheidung kann "Offen" sein
   - **3x3-Blockung:** Nummeriere Schritte fortlaufend pro Phase (1.1, 1.2, 1.3, 1.4 ...) und setze nach jedem 3. Schritt einen `> 3x3-Block`-Hinweis. Jeder Schritt soll ein konkretes, testbares Ergebnis liefern.
   - **Progress-Sektion (Pflicht):** Erzeuge fuer JEDEN Schritt N.M genau eine Checkbox-Zeile `- [ ] N.M Kurzname` in `## Progress`. Format gemaess `project-rules/DERIVED_STATE_RULES.md`: 1 Zeile pro Schritt, keine Prosa, SHA-Beleg kommt erst beim Abhaken dazu. Diese Sektion ist die Single Source of Truth fuer den Umsetzungsstand — es gibt KEIN separates Status-Artefakt (IMPL_STATUS_*.md ist abgeschafft).
   - **Max. 500 Zeilen** — laengere Plaene verschlechtern die AI-Verarbeitung. Bei sehr grossen Features: in mehrere Phasen-Dateien aufteilen oder Details in Schritten knapp halten.

6. **Speichere die Datei**

7. **Bestaetige:**
   ```
   Implementierungsplan gespeichert: {config.paths.workflows}/features/{slug}/plan.md

   Naechste Schritte:
   1. Plan reviewen: /dtb:plan-review [Feature-Name]
   2. Feature starten: /dtb:feature-start
   ```

## Lektion-Kandidat erkennen (Vorschlager)

Wenn dir waehrend der Planung eine nicht-offensichtliche, wiederverwendbare Erkenntnis auffaellt
(Trigger-Frage: „Wuerde ich denselben Fehler nochmal machen, wenn das nur im Session-Log stuende?"),
schlage sie zur Aufnahme vor — **nie stiller Auto-Write**:
```
💡 Lektion-Kandidat: "{knappe Regel}". Nach lessons.md uebernehmen? (/dtb:lesson oder ja/nein)
```
Bei „ja": den Text an `/dtb:lesson` uebergeben.

## Verwandte Commands

- `/dtb:feature-plan` — Feature-Spec erstellen
- `/dtb:plan-review` — Plan reviewen lassen
- `/dtb:feature-start` — Feature starten
- `/dtb:lesson` — Lektion festhalten (Prior-Quelle)
