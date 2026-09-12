# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-12
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-12.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| feature-start-statusfeld | Fertig zum Testen | 5/5 | /dtb:workflow-checkpoint |
| idea-review-sofortschreiben (#71) | Abgenommen | 6/6 | /dtb:archive |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `feature-start-statusfeld`: Review triagiert, Abnahme braucht die 4 Manual-Kriterien (realer Start: `gitattributes-eol` nicht mehr unter `features/` → Ersatz suchen); Ableitungsluecke #86 |

---

## Offene Aufgaben

- [ ] **Abnahme `feature-start-statusfeld`** — Kontext: 4 Manual-Kriterien in `features/feature-start-statusfeld/plan.md`, inkl. Wegwerf-Test Progress-Nachruestung
- [ ] **`/dtb:idea-triage`** — Kontext: 42 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, neu #92/#93
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1` (Quelle jetzt `claude-code-tts`)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-12 | Abnahme idea-review Sofort-Schreiben (#71) | Wirklauf in 2 Laeufen belegt, Restluecke Zusammenlegen (L43) | `features/idea-review-sofortschreiben/task.md` |
| 2026-09-11 | Sprachausgabe veroeffentlicht | Oeffentliches Repo `spyrad/claude-code-tts` (Einzeiler, Stopp-Hotkey, Uninstall) | `2026-09/2026-09-11.md` (S2) |
| 2026-09-11 | Abnahme + Archiv feature-fast, meeting-agenda, output-style-gezielt | 3 Features seit August abgenommen und archiviert | `archive/ARCHIVE_LOG.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — Checkpoint 2026-09-12 S1 (L56, #92/#93, INBOX #41, Abnahme, Session-Log) ist uncommittet; danach `/dtb:archive` fuer `idea-review-sofortschreiben`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange die Checkpoint-Pfade uncommittet sind und `features/idea-review-sofortschreiben/` existiert.
**Becken:** 42 ungesichtet → /dtb:idea-triage
