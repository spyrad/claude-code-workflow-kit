# Bug: project-init seedet veraltete DERIVED_STATE_RULES.md

**Erstellt:** 2026-07-10
**Severity:** Hoch
**Status:** Abgeschlossen — Behoben (Fix umgesetzt, lokal verifiziert, verteilt; realer Abnahme-Test bestanden 2026-07-10; archiviert 2026-07-13)
**Betroffene Komponente:** `skills/dtb-project-init/SKILL.md` (Abschnitt „Regel-Datei verteilen (Seed)", Z. ~231-236)

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

## Analyse

**Analysiert:** 2026-07-10
**Status:** Offen → Analysiert

### Root-Cause-Hypothesen

| # | Hypothese | Wo (Datei:Zeile) | Evidenz | Staerke |
|---|-----------|------------------|---------|---------|
| 1 | Seed-Anweisung nennt **keinen auflösbaren (absoluten) Pfad** → Modell rekonstruiert die Regel-Datei in Zielprojekt-Sessions aus dem Gedächtnis (veraltet) statt sie zu lesen | `skills/dtb-project-init/SKILL.md:231-236` | Text „Quelle: Kit-Repo `dtb-project/project-rules/DERIVED_STATE_RULES.md`" — relativer, in Nicht-Kit-cwd nicht auflösbarer Pfad; kein Bezug auf `lock.localPath`. In `pkp` belegt (Hash `d4517110` ≠ Kit `a7961f7e`) | STRONG |
| 2 | „Kopiere" ohne mechanischen Zwang (Bash `cp`) lädt zum Nach-Schreiben-aus-Gedächtnis ein statt zu byte-genauem Kopieren | `skills/dtb-project-init/SKILL.md:231` | Verb „Kopiere" + generierende Template-Umgebung (umliegende Blöcke werden erzeugt, nicht kopiert) | WEAK |

Je Hypothese ergaenzend:
- **H1 — Begruendung:** Kit-Repo ist in einer Zielprojekt-Session nicht cwd → relativer Pfad zeigt ins Leere → Modell füllt aus dem Gedächtnis (alte 86-Z.-Flach-Version). **Pruefung:** in `pkp` bereits belegt (Hash-Diff).
- **H2 — Begruendung:** Auch mit korrektem Pfad kein byte-genauer Transfer garantiert, solange kein mechanischer Kopiervorgang vorgeschrieben ist. **Pruefung:** Hash-Vergleich Quelle↔Ziel nach Fix.

Der Fix adressiert beide Hypothesen: Quelle absolut über `lock.localPath` auflösen **und** mechanisch (Bash `cp`) kopieren + Hash-Verifikation.

---

## Fix-Schritte

- [x] `skills/dtb-project-init/SKILL.md` Abschnitt „Regel-Datei verteilen (Seed)" (Z. ~231-236) umschreiben: Seed-Quelle **mechanisch** ermitteln — `localPath` aus `~/.claude/dtb-lock.json` lesen und den **absoluten** Quellpfad `<localPath>/dtb-project/project-rules/DERIVED_STATE_RULES.md` per Bash `cp` (kein Neu-Schreiben aus dem Gedächtnis) nach `{config.paths.rules}/DERIVED_STATE_RULES.md` kopieren. Beispiel-Bash-Block eingefügt.
- [x] **Hash-Verifikation** ergänzt: nach dem Kopieren Quelle↔Ziel per `git hash-object` vergleichen; bei Abweichung Warnung (kein stiller Fehlschlag). Lokal verifiziert: Kopie hashgleich (`a7961f7e…`).
- [x] **Fallback (ehrliche Meldung, keine Rekonstruktion):** Lock fehlt / `localPath` leer / Quelldatei nicht lesbar → Seed **abbrechen** mit klarer Meldung + manueller Kopier-Hinweis. Niemals aus dem Gedächtnis rekonstruieren. Fallback-Zweig lokal getestet.
- [x] Nach dem Fix: da `skills/dtb-project-init/SKILL.md` **Klasse A** ist (`skills/dtb-*/SKILL.md`) → Commit nach `origin/master` pushen und `/dtb:kit-sync sync` (Lock-Update), damit die installierte Kopie unter `~/.claude/` den Fix erhält. Erledigt: Commit `96eb2df` gepusht + Sync (Lock `8c1c906 → 96eb2df`, `updatedAt 2026-07-10`).

**Regressionsrisiko:** Gering. Der Seed hängt nun an der Lock-Existenz — project-init prüft den Lock aber bereits in Schritt 0 (Hinweis bei Fehlen). Windows-`localPath` steht mit Forward-Slashes (`C:/…`) im Lock → Bash `cp` verarbeitet ihn direkt; kein Pfad-Umbau nötig. Kein Einfluss auf die übrigen Init-Schritte (Config, Verzeichnisse, CLAUDE.md).

## Testplan

- [x] **Repro/Fix-Beleg:** in einem frischen Zielprojekt (oder erneut in `pkp`) `/dtb:project-init` laufen lassen → `git hash-object dtb-project/project-rules/DERIVED_STATE_RULES.md` == Kit-Quell-Hash (`a7961f7e` bzw. aktueller Kit-Hash). **Bestanden 2026-07-10** (realer Abnahme-Test durch Nutzer).
- [ ] **Regression Lock-Fehlt:** `~/.claude/dtb-lock.json` temporär unauffindbar → Seed bricht mit ehrlicher Meldung ab, erzeugt **keine** veraltete Datei.
- [ ] **Regression Rest-Init:** Config, Verzeichnisstruktur und CLAUDE.md-Sentinel-Block unverändert korrekt.

---

**Analysiert mit:** `/dtb:debug-plan`

---

**Erfasst mit:** `/dtb:bug-report`
