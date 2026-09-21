# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-21
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-21.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| rueckfragen-erhebung (Task) | Fertig zum Testen | 6/6 | Policy-Tabelle festlegen (`erhebung.md:314`), dann /dtb:idea-review |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | Autonomie-Achse #57→#98→#97→#99 in drei Stationen; Station 1 (Erhebung) per Worker durch, Kriterium/Policy sind Vorschlaege |

---

## Offene Aufgaben

- [ ] **Policy-Tabelle festlegen** — Kontext: 16 Fragetypen in `features/rueckfragen-erhebung/erhebung.md` ab Z. 314; Vorbedingung fuer Station 2 (`/dtb:feature-fast` #57)
- [ ] **`/dtb:idea-review` fortsetzen** — Kontext: 9 offene Ideen; #97 ohne Beleg (0 Pane-Nachfragen in 5 Laeufen) → verwerfen oder mit #95 (4) zusammenlegen
- [ ] **`/dtb:idea-triage`** — Kontext: 46 ungesichtet; Worker-Buendel-Kandidaten #89→#46+58→#88, #93 ∥; #70/#54 vorher von bare Pipes befreien
- [ ] **Report-Kandidaten selbst erfassen (optional)** — Kontext: 2 Lektionen + 3 Ideen, Befehle im Log 2026-09-21
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; per `! rm {pfad}` (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`
- [ ] **Fremder Ordner `..\.dtb-worktrees\pane-artikel-sdd-was-ist-das`** — Kontext: nicht registriert, 2026-09-21 16:44, nicht aus dieser Session

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-21 | Station 1 Autonomie-Achse: Erhebung per Worker | 16 Rueckfrage-Typen ausgezaehlt, Kriterium-Vorschlag „Ruecknahmekosten statt Haeufigkeit", #97 P8 nicht bestaetigt; erster Worker-Lauf ueber Urteils-Schritte gruen (`c946bf5`) | `2026-09/2026-09-21.md` |
| 2026-09-21 | Autonomie-Achse eingeordnet | #99 (TypeSafe) erfasst, #57/#97/#98/#99 mit Rolle + Stationen-Zuschnitt; TypeSafe-Installation abgelehnt, L68/L69 | `2026-09/2026-09-21.md` |
| 2026-09-18 | Autopilot-Machbarkeit geklaert | Wand ist `dtb:implement:215`, nicht Herdr; kein Harness-Schalter; Ideen #97/#98 | `2026-09/2026-09-18.md` |
| 2026-09-17 | Abnahme + Archiv `idea-rank` | Lauf ueber 6 Ideen „passt" → Abgenommen → `archive/idea-rank/` (`6e511c5`) | `2026-09/2026-09-17.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:idea-review`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 46 ungesichtet → /dtb:idea-triage
