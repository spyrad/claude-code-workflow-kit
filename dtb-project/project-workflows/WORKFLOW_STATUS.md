# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-10-28
**Letzter Session-Log:** `dtb-project/project-changelog/2026-10/2026-10-28.md`

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
| **Notizen** | Zwei Pane-Worktrees: #158 `dashboard-projektname-hintergrund` (5/5, Hand-off da, Abnahme offen), #141 `lektionen-kuratieren` (2/11, laeuft); Tick-Job `6a81ac09` |

---

## Offene Aufgaben

- [ ] **Abnahme #158 Dashboard mit Projektname und Raster-Hintergrund** — Kontext: Seite nach den Review-Fixes neu erzeugen und im Browser pruefen (h1-id, Umbruch, `color-mix`, Hex-Tokens), dann Merge `feature/dashboard-projektname-hintergrund` → `master`, `/dtb:kit-sync sync`, Probeseite im Testbett, Worktree abbauen (seit 2026-10-28)
- [ ] **Nach Merge #158: globale Updates nachziehen** — Kontext: INBOX #158 → Ausgearbeitet + Links discovery/spec, BACKLOG-Zeile „Aktive Features" (Prio Niedrig), `spec.md`-Kopf auf abgeleiteten Status; vor dem Merge fehlen die Dateien auf `master` (seit 2026-10-28)
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27)
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27)
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — bisher nur „Ende" im Betrieb gesehen (seit 2026-10-22)
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-10-27)
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-22)
- [ ] **`/dtb:idea-triage`** — Kontext: 91 ungesichtet, mit Vorsortierung; #70/#54 vorher von bare Pipes befreien (seit ≤2026-09-09 · behalten 2026-10-22)
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-22)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-10-27 | #135 Projekt-Dashboard abgenommen | Pane-Arbeitsplatz Phasen 1–3, impl-review 10/10 FIXED (`155e837`), Merge `a7a76a9`, kit-sync 52/52, Abnahme 3.4 (a)–(c), 11/11; L98–L100 | `2026-10/2026-10-27.md` |
| 2026-10-27 | Doppelte Skill-Trigger entfernt | 3 Beschreibungen (`archive`, `backlog-status`, `workflow-resume`) eindeutig, Commit `e4c6b62` | `2026-10/2026-10-27.md` |
| 2026-10-22 | #142 Pane-Session-Neustart abgeschlossen | Befunde A1-A4 + 2 Cap-Findings nachgearbeitet (`1632323`), kit-sync 51/51, archiviert; L97 | `2026-10/2026-10-22.md` |
| 2026-10-22 | #142 Pane-Session-Neustart abgenommen | Abnahme 3.3 am echten Wechsel (a)-(f) bestanden, 9/9 (`4062b28`), 4 Befunde in review.md; L95, L96 | `2026-10/2026-10-22.md` |
| 2026-10-21 | #142 Pane-Session-Neustart Phasen 1–3 | Pane-Session, 8/9, plan-review REVISE → behoben, 2× impl-review 20/20 FIXED (`f2fd655`); L93, L94, #143, #144 | `2026-10/2026-10-21.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 91 ungesichtet → /dtb:idea-triage
