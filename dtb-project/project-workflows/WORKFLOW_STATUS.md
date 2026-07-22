# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-22 (Session 1)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-22.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| Verifikations-Gate | Abgenommen | 18/18 | Abgeschlossen → `/dtb:archive` (optional) |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Opportunity-Map | Abgenommen | 11/11 | Abgeschlossen → `/dtb:archive` (optional) |
| Greenfield-Autoren-Skills | Abgenommen | 14/14 | Abgeschlossen → `/dtb:archive` (optional) |

Kein Feature „In Arbeit" (alle `## Progress` vollstaendig). Diese Session: Konventions-/Doku-Aenderung ausserhalb der Feature-Kette (kein Change-Ordner).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-22 (S1): DtB-Designsprache aus pkp extrahiert (antd v6, IBCS-Charts, Inter, 4/8-Raster) → Artefakte **intern in pkp** (`project-rules/UI.md` + `project-design/`-Tokens). Kit erhielt nur die **leere Konvention** (`project-design`-Bucket in project-init + Doku), keine Werte. Kit + pkp uncommitted. |

---

## Offene Aufgaben

- [ ] Kit-Aenderung committen: `docs(project-init): project-design-Bucket + UI.md-Konvention`
- [ ] pkp committen (intern): `UI.md` + `project-design/`-Tokens → `/dtb:commit-and-push`
- [ ] Folge-Idee: `generate-rules ui` koennte Tokens nach `project-design/` emittieren/referenzieren (ggf. `/dtb:idea`)
- [ ] `/dtb:idea-review` fortsetzen — 9 offene Ideen (zweimal unterbrochen)
- [ ] meeting-dump real abnehmen; commit-and-push-Vollabnahme (pkp Multi-Repo); #23 (Multi-Repo-Begriff)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-22 | DtB-Designsprache aus pkp extrahiert + Kit-Konvention | pkp: `UI.md`+Tokens (intern); Kit: `project-design`-Bucket + Doku | `2026-07/2026-07-22.md` |
| 2026-07-21 | meeting-dump (#24) gebaut + reviewt | 10/10, impl-review 4 Fixed, P1–P3 `317a959`/`757cb7f`/`05c1ca7` | `features/meeting-dump/review.md` |
| 2026-07-20 | commit-and-push Kern-Routine abgenommen (Single-Repo) | via `791027d`, Multi-Repo offen | `2026-07/2026-07-20.md` (S2) |
| 2026-07-20 | Verifikations-Gate (#19) real abgenommen | pkp-Lauf `f39af15`, Gate biss bei 1.2 | `2026-07/2026-07-20.md` (S1) |
| 2026-07-19 | open-question (#26) gebaut + reviewt + verteilt | 9/9, impl-review 9 Fixed, live `b7c0e0b`/`d399be8` | `features/open-question/review.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — konkrete uncommittete Design-Arbeit in **zwei** Repos sichern (Kit: `CLAUDE.md` + `project-init`; pkp intern: `UI.md` + `project-design/`). Danach kein Feature „In Arbeit" → offener Faden `/dtb:idea-review` (9 Ideen, zweimal unterbrochen) bzw. `/dtb:workflow-next`. Parallele manuelle Spur: meeting-dump in echtem Meeting durchspielen → Checkpoint mit Abnahme-Beleg.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
