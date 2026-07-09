# Discovery: DERIVED_STATE

**Erstellt:** 2026-07-06
**Idee-Referenz:** Inbox #1 — "Derived State statt Statusfelder: `## Progress`-Checkboxen in PLAN_*.md als Single Source of Truth (mit Commit-SHA-Rueckschreibung), IMPL_STATUS_*.md abloesen, WORKFLOW_STATUS.md auf generiertes Dashboard abspecken; workflow-next/-status/-resume leiten Status aus Artefakten ab statt BACKLOG-Feldern zu vertrauen"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-impl-plan/SKILL.md` | Kern (Schreibseite): `## Progress`-Sektion wird Pflichtteil des PLAN-Templates; IMPL_STATUS_*.md entfaellt |
| `skills/dtb-feature-start/SKILL.md` | Schreibseite: IMPL_STATUS-Erzeugung entfernen; Checkbox-Abhaken (mit Commit-SHA) beim Implementieren verankern |
| `skills/dtb-workflow-next/SKILL.md` | Leseseite: naechster Schritt aus Artefakt-Existenz + Progress-Checkboxen abgeleitet |
| `skills/dtb-workflow-status/SKILL.md` | Leseseite: Pipeline-/Queue-Ansicht aus Artefakten statt Statusfeldern |
| `skills/dtb-workflow-resume/SKILL.md` | Leseseite: aktive Features abgeleitet statt aus BACKLOG-Feld "In Arbeit" |
| `skills/dtb-backlog-status/SKILL.md` | Leseseite: Read-only-Uebersicht auf Ableitungslogik umstellen |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Dashboard: Status-Teil von WORKFLOW_STATUS.md wird generiert statt formuliert; Session-Log (Prosa) bleibt |
| `skills/dtb-archive/SKILL.md` | Lifecycle: Abschluss-Kriterium anpassen (alle Checkboxen ≠ automatisch "Abgeschlossen") |
| `skills/dtb-feature-plan/SKILL.md` | Lifecycle: BACKLOG-Eintrag ohne gepflegtes Statusfeld |
| `skills/dtb-task/SKILL.md`, `skills/dtb-bug-report/SKILL.md` | Lifecycle: BACKLOG-Eintraege; eigene einfachere Ableitungsregel (Checkliste in der Datei) |
| `skills/dtb-project-init/SKILL.md` | Erzeugt BACKLOG-/WORKFLOW_STATUS-Vorlagen im Zielprojekt — Vorlagen anpassen |
| `skills/dtb-project-health/SKILL.md` | QS: Drift-Checks auf Derived State umstellen; verwaiste FEATURE/PLAN-Paare erkennen |
| `skills/dtb-plan-review/SKILL.md` | QS: neue Progress-Sektion tolerieren/pruefen |
| `dtb-project/project-workflows/BACKLOG.md` (Vorlage) | Statusfeld-Spalten + Status-Legende aendern sich |
| `CLAUDE.md`, `README.md`, `skills/CLAUDE.md`, `skills/dtb-pipeline-graph/SKILL.md` | Doku + Pipeline-Frontmatter (`consumes`/`produces`: IMPL_STATUS_*.md ueberall raus) |

Nicht betroffen (verifiziert): `skills/dtb-code-review/SKILL.md` — konsumiert nur `project-rules/*.md`, `CLAUDE.md`, `workflow.config.yaml`.

---

## Anforderungen

### Scope

**Enthalten:**
- `## Progress`-Sektion mit Checkboxen wird Pflichtteil von `PLAN_*.md` (Template in `dtb:impl-plan`), optional mit Commit-SHA-Rueckschreibung beim Abhaken
- `IMPL_STATUS_*.md` wird komplett abgeloest (aus `impl-plan` und `feature-start` entfernt)
- `workflow-next`, `workflow-status`, `workflow-resume`, `backlog-status` leiten Status aus Artefakt-Existenz + Progress-Checkboxen ab
- `WORKFLOW_STATUS.md` wird abgespeckt: generiertes Dashboard, keine handgepflegten Statusaussagen mehr
- BACKLOG.md-Rolle klaeren: Statusfeld entfaellt oder wird zu abgeleiteter Anzeige (Detailentscheidung → Feature-Spec)

**Nicht enthalten:**
- Kein Change-Folder-Modell (Idee #7, explizit spaeter, baut auf diesem Feature auf)
- Kein Migrations-Tooling fuer bestehende Zielprojekte (manuelle Anpassung reicht)
- Keine Git-Hooks/Automatisierung — Ableitung passiert beim Skill-Aufruf, nicht im Hintergrund

### Gewuenschtes Verhalten
- **Abhaken statt berichten:** Nach einem Implementierungsschritt wird die Checkbox im `PLAN_*.md` abgehakt (mit Commit-SHA) — das ist die einzige Statuspflege
- **Fragen liefern immer die Wahrheit:** `workflow-next` & Co. antworten aus dem Ist-Zustand der Artefakte, auch ohne vorherigen Checkpoint
- **Checkpoint wird leichter:** Session-Log (Prosa, Entscheidungen, Kontext) bleibt; Status-Teil von WORKFLOW_STATUS.md wird generiert
- **Drift wird sichtbar statt stumm:** Bei Widerspruch manuelles Feld ↔ abgeleiteter Zustand gewinnt das Artefakt, der Widerspruch wird gemeldet
- **UX-Muster:** Checkbox-Konvention `- [ ]`/`- [x]` wie im Kit ueblich; Commit-SHA als Inline-Code (`` `071cc12` ``); Report-Formate bleiben aeusserlich gleich (kompakt, max 60 Zeilen); Vorbild 10x-devs-3.0 Change-Chain ohne deren Skill-Umfang

### Randfaelle
- **Plan ohne `## Progress`-Sektion (Altbestand):** als "Plan vorhanden, Fortschritt unbekannt" behandeln, Nachruestung anbieten — kein Abbruch
- **Checkbox ohne Commit-SHA:** gueltig (SHA ist Beleg, keine Pflicht — z.B. Doku-Schritte)
- **Widerspruch Artefakt ↔ BACKLOG-Feld:** Artefakt gewinnt, Hinweis im Report
- **Progress-Sektion mit 0 Checkboxen:** wie "keine Sektion" behandeln
- **Alle Checkboxen abgehakt:** Status "Fertig zum Testen" — nicht automatisch "Abgeschlossen"; Abnahme/Archivierung bleibt explizite Nutzer-Entscheidung (`/dtb:archive`)
- **Spec ohne Plan / Plan ohne Spec:** abgeleiteter Status "Discovery/Spec-Phase" bzw. Meldung "verwaister Plan"
- **Keinerlei Artefakte:** wie heute ("Kein aktives Feature")
- **Mehrere Features parallel:** Ableitung pro Feature-Paar (Namens-Pairing), Reports listen alle
- **Umbenannte Dateien:** Namens-Pairing bricht → `project-health` erkennt verwaiste Paare
- **Manuell editierte Checkboxen:** ausdruecklich erlaubt (Artefakt = Wahrheit)
- **TASK_*/BUG_* ohne Plan:** eigene, einfachere Ableitungsregel (Checkliste direkt in der Datei)

### Einschraenkungen
- **Spec-Size-Limit bleibt:** PLAN_*.md max 500 Zeilen inkl. Progress-Sektion (kompakte Checkliste)
- **Nur Markdown + Konvention:** keine Skripte, kein Parser-Tooling, keine Sidecar-Dateien; Ableitung via Glob/Grep/Read beim Skill-Aufruf; Windows + Unix
- **Read-only-Skills bleiben read-only:** `workflow-next`, `-status`, `backlog-status`, `session-summary` leiten nur ab; schreibende Statuspflege nur in `impl-plan` (Sektion anlegen) und beim Implementieren (Checkbox + SHA)
- **Kit-Konventionen gelten weiter:** Deutsch, YYYY-MM-DD, UPPER_SNAKE_CASE, Pipeline-Frontmatter konsistent halten
- **Distributions-Charakter:** Aenderungen betreffen Skill-Vorlagen im Kit; Zielprojekte migrieren manuell
- **Rueckwaertskompatibel lesen:** alte Artefakte (mit IMPL_STATUS, ohne Progress) duerfen Skills nicht brechen
- **Idee #7 nicht vorwegnehmen:** flaches Dateilayout bleibt

### Integrationspunkte
- **Schreibseite:** `impl-plan`, `feature-start`
- **Leseseite:** `workflow-next`, `workflow-status`, `workflow-resume`, `backlog-status` — gemeinsame Ableitungsregel **einmal zentral definieren** (z.B. `skills/CLAUDE.md` oder geteilte Referenz), sonst ersetzt Daten-Drift nur Logik-Drift
- **Dashboard:** `workflow-checkpoint`
- **Lifecycle:** `archive`, `feature-plan`, `task`, `bug-report`, `project-init`
- **QS:** `project-health`, `plan-review`
- **Doku/Meta:** `CLAUDE.md`, `README.md`, `skills/CLAUDE.md`, Pipeline-Frontmatter → `pipeline-graph` zeigt neue Kanten automatisch
- **Externe Abhaengigkeiten:** keine (Markdown + Git; optional `git log`/`git show` read-only zur SHA-Verifikation)

---

## Abhaengigkeiten

- Bestehende Features: keine (`features/` war leer)
- INBOX-Querbezuege: #4 (Distribution) und #6 (Bestands-Optimierungen) beruehren teils dieselben Skills — Reihenfolge beachten, keine harte Abhaengigkeit; #7 (Change-Folder) baut explizit auf diesem Feature auf

---

## Offene Punkte

- BACKLOG.md-Zukunft im Detail: Statusfeld ganz entfernen oder als abgeleitete Anzeige behalten (fuer Ideen/Prio-Verwaltung)? → in Feature-Spec entscheiden
- Ort der zentralen Ableitungsregel: `skills/CLAUDE.md` vs. eigene geteilte Referenzdatei → in Feature-Spec entscheiden

---

**Erstellt mit:** `/dtb:feature-discover`
