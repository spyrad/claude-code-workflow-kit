# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-30
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-30.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| plan-status-feld (#30) | Fertig zum Testen | 12/12 | Frisches `/dtb:impl-review` (Snapshot-Verdikt ist vor-Triage), dann reale Abnahme |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen — heute zweimal produktiv gelaufen (`eda0ed1`, `8f3c3da`) |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) |

Kein Feature „In Arbeit". Keine Konflikte zwischen Statusfeldern und Ableitung.
`features/plan-status-feld/review.md` traegt Gesamt-Verdikt REJECTED — Stand VOR der Triage
(8 Fixed · 2 Skipped · 0 PENDING, beide Blocker behoben und seit `8f3c3da` distribuiert).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Entschieden** | **`lessons.md` bleibt ungetrackt** — entschieden 2026-07-18 (S5), Begruendung in `.gitignore:10-13`. Die Wiederaufnahme ist als **Idee #34** erfasst (neues Faktum: belegte Zwei-Maschinen-Divergenz L1–L11 vs. L1–L8) — bis zu deren Entscheidung gilt der Beschluss unveraendert. **Diese Zeile bleibt der Wiedervorlage-Schutz.** `Applies-to: alle`-Lektionen leben versioniert in `skills/CLAUDE.md`; L7 und L8 warten aufs Heben |
| **Notizen** | 2026-07-30: Idee #30 an einem Tag komplett durch die Pipeline (Triage → Discovery → Spec → Plan → Review → Umsetzung → Distribution → impl-review → Nacharbeit → Distribution). **Drei Gates haben je einen echten Fehler gefangen:** `plan-review` 3 WARNs im eigenen Plan, `impl-review` 2 Blocker aus frisch geschriebenem Text, und die Push-Pruefung vor kit-sync einen Lauf, der „alles synchron" gemeldet und nichts verteilt haette. Distribution auf dieser Maschine 41/41 @ `8f3c3da`, inhaltlich gegengeprueft (inkl. Negativ-Probe) |

---

## Offene Aufgaben

- [ ] **`/dtb:kit-sync sync` auf der anderen Maschine** — deren Lock steht auf `07d5107`, ihr fehlen 7 Skill-Updates
- [ ] Frisches `/dtb:impl-review plan-status-feld` — loest das REJECTED im Snapshot auf (Fixes sind seit `8f3c3da` drin)
- [ ] `/dtb:idea-review` fuer die 12 offenen Ideen — Triage vom 2026-07-30 liegt vor (#32 zwingend vor #27)
- [ ] Reale Abnahmen der 5 „Fertig zum Testen"-Features — Kontext: haengt am Zielprojekt pkp
- [ ] L7 **und L8** in `skills/CLAUDE.md` heben (Konvention, `Applies-to`-relevant)
- [ ] #28 (`.gitattributes`) entscheiden — dreifach belegt (Staging-Warnungen, Lock-Diff)
- [ ] `dtb:implement:157` auf Auswahlfrage umstellen, wenn sich Option A (`eda0ed1`) bewaehrt
- [ ] `workflow.config.yaml`/`ROADMAP.md` im Kit-Repo ausfuellen oder als Vorlage belassen?
- [ ] Zweiter blinder Lauf gegen die `project-init`-Fassung nach Schritt 8 — bewusst offen
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: aus S3 2026-07-28
- [ ] B4/B8/B9 zusammenfassen? — nur bei einem dritten Fall
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-30 | plan-status-feld (#30): Kanon §7, Pfleger `plan-review`, gehaertete Leser, impl-review mit 8 Fixes | 12/12, 5 Commits, distribuiert 41/41 | `bdb412e`…`8f3c3da` |
| 2026-07-30 | commit-and-push: Bestaetigung als blockierende Auswahlfrage (Abnahme-Befund) | Fix + Distribution; danach zweimal produktiv genutzt | `eda0ed1` |
| 2026-07-30 | Beide project-init-Bugs + Idee #16 archiviert; Rechner „zuhause" auf Kit-Stand | Maschine synchron | `4641956` |
| 2026-07-29 | Drei-Punkt-Diff in `workflow-resume` + `Applies-to: alle`-Lektionen als Autoring-Regeln | Fremdbefund verifiziert; L8/L10/L11 in `skills/CLAUDE.md` | `07d5107`, `4bb2b15` |
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben, blinde Abnahme fand Regression B1 | Seed-Mechanik auf Klasse umgestellt | `41ebf97`, `88d6087` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:impl-review plan-status-feld` — ein frischer Lauf vergibt das Verdikt
neu; der gespeicherte Snapshot steht auf REJECTED, obwohl die Nacharbeit erfolgt und distribuiert
ist. Alternativ direkt `/dtb:idea-review` (12 offene Ideen, Triage liegt vor, #32 vor #27).
**Empfehlung:** Neue Session mit `/clear`, dann `/dtb:workflow-resume`, danach obiger Befehl.
Kontext-Zeile **„Entschieden"** ist Wiedervorlage-Schutz (`lessons.md` — Wiederaufnahme laeuft
geordnet ueber Idee #34). Bei **Rechnerwechsel** zuerst `/dtb:kit-sync sync` — die andere Maschine
steht auf `07d5107`. Arbeitsbaum bei Session-Ende clean @ `8f3c3da`; nur dieser Checkpoint
(Session-Log + diese Datei) ist uncommittet.
