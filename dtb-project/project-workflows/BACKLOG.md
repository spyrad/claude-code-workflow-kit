# Feature Backlog

**Letzte Aktualisierung:** 2026-07-21 (meeting-dump #24 umgesetzt + reviewt → Fertig zum Testen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| meeting-dump | Fertig zum Testen | Mittel | features/meeting-dump/spec.md | Skill `/dtb:meeting-dump`: Meeting-Input als Beleg persistieren + gegen offene `[Fach]`-Fragen abgleichen — Antwort-Rückfluss der Fachfragen-Kette (#13→#26→#24) |
| Verifikations-Gate | Abgenommen | Hoch | features/verifikations-gate/spec.md | Umsetzungs-Loop erhält ein echtes Verifikations-Gate: dtb:implement treibt den Plan phasenweise, Checkbox flippt erst bei grünen Checkpoint-Kriterien, SHA wird Verifikations-Beleg |
| Greenfield-Autoren-Skills | Abgenommen | Hoch | features/greenfield-autoren-skills/spec.md | greenfield-prd/-roadmap werden Autoren-Skills (PRD-Interview → PRD-MVP.md, Lean-Roadmap → ROADMAP.md + TECH-STACK.md) nach 10x-Vorbild, Derived-State-konform |
| Opportunity-Map | Abgenommen | Mittel | features/opportunity-map/spec.md | Vorfeld-Skill, der wiederkehrende Reibung in eine build/buy/complement/wait-Entscheidung überführt, bevor teure PRD-/Bau-Arbeit beginnt |
| commit-and-push | Fertig zum Testen | Mittel | features/commit-and-push/spec.md | Geführter Routine-Skill, der Änderungen sicher committet und pusht; Repo-Grenzen aus git (rev-parse --show-toplevel) statt config.repos → monorepo-, poly-repo- und einzelverzeichnis-fest |
| Fachfragen-Erfassung | Fertig zum Testen | Mittel | features/fachfragen-erfassung/spec.md | Fach-Fragen aus der Entwicklung statusfähig + maschinell erkennbar direkt im Artefakt erfassen (`- [ ] [Fach] {Frage}`), Derived-State-konform — Fundament für spätere Meeting-Agenda-Ansicht |
| open-question | Fertig zum Testen | Mittel | features/open-question/spec.md | Aktiver Erfassungs-Skill `/dtb:open-question`, der eine Fach-Frage per Argument §6-konform als `- [ ] [Fach] {Frage}` ins aktive Feature-Artefakt schreibt — das Eingabe-Werkzeug der Fachfragen-Kette (#13→#26→#25→#24) |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
| impl-review | 2026-07-17 | `archive/impl-review/` |
| Codebase-Research-Step | 2026-07-14 | `archive/codebase-research-step/` |
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
