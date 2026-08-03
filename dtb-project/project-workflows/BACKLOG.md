# Feature Backlog

**Letzte Aktualisierung:** 2026-08-03 S3 (Feature **abnahme-zustand** komplett in einer Session: Idee #38 → Fast-Track → plan-review REVISE→Reviewed → implement 6/6 → impl-review-Triage 6/6 Fixed → distribuiert `f3288db` → **Abgenommen**. Damit 6 von 8 Features abgenommen; S1/S2: Zwei-Maschinen-Merge `594124c`, 5 Abnahmen, Distribution 43 @ `f3288db`)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| abnahme-zustand | Abgenommen (2026-08-03, alle 4 Manual-Gates in-session belegt) | Hoch | features/abnahme-zustand/spec.md | Der explizite Zustand `Abgenommen` erhält eine widerspruchsfreie Kanon-Definition und durchgängige Leser-Behandlung, damit freigegebene Changes nicht weiter als „Fertig zum Testen" geführt oder als Widerspruch gemeldet werden (Idee #38) |
| meeting-dump | Abgenommen (2026-08-03, Lauf im Zielprojekt — Projekt/Datum nicht protokolliert) | Mittel | features/meeting-dump/spec.md | Skill `/dtb:meeting-dump`: Meeting-Input als Beleg persistieren + gegen offene `[Fach]`-Fragen abgleichen — Antwort-Rückfluss der Fachfragen-Kette (#13→#26→#24) |
| commit-and-push | Abgenommen (2026-08-03, mit Vorbehalt Multi-Root) | Mittel | features/commit-and-push/spec.md | Geführter Routine-Skill, der Änderungen sicher committet und pusht; Repo-Grenzen aus git (rev-parse --show-toplevel) statt config.repos → monorepo-, poly-repo- und einzelverzeichnis-fest |
| Fachfragen-Erfassung | Abgenommen (2026-08-03, alle 3 Manual-Kriterien belegt) | Mittel | features/fachfragen-erfassung/spec.md | Fach-Fragen aus der Entwicklung statusfähig + maschinell erkennbar direkt im Artefakt erfassen (`- [ ] [Fach] {Frage}`), Derived-State-konform — Fundament für spätere Meeting-Agenda-Ansicht |
| open-question | Abgenommen (2026-08-03, alle 6 Manual-Kriterien belegt) | Mittel | features/open-question/spec.md | Aktiver Erfassungs-Skill `/dtb:open-question`, der eine Fach-Frage per Argument §6-konform als `- [ ] [Fach] {Frage}` ins aktive Feature-Artefakt schreibt — das Eingabe-Werkzeug der Fachfragen-Kette (#13→#26→#25→#24) |
| plan-status-feld | Abgenommen (2026-08-03, alle 3 Manual-Kriterien belegt) | Hoch | features/plan-status-feld/spec.md | plan.md-Kopf-Statusfeld bekommt genau einen Pfleger (plan-review schreibt bei jedem Verdikt den letzten Review-Stand), Leser gehaertet (Checkbox-Guard, ⚠-Konfliktmeldung, Toleranz-Matrix) + Kanonisierung in DERIVED_STATE_RULES.md |
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |

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
| Bug: project-init-status-pfad | 2026-07-30 | `archive/project-init-status-pfad/` |
| Bug: project-init-settings-seed | 2026-07-30 | `archive/project-init-settings-seed/` |
| Verifikations-Gate | 2026-07-22 | `archive/verifikations-gate/` |
| Greenfield-Autoren-Skills | 2026-07-22 | `archive/greenfield-autoren-skills/` |
| Opportunity-Map | 2026-07-22 | `archive/opportunity-map/` |
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
