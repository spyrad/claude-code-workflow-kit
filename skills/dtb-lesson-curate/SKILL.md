---
name: dtb:lesson-curate
description: >-
  Use when: "Lektionen kuratieren", "lessons aufraeumen", "Lektionen ausmustern",
  "lessons.md ist zu gross", "lesson curate". Checks every lesson in
  project-rules/lessons.md with read-only background agents for being outdated,
  duplicated or already lifted into a versioned rules file, lets the human confirm
  one pre-filled collection list with veto (unclear cases one by one), and moves
  each confirmed lesson with its reason to archive/lessons-ausgemustert.md instead
  of deleting it. Writing — every confirmed decision is written immediately.
disable-model-invocation: true
argument-hint: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
pipeline:
  stage: development
  after: [dtb:lesson]
  next: null
  consumes: [project-rules/lessons.md, archive/lessons-ausgemustert.md, workflow.config.yaml, project-rules/*.md, features/*/spec.md, features/*/plan.md]
  produces: [project-rules/lessons.md, archive/lessons-ausgemustert.md]
---

# Lektionen kuratieren

Du haeltst die Lektionen-Sammlung kompakt: Eine lesende Voranalyse prueft jede Lektion, ob sie
**ueberholt**, **doppelt** oder **schon gehoben** ist, und belegt jeden Vorschlag. Der Mensch
bestaetigt die sicheren Vorschlaege als EINE Sammelliste; unklare Faelle kommen einzeln. Jede
bestaetigte Lektion wandert mit Grund ins Archiv — geloescht wird nichts.

**Warum es diesen Skill gibt:** `lessons.md` wird von mehreren Skills bei jedem Lauf als Prior
geladen; jede Lektion kostet dort Tokens, auch wenn sie laengst ueberholt ist. Die Sammlung ist
append-only fuers **Schreiben** — die **Entnahme** laeuft ausschliesslich ueber diesen Skill, mit
Bestaetigung und Archiv-Eintrag. Damit bleibt jede Lektion auffindbar und ihre Nummer vergeben.

**Grundhaltung: im Zweifel behalten.** Eine zu Unrecht behaltene Lektion kostet ein paar hundert
Tokens; eine zu Unrecht ausgemusterte laesst einen schon gemachten Fehler wiederholen.

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
  ⛔ dtb:lesson-curate schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Der Skill nimmt keinen Text entgegen — die Meldung nennt nur den Befehl
  `/dtb:lesson-curate` zum Absetzen im Haupt-Checkout.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfade `dtb-project/project-workflows/` (`{wf}`) und
`dtb-project/project-rules/` (`{rules}`).

Lies zusaetzlich den optionalen Block `lessons`:

```yaml
lessons:
  schwelle_kb: 40         # ab dieser Groesse von lessons.md warnt dtb:lesson und nennt diesen Skill
  einzeln_pro_lauf: 5     # wieviele Einzelfaelle ein Lauf hoechstens vorlegt
```

Fehlt ein Schluessel oder der ganze Block → Default (`40` bzw. `5`). Kein Hinweis, kein Abbruch.

---

## Schritt 1: Bestand laden

### 1a: Messen und Selbstheilung erkennen

Ein selbstaendiger Bash-Block (Platzhalter `{rules}`/`{wf}` vorher einsetzen):

```bash
L="{rules}/lessons.md"; A="{wf}/archive/lessons-ausgemustert.md"
[ -f "$L" ] || { echo FEHLT; exit 0; }
[ -f "$A" ] || A=/dev/null
echo "BYTES $(wc -c < "$L" | tr -d ' ')"
echo "ZEILEN $(wc -l < "$L" | tr -d ' ')"
awk -F'|' 'FNR==1{f++}
  f==1 && /^\| *[0-9]+ *\|/ {n=$2; gsub(/ /,"",n); l[n]=1; c++}
  f==2 && /^\| *[0-9][0-9-]* *\| *[0-9]+ *\|/ {n=$3; gsub(/ /,"",n); if (n in l) print "DOPPELT " n}
  END{print "LEKTIONEN " c+0}' "$L" "$A"
```

- `FEHLT` oder `LEKTIONEN 0` → genau eine Zeile, Ende:
  `Nichts zu kuratieren — {rules}/lessons.md fehlt oder hat keine Lektionen.`
- **Groesse:** KB = Bytes/1024, abgerundet.
  > **Kopplungs-Hinweis (KB-Definition):** dieselbe Rechenregel steht in `dtb:lesson`
  > (Schritt 4, Groessen-Warnung) und `dtb:project-dashboard` (Kennzahl Lektionen). Aenderung
  > hier → beide mitziehen; Verifikation: Grep `Bytes/1024` ueber `skills/` = 3 Skills.
- **Messung ausgefallen** (keine `BYTES`-Zeile oder leerer Wert) → Werkzeug-Fehlschlag, kein
  Befund: Groesse in der Uebersicht als `—`, eine Zeile `⚠ Groesse nicht messbar — Lauf geht weiter`
- **Unter `schwelle_kb`** → der Lauf geht trotzdem weiter (bewusst gestartet), eine Zeile:
  `→ lessons.md: {KB} KB (Schwelle {schwelle_kb} KB) — Kuratierung laeuft trotzdem`
- **`DOPPELT {N}`-Zeilen** = Lektion steht in `lessons.md` UND im Archiv (ein frueherer Lauf
  brach zwischen Archiv-Eintrag und Entnahme ab). Diese Nummern **nicht** analysieren — sie
  werden in Schritt 6 (Selbstheilung) nachgezogen. Eine Zeile je Nummer:
  `↻ L{N} steht noch in lessons.md, ist aber schon archiviert — Entnahme wird nachgeholt`

### 1b: Lektionen einlesen

Lies `{rules}/lessons.md` vollstaendig.

- **Datenzeile** = Zeile, die mit `| {Zahl} |` beginnt (unter der `|---|`-Trennzeile). Jede
  andere Zeile (Kopf, Kommentar, kaputtes Format) wird **nie angefasst**
- Lektionen werden **nach Nummer** gefuehrt, nie nach Position — die Datei ist nicht monoton
  sortiert und hat Nummernluecken
- Die in 1a als `DOPPELT` gemeldeten Nummern aus der Analysemenge nehmen

---

## Schritt 2: Voranalyse

Je Lektion entsteht ein **Urteil mit Beleg** — gelesen, nie geschrieben. Die Voranalyse
entscheidet nichts: was mit einer Lektion passiert, bestaetigt der Mensch.

### 2a: Weiche — inline oder Hintergrund-Agenten

- **Weniger als 5 Lektionen** in der Analysemenge → keine Agenten; du fuehrst den Auftrag unten
  selbst im Hauptkontext aus (gleiches Ergebnis-Format)
- **Sonst** → Analysemenge nach Nummer in **Portionen zu hoechstens 15 Lektionen** teilen, je
  Portion **ein** Agent, alle parallel starten und auf alle Ergebnisse warten
- **Agenten-Typ:** `Explore` — er hat werkzeugseitig kein Edit/Write. Ist `Explore` nicht
  verfuegbar → `general-purpose` mit demselben Auftrag und genau eine Zeile:
  ```
  ⚠ Agenten-Typ Explore nicht verfuegbar — Voranalyse mit general-purpose, Schreibverbot nur im Auftrag
  ```

### 2b: Auftrag (je Portion)

Platzhalter fuellen: `{root}` = absoluter Projekt-Root, `{rules}` = `{config.paths.rules}`,
`{nummern}` = die Nummern der Portion, kommagetrennt (`1, 2, 3, …`), `{hebeziele}` = die
vorhandenen Dateien aus: `{root}/skills/CLAUDE.md` und `{rules}/*.md` ohne `lessons.md` und
`DERIVED_STATE_RULES.md` (Glob; keine vorhanden → `—`).

**Nur Nummern, nie Zeilen in den Auftrag:** Der Agent liest `lessons.md` selbst. So sieht er alle
Lektionen im vollen Wortlaut (genauere Dubletten-Pruefung), und der Auftrag bleibt klein — die
Zeilen einzusetzen kostete mehr Text als die ganze Datei (Probe 2026-10-28: ~115 KB Auftraege
gegen 55 KB Bestand). Falsch gelesene Zeilen faengt das Nummern-Gate in 2c.

```
Du pruefst Lektionen aus einer Lektionen-Sammlung gegen den aktuellen Projektstand und schlaegst
je Lektion ein Urteil vor. NUR LESEN: keine Datei anlegen, aendern oder loeschen, keine Kommandos
mit Schreibwirkung. Du entscheidest nichts — du lieferst Urteile mit Beleg.

Projekt-Root: {root}

Lektionen-Sammlung: {rules}/lessons.md — lies sie vollstaendig. Datenzeilen beginnen mit
`| {Zahl} |`, Spalten: # | Datum | Context | Problem | Rule | Applies-to.

Deine Lektionen (nur diese Nummern beurteilen; alle anderen sind Vergleichsmaterial fuer Dubletten):
{nummern}

Versionierte Regel-Dateien (Hebe-Ziele):
{hebeziele}

Urteil — genau eines je Lektion:
- behalten       — die Lektion traegt noch und steht nirgends sonst
- ueberholt      — die beschriebene Mechanik gibt es nicht mehr, oder ein Skill/der Code erzwingt
                   die Regel inzwischen selbst, sodass niemand den Fehler mehr machen kann
- doppelt L{M}   — Lektion L{M} aus der Sammlung ersetzt diese ohne Informationsverlust
- gehoben        — eine Hebe-Ziel-Datei traegt die Regel bereits

Ersetzungsprobe (gilt fuer doppelt UND gehoben): gleicher Gegenstand UND gleiche Aussage — die
bleibende Lektion bzw. die Fundstelle traegt die Aussage dieser Lektion vollstaendig. Derselbe
Gegenstand mit anderer oder schmalerer Aussage reicht NICHT → behalten. Bringt diese Lektion
mehr mit als L{M}, ist sie nicht doppelt.

Beleg: wo du es gesehen hast, als Datei:Zeile. Fuer doppelt: L{M}. Fuer ueberholt durch
Abwesenheit: Begriff + Suchraum ohne Treffer ("`X` 0 Treffer in skills/") PLUS die Stelle der
Nachfolge-Mechanik (Datei:Zeile) — ohne Nachfolge-Stelle hoechstens Sicherheit mittel.
Fuer behalten: "—".

Sicherheit: hoch | mittel | niedrig. Im Zweifel niedriger einstufen.

Ausgabe: GENAU eine Zeile je Lektion, keine Kopfzeile, keine Prosa davor oder danach, Format:
L{N} | {Urteil} | {Grund, 1 Satz} | {Beleg} | {Sicherheit}
Literale Pipes in Grund oder Beleg immer als \| angeben.
```

### 2c: Ergebnis pruefen (Werkzeug-Fehlschlag ist kein Datenbefund)

Je Portion, bevor irgendetwas weiterverarbeitet wird:

1. **Nummern-Gate:** Die Nummern der Ergebniszeilen (Zeilen, die mit `L` und einer Ziffer
   beginnen) muessen **genau** die Nummern der Portion sein: jede genau einmal, keine fremde.
   Fehlt eine, steht eine doppelt oder stammt eine aus einer anderen Portion, liefert der Agent
   nichts, oder ist das Format unlesbar → **alle Lektionen dieser Portion gelten als
   `nicht geprueft`**. Nie als „alles behalten, nichts gefunden" werten — ein leeres Ergebnis ist
   ein Ausfall, kein Befund
2. **Spaltenpruefung je Zeile:** genau **5 Spalten** — also genau 4 Trenner `|`, escapte `\|`
   zaehlen nicht. Weicht eine Zeile ab → nur diese Lektion gilt als `nicht geprueft`
3. **Bekanntes Urteil:** Spalte 2 muss `behalten`, `ueberholt`, `doppelt L{M}` (mit `L{M}` aus
   der Analysemenge, nicht die eigene Nummer) oder `gehoben` sein; sonst `nicht geprueft`

`nicht geprueft` heisst **behalten** — die Lektion erscheint nur als Zahl in der Bilanz, nie als
Vorschlag. Faellt eine ganze Portion aus, genau eine Zeile:
```
⚠ Voranalyse fuer {K} Lektion(en) ausgefallen (L{a}–L{b}) — sie bleiben ungeprueft im Bestand
```
**Fallen alle Portionen aus** → Abbruch ohne Schreiben, genau eine Zeile:
```
Nichts geschrieben — Voranalyse vollstaendig ausgefallen, Bestand unveraendert.
```

---

## Wichtig

- **Nie loeschen ohne Archiv:** Jede Entnahme aus `lessons.md` setzt einen Archiv-Eintrag voraus
- **Nummern bleiben vergeben:** Eine ausgemusterte Nummer wird nie neu vergeben (`dtb:lesson`
  zaehlt das Archiv mit)
- **Kein Umformulieren, kein Zusammenfuehren, kein Heben:** nur ganz ausmustern oder behalten
- **Prior-Leser lesen das Archiv nicht** — ausgemusterte Lektionen wirken nicht mehr

## Verwandte Skills

- `/dtb:lesson` — Lektion erfassen (warnt ab `lessons.schwelle_kb` und nennt diesen Skill)
- `/dtb:idea-triage` — Vorbild: Vorsortierung des Befund-Beckens mit Sammelliste
