# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-23 (Session 1)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-23.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit" (alle `## Progress` vollstaendig, alle reviewt). Diese Session: kein Progress-Flip — Arbeit lag auf Kit-Struktur, Distribution und Ideen-Triage.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-23 (S1): Personas + pitch-coach-Command aus dem Kit entfernt (`7c3272a`) — Quelle liegt byte-identisch in `oma-personas`; Kit traegt Personas nur als Destillate. kit-sync auf `7c3272a`, 41 Artefakte, 0 Abweichung; meeting-dump erstmals global. INBOX 11 offen (#30/#31 neu, #10 verworfen+archiviert). |

---

## Offene Aufgaben

- [ ] `/dtb:idea-review` fortsetzen — 11 offene Ideen (Kandidat #25 Fach-Agenda)
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features abbauen
- [ ] #31 entscheiden: `skills/CLAUDE.md` als Klasse A aufnehmen oder aus dem Lock streichen — Kontext: installierte Kopie haengt am alten Stand, kein check meldet es
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)
- [ ] `[Fach]`-Strang: #25 (Fach-Agenda, liest open-question-Output) → #24-Rückfluss (meeting-dump)
- [ ] #23 (Multi-Repo-Begriff auf git-toplevel vereinheitlichen)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-23 | Personas aus dem Kit entfernt (S1) | Halbzustand aufgeloest; Doku + tote #8-Verweise bereinigt | `7c3272a` |
| 2026-07-23 | kit-sync auf 7c3272a (S1) | 4 uebernommen, 1 verwaist entfernt, 0 Abweichung | `2026-07/2026-07-23.md` |
| 2026-07-22 | 3 Features archiviert (S2) | verifikations-gate, greenfield-autoren-skills, opportunity-map | `1ad8c6e`, `archive/ARCHIVE_LOG.md` |
| 2026-07-22 | Opportunity-Map + Greenfield-Autoren-Skills abgenommen (S2) | Nutzer-Entscheidung; `8debb8c` | `2026-07/2026-07-22.md` |
| 2026-07-22 | DtB-Designsprache aus pkp extrahiert + Kit-Konvention (S1) | pkp intern `UI.md`+Tokens; Kit `project-design`-Bucket | `2026-07/2026-07-22.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — 3 uncommittete Dateien aus dieser Session (Session-Log, `WORKFLOW_STATUS.md`, `INBOX.md`+`ARCHIVE_LOG.md`). Danach `/dtb:idea-review` fortsetzen: kein Feature „In Arbeit", die 4 aktiven sind reviewt und warten auf reale Abnahme (kein Kit-interner Schritt); offener Kit-Faden sind die 11 INBOX-Ideen (Kandidat #25 Fach-Agenda).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
