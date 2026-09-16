# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-16 (`/dtb:archive`)
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-16.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine — der Abnahme-Blocker vom 2026-09-14 (L57) ist aufgeloest: das Manual-Kriterium „Realer Start" haengt jetzt an einem selbst erzeugten Wegwerf-Objekt statt am archivierten `gitattributes-eol` |
| **Notizen** | Becken 44 ungesichtet (Nachzaehlung bestaetigt; der erste Zaehlausdruck verfehlte die zwei Pipe-Zeilen `#54`/`#70`). Ableitungsluecke #86 unveraendert |

---

## Offene Aufgaben

- [ ] **`/dtb:idea-triage`** — Kontext: 44 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92/#93
- [ ] **Idee erfassen: Kriterien-Checkboxen ohne Pfleger** — Kontext: `dtb:implement` prueft Checkpoint-Kriterien, flippt aber nur `## Progress` (Befehl im Verlustpruefungs-Report 2026-09-16)
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; Auto-Modus lehnt `rm` ab → per `! rm {pfad}` selbst ausfuehren (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-16 | Abnahme `feature-start-statusfeld` | 4/4 Manual + 13/13 Automated belegt; Rueckweg-Kriterium fand einen realen Planfehler (→ L59) | `2026-09/2026-09-16.md` |
| 2026-09-12 | Abnahme + Archiv idea-review Sofort-Schreiben (#71) | Wirklauf in 2 Laeufen belegt, archiviert samt INBOX #41/#71 (`2bdf56b`) | `archive/idea-review-sofortschreiben/task.md` |
| 2026-09-11 | Sprachausgabe veroeffentlicht | Oeffentliches Repo `spyrad/claude-code-tts` (Einzeiler, Stopp-Hotkey, Uninstall) | `2026-09/2026-09-11.md` (S2) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` (Archiv-Aenderungen dieser Session: Ordner-Move nach `archive/feature-start-statusfeld/`, `ARCHIVE_LOG.md`, `BACKLOG.md`, Status), danach `/dtb:idea-triage` (44 ungesichtet)
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange die Archiv-Aenderungen nicht committet sind und das Becken ungesichtet ist.
**Becken:** 44 ungesichtet → /dtb:idea-triage
