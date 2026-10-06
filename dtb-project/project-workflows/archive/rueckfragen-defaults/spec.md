# Feature: Rueckfragen-Defaults

**Erstellt:** 2026-09-30
**Ziel:** Rueckfragen der Voll-Schiene, die keine teuer umkehrbare Festlegung tragen, durch sichtbare Vorschlaege mit Veto oder durch stille Defaults ersetzen — nach der verbindlichen Festlegung vom 2026-09-22.
**Prioritaet:** offen (siehe Offene Punkte)
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Station 1 der Autonomie-Achse hat die Rueckfragen der Voll-Schiene ausgezaehlt und am 2026-09-22 je Fragetyp eine Policy festgelegt (`features/rueckfragen-erhebung/erhebung.md` → „## Festlegung 2026-09-22 (verbindlich)"). Dieses Feature setzt die 11 skill-wirksamen Zeilen dieser Festlegung plus fuenf in der Discovery vom 2026-09-30 beschlossene Zusaetze in den Skills um. Ergebnis: weniger Einzelfragen ohne Informationsgewinn, jede Entscheidung mit Folge bleibt sichtbar und beim Menschen.

Leitkriterium (unveraendert aus Station 1): Eine Rueckfrage ist delegierbar, wenn ihre Antwort keine Festlegung traegt, deren Ruecknahme mehr kostet als ein einzelner, lokal umkehrbarer Schreibvorgang.

---

## Scope / Abgrenzung

### Enthalten

**Aus der Festlegung 2026-09-22** (Zeilennummer = Z):

| Z | Stelle | Neues Verhalten |
|---|--------|-----------------|
| 1 | Slug-Vorschlag (`feature-discover` Schritt 5, `feature-fast` Schritt 3) | Vorschlag mit Veto (Textzeile) |
| 2 | Backlog-Frage `task` | entfaellt — Eintrag ohne Frage, Ausnahme Testordner |
| 3 | Backlog-Frage `feature-plan` / `feature-fast` | entfaellt — Eintrag ohne Frage, Ausnahme Testordner |
| 7 | `plan-review` „Anpassungen? (Ja/Nein)" | entfaellt bei Verdikt REVISE/REJECTED — direkt in die Finding-Runde; Findings selbst bleiben einzeln |
| 9 | `implement` Staging bei fremden geaenderten Dateien | Vorschlag mit Veto (Knopf), Default „nur geplantes Set" |
| 10 | `implement` Commit-Message | Vorschlag mit Veto (Knopf) |
| 11 | `implement` Naechste Phase | Default „direkt weiter"; Skill meldet von sich aus, wenn der Kontext knapp wirkt, und bietet den Wiedereinstieg an; Nutzer-„Stopp" jederzeit |
| 13 | `impl-review` Triage | non-blocking Findings in EINER Sammelliste (Knopf), alle auf Fix vorbelegt, einzelne streichbar; blocking Findings weiterhin einzeln |
| 14 | Codebase-Scan-Bestaetigung (`feature-discover` Schritt 2, `impl-plan` 2b) | Vorschlag mit Veto (Textzeile) |
| 15 | `feature-start` „Bereit? Los" | entfaellt — direkt der Einstiegsbefehl |
| 16 | Lektion-Kandidat (`impl-plan`, `debug-plan`) | siehe Zusatz C |

**Zusaetze aus der Discovery 2026-09-30** (ueber die Festlegung hinaus, bewusst beschlossen):

- **A — Bug-Backlog:** `bug-report` traegt ebenfalls ohne Frage ins Backlog ein (gleiche Datenlage wie `task`, in der Erhebung als uebersehener Fall vermerkt).
- **B — Allgemeine Namensregel (Z1):** „Liefert das Feature etwas mit festem Namen, uebernimmt der Slug diesen Namen" — statt der kit-spezifischen Fassung „Kit-Skill → englischer Skill-Name".
- **C — Lektion-Frage entfaellt (Z16):** statt einer Rueckfrage merkt der Skill den Kandidaten mit einer festen, erkennbaren Zeile vor; `workflow-checkpoint` erfasst ihn ueber die Verlustpruefung.
- **D — Form des Manual-Gates (Z8):** Das Gate bleibt beim Menschen und je Phase; es wird aber von Freitext auf eine blockierende Auswahl (passt / Korrekturen) umgestellt (Lehre 2026-07-30: uebersehene Freitext-Frage liess einen Lauf still versanden).
- **E — `feature-start` bei Bugs und Aufgaben:** „Bereit? Los" entfaellt auch dort, wo keine `plan.md` vorliegt.

**Uebergreifend:**

- **Eine einheitliche Veto-Form**, einmal beschrieben, in zwei Varianten: Einzel-Vorschlag und Sammelliste. Jeder Vorschlag ist sichtbar und hat ein eindeutiges „weiter".
- **Bedienform nach Folge:** Knopf (blockierende Auswahl) bei allem, was zu einem Commit fuehrt (Commit-Message, Staging, impl-review-Korrekturen); Textzeile bei Kleinem ohne Commit-Folge (Slug, Scan-Liste).
- **Anzeige statt Frage bei stillen Defaults:** Backlog-Eintrag, Lektion-Vormerkung und Wegfall von „Los" hinterlassen je eine Zeile im Abschluss, z.B. `→ in BACKLOG.md eingetragen (Status: Spezifiziert)` bzw. `→ kein BACKLOG-Eintrag (Testordner)`.
- **Backlog-Regel fuer alle drei Arten:** Feature, Aufgabe und Bug werden eingetragen; Ideen nie (sie bleiben in der Inbox). Testordner-Ausnahme = Ordner-Praefix `zz-test-` oder `abnahmeprobe-`.

### Nicht enthalten

- Arbeiten ganz ohne Menschen: Antwortgeber, Entsperrung des Selbstaufrufs, Autopilot (#98)
- Konfidenz-Mechanik und Anbieterwahl (#99)
- Pane-/Worktree-Stand-Nachfrage (Z4, wird nicht gebaut); Entscheidung ueber #97 (gehoert in `/dtb:idea-review`)
- Inhaltliche Aenderung der Stellen „nie automatisch": Kleinfall-Weiche (Z5), Escape-Hatch (Z6), Manual-Gate als Entscheidung (Z8 — nur die Form aendert sich, Zusatz D), Mismatch-Dialog (Z12), Ueberschreib-Fragen, Kernfragen von `feature-fast`
- Aenderung der `feature-fast`-Sammelvorlage (Z17, bleibt wie sie ist)
- BACKLOG-Spalte „#" (INBOX #107) — beruehrt dieselben Stellen, wird aber separat umgesetzt
- Aenderung der Worktree-Schutzregeln: im Worktree werden zentrale Dateien weiterhin nicht beschrieben, der Backlog-Eintrag geht in den Hand-off

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Ein Vorschlag wird blind mit „weiter" bestaetigt und fuehrt zu einem falschen Commit | Mittel | Mittel | Knopf statt Textzeile bei allem mit Commit-Folge; Vorschlag wird vollstaendig angezeigt; blocking Findings bleiben einzeln |
| Sammelliste der impl-review verleitet zum Durchwinken schwacher Fixes | Mittel | Mittel | Jede Listenzeile nennt Befund und geplanten Fix; einzelne Zeilen streichbar; Datenlage: 6 % wurden bisher nicht uebernommen — die Streichmoeglichkeit bleibt echt |
| Querverweise zwischen Skills brechen (Scan-Form, „feature-plan Schritt 10", Struktur-Anker) | Mittel | Hoch | Schritt-Ueberschriften bleiben stabil; alle Verweisstellen werden beim Umbau gegengeprueft |
| Lektion-Kandidat geht verloren, weil die Session ohne Checkpoint endet | Niedrig | Mittel | Feste Vormerk-Zeile, die die Verlustpruefung erkennt; Verlustpruefung ist ohnehin proaktiv am Session-Ende vorgesehen |
| „Kontext wird knapp" (Z11) wird falsch eingeschaetzt | Mittel | Niedrig | Reine Ablaufwahl, jederzeit umkehrbar; Nutzer-„Stopp" gilt immer |
| Merge-Konflikt mit #107 an denselben Backlog-Zeilen | Mittel | Niedrig | Koordination beim Merge (siehe Offene Punkte) |
| Scope waechst in Richtung #98 | Niedrig | Mittel | Abgrenzung oben; alles ohne Mensch ist ausdruecklich draussen |

---

## Dependencies

### Erforderlich vor Start
- [x] Verbindliche Festlegung 2026-09-22 (Station 1) liegt vor
- [x] Discovery abgeschlossen (`features/rueckfragen-defaults/discovery.md`)

### Referenz-Dokumente
- `dtb-project/project-workflows/features/rueckfragen-erhebung/erhebung.md` — Festlegung (verbindlich), Begruendungstabelle, Abgrenzungskriterium
- `dtb-project/project-workflows/features/rueckfragen-defaults/discovery.md` — betroffene Skill-Dateien, Zusaetze, Randfaelle, Einschraenkungen
- `dtb-project/project-rules/lessons.md` — L64 (bestandenes Gate ≠ nuetzliches Ergebnis), L70 (Lane-Wahl nach Mitrede-Bedarf)
- `skills/CLAUDE.md` — Worktree-Guard und Schreibgrenzen (bleiben unveraendert)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Alle 11 Zeilen der Festlegung (Z1, 2, 3, 7, 9, 10, 11, 13, 14, 15, 16) sind in den betroffenen Skills umgesetzt
- [ ] Die fuenf Zusaetze A–E sind umgesetzt und in den Skills als solche nachvollziehbar
- [ ] Keine der Stellen „nie automatisch" hat ihr Entscheidungsverhalten geaendert (nur Z8-Form nach Zusatz D)
- [ ] Die Veto-Form ist an genau einer Stelle beschrieben; die Skills verweisen darauf oder folgen ihr erkennbar gleich
- [ ] Jeder Vorschlag mit Veto ist sichtbar und hat ein eindeutiges „weiter"; Knopf bei Commit-Folge, Textzeile sonst
- [ ] Jeder stille Default hinterlaesst genau eine Anzeige-Zeile im Abschluss
- [ ] Feature, Aufgabe und Bug landen ohne Frage im Backlog; Testordner (`zz-test-`/`abnahmeprobe-`) nicht; im Worktree geht der Eintrag in den Hand-off
- [ ] Alle Querverweise zwischen Skills (Scan-Form, Backlog-Schritt, Struktur-Anker) stimmen nach dem Umbau
- [ ] Abnahme in einem Testlauf der Voll-Schiene: an keiner der delegierten Stellen erscheint noch eine Einzelfrage ohne Default

---

## Offene Punkte

- **Prioritaet:** wurde in der Discovery nicht besprochen — Hoch, Mittel oder Niedrig?
- **Ort der Veto-Form:** zentral in `skills/CLAUDE.md` mit Verweis aus den Skills (Muster Worktree-Guard) oder je Skill ausformuliert? — in `impl-plan` entscheiden
- **Ort der Namensregel (Zusatz B):** passt die allgemein gefasste Regel in `DERIVED_STATE_RULES.md` §4 (wird an alle Projekte verteilt), oder gehoert sie nur in die Namens-Schritte von `feature-discover`/`feature-fast`?
- **Z11-Formulierung:** woran der Skill „Kontext wird knapp" festmacht und wie er es meldet — konkrete Formel in `impl-plan`
- **Testlauf fuer die Abnahme:** in welchem Projekt (dieses Repo oder das Referenz-Testbett) und mit welchem Probe-Change?
- **#107-Koordination:** wer zuerst fertig ist, dessen Backlog-Zeilenvorlage uebernimmt der andere — beim Merge pruefen

---

**Erstellt mit:** `/dtb:feature-plan`
