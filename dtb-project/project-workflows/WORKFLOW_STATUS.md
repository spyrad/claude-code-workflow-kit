# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-11-09
**Letzter Session-Log:** `dtb-project/project-changelog/2026-11/2026-11-09.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| checkpoint-ohne-rueckfragen | Fertig zum Testen | 8/8 | gemeinsame Nachmessung bis 2026-12-02, dann Abnahme |
| checkpoint-schneller | Fertig zum Testen | 6/6 | gemeinsame Nachmessung bis 2026-12-02, dann Abnahme |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | #22 seed-skew-aktiv-melden im Pane-Worktree fertig und abgenommen, Merge offen (Branch `feature/seed-skew-aktiv-melden`, 3 Commits); Herdr-Integration claude jetzt v11 |

---

## Offene Aufgaben

- [ ] **#22 seed-skew-aktiv-melden mergen und abbauen** — Kontext: abgenommen 2026-11-09; Merge `feature/seed-skew-aktiv-melden` (`940a4b1`, `3b6d00d`, `226b7ff`), `spec.md` Status nachziehen, `/dtb:kit-sync sync`, Arbeitsplatz `w3:pZ` abbauen (Reihenfolge `dtb:worker` → `#### Abschluss`); fetch-Teil der Abhilfe-Befehle ungetestet (seit 2026-11-09)
- [ ] **checkpoint-schneller + checkpoint-ohne-rueckfragen: gemeinsame Nachmessung bis 2026-12-02** — Kontext: Kriterium in `features/checkpoint-ohne-rueckfragen/spec.md` (Success Criteria, Ausgangswert 89 Läufe: Kern-Median 5,0 min); chain-metrics + `checkpoint-phasen.py --rueckfragen`, 3 Vergleichsläufe mit denselben Funden (seit 2026-11-02) ⏳
- [ ] **checkpoint-ohne-rueckfragen: Nachbesserung Erfassungs-Block beim ersten Checkpoint nach dem Merge prüfen** — Kontext: Probelauf-Befund 1 (Alters-Zeile nicht mehr unter „Erfasst:"); erster Echtlauf mit Funden und ⏳ ist der Checkpoint 2026-11-06 — dessen Bestätigung ansehen (seit 2026-11-03)
- [ ] **PKP-Durchlaufzeiten am 2026-11-27 wiederholen** — Kontext: Windows-Erinnerung 09:07, Anleitung `~/.claude/analysen/pkp-durchlaufzeiten/README.md`; spaeter nicht moeglich (Protokolle 30 Tage, L106) (seit 2026-10-28) ⏳
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27 · behalten 2026-11-03)
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27 · behalten 2026-11-03)
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — bisher nur „Ende" im Betrieb gesehen (seit 2026-10-22 · behalten 2026-10-29) ⏳
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-11-03)
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-29) ⏳
- [ ] **`/dtb:idea-triage`** — Kontext: 110 ungesichtet, mit Vorsortierung; #54/#70 sind korrekt escapt (geprüft 2026-11-06) (seit ≤2026-09-09 · behalten 2026-10-29) ⏳
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-29) ⏳

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-11-09 | #22 seed-skew-aktiv-melden abgenommen | Fast-Track im Pane-Worktree, plan-review REVISE → 3 WARNs behoben, Phasen 1–2 (`940a4b1`, `3b6d00d`), impl-review 10/10 FIXED (`226b7ff`), Abnahme beider Manual-Kriterien; `kit-sync check` meldet veraltete Seeds; L125–L127, #192; Merge offen | `2026-11/2026-11-09.md` |
| 2026-11-09 | #175 worker-job-ende-meldung archiviert | INBOX- und BACKLOG-Zeile entfernt, Ordner nach `archive/worker-job-ende-meldung/`, ARCHIVE_LOG +2 | `2026-11/2026-11-09.md` |
| 2026-11-06 | #175 worker-job-ende-meldung abgenommen und gemergt | Discovery → plan-review REVISE → 3 Phasen (`45ba7d6`, `4b48528`, `d80ab5d`), impl-review 10/10 FIXED (`e0a2ba6`), Abnahme per probe.md, Merge `ffe509e`; Stop-Hook-Signal mit Dialog-Schutz; L119–L124, #189–#191 | `2026-11/2026-11-06.md` |
| 2026-11-06 | Health-Fixes + kit-sync | project-health ✅28 ⚠️2 ❌1; `allowed-tools` (idea-review, meeting-dump) und `project_name` (`ddc7d91`), kit-sync 2/2; #187, #188 | `2026-11/2026-11-06.md` |
| 2026-11-03 | #173 checkpoint-ohne-rueckfragen gemergt | Pane-Worktree Discovery → 2 Phasen (`4d538b8`, `5e41cfc`), plan-review REVISE, impl-review 10/10 FIXED (`98b5b45`), Merge `5ede096`, kit-sync 7/7; Probelauf 0 Rückfragen; L118, #186 | `2026-11/2026-11-03.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** Merge `feature/seed-skew-aktiv-melden` nach master (Reihenfolge `dtb:worker` → `#### Abschluss`), danach `/dtb:kit-sync sync`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 110 ungesichtet → /dtb:idea-triage
