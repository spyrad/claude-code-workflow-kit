# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-11
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-11.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| feature-start-statusfeld | Fertig zum Testen | 5/5 | /dtb:workflow-checkpoint |
| idea-review-sofortschreiben (#71) | In Arbeit | 5/6 | 5: /dtb:kit-sync sync |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `feature-start-statusfeld`: Review triagiert (9 Fixed) — fehlt nur die Abnahme mit Beleg; Ableitungsluecke dazu #86 |

---

## Offene Aufgaben

- [ ] **`#81` verwerfen** — Kontext: der Becken-Eintrag IST der erledigte Migrationsauftrag, Ausgang via `/dtb:idea-triage`
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52 heben** — Kontext: Applies-to `alle`, dauerhafte Regel → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: `install-claude-tts.ps1` (Desktop) ausfuehren, dann `/hooks`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-11 | Abnahme feature-fast, meeting-agenda, output-style-gezielt | 3 Features seit August fertig → abgenommen mit Beleg, archiviert | `archive/ARCHIVE_LOG.md` |
| 2026-09-11 | Archivierung ideen-becken + inbox-becken-migration | 2 Change-Ordner + INBOX #76/#74/#73 im Archiv | `archive/ARCHIVE_LOG.md` |
| 2026-09-10 | Sprachausgabe #41 (lokal) | Katja via edge-tts, Hedda-Fallback, Installer fuer weitere Rechner | `2026-09/2026-09-10.md` (S1) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:kit-sync sync` — neue `dtb:idea-review`-Fassung verteilen (Schritt 5 von `idea-review-sofortschreiben`), danach `/dtb:workflow-checkpoint`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange Schritt 5 in `features/idea-review-sofortschreiben/task.md` offen ist.
**Becken:** 38 ungesichtet → /dtb:idea-triage
