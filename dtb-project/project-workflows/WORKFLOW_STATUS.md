# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-11-27
**Letzter Session-Log:** `dtb-project/project-changelog/2026-11/2026-11-27.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|

Kein aktives Feature.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-11-27: #215 plan-review-subagenten per Pane umgesetzt, gemergt (`5381a71`), kit-sync 7/7, abgenommen, Arbeitsplatz abgebaut, archiviert 2026-11-27; Push-Kollision mit dem Arbeitsrechner per Rebase gelöst (L150, #226); #216 läuft im Tab `t22` (Privatrechner). PKP-Durchlaufzeiten wiederholt (`~/.claude/analysen/pkp-durchlaufzeiten/lauf-2026-11-27/vergleich.md`), Dashboard-Seite um den Vergleich ergänzt — Abschluss jetzt teuerste Phase (24,0 → 34,7 h), stützt #199. Reihenfolge: #216 → #219 (nach #199-Merge), siehe #221. #199 hat einen Worktree auf dem anderen Rechner |

---

## Offene Aufgaben

- [ ] **`/dtb:lesson-curate`** — Kontext: `lessons.md` hat nach L150/L151 80 KB erreicht (Soft-Limit 80 KB) (seit 2026-11-27)
- [ ] **#215: 4 Nits unter dem Cap aus impl-review** — Kontext: general-purpose statt Explore begründen, Form des Lektionen-Slots, Warte-Regel harness-neutral, Begriffe Agent/Rolle/Subagent; optional erneutes `/dtb:impl-review` (seit 2026-11-27)
- [ ] **#215: offene Runde-4-Fragen aus plan-review** — Kontext: Subagent-Typ `Plan` statt `general-purpose`? Zahl der Läufe in der 🤖-Zeile zeigen? (seit 2026-11-27)
- [ ] **#215: Rückfall-Pfade „Agent-Werkzeug fehlt“ und „Rückgabe unbrauchbar“ beobachten** — Kontext: im Probelauf nicht herbeiführbar, ungeprüft; nächster echter `/dtb:plan-review`-Lauf (seit 2026-11-27)
- [ ] **PKP-Durchlaufzeiten-Seite: Vergleichsabschnitt im Browser ansehen** — Kontext: Abschnitt „Zweiter Monat im Vergleich" auf https://claude.ai/artifact/AA1DVkgDV1WXR2PsjhWUpn; die Seitenprüfung des Dashboards meldete sich nicht, Rechnungen offline geprüft (seit 2026-11-27)
- [ ] **INBOX-BEFUNDE #46, #58 Fall (1), #88, #195 abräumen** — Kontext: durch skill-lint erledigt (Gegenkanten-Regel, greenfield-prd.after, Stage-Tabelle, Bash in Teil-Guard-Skills); beim nächsten `/dtb:idea-triage` (seit 2026-11-26)
- [ ] **mega.dev-Reihenfolge #221: #216 CLAUDE.md ohne Codebase-Karte läuft im Tab `t22`** — Kontext: beim Merge auf `CLAUDE.md`-Konflikt mit #215 achten (Zweig von `8940abb`); danach #219 erst nach dem Merge von #199 (seit 2026-11-26)
- [ ] **#217 skill-beschreibungen: Auslöse-Probe in frischer Session** — Kontext: „was steht an", „wo steckt was", „offene Features", „Projektstand als Seite" → wählt Claude den passenden Status-Skill? (offener Punkt in archive/skill-beschreibungen/spec.md) (seit 2026-11-26)
- [ ] **#200 herdr-app-umstellung: Zweig `feature/herdr-app-umstellung` auf GitHub und lokal löschen** — Kontext: archiviert 2026-11-23; am 2026-11-26 geprüft: `origin/feature/herdr-app-umstellung` und der lokale Zweig existieren beide noch (seit 2026-11-12) ⏳
- [ ] **#199 checkpoint-auto-commit: Umsetzung nach der Nachmessung (bis 2026-12-02)** — Kontext: `/dtb:implement Checkpoint Auto-Commit` im Tab `checkpoint-auto-commit`; Plan Reviewed 0/18, Schritt 4.5 (kit-sync-Nachweis) erst nach Merge und Push; Messung 2026-11-27: Checkpoint → commit-and-push 35× (#224) (seit 2026-11-13) ⏳
- [ ] **#199 checkpoint-auto-commit: übersprungene globale Updates beim Merge nachtragen** — Kontext: INBOX #199 → Ausgearbeitet mit Links auf discovery/spec/plan; BACKLOG-Zeile „Checkpoint Auto-Commit · Geplant · Mittel"; vorher zeigen die Links ins Leere (#114, #131) (seit 2026-11-13) ⏳
- [ ] **#200 herdr-app-umstellung: restliche Review-Fixes im nächsten echten Worker-/Pane-Lauf beobachten** — Kontext: F1 und F5 belegt (`archive/herdr-app-umstellung/probe.md` → Nachtrag); `pane-start` lief am 2026-11-13 (#199) und 2026-11-26 (#217) sauber, F2, F3, F4, F9, F10 dort nicht einzeln geprüft; Schließen eines Worker-Tabs mit laufender Claude-Session offen (seit 2026-11-12) ⏳
- [ ] **herdr-app-umstellung: 5 Review-Findings unter dem Cap** — Kontext: am Ende von `archive/herdr-app-umstellung/review.md`, alles Kleinigkeiten; dazu F6 (Heredoc, L38) übersprungen (seit 2026-11-12) ⏳
- [ ] **INBOX #112 (Checkliste vor dem Feature-Start) auf `dtb:implement` Schritt 1 umhängen** — Kontext: seit #179 startet `feature-start` keine Features mehr; beim nächsten `/dtb:idea-review` umformulieren (Nachtrag 2 zum Hand-off #179) (seit 2026-11-10) ⏳
- [ ] **#178 plan-in-einem-befehl: ersten echten `/dtb:feature-plan`-Lauf beobachten** — Kontext: erster Lauf mit der neuen Fassung am 2026-11-13 in der Pane von #199 (Struktur-Check 5/5, Spec und Plan in einem Lauf); Backlog-Zweig dort planmäßig übersprungen (Worktree), Fehlerpfad „impl-plan nicht installiert" weiter ungefahren — den nächsten Lauf im Haupt-Checkout ansehen (seit 2026-11-09) ⏳
- [ ] **#22 seed-skew-aktiv-melden: fetch-Teil der Abhilfe-Befehle im ersten echten Bestandsprojekt-Lauf beobachten** — Kontext: im Pane bewusst ungetestet (Kit-Klon nicht angefasst), show/diff/mv an einer Kopie gruen; naechster `kit-sync check` in einem Zielprojekt mit altem Seed (z. B. PKP) — seit #179 weicht der Seed (§7.3) überall ab (seit 2026-11-09) ⏳
- [ ] **checkpoint-ohne-rueckfragen: Nachbesserung Erfassungs-Block beim ersten Checkpoint nach dem Merge prüfen** — Kontext: Probelauf-Befund 1 (Alters-Zeile nicht mehr unter „Erfasst:"); erster Echtlauf mit Funden und ⏳ ist der Checkpoint 2026-11-06 — dessen Bestätigung ansehen; die Nachmessung 2026-11-20 hat das nicht geprüft (seit 2026-11-03) ⏳
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — in Abnahme 4.2 (Wegwerf-Change) A1, A2, A4 gesehen, A3 nicht; zählt erst an einem echten Change; 2026-11-13 (#199) und 2026-11-26 (#217) nur „Ende", kein Wechsel (seit 2026-10-22 · behalten 2026-10-29) ⏳
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-11-03) ⏳
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-29) ⏳
- [ ] **`/dtb:idea-triage`** — Kontext: 135 ungesichtet, mit Vorsortierung; #54/#70 sind korrekt escapt (geprüft 2026-11-06) (seit ≤2026-09-09 · behalten 2026-10-29) ⏳
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-29) ⏳

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-11-27 | #215 plan-review-subagenten per Pane (Fast-Track) umgesetzt, abgenommen, gemergt, kit-sync | Rollen als isolierte Subagenten, Modell je Rolle (`plan_review.modelle`), Probelauf 4/4 isoliert; impl-review 10× FIXED; L147–L149 | `2026-11/2026-11-27.md` |
| 2026-11-27 | PKP-Durchlaufzeiten wiederholt, Dashboard um den Vergleich ergänzt | 28.10.–27.11. gegen 28.09.–28.10.: 17 statt 13 Changes fertig, Fast-Track 0,2 statt 0,7 Tage, Abschluss 34,7 statt 24,0 h, offene Auswahlfragen 9,2 statt 4,6 h; L146, #223–#225 | `2026-11/2026-11-27.md` |
| 2026-11-27 | Arbeitsrechner nachgezogen: Pull + kit-sync | Fast-Forward auf `8940abb`, kit-sync 8/8 (skill-lint) nach 7/7 am Vorabend, Lock auf `8940abb`; #222 | `2026-11/2026-11-27.md` |
| 2026-11-26 | #214 skill-lint per Pane (Fast-Track) umgesetzt, abgenommen, gemergt, kit-sync | `scripts/lint-skills.py` + 37 Selbsttests + CI `lint-skills.yml` (erster Lauf grün), Check 8 ruft das Skript, Gegenkanten-Regel; impl-review 10× FIXED; L143–L145 | `2026-11/2026-11-26.md` |
| 2026-11-26 | #217 skill-beschreibungen (mit #218) per Pane umgesetzt, abgenommen, gemergt, kit-sync, archiviert | 7 Beschreibungen ≤ 338 Zeichen mit „Not for"-Abgrenzung, Regel in `skills/CLAUDE.md`, impl-review 8× FIXED, kit-sync 7/7; #214–#219 aus mega.dev übernommen; L141, L142, #220, #221 | `2026-11/2026-11-26.md` |
| 2026-11-23 | #200 herdr-app-umstellung, #177 checkpoint-schneller, #173 checkpoint-ohne-rueckfragen archiviert | drei Ordner nach `archive/`, Archiv-Log ergänzt; kein aktives Feature mehr im Haupt-Checkout | `2026-11/2026-11-23.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 135 ungesichtet → /dtb:idea-triage
