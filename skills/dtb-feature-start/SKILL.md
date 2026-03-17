---
name: dtb:feature-start
description: >-
  Use when: "Feature starten", "feature start", "naechstes Feature",
  "Feature aus Backlog starten". Starts a planned feature from the backlog
  by updating status to "In Arbeit" and showing the feature context.
disable-model-invocation: true
allowed-tools: Read, Write
pipeline:
  stage: implementation
  after: dtb:plan-review
  next: dtb:build-check
  consumes: [BACKLOG.md, FEATURE_*.md, PLAN_*.md]
  produces: [BACKLOG.md, WORKFLOW_STATUS.md]
---

# Neues Feature starten

Du startest ein neues Feature aus dem Backlog.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden.
Erstelle eine Config-Datei mit /dtb:project-init.
```

### Schritt 2: Backlog lesen

1. **Lies das Backlog:** `{config.paths.workflows}/BACKLOG.md`
2. **Filtere Features mit Status "Geplant"**

Falls keine Features mit Status "Geplant" vorhanden:
```
Keine geplanten Features im Backlog.
Alle Features sind bereits in Arbeit oder abgeschlossen.
```

### Schritt 3: Feature-Auswahl

Zeige die geplanten Features als Auswahlliste:

```
# Feature starten

Geplante Features im Backlog:
  1. {Feature-Name} ({Prio})
  2. {Feature-Name} ({Prio})
  ...

Welches Feature moechtest du starten?
```

### Schritt 4: Feature aktivieren

Nach Auswahl durch den Benutzer:

1. **Lies die Feature-Spec:** `{config.paths.workflows}/features/FEATURE_*.md` (passend zum gewaehlten Feature)
2. **Lies den Implementierungsplan:** `{config.paths.workflows}/features/PLAN_*.md` (passend zum gewaehlten Feature, falls vorhanden)
3. **Setze Status in BACKLOG.md** auf "In Arbeit"
4. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Feature-Name eintragen

### Schritt 5: Feature-Kontext zeigen

```
# Feature gestartet: {Feature-Name}

**Status:** Geplant → In Arbeit

## Feature-Uebersicht

[2-3 Zeilen aus Feature-Spec: Ziel, Scope]

## Naechster Schritt

[Falls PLAN_*.md vorhanden: Erste Phase aus dem Implementierungsplan mit Ziel und ersten Schritten]
[Falls PLAN_*.md NICHT vorhanden: "Kein Implementierungsplan vorhanden. Erstelle einen mit /dtb:impl-plan"]

Bereit? Sage "Los" oder stelle Fragen.
```

---

## Wichtig

- **Nur "Geplant":** Zeige ausschliesslich Features mit Status "Geplant", keine "In Arbeit" oder "Abgeschlossen"
- **Status-Update:** BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden
- **Feature-Spec lesen:** Immer die vollstaendige Spec lesen um den Kontext zu zeigen
- **Kompakt:** Max 40 Zeilen Output
- **Deutsch:** Alle Texte auf Deutsch
