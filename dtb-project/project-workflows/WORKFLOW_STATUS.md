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
| Opportunity-Map | Fertig zum Testen | 11/11 | impl-review ✓ — Real abnehmen (Map in echtem Flow nutzen) |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | impl-review ✓ — Real abnehmen (erster realer Greenfield-Lauf, zweistufig) |

Kein Feature „In Arbeit" — Pipeline leer. Review-Front leer: alle fuenf „Fertig zum Testen" sind reviewt, es bleiben nur reale Abnahmen.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-18 (S2): greenfield-autoren-skills impl-review → 6 Fixed/1 Skipped (F1: L5-Format-Kopplung war defekt, gefixt). 4 Dateien im Working Tree, noch nicht committet. F2-Follow-up (Verifikations-Gate) lebt in `verifikations-gate/review.md`. |

---

## Offene Aufgaben

- [ ] greenfield-autoren-skills-Fixes committen + verteilen — Kontext: 4 Dateien Working Tree (`/dtb:commit-and-push` → `/dtb:kit-sync sync`)
- [ ] Restliche Abnahmen abbauen — Kontext: opportunity-map + greenfield-autoren-skills (echter Flow), commit-and-push / Verifikations-Gate (pkp), fachfragen-erfassung
- [ ] Follow-up F2 (§2 Regel 3 „verletzt ≠ ausstehend") — Kontext: `verifikations-gate/review.md` PENDING
- [ ] `[Fach]`-Strang #26 → #25 → #24 ausarbeiten — Kontext: baut auf §6, bei Kapazitaet
- [ ] Idee-Triage fortsetzen — Kontext: #27, #23, #22, #18, #16, #15, #10 offen

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-18 | greenfield-autoren-skills impl-review | NEEDS ATTENTION, 7 Findings (6 Fixed/1 Skipped) | `features/greenfield-autoren-skills/review.md` |
| 2026-07-18 | opportunity-map impl-review + verteilt | 4 Fixed/2 Skipped, `773dd73` gepusht, global synchron | `features/opportunity-map/review.md` |
| 2026-07-17 | impl-review (#20) abgeschlossen | 19/19, 7 Findings FIXED, global verteilt → archiviert | `archive/impl-review/` |
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention, impl-review 5/5 FIXED | `2026-07/2026-07-17.md` (S1) |
| 2026-07-16 | commit-and-push (#21) fertig | 10/10, 7/7 FIXED, gepusht + global verteilt | `2026-07/2026-07-16.md` (S5-S6) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — 4 greenfield-autoren-skills-Fixes im Working Tree sichern, danach `/dtb:kit-sync sync` (greenfield-prd/-roadmap global). Kein Feature in Arbeit, Review-Front leer → danach `/dtb:workflow-next` fuer die realen Abnahmen.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
