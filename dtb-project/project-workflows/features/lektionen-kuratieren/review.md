# Review-Snapshot: lektionen-kuratieren
Scope: skills/dtb-lesson-curate, dtb-lesson, dtb-project-dashboard, dtb-project-init, skills/CLAUDE.md, CLAUDE.md, README.md, workflow.config.yaml, lessons.md (Kopf), Change-Ordner (13 Dateien, 4 Commits) · Geprueft bis: `9ab1fd0` · Datum: 2026-10-28
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-lesson-curate/SKILL.md:484-492 — Zuruecklesen erwartet fest `SPALTEN 8`; L17 und L36 (unescapte Pipes in Backticks) ergeben 9 → korrekter Archiv-Eintrag gilt als Schreibfehler, Durchgang bricht ab; 1c heilt dieselbe Zeile spaeter per `GLEICH`
Fix: 6b.2 prueft `ANZAHL 1` und woertliches Enthaltensein der Lektionszeile (`grep -qF -- "$z"`, wie 1c) statt fester Spaltenzahl
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-lesson-curate/SKILL.md:475-477 — 6b.1 springt bei „Nummer schon im Archiv" nur nach Nummer zur Entnahme, ohne Inhaltsvergleich (1c verlangt ihn); Ueberbleibsel der alten Selbstheilungs-Stelle
Fix: Bei Nummern-Treffer den 1c-Vergleich ausfuehren; nur `GLEICH` → Entnahme, sonst Schreibfehler
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-lesson-curate/SKILL.md:278-285, 433-435 — Ketten-Paar: wird L{M} zuerst ausgemustert, bietet L{N} weiter `doppelt zu L{M}` bzw. „Die andere ausmustern" an → falscher Archiv-Grund bzw. Schreibfehler
Fix: 3b: Ist ein Paar-Partner ausgemustert, faellt der andere fuer diesen Lauf auf behalten (eine Zeile), naechster Lauf prueft neu
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-lesson-curate/SKILL.md:176, 313, 332 — `{nummern}` mit drei Bedeutungen und zwei Formaten; Kommaform in 3f liefert 0 Bytes → „Einsparung 0 KB" ohne Warnung
Fix: `{portion}` / `{vorschlaege}` / `{vorgelegt}`, 3f leerzeichengetrennt, Gate: Vorschlaege > 0 und Ausgabe 0 → `—` + ⚠-Zeile
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-lesson-curate/SKILL.md:369-371 — Sammelliste kuerzt den Beleg auf ~40 Zeichen und verweist auf eine Uebersicht ohne Einzelzeilen; Zeilennummer (Kriterium fuer „Alle uebernehmen") kann wegfallen
Fix: Beleg nie kuerzen (nur Grund), Verweis auf die Uebersicht streichen
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-lesson-curate/SKILL.md:101-104, 347-351 — doppelte Nummer in lessons.md: 1a zaehlt beide, Analyse eine → Mengenprobe scheitert bei jedem Lauf ohne Diagnose
Fix: 1a meldet `MEHRFACH {n}`; Nummern aus der Analysemenge nehmen, als eigenen Topf zaehlen, „von Hand klaeren"
Decision: FIXED

### F7 — Plan Adherence — [S:Niedrig × I:Mittel]
skills/dtb-lesson-curate/SKILL.md:18 — `consumes` ohne `skills/CLAUDE.md` (Plan 1.1 nennt es, Skill liest es als Hebe-Ziel)
Fix: `skills/CLAUDE.md` in `consumes` ergaenzen
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-lesson-curate/SKILL.md:340, 532-533 — „ueber der Schwelle" gegen `KB ≥ schwelle_kb` in dtb:lesson/Dashboard; bei genau 40 KB fehlt die Bilanz-Zeile
Fix: In 3f und 7 die Bedingung woertlich `KB ≥ schwelle_kb`
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-lesson/SKILL.md:213 — Mess-Block mit `{config.paths.rules}` statt aufgeloestem Pfad inkl. Fallback
Fix: `{rules}` wie in den Spiegel-Skills, in Schritt 0 benennen
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-lesson-curate/SKILL.md:418 — Zaehler `Einzelfall {i}/{E}` nutzt `{E}` aus 3f; gestrichene und entfallene Faelle verfaelschen ihn
Fix: Eigener Nenner = gestrichene + vorgelegte Einzelfaelle, beim Entfallen neu gezaehlt
Decision: FIXED

Unter dem Cap: Plan 2.2 — Einzelfall zeigt die gekuerzte Rule statt der „Lektion im Wortlaut" (durch abgenommene Probe-Zielform gedeckt).
