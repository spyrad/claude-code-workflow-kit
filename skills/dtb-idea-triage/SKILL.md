---
name: dtb:idea-triage
description: >-
  Use when: "Becken sichten", "Befunde triagieren", "idea triage",
  "Verlustfunde durchgehen", "was liegt im Becken". Sichtet die maschinell
  erfassten Verlustfunde in INBOX-BEFUNDE.md portionsweise und entscheidet je
  Eintrag: befoerdern nach INBOX.md, verwerfen ins Archiv, oder genau einmal
  liegenlassen. Schreibend — jede Entscheidung wird sofort festgeschrieben.
disable-model-invocation: true
argument-hint: "[optional: alle | anzahl]"
allowed-tools: Read, Write, Edit, Grep, Bash
pipeline:
  stage: idea
  after: [dtb:workflow-checkpoint]
  next: [dtb:idea-review]
  consumes: [INBOX-BEFUNDE.md, INBOX.md, workflow.config.yaml]
  produces: [INBOX-BEFUNDE.md, INBOX.md, archive/INBOX-BEFUNDE-verworfen.md]
---

# Befund-Becken sichten (Triage)

Du sichtest die maschinell erfassten Verlustfunde und entscheidest je Eintrag, ob er in die
Haupt-INBOX befoerdert, verworfen oder ein einziges Mal liegengelassen wird.

**Warum es dieses Becken gibt:** Die Verlustpruefung erfasst mehr Funde, als je abgearbeitet
werden. Landeten sie in `INBOX.md`, stuenden sie zwischen den Fach-Wuenschen und machten jede
Ideen-Sichtung unbenutzbar. Ein Becken-Eintrag wird deshalb **nie gearbeitet**, bevor er
befoerdert wurde — das ist die eigentliche Zulauf-Bremse, nicht die Datei-Trennung allein.

## Worktree-Guard

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions".

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(cd "$C" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar
- **Branch-Pruefung (optional, nur im `HAUPT-CHECKOUT`-Fall):** Ist `parallel.default_branch`
  in `workflow.config.yaml` gesetzt (nicht `null`) und `git branch --show-current` ungleich
  diesem Wert → Abbruch mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:idea-triage schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

Lies zusaetzlich den optionalen Block `idea_triage`:

```yaml
idea_triage:
  becken_schwelle: 10     # ab N ungesichteten Eintraegen meldet der Checkpoint (nur dort gelesen)
  altbestand_pro_lauf: 5  # wieviele Altbestands-Eintraege ein Lauf zusaetzlich sichtet
```

Fehlt der Block oder ein Schluessel → Defaults `becken_schwelle: 10`, `altbestand_pro_lauf: 5`.
Kein Hinweis, kein Abbruch.

---

## Schritt 1: Becken laden (Selbstanlage bei Fehlen)

Lies `{config.paths.workflows}/INBOX-BEFUNDE.md`.

**Fehlt die Datei → selbst anlegen**, mit dem Kopf unten, und danach mit „nichts zu sichten"
enden. Grund: `dtb:project-init` legt das Becken nur in NEUEN Projekten an; Seeds sind
„copied once, never drift-checked" und erreichen Bestandsprojekte nicht (INBOX #22). Der Skill
muss in einem Projekt laufen koennen, das `project-init` vor Monaten gesehen hat.

```markdown
# Befund-Becken (maschinelle Verlustfunde)

> Automatisch erfasste Funde aus der Verlustpruefung (`dtb:no-loss-check` /
> `dtb:workflow-checkpoint` Schritt 0). **Kein Eintrag hier wird gearbeitet** — er muss erst
> mit `/dtb:idea-triage` befoerdert werden. Fach-Wuensche gehoeren nach `INBOX.md`, nicht hierher.

**Sichtung-Spalte:** leer = neu, noch nie gesichtet · `L1 YYYY-MM-DD` = einmal liegengelassen,
der naechste Lauf erzwingt die Entscheidung · `Altbestand` = aus der Migration uebernommen.

**Nummernkreis:** gemeinsam mit `INBOX.md` — eine Nummer wird nie zweimal vergeben, und sie
bleibt bei der Befoerderung erhalten (Session-Logs referenzieren Nummern).

**Feld-Hygiene:** literale Pipes im Befund-Text escapen — sonst bricht die Zeile die Tabelle.

---

| # | Datum | Befund | Sichtung |
|---|-------|--------|----------|
```

Meldung bei Selbstanlage — genau eine Zeile, dann Ende:
```
Becken angelegt: {config.paths.workflows}/INBOX-BEFUNDE.md — noch keine Funde. Nichts zu sichten.
```

---

## Lesestand-Pruefung (Lese-Seite)

Parallele Sessions koennen das Becken zwischen Einlesen und Entscheidung veraendern — der
Checkpoint schreibt hier ebenfalls hinein (Orchestrator-Muster: `skills/CLAUDE.md` →
„Parallele Sessions"; dieser Skill ist lesend-entscheidend).

1. **Beim Einlesen merken:** mtime des Beckens festhalten — in EINEM selbstaendigen Bash-Block:
   ```bash
   ls -l --time-style=full-iso {pfad}/INBOX-BEFUNDE.md
   ```
2. **Unmittelbar vor JEDER Statusentscheidung** (jedem Schreiben in Schritt 4) dieselbe Abfrage
   erneut ausfuehren und vergleichen:
   - mtime unveraendert → still weiterarbeiten (kein Output)
   - mtime veraendert → Datei NEU lesen und den Inhalt vergleichen:
     - Inhalt tatsaechlich abweichend → genau eine Zeile
       `⚠ INBOX-BEFUNDE.md wurde seit dem Einlesen geaendert ({neue mtime}) — Stand neu geladen`
       und mit dem FRISCHEN Stand weiterarbeiten (kein Abbruch, keine Nachfrage)
     - Inhalt identisch (nur mtime, z.B. touch/Checkout) → keine Warnung
   - Datei existiert nicht mehr → wie Abweichung behandeln:
     `⚠ INBOX-BEFUNDE.md seit dem Einlesen entfernt/verschoben — Entscheidung ggf. hinfaellig`
3. **Bewusste Restluecke:** Das Fenster zwischen Pruefung und eigenem Schreiben bleibt
   (kein Locking) — Konvention: `skills/CLAUDE.md` → „Parallele Sessions".

---

## Schritt 2: Sichtungsmenge bestimmen

Ein Lauf sichtet NIE das ganze Becken. Andernfalls waechst die Sichtungsarbeit mit dem
Bestand, und genau dort bricht die Triage ab.

**Aufgenommen wird, in dieser Reihenfolge:**

1. **Neue** — Sichtung-Spalte leer (noch nie gesichtet), ALLE davon
2. **Faellige** — Sichtung-Spalte `L1 …` (einmal liegengelassen), ALLE davon;
   fuer sie gilt die Zwangsentscheidung (Schritt 4)
3. **Altbestand** — Sichtung-Spalte `Altbestand`, hoechstens `altbestand_pro_lauf` Stueck

**Innerhalb jeder Gruppe: aelteste zuerst** (aufsteigend nach Datum, bei gleichem Datum nach
Nummer). Der Kontext baut aufeinander auf, und der Altbestand schrumpft sichtbar.

**Argument `alle`** → die Kappung auf `altbestand_pro_lauf` entfaellt; alles Ungesichtete kommt
in den Lauf. **Argument als Zahl** → diese Zahl ersetzt `altbestand_pro_lauf`.

**Leere Sichtungsmenge** (Becken leer, oder alles gesichtet und nichts faellig) → genau eine
Zeile, Skill endet:
```
Nichts zu sichten — {N} Eintrag(e) im Becken, davon 0 neu und 0 faellig.
```

**Uebersicht vor dem Durchgang:**
```
Becken-Triage: {N} Eintrag(e) zu sichten

  Neu:        {N}
  Faellig:    {N}  (einmal liegengelassen, Entscheidung jetzt erzwungen)
  Altbestand: {N} von {M}  (Rest bleibt fuer spaetere Laeufe)

Einzeln durchgehen? (Ja / Abbrechen)
```

---

## Schritt 3: Alterungshinweis (optional, nie ein Urteil)

Maschinelle Befunde altern schnell: Sie beschreiben einen Zustand zu einem Zeitpunkt, und der
genannte Ort wird oft spaeter umgebaut. Der Hinweis macht das sichtbar — **er entscheidet nichts**.

Je Eintrag:
1. Ersten Datei-Pfad im Befund-Text suchen (Token, das wie ein repo-relativer Pfad aussieht,
   Backticks optional). **Kein Pfad erkennbar → Hinweis entfaellt ersatzlos.**
2. Existiert der Pfad nicht (mehr) → Hinweis entfaellt ersatzlos (nie raten, nie `--follow`-Ketten).
3. Aenderungsdatum der Datei ermitteln:
   ```bash
   git -C {root} log -1 --format=%ad --date=short -- {pfad}
   ```
   Schlaegt das Kommando fehl (kein Git-Repo, keine Historie) → Hinweis entfaellt ersatzlos.
4. Ist das Aenderungsdatum **juenger** als das Befund-Datum → genau eine Zeile ausgeben:
   ```
   ⓘ Moeglicherweise gegenstandslos: {pfad} zuletzt geaendert {datum} (nach dem Befund)
   ```

Der Hinweis ist bewusst schwach formuliert. Er sagt „koennte", nicht „ist" — die Datei kann aus
ganz anderen Gruenden angefasst worden sein.

---

## Schritt 4: Einzeln entscheiden

**Jede Entscheidung wird SOFORT geschrieben, nicht am Lauf-Ende gesammelt.** Bricht der Lauf
nach Eintrag 4 von 8 ab, sind vier Entscheidungen fest und vier stehen beim naechsten Lauf
wieder an. Ein Sammel-Schreiben am Ende verliert bei jedem Abbruch alles, was schon entschieden
war (INBOX #71) — deshalb ist die Reihenfolge hier verbindlich: entscheiden → schreiben →
naechster Eintrag.

Fuer jeden Eintrag der Sichtungsmenge:

```
Befund #{N} ({Datum}){, Sichtung: L1 {Datum} — Entscheidung jetzt erzwungen}
  "{Befund-Text, auf ~200 Zeichen gekuerzt}"

  {Alterungshinweis aus Schritt 3, falls vorhanden}

  Aktion?
    1. Befoerdern → INBOX.md
    2. Verwerfen  → archive/ (Begruendung noetig)
    3. Liegenlassen (nur einmal moeglich)
```

### Aktionen

**Befoerdern (1):** Ausfuehrung in Schritt 5.

**Verwerfen (2):**
- **Begruendung ist Pflicht** — ein Satz genuegt. Sie landet in der Archivdatei und ist in
  sechs Monaten das Einzige, was den Vorgang noch erklaert. Ohne Begruendung nicht schreiben,
  sondern einmal nachfragen.
- Ausfuehrung in Schritt 5.

**Liegenlassen (3):**
- **Nur zulaessig, wenn die Sichtung-Spalte leer ist.** Bei `L1 …` ist die Option nicht im
  Angebot — dort gilt die **Zwangsentscheidung**: nur 1 oder 2. Wird sie trotzdem gewaehlt:
  ```
  #{N} wurde bereits einmal liegengelassen ({L1-Datum}). Jetzt entscheiden: befoerdern oder verwerfen.
  ```
- Sonst: Sichtung-Spalte auf `L1 {heutiges Datum}` setzen, Zeile bleibt im Becken, weiter.
- Bei `Altbestand`: gilt wie leer — Liegenlassen setzt `L1 {heute}` und ersetzt damit den
  Altbestand-Vermerk (der Eintrag ist dann in der normalen Faelligkeits-Schiene).

---

## Schritt 5: Entscheidung ausfuehren (sofort schreiben)

### 5a: Befoerdern

> **Kopplungs-Hinweis:** Der Duplikat-Check unten fuehrt die Bewertung aus `dtb:idea` per
> Referenz aus und greppt auf deren Sektions-Titel `## Duplikat-Check` (Struktur-Check).
> Umbenennung oder Umbau dieser Sektion dort → hier mitziehen. Bewusst Referenz statt Kopie:
> eine zweite Bewertungsregel wuerde mit der ersten auseinanderlaufen.

1. **Duplikat-Check — unscharf, NUR gegen `INBOX.md`.** Nicht gegen das Becken: dort steht der
   Eintrag selbst, und ein Treffer gegen die eigene Herkunft waere immer positiv. Bewertung
   nach `## Duplikat-Check` in `dtb:idea`. Treffer → genau eine Rueckfrage:
   ```
   Aehnliche Idee steht schon in der INBOX (#{N}, {Status}): "{Bestandstext, gekuerzt}"
   Trotzdem befoerdern? (Ja / stattdessen verwerfen)
   ```
   Kein Treffer → keine Ausgabe, direkt weiter.
2. **Zeile aus dem Becken entfernen.**
3. **Zeile in `INBOX.md` einfuegen — direkt unter der Tabellen-Trennzeile**, nicht ans
   Tabellenende: die INBOX ist absteigend sortiert (setzt INBOX #74 um).
4. **Nummer bleibt.** Sie wird nicht neu vergeben — Session-Logs, Plaene und Archiv-Eintraege
   referenzieren sie.
5. **Status `Offen`**, Textfeld unveraendert plus Suffix `(befoerdert {YYYY-MM-DD})`.
6. **Spaltenzahl nach dem Schreiben pruefen** (Feld-Hygiene): die neue Zeile muss so viele
   Felder haben wie ihre Nachbarn. Bare Pipes im uebernommenen Text escapen.

Meldung: `✔ #{N} befoerdert → INBOX.md`

### 5b: Verwerfen

1. **Archivdatei sicherstellen:** `{config.paths.workflows}/archive/INBOX-BEFUNDE-verworfen.md`.
   Fehlt sie → mit diesem Kopf anlegen:
   ```markdown
   # Verworfene Befunde

   > Append-only. Aus dem Becken (`INBOX-BEFUNDE.md`) verworfene Funde mit Begruendung.
   > Nichts wird hier geloescht — die Datei ist der Suchraum, wenn ein Thema wiederkommt.

   | Verworfen am | # | Datum | Befund | Begruendung |
   |--------------|---|-------|--------|-------------|
   ```
2. **Anhaengen** (append-only, nie ueberschreiben): heutiges Datum, Nummer, Befund-Datum,
   Befund-Text, Begruendung.
3. **Zeile aus dem Becken entfernen.**

Meldung: `✔ #{N} verworfen → archive/INBOX-BEFUNDE-verworfen.md`

### 5c: Liegenlassen

Sichtung-Spalte auf `L1 {heutiges Datum}` setzen, sonst nichts aendern.

Meldung: `↷ #{N} liegengelassen — naechster Lauf erzwingt die Entscheidung`

---

## Schritt 6: Abschluss-Bilanz

Nach dem letzten Eintrag der Sichtungsmenge — oder nach einem Abbruch durch den Nutzer:

```
Becken-Triage abgeschlossen:

  Befoerdert:      {N}
  Verworfen:       {N}
  Liegengelassen:  {N}

Im Becken verbleibend: {N} ({M} davon Altbestand, noch nicht gesichtet)
```

**Genau eine Hinweiszeile, nur wenn befoerdert wurde:**
```
{N} Idee(n) sind jetzt in der Haupt-INBOX — sichten mit /dtb:idea-review
```

**Kein Automatismus, kein Kettenaufruf.** Der Skill startet `dtb:idea-review` nicht selbst; die
Entscheidung, ob jetzt sofort weitergearbeitet wird, gehoert dem Menschen.

Bei Abbruch mitten im Durchgang zusaetzlich eine Zeile:
```
Abgebrochen nach Eintrag {K} von {N} — die {K} getroffenen Entscheidungen sind geschrieben.
```

---

## Schreibmechanik INBOX-BEFUNDE.md

> **Kopplungs-Hinweis:** `dtb:workflow-checkpoint` fuehrt diesen Abschnitt fuer seine
> Verlustfunde per Referenz aus (Schritt 0, Sammelvorlage) und greppt zeilenverankert auf den
> Sektions-Titel `## Schreibmechanik INBOX-BEFUNDE.md` (Struktur-Check). Umbenennung oder Umbau
> dieses Abschnitts → `skills/dtb-workflow-checkpoint/SKILL.md` mitziehen.
>
> Dieser Abschnitt liegt hier und nicht in `dtb:idea`, weil `dtb:idea` ausschliesslich nach
> `INBOX.md` schreibt — sein Sektions-Titel ist dort korrekt und bleibt unangetastet. Wer die
> Datei besitzt, beschreibt, wie man in sie hineinschreibt.

### Datei
- Pfad: `{config.paths.workflows}/INBOX-BEFUNDE.md`
- Fehlt sie → mit dem Kopf aus Schritt 1 anlegen, dann schreiben (Seed-Skew, INBOX #22)

### Nummernvergabe (gemeinsamer Nummernkreis)

Die naechste Nummer ist das **Maximum ueber BEIDE Dateien plus eins** — `INBOX.md` UND
`INBOX-BEFUNDE.md`. Wird nur eine Datei gezaehlt, vergibt der jeweils andere Schreiber dieselbe
Nummer ein zweites Mal, und zwei verschiedene Vorgaenge tragen dieselbe ID.

Fehlt eine der beiden Dateien → nur die vorhandene zaehlen (fail-open, kein Abbruch).

Den Zaehl-Ausdruck vor der Vergabe gegen eine **Stichprobe der getroffenen Zeilen** pruefen,
nicht nur gegen die Zahl (L17) — eine einmal vergebene Nummer wird nicht mehr hinterfragt.

### Zeile schreiben
- Neue Zeile **direkt unter der Tabellen-Trennzeile** einfuegen (das Becken ist absteigend
  sortiert), nicht ans Tabellenende
- Felder: `| {Nr} | {heutiges Datum} | {Befund-Text} | |` — die Sichtung-Spalte bleibt **leer**
  (= neu, noch nie gesichtet)
- **Kein Herkunfts-Marker.** Ein `(via Checkpoint …)`-Suffix waere hier redundant: dass der Fund
  maschinell erfasst wurde, sagt bereits die Datei, in der er steht
- Literale Pipes im Befund-Text escapen; nach dem Schreiben die Spaltenzahl gegen die
  Nachbarzeilen pruefen
- Schreibfehler mitten in einer Serie → melden, was geschrieben ist, Rest als Befehle ausgeben —
  **nie zurueckrollen**

---

## Wichtig

- **Nie das ganze Becken sichten:** Die Portionierung (Schritt 2) ist der Grund, warum die
  Triage nicht abbricht. Ein Lauf, der 150 Eintraege vorlegt, wird nie zu Ende gefuehrt
- **Sofort schreiben, nie sammeln:** Jede Entscheidung geht einzeln in die Datei (INBOX #71)
- **Der Alterungshinweis entscheidet nichts** — er ist ein Indiz, kein Urteil, und entfaellt
  im Zweifel ersatzlos statt zu raten
- **Ein Becken-Eintrag wird nie gearbeitet:** kein Worker greift ihn, kein `feature-fast` laedt
  ihn, er steht in keiner Arbeits-Ansicht. Erst die Befoerderung macht ihn zum Vorgang
- **Deutsch:** Alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:workflow-checkpoint` — schreibt die Verlustfunde ins Becken (Vorgaenger)
- `/dtb:idea-review` — sichtet die Haupt-INBOX; Ziel der Befoerderung (Nachfolger)
- `/dtb:idea` — Erfassung durch den Menschen, schreibt immer nach `INBOX.md`

---

**Erstellt mit:** Kit-Feature `ideen-becken` (INBOX #76)
