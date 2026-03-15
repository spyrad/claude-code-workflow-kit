---
name: dtb:workflow-resume
description: >-
  Use when: "Session fortsetzen", "workflow resume", "wo war ich",
  "Kontext wiederherstellen". Restores workflow context after a session break
  by reading WORKFLOW_STATUS.md, session logs, and git status.
disable-model-invocation: true
---

# Workflow fortsetzen (Resume)

Du stellst den Workflow-Kontext nach einem Session-Break wieder her.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden.
Erstelle eine Config-Datei mit /dtb:project-init.
```

### Schritt 2: Status & Session-Log lesen

1. **Lies die Status-Datei:** `{config.paths.workflows}/WORKFLOW_STATUS.md`
2. **Lies den neuesten Session-Log:** `{config.paths.changelog}/` (neueste Datei im neuesten Monats-Ordner)
3. **Lies das Backlog:** `{config.paths.workflows}/BACKLOG.md`

Falls WORKFLOW_STATUS.md nicht existiert:
```
WORKFLOW_STATUS.md nicht gefunden.
Empfehlung: Am Ende dieser Session /dtb:workflow-checkpoint ausfuehren.
```

### Schritt 3: Git-Status pruefen

Fuer jeden Eintrag in `config.repos`:
```bash
git -C {repo.path} branch --show-current && git -C {repo.path} log --oneline -3 && git -C {repo.path} status --short
```

### Schritt 4: Feature-Kontext bestimmen

Pruefe ob ein Feature aktiv bearbeitet wird:

1. Lies BACKLOG.md und suche Features mit Status **"In Arbeit"**
2. Pruefe WORKFLOW_STATUS.md ob "Laufende Arbeit" ein Feature referenziert

**Fall A: Feature "In Arbeit" erkannt**
- Lies die zugehoerige Feature-Spec (`features/FEATURE_*.md`)
- Zeige Feature-Kontext im Resume-Report (aktueller Stand, naechste Phase/Schritt)

**Fall B: Mehrere Features "In Arbeit"**
- Zeige Auswahlliste der laufenden Features
- User waehlt welches Feature fortgesetzt wird

**Fall C: Kein Feature "In Arbeit"**
- Hinweis: "Kein aktives Feature. Starte eines mit `/dtb:feature-start`"

### Schritt 5: Resume-Report

Halte den Report **kompakt** (max 60 Zeilen Output). Fokus auf Actionable Info.

**Fall A: Mit aktivem Feature**

```
# Resume: {config.project_name}

**Feature:** {Feature-Name} (Status: In Arbeit)
**Letzte Session:** {Datum}

## Feature-Stand

[2-3 Zeilen aus Feature-Spec: Aktuelle Phase, was ist offen]

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}

## Naechster Schritt

[Konkret: Was jetzt tun, welche Dateien]

Bereit? Sage "Los" oder stelle Fragen.
```

**Fall B: Mehrere Features "In Arbeit"**

```
# Resume: {config.project_name}

**Letzte Session:** {Datum}
**Zusammenfassung:** [1 Satz aus WORKFLOW_STATUS "Laufende Arbeit"]

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}

## Feature fortsetzen

Folgende Features sind in Arbeit:
  1. {Feature-Name} ({Prio})
  2. {Feature-Name} ({Prio})

Welches Feature moechtest du fortsetzen?
```

**Bei Feature-Auswahl durch den Benutzer:**
1. Lies die Feature-Spec (`features/FEATURE_*.md`)
2. Zeige Feature-Kontext (aktuelle Phase, naechster Schritt)

**Fall C: Kein Feature "In Arbeit"**

```
# Resume: {config.project_name}

**Letzte Session:** {Datum}
**Zusammenfassung:** [1 Satz aus WORKFLOW_STATUS "Laufende Arbeit"]

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}

---

Kein aktives Feature. Starte eines mit `/dtb:feature-start`.
```

---

## Wichtig

- **Actionable:** Benutzer muss sofort wissen was zu tun ist
- **Kompakt:** Max 60 Zeilen Report, keine Detail-Tabellen
- **Feature-Kontext:** Bei aktivem Feature die Spec lesen und relevante Phase zeigen
- **Deutsch:** Alle Texte auf Deutsch
- Am Ende immer fragen ob Benutzer starten oder Fragen hat
