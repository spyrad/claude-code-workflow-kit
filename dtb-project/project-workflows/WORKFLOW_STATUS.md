# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-16
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-16.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| commit-and-push | In Arbeit | 9/10 | 3.3 (Verteilung) — `/dtb:impl-review commit-and-push` empfohlen davor |
| impl-review | Fertig zum Testen | 19/19 | Realeinsatz (pkp) → Abnahme; Follow-up F2 offen |
| Verifikations-Gate | Fertig zum Testen | 18/18 | Realeinsatz (pkp), dann Abnahme; Follow-up F2 offen |
| Opportunity-Map | Fertig zum Testen | 11/11 | Abnahme beim ersten realen Greenfield-Vorhaben |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Abnahme beim ersten realen Greenfield (Entscheidung G) |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-16 (S4): `commit-and-push` (#21) 9/10 umgesetzt. Kern: Repo-Grenzen aus `git rev-parse --show-toplevel`, nicht `config.repos` — monorepo-fest (an pkp belegt). Offen: 3.3 (Push + kit-sync), bewusst nach impl-review verschoben (keine Verteilung ungepruefter Skills). |

---

## Offene Aufgaben

- [ ] `/dtb:impl-review commit-and-push` — Feature-End-Review VOR der Verteilung (Code fertig 9/10)
- [ ] commit-and-push 3.3: Push nach origin + `/dtb:kit-sync` (globale Verteilung des neuen Skills)
- [ ] INBOX #23 triagieren — Multi-Repo-Begriff kitweit auf `rev-parse --show-toplevel` vereinheitlichen (implement/§2 Regel 5 vs. commit-and-push)
- [ ] impl-review + Verifikations-Gate real abnehmen — erster echter Einsatz im Zielprojekt (pkp), dann „Abgenommen" via Checkpoint-Beleg
- [ ] Follow-up F2 — `DERIVED_STATE_RULES.md` §2 Regel 3 um „verletzt ≠ ausstehend"-Nuance (`features/verifikations-gate/review.md`, PENDING)
- [ ] Idee-Triage fortsetzen — verbleibende offene Ideen (#22, #18, #16, #15, #13, #10)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-16 | commit-and-push (#21) 9/10 | Neuer Skill; git-toplevel statt config.repos (monorepo-fest, an pkp belegt); nur Verteilung (3.3) offen | `2026-07/2026-07-16.md` (S4) |
| 2026-07-16 | commit-and-push (#21) Discovery | Form=Skill, `git add -A`+Red-Flag-Scan, Multi-Repo pro-Repo, #19-entkoppelt | `2026-07/2026-07-16.md` (S3) |
| 2026-07-16 | impl-review verteilt | Push origin (ee0f3c8) + kit-sync: Skill global, code-review entfernt, 40 synchron | `2026-07/2026-07-16.md` (S2) |
| 2026-07-16 | impl-review (#20) umgesetzt | Neuer 3-Dimensionen-Review-Skill; code-review abgeloest; 19/19 | `2026-07/2026-07-16.md` (S1) |
| 2026-07-15 | Verifikations-Gate (#19) umgesetzt | `dtb:implement` neu; §2 gehaertet; 18/18; global verteilt | `2026-07/2026-07-15.md` (S2-S3) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:impl-review commit-and-push` — der Skill ist inhaltlich fertig (9/10, nur die Verteilung 3.3 offen); der Feature-End-Review (Plan-Drift + Craft + Rules) sollte VOR der globalen kit-sync-Verteilung laufen. Danach Schritt 3.3 (Push nach origin + `/dtb:kit-sync`).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
