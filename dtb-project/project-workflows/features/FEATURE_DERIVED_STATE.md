# Feature: DERIVED_STATE

**Erstellt:** 2026-07-06
**Ziel:** Feature-Status wird aus Artefakten abgeleitet statt in mehreren Dateien manuell gepflegt — Status-Drift wird strukturell unmoeglich.
**Prioritaet:** Hoch
**Status:** Geplant

---

## Executive Summary

Der Status eines Features steht heute redundant in BACKLOG.md, WORKFLOW_STATUS.md und IMPL_STATUS_*.md — jede Stelle muss manuell gepflegt werden, was nachweislich zu Drift fuehrt (2026-07-03: erledigter Fix stand noch als offen). Kuenftig ist eine `## Progress`-Checkliste in `PLAN_*.md` die Single Source of Truth; alle Lese-Skills leiten den Status aus Artefakt-Existenz und Checkboxen ab. IMPL_STATUS_*.md entfaellt, WORKFLOW_STATUS.md wird zum generierten Dashboard. (Vorbild: 10x-devs-3.0 Change-Chain, ohne deren Skill-Umfang.)

---

## Scope / Abgrenzung

### Enthalten
- `## Progress`-Sektion mit Checkboxen als Pflichtteil des PLAN-Templates in `dtb:impl-plan`; beim Abhaken optional Commit-SHA als Beleg (`- [x] Schritt 3 — \`071cc12\``)
- `IMPL_STATUS_*.md` komplett abloesen (aus `impl-plan` und `feature-start` entfernen; Kontextverlust-Handoff laeuft ueber PLAN-Progress)
- Zentrale Ableitungsregel als **eigene Referenzdatei** `project-rules/DERIVED_STATE_RULES.md` (existierende Kategorie, von project-init verteilt; entschieden im Plan-Review 2026-07-06), von allen Lese-Skills explizit referenziert
- Lese-Skills `workflow-next`, `workflow-status`, `workflow-resume`, `backlog-status` leiten Status aus Artefakten ab statt BACKLOG-Feldern zu vertrauen
- `WORKFLOW_STATUS.md` abspecken: Status-Teil wird von `workflow-checkpoint` generiert; Session-Log (Prosa, Entscheidungen) bleibt manuell
- BACKLOG.md behaelt die Status-Spalte als **abgeleitete Anzeige** (von Skills befuellt, nicht manuell gepflegt); Prio- und Ideen-Verwaltung bleiben manuell
- Lifecycle-Skills anpassen: `archive` (Abschluss-Kriterium), `feature-plan`/`task`/`bug-report` (BACKLOG-Eintraege), `project-init` (Vorlagen), `project-health` (Drift-Checks → Derived-State-Checks), `plan-review` (Progress-Sektion)
- Doku + Pipeline-Frontmatter (`consumes`/`produces`) kit-weit konsistent nachziehen

### Nicht enthalten
- Change-Folder-Modell (Idee #7 — baut auf diesem Feature auf, kommt erst nach Bewaehrung)
- Migrations-Tooling fuer bestehende Zielprojekte (manuelle Anpassung reicht)
- Git-Hooks oder Hintergrund-Automatisierung — Ableitung passiert ausschliesslich beim Skill-Aufruf
- Aenderungen an `dtb:code-review` (verifiziert nicht betroffen)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Checkbox-Hygiene: Abhaken nach Implementierung wird vergessen → abgeleiteter Status luegt genauso | Mittel | Hoch | Abhaken als expliziten Schritt im Implementierungs-Loop von `feature-start` verankern; Commit-SHA-Konvention macht Luecken sichtbar; `project-health` prueft Commits-ohne-Checkbox |
| Logik-Drift: 4 Lese-Skills implementieren die Ableitung unterschiedlich | Mittel | Mittel | Eine zentrale Referenzdatei, alle Skills referenzieren sie; keine Duplikation |
| Rueckwaertskompatibilitaet: Alt-Artefakte (IMPL_STATUS, PLAN ohne Progress) brechen Skills | Niedrig | Mittel | Definierte Fallbacks: "Fortschritt unbekannt" + Nachruest-Angebot, kein Abbruch |
| Umbau-Umfang: 15 Dateien anfassen, Inkonsistenz waehrend der Umstellung | Mittel | Mittel | Implementierung in Phasen (Regel-Datei → Schreibseite → Leseseite → Lifecycle → Doku); Kit ist Vorlagensammlung, kein Laufzeit-Risiko |
| 500-Zeilen-Limit: Progress-Sektion blaeht PLAN_*.md auf | Niedrig | Niedrig | Kompakte Checkliste (1 Zeile/Schritt), keine Prosa in Progress |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — `features/` war leer, keine konkurrierenden Features

### Referenz-Dokumente
- `features/DISCOVERY_DERIVED_STATE.md` - Discovery mit allen 15 betroffenen Modulen, Randfaellen und Constraints
- `dtb-project/project-workflows/INBOX.md` - Idee #1 (Ursprung), Querbezuege #4/#6/#7
- `dtb-project/project-changelog/2026-07/2026-07-03.md` - 10x-devs-3.0-Analyse, belegter Drift-Fall
- `~/.claude/projects/.../memory/10x-devs-kurs-referenz.md` - Vorbild-Referenz (10x Change-Chain)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `dtb:impl-plan` erzeugt PLAN_*.md mit `## Progress`-Sektion; IMPL_STATUS_*.md wird nirgendwo mehr erzeugt oder referenziert (kit-weit 0 Treffer ausser Archiv/Changelog)
- [ ] Zentrale Ableitungsregel existiert als eine Datei; alle 4 Lese-Skills referenzieren sie
- [ ] `workflow-next`/`-resume` liefern korrekten Stand allein aus Artefakten — auch wenn nie ein Checkpoint lief (Test: Checkpoint weglassen, Resume zeigt trotzdem richtigen naechsten Schritt)
- [ ] Widerspruch zwischen BACKLOG-Feld und Artefakt-Zustand wird im Report gemeldet, Artefakt gewinnt
- [ ] Alt-Artefakte (PLAN ohne Progress, vorhandene IMPL_STATUS) fuehren zu definiertem Fallback statt Fehlverhalten
- [ ] WORKFLOW_STATUS.md enthaelt keine handgepflegten Statusaussagen mehr; Pipeline-Frontmatter (`consumes`/`produces`) kit-weit konsistent
- [ ] `pipeline-graph` zeigt die neuen Kanten ohne manuelle Nacharbeit

---

**Erstellt mit:** `/dtb:feature-plan`
