# Bug: project-init seedet veraltete DERIVED_STATE_RULES.md

**Erstellt:** 2026-07-10
**Severity:** Hoch
**Status:** Offen
**Betroffene Komponente:** `skills/dtb-project-init/SKILL.md` (Abschnitt „Regel-Datei verteilen (Seed)", Z. ~231-235)

---

## Symptom

Beim Ausführen von `/dtb:project-init` in einem Zielprojekt entsteht eine **veraltete**
`DERIVED_STATE_RULES.md` (86 Zeilen, altes „§"-Flach-Modell) statt der aktuellen Kit-Version
(162 Zeilen, Change-Folder-Modell mit §1.1-Tabelle, §4 Slug-Regeln, §1.5 Bug/Task-Ableitung).
Die derived-state- und die neuen Eligibility-Gate-Skills lesen damit **falsche Regeln** —
still, ohne Fehler. Verifiziert in Projekt `pkp` (2026-07-10): geseedeter Hash `d4517110`
statt Kit-Hash `a7961f7e`.

## Erwartetes Verhalten

`project-init` kopiert die **aktuelle** `DERIVED_STATE_RULES.md` aus dem Kit-Repo unverändert
(byte-/hashgleich) nach `{config.paths.rules}/DERIVED_STATE_RULES.md`.

## Reproduktion

1. In einem Zielprojekt-Ordner (nicht dem Kit-Repo) eine Claude-Code-Session öffnen
2. `/dtb:project-init` ausführen, Bootstrap-Artefakte anlegen lassen
3. `kithash` der erzeugten `dtb-project/project-rules/DERIVED_STATE_RULES.md` mit der
   Kit-Repo-Version vergleichen → weicht ab (veraltete Rekonstruktion)

## Kontext

- **Ursache:** Der Skill sagt „kopiere aus dem Kit-Repo `dtb-project/project-rules/DERIVED_STATE_RULES.md`",
  gibt aber **keinen auflösbaren Pfad** an. In einer Zielprojekt-Session ist das Kit-Repo nicht der
  cwd → das Modell rekonstruiert die Datei aus dem Gedächtnis (veraltet) statt sie zu lesen.
- **Lösungsrichtung:** Seed-Quelle über `~/.claude/dtb-lock.json` → `localPath` als **absoluten
  Pfad** auflösen und die Datei von dort lesen/kopieren; danach optional Hash-Verifikation gegen
  die Quelle. (Klasse-B-Seeds sind nicht kit-sync-drift-geprüft — die Robustheit muss in project-init liegen.)
- **Blast-Radius:** jede Neu-Initialisierung / Re-Initialisierung eines Projekts.
- **Workaround:** `DERIVED_STATE_RULES.md` nach dem Init manuell aus dem Kit-Repo kopieren (in `pkp` geschehen).
- **Erstmals bemerkt:** 2026-07-10 beim Aufsetzen von `pkp` als Testbett für Eligibility-Gates.
- **Frequenz:** Immer (bei Init außerhalb einer Kit-Repo-Session).

---

**Erfasst mit:** `/dtb:bug-report`
