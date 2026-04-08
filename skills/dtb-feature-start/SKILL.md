---
name: dtb:feature-start
description: >-
  Use when: "Feature starten", "feature start", "naechstes Feature",
  "Feature aus Backlog starten", "Bug fixen", "Bug-Fix starten",
  "Aufgabe starten", "Task starten".
  Starts a planned feature, analyzed bug, or open task from the backlog
  by updating status to "In Arbeit" and showing the context.
disable-model-invocation: true
allowed-tools: Read, Write
pipeline:
  stage: implementation
  after: dtb:plan-review
  next: dtb:build-check
  consumes: [BACKLOG.md, FEATURE_*.md, PLAN_*.md, BUG_*.md, TASK_*.md]
  produces: [BACKLOG.md, WORKFLOW_STATUS.md, IMPL_STATUS_*.md, TASK_*.md]
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
2. **Filtere Features mit Status "Geplant"**
3. **Scanne Bug-Reports:** `{config.paths.workflows}/features/BUG_*.md`
4. **Filtere Bugs mit Status "Analysiert"** (haben einen Debug-Plan, sind bereit zum Fixen)
5. **Scanne Aufgaben:** `{config.paths.workflows}/features/TASK_*.md`
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
1. **Lies die Feature-Spec:** `{config.paths.workflows}/features/FEATURE_*.md`
2. **Lies den Implementierungsplan:** `{config.paths.workflows}/features/PLAN_*.md` (falls vorhanden)
3. **Setze Status in BACKLOG.md** auf "In Arbeit"
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Feature-Name eintragen

**Bei Bug:**
1. **Lies den Bug-Report:** `{config.paths.workflows}/features/BUG_*.md`
2. **Setze Status in BUG_*.md** von "Analysiert" auf "In Arbeit"
3. **Falls Bug in BACKLOG.md:** Setze Status auf "In Arbeit"
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Bug-Name eintragen

**Bei Aufgabe:**
1. **Lies die Aufgabe:** `{config.paths.workflows}/features/TASK_*.md`
2. **Setze Status in TASK_*.md** von "Offen" auf "In Arbeit"
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

[Falls PLAN_*.md vorhanden: Erste Phase aus dem Implementierungsplan mit Ziel und ersten Schritten]
[Falls PLAN_*.md NICHT vorhanden: "Kein Implementierungsplan vorhanden. Erstelle einen mit /dtb:impl-plan"]

## Arbeitsrhythmus: 3x3

[Falls PLAN_*.md vorhanden:]
Wir arbeiten im **3x3-Rhythmus**:
1. Ich setze max. 3 Schritte aus dem Plan um
2. Fasse zusammen was erledigt wurde
3. Beschreibe die naechsten 3 Schritte
4. Warte auf dein Feedback

Erster Block: Schritte [1.1 – 1.3 aus dem Plan]

Bei Kontextverlust oder nach >6 Schritten:
→ Erstelle `IMPL_STATUS_[NAME].md` und setze in neuer Konversation fort.

Bereit? Sage "Los" oder stelle Fragen.
```

**Bei Bug:**
```
# Bug-Fix gestartet: {Bug-Name}

**Status:** Analysiert → In Arbeit
**Severity:** {Severity}

## Symptom

[Symptom aus BUG_*.md]

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

[Beschreibung aus TASK_*.md]

## Schritte

[Schritte-Checkliste aus TASK_*.md]

Bereit? Sage "Los" oder stelle Fragen.
```

---

## Wichtig

- **Nur startbare Items:** Features mit Status "Geplant", Bugs mit Status "Analysiert" und Aufgaben mit Status "Offen" — keine "In Arbeit" oder "Abgeschlossen"
- **Status-Update:** BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden
- **Feature-Spec lesen:** Immer die vollstaendige Spec lesen um den Kontext zu zeigen
- **3x3-Rhythmus:** Wenn ein PLAN_*.md vorhanden ist, weise auf den Arbeitsrhythmus hin (max. 3 Schritte → Zusammenfassung → Feedback → naechste 3)
- **Kompakt:** Max 40 Zeilen Output
- **Deutsch:** Alle Texte auf Deutsch
