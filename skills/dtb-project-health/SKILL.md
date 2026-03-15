---
name: dtb:project-health
description: >-
  Use when: "Health Check", "Projekt pruefen", "Konsistenz check",
  "Projekt-Linting". Project linting: checks consistency, cross-references,
  freshness, and naming conventions of all project artifacts.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
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

Fuehre die folgenden 8 Check-Kategorien aus. Sammle Ergebnisse mit Status-Emojis: `✅` (OK), `⚠️` (Warnung), `❌` (Fehler).

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
- Pruefe: WORKFLOW_STATUS "Laufende Arbeit" → das referenzierte Feature sollte in BACKLOG "In Arbeit" sein
- Erlaubte Abweichungen: "Geplant" in BACKLOG + beliebiger Status in Spec ist OK solange Spec nicht "In Arbeit"/"Fertig" sagt

#### Check 4: Namenskonventionen

**dtb-project/ Root-Dateien:**
- Alle `.md`-Dateien direkt in `dtb-project/project-workflows/` und `dtb-project/project-strategy/` muessen UPPER_SNAKE_CASE sein (z.B. BACKLOG.md, WORKFLOW_STATUS.md, TEAM.md)
- Warnung bei Abweichung

**Feature-Dateien:**
- Alle `.md`-Dateien in `{config.paths.workflows}/features/` muessen dem Pattern `FEATURE_*.md` folgen
- FEHLER bei Abweichung

**Commands:**
- Alle `.md`-Dateien in `~/.claude/commands/dtb/` muessen kebab-case sein (kleinbuchstaben, bindestriche)
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

#### Check 8: Memory-Health

- `MEMORY.md` existiert unter dem Memory-Pfad (`~/.claude/projects/.../memory/MEMORY.md`)
- Suche alle `.md`-Dateien im Memory-Verzeichnis (ausser MEMORY.md)
- Pruefe ob jede Memory-Datei in MEMORY.md referenziert ist (und umgekehrt)
- Pruefe ob Memory-Dateien gueltiges Frontmatter haben (name, type, description)

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
- ✅/❌ WORKFLOW_STATUS → Logs: {Status}
- ✅/❌ WORKFLOW_STATUS → Plans: {Status}

## Status-Konsistenz
- ✅/❌ Feature-Status: BACKLOG ↔ Specs {konsistent/inkonsistent}
- ✅/❌ Laufende Arbeit: {Status}

## Namenskonventionen
- ✅/⚠️ dtb-project/: {Status}
- ✅/⚠️ features/: {Status}
- ✅/⚠️ commands/: {Status}

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

## Memory
- ✅/❌ MEMORY.md: {N} Eintraege, {Status}
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

## Verwandte Commands

- `/dtb:build-check` — Tests und Builds ausfuehren
- `/dtb:backlog-status` — Backlog-Details
- `/dtb:workflow-resume` — Session fortsetzen
- `/dtb:project-init` — Erstinitialisierung

---

Fuehre jetzt den Health-Check durch und erstelle den Report.
