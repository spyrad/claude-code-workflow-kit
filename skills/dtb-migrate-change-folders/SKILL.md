---
name: dtb:migrate-change-folders
description: >-
  Use when: "auf Change-Folder migrieren", "Ordner-Modell migrieren",
  "migrate change folders", "flaches Layout umstellen", "features migrieren".
  One-time migration of a project's flat features/ layout (FEATURE_*/PLAN_*/…)
  into the Change-Folder model (features/<slug>/ with fixed filenames).
disable-model-invocation: true
argument-hint: ""
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: setup
  after: null
  next: null
  consumes: [features/*.md, archive/*.md]
  produces: [features/*/*.md, archive/*/*.md]
---

# Change-Folder-Migration

Einmaliges Werkzeug: Konvertiert ein Projekt vom **flachen** Layout
(`features/FEATURE_X.md` + `PLAN_X.md` + …, gepaart per Namen) ins
**Change-Folder-Modell** (`features/<slug>/` mit fixen Dateinamen `discovery.md`/`spec.md`/
`plan.md`/`bug.md`/`task.md`). Slug-/Ableitungsregeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4.

Idempotent und sicher: bereits migrierte Projekte werden erkannt, uncommittete/kollidierende
Zustaende brechen sauber ab, unbekannte Fremd-Dateien werden nie geraten.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root. Fehlt sie: Fallback `dtb-project/project-workflows/`.

---

## Schritt 1: Layout-Selbsterkennung

Scanne **beide** Bereiche `{config.paths.workflows}/features/` UND `{config.paths.workflows}/archive/`
(falls vorhanden) auf lose `.md`-Dateien:

- **Lose `.md` in features/ oder archive/** (z.B. `FEATURE_*.md`, `PLAN_*.md`) → flaches Layout,
  Migration noetig — den jeweils flachen Bereich migrieren (features/ in Schritt 4, archive/ in Schritt 5)
- **Beide Bereiche frei von losen `.md`** (nur Unterordner + evtl. `ARCHIVE_LOG.md`) → bereits migriert.
  Dies IST der Eligibility-Gate von `migrate` (Konvention: `skills/CLAUDE.md` → „Eligibility-Gates") —
  kritische Vorbedingung sind flache Alt-Dateien; ohne sie kein Redirect (`after: null`), nur ehrliche Meldung:
  ```
  Projekt ist bereits im Change-Folder-Modell — nichts zu migrieren.
  ```
  sauber beenden (kein Fehler)
- **Gemischt** (Ordner UND lose Dateien) → nur die losen Dateien migrieren, vorhandene Ordner
  unangetastet lassen (idempotenter Wiederlauf). Die „bereits migriert"-Abkuerzung greift nur,
  wenn BEIDE Bereiche frei von losen `.md` sind.

---

## Schritt 2: Sicherheits-Guards

**„Betroffene Pfade"** = ausschliesslich die Kategorie-A-Quelldateien (erkannte Praefixe, Schritt 3)
in `features/` UND `archive/`. Kategorie-B-Dateien loesen NIE einen Abbruch aus (sie werden nicht angefasst).

**Git-Erkennung:** `git -C {Projekt-Root} rev-parse --is-inside-work-tree 2>/dev/null`

- **Git-Repo vorhanden:**
  - Pruefe `git status --short` fuer die betroffenen Pfade. **Modifizierte getrackte Dateien**
    (` M`, `MM`, `AM` an einer zu migrierenden Datei) → **ABBRUCH** mit Meldung (kein Move+Edit-Mix):
    ```
    ❌ Uncommittete Aenderungen an zu migrierenden Dateien — bitte erst committen, dann erneut migrieren.
    ```
  - **Ungetrackte** betroffene Dateien (`??`) sind KEIN Abbruchgrund — sie werden in Schritt 4
    per Dateisystem-Move + `git add` behandelt (nicht `git mv`, das scheitert an Ungetracktem)
  - Getrackte, unveraenderte Dateien → `git mv` (erhaelt Historie)
- **Kein Git-Repo:**
  - **PFLICHT-Backup** vor jeder Aenderung: kopiere den kompletten `features/`-Baum (und
    `archive/`, falls vorhanden) nach `{config.paths.workflows}/.migration-backup-{Datum}/`
    (Datum aus dem Kontext, nie raten). **Existiert der Backup-Ordner schon** (abgebrochener
    Vorlauf) → nicht ueberschreiben, Suffix `-2`/`-3` anhaengen
  - Laute Warnung ausgeben:
    ```
    ⚠ Kein Git-Repo — Dateisystem-Move ohne Versionshistorie. Backup unter .migration-backup-{Datum}/ angelegt.
    ```
  - Verschiebe spaeter per Dateisystem-Move

---

## Schritt 3: Namens-Taxonomie (Mapping bestimmen, nichts raten)

Ordne jede lose Datei in `features/` einer Kategorie zu:

**A. Erkannte Praefixe → Change-Ordner-Datei** (Basis-Name = Teil nach dem Praefix):

| Flache Datei | Ziel im Ordner |
|--------------|----------------|
| `FEATURE_<NAME>.md` | `<slug>/spec.md` |
| `DISCOVERY_<NAME>.md` | `<slug>/discovery.md` |
| `PLAN_<NAME>.md` | `<slug>/plan.md` |
| `BUG_<NAME>.md` | `<slug>/bug.md` |
| `TASK_<NAME>.md` | `<slug>/task.md` |

`<slug>` = kebab-case aus `<NAME>` (§4). Dateien mit gleichem `<NAME>` landen im **selben** Ordner
(Teil-Paarungen wie nur `FEATURE`, `FEATURE`+`PLAN`, `FEATURE`+`PLAN`+`DISCOVERY` korrekt falten).

**B. Abgeschafft/fremd → NICHT migrieren, in Drift-Report als „manuell pruefen":**
- `IMPL_STATUS_*.md` (abgeschafftes Artefakt) — Hinweis: Stand ggf. manuell in `plan.md` `## Progress` uebertragen
- `WORKFLOW_*_PLAN.md` / `WORKFLOW_*_STATUS.md` (Alt-Konvention)
- nicht-praefigierte Dateien (z.B. `finn-018-...md`) — kein erkennbarer Change-Bezug
- ein separater `bugs/`-Ordner neben `features/` — Inhalt melden, nicht automatisch einfalten

**C. Kollisions-Check (pro Bereich):** Leiten zwei verschiedene `<NAME>` **im selben Bereich**
(`features/` bzw. `archive/`) denselben `<slug>` ab → **ABBRUCH** mit Meldung der kollidierenden
Namen (§4, kein Auto-Suffix); Nutzer benennt eine Quelle um. Gleicher Slug in `features/` UND
`archive/` ist KEINE Kollision (verschiedene Elternordner).

---

## Schritt 4: Migration durchfuehren (idempotent)

Fuer jeden Ziel-`<slug>` aus Kategorie A:

1. Ziel-Ordner **zuerst anlegen** — `mkdir -p features/<slug>` (Pflicht vor jedem Move; `git mv`
   legt den Zielordner NICHT selbst an). Existiert die Ziel-Datei bereits → **ueberspringen** (idempotent)
2. Jede zugehoerige Quelldatei in ihre Ziel-Datei verschieben:
   - Git, getrackt+unveraendert: `mkdir -p features/<slug> && git mv features/<NAME-Datei> features/<slug>/<ziel>.md`
   - Git, ungetrackt (`??`): `mkdir -p features/<slug>`, Dateisystem-Move, dann `git add features/<slug>/<ziel>.md`
   - Non-Git: Dateisystem-Move
3. Kategorie-B-Dateien bleiben unangetastet

---

## Schritt 5: Archiv migrieren

Falls `{config.paths.workflows}/archive/` existiert, dieselbe Taxonomie (Schritt 3+4) auf die
flachen Dateien darin anwenden → `archive/<slug>/…`. `ARCHIVE_LOG.md` bleibt liegen (keine
Change-Datei). Kategorie-B im Archiv ebenfalls nur melden.

---

## Schritt 6: Drift-Report

```
Change-Folder-Migration abgeschlossen ({Git-Repo|Dateisystem-Move + Backup}):

Migriert:  {N} Change-Ordner ({M} Dateien) in features/
Archiv:    {N} Change-Ordner in archive/

Nicht migriert (manuell pruefen):
  - IMPL_STATUS_<NAME>.md — Stand ggf. in plan.md ## Progress uebertragen
  - WORKFLOW_<NAME>_PLAN.md / _STATUS.md — Alt-Konvention, Zuordnung unklar
  - <datei> — nicht-praefigiert, kein Change-Bezug
  - bugs/ — separater Ordner, {K} Dateien

Naechster Schritt: /dtb:project-health (verifiziert Ordner-Vollstaendigkeit + Querverweise)
```

Falls Backlog/WORKFLOW_STATUS `Datei`-Spalten noch auf flache Pfade zeigen: Hinweis, dass
`/dtb:workflow-checkpoint` die Anzeige-Felder beim naechsten Lauf nachzieht (dieser Helfer
fasst nur `features/`/`archive/` an, keine Status-Anzeigen).

---

## Richtlinien

- **Einmalig & idempotent:** gefahrlos wiederholbar; bereits migrierte Projekte werden erkannt
- **Nichts raten:** unbekannte/fremde Dateien werden gemeldet, nie automatisch zugeordnet
- **Sicher:** Git → `git mv`; kein Git → Pflicht-Backup + Move; uncommitteter/kollidierender Stand → Abbruch
- **Deutsch:** Alle Texte auf Deutsch
