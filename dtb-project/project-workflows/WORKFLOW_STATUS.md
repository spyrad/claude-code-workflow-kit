# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-16
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-16.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| commit-and-push | In Arbeit | 0/10 | `/dtb:implement commit-and-push` (Schritt 1.1) |
| impl-review | Fertig zum Testen | 19/19 | Realeinsatz (pkp) → Abnahme; Follow-up F2 offen (review.md) |
| Verifikations-Gate | Fertig zum Testen | 18/18 | Realeinsatz (pkp), dann Abnahme; Follow-up F2 offen |
| Opportunity-Map | Fertig zum Testen | 11/11 | Abnahme beim ersten realen Greenfield-Vorhaben |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Abnahme beim ersten realen Greenfield (Entscheidung G) |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-16 (S3): #21 `commit-and-push` aus INBOX gezogen, Discovery fertig (Form=Skill, #19-entkoppelt). Monorepo-Scoping offen — Damian zeigt konkretes Beispiel (anderer Rechner). |

---

## Offene Aufgaben

- [ ] `/dtb:feature-plan commit-and-push` — Kontext: Spec aus Discovery; klaeren: geteilte vs. duplizierte Sicherheits-Formulierung mit `implement`, Pipeline-Frontmatter (`stage: monitoring`/`utility`)
- [ ] Monorepo-Scoping bewerten — Kontext: Damian bringt konkretes Monorepo-Projekt (Folge-Session, anderer Rechner) → MVP oder spaetere Erweiterung (`commit-and-push/discovery.md`, Offene Punkte)
- [ ] impl-review + Verifikations-Gate real abnehmen — Kontext: erster echter Einsatz im Zielprojekt (pkp), dann „Abgenommen" via Checkpoint-Beleg-Rueckfrage
- [ ] Follow-up F2 — Kontext: `DERIVED_STATE_RULES.md` §2 Regel 3 um „verletzt ≠ ausstehend"-Nuance ergaenzen (`features/verifikations-gate/review.md`, PENDING)
- [ ] Idee-Triage fortsetzen — Kontext: verbleibende offene Ideen (#22, #18, #16, #15, #13, #10) → `/dtb:idea-review`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-16 | commit-and-push (#21) Discovery | Form=Skill, `git add -A`+Red-Flag-Scan, Multi-Repo pro-Repo-Commit, #19-entkoppelt; Monorepo-Frage offen | `2026-07/2026-07-16.md` (S3) |
| 2026-07-16 | impl-review verteilt | Push origin (ee0f3c8) + kit-sync: Skill global, code-review entfernt, 40 synchron | `2026-07/2026-07-16.md` (S2) |
| 2026-07-16 | impl-review (#20) umgesetzt | Neuer 3-Dimensionen-Review-Skill; code-review abgeloest; 19/19 | `2026-07/2026-07-16.md` (S1) |
| 2026-07-15 | Verifikations-Gate (#19) umgesetzt | `dtb:implement` neu; §2 gehaertet; 18/18; global verteilt | `2026-07/2026-07-15.md` (S2-S3) |
| 2026-07-14 | Opportunity-Map fertig + verteilt | Skill + greenfield-prd-Nudge; 11/11; global verteilt | `2026-07/2026-07-14.md` (S2-S4) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:feature-plan commit-and-push` — Discovery ist abgeschlossen, Spec ist der naechste Schritt. Die vier „Fertig zum Testen"-Features warten weiterhin auf reale Abnahme im Zielprojekt (pkp) — manueller Einsatz-Schritt, kein Skill.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
