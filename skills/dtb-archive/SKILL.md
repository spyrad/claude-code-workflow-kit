---
name: dtb:archive
description: >-
  Use when: "aufraumen", "archivieren", "archive", "Inbox aufraumen",
  "alte Features entfernen", "Backlog aufraumen". Moves completed and
  discarded items from active workflow files into the archive directory.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [INBOX.md, BACKLOG.md, DISCOVERY_*.md, FEATURE_*.md, PLAN_*.md, BUG_*.md]
  produces: [ARCHIVE_LOG.md, INBOX.md, BACKLOG.md]
---

# Workflow archivieren

Du raeumst die aktiven Workflow-Dateien auf, indem du abgeschlossene und verworfene Eintraege ins Archiv verschiebst.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Archiv-Verzeichnis sicherstellen

Erstelle falls nicht vorhanden: `{config.paths.workflows}/archive/`

---

## Schritt 2: Archivierbare Eintraege sammeln

Pruefe die folgenden Quellen und sammle alle Kandidaten:

### INBOX.md
- Eintraege mit Status `Verworfen`
- Eintraege mit Status `Ausgearbeitet` (bereits als Feature-Plan vorhanden)

### BACKLOG.md
- Features im Abschnitt "Abgeschlossen"

### Feature-Specs
- `{config.paths.workflows}/features/FEATURE_*.md` mit `**Status:** Abgeschlossen`

### Bug-Reports
- `{config.paths.workflows}/features/BUG_*.md` mit `**Status:** Behoben`

---

## Schritt 3: Uebersicht zeigen

```
Archiv-Kandidaten gefunden:

Inbox:
  - #{N} "{Idee-Text}" (Verworfen)
  - #{N} "{Idee-Text}" (Ausgearbeitet → FEATURE_*.md)

Backlog:
  - {Feature-Name} (Abgeschlossen, {Datum})

Feature-Specs:
  - FEATURE_{NAME}.md (Abgeschlossen)

Bug-Reports:
  - BUG_{NAME}.md (Behoben)

Alles archivieren? (Ja / Auswahl treffen / Abbrechen)
```

Falls keine Kandidaten gefunden:
```
Nichts zu archivieren — alle Eintraege sind aktiv.
```

---

## Schritt 4: Archivieren

### 4a: Archiv-Log schreiben

Schreibe/ergaenze `{config.paths.workflows}/archive/ARCHIVE_LOG.md`:

```markdown
# Archiv-Log

| Datum | Typ | Name | Herkunft | Grund |
|-------|-----|------|----------|-------|
| YYYY-MM-DD | Idee | #{N} "{Text}" | INBOX.md | Verworfen |
| YYYY-MM-DD | Idee | #{N} "{Text}" | INBOX.md | Ausgearbeitet → FEATURE_*.md |
| YYYY-MM-DD | Feature | {Name} | BACKLOG.md | Abgeschlossen |
| YYYY-MM-DD | Bug | {Name} | BUG_*.md | Behoben |
```

### 4b: Feature-Specs und Plaene verschieben

- Verschiebe abgeschlossene `FEATURE_*.md` von `{config.paths.workflows}/features/` nach `{config.paths.workflows}/archive/`
- Verschiebe die zugehoerige `DISCOVERY_*.md` und `PLAN_*.md` mit (falls vorhanden, gleicher Name)
- Verschiebe behobene `BUG_*.md` von `{config.paths.workflows}/features/` nach `{config.paths.workflows}/archive/`

### 4c: INBOX.md bereinigen

- Entferne archivierte Zeilen aus der Tabelle
- Nummern der verbleibenden Eintraege **nicht** neu vergeben (Luecken sind OK — die Nummern sind IDs)

### 4d: BACKLOG.md bereinigen

- Entferne archivierte Features aus dem Abschnitt "Abgeschlossen"
- Abschnitt "Aktive Features" bleibt unberuehrt

---

## Schritt 5: Bestaetigung

```
Archivierung abgeschlossen:

  Ideen archiviert:    {N}
  Features archiviert: {N}

Archiv-Log: {config.paths.workflows}/archive/ARCHIVE_LOG.md
Feature-Specs: {config.paths.workflows}/archive/FEATURE_*.md (+ PLAN_*.md falls vorhanden)

Verbleibend in INBOX.md: {N} offene Ideen
Verbleibend in BACKLOG.md: {N} aktive Features
```

---

## Richtlinien

- **Keine aktiven Eintraege archivieren:** Nur Status "Verworfen", "Ausgearbeitet" (Inbox) und "Abgeschlossen" (Backlog/Features)
- **Immer bestaetigen:** Nichts archivieren ohne explizites OK vom Benutzer
- **Nummern beibehalten:** Inbox-Nummern sind IDs und werden nie wiederverwendet
- **Archiv-Log ist append-only:** Neue Eintraege anhaengen, nie ueberschreiben
- **Deutsch:** Alle Texte auf Deutsch
