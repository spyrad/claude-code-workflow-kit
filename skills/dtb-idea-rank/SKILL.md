---
name: dtb:idea-rank
description: >-
  Use when: "Ideen priorisieren", "Rangliste der Ideen", "Aufwand Nutzen",
  "was lohnt sich zuerst", "welche Idee zuerst", "idea rank". Read-only
  ranking of all open ideas in INBOX.md as one table sorted by importance —
  columns number, short title, effort as a time range, importance (six levels,
  four colors) and a one-sentence remark carrying blockers and dependencies.
  Changes nothing. Not for the machine basin INBOX-BEFUNDE.md (that is dtb:idea-triage)
  and not for per-idea decisions (that is dtb:idea-review).
disable-model-invocation: false
argument-hint: "[Ideen-Nummern, z.B. 27 33 45]"
allowed-tools: Read, Glob, Grep
pipeline:
  stage: idea
  after: null
  next: [dtb:idea-review]
  consumes: [INBOX.md, BACKLOG.md, features/*/spec.md, features/*/plan.md, features/*/task.md, features/*/bug.md, project-rules/DERIVED_STATE_RULES.md, workflow.config.yaml]
  produces: []
---

# DTB Idea-Rank

Zeigt alle offenen Ideen der Inbox als **eine Tabelle**, sortiert nach Wichtigkeit — je Idee
Aufwand als Zeitspanne, Wichtigkeit und eine Bemerkung mit Blockern und Abhaengigkeiten. Die
Zeilen-Reihenfolge ist die Empfehlung. Rein lesend, als Chat-Report.

**Warum es diesen Skill gibt:** Dieselbe Sicht wurde mehrfach von Hand gebaut — am
2026-07-30 wurde ein angesetztes `dtb:idea-review` dreimal in genau diese Priorisierung
umgelenkt, am 2026-08-08 lief sie erneut ueber 26 Ideen. Das Muster ist formalisiert,
damit jeder Lauf nach denselben Regeln einsortiert. Die Ausgabe ist seit 2026-09-17 eine
Tabelle statt vier Toepfen — die Topf-Form verteilte die Einschaetzung auf drei Bloecke und
half bei der Entscheidung „was zuerst" nicht (Abnahme-Lauf 2026-09-17).

**Abgrenzung (nicht verwechseln):**

| Skill | Gegenstand | Wirkung |
|-------|-----------|---------|
| `dtb:idea-rank` (dieser) | `INBOX.md`, Status `Offen` | liest nur — Rangliste, keine Entscheidung |
| `dtb:idea-review` | `INBOX.md`, Status `Offen` | schreibt — Entscheidung je Idee (Status, Links) |
| `dtb:idea-triage` | `INBOX-BEFUNDE.md` (Befund-Becken) | schreibt — befoerdern, verwerfen, liegenlassen |

Die Rangliste ist eine **optionale Vorstufe** von `dtb:idea-review`: Sie ordnet, der Review
entscheidet. Der Review uebernimmt die Reihenfolge nicht automatisch.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Inbox laden

Lies `{config.paths.workflows}/INBOX.md`.

- **Datei fehlt** →
  ```
  Keine Inbox vorhanden — nichts zu ranken. Ideen erfassen mit /dtb:idea
  ```
  Ende. Eine vorhandene Datei **ohne Datenzeile** laeuft normal weiter: Schritt 2 meldet
  genannte Nummern als nicht vorhanden und endet dann in „nichts zu ranken".
- **Kandidaten:** alle Eintraege mit Status `Offen`. „Offen" ist genau dieser Status-Wert
  der Inbox — keine eigene Auslegung (weder `In Arbeit` noch `Ausgearbeitet` zaehlen).
  Ob Kandidaten uebrig bleiben, prueft erst Schritt 2 — nach der Argument-Auswertung.
- **Eintraege mit Status `In Arbeit`** merken — sie werden nicht gerankt, dienen aber als
  Blocker-Kontext (Schritt 4).

**Das Befund-Becken `INBOX-BEFUNDE.md` wird NICHT gelesen.** Becken-Eintraege sind bis zu
ihrer Befoerderung fuer keine Arbeitssicht sichtbar (`DERIVED_STATE_RULES.md` §6.4). Weil das
Becken ungelesen bleibt, ist eine Becken-Nummer im Idee-Text nicht von einer archivierten
Idee unterscheidbar — beide behandelt Schritt 4.2 als **Verweis ausserhalb der Inbox**.

## Schritt 2: Argument auswerten

| Argument | Umfang |
|----------|--------|
| _(leer)_ | alle `Offen`-Ideen |
| Nummern (`27 33 45`, auch `#27, #33`) | nur diese Ideen |

Je Nummer des Arguments, die nicht zu einer `Offen`-Idee gehoert, eine Hinweiszeile vor dem
Report — der Rest wird normal gerankt:

- existiert nicht → `⚠ #{N} nicht in der Inbox — uebersprungen`
- anderer Status → `⚠ #{N} hat Status "{Status}" — nur "Offen" wird gerankt`

**Nichts zu ranken** (mit oder ohne Argument bleibt keine `Offen`-Idee im Umfang) → die
⚠-Hinweiszeilen (falls vorhanden), dann:
```
Keine offenen Ideen im Umfang — nichts zu ranken.
Geprueft: {config.paths.workflows}/INBOX.md (Status "Offen"{, Teilmenge: #a, #b})
```
Ende. Die Reihenfolge ist Absicht: Wer Nummern nennt, erfaehrt auch bei leerem Ergebnis,
warum sie nicht gerankt werden.

Bei einer Teilmenge werden Abhaengigkeiten zu Ideen **ausserhalb** der Teilmenge trotzdem
genannt (mit Nummer), nur nicht selbst gerankt. Eine `Offen`-Vorbedingung ausserhalb der
Teilmenge zaehlt als nicht erfuellt (4.2), weil ihre Arbeitsbereitschaft in diesem Lauf nicht
geprueft wird — ein Lauf ohne Argument kann dieselbe Idee deshalb ohne `Blockiert:` zeigen.
Das ist Absicht, kein Widerspruch.

## Schritt 3: Querbelege lesen

Lies read-only, um Blocker und Ueberschneidungen zu erkennen:

- `{config.paths.rules}/DERIVED_STATE_RULES.md` §1 (Fallback:
  `dtb-project/project-rules/DERIVED_STATE_RULES.md`) — der Status eines Change wird nach
  diesen Regeln abgeleitet, nie selbst definiert. Fehlt die Datei → Hinweiszeile
  `⚠ DERIVED_STATE_RULES.md nicht gefunden — Change-Status aus plan.md/spec.md grob abgeleitet`
- `{config.paths.workflows}/features/*/spec.md`, `plan.md`, `task.md` und `bug.md` — laufende
  Changes (Ziel, Scope, abgeleiteter Status nach §1; Aufgaben und Bugs nach §1.5 —
  hat ein Ordner auch `plan.md`, gilt die plan-basierte Ableitung)
- `{config.paths.workflows}/BACKLOG.md` — geplante Features und Aufgaben

`archive/` und das Changelog werden nicht gelesen: Belege aus frueheren Sessions stehen in
der Praxis bereits im Idee-Text, und der Lauf soll schnell bleiben.

**Fakt vs. Vermutung:** Was im Idee-Text oder einem Querbeleg steht, ist Fakt. Was du nur
schliesst (z.B. „ueberschneidet sich vermutlich mit Feature X"), kennzeichnest du in der
Bemerkung mit `(Vermutung)`.

## Schritt 4: Bewerten

### 4.1 Teil-Routing beachten

Traegt eine `Offen`-Idee einen Vermerk, dass ein Teil bereits geroutet ist (Task-/Feature-Link
zu einem Teilaspekt), bewerte **nur den ungerouteten Rest** und markiere die Zeile mit
`(Rest nach Teil-Routing)`.

### 4.2 Abhaengigkeiten erkennen

Eine Abhaengigkeit ist ein gerichtetes Paar `#A vor #B` mit Grund. Quellen:

- **ausdruecklich im Text** — Nennung einer anderen Nummer mit Reihenfolge-Aussage („nach",
  „setzt voraus", „blockiert", „erst wenn") → `zwingend`
- **Querbeleg** — die Idee aendert, was ein laufender Change gerade baut, oder braucht
  dessen Ergebnis → `zwingend`, wenn der Text es sagt; sonst `sinnvoll (Vermutung)`
- **inhaltlich geschlossen** — zwei Ideen beruehren dieselbe Stelle, eine sollte zuerst
  → `sinnvoll (Vermutung)`
- **externe Voraussetzung, ausdruecklich im Text** (Release, Entscheidung, Werkzeug) →
  `zwingend`, nicht erfuellt, bis Text oder Querbeleg das Gegenteil zeigen

**Vorbedingung → Wirkung** (Change-Status nach `DERIVED_STATE_RULES.md` §1, Aufgaben/Bugs §1.5):

| Vorbedingung | Wirkung |
|--------------|---------|
| Change unter `features/` (Ordner existiert, gleich mit welcher der vier Dateien), Status `Fertig zum Testen`, `Erledigt`, `Behoben` oder `Abgenommen` | erfuellt — kein Blocker |
| Change unter `features/`, jeder andere Status | nicht erfuellt (blockiert nur bei `zwingend` → `Blockiert: …` in der Bemerkung, 4.3) |
| Inbox-Idee `Offen`, im selben Lauf gerankt | **Reihenfolge-Kante** — Wirkung in 4.4 (zwingende Kanten) |
| Inbox-Idee `Offen` ausserhalb der Teilmenge, oder `In Arbeit` | nicht erfuellt (blockiert nur bei `zwingend` → `Blockiert: …` in der Bemerkung, 4.3) |
| Inbox-Idee `Ausgearbeitet` mit Change-Link (`→ features/{slug}/…`) | wie der verlinkte Change (Zeilen 1-2) |
| Inbox-Idee `Verworfen` | kein Blocker; `↪ Vorbedingung verworfen — Abhaengigkeit pruefen` |
| **nicht pruefbar** — Nummer steht nicht in `INBOX.md` · Change nicht unter `features/` · `Ausgearbeitet` ohne Change-Link · unbekannter Status | kein Blocker, keine Abhaengigkeit, Nummer **nicht** in den Report; `↪ {Grund} — Reihenfolge nicht pruefbar` mit {Grund} aus: `Verweis ausserhalb der Inbox` · `Verweis ausserhalb der laufenden Changes` · `Vorbedingung ausgearbeitet, Change nicht verlinkt` · `Vorbedingung mit unbekanntem Status` |

Warum `Ausgearbeitet` nicht pauschal erfuellt: der Status heisst „Change angelegt", nicht
„umgesetzt" — `dtb:idea-review` setzt ihn in der Task-Lane sogar vor `/dtb:task`.

Warum eine Nummer ausserhalb der Inbox nicht pruefbar ist: sie kann eine archivierte Idee oder
ein Becken-Eintrag sein — ohne das Becken zu lesen, ist das nicht entscheidbar, und ein
Becken-Eintrag darf in keiner Arbeitssicht erscheinen (§6.4). Ebenso unterscheidet der Skill
ohne `archive/` nicht zwischen archiviertem und nicht existentem Change.

### 4.3 Aufwand und Wichtigkeit je Idee

Jede Idee bekommt genau einen Aufwand-Wert und genau eine Wichtigkeit-Stufe. Beide fliessen
direkt in die Tabelle (Schritt 5), die Begruendung in die Spalte „Bemerkung".

**Aufwand** — Probe: „Was muesste man tun, um die Idee abzuschliessen?" Angabe immer als
**Zeitspanne, nie als Einzelzahl** — die Spanne haelt die Schaetz-Unschaerfe sichtbar
(einzige Ausnahme: die kleinste Stufe `~1 h`).

| Spanne | Merkmal |
|--------|---------|
| `~1 h` | rein mechanisch, eine Datei, Fix-Muster bekannt |
| `1–2 h` | eine Session, wenige Dateien, kein neues Konzept |
| `2–4 h` | eine Session, mehrere Dateien oder ein kleiner Nachweis/Probelauf |
| `0,5–1 Tag` | eigener kleiner Change (Fast-Track), Design-Fragen benannt und eingrenzbar |
| `1–2 Tage` | eigener Change mit Plan, bis zwei Phasen |
| `3+ Tage` | mehrere Phasen oder Changes, kit-weite Querwirkung, oder die Idee ist selbst noch eine offene Grundsatzfrage („pruefen, ob …", „wo passt …") |

Optional ein kurzer Zusatz, wenn der Aufwand an etwas haengt: `2–4 h nach Input`,
`15 Min Frage + 0,5–1 Tag Fix`, `1–2 Tage + Discovery`.

**Wichtigkeit** — Probe: „Was geht verloren, wenn die Idee nie umgesetzt wird?"

| Stufe | Merkmal |
|-------|---------|
| 🔴 `sehr hoch` | blockiert laufende Arbeit (Abnahme/Umsetzung eines Change unter `features/`) oder erzeugt jetzt falsche Ergebnisse — Beleg im Text oder Querbeleg |
| 🔴 `hoch` | beseitigt einen belegt wiederkehrenden Schmerz oder eine Fehlerklasse (Beleg im Text: Datum, Anzahl, Session), oder ist ueber eine **zwingende** Abhaengigkeit aus 4.2 Vorbedingung anderer Ideen (eine `sinnvoll (Vermutung)`-Kante zaehlt nicht) |
| 🟠 `mittel-hoch` | spuerbare Verbesserung eines regelmaessig genutzten Ablaufs mit **einem** Beleg (einmal aufgetreten, nicht wiederkehrend) |
| 🟡 `mittel` | spuerbare Verbesserung eines regelmaessig genutzten Ablaufs, ohne Beleg |
| 🟢 `niedrig-mittel` | konkreter, aber kleiner Gewinn — z.B. Aufraeumen, Nachdokumentation, Verlustschutz fuer einen seltenen Fall |
| 🟢 `niedrig` | wuenschenswert, aber kein belegter Bedarf; Erkundung ohne konkreten Anlass; Workaround existiert und reicht |

Die Farbe gehoert fest zur Stufe und steht immer davor (`🟠 mittel-hoch`).

Grenzfall zwischen zwei Stufen → die **niedrigere** Wichtigkeit bzw. die **groessere**
Aufwand-Spanne waehlen. Die Tabelle soll eher zu vorsichtig empfehlen als eine Idee
hochzureden.

**Blocker aendern die Wichtigkeit nicht.** Eine Idee mit zwingendem, nicht erfuelltem Blocker
nach 4.2 (jede **zwingende** Kante auf eine Zeile mit Wirkung `nicht erfuellt` aus der Tabelle
„Vorbedingung → Wirkung", dazu externe Voraussetzungen) behaelt ihre Stufe; der Blocker steht
am Anfang ihrer Bemerkung (`Blockiert: …`, Schritt 5). So bleibt sichtbar, dass eine wichtige
Idee wartet.

### 4.4 Sortierung (feste Reihenfolge der Schluessel)

Jede Idee ist genau **eine** Tabellenzeile. Die Zeilen-Reihenfolge ist die Empfehlung — es gibt
keine getrennte Reihenfolge-Liste. Sortiert wird so:

1. Wichtigkeit absteigend (`sehr hoch` → `hoch` → `mittel-hoch` → `mittel` → `niedrig-mittel` → `niedrig`)
2. bei gleicher Wichtigkeit: kleinere Aufwand-Spanne zuerst (Reihenfolge der Tabelle in 4.3;
   ein Zusatz wie `nach Input` aendert die Spanne nicht)
3. bei gleichem Aufwand: aeltere Idee zuerst (Datum, bei gleichem Datum die niedrigere Nummer)

**Zwingende Kanten** `#A vor #B`, bei denen **beide** Ideen in der Tabelle stehen, werden danach
eingehalten: steht `#A` unter `#B`, rueckt `#A` direkt vor `#B` (ihre Wichtigkeit bleibt; die
Bemerkung von `#A` nennt `Vorbedingung fuer #B`). Ketten (`#A vor #B vor #C`) wiederholen den
Schritt, bis sich nichts mehr aendert. `sinnvoll`-Kanten verschieben keine Zeile — sie stehen
nur in der Bemerkung.

**Zyklus** (`#A vor #B` und `#B vor #A`, auch ueber Ketten): zuerst die `sinnvoll`-Kanten des
Zyklus verwerfen. Bleibt ein Zyklus aus zwingenden Kanten, gilt fuer die beteiligten Ideen nur
die Sortierung aus 1–3, und ihre Bemerkungen tragen
`⚠ Zyklus mit #A — Reihenfolge widerspruechlich, im Review klaeren`.

## Schritt 5: Ausgeben

Keine Rueckfragen — sofort ausgeben. **Eine** Tabelle, sortiert nach 4.4; jede Idee im Umfang
ist genau eine Zeile.

```
# Ideen-Rangliste

**Stand:** {YYYY-MM-DD} · {N} offene Ideen bewertet{ (Teilmenge: #a, #b)}
{⚠-Hinweiszeilen aus Schritt 2, falls vorhanden}

| # | Idee (kurz) | Aufwand | Wichtigkeit | Bemerkung |
|---|---|---|---|---|
| {N} | {Kurztitel} | {Spanne} | {Farbe} {Stufe} | {Bemerkung} |

Momentaufnahme — INBOX.md unveraendert. Entscheidungen je Idee: /dtb:idea-review
```

**Spalten:**

- **#** — Inbox-Nummer ohne `#`
- **Idee (kurz)** — eigene Kurzfassung, hoechstens ~6 Woerter, sinngemaess aus dem Idee-Text
  verdichtet (Kern der Idee, keine neue Aussage; Skill-/Dateinamen in Backticks). Der volle
  Text bleibt ueber die Nummer in `INBOX.md` erreichbar. Bei Teil-Routing (4.1) mit
  Zusatz `(Rest)`
- **Aufwand** — Spanne aus 4.3, ggf. mit Zusatz
- **Wichtigkeit** — Farbe + Stufe aus 4.3 (`🔴 hoch`)
- **Bemerkung** — **ein** Satz, der die Einstufung begruendet und zeigt, was man vor dem
  Anfangen wissen muss. Teile in dieser Reihenfolge, mit `;` verbunden:
  1. Blocker, falls vorhanden: `Blockiert: {#A (Status) | Change {slug} | externe Voraussetzung}`
  2. Grund der Wichtigkeit (Beleg aus Text/Querbeleg, Vermutungen mit `(Vermutung)`)
  3. Reihenfolge, falls vorhanden: `Vorbedingung fuer #B` · `Sinnvoll erst nach #A (Vermutung)`
     · `⚠ Zyklus mit #A — Reihenfolge widerspruechlich, im Review klaeren`
  4. Hinweise aus 4.2 im Wortlaut der Tabelle „Vorbedingung → Wirkung" ohne `↪`
     (z.B. `Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar`); eine nicht
     pruefbare Nummer wird dabei nie genannt

Keine Zeilen unter der Tabelle ausser der Fusszeile — keine Topf-, Abhaengigkeits- oder
Reihenfolge-Abschnitte. `|` im Zellentext als `/` schreiben, damit die Tabelle nicht bricht.

## Wichtig

- **Rein lesend:** Dieser Skill aendert keine Datei — kein Statuswechsel, kein Link, kein
  Vermerk in der Inbox. Entscheidungen trifft `/dtb:idea-review`
- **Kein zweiter Speicherort:** Die Rangliste ist ein Chat-Report, keine Datei. Sie veraltet
  mit jeder neuen Idee; jeder Aufruf bewertet frisch und schreibt keine fruehere Rangliste fort
- **Becken bleibt draussen:** `INBOX-BEFUNDE.md` wird nicht gelesen (§6.4)
- **Jede Idee genau eine Zeile:** Stufen und Sortierung folgen den Tabellen in 4.3/4.4,
  nicht dem Gesamteindruck
- **Laeuft ueberall:** auch in einem verlinkten Worktree unveraendert (Read-only-Sicht) —
  der Lesestand kann dort aelter sein als im Haupt-Checkout
- **Deutsch:** alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:idea-review` — entscheidet je Idee (Nachfolger dieser Sicht)
- `/dtb:idea` — erfasst eine neue Idee
- `/dtb:idea-triage` — sichtet das Befund-Becken `INBOX-BEFUNDE.md` (anderer Gegenstand)
- `/dtb:workflow-next` — naechster Schritt pro laufendem Change (andere Lese-Ansicht)

---

Lies jetzt die Inbox und gib die Rangliste aus.
