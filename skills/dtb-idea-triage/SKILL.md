---
name: dtb:idea-triage
description: >-
  Use when: "Becken sichten", "Befunde triagieren", "idea triage",
  "Verlustfunde durchgehen", "was liegt im Becken". Pre-sorts the machine
  findings in INBOX-BEFUNDE.md with read-only background agents (checked against
  the project state, related findings bundled, discards proposed with evidence,
  lessons and subject-matter questions routed to their own targets), lets the
  human confirm one pre-filled collection list with veto, then triages the rest
  one by one: promote to INBOX.md, discard to the archive, or leave lying exactly
  once. Writing — every confirmed decision is written immediately.
disable-model-invocation: true
argument-hint: "[optional: alle | anzahl]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
pipeline:
  stage: idea
  after: [dtb:workflow-checkpoint]
  next: [dtb:idea-review]
  consumes: [INBOX-BEFUNDE.md, INBOX.md, workflow.config.yaml, ARCHIVE_LOG.md, archive/INBOX-BEFUNDE-verworfen.md, project-rules/lessons.md, features/*/spec.md, features/*/discovery.md]
  produces: [INBOX-BEFUNDE.md, INBOX.md, archive/INBOX-BEFUNDE-verworfen.md, project-rules/lessons.md, features/*/spec.md, features/*/discovery.md]
---

# Befund-Becken sichten (Triage)

Du sortierst die maschinell erfassten Verlustfunde vor und laesst den Menschen entscheiden: Eine
lesende Voranalyse schlaegt je Fund mit Beleg vor, ob er befoerdert, gebuendelt, verworfen,
an eine bestehende Idee nachgetragen oder als Lektion bzw. Fach-Frage abgelegt wird. Der Mensch
bestaetigt die sicheren Vorschlaege als EINE Sammelliste; der Rest laeuft einzeln — befoerdern,
verwerfen oder ein einziges Mal liegenlassen.

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
  einzeln_pro_lauf: 5     # wieviele Einzelfaelle (Schritt 6) ein Lauf hoechstens vorlegt
```

Fehlt `einzeln_pro_lauf` → Rueckfall auf den Alt-Schluessel `altbestand_pro_lauf` (bis
2026-10 die Kappung des Altbestands; Bestandsprojekte tragen nur ihn), fehlen beide → `5`.
Fehlt `becken_schwelle` → `10`. Kein Hinweis, kein Abbruch.

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

**„Ungesichtet" heisst: noch nicht endgueltig entschieden** — also `leer` ODER `L1 …` ODER
`Altbestand`. Diese eine Definition gilt fuer alle Zaehler (Handoff-Erinnerung des Checkpoints,
`dtb:project-health`, Abschluss-Bilanz der Triage). Entschieden ist ein Eintrag erst, wenn er das
Becken verlassen hat — befoerdert (auch als Buendel-Traeger) oder mit Archiv-Eintrag verworfen,
gebuendelt, nachgetragen oder als Lektion bzw. Fach-Frage erfasst.

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
2. **Unmittelbar vor JEDER Statusentscheidung** (jedem Schreiben in Schritt 7) dieselbe Abfrage
   erneut ausfuehren und vergleichen:
   - mtime unveraendert → still weiterarbeiten (kein Output)
   - mtime veraendert → Datei NEU lesen und den Inhalt vergleichen:
     - Inhalt tatsaechlich abweichend → genau eine Zeile
       `⚠ INBOX-BEFUNDE.md wurde seit dem Einlesen geaendert ({neue mtime}) — Stand neu geladen`
       und mit dem FRISCHEN Stand weiterarbeiten (kein Abbruch, keine Nachfrage)
     - Inhalt identisch (nur mtime, z.B. touch/Checkout) → keine Warnung
     - **Existenzprobe nach Neu-Laden:** steht die Zeile des Funds, der gerade geschrieben werden
       soll, im frischen Stand nicht mehr oder mit anderem Befund-Text → fuer diesen Fund nichts
       schreiben (auch nicht am Ziel — „Ziel vor Quelle" erzeugte sonst einen Eintrag ohne
       Quelle), genau eine Zeile `⚠ #{N} nicht mehr unveraendert im Becken — uebersprungen`, weiter
       mit dem naechsten
   - Datei existiert nicht mehr → wie Abweichung behandeln:
     `⚠ INBOX-BEFUNDE.md seit dem Einlesen entfernt/verschoben — Entscheidung ggf. hinfaellig`
   - **Nach jedem EIGENEN Schreibvorgang** am Becken die gemerkte mtime (und den gemerkten
     Inhalt) auf den neuen Stand nachfuehren (L46) — sonst meldet die Pruefung ab dem zweiten
     Eintrag jedes Mal die eigene Aenderung als fremde
3. **Bewusste Restluecke:** Das Fenster zwischen Pruefung und eigenem Schreiben bleibt
   (kein Locking) — Konvention: `skills/CLAUDE.md` → „Parallele Sessions".

---

## Schritt 2: Sichtungsmenge bestimmen

Die Voranalyse (Schritt 3) liest **alles Ungesichtete** — Sichtung-Spalte leer (neu),
`L1 …` (faellig, Zwangsentscheidung in Schritt 6) und `Altbestand`. Reihenfolge: **aelteste
zuerst** (aufsteigend nach Datum, bei gleichem Datum nach Nummer).

**Warum hier das ganze Becken, obwohl die Triage frueher nie alles sichtete:** Die alte Regel
galt, weil jeder Eintrag einzeln entschieden wurde — die Sichtungsarbeit wuchs mit dem Bestand,
und genau dort brach die Triage ab. Mit der Vorsortierung kostet ein sicherer Vorschlag in der
Sammelliste (Schritt 5) nur einen Blick, und Buendel und Dubletten erkennt man nur im
Gesamtbild. Die Portionierung lebt weiter — sie wandert an die **Einzelfaelle**: hoechstens
`einzeln_pro_lauf` davon je Lauf (Schritt 4); der Rest bleibt ungesichtet im Becken und kommt
im naechsten Lauf erneut in die Voranalyse.

**Argument `alle`** → die Kappung der Einzelfaelle entfaellt. **Argument als Zahl** → diese Zahl
ersetzt `einzeln_pro_lauf`.

**Leere Sichtungsmenge** (Becken leer, oder alles gesichtet und nichts faellig) → genau eine
Zeile, Skill endet — es werden keine Agenten gestartet:
```
Nichts zu sichten — {N} Eintrag(e) im Becken, davon 0 neu und 0 faellig.
```

---

## Schritt 3: Voranalyse

Je Fund entsteht ein **Vorschlag mit Beleg** — gelesen, nie geschrieben. Die Voranalyse
entscheidet nichts: was mit einem Fund passiert, bestaetigt der Mensch in Schritt 5 oder 6.

### 3a: Weiche — inline oder Hintergrund-Agenten

- **Weniger als 5 Funde** in der Sichtungsmenge → keine Agenten; du fuehrst den Auftrag unten
  selbst im Hauptkontext aus (gleiches Ergebnis-Format). Ein Agenten-Start lohnt sich hier nicht
- **Sonst** → Sichtungsmenge in **Portionen zu hoechstens 25 Funden** teilen (aelteste zuerst,
  Reihenfolge aus Schritt 2), je Portion **ein** Agent, alle parallel starten und auf alle
  Ergebnisse warten
- **Agenten-Typ:** `Explore` — er hat werkzeugseitig kein Edit/Write. Ist `Explore` in dieser
  Umgebung nicht verfuegbar → `general-purpose` mit demselben Auftrag (das Schreibverbot steht
  dann nur im Auftrag, wie bei den Sub-Agenten von `dtb:impl-review`) und genau eine Zeile:
  ```
  ⚠ Agenten-Typ Explore nicht verfuegbar — Voranalyse mit general-purpose, Schreibverbot nur im Auftrag
  ```

### 3b: Auftrag (je Portion)

Platzhalter fuellen: `{root}` = absoluter Projekt-Root, `{wf}` = `{config.paths.workflows}`,
`{rules}` = `{config.paths.rules}`, `{portion}` = die Zeilen der Portion im vollen Wortlaut,
`{alle}` = **alle** Funde der Sichtungsmenge als `#{N} {erste ~80 Zeichen}` (macht Verwandtschaft
ueber Portionsgrenzen sichtbar).

```
Du pruefst maschinell erfasste Befunde gegen den aktuellen Projektstand und schlaegst je
Befund vor, was mit ihm passieren soll. NUR LESEN: keine Datei anlegen, aendern oder loeschen,
keine Kommandos mit Schreibwirkung. Du entscheidest nichts — du lieferst Vorschlaege mit Beleg.

Projekt-Root: {root}

Deine Befunde (vollstaendig):
{portion}

Alle Befunde dieses Laufs (nur Nummer + Anfang, fuer Verwandtschaft):
{alle}

Pruefe je Befund gegen:
- den Code- und Skill-Bestand unter {root} (ist der beschriebene Zustand noch so?)
- {wf}/archive/ inkl. ARCHIVE_LOG.md (umgesetzt, archiviert?)
- {wf}/INBOX.md (steht die Sache dort schon, oder ergaenzt sie eine offene Idee?)
- {wf}/archive/INBOX-BEFUNDE-verworfen.md (schon einmal verworfen?)
- {rules}/lessons.md (steht die Erkenntnis schon als Lektion?)
- Alterungs-Indiz: nennt der Befund einen Pfad, der existiert, pruefe
  `git -C {root} log -1 --format=%ad --date=short -- {pfad}`. Ist die Datei NACH dem
  Befund-Datum geaendert, nenne das im Grund ("Datei seit dem Befund geaendert") — ein Indiz,
  kein Urteil. Kein Git, kein Pfad → entfaellt.

Vorschlag — genau einer je Befund:
- Befoerdern            — offener, echter Aenderungswunsch
- Verwerfen: erledigt   — bereits umgesetzt
- Verwerfen: ueberholt  — Bezug oder Anlass entfallen
- Verwerfen: Dublette #N — die Sache steht schon als #N (INBOX, Becken oder Verworfen-Archiv)
- Verwerfen: falsches Repo — gehoert nicht in dieses Projekt
- Nachtrag #N           — ergaenzt die offene INBOX-Idee #N, traegt allein nicht
- Lektion               — nicht-offensichtliche, wiederverwendbare Erkenntnis ohne
                          Aenderungsauftrag (Kontext → Falle → kuenftige Regel)
- Fachfrage {slug}      — nur fachlich (im Meeting) beantwortbare Frage; {slug} = passender
                          Ordner unter {wf}/features/ mit spec.md oder discovery.md, sonst "—"
- Unklar: {Frage}       — du kannst nicht einordnen; formuliere die eine Frage an den Menschen

Dublette heisst: gleicher Gegenstand + gleiche Aussage — der vorhandene Eintrag koennte den
Befund ohne Verlust ersetzen. Gleicher Gegenstand mit anderer Aussage ist KEINE Dublette
(eher Nachtrag oder Verwandt).

Beleg: wo du es gesehen hast. Bei JEDEM Verwerfen mindestens ein nachsehbarer Ort —
Datei:Zeile oder Commit-SHA. Ohne Ort bleibt der Vorschlag ein Verdacht.

Sicherheit: hoch | mittel | niedrig.
Verwandt: andere Befund-Nummern AUS DER GESAMTLISTE, die denselben Gegenstand betreffen und
gemeinsam zugeschnitten werden sollten (z.B. "#86, #118"), sonst "—".

Ausgabe: GENAU eine Zeile je Befund, keine Kopfzeile, keine Prosa davor oder danach, Format:
#{N} | {Vorschlag} | {Grund, 1 Satz} | {Beleg} | {Sicherheit} | {Verwandt}
Literale Pipes in Grund oder Beleg immer als \| angeben.
```

### 3c: Ergebnis pruefen (Werkzeug-Fehlschlag ist kein Datenbefund)

Je Portion, bevor irgendetwas weiterverarbeitet wird:

1. **Nummern-Gate:** Die Nummern der Ergebniszeilen (Zeilen, die mit `#` und einer Ziffer
   beginnen — eine Ueberschrift wie `# Ergebnis` zaehlt nicht) muessen **genau** die Nummern der
   Portion sein: jede genau einmal, keine fremde. Fehlt eine, steht eine doppelt oder stammt eine
   aus einer anderen Portion, liefert der Agent nichts, oder ist das Format unlesbar → **alle Funde
   dieser Portion gelten als „ohne Vorschlag"**. Nie als „nichts gefunden" werten — ein leeres
   Ergebnis ist ein Ausfall, kein Befund. Mengen- statt Zahlpruefung, weil eine fremde Nummer den
   eigenen Fund still verschwinden liesse und dem fremden zwei Vorschlaege gaebe
2. **Spaltenpruefung je Zeile:** genau **6 Spalten** — also genau 5 Trenner `|`, escapte `\|`
   zaehlen nicht. Weicht eine Zeile ab → nur dieser Fund gilt als „ohne Vorschlag". Grund: ein
   unescapter Trenner verschiebt die Spalten, ohne dass das Nummern-Gate anschlaegt
3. **Bekannter Vorschlag:** Spalte 2 muss einer der Vorschlaege aus dem Auftrag sein; sonst
   „ohne Vorschlag"

Funde „ohne Vorschlag" gehen als Einzelfaelle in Schritt 6 (mit der Kennzeichnung
`Voranalyse ausgefallen`). Faellt eine ganze Portion aus, genau eine Zeile:
```
⚠ Voranalyse fuer {K} Fund(e) ausgefallen (#{a}–#{b}) — sie kommen einzeln, ohne Vorschlag
```

---

## Schritt 4: Konsolidieren

Aus den Ergebniszeilen aller Portionen entsteht die Vorlage: Buendel, Einzelfaelle und
Sammelliste. Alles hier ist mechanisch aus den Feldern abgeleitet — keine neue Bewertung.

### 4a: Struktur-Check (vor der ersten Nutzung einer Quelle per Referenz)

Mehrere Regeln dieses Skills stehen NICHT hier, sondern in den Skills, denen sie gehoeren
(`dtb:lesson`, `dtb:open-question`, `dtb:idea`). Bevor eine davon zum ersten Mal genutzt wird,
muss die Quelle existieren und ihre Anker tragen. Der Check steht hier und nicht erst vor dem
Schreiben (Schritt 7), weil 4c `dtb:lesson` bereits lesend nutzt. Muster:
`dtb:workflow-checkpoint` Schritt 0 („Struktur-Check (Kopplungs-Waechter)").

- **Nur benoetigte Quellen pruefen** — nach den Vorschlaegen ALLER Funde dieses Laufs (auch der
  kuenftigen Einzelfaelle, L42): `Lektion` → `dtb:lesson`; `Fachfrage` → `dtb:open-question`;
  `Befoerdern`, Buendel oder `Fachfrage —` → `dtb:idea`. `dtb:idea` wird immer geprueft, sobald
  irgendein Fund in Schritt 6 befoerdert werden koennte — also in jedem Lauf mit Einzelfaellen
- **Quelle aufloesen — Repo zuerst, dann Installation:** `skills/dtb-{lesson,open-question,idea}/SKILL.md`
  relativ zum Projekt-Root, sonst `~/.claude/skills/dtb-{lesson,open-question,idea}/SKILL.md`. Im
  Kit-Repo ist das Repo die Quelle, aus der `kit-sync` verteilt; Zielprojekte haben kein `skills/`
- **Anker-Grep zeilenverankert** auf den ganzen Titel, nie als Substring (die
  Kopplungs-Hinweise zitieren die Titel selbst und lieferten ein falsches Gruen) — je Anker in
  EINEM selbstaendigen Bash-Block:
  ```bash
  tr -d '\r' < {quelle} | grep -c -x -F "{anker}"
  ```

  | Quelle | Anker (woertlich) | Genutzt in |
  |--------|-------------------|------------|
  | `dtb:lesson` | `## Schritt 2: In 4 Felder strukturieren` | 7f Punkt 1 |
  | `dtb:lesson` | `## Schritt 3: Duplikat-Check` | 4c |
  | `dtb:lesson` | `## Schritt 4: Append-only speichern` | 7f Punkt 2 |
  | `dtb:open-question` | `## Schritt 3: Ziel-Datei waehlen` | 7g Punkt 2 |
  | `dtb:open-question` | `## Schritt 4: Zeile formatieren, Duplikat pruefen, Ziel bestaetigen` | 7g Punkt 2 |
  | `dtb:open-question` | `## Schritt 5: Schreiben + Abschluss` | 7g Punkt 3 |
  | `dtb:idea` | `## Duplikat-Check` | 7a Punkt 1 |

- Alle Anker gefunden → eine Statuszeile: `🧩 Struktur-Check: {n}/{n} Anker in {aufgeloeste Quelle(n)} gefunden`
- **Zwei getrennte Fehlerpfade** (nie vermischen — eine fehlende Installation ist KEINE Drift):
  1. Datei in beiden Quellen nicht gefunden → Installations-Problem:
     ```
     ⚠ Quelle dtb:{lesson|open-question|idea} weder im Projekt (skills/) noch global
        (~/.claude/skills/) gefunden. → /dtb:kit-sync sync
     ```
  2. Datei vorhanden, Anker fehlt → Struktur-Drift:
     ```
     ⚠ Struktur-Check fehlgeschlagen: {Quelle} — Anker "{Anker}" nicht gefunden.
        dtb:{lesson|open-question|idea} wurde umgebaut; ich nutze die Regel NICHT auf veralteter
        Basis. → diesen Abschnitt anpassen (die Kopplungs-Hinweise dort nennen diesen Leser).
     ```
- **Folge je gefallener Quelle:**
  - `dtb:lesson` → alle `Lektion`-Vorschlaege werden Einzelfaelle (4d); in Schritt 6 nur
    befoerdern, verwerfen oder liegenlassen — der Lektions-Weg ist in diesem Lauf gesperrt
  - `dtb:open-question` → alle `Fachfrage`-Vorschlaege mit Slug werden Einzelfaelle; der
    Fachfrage-Weg ist gesperrt
  - `dtb:idea` → der Duplikat-Check in 7a entfaellt mit genau einer Zeile
    `⚠ Duplikat-Check beim Befoerdern entfaellt (dtb:idea nicht pruefbar)` — er stellt nur eine
    Frage, sein Ausfall schreibt nichts Falsches (fail-open wie bei den Capture-Skills)

> **Benanntes Restrisiko:** Der Check prueft Anker-EXISTENZ, nicht Regel-INHALT. Gegen
> inhaltliche Drift verteidigen die Kopplungs-Hinweise an den sieben Sektionen der Quellen.

### 4b: Buendel bilden

1. **Kanten nur gegenseitig:** Eine Kante zwischen #a und #b entsteht nur, wenn #a in `Verwandt`
   #b nennt **und** #b #a nennt. Einseitige Nennungen und Verweise auf Nummern ausserhalb der
   Sichtungsmenge erzeugen keine Kante — sie bleiben ein Hinweis „verwandt" in der Zeile
2. **Keine transitive Huelle:** #a~#b und #b~#c machen #a und #c nicht verwandt; ein Buendel ist
   ein Traeger plus seine **direkten** Nachbarn. Grund: die Agenten setzen `Verwandt` grosszuegig —
   im Trockenlauf 2026-10-16 verschmolz die Huelle fuenf Themen zu einem Buendel aus 21 Funden,
   nicht pruefbar und beim Streichen ungekappt
3. **Traeger und Glieder:** Kandidaten sind Funde mit Vorschlag `Befoerdern`, die nach 4d kein
   Einzelfall sind. Absteigend nach Nummer: hat der hoechste noch freie Kandidat mindestens einen
   gegenseitigen Nachbarn unter den freien Kandidaten, wird er **Traeger**, diese Nachbarn werden
   seine **Glieder**, alle gelten danach als vergeben (jeder Fund in hoechstens einem Buendel).
   Deterministisch, damit zwei Laeufe dieselben Buendel bilden; wer einen anderen Traeger will,
   streicht die Buendel-Zeile in Schritt 5 — die Glieder kommen dann einzeln in Schritt 6
4. **Nachbarn mit anderem Vorschlag** (Verwerfen, Lektion …) behalten ihren eigenen Vorschlag und
   werden in der Buendel-Zeile nur als „verwandt" genannt; ohne zwei Kandidaten kein Buendel

### 4c: Lektions-Vorschlaege gegen den Bestand pruefen

Je Vorschlag `Lektion` die Duplikat-Bewertung aus `## Schritt 3: Duplikat-Check` in
`dtb:lesson` ausfuehren (per Referenz — die Regel dort lesen, nicht hier; nur die Bewertung,
ohne deren Rueckfrage). Treffer → der Vorschlag wird zu
`Verwerfen: Lektion L{N} deckt ab` (Beleg `lessons.md:{Zeile} (L{N})`, Sicherheit **`mittel`** —
der Stichwort-Treffer ist ein unscharfer Vergleich, eine neue Behauptung mit eigener Unsicherheit;
er wird deshalb immer einzeln vorgelegt, nie per Sammelliste verworfen). Faellt die
Quelle im Struktur-Check (4a) → alle `Lektion`-Vorschlaege werden Einzelfaelle.

### 4d: Einzelfall oder Sammelliste (mechanisch)

Ein Fund ist **Einzelfall** (Schritt 6), wenn mindestens eines gilt:
- Vorschlag `Unklar: …`
- Vorschlag `Verwerfen: …` mit Sicherheit ≠ `hoch`
- Vorschlag `Verwerfen: …` **ohne pruefbaren Ort** im Beleg (kein `Datei:Zeile`, keine
  Commit-SHA) — auch bei Sicherheit `hoch`: ein plausibler Beleg ohne Ort rutscht bei
  „Alle uebernehmen" ungeprueft durch
- Vorschlag `Verwerfen: Dublette #M`, wenn #M selbst in der Sichtungsmenge steht — zwei Funde
  koennten sich sonst gegenseitig verwerfen, und keiner bliebe uebrig
- **ohne Vorschlag** (Voranalyse ausgefallen, 3c)
- Vorschlag eines Typs, dessen Quelle im Struktur-Check (4a) gefallen ist

Alle anderen Funde kommen in die **Sammelliste** (Schritt 5). Die Sichtung-Spalte `L1 …`
aendert daran nichts — ein faelliger Fund mit sicherem Vorschlag darf in die Sammelliste; wird
er dort gestrichen, gilt in Schritt 6 die Zwangsentscheidung.

### 4e: Kappung der Einzelfaelle

Hoechstens `einzeln_pro_lauf` Einzelfaelle (Argument `alle` → keine Kappung; Zahl-Argument
ersetzt den Wert), **aelteste zuerst**. Die uebrigen bleiben **unveraendert** im Becken
(Sichtung-Spalte bleibt, wie sie ist) und kommen im naechsten Lauf erneut in die Voranalyse.

**Die Kappung gilt fuer alles, was der Lauf selbst nach Schritt 6 schickt** — die Einzelfaelle
aus 4d UND die von Schritt 7 verschobenen Zeilen (Duplikat-Treffer beim Befoerdern,
Nachtrag-Ziel nicht offen, aufgeloestes Buendel). Die verschobenen entstehen erst beim
Schreiben; deshalb wird die Kappung vor Schritt 6 ueber beide Gruppen gemeinsam neu angewandt
(aelteste zuerst), ueberzaehlige bleiben unveraendert im Becken.
**Ausgenommen ist nur, was der Mensch selbst herausnimmt** — gestrichene Sammellisten-Zeilen und
„Einzeln durchgehen" (Schritt 5): wer streicht, hat sich die Einzelentscheidung bewusst geholt.

### 4f: Uebersicht vor der Vorlage

```
Becken-Triage: {N} Fund(e) vorsortiert{ ({K} inline, ohne Agenten)}

  Buendel:       {B} (mit {G} Gliedern)
  Sammelliste:   {S}
  Einzelfaelle:  {E}{ — davon {A} ohne Vorschlag (Voranalyse ausgefallen)}
  Zurueckgestellt (Kappung): {R} → naechster Lauf
```

**Groessen (gelten auch in Schritt 5 und 8):** `{B}` = Buendel = Traeger · `{G}` = Glieder
**ohne** Traeger (archiviert „gebuendelt in #…") · `{S}` = Einzelzeilen der Sammelliste ohne
Buendel · `{E}` = vorgelegte Einzelfaelle · `{R}` = zurueckgestellt · `{N}` = Sichtungsmenge.

**Summenprobe (hartes Gate):** `{B} + {G} + {S} + {E} + {R} = {N}` — jeder Fund steht genau
einmal in genau einem Topf. Weicht die Summe ab → keine Vorlage, nichts schreiben, genau eine
Zeile, Skill endet:
```
⚠ Vorsortierung unvollstaendig: {B}+{G}+{S}+{E}+{R} = {Summe} ≠ {N} — nichts geschrieben, Lauf erneut starten
```
Grund: Ein beim Bau der Vorlage verlorener Fund wuerde sonst weder geschrieben noch vorgelegt
(Testprojekt 2026-10-16: ein Fund fehlte, die Zahlen standen schon da, nur der Vergleich fehlte).

Kein „Weiter?" — die Sammelliste (Schritt 5) ist die naechste Entscheidung.

---

## Schritt 5: Sammelliste

Alle sicheren Vorschlaege als EINE Liste, vorbelegt — der Mensch bestaetigt einmal und
streicht, was er selbst entscheiden will. Die Liste ist eine **Bestaetigung**, kein
Sammel-Schreiben: geschrieben wird danach Zeile fuer Zeile, jede sofort (Schritt 7).

Leere Sammelliste (alles Einzelfaelle) → dieser Schritt entfaellt still, weiter mit Schritt 6.

**Vorlage** (Buendel oben, dann je Fund eine Zeile; Grund auf ~60, Beleg auf ~40 Zeichen
gekuerzt — der volle Text steht im Becken):

```
Sammelliste — {S} Einzelzeilen{ + {B} Buendel (mit {G} Gliedern)}

Buendel:
 B1  #{T} traegt #{a}, #{b}{ (verwandt: #{c} {Vorschlag})}  → INBOX.md #{T}; Glieder → Archiv „gebuendelt in #{T}"

 1  #{N}  Befoerdern                 {Grund} · {Beleg}   → INBOX.md
 2  #{N}  Verwerfen: erledigt        {Grund} · {Beleg}   → Archiv
 3  #{N}  Nachtrag #{Z}              {Grund} · {Beleg}   → INBOX.md #{Z}
 4  #{N}  Lektion                    {Kern der Regel}    → lessons.md
 5  #{N}  Fachfrage {slug}           {Frage, gekuerzt}   → features/{slug}/
 6  #{N}  Fachfrage —                {Frage, gekuerzt}   → INBOX.md („Fachfrage: …")
```

Dann EINE blockierende Auswahl (`AskUserQuestion`), erste Option = Vorschlag:

- **Alle uebernehmen (Vorschlag)** → jede Zeile wird in Schritt 7 ausgefuehrt
- **Nummern streichen** → danach Freitext, z.B. `3, 7, B1`; nur das Gestrichene kurz
  rueckbestaetigen (`Gestrichen: 3, 7, B1 → einzeln in Stufe 2`), nicht die ganze Liste erneut
  zeigen. **Gestrichen heisst NICHT verworfen** — gestrichene Zeilen gehen als Einzelfaelle in
  Schritt 6. Eine gestrichene Buendel-Zeile schickt alle ihre Glieder einzeln dorthin. Gestrichene
  Zeilen zaehlen nicht gegen die Kappung `einzeln_pro_lauf`
- **Einzeln durchgehen** → alle Zeilen der Liste werden Einzelfaelle (ohne Kappung)

**Jede andere Antwort** gilt als nicht bestaetigt — genau eine Rueckfrage
(`Alle uebernehmen / streiche {Nr} / einzeln / Abbruch?`); bleibt sie unklar oder lautet
`Abbruch` → nichts schreiben, genau eine Zeile, Skill endet:
```
Nichts geschrieben — Vorschlaege verworfen, Becken unveraendert.
```
Nie stiller Auto-Write: ohne sichtbare Liste und ausdrueckliche Bestaetigung wird keine Zeile
aus der Sammelliste geschrieben.

---

## Schritt 6: Einzeln entscheiden (Stufe 2)

**Jede Entscheidung wird SOFORT geschrieben, nicht am Lauf-Ende gesammelt.** Bricht der Lauf
nach Eintrag 4 von 8 ab, sind vier Entscheidungen fest und vier stehen beim naechsten Lauf
wieder an. Ein Sammel-Schreiben am Ende verliert bei jedem Abbruch alles, was schon entschieden
war (INBOX #71) — deshalb ist die Reihenfolge hier verbindlich: entscheiden → schreiben →
naechster Eintrag.

**Wer hierher kommt** — in dieser Reihenfolge, innerhalb jeder Gruppe aelteste zuerst:
1. die vom Menschen herausgenommenen Zeilen (gestrichen oder „Einzeln durchgehen", Schritt 5) —
   ungekappt
2. die Einzelfaelle aus 4d und die von Schritt 7 verschobenen Zeilen (Duplikat-Treffer beim
   Befoerdern, Nachtrag-Ziel nicht offen, aufgeloestes Buendel) — gemeinsam gekappt nach 4e

Laeuft zeitlich NACH dem Schreiben der Sammelliste (Schritt 7): wer streicht, entscheidet die
gestrichenen Zeilen hier, nachdem die sicheren schon festgeschrieben sind.

Fuer jeden dieser Funde:

```
Befund #{N} ({Datum}){, Sichtung: L1 {Datum} — Entscheidung jetzt erzwungen}
  "{Befund-Text, auf ~200 Zeichen gekuerzt}"

  Vorschlag: {Vorschlag} ({Sicherheit}) — {Grund}
  Beleg:     {Beleg}
  {nur bei Unklar:}            Frage der Voranalyse: {Frage}
  {nur ohne Vorschlag:}        Voranalyse ausgefallen — kein Vorschlag
  {nur bei verschobener Zeile:} Verschoben aus Schritt 7: {Grund, z.B. aehnliche Idee #{M}}

  Aktion?
    {nur bei Nachtrag/Lektion/Fachfrage:} 0. Vorschlag uebernehmen: {Vorschlag} → {Ziel}
    1. Befoerdern → INBOX.md
    2. Verwerfen  → archive/ (Begruendung noetig)
    3. Liegenlassen (nur einmal moeglich)
```

### Aktionen

**Vorschlag uebernehmen (0):** Nur angeboten, wenn der Vorschlag `Nachtrag #Z`, `Lektion` oder
`Fachfrage …` lautet, seine Quelle im Struktur-Check (4a) gefunden wurde und die Zeile nicht
gerade wegen dieses Wegs verschoben wurde (z.B. Nachtrag-Ziel nicht offen). Sonst entfiele mit
dem Streichen einer Sammellisten-Zeile auch ihr Ausgang — „gestrichen heisst nicht verworfen"
verspraeche mehr, als Stufe 2 bietet. Ausfuehrung in Schritt 7 ueber 7e, 7f bzw. 7g.

**Befoerdern (1):** Ausfuehrung in Schritt 7.

**Verwerfen (2):**
- **Begruendung ist Pflicht** — ein Satz genuegt. Sie landet in der Archivdatei und ist in
  sechs Monaten das Einzige, was den Vorgang noch erklaert. Ohne Begruendung nicht schreiben,
  sondern einmal nachfragen. Lag ein `Verwerfen`-Vorschlag vor, ist `{Grund} — Beleg: {Beleg}`
  der Vorschlag: `→ weiter = uebernehmen · oder eigene Begruendung nennen`.
- Ausfuehrung in Schritt 7.

**Liegenlassen (3):**
- **Nur zulaessig, wenn die Sichtung-Spalte leer ist.** Bei `L1 …` ist die Option nicht im
  Angebot — dort gilt die **Zwangsentscheidung**: nur 0 (falls angeboten), 1 oder 2. Wird sie
  trotzdem gewaehlt:
  ```
  #{N} wurde bereits einmal liegengelassen ({L1-Datum}). Jetzt entscheiden: befoerdern oder verwerfen.
  ```
- Sonst: Sichtung-Spalte auf `L1 {heutiges Datum}` setzen, Zeile bleibt im Becken, weiter.
- Bei `Altbestand`: gilt wie leer — Liegenlassen setzt `L1 {heute}` und ersetzt damit den
  Altbestand-Vermerk (der Eintrag ist dann in der normalen Faelligkeits-Schiene).

---

## Schritt 7: Entscheidung ausfuehren

Fuehrt jede bestaetigte Zeile aus — aus der Sammelliste (Schritt 5) in Listen-Reihenfolge,
Buendel zuerst, und danach jede Einzelentscheidung aus Schritt 6 sofort nach ihrer Wahl.

**Regeln fuer jeden Weg:**
- **Eine Zeile, ein Schreibvorgang, sofort** (INBOX #71) — nie am Ende gesammelt
- **Ziel vor Quelle** (L43): erst am Ziel schreiben und pruefen, dann die Becken-Zeile entfernen.
  Bricht der Lauf dazwischen ab, steht der Fund doppelt (sichtbar, heilbar) statt gar nicht
- **Lesestand-Pruefung** vor jedem Schreiben (Abschnitt oben), inkl. Existenzprobe der Zeile nach
  einem Neu-Laden
- **Schreibfehler mitten drin** → melden, was geschrieben ist; die uebrigen Zeilen bleiben
  unveraendert im Becken — **nie zurueckrollen**
- **Archiv-Eintrag** = 7b Punkte 1–2 (Datei sicherstellen, anhaengen) mit der jeweils genannten
  Begruendung

### 7a: Befoerdern

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
   `stattdessen verwerfen` → **weiter mit 7b**, unveraendert: die Begruendung bleibt Pflicht,
   der Eintrag geht mit ihr ins Archiv. Kein eigener Kurzpfad, keine Ausnahme.
   Kein Treffer → keine Ausgabe, direkt weiter.
   **Zeile aus der Sammelliste:** statt der Rueckfrage wird die Zeile nicht geschrieben, sondern
   als Einzelfall nach Schritt 6 verschoben (mit dem Treffer als Hinweis) — keine Rueckfrage
   mitten im Sammel-Durchgang.

   > **Schema-Abweichung (begruendet):** Das Meldeform-Schema in `skills/CLAUDE.md` sieht
   > `(Ja / Abbrechen)` vor. Hier steht `stattdessen verwerfen` statt `Abbrechen`, weil
   > „Abbrechen" den Eintrag im Becken liesse — und derselbe Lauf legt ihn unmittelbar danach
   > wieder vor. Der Duplikat-Treffer ist ein Argument FUER eine Entscheidung, nicht gegen sie.
   > Wer die Entscheidung wirklich vertagen will, waehlt in Schritt 6 „Liegenlassen".
2. **Zeile in `INBOX.md` an ihrer sortierten Position einfuegen** — vor der ersten Datenzeile mit
   kleinerer Nummer (gibt es keine, ans Tabellenende): die INBOX ist absteigend sortiert (setzt
   INBOX #74 um), und befoerderte Becken-Nummern liegen wegen des gemeinsamen Nummernkreises fast
   immer unter dem INBOX-Maximum — pauschal unter der Trennzeile eingefuegt, braeche jeder
   groessere Lauf die Ordnung.
   **Nummer bleibt** — sie wird nicht neu vergeben, Session-Logs, Plaene und Archiv-Eintraege
   referenzieren sie. **Status `Offen`**, Textfeld unveraendert plus Suffix
   `(befoerdert {YYYY-MM-DD})`. Kommt der Fund aus dem Fachfrage-Rueckfall (7g), steht vor dem
   Text `Fachfrage: `.
3. **Spaltenzahl der neuen Zeile pruefen** (Feld-Hygiene): so viele Felder wie die Nachbarn,
   bare Pipes im uebernommenen Text escapen.
4. **Zuletzt:** Becken-Zeile entfernen.

> **Die Reihenfolge ist bindend, nicht kosmetisch** (dieselbe wie in 7b): Ziel schreiben, dann
> Quelle loeschen. Bricht der Lauf dazwischen ab, steht der Eintrag doppelt — und die Dublette
> sieht der Duplikat-Check des naechsten Laufs. Umgekehrt waere der Eintrag ersatzlos weg, und
> die Zusage „nie zurueckrollen" machte den Verlust endgueltig.

Meldung: `✔ #{N} befoerdert → INBOX.md`

### 7b: Verwerfen

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
   Befund-Text, Begruendung. Aus der Sammelliste ist die Begruendung
   `{Grund} — Beleg: {Beleg}` aus der Voranalyse (keine eigene Beleg-Spalte: die Datei ist
   append-only, eine neue Spalte braeche bestehende Zeilen in Bestandsprojekten). Bare Pipes
   escapen, Spaltenzahl gegen die Nachbarn pruefen.
3. **Zuletzt:** Becken-Zeile entfernen.

Meldung: `✔ #{N} verworfen → archive/INBOX-BEFUNDE-verworfen.md`

### 7c: Liegenlassen

Sichtung-Spalte auf `L1 {heutiges Datum}` setzen, sonst nichts aendern.

Meldung: `↷ #{N} liegengelassen — naechster Lauf erzwingt die Entscheidung`

### 7d: Buendel

1. **Traeger befoerdern** — 7a Punkte 1–3, Textfeld zusaetzlich mit Suffix
   `(enthaelt #{a}, #{b}, …)`. Fuehrt der Duplikat-Check den Traeger nach Schritt 6, wird das
   ganze Buendel aufgeloest: alle Glieder gehen einzeln nach Schritt 6, hier wird nichts weiter
   geschrieben.
2. **Je Glied:** Archiv-Eintrag mit Begruendung `gebuendelt in #{T}`, danach die Becken-Zeile
   dieses Glieds entfernen (Ziel vor Quelle je Glied).
3. **Zuletzt:** Becken-Zeile entfernen.

Meldung: `✔ #{T} befoerdert → INBOX.md (Buendel mit #{a}, #{b}, …)`

### 7e: Nachtrag

1. **Ziel pruefen:** Die Ziel-Idee #{Z} steht in `INBOX.md` mit Status `Offen` oder `In Arbeit`.
   Sonst (fehlt, `Verworfen`, `Ausgearbeitet`) → nichts schreiben, der Fund geht als Einzelfall
   nach Schritt 6 (`Nachtrag-Ziel #{Z} nicht offen`).
2. **Ziel-Idee ergaenzen** (Muster `dtb:idea-review` „Zusammenlegen"): an das Ende ihres
   Textfelds ` **Nachtrag {YYYY-MM-DD} aus Befund #{N}:** {Befund-Text}` anhaengen; bare Pipes
   escapen, Spaltenzahl der Zeile pruefen. Status der Ziel-Idee bleibt unveraendert.
3. **Archiv-Eintrag** mit Begruendung `nachgetragen in #{Z}`.
4. **Zuletzt:** Becken-Zeile entfernen.

Meldung: `✔ #{N} nachgetragen → INBOX.md #{Z}`

### 7f: Lektion

> **Kopplungs-Hinweis:** Feld-Ableitung und Schreibmechanik stehen in `dtb:lesson`, nicht hier
> (per Referenz — eine zweite Fassung wuerde auseinanderlaufen). Der Struktur-Check in 4a
> prueft die Anker vor der ersten Nutzung.

1. **Felder ableiten** nach `## Schritt 2: In 4 Felder strukturieren` in `dtb:lesson` — OHNE
   dessen Bestaetigungsfrage (die Sammelliste bzw. die Einzelentscheidung ist die Bestaetigung)
   und ohne Applies-to-Rueckfrage (nicht ableitbar → `alle`). Herkunfts-Marker ans Ende von
   `Context`: `(via Triage {YYYY-MM-DD}, Befund #{N})`.
2. **Schreiben** nach `## Schritt 4: Append-only speichern` in `dtb:lesson`.
3. **Archiv-Eintrag** mit Begruendung `als Lektion L{N} erfasst`.
4. **Zuletzt:** Becken-Zeile entfernen.

Meldung: `✔ #{N} als Lektion L{N} → lessons.md`

### 7g: Fachfrage

> **Kopplungs-Hinweis:** Ziel-Datei, Zeilenform, Duplikat-Pruefung und Platzierung stehen in
> `dtb:open-question`, nicht hier (per Referenz). Der Struktur-Check in 4a prueft die Anker.

1. **Ziel:** der Slug aus dem Vorschlag. Slug `—`, Ordner fehlt, liegt unter `archive/` oder
   traegt weder `spec.md` noch `discovery.md` → **Rueckfall:** Fund wird nach 7a befoerdert mit
   Vorsatz `Fachfrage: ` (7a endet mit seiner eigenen Becken-Entfernung; hier nichts weiter).
2. **Ziel-Datei** nach `## Schritt 3: Ziel-Datei waehlen`, **Zeile bilden und exakt pruefen**
   nach `## Schritt 4: Zeile formatieren, Duplikat pruefen, Ziel bestaetigen` (Punkte 1–2; die
   Ziel-Bestaetigung in Punkt 3 entfaellt — die Sammelliste bzw. Einzelentscheidung zeigte das
   Ziel). Steht die Frage schon offen da → nichts schreiben, Archiv-Eintrag mit Begruendung
   `Fachfrage steht schon in features/{slug}/{datei}`, dann weiter mit Punkt 5.
3. **Schreiben** nach `## Schritt 5: Schreiben + Abschluss` (Punkte 1–4; statt der dortigen
   Abschlussmeldung die Meldung unten).
4. **Archiv-Eintrag** mit Begruendung `als Fachfrage in features/{slug}/{datei} erfasst`.
5. **Zuletzt:** Becken-Zeile entfernen.

Meldung: `✔ #{N} als Fachfrage → features/{slug}/{datei}`

---

## Schritt 8: Abschluss-Bilanz

Nach dem letzten Fund aus Schritt 6 — oder nach einem Abbruch durch den Nutzer:

```
Becken-Triage abgeschlossen:

  Befoerdert:      {N}  (davon {B} Buendel-Traeger, {F} als „Fachfrage:")
  Gebuendelt:      {G}  (archiviert „gebuendelt in #…")
  Nachgetragen:    {N}
  Lektionen:       {N}
  Fachfragen:      {N}
  Verworfen:       {N}
  Liegengelassen:  {N}
  Zurueckgestellt: {R}  (Kappung einzeln_pro_lauf → naechster Lauf)

Im Becken verbleibend: {N} ungesichtet ({M} davon Altbestand)
```

Zeilen mit `0` entfallen — die Bilanz zeigt nur, was passiert ist.

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

- **Nie das ganze Becken einzeln vorlegen:** Die Voranalyse liest alles, aber einzeln vorgelegt
  werden hoechstens `einzeln_pro_lauf` Faelle, die der Lauf selbst erzeugt (4e) — ausgenommen nur,
  was der Mensch bewusst herausnimmt (gestrichen, „Einzeln durchgehen"). Ein Lauf, der 150
  Einzelentscheidungen verlangt, wird nie zu Ende gefuehrt
- **Sofort schreiben, nie sammeln:** Jede Entscheidung geht einzeln in die Datei (INBOX #71).
  Die Sammelliste ist eine Bestaetigung, kein Sammel-Schreiben — nach ihr wird Zeile fuer Zeile
  geschrieben
- **Die Voranalyse entscheidet nichts** — sie schlaegt vor, mit Beleg. Agenten lesen nur; das
  Alterungs-Indiz ist ein Indiz, kein Urteil
- **Ein Becken-Eintrag wird nie gearbeitet:** kein Worker greift ihn, kein `feature-fast` laedt
  ihn, er steht in keiner Arbeits-Ansicht. Er verlaesst das Becken nur nach Bestaetigung —
  befoerdert, gebuendelt, nachgetragen, als Lektion oder Fach-Frage erfasst, oder verworfen
- **Deutsch:** Alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:workflow-checkpoint` — schreibt die Verlustfunde ins Becken (Vorgaenger)
- `/dtb:idea-review` — sichtet die Haupt-INBOX; Ziel der Befoerderung (Nachfolger)
- `/dtb:idea` — Erfassung durch den Menschen, schreibt immer nach `INBOX.md`
- `/dtb:lesson`, `/dtb:open-question` — Ausgaenge fuer Lektionen und Fach-Fragen (per Referenz, 7f/7g)

---

**Erstellt mit:** Kit-Feature `ideen-becken` (INBOX #76); Vorsortierung: `triage-vorsortierung` (INBOX #137)
