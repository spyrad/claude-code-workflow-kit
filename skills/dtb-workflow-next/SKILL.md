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
  consumes: [INBOX.md, DISCOVERY_*.md, FEATURE_*.md, PLAN_*.md, BUG_*.md, BACKLOG.md, WORKFLOW_STATUS.md]
  produces: []
---

# DTB Workflow-Next

Leichtgewichtiger "Workflow-GPS": Zeigt den konkreten naechsten Schritt pro aktivem Feature.

## Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 2: Alle aktiven Features scannen

Scanne die Workflow-Artefakte und bestimme pro Feature die aktuelle Pipeline-Position anhand vorhandener Artefakte:

**Quellen:**
- `{config.paths.workflows}/INBOX.md` — Eintraege mit Status `In Arbeit`
- `{config.paths.workflows}/features/DISCOVERY_*.md` — Discovery-Dokumente
- `{config.paths.workflows}/features/FEATURE_*.md` — Feature-Specs
- `{config.paths.workflows}/features/PLAN_*.md` — Implementierungsplaene (Status aus ersten 10 Zeilen)
- `{config.paths.workflows}/features/BUG_*.md` — Bug-Reports (Status aus ersten 10 Zeilen)
- `{config.paths.workflows}/BACKLOG.md` — Backlog-Eintraege mit Status

**Pipeline-Position pro Feature ermitteln:**

Fuer jedes Feature den "weitesten" Stand bestimmen:

**Feature-Pipeline:**

| Artefakt-Kombination | Pipeline-Position | Naechster Skill |
|---|---|---|
| INBOX `In Arbeit`, kein DISCOVERY | Discovery ausstehend | `/dtb:feature-discover` |
| DISCOVERY_*.md vorhanden, kein FEATURE | Spec ausstehend | `/dtb:feature-plan [NAME]` |
| FEATURE_*.md vorhanden, kein PLAN | Plan ausstehend | `/dtb:impl-plan [NAME]` |
| PLAN_*.md Status `Entwurf` | Review ausstehend | `/dtb:plan-review [NAME]` |
| PLAN_*.md Status `Reviewed` | Start ausstehend | `/dtb:feature-start` |
| BACKLOG Status `In Arbeit` | In Entwicklung | `/dtb:build-check` |
| BACKLOG Status `Fertig zum Testen` | Test ausstehend | Manuell testen |
| BACKLOG Status `Abgenommen` | Abschluss | `/dtb:workflow-checkpoint` |

**Bug-Pipeline:**

| Artefakt-Kombination | Pipeline-Position | Naechster Skill |
|---|---|---|
| BUG_*.md Status `Offen` | Analyse ausstehend | `/dtb:debug-plan [NAME]` |
| BUG_*.md Status `Analysiert` | Fix ausstehend | `/dtb:feature-start` oder direkt fixen |
| BUG_*.md Status `In Arbeit` | Fix in Arbeit | `/dtb:build-check` |
| BUG_*.md Status `Behoben` | Abschluss | `/dtb:workflow-checkpoint` |

## Schritt 3: Sortieren & priorisieren

- Features mit Status "In Arbeit" (Entwicklung) zuerst — die sind am weitesten
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
  Backlog        In Arbeit
  Build/Test     ○
  Abnahme        ○

→ Naechster Schritt: /dtb:build-check
```

## Richtlinien

- **Read-Only**: Dieser Skill aendert keine Dateien
- **Kompakt**: Max 15 Zeilen Output (ohne Argument), max 12 Zeilen (mit Argument)
- **Keine Rueckfragen**: Sofort Output liefern
- **Deutsch**: Alle Texte auf Deutsch
- **Leer-Zustand**: Bei 0 aktiven Features/Bugs: "Keine aktiven Features oder Bugs. Starte mit `/dtb:idea`, `/dtb:feature-plan` oder `/dtb:bug-report`."

## Verwandte Skills

- `/dtb:workflow-status` — Globale Pipeline-Visualisierung mit Queue-Details
- `/dtb:backlog-status` — Backlog-Details
- `/dtb:workflow-resume` — Session fortsetzen

---

Scanne jetzt die Workflow-Artefakte und zeige die naechsten Schritte.
