# Feature Backlog

**Letzte Aktualisierung:** 2026-07-10 (Kit-Bug project-init-stale-rules-seed behoben + global verteilt, Lock `96eb2df`)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| Review-Härtung | Fertig zum Testen (nur plan-review-Hälfte real belegt) | Hoch | features/review-haertung/spec.md | plan-review und code-review liefern mechanisch geprüfte, verbindliche Verdikte: Grounding + Challenger-Pass + Dimensions-Verdikte; Severity×Impact-Doppelachse + Cap + Resume-Marker |
| Spec-Härtung | Abgenommen | Mittel | features/spec-haertung/spec.md | feature-plan-Specs lösungsneutral + ehrlich halten: Technical-Leak-Lint (7 Kategorien, Hard-Block+Override) + „nie erfinden → Offene Punkte" statt [TODO] |
| Skill-10x-Optimierungen | Fertig zum Testen | Mittel | features/skill-10x-optimierungen/spec.md | Fünf Bestands-Skills additiv nach 10x-Vorbild härten: project-health (A/B, WARN-CONTINUE, Fixes), debug-plan (Evidenz-Tabelle), greenfield-roadmap (Slices/Unlocks), feature-discover (Checkpoint, Recommended), checkpoint/resume (Handoff) |
| Change-Folder-Modell | Fertig zum Testen | Mittel | features/change-folder-modell/spec.md | Ein Ordner pro Change (`features/<kebab-slug>/` mit fixen Dateinamen) statt flacher UPPER_SNAKE-Dateien mit Namens-Pairing; Archivierung = `git mv` des Ordners; harter Schnitt + einmaliger Migrations-Helfer |
| Frontmatter- und Pfad-Hygiene | Abgenommen | Hoch | features/frontmatter-pfad-hygiene/spec.md | Konsistenz-Lecks schliessen (#8+#9): plan-review/pipeline-graph agents/-Pfad global+Fallback; after/next zu Listen (1:n-Pipeline); context:fork + Stage-Enum `bug` bereinigen; debug-plan schreibt `## Fix-Schritte` (aktiver Ableitungs-Bug) |
| Eligibility-Gates | Abgenommen | Mittel | features/eligibility-gates/spec.md | Schreibende Skills prüfen am Eingang das primäre `consumes`-Artefakt (+ gezielt Git-Zustand) und verweigern bei Nichteignung konstruktiv mit Redirect (produces-Rückwärtssuche → after-Liste); differenziert nach Hard-/Soft-/kein Gate |
| Bug: project-init seedet veraltete DERIVED_STATE_RULES.md | Behoben | Hoch | features/project-init-stale-rules-seed/bug.md | project-init erzeugt eine veraltete Regel-Datei (Flach-Modell), weil die Seed-Quelle in Zielprojekt-Sessions nicht auflösbar ist → Rekonstruktion statt Kopie |

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
