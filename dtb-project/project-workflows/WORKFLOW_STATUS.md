# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-28 (Session 3)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-28.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-status-pfad | Behoben | 5/5 | Fix wirksam (`kit-sync` Lauf 2, Lock `9e2e9e3`) — optional `/dtb:archive` |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) → `/dtb:workflow-checkpoint` |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) → `/dtb:workflow-checkpoint` |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) → `/dtb:workflow-checkpoint` |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) → `/dtb:workflow-checkpoint` |
| Bug: project-init-settings-seed | Behoben | 7/7 | Blinde Abnahme (Subagent) → dann committen + `/dtb:kit-sync sync` |

**Laufende Arbeit:** Bug-Fix `project-init-settings-seed` umgesetzt (2026-07-29, S4) — `settings.json` wird jetzt nach `.claude/settings.json` verteilt, Seed-Mechanik von Einzelfall auf Klasse umgestellt (gemeinsame Quellenaufloesung + zwei Seeds), Existenz-Gate gegen Ueberschreiben. 5/6 Testschritte gruen (Bloecke aus der SKILL.md extrahiert und ausgefuehrt); offen: blinde Abnahme, Commit, `kit-sync`. Die vier Features bleiben unveraendert „Fertig zum Testen" (Abnahme haengt am Zielprojekt pkp).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-28 (S3): Kit-Bug aus einem Zielprojekt behoben — `project-init` legte `WORKFLOW_STATUS.md`/`BACKLOG.md` im Projekt-Root an (`SKILL.md:248` ohne Zielverzeichnis). Jede Pruefstufe korrigierte die vorherige: die Analyse widerlegte die `produces`-Hypothese der Erfassung, die blinde Abnahme fand einen Fehler im Fix (`CLAUDE.md` faelschlich aus dem Root ausgeschlossen). L10 erfasst (erste Lektion mit `Applies-to: alle`). kit-sync Lauf 1: 2 Updates + verwaiste `dtb-pitch-coach.md` entfernt, Lock 42 → 41. Drei neue Befunde aus dem blinden Lauf offen (s. Aufgaben). |

---

## Offene Aufgaben

- [ ] Bug archivieren? `features/project-init-status-pfad/` ist behoben und wirksam, also archivreif — sein `bug.md` traegt aber die Analyse zu den drei Folgebefunden unten
- [ ] Zweiten Bug erfassen: `settings.json` wird von `project-init` nicht verteilt — steht nicht im Body und nicht in `produces`, widerspricht dem Kit-CLAUDE.md (Befund des blinden Laufs)
- [ ] `CLAUDE.md` hat im `project-init`-Skill keinen Zielort — selber Defekt-Typ wie der behobene, harmloser
- [ ] `.gitkeep` nur in `input/`-Ordnern — `project-changelog/`, `project-testing/`, `features/` bleiben unversioniert; Skill sagt dazu nichts
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — deckt die Bestandsbereinigung ab, die bewusst nicht Teil des Bugfixes war
- [ ] Applies-to-Luecke im Lektionen-Prior — `debug-plan` sah bis L10 nie eine Lektion; L4/L5/L7 tragen Legacy-`code-review`
- [ ] `/dtb:idea-review` fortsetzen — 10 offene Ideen ohne #15 (naechstliegend #27, #25)
- [ ] `workflow-resume` um Remote-Divergenz-Check erweitern (Lehre aus der Parallelarbeit, S2)
- [ ] `git stash drop stash@{0}` — Sicherungsnetz gegenstandslos; `stash@{1}` (`ac81265`) bleibt
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features abbauen (haengt am Zielprojekt pkp)
- [ ] #31 entscheiden: `skills/CLAUDE.md` als Klasse A aufnehmen oder aus dem Lock streichen
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-28 | Kit-Bug `project-init-status-pfad` behoben (S3) | Statusdateien landen am Zielort; blinde Abnahme bestanden und fand zusaetzlich einen Fehler im Fix selbst | `9e2e9e3` |
| 2026-07-28 | kit-sync Lauf 1 + Lektion L10 (S3) | 2 Updates uebernommen, verwaiste `dtb-pitch-coach.md` entfernt (Lock 42 → 41); L10 als erste `alle`-Lektion | `2026-07/2026-07-28.md` |
| 2026-07-28 | #32 erfasst + #15 vertagt (S2) | `feature-discover`-Schwachpunkt mit 4-von-20-Bestandsbefund belegt; #15 als Ast-Entscheidung erkannt | `54fbade` |
| 2026-07-28 | #16 verworfen + Backlog-Sichtung (S1) | Mom-Test-Substanz in `opportunity-map` belegt | `df7232c` |
| 2026-07-27 | #15 vorgeprueft + build-check-Befund (S1) | Abgrenzung belegt, build-check als ungenutzt nachgewiesen | `2026-07/2026-07-27.md` |
| 2026-07-23 | Personas aus dem Kit entfernt (S1) | Halbzustand aufgeloest; Doku + tote #8-Verweise bereinigt | `7c3272a` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — braucht zusammenhaengenden Fokus. Nach dem Kettenbefund keine Skill-Frage, sondern eine **Ast-Entscheidung** (Brownfield-Zweig im Kit: ja/nein, in welcher Reihenfolge).
**Details:** Kontext vollstaendig im Idee-Text (`INBOX.md` #15); Analyse in `2026-07/2026-07-27.md` (S1) und `2026-07/2026-07-28.md` (S2)

---

## Handoff

**Naechster Befehl:** `/dtb:idea-review` — 10 offene Ideen sind nicht durchgegangen (#15 dabei ueberspringen, ist vertagt); naechstliegend **#27** (`grill-me` global bereits installiert, ohne Bau entscheidbar) und **#25** (Fach-Agenda, fehlendes Glied der Kette #13→#26→#25→#24). Kein Feature-Befehl ableitbar: alle vier Items `Y/Y`, reviewt, warten auf reale Abnahme in pkp — von dieser Maschine nicht moeglich. Der Bug-Zyklus ist abgeschlossen (Fix wirksam, Lock `9e2e9e3`); `/dtb:archive` waere reine Hygiene, kein offener Schritt.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl. **Bei Rechnerwechsel vorher `git fetch` + Divergenz pruefen** — am 2026-07-28 entstand so Doppelarbeit an #16.
