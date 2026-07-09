# Feature Backlog

**Letzte Aktualisierung:** 2026-07-09 (SKILL_10X_OPTIMIERUNGEN spezifiziert)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| Review-Härtung | Fertig zum Testen | Hoch | FEATURE_REVIEW_HAERTUNG.md | plan-review und code-review liefern mechanisch geprüfte, verbindliche Verdikte: Grounding + Challenger-Pass + Dimensions-Verdikte; Severity×Impact-Doppelachse + Cap + Resume-Marker |
| Spec-Härtung | Fertig zum Testen | Mittel | FEATURE_SPEC_HAERTUNG.md | feature-plan-Specs lösungsneutral + ehrlich halten: Technical-Leak-Lint (7 Kategorien, Hard-Block+Override) + „nie erfinden → Offene Punkte" statt [TODO] |
| Skill-10x-Optimierungen | In Arbeit | Mittel | FEATURE_SKILL_10X_OPTIMIERUNGEN.md | Fünf Bestands-Skills additiv nach 10x-Vorbild härten: project-health (A/B, WARN-CONTINUE, Fixes), debug-plan (Evidenz-Tabelle), greenfield-roadmap (Slices/Unlocks), feature-discover (Checkpoint, Recommended), checkpoint/resume (Handoff) |

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
| Derived State | 2026-07-08 | `archive/FEATURE_DERIVED_STATE.md` |
| Kit Sync | 2026-07-08 | `archive/FEATURE_KIT_SYNC.md` |
| Lesson Loop | 2026-07-08 | `archive/FEATURE_LESSON_LOOP.md` |
| Betriebs-Wächter (plan-review) | 2026-07-08 | kein FEATURE-Artefakt — Commit `4ee4a9a` (bedingter 4. Review-Agent + Rollen-Schärfung) |

---

## Status-Legende (abgeleitet aus Artefakten)

| Status | Abgeleitet aus |
|--------|----------------|
| Idee | Nur INBOX-/BACKLOG-Eintrag, keine Artefakte |
| In Discovery | DISCOVERY_*.md existiert |
| Spezifiziert | FEATURE_*.md existiert, kein PLAN |
| Geplant | PLAN_*.md existiert, 0 Schritte abgehakt |
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
