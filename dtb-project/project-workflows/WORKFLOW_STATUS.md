# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-07-10
**Letzter Session-Log:** `dtb-project/project-changelog/2026-07/2026-07-10.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| Bug: project-init-stale-rules-seed | Behoben | 4/4 | Abnahme-Test (`project-init` + Hash-Vergleich), dann `/dtb:archive` |
| Eligibility-Gates | Abgenommen | 13/13 | Beim gemeinsamen Abnahme-Durchgang → `/dtb:archive` |
| Review-Härtung | Fertig zum Testen | 11/11 | Praxiserprobung, dann Abnahme + `/dtb:archive` |
| Spec-Härtung | Fertig zum Testen | 9/9 | Praxiserprobung, dann Abnahme + `/dtb:archive` |
| Skill-10x-Optimierungen | Fertig zum Testen | 15/15 | Praxiserprobung, dann Abnahme + `/dtb:archive` |
| Change-Folder-Modell | Fertig zum Testen | 15/15 | Praxiserprobung, dann Abnahme + `/dtb:archive` |
| Frontmatter- und Pfad-Hygiene | Fertig zum Testen | 12/12 | Praxiserprobung, dann Abnahme + `/dtb:archive` |

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine (alles nach `origin/master` gepusht, `96eb2df`) |
| **Notizen** | Kit-Bug `project-init-stale-rules-seed` behoben: Seed kopiert nun mechanisch über `lock.localPath` (+ Hash + Fallback), global verteilt (Lock `8c1c906 → 96eb2df`). Lokal verifiziert; realer Abnahme-Test offen. Lektion L4 („mechanisch kopieren statt rekonstruieren") erfasst |

---

## Offene Aufgaben

- [ ] Abnahme-Test des Fixes: `project-init` in frischem Projekt/`pkp` → Hash der geseedeten `DERIVED_STATE_RULES.md` == Kit-Hash `a7961f7e`
- [ ] Gemeinsamer Abnahme-/Archiv-Durchgang: 6 abnahmereife Features + behobener Bug → `/dtb:archive`
- [ ] Ideen triagieren: #11 (Greenfield), #13 (Fachfragen-Agenda), #10 (kit-sync pinned) → `/dtb:idea-review`
- [ ] Folge-Feature Eligibility-Gates: Git-Gates + Soft-Gates

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-07-10 | Kit-Bug project-init-stale-rules-seed behoben | Mechanisches Seed-cp über `lock.localPath` + Hash + Fallback, global (Lock `96eb2df`) | `2026-07/2026-07-10.md` (Session 4) |
| 2026-07-10 | Eligibility-Gates abgenommen | 13/13, Fixture 10/10 + pkp-Realtest, global (Lock `8c1c906`) | `2026-07/2026-07-10.md` (Session 1-3) |
| 2026-07-09 | Frontmatter- und Pfad-Hygiene umgesetzt | 12/12, global (Lock `8f508b8`) | `2026-07/2026-07-09.md` (Session 6) |
| 2026-07-09 | CHANGE_FOLDER_MODELL umgesetzt | 15/15, global (Lock `2dfce5f`) | `2026-07/2026-07-09.md` (Session 5) |
| 2026-07-09 | SKILL_10X_OPTIMIERUNGEN umgesetzt | 15/15, global (Lock `77f7f7f`) | `2026-07/2026-07-09.md` (Session 4) |

---

## Pausierte Themen

Keine.

---

## Handoff

**Naechster Befehl:** `/dtb:archive` — gemeinsamer Abnahme-/Archiv-Durchgang der 6 abnahmereifen Features + des behobenen Bugs. Empfohlen davor: kurzer Abnahme-Test des project-init-Fixes (`project-init` in frischem Projekt → Hash-Vergleich) und Lektion via `/dtb:lesson` bestätigen.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
