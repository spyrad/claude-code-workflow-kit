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
  consumes: [INBOX.md, BACKLOG.md, WORKFLOW_STATUS.md, DISCOVERY_*.md, FEATURE_*.md, PLAN_*.md, BUG_*.md, TASK_*.md]
  produces: [ARCHIVE_LOG.md, INBOX.md, BACKLOG.md, WORKFLOW_STATUS.md]
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

### Feature-Specs (abgeleitet, Regeln: `project-rules/DERIVED_STATE_RULES.md`)
- `FEATURE_*.md` mit explizitem `**Status:** Abgenommen` oder `Abgeschlossen`
- `FEATURE_*.md` deren `PLAN_*.md` vollstaendig abgehakt ist ("Fertig zum Testen") —
  NUR als Kandidat vorschlagen, Archivierung braucht explizite Bestaetigung
  (Regel-Datei §1.2: 100% Checkboxen ≠ automatisch abgeschlossen)

### Bug-Reports (abgeleitet, §1.5)
- `BUG_*.md` deren `## Fix-Schritte` vollstaendig abgehakt sind (= Behoben)

### Aufgaben (abgeleitet, §1.5)
- `TASK_*.md` deren `## Schritte` vollstaendig abgehakt sind (= Erledigt)

### Altlasten
- `IMPL_STATUS_*.md` Dateien (abgeschafftes Artefakt) — beim Archivieren des
  zugehoerigen Features mit verschieben; verwaiste IMPL_STATUS ohne aktives Feature
  direkt als Archiv-Kandidat vorschlagen

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

Aufgaben:
  - TASK_{NAME}.md (Erledigt)

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
| YYYY-MM-DD | Aufgabe | {Name} | TASK_*.md | Erledigt |
```

### 4b: Feature-Specs und Plaene verschieben

- Verschiebe abgeschlossene `FEATURE_*.md` von `{config.paths.workflows}/features/` nach `{config.paths.workflows}/archive/`
- Verschiebe die zugehoerige `DISCOVERY_*.md`, `PLAN_*.md` und `IMPL_STATUS_*.md` mit (falls vorhanden, gleicher Name)
- Setze beim Archivieren `**Status:** Abgeschlossen` in der Feature-Spec — die Archivierung IST der explizite Abschluss-Akt (Regel-Datei §1.2)
- Verschiebe behobene `BUG_*.md` von `{config.paths.workflows}/features/` nach `{config.paths.workflows}/archive/`
- Verschiebe erledigte `TASK_*.md` von `{config.paths.workflows}/features/` nach `{config.paths.workflows}/archive/`

### 4c: INBOX.md bereinigen

- Entferne archivierte Zeilen aus der Tabelle
- Nummern der verbleibenden Eintraege **nicht** neu vergeben (Luecken sind OK — die Nummern sind IDs)

### 4d: BACKLOG.md bereinigen

- Entferne archivierte Features aus dem Abschnitt "Abgeschlossen"
- Entferne archivierte Bugs aus dem Abschnitt "Bugs" (Status `Behoben`)
- Entferne archivierte Aufgaben aus dem Abschnitt "Aufgaben" (Status `Erledigt`)
- Abschnitt "Aktive Features" bleibt unberuehrt

### 4e: WORKFLOW_STATUS.md bereinigen

- Lies `{config.paths.workflows}/WORKFLOW_STATUS.md`
- Entferne Referenzen auf soeben archivierte Features, Bugs und Tasks
- Falls ein archiviertes Item dort als "aktiv" oder "in Arbeit" gefuehrt wird: **nicht entfernen**, sondern Warnung ausgeben

---

## Schritt 5: Bestaetigung

```
Archivierung abgeschlossen:

  Ideen archiviert:    {N}
  Features archiviert: {N}
  Aufgaben archiviert: {N}

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
