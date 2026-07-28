# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-28 (Session 1)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-28.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit" (alle `## Progress` vollstaendig, alle reviewt). Diese Session: kein Progress-Flip — Arbeit lag auf Ideen-Review und Abgrenzungs-Analyse. Ideen-Ebene: **#15 auf „In Arbeit"** (wartet auf `/dtb:feature-discover`), **#16 verworfen**.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-28 (S1): #16 (`10x-mom-test`-Pendant) verworfen — Substanz sitzt bereits in `dtb:opportunity-map` (`SKILL.md:78`/`:83`/`:145-157`); Abgrenzung: Selbstauskunft (opportunity-map) vs. Gespraeche mit Dritten (Mom-Test), ohne Nutzer-Interviews liefe der Leitfaden leer. Backlog-Umsetzungsseite leer (0 in Arbeit, 0 geplant, 0 Bugs/Tasks). INBOX 9 offen. `grill-me`/#27 global bereits installiert, nie abgegrenzt. |

---

## Offene Aufgaben

- [ ] `/dtb:feature-discover 15` — Zuschnitt, Traeger und Naming entscheiden; Startkontext ist der Log vom 2026-07-27
- [ ] `/dtb:idea-review` fortsetzen — 9 offene Ideen (naechstliegend: #27 `grill-me` schon installiert, #25 Fach-Agenda)
- [ ] build-check entscheiden: streichen (Option A von 2026-07-15 nachholen) oder behalten — braucht den pkp-Nutzungsbeleg
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features abbauen
- [ ] #31 entscheiden: `skills/CLAUDE.md` als Klasse A aufnehmen oder aus dem Lock streichen
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)
- [ ] `[Fach]`-Strang: #25 (Fach-Agenda, liest open-question-Output) → #24-Rueckfluss (meeting-dump)
- [ ] #23 (Multi-Repo-Begriff auf git-toplevel vereinheitlichen)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-28 | #16 verworfen + Backlog-Sichtung (S1) | Mom-Test-Substanz in `opportunity-map` belegt; Umsetzungsseite des Backlogs leer | `2026-07/2026-07-28.md` |
| 2026-07-27 | #15 vorgeprueft + build-check-Befund (S1) | Abgrenzung belegt, Verdikt gefasst, build-check als ungenutzt nachgewiesen | `2026-07/2026-07-27.md` |
| 2026-07-23 | Personas aus dem Kit entfernt (S1) | Halbzustand aufgeloest; Doku + tote #8-Verweise bereinigt | `7c3272a` |
| 2026-07-23 | kit-sync auf 7c3272a (S1) | 4 uebernommen, 1 verwaist entfernt, 0 Abweichung | `2026-07/2026-07-23.md` |
| 2026-07-22 | 3 Features archiviert (S2) | verifikations-gate, greenfield-autoren-skills, opportunity-map | `1ad8c6e`, `archive/ARCHIVE_LOG.md` |
| 2026-07-22 | Opportunity-Map + Greenfield-Autoren-Skills abgenommen (S2) | Nutzer-Entscheidung; `8debb8c` | `2026-07/2026-07-22.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:feature-discover 15` — unveraendert aus der Vorsession: Idee #15 steht auf „In Arbeit" und wartet auf die Ausarbeitung. Die Vorpruefung, die der Idee-Text noch verlangt („VOR dem Bau gegen `project-health` pruefen"), ist erledigt und liegt im Session-Log vom 2026-07-27; ohne diesen Kontext beginnt die Discovery bei Null. Drei Entscheidungen dort: Zuschnitt (1:1-Pendant vs. schlanker Brownfield-Check), Traeger (eigener Skill vs. `project-init` vs. `build-check` — Letzteres waere Wiederbelebung eines ungenutzten Skills), Naming (`dtb:project-health` belegt den Namen). Alternative ohne Zielprojekt-Abhaengigkeit: `/dtb:idea-review` fortsetzen (9 offen, #27 ist ohne Bau entscheidbar).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
