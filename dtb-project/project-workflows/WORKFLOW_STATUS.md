# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-14
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-14.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Opportunity-Map | In Arbeit | 10/11 | Schritt 3.3 — kit-sync (Verteilung) + SC-Abschluss |
| Greenfield-Autoren-Skills | Fertig zum Testen | 14/14 | Abnahme beim ersten realen Greenfield (Entscheidung G) |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Notizen** | 2026-07-14 (S3): opportunity-map-Nudge in greenfield-prd gebaut + verifiziert (SC8), 6 Commits nach origin gepusht (`ff214ed`). Offen nur 3.3: kit-sync-Verteilung (außenwirksam) — check gemacht (opportunity-map neu, greenfield-prd/pipeline-graph Update, pitch-coach bewusst halten), Sync noch nicht ausgeführt. |

---

## Offene Aufgaben

- [ ] Opportunity-Map 3.3 abschließen — Kontext: `/dtb:kit-sync` sync (Bündel 1; pitch-coach halten), Lock → `ff214ed`, dann SC1-9 in spec.md abhaken → Fertig zum Testen
- [ ] Lektion-Kandidaten festhalten — Kontext: (a) nicht-deterministische Tool-Anteile geteilt verifizieren, (b) blinde Fixtures decken Pfad-Inkonsistenzen auf → `/dtb:lesson`
- [ ] Idee-Triage Rest — Kontext: #10 (pinned/hold, durch pitch-coach-Fall erneut motiviert), #13, #15, #16, #18
- [ ] Erstes reales Greenfield-Vorhaben — Kontext: echte Abnahme Greenfield-Autoren-Skills (Entscheidung G)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-14 | Opportunity-Map gebaut + verifiziert | Skill + greenfield-prd-Nudge; SC1-9 belegt (7 Blindläufe + Websuche-Läufe); 10/11, nur Verteilung offen | `2026-07/2026-07-14.md` (S2/S3) |
| 2026-07-14 | Codebase-Research-Step abgenommen | pkp-praxiserprobt; abgenommen + archiviert | `archive/codebase-research-step/` |
| 2026-07-13 | Greenfield-Autoren-Skills umgesetzt | prd/roadmap Autoren-Skills; 14/14, SC1-9 belegt | `2026-07/2026-07-13.md` (S8) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:kit-sync` (sync) — Schritt 3.3: Bündel 1 verteilen (opportunity-map neu + greenfield-prd/pipeline-graph Update), **pitch-coach bewusst halten** (nicht syncen), Lock → `sourceCommit ff214ed`. Danach SC1-9 in `features/opportunity-map/spec.md` abhaken (letzter nicht abgehakter Progress-Schritt 3.3).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl. kit-sync ist außenwirksam (globale `~/.claude/`-Installation) — vor Ausführung bewusst bestätigen.
