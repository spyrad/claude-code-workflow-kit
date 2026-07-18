# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-18
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-18.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Verifikations-Gate | Fertig zum Testen | 18/18 | Real abnehmen (pkp) + Follow-up F2 → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen (pkp) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Opportunity-Map | Fertig zum Testen | 11/11 | impl-review ✓ (review.md, NEEDS ATTENTION, 4 Fixed/2 Skipped) — Real abnehmen (Map in echtem Flow nutzen) |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Feature-End-Review → `/dtb:impl-review Greenfield-Autoren-Skills` |

Kein Feature „In Arbeit" — Pipeline leer, fuenf Features warten auf Review/Abnahme (Opportunity-Map am 2026-07-18 reviewt; nur Greenfield-Autoren-Skills braucht noch ein Review).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-18 (S1): opportunity-map impl-review → 4 Guard-/Konsistenz-Fixes im Working Tree (noch nicht committet). F2-Follow-up (Verifikations-Gate „verletzt ≠ ausstehend") lebt weiter in `verifikations-gate/review.md`. |

---

## Offene Aufgaben

- [ ] opportunity-map-Fixes committen — Kontext: 3 Dateien im Working Tree (`/dtb:commit-and-push`)
- [ ] Greenfield-Autoren-Skills reviewen — Kontext: einziges „Fertig zum Testen" ohne review.md
- [ ] Restliche Abnahmen abbauen — Kontext: opportunity-map (echter Flow), commit-and-push / Verifikations-Gate (pkp), fachfragen-erfassung
- [ ] Follow-up F2 (§2 Regel 3 „verletzt ≠ ausstehend") — Kontext: `verifikations-gate/review.md` PENDING
- [ ] `[Fach]`-Strang #26 → #25 → #24 ausarbeiten — Kontext: baut auf §6, bei Kapazitaet
- [ ] Idee-Triage fortsetzen — Kontext: #27, #23, #22, #18, #16, #15, #10 offen

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-18 | opportunity-map impl-review | NEEDS ATTENTION, 6 Findings (4 Fixed/2 Skipped) | `features/opportunity-map/review.md` |
| 2026-07-17 | impl-review (#20) abgeschlossen | 19/19, 7 Findings FIXED, global verteilt → archiviert | `archive/impl-review/` |
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention, impl-review 5/5 FIXED | `2026-07/2026-07-17.md` (S1) |
| 2026-07-16 | commit-and-push (#21) fertig | 10/10, 7/7 FIXED, gepusht + global verteilt | `2026-07/2026-07-16.md` (S5-S6) |
| 2026-07-15 | Verifikations-Gate (#19) umgesetzt | `dtb:implement` neu; §2 gehaertet; 18/18; verteilt | `2026-07/2026-07-15.md` (S2-S3) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:impl-review Greenfield-Autoren-Skills` — einziges „Fertig zum Testen"-Feature ohne `review.md` (Feature-End-Review vor der Abnahme). Danach nur noch reale Abnahmen offen → `/dtb:workflow-next` priorisiert.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
