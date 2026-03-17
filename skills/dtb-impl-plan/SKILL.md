---
name: dtb:impl-plan
description: >-
  Use when: "Implementierungsplan", "impl plan", "Umsetzung planen",
  "Phasen planen". Creates a structured implementation plan (PLAN_*.md)
  based on an existing feature specification (FEATURE_*.md).
disable-model-invocation: true
argument-hint: "[Feature-Name]"
allowed-tools: Read, Glob, Grep, Write
pipeline:
  stage: planning
  after: dtb:feature-plan
  next: dtb:plan-review
  consumes: [FEATURE_*.md]
  produces: [PLAN_*.md]
---

# Implementierungsplan erstellen

Du bist ein Implementierungsplan-Manager. Deine Aufgabe ist es, basierend auf einer bestehenden Feature-Spec einen detaillierten Implementierungsplan zu erstellen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Aufgabe

1. **Feature-Name ermitteln:** Aus dem Argument oder Frage den Benutzer
2. **Feature-Spec lesen:** Lies `{config.paths.workflows}/features/FEATURE_[NAME].md`
3. **Analysiere** Ziel, Scope, Dependencies und Success Criteria aus der Feature-Spec
4. **Erstelle** den Implementierungsplan nach dem Template
5. **Speichere** in `{config.paths.workflows}/features/PLAN_[NAME].md`

## Template fuer PLAN_[NAME].md

Verwende folgende Struktur:

```markdown
# Implementierungsplan: [Feature-Name]

**Erstellt:** [Datum]
**Feature-Spec:** `features/FEATURE_[NAME].md`
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

#### Schritt 1: [Name]
- **Zweck:** [Warum?]
- **Dateien:** [Welche Dateien werden geaendert/erstellt?]
- **Input:** [Was wird benoetigt?]
- **Output:** [Was wird erzeugt?]
- **Geschaetzte Dauer:** [Zeit]

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

**Erstellt mit:** `/dtb:impl-plan`
```

---

## Wichtig - Anweisungen fuer die Ausfuehrung

### Beim Ausfuehren des Commands:

1. **Feature-Name ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Konvertiere zu UPPER_SNAKE_CASE fuer den Dateinamen (z.B. "Chat History" → `PLAN_CHAT_HISTORY.md`)

2. **Feature-Spec lesen:**
   - Lies `{config.paths.workflows}/features/FEATURE_[NAME].md`
   - Falls Datei nicht gefunden:
     ```
     Feature-Spec nicht gefunden: FEATURE_[NAME].md
     Erstelle zuerst eine Feature-Spec mit /dtb:feature-plan.
     ```

3. **Prüfe ob PLAN_*.md bereits existiert:**
   - Falls JA: Frage "Implementierungsplan existiert bereits. Soll ich ueberschreiben oder aktualisieren?"
   - Falls NEIN: Erstelle neue Datei

4. **Analysiere die Feature-Spec:**
   - Identifiziere Ziel und Scope
   - Leite sinnvolle Phasen ab (Reihenfolge, Abhaengigkeiten)
   - Beruecksichtige Risiken und Dependencies aus der Feature-Spec

5. **Fuelle das Template:**
   - Nutze konkrete Informationen aus der Feature-Spec und dem Chat-Verlauf
   - Bei fehlenden Infos: Nutze Platzhalter `[TODO: ...]`
   - Jede Phase braucht ein klares Ziel, Schritte mit Dateibezug, und Checkpoint-Kriterien
   - Technische Entscheidungen: Optionen auflisten, Entscheidung kann "Offen" sein

6. **Speichere die Datei**

7. **Bestaetige:**
   ```
   Implementierungsplan gespeichert: {config.paths.workflows}/features/PLAN_[NAME].md

   Naechste Schritte:
   1. Plan reviewen: /dtb:plan-review [Feature-Name]
   2. Feature starten: /dtb:feature-start
   ```

## Verwandte Commands

- `/dtb:feature-plan` — Feature-Spec erstellen
- `/dtb:plan-review` — Plan reviewen lassen
- `/dtb:feature-start` — Feature starten
