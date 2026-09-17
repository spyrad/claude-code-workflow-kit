# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-17
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-17.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| idea-rank | Abgenommen | 9/9 | /dtb:archive |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `idea-rank` im zweiten Abnahme-Lauf bestanden (Tabellen-Fassung, „passt"); wartet auf Archivierung |

---

## Offene Aufgaben

- [ ] **`/dtb:archive` fuer `idea-rank`** — Kontext: Abgenommen 2026-09-17, INBOX #33 (Ausgearbeitet) mitnehmen
- [ ] **`/dtb:idea-review` fortsetzen** — Kontext: 6 offene Ideen, Rangliste empfiehlt #95 zuerst
- [ ] **`/dtb:idea-triage`** — Kontext: 46 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92–#94, #96; #27-Verweis mitsichten
- [ ] **Idee erfassen: Kriterien-Checkboxen ohne Pfleger** — Kontext: `dtb:implement` prueft Checkpoint-Kriterien, flippt aber nur `## Progress` (Beleg idea-rank)
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53/L63 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; per `! rm {pfad}` selbst ausfuehren (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-17 | Abnahme `idea-rank` | Lauf ueber 6 Ideen „passt" → Abgenommen | `2026-09/2026-09-17.md` |
| 2026-09-17 | `idea-rank` Phase 3: Tabelle nach Wichtigkeit | Abnahme 1 nicht bestanden → Phase 3 `8f2b197`, Review-Laeufe 3+4 (20 FIXED), Push `c7e8f45`, kit-sync | `2026-09/2026-09-17.md` |
| 2026-09-17 | `idea-rank` via Pane gebaut (#33) | 6/6, impl-review 2 Laeufe (20 FIXED), ff-Merge + Push `19a7ea0`, kit-sync | `2026-09/2026-09-17.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:archive idea-rank`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 46 ungesichtet → /dtb:idea-triage
