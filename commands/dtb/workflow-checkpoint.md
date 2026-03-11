# DTB Workflow-Checkpoint (Log + Status)

Du dokumentierst den aktuellen Stand einer Development-Session. Zwei Aufgaben:
1. **Session-Log schreiben** (Tages-Changelog)
2. **WORKFLOW_STATUS.md aktualisieren** (kompaktes Status-Dashboard)

---

## Teil 1: Session-Log

### Datei
- Pfad: `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md`
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
- **Lesbar**: Bullet Points, keine langen Absaetze

---

## Teil 2: WORKFLOW_STATUS.md aktualisieren

### Datei
- Pfad: `dtb-project/project-workflows/WORKFLOW_STATUS.md`
- **IMMER UEBERSCHREIBEN** (nicht anhaengen)
- **Max 60-80 Zeilen** — keine Detail-Tabellen, nur 1-Zeilen-Zusammenfassungen mit Links

### Template

```markdown
# Workflow-Status: DTB-Assistant

**Letztes Update:** YYYY-MM-DD
**Letzter Session-Log:** `project-changelog/YYYY-MM/YYYY-MM-DD.md`

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
| ... | ... | ... | ... |

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
- **Keine Detail-Tabellen** in WORKFLOW_STATUS (keine V11-Einzelergebnisse, keine Tuning-Matrizen)
- Nur **1-Zeilen-Zusammenfassungen** mit Link zur Quelle
- Details leben in:
  - Session-Logs (`project-changelog/`)
  - Testberichte (`project-testing/`)
  - Planfiles (`.claude/plans/`)
- Meilenstein-Tabelle: nur abgeschlossene Dinge, jeweils 1 Zeile

---

## Ausfuehrung

### Schritt 1: Informationen sammeln

**Aus Chat-Verlauf:**
- Was wurde implementiert/geaendert?
- Welche Entscheidungen wurden getroffen?
- Was sind naechste Schritte?
- Gibt es Blocker?

**Aus Git (beide Repos pruefen):**
```bash
cd assistant-backend && git status --short && git log --oneline -3 && cd ..
cd assistant-frontend && git status --short && git log --oneline -3 && cd ..
```

### Schritt 2: Session-Log schreiben
- Erstelle/aktualisiere die Tages-Datei
- Halte das Format ein (Implementiert, Dateien, Kontext, Naechste Schritte)
- Sei praezise und technisch

### Schritt 3: WORKFLOW_STATUS.md aktualisieren
- Lies den aktuellen Stand
- Aktualisiere mit neuem Status
- **Halte die 60-80 Zeilen-Grenze ein**
- Verschiebe abgeschlossene Detail-Tabellen NICHT in die Status-Datei — sie gehoeren in die Session-Logs/Testberichte

### Schritt 4: Bestaetigung

```
Workflow-Checkpoint dokumentiert:

Session-Log: dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md (Session N)
Status: dtb-project/project-workflows/WORKFLOW_STATUS.md

Naechster Schritt: [Konkret]
Blocker: [Keine / Beschreibung]

Fuer naechste Session: /dtb:workflow-resume
```
