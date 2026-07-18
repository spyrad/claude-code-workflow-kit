# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-18
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-18.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Verifikations-Gate | Fertig zum Testen | 18/18 | Real abnehmen (pkp) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen (pkp) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Opportunity-Map | Fertig zum Testen | 11/11 | Real abnehmen (Map in echtem build/buy-Flow nutzen) → `/dtb:workflow-checkpoint` |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Real abnehmen (erster realer Greenfield-Lauf, zweistufig) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit" — Pipeline leer. Review-Front vollstaendig abgearbeitet (alle 5 Features reviewt, alle Findings FIXED); es bleiben nur reale Abnahmen im Zielprojekt.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-18 (S4): verifikations-gate-Review vollstaendig entschieden — F1/F2/F3 FIXED (`36d6c1a` F2, `b28451d` F1+F3). F2 haertete §2 Regel 3 (ausstehend≠verletzt). Kein kit-sync noetig (kein Klasse-A-Artefakt beruehrt; F2 = Klasse-B-Seed). |

---

## Offene Aufgaben

- [ ] Reale Abnahmen abbauen — Kontext: alle 5 Features „Fertig zum Testen", brauchen realen Zielprojekt-Lauf (pkp / echter Greenfield-/build-buy-Lauf / `[Fach]`-Nutzung)
- [ ] `[Fach]`-Strang #26 → #25 → #24 ausarbeiten — Kontext: baut auf §6, kit-intern machbar
- [ ] Idee-Triage fortsetzen — Kontext: #27, #23, #22, #18, #16, #15, #10 offen
- [ ] `lessons.md`-gitignore-Beobachtung festhalten — Kontext: im Kit-Repo lokal, „nicht-ausliefern"-Grund greift faktisch nicht → via `/dtb:idea`
- [ ] Kosmetik: BACKLOG „Ideen"-Platzhalter `[Feature 1]` entfernen

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-18 | verifikations-gate-Review vollstaendig entschieden | F1/F2/F3 FIXED, 2 Commits (`36d6c1a`, `b28451d`) | `features/verifikations-gate/review.md` |
| 2026-07-18 | greenfield-autoren-skills impl-review + verteilt | 6 Fixed/1 Skipped, `e157cdf` gepusht, global synchron | `features/greenfield-autoren-skills/review.md` |
| 2026-07-18 | opportunity-map impl-review + verteilt | 4 Fixed/2 Skipped, `773dd73` gepusht, global synchron | `features/opportunity-map/review.md` |
| 2026-07-17 | impl-review (#20) abgeschlossen | 19/19, 7 Findings FIXED, global verteilt → archiviert | `archive/impl-review/` |
| 2026-07-17 | fachfragen-erfassung (#13) fertig | 8/8, §6 Fach-Frage-Konvention, impl-review 5/5 FIXED | `2026-07/2026-07-17.md` (S1) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` — kein Feature in Arbeit, Review-Front leer, alle Findings verteilt/entschieden. Die fuenf „Fertig zum Testen" brauchen reale Zielprojekt-Abnahmen (kein Kit-interner Schritt); workflow-next listet sie. Kit-intern alternativ: `[Fach]`-Strang (#26) oder Ideen-Triage.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
