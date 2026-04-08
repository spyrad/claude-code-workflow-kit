---
name: dtb:project-health
description: >-
  Use when: "Health Check", "Projekt pruefen", "Konsistenz check",
  "Projekt-Linting". Project linting: checks consistency, cross-references,
  freshness, and naming conventions of all project artifacts.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [workflow.config.yaml, BACKLOG.md, DISCOVERY_*.md, FEATURE_*.md, PLAN_*.md, BUG_*.md, TASK_*.md, INBOX.md, WORKFLOW_STATUS.md, CLAUDE.md, project-rules/*.md]
  produces: []
---

# DTB Projekt-Health

Projekt-Linting: Pruefe Konsistenz, Querverweise, Frische und Namenskonventionen aller Projekt-Artefakte.

## Aufgabe

### Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden. Bitte zuerst /dtb:project-init ausfuehren.
```
→ Abbruch.

### Schritt 1: Alle Checks ausfuehren

Fuehre die folgenden 10 Check-Kategorien aus. Sammle Ergebnisse mit Status-Emojis: `✅` (OK), `⚠️` (Warnung), `❌` (Fehler).

---

#### Check 1: Config-Integritaet

- `workflow.config.yaml` existiert und ist valides YAML
- Alle Verzeichnisse aus `config.paths.*` existieren
- Alle `config.repos[].path` existieren und sind Git-Repos (pruefe mit `git -C {path} rev-parse --git-dir`)

#### Check 2: Querverweise (Dead Links + Orphans)

**BACKLOG → Features:**
- Lies BACKLOG.md, extrahiere alle `Datei`-Spalten-Eintraege (Pattern: `` `features/FEATURE_*.md` ``)
- Pruefe ob jede referenzierte Datei unter `{config.paths.workflows}/features/` existiert
- Ignoriere Eintraege mit `-` (kein Feature-File)

**Features → BACKLOG (Orphan-Check):**
- Liste alle `FEATURE_*.md` in `{config.paths.workflows}/features/`
- Pruefe ob jede Datei in BACKLOG.md referenziert wird
- Nicht referenzierte = Orphan → FEHLER

**Bugs → BACKLOG (Orphan-Check):**
- Liste alle `BUG_*.md` in `{config.paths.workflows}/features/`
- Pruefe ob jede Datei in BACKLOG.md referenziert wird
- Nicht referenzierte = INFO (Bugs muessen nicht zwingend im Backlog stehen, aber Warnung bei Severity "Kritisch" oder "Hoch")

**Tasks → BACKLOG (Orphan-Check):**
- Liste alle `TASK_*.md` in `{config.paths.workflows}/features/`
- Pruefe ob jede Datei in BACKLOG.md (Abschnitt "Aufgaben") referenziert wird
- Nicht referenzierte = INFO (Tasks muessen nicht zwingend im Backlog stehen, aber Warnung bei Prioritaet "Hoch")

**Bug-Status-Konsistenz:**
- Pruefe ob jede `BUG_*.md` einen gueltigen Status hat (Offen, Analysiert, In Arbeit, Behoben)
- Bugs mit Status "Analysiert" sollten einen Analyse-Abschnitt enthalten → WARNUNG wenn fehlend
- Bugs mit Status "Offen" aelter als 14 Tage → WARNUNG

**PLAN ↔ FEATURE Pairing:**
- Liste alle `PLAN_*.md` in `{config.paths.workflows}/features/`
- Pruefe ob zu jeder `PLAN_*.md` eine passende `FEATURE_*.md` existiert (gleicher Name)
- PLAN ohne FEATURE = FEHLER (verwaister Implementierungsplan)
- FEATURE ohne PLAN = INFO (kein Fehler — Plan kann spaeter mit `/dtb:impl-plan` erstellt werden)

**INBOX → Features:**
- Lies INBOX.md, filtere Eintraege mit Status `Ausgearbeitet`
- Pruefe ob der verlinkte `FEATURE_*.md` Eintrag existiert
- Eintraege mit Status `Offen` oder `Verworfen` brauchen keinen Link

**INBOX Integritaet:**
- Pruefe ob alle Eintraege einen gueltigen Status haben (Offen, In Arbeit, Ausgearbeitet, Verworfen)
- Luecken in den Nummern sind erlaubt (entstehen durch Archivierung)

**Archiv-Integritaet:**
- Falls `{config.paths.workflows}/archive/` existiert:
  - Pruefe ob ARCHIVE_LOG.md vorhanden ist
  - Pruefe ob jede `FEATURE_*.md` im Archiv einen Eintrag im ARCHIVE_LOG hat
  - Warnung bei verwaisten Feature-Specs im Archiv (ohne Log-Eintrag)

**Archiv-Empfehlung:**
- Zaehle verworfene/ausgearbeitete Eintraege in INBOX.md, abgeschlossene Features in BACKLOG.md und behobene Bugs
- Warnung wenn mehr als 5 archivierbare Eintraege vorhanden → Empfehlung: `/dtb:archive`

**WORKFLOW_STATUS → Logs:**
- Extrahiere alle Session-Log-Links aus WORKFLOW_STATUS.md (Pattern: `` `project-changelog/...` ``)
- Pruefe ob jeder referenzierte Log existiert

**WORKFLOW_STATUS → Plans:**
- Extrahiere alle Plan-Links (Pattern: `` `.claude/plans/*.md` ``)
- Pruefe ob jeder referenzierte Plan existiert

#### Check 3: Status-Konsistenz

- Lies den Status jedes Features aus BACKLOG.md (Spalte "Status")
- Lies den `**Status:**`-Wert aus der jeweiligen FEATURE_*.md
- Vergleiche: Wenn BACKLOG "In Arbeit" sagt aber Feature-Spec "Geplant" (oder umgekehrt) → FEHLER
- Pruefe: WORKFLOW_STATUS "Laufende Arbeit" → das referenzierte Feature/Task sollte in BACKLOG "In Arbeit" sein
- Erlaubte Abweichungen: "Geplant" in BACKLOG + beliebiger Status in Spec ist OK solange Spec nicht "In Arbeit"/"Fertig" sagt

**TASK Status-Konsistenz:**
- Lies den Status jeder Aufgabe aus BACKLOG.md (Abschnitt "Aufgaben")
- Lies den `**Status:**`-Wert aus der jeweiligen TASK_*.md
- Vergleiche: Status muss uebereinstimmen (Offen, In Arbeit, Erledigt) → FEHLER bei Abweichung

**INBOX ↔ Feature-Status:**
- Idee "In Arbeit" → es sollte noch kein FEATURE_*.md existieren (sonst muesste Status "Ausgearbeitet" sein). Ein DISCOVERY_*.md-Link ist erlaubt (Discovery-Phase laeuft)
- Idee "Ausgearbeitet" → das verlinkte FEATURE_*.md muss existieren

#### Check 4: Namenskonventionen

**dtb-project/ Root-Dateien:**
- Alle `.md`-Dateien direkt in `dtb-project/project-workflows/`, `dtb-project/project-strategy/`, `dtb-project/project-infrastructure/` und `dtb-project/project-requirements/` muessen UPPER_SNAKE_CASE sein (z.B. BACKLOG.md, GPU_SERVERS.md, TEAM.md)
- `.md`-Dateien in `integrations/*/` (ausser `input/`) muessen ebenfalls UPPER_SNAKE_CASE sein
- Warnung bei Abweichung

**Feature-Dateien:**
- Alle `.md`-Dateien in `{config.paths.workflows}/features/` muessen dem Pattern `DISCOVERY_*.md`, `FEATURE_*.md`, `PLAN_*.md`, `BUG_*.md` oder `TASK_*.md` folgen
- FEHLER bei Abweichung

**Skills:**
- Alle Skill-Verzeichnisse in `.claude/skills/` muessen kebab-case sein (kleinbuchstaben, bindestriche)
- Jedes Skill-Verzeichnis muss eine `SKILL.md` enthalten
- Warnung bei Abweichung

#### Check 5: Frische / Aktualitaet

- Lies WORKFLOW_STATUS.md → `**Letztes Update:**` Datum → Warnung wenn aelter als 7 Tage
- Lies BACKLOG.md → `**Letzte Aktualisierung:**` Datum → Warnung wenn aelter als 14 Tage
- Finde den neuesten Session-Log in `{config.paths.changelog}/` → Warnung wenn aelter als 7 Tage

#### Check 6: CLAUDE.md Compliance

**Root CLAUDE.md:**
- Zaehle Zeilen → Warnung ab >160 Zeilen

**Entry Points:**
- `{repos[backend].path}/src/main.py` existiert
- `{repos[frontend].path}/src/main.tsx` existiert

**Quick Reference — Critical Files:**
- Lies die "Critical Backend Files" und "Critical Frontend Files" Sektionen
- Pruefe ob jeder gelistete Pfad (relativ zum jeweiligen Repo) existiert
- Warnung bei nicht gefundenen Pfaden

#### Check 7: Git-Status

Fuer jedes Repo in `config.repos`:
```bash
git -C {repo.path} branch --show-current
git -C {repo.path} status --porcelain
git -C {repo.path} log -1 --format="%cr"
```
- Zeige: Branch, Uncommitted Changes (Warnung wenn vorhanden), letzter Commit-Zeitpunkt

#### Check 8: Skill-Frontmatter-Konsistenz

Scanne alle `.claude/skills/dtb-*/SKILL.md` im Projekt:

**Pflichtfelder pruefen:**
- `name` vorhanden → FEHLER wenn fehlend
- `description` vorhanden → FEHLER wenn fehlend
- `disable-model-invocation` vorhanden → WARNUNG wenn fehlend
- `allowed-tools` vorhanden → WARNUNG wenn fehlend
- `pipeline` Block vorhanden → WARNUNG wenn fehlend

**Pipeline-Konsistenz pruefen:**
- `pipeline.after` referenziert einen existierenden Skill (Verzeichnis `.claude/skills/dtb-*/SKILL.md` muss existieren) → FEHLER wenn nicht
- `pipeline.next` referenziert einen existierenden Skill → FEHLER wenn nicht
- `pipeline.consumes` Artefakte: Pruefe ob mindestens ein anderer Skill diese in `produces` listet → WARNUNG wenn verwaist
- Zirkulaere Referenzen (A→B→A via `next`) → FEHLER

**allowed-tools vs. Body pruefen:**
- Skill-Body referenziert `Write` oder `Bash` Aktionen aber `allowed-tools` enthaelt es nicht → WARNUNG

#### Check 9: Memory-Health

- `MEMORY.md` existiert unter dem Memory-Pfad (`~/.claude/projects/.../memory/MEMORY.md`)
- Suche alle `.md`-Dateien im Memory-Verzeichnis (ausser MEMORY.md)
- Pruefe ob jede Memory-Datei in MEMORY.md referenziert ist (und umgekehrt)
- Pruefe ob Memory-Dateien gueltiges Frontmatter haben (name, type, description)

#### Check 10: Rules-Konsistenz

- `{config.paths.rules}/` Verzeichnis existiert → INFO wenn fehlend (kein Fehler — Rules sind optional)
- Falls vorhanden: Zaehle Rules-Dateien
- Pruefe ob Rules-Dateien das erwartete Format haben (Titel `# Coding Rules:`, Sektionen wie `## Do's`, `## Don'ts`)
- Pruefe ob `**Manuell angepasst:**` Feld vorhanden → INFO wenn noch "Nein" (Hinweis: Review empfohlen)

---

### Schritt 2: Report generieren

Erstelle einen kompakten Report (max 80 Zeilen) im folgenden Format. Zeige Details nur bei FEHLER und WARNUNG — bei OK nur die Zusammenfassung.

```markdown
# Projekt-Health: {project_name}

**Datum:** YYYY-MM-DD
**Checks:** ✅ X bestanden, ⚠️ Y Warnungen, ❌ Z Fehler

---

## Config-Integritaet
- ✅/❌ workflow.config.yaml — {Status}
- ✅/❌ Pfade: {Anzahl}/{Anzahl} existieren
- ✅/❌ Repos: {Details pro Repo}

## Querverweise
- ✅/❌ BACKLOG → Features: {X}/{Y} Referenzen gueltig
- ✅/❌ Features → BACKLOG: {Orphan-Details falls vorhanden}
- ✅/ℹ️ Bugs → BACKLOG: {N} Bugs, davon {M} ohne Backlog-Eintrag
- ✅/⚠️ Bug-Status: {N}/{M} konsistent
- ✅/ℹ️ Tasks → BACKLOG: {N} Aufgaben, davon {M} ohne Backlog-Eintrag
- ✅/⚠️ Task-Status: {N}/{M} konsistent
- ✅/❌ INBOX → Features: {X}/{Y} ausgearbeitete Ideen mit gueltigem Link
- ✅/❌ Archiv: {Status}
- ✅/⚠️ Archivierbare Eintraege: {N} (Empfehlung: /dtb:archive bei >5)
- ✅/❌ WORKFLOW_STATUS → Logs: {Status}
- ✅/❌ WORKFLOW_STATUS → Plans: {Status}

## Status-Konsistenz
- ✅/❌ Feature-Status: BACKLOG ↔ Specs {konsistent/inkonsistent}
- ✅/❌ Laufende Arbeit: {Status}

## Namenskonventionen
- ✅/⚠️ dtb-project/: {Status}
- ✅/⚠️ features/: {Status}
- ✅/⚠️ skills/: {Status}

## Frische
- ✅/⚠️ WORKFLOW_STATUS: Aktualisiert vor {N} Tagen
- ✅/⚠️ BACKLOG: Aktualisiert vor {N} Tagen
- ✅/⚠️ Letzter Session-Log: {Datum}

## CLAUDE.md
- ✅/⚠️ Root: {N} Zeilen (Limit: 160)
- ✅/❌ Entry Points: {Status}
- ✅/⚠️ Quick Reference: {Status}

## Git
- ✅/⚠️ {Repo}: `{Branch}` — letzter Commit vor {N}, {Changes}

## Skill-Frontmatter
- ✅/⚠️ Pflichtfelder: {N}/{M} Skills vollstaendig
- ✅/⚠️ Pipeline: {N}/{M} Skills mit Pipeline-Block
- ✅/❌ Pipeline-Referenzen: {Status}
- ✅/⚠️ allowed-tools: {N}/{M} konsistent

## Memory
- ✅/❌ MEMORY.md: {N} Eintraege, {Status}

## Rules
- ✅/ℹ️ Rules-Verzeichnis: {vorhanden/nicht vorhanden}
- ✅/ℹ️ Rules-Dateien: {N} vorhanden
- ✅/ℹ️ Manuell reviewed: {N}/{M}
```

### Schritt 3: Empfohlene Aktionen

Am Ende des Reports: Konkrete Handlungsempfehlungen fuer jeden FEHLER und jede WARNUNG, priorisiert (FEHLER zuerst).

```markdown
---

## Zusammenfassung

✅ X bestanden | ⚠️ Y Warnungen | ❌ Z Fehler

Empfohlene Aktionen:
1. ❌ {Beschreibung} — {Empfehlung}
2. ⚠️ {Beschreibung} — {Empfehlung}
```

Falls keine Fehler/Warnungen: "✅ Alle Checks bestanden — keine Aktionen noetig."

---

## Richtlinien

- **Readonly:** Keine Dateien aendern, nur lesen und pruefen
- **Schnell:** Kein Build, kein Test — nur Dateisystem + Git
- **Kompakt:** Max 80 Zeilen Output (Details nur bei Fehlern/Warnungen)
- **Deutsch:** Alle Texte auf Deutsch
- **Idempotent:** Kann jederzeit ohne Seiteneffekte ausgefuehrt werden
- **Kein Overkill:** Bei OK-Checks eine Zeile, nicht auswalzen

## Verwandte Skills

- `/dtb:build-check` — Tests und Builds ausfuehren
- `/dtb:backlog-status` — Backlog-Details
- `/dtb:archive` — Abgeschlossene/verworfene Eintraege archivieren
- `/dtb:workflow-resume` — Session fortsetzen
- `/dtb:project-init` — Erstinitialisierung
- `/dtb:workflow-status` — Pipeline-Status und Queue-Analyse

---

Fuehre jetzt den Health-Check durch und erstelle den Report.
