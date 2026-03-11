# Workflow-Status pruefen

Du analysierst die Status-Datei und zeigst den aktuellen Fortschritt an.

## Aufgabe

1. **Pruefe** ob `dtb-project/project-workflows/WORKFLOW_STATUS.md` existiert
   - Falls NEIN: Informiere "Kein Workflow-Status gefunden. Erstelle einen mit `/dtb:workflow-checkpoint`"
   - Falls JA: Fahre fort

2. **Lese** `dtb-project/project-workflows/WORKFLOW_STATUS.md`

3. **Extrahiere** die wichtigsten Informationen:
   - Session-Nummer und Datum
   - Quick Status Tabelle (Aktueller Schritt, Naechster Schritt, Blocker)
   - Erfolgsraten-Trend (falls vorhanden)
   - Bug-Tracker Status
   - Feature-Backlog Prioritaeten

4. **Zeige** formatierten Status:

```
+--------------------------------------------------+
|  WORKFLOW STATUS                                  |
+--------------------------------------------------+

Projekt: DTB-Assistant
Status: dtb-project/project-workflows/WORKFLOW_STATUS.md

Session:        [Session-Nummer] ([Datum])
Aktueller Fokus: [Aus Quick Status]
Naechster Schritt: [Aus Quick Status]

--------------------------------------------------
Blocker:        [Anzahl] - [Kurzbeschreibung]
--------------------------------------------------

Aktive Bugs:
- [Bug-ID]: [Status-Emoji] [Kurzbeschreibung]
- [Bug-ID]: [Status-Emoji] [Kurzbeschreibung]

Feature-Backlog (Top 3):
1. [Feature] - [Status]
2. [Feature] - [Status]
3. [Feature] - [Status]

Befehle:
- /dtb:workflow-checkpoint          → Session beenden (Log + Status)
- /dtb:workflow-resume      → Nach Session-Break fortfahren
```

## Zusaetzliche Informationen anzeigen

Falls vorhanden im Status, zeige auch:
- Erfolgsraten-Trend (ASCII-Balkendiagramm)
- Offene Projekt-Entscheidungen
- Session-Historie (letzte 5)

## Fehlerbehandlung

### Fehler: Datei nicht gefunden
```
Kein Workflow-Status gefunden.

Erstelle einen mit:
  /dtb:workflow-checkpoint

Oder pruefe ob `dtb-project/project-workflows/WORKFLOW_STATUS.md` existiert.
```

### Fehler: Status-Datei leer oder unlesbar
```
Warnung: WORKFLOW_STATUS.md ist leer oder hat unerwartetes Format.

Empfehlung:
1. Pruefe die Datei manuell
2. Erstelle neuen Status mit /dtb:workflow-checkpoint
```
