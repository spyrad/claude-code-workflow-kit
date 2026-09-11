# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-11
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-11.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| feature-start-statusfeld | Fertig zum Testen | 5/5 | /dtb:workflow-checkpoint |
| idea-review-sofortschreiben (#71) | Erledigt | 6/6 | /dtb:archive |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `feature-start-statusfeld`: Review triagiert, fehlt nur die Abnahme mit Beleg (Ableitungsluecke #86); `idea-review-sofortschreiben`: vor dem Archivieren Wirklauf (Abbruch nach 2. Entscheidung) |

---

## Offene Aufgaben

- [ ] **Wirklauf Sofort-Schreiben** — Kontext: `/dtb:idea-review`, nach der 2. Entscheidung abbrechen, beide in `INBOX.md` pruefen
- [ ] **`/dtb:idea-triage`** — Kontext: 40 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1` (Quelle jetzt `claude-code-tts`)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-11 | Sprachausgabe veroeffentlicht | Oeffentliches Repo `spyrad/claude-code-tts` (Einzeiler, Stopp-Hotkey, Uninstall) | `2026-09/2026-09-11.md` (S2) |
| 2026-09-11 | idea-review Sofort-Schreiben (#71) | 6/6, verteilt (Lock 48 @ `e4e436d`) | `features/idea-review-sofortschreiben/task.md` |
| 2026-09-11 | Abnahme + Archiv feature-fast, meeting-agenda, output-style-gezielt | 3 Features seit August abgenommen und archiviert | `archive/ARCHIVE_LOG.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — Checkpoint S2 (L53-L55, #90/#91, Status-Sync, Session-Log) ist uncommittet; danach Wirklauf `/dtb:idea-review` fuer `idea-review-sofortschreiben`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange die Checkpoint-Pfade uncommittet sind und `features/idea-review-sofortschreiben/` existiert.
**Becken:** 40 ungesichtet → /dtb:idea-triage
