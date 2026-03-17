---
name: dtb:workflow-checkpoint
description: >-
  Use when: "Session speichern", "checkpoint", "workflow checkpoint",
  "Session dokumentieren". Documents the current development session with
  a session log entry and updates WORKFLOW_STATUS.md.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
pipeline:
  stage: session
  after: null
  next: dtb:workflow-resume
  consumes: [BACKLOG.md, INBOX.md, FEATURE_*.md]
  produces: [WORKFLOW_STATUS.md, BACKLOG.md, FEATURE_*.md, session-log]
---

# DTB Workflow-Checkpoint (Log + Status)

Du dokumentierst den aktuellen Stand einer Development-Session. Zwei Aufgaben:
1. **Session-Log schreiben** (Tages-Changelog)
2. **WORKFLOW_STATUS.md aktualisieren** (kompaktes Status-Dashboard)

---

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfade `dtb-project/project-workflows/` und `dtb-project/project-changelog/`.

---

## Teil 1: Session-Log

### Datei
- Pfad: `{config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md`
- Falls Datei existiert: Neue Session anhaengen (mit `---` Trenner)
- Falls neu: Neue Datei erstellen

### Session-Nummer
- Zaehle vorhandene Sessions in der Datei
- Neue Session bekommt naechste Nummer
- Zeitstempel: Aktuelle Zeit (HH:MM Format)

### Format

```markdown
## Session {N} - {HH:MM}

### Implementiert
- Feature/Fix/Aenderung 1
- Feature/Fix/Aenderung 2

### Dateien
- `pfad/zur/datei.py` - Kurzbeschreibung der Aenderung

### Kontext
1-2 Saetze: Warum diese Aenderungen? Welches Problem wurde geloest?

### Naechste Schritte
- [ ] Offener Punkt 1
- [ ] Offener Punkt 2
```

### Richtlinien
- **Technisch**: Dateinamen, Funktionsnamen, konkrete Werte
- **Praezise**: Was genau wurde geaendert, nicht nur "Code optimiert"
- **Kontext**: Kurz erklaeren warum, nicht nur was
- **Deutsch**: Alle Texte auf Deutsch

---

## Teil 2: WORKFLOW_STATUS.md aktualisieren

### Datei
- Pfad: `{config.paths.workflows}/WORKFLOW_STATUS.md`
- **IMMER UEBERSCHREIBEN** (nicht anhaengen)
- **Max 60-80 Zeilen** — keine Detail-Tabellen, nur 1-Zeilen-Zusammenfassungen mit Links

### Template

```markdown
# Workflow-Status: {config.project_name}

**Letztes Update:** YYYY-MM-DD
**Letzter Session-Log:** `{config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md`

---

## Aktueller Stand

| Kennzahl | Wert |
|----------|------|
| **Laufende Arbeit** | [Was gerade offen ist] |
| **Naechster Schritt** | [Konkret] |
| **Blocker** | Keine / [Beschreibung] |

---

## Offene Aufgaben

- [ ] [Aufgabe 1] — Kontext: [kurz]
- [ ] [Aufgabe 2] — Kontext: [kurz]

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| YYYY-MM-DD | [Meilenstein] | [Ergebnis] | `[Link zu Quelle]` |

---

## Pausierte Themen

### [Ticket-ID]: [Titel]
**Status:** [Warum pausiert]
**Details:** `[Link zu Planfile oder Testbericht]`

---

## Session-Resume

Fuer neue Session: `/dtb:workflow-resume`
```

### Kernprinzip
- **Keine Detail-Tabellen** in WORKFLOW_STATUS
- Nur **1-Zeilen-Zusammenfassungen** mit Link zur Quelle
- Details leben in Session-Logs, Testberichten, Planfiles

---

## Ausfuehrung

### Schritt 1: Informationen sammeln

**Aus Chat-Verlauf:**
- Was wurde implementiert/geaendert?
- Welche Entscheidungen wurden getroffen?
- Was sind naechste Schritte?
- Gibt es Blocker?

**Aus Git (alle config.repos pruefen):**
```bash
git -C {repo.path} status --short && git -C {repo.path} log --oneline -3
```

### Schritt 2: Feature-Status pruefen

Lies `{config.paths.workflows}/BACKLOG.md` und pruefe ob die Arbeit dieser Session mit einem Feature zusammenhaengt:

1. **Vergleiche** die Chat-Inhalte mit den Features in BACKLOG.md (Abschnitt "Aktive Features")
2. **Falls ein Feature betroffen ist**, frage den Benutzer:

```
Feature-Status-Update erkannt:

Feature: {Feature-Name}
Aktueller Status: {aktueller Status aus BACKLOG}

Neuen Status setzen?
  1. In Arbeit
  2. Fertig zum Testen
  3. Abgenommen
  4. Abgeschlossen (deployed/merged)
  5. Pausiert
  6. Kein Update
```

3. **Bei Statusaenderung:**
   - Aktualisiere die Zeile in BACKLOG.md mit dem neuen Status
   - Bei **"Abgeschlossen"**: Verschiebe das Feature von "Aktive Features" nach "Abgeschlossen" mit aktuellem Datum
   - Aktualisiere das Datum in "Letzte Aktualisierung"
   - Aktualisiere auch den Status in der `features/FEATURE_*.md` Datei (Zeile `**Status:**`)

4. **Falls kein Feature erkannt wird**, ueberspringe diesen Schritt ohne Nachfrage.

### Schritt 3: Session-Log schreiben

### Schritt 4: WORKFLOW_STATUS.md aktualisieren
- Halte die 60-80 Zeilen-Grenze ein

### Schritt 5: Archiv-Hinweis pruefen

Zaehle in INBOX.md (Status `Verworfen` + `Ausgearbeitet`) und BACKLOG.md (Abschnitt "Abgeschlossen") die archivierbaren Eintraege.

- Falls >5 archivierbare Eintraege: Hinweis in die Bestaetigung aufnehmen
- Falls <=5: Keinen Hinweis zeigen

### Schritt 6: Bestaetigung

```
Workflow-Checkpoint dokumentiert:

Session-Log: {config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md (Session N)
Status: {config.paths.workflows}/WORKFLOW_STATUS.md
{Falls Feature-Update: "Feature-Update: {Feature-Name} → {neuer Status}"}

Naechster Schritt: [Konkret]
Blocker: [Keine / Beschreibung]
{Falls >5 archivierbare Eintraege: "Aufraumen: {N} Eintraege koennten archiviert werden → /dtb:archive"}

Fuer naechste Session: /dtb:workflow-resume
```
