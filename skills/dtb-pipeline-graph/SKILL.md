---
name: dtb:pipeline-graph
description: >-
  Use when: "Pipeline-Graph", "Pipeline-Graph generieren", "Pipeline Doku",
  "Toolkit Uebersicht", "Skills HTML", "Pipeline HTML generieren",
  "Skill-Matrix". Generates an interactive
  HTML overview of the entire skill pipeline from frontmatter metadata,
  styled per project-rules/STYLE.md.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: []
  produces: []
---

# DTB Pipeline-Graph

Generiert eine interaktive HTML-Uebersicht des gesamten Skill-Systems aus den Frontmatter-Metadaten aller Skills. Das Ergebnis ist eine einzelne, selbststaendige HTML-Datei mit Mermaid-Pipeline-Diagramm, Skill-Tabellen, Artefakt-Matrix und Agenten-Uebersicht.

## Schritt 0: Alle Skill-Frontmatter sammeln

Scanne alle Skill-Dateien:

```
Glob: skills/dtb-*/SKILL.md
```

Fuer jede gefundene SKILL.md: Lies die ersten 20 Zeilen und extrahiere aus dem YAML-Frontmatter:
- `name` (z.B. `dtb:workflow-status`)
- `description` (vollstaendiger Text)
- `disable-model-invocation` (true/false)
- `allowed-tools` (Liste)
- `pipeline.stage` (setup/idea/planning/implementation/development/session/monitoring/greenfield)
- `pipeline.after` (Liste von Vorgaenger-Skills, oder null)
- `pipeline.next` (Liste von Nachfolger-Skills, oder null)
- `pipeline.consumes` (Liste von Artefakt-Patterns)
- `pipeline.produces` (Liste von Artefakt-Patterns)

Speichere alle Daten in einer internen Liste, sortiert nach Stage.

## Schritt 1: Agenten sammeln

Scanne Agenten-Dateien:

```
Glob: ~/.claude/agents/*.md   (Fallback: agents/*.md im Projekt-Root, falls global leer)
```

Ignoriere `CLAUDE.md` im Agenten-Ordner. Fuer jede andere Datei: Lies die ersten 5 Zeilen und extrahiere:
- Dateiname (ohne `.md`)
- **Rolle:** Wert
- **Perspektive:** Wert

## Schritt 2: STYLE.md laden

Pruefe ob `dtb-project/project-rules/STYLE.md` existiert.

Falls ja: Verwende die CSS-Variablen und Font-Imports daraus fuer das HTML-Styling:
- Farbpalette (`--bg-primary`, `--bg-surface`, `--border`, `--accent`, etc.)
- Fonts (Lexend Deca + DM Mono)
- Dot-Grid Background
- Node/Connector Styles

Falls nein: Verwende ein neutrales Dark-Theme als Fallback:
```css
--bg-primary: #1a1a2e;
--bg-surface: #16213e;
--border: #3a3a5c;
--text-primary: #e0e0e0;
--text-muted: #888;
--accent: #4fc3f7;
```

## Schritt 3: Pipeline-Daten aufbereiten

### 3a: Stage-Gruppen bilden

Gruppiere Skills nach `pipeline.stage`. Verwende diese Reihenfolge und Labels:

| Stage | Label | Beschreibung |
|-------|-------|-------------|
| setup | Setup | Erstinitialisierung |
| idea | Idee | Ideenerfassung und -bewertung |
| planning | Planung | Feature-Spezifikation und Planung |
| implementation | Umsetzung | Feature-Start und Implementierung |
| development | Entwicklung | Build, Test, Review |
| session | Session | Checkpoint und Resume |
| monitoring | Monitoring | Read-Only Ueberwachung |
| greenfield | Greenfield | PRD und Roadmap |

### 3b: Pipeline-Edges ermitteln

Erstelle die Kanten des Pipeline-Graphen aus den `after`/`next` Feldern:
- Fuer jeden Skill mit `next != null`: Kante von Skill → next
- Fuer jeden Skill mit `after != null`: Kante von after → Skill (als Validierung)
- Dedupliziere Kanten

### 3c: Artefakt-Typen sammeln

Sammle alle einzigartigen Artefakt-Patterns aus `consumes` und `produces` aller Skills. Sortiere alphabetisch. Das sind die Spalten der Matrix.

## Schritt 4: HTML generieren

Erstelle eine einzelne HTML-Datei mit folgendem Aufbau. Alle Inhalte werden dynamisch aus den gesammelten Daten erzeugt — keine hartcodierten Skill-Listen.

### HTML-Grundstruktur

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude Code Workflow Kit — Pipeline & Artefakt-Uebersicht</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <style>
    [CSS aus STYLE.md — siehe Schritt 2]
    [Zusaetzliche Styles fuer Tabellen, Details/Summary, Footer]
  </style>
</head>
<body>
  <header>
    <h1 class="title">CLAUDE CODE WORKFLOW KIT</h1>
    <p class="subtitle">Pipeline & Artefakt-Uebersicht</p>
    <p class="meta">Generiert am [YYYY-MM-DD] — [N] Skills, [M] Agenten</p>
  </header>

  [Sektion 1: Pipeline-Flowchart]
  [Sektion 2: Hauptpipeline Text]
  [Sektion 3: Skill-Uebersicht nach Stage]
  [Sektion 4: Skill-Artefakt-Matrix]
  [Sektion 5: Artefakte & Speicherorte]
  [Sektion 6: Agenten]

  <footer>
    <p>Generiert mit <code>dtb:pipeline-graph</code> am [YYYY-MM-DD]</p>
  </footer>

  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {
        primaryColor: '#161616',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#3a3a3a',
        lineColor: '#4a4a4a',
        secondaryColor: '#161616',
        tertiaryColor: '#0a0a0a'
      }
    });
  </script>
</body>
</html>
```

### Sektion 1: Pipeline-Flowchart (Mermaid)

Generiere ein `flowchart TD` Diagramm. Fuer jede Stage-Gruppe einen `subgraph`:

```
flowchart TD
    subgraph SETUP["Setup"]
        init["dtb:project-init"]
        team["dtb:project-team"]
        ...
    end

    subgraph IDEA["Idee"]
        ...
    end

    ...

    %% Kanten aus Schritt 3b
    review --> fplan
    fplan --> iplan
    ...
```

Regeln:
- Knoten-ID: Skill-Name ohne `dtb:` Praefix, Bindestriche durch Unterstriche ersetzen
- Knoten-Label: Voller `dtb:*` Name
- Kanten nur zwischen Skills mit explizitem `after`/`next`; beide sind **Listen** → **eine Kante pro Element** (z.B. `project-init` → 3 Nachfolger, `feature-start` ← 2 Vorgaenger)
- Monitoring-Skills haben keine Kanten (standalone)

Wickle das Diagramm in ein `<div class="mermaid">` Element.

### Sektion 2: Hauptpipeline (Text)

Generiere die Pipeline als Textzeile:

```
Feature: project-init → idea → idea-review → feature-discover → feature-plan → impl-plan → plan-review → feature-start → build-check → code-review → workflow-checkpoint → workflow-resume
Bug:     bug-report → debug-plan → feature-start → build-check → code-review → workflow-checkpoint → workflow-resume
```

Zeige den typischen linearen Haupt-Durchlauf als Lesehilfe (Feature-/Bug-Pfad separat) — bewusst auf den dominanten Pfad linearisiert, **nicht** 1:1 kantenabgeleitet; die vollstaendigen Verzweigungen stehen im Flowchart (Sektion 1).

Wickle den Text in ein `<pre class="code">` Element mit der Annotation:
> Die Bug-Pipeline muendet bei `feature-start` in die Feature-Pipeline ein. Monitoring-Skills stehen seitlich — sie lesen quer ueber alle Artefakte.

### Sektion 3: Skill-Uebersicht nach Stage

Fuer jede Stage-Gruppe (in Reihenfolge aus Schritt 3a): Erstelle ein `<details>` Element (standardmaessig offen fuer die ersten 3 Gruppen) mit einer Tabelle:

```html
<details open>
  <summary>[Stage-Label] ([Anzahl] Skills)</summary>
  <table>
    <thead>
      <tr><th>Skill</th><th>Beschreibung</th><th>Vorgaenger</th><th>Nachfolger</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>dtb:skill-name</code></td>
        <td>[Englischer Teil der Description]</td>
        <td><code>dtb:after</code> oder —</td>
        <td><code>dtb:next</code> oder —</td>
      </tr>
      ...
    </tbody>
  </table>
</details>
```

Fuer Monitoring-Skills: Lasse die Spalten "Vorgaenger" und "Nachfolger" weg (immer null).

### Sektion 4: Skill-Artefakt-Matrix

Erstelle eine Matrix-Tabelle. Spaltenkoepfe = Artefakt-Patterns (aus Schritt 3c). Zeilen = Skills gruppiert nach Stage.

Zellwerte:
- Leer wenn der Skill das Artefakt weder liest noch schreibt
- `R` (mit Klasse `.pill`) wenn der Skill das Artefakt konsumiert
- `W` (mit Klasse `.pill .pill--active`) wenn der Skill das Artefakt produziert
- `R/W` wenn beides

Wickle die Matrix in ein `<details>` Element:

```html
<details>
  <summary>Skill-Artefakt-Matrix</summary>
  <div style="overflow-x: auto;">
    <table class="matrix">...</table>
  </div>
</details>
```

### Sektion 5: Artefakte & Speicherorte (statische Referenz)

| Artefakt | Pfad (im Zielprojekt) | Beschreibung |
|----------|----------------------|--------------|
| `workflow.config.yaml` | Projekt-Root | Single Source of Truth fuer Projektconfig |
| `CLAUDE.md` | Projekt-Root | Projektkontext fuer Claude Code |
| `INBOX.md` | `dtb-project/project-workflows/` | Ideen-Inbox |
| `BACKLOG.md` | `dtb-project/project-workflows/` | Feature-Backlog mit Priorisierung |
| `WORKFLOW_STATUS.md` | `dtb-project/project-workflows/` | Kompaktes Status-Dashboard |
| `features/<slug>/` | `dtb-project/project-workflows/features/<slug>/` | Change-Ordner (ein Ordner pro Change): `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md` |
| `session-log` | `dtb-project/project-changelog/YYYY-MM/` | Tages-Changelogs |
| `TEAM.md` | `dtb-project/project-strategy/` | Projektteam-Dokumentation |
| `ARCHIVE_LOG.md` | `dtb-project/project-workflows/archive/` | Log archivierter Eintraege |
| `project-rules/*.md` | `dtb-project/project-rules/` | Coding-Richtlinien + `lessons.md` (Prior, keine Rule) |
| `agents/*.md` | `~/.claude/agents/` (Fallback: `agents/`) | Agenten-Rollen |
| `PRD-MVP.md` | `dtb-project/project-strategy/` | Product Requirements Document |
| `ROADMAP.md` | `dtb-project/project-strategy/` | Strategische Projekt-Roadmap |

Wickle in `<details>` Element.

### Sektion 6: Agenten

Erstelle eine Tabelle aus den in Schritt 1 gesammelten Agenten-Daten:

```html
<details>
  <summary>Agenten ([Anzahl])</summary>
  <table>
    <thead><tr><th>Agent</th><th>Rolle</th><th>Perspektive</th></tr></thead>
    <tbody>
      <tr>
        <td><code>architekt</code></td>
        <td>Technischer Reviewer...</td>
        <td>Systemgrenzen, Seiteneffekte...</td>
      </tr>
      ...
    </tbody>
  </table>
</details>
```

### Zusaetzliche CSS-Styles

Ergaenze die Styles aus STYLE.md um diese tabellenspezifischen Regeln:

```css
/* Page Layout */
body {
  max-width: 1200px;
  margin: 0 auto;
}

header {
  text-align: center;
  margin-bottom: 48px;
}

.subtitle {
  font-size: 16px;
  color: var(--text-muted);
  margin-top: 8px;
}

.meta {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 16px;
}

/* Sections */
section {
  margin-bottom: 32px;
}

/* Details/Summary */
details {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 16px;
}

details[open] {
  border-color: var(--border-strong);
}

summary {
  font-family: 'Lexend Deca', sans-serif;
  font-size: 15px;
  font-weight: 600;
  padding: 16px 24px;
  cursor: pointer;
  color: var(--text-primary);
  user-select: none;
}

summary:hover {
  color: var(--accent);
}

details > :not(summary) {
  padding: 0 24px 24px;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  text-align: left;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border-strong);
}

td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
  vertical-align: top;
}

tr:last-child td {
  border-bottom: none;
}

code {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: var(--accent);
}

/* Matrix specifics */
.matrix th {
  writing-mode: vertical-lr;
  text-orientation: mixed;
  transform: rotate(180deg);
  max-width: 32px;
  padding: 12px 4px;
}

.matrix td {
  text-align: center;
  padding: 4px;
  min-width: 32px;
}

.matrix td.stage-header {
  text-align: left;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: 11px;
  padding-top: 16px;
}

/* Mermaid container */
.mermaid-container {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 16px;
  overflow-x: auto;
}

/* Pipeline text */
.pipeline-text {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 16px;
}

.pipeline-text pre {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-primary);
  white-space: pre-wrap;
}

.pipeline-text .annotation {
  margin-top: 16px;
  font-size: 13px;
  color: var(--text-muted);
  border-left: 3px solid var(--accent);
  padding-left: 12px;
}

/* Footer */
footer {
  text-align: center;
  padding: 32px 0;
  font-size: 12px;
  color: var(--text-muted);
  border-top: 1px solid var(--border);
  margin-top: 48px;
}
```

## Schritt 5: HTML-Datei schreiben

Schreibe die generierte HTML-Datei nach:

```
dtb-project/claude-code-workflow-kit.html
```

Im `dtb-project/` Verzeichnis.

## Schritt 6: Ergebnis melden

Gib dem Benutzer eine kurze Zusammenfassung:

```
Pipeline-Graph generiert: dtb-project/claude-code-workflow-kit.html
- [N] Skills in [M] Stages
- [K] Artefakt-Typen in der Matrix
- [L] Agenten
→ Im Browser oeffnen: start dtb-project/claude-code-workflow-kit.html
```

## Richtlinien

- **Dynamisch**: Alle Inhalte aus Frontmatter generieren — keine hartcodierten Listen
- **Selbststaendig**: Einzelne HTML-Datei, kein externer CSS (nur Mermaid CDN + Google Fonts)
- **STYLE.md respektieren**: CSS-Variablen und Designprinzipien uebernehmen
- **Deutsch**: Alle sichtbaren Texte auf Deutsch
- **Kompakt**: Collapsible Sections, damit die Seite nicht ueberladen wirkt
- **Artefakt-Tabelle**: Statischer Inhalt (Pfade aendern sich selten), Rest dynamisch

## Verwandte Skills

- `/dtb:workflow-status` — Laufzeit-Pipeline-Status eines Zielprojekts
- `/dtb:project-health` — Konsistenz-Audit des Projekts
- `/dtb:backlog-status` — Backlog-Uebersicht
