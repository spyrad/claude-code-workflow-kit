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
  consumes: [project-rules/lessons.md, archive/lessons-ausgemustert.md, workflow.config.yaml, skills/CLAUDE.md, project-rules/*.md, features/*/spec.md, features/*/plan.md]
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
  schwelle_kb: 80         # ab dieser Groesse von lessons.md warnt dtb:lesson und nennt diesen Skill
  einzeln_pro_lauf: 5     # wieviele Einzelfaelle ein Lauf hoechstens vorlegt
```

Fehlt ein Schluessel oder der ganze Block → Default (`80` bzw. `5`). Kein Hinweis, kein Abbruch.

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
  f==1 && /^\| *[0-9]+ *\|/ {n=$2; gsub(/ /,"",n); if (n in l) print "MEHRFACH " n; l[n]=1; c++}
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
  gehen in die Selbstheilung (1c), die auch die Meldezeile je Nummer ausgibt
- **`MEHRFACH {N}`-Zeilen** = dieselbe Nummer steht mehrmals in `lessons.md` (z.B. nach einem
  Merge zweier Klone). Diese Nummer **nicht** analysieren und **nicht** heilen (auch wenn sie
  zugleich `DOPPELT` ist) — unklar, welche Zeile gemeint ist. Je Nummer genau eine Zeile:
  `⚠ L{N} steht mehrfach in lessons.md — Nummer doppelt vergeben? Von Hand klaeren`. Alle Zeilen
  dieser Nummern zaehlen in der Mengenprobe (3f) als Topf **mehrfach**

### 1b: Lektionen einlesen

Lies `{rules}/lessons.md` vollstaendig.

- **Datenzeile** = Zeile, die mit `| {Zahl} |` beginnt (unter der `|---|`-Trennzeile). Jede
  andere Zeile (Kopf, Kommentar, kaputtes Format) wird **nie angefasst**
- Lektionen werden **nach Nummer** gefuehrt, nie nach Position — die Datei ist nicht monoton
  sortiert und hat Nummernluecken
- Die in 1a als `DOPPELT` oder `MEHRFACH` gemeldeten Nummern aus der Analysemenge nehmen

### 1c: Selbstheilung (vor der Analyse)

Nur bei `DOPPELT`-Zeilen aus 1a, ohne die `MEHRFACH`-Nummern. Ein frueherer Lauf hat die Lektion schon archiviert, die Entnahme
aber nicht mehr geschafft (Ziel vor Quelle, Schritt 6). Je Nummer ein selbstaendiger Bash-Block
(Platzhalter vorher einsetzen):

```bash
L="{rules}/lessons.md"; A="{wf}/archive/lessons-ausgemustert.md"; n={N}
z=$(grep -E "^\| *$n *\|" "$L" | tr -d '\r')
[ "$(printf '%s\n' "$z" | grep -c .)" = 1 ] || { echo MEHRDEUTIG; exit 0; }
tr -d '\r' < "$A" | grep -E "^\| *[0-9-]+ *\| *$n *\|" | grep -qF -- "$z" && echo GLEICH || echo VERSCHIEDEN
```

- `GLEICH` (die Archivzeile enthaelt die Lektionszeile woertlich) → **nur die Entnahme** nachholen
  nach 6b Punkt 3 — kein zweiter Archiv-Eintrag. Exakter Vergleich, darum ohne Rueckfrage. Zeile:
  `↻ L{N} war schon archiviert — Entnahme aus lessons.md nachgeholt`
- `VERSCHIEDEN` oder `MEHRDEUTIG` → nichts schreiben, die Lektion bleibt und wird in diesem Lauf
  nicht analysiert. Zeile:
  `⚠ L{N} steht in lessons.md und im Archiv mit verschiedenem Inhalt — Nummer doppelt vergeben? Von Hand klaeren`

Alle `DOPPELT`-Nummern (ohne `MEHRFACH`) zaehlen in der Mengenprobe (3f) als Topf
**Selbstheilung** — geheilt oder nicht.

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
`{portion}` = die Nummern der Portion, kommagetrennt (`1, 2, 3, …`), `{hebeziele}` = die
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
{portion}

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
   zaehlen nicht. Weicht eine Zeile ab → nur diese Lektion gilt als `nicht geprueft`.
   Mechanisch: escapte Pipes zuerst per Klammer-Ausdruck entfernen, dann zaehlen —
   `sed 's/[\][|]//g' | awk -F'|' '{print NF}'` = 5. Nie `sed 's/\|//g'`: in GNU-sed ist `\|`
   eine Alternation, Zeilen mit `\|\|` zerfallen falsch (Probe 2026-10-28)
3. **Bekanntes Urteil:** Spalte 2 muss `behalten`, `ueberholt`, `doppelt L{M}` (mit `L{M}` aus
   der Analysemenge, nicht die eigene Nummer) oder `gehoben` sein; sonst `nicht geprueft`

`nicht geprueft` heisst **behalten** — die Lektion erscheint nur als Zahl in der Bilanz, nie als
Vorschlag. Faellt eine ganze Portion aus, genau eine Zeile:
```
⚠ Voranalyse fuer {K} Lektion(en) ausgefallen (L{a}–L{b}) — sie bleiben ungeprueft im Bestand
```
**Fallen alle Portionen aus** → Abbruch ohne Ausmusterung, genau eine Zeile:
```
Nichts ausgemustert — Voranalyse vollstaendig ausgefallen{, Selbstheilung: {H} nachgeholt}.
```

---

## Schritt 3: Konsolidieren

Aus den geprueften Ergebniszeilen entstehen mechanisch die Toepfe — hier wird nichts neu
bewertet. Jede Lektion des Bestands landet in genau einem Topf.

### 3a: Einordnen

| Ergebnis | Topf |
|----------|------|
| `behalten` (jede Sicherheit) | **behalten** — nur als Zahl |
| jedes andere Urteil mit Sicherheit `niedrig` | **behalten** — nur als Zahl (im Zweifel behalten) |
| `nicht geprueft` (2c) | **nicht geprueft** — nur als Zahl, gilt als behalten |
| `ueberholt` / `doppelt L{M}` / `gehoben` mit `hoch` oder `mittel` | **Vorschlag** → 3b, 3c |
| `DOPPELT` aus 1a | **Selbstheilung** (1c) |
| `MEHRFACH` aus 1a (alle Zeilen der Nummer) | **mehrfach** — nur als Zahl, bleibt unveraendert |

`behalten` wird nie vorgelegt.

### 3b: Ketten-Sperre (`doppelt`)

Die bleibende Lektion L{M} eines Vorschlags `doppelt L{M}` ist fuer diesen Lauf **gesperrt**:
sie wird nicht ausgemustert, solange eine andere Lektion auf sie verweist. Sonst koennten zwei
Lektionen, die sich gegenseitig ersetzen, gemeinsam verschwinden — und mit ihnen die Aussage.

- **Kette:** L{M} ist selbst Vorschlag (jedes Urteil) → **beide** werden Einzelfall
- **Kreis:** L{N} `doppelt L{M}` und L{M} `doppelt L{N}` → beide Einzelfall (Sonderfall der Kette)
- Ketten- und Kreis-Partner bilden ein **Paar**: gemeinsam vorgelegt, gemeinsam gekappt (3d),
  dort zaehlen sie als 2
- **Sperre waehrend des Laufs:** Wird eine Lektion als `doppelt zu L{M}` ausgemustert (Sammelliste
  oder Einzelfall), ist L{M} ab dann gesperrt. Ein noch offener Einzelfall zu L{M} entfaellt —
  keine Frage, genau eine Zeile, zaehlt als behalten:
  `→ L{M} bleibt (gesperrt: L{N} wurde mit Verweis auf sie ausgemustert)`
- **Partner ausgemustert (jede Richtung):** Wird ein Paar-Partner ausgemustert — mit welchem
  Urteil auch immer —, entfaellt der noch offene Einzelfall des anderen ebenso: keine Frage, genau
  eine Zeile, zaehlt als behalten, der naechste Lauf prueft ihn neu. Sonst stuetzte sich ein
  `doppelt zu L{M}` auf eine Lektion, die schon im Archiv steht, und „Die andere ausmustern"
  griffe ins Leere: `→ L{N} bleibt (Paar-Partner L{M} ausgemustert — naechster Lauf prueft neu)`

### 3c: Sammelliste oder Einzelfall (mechanisch)

**Sammelliste** (Schritt 4) — alle drei Bedingungen:
- Sicherheit `hoch`
- Beleg mit pruefbarem Ort: `Datei:Zeile`, bei `doppelt` die Nummer `L{M}`
- weder Teil einer Kette noch eines Kreises (3b) — das gilt auch fuer die bleibende Lektion L{M},
  wenn sie selbst Vorschlag ist (jedes Urteil, z.B. `ueberholt`)

**Einzelfall** (Schritt 5) — jeder andere Vorschlag: Sicherheit `mittel`; `hoch` ohne Ort im
Beleg (ein plausibler Beleg ohne Ort rutschte bei „Alle uebernehmen" ungeprueft durch); Ketten
und Kreise. `nicht geprueft` ist **kein** Einzelfall — ohne Urteil gibt es nichts zu entscheiden.

### 3d: Kappung der Einzelfaelle

Hoechstens `einzeln_pro_lauf` Einzelfaelle, **aelteste zuerst** (Spalte `Datum`, bei Gleichstand
die kleinere Nummer). Ein Paar (3b) wird nur ganz vorgelegt oder ganz zurueckgestellt — passt es
nicht mehr hinein, rueckt die naechste Lektion nach. Die uebrigen bleiben unveraendert in
`lessons.md` und werden im naechsten Lauf neu geprueft (Lektionen tragen keinen Sichtungsvermerk).

**Nicht gekappt** wird, was der Mensch selbst aus der Sammelliste herausnimmt (Schritt 4) — wer
streicht, hat sich die Einzelentscheidung bewusst geholt.

### 3e: Hinweis auf offene Changes (nicht blockierend)

Eine Lektion, auf die ein laufender Change verweist, kann trotzdem ueberholt sein — der Hinweis
hilft nur beim Gegenlesen. Ein selbstaendiger Bash-Block ueber alle Vorschlags-Nummern
(`{vorschlaege}` = Nummern aller Vorschlaege, leerzeichengetrennt einsetzen, z.B. `1 4 84`):

```bash
W="{wf}/features"; [ -d "$W" ] || exit 0
for n in {vorschlaege}; do
  grep -lwE "L$n" "$W"/*/spec.md "$W"/*/plan.md 2>/dev/null | sed "s|^$W/|L$n |"
done
```

Je Treffer traegt die Zeile in der Vorlage `ⓘ in features/{slug}/{datei}`. `archive/` liegt
ausserhalb von `features/` und zaehlt nicht.

### 3f: Uebersicht vor der Vorlage

Erwartete Einsparung = Bytes der vorgeschlagenen Zeilen (Sammelliste + vorgelegte Einzelfaelle),
ein selbstaendiger Bash-Block (`{vorgelegt}` = deren Nummern, leerzeichengetrennt wie in 3e):

```bash
L="{rules}/lessons.md"
for n in {vorgelegt}; do grep -E "^\| *$n *\|" "$L"; done | wc -c
```

Ausgabe `0` bei `{S} + {E}` > 0 ist ein Werkzeug-Fehlschlag (z.B. falsch eingesetzte Nummern),
kein Befund: `{X}` = `—` und genau eine Zeile `⚠ Einsparung nicht messbar — Vorlage geht weiter`.

```
Lektionen kuratieren — Bestand {N} Lektionen, {Z} Zeilen, {KB} KB (Schwelle {schwelle_kb} KB)

Voranalyse: {G} geprueft · {U} nicht geprueft{ · {H} Selbstheilung}{ · {D} mehrfach}
  Vorschlaege: {V} (ueberholt {a} · gehoben {b} · doppelt {c})
  davon Sammelliste: {S} · Einzelfaelle: {E} · zurueckgestellt: {R}
  Erwartete Einsparung bei voller Annahme: {X} KB → {KB−X} KB{ (weiter KB ≥ schwelle_kb)}
```

Der Zusatz `(weiter KB ≥ schwelle_kb)` steht genau dann, wenn `{KB−X}` ≥ `{schwelle_kb}` — dieselbe
Bedingung, mit der `dtb:lesson` warnt.

**Groessen:** `{N}` = `LEKTIONEN` aus 1a · `{B}` = Topf behalten · `{U}` = nicht geprueft ·
`{S}` = Sammelliste · `{E}` = vorgelegte Einzelfaelle · `{R}` = zurueckgestellt (3d) · `{H}` =
Selbstheilung · `{D}` = Zeilen im Topf mehrfach (1a) · `{G}` = `{N} − {U} − {H} − {D}` ·
`{V}` = `{S} + {E} + {R}`.

**Mengenprobe (hartes Gate):** `{B} + {U} + {S} + {E} + {R} + {H} + {D} = {N}`, und jede Zeile aus
`lessons.md` steht in genau einem Topf. Weicht etwas ab → keine Vorlage, nichts ausmustern, genau
eine Zeile, Skill endet:
```
⚠ Konsolidierung unvollstaendig: {B}+{U}+{S}+{E}+{R}+{H}+{D} = {Summe} ≠ {N} — nichts ausgemustert, Lauf erneut starten
```
Grund: Eine beim Bau der Vorlage verlorene Lektion wuerde weder vorgelegt noch gezaehlt — und die
Bilanz meldete einen Bestand, den es nicht gibt.

`{V}` = 0 → nach der Uebersicht direkt die Bilanz (Schritt 7). Sonst kein „Weiter?" — die
Sammelliste ist die naechste Entscheidung.

---

## Schritt 4: Sammelliste

Alle sicheren Vorschlaege als EINE Liste, vorbelegt — der Mensch bestaetigt einmal und streicht,
was er selbst entscheiden will. Die Liste ist eine **Bestaetigung**, kein Sammel-Schreiben:
geschrieben wird danach Lektion fuer Lektion, jede sofort (Schritt 6).

Leere Sammelliste (alles Einzelfaelle) → dieser Schritt entfaellt still, weiter mit Schritt 5.

**Vorlage** (nur der Grund wird auf ~60 Zeichen gekuerzt; der Beleg steht immer vollstaendig — sein
pruefbarer Ort ist das Kriterium, das diese Zeile in die Sammelliste gebracht hat, 3c):

```
Sammelliste — {S} Lektion(en), Wirkung je Zeile: → Archiv ({wf}/archive/lessons-ausgemustert.md)

 1. L{N}  {Urteil}   {Grund}   {Beleg}  → Archiv{  ⓘ in features/{slug}/{datei}}
```

`{Urteil}` = `ueberholt`, `gehoben` oder `doppelt zu L{M}`.

Dann EINE blockierende Auswahl (`AskUserQuestion`), erste Option = Vorschlag:

- **Alle uebernehmen (Vorschlag)** → jede Zeile wird in Schritt 6 ausgemustert, in
  Listen-Reihenfolge
- **Nummern streichen** → danach Freitext, z.B. `2, 5`; nur das Gestrichene kurz
  rueckbestaetigen (`Gestrichen: 2, 5 → einzeln in Schritt 5`), nicht die ganze Liste erneut
  zeigen. **Gestrichen heisst NICHT ausgemustert und NICHT behalten** — gestrichene Zeilen gehen
  als Einzelfaelle in Schritt 5 und zaehlen nicht gegen die Kappung
- **Einzeln durchgehen** → alle Zeilen der Liste werden Einzelfaelle (ohne Kappung)

**Jede andere Antwort** gilt als nicht bestaetigt — genau eine Rueckfrage
(`Alle uebernehmen / streiche {Nr} / einzeln / Abbruch?`); bleibt sie unklar oder lautet
`Abbruch` → nichts ausmustern, genau eine Zeile, weiter mit der Bilanz (Schritt 7):
```
Nichts ausgemustert — Vorschlaege verworfen, lessons.md unveraendert{ bis auf die Selbstheilung}.
```
Nie stiller Auto-Write: ohne sichtbare Liste und ausdrueckliche Bestaetigung wird keine Lektion
ausgemustert.

---

## Schritt 5: Einzeln entscheiden

**Jede Entscheidung wird SOFORT geschrieben, nicht am Lauf-Ende gesammelt** (Schritt 6). Bricht
der Lauf nach dem dritten von sechs Einzelfaellen ab, sind drei Entscheidungen fest, und die
anderen drei prueft der naechste Lauf neu.

**Wer hierher kommt** — in dieser Reihenfolge, innerhalb jeder Gruppe aelteste zuerst, Paare (3b)
nebeneinander:
1. die vom Menschen herausgenommenen Zeilen (gestrichen oder „Einzeln durchgehen") — ungekappt
2. die Einzelfaelle aus 3c — gekappt nach 3d

Laeuft zeitlich NACH dem Schreiben der Sammelliste: die sicheren Ausmusterungen stehen schon
fest, ihre Sperren (3b) gelten hier bereits.

Fuer jede dieser Lektionen:

```
Einzelfall {i}/{E_lauf} — L{N} ({Datum}) · Vorschlag: {Urteil} ({Sicherheit}){ · Applies-to: alle}
  Rule:  {Rule, auf ~200 Zeichen gekuerzt}
  Grund: {Grund}
  Beleg: {Beleg}
  {nur bei doppelt:}          Bleibend: L{M} — "{Rule von L{M}, ~120 Zeichen}"
  {nur bei Kette/Kreis:}      Paar: L{M} ist selbst Vorschlag ({Urteil von L{M}})
  {nur bei gestrichener Zeile:} Aus der Sammelliste gestrichen
  {nur bei Treffer aus 3e:}   ⓘ in features/{slug}/{datei}
```

`{E_lauf}` = gestrichene bzw. herausgenommene Zeilen + `{E}` aus 3f. Entfaellt ein Fall durch eine
Sperre (3b), sinkt `{E_lauf}` fuer die folgenden Faelle um eins — der Zaehler zeigt nie mehr Faelle,
als noch vorgelegt werden.

Dann eine blockierende Auswahl (`AskUserQuestion`):

- **Ausmustern ({Urteil})** → Schritt 6
- **Behalten** → nichts schreiben; der naechste Lauf prueft die Lektion neu. Es gibt keinen
  Liegenlassen-Zustand — Lektionen tragen keinen Sichtungsvermerk
- **Die andere ausmustern (L{M})** — nur bei `doppelt`, und nur wenn L{M} nicht gesperrt ist
  (3b): der Mensch dreht die Richtung um; L{M} wird mit Grund `doppelt zu L{N}` ausgemustert,
  L{N} ist ab dann gesperrt. Ein noch offener Einzelfall zu L{M} entfaellt (schon entschieden)

**Jede andere Antwort** → genau eine Rueckfrage; bleibt sie unklar → **behalten** (im Zweifel
behalten), genau eine Zeile `→ L{N} behalten (keine eindeutige Antwort)`. `Stopp` oder `Abbruch`
→ alle noch offenen Einzelfaelle bleiben unveraendert, weiter mit der Bilanz (Schritt 7).

---

## Schritt 6: Schreiben

Jede bestaetigte Ausmusterung, sofort nach ihrer Bestaetigung — aus der Sammelliste in
Listen-Reihenfolge, aus Schritt 5 direkt nach der Wahl.

**Regeln fuer jede Ausmusterung:**
- **Ziel vor Quelle (L43):** zuerst die Archivzeile schreiben und zuruecklesen,
  danach erst die Entnahme aus `lessons.md`. Bricht der Lauf dazwischen ab, steht die Lektion
  an beiden Orten — sichtbar, und der naechste Lauf heilt es (1c) — statt an keinem
- **Eine Lektion, ein Durchgang, sofort** — nie am Ende gesammelt
- **Schreibfehler mitten drin** → melden, was geschrieben ist; alle noch offenen Lektionen bleiben
  unveraendert in `lessons.md`, weiter mit der Bilanz — **nie zurueckrollen**

### 6a: Archiv sicherstellen

`{wf}/archive/lessons-ausgemustert.md`. Fehlt die Datei → mit diesem Kopf anlegen (das einzige
`Write` dieses Skills — nur bei Neuanlage):

```markdown
# Ausgemusterte Lektionen

> Append-only. Aus `lessons.md` ausgemusterte Lektionen mit Grund (`/dtb:lesson-curate`).
> Nichts wird hier geloescht — die Datei ist der Suchraum, wenn ein Thema wiederkommt.
> Wiederherstellen: die Zeile ohne erste und letzte Spalte zurueck nach `lessons.md` kopieren.
> Die Nummern bleiben vergeben — `/dtb:lesson` zaehlt diese Datei bei der Nummernvergabe mit.

| Ausgemustert am | # | Datum | Context | Problem | Rule | Applies-to | Grund |
|-----------------|---|-------|---------|---------|------|------------|-------|
```

### 6b: Je Ausmusterung

1. **Archivzeile anhaengen.** Vorher exakt pruefen, ob die Nummer schon im Archiv steht (Spalte
   `#` = N) — dann nicht erneut anhaengen, sondern direkt Punkt 2: das Zuruecklesen vergleicht den
   Inhalt wie 1c, nur `ENTHALTEN` fuehrt zur Entnahme (eine bloss gleiche Nummer reicht nie). Sonst das
   Archiv per Read frisch lesen und per `Edit` am Tabellenende anhaengen (Anker = letzte Zeile
   der Datei). Die Zeile ist:
   `| {heute} ` + **die Lektionszeile woertlich** + ` {Grund-Zelle} |`
   — so bleiben die Lektions-Spalten byte-gleich, und Wiederherstellen heisst: erste und letzte
   Spalte wieder abschneiden. `{Grund-Zelle}` = `{Urteil}: {Grund} — Beleg: {Beleg}` aus der
   Voranalyse (`ueberholt`, `gehoben` oder `doppelt zu L{M}`); bei „Die andere ausmustern"
   `doppelt zu L{N}: vom Menschen umgekehrt — {Grund}`. Bare Pipes in der Grund-Zelle escapen
2. **Zuruecklesen** — ein selbstaendiger Bash-Block, erwartet `ANZAHL 1` und `ENTHALTEN`:
   ```bash
   L="{rules}/lessons.md"; A="{wf}/archive/lessons-ausgemustert.md"; n={N}
   z=$(grep -E "^\| *$n *\|" "$L" | tr -d '\r')
   [ "$(printf '%s\n' "$z" | grep -c .)" = 1 ] || { echo MEHRDEUTIG; exit 0; }
   r=$(tr -d '\r' < "$A" | grep -E "^\| *[0-9-]+ *\| *$n *\|")
   echo "ANZAHL $(printf '%s\n' "$r" | grep -c .)"
   printf '%s\n' "$r" | grep -qF -- "$z" && echo ENTHALTEN || echo FEHLT
   ```
   Dieselbe Pruefung wie die Selbstheilung (1c): die Archivzeile traegt die Lektionszeile
   woertlich — genau das braucht das Wiederherstellen. Keine feste Spaltenzahl: eine Lektion mit
   unescapter Pipe in Backticks (heute L17, L36) hat mehr Trenner und ist trotzdem korrekt
   archiviert. Abweichung (`MEHRDEUTIG`, `ANZAHL` ≠ 1, `FEHLT`) → Schreibfehler: keine Entnahme,
   melden, weiter mit der Bilanz
3. **Entnahme aus `lessons.md`** — die Datei unmittelbar vorher per Read neu lesen (das
   Edit-Werkzeug verlangt es, L99, und eine parallele Session kann inzwischen eine Lektion
   angehaengt haben), dann per `Edit`, exakte Zeile als Anker: `old_string` = die Lektionszeile
   samt Zeilenumbruch, `new_string` leer. **Nie `Write`** — die ganze Datei neu zu schreiben,
   ueberschriebe eine parallel erfasste Lektion. Schlaegt das Edit fehl (Zeile nicht mehr exakt
   vorhanden oder nicht eindeutig) → Schreibfehler; die Lektion steht dann an beiden Orten, und
   der naechste Lauf entscheidet in 1c
4. Meldung: `✔ L{N} ausgemustert ({Urteil}) → archive/lessons-ausgemustert.md`

---

## Schritt 7: Bilanz

Nach der letzten Entscheidung — oder nach Stopp, Abbruch, Schreibfehler oder `{V}` = 0. Zuerst
den Mess-Block aus 1a erneut ausfuehren (neuer Umfang), dann die Kandidaten zum Heben — ein
selbstaendiger Bash-Block:

```bash
L="{rules}/lessons.md"
tr -d '\r' < "$L" | sed 's/[\][|]//g' \
  | awk -F'|' '/^\| *[0-9]+ *\|/ && $(NF-1) ~ /(^|[ ,])alle([ ,]|$)/ {n=$2; gsub(/ /,"",n); printf "L%s ", n}'
```

```
Lektionen kuratiert:

  Ausgemustert:    {n_aus}  (ueberholt {a} · doppelt {b} · gehoben {c})
  Selbstheilung:   {n_heil}  (Entnahme nachgeholt)
  Behalten:        {n_beh}  (davon {n_mensch} vom Menschen behalten)
  Nicht geprueft:  {n_ung}  (Voranalyse ausgefallen — bleiben ungeprueft im Bestand)
  Zurueckgestellt: {n_zur}  (Kappung einzeln_pro_lauf → naechster Lauf)
  Mehrfach:        {n_mehr}  (Nummer mehrmals in lessons.md — von Hand klaeren)

  lessons.md: {Zeilen} Zeilen, {KB} KB (vorher {KB_vorher} KB, Schwelle {schwelle_kb} KB)
```

**Ist-Werte, nicht die Groessen aus 3f:** jede Zahl zaehlt, was tatsaechlich geschrieben bzw.
entschieden wurde. Zeilen mit `0` entfallen — die Bilanz zeigt nur, was passiert ist.

Darunter, je nur wenn zutreffend, genau eine Zeile:
- Neuer Umfang `KB ≥ schwelle_kb` (dieselbe Bedingung, mit der `dtb:lesson` warnt):
  `⚠ lessons.md bleibt bei KB ≥ {schwelle_kb} — die Warnung in /dtb:lesson feuert weiter`
- Lektionen mit `Applies-to: alle` vorhanden (nur Hinweis — gehoben wird nicht hier):
  `💡 {K} Lektion(en) gelten fuer alle Skills ({Nummern}) — Kandidaten zum Heben nach skills/CLAUDE.md bzw. {rules}/`
- Abbruch oder Schreibfehler mitten im Durchgang:
  `Abgebrochen nach Entscheidung {K} von {M} — die {K} getroffenen Entscheidungen sind geschrieben.`

**Kein Automatismus, kein Kettenaufruf.** Der Skill committet nicht und startet keinen weiteren
Skill.

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
