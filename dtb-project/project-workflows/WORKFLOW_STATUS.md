# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-11-12
**Letzter Session-Log:** `dtb-project/project-changelog/2026-11/2026-11-12.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| checkpoint-ohne-rueckfragen | Fertig zum Testen | 8/8 | gemeinsame Nachmessung bis 2026-12-02, dann Abnahme |
| checkpoint-schneller | Fertig zum Testen | 6/6 | gemeinsame Nachmessung bis 2026-12-02, dann Abnahme |
| herdr-app-umstellung | Fertig zum Testen | 19/19 | Review-Fixes in der App gegenprüfen, dann Abnahme und Merge |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-11-12: #200 herdr-app-umstellung komplett (Phasen 1–4: `0378ebe`, `5da0035`, `c188566`, `851b4b9`), alle drei Abnahme-Läufe in `features/herdr-app-umstellung/probe.md`; impl-review NEEDS ATTENTION, Triage 9 FIXED · 1 SKIPPED (`1818764`), Fixes in der App ungetestet; Stand liegt bis zum Merge nur auf `feature/herdr-app-umstellung` im Haupt-Checkout (#204); nach Merge und Push `/dtb:kit-sync sync` — bis dahin laufen unter `~/.claude/` die alten Skills (L133); #199 nach der Nachmessung; #180 als nächstes Fast-Track-Thema |

---

## Offene Aufgaben

- [ ] **#200 herdr-app-umstellung: Abnahme, Merge, Push, danach `/dtb:kit-sync sync`** — Kontext: 19/19, Abnahme-Belege in `probe.md`, impl-review erledigt (`review.md`); erst pushen, dann syncen (L39) (seit 2026-11-12)
- [ ] **#200 herdr-app-umstellung: Review-Fixes in der App gegenprüfen** — Kontext: vor allem der neue Filter im Block „Tab schließen" (`"parent":"$HC_TERMINAL_ID"`) im Worker; Textänderungen aus `1818764`, in keinem Lauf gefahren (seit 2026-11-12)
- [ ] **herdr-app-umstellung: 5 Review-Findings unter dem Cap** — Kontext: am Ende von `features/herdr-app-umstellung/review.md`, alles Kleinigkeiten; dazu F6 (Heredoc, L38) übersprungen (seit 2026-11-12)
- [ ] **INBOX #112 (Checkliste vor dem Feature-Start) auf `dtb:implement` Schritt 1 umhängen** — Kontext: seit #179 startet `feature-start` keine Features mehr; beim nächsten `/dtb:idea-review` umformulieren (Nachtrag 2 zum Hand-off #179) (seit 2026-11-10)
- [ ] **#178 plan-in-einem-befehl: ersten echten `/dtb:feature-plan`-Lauf beobachten** — Kontext: Lauf vom 2026-11-12 (#200) zählt nicht, er lud die alte installierte Kopie (#202); seit dem `kit-sync` vom 2026-11-12 ist die neue Fassung installiert — der nächste Lauf zählt; Beleg mit frischem Blick; dabei Backlog-Zweig (Status Geplant bzw. Spezifiziert) und Fehlerpfad „impl-plan nicht installiert" ansehen — im Probelauf nicht gefahren; Fehlerpfad „Anker fehlt" bei der Abnahme an einer Kopie belegt (seit 2026-11-09)
- [ ] **#22 seed-skew-aktiv-melden: fetch-Teil der Abhilfe-Befehle im ersten echten Bestandsprojekt-Lauf beobachten** — Kontext: im Pane bewusst ungetestet (Kit-Klon nicht angefasst), show/diff/mv an einer Kopie gruen; naechster `kit-sync check` in einem Zielprojekt mit altem Seed (z. B. PKP) — seit #179 weicht der Seed (§7.3) überall ab (seit 2026-11-09)
- [ ] **checkpoint-schneller + checkpoint-ohne-rueckfragen: gemeinsame Nachmessung bis 2026-12-02** — Kontext: Kriterium in `features/checkpoint-ohne-rueckfragen/spec.md` (Success Criteria, Ausgangswert 89 Läufe: Kern-Median 5,0 min); chain-metrics + `checkpoint-phasen.py --rueckfragen`, 3 Vergleichsläufe mit denselben Funden (seit 2026-11-02) ⏳
- [ ] **checkpoint-ohne-rueckfragen: Nachbesserung Erfassungs-Block beim ersten Checkpoint nach dem Merge prüfen** — Kontext: Probelauf-Befund 1 (Alters-Zeile nicht mehr unter „Erfasst:"); erster Echtlauf mit Funden und ⏳ ist der Checkpoint 2026-11-06 — dessen Bestätigung ansehen (seit 2026-11-03) ⏳
- [ ] **PKP-Durchlaufzeiten am 2026-11-27 wiederholen** — Kontext: Windows-Erinnerung 09:07, Anleitung `~/.claude/analysen/pkp-durchlaufzeiten/README.md`; spaeter nicht moeglich (Protokolle 30 Tage, L106) (seit 2026-10-28) ⏳
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — in Abnahme 4.2 (Wegwerf-Change) A1, A2, A4 gesehen, A3 nicht; zählt erst an einem echten Change (seit 2026-10-22 · behalten 2026-10-29) ⏳
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-11-03) ⏳
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-29) ⏳
- [ ] **`/dtb:idea-triage`** — Kontext: 122 ungesichtet, mit Vorsortierung; #54/#70 sind korrekt escapt (geprüft 2026-11-06) (seit ≤2026-09-09 · behalten 2026-10-29) ⏳
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-29) ⏳

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-11-12 | #200 herdr-app-umstellung reviewt | impl-review NEEDS ATTENTION ohne Blocker, Triage 9 FIXED · 1 SKIPPED (`1818764`); L135–L137, #207 | `2026-11/2026-11-12.md` |
| 2026-11-12 | #200 herdr-app-umstellung fertig umgesetzt | Phasen 1–4 (`0378ebe`, `5da0035`, `c188566`, `851b4b9`); Abnahme-Läufe 4.1–4.3 in der App: Worker- und Pane-Tab, Wechsel/clear/resume, Hand-off aus der Datei bei offenem Dialog, Arbeit bei geschlossenem Fenster, Gate außerhalb der App; L130–L134 | `2026-11/2026-11-12.md` |
| 2026-11-10 | #179 implement-ohne-feature-start abgenommen, gemergt, kit-sync, archiviert | impl-review-Folgelauf 8/8 FIXED (`8ad9d69`), Abnahme beider Manual-Kriterien, Merge `3ab951d`, kit-sync 9/9 auf `85ba9c1`, Ordner nach `archive/`; #198 | `2026-11/2026-11-10.md` |
| 2026-11-10 | #179 implement-ohne-feature-start im Pane fertig | `/dtb:pane-start 179` → feature-fast, plan-review REVISE → Reviewed, Phasen 1–2 (`0701707`, `d5c592d`), impl-review 8/8 FIXED (`52efdd8`), Hand-off 13:45; L128, #196, #197 | `2026-11/2026-11-10.md` |
| 2026-11-09 | #178 plan-in-einem-befehl abgenommen, gemergt, kit-sync | Abnahme mit Probelauf A/B und selbst gefahrenem Fehlerpfad „Anker fehlt", Merge `4bc2a47`, kit-sync 3/3 auf `485942f` | `2026-11/2026-11-09.md` |
| 2026-11-09 | #22 seed-skew-aktiv-melden abgenommen, gemergt und archiviert | Fast-Track im Pane-Worktree, Phasen 1–2, impl-review 10/10 FIXED, Merge `ac5c742`, kit-sync 3/3; `kit-sync check` meldet veraltete Seeds; L125–L127, #192 | `2026-11/2026-11-09.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** — offen — (mit /dtb:workflow-next bestimmen)
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 122 ungesichtet → /dtb:idea-triage
