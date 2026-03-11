# DTB Repo-Sync

Pruefe den Git-Status beider Repos und erkenne Cross-Repo-Abhaengigkeiten.

## Aufgabe

Erstelle einen kompakten Multi-Repo Status-Report fuer assistant-backend/ und assistant-frontend/.

## Schritt 1: Git-Status beider Repos

Fuehre fuer **beide** Repos (`assistant-backend/` und `assistant-frontend/`) aus:

```bash
# Pro Repo:
git -C {repo} status --short
git -C {repo} branch --show-current
git -C {repo} log --oneline -5
git -C {repo} remote -v
git -C {repo} diff --stat
```

## Schritt 2: Cross-Repo-Abhaengigkeiten pruefen

Pruefe ob Aenderungen in einem Repo Aenderungen im anderen erfordern:

1. **Event-Konsistenz**: Neue/geaenderte Events im Backend (`src/routes/`) muessen im Frontend (`src/events/event-list.tsx`) existieren
2. **Schema-Aenderungen**: Geaenderte Pydantic-Schemas (`src/schemas/`) muessen im Frontend-Typ-System reflektiert sein
3. **API-Aenderungen**: Neue Endpoints oder Payload-Aenderungen

## Schritt 3: Status-Report erstellen

Erstelle einen kompakten Report (max 60 Zeilen):

```markdown
# Repo-Sync Status
**Datum:** {DD.MM.YYYY HH:MM}

## Backend (assistant-backend/)
- **Branch:** {branch}
- **Status:** {clean / X uncommitted changes}
- **Letzte Commits:** {3 neueste, einzeilig}
- **Remote:** {sync status}

## Frontend (assistant-frontend/)
- **Branch:** {branch}
- **Status:** {clean / X uncommitted changes}
- **Letzte Commits:** {3 neueste, einzeilig}
- **Remote:** {sync status}

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
- **Cross-Repo-Fokus**: Der Mehrwert liegt in der Koordination, nicht im einzelnen `git status`

## Verwendung

Nutze diesen Command:
- Am Session-Start (nach `/dtb:workflow-resume`)
- Vor Commits (sind beide Repos konsistent?)
- Vor Deployments (gleicher Stand?)
- Bei Branch-Wechseln

## Verwandte Commands

- `/dtb:build-check` - Build/Test Verification
- `/dtb:workflow-resume` - Session-Start
- `/dtb:workflow-checkpoint` - Session-Ende

---

Pruefe jetzt den Status beider Repos und erstelle den Sync-Report.
