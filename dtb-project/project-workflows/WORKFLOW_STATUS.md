# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-29 (Session 4)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-29.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-settings-seed | Behoben | 8/8 | Blinde Abnahme durchgefuehrt (fand B1, behoben) — optional `/dtb:archive` |
| Bug: project-init-status-pfad | Behoben | 5/5 | Fix wirksam und installiert — optional `/dtb:archive` |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) |
| commit-and-push | Fertig zum Testen | 10/10 | Multi-Repo-Zweig in pkp abnehmen (Kern via `791027d` belegt) |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) |

Kein Feature „In Arbeit". Keine Konflikte zwischen Statusfeldern und Ableitung.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Entschieden** | **`lessons.md` bleibt ungetrackt** — entschieden 2026-07-18 (S5), Begruendung in `.gitignore:10-13`, ausdruecklich „nicht erneut als offene Frage aufmachen". Stand trotzdem in S1-S3 des 2026-07-29 wieder auf der Liste, weil kein Lese-Skill in `.gitignore` schaut. **Diese Zeile ist der Wiedervorlage-Schutz — nicht streichen.** Der reale Restschmerz (Prior 0 Treffer trotz passendem L10) ist am 2026-07-29 (S4) anders geloest: die drei `Applies-to: alle`-Lektionen L8/L10/L11 sind als Autoring-Regeln in `skills/CLAUDE.md` verankert (versioniert, reisen ueber Git mit) |
| **Notizen** | 2026-07-29 (S3): Blinde Abnahme von `41ebf97` **nicht bestanden** — fand B1 (`$KIT` ueberlebt den Blockwechsel nicht, jeder Bash-Aufruf ist eine eigene Shell). Regression, belegt gegen `4ab0069`: vor dem Fix stand die Aufloesung im selben Block wie das `cp`, der Fix hat den vorher funktionierenden Regel-Seed mit gebrochen. Behoben als Fix-Schritt 8 (+ B3/B11), `88d6087` gepusht, `kit-sync sync` → 41/41. **Merksatz:** der Testplan war 5/6 gruen, weil er die Bash-Bloecke **gebuendelt** ausfuehrte — der Defekt sass an der **Naht zwischen** den Bloecken. Bloecke, die Variablen teilen, einzeln in frischer Shell pruefen. |

---

## Offene Aufgaben

- [ ] Zweiter blinder Lauf gegen die Fassung nach Schritt 8 — Kontext: bewusst offen, B1 selbst ist haerter belegt
- [ ] Kopfzeile `project-init-status-pfad/bug.md` korrigieren — Kontext: behauptet weiter „Fix nicht installiert"; Schwester-Datei ist erledigt
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
| 2026-07-29 | Blinde Abnahme `41ebf97` + Fix-Schritt 8 (S3) | Regression B1 gefunden und behoben; Lehre: Bash-Bloecke an der Naht testen, nicht gebuendelt | `88d6087` |
| 2026-07-29 | Remote-Divergenz-Check in `workflow-resume` (S2) | Schritt 3 prueft `fetch` + ahead/behind + Kollisionsrisiko | `0130f2b` |
| 2026-07-29 | Kit-Distribution bereinigt (S2) | „Lock veraltet" nachgezogen → 41/41 synchron | `2026-07/2026-07-29.md` |
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben (S1) | Seed-Mechanik auf Klasse umgestellt, Existenz-Gate gegen Ueberschreiben | `41ebf97` |
| 2026-07-28 | Kit-Bug `project-init-status-pfad` behoben (S3) | Statusdateien landen am Zielort; blinde Abnahme fand einen Fehler im Fix selbst | `9e2e9e3` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, in welcher Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` (Aenderungen aus S4 liegen uncommittet vor:
`skills/CLAUDE.md` + diese Datei). Danach kein Befehl ableitbar: alle vier Features `Y/Y` mit
vorliegendem `review.md`, beide Bugs `Behoben`. Die zwei verbliebenen naechstliegenden Handlungen
sind **keine** Skill-Befehle, sondern Entscheidungen: die beiden behobenen Bugs archivieren oder
ihre Analysen liegen lassen; `/dtb:idea-review` mit Kopf fortsetzen (11 Eintraege `Offen`).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her),
danach obigen Befehl. Beachten: die Blocknaht-Lehre steht seit S4 **versioniert** in
`skills/CLAUDE.md` („Bash-Bloecke sind eigene Shells") und reist damit ueber Git mit; `lessons.md`
selbst bleibt per `.gitignore:10-13` bewusst rechnerlokal (entschieden 2026-07-18 — siehe
Kontext-Zeile „Entschieden", nicht erneut aufmachen). Der Resume-Lauf prueft die **Git**-Seite
selbst; die **Distributions**-Seite braucht bei Rechnerwechsel zusaetzlich `/dtb:kit-sync check` —
`skills/CLAUDE.md` ist allerdings **nicht** Klasse A und wird von `kit-sync` nicht verteilt.
