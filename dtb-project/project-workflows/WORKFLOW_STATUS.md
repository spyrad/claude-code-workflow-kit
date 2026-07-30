# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-30
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-30.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| plan-status-feld (#30) | Fertig zum Testen | 12/12 | Triage-Fixes committen, dann kit-sync + reale Abnahme |
| meeting-dump (#24) | Fertig zum Testen | 10/10 | Real abnehmen (echtes Meeting im Zielprojekt) |
| commit-and-push | Fertig zum Testen | 10/10 | Real abnehmen — Nacharbeit `eda0ed1` (Auswahlfrage) ist eingespielt |
| open-question | Fertig zum Testen | 9/9 | Real abnehmen (erster echter Fach-Frage-Einsatz) |
| Fachfragen-Erfassung | Fertig zum Testen | 8/8 | Real abnehmen (naechste feature-discovery nutzt `[Fach]`) |

Kein Feature „In Arbeit". Keine Konflikte zwischen Statusfeldern und Ableitung.
`features/plan-status-feld/review.md` traegt Gesamt-Verdikt REJECTED — das ist der Stand VOR der
Triage (8 Fixed · 2 Skipped · 0 PENDING, beide Blocker behoben); ein frisches Review nach dem
Commit wuerde neu vergeben.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Entschieden** | **`lessons.md` bleibt ungetrackt** — entschieden 2026-07-18 (S5), Begruendung in `.gitignore:10-13`. Die Wiederaufnahme ist jetzt als **Idee #34** erfasst (neues Faktum: belegte Zwei-Maschinen-Divergenz L1–L11 vs. L1–L7) — bis zu deren Entscheidung gilt der Beschluss unveraendert weiter. **Diese Zeile bleibt der Wiedervorlage-Schutz.** `Applies-to: alle`-Lektionen leben als Autoring-Regeln versioniert in `skills/CLAUDE.md`; L7 und L8 warten noch aufs Heben |
| **Notizen** | 2026-07-30 (S2): Idee #30 in einer Session komplett durch die Pipeline. Das Kit hat sich zweimal selbst korrigiert — `plan-review` fand 3 WARNs im eigenen Plan, `impl-review` danach 2 echte Blocker, die erst beim Umsetzen entstanden waren (Parse-Regel-Luecke, nicht entscheidbare Konfliktklausel). Ohne die Reviews waeren beide distribuiert worden. Dritter Gate-Beleg: Die Push-Pruefung vor kit-sync verhinderte einen Lauf, der „alles synchron" gemeldet und nichts verteilt haette |

---

## Offene Aufgaben

- [ ] **`/dtb:commit-and-push`** — Triage-Fixes (5 Skills + Regel-Datei), `review.md`, Register, Session-Log sind uncommittet
- [ ] **Danach erneut `/dtb:kit-sync sync`** — die Triage fasste 5 Skill-Dateien an, darunter `project-health` und `backlog-status` (vorher nicht im Scope)
- [ ] **`/dtb:kit-sync sync` auf der anderen Maschine** — deren Lock steht auf `07d5107`, ihr fehlen inzwischen 6+ Skill-Updates
- [ ] Optional: frisches `/dtb:impl-review plan-status-feld` nach dem Commit (Snapshot-Verdikt ist vor-Triage)
- [ ] L7 **und L8** in `skills/CLAUDE.md` heben (Konvention, `Applies-to`-relevant)
- [ ] #28 ist dreifach belegt (Staging-Warnungen, Lock-Diff) — `.gitattributes` entscheiden
- [ ] `/dtb:idea-review` fuer die restlichen 12 offenen Ideen — Triage vom 2026-07-30 liegt vor (#32 zwingend vor #27)
- [ ] `dtb:implement:157` auf Auswahlfrage umstellen, wenn sich Option A (`eda0ed1`) bewaehrt
- [ ] `workflow.config.yaml`/`ROADMAP.md` im Kit-Repo ausfuellen oder als Vorlage belassen?
- [ ] Zweiter blinder Lauf gegen die `project-init`-Fassung nach Schritt 8 — bewusst offen
- [ ] `project-health`-Check „Artefakt am falschen Ort" erwaegen — Kontext: aus S3 2026-07-28
- [ ] B4/B8/B9 zusammenfassen? — nur bei einem dritten Fall
- [ ] Reale Abnahmen der 5 „Fertig zum Testen"-Features — haengt am Zielprojekt pkp
- [ ] pkp intern committen: `UI.md` + `project-design/`-Tokens (separates Repo)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-30 | plan-status-feld (#30): Kopf-Statusfeld bekommt Kanon (§7), Pfleger (plan-review) und gehaertete Leser | 12/12, 4 Phasen-Commits, impl-review mit 8 Fixes | `bdb412e`…`bf87fd2` |
| 2026-07-30 | commit-and-push: Bestaetigung als blockierende Auswahlfrage (Abnahme-Befund aus echter Nutzung) | Fix + spec + Distribution 41/41 | `eda0ed1` |
| 2026-07-30 | Beide project-init-Bugs + Idee #16 archiviert; Rechner „zuhause" via kit-sync auf Kit-Stand | Beide Maschinen synchron (bis S2) | `4641956` |
| 2026-07-29 | Drei-Punkt-Diff in `workflow-resume` (S5) + `Applies-to: alle`-Lektionen als Autoring-Regeln (S4) | Fremdbefund verifiziert; L8/L10/L11 in `skills/CLAUDE.md` | `07d5107`, `4bb2b15` |
| 2026-07-29 | Kit-Bug `project-init-settings-seed` behoben, blinde Abnahme fand Regression B1 | Seed-Mechanik auf Klasse umgestellt + Blocknaht-Fix | `41ebf97`, `88d6087` |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant

**Status:** Bewusst vertagt (2026-07-28, S2) — keine Skill-Frage, sondern eine **Ast-Entscheidung**
(Brownfield-Zweig im Kit: ja/nein, Reihenfolge); braucht zusammenhaengenden Fokus.
**Details:** `INBOX.md` #15; Analyse in `2026-07/2026-07-27.md` und `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — die Triage-Fixes aus dem impl-review (5 Skills +
`DERIVED_STATE_RULES.md`), `review.md`, die Register und dieser Session-Log sind uncommittet.
**Direkt danach `/dtb:kit-sync sync`** (die installierten Kopien weichen durch die Triage wieder ab).
**Empfehlung:** Neue Session mit `/clear`, dann `/dtb:workflow-resume`, danach obige Befehle.
Kontext-Zeile **„Entschieden"** ist Wiedervorlage-Schutz (`lessons.md` — Wiederaufnahme laeuft
geordnet ueber Idee #34). Bei **Rechnerwechsel** zuerst `/dtb:kit-sync sync` — die andere Maschine
steht auf `07d5107`.
