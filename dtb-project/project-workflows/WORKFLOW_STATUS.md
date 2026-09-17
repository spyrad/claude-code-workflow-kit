# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-09-17
**Letzter Session-Log:** `dtb-project/project-changelog/2026-09/2026-09-17.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| idea-rank | Fertig zum Testen | 6/6 | — offen — (mit /dtb:workflow-next bestimmen) |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | `idea-rank` gemergt, gepusht, installiert (`19a7ea0`); Abnahme steht aus, weil der Probelauf vor den Review-Triagen lag. Worktree `pane-idea-rank` noch vorhanden |

---

## Offene Aufgaben

- [ ] **Abnahme `idea-rank`** — Kontext: frischer `/dtb:idea-rank`-Lauf auf installiertem Skill, Manual-Kriterien in `plan.md` abhaken
- [ ] **Arbeitsplatz `pane-idea-rank` abbauen** — Kontext: Pane `w3:p9` `/exit`, `git worktree remove ../.dtb-worktrees/pane-idea-rank`, `git branch -d feature/idea-rank`
- [ ] **`/dtb:idea-review` fortsetzen** — Kontext: 6 offene Ideen ab #95
- [ ] **`/dtb:idea-triage`** — Kontext: 46 ungesichtet; #85 mit Vermerk aus #91 verwerfen, #81 verwerfen, #92–#94, #96; #27-Verweis mitsichten
- [ ] **Idee erfassen: Kriterien-Checkboxen ohne Pfleger** — Kontext: `dtb:implement` prueft Checkpoint-Kriterien, flippt aber nur `## Progress`
- [ ] **5 Findings unter dem Review-Cap** — Kontext: Befehle in `archive/ideen-becken/review.md`
- [ ] **L52/L53/L63 heben** — Kontext: Applies-to `alle` → `skills/CLAUDE.md` „Mechanik-Regeln"
- [ ] **Veraltete TTS-Dateien loeschen** — Kontext: `Desktop\install-claude-tts.ps1`, `~/.claude/tts/install-template.ps1`, `build-installer.ps1`; per `! rm {pfad}` selbst ausfuehren (L58)
- [ ] **Sprachausgabe auf dem Arbeitsrechner** — Kontext: Einzeiler aus github.com/spyrad/claude-code-tts, ggf. `-OfflineOnly`

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-09-17 | `idea-rank` via Pane gebaut (#33) | 6/6, impl-review 2 Laeufe (20 FIXED), ff-Merge + Push `19a7ea0`, kit-sync | `2026-09/2026-09-17.md` |
| 2026-09-16 | Archiv `feature-start-statusfeld` (S2) | Ordner nach `archive/` verschoben, `b0efe50` gepusht | `2026-09/2026-09-16.md` |
| 2026-09-16 | Abnahme `feature-start-statusfeld` (S1) | 4/4 Manual + 13/13 Automated belegt (→ L59) | `2026-09/2026-09-16.md` |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** — offen — (mit /dtb:workflow-next bestimmen) — inhaltlich vorgesehen: `/dtb:idea-rank` als Abnahme-Lauf
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
**Becken:** 46 ungesichtet → /dtb:idea-triage
