# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-17
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-17.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| fachfragen-erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → Abnahme via `/dtb:workflow-checkpoint`; danach `/dtb:kit-sync` |
| commit-and-push | Fertig zum Testen | 10/10 | Real testen (pkp) → Abnahme; review.md alle FIXED |
| impl-review | Fertig zum Testen | 19/19 | Realeinsatz (pkp) → Abnahme; Follow-up F2 offen |
| Verifikations-Gate | Fertig zum Testen | 18/18 | Realeinsatz (pkp), dann Abnahme; Follow-up F2 offen |
| Opportunity-Map | Fertig zum Testen | 11/11 | Abnahme beim ersten realen Greenfield-Vorhaben |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Abnahme beim ersten realen Greenfield (Entscheidung G) |

Kein Feature „In Arbeit" — Pipeline leer, sechs Features warten auf reale Abnahme.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-17 (S2): Keine Umsetzung — Ideen #26 (`/dtb:open-question`, das in #13 fehlende Eingabe-Werkzeug) + #27 (`grill-me` fuer Greenfield) erfasst. Design-Smell: §6 status-neutral, sitzt aber im Status-Regelwerk → bei #26 neu verorten. |

---

## Offene Aufgaben

- [ ] #26 (`/dtb:open-question`) ausarbeiten — §6-Verortung + „an Feature gebunden vs. flaches Postfach" klaeren
- [ ] #27 (`grill-me`) evaluieren — Abgrenzung zu plan-review/feature-discover, Platz im Vorfeld
- [ ] Reale Abnahmen nicht weiter aufstauen: commit-and-push / impl-review / Verifikations-Gate (pkp), fachfragen-erfassung
- [ ] `/dtb:kit-sync sync` fuer fachfragen-erfassung erst NACH realer Abnahme (§6-Seed erreicht Bestand nicht, #22)
- [ ] Idee-Triage fortsetzen — offene Ideen (#25, #24, #23, #22, #18, #16, #15, #10)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention, impl-review 5/5 FIXED, gepusht | `2026-07/2026-07-17.md` (S1) |
| 2026-07-16 | commit-and-push (#21) fertig | 10/10, impl-review 7/7 FIXED, gepusht + global verteilt | `2026-07/2026-07-16.md` (S5-S6) |
| 2026-07-16 | impl-review (#20) umgesetzt + verteilt | 3-Dimensionen-Review-Skill; code-review abgeloest; 19/19 | `2026-07/2026-07-16.md` (S1-S2) |
| 2026-07-15 | Verifikations-Gate (#19) umgesetzt | `dtb:implement` neu; §2 gehaertet; 18/18; verteilt | `2026-07/2026-07-15.md` (S2-S3) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` — kein Feature in Arbeit/geplant; naechster produktiver Schritt ist entweder eine reale Abnahme (Testau abbauen) oder das Ausarbeiten von Idee #26 (`/dtb:feature-discover`). workflow-next bestimmt konkret.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
