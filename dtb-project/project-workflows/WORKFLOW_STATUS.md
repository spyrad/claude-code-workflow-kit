# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-29 (Session 2)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-29.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-settings-seed | Behoben | 7/7 | Blinde Abnahme (Fix ist hier installiert, 41/41 synchron) |
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
| **Notizen** | 2026-07-29 (S2): Aufraeum-Session ohne Feature-Fortschritt. Der S1-Handoff beschrieb einen Maschinenstand, der nicht zutraf — Lock steht hier auf `7b6ba14` **mit** `localPath`, `project-init` ist byte-identisch installiert, `lessons.md` vollstaendig (L1-L10). Drei offene Punkte damit ohne Arbeit erledigt. `0130f2b` (Remote-Divergenz-Check in `workflow-resume`) gepusht; `kit-sync sync` hat einen „Lock veraltet"-Eintrag bereinigt → **41/41 synchron**. Merksatz: der neue Remote-Check deckt die **Git**-Seite ab, die **Distributions**-Seite (Lock, installierte Kopien) bleibt Sache eines `kit-sync check`. |

---

## Offene Aufgaben

- [ ] Blinde Abnahme des settings-seed-Fixes — Kontext: fand beim Vorgaenger-Bug einen Fehler im Fix; braucht Subagent-Freigabe
- [ ] Zwei `bug.md`-Kopfzeilen korrigieren — Kontext: behaupten „Fix noch nicht installiert", hier widerlegt; kein Skill pflegt diese Prosa
- [ ] `/dtb:idea-review` fortsetzen — Kontext: 11 Eintraege `Offen`, ohne Entscheidung abgebrochen; Vorschlag #30, dann #32
- [ ] Beide behobenen Bugs archivieren? — Kontext: archivreif, aber ihre `bug.md` tragen die Analysen
- [ ] `lessons.md` versionieren oder bewusst lokal lassen — Kontext: hier L1-L10, per `.gitignore:15` aber rechnerlokal
- [ ] #28 um den CRLF-Beleg ergaenzen — Kontext: 0 vs. 221 CRLF-Zeilen bei gleichen Blob-Hashes
- [ ] #31 auf den generischen Teil reduzieren — Kontext: `skills/CLAUDE.md` steht nicht mehr im Lock
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: deckt die Bestandsbereinigung ab
- [ ] Erfassen? `feature-start` setzt `bug.md`-Header auf „In Arbeit", §1.5 laesst dort nur *Pausiert* gelten
- [ ] Reale Abnahmen der 4 „Fertig zum Testen"-Features — Kontext: haengt am Zielprojekt pkp
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-29 | Remote-Divergenz-Check in `workflow-resume` (S2) | Schritt 3 prueft `fetch` + ahead/behind + Kollisionsrisiko; offener Punkt seit 2026-07-28 geschlossen | `0130f2b` |
| 2026-07-29 | Kit-Distribution bereinigt (S2) | „Lock veraltet" (Kopie am Skill vorbei aktualisiert) nachgezogen → 41/41 synchron | `2026-07/2026-07-29.md` |
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben (S1) | Seed-Mechanik auf Klasse umgestellt, Existenz-Gate gegen Ueberschreiben, 5/6 Tests gruen | `41ebf97` |
| 2026-07-29 | Drei S3-Folgebefunde sortiert (S1) | Nur einer war ein Bug; `CLAUDE.md`-Zielort war durch `9e2e9e3` bereits erledigt | `2026-07/2026-07-29.md` |
| 2026-07-28 | Kit-Bug `project-init-status-pfad` behoben (S3) | Statusdateien landen am Zielort; blinde Abnahme fand einen Fehler im Fix selbst | `9e2e9e3` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, in welcher Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** — offen — (mit `/dtb:workflow-next` bestimmen). Kein Skill-Befehl ableitbar:
alle vier Features `Y/Y` mit vorliegendem `review.md` (beide `REJECTED`-Verdikte im Dokument
aufgeloest), beide Bugs `Behoben`. Die konkret naechste Handlung ist **kein Skill**, sondern die
**blinde Abnahme von `41ebf97`** (Subagent, leeres Verzeichnis, nur die SKILL.md als Quelle,
Freigabe noetig) — beim Vorgaenger-Bug fand genau dieser Schritt einen Fehler im Fix.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her),
danach obige Abnahme. Der Resume-Lauf prueft ab jetzt selbst den Remote-Stand (`0130f2b`); die
**Distributions**-Seite deckt er nicht ab — bei Rechnerwechsel zusaetzlich `/dtb:kit-sync check`,
und daran denken, dass `lessons.md` und das Lock **nicht** mitwandern.
