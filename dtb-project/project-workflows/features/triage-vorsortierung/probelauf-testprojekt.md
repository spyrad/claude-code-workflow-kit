# Probelauf Testprojekt (Phase 4, Schritt 4.1/4.2)

**Datum:** 2026-10-16
**Skill-Fassung:** Repo-Fassung `skills/dtb-idea-triage/SKILL.md` (Branch `feature/triage-vorsortierung`, Stand nach `9004f2c`) — nicht die installierte Kopie (L74)
**Testprojekt:** Scratchpad, ausserhalb jedes Git-Repos (Worktree-Guard → `DURCHLASS-NOGIT`), erzeugt per `setup_tp.py` (Scratchpad dieser Session)

## Aufbau

- „Notiz-App": `src/notes.py` (`save_note`, `find_notes`, `delete_note`, `export_csv`, `backup`), `README.md`
- `INBOX.md`: #3 Offen (Export CSV + JSON), #2 Ausgearbeitet (Tags), #1 Verworfen (E-Mail)
- `lessons.md`: L1 „Pfade mit Leerzeichen in Shell-Befehlen immer quoten"
- `features/suche/spec.md` mit `## Offene Punkte` (eine offene `[Fach]`-Frage)
- `archive/ARCHIVE_LOG.md` (ein Eintrag), kein `archive/INBOX-BEFUNDE-verworfen.md` (Selbstanlage in 7b wird mitgetestet)
- Kein `skills/` im Testprojekt — die Quellen per Referenz loesen wie in einem Zielprojekt nach `~/.claude/skills/` auf; nur der Negativtest legt eine umgebaute `skills/dtb-lesson/SKILL.md` an („Repo zuerst")

> **Zaehl-Hinweis:** Der Plan nennt „8 konstruierte Funde"; seine Aufzaehlung der Wege braucht aber 11 (Buendel = 2 Glieder, Lektion = neu + Dublette, Fachfrage = mit + ohne Feature). Gebaut sind 11 Funde fuer **8 Wege** — das Deliverable „8/8 Wege" bleibt der Massstab.

## Erwartungstabelle

| # | Fund (Kurz) | Weg | Erwarteter Vorschlag | Erwartete Einordnung | Erwartetes Ziel |
|---|-------------|-----|----------------------|----------------------|-----------------|
| 4 | `delete_note` fragt nicht nach | 1 Befoerdern | Befoerdern | Sammelliste | `INBOX.md` #4, `(befoerdert 2026-10-16)` |
| 5 | `backup()` ueberschreibt vorige Sicherung | 2 Buendel | Befoerdern, verwandt #6 | Buendel-Glied | Archiv „gebuendelt in #6" |
| 6 | `backup()` legt Zielordner nicht an | 2 Buendel | Befoerdern, verwandt #5 | Buendel-Traeger (juengstes Glied) | `INBOX.md` #6, `(enthaelt #5)` |
| 7 | `save_note` ohne Encoding | 3 Verwerfen sicher | Verwerfen: erledigt, hoch, Beleg `src/notes.py:10` | Sammelliste | Archiv mit `{Grund} — Beleg: {Beleg}` |
| 8 | `import_old_format()` entfernen | 4 Verwerfen unsicher | Verwerfen (Funktion fehlt im Code, README behauptet Import) mit Sicherheit < hoch — oder Unklar | Einzelfall (Stufe 2) | Entscheidung des Menschen |
| 9 | JSON-Export mit Tags | 5 Nachtrag | Nachtrag #3 | Sammelliste | `INBOX.md` #3 Textfeld + Archiv „nachgetragen in #3" |
| 10 | mtime auf FAT32 | 6 Lektion | Lektion | Sammelliste | `lessons.md` L2 + Archiv „als Lektion L2 erfasst" |
| 11 | Pfade mit Leerzeichen quoten | 6 Lektion (Dublette) | Lektion → 4c: `Verwerfen: Lektion L1 deckt ab` (oder direkt Verwerfen mit Beleg `lessons.md`) | Sammelliste | Archiv mit Beleg L1 |
| 12 | Suche: archivierte Notizen? | 7 Fachfrage mit Feature | Fachfrage suche | Sammelliste | `features/suche/spec.md` `## Offene Punkte` + Archiv |
| 13 | Aufbewahrungsfrist | 7 Fachfrage ohne Feature | Fachfrage — | Sammelliste | `INBOX.md` #13 mit Vorsatz `Fachfrage: ` |
| 14 | „Das Ding mit dem Sync" | 8 Unklar | Unklar: {Frage} | Einzelfall (Stufe 2) | im Test: Liegenlassen → `L1 2026-10-16` |

**Erwartete Endlage nach dem Wirklauf:** im Becken nur #14 (`L1 2026-10-16`) und ggf. #8, falls dort ebenfalls liegengelassen; Kappung greift nicht (2 Einzelfaelle ≤ `einzeln_pro_lauf` 5).

## Protokoll Wirklauf (Schritt 4.2)

### Hauptlauf `tp1` (11 Funde → 1 Agent, Typ `Explore`)

- Worktree-Guard: `DURCHLASS-NOGIT` (still) · Lesestand-Referenz beim Einlesen gemerkt, vor JEDEM Becken-Schreiben geprueft (11×: „unveraendert"), nach jedem eigenen Schreiben nachgefuehrt (L46)
- 3c-Gates: Zeilenzahl 11/11, jede Zeile 6 Spalten, alle Vorschlaege bekannt → kein Ausfall
- 4a Struktur-Check: 7/7 Anker, aufgeloest nach `~/.claude/skills/` (kein `skills/` im Testprojekt — Zielprojekt-Fall)
- 4b Buendel: Kanten #4~#13 und #5~#6 → **kein Buendel** (je Gruppe nur ein `Befoerdern`) — siehe Abweichung A1
- 4c: #10 gegen `lessons.md` (mtime/FAT32/Hash) → kein Treffer, bleibt Lektion
- 4d: Einzelfaelle #6, #8 (Verwerfen `mittel`), #14 (Unklar) · 4e: keine Kappung (3 ≤ 5)
- Sammelliste mit „Alle uebernehmen" bestaetigt (Mensch, AskUserQuestion)

| # | erwartet | tatsaechlich (Voranalyse → Weg) | Datei-Beleg im Testprojekt |
|---|----------|----------------------------------|----------------------------|
| 4 | Befoerdern, Sammelliste | Befoerdern hoch → Sammelliste → 7a | `INBOX.md` Zeile `\| 4 \| … (befoerdert 2026-10-16) \| Offen \|` |
| 5 | Buendel-Glied | Befoerdern hoch, verwandt #6 → **fehlte in der gezeigten Sammelliste** (A2) → Stufe 2 → Mensch: Befoerdern | `INBOX.md` `\| 5 \| … \| Offen \|` |
| 6 | Buendel-Traeger | **Verwerfen: ueberholt, mittel** — `shutil.copytree` legt fehlende Ordner selbst an (A1) → Stufe 2 → Mensch: Verwerfen | Archiv `\| 6 \| … \| Verwerfen: ueberholt — … — Beleg: src/notes.py:41; …` |
| 7 | Verwerfen sicher, Sammelliste | Verwerfen: erledigt, hoch, `src/notes.py:10` → Sammelliste → 7b | Archiv neu angelegt (Kopf aus 7b), Begruendung `{Grund} — Beleg: src/notes.py:10` |
| 8 | Verwerfen unsicher → Einzelfall | Verwerfen: erledigt, mittel → Stufe 2 → Mensch: Verwerfen | Archiv `\| 8 \| …` |
| 9 | Nachtrag #3 | Nachtrag #3, hoch → Sammelliste → 7e (Ziel `Offen` geprueft) | `INBOX.md` #3: `**Nachtrag 2026-10-16 aus Befund #9:** …`, Status `Offen`; Archiv „nachgetragen in #3" |
| 10 | Lektion | Lektion, hoch → Sammelliste → 7f | `lessons.md` L2, `Context` endet auf `(via Triage 2026-10-16, Befund #10)`; Archiv „als Lektion L2 erfasst" |
| 11 | Lektion-Dublette | **Verwerfen: erledigt, hoch, Beleg `lessons.md:10`** (Agent erkannte L1 direkt; 4c nicht beruehrt) → Sammelliste → 7b | Archiv `\| 11 \| … — Beleg: dtb-project/project-rules/lessons.md:10` |
| 12 | Fachfrage suche | Fachfrage suche, hoch → Sammelliste → 7g | `features/suche/spec.md` `## Offene Punkte`: `- [ ] [Fach] Sollen archivierte Notizen in den Suchtreffern erscheinen?` (nach der letzten Inhaltszeile, Statusfeld unveraendert); Archiv „als Fachfrage in features/suche/spec.md erfasst" |
| 13 | Fachfrage — | Fachfrage —, hoch → Sammelliste → 7g Rueckfall → 7a | `INBOX.md` `\| 13 \| … \| Fachfrage: **Fachfrage: …** … (befoerdert 2026-10-16) \| Offen \|` (A3) |
| 14 | Unklar → Liegenlassen | Unklar mit Frage („Welche Sync-Funktion …?"), hoch → Stufe 2 → Mensch: Liegenlassen | Becken `\| 14 \| … \| L1 2026-10-16 \|` |

**Endlage:** Becken 1 Zeile (#14, `L1 2026-10-16`) — `grep -c "^| [0-9]" INBOX-BEFUNDE.md` = **1** = 1 liegengelassen + 0 zurueckgestellt. INBOX 6 Zeilen, Archiv 7, `lessons.md` 2 — Spaltenzahl aller vier Dateien gegen den Kopf geprueft: OK.

Bilanz laut Skill: Befoerdert 3 (davon 1 als „Fachfrage:") · Nachgetragen 1 · Lektionen 1 · Fachfragen 1 · Verworfen 4 · Liegengelassen 1 · verbleibend 1 ungesichtet.

### Ergaenzungslauf `tp-buendel` (Weg 2, 2 Funde → inline)

Noetig wegen A1. Zwei echt verwandte Funde: #5 (Zeitstempel-Ordner) + #15 (Aufbewahrungsregel fuer die dann wachsenden Sicherungen). Voranalyse inline (< 5, keine Agenten): beide `Befoerdern hoch`, gegenseitig verwandt → Buendel B1, Traeger #15 (hoechste Nummer). Mensch: „Alle uebernehmen".

- 7d.1: `INBOX.md` `\| 15 \| … (befoerdert 2026-10-16) (enthaelt #5) \| Offen \|`
- 7d.2: Archiv `\| 5 \| … \| gebuendelt in #15 \|`, danach Becken-Zeile #5 entfernt
- 7d.3: Becken-Zeile #15 entfernt → Becken leer; keine Nummer neu vergeben, keine doppelte Nummer in `INBOX.md`

### Zusatztests

| Test | Aufbau | Ergebnis |
|------|--------|----------|
| Abbruch | `tp-abbruch` = Ausgangslage `tp1`; Sammelliste (8 Zeilen, #5 diesmal korrekt enthalten) bestaetigt; nach Zeile 3 abgebrochen | ✅ geschrieben: `INBOX.md` #4, #5; Archiv #7. Becken: 8 Zeilen (#14 13 12 11 10 9 8 6). `lessons.md` und `features/suche/spec.md` unveraendert. Abbruch-Zeile: `Abgebrochen nach Eintrag 3 von 8 — die 3 getroffenen Entscheidungen sind geschrieben.` |
| Becken leer | `tp-leer` (0 Funde) | ✅ Schritt 2 → `Nichts zu sichten — 0 Eintrag(e) im Becken, davon 0 neu und 0 faellig.` — keine Agenten |
| Unter 5 | `tp-drei` (#4, #7, #9) | ✅ 3a-Weiche → inline, keine Agenten; Ergebnis im selben Format: #4 Befoerdern (`src/notes.py:24-25`, hoch) · #7 Verwerfen: erledigt (`src/notes.py:10`, hoch) · #9 Nachtrag #3 (`INBOX.md:9`, hoch); Uebersicht `Becken-Triage: 3 Fund(e) vorsortiert (3 inline, ohne Agenten)`, alle drei in der Sammelliste (Lauf dort beendet — die Schreibwege belegt der Hauptlauf) |
| Negativ Struktur-Check | `tp-drift` = `tp1` + `skills/dtb-lesson/SKILL.md` mit `## Schritt 4: Speichern (umgebaut)` | ✅ Aufloesung „Repo zuerst" greift die Kopie; Anker 1/2 gefunden, Anker 3 = 0 → `⚠ Struktur-Check fehlgeschlagen: skills/dtb-lesson/SKILL.md — Anker "## Schritt 4: Append-only speichern" nicht gefunden.` Folge nach 4a/4d: #10 (Lektion) wird Einzelfall, die Sammelliste traegt keine Lektions-Zeile, `lessons.md` bleibt unberuehrt. Voranalyse aus dem Hauptlauf wiederverwendet (identische Funde) |

### Abweichungen und Beobachtungen

- **A1 — Testdaten-Fehler, vom Agenten aufgedeckt:** #6 war als echter Defekt konstruiert, ist aber keiner (`shutil.copytree` ruft `os.makedirs(dst)`). Der Agent verwarf ihn mit nachpruefbarem Grund und nur `mittel` — genau der Fall, fuer den die Einzelvorlage existiert. Folge: kein Buendel im Hauptlauf → Ergaenzungslauf `tp-buendel`. Positiver Beleg fuer die Vorschlagsqualitaet, kein Skill-Defekt
- **A2 — Ausfuehrungsfehler beim Bau der Sammelliste (nicht im Skill-Text):** #5 (Befoerdern hoch) fehlte in der gezeigten Liste; die Uebersicht 4f zeigte `Sammelliste 7 · Einzelfaelle 3` bei 11 Funden. Behandelt als verschobene Zeile in Stufe 2 (nie still geschrieben, da nicht bestaetigt). **Verbesserungsvorschlag:** 4f eine Summenprobe geben (`Sammelliste + Buendel-Glieder + Einzelfaelle + Zurueckgestellt = N`, sonst ⚠ statt Vorlage) — die Zahlen standen schon da, nur der Vergleich fehlte
- **A3 — doppelter Vorsatz:** 7a setzt `Fachfrage: ` vor den Text, auch wenn der Befund schon mit „Fachfrage:" beginnt (`Fachfrage: **Fachfrage: …**`). Kosmetisch; Vorschlag: Vorsatz nur, wenn der Text nicht schon so beginnt
- **A4 — Sortierung der INBOX:** 7a fuegt direkt unter der Trennzeile ein; wird eine aeltere Nummer nach einer juengeren befoerdert (#5 nach #13), steht #5 oben — die absteigende Ordnung bricht. Folge der Regel „Nummer bleibt", kein Datenverlust
- **A5 — Weg 6 Dublette:** der Agent ordnete #11 direkt als `Verwerfen: erledigt` mit Beleg `lessons.md:10` ein, nicht als `Lektion` — die 4c-Umwandlung („Lektion L{N} deckt ab") wurde dadurch nicht beruehrt. Ergebnis gleichwertig (Archiv mit Beleg), der 4c-Pfad bleibt im Wirklauf unbelegt
