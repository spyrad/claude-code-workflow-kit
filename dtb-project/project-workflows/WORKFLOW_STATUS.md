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

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-17 (S1): `fachfragen-erfassung` (#13) 8/8 fertig — §6 Fach-Frage-Konvention (`[Fach]` in `## Offene Punkte`), reviewt (5 Findings FIXED), noch nicht verteilt. Lese-Ansicht ausgelagert (#25). Sechs Features warten auf reale Abnahme. |

---

## Offene Aufgaben

- [ ] `fachfragen-erfassung` real abnehmen (naechste feature-discovery/-plan nutzt `[Fach]`) → Abnahme, dann `/dtb:kit-sync` (feature-discover, feature-plan; §6-Seed erreicht Bestand nicht, #22)
- [ ] `dtb:commit-and-push` real im pkp-Monorepo testen → Abnahme via `/dtb:workflow-checkpoint`
- [ ] INBOX #25 (Fach-Agenda) + #23 (Multi-Repo-Begriff auf toplevel) triagieren
- [ ] impl-review + Verifikations-Gate real abnehmen (pkp); Follow-up F2 (§2 Regel 3)
- [ ] Idee-Triage fortsetzen — verbleibende Ideen (#24, #22, #18, #16, #15, #10)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention, impl-review 5/5 FIXED, 3 Phasen-Commits | `2026-07/2026-07-17.md` (S1) |
| 2026-07-16 | commit-and-push (#21) fertig | 10/10, impl-review 7/7 FIXED, gepusht + global verteilt | `2026-07/2026-07-16.md` (S5-S6) |
| 2026-07-16 | impl-review (#20) umgesetzt + verteilt | 3-Dimensionen-Review-Skill; code-review abgeloest; 19/19 | `2026-07/2026-07-16.md` (S1-S2) |
| 2026-07-15 | Verifikations-Gate (#19) umgesetzt | `dtb:implement` neu; §2 gehaertet; 18/18; verteilt | `2026-07/2026-07-15.md` (S2-S3) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` — fachfragen-erfassung ist fertig+reviewt (kein zwingender Skill-Schritt offen; wartet auf reale Abnahme + kit-sync-Verteilung). workflow-next bestimmt den naechsten produktiven Schritt (reale Abnahme, INBOX #25/#23-Triage oder Idee-Triage).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
