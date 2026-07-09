---
name: dtb:feature-start
description: >-
  Use when: "Feature starten", "feature start", "naechstes Feature",
  "Feature aus Backlog starten", "Bug fixen", "Bug-Fix starten",
  "Aufgabe starten", "Task starten".
  Starts a planned feature, analyzed bug, or open task from the backlog
  by updating status to "In Arbeit" and showing the context.
disable-model-invocation: true
allowed-tools: Read, Write, Edit
pipeline:
  stage: implementation
  after: [dtb:plan-review, dtb:debug-plan]
  next: [dtb:build-check]
  consumes: [BACKLOG.md, features/*/spec.md, features/*/plan.md, features/*/bug.md, features/*/task.md, project-rules/DERIVED_STATE_RULES.md]
  produces: [BACKLOG.md, WORKFLOW_STATUS.md, features/*/plan.md, features/*/task.md]
---

# Feature, Bug-Fix oder Aufgabe starten

Du startest ein neues Feature aus dem Backlog, einen analysierten Bug-Fix oder eine offene Aufgabe.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden.
Erstelle eine Config-Datei mit /dtb:project-init.
```

### Schritt 2: Backlog, Bugs und Tasks lesen

1. **Lies das Backlog:** `{config.paths.workflows}/BACKLOG.md`
2. **Filtere Features mit Status "Geplant"** (Change-Ordner mit `plan.md`, 0 Progress-Checkboxen)
3. **Scanne Bug-Reports:** `{config.paths.workflows}/features/*/bug.md`
4. **Filtere Bugs mit Status "Analysiert"** (haben einen Debug-Plan, sind bereit zum Fixen)
5. **Scanne Aufgaben:** `{config.paths.workflows}/features/*/task.md`
6. **Filtere Tasks mit Status "Offen"**

Falls weder geplante Features, analysierte Bugs noch offene Aufgaben vorhanden:
```
Nichts zu starten — keine geplanten Features, analysierten Bugs oder offenen Aufgaben.
```

### Schritt 3: Auswahl

Zeige Features, Bugs und Aufgaben als gemeinsame Auswahlliste:

```
# Feature / Bug-Fix / Aufgabe starten

Geplante Features:
  1. {Feature-Name} ({Prio})
  2. {Feature-Name} ({Prio})

Analysierte Bugs:
  3. Bug: {Bug-Name} ({Severity})
  4. Bug: {Bug-Name} ({Severity})

Offene Aufgaben:
  5. Aufgabe: {Aufgaben-Name} ({Prio})
  6. Aufgabe: {Aufgaben-Name} ({Prio})

Was moechtest du starten?
```

Falls nur eine oder zwei Kategorien vorhanden: Zeige nur die relevanten Sektionen.

### Schritt 4: Aktivieren

Nach Auswahl durch den Benutzer:

**Bei Feature:**
1. **Lies die Feature-Spec:** `{config.paths.workflows}/features/{slug}/spec.md`
2. **Lies den Implementierungsplan:** `{config.paths.workflows}/features/{slug}/plan.md` (falls vorhanden)
   — die `## Progress`-Sektion bestimmt den Einstiegspunkt (erster nicht abgehakter Schritt).
   Falls der Plan keine `## Progress`-Sektion hat (Altbestand): Nachruestung anbieten
   (Fallback gemaess `project-rules/DERIVED_STATE_RULES.md`)
3. **Setze Status in BACKLOG.md** auf "In Arbeit" (abgeleitete Anzeige, siehe Regeln)
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Feature-Name eintragen

**Bei Bug:**
1. **Lies den Bug-Report:** `{config.paths.workflows}/features/{slug}/bug.md`
2. **Setze Status in `bug.md`** von "Analysiert" auf "In Arbeit"
3. **Falls Bug in BACKLOG.md:** Setze Status auf "In Arbeit"
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Bug-Name eintragen

**Bei Aufgabe:**
1. **Lies die Aufgabe:** `{config.paths.workflows}/features/{slug}/task.md`
2. **Setze Status in `task.md`** von "Offen" auf "In Arbeit"
3. **Falls Aufgabe in BACKLOG.md:** Setze Status auf "In Arbeit"
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Aufgaben-Name eintragen

### Schritt 5: Kontext zeigen

**Bei Feature:**
```
# Feature gestartet: {Feature-Name}

**Status:** Geplant → In Arbeit

## Feature-Uebersicht

[2-3 Zeilen aus Feature-Spec: Ziel, Scope]

## Naechster Schritt

[Falls `plan.md` vorhanden: Erste Phase aus dem Implementierungsplan mit Ziel und ersten Schritten]
[Falls `plan.md` NICHT vorhanden: "Kein Implementierungsplan vorhanden. Erstelle einen mit /dtb:impl-plan"]

## Arbeitsrhythmus: 3x3

[Falls `plan.md` vorhanden:]
Wir arbeiten im **3x3-Rhythmus**:
1. Ich setze max. 3 Schritte aus dem Plan um
2. Hake erledigte Schritte in der `## Progress`-Sektion des Plans ab (Commit-SHA als Beleg)
3. Fasse zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. Warte auf dein Feedback

Erster Block: Schritte [erste 3 nicht abgehakte Schritte aus `## Progress`]

Bei Kontextverlust oder nach >6 Schritten:
→ `## Progress` in `features/{slug}/plan.md` ist der Wiedereinstiegspunkt — in neuer Konversation
  den Plan laden; der erste nicht abgehakte Schritt ist der naechste.

Bereit? Sage "Los" oder stelle Fragen.
```

**Bei Bug:**
```
# Bug-Fix gestartet: {Bug-Name}

**Status:** Analysiert → In Arbeit
**Severity:** {Severity}

## Symptom

[Symptom aus `bug.md`]

## Root-Cause

[Wahrscheinlichste Hypothese aus Analyse-Abschnitt]

## Fix-Schritte

[Fix-Schritte aus Analyse-Abschnitt]

## Testplan

[Testplan aus Analyse-Abschnitt]

Bereit? Sage "Los" oder stelle Fragen.
```

**Bei Aufgabe:**
```
# Aufgabe gestartet: {Aufgaben-Name}

**Status:** Offen → In Arbeit
**Prioritaet:** {Prio}

## Beschreibung

[Beschreibung aus `task.md`]

## Schritte

[Schritte-Checkliste aus `task.md`]

Bereit? Sage "Los" oder stelle Fragen.
```

---

## Wichtig

- **Nur startbare Items:** Features mit Status "Geplant", Bugs mit Status "Analysiert" und Aufgaben mit Status "Offen" — keine "In Arbeit" oder "Abgeschlossen"
- **Status-Update:** BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden
- **Checkbox-Pflicht im Implementierungs-Loop:** Nach JEDEM umgesetzten Schritt sofort die Checkbox in der `## Progress`-Sektion des Plans abhaken — mit Commit-SHA als Beleg (`- [x] N.M Kurzname — \`SHA\``; SHA optional bei Schritten ohne Commit, ein Commit darf mehrere Checkboxen belegen). Nicht gesammelt am Session-Ende. Die Progress-Sektion ist die Single Source of Truth (`project-rules/DERIVED_STATE_RULES.md`) — es gibt kein IMPL_STATUS_*.md mehr
- **Feature-Spec lesen:** Immer die vollstaendige Spec lesen um den Kontext zu zeigen
- **3x3-Rhythmus:** Wenn ein `plan.md` vorhanden ist, weise auf den Arbeitsrhythmus hin (max. 3 Schritte → Zusammenfassung → Feedback → naechste 3)
- **Kompakt:** Max 40 Zeilen Output
- **Deutsch:** Alle Texte auf Deutsch
