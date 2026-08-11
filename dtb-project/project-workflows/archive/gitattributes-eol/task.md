# Aufgabe: .gitattributes fuer deterministische Zeilenenden

**Erstellt:** 2026-08-05
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- archiviert 2026-08-10 (`/dtb:archive`) — die Archivierung IST der Abschluss-Akt nach DERIVED_STATE_RULES.md §1.2. Davor: Erledigt (## Schritte 6/6, §1.5) -->
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

- [x] Scope entscheiden: `* text=auto` fuer alles vs. gezielt `*.md text` / `*.json text` (+ ggf. `*.yaml`/`*.sh`) — Entscheidung des Menschen: `* text=auto`
- [x] `.gitattributes` anlegen und als eigener Commit committen — Datei angelegt + gestaged (Worker), Commit bei Abnahme 2026-08-08: `3de7923`
- [x] Einmal-Renormalisierung: `git add --renormalize .` als **separater** Commit (reiner EOL-Commit, kein Inhalt) — ausgefuehrt: No-op, alle 187 Blobs waren bereits LF; separater Commit entfaellt (waere leer; Abnahme-Probe im Haupt-Repo: `git ls-files --eol` → 0 nicht-LF)
- [x] Auswirkung auf kit-sync pruefen: Renormalisierung kann Content-Hashes der Klasse-A-Dateien aendern → geprueft: Hashes VOR = NACH fuer 3 Stichproben, kein Drift moeglich (kithash strippt CR, Blobs schon LF)
- [x] Verifikation lokal: EOL-Artefakt reproduziert nicht mehr (`git status` sauber nach Checkout/Touch einer betroffenen Datei)
- [x] Andere Maschine: pull + pruefen, dass dort keine Massen-„modified"-Anzeige entsteht; ggf. `/dtb:kit-sync sync` — **erledigt 2026-08-10.** Maschine mechanisch identifiziert (`git branch --list backup/2026-08-03-pre-merge` → Treffer; `core.autocrlf=true`, also die Risikokonfiguration). Arbeitsbaum stand bereits auf `f0c204a` = `origin/master` (0/0), `git status --short` **leer** trotz gemischter Zeilenenden im Working Tree (119 CRLF / 75 LF / 2 mixed) — alle 196 Index-Blobs `i/lf`. Keine Massen-„modified"-Anzeige, damit ist der maschinenspezifische Teil belegt, den kein Clone-Test liefern konnte. Der `ggf.`-Teil war **faellig**: Lock stand hier auf 44 Artefakte @ `3d15d0a` (2026-08-06), `sync` spielte 10 ein (8 Updates + `dtb-worker` + `output-styles/dtb-gezielt.md`) → 46 synchron @ `f0c204a`. Sicherungs-Branch im selben Gang geloescht (`ecb10ea`, war in `master` enthalten).
  - **Vorab-Beleg 2026-08-09 (ersetzt den Schritt NICHT):** Das Konfigurations-Risiko ist ausgeschlossen. Drei frische Clones von `edca1e0` mit `core.autocrlf=true|false|input` zeigten je **0** Eintraege in `git status --short` (WT-EOL: 196×CRLF | 196×CRLF | 196×LF). Basis: alle 196 Index-Blobs sind `i/lf` (`git ls-files --eol`), und der Working Tree der Arbeitsmaschine ist trotz gemischter Zeilenenden (146 CRLF / 49 LF / 1 mixed) sauber. **Offen bleibt allein der maschinenspezifische Teil:** ob dort lokal modifizierte oder ungepushte Dateien mit dem Pull kollidieren — das sieht kein Clone-Test.
  - **Wo ausfuehren:** Nicht ueber „Maschine 2" identifizieren (relative Bezeichnung, aendert je nach Leseort ihre Bedeutung), sondern mechanisch: `git branch --list backup/2026-08-03-pre-merge` — **Trefferzeile = die richtige Maschine**, leere Ausgabe = die Arbeitsmaschine, dort ist nichts zu tun.
  - **Fertige Sequenz (dort ausfuehren, von oben nach unten):**
    ```bash
    git branch --list backup/2026-08-03-pre-merge   # Treffer erwartet, sonst falsche Maschine
    git status --short                              # (A) leer?  -> weiter mit git pull
                                                    #     Eintraege? -> (B) unten zuerst
    git pull
    git status --short                              # muss leer bleiben
    git ls-files --eol | awk '{print $1}' | sort -u # muss nur i/lf zeigen
    git branch -d backup/2026-08-03-pre-merge       # zweite offene Maschinen-Aufgabe, gleicher Gang
    ```
  - **(B) Fall „Pull blockiert" (`local changes would be overwritten`)** — der wahrscheinlichste Stolperstein, weil genau dieses Symptom den Task ausgeloest hat: erst pruefen, ob es echte Arbeit oder ein EOL-Phantom ist — `git diff --stat` (leer trotz „modified" = Phantom). **Phantom** → `git checkout -- .` , dann Sequenz ab `git pull` wiederholen. **Echte Aenderungen** → committen oder stashen, NICHT verwerfen.

## Ergebnis

`.gitattributes` ist committet, der Bestand einmalig renormalisiert, `git status` bleibt
auf beiden Maschinen frei von EOL-Phantom-Diffs, und kit-sync meldet keinen Drift durch
die Renormalisierung. Das Muster „LF-Datei faelschlich modified" tritt nicht mehr auf.

---

**Erfasst mit:** `/dtb:task`
