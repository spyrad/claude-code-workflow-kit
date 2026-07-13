# Feature Backlog

**Letzte Aktualisierung:** 2026-07-13 (S3: 5 reife Items archiviert → `archive/`; verbleiben 2 Features „Fertig zum Testen")

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| Skill-10x-Optimierungen | Abgenommen | Mittel | features/skill-10x-optimierungen/spec.md | Fünf Bestands-Skills additiv nach 10x-Vorbild härten: project-health (A/B, WARN-CONTINUE, Fixes), debug-plan (Evidenz-Tabelle), greenfield-roadmap (Slices/Unlocks), feature-discover (Checkpoint, Recommended), checkpoint/resume (Handoff) |
| Change-Folder-Modell | Abgenommen | Mittel | features/change-folder-modell/spec.md | Ein Ordner pro Change (`features/<kebab-slug>/` mit fixen Dateinamen) statt flacher UPPER_SNAKE-Dateien mit Namens-Pairing; Archivierung = `git mv` des Ordners; harter Schnitt + einmaliger Migrations-Helfer |

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
