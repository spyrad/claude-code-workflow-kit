---
name: dtb:idea-rank
description: >-
  Use when: "Ideen priorisieren", "Rangliste der Ideen", "Aufwand Nutzen",
  "was lohnt sich zuerst", "welche Idee zuerst", "idea rank". Read-only
  ranking of all open ideas in INBOX.md as one table sorted by importance —
  columns number, short title, effort as a time range, importance (six levels,
  four colors) and a remark cell carrying blockers and dependencies.
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
zu einem Teilaspekt), bewerte **nur den ungerouteten Rest**; der Kurztitel erhaelt den Zusatz
`(Rest)` (Schritt 5).

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
| Change unter `features/`, jeder andere Status | nicht erfuellt (blockiert nur bei `zwingend` → Schritt 5, Teil 1) |
| Inbox-Idee `Offen`, im selben Lauf gerankt | **Reihenfolge-Kante** — Wirkung in 4.4 (zwingende Kanten) |
| Inbox-Idee `Offen` ausserhalb der Teilmenge, oder `In Arbeit` | nicht erfuellt (blockiert nur bei `zwingend` → Schritt 5, Teil 1) |
| Inbox-Idee `Ausgearbeitet` mit Change-Link (`→ features/{slug}/…`) | wie der verlinkte Change (Zeilen 1-2) |
| Inbox-Idee `Verworfen` | kein Blocker; `Vorbedingung #A verworfen — Abhaengigkeit pruefen` |
| **nicht pruefbar** — Nummer steht nicht in `INBOX.md` · Change nicht unter `features/` · `Ausgearbeitet` ohne Change-Link · unbekannter Status | kein Blocker, keine Abhaengigkeit, Nummer **nicht** in den Report; `{Grund} — Reihenfolge nicht pruefbar` mit {Grund} aus: `Verweis ausserhalb der Inbox` · `Verweis ausserhalb der laufenden Changes` · `Vorbedingung ausgearbeitet, Change nicht verlinkt` · `Vorbedingung mit unbekanntem Status` |

**Blocker** = jede **zwingende** Kante auf eine Zeile mit Wirkung `nicht erfuellt`, dazu externe
Voraussetzungen (ausdruecklich im Text).

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
| `0,5–1 Tag` | eigener Change, eine Phase; Design-Fragen benannt und eingrenzbar |
| `1–2 Tage` | eigener Change, zwei Phasen |
| `3+ Tage` | mehrere Phasen oder Changes, kit-weite Querwirkung |

**Offene Grundsatzfrage** („pruefen, ob …", „wo passt …", „integrieren?"): Die Idee ist mit der
Entscheidung abgeschlossen — angegeben wird der Aufwand **bis zur Entscheidung** (meist `1–2 h`
oder `2–4 h`) mit dem Zusatz `+ Umsetzung offen`. Der Umsetzungsaufwand entsteht erst, wenn die
Entscheidung „bauen" lautet, und gehoert dann zu einer neuen Idee bzw. einem Change.
Die Wichtigkeit bewertet den Gegenstand der Frage (was verloren geht, wenn nie entschieden
wird), nicht die Entscheidungsarbeit.

**Genau eine Spanne je Zelle.** Mehrteiliger Aufwand („kurze Frage + Fix") wird zu einer
Spanne zusammengefasst, im Grenzfall die groessere. Optional ein Zusatz **ohne Zeitangabe**, wenn
der Aufwand an etwas haengt: `2–4 h nach Input`, `1–2 Tage + Discovery offen`,
`1–2 h + Umsetzung offen`. Sortiert wird nur nach der Spanne (4.4).

**Wichtigkeit** — Probe: „Was geht verloren, wenn die Idee nie umgesetzt wird?"

| Stufe | Merkmal |
|-------|---------|
| 🔴 `sehr hoch` | blockiert laufende Arbeit: Abnahme oder Umsetzung eines Change unter `features/` haengt an der Idee (Beleg im Text oder Querbeleg) |
| 🔴 `hoch` | erzeugt jetzt falsche Ergebnisse, beseitigt eine Fehlerklasse oder einen Schmerz — **jeweils** belegt mit mindestens **zwei verschiedenen** Daten oder Sessions |
| 🟠 `mittel-hoch` | dasselbe mit **genau einem** Beleg, oder Verbesserung eines regelmaessig genutzten Ablaufs\* mit einem Beleg |
| 🟡 `mittel` | Verbesserung eines regelmaessig genutzten Ablaufs\*, ohne Beleg |
| 🟢 `niedrig-mittel` | konkreter, aber kleiner Gewinn — Aufraeumen, Nachdokumentation, Verlustschutz fuer einen seltenen Fall |
| 🟢 `niedrig` | kein belegter Bedarf; Erkundung ohne konkreten Anlass; Workaround existiert und reicht |

\* **Regelmaessig genutzter Ablauf** = ein Skill mit `pipeline.stage` ∈ {`idea`, `planning`,
`implementation`, `development`, `session`}; im Zielprojekt ein Ablauf, den der Idee-Text als
regelmaessig genutzt belegt. Die Bedingung gilt nur fuer `mittel-hoch` (zweite Haelfte) und
`mittel` — trifft sie nicht zu, hoechstens `niedrig-mittel`.

Die Farbe gehoert fest zur Stufe und steht immer davor (`🟠 mittel-hoch`).

Grenzfall zwischen zwei Stufen → die **niedrigere** Wichtigkeit bzw. die **groessere**
Aufwand-Spanne waehlen. Die Tabelle soll eher zu vorsichtig empfehlen als eine Idee
hochzureden.

**Abhaengigkeiten aendern die Wichtigkeit nicht** — weder ein Blocker (4.2) noch die Rolle als
Vorbedingung anderer Ideen (die Reihenfolge regelt 4.4). Eine blockierte Idee behaelt ihre Stufe;
der Blocker steht am Anfang ihrer Bemerkung (Schritt 5, Teil 1). So bleibt sichtbar, dass eine
wichtige Idee wartet.

### 4.4 Sortierung (feste Reihenfolge der Schluessel)

Jede Idee ist genau **eine** Tabellenzeile. Die Zeilen-Reihenfolge ist die Empfehlung — es gibt
keine getrennte Reihenfolge-Liste. Sortiert wird so:

1. Wichtigkeit absteigend (`sehr hoch` → `hoch` → `mittel-hoch` → `mittel` → `niedrig-mittel` → `niedrig`)
2. bei gleicher Wichtigkeit: kleinere Aufwand-Spanne zuerst (Reihenfolge der Tabelle in 4.3;
   ein Zusatz wie `nach Input` aendert die Spanne nicht)
3. bei gleichem Aufwand: aeltere Idee zuerst (Datum, bei gleichem Datum die niedrigere Nummer)

**Zwingende Kanten** `#A vor #B` (beide Ideen in der Tabelle) werden eingehalten, indem die
Tabelle **Zeile fuer Zeile aufgebaut** wird:

0. **Zyklen zuerst:** Liegen zwingende Kanten in einem Zyklus (`#A vor #B vor … vor #A`), gelten
   sie fuer den Aufbau als nicht zwingend. **Jede** beteiligte Idee traegt in ihrer Bemerkung
   `⚠ Zyklus mit #X, #Y — Reihenfolge widerspruechlich, im Review klaeren`
   (X, Y = die anderen Beteiligten)
1. Naechste Zeile = die oberste noch nicht gesetzte Idee nach den Schluesseln 1–3, deren
   zwingende Vorgaenger **unter den Tabellen-Ideen** alle schon gesetzt sind (Vorgaenger
   ausserhalb der Tabelle sind Blocker, 4.2 — sie halten den Aufbau nicht auf)
2. Wiederholen, bis alle Ideen stehen — nach Schritt 0 bleibt der Aufbau nie haengen

Ohne Kanten ergibt das genau die Sortierung 1–3; Ketten und mehrere Vorgaenger derselben Idee
brauchen keine Sonderregel. Die Wichtigkeit einer Idee aendert sich dabei nie.
`sinnvoll`-Kanten verschieben keine Zeile — sie stehen nur in der Bemerkung (Schritt 5).

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
- **Bemerkung** — **eine** Zelle, die die Einstufung begruendet und zeigt, was man vor dem
  Anfangen wissen muss. Teile in dieser Reihenfolge, getrennt mit `; ` (innerhalb eines Teils
  kein `;`), leere Teile entfallen:
  1. Blocker, falls vorhanden: `Blockiert: {Liste, getrennt mit ", "}` — je Eintrag `#A (Status)` /
     `Change {slug} (Status)` / `{externe Voraussetzung}`, z.B.
     `Blockiert: #12 (In Arbeit), Change foo (In Arbeit)`
  2. Grund der Wichtigkeit (Beleg aus Text/Querbeleg, Vermutungen mit `(Vermutung)`)
  3. Reihenfolge — fuer **jede** Kante `#A vor #B` zwischen zwei Tabellenzeilen, auf **beiden**
     Seiten, unabhaengig davon, ob eine Zeile verschoben wurde:

     | Kante | bei `#A` | bei `#B` |
     |-------|----------|----------|
     | zwingend | `Vorbedingung fuer #B` | `Erst nach #A` |
     | sinnvoll (Vermutung) | `Vorbedingung fuer #B (Vermutung)` | `Sinnvoll erst nach #A (Vermutung)` |

     dazu bei Zyklus-Beteiligten der Vermerk aus 4.4 (`⚠ Zyklus mit #X, #Y — …`).

     **Ziel ausserhalb der Tabelle** (laufender Change, Idee ausserhalb der Teilmenge):

     | Fall | Bemerkung |
     |------|-----------|
     | zwingend, Vorbedingung ausserhalb, nicht erfuellt (4.2) | Blocker in Teil 1 |
     | sinnvoll, Vorbedingung ausserhalb | `Sinnvoll erst nach {#A / Change {slug}} (Vermutung)` |
     | Idee dieser Zeile ist Vorbedingung einer Idee ausserhalb | `Vorbedingung fuer #B`, bei sinnvoll mit `(Vermutung)` |

     Eine erfuellte Vorbedingung (4.2) erzeugt keinen Text
  4. Hinweise aus 4.2 im Wortlaut der Tabelle „Vorbedingung → Wirkung"
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
