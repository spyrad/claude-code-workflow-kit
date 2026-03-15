---
name: dtb:repo-sync
description: >-
  Use when: "Repo-Status", "repo sync", "Git-Status aller Repos",
  "Cross-Repo pruefen". Checks git status of all configured repos
  and detects cross-repo dependency issues.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# DTB Repo-Sync

Pruefe den Git-Status aller konfigurierten Repos und erkenne Cross-Repo-Abhaengigkeiten.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden. Erstelle eine Config mit repos-Eintraegen.
```

### Schritt 2: Git-Status aller Repos

Fuer jeden Eintrag in `config.repos`:
```bash
git -C {repo.path} status --short
git -C {repo.path} branch --show-current
git -C {repo.path} log --oneline -5
git -C {repo.path} remote -v
git -C {repo.path} diff --stat
```

### Schritt 3: Cross-Repo-Abhaengigkeiten pruefen

Falls mehrere Repos konfiguriert, pruefe:
1. **Event-Konsistenz**: Neue/geaenderte Events im Backend muessen im Frontend existieren
2. **Schema-Aenderungen**: Geaenderte Schemas muessen im anderen Repo reflektiert sein
3. **API-Aenderungen**: Neue Endpoints oder Payload-Aenderungen

### Schritt 4: Status-Report

Erstelle einen kompakten Report (max 60 Zeilen):

```markdown
# Repo-Sync Status
**Datum:** {DD.MM.YYYY HH:MM}

## {repo.name} ({repo.path}/)
- **Branch:** {branch}
- **Status:** {clean / X uncommitted changes}
- **Letzte Commits:** {3 neueste, einzeilig}
- **Remote:** {sync status}

[Fuer jeden Eintrag in config.repos]

## Cross-Repo
- **Event-Konsistenz:** {OK / Warnung}
- **Schema-Sync:** {OK / Warnung}
- **Abhaengigkeiten:** {Keine / Liste}

## Empfohlene Aktionen
1. {Aktion mit Begruendung}
```

## Richtlinien

- **Kompakt**: Max 60 Zeilen Output
- **Actionable**: Konkrete Empfehlungen, nicht nur Status
- **Deutsch**: Alle Texte auf Deutsch
- **Cross-Repo-Fokus**: Mehrwert liegt in der Koordination

## Verwandte Commands

- `/dtb:build-check` - Build/Test Verification
- `/dtb:workflow-resume` - Session-Start
- `/dtb:workflow-checkpoint` - Session-Ende

---

Pruefe jetzt den Status aller Repos und erstelle den Sync-Report.
