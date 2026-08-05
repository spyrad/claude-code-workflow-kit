# Aufgabe: .gitattributes fuer deterministische Zeilenenden

**Erstellt:** 2026-08-05
**Prioritaet:** Mittel
**Status:** Offen
**Bereich:** Repo-Infrastruktur (Git-Konfiguration, betrifft alle Textdateien + kit-sync-Distribution)

---

## Beschreibung

`.gitattributes` im Repo-Root ergaenzen, damit Zeilenenden deterministisch normalisiert
werden (`* text=auto` bzw. gezielt `*.md text` / `*.json text`) und anschliessend den
Bestand einmalig renormalisieren. Scope-Entscheidung (alles vs. nur Markdown/JSON) ist
Teil der Aufgabe.

## Begruendung

Bei `core.autocrlf=true` **ohne** `.gitattributes` flaggt Git LF-Dateien als „modified"
(LF↔CRLF), obwohl der Inhalt unveraendert ist. Erstbefund 2026-07-18 an
`DERIVED_STATE_RULES.md` (`git diff` leer, reines EOL-Artefakt, per `git checkout --`
geklaert); seither wiederholt aufgetreten — **10 dokumentierte Belege** (Stand der Weiche
2026-08-02, s. Session-Logs). Ohne Fix erzeugt jedes Auftreten Phantom-Diffs, die
`git status`-basierte Skill-Schritte (`workflow-resume`, `commit-and-push`) verrauschen
und manuellen Klaeraufwand kosten.

## Schritte

- [ ] Scope entscheiden: `* text=auto` fuer alles vs. gezielt `*.md text` / `*.json text` (+ ggf. `*.yaml`/`*.sh`)
- [ ] `.gitattributes` anlegen und als eigener Commit committen
- [ ] Einmal-Renormalisierung: `git add --renormalize .` als **separater** Commit (reiner EOL-Commit, kein Inhalt)
- [ ] Auswirkung auf kit-sync pruefen: Renormalisierung kann Content-Hashes der Klasse-A-Dateien aendern → `/dtb:kit-sync check`, bei Drift-Meldungen `sync` nachziehen
- [ ] Verifikation lokal: EOL-Artefakt reproduziert nicht mehr (`git status` sauber nach Checkout/Touch einer betroffenen Datei)
- [ ] Andere Maschine: pull + pruefen, dass dort keine Massen-„modified"-Anzeige entsteht; ggf. `/dtb:kit-sync sync`

## Ergebnis

`.gitattributes` ist committet, der Bestand einmalig renormalisiert, `git status` bleibt
auf beiden Maschinen frei von EOL-Phantom-Diffs, und kit-sync meldet keinen Drift durch
die Renormalisierung. Das Muster „LF-Datei faelschlich modified" tritt nicht mehr auf.

---

**Erfasst mit:** `/dtb:task`
