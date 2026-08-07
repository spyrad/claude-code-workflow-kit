# Implementierungsplan: Output-Style „gezielt"

**Erstellt:** 2026-08-07
**Feature-Spec:** `features/output-style-gezielt/spec.md`
**Geschaetzte Dauer:** 2-3 Sessions
**Status:** Reviewed (plan-review 2026-08-07: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Style-Datei bauen | 0.5 Session | Geplant |
| Phase 2 | Distribution: neue kit-sync-Klasse + Spiegel-Kopplung | 1 Session | Geplant |
| Phase 3 | Aktivierung, project-health-Check, Kalibrier-Abnahme | 1 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Pfade verifiziert 2026-08-07), ergaenzt um Detail-Befunde aus dem Lesen
> von `kit-sync` und `project-health` bei der Planerstellung.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `output-styles/` | **Neubau** — existiert weder im Repo noch als `~/.claude/output-styles/` auf dieser Maschine |
| `skills/dtb-kit-sync/SKILL.md` | Klassen-Tabelle Z. 72-77 (3x Klasse A + 1x Seed). check-Schritt 3 arbeitet generisch „gemaess Klassen-Tabelle" ✓. **Aber:** Verwaisten-Erkennung (Schritt 5) nennt „die drei Zielverzeichnisse" (Z. 147) und erkennt Altbestand nur an der `dtb-*`-Praefix-Heuristik — eine vierte Klasse muss beide Stellen mitziehen. Zustand „neu" (Z. 142) + sync-Buendel 1 (Z. 218) beantworten die Lock-Frage der Spec: Repo-Datei ohne Lock-Eintrag wird als „neu" erkannt und installiert |
| `skills/CLAUDE.md` | `## Distribution (kit-sync)` Z. 214-215 listet die Klasse-A-Muster (Spiegel der Klassen-Tabelle); kein Output-/Stil-Abschnitt vorhanden |
| `skills/dtb-project-health/SKILL.md` | 11 Checks; Check 11 (Kit-Drift) iteriert generisch „pro `mode: synced`-Eintrag im Lock" — erfasst die neue Klasse automatisch ✓. Neuer Aktivierungs-Check waere Check 12 |
| `CLAUDE.md` (Root) | Z. 21-22 nennt die Klasse-A-Muster explizit (zweiter Spiegel); Z. 80-81 dokumentiert das Muster-Prinzip am Beispiel `commands/` |

---

## Phase 1: Style-Datei bauen

### Ziel
Die Stil-Datei liegt versioniert im Kit-Repo: Leitsatz, Ausnahme-Klausel, Vorrang-Regel,
korrektes Frontmatter, ≤ 40 Zeilen.

### Schritte

#### Schritt 1.1: Verzeichnis + Datei anlegen
- **Zweck:** Das Kit-Artefakt entsteht an seiner Quelle
- **Dateien:** `output-styles/dtb-gezielt.md` (neu)
- **Input:** Spec (Leitsatz, Klauseln), Frontmatter-Felder aus der Doku-Verifikation in `discovery.md`
- **Output:** Datei mit Frontmatter `name: Gezielt`, `description`, **`keep-coding-instructions: true`** (Pflicht — Risiko „sehr hoch" in der Spec)

#### Schritt 1.2: Inhalt ausformulieren
- **Zweck:** Die drei Bausteine der Spec in wirksame Anweisungen uebersetzen
- **Dateien:** `output-styles/dtb-gezielt.md`
- **Input:** Leitsatz (worum geht es / Stand bzw. Problem / verlangte Entscheidung; kurz, knapp, einfach — reduziert, nicht weggelassen), Ausnahme-Klausel (ausdrueckliche Bitte um Analyse/Begruendung/Vergleich hebt die Beschraenkung auf), Vorrang-Regel (Skill-Ausgabeformat schlaegt Stil)
- **Output:** Ausformulierter Body, deutsch, gesamt ≤ 40 Zeilen

#### Schritt 1.3: Selbst-Review gegen die Spec
- **Zweck:** Vollstaendigkeit der drei Bausteine + Substanz-Schutz (keine Anweisung, die Belege/Zahlen kuerzt)
- **Dateien:** `output-styles/dtb-gezielt.md` (nur Korrekturen)
- **Input:** Spec-Abschnitte Scope/Nicht-enthalten
- **Output:** Datei final fuer Phase 1; Abweichungen im Chat vermerkt

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `output-styles/dtb-gezielt.md` — versioniert, vollstaendig, ≤ 40 Zeilen

### Checkpoint-Kriterien

#### Automated
- [ ] Datei existiert: `ls output-styles/dtb-gezielt.md`
- [ ] `grep -c "keep-coding-instructions: true" output-styles/dtb-gezielt.md` = 1
- [ ] Zeilenzahl ≤ 40: `wc -l output-styles/dtb-gezielt.md`
- [ ] Alle drei Bausteine im Body verankert: je 1 Grep auf Kernbegriff von Leitsatz („Entscheidung"), Ausnahme-Klausel („Analyse"), Vorrang-Regel („Ausgabeformat") — Anker ist der Datei-Body, nicht das Repo (Lektion 2/8)

#### Manual
- [ ] Formulierungen vom Nutzer freigegeben (es ist SEINE Stil-Vorgabe)

---

## Phase 2: Distribution — neue kit-sync-Klasse + Spiegel-Kopplung

### Ziel
`kit-sync` erfasst `output-styles/*.md` als Klasse-A-**Muster**; alle drei Spiegel-Stellen sind
konsistent; ein sync-Lauf verteilt die Datei mit 0 Abweichungen.

### Schritte

#### Schritt 2.1: Klassen-Tabelle + Verwaisten-Logik in kit-sync erweitern
- **Zweck:** Die neue Klasse mechanisch verankern — an ALLEN Stellen, nicht nur der Tabelle
- **Dateien:** `skills/dtb-kit-sync/SKILL.md`
- **Input:** Ist-Befund: Klassen-Tabelle Z. 72-77; Verwaisten-Erkennung Z. 144-150 („drei Zielverzeichnisse", `dtb-*`-Heuristik)
- **Output:** Tabellen-Zeile `A | output-styles/dtb-*.md | ~/.claude/output-styles/dtb-*.md | synced | ja` — Muster bewusst auf `dtb-*` verengt, damit Verteilungs-Muster und Verwaisten-Heuristik dasselbe versprechen (plan-review 2026-08-07, Architekt); Verwaisten-Text auf vier Zielverzeichnisse erweitert

#### Schritt 2.2: Spiegel mitziehen (skills/CLAUDE.md + Root-CLAUDE.md)
- **Zweck:** Spiegel-Kopplung geschlossen halten (`skills/CLAUDE.md` „Kopplungs-Hinweise"; Praezedenz-Risiko der Spec)
- **Dateien:** `skills/CLAUDE.md` (Z. 214-215), `CLAUDE.md` (Z. 21-22)
- **Input:** Neue Klassen-Zeile aus 2.1
- **Output:** Beide Spiegel nennen das Muster `output-styles/*.md`; Nachbarschaft gegengelesen (Lektion 12)

#### Schritt 2.3: sync-Lauf + Drei-Punkte-Verifikation
- **Zweck:** Beweis, dass das Muster traegt — die Datei wird als „neu" erkannt und installiert
- **Dateien:** keine Repo-Aenderung (Lock + `~/.claude/output-styles/` sind ausserhalb)
- **Input:** **Feste Reihenfolge (Nachlauf!):** Phase-2-Aenderungen committen → pushen → `/dtb:kit-sync sync` → Kriterien pruefen → SHA-Nachtrag in `## Progress`. Die sync-Quelle ist der GitHub-Stand; vor dem Push koennen die Nachlauf-Kriterien dieser Phase gar nicht gruen sein (ausstehend ≠ verletzt, Lektion 1)
- **Output:** Lock-Eintrag `output-styles/dtb-gezielt.md`; anschliessender `/dtb:kit-sync check` meldet 0 Abweichungen (45 Artefakte). **Dabei beobachten:** legt sync das fehlende Zielverzeichnis `~/.claude/output-styles/` selbst an? (ungetestete Annahme, plan-review 2026-08-07)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Muster-Beleg: Wegwerf-Test
- **Zweck:** Spec-Erfolgskriterium „testweise zweite Datei" real erfuellen statt als Gedankenexperiment (plan-review 2026-08-07, Pragmatiker) — testet nebenbei die Verwaisten-Heuristik
- **Dateien:** `output-styles/dtb-test.md` (temporaer, wird wieder geloescht)
- **Input:** Minimale Wegwerf-Datei committen + pushen → `/dtb:kit-sync sync` (erkennt sie als „neu" OHNE kit-sync-Aenderung = Muster belegt) → Datei im Repo loeschen, committen + pushen → `/dtb:kit-sync check` (meldet „verwaist") → sync: entfernen bestaetigen
- **Output:** Beide Zustaende („neu" → installiert; „verwaist" → entfernt) im Chat belegt; Endzustand: Repo, Lock und `~/.claude/output-styles/` tragen nur `dtb-gezielt.md`

### Deliverables
- [ ] kit-sync kennt die Klasse als Muster; Kopie liegt unter `~/.claude/output-styles/`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "output-styles/dtb-\*" skills/dtb-kit-sync/SKILL.md` ≥ 2 (Klassen-Tabelle + Verwaisten-Abschnitt)
- [ ] Spiegel: `grep -c "output-styles" skills/CLAUDE.md` ≥ 1 UND `grep -c "output-styles" CLAUDE.md` ≥ 1
- [ ] **(Nachlauf — gruen erst nach Commit→Push→Sync, Reihenfolge in 2.3)** Lock-Eintrag existiert: `python`-Einzeiler auf `artifacts["output-styles/dtb-gezielt.md"]`
- [ ] **(Nachlauf)** `kithash(~/.claude/output-styles/dtb-gezielt.md)` = Lock-Hash = Repo-Hash (Drei-Punkte; Gate: alle drei Seiten gefuellt, Lektion 7)

#### Manual
- [ ] Muster-Beleg aus 2.4: beide Zustaende des Wegwerf-Tests („neu" → installiert, „verwaist" → entfernt) im Chat belegt

---

## Phase 3: Aktivierung, project-health-Check, Kalibrier-Abnahme

### Ziel
Die Vorgabe ist aktiv; `project-health` meldet den inaktiven Zustand korrekt in beide
Richtungen; die Wirkung ist an einem Fall-Set abgenommen statt an Stimmung.

### Schritte

#### Schritt 3.1: project-health Check 12 („Style installiert, aber nicht aktiviert")
- **Zweck:** Randfall 2 der Spec (zweite Maschine) mechanisch abfangen
- **Dateien:** `skills/dtb-project-health/SKILL.md`
- **Input:** Logik: Lock-Eintrag `output-styles/*` vorhanden ∧ `outputStyle` fehlt in `~/.claude/settings.json` → INFO-Meldung mit Aktivierungs-Hinweis. Projektlokale Overrides (`.claude/settings.local.json`) NICHT pruefen — bekannte Einschraenkung, kein Befund (Spec-Randfall 3)
- **Output:** Neuer Check 12 nach dem Muster von Check 11 (read-only, kein Netzwerk). Die INFO-Meldung dokumentiert **beide Wege**: Aktivierung (`outputStyle` setzen + Session-Neustart) UND Rueckweg (Feld entfernen + Session-Neustart) — der Rueckweg ist trivial, aber nur dokumentiert ist er auch in drei Wochen auf der zweiten Maschine noch trivial (plan-review 2026-08-07, Betriebs-Waechter)

#### Schritt 3.2: Aktivieren auf dieser Maschine + Annahmen-Probe
- **Zweck:** Der Schalter — einmalig, von Hand dokumentiert; dabei die drei ungetesteten Annahmen aus dem plan-review pruefen
- **Dateien:** `~/.claude/settings.json` (ausserhalb des Repos)
- **Input:** `"outputStyle": "Gezielt"` ergaenzen. **Annahmen-Probe (Senior Dev, plan-review 2026-08-07):** (1) greift das Feld in der User-settings.json ueberhaupt, und loest es gegen Frontmatter-`name` oder Dateinamen auf? — nach dem Neustart via `/config` verifizieren; (2) Verzeichnis-Anlage durch sync — bereits in 2.3 beobachtet; (3) Zusammenspiel mit `language`-Setting und Session-Hooks — im ersten Lauf beobachten
- **Output:** Nach Session-Neustart aktiv (via `/config` bestaetigt); Check 12 meldet vorher INFO, nachher nichts (beide Richtungen = Success Criterion). **Zweite Maschine bewusst NICHT Teil dieses Features** — sie zieht Check-12-getrieben nach, wann immer sie synct (Nutzer-Entscheid plan-review 2026-08-07)

#### Schritt 3.3: Kalibrier-Fall-Set definieren + Abnahmelauf
- **Zweck:** „Wirkt der Stil?" pruefbar machen (offener Punkt der Spec; Vorbild: no-loss-check-Kalibrierung 5/5). **Voraussetzung: frische Session NACH 3.2** — der System-Prompt wird beim Session-Start gelesen; in der Arbeits-Session von 3.2 gemessen, misst dieser Schritt nichts (plan-review 2026-08-07, Senior Dev)
- **Dateien:** Fall-Tabelle im Session-Log (kein neues Artefakt — Kalibrier-Doku gehoert persistiert, Lehre aus no-loss-check H1)
- **Input:** 4-5 Faelle mit erwarteter Antwortform, mindestens: (a) einfache Sachfrage → kurze Antwort ohne Vorwegnahme; (b) Entscheidungsfrage → Kern/Stand/Entscheidung erkennbar; (c) ausdrueckliche Analyse-Bitte → Ausnahme-Klausel greift, ausfuehrlich; (d) **Gegenprobe:** Skill mit festem Report-Format (z.B. `/dtb:workflow-next`) → Format unveraendert (Vorrang-Regel); (e) Belege/Zahlen im Thema → Substanz vollstaendig
- **Output:** Fall-Tabelle mit Soll/Ist je Fall im Session-Log; Nutzer-Verdikt je Fall

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Nachschaerfen + Abschluss-Verteilung
- **Zweck:** Befunde aus 3.3 in die Datei zurueckfuehren; Endstand verteilen
- **Dateien:** `output-styles/dtb-gezielt.md` (nur bei Befunden), danach `/dtb:kit-sync sync`
- **Input:** Fall-Tabelle aus 3.3
- **Output:** Finale Fassung committet + gepusht + gesynct; `check` 0 Abweichungen. **Nachlauf wie 2.3:** Reihenfolge Commit → Push → Sync → Kriterien → SHA-Nachtrag

### Deliverables
- [ ] Check 12 in project-health; Stil aktiv; Kalibrier-Tabelle im Session-Log

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "Check 12" skills/dtb-project-health/SKILL.md` ≥ 1
- [ ] `outputStyle` gesetzt: `python`-Einzeiler auf `~/.claude/settings.json`
- [ ] Kalibrier-Tabelle existiert: Grep auf `| Fall |` im heutigen Session-Log (Wirkstellen-Anker, Lektion 8)
- [ ] **(Nachlauf)** Abschluss-`check`: 0 Abweichungen ueber alle Artefakte
- [ ] Rueckweg dokumentiert: `grep -c "entfernen" skills/dtb-project-health/SKILL.md` im Check-12-Abschnitt ≥ 1

#### Manual
- [ ] Kalibrier-Verdikt: alle Faelle vom Nutzer als bestanden beurteilt (inkl. Gegenprobe d)
- [ ] Check 12 in beide Richtungen beobachtet (INFO vor Aktivierung, still danach)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Dateiname | `gezielt.md` vs. `dtb-gezielt.md` | `dtb-gezielt.md` | Die Verwaisten-Erkennung von kit-sync identifiziert Kit-Altbestand per `dtb-*`-Heuristik — ohne Praefix waere eine verwaiste Style-Kopie unsichtbar. Anzeigename bleibt via Frontmatter `name: Gezielt` sauber |
| Klassen-Muster | `output-styles/*.md` vs. `output-styles/dtb-*.md` | `output-styles/dtb-*.md` | Verteilungs-Muster und Verwaisten-Heuristik versprechen dasselbe (plan-review 2026-08-07, Nutzer-Entscheid) |
| Zweite Maschine | Teil des Features vs. Check-12-getrieben | Check-12-getrieben | Scope endet auf dieser Maschine; die zweite zieht beim naechsten sync nach, Check 12 meldet dort den inaktiven Zustand (Nutzer-Entscheid) |
| Style-Name (Frontmatter) | Dateiname als Name vs. `name:`-Feld | `name: Gezielt` | Ohne Feld hiesse der Stil „dtb-gezielt" im Picker |
| Ort des Aktivierungs-Checks | Check 11 erweitern vs. neuer Check 12 | Neuer Check 12 | Check 11 prueft Drift (Hash-Vergleich), Aktivierung ist ein anderes Thema; Vermischung wuerde die „Logik nicht duplizieren"-Regel von Check 11 verwaessern |
| Sprache der Style-Datei | Deutsch vs. Englisch | **Deutsch (bestaetigt)** | Kit-Konvention fuer Bodies; vom Nutzer im plan-review 2026-08-07 entschieden — Frage ist geschlossen |
| Kalibrier-Doku-Ort | Eigenes Artefakt vs. Session-Log | Session-Log | Kein neues Artefakt fuer einen Einmal-Vorgang; Lehre aus no-loss-check H1: die Tabelle MUSS persistiert werden, der Log reicht dafuer |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Verzeichnis + Datei anlegen — `7172b9c`
- [x] 1.2 Inhalt ausformulieren — `7172b9c`
- [x] 1.3 Selbst-Review gegen die Spec — `7172b9c`
- [x] 2.1 kit-sync: Klassen-Tabelle + Verwaisten-Logik — `89ede9c`
- [x] 2.2 Spiegel mitziehen (skills/CLAUDE.md + Root-CLAUDE.md) — `89ede9c`
- [x] 2.3 sync-Lauf + Drei-Punkte-Verifikation — `89ede9c`
- [ ] 2.4 Muster-Beleg: Wegwerf-Test
- [ ] 3.1 project-health Check 12
- [ ] 3.2 Aktivieren auf dieser Maschine + Annahmen-Probe
- [ ] 3.3 Kalibrier-Fall-Set + Abnahmelauf
- [ ] 3.4 Nachschaerfen + Abschluss-Verteilung

---

## Umsetzung

Umsetzung mit `/dtb:implement output-style-gezielt` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/output-style-gezielt/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
