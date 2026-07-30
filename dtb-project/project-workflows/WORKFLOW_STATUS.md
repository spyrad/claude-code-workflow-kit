# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-30 (Checkpoint zu Session 5, deren Arbeit auf den 2026-07-29 faellt)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-29.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-settings-seed | Behoben | 8/8 | Blinde Abnahme durchgefuehrt (fand B1, behoben) — optional `/dtb:archive` |
| Bug: project-init-status-pfad | Behoben | 5/5 | Fix wirksam und installiert — optional `/dtb:archive` |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) |

Kein Feature „In Arbeit". Keine Konflikte zwischen Statusfeldern und Ableitung.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Entschieden** | **`lessons.md` bleibt ungetrackt** — entschieden 2026-07-18 (S5), Begruendung in `.gitignore:10-13`, ausdruecklich „nicht erneut als offene Frage aufmachen". Stand trotzdem in S1-S3 des 2026-07-29 wieder auf der Liste, weil kein Lese-Skill in `.gitignore` schaut. **Diese Zeile ist der Wiedervorlage-Schutz — nicht streichen.** Der reale Restschmerz (Prior 0 Treffer trotz passendem L10) ist seit S4 anders geloest: die drei `Applies-to: alle`-Lektionen L8/L10/L11 stehen als Autoring-Regeln in `skills/CLAUDE.md` (versioniert, reisen ueber Git mit) |
| **Notizen** | 2026-07-29 (S5): Skill-Defekte zeigen sich in **Zielprojekten**, nicht im Autoring-Repo — der Zwei-Punkt-diff fiel erst am divergierten Branch auf, im Kit-Repo (immer `0 0`) waere er unsichtbar geblieben. Zweitens Werkzeuglage dieser Maschine: `jq` fehlt, `python3` ist nur der Store-Stub → kit-sync-Auswertung als Skript in Datei-Form (`kitcheck.sh`), mit hartem Gate gegen die Leer-Seiten-Falle aus S4 (`GATE OK: Lock=41, Repo=41` vor jedem Vergleich) |

---

## Offene Aufgaben

- [ ] `/dtb:kit-sync sync` auf dem **zweiten Rechner** — dort traegt die installierte `workflow-resume`-Kopie noch die Zwei-Punkt-Fassung (Lock ist rechnerlokal)
- [ ] Lektion erfassen: Werkzeug-Fehlschlag ist kein Datenbefund (jetzt mit Praxisbeleg aus S5) + verbindliche Sequenzen nicht improvisieren + Shell-Syntax nicht ueber Werkzeuggrenzen mischen
- [ ] `workflow.config.yaml`/`ROADMAP.md` im Kit-Repo ausfuellen oder als Vorlage belassen? — Kontext: beide unausgefuellte Templates; betrifft jede `{config.project_name}`-Ausgabe, §5-Sync gegenstandslos
- [ ] Zweiter blinder Lauf gegen die `project-init`-Fassung nach Schritt 8 — bewusst offen
- [ ] Kopfzeile `project-init-status-pfad/bug.md` korrigieren — behauptet weiter „Fix nicht installiert"
- [ ] `/dtb:idea-review` fortsetzen — Kontext: 11 Eintraege `Offen`; Vorschlag #30, dann #32
- [ ] Beide behobenen Bugs archivieren? — Kontext: archivreif, aber ihre `bug.md` tragen die Analysen
- [ ] #28 um den CRLF-Beleg ergaenzen; #31 auf den generischen Teil reduzieren
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: aus S3 2026-07-28
- [ ] B4/B8/B9 zusammenfassen? — Kontext: Platzhalter-/Namensregeln in `project-init`; erst bei einem dritten Fall
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features — Kontext: haengt am Zielprojekt pkp
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-29 | Drei-Punkt-Diff in `workflow-resume` (S5) | Fremdbefund verifiziert (2 falsche Zeilen statt 1), Fix + Distribution 41/41 | `07d5107` |
| 2026-07-29 | `Applies-to: alle`-Lektionen als Autoring-Regeln verankert (S4) | L8/L10/L11 in `skills/CLAUDE.md`; `dtb:lesson` mit Hebe-Hinweis; `lessons.md`-Frage als entschieden geschlossen | `4bb2b15` |
| 2026-07-29 | Blinde Abnahme `41ebf97` + Fix-Schritt 8 (S3) | Regression B1 gefunden und behoben; Lehre: Bash-Bloecke an der Naht testen, nicht gebuendelt | `88d6087` |
| 2026-07-29 | Remote-Divergenz-Check in `workflow-resume` (S2) | Schritt 3 prueft `fetch` + ahead/behind + Kollisionsrisiko | `0130f2b` |
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben (S1) | Seed-Mechanik auf Klasse umgestellt, Existenz-Gate gegen Ueberschreiben | `41ebf97` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung** (Brownfield-Zweig im Kit: ja/nein, Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — dieser Checkpoint (Session-Log, diese Datei,
BACKLOG-Datum) ist uncommittet; `07d5107` ist gepusht, Distribution 41/41. Danach kein Befehl
eindeutig ableitbar (4 Features `Y/Y` **mit** `review.md`, beide Bugs `Behoben`) ausser
`/dtb:lesson` (Beleg liegt vor) und `/dtb:idea-review` (11 `Offen`); der Rest sind Entscheidungen.
**Empfehlung:** Neue Session mit `/clear`, dann `/dtb:workflow-resume`, danach obiger Befehl.
Kontext-Zeile **„Entschieden"** ist Wiedervorlage-Schutz (`lessons.md` nicht erneut aufmachen).
Bei **Rechnerwechsel** zuerst `/dtb:kit-sync sync` — der S5-Fix ist nur hier installiert.
