# Discovery: Change-Folder-Modell
<!-- resume: done -->

**Erstellt:** 2026-07-09
**Idee-Referenz:** Inbox #7 — "Change-Folder-Modell erwaegen (langfristig): ein Ordner pro Change (features/<name>/ mit fixen Dateinamen spec.md/plan.md/...) statt flacher UPPER_SNAKE-Dateien mit Namens-Pairing; Archivierung = git mv des Ordners, kein Pairing-Drift (Vorbild: 10x context/changes/<id>/). NUR angehen, wenn Idee #1 (Derived State) sich bewaehrt hat — Migration betrifft fast alle Skills"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-feature-discover, -feature-plan, -impl-plan, -bug-report, -task, -project-init | Schreiber: legen Artefakte an — muessten Ordner + fixe Dateinamen schreiben |
| skills/dtb-workflow-resume, -workflow-next, -workflow-status, -backlog-status, -project-health, -plan-review, -debug-plan | Leser/Ableiter: globben nach PLAN_*/FEATURE_*, leiten Status per Namens-Pairing ab |
| skills/dtb-archive | Mover: verschiebt gepaarte Dateien -> wird zu `git mv <ordner>` |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | Regel-Quelle: definiert Pairing + Ableitung (zentraler Angelpunkt) |
| skills/CLAUDE.md, skills/dtb-pipeline-graph, -generate-rules, -docs-extract, -feature-start, -idea | Doku/sonstige: referenzieren Pfad-/Namenskonventionen, teils nur nachziehen |

---

## Anforderungen

### Scope
**Enthalten:**
- Umstellung auf ein Ordner-pro-Change-Modell: `features/<kebab-name>/` mit fixen Dateinamen (`spec.md`, `plan.md`, `discovery.md`, ggf. `bug.md`/`task.md`)
- Change-Name in **kebab-case** (nicht mehr UPPER_SNAKE) — Ordner macht Unterscheidbarkeit unnoetig
- Archivierung = `git mv features/<name>/ archive/<name>/` (kein Pairing-Drift mehr)
- **Echte Migration** der bestehenden 3 aktiven Features + Archiv (Kit als Dogfood-Fall)
- Migration bestehender Zielprojekte: **einmaliger Migrations-Helfer** (dediziertes Kommando/Modus), der flach -> Ordner konvertiert; Skills verstehen nur das neue Layout (kein Dual-Mode)

**Nicht enthalten:**
- Kein Dual-Mode / keine Rueckwaertskompatibilitaet zum flachen Modell (harter Schnitt)
- (offen: INBOX/BACKLOG-Struktur unveraendert? -> in 3d/3e klaeren)

### Gewuenschtes Verhalten
- Change-Ordner in **reinen Namens-Slugs** (kebab-case), **keine** laufenden Nummern (`features/change-folder-modell/`, nicht `0007-...`)
- Ordnername wird beim Anlegen bestaetigt (wie heute der Feature-Name); Skills legen darin die fixen Dateien an
- Orientierung ueber Ordnernamen im `features/`-Verzeichnis; **keine** zusaetzliche Index-Datei (BACKLOG.md bleibt der Index)

### Randfaelle
- **Ungepaarte Dateien** (z.B. `PLAN_X.md` ohne `FEATURE_X.md`): trotzdem Ordner anlegen, aber im Migrations-Report als Drift-Warnung listen. Reine Commit-Features ohne Artefakt (Betriebs-Waechter) werden nicht angefasst (stehen nur im BACKLOG)
- **Namenskollision** (zwei Basis-Namen -> selber kebab-Slug): Migration **abbricht** mit Meldung der kollidierenden Namen; Benutzer benennt Quelle um und startet neu (kein Auto-Rename)
- **Teilabbruch**: Migration **idempotent** — vorhandene Ziel-Ordner ueberspringen, nur Rest migrieren
- **Leere/Teil-Daten**: Ableitung unveraendert (Ordner mit nur `spec.md` -> "Spezifiziert", mit `plan.md` ohne abgehakte Progress -> "Geplant"); voellig leerer Ordner -> ignorieren + Hinweis
- **Archiv**: die 4 flachen `archive/FEATURE_*.md` werden **mitmigriert** (`archive/<name>/spec.md`), damit `archive` nur noch Ordner verschiebt

### Einschraenkungen
- **Kit-Distribution:** geaenderte Skills sind Klasse-A (global via kit-sync, Lock `77f7f7f`); Projekt-Migration laeuft *nach* dem kit-sync-Update. Helfer erkennt selbst, ob ein Projekt noch flach ist -> gefahrlos wiederholbar
- **`git mv` braucht Git-Repo + sauberen Zustand:** Migration prueft vorab `git status`; uncommittete Aenderungen an Betroffenen -> Abbruch mit Hinweis (kein Move+Edit-Mix)
- **500-Zeilen-Budget:** Reader/Writer werden umgeschrieben (Pfad-Logik), nicht nur erweitert; kein Budget-Risiko erwartet
- **`DERIVED_STATE_RULES.md`** (einzige versionierte Datei in project-rules/, von project-init verteilt) muss zuerst umgeschrieben werden (Pairing -> Ordner-Konvention); alle Reader referenzieren sie
- **Vorbedingung erfuellt:** Derived State seit 2026-07-08 abgeschlossen, 4 Sessions konfliktfrei im Einsatz

### Integrationspunkte
- **Kern:** alle 22 gescannten Skills (Reader/Writer/Mover) + `DERIVED_STATE_RULES.md` + `CLAUDE.md` (Output-Locations-Doku)
- **INBOX/BACKLOG bleiben flache Einzeldateien** (pro-Projekt, nicht pro-Change) — nur der `features/`-Bereich wird zu Ordnern
- **Kollision mit offenen Ideen #9 (Frontmatter-/Pfad-Hygiene) und #11 (Greenfield-Redesign):** fassen teils dieselben Skills an, aber #7 aendert Pfade/Namen, die anderen Inhalte/Frontmatter — Reihenfolge klaeren
- **Externe Abhaengigkeiten:** keine (rein interne Datei-/Git-Operationen); `kit-sync` verteilt nur die neuen Skills, ist selbst kein Consumer

---

## Abhaengigkeiten

- **Bestehende Features:** 3 (REVIEW_HAERTUNG, SPEC_HAERTUNG, SKILL_10X_OPTIMIERUNGEN) — alle "Fertig zum Testen", noch nicht abgenommen
- **Konflikt (Timing):** diese 3 haerten inhaltlich genau die Skills, die #7 im Pfad/Namen umbaut. Empfehlung: #7 erst **nach deren Abnahme + `/dtb:archive`** umsetzen (frisches Archiv = direkter Test der Archiv-Migration)
- **Konflikt (Ueberschneidung mit Idee #9, Frontmatter-/Pfad-Hygiene):** beruehrt `pipeline-graph`/`generate-rules`-Pfade — vor oder gebuendelt mit #7 laufen, um doppeltes Anfassen zu vermeiden
- **Ueberschneidung Idee #11 (Greenfield):** nur inhaltlich (Write-Faehigkeit), nicht im Layout — kollisionsarm, unabhaengig

---

## Offene Punkte

- Migrations-Helfer als **eigenes Kommando** (`/dtb:migrate-change-folders`) vs. **Modus in project-init/kit-sync** — im Plan zu entscheiden
- Fixe Dateinamen final festzurren: `spec.md`/`plan.md`/`discovery.md`/`bug.md`/`task.md` — Bug/Task bestaetigt im Scope
- Umsetzungs-Reihenfolge zu #9 (vor/gebuendelt) im impl-plan festlegen

---

**Erstellt mit:** `/dtb:feature-discover`
