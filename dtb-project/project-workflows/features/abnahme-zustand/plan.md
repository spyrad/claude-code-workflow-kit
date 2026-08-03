# Implementierungsplan: Abnahme-Zustand

**Erstellt:** 2026-08-03
**Feature-Spec:** `features/abnahme-zustand/spec.md`
**Geschaetzte Dauer:** ~2,5–3 h (plan-review 2026-08-03: urspruengliche 1,5 h als zu optimistisch bewertet)
**Status:** Reviewed (plan-review 2026-08-03: REVISE → 6 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Kanon: §1.2 aufspalten, Lese-Regel, Archiv-Widerspruch | ~1 h | Geplant |
| Phase 2 | Leser spiegeln + Verifikation am echten Bestand + Distribution | ~1,5–2 h | Geplant |

---

## Ist-Analyse

> Ergebnis der Codebase-Research (Quelle: `discovery.md`, alle Fundstellen am 2026-08-03 gegrept).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §1.2 Z. 50: ein Satz fuer beide Zustaende, Schreiber falsch (`nur via /dtb:archive`). §3-Matrix Z. 147/148 trennt sie korrekt — Zielbild. §1.3 definiert die Konfliktregel, auf die verwiesen werden muss. §7.3 liefert das Formulierungsmuster (Toleranz + Konflikt-Praedikat + Still-Vorrang) |
| `skills/dtb-workflow-next/SKILL.md` | Z. 68 Pipeline-Zeile: `plan.md` alle Checkboxen → "Fertig zum Testen", Vorschlag "Abnahme via `/dtb:workflow-checkpoint`, dann `/dtb:archive`". 0 Treffer fuer "Abgenommen"; Z. 105 traegt bereits das Feld-Konflikt-Praedikat fuers Plan-Kopffeld (Muster) |
| `skills/dtb-backlog-status/SKILL.md` | Schritt 2 Fallback-Liste nennt nur `Pausiert` als ueberschreibend; Template-Abschnitt "Fertig zum Testen / Abgenommen" existiert, aber ohne Regel dahinter |
| `skills/dtb-workflow-resume/SKILL.md` | Schritt 4 leitet nur "In Arbeit" ab (0 < X < Y); Y/Y-Changes fallen in Fall C ("Kein aktives Feature"). 0 Treffer fuer "Abgenommen" |
| `skills/dtb-archive/SKILL.md` | Z. 48 Kandidat-Regel nennt `**Status:** Abgenommen`; Z. 111 setzt beim Verschieben `Abgeschlossen`; Z. 159 Richtlinie zaehlt nur "Verworfen/Ausgearbeitet/Abgeschlossen" — Widerspruch zu Z. 48 |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 2.3 setzt `Abgenommen` nach Beleg-Rueckfrage; verweist auf "Regel-Datei §1.2" — Verweis muss nach der Aufspaltung noch treffen |
| `dtb-project/project-workflows/features/*/spec.md` | 5 Changes tragen `**Status:** Abgenommen` (2026-08-03), 2 tragen `Fertig zum Testen` bei Y/Y — fertiges Testmaterial fuer Positiv- und Negativ-Test |

---

## Phase 1: Kanon — Zustaende trennen und Lese-Regel definieren

### Ziel

§1.2 nennt beide Zustaende getrennt mit je ihrem Schreiber, die Lese-Semantik von `Abgenommen`
ist definiert (inkl. des einen echten Konfliktfalls), und der Archiv-Skill widerspricht sich
nicht mehr selbst.

### Schritte

#### Schritt 1.1: §1.2 in zwei Eintraege aufspalten
- **Zweck:** Den sachlich falschen Satz ersetzen, der beiden Zustaenden denselben Schreiber zuschreibt
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (§1.2)
- **Input:** Bestehender Wortlaut Z. 50; §3-Matrix Z. 147/148 als Zielbild; Nachbareintrag `Pausiert` als Formvorbild
- **Output:** Zwei Eintraege — `Abgenommen` (getestet und freigegeben; Schreiber `dtb:workflow-checkpoint` Schritt 2.3 mit Beleg-Gate; Change bleibt unter `features/`) und `Abgeschlossen` (nur via `dtb:archive`; die Archivierung IST der Akt; 100 % Checkboxen ≠ automatisch abgeschlossen). Additiv, keine §-Nummer verschoben

#### Schritt 1.2: Lese-Regel, Konflikt-Praedikat und Kopplungs-Hinweis ergaenzen
- **Zweck:** Den Lesern eine verbindliche Behandlung geben und die Spiegel benennen, damit kuenftige Aenderungen sie mitziehen
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (§1.2, ggf. Verweis in §1.3)
- **Input:** Muster aus §7.3 (Toleranz-Matrix, positiv definiertes Konflikt-Praedikat, Vorrang der Still-Regel)
- **Output:** Regel „ein gesetztes `Abgenommen` ueberschreibt die Ableitung und ist **kein** §1.3-Konflikt"; Praedikat „Konflikt ist genau eine Kombination: `Abgenommen` gesetzt UND `## Progress` unvollstaendig (< Y/Y)"; fehlender Zustand → still wie abgeleitet; Kopplungs-Hinweis mit Nennung der vier Leser

#### Schritt 1.3: Archiv-Widerspruch und Schreiber-Verweis bereinigen
- **Zweck:** Die interne Inkonsistenz im Archiv-Skill schliessen und pruefen, ob der Schreiber noch auf den richtigen Wortlaut zeigt
- **Dateien:** `skills/dtb-archive/SKILL.md` (Richtlinie Z. 159), `skills/dtb-workflow-checkpoint/SKILL.md` (Verweis in Schritt 2.3)
- **Input:** Z. 48 (Kandidat-Regel) als maßgeblich; neuer §1.2-Wortlaut aus 1.1
- **Output:** Richtlinie nennt `Abgenommen` konsistent mit Z. 48; Checkpoint-Verweis trifft den neuen Wortlaut (praezisiert oder unveraendert bestaetigt — Ergebnis wird notiert)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] §1.2 mit zwei getrennten Eintraegen, je mit Schreiber
- [ ] Lese-Regel + Konflikt-Praedikat + Kopplungs-Hinweis im Kanon
- [ ] Archiv-Richtlinie widerspruchsfrei, Schreiber-Verweis geprueft

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'nur via `/dtb:archive`' DERIVED_STATE_RULES.md` zaehlt genau 1 Treffer, und dieser steht in der `Abgeschlossen`-Zeile (Wirkstelle, nicht dateiweit)
- [ ] §1.2 enthaelt je eine Zeile, die mit `- **Abgenommen**` bzw. `- **Abgeschlossen**` beginnt
- [ ] §-Ueberschriften unveraendert: `grep -c '^## [0-9]\.' ` liefert denselben Wert wie vor der Aenderung
- [ ] `skills/dtb-archive/SKILL.md` nennt `Abgenommen` in der Richtlinien-Aufzaehlung (1 Treffer)

#### Manual
- [ ] Die Aufspaltung liest sich neben dem Nachbareintrag `Pausiert` kohaerent; kein Satz schreibt beiden Zustaenden denselben Schreiber zu
- [ ] Das Konflikt-Praedikat unterdrueckt keinen echten Fehlerfall — eine vorschnelle Freigabe bleibt meldepflichtig
- [ ] Ergebnis des Schreiber-Verweis-Checks (Schritt 1.3) liegt notiert vor — „praezisiert" oder „unveraendert bestaetigt", nicht offen

---

## Phase 2: Leser spiegeln, am echten Bestand verifizieren, verteilen

### Ziel

Alle vier lesenden Skills behandeln `Abgenommen`; die fuenf real freigegebenen Changes erscheinen
korrekt, die beiden nicht freigegebenen unveraendert; die Fassung ist installiert.

### Schritte

#### Schritt 2.1: Naechster-Schritt-Leser haerten
- **Zweck:** Der Skill soll fuer freigegebene Changes keine Abnahme mehr empfehlen
- **Dateien:** `skills/dtb-workflow-next/SKILL.md` (Pipeline-Tabelle Z. 68 + Quellen-/Konflikt-Abschnitt)
- **Input:** Kanon-Wortlaut aus 1.1/1.2; vorhandenes Feld-Konflikt-Praedikat Z. 105 als Formvorbild
- **Output:** Y/Y-Zeile unterscheidet freigegeben von „Fertig zum Testen"; freigegeben → naechster Schritt ist `/dtb:archive` (nicht erneut Abnahme); Konflikt-Praedikat aus 1.2 gespiegelt

#### Schritt 2.2: Backlog-Uebersicht und Wiederaufnahme nachziehen
- **Zweck:** Kein falscher Widerspruchs-Hinweis; freigegebene Changes werden beim Wiederaufnehmen sichtbar
- **Dateien:** `skills/dtb-backlog-status/SKILL.md` (Schritt 2 Fallbacks + Schritt 3 Abgleich), `skills/dtb-workflow-resume/SKILL.md` (Schritt 4 Ableitung)
- **Input:** Kanon-Wortlaut; Bestandsformulierung zu `Pausiert` als Muster
- **Output:** Beide nennen `Abgenommen` als ueberschreibenden Zustand; die Uebersicht meldet ihn nicht als Konflikt; die Wiederaufnahme zeigt freigegebene Changes als eigene Zeile statt sie in „Kein aktives Feature" fallen zu lassen

#### Schritt 2.3: Verifikation am echten Bestand + Distribution
- **Zweck:** Ausfuehrung statt Interpretation — der gehaertete Text laeuft gegen reales Material
- **Dateien:** keine (read-only Laeufe), danach installierte Kopien via `dtb:kit-sync`
- **Input:** 5 freigegebene Changes (Positiv-Test), 2 fertige ohne Freigabe (Negativ-Test), 1 konstruierter Fall „freigegeben bei unvollstaendigem Fortschritt" als **temporaerer Change-Ordner unter `features/`** — die Leser scannen `features/*`, das Scratchpad sehen sie nicht (plan-review 2026-08-03). Untracked lassen, kein Commit; **Aufraeumschritt gehoert zum Test:** Ordner nach dem Lauf loeschen, `git status` zeigt keinen Rest
- **Output:** Erwartungsabgleich dokumentiert; Spiegel-Zaehlung mechanisch belegt; `kit-sync sync` gelaufen, Lock fortgeschrieben, Inhaltskontrolle an je einer Wirkstelle pro geaenderter Datei. **Hinweis fuer den zweiten Rechner notiert** (Checkpoint/Status): dort ist ein eigener `kit-sync sync` noetig — bis dahin verhalten sich die beiden Maschinen bei denselben Artefakten unterschiedlich

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Drei Leser behandeln `Abgenommen` explizit
- [ ] Erwartungsabgleich fuer Positiv-, Negativ- und Konflikt-Test dokumentiert
- [ ] Distribution abgeschlossen, Inhaltskontrolle belegt

### Checkpoint-Kriterien

#### Automated
- [ ] **Kernsatz der Lese-Regel per Grep sinngleich in den 3 Spiegeln** (`workflow-next`, `backlog-status`, `workflow-resume`) — Zielzahl 3/3, woertlicher Kernsatz, nicht Sinn-Aehnlichkeit (plan-review 2026-08-03: von Manual mechanisiert). Gegenprobe: `workflow-status` behandelt `Abgenommen` bereits im Bestand (kein neuer Spiegel noetig)
- [ ] `/dtb:workflow-next`-Lauf im Kit-Repo nennt fuer die 5 freigegebenen Changes **keinen** Abnahme-Vorschlag (0 Treffer auf „Abnahme via")
- [ ] `/dtb:backlog-status`-Lauf gibt **0** Konfliktzeilen fuer die 5 freigegebenen aus
- [ ] Konstruierter Konflikt-Fall (Temp-Ordner) erzeugt **genau 1** Meldezeile; danach ist der Ordner entfernt (`git status` ohne Rest)
- [ ] `kit-sync check` meldet 0 Abweichungen nach der Distribution

#### Manual
- [ ] Negativ-Test bestanden: die beiden fertigen, nicht freigegebenen Changes erscheinen unveraendert als „Fertig zum Testen" — die Haertung hat nicht ueberschossen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Zustand ueberhaupt behalten? | `Abgenommen` abschaffen und beim Abnehmen direkt archivieren; Zustand behalten | Behalten | Die Freigaben tragen dokumentierte Vorbehalte und Beleg-Luecken, die im **aktiven** Bereich sichtbar bleiben muessen, bis sie erledigt sind; Archivierung bleibt ein bewusster zweiter Akt. Direkt-Archivierung waere einfacher, verschoebe aber offene Nacharbeit ins Archiv (Devil's-Advocate-Alternative, plan-review 2026-08-03) |
| Verortung im Kanon | §1.2 aufspalten, eigener Paragraf wie §7 | §1.2 aufspalten | §1.2 ist die Heimat der expliziten Zustaende; ein eigener Paragraf trennte `Abgenommen` von `Pausiert`, obwohl beide dieselbe Mechanik haben (per Veto-Vorlage bestaetigt 2026-08-03) |
| Lese-Semantik | Wie `Pausiert` (ueberschreibt, still), als eigener Sonderfall | Wie `Pausiert` | Gleiche Mechanik, gleiche Behandlung — kein neues Muster fuer denselben Sachverhalt |
| Konfliktdefinition | Negativ (alles ausser X ist Konflikt), positiv (genau eine Kombination) | Positiv | §7.3 hat gezeigt, dass ein negativ formuliertes Praedikat undefinierte Faelle hinterlaesst |
| Bestandsbehandlung | Migration aller Specs, Selbstheilung | Selbstheilung | Anzeige-Felder werden beim naechsten Abgleich synchronisiert; Migration erzeugte Aufwand ohne Nutzen |
| Wiederaufnahme-Leser | Anfassen, auslassen | Anfassen (auf `Abgenommen` begrenzt) | Ohne Ergaenzung bleiben freigegebene Changes dort unsichtbar; eine allgemeine Y/Y-Ansicht bleibt aber ausserhalb des Schnitts |
| Verifikationsmaterial | Konstruierte Koepfe, echter Bestand | Beides | Der echte Bestand deckt Positiv- und Negativ-Test kostenlos ab; der Konfliktfall kommt real nicht vor und braucht einen temporaeren Change-Ordner unter `features/` (nicht Scratchpad — wird nicht gescannt; nicht als bleibende Fixture — wuerde jeden kuenftigen Report verschmutzen; plan-review 2026-08-03) |
| Roadmap-Ableitung (§5) | Um den Zwischenzustand erweitern, ausschliessen | Ausschliessen | `ROADMAP.md` ist im Kit-Repo ein reiner Platzhalter (bestaetigt 2026-08-03) — keine reale Verifikationsbasis; bewusster Ausschluss in der Spec, offener Punkt bleibt als Wiedervorlage (plan-review 2026-08-03) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `dtb-project/project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 §1.2 aufspalten — `7844bc4`
- [x] 1.2 Lese-Regel + Konflikt-Praedikat + Kopplungs-Hinweis — `7844bc4`
- [x] 1.3 Archiv-Widerspruch + Schreiber-Verweis — `7844bc4`
- [x] 2.1 Naechster-Schritt-Leser haerten
- [x] 2.2 Backlog-Uebersicht + Wiederaufnahme nachziehen
- [ ] 2.3 Verifikation am echten Bestand + Distribution

---

## Umsetzung

Umsetzung mit `/dtb:implement Abnahme-Zustand` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-03)
