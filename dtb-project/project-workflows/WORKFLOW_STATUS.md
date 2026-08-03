# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-31
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-31.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| plan-status-feld (#30) | Fertig zum Testen | 12/12 | Real abnehmen (Triage 10/10 behoben, distribuiert `5b29f81`) |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen — heute erneut produktiv gelaufen (`5b29f81`) |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) |
| Idee #29 (No-Loss-Gate) | In Arbeit (INBOX) | — | `/dtb:feature-discover` |

Kein Feature „In Arbeit". Anzeige-Felder (BACKLOG, `spec.md`) stimmen mit der Ableitung ueberein.
⚠ plan-status-feld: `review.md` traegt Gesamt-Verdikt REJECTED, die Triage ist abgeschlossen
(10 Fixed · 0 PENDING, seit `5b29f81` committet und distribuiert) — der Snapshot ist der Stand
VOR der Triage; die mechanische Handoff-Regel „REJECTED → `/dtb:implement`" greift hier nicht.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Entschieden** | **`lessons.md` bleibt ungetrackt** — entschieden 2026-07-18 (S5), Begruendung in `.gitignore:10-13`. Die Wiederaufnahme ist als **Idee #34** erfasst (Zwei-Maschinen-Divergenz belegt) — bis zu deren Entscheidung gilt der Beschluss unveraendert. **Diese Zeile bleibt der Wiedervorlage-Schutz.** `Applies-to: alle`-Lektionen leben versioniert in `skills/CLAUDE.md`; L7, L8 und L14 sind seit 2026-07-31 gehoben — der Hebe-Rueckstand ist damit abgebaut |
| **Notizen** | 2026-07-31: Der frische impl-review sollte nur ein veraltetes Verdikt aufloesen und fand einen **neuen** Blocker — zum dritten Mal in Folge entstand der Defekt nicht in der Mechanik, sondern zwischen zwei frisch geschriebenen Stellen. Zweiter Faden: Hash-Gleichheit ist kein Inhaltsnachweis — beide kit-sync-Laeufe wurden per Grep auf die Wirkstellen gegengeprueft (inkl. Negativ-Probe) |

---

## Offene Aufgaben

- [ ] **`/dtb:feature-discover` fuer #29** — Idee steht auf `In Arbeit`; zwei Praxisbelege aus dem 2026-07-31 als Discovery-Material
- [ ] `/dtb:commit-and-push` — `skills/CLAUDE.md` (Lektionen-Hebung) + `INBOX.md` + Checkpoint uncommittet
- [ ] **`/dtb:kit-sync sync` auf der anderen Maschine** — deren Lock steht auf `eda0ed1`, ihr fehlen 8 Skill-Updates
- [ ] Reale Abnahmen der 5 „Fertig zum Testen"-Features — Kontext: haengt am Zielprojekt pkp
- [ ] #31 auf den generischen Teil reduzieren — der konkrete Fall ist auf beiden Maschinen erledigt
- [ ] #28 (`.gitattributes`) entscheiden — vierfach belegt (zuletzt beim Commit `5b29f81`)
- [ ] `/dtb:idea-review` fuer die restlichen 11 offenen Ideen (#32 zwingend vor #27)
- [ ] `dtb:implement:157` auf Auswahlfrage umstellen, wenn sich Option A bewaehrt
- [ ] `workflow.config.yaml`/`ROADMAP.md` im Kit-Repo ausfuellen oder als Vorlage belassen?
- [ ] Zweiter blinder Lauf gegen die `project-init`-Fassung nach Schritt 8 — bewusst offen
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: aus S3 2026-07-28
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-31 | impl-review plan-status-feld: neuer Blocker gefunden + 10 Findings triagiert | 10 Fixed · 0 PENDING, distribuiert 41/41 | `5b29f81` |
| 2026-07-31 | L7/L8/L14 nach `skills/CLAUDE.md` gehoben; Maschine auf Kit-Stand (2 Sync-Laeufe) | Hebe-Rueckstand abgebaut; #31-Fall beidseitig vollzogen | `2026-07-31.md` |
| 2026-07-30 | plan-status-feld (#30): Kanon §7, Pfleger `plan-review`, gehaertete Leser | 12/12, 5 Commits, distribuiert | `bdb412e`…`8f3c3da` |
| 2026-07-30 | commit-and-push: Bestaetigung als blockierende Auswahlfrage (Abnahme-Befund) | Fix + Distribution; seither dreimal produktiv | `eda0ed1` |
| 2026-07-29 | Drei-Punkt-Diff in `workflow-resume` + `Applies-to: alle`-Lektionen als Autoring-Regeln | Fremdbefund verifiziert | `07d5107`, `4bb2b15` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:feature-discover` — Idee #29 (Session-Hygiene-/No-Loss-Gate) steht auf
`In Arbeit` und ist der bewusst gewaehlte naechste Strang. Vorher optional
`/dtb:commit-and-push` (2 Dateien + Checkpoint uncommittet).
**Empfehlung:** Neue Session mit `/clear`, dann `/dtb:workflow-resume`, danach obiger Befehl.
Kontext-Zeile **„Entschieden"** ist Wiedervorlage-Schutz (`lessons.md` — Wiederaufnahme laeuft
geordnet ueber Idee #34). Bei **Rechnerwechsel** zuerst `/dtb:kit-sync sync` — die andere Maschine
steht auf `eda0ed1`. Das REJECTED in `features/plan-status-feld/review.md` ist der Stand VOR der
Triage; **nicht** als Nacharbeits-Auftrag lesen.
