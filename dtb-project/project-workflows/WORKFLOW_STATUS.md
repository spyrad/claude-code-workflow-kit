# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-10-29
**Letzter Session-Log:** `dtb-project/project-changelog/2026-10/2026-10-29.md`

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
| **Notizen** | #141 archiviert; INBOX #171 neu (Zahlen in automatischen Tests maskieren), #164 um „technisch pruefbar" ergaenzt |

---

## Offene Aufgaben

- [ ] **kit-sync nach dem Push** — Kontext: Default `schwelle_kb` 80 in `dtb-lesson`, `dtb-lesson-curate`, `dtb-project-dashboard`, `dtb-project-init` erreicht die Kopien unter `~/.claude/` erst damit (seit 2026-10-29)
- [ ] **PKP-Durchlaufzeiten am 2026-11-27 wiederholen** — Kontext: Windows-Erinnerung 09:07, Anleitung `~/.claude/analysen/pkp-durchlaufzeiten/README.md`; spaeter nicht moeglich (Protokolle 30 Tage, L106) (seit 2026-10-28)
- [ ] **projekt-dashboard: 2 Review-Findings unter dem Cap** — Kontext: feste Slot-Zahl in Schritt 5 (durch #158 jetzt 9, `grep -c` zaehlt Zeilen), Guard-Kopie ohne Spiegel-Eintrag in `skills/CLAUDE.md` (seit 2026-10-27)
- [ ] **dtb-assistant: Probeseite project-dashboard.html loeschen oder behalten** — Kontext: Testbett ohne Git, Rest aus dem Probelauf Phase 2 (seit 2026-10-27)
- [ ] **A1-A4 beim naechsten echten Pane-Wechsel beobachten** — Kontext: Weiche nur „Wechsel"/„Ende", Offene Punkte als Momentaufnahme, kein leerer Wiederholungs-Block, Resume zeigt eigenen Change — bisher nur „Ende" im Betrieb gesehen (seit 2026-10-22 · behalten 2026-10-29)
- [ ] **triage-vorsortierung: Review-Findings unter dem Cap** — Kontext: in `archive/triage-vorsortierung/review.md`, u. a. B1 (Lektions-Dublette ohne eigenen Vorschlag in 3b), Meldezeile verschobene Zeilen, „streichen" dreifach, Guard-Tabelle (seit 2026-10-18 · behalten 2026-10-27)
- [ ] **TypeSafe-Key rotieren** — Kontext: L71 auf beiden Rechnern eingetreten, Key steht in zwei Session-Transcripts (seit 2026-09-28 · behalten 2026-10-29)
- [ ] **`/dtb:idea-triage`** — Kontext: 100 ungesichtet, mit Vorsortierung; #70/#54 vorher von bare Pipes befreien (seit ≤2026-09-09 · behalten 2026-10-29)
- [ ] **edge-tts auf dem Arbeitsrechner aktualisieren** — Kontext: `pip install --user --upgrade edge-tts --cert ~/.claude/tts/ca-bundle.pem` (L88) (seit 2026-10-15 · behalten 2026-10-29)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-10-29 | #141 Lektionen kuratieren abgenommen und archiviert | Erstlauf: 96 geprueft, 4 ausgemustert (Archiv neu), 56 KB; Default `schwelle_kb` 40 → 80; archiviert nach `archive/lektionen-kuratieren/`; L110–L112, #168–#172 | `2026-10/2026-10-29.md` |
| 2026-10-28 | PKP-Durchlaufzeiten ausgewertet | Claude ~14 % der aktiven Zeit; Voll-Schiene ~11 h, Fast-Track ~4 h je Change; Seite + Wiederholung 27.11.; L106–L109, #164–#167 | `2026-10/2026-10-28.md` |
| 2026-10-28 | #141 Lektionen kuratieren gemergt | Pane-Worktree Phasen 1–4, 11/11, impl-review 10/10 FIXED (`62ee1af`), Merge `2cba137` konfliktfrei, kit-sync 53/53; L103–L105 | `2026-10/2026-10-28.md` |
| 2026-10-28 | #158 Dashboard mit Projektname abgenommen | Fast-Track im Pane-Worktree, impl-review 7/7 FIXED (`268da05`), Merge `ed831bb`, kit-sync 52/52, Abnahme in pkp, archiviert; L101, L102 | `2026-10/2026-10-28.md` |
| 2026-10-27 | #135 Projekt-Dashboard abgenommen | Pane-Arbeitsplatz Phasen 1–3, impl-review 10/10 FIXED (`155e837`), Merge `a7a76a9`, kit-sync 52/52, Abnahme 3.4 (a)–(c), 11/11; L98–L100 | `2026-10/2026-10-27.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 100 ungesichtet → /dtb:idea-triage
