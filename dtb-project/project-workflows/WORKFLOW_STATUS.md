# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-18
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-18.md`

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
| **Notizen** | Autopilot-Machbarkeit geklaert; kein Harness-Schalter fuer `disable-model-invocation` (getestet) |

---

## Offene Aufgaben

- [ ] **`/dtb:idea-review` fortsetzen** — Kontext: pausiert bei Schritt 2 von 4, 8 offene Ideen
- [ ] **#97, #57 und #98 zusammen entscheiden** — Kontext: dieselbe Autonomie-Achse, getrennt entschieden widerspruechlich
- [ ] **`/dtb:idea-triage`** — Kontext: 46 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92–#94, #96
- [ ] **Lektion selbst erfassen** — Kontext: Slash-Befehl = Text-Injektion des Skill-Koerpers (Befehl im Verlustpruefungs-Report)
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; per `! rm {pfad}` selbst ausfuehren (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-18 | Autopilot-Machbarkeit geklaert | Wand ist `dtb:implement:215`, nicht Herdr; kein Harness-Schalter (Doku + eigener Test); Ideen #97/#98 erfasst | `2026-09/2026-09-18.md` |
| 2026-09-17 | Abnahme + Archiv `idea-rank` | Lauf ueber 6 Ideen „passt" → Abgenommen → `archive/idea-rank/` (`6e511c5`) | `2026-09/2026-09-17.md` |
| 2026-09-17 | `idea-rank` Phase 3: Tabelle nach Wichtigkeit | Abnahme 1 nicht bestanden → Phase 3 `8f2b197`, Review-Laeufe 3+4 (20 FIXED), Push `c7e8f45`, kit-sync | `2026-09/2026-09-17.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:workflow-next`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 46 ungesichtet → /dtb:idea-triage
