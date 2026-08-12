---
name: dtb:archive
description: >-
  Use when: "aufraumen", "archivieren", "archive", "Inbox aufraumen",
  "alte Features entfernen", "Backlog aufraumen". Moves completed and
  discarded items from active workflow files into the archive directory.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [INBOX.md, BACKLOG.md, WORKFLOW_STATUS.md, features/*/discovery.md, features/*/spec.md, features/*/plan.md, features/*/bug.md, features/*/task.md]
  produces: [ARCHIVE_LOG.md, INBOX.md, BACKLOG.md, WORKFLOW_STATUS.md]
---

# Workflow archivieren

Du raeumst die aktiven Workflow-Dateien auf, indem du abgeschlossene und verworfene Eintraege ins Archiv verschiebst.

## Worktree-Guard (Schritt 0)

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions".

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" && pwd); C=$(cd "$C" && pwd)
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar. Zusatz nur bei gesetztem `parallel.default_branch`
  (nicht `null`) in `workflow.config.yaml`: aktueller Branch ungleich dem Wert → Abbruch
  mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:archive schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele Sessions").
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Archiv-Verzeichnis sicherstellen

Erstelle falls nicht vorhanden: `{config.paths.workflows}/archive/`

---

## Schritt 2: Archivierbare Eintraege sammeln

Pruefe die folgenden Quellen und sammle alle Kandidaten:

### INBOX.md
- Eintraege mit Status `Verworfen`
- Eintraege mit Status `Ausgearbeitet` (bereits als Feature-Plan vorhanden)

### BACKLOG.md
- Features im Abschnitt "Abgeschlossen"

### Change-Ordner (abgeleitet, Regeln: `project-rules/DERIVED_STATE_RULES.md`)
Ein Change ist der Ordner `features/<slug>/`. Kandidat, wenn:
- `spec.md` — bei reinen Tasks/Bugs `task.md`/`bug.md` (Regel-Datei §1.5) — mit explizitem `**Status:** Abgenommen` oder `Abgeschlossen`
- `plan.md` vollstaendig abgehakt ("Fertig zum Testen") — NUR als Kandidat vorschlagen,
  Archivierung braucht explizite Bestaetigung (Regel-Datei §1.2: 100% Checkboxen ≠ automatisch abgeschlossen)
- `bug.md` deren `## Fix-Schritte` vollstaendig abgehakt sind (= Behoben) — §1.5
- `task.md` deren `## Schritte` vollstaendig abgehakt sind (= Erledigt) — §1.5

### Altbestand
- Flache Alt-Dateien (`FEATURE_*.md` etc.) oder `IMPL_STATUS_*.md` direkt in `features/`
  (nicht migriert) → **nicht** hier archivieren, sondern zuerst `/dtb:migrate-change-folders` empfehlen

---

## Schritt 3: Uebersicht zeigen

```
Archiv-Kandidaten gefunden:

Inbox:
  - #{N} "{Idee-Text}" (Verworfen)
  - #{N} "{Idee-Text}" (Ausgearbeitet → features/{slug}/spec.md)

Backlog:
  - {Feature-Name} (Abgeschlossen, {Datum})

Change-Ordner:
  - features/{slug}/ (Feature, Abgeschlossen)
  - features/{slug}/ (Bug, Behoben)
  - features/{slug}/ (Aufgabe, Erledigt)

Alles archivieren? (Ja / Auswahl treffen / Abbrechen)
```

**Eligibility-Gate (Fit-Check):** Dies IST der Gate von `archive` (Konvention: `skills/CLAUDE.md` →
„Eligibility-Gates") — kritische Vorbedingung sind **archivierbare Kandidaten**, nicht ein Argument.
`archive` ist ein Scanner (`after: null`) → kein Redirect-Ziel, nur ehrliche Meldung. Falls keine
Kandidaten gefunden:
```
Nichts zu archivieren — alle Eintraege sind aktiv.
(Falls nur nicht-migrierter flacher Altbestand vorliegt: zuerst /dtb:migrate-change-folders.)
```

---

## Schritt 4: Archivieren

### 4a: Archiv-Log schreiben

Schreibe/ergaenze `{config.paths.workflows}/archive/ARCHIVE_LOG.md`:

```markdown
# Archiv-Log

| Datum | Typ | Name | Herkunft | Grund |
|-------|-----|------|----------|-------|
| YYYY-MM-DD | Idee | #{N} "{Text}" | INBOX.md | Verworfen |
| YYYY-MM-DD | Idee | #{N} "{Text}" | INBOX.md | Ausgearbeitet → features/{slug}/spec.md |
| YYYY-MM-DD | Feature | {slug} | BACKLOG.md | Abgeschlossen |
| YYYY-MM-DD | Bug | {slug} | features/{slug}/bug.md | Behoben |
| YYYY-MM-DD | Aufgabe | {slug} | features/{slug}/task.md | Erledigt |
```

### 4b: Change-Ordner verschieben

- Setze beim Archivieren `**Status:** Abgeschlossen` in der `spec.md` des Change-Ordners — die
  Archivierung IST der explizite Abschluss-Akt (Regel-Datei §1.2)
- Verschiebe den **ganzen Change-Ordner** `features/<slug>/` nach `archive/<slug>/` (mit allen
  enthaltenen `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md`):
  - **Git-Repo:** `git mv {config.paths.workflows}/features/<slug> {config.paths.workflows}/archive/<slug>`
  - **Kein Git-Repo:** Dateisystem-Move des Ordners
- Ein reiner Bug-/Task-Change (`bug.md`/`task.md` ohne `spec.md`) wird genauso als Ordner verschoben

### 4c: INBOX.md bereinigen

- Entferne archivierte Zeilen aus der Tabelle
- Nummern der verbleibenden Eintraege **nicht** neu vergeben (Luecken sind OK — die Nummern sind IDs)

### 4d: BACKLOG.md bereinigen

- Entferne archivierte Features aus dem Abschnitt "Abgeschlossen"
- Entferne archivierte Bugs aus dem Abschnitt "Bugs" (Status `Behoben`)
- Entferne archivierte Aufgaben aus dem Abschnitt "Aufgaben" (Status `Erledigt`)
- Abschnitt "Aktive Features" bleibt unberuehrt

### 4e: WORKFLOW_STATUS.md bereinigen

- Lies `{config.paths.workflows}/WORKFLOW_STATUS.md`
- Entferne Referenzen auf soeben archivierte Features, Bugs und Tasks
- Falls ein archiviertes Item dort als "aktiv" oder "in Arbeit" gefuehrt wird: **nicht entfernen**, sondern Warnung ausgeben

---

## Schritt 5: Bestaetigung

```
Archivierung abgeschlossen:

  Ideen archiviert:    {N}
  Features archiviert: {N}
  Aufgaben archiviert: {N}

Archiv-Log: {config.paths.workflows}/archive/ARCHIVE_LOG.md
Change-Ordner: {config.paths.workflows}/archive/<slug>/ (ganzer Ordner verschoben)

Verbleibend in INBOX.md: {N} offene Ideen
Verbleibend in BACKLOG.md: {N} aktive Features
```

---

## Richtlinien

- **Keine aktiven Eintraege archivieren:** Nur Status "Verworfen", "Ausgearbeitet" (Inbox) sowie "Abgenommen" und "Abgeschlossen" (Backlog/Features — konsistent zur Kandidat-Regel oben; `Abgenommen` ist der Eingang der Archivierung, `Abgeschlossen` wird beim Verschieben gesetzt)
- **Immer bestaetigen:** Nichts archivieren ohne explizites OK vom Benutzer
- **Nummern beibehalten:** Inbox-Nummern sind IDs und werden nie wiederverwendet
- **Archiv-Log ist append-only:** Neue Eintraege anhaengen, nie ueberschreiben
- **Deutsch:** Alle Texte auf Deutsch
