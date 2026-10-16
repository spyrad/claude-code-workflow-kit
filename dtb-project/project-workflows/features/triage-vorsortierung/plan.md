# Implementierungsplan: Triage-Vorsortierung

**Erstellt:** 2026-10-16
**Feature-Spec:** `features/triage-vorsortierung/spec.md`
**Geschaetzte Dauer:** ~7,5 h (4 Phasen)
**Status:** Reviewed (plan-review 2026-10-16: REVISE → 6 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Voranalyse im Skill (Agenten, Ergebnis-Format, Konsolidierung) | 1,5 h | Geplant |
| Phase 2 | Sammelliste, Schreibwege und Stufe 2 | 3 h | Geplant |
| Phase 3 | Kopplungen und Kit-Doku nachziehen | 1 h | Geplant |
| Phase 4 | Probelaeufe (Testprojekt + Trockenlauf gegen das echte Becken) | 2 h | Geplant |

---

## Ist-Analyse

📂 Uebernommen aus `discovery.md` (11 Module, Pfade verifiziert 2026-10-16), ergaenzt um die Lese-Befunde der Planung.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-idea-triage/SKILL.md | 407 Zeilen; Schritte 0–6 + `## Schreibmechanik INBOX-BEFUNDE.md` (Checkpoint-Anker, bleibt). `allowed-tools: Read, Write, Edit, Grep, Bash` — ohne `Agent`. Schritt 2 portioniert (neu/faellig/Altbestand ≤ `altbestand_pro_lauf`), Schritt 4 entscheidet einzeln und schreibt sofort (#71), 5a Befoerdern Ziel-vor-Quelle, 5b Verwerfen ins Archiv (Spalten: Verworfen am, #, Datum, Befund, Begruendung) |
| skills/dtb-lesson/SKILL.md | Anker `## Schritt 2: In 4 Felder strukturieren`, `## Schritt 3: Duplikat-Check`, `## Schritt 4: Append-only speichern` — Kopplungs-Hinweise nennen bisher nur `dtb:workflow-checkpoint` als Leser per Referenz; „Zwei Eingangskanaele" in Schritt 1 |
| skills/dtb-open-question/SKILL.md | Schritt 2 leitet das Ziel ab (0 aktiv → Abbruch), Schritt 3 waehlt `spec.md` vor `discovery.md`, Schritt 4 formt §6-Zeile + exakter Duplikat-Check + Ziel-Bestaetigung, Schritt 5 schreibt in `## Offene Punkte`. Keine Kopplungs-Hinweise fuer Leser per Referenz |
| skills/dtb-idea/SKILL.md | `## Duplikat-Check` — von der Triage bereits per Referenz genutzt (5a) |
| skills/dtb-workflow-checkpoint/SKILL.md | Schritt 0 = Vorbild: Struktur-Check (Quelle Repo zuerst, dann Installation; Anker-Grep `grep -x -F`; zwei Fehlerpfade), Sammelvorlage mit `Ok / streiche / behalte / Abbruch`, Schreiben per Referenz. Greppt `## Schreibmechanik INBOX-BEFUNDE.md` in der Triage |
| skills/dtb-impl-review/SKILL.md | Schritt 9 = Vorbild Sammelliste: Einzel-Findings zuerst per AskUserQuestion, Rest als EINE Liste mit `Alle uebernehmen / Nummern streichen / Einzeln durchgehen`; Sub-Agent-Prompts inline (Schritt 4–6) |
| skills/dtb-idea-review/SKILL.md | Zusammenlegen (4): Ziel-Idee-Text ergaenzen, dann Quelle — Vorbild fuer den Nachtrag |
| skills/dtb-worker/SKILL.md | Background-Subagent-Traeger; nur Referenz, kein Umbau |
| skills/CLAUDE.md | Zwei-Becken-Regel (Schreiber-Tabelle), Rueckfragen-Defaults (Zuordnung Z/A–E), Duplikat-Schutz („Vierter Anwender per Referenz") |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §6.4: „Vorgang erst durch die Befoerderung" — neue Ausgaenge (Lektion, Fachfrage, Nachtrag, gebuendelt) fehlen; Klasse-B-Seed (L82) |
| skills/dtb-project-health/SKILL.md | Becken-Integritaet + Nummernkreis (Nummer in `INBOX.md` UND Becken) — Buendel/Nachtrag entfernen die Nummer aus dem Becken, keine Doppelung; voraussichtlich unveraendert |
| workflow.config.yaml | `idea_triage: becken_schwelle, altbestand_pro_lauf` |
| CLAUDE.md | Beschreibung `idea-triage` unter „Idea management" |
| dtb-project/project-workflows/INBOX-BEFUNDE.md | 73 Funde — Material fuer den Trockenlauf (Phase 4), wird NICHT beschrieben |

---

## Phase 1: Voranalyse im Skill

### Ziel
`dtb:idea-triage` erzeugt vor jeder Entscheidung eine lesende Voranalyse des ganzen ungesichteten Beckens: je Fund ein Vorschlag mit Grund, Beleg, Sicherheit und Verwandtschaft — und konsolidiert daraus Buendel sowie die Aufteilung in Einzelfaelle und Sammelliste.

### Schritte

#### Schritt 1.1: Frontmatter, Config und Schritt 2 umbauen
- **Zweck:** Grundlage fuer die neue Lauf-Form legen (L44, L75)
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (Frontmatter, Schritt 0, Schritt 2), `workflow.config.yaml`
- **Input:** Technische Entscheidungen T1, T4
- **Output:**
  - `allowed-tools` um `Agent` und `Glob` ergaenzt; `consumes` um `project-rules/lessons.md`, `features/*/spec.md`, `features/*/discovery.md`; `produces` um `project-rules/lessons.md`, `features/*/spec.md`, `features/*/discovery.md`; `description` nennt Vorsortierung und die neuen Ausgaenge
  - Config-Schluessel `einzeln_pro_lauf` (Default 5; fehlt er, gilt `altbestand_pro_lauf` als Rueckfall, fehlen beide → 5); `altbestand_pro_lauf` im Kommentar als Alt-Schluessel markiert
  - Schritt 2: Sichtungsmenge = ALLES Ungesichtete (neu, faellig, Altbestand) fuer die Voranalyse; die Kappung wandert an die Einzelfaelle (Schritt 1.3); Argumente `alle` (keine Kappung) und Zahl (ersetzt `einzeln_pro_lauf`) bleiben; Begruendung der Regelanpassung im Text (warum „nie das ganze Becken" fuer die Sammelliste nicht mehr gilt)
  - Leeres Becken → bestehende Ein-Zeilen-Meldung, keine Agenten
  - **Geruest einmalig (plan-review 2026-10-16):** alle endgueltigen Sektionstitel in einem Zug setzen — `## Schritt 3: Voranalyse`, `## Schritt 4: Konsolidieren`, `## Schritt 5: Sammelliste` (neu, zunaechst mit Platzhalter-Satz), `## Schritt 6: Einzeln entscheiden (Stufe 2)` (bisher Schritt 4), `## Schritt 7: Entscheidung ausfuehren` (bisher Schritt 5 „… (sofort schreiben)"), `## Schritt 8: Abschluss-Bilanz` (bisher Schritt 6); der bisherige Schritt 3 (Alterungshinweis) entfaellt als Sektion (Inhalt wandert in 1.2). Interne Verweise auf alte Schritt-Nummern im Skill im selben Zug nachziehen. Alle Folgeschritte fuellen nur noch Inhalt

#### Schritt 1.2: Neue Sektion `## Schritt 3: Voranalyse` (Agenten-Auftrag inline)
- **Zweck:** die lesende Pruefung je Fund gegen den Projektstand — einzige Datei, weil `kit-sync` nur `SKILL.md` verteilt
- **Dateien:** `skills/dtb-idea-triage/SKILL.md`
- **Input:** T2, T3, Probelauf-Tabelle `becken-vorsortierung.md` (Spalten als Vorbild)
- **Output:**
  - Weiche: < 5 Funde → Voranalyse inline im Hauptkontext, keine Agenten; sonst Aufteilung in Portionen zu hoechstens 25 Funden, je Portion ein Hintergrund-Agent (Typ `Explore` — werkzeugseitig ohne Edit/Write; Prompt zusaetzlich „nur lesen"). **Rueckfall:** `Explore` in der Umgebung nicht verfuegbar → Typ `general-purpose` mit demselben Auftrag (Schreibverbot nur im Prompt, wie die Sub-Agenten von `dtb:impl-review`) und genau eine Hinweiszeile `⚠ Agenten-Typ Explore nicht verfuegbar — Voranalyse mit general-purpose, Schreibverbot nur im Auftrag`
  - Agenten-Prompt inline: eigene Portion (voller Text) + Nummer und Kurztitel ALLER Becken-Funde (fuer Verwandtschaft ueber Portionsgrenzen); Pruefauftrag gegen Projektstand (Skills/Code, `archive/` inkl. `ARCHIVE_LOG.md`, `INBOX.md`, `lessons.md`, `archive/INBOX-BEFUNDE-verworfen.md`); Dublette = Ersetzungsprobe (Kurzform inline, Laufzeit-Autarkie; enthaelt woertlich „gleiche Aussage" — Spiegel-Zaehlung, Schritt 3.2)
  - Festes Ergebnis-Format (T3), eine Zeile je Fund
  - Der bisherige Alterungshinweis (alter Schritt 3) geht als Pflicht-Indiz in den Agenten-Auftrag ein (Datei nach dem Befund geaendert → im Grund nennen); die Sektion ist bereits in 1.1 entfallen
- **Ausfall-Regel:** Agent liefert nichts oder unparsebares Format → seine Funde gelten als „ohne Vorschlag" und gehen in Stufe 2 (nie „nichts gefunden" — Werkzeug-Fehlschlag ist kein Datenbefund); Gate: Zeilenzahl des Ergebnisses = Zahl der Funde der Portion
- **Spaltenpruefung je Zeile:** jede Ergebniszeile hat genau 6 Spalten (escapte `\|` zaehlen nicht als Trenner); Abweichung → Ausfall nur fuer diesen Fund (ohne Vorschlag → Stufe 2). Grund: ein unescapter Trenner im Grund verschiebt die Spalten, ohne dass das Zeilenzahl-Gate anschlaegt
- **Pruefbarer Ort:** jeder `Verwerfen`-Vorschlag nennt im Beleg mindestens einen nachsehbaren Ort (Datei:Zeile oder Commit-SHA); fehlt er → Einzelfall, auch bei Sicherheit `hoch` (Pre-Mortem plan-review 2026-10-16: plausibler Beleg ohne Ort rutscht bei „Alle uebernehmen" durch)

#### Schritt 1.3: Konsolidierung im Hauptkontext
- **Zweck:** aus den Agenten-Zeilen die Vorlage bauen — Buendel ueber Portionsgrenzen, Einzel/Sammel-Abgrenzung
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (Inhalt von `## Schritt 4: Konsolidieren` — Titel aus dem Geruest 1.1)
- **Input:** Ergebnis-Zeilen aller Agenten
- **Output:**
  - Buendel = Zusammenhangskomponenten der `Verwandt`-Angaben (transitiv), nur wenn mindestens ein Glied `Befoerdern` traegt; Traeger = das juengste Glied (hoechste Nummer) mit Vorschlag `Befoerdern` (deterministisch, kein eigenes Feld in T3 noetig — Probelauf waehlte #131 als „spaeteren, konkreteren"); der Traeger steht sichtbar in der Buendel-Zeile, wer ihn aendern will, streicht die Buendel-Zeile → Glieder einzeln in Stufe 2; Buendel aus lauter Verwerfen-Vorschlaegen werden nicht gebildet
  - **Einzelfall** (mechanisch aus den Feldern): Vorschlag `Unklar` ODER Vorschlag `Verwerfen` mit Sicherheit ≠ `hoch` ODER `Verwerfen` ohne pruefbaren Ort im Beleg ODER „ohne Vorschlag" (Agenten-Ausfall, auch zeilenweise aus der Spaltenpruefung); Faelligkeit `L1` bleibt erhalten (Zwangsentscheidung in Stufe 2)
  - Kappung: hoechstens `einzeln_pro_lauf` Einzelfaelle je Lauf, aelteste zuerst; der Rest bleibt unveraendert im Becken (ungesichtet) und kommt im naechsten Lauf erneut in die Voranalyse
  - Alles andere = Sammelliste; Lektion-Vorschlaege laufen hier durch `## Schritt 3: Duplikat-Check` von `dtb:lesson` — Treffer → Zeile wird zu „Verwerfen — Lektion L{N} deckt ab"
  - Uebersicht vor der Vorlage (ersetzt die alte `Becken-Triage`-Uebersicht): Zahl Funde, Buendel, Sammelliste, Einzelfaelle, zurueckgestellt durch Kappung

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Neue Sektionen `## Schritt 3: Voranalyse` und `## Schritt 4: Konsolidieren` mit inline Agenten-Prompt und Ergebnis-Format
- [ ] Frontmatter und Config nachgezogen

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -E "^allowed-tools:.*\bAgent\b" skills/dtb-idea-triage/SKILL.md` trifft
- [ ] Geruest vollstaendig: `tr -d '\r' < skills/dtb-idea-triage/SKILL.md | grep -c -x -F` je Titel = 1 fuer alle sechs Titel aus 1.1 (Schritt 3–8), und `grep -c "^## Schritt [0-9]" skills/dtb-idea-triage/SKILL.md` ergibt keine doppelte Nummer
- [ ] `grep -x -F "## Schreibmechanik INBOX-BEFUNDE.md" skills/dtb-idea-triage/SKILL.md` trifft 1× (Checkpoint-Anker unversehrt)
- [ ] `grep -n "einzeln_pro_lauf" workflow.config.yaml skills/dtb-idea-triage/SKILL.md` trifft in beiden Dateien
- [ ] Im Agenten-Prompt-Block keine Schreib-Anweisung: `grep -n -i "schreib\|edit\|write" ` auf den Prompt-Fence liefert nur die Verbots-Zeile („nur lesen")

#### Manual
- [ ] Der Agenten-Prompt ist ohne Kit-Wissen lesbar (Laufzeit-Autarkie) und in Zielprojekten sinnvoll („Projektstand" statt „Kit-Stand")

---

## Phase 2: Sammelliste, Schreibwege und Stufe 2

### Ziel
Der Mensch bestaetigt eine Sammelliste mit Veto; danach wird Eintrag fuer Eintrag sofort geschrieben (Ziel vor Quelle, L43). Gestrichene Zeilen und Einzelfaelle laufen durch die bestehende Einzeltriage (Stufe 2).

### Schritte

#### Schritt 2.1: Sammelliste (Vorlage + Antwortregeln)
- **Zweck:** die eine Bestaetigung fuer alle sicheren Vorschlaege (Entscheidung (1))
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (Inhalt von `## Schritt 5: Sammelliste` — Titel aus dem Geruest 1.1)
- **Input:** Konsolidierung aus 1.3; Vorbilder `dtb:impl-review` Schritt 9 und Checkpoint-Sammelvorlage
- **Output:**
  - Vorlage: Kopfzeile mit Zahlen; Block **Buendel** oben (je Buendel eine Zeile: Traeger, Glieder, Wirkung); danach je Fund eine Zeile `Nr · Vorschlag · Grund (gekuerzt) · Beleg (gekuerzt) → Ziel`
  - EINE `AskUserQuestion`: `Alle uebernehmen (Vorschlag)` / `Nummern streichen` / `Einzeln durchgehen`; `Nummern streichen` → Freitext, gestrichene Zeilen gehen in Stufe 2 (nicht verworfen!); Buendel-Zeile streichen → Glieder einzeln in Stufe 2
  - `Abbruch`/unklare Antwort → nichts schreiben, Lauf endet mit Zeile „Nichts geschrieben — Vorschlaege verworfen, Becken unveraendert"
  - Leere Sammelliste → Block entfaellt still
  - `allowed-tools` um `AskUserQuestion` ergaenzt (L75)

#### Schritt 2.2: Schreibwege je Vorschlagsart (sofort, Ziel vor Quelle)
- **Zweck:** jede bestaetigte Zeile einzeln und abbruchsicher festschreiben (Entscheidung (5))
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (Inhalt von `## Schritt 7: Entscheidung ausfuehren` — Titel aus dem Geruest 1.1, bisheriger Schritt 5 erweitert)
- **Input:** bestaetigte Sammelliste
- **Output:** Unterabschnitte je Art, jeweils Ziel schreiben → pruefen → Becken-Zeile entfernen. **Jeder der sechs Unterabschnitte endet mit der woertlich gleichen Zeile `**Zuletzt:** Becken-Zeile entfernen.`** (plan-review 2026-10-16) — auch Befoerdern und Verwerfen werden auf diesen Wortlaut gezogen (bisher „ERST JETZT die Zeile aus dem Becken entfernen" / „Zeile aus dem Becken entfernen"), Verhalten unveraendert:
  - **Befoerdern** — Verhalten unveraendert (5a inkl. Duplikat-Check gegen `INBOX.md`), nur der Schlusssatz nach Schema
  - **Buendel** — Traeger befoerdern, Text-Suffix „(enthaelt #a, #b, …)"; danach je Glied Verwerfen-Weg mit Begruendung „gebuendelt in #{Traeger}"; Becken-Zeilen der Glieder erst nach ihrem Archiv-Eintrag entfernen
  - **Verwerfen** — wie 5b; Begruendung = `{Grund} — Beleg: {Beleg}` (T5, keine neue Spalte)
  - **Nachtrag** — Ziel-Idee in `INBOX.md` um `Nachtrag {YYYY-MM-DD} aus Befund #{N}: {Text}` ergaenzen (Muster `dtb:idea-review` Zusammenlegen), dann Archiv „nachgetragen in #{Ziel}", dann Becken-Zeile entfernen; Ziel-Idee fehlt oder ist nicht `Offen`/`In Arbeit` → Zeile faellt in Stufe 2
  - **Lektion** — Felder per `## Schritt 2: In 4 Felder strukturieren`, Schreiben per `## Schritt 4: Append-only speichern` aus `dtb:lesson` (Herkunfts-Marker `(via Triage {YYYY-MM-DD}, Befund #{N})` ans Ende von `Context`); dann Archiv „als Lektion L{N} erfasst", dann Becken-Zeile entfernen
  - **Fachfrage** — Zielfeature aus dem Vorschlag; Ziel-Datei per `## Schritt 3: Ziel-Datei waehlen`, Zeile + exakter Duplikat-Check per `## Schritt 4: …`, Schreiben per `## Schritt 5: Schreiben + Abschluss` aus `dtb:open-question` (deren Einzelbestaetigung ersetzt die Sammelliste); kein passendes Feature → Befoerdern mit Vorsatz „Fachfrage: "; dann Archiv „als Fachfrage in features/{slug}/ erfasst"
  - Lesestand-Pruefung vor JEDEM Schreiben, Referenz-mtime nach eigenem Schreibvorgang nachfuehren (L46)
  - Schreibfehler mitten drin → melden, Rest unveraendert im Becken lassen, nie zurueckrollen

#### Schritt 2.3: Struktur-Check fuer die Ausfuehrung per Referenz
- **Zweck:** nie auf veralteter Basis schreiben, wenn `lesson`/`open-question` umgebaut werden (Spec-Risiko 4)
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (im Schritt 7, vor dem ersten Schreiben)
- **Input:** Muster `dtb:workflow-checkpoint` Schritt 0 „Struktur-Check (Kopplungs-Waechter)"
- **Output:**
  - Quelle aufloesen Repo zuerst, dann `~/.claude/skills/`; nur Quellen, deren Typ in der bestaetigten Liste vorkommt (L42)
  - Anker-Tabelle: lesson Schritt 2/3/4, open-question Schritt 3/4/5, idea `## Duplikat-Check`; Grep zeilenverankert (`tr -d '\r' | grep -x -F`)
  - Statuszeile `🧩 Struktur-Check: {n}/{n} Anker …`; zwei getrennte Fehlerpfade (Installation fehlt / Anker fehlt) → Zeilen des gefallenen Typs gehen in Stufe 2 statt geschrieben zu werden

#### Schritt 2.4: Stufe 2 und Abschluss-Bilanz
- **Zweck:** die bestehende Einzeltriage fuer den Rest; vollstaendige Bilanz
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (Inhalt von `## Schritt 6: Einzeln entscheiden (Stufe 2)` und `## Schritt 8: Abschluss-Bilanz` — Titel aus dem Geruest 1.1)
- **Input:** Einzelfaelle (≤ `einzeln_pro_lauf`), gestrichene Zeilen, Agenten-Ausfaelle
- **Output:**
  - Stufe 2 zeigt je Fall zusaetzlich Vorschlag, Grund, Beleg und bei `Unklar` die Frage der Agenten; Aktionen 1–3 unveraendert (Liegenlassen nur hier, Zwangsentscheidung bei `L1`)
  - Reihenfolge des Laufs: Sammelliste → Schreiben → Stufe 2 (gestrichene Zeilen kommen damit nach den sicheren Faellen)
  - Bilanz: Befoerdert, davon Buendel, Nachgetragen, Lektionen, Fachfragen, Verworfen, Liegengelassen, zurueckgestellt (Kappung); bestehende Hinweiszeile `/dtb:idea-review` bleibt
  - `## Wichtig` angepasst: „Nie das ganze Becken sichten" → „Nie das ganze Becken einzeln vorlegen"; „Sofort schreiben, nie sammeln" bleibt mit Hinweis, dass die Sammelliste eine Bestaetigung ist, kein Sammel-Schreiben

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Sammelliste mit Veto, sechs Schreibwege, Struktur-Check, Stufe 2 und erweiterte Bilanz in `skills/dtb-idea-triage/SKILL.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -x -F` trifft je 1×: `## Schritt 5: Sammelliste`, `## Schritt 6: Einzeln entscheiden (Stufe 2)`, `## Schritt 7: Entscheidung ausfuehren`, `## Schritt 8: Abschluss-Bilanz` in `skills/dtb-idea-triage/SKILL.md`
- [ ] Anker-Tabelle im Struktur-Check nennt alle 7 Anker woertlich; jeder davon existiert zeilenverankert in seiner Quelle (Schleife `tr -d '\r' | grep -x -F` ueber lesson/open-question/idea → 7/7)
- [ ] `grep -c "gebuendelt in #\|nachgetragen in #\|als Lektion L\|Lektion L{N} deckt ab" skills/dtb-idea-triage/SKILL.md` ≥ 4
- [ ] `grep -E "^allowed-tools:.*AskUserQuestion" skills/dtb-idea-triage/SKILL.md` trifft
- [ ] Ziel-vor-Quelle: `grep -c -F "**Zuletzt:** Becken-Zeile entfernen." skills/dtb-idea-triage/SKILL.md` = 6 (je Schreibweg genau einmal, jeweils letzter Punkt seines Unterabschnitts)

#### Manual
- [ ] Die Sammelliste ist bei ~50 Zeilen noch pruefbar (Probe am Probelauf-Becken, Phase 4)

---

## Phase 3: Kopplungen und Kit-Doku nachziehen

### Ziel
Alle Quellen, die die Triage jetzt per Referenz liest, kennen ihren neuen Leser; die Kit-Regeln nennen die neuen Schreibwege (L3, Kopplungs-Regel).

### Schritte

#### Schritt 3.1: Kopplungs-Hinweise in `dtb:lesson` und `dtb:open-question`
- **Zweck:** Umbau einer Anker-Sektion soll den zweiten Leser mitziehen
- **Dateien:** `skills/dtb-lesson/SKILL.md` (Hinweise an Schritt 2/3/4 + „Zwei Eingangskanaele"), `skills/dtb-open-question/SKILL.md` (neue Hinweise an Schritt 3/4/5)
- **Input:** Anker-Tabelle aus 2.3
- **Output:** jeder Kopplungs-Hinweis nennt `dtb:workflow-checkpoint` (lesson) bzw. nur `dtb:idea-triage` (open-question) als Leser per Referenz; „Zwei Eingangskanaele" erwaehnt die Triage als dritten Weg (Becken-Lektion, Bestaetigung ueber Sammelliste)

#### Schritt 3.2: `skills/CLAUDE.md` nachziehen
- **Zweck:** Autoren-Kanon aktuell halten
- **Dateien:** `skills/CLAUDE.md`
- **Input:** Spec, Schritt 2.2
- **Output:**
  - Zwei-Becken-Regel: Schreiber-Tabelle um die neuen Triage-Ziele (Nachtrag in `INBOX.md`, `lessons.md`, `features/*/` per open-question, Archiv) ergaenzt; Satz „Ein Becken-Eintrag wird nie gearbeitet" um „— auch die Agenten der Voranalyse lesen nur"
  - Rueckfragen-Defaults: neue Zuordnungszeile `idea-triage` Schritt 5 — Sammelliste (Einzelfaelle = Unklar / Verwerfen < hoch / ohne Vorschlag)
  - Duplikat-Schutz: „Vierter Anwender per Referenz" → zweiter Anwender per Referenz `idea-triage` (lesson Schritt 3, open-question Schritt 4) ergaenzt
  - Duplikat-Schutz, Kopplungs-Hinweis Stufe 2 (Laufzeit-Kurzformen): `idea-triage` (Agenten-Auftrag in `## Schritt 3: Voranalyse`) als vierte Kurzform neben `idea`, `task`, `bug-report` aufnehmen; Zielzahl `gleiche Aussage` 7 → **8** (Aufschluesselung im Hinweis nachziehen); Zielzahl `Informationsverlust ersetzen koennte` bleibt **4**. Voraussetzung aus 1.2: die Kurzform im Agenten-Auftrag enthaelt woertlich „gleiche Aussage" (plan-review 2026-10-16)

#### Schritt 3.3: DSR §6.4, Root-`CLAUDE.md`, Repo-weiter Namens-Sweep
- **Zweck:** Beschreibungen konsistent; keine verwaiste Referenz auf alte Schritt-Nummern (L3)
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` §6.4, `CLAUDE.md`, ggf. Treffer des Sweeps
- **Input:** `grep -rn "idea-triage" skills/ CLAUDE.md dtb-project/project-rules/` (ohne `archive/`, Changelog)
- **Output:**
  - §6.4: „Er wird zum Vorgang erst durch die Befoerderung" ergaenzt um die uebrigen Ausgaenge (Lektion, Fachfrage, Nachtrag, gebuendelt — alle verlassen das Becken nur nach Bestaetigung); Hinweis: Klasse-B-Seed, Bestandsprojekte erhalten die Ergaenzung nicht — zulaessig, weil die Laufzeit-Regel im Skill selbst steht (L82)
  - Root-`CLAUDE.md`: Beschreibung `idea-triage` (Vorsortierung, Sammelliste, Ausgaenge)
  - Sweep: jede Fundstelle, die Schritt-Nummern oder das Verhalten der Triage zitiert, geprueft und ggf. angepasst; Ergebnis als Liste im Commit-Text (L20: Pruefprotokoll muss irgendwo landen)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Kopplungs-Hinweise in lesson (3) und open-question (3)
- [ ] `skills/CLAUDE.md`, DSR §6.4, Root-`CLAUDE.md` nachgezogen

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "dtb:idea-triage" skills/dtb-lesson/SKILL.md` ≥ 4 (3 Kopplungs-Hinweise + Eingangskanal)
- [ ] `grep -c "dtb:idea-triage" skills/dtb-open-question/SKILL.md` ≥ 3
- [ ] Spiegel-Zielzahlen Duplikat-Schutz: `grep -ro "Informationsverlust ersetzen koennte" skills/ | wc -l` = 4 und `grep -ro "gleiche Aussage" skills/ | wc -l` = 8; `skills/CLAUDE.md` nennt woertlich „Zielzahl 8" im Kopplungs-Hinweis
- [ ] `grep -n "idea-triage" skills/CLAUDE.md` trifft in der Rueckfragen-Zuordnungstabelle (Zeile beginnt mit `|`)
- [ ] Die Checkpoint-Anker-Pruefung bleibt gruen: 5/5 Anker aus `skills/dtb-workflow-checkpoint/SKILL.md` Schritt 0 zeilenverankert gefunden

---

## Phase 4: Probelaeufe

### Ziel
Belegen, dass der Umbau die Spec erfuellt — Schreibwege im Testprojekt, Vorschlagsqualitaet am echten Becken (L74: immer gegen die Repo-Fassung).

### Schritte

#### Schritt 4.1: Testprojekt im Scratchpad anlegen
- **Zweck:** alle Schreibwege ausfuehren, ohne globale Dateien des Kits zu beruehren (Worktree-Grenze)
- **Dateien:** Scratchpad (nicht-Git → Guard `DURCHLASS-NOGIT`): `workflow.config.yaml`, `dtb-project/project-workflows/{INBOX.md, INBOX-BEFUNDE.md}`, `dtb-project/project-rules/lessons.md`, ein Feature-Ordner mit `spec.md`, ein Mini-Codebestand
- **Input:** 8 konstruierte Funde, die jeden Weg treffen: Befoerdern, Buendel (2 Glieder), Verwerfen sicher, Verwerfen unsicher, Nachtrag, Lektion (davon 1 Dublette zu bestehender Lektion), Fachfrage mit und ohne passendes Feature, Unklar
- **Output:** Testprojekt + Erwartungstabelle (Fund → erwarteter Weg) als `features/triage-vorsortierung/probelauf-testprojekt.md`

#### Schritt 4.2: Wirklauf im Testprojekt
- **Zweck:** Success Criteria 1–9 belegen
- **Dateien:** nur Testprojekt; Protokoll in `features/triage-vorsortierung/probelauf-testprojekt.md`
- **Input:** Repo-Fassung `skills/dtb-idea-triage/SKILL.md` (nicht die installierte Kopie)
- **Output:** Protokoll je Fund: erwartet / tatsaechlich / Datei-Beleg; zusaetzlich (plan-review 2026-10-16):
  - Abbruch-Test (nach 3 geschriebenen Zeilen abbrechen → 3 bleiben, Rest im Becken)
  - Becken-leer-Test (eine Zeile, keine Agenten)
  - **Unter-5-Test:** zweiter Lauf mit 3 Funden → keine Hintergrund-Agenten, Voranalyse inline
  - **Negativtest Struktur-Check:** Kopie von `dtb-lesson/SKILL.md` mit umbenannter Anker-Sektion als aufgeloeste Quelle → ⚠-Zeile „Struktur-Check fehlgeschlagen", Lektions-Zeilen werden nicht geschrieben, sondern gehen in Stufe 2

#### Schritt 4.3: Trockenlauf gegen das echte Becken
- **Zweck:** Vorschlagsqualitaet und Pruefbarkeit der Sammelliste bei realer Groesse (Spec-Kriterium 11, Manual von Phase 2)
- **Dateien:** Kopie von `dtb-project/project-workflows/{INBOX-BEFUNDE.md, INBOX.md, archive/}` und `dtb-project/project-rules/lessons.md` in ein zweites Testprojekt im Scratchpad (nicht-Git → Guard `DURCHLASS-NOGIT`; im Worktree selbst bricht der Voll-Guard ab); Projektstand fuer die Agenten = dieser Worktree (Pfad im Auftrag). Schreibt im Kit NICHTS ausser dem Protokoll `features/triage-vorsortierung/probelauf-becken.md` (Variante A, plan-review 2026-10-16)
- **Input:** Schritte 3–5 des Skills, Abbruch vor dem Schreiben (Sammelliste zeigen, dann `Abbruch`)
- **Output:** Gegenueberstellung zur Tabelle `becken-vorsortierung.md` (Befoerdern / Verwerfen / Unklar / Buendel), Abweichungen begruendet

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `probelauf-testprojekt.md` mit 8/8 Wegen belegt, dazu Abbruch-, Becken-leer-, Unter-5- und Negativtest
- [ ] `probelauf-becken.md` mit Gegenueberstellung

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f features/triage-vorsortierung/probelauf-testprojekt.md && test -f features/triage-vorsortierung/probelauf-becken.md`
- [ ] Im Testprojekt nach dem Lauf: `grep -c "^| [0-9]" INBOX-BEFUNDE.md` = Zahl der liegengelassenen + zurueckgestellten Funde laut Protokoll
- [ ] `git -C {kit-root} status --porcelain dtb-project/project-workflows/INBOX-BEFUNDE.md dtb-project/project-workflows/INBOX.md dtb-project/project-rules/lessons.md` leer (Trockenlauf hat nichts geschrieben)

#### Manual
- [ ] Sammelliste des Trockenlaufs ist in einem Durchgang pruefbar
- [ ] Abweichungen zum Probelauf vom 2026-10-16 sind plausibel begruendet

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| T1 Kappung | (a) `altbestand_pro_lauf` umdeuten · (b) neuer Schluessel `einzeln_pro_lauf`, Rueckfall auf den alten · (c) keine Kappung | **b** (Vorschlag) | Spec: Kappung nur noch fuer Einzelfaelle. Umdeuten gaebe dem alten Namen zwei Bedeutungen (L47); der Rueckfall haelt Bestandsprojekte ohne neuen Schluessel lauffaehig |
| T2 Agenten-Aufteilung | (a) ein Agent fuer alles · (b) Portionen ≤ 25, jeder sieht Nummer+Kurztitel aller Funde · (c) nach Themen | **b** (Vorschlag) | Probelauf: 3 Agenten fuer 73 Funde. Die Kurzliste aller Funde macht Verwandtschaft ueber Portionsgrenzen sichtbar; das Buendeln selbst passiert im Hauptkontext (1.3) |
| T3 Ergebnis-Format | Freitext · feste Zeile | **feste Zeile** `#{N} \| {Vorschlag} \| {Grund} \| {Beleg} \| {Sicherheit} \| {Verwandt}`; Vorschlag ∈ `Befoerdern`, `Verwerfen: erledigt\|ueberholt\|Dublette #N\|falsches Repo`, `Nachtrag #N`, `Lektion`, `Fachfrage {slug\|—}`, `Unklar: {Frage}`; Sicherheit ∈ `hoch\|mittel\|niedrig`; genau 6 Spalten je Zeile; `Verwerfen`-Beleg mit Datei:Zeile oder SHA | Mechanisch parsebar (Einzelfall-Abgrenzung, Zeilenzahl-Gate + Spaltenpruefung); Spalten wie im Probelauf; Ortspflicht gegen plausible, aber unpruefbare Verwerfen-Belege (plan-review 2026-10-16) |
| T4 Agenten-Typ | `Explore` · `general-purpose` + Lese-Anweisung | **`Explore`, Rueckfall `general-purpose`** (plan-review 2026-10-16) | Ohne Edit/Write schon werkzeugseitig; fehlt der Typ, traegt das Schreibverbot im Auftrag (sichtbare ⚠-Zeile) — sonst ginge in solchen Umgebungen das ganze Feature verloren |
| T5 Beleg im Archiv | eigene Spalte · in der Begruendung | **in der Begruendung** (`{Grund} — Beleg: {Beleg}`) | `INBOX-BEFUNDE-verworfen.md` ist append-only; eine neue Spalte braeche bestehende Zeilen in Bestandsprojekten |
| T6 Lauf-Reihenfolge | Einzelfaelle zuerst (wie impl-review) · Sammelliste zuerst | **Sammelliste zuerst** | Entspricht „danach den normalen Triage-Schritt"; gestrichene Zeilen landen ohne zweiten Durchgang in Stufe 2 |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Frontmatter, Config, Schritt 2 — `f0f7a45`
- [x] 1.2 Voranalyse (Agenten-Auftrag) — `f0f7a45`
- [x] 1.3 Konsolidierung — `f0f7a45`
- [x] 2.1 Sammelliste
- [x] 2.2 Schreibwege
- [x] 2.3 Struktur-Check
- [x] 2.4 Stufe 2 + Bilanz
- [ ] 3.1 Kopplungs-Hinweise lesson/open-question
- [ ] 3.2 skills/CLAUDE.md
- [ ] 3.3 DSR §6.4, Root-CLAUDE.md, Sweep
- [ ] 4.1 Testprojekt
- [ ] 4.2 Wirklauf Testprojekt
- [ ] 4.3 Trockenlauf echtes Becken

---

## Umsetzung

Umsetzung mit `/dtb:implement Triage-Vorsortierung` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/triage-vorsortierung/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
