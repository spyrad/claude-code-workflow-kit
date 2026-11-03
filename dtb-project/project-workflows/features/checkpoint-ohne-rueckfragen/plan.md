# Implementierungsplan: Checkpoint ohne Rueckfragen

**Erstellt:** 2026-11-03
**Feature-Spec:** `features/checkpoint-ohne-rueckfragen/spec.md`
**Geschaetzte Dauer:** 2,5–3 h (gemeinsame Nachmessung mit #177 nach dem Merge nicht eingerechnet)
**Status:** Reviewed (plan-review 2026-11-03: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Regel und Checkpoint-Verhalten (§9.4, Auto-Erfassung, ⏳ ohne Frage, Kontrollpunkt nur Zuordnung, Verlustpruefung ohne Schlussfrage) | 1,5–2 h | Geplant |
| Phase 2 | Spiegel und Doku, Messauftrag zusammenfuehren, Probelauf | 1 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Betroffene Module), ergaenzt um drei Fundstellen aus dem Grep am 2026-11-03 (`README.md`, `impl-plan`, `debug-plan`).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | 829 Zeilen. Schritt 0 „Funde erfassen": bereitet Teil A vor, Duplikate vorgestrichen, Struktur-Check auf 5 Anker. Schritt 1: Aufgaben-Vergleich (Teil B), „⏳ Alter" (Teil C, „behalten" nur auf `passt`), `#### Kontrollpunkt (eine Rueckfrage-Runde)` mit Format A/B/C, Antwortregeln je Teil, Fallback, „Danach schreiben". Log-Format: Pfeil-Slot mit `Abbruch|alle gestrichen|…`. Schritt 6: Bestaetigung ohne Erfassungs-Block |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §9.1: „Ueberlauf baut die ⏳-Vorlage (9.4) ab". §9.4: Sammelvorlage mit Default „behalten", „Keine automatische Entscheidung", Absatz „Eine Rueckfrage-Runde (seit 2026-11-02)". §9.2/§9.3: Rueckfrage bei unsicherer Zuordnung / Abgang ohne Beleg (bleibt). Aenderungs-Absaetze am Dateiende |
| `skills/dtb-no-loss-check/SKILL.md` | Abschlussfrage entfaellt aus dem Checkpoint nur „mit nicht-leerer Vorlage" (Z. ~324–330, „wortgleich zur Checkpoint-Seite", #73); Z. 34 und Z. 98 nennen die Sammelvorlage; Kopplungs-Hinweis Z. 311 „Kontrollpunkt Teil A" |
| `skills/CLAUDE.md` | Zeile `I` der Rueckfragen-Defaults (Kontrollpunkt A/B/C, „Ok/passt = A bestaetigt + C behalten"); Zwei-Becken-Tabelle Z. 375 „Kontrollpunkt Teil A schreibt"; Z. 448 „per Sammelvorlage" |
| `CLAUDE.md` | Session lifecycle + Skill-Kategorien: „after ONE confirmed collection template", „ONE ⏳ decision template", Teile A/B/C |
| `README.md` | Z. 68: „overdue ones one ⏳ decision" |
| `skills/dtb-lesson/SKILL.md` | Kopplungs-Hinweise „Kontrollpunkt Teil A" Z. 113/156/177; Z. 96 „Verlustpruefung + Sammelvorlage" |
| `skills/dtb-idea/SKILL.md` | Kopplungs-Hinweise „Kontrollpunkt Teil A" Z. 79/118 |
| `skills/dtb-idea-triage/SKILL.md` | Z. 99 (Herkunft Becken-Eintraege), Z. 778 (Kopplungs-Hinweis) |
| `skills/dtb-impl-plan/SKILL.md`, `skills/dtb-debug-plan/SKILL.md` | Lektion-Kandidat-Absatz: „der Mensch bestaetigt in der Sammelvorlage" |
| `skills/dtb-project-dashboard/SKILL.md` | zaehlt ⏳ woertlich aus der Liste — unveraendert |
| `features/checkpoint-schneller/` | spec.md: Nachmessung bis 2026-12-02 (Median ≤ 4 min, 3 Vergleichslaeufe); `checkpoint-phasen.py` klassifiziert Rueckfragen per Regex (`Kontrollpunkt —`, `Aufgaben-Zuordnung`) |

---

## Phase 1: Regel und Checkpoint-Verhalten

### Ziel
Der Checkpoint erfasst Verlustfunde ohne Rueckfrage, markiert alte Aufgaben nur noch mit ⏳ und fragt
ausschliesslich bei unsicherer Aufgaben-Zuordnung; Regel und Kurzkopie sagen dasselbe, und die
Verlustpruefung stellt aus dem Checkpoint heraus keine Schlussfrage mehr.

### Schritte

#### Schritt 1.1: Regel §9 aendern
- **Zweck:** Die bewusste Regelaenderung (Becken #185) zuerst an der Quelle — der Skill folgt ihr
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (§9.1, §9.4, Aenderungs-Absatz am Dateiende)
- **Input:** Discovery-Entscheide 3a/3b
- **Output:** §9.4: faellig → ⏳ am Zeilenende, **keine Sammelvorlage, keine Frage, kein automatischer
  `· behalten`-Stempel**; bestehende `· behalten`-Stempel bleiben gueltig (juengeres Datum zaehlt weiter);
  Abgang nur ueber ein Session-Signal (§9.3). Der Absatz „Eine Rueckfrage-Runde" schrumpft auf die
  Zuordnungs- und Abgangsfragen aus 9.2/9.3. §9.1: „Ueberlauf baut die ⏳-Vorlage (9.4) ab" ersetzen
  (die Liste schrumpft nur ueber Abgangsvermerke; ⏳ macht Ueberlauf sichtbar). Aenderungs-Absatz mit
  Datum und Grund (Bestaetigung ohne Informationsgewinn, #173/#185)

#### Schritt 1.2: Verlustfunde automatisch erfassen
- **Zweck:** Teil A des Kontrollpunkts entfaellt — die Gruppe der Verlustpruefung entscheidet
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 0 inkl. „Funde erfassen", Log-Format + Richtlinie „Verlustpruefung")
- **Input:** Discovery-Entscheide 3a/3c; Struktur-Check und Quellen-Aufloesung bleiben unveraendert
- **Output:** Schritt 0 schreibt direkt nach der Vorbereitung (per Referenz wie bisher, Herkunfts-Marker
  bleibt): dringende Lektionen/Ideen + Ideen aus `## Kann warten`. Duplikat-Treffer werden **nicht**
  geschrieben, sondern als Meldung gefuehrt. Rueckfall „> 10 Funde" und Mengenprobe (L90: geschriebene +
  uebersprungene = Eingang) bleiben. Die Meldungen werden fuer Schritt 6 gesammelt. Log-Pfeil-Slot:
  `Abbruch|alle gestrichen` entfallen, neu `nur Duplikate`; der Pfeil-Teil haengt an der Zahl der
  **erfassten** Eintraege, nicht an `{D}` — die Regel „bei `D = 0` entfaellt der Pfeil-Teil" entfaellt,
  weil „Kann warten"-Ideen auch bei `D = 0` geschrieben werden (sonst still ohne Log-Spur, L47). Selbstpruefung L15 bleibt
  (nur Anker, keine Regel-Spiegel)

#### Schritt 1.3: ⏳ ohne Frage, Kontrollpunkt nur fuer Zuordnung
- **Zweck:** Teil C entfaellt; uebrig bleibt die eine echte Entscheidung
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 1 „⏳ Alter" = §9-Kurzkopie, `#### Kontrollpunkt (eine Rueckfrage-Runde)`)
- **Input:** §9 aus Schritt 1.1 (Grep-Anker `Aufgaben-Abgaenge` bleibt)
- **Output:** „⏳ Alter": nur markieren, Zaehlung fuer die Anzeigezeile in Schritt 6. Kontrollpunkt:
  Ueberschrift bleibt (Messkontinuitaet, siehe Entscheidungen), Kopfzeile `# Kontrollpunkt — {Z}
  Aufgaben-Frage(n)`, nur noch die Zuordnungs- und Abgangszeilen mit `ja`/`nein`/`verwerfen: {Grund}`,
  Fallback-Rueckfrage bei fehlender Angabe bleibt. Alle Antwortregeln zu A und C, „Ein Wort fuer alles",
  die Mengenprobe je Teil und die Sonderregel „Punkte mit offener Zuordnung fehlen in Teil C" entfallen
  (Letzteres: sie bekommen nach der Antwort ⏳, falls faellig). Ohne Zuordnungsfrage → keine Runde.
  Die Teil-Buchstaben verschwinden ganz: die Verweise im Aufgaben-Vergleich („als Teil B in den
  Kontrollpunkt") werden zu „in den Kontrollpunkt"

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Erfassungs-Block in der Bestaetigung
- **Zweck:** Ohne Vorab-Bestaetigung muss das Ergebnis am Ende sichtbar sein
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 6)
- **Input:** gesammelte Meldungen aus Schritt 1.2, ⏳-Zaehlung aus Schritt 1.3
- **Output:** Block im Bestaetigungs-Template (entfaellt ohne Inhalt): je Lektion `✔ L{N} → lessons.md — „{Regelsatz gekuerzt}"`,
  je Idee `✔ #{N} → INBOX-BEFUNDE.md`, je Lektions-Duplikat `übersprungen — ähnlich L{N} (trotzdem: /dtb:lesson „…")`,
  je Ideen-Duplikat nur `übersprungen — ähnlich #{N}` (kein Befehl: `dtb:idea` schriebe nach `INBOX.md` statt ins Becken — Zwei-Becken-Trennung);
  bei ≥ 1 Lektion `Falsch erfasst? → /dtb:lesson-curate`; Rueckfall-Zeile bei > 10 Funden; bei faelligen
  Aufgaben `⏳ {K} offene Aufgabe(n) ≥ {S} Tage — erledigt/verworfen per Ansage in einer Session`

#### Schritt 1.5: Verlustpruefung ohne Schlussfrage im Checkpoint
- **Zweck:** Ohne Teil A wuerde die Abschlussfrage von `no-loss-check` wieder auftauchen (L42: der Waechter behielte seine alte Bedingung)
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md` (Abschlussfrage-Absatz, Z. 34, Z. 98), `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 0 „Weich, nie blockierend")
- **Input:** Discovery 3e
- **Output:** Auf beiden Seiten wortgleich der Satz `Aus dtb:workflow-checkpoint aufgerufen entfaellt die Abschlussfrage immer — der Checkpoint erfasst selbst.`;
  eigenstaendiger Aufruf unveraendert. Z. 34/98 ohne „Sammelvorlage"

### Deliverables
- [ ] Geaenderte `DERIVED_STATE_RULES.md` (§9.1, §9.4, Aenderungs-Absatz)
- [ ] Geaenderte `skills/dtb-workflow-checkpoint/SKILL.md` (Schritte 0, 1, 6, Log-Format)
- [ ] Geaenderte `skills/dtb-no-loss-check/SKILL.md` (Abschlussfrage)

### Checkpoint-Kriterien

#### Automated
- [ ] `wc -l < skills/dtb-workflow-checkpoint/SKILL.md` < 829 (Skill kuerzer)
- [ ] `sed -n '/^### Schritt 0/,/^### Schritt 2/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'Teil [ABC]\b'` = 0 (Teil-Buchstaben weg; auf die Wirkstelle begrenzt, damit ein Aenderungsvermerk anderswo nicht falsch rot macht — L116)
- [ ] `sed -n '/^#### Kontrollpunkt/,/^### Schritt 2/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'nicht gestrichenen\|alle behalten\|Abbruch A\|Abbruch C'` = 0
- [ ] `sed -n '/^#### Kontrollpunkt/,/^### Schritt 2/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'verwerfen: {Grund}'` ≥ 1 (Zuordnungsfrage traegt weiter — L15)
- [ ] `sed -n '/^### Schritt 6: Bestaetigung/,$p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'lesson-curate\|übersprungen — ähnlich\|⏳ {K}'` ≥ 3 (neuer Erfassungs-Block — L15)
- [ ] `grep -c 'Aufgaben-Abgaenge' skills/dtb-workflow-checkpoint/SKILL.md` ≥ 3 (Kopplungsanker bleibt)
- [ ] `grep -c 'D = 0' skills/dtb-workflow-checkpoint/SKILL.md` = 0 (Pfeil-Slot haengt nicht mehr an den dringenden Funden)
- [ ] `sed -n '/^### 9.4/,/^### 9.5/p' dtb-project/project-rules/DERIVED_STATE_RULES.md | grep -c 'Sammelvorlage\|„passt"'` = 0 und `… | grep -c 'kein automatischer'` ≥ 1
- [ ] `grep -c 'Aus dtb:workflow-checkpoint aufgerufen entfaellt die Abschlussfrage immer' skills/dtb-no-loss-check/SKILL.md skills/dtb-workflow-checkpoint/SKILL.md` = 1 je Datei; `grep -c 'nicht-leerer Vorlage' skills/dtb-no-loss-check/SKILL.md` = 0

#### Manual
- [ ] Beispiel-Ausgabe im Chat gezeigt und als lesbar abgenommen: (a) Bestaetigung mit Erfassungs-Block (Lektion, Idee, Duplikat, ⏳-Zeile), (b) Kontrollpunkt mit nur einer Zuordnungsfrage. Grundlage: echter Stand des Haupt-Checkouts; fehlende Faelle als sichtbar gekennzeichnete Attrappe

---

## Phase 2: Spiegel, Messauftrag, Probelauf

### Ziel
Alle Stellen, die das alte Verhalten beschreiben, stimmen; die gemeinsame Nachmessung mit #177 hat
ein Kriterium fuer #173; ein echter Lauf belegt das neue Verhalten.

### Schritte

#### Schritt 2.1: Spiegel und Doku nachziehen
- **Zweck:** Kopplungs-Hinweise und Kit-Doku zeigen auf das neue Verhalten (L3, L44)
- **Dateien:** `skills/CLAUDE.md` (Zeile `I`, Z. 375, Z. 448), `CLAUDE.md` (Session lifecycle, Skill-Kategorien `workflow-checkpoint`/`no-loss-check`), `README.md` Z. 68, `skills/dtb-lesson/SKILL.md` (Z. 96/113/156/177), `skills/dtb-idea/SKILL.md` (Z. 79/118), `skills/dtb-idea-triage/SKILL.md` (Z. 99/778), `skills/dtb-no-loss-check/SKILL.md` Z. 311, `skills/dtb-impl-plan/SKILL.md` + `skills/dtb-debug-plan/SKILL.md` (Lektion-Kandidat-Absatz)
- **Input:** repo-weiter Grep nach `Kontrollpunkt Teil`, `Sammelvorlage` + `checkpoint`, `⏳ decision`, `bestaetigt in der` (ausserhalb `project-changelog/` und `archive/`); `feature-fast`-Treffer zu „Sammelvorlage" sind ein anderer Mechanismus und bleiben
- **Output:** jede Fundstelle angepasst oder als „passt schon" vermerkt (Fundliste im Session-Log); Pipeline-Frontmatter geprueft (L44 — `produces`/`consumes` aendern sich voraussichtlich nicht)

#### Schritt 2.2: Messauftrag zusammenfuehren
- **Zweck:** Die gemeinsame Nachmessung (Entscheid 2026-11-03) braucht ein Kriterium fuer #173 und einen Ausgangswert
- **Dateien:** `features/checkpoint-ohne-rueckfragen/spec.md` (Success Criteria, Offene Punkte), `features/checkpoint-schneller/spec.md` (Hinweis: Messung gemeinsam mit #173)
- **Input:** `python -I dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py --rueckfragen` (Ausgangswert: wie oft trat die Kategorie „Aufgaben-Zuordnung" auf, wie oft „Sammelvorlage/Kontrollpunkt")
- **Output:** Ausgangswert im Session-Log; in der Spec das Messkriterium (entschieden im plan-review 2026-11-03): „In der gemeinsamen Nachmessung bis 2026-12-02 stellt der Checkpoint keine Rueckfrage zu Verlustfunden oder alten Aufgaben mehr — nur noch Zuordnungsfragen (Kategorien von `checkpoint-phasen.py --rueckfragen`); Median ≤ 4 aktive min gilt gemeinsam mit #177"; offener Punkt zur Haeufigkeit geschlossen, offener Punkt zu den Erfolgskriterien geschlossen. Fuer den Hand-off vorgemerkt: offene Aufgabe „Nachmessung #177" in `WORKFLOW_STATUS.md` → „Nachmessung #177 + #173 … bis 2026-12-02" (Orchestrator)

#### Schritt 2.3: Probelauf im Haupt-Checkout
- **Zweck:** Das neue Verhalten an einem echten Stand belegen — im Worktree bricht der Voll-Guard ab
- **Dateien:** `features/checkpoint-ohne-rueckfragen/probelauf.md` (neu, status-neutral: Datum, Projekt, Zahl der Rueckfragen, erfasste Funde, Duplikate, ⏳-Zeile, Schlussfrage der Verlustpruefung ja/nein)
- **Input:** Die Orchestrator-Session fuehrt ihren naechsten regulaeren Checkpoint nach der Worktree-Fassung von `skills/dtb-workflow-checkpoint/SKILL.md` aus (L74: Repo-Fassung, nicht installierte Kopie). Rollen wie bei #177: der Orchestrator fuehrt aus und schreibt nichts in diesen Worktree, der Mensch meldet das Ergebnis in dieser Pane, die Worktree-Session schreibt `probelauf.md`
- **Output:** `probelauf.md` mit dem Beleg; Abweichungen als Nacharbeit vor der Abnahme (L97)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Angepasste Spiegel und Doku (Liste in 2.1)
- [ ] Messkriterium in `spec.md`, Hinweis in `checkpoint-schneller/spec.md`
- [ ] `features/checkpoint-ohne-rueckfragen/probelauf.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -rn 'Kontrollpunkt Teil' skills/ CLAUDE.md README.md | wc -l` = 0
- [ ] `grep -c 'bestaetigt in der' skills/dtb-impl-plan/SKILL.md skills/dtb-debug-plan/SKILL.md` = 0 je Datei
- [ ] `grep '^| I |' skills/CLAUDE.md | grep -c 'C behalten'` = 0 und `grep '^| I |' skills/CLAUDE.md | grep -c 'Zuordnung'` = 1
- [ ] `grep -n 'workflow-checkpoint' README.md | grep -c '⏳ decision'` = 0
- [ ] `sed -n '/^## Success Criteria/,/^## Offene Punkte/p' dtb-project/project-workflows/features/checkpoint-ohne-rueckfragen/spec.md | grep -c 'Nachmessung'` ≥ 1
- [ ] `grep -c '#173' dtb-project/project-workflows/features/checkpoint-schneller/spec.md` ≥ 1
- [ ] `test -f dtb-project/project-workflows/features/checkpoint-ohne-rueckfragen/probelauf.md`

#### Manual
- [ ] Probelauf belegt in `probelauf.md`: ohne unsichere Zuordnung keine Rueckfrage vor dem Schreiben (Abnahme ausgenommen), Erfassungs-Block in der Bestaetigung sichtbar, keine Schlussfrage der Verlustpruefung

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Zeitpunkt des Schreibens | A: direkt in Schritt 0 · B: nach dem Kontrollpunkt (Ende Schritt 1) | A | Keine Antwort mehr abzuwarten; die Zuordnungsfrage hat mit den Funden nichts zu tun |
| Ueberschrift `#### Kontrollpunkt (eine Rueckfrage-Runde)` | A: behalten · B: umbenennen | A | `checkpoint-phasen.py` erkennt die Runde an `Kontrollpunkt —` — gleiche Kategorie vor und nach der Aenderung, gemeinsame Nachmessung bleibt vergleichbar |
| ⏳ bei faelligen Aufgaben | A: nur markieren · B: automatisch `· behalten` stempeln | A | Discovery 3b: mit Stempel verschwaende ⏳ alle `alter_schwelle_tage` still |
| Listen-Ueberlauf (§9.1) | A: hinnehmen · B: Hinweis in der ⏳-Zeile | B | Kostet eine Zeile; nennt den einzigen Weg, die Liste zu verkleinern (Ansage in einer Session) |
| Duplikat-Treffer | A: nur melden · B: vorgestrichen mit Veto wie bisher | A | Discovery 3c; Veto braeuchte wieder eine Antwort — der Ersatz ist der kopierfertige Befehl in der Meldung |
| Mengengrenze > 10 | A: bleibt · B: entfaellt | A | Discovery 3c: Schutz gegen Massen-Fehlerkennung |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Regel §9 aendern — `4d538b8`
- [x] 1.2 Verlustfunde automatisch erfassen — `4d538b8`
- [x] 1.3 ⏳ ohne Frage, Kontrollpunkt nur fuer Zuordnung — `4d538b8`
- [x] 1.4 Erfassungs-Block in der Bestaetigung — `4d538b8`
- [x] 1.5 Verlustpruefung ohne Schlussfrage im Checkpoint — `4d538b8`
- [x] 2.1 Spiegel und Doku nachziehen — `5e41cfc`
- [x] 2.2 Messauftrag zusammenfuehren — `5e41cfc`
- [x] 2.3 Probelauf im Haupt-Checkout — `5e41cfc`

---

## Umsetzung

Umsetzung mit `/dtb:implement Checkpoint ohne Rueckfragen` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/checkpoint-ohne-rueckfragen/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).
Nach dem Merge: gemeinsame Nachmessung mit #177 bis spaetestens 2026-12-02 — keine Progress-Schritte,
Traeger ist der Hand-off (Schritt 2.2).

---

**Erstellt mit:** `/dtb:impl-plan`
