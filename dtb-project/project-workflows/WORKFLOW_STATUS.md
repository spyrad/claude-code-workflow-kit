# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-29 (Session 1)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-29.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-settings-seed | Behoben | 7/7 | Blinde Abnahme + `/dtb:kit-sync sync` (Fix hier noch nicht installiert) |
| Bug: project-init-status-pfad | Behoben | 5/5 | Fix wirksam (Lock `9e2e9e3`, andere Maschine) — optional `/dtb:archive` |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |

Kein Feature „In Arbeit". Keine Konflikte zwischen Statusfeldern und Ableitung.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-29 (S1): Zweiter Kit-Bug in Folge geschlossen (`41ebf97`) — `project-init` verteilte `settings.json` nicht, obwohl `kit-sync` beide Klasse-B-Seeds ausdruecklich an ihn delegiert. Seed-Mechanik von Einzelfall auf Klasse umgestellt; Kernaufwand war das Existenz-Gate (eine vorhandene `.claude/settings.json` nie ueberschreiben). Von den drei S3-Folgebefunden hielt nur einer als eigener Vorgang stand. **Diese Maschine hinkt hinterher:** Lock auf `7c3272a` (2026-07-23), `localPath` fehlt, `lessons.md` nur L1-L6 → Lektionen-Prior lief auf 0 Treffer. |

---

## Offene Aufgaben

- [ ] Blinde Abnahme des settings-seed-Fixes — Kontext: fand beim Vorgaenger-Bug einen Fehler im Fix; braucht Subagent-Freigabe
- [ ] `/dtb:kit-sync sync` + `localPath` im Lock nachtragen — Kontext: Kopie hier auf `7c3272a`; ohne `localPath` laufen beide Seeds in die Fehlermeldung
- [ ] `lessons.md` versionieren oder bewusst lokal lassen — Kontext: L7-L10 fehlen auf dieser Maschine, Prior wirkungslos
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: deckt die Bestandsbereinigung ab
- [ ] Erfassen? `feature-start` setzt `bug.md`-Header auf „In Arbeit", §1.5 laesst dort nur *Pausiert* gelten
- [ ] Beide behobenen Bugs archivieren? — Kontext: archivreif, aber ihre `bug.md` tragen die Analysen
- [ ] `/dtb:idea-review` fortsetzen — Kontext: 10 offene Ideen ohne #15; naechstliegend #27, #25
- [ ] `workflow-resume` um Remote-Divergenz-Check erweitern — Kontext: diesmal manuell gefahren (0/0)
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features — Kontext: haengt am Zielprojekt pkp
- [ ] #31 entscheiden: `skills/CLAUDE.md` als Klasse A aufnehmen oder aus dem Lock streichen
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben (S1) | Seed-Mechanik auf Klasse umgestellt, Existenz-Gate gegen Ueberschreiben, 5/6 Tests gruen | `41ebf97` |
| 2026-07-29 | Drei S3-Folgebefunde sortiert (S1) | Nur einer war ein Bug; `CLAUDE.md`-Zielort war durch `9e2e9e3` bereits erledigt | `2026-07/2026-07-29.md` |
| 2026-07-28 | Kit-Bug `project-init-status-pfad` behoben (S3) | Statusdateien landen am Zielort; blinde Abnahme fand einen Fehler im Fix selbst | `9e2e9e3` |
| 2026-07-28 | kit-sync Lauf 1 + Lektion L10 (S3) | 2 Updates, verwaiste `dtb-pitch-coach.md` entfernt (Lock 42 → 41) | `2026-07/2026-07-28.md` |
| 2026-07-28 | #32 erfasst + #15 vertagt (S2) | `feature-discover`-Schwachpunkt mit 4-von-20-Bestandsbefund belegt | `54fbade` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, in welcher Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:kit-sync sync` — macht den Fix `41ebf97` auf dieser Maschine wirksam
(installierte Kopie steht auf `7c3272a` / 2026-07-23). **Davor** die blinde Abnahme des Fixes
(Subagent, leeres Verzeichnis, nur die SKILL.md — kein Skill-Befehl, braucht Freigabe); beim
Vorgaenger-Bug fand genau dieser Schritt einen Fehler im Fix. **Danach** `localPath` im Lock
nachtragen, sonst bleibt `/dtb:project-init` hier unbenutzbar. Kein Feature-Befehl ableitbar:
alle vier Features `Y/Y`, reviewt, warten auf reale Abnahme in pkp.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her),
danach obigen Befehl. **Bei Rechnerwechsel vorher `git fetch` + Divergenz pruefen** — und daran
denken, dass `lessons.md` und der Lock **nicht** mitwandern.
