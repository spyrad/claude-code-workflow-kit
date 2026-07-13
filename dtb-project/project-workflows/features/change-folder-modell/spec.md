# Feature: Change-Folder-Modell

**Erstellt:** 2026-07-09
**Ziel:** Jeder Change bekommt einen eigenen Ordner (`features/<kebab-slug>/`) mit fixen Dateinamen statt flacher UPPER_SNAKE-Dateien mit fragilem Namens-Pairing.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- expliziter Zustand (ueberschreibt Ableitung), gesetzt 2026-07-13: SC1-3 live dogfooded (feature-discover-Ordneranlage, resume/backlog-Ableitung, archive git-mv), SC4 Dogfood-Migration 080b556, SC5/SC6 verhaltensecht via 3 blinde Multi-Varianten-Agenten (Git-Happy+Idempotenz, Non-Git+Backup, Kollisions-/uncommitted-Abbruch), SC7 Sweep, SC8 Budget -->

---

## Executive Summary

Das Artefakt-Layout wird von flachen, per Namens-Konvention gepaarten Dateien
(`FEATURE_X.md` + `PLAN_X.md` + `DISCOVERY_X.md`) auf **einen Ordner pro Change**
(`features/<kebab-slug>/` mit fixen Dateinamen `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md`)
umgestellt. Das beseitigt Pairing-Drift, macht Archivierung zu einem einzigen Ordner-Verschieben
und spiegelt das bewaehrte Vorbild (10x `context/changes/<id>/`). Der Umbau betrifft fast alle
Skills; er wird als harter Schnitt (kein Dual-Mode) plus einmaligem Migrations-Helfer umgesetzt.

---

## Scope / Abgrenzung

### Enthalten
- **Neues Layout:** `features/<kebab-slug>/` mit fixen Dateinamen `discovery.md`, `spec.md`, `plan.md`, optional `bug.md`, `task.md`
- **Namensform:** reine kebab-case-Slugs, keine laufenden Nummern; Ordnername wird beim Anlegen bestaetigt (wie heute der Feature-Name)
- **Archivierung:** wird zu `git mv features/<slug>/ archive/<slug>/` (kein Pairing mehr)
- **Regel-Quelle zuerst:** `DERIVED_STATE_RULES.md` auf Ordner-Konvention umschreiben; alle Reader referenzieren sie
- **Schreiber-Skills** anpassen: `feature-discover`, `feature-plan`, `impl-plan`, `bug-report`, `task`, `project-init`
- **Leser/Ableiter-Skills** anpassen: `workflow-resume`, `workflow-next`, `workflow-status`, `backlog-status`, `project-health`, `plan-review`, `debug-plan`
- **Mover-Skill** `archive` auf Ordner-Verschieben umstellen; Doku (`CLAUDE.md`, `pipeline-graph`, `generate-rules`, `docs-extract`, `feature-start`) nachziehen
- **Echte Migration** der 3 aktiven Features + 4 Archiv-Eintraege dieses Kits (Dogfood)
- **Einmaliger, idempotenter Migrations-Helfer** (`dtb:migrate-change-folders`) fuer bestehende Zielprojekte (flach -> Ordner, Kollisions-Abbruch, Drift-Report). Muss reale Fremd-Layouts aushalten (Fund aus `dtb-assistant`, 3-4 Alt-Projekte): **Nicht-Git-Projekte** (Move + Pflicht-Backup statt `git mv`), abgeschaffte/fremde Namen (`IMPL_STATUS_*`, `WORKFLOW_*_PLAN/_STATUS`, nicht-praefigierte Dateien, separater `bugs/`-Ordner) werden **nicht geraten**, sondern im Drift-Report gelistet

### Nicht enthalten
- Kein Dual-Mode / keine Rueckwaertskompatibilitaet zum flachen Modell (harter Schnitt)
- INBOX.md und BACKLOG.md bleiben flache Einzeldateien (pro-Projekt, nicht pro-Change) — nur der `features/`-Bereich wird zu Ordnern
- Keine inhaltliche Aenderung an Skill-Logik jenseits der Pfad-/Namens-Umstellung (Frontmatter-Hygiene ist Idee #9)
- Keine Write-Faehigkeit fuer Greenfield-Skills (Idee #11)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Breiter Blast-Radius (~22 Skills + Regel-Datei) — inkonsistente Teil-Umstellung | Hoch | Hoch | `DERIVED_STATE_RULES.md` zuerst als Single Source; Reader/Writer gebuendelt umstellen; Abnahme gegen Fixture-Projekt |
| Layout-Umbau kollidiert mit noch nicht abgenommenen Features (3x "Fertig zum Testen") | Hoch | Mittel | #7 erst nach Abnahme + `/dtb:archive` der 3 Features starten (frisches Archiv = Testfall) |
| Bestehende Zielprojekte verlieren nach kit-sync-Update ihren abgeleiteten Status | Mittel | Hoch | Migrations-Helfer erkennt flaches Layout selbst, idempotent, laeuft nach kit-sync |
| Datenverlust/Vermischung durch `git mv` bei uncommittetem Stand | Niedrig | Hoch | Migration prueft vorab `git status`; Abbruch bei uncommitteten Aenderungen an Betroffenen |
| Namenskollision zweier Basis-Namen auf denselben Slug | Niedrig | Mittel | Migration bricht mit Meldung der kollidierenden Namen ab (kein Auto-Rename) |
| Doppeltes Anfassen derselben Skills durch Idee #9 (Pfad-Hygiene) | Mittel | Niedrig | Reihenfolge zu #9 im impl-plan festlegen (vor oder gebuendelt) |

---

## Dependencies

### Erforderlich vor Start
- [x] Entscheidung Migrations-Helfer-Form (eigenes Kommando `dtb:migrate-change-folders`) — Plan-Review
- [x] Reihenfolge zu Idee #9 (gebuendelt mit Phase 2/3) — Plan-Review

**Hinweis Start-Reihenfolge (umgedreht 2026-07-09):** Change-Folder ist der **Enabler** fuer die
Praxiserprobung der 3 offenen Features (REVIEW/SPEC/SKILL_10X) — deren reales Testbett (`dtb-assistant`
u.a.) ist flach+chaotisch, Derived State greift dort erst nach Migration. Code der 3 ist fertig+ausgerollt,
nur ihre Abnahme ist offen -> alle 4 gemeinsam auf migriertem `dtb-assistant` abnehmen.

### Referenz-Dokumente
- `DISCOVERY_CHANGE_FOLDER_MODELL.md` - Discovery-Ergebnisse (Scope, Randfaelle, Einschraenkungen)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - zentrale Ableitungs-/Pairing-Regeln (Angelpunkt)
- `CLAUDE.md` - Output-Locations-Doku (muss nachgezogen werden)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [x] Ein neuer Change wird von den Schreiber-Skills als `features/<slug>/`-Ordner mit fixen Dateinamen angelegt — live belegt 2026-07-13 (feature-discover legte `features/passwort-reset-per-e-mail/` in der skill-10x-Verprobung an)
- [x] Alle Leser/Ableiter-Skills leiten Status korrekt aus dem Ordner-Layout ab — live belegt 2026-07-13 (workflow-resume + backlog-status leiteten aus `features/*/plan.md` ab, ohne Konflikt)
- [x] `archive` verschiebt einen Change als ganzen Ordner (`git mv`), kein Pairing-Drift mehr moeglich — live belegt 2026-07-13 (5 Ordner per git mv archiviert, von Git als Renames getrackt)
- [x] Die 3 aktiven Features + 4 Archiv-Eintraege dieses Kits sind fehlerfrei ins Ordner-Layout migriert — Dogfood-Migration `080b556`; heute verifiziert (alle Changes + Archiv-Eintraege sind Ordner)
- [x] Der Migrations-Helfer konvertiert ein flaches Fixture-Projekt idempotent, meldet unmigrierbare Dateien als Drift und bricht bei Kollision/uncommittetem Stand sauber ab — 2026-07-13 blind verprobt: M1 (Git-Happy: git-mv-Renames, Teil-Paarungen, Drift-Report, idempotenter No-Op-Zweitlauf) + M3 (Kollision + uncommitted → fail-safe Abbruch vor jeder Schreibaktion)
- [x] Der Helfer migriert ein **Nicht-Git-Projekt** korrekt (Move + Pflicht-Backup) und raet bei Fremd-Namen (`IMPL_STATUS_*`, `WORKFLOW_*`, nicht-praefigiert, `bugs/`) nichts — 2026-07-13 blind verprobt M2 (Backup `.migration-backup-2026-07-13/` + Warnung + Dateisystem-Move; Fremd-Namen liegen gelassen + im Drift-Report)
- [x] `DERIVED_STATE_RULES.md` + `CLAUDE.md` beschreiben ausschliesslich das Ordner-Modell; keine Skill referenziert mehr das flache Pairing — 2026-07-13 Sweep: 8 Treffer, alle Deprecation-/Migrations-Hinweise (kein operatives Pairing)
- [x] Alle geaenderten Skills bleiben < 500 Zeilen — 2026-07-13 geprüft (Maximum: pipeline-graph 498)

---

## Offene Punkte

- Priorisierung der 3-4 realen Alt-Projekte fuer die Migration (Reihenfolge, wann) — operativ, kein Blocker fuer die Umsetzung

_Im Plan-Review (2026-07-09) entschieden:_ Migrations-Helfer = eigenes Kommando `dtb:migrate-change-folders`;
Idee #9 gebuendelt mit Phase 2/3; Nicht-Git = Move + Pflicht-Backup; Fremd-Namen = liegen lassen + Drift-Report;
Start erst nach Abnahme+Archiv der 3 offenen Features.

---

**Erstellt mit:** `/dtb:feature-plan`
