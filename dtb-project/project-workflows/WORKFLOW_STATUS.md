# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-20
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-20.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Verifikations-Gate | Abgenommen | 18/18 | Abgeschlossen → `/dtb:archive` (optional) |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen (naechster pkp-implement-Lauf, selbes Muster) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Opportunity-Map | Fertig zum Testen | 11/11 | Real abnehmen (Map in echtem build/buy-Flow) → `/dtb:workflow-checkpoint` |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Real abnehmen (erster realer Greenfield-Lauf) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit". Verifikations-Gate (#19) heute real abgenommen (pkp-Lauf `f39af15`, Gate biss). 5 Features bleiben „Fertig zum Testen".

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-20: Verifikations-Gate im Zielprojekt pkp durchgespielt — Gate verweigerte Flip bei rotem Kriterium; #23 (Multi-Repo-SHA-Praefix) dabei hart reproduziert. |

---

## Offene Aufgaben

- [ ] pkp aufraeumen: SHA-Rueckschreibung in `ws-status-fallthrough/plan.md` noch uncommitted → pkp-eigener Checkpoint; optional `/dtb:impl-review` + Folge-Change `useFilterOptions.ts`
- [ ] #23 (Multi-Repo-Begriff auf Git-toplevel) ausarbeiten — jetzt hart belegt → `/dtb:feature-discover 23`
- [ ] Reale Abnahmen abbauen — 5 Features „Fertig zum Testen" (commit-and-push liefe im selben pkp-Muster mit ab)
- [ ] Ideen-Triage fortsetzen — #28, #27, #25, #24, #22, #18, #17, #16, #15, #10 offen
- [ ] `[Fach]`-Strang: #25 (Fach-Agenda, liest open-question-Output) → #24 (Antwort-Rueckfluss)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-20 | Verifikations-Gate (#19) real abgenommen | pkp-Lauf `f39af15`, Gate biss bei 1.2, SHA am Phasen-Ende, #23 reproduziert | `2026-07/2026-07-20.md` |
| 2026-07-19 | open-question (#26) gebaut + reviewt + verteilt | 9/9, impl-review 9 Fixed (F1 blocking), live `b7c0e0b`/`d399be8` | `features/open-question/review.md` |
| 2026-07-18 | verifikations-gate-Review vollstaendig entschieden | F1/F2/F3 FIXED | `features/verifikations-gate/review.md` |
| 2026-07-18 | greenfield-autoren-skills impl-review + verteilt | 6 Fixed/1 Skipped, `e157cdf` | `features/greenfield-autoren-skills/review.md` |
| 2026-07-18 | opportunity-map impl-review + verteilt | 4 Fixed/2 Skipped, `773dd73` | `features/opportunity-map/review.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` — kein Feature in Arbeit. Verifikations-Gate abgenommen; die verbleibenden 5 „Fertig zum Testen" brauchen reale Zielprojekt-Abnahmen (kein Kit-interner Schritt). Kit-intern reif: `/dtb:feature-discover 23` (#23 jetzt hart belegt) oder Ideen-Triage (`/dtb:idea-review`).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
