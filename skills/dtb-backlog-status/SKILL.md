---
name: dtb:backlog-status
description: >-
  Use when: "Backlog zeigen", "backlog status", "offene Features",
  "was steht an". Read-only overview of open features, priorities,
  and current progress from BACKLOG.md and features/*/spec.md files.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [BACKLOG.md, features/*/spec.md, features/*/plan.md, features/*/bug.md, features/*/task.md, features/*/worker-report.md, project-rules/DERIVED_STATE_RULES.md, workflow.config.yaml]
  produces: []
---

# DTB Backlog-Status

Schneller Read-Only-Ueberblick ueber offene Features, Prioritaeten und aktuellen Fortschritt.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Backlog laden

Lies die Datei:
- **`{config.paths.workflows}/BACKLOG.md`**

Die Status-Spalte ist eine **abgeleitete Anzeige** — verwende sie NICHT als Quelle.
Manuell gepflegt (und damit verbindlich) sind nur Prio und Ziel.

## Schritt 2: Status ableiten

**Ableitungsregel:** verbindliche Regeln in `{config.paths.rules}/DERIVED_STATE_RULES.md`
(Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`). Lies diese Datei zuerst.

Finde alle Change-Ordner `{config.paths.workflows}/features/*/` und lies deren `spec.md`,
`plan.md`, `bug.md`, `task.md`; leite den Status pro Item ab:

- **Features:** `spec.md` ohne `plan.md` → Spezifiziert; `plan.md` vorhanden + 0 Checkboxen → Geplant (das Kopf-Statusfeld ist status-neutral und wird hier NICHT gelesen — Regel-Datei §7.4);
  `## Progress` teilweise abgehakt → In Arbeit (X/Y); vollstaendig → Fertig zum Testen
- **Bugs:** `bug.md` Analyse-Abschnitt + `## Fix-Schritte`-Checkliste zaehlen (Offen/Analysiert/In Arbeit/Behoben)
- **Tasks:** `task.md` `## Schritte`-Checkliste zaehlen (Offen/In Arbeit/Erledigt)
- **Fallbacks (Regel-Datei §1.4):** `plan.md` ohne Progress → "Fortschritt unbekannt"; flache Alt-Dateien/IMPL_STATUS_*.md
  ignorieren + Migrations-Hinweis; explizit `Pausiert` → als Pausiert zeigen (ueberschreibt Ableitung)
- **Explizit `Abgenommen` (Regel-Datei §1.2, gespiegelte Lese-Regel — Grep-Anker, eine Zeile):**
  Ein gesetztes `Abgenommen` ueberschreibt die Ableitung „Fertig zum Testen" und ist KEIN Konflikt nach §1.3 (analog `Pausiert`).
  Als Abgenommen zeigen (Abschnitt "Fertig zum Testen / Abgenommen")

## Schritt 3: Abgleich

Vergleiche die gefundenen Dateien mit den Eintraegen in BACKLOG.md:
- Markiere Features/Bugs/Tasks die in BACKLOG.md **fehlen** (Datei existiert aber kein Backlog-Eintrag)
- **Konflikte melden (Regel-Datei §1.3):** Weicht die BACKLOG-Status-Spalte vom abgeleiteten
  Status ab, gewinnt das Artefakt — 1 Hinweiszeile pro Widerspruch im Report, Feld NICHT
  korrigieren (read-only)
- **Ausnahme `Abgenommen` (§1.2):** kein Konflikt (Lese-Regel in Schritt 2). **Konflikt ist genau
  eine Kombination:** `**Status:** Abgenommen` gesetzt UND `## Progress` unvollstaendig (< Y/Y) —
  dann 1 Hinweiszeile: `⚠ {Item}: Feld sagt "Abgenommen", ## Progress zeigt "{X/Y}"`.
  Still-Regel: Feld fehlt oder traegt den (mit der Ableitung uebereinstimmenden) Wert → still; jeder andere Nicht-`Abgenommen`-Wert faellt unter die normale Konfliktregel §1.3.

## Schritt 3b: Worktree-Stand

Die Backlog-Uebersicht zeigt, woran gerade ausserhalb des Haupt-Checkouts gearbeitet wird.

**Worktree-Stand (operative Kopie von Regel-Datei §10 — rein lesend).**
Kernsatz: Die Sichten zeigen unter `In Worktrees` je verlinktem Worktree genau eine Zeile — gelesen, nie beschrieben.
- **Quelle:** `git worktree list --porcelain`; der **erste** Eintrag ist der Haupt-Checkout und wird nicht
  gelistet; die Zeilen folgen der Reihenfolge der Liste. Kein Git-Repo (`git rev-parse --git-dir` scheitert) oder
  kein weiterer Worktree → Block entfaellt still (kein „keine"); scheitert `worktree list` IM Git-Repo → genau eine
  Zeile `In Worktrees: nicht lesbar ({Fehler})` — nie still schlucken
- **Slug / Art:** Verzeichnisname ohne Praefix `pane-`/`worker-`. `pane-` → `interaktiv (pane)`; `worker-` mit
  Branch → `autonom (pane)`; `worker-` detached → `autonom (subagent)`; alles andere → `manuell`
- **Hauptbranch:** `parallel.default_branch` aus `workflow.config.yaml`, sonst Branch des ersten Eintrags — nie
  zwischen master/main raten
- **Stand** — erster zutreffender Zustand gilt; n = `git rev-list --count {haupt}..{branch}`, Reflog =
  `git reflog show refs/heads/{branch}`:
  1. Eintrag traegt `prunable` oder Pfad fehlt → `verwaist → git worktree prune` (Rest der Zeile entfaellt)
  2. n > 0 → `+{n} Commits, zuletzt YYYY-MM-DD` (`git log -1 --format=%cs {branch}`) — `laufend`
  3. n = 0 UND Reflog hat mehr als den Anlage-Eintrag → `gemergt → aufraeumen (git worktree remove "{pfad}")`;
     bei uncommitted > 0 stattdessen `gemergt, {N} uncommitted → erst sichern` (nie zum Entfernen raten, solange
     Arbeit ungesichert ist); in beiden Faellen entfaellt der Rest der Zeile
  4. sonst (n = 0, Reflog nur mit Anlage-Eintrag oder fehlend) → `frisch` — nie „aufraeumen"
- **uncommitted:** Zeilen von `git -C {pfad} status --porcelain`. **Fortschritt** aus dem Worktree-Pfad (inkl.
  uncommitteter Flips): `{pfad}/{config.paths.workflows}/features/{slug}/plan.md` `## Progress` → `Progress X/Y` ·
  sonst `task.md` `## Schritte` → `Schritte X/Y` · sonst Stage-Name (Regel-Datei §1.1, z.B. `Discovery`) · sonst `—`
- **Detached** (Subagent-Worker): Branch-Feld `detached @{sha7}`, Feld „Stand" entfaellt, statt Fortschritt
  `worker-report {vorhanden | fehlt}` (Datei im Change-Ordner unter `{pfad}`)
- **⏳** am Zeilenende bei `laufend` und `frisch`, wenn der letzte Commit (bei `frisch`: der Anlage-Eintrag im
  Reflog) ≥ `status.alter_schwelle_tage` Tage alt ist (Default 7)
- **Nur lesend:** erlaubt sind ausschliesslich die Kommandos oben (`worktree list`, `rev-list --count`,
  `log -1`, `reflog show`, `rev-parse --git-dir`, `-C {pfad} status --porcelain`) und das Lesen von Dateien unter `{pfad}`. Nie
  `checkout`, `add`, `commit`, `stash`, `worktree remove`/`prune` — „aufraeumen"/„prune" sind Hinweise an den Menschen

```
In Worktrees:
  {slug}  {Art}  {branch | detached @sha7}  {Stand}  {N} uncommitted  {Fortschritt}[  ⏳]
```

> **Wartungs-Hinweis (Format-Kopplung):** spiegelt §10 (Kopie ist Absicht, §10 — Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22);
> Aenderung dort → hier UND in den beiden anderen Sichten mitziehen (`dtb:workflow-resume`, `dtb:workflow-next`,
> `dtb:backlog-status` — der Block ist in allen dreien wortgleich; Grep-Anker: `In Worktrees`).

## Schritt 4: Backlog-Report erstellen

Erstelle einen kompakten Report:

```markdown
# Backlog-Status
**Datum:** {DD.MM.YYYY}

## Aktiv (in Arbeit)
| Feature | Status (abgeleitet) | Prio | Fortschritt | Datei | Ziel |
|---------|---------------------|------|-------------|-------|------|
| {Feature} | {abgeleiteter Status} | {Prio} | {X/Y} | {Datei} | {Ziel} |

{Falls Konflikte: ⚠ {Item}: BACKLOG sagt "{Feld}", Artefakte zeigen "{abgeleitet}"}

## In Worktrees
{Zeilen aus Schritt 3b ohne Kopfzeile — Abschnitt entfaellt still, wenn der Block entfaellt}

## Geplant (priorisiert)
| Feature | Status | Prio | Plan | Datei | Ziel |
|---------|--------|------|------|-------|------|
| {Feature} | Geplant | {Prio} | ✅/❌ | {Datei} | {Ziel} |

## Ideen / Backlog
- {Feature}: {Einzeiler-Beschreibung}

## Fertig zum Testen / Abgenommen
| Feature | Status | Datei |
|---------|--------|-------|
| {Feature} | {Status} | {Datei} |

## Abgeschlossen (letzte 5)
| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
| {Feature} | {Datum} | {Datei} |

---

## Offene Bugs
| Bug | Severity | Status | Analyse | Datei |
|-----|----------|--------|---------|-------|
| {Bug-Name} | {Severity} | {Status} | ✅/❌ | {Datei} |

## Offene Aufgaben
| Aufgabe | Prio | Status | Datei |
|---------|------|--------|-------|
| {Aufgaben-Name} | {Prio} | {Status} | {Datei} |

## Nicht im Backlog (Change-Ordner mit spec.md / bug.md / task.md ohne Eintrag)
| Datei | Titel | Status |
|-------|-------|--------|
| {Datei} | {Titel} | {Status} |

> Diese Features/Bugs haben eine Datei, sind aber nicht in BACKLOG.md eingetragen.
> Trage sie manuell ein oder nutze `/dtb:feature-plan` bzw. `/dtb:bug-report`.

---

## Empfehlung
{Was sollte als naechstes angegangen werden und warum?}
```

## Richtlinien

- **Read-Only**: Dieser Command aendert keine Dateien
- **Kompakt**: Uebersicht, nicht Detail — Details stehen in den `spec.md` Dateien
- **Priorisiert**: Wichtigstes zuerst
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Klare Empfehlung am Ende

## Verwendung

Nutze diesen Command:
- Am Session-Start fuer Orientierung
- Bei Planungsentscheidungen
- Fuer Stakeholder-Updates
- Wenn unklar ist was als naechstes kommt

## Verwandte Commands

- `/dtb:workflow-resume` - Session-Start mit vollem Kontext
- `/dtb:feature-plan` - Neues Feature planen (mit Backlog-Eintrag)
- `/dtb:workflow-checkpoint` - Session dokumentieren (mit Feature-Status-Update)
- `/dtb:workflow-status` - Pipeline-Visualisierung (alle Workflow-Stufen)

---

Scanne jetzt die Workflow-Dateien und erstelle den Backlog-Status.
