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
2. **Setze Status in BACKLOG.md** auf "In Arbeit"
3. **Aktualisiere WORKFLOW_STATUS.md:** "Laufende Arbeit" → Feature-Name eintragen

### Schritt 5: Feature-Kontext zeigen

```
# Feature gestartet: {Feature-Name}

**Status:** Geplant → In Arbeit

## Feature-Uebersicht

[2-3 Zeilen aus Feature-Spec: Ziel, Scope]

## Naechster Schritt

[Konkret: Erste Phase/Aufgabe aus der Feature-Spec, welche Dateien]

Bereit? Sage "Los" oder stelle Fragen.
```

---

## Wichtig

- **Nur "Geplant":** Zeige ausschliesslich Features mit Status "Geplant", keine "In Arbeit" oder "Abgeschlossen"
- **Status-Update:** BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden
- **Feature-Spec lesen:** Immer die vollstaendige Spec lesen um den Kontext zu zeigen
- **Kompakt:** Max 40 Zeilen Output
- **Deutsch:** Alle Texte auf Deutsch
