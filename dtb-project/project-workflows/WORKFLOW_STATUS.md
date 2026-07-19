# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-19
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-19.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Verifikations-Gate | Fertig zum Testen | 18/18 | Real abnehmen (pkp) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen (pkp) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Opportunity-Map | Fertig zum Testen | 11/11 | Real abnehmen (Map in echtem build/buy-Flow) → `/dtb:workflow-checkpoint` |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Real abnehmen (erster realer Greenfield-Lauf) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit". open-question (#26) komplett gebaut, reviewt (9 Findings FIXED) und global verteilt — es bleiben nur reale Zielprojekt-Abnahmen.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-19: open-question end-to-end durch die Pipeline (idea-review→…→kit-sync). impl-review-F1 (blocking Routing-Bug in Schritt 2a) gefixt + re-verteilt (`b7c0e0b`/`d399be8`). |

---

## Offene Aufgaben

- [ ] Reale Abnahmen abbauen — 6 Features „Fertig zum Testen" brauchen realen Zielprojekt-Lauf (pkp / echter Greenfield-/build-buy-Lauf / `[Fach]`-Nutzung / open-question im Alltag)
- [ ] Idee #28 (.gitattributes/EOL-Determinismus) ausarbeiten — `/dtb:feature-discover 28`
- [ ] Ideen-Triage fortsetzen — #27, #25, #24, #23, #22, #18, #16, #15, #10 offen
- [ ] `[Fach]`-Strang: #25 (Fach-Agenda, liest open-question-Output) → #24 (Antwort-Rueckfluss)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-19 | open-question (#26) gebaut + reviewt + verteilt | 9/9, impl-review 9 Fixed (F1 blocking), live `b7c0e0b`/`d399be8` | `features/open-question/review.md` |
| 2026-07-18 | verifikations-gate-Review vollstaendig entschieden | F1/F2/F3 FIXED | `features/verifikations-gate/review.md` |
| 2026-07-18 | greenfield-autoren-skills impl-review + verteilt | 6 Fixed/1 Skipped, `e157cdf` | `features/greenfield-autoren-skills/review.md` |
| 2026-07-18 | opportunity-map impl-review + verteilt | 4 Fixed/2 Skipped, `773dd73` | `features/opportunity-map/review.md` |
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention | `2026-07/2026-07-17.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` — kein Feature in Arbeit; open-question-Review aufgeloest (9 FIXED, verteilt). Die sechs „Fertig zum Testen" brauchen reale Zielprojekt-Abnahmen (kein Kit-interner Schritt). Kit-intern alternativ: `/dtb:feature-discover 28` (.gitattributes) oder Ideen-Triage (`/dtb:idea-review`).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
