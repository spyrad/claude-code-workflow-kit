# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-12
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-12.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| feature-start-statusfeld | Fertig zum Testen | 5/5 | /dtb:workflow-checkpoint |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `feature-start-statusfeld`: Review triagiert, Abnahme braucht die 4 Manual-Kriterien (realer Start: `gitattributes-eol` nicht mehr unter `features/` → Ersatz suchen); Ableitungsluecke #86 |

---

## Offene Aufgaben

- [ ] **Abnahme `feature-start-statusfeld`** — Kontext: 4 Manual-Kriterien in `features/feature-start-statusfeld/plan.md`, inkl. Wegwerf-Test Progress-Nachruestung
- [ ] **`/dtb:idea-triage`** — Kontext: 42 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92/#93
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1` (Quelle jetzt `claude-code-tts`)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-12 | Abnahme + Archiv idea-review Sofort-Schreiben (#71) | Wirklauf in 2 Laeufen belegt, archiviert samt INBOX #41/#71 (`2bdf56b`) | `archive/idea-review-sofortschreiben/task.md` |
| 2026-09-11 | Sprachausgabe veroeffentlicht | Oeffentliches Repo `spyrad/claude-code-tts` (Einzeiler, Stopp-Hotkey, Uninstall) | `2026-09/2026-09-11.md` (S2) |
| 2026-09-11 | Abnahme + Archiv feature-fast, meeting-agenda, output-style-gezielt | 3 Features seit August abgenommen und archiviert | `archive/ARCHIVE_LOG.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-checkpoint` — Abnahme `feature-start-statusfeld`, nachdem die 4 Manual-Kriterien ausgeuebt sind (mechanische Regel ergaebe `/dtb:implement` wegen REJECTED, die Triage ist aber komplett — #86); vorher `/dtb:commit-and-push` fuer diesen Checkpoint (Log S2 + Status), falls noch nicht geschehen
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange `features/feature-start-statusfeld/` existiert und dort kein `Abgenommen` gesetzt ist.
**Becken:** 42 ungesichtet → /dtb:idea-triage
