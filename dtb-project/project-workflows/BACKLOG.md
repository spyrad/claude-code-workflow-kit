# Feature Backlog

**Letzte Aktualisierung:** 2026-07-13 (S8: Greenfield-Autoren-Skills umgesetzt + verifiziert → Fertig zum Testen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| Codebase-Research-Step | Fertig zum Testen | Hoch | features/codebase-research-step/spec.md | impl-plan stellt vor der Schrittplanung eine verifizierte Ist-Analyse der betroffenen Module sicher — Pläne fußen auf realem Code statt Annahmen |
| Greenfield-Autoren-Skills | Fertig zum Testen | Hoch | features/greenfield-autoren-skills/spec.md | greenfield-prd/-roadmap werden Autoren-Skills (PRD-Interview → PRD-MVP.md, Lean-Roadmap → ROADMAP.md + TECH-STACK.md) nach 10x-Vorbild, Derived-State-konform |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|
| [Feature 1] | Idee | [Prio] | - | [Kurzbeschreibung] |

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
| Derived State | 2026-07-08 | `archive/derived-state/` |
| Kit Sync | 2026-07-08 | `archive/kit-sync/` |
| Lesson Loop | 2026-07-08 | `archive/lesson-loop/` |
| Betriebs-Wächter (plan-review) | 2026-07-08 | kein FEATURE-Artefakt — Commit `4ee4a9a` (bedingter 4. Review-Agent + Rollen-Schärfung) |
| Review-Härtung | 2026-07-13 | `archive/review-haertung/` |
| Spec-Härtung | 2026-07-13 | `archive/spec-haertung/` |
| Eligibility-Gates | 2026-07-13 | `archive/eligibility-gates/` |
| Frontmatter- und Pfad-Hygiene | 2026-07-13 | `archive/frontmatter-pfad-hygiene/` |
| Bug: project-init-stale-rules-seed | 2026-07-13 | `archive/project-init-stale-rules-seed/` |
| Skill-10x-Optimierungen | 2026-07-13 | `archive/skill-10x-optimierungen/` |
| Change-Folder-Modell | 2026-07-13 | `archive/change-folder-modell/` |

---

## Status-Legende (abgeleitet aus Artefakten)

| Status | Abgeleitet aus |
|--------|----------------|
| Idee | Nur INBOX-/BACKLOG-Eintrag, keine Artefakte |
| In Discovery | discovery.md existiert, kein spec.md |
| Spezifiziert | spec.md existiert, kein plan.md |
| Geplant | plan.md existiert, 0 Progress-Checkboxen |
| In Arbeit | `## Progress` teilweise abgehakt (X/Y) |
| Fertig zum Testen | Alle Schritte abgehakt |
| Abgenommen | Explizit gesetzt (getestet und freigegeben) |
| Abgeschlossen | Explizit via `/dtb:archive` |
| Pausiert | Explizit gesetzt, ueberschreibt Ableitung |

## Prio-Legende

| Prio | Bedeutung |
|------|-----------|
| Kritisch | Blocker, sofort umsetzen |
| Hoch | Naechster Sprint |
| Mittel | Backlog, bei Kapazitaet |
| Niedrig | Nice-to-have |
