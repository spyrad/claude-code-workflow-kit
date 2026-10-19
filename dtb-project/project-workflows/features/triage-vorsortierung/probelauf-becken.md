# Trockenlauf gegen das echte Becken (Phase 4, Schritt 4.3)

**Datum:** 2026-10-16
**Skill-Fassung:** Repo-Fassung `skills/dtb-idea-triage/SKILL.md` (Stand nach `9004f2c`), Schritte 2–5, Abbruch an der Sammelliste
**Material:** Kopie von `INBOX-BEFUNDE.md` (73 Funde: 45 neu, 28 Altbestand, 0 `L1`), `INBOX.md`, `archive/`, `lessons.md`, `workflow.config.yaml` in ein Scratchpad-Testprojekt (nicht-Git → `DURCHLASS-NOGIT`). Projektstand fuer die Agenten = dieser Worktree (Pfad im Auftrag)
**Vergleichsbasis:** [becken-vorsortierung.md](becken-vorsortierung.md) (Probelauf 2026-10-16, 3 Agenten, ohne Nachtrag/Lektion als Ausgang)

## Ablauf

| Schritt | Ergebnis |
|---------|----------|
| 2 Sichtungsmenge | 73 ungesichtete Funde, aelteste zuerst; `einzeln_pro_lauf` = 5 (Config) |
| 3a Weiche | ≥ 5 → 3 Portionen (25 / 25 / 23), 3 Agenten Typ `Explore` parallel; kein Rueckfall noetig |
| 3b Auftrag | woertlich aus dem Skill, Platzhalter gefuellt (`{portion}` voller Zeilentext, `{alle}` = 73 × `#N` + 80 Zeichen) |
| 3c Gates | Zeilenzahl 25/25, 25/25, 23/23 · alle 73 Zeilen genau 6 Spalten · alle Vorschlaege bekannt → **kein Ausfall**. Portion 3 haengte eine Prosazeile an (verbotene „Prosa danach"); das Gate zaehlt nur `#`-Zeilen und blieb davon unberuehrt |
| 4a Struktur-Check | benoetigt: lesson (3 Lektion-Vorschlaege), idea (Befoerdern) → Anker gefunden (Repo-Quelle `skills/`) |
| 4b Buendel | 11 Verwandtschafts-Gruppen, 7 Buendel mit 42 Gliedern — siehe Befund B |
| 4c Lektionen | #77, #79, #80 gegen `lessons.md` (Stichwort-Grep nach `dtb:lesson` Schritt 3): Treffer L59, L36, L38 tragen andere Aussagen → keine Dublette, keine Umwandlung |
| 4d/4e | 8 Einzelfaelle, 5 vorgelegt, 3 zurueckgestellt (Kappung) |
| 4f Uebersicht | `Buendel 7 (42 Glieder) · Sammelliste 23 · Einzelfaelle 5 · Zurueckgestellt 3` — Summenprobe 42 + 23 + 5 + 3 = 73 ✓ (die Probe aus A2 des Testprojekt-Protokolls, hier im Auswerteskript ausgefuehrt) |
| 5 Sammelliste | 34 Zeilen (Kopf + 7 Buendel + 23 Einzelzeilen), Wortlaut unten · Antwort laut Plan: **`Abbruch`** → `Nichts geschrieben — Vorschlaege verworfen, Becken unveraendert.` |

**Nichts geschrieben (Automated-Beleg):** `git status --porcelain` auf `INBOX-BEFUNDE.md`, `INBOX.md`, `lessons.md` leer; die Scratchpad-Kopien sind byte-gleich mit dem Kit (`cmp`).

## Gegenueberstellung zum Probelauf

| Vorschlag | Probelauf | Trockenlauf |
|-----------|-----------|-------------|
| Befoerdern | 51 | 50 |
| Verwerfen (erledigt / ueberholt / Dublette / falsches Repo) | 16 | 15 |
| Unklar | 6 | 1 |
| Nachtrag | — (Ausgang fehlte) | 4 |
| Lektion | — (Ausgang fehlte) | 3 |
| **Summe** | **73** | **73** |

**Gleiche Klasse bei 65 von 73 Funden.** Die 8 Abweichungen:

| # | Probelauf | Trockenlauf | Begruendung |
|---|-----------|-------------|-------------|
| 46, 58 | Verwerfen: Dublette #100 | Nachtrag #100 (mittel) | Probelauf hatte keinen Nachtrag-Ausgang und empfahl selbst „als Beleg an #100 haengen" — der neue Ausgang setzt genau das um |
| 103 | Unklar (Nachtrag oder eigene Idee?) | Nachtrag #99 (hoch) | Die Frage des Probelaufs ist mit dem Nachtrag-Ausgang beantwortbar geworden |
| 106 | Befoerdern („als Korrektur-Nachtrag in #99, keine eigene Idee") | Nachtrag #99 (mittel) | Probelauf beschrieb einen Nachtrag, konnte ihn aber nur als Befoerdern ausdruecken |
| 77, 79, 80 | Unklar („Lektion, Triage hat keinen Ausgang") | Lektion (mittel) | Die Prozessluecke des Probelaufs ist geschlossen |
| 60 | Unklar (Harness oder Kit?) | Verwerfen: erledigt (mittel) | Der Agent fand L69 (Ursache + Workaround) — bleibt wegen `mittel` Einzelfall, der Mensch entscheidet |

Groessenordnung reproduziert (Spec-Kriterium 11): Befoerdern 51→50, Verwerfen 16→15; der Rueckgang bei Unklar (6→1) wandert vollstaendig in die neuen Ausgaenge.

**Einschraenkung der Unabhaengigkeit:** `becken-vorsortierung.md` liegt im Change-Ordner und damit im Projektstand, den die Agenten lesen. Agent 3 meldete ausdruecklich, die Datei gesehen zu haben. Die Uebereinstimmung ist daher teils Abgleich mit dem Probelauf, nicht nur unabhaengige Wiederholung. Die Begruendungen der Agenten tragen aber durchweg eigene, frische Belege (Zeilennummern im heutigen Stand, Commits nach dem Probelauf wie `3fc03ee` bei #69).

## Buendel im Vergleich

| Probelauf | Trockenlauf |
|-----------|-------------|
| 5 Worktree-Hand-off-Empfang (#123, #128, #131) | ✅ **B6** — #131 traegt #123, #128 (#114 als Dublette von #131 verworfen, Einzelfall) |
| 6 Ueberwachungs-Tick (#104, #116, #127) | ✅ **B7** — #127 traegt #104, #116 |
| 7 kit-sync (#31, #51, #55, #82, #108, #109) | ✅ **B2** — #109 traegt dieselben sechs + #22 |
| 8 feature-discover (#18, #32, #47) | ✅ **B1** — #47 traegt #18, #32 |
| 10 Nachtraege (#103, #106 → #99 · #46, #58 → #100) | ✅ jetzt eigene Nachtrag-Zeilen statt Buendel |
| 1 Handoff-Regel · 2 `dtb:archive` · 3 `task.md`-Schiene · 4 `pane-start`-Kleinkram · 9 Zustand ohne Pfleger | ❌ **alle fuenf in B3 verschmolzen** — #132 traegt 20 Glieder |
| — | neu: **B4** #70 traegt #54 (Feld-Hygiene/Kriterien) · **B5** #125 traegt #56, #63 (relative Bezeichnungen Zeit/Ort) |

## Befunde

### B — Transitive Buendelung erzeugt ein Mega-Buendel (Skill-Defekt, Schritt 4b)

Schritt 4b bildet Buendel als **transitive** Zusammenhangskomponenten der `Verwandt`-Kanten (Plan 1.3). Die Agenten setzen `Verwandt` grosszuegig, und wenige Brueckenkanten verbinden fachlich getrennte Themen: #35 → #23/#52/#86, #90 ↔ #124 ↔ #115, #89 ↔ #88, #87 ↔ #83. Ergebnis: eine Komponente aus 25 Funden, davon 21 `Befoerdern` → **B3 mit Traeger #132 und 20 Gliedern**. Fuenf der zehn Probelauf-Buendel gehen darin auf.

Folgen:
- Eine B3-Zeile ist in der Sammelliste nicht ernsthaft pruefbar (Manual-Kriterium „in einem Durchgang pruefbar" faellt fuer diesen Block)
- Wird B3 gestrichen, gehen alle 21 Glieder einzeln in Stufe 2, und **gestrichene Zeilen zaehlen nicht gegen die Kappung** (4e) → 21 Einzelentscheidungen in einem Lauf. Genau das sollte die Vorsortierung verhindern
- Wird B3 uebernommen, entsteht EINE INBOX-Idee #132 fuer fuenf Changes; 20 Nummern gehen mit „gebuendelt in #132" ins Archiv

Ein Fix ist nicht Teil von Phase 4 (Plan-Bloecke sind waehrend der Umsetzung read-only). Moegliche Richtungen fuer den Folge-Change: (a) keine transitive Huelle — Buendel = Traeger + seine **direkten** Nachbarn; (b) nur **gegenseitige** Kanten zaehlen; (c) Groessendeckel (z.B. > 6 Glieder → Gruppe nicht buendeln, sondern als Hinweis „verwandt" in die Einzelzeilen). Im Probelauf entstanden die zehn Buendel durch Urteil im Hauptkontext, nicht durch eine Huellenregel.

> **Nachtrag 2026-10-18 — B3 behoben (Review-F1, Commit `d613277`):** 4b nutzt jetzt (a)+(b): nur gegenseitige Kanten, Buendel = Traeger + direkte gegenseitige Nachbarn, keine Huelle. Simulation derselben 73 Vorschlaege (`tb-konsolidiert.json`, Skript `gegenseitig.py` im Session-Scratchpad): **13 Buendel, groesstes 4 Funde** — Handoff #132/#86/#118/#121, archive #130/#87/#94/#129, pane-start #126/#89/#115/#124, Hand-off-Empfang #131/#123/#128, Tick #127/#104/#116, feature-discover #47/#18/#32, Pfleger #53/#52, kit-sync in drei Paaren. Das deckt die Probelauf-Themen 1–4 und 9 wieder getrennt ab. Die Sammelliste unten zeigt den Stand VOR dem Fix (nicht erneut gelaufen — Simulation auf denselben Agenten-Vorschlaegen, da 4b deterministisch ist); der Wirklauf der neuen Regel steht in [probelauf-testprojekt.md](probelauf-testprojekt.md) („Wiederholungslauf 2026-10-18").

### Weitere Beobachtungen

- **Prosa nach dem Ergebnis** (Portion 3): vom Gate korrekt ignoriert. Kein Handlungsbedarf, solange das Gate nur `#`-Zeilen zaehlt
- **Verworfen-Archiv fehlt im Kit:** `archive/INBOX-BEFUNDE-verworfen.md` existiert nicht (bisher wurde nie aus dem Becken verworfen); Agent 3 meldete den Abgleich als leer. Kein Defekt — der Skill legt die Datei beim ersten Verwerfen an (7b, im Testprojekt belegt)
- **Kuerzung der Gruende auf ~60 Zeichen** schneidet bei den langen Agenten-Saetzen oft vor der eigentlichen Aussage ab (z.B. #34 „Die Entscheidung wurde am 2026-09-07 revidiert: `lessons.md…`"). Der Beleg mit Ort bleibt sichtbar; Pruefbarkeit haengt dann am Beleg, nicht am Grund
- **Einzelfaelle:** alle 7 Verwerfen-Einzelfaelle tragen `mittel` und einen Ort — die Ortspflicht hat hier nichts ausgesondert; die Sicherheitsschwelle hat die Arbeit getan

## Sammelliste (Wortlaut, wie vorgelegt)

```
Sammelliste — 30 Vorschlaege, davon 7 Buendel

Buendel:
 B1  #47 traegt #18, #32  → INBOX.md #47; Glieder → Archiv „gebuendelt in #47"
 B2  #109 traegt #22, #31, #51, #55, #82, #108  → INBOX.md #109; Glieder → Archiv „gebuendelt in #109"
 B3  #132 traegt #23, #35, #52, #53, #83, #86, #87, #88, #89, #90, #92, #94, #115, #117, #118, #121, #124, #126, #129, #130 (verwandt: #44 Verwerfen, #46 Nachtrag, #58 Nachtrag, #84 Verwerfen)  → INBOX.md #132; Glieder → Archiv „gebuendelt in #132"
 B4  #70 traegt #54  → INBOX.md #70; Glieder → Archiv „gebuendelt in #70"
 B5  #125 traegt #56, #63 (verwandt: #66 Verwerfen)  → INBOX.md #125; Glieder → Archiv „gebuendelt in #125"
 B6  #131 traegt #123, #128 (verwandt: #60 Verwerfen, #69 Unklar, #114 Verwerfen)  → INBOX.md #131; Glieder → Archiv „gebuendelt in #131"
 B7  #127 traegt #104, #116 (verwandt: #102 Verwerfen)  → INBOX.md #127; Glieder → Archiv „gebuendelt in #127"

 1  #34   Verwerfen: erledigt        Die Entscheidung wurde am 2026-09-07 revidiert: `lessons.md… · Commit f75979d; .gitignore:10-16; dtb-p…   → Archiv
 2  #46   Nachtrag #100              Die beiden echten Kanten sind behoben (`plan-review.after` … · skills/dtb-plan-review/SKILL.md Frontma…   → INBOX.md #100
 3  #58   Nachtrag #100              Fall (2) ist erledigt (acb405e; `workflow-checkpoint.after`… · skills/dtb-greenfield-prd/SKILL.md Fron…   → INBOX.md #100
 4  #59   Befoerdern                 Die Worker-Sicht füllt eine Vorab-Frage weiter nur beim Urt… · skills/dtb-worker/SKILL.md:83-84, :98-1…   → INBOX.md
 5  #61   Befoerdern                 Die Tabelle ist weiter unsortiert (Reihenfolge 6, 8, 7 … 11… · dtb-project/project-rules/lessons.md:15…   → INBOX.md
 6  #62   Befoerdern                 Wohin die Minimal-Notiz bei hartem Stopp geschrieben wird, … · skills/dtb-worker/SKILL.md:555-558   → INBOX.md
 7  #64   Verwerfen: erledigt        `lessons.md` ist seit 2026-09-07 versioniert und reist mit … · Commit f75979d; .gitignore:10-12, :16; …   → Archiv
 8  #77   Lektion                    Der Anlass ist behoben (die Zwei-Becken-Regel nennt die Tri… · skills/CLAUDE.md:383-391; lessons.md L1…   → lessons.md
 9  #79   Lektion                    Eine wiederverwendbare Werkzeug-Falle ohne Gegenstueck in l… · lessons.md L38 (Zeile 34); Grep Anfuehr…   → lessons.md
10  #80   Lektion                    Dass das Arbeitsverzeichnis ueber Bash-Aufrufe erhalten ble… · skills/CLAUDE.md:559-566; lessons.md L6…   → lessons.md
11  #81   Verwerfen: erledigt        Die Migration ist als Aufgabe `inbox-becken-migration` erle… · ARCHIVE_LOG.md:90 (`daf7e24`, `badc097`…   → Archiv
12  #85   Verwerfen: ueberholt       Durch #91 entschieden: Die Sprachausgabe ist ein eigenes oe… · ARCHIVE_LOG.md:94   → Archiv
13  #91   Verwerfen: erledigt        Die Entscheidung ist umgesetzt: #41 ist mit Verweis auf das… · ARCHIVE_LOG.md:94; ls auf Desktop/insta…   → Archiv
14  #93   Befoerdern                 Die Zusammenfassung in Schritt 4 kennt weiter nur Behalten,… · skills/dtb-idea-review/SKILL.md:189-207   → INBOX.md
15  #96   Verwerfen: ueberholt       Die Bezugsidee #57 ist umgesetzt und archiviert, und die Ba… · skills/CLAUDE.md:334; ARCHIVE_LOG.md:10…   → Archiv
16  #101  Befoerdern                 `.env` fehlt weiter in der Kit-`.gitignore` (letzte Aenderu… · .gitignore (ganze Datei, kein .env); se…   → INBOX.md
17  #102  Verwerfen: erledigt        Der Beleg ist in #97 aufgegangen: Das Feature `ueberwachung… · archive/ueberwachungs-tick/spec.md:17, …   → Archiv
18  #103  Nachtrag #99               Ergaenzt die offene Idee #99 um die Schattenbetrieb-Stellen… · INBOX.md:19 (#99, Offen); Grep jev/type…   → INBOX.md #99
19  #106  Nachtrag #99               INBOX #99 Punkt (2) nennt die Station-1-Erhebung weiterhin … · INBOX.md:19 („das Eval-Set dafuer ist g…   → INBOX.md #99
20  #119  Befoerdern                 idea-triage nennt `Altbestand` nur als Sichtungsvermerk „au… · skills/dtb-idea-triage/SKILL.md:103 (ke…   → INBOX.md
21  #120  Befoerdern                 Beide gespiegelten Matrizen haben fuer RETHINK weiter genau… · skills/dtb-plan-review/SKILL.md:222; dt…   → INBOX.md
22  #122  Befoerdern                 Check 4 erlaubt weiter nur fuenf Dateinamen; `review.md`, B… · skills/dtb-project-health/SKILL.md:172-…   → INBOX.md
23  #136  Verwerfen: falsches Repo   Die Sprachausgabe ist seit 2026-09-11 ein eigenes Repo (git… · ARCHIVE_LOG.md:94; lessons.md:84 (L88)   → Archiv
```

**Einzelfaelle (Stufe 2, aelteste zuerst):** #44 Verwerfen: erledigt (mittel) · #60 Verwerfen: erledigt (mittel) · #66 Verwerfen: erledigt (mittel) · #69 Unklar („Sollen `dtb:task` und `dtb:bug-report` ebenfalls modellaufrufbar werden, oder ist der Umfang mit `3fc03ee` erledigt?") · #75 Verwerfen: erledigt (mittel)
**Zurueckgestellt (Kappung 5):** #78, #84, #114 — bleiben ungesichtet, naechster Lauf

Die Auswerte-Skripte (Gates, Konsolidierung, Vergleich, Sammelliste) liegen nur im Scratchpad dieser Session; die Ergebnisse oben sind ihre Ausgabe.
