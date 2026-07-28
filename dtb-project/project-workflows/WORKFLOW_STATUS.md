# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-28 (Session 2)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-28.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit" (alle `## Progress` vollstaendig, alle reviewt). Beide Sessions heute: kein Progress-Flip — Arbeit lag auf Ideen-Ebene. Abnahme-Abfrage: keines der vier Features abgenommen. Ideen-Ebene: **kein Eintrag auf „In Arbeit"** (#15 zurueckgesetzt und vertagt, #16 verworfen, #32 neu).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-28: Zwei Parallel-Sessions an zwei Rechnern (S1 zuhause `df7232c`, S2 am Arbeitsplatz) — #16 doppelt bearbeitet, per Stash + `pull --ff-only` zusammengefuehrt, staerker belegter S1-Text behalten. S1: #16 verworfen (Substanz sitzt in `opportunity-map` `SKILL.md:78`/`:83`/`:145-157`); `grill-me`/#27 global bereits installiert. S2: #32 erfasst (`feature-discover` ohne Aufnahmekriterium, 4 von 20 `discovery.md` mit Fremdpfaden), #15 vertagt (Vorbild ist Kettenglied, Brownfield-Ast fehlt im Kit). INBOX 11 offen, 4 ausgearbeitet, 1 verworfen. |

---

## Offene Aufgaben

- [ ] `workflow-resume` um Remote-Divergenz-Check erweitern (`git fetch` + `rev-list --left-right --count`) — prueft heute nur lokal, Parallelarbeit an zwei Rechnern faellt erst beim Commit auf (Lehre 2026-07-28)
- [ ] `/dtb:idea-review` fortsetzen — 10 offene Ideen ohne #15; naechstliegend #27 (`grill-me` schon installiert, ohne Bau entscheidbar) und #25 (Fach-Agenda, fehlendes Glied der Kette #13→#26→#25→#24)
- [ ] `opportunity-map` `stage: greenfield` entscheiden — widerspricht dem eigenen Brownfield-Hinweis; `workflow-status` liest die Stage
- [ ] Checkpoint committen (`/dtb:commit-and-push`)
- [ ] build-check entscheiden: streichen (Option A von 2026-07-15 nachholen) oder behalten — braucht den pkp-Nutzungsbeleg
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features abbauen
- [ ] #31 entscheiden: `skills/CLAUDE.md` als Klasse A aufnehmen oder aus dem Lock streichen
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)
- [ ] #23 (Multi-Repo-Begriff auf git-toplevel vereinheitlichen)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-28 | #32 erfasst + #15 vertagt (S2) | `feature-discover`-Schwachpunkt mit 4-von-20-Bestandsbefund belegt; #15 als Ast-Entscheidung erkannt, Kontext verankert | `2026-07/2026-07-28.md` |
| 2026-07-28 | #16 verworfen + Backlog-Sichtung (S1) | Mom-Test-Substanz in `opportunity-map` belegt; Umsetzungsseite des Backlogs leer | `2026-07/2026-07-28.md` |
| 2026-07-27 | #15 vorgeprueft + build-check-Befund (S1) | Abgrenzung belegt, Verdikt gefasst, build-check als ungenutzt nachgewiesen | `2026-07/2026-07-27.md` |
| 2026-07-23 | Personas aus dem Kit entfernt (S1) | Halbzustand aufgeloest; Doku + tote #8-Verweise bereinigt | `7c3272a` |
| 2026-07-23 | kit-sync auf 7c3272a (S1) | 4 uebernommen, 1 verwaist entfernt, 0 Abweichung | `2026-07/2026-07-23.md` |
| 2026-07-22 | 3 Features archiviert (S2) | verifikations-gate, greenfield-autoren-skills, opportunity-map | `1ad8c6e`, `archive/ARCHIVE_LOG.md` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — braucht zusammenhaengenden Fokus, nicht einen Rest-Slot. Nach dem Kettenbefund ist es keine Skill-Frage, sondern eine **Ast-Entscheidung** (Brownfield-Zweig im Kit: ja/nein, in welcher Reihenfolge).
**Details:** Kontext vollstaendig im Idee-Text (`INBOX.md` #15) — sechs benannte Entscheidungen; Analyse in `2026-07/2026-07-27.md` (S1) und `2026-07/2026-07-28.md` (S2)

---

## Handoff

**Naechster Befehl:** `/dtb:idea-review` — der Lauf wurde nach #16 unterbrochen, 10 offene Ideen sind noch nicht durchgegangen (#15 dabei ueberspringen, ist vertagt). Kein Feature-Befehl ableitbar: alle vier Items sind `Y/Y`, reviewt und warten auf reale Abnahme im Zielprojekt pkp — von hier aus nicht moeglich. Der frueher hier stehende `/dtb:feature-discover 15` ist **nicht** mehr gueltig (Idee vertagt).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl. **Bei Rechnerwechsel vorher `git fetch` + Divergenz pruefen** — heute entstand so Doppelarbeit an #16.
