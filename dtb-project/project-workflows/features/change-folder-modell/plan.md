# Implementierungsplan: Change-Folder-Modell

**Erstellt:** 2026-07-09
**Feature-Spec:** `features/FEATURE_CHANGE_FOLDER_MODELL.md`
**Geschaetzte Dauer:** ~6-7 Sessions (breiter Blast-Radius ~22 Skills + robuster Migrations-Helfer fuer reale Fremd-Layouts)
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Regel-Fundament + Doku | ~0.5 Session | Geplant |
| Phase 2 | Schreiber-Skills umstellen | ~1 Session | Geplant |
| Phase 3 | Leser/Ableiter-Skills umstellen | ~1 Session | Geplant |
| Phase 4 | Mover (archive) + robuster Migrations-Helfer | ~2 Sessions | Geplant |
| Phase 5 | Dogfood-Migration + Multi-Varianten-Abnahme + kit-sync | ~1.5 Sessions | Geplant |

---

## Phase 1: Regel-Fundament + Doku

### Ziel
Die Single Source der Ableitungslogik (`DERIVED_STATE_RULES.md`) und die Doku beschreiben das
Ordner-Modell — bevor irgendein Skill umgestellt wird (alle Reader referenzieren die Regel-Datei).

### Schritte

#### Schritt 1.1: DERIVED_STATE_RULES.md umschreiben
- **Zweck:** Pairing-Konvention durch Ordner-Konvention ersetzen (zentraler Angelpunkt)
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** aktuelle Pairing-/Ableitungsregeln
- **Output:** Regeln lesen aus `features/<slug>/plan.md` (Progress), `spec.md`, `discovery.md`, `bug.md`, `task.md`; Slug = kebab-case; Ableitungssemantik unveraendert, nur Quelle geaendert

#### Schritt 1.2: Doku nachziehen
- **Zweck:** Output-Locations + Artefakt-Tabellen konsistent zum Ordner-Modell
- **Dateien:** `CLAUDE.md` (Root, Output-Locations-Block), `skills/CLAUDE.md` (Artifact-Status-/Naming-Tabelle)
- **Output:** beide beschreiben ausschliesslich `features/<slug>/{discovery,spec,plan,bug,task}.md`

#### Schritt 1.3: Slug-Ableitungsregel festlegen
- **Zweck:** eindeutige, kollisionsarme Ordnernamen
- **Dateien:** `DERIVED_STATE_RULES.md` (Slug-Abschnitt)
- **Output:** Regel „Feature-Name -> kebab-case-Slug", Kollisions-Definition (zwei Namen -> selber Slug), keine Nummern

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `DERIVED_STATE_RULES.md` beschreibt Ordner-Modell + Slug-Regel
- [ ] Root- und Skills-CLAUDE.md nachgezogen

### Checkpoint-Kriterien
- [ ] Keine Referenz mehr auf flaches Pairing in Regel-Datei/Doku
- [ ] Ableitungssemantik (Spezifiziert/Geplant/In Arbeit/Fertig) unveraendert beschrieben

---

## Phase 2: Schreiber-Skills umstellen

### Ziel
Alle Skills, die Artefakte anlegen, schreiben ins Ordner-Layout und deklarieren korrekte `produces`.

### Schritte

#### Schritt 2.1: feature-discover + feature-plan
- **Zweck:** Discovery/Spec ins Ordner-Layout
- **Dateien:** `skills/dtb-feature-discover/SKILL.md`, `skills/dtb-feature-plan/SKILL.md`
- **Output:** legen `features/<slug>/discovery.md` bzw. `spec.md` an; Ordner-Anlage + Bestaetigung des Slugs; `pipeline.produces` aktualisiert

#### Schritt 2.2: impl-plan + feature-start
- **Zweck:** Plan-Artefakt + Feature-Start im Ordner
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`, `skills/dtb-feature-start/SKILL.md`
- **Output:** `features/<slug>/plan.md`; Progress-/Pfad-Referenzen; `produces`/`consumes` aktualisiert

#### Schritt 2.3: bug-report + task + project-init
- **Zweck:** Bug/Task im Ordner; project-init legt Ordner-Struktur an
- **Dateien:** `skills/dtb-bug-report/SKILL.md`, `skills/dtb-task/SKILL.md`, `skills/dtb-project-init/SKILL.md`
- **Output:** `features/<slug>/bug.md`/`task.md`; project-init scaffolding auf Ordner-Modell (hat bereits `Bash`)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 6 Schreiber-Skills schreiben ins Ordner-Layout
- [ ] `pipeline.produces` je Skill aktualisiert

### Checkpoint-Kriterien
- [ ] Ein neu angelegter Change erscheint als `features/<slug>/`-Ordner mit fixen Dateinamen
- [ ] Alle 6 Skills < 500 Zeilen

---

## Phase 3: Leser/Ableiter-Skills umstellen

### Ziel
Alle lesenden Skills leiten Status aus dem Ordner-Layout ab (gleiche Semantik, neue Quelle).

### Schritte

#### Schritt 3.1: workflow-resume + workflow-next + workflow-status
- **Zweck:** Session-Lifecycle-Leser auf Ordner-Glob
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md`, `-workflow-next/SKILL.md`, `-workflow-status/SKILL.md`
- **Output:** globben `features/*/plan.md` statt `PLAN_*.md`; Ableitung + `consumes` aktualisiert

#### Schritt 3.2: backlog-status + project-health
- **Zweck:** Uebersicht + Health-Checks auf Ordner
- **Dateien:** `skills/dtb-backlog-status/SKILL.md`, `skills/dtb-project-health/SKILL.md`
- **Output:** Glob-/Pfad-Logik + Health-Checks (Pairing-Check entfaellt/wird Ordner-Vollstaendigkeits-Check); `consumes` aktualisiert

#### Schritt 3.3: plan-review + debug-plan
- **Zweck:** Review liest `plan.md`, debug liest/schreibt `bug.md` im Ordner
- **Dateien:** `skills/dtb-plan-review/SKILL.md`, `skills/dtb-debug-plan/SKILL.md`
- **Output:** Pfad-Referenzen; `consumes`/`produces` aktualisiert

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 7 Leser/Ableiter-Skills nutzen Ordner-Layout
- [ ] `pipeline.consumes` je Skill aktualisiert

### Checkpoint-Kriterien
- [ ] Status wird aus `features/<slug>/plan.md` korrekt abgeleitet (identisch zu vorher)
- [ ] Alle 7 Skills < 500 Zeilen

---

## Phase 4: Mover (archive) + Migrations-Helfer

### Ziel
Archivierung verschiebt ganze Ordner; ein einmaliger, idempotenter Helfer migriert bestehende
flache Projekte.

### Schritte

#### Schritt 4.1: archive auf Ordner-Verschieben umstellen
- **Zweck:** ein Verschiebe-Vorgang pro Change, kein Pairing
- **Dateien:** `skills/dtb-archive/SKILL.md`
- **Output:** `archive/<slug>/`-Verschieben; **`Bash` in `allowed-tools` ergaenzen** (Grounding: fehlt aktuell); Git-Erkennung: `git mv` falls Repo, sonst Dateisystem-Move; `consumes`/`produces` aktualisiert; tote `IMPL_STATUS_*.md`-Referenz (Z.117) entfernen

#### Schritt 4.2: Migrations-Helfer — Erkennung + Kernlogik
- **Zweck:** flach -> Ordner konvertieren (einmalig, idempotent, sicher)
- **Dateien:** neuer Skill/Kommando `dtb:migrate-change-folders` mit `Bash`
- **Output:**
  - **Layout-Selbsterkennung** (schliesst Promise-Gap 1): erkennt flaches vs. bereits migriertes Projekt und bricht bei bereits-Ordner sauber ab
  - **Git-Erkennung** (realer Fund dtb-assistant = kein Repo): Repo -> `git mv` + `git status`-Guard (Abbruch bei uncommitteten Betroffenen); **kein Repo -> Dateisystem-Move + PFLICHT-Backup** des `features/`-Baums vorher (Ersatz fuer git-Rollback) + laute Warnung
  - **Idempotenz:** vorhandene Ziel-Ordner ueberspringen; **Kollisions-Abbruch** (zwei Basis-Namen -> selber Slug)

#### Schritt 4.3: Migrations-Helfer — Namens-Taxonomie + Archiv + Drift-Report
- **Zweck:** reale Fremd-Layouts korrekt einordnen, nichts raten, Ergebnis transparent
- **Dateien:** derselbe neue Skill/Kommando; Klasse-A automatisch abgedeckt
- **Output:**
  - **Erkannte Praefixe** -> Ordner-Dateien: `FEATURE_->spec`, `DISCOVERY_->discovery`, `PLAN_->plan`, `BUG_->bug`, `TASK_->task`; Teil-Paarungen (nur FEATURE, FEATURE+PLAN, FEATURE+PLAN+IMPL_STATUS) korrekt falten
  - **Abgeschafft/fremd -> NICHT raten, liegen lassen + im Report als „manuell pruefen":** `IMPL_STATUS_*` (abgeschafft, real vorhanden), `WORKFLOW_*_PLAN`/`WORKFLOW_*_STATUS` (Alt-Konvention), nicht-praefigierte Dateien (`FINN-018-…`), separater `bugs/`-Ordner
  - Archiv mitmigrieren (`archive/FEATURE_* -> archive/<slug>/spec.md`); **Drift-Report** (ungepaarte + unmigrierbare Dateien mit Grund)

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `archive` verschiebt ganze Ordner (git mv | Move je nach Repo)
- [ ] Migrations-Helfer vorhanden (Selbsterkennung, Git-/Non-Git-Pfad, Backup, Idempotenz, Taxonomie, Drift-Report)

### Checkpoint-Kriterien
- [ ] Helfer laeuft auf flachem Fixture (Git UND Non-Git) fehlerfrei durch
- [ ] Kollision/uncommitteter Stand/bereits-migriert -> sauberer Abbruch mit Meldung
- [ ] Unbekannte Namen werden nie geraten, sondern im Report gelistet

---

## Phase 5: Dogfood-Migration + Abnahme + kit-sync

### Ziel
Dieses Kit migrieren, Verhalten unabhaengig abnehmen, Skills global verteilen.

### Schritte

#### Schritt 5.1: Sicherungspunkt + Dogfood-Migration dieses Kits
- **Zweck:** 3 aktive Features + Archiv ins Ordner-Layout, mit Rollback-Anker
- **Dateien:** `dtb-project/project-workflows/features/*`, `.../archive/*`
- **Output:** **zuerst** `git`-Branch/Tag als Sicherungspunkt (Rollback-Anker); dann Helfer laufen lassen; alle Changes als Ordner; Drift-Report geprueft; Historie via `git mv` erhalten

#### Schritt 5.2: Unabhaengige Multi-Varianten-Abnahme
- **Zweck:** Migration gegen reale Fremd-Layouts verifizieren (abgeleitet aus `dtb-assistant`)
- **Dateien:** mehrere temporaere Fixture-Projekte (Scratchpad)
- **Output:** unabhaengiger Agent prueft Varianten: (a) **Non-Git-Projekt** -> Move + Backup, (b) `IMPL_STATUS_*`/`WORKFLOW_*`/nicht-praefigiert -> Drift-Report statt Rateergebnis, (c) separater `bugs/`-Ordner, (d) Teil-Paarungen, (e) idempotenter Zweitlauf, (f) Kollisions- + uncommitteter-Abbruch

#### Schritt 5.3: Konsistenz-Sweep + Budget-Check + kit-sync
- **Zweck:** vollstaendige Umstellung verifizieren, Distribution, Zeilen-Budget
- **Dateien:** alle geaenderten Skills, `~/.claude/` (global), `dtb-lock.json`
- **Output:** **Konsistenz-Sweep** (grep ueber alle Skills nach `PLAN_*`/`FEATURE_*`/flachen Mustern -> 0 Treffer; schliesst Promise-Gap 2 + Pre-Mortem-Ursache); alle geaenderten Skills < 500 Zeilen; `kit-sync` check->sync, Lock aktualisiert, R=L=K verifiziert

> **3x3-Block:** Nach Schritt 5.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Kit vollstaendig migriert (aktiv + Archiv), Sicherungspunkt gesetzt
- [ ] Multi-Varianten-Abnahme PASS (inkl. Non-Git)
- [ ] Konsistenz-Sweep 0 Treffer; kit-sync global, Lock aktualisiert

### Checkpoint-Kriterien
- [ ] Alle Success Criteria der Feature-Spec erfuellt
- [ ] Keine Skill referenziert mehr flaches Pairing (per Sweep belegt)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Migrations-Helfer Form | A: eigenes Kommando `dtb:migrate-change-folders` (Bash) · B: Modus in `project-init` · C: Modus in `kit-sync` | **A** | mehrere reale flache Projekte (3-4) -> Helfer noetig; A = klare Trennung, Klasse-A-Distribution automatisch |
| archive Verschiebe-Mechanik | A: `git mv` (+ Bash) · B: Read+Write-Kopie | **A (mit Non-Git-Fallback)** | Grounding: archive hat kein Bash; `git mv` erhaelt Historie; ohne Repo -> Dateisystem-Move |
| **Nicht-Git-Projekte** (realer Fund dtb-assistant) | A: `git mv` falls Repo, sonst Move + Pflicht-Backup · B: Verweigern + `git init` · C: Move ohne Backup | **A** | einmaliges Werkzeug darf realen Non-Git-Fall nicht blocken; Pflicht-Backup ersetzt git-Rollback |
| **Unbekannte/Fremd-Namen** (`IMPL_STATUS_*`, `WORKFLOW_*`, nicht-praefigiert, separater `bugs/`) | Raten/mappen vs. liegen lassen + Report | **Liegen lassen + Drift-Report** | reale Layouts zu divers; falsches Mapping zerstoert Status stumm |
| Reihenfolge zu Idee #9 (Pfad-/Frontmatter-Hygiene) | A: #9 vor #7 · B: gebuendelt · C: #9 nach #7 | **B (gebuendelt)** | consumes/produces-Umstellung ueberschneidet sich mit #9 — gebuendelt vermeidet doppeltes Anfassen |
| Start-Zeitpunkt vs. 3 offene Features | A: erst nach deren Abnahme+Archiv · B: sofort (Enabler) | **B (umgedreht 2026-07-09)** | Praxiserprobung der 3 braucht ein sauberes reales Testbett; die realen Alt-Projekte sind flach+chaotisch (IMPL_STATUS/Altnamen), auf denen Derived State nicht greift. Change-Folder + Migration IST der Enabler. Kein Code-Konflikt: Code der 3 ist fertig+ausgerollt, offen ist nur ihre Abnahme -> alle 4 gemeinsam auf migriertem `dtb-assistant` abnehmen |
| Slug bei Kollision | Abbruch vs. Auto-Rename | **Abbruch** | sicherer; Benutzer entscheidet Umbenennung bewusst |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [x] 1.1 DERIVED_STATE_RULES.md umschreiben — `de486a5`
- [x] 1.2 Doku nachziehen (CLAUDE.md x2) — `de486a5`
- [x] 1.3 Slug-Ableitungsregel — `de486a5`
- [x] 2.1 feature-discover + feature-plan — `48b0879`
- [x] 2.2 impl-plan + feature-start — `48b0879`
- [x] 2.3 bug-report + task + project-init — `48b0879`
- [x] 3.1 workflow-resume + -next + -status — `b6f1a8c`
- [x] 3.2 backlog-status + project-health — `b6f1a8c`
- [x] 3.3 plan-review + debug-plan — `b6f1a8c`
- [x] 4.1 archive auf Ordner-Verschieben (+ Bash, Git-/Non-Git) — `e0de0d5`
- [x] 4.2 Migrations-Helfer Erkennung + Kernlogik (Git/Non-Git, Backup) — `e0de0d5`
- [x] 4.3 Migrations-Helfer Namens-Taxonomie + Archiv + Drift-Report — `e0de0d5`
- [x] 5.1 Sicherungspunkt + Dogfood-Migration dieses Kits — `080b556`
- [x] 5.2 Unabhaengige Multi-Varianten-Abnahme (inkl. Non-Git) — `ee84481`
- [x] 5.3 Konsistenz-Sweep + Budget-Check + kit-sync — `2dfce5f` (kit-sync global, Lock 2dfce5f)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_CHANGE_FOLDER_MODELL.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
