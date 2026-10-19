# Review-Snapshot: triage-vorsortierung
Scope: skills/dtb-idea-triage/SKILL.md, workflow.config.yaml, CLAUDE.md, DERIVED_STATE_RULES.md, skills/CLAUDE.md, skills/dtb-{idea,idea-rank,lesson,open-question}/SKILL.md, probelauf-{testprojekt,becken}.md · Geprueft bis: `d613277` · Datum: 2026-10-18
Gesamt-Verdikt: REJECTED

> Zweitreview nach der Triage vom 2026-10-16 (F1–F10 FIXED in `d613277` — Snapshot dieses Laufs per `git show d613277:dtb-project/project-workflows/features/triage-vorsortierung/review.md`). Scope = Progress-SHAs `f0f7a45`, `d6eb24c`, `9004f2c`, `604e06d` plus Review-Fix-Commit `d613277`.

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-idea-triage/SKILL.md:147-151 vs. 644-650 — Existenzprobe ueberspringt nur den Traeger; 7d archiviert die Glieder trotzdem „gebuendelt in #T", obwohl #T nie in INBOX.md steht (Verweis ins Leere, Vorgang verloren).
Fix: In 7d.1 gescheiterte Existenzprobe des Traegers wie Duplikat-Treffer behandeln — Buendel aufloesen, Glieder einzeln nach Schritt 6.
Decision: FIXED

### F2 — Plan Adherence — [S:Mittel × I:Hoch]
probelauf-testprojekt.md, probelauf-becken.md — Probelaeufe 4.2/4.3 belegen den Stand vor den Fixes (gegen 9004f2c/604e06d); probelauf-becken.md zeigt noch Mega-Buendel B3; die Buendelregel nach F1 ist nur simuliert.
Fix: Wirklauf Testprojekt gegen d613277 wiederholen; probelauf-becken.md um Vermerk „B3 durch Review-F1 behoben" + Simulationsergebnis ergaenzen.
Decision: FIXED

### F3 — Plan Adherence — [S:Mittel × I:Mittel]
spec.md:27-28, :52; plan.md Schritt 1.3 — Spec/Plan beschreiben den Vor-Fix-Stand (transitive Huelle, Einzelfaelle „nur Unklar/Verwerfen unter hoch", Stufe 2 ohne Option 0, Lektions-Dublette „wird verworfen").
Fix: spec.md an den Ist-Zustand angleichen; in Plan 1.3 einen Abweichungs-Vermerk („durch Review-F1 ersetzt") statt Umschreiben.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:423 vs. 712-736 — „Groessen gelten auch in Schritt 8" stimmt nicht: {N} steht dort fuer mehrere Zaehler, {B}/{G}/{R} weichen nach Aufloesung/erneuter Kappung/Ueberspringen ab; verschobene und gekappte Zeilen fehlen in R.
Fix: Satz auf Schritt 5 beschraenken; Schritt 8 eigene Ist-Platzhalter („tatsaechlich geschrieben"), R nach der erneuten Kappung.
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:373-379 vs. 524-528 — 4c macht aus einer unscharfen Lektions-Dublette „Verwerfen"; in Stufe 2 ist der Lektions-Weg nicht mehr waehlbar — ein Falsch-Treffer ist nicht ueberstimmbar (verletzt „unscharf → fragen").
Fix: Fuer 4c-Zeilen in Stufe 2 Option 0 „Lektion trotzdem erfassen → 7f"; Grund „Lektion L{N} deckt ab".
Decision: FIXED

### F6 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:559-560, 607-610 — „Ziel vor Quelle" laesst nach Abbruch ein Doppel am Ziel; Heilung nur ueber den unscharfen Check des Folgelaufs (7b: zweite Zeile im append-only-Archiv, 7e: doppelter Nachtrag).
Fix: Vor jedem Schreiben exakte Probe „#N steht schon am Ziel"; bei Treffer nur Quelle entfernen + eine Meldezeile.
Decision: FIXED

### F7 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:758-762, skills/dtb-idea/SKILL.md:146 — vier neue Abgaenge nehmen die Nummer aus beiden gezaehlten Dateien; war sie das Maximum, wird sie erneut vergeben (Kollision mit Archiv-Zeile und Logs).
Fix: `#`-Spalte von archive/INBOX-BEFUNDE-verworfen.md in die Max-Berechnung aufnehmen (Schreibmechanik + Spiegel in dtb:idea).
Decision: FIXED

### F8 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-triage/SKILL.md:152-153, 754 — „Becken-Datei fehlt" laesst offen, ob weiter Ziele geschrieben werden; :754 laedt zum Neuanlegen ein.
Fix: Becken fehlt → Existenzprobe fuer alle restlichen Funde gescheitert → nichts mehr schreiben, nur Bilanz.
Decision: FIXED

### F9 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-triage/SKILL.md:389-390 vs. 656-658 — `Nachtrag #Z` mit #Z in der Sichtungsmenge ist reihenfolgeabhaengig.
Fix: In 4d analog zur Dubletten-Regel: `Nachtrag #Z` mit #Z in der Sichtungsmenge → Einzelfall.
Decision: FIXED

### F10 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-triage/SKILL.md:524-528 mit 656-658 — scheitert Option 0 (Nachtrag) in Stufe 2, geht der Fund „nach Schritt 6", wo er schon ist; Position und Kappung undefiniert.
Fix: Ziel-Pruefung aus 7e.1 vor dem Anbieten von Option 0; nicht offen → Option 0 nicht anbieten.
Decision: FIXED

Unterhalb des Caps (7): verschobene Zeilen ohne Meldezeile (↪) · Wortlaut nach F5/F6 nicht nachgezogen (Zwangsentscheidung :544, Einleitung, description, skills/CLAUDE.md Zeile F, CLAUDE.md:51) · 4b.1-Hinweis „verwandt" ohne Slot · idea-triage fehlt in Voll-Guard-Tabelle und Lesestand-Spiegelliste in skills/CLAUDE.md (Lesestand-Sektion weicht zudem von der gespiegelten 3-Schritte-Struktur ab) · „streichen" mit drei Bedeutungen · zwei Fachfrage-Markierungen (`Fachfrage: ` vs. `[Fach-Frage ohne Ablage-Ort]`) · tote Zweige (Leer-Meldung, 4b.4, idea-Bedingung in 4a).

## Triage 2026-10-18/19

10 Fixed · 0 Lesson · 0 Skipped (F1, F5, F7, F8, F9, F10 einzeln — FAIL-Achse Safety & Quality; F2, F3, F4, F6 als Sammelliste „Alle uebernehmen"). Fixes im Working Tree, nicht committet.

- F1: 7d.1 loest das Buendel auch bei gescheiterter Existenzprobe des Traegers auf (Zusatztest Z1)
- F5: 4c-Umwandlung bekommt in Stufe 2 Option 0 `Lektion trotzdem erfassen → lessons.md`
- F6: neue Regel „Exakte Ziel-Probe" in Schritt 7 (Nummer UND Befund-Text, je Teilschritt; Zusatztest Z2)
- F7: Nummernkreis ueber drei Quellen inkl. `#`-Spalte des Verworfen-Archivs — Schreibmechanik + Spiegel in `dtb:idea` (Zusatztest Z3: alte Regel haette #17 erneut vergeben)
- F8: verschwundenes Becken beendet den Lauf, nichts mehr schreiben (Zusatztest Z4)
- F9: 4d — `Nachtrag #Z` mit #Z in der Sichtungsmenge → Einzelfall
- F10: Ziel-Pruefung aus 7e.1 vor dem Anbieten von Option 0
- F4: Schritt 8 mit eigenen Ist-Platzhaltern (`{n_…}`), Zeile „Uebersprungen", R nach erneuter Kappung
- F3: spec.md (Bündel, Einzelfälle, Stufe 2, Lektions-Dublette) und Plan 1.3 (Abweichungs-Vermerk) angeglichen
- F2: Wiederholungslauf `tp2` (14 Funde, Agent neu, Mensch bestaetigt Sammelliste + 3 Einzelfaelle) + Zusatztests Z1–Z4 + Schreibtisch F5/F9/F10 → `probelauf-testprojekt.md` „Wiederholungslauf 2026-10-18/19"; B3-Vermerk in `probelauf-becken.md`
- Gegenprobe der Beschreibungen (L16): `skills/CLAUDE.md` Zeile F (Nachtrag im selben Lauf) und Zwei-Becken-Regel (Nummernkreis), Root-`CLAUDE.md` Zeilen 51 und 90
- Automated-Kriterien Phasen 1–4 nach der Triage erneut ausgefuehrt (L13): 21/21 gruen

Neu unterhalb des Caps (aus F2-Lauf): **B1** — Lektions-Dublette hat keinen eigenen Vorschlag im Agenten-Auftrag; der Agent schrieb `Verwerfen: Dublette #1` fuer L1 (Vorschlag: `Verwerfen: Lektion L{N}` in 3b).

