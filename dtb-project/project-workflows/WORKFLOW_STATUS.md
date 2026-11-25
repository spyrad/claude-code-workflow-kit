# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-11-23
**Letzter Session-Log:** `dtb-project/project-changelog/2026-11/2026-11-23.md`

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
| **Notizen** | 2026-11-23: #200, #177, #173 archiviert und gepusht (`6e579d7`); S3: Pi in der Herdr-App repariert (`shellPath`, `~/.pi/agent/AGENTS.md`), L139, #213. #199 checkpoint-auto-commit (Plan Reviewed 0/18, `2dffa04` auf `feature/checkpoint-auto-commit`, nicht gepusht) liegt mit Worktree und Tab nur auf dem anderen Rechner. S4: PKP-Datenschutz-Hook als Vorlage für #145/#110 nachgetragen; Zusammenlegung #145/#193 beim nächsten `/dtb:idea-review` |

---

## Offene Aufgaben

- [ ] **#200 herdr-app-umstellung: Zweig `feature/herdr-app-umstellung` auf GitHub löschen** — Kontext: archiviert 2026-11-23; lokal schon weg, `origin/feature/herdr-app-umstellung` existiert noch (seit 2026-11-12) ⏳
- [ ] **#199 checkpoint-auto-commit: Umsetzung nach der Nachmessung (bis 2026-12-02)** — Kontext: Nachmessung am 2026-11-20 erledigt, Umsetzung damit frei; `/dtb:implement Checkpoint Auto-Commit` im Tab `checkpoint-auto-commit` auf dem anderen Rechner; Plan Reviewed 0/18, Schritt 4.5 (kit-sync-Nachweis) erst nach Merge und Push (seit 2026-11-13) ⏳
- [ ] **#199 checkpoint-auto-commit: übersprungene globale Updates beim Merge nachtragen** — Kontext: INBOX #199 → Ausgearbeitet mit Links auf discovery/spec/plan; BACKLOG-Zeile „Checkpoint Auto-Commit · Geplant · Mittel"; vorher zeigen die Links ins Leere (#114, #131) (seit 2026-11-13) ⏳
- [ ] **#200 herdr-app-umstellung: restliche Review-Fixes im nächsten echten Worker-/Pane-Lauf beobachten** — Kontext: F1 und F5 belegt (`archive/herdr-app-umstellung/probe.md` → Nachtrag); `pane-start` lief am 2026-11-13 sauber (#199), F2, F3, F4, F9, F10 dort nicht einzeln geprüft; Schließen eines Worker-Tabs mit laufender Claude-Session offen (seit 2026-11-12) ⏳
- [ ] **herdr-app-umstellung: 5 Review-Findings unter dem Cap** — Kontext: am Ende von `archive/herdr-app-umstellung/review.md`, alles Kleinigkeiten; dazu F6 (Heredoc, L38) übersprungen (seit 2026-11-12) ⏳
- [ ] **INBOX #112 (Checkliste vor dem Feature-Start) auf `dtb:implement` Schritt 1 umhängen** — Kontext: seit #179 startet `feature-start` keine Features mehr; beim nächsten `/dtb:idea-review` umformulieren (Nachtrag 2 zum Hand-off #179) (seit 2026-11-10) ⏳
- [ ] **#178 plan-in-einem-befehl: ersten echten `/dtb:feature-plan`-Lauf beobachten** — Kontext: erster Lauf mit der neuen Fassung am 2026-11-13 in der Pane von #199 (Struktur-Check 5/5, Spec und Plan in einem Lauf); Backlog-Zweig dort planmäßig übersprungen (Worktree), Fehlerpfad „impl-plan nicht installiert" weiter ungefahren — den nächsten Lauf im Haupt-Checkout ansehen (seit 2026-11-09) ⏳
- [ ] **#22 seed-skew-aktiv-melden: fetch-Teil der Abhilfe-Befehle im ersten echten Bestandsprojekt-Lauf beobachten** — Kontext: im Pane bewusst ungetestet (Kit-Klon nicht angefasst), show/diff/mv an einer Kopie gruen; naechster `kit-sync check` in einem Zielprojekt mit altem Seed (z. B. PKP) — seit #179 weicht der Seed (§7.3) überall ab (seit 2026-11-09) ⏳
- [ ] **checkpoint-ohne-rueckfragen: Nachbesserung Erfassungs-Block beim ersten Checkpoint nach dem Merge prüfen** — Kontext: Probelauf-Befund 1 (Alters-Zeile nicht mehr unter „Erfasst:"); erster Echtlauf mit Funden und ⏳ ist der Checkpoint 2026-11-06 — dessen Bestätigung ansehen; die Nachmessung 2026-11-20 hat das nicht geprüft (seit 2026-11-03) ⏳
- [ ] **PKP-Durchlaufzeiten am 2026-11-27 wiederholen** — Kontext: Windows-Erinnerung 09:07, Anleitung `~/.claude/analysen/pkp-durchlaufzeiten/README.md`; spaeter nicht moeglich (Protokolle 30 Tage, L106) (seit 2026-10-28) ⏳
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27 · behalten 2026-11-03) ⏳
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — in Abnahme 4.2 (Wegwerf-Change) A1, A2, A4 gesehen, A3 nicht; zählt erst an einem echten Change; 2026-11-13 (#199) nur „Ende", kein Wechsel (seit 2026-10-22 · behalten 2026-10-29) ⏳
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-11-03) ⏳
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-29) ⏳
- [ ] **`/dtb:idea-triage`** — Kontext: 128 ungesichtet, mit Vorsortierung; #54/#70 sind korrekt escapt (geprüft 2026-11-06) (seit ≤2026-09-09 · behalten 2026-10-29) ⏳
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-29) ⏳

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-11-23 | #200 herdr-app-umstellung, #177 checkpoint-schneller, #173 checkpoint-ohne-rueckfragen archiviert | drei Ordner nach `archive/`, Archiv-Log ergänzt; kein aktives Feature mehr im Haupt-Checkout | `2026-11/2026-11-23.md` |
| 2026-11-20 | #177 checkpoint-schneller + #173 checkpoint-ohne-rueckfragen nachgemessen und abgenommen | 58 Läufe nach dem Merge: Kern-Median 3,0 min (vorher 5,2), Alters-Fragen 0, Kontrollpunkt nur 2× Duplikat; #211, #212, L138 | `2026-11/2026-11-20.md` |
| 2026-11-13 | #199 checkpoint-auto-commit bis zum reviewten Plan (Pane) | `/dtb:pane-start 199` → Discovery, Spec, Plan in einem Lauf, plan-review REVISE → Reviewed (12 Findings), `2dffa04` auf dem Branch; #209, #210 | `2026-11/2026-11-13.md` |
| 2026-11-12 | #200 herdr-app-umstellung abgenommen, gemergt, kit-sync | Merge `2baaf1e..164c644`, kit-sync 4/4, Gegenprüfung F1/F5 in der App (`02ff5e8`), Abnahme mit Beleg; #208 | `2026-11/2026-11-12.md` |
| 2026-11-12 | #200 herdr-app-umstellung reviewt | impl-review NEEDS ATTENTION ohne Blocker, Triage 9 FIXED · 1 SKIPPED (`1818764`); L135–L137, #207 | `2026-11/2026-11-12.md` |
| 2026-11-12 | #200 herdr-app-umstellung fertig umgesetzt | Phasen 1–4 (`0378ebe`, `5da0035`, `c188566`, `851b4b9`); Abnahme-Läufe 4.1–4.3 in der App; L130–L134 | `2026-11/2026-11-12.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 128 ungesichtet → /dtb:idea-triage
