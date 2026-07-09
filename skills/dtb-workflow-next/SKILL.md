---
name: dtb:workflow-next
description: >-
  Use when: "was steht an", "naechster Schritt", "wo war ich",
  "workflow next", "was mache ich als naechstes". Read-only skill
  showing the concrete next action per active feature based on
  artifact existence and pipeline position.
disable-model-invocation: false
argument-hint: "[Feature-Name]"
allowed-tools: Read, Glob, Grep
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [INBOX.md, features/*/discovery.md, features/*/spec.md, features/*/plan.md, features/*/bug.md, features/*/task.md, BACKLOG.md, WORKFLOW_STATUS.md, project-rules/DERIVED_STATE_RULES.md]
  produces: []
---

# DTB Workflow-Next

Leichtgewichtiger "Workflow-GPS": Zeigt den konkreten naechsten Schritt pro aktivem Feature.

## Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 2: Alle aktiven Features scannen

**Ableitungsregel:** Der Status wird aus Artefakten ABGELEITET, nie aus Statusfeldern
uebernommen — verbindliche Regeln in `{config.paths.rules}/DERIVED_STATE_RULES.md`
(Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`). Lies diese Datei zuerst.
Statusfelder in BACKLOG.md dienen nur der Konflikterkennung (siehe Schritt 3).

**Quellen:**
- `{config.paths.workflows}/INBOX.md` — Eintraege mit Status `In Arbeit`
- `{config.paths.workflows}/features/*/discovery.md` — Discovery-Dokumente
- `{config.paths.workflows}/features/*/spec.md` — Feature-Specs
- `{config.paths.workflows}/features/*/plan.md` — Implementierungsplaene: `## Progress`-Checkboxen zaehlen (X von Y abgehakt); Plan-Status (`Entwurf`/`Reviewed`) aus den ersten 10 Zeilen
- `{config.paths.workflows}/features/*/bug.md`, `task.md` — Checkliste in der Datei zaehlen (`## Fix-Schritte` bzw. `## Schritte`)
- `{config.paths.workflows}/BACKLOG.md` — NUR fuer Konflikterkennung und Prio

**Pipeline-Position pro Feature ermitteln (abgeleitet):**

**Feature-Pipeline:**

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| INBOX `In Arbeit`, kein Change-Ordner | Discovery ausstehend | `/dtb:feature-discover` |
| `discovery.md` vorhanden, kein `spec.md` | Spec ausstehend | `/dtb:feature-plan [NAME]` |
| `spec.md` vorhanden, kein `plan.md` | Plan ausstehend | `/dtb:impl-plan [NAME]` |
| `plan.md` Status `Entwurf` | Review ausstehend | `/dtb:plan-review [NAME]` |
| `plan.md` Status `Reviewed`, 0/Y Checkboxen | Start ausstehend | `/dtb:feature-start` |
| `plan.md` teilweise abgehakt (X/Y) | In Entwicklung | Schritt {erster nicht abgehakter N.M} umsetzen |
| `plan.md` alle Checkboxen abgehakt | Fertig zum Testen | Manuell testen, dann `/dtb:archive` |
| Ordner in `archive/<slug>/` | Abgeschlossen | — |

**Bug-Pipeline** (Checkliste = `## Fix-Schritte` im Bug-Report):

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| kein Analyse-Abschnitt (nur Symptom) | Analyse ausstehend | `/dtb:debug-plan [NAME]` |
| Analyse vorhanden, 0 Fix-Schritte abgehakt | Fix ausstehend | `/dtb:feature-start` oder direkt fixen |
| Fix-Schritte teilweise abgehakt | Fix in Arbeit | naechsten Fix-Schritt umsetzen |
| alle Fix-Schritte abgehakt | Test/Abschluss | Testplan ausfuehren, `/dtb:workflow-checkpoint` |

**Aufgaben-Pipeline** (Checkliste = `## Schritte` in `task.md`):

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| 0 Schritte abgehakt | Start ausstehend | `/dtb:feature-start` |
| teilweise abgehakt | In Arbeit | naechsten Schritt umsetzen |
| alle abgehakt | Abschluss | `/dtb:workflow-checkpoint` |

**Fallbacks (kein Abbruch, siehe Regel-Datei §1.4):**
- `plan.md` ohne `## Progress` oder mit 0 Checkbox-Zeilen → "Plan vorhanden, Fortschritt unbekannt"; Nachruestung anbieten
- Flache Alt-Dateien (`PLAN_*.md` etc.) oder `IMPL_STATUS_*.md` direkt in `features/` (Altbestand) → fuer Ableitung ignorieren, Migrations-Hinweis (`/dtb:migrate-change-folders`)
- Ordner mit `plan.md` ohne `spec.md` → als "Change ohne Spec" melden
- Explizit `Pausiert` markierte Items → nicht anzeigen (ueberschreibt Ableitung)

## Schritt 3: Konflikte erkennen, sortieren & priorisieren

**Konfliktregel (Regel-Datei §1.3):** Weicht ein BACKLOG-Statusfeld vom abgeleiteten
Zustand ab, gewinnt das Artefakt. Den Widerspruch mit 1 Hinweiszeile melden
(`⚠ BACKLOG sagt "{Feld}", Artefakte zeigen "{abgeleitet}"`), NICHT selbst korrigieren (read-only).

- Abgeleitet "In Entwicklung" zuerst — die sind am weitesten
- Dann nach Pipeline-Position absteigend (weiter fortgeschritten = hoehere Prio)
- Falls ein Argument uebergeben wurde: Nur dieses Feature zeigen

## Schritt 4: Kompakt ausgeben

### Ohne Argument (alle aktiven Features):

```
Naechste Schritte:

1. {Feature-Name}  → /dtb:{skill} [NAME]
   ({Status-Detail})
2. {Feature-Name}  → /dtb:{skill} [NAME]
   ({Status-Detail})
...

{N} weitere Feature-Specs ohne Plan → /dtb:impl-plan
```

### Mit Argument (ein Feature im Detail):

```
{Feature-Name}:
  Inbox          ✓
  Discovery      ✓ (YYYY-MM-DD)
  Feature-Spec   ✓ (YYYY-MM-DD)
  Impl-Plan      ✓ Reviewed
  Progress       X/Y Schritte (abgeleitet)
  Build/Test     ○
  Abnahme        ○

→ Naechster Schritt: {erster nicht abgehakter Schritt N.M aus ## Progress}
{falls Konflikt: ⚠ BACKLOG sagt "...", Artefakte zeigen "..."}
```

## Richtlinien

- **Read-Only**: Dieser Skill aendert keine Dateien
- **Kompakt**: Max 15 Zeilen Output (ohne Argument), max 12 Zeilen (mit Argument)
- **Keine Rueckfragen**: Sofort Output liefern
- **Deutsch**: Alle Texte auf Deutsch
- **Leer-Zustand**: Bei 0 aktiven Features/Bugs/Aufgaben: "Keine aktiven Features, Bugs oder Aufgaben. Starte mit `/dtb:idea`, `/dtb:feature-plan`, `/dtb:bug-report` oder `/dtb:task`."

## Verwandte Skills

- `/dtb:workflow-status` — Globale Pipeline-Visualisierung mit Queue-Details
- `/dtb:backlog-status` — Backlog-Details
- `/dtb:workflow-resume` — Session fortsetzen

---

Scanne jetzt die Workflow-Artefakte und zeige die naechsten Schritte.
