# DTB Build-Check

Strukturierter Build/Test-Check ueber beide Repos vor Deploy.

## Aufgabe

Fuehre alle Build- und Test-Schritte aus und erstelle einen Deploy-Readiness Report.

## Schritt 1: Backend Tests

```bash
cd assistant-backend
set PYTHON_TEST_ENVIRONMENT=TRUE
python -m pytest --tb=short -q
```

Erfasse: Anzahl Tests, Passed, Failed, Errors, Warnungen.

## Schritt 2: Frontend Build

```bash
cd assistant-frontend
npx tsc --noEmit
npm run build
```

Erfasse: TypeScript-Fehler, Build-Erfolg/Fehler, Bundle-Groesse.

## Schritt 3: Event-Konsistenz

Pruefe ob alle Backend-Events im Frontend registriert sind:

1. Lies alle Event-Namen aus `assistant-backend/src/routes/` (Pattern: `@fastws.post("EVENT_*")`)
2. Lies alle Events aus `assistant-frontend/src/events/event-list.tsx`
3. Vergleiche: Fehlende Events im Frontend? Verwaiste Events?

## Schritt 4: Deploy-Readiness Report

```markdown
# Build-Check Report
**Datum:** {DD.MM.YYYY HH:MM}

## Ergebnis-Uebersicht

| Check | Status | Details |
|-------|--------|---------|
| Backend Tests | {PASS/FAIL} | {X passed, Y failed} |
| Frontend TypeScript | {PASS/FAIL} | {X errors} |
| Frontend Build | {PASS/FAIL} | {Bundle-Info} |
| Event-Konsistenz | {PASS/WARN} | {Details} |

## Gesamt-Status: {DEPLOY-READY / NICHT READY}

## Fehler-Details (falls vorhanden)

### Backend
{Fehlermeldungen oder "Alle Tests bestanden"}

### Frontend
{TypeScript-Fehler oder "Keine Fehler"}

### Events
{Inkonsistenzen oder "Alle Events konsistent"}

## Empfehlung
{Konkreter naechster Schritt}
```

## Richtlinien

- **Ausfuehren, nicht nur beschreiben**: Tests und Builds tatsaechlich laufen lassen
- **Fehler-Fokus**: Bei Erfolg kurz, bei Fehlern detailliert
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Bei Fehlern konkrete Fix-Empfehlungen

## Verwendung

Nutze diesen Command:
- Vor Deployments auf DEV/PROD
- Nach groesseren Refactorings
- Vor Pull Requests
- Als Smoke-Test nach Merges

## Verwandte Commands

- `/dtb:repo-sync` - Git-Status beider Repos
- `/dtb:code-review` - Code-Review
- `/dtb:workflow-checkpoint` - Session-Ende

---

Fuehre jetzt den Build-Check durch und erstelle den Report.
