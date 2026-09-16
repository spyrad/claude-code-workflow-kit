# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-16
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-16.md`

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
| **Notizen** | Erstmals kein offener Change in `features/` — naechste Arbeit kommt aus dem Becken oder der INBOX. Becken 45 ungesichtet (neu: #94). Ableitungsluecke #86 unveraendert |

---

## Offene Aufgaben

- [ ] **`/dtb:idea-triage`** — Kontext: 45 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92/#93/#94
- [ ] **Idee erfassen: Kriterien-Checkboxen ohne Pfleger** — Kontext: `dtb:implement` prueft Checkpoint-Kriterien, flippt aber nur `## Progress` (Befehl im Verlustpruefungs-Report 2026-09-16)
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; Auto-Modus lehnt `rm` ab → per `! rm {pfad}` selbst ausfuehren (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-16 | Archiv `feature-start-statusfeld` (S2) | Ordner nach `archive/` verschoben, `b0efe50` gepusht; `features/` erstmals leer | `2026-09/2026-09-16.md` |
| 2026-09-16 | Abnahme `feature-start-statusfeld` (S1) | 4/4 Manual + 13/13 Automated belegt; Rueckweg-Kriterium fand einen realen Planfehler (→ L59) | `2026-09/2026-09-16.md` |
| 2026-09-12 | Abnahme + Archiv idea-review Sofort-Schreiben (#71) | Wirklauf in 2 Laeufen belegt, archiviert samt INBOX #41/#71 (`2bdf56b`) | `archive/idea-review-sofortschreiben/task.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next` (kein aktives Item ableitbar) — inhaltlich vorgesehen: `/dtb:idea-triage`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Gueltigkeitsbedingung:** Gilt, solange `features/` leer ist und das Becken ungesichtet bleibt.
**Becken:** 45 ungesichtet → /dtb:idea-triage
