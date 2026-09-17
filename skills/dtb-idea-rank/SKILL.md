---
name: dtb:idea-rank
description: >-
  Use when: "Ideen priorisieren", "Rangliste der Ideen", "Aufwand Nutzen",
  "was lohnt sich zuerst", "Quick Wins in der Inbox", "idea rank". Read-only
  ranking of all open ideas in INBOX.md: sorts each into one of four pots
  (Quick Wins / strategisch wertvoll / wartend/blockiert / braucht eigenen Fokus)
  with effort and value, lists dependencies and recommends an order. Changes
  nothing. Not for the machine basin INBOX-BEFUNDE.md (that is dtb:idea-triage)
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

Ordnet alle offenen Ideen der Inbox nach Aufwand und Nutzen in vier Toepfe und empfiehlt
eine Bearbeitungs-Reihenfolge — rein lesend, als Chat-Report.

**Warum es diesen Skill gibt:** Dieselbe Sicht wurde mehrfach von Hand gebaut — am
2026-07-30 wurde ein angesetztes `dtb:idea-review` dreimal in genau diese Priorisierung
umgelenkt, am 2026-08-08 lief sie erneut ueber 26 Ideen. Das Muster ist formalisiert,
damit jeder Lauf nach denselben Regeln einsortiert.

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
geprueft wird — ein Lauf ohne Argument kann dieselbe Idee deshalb in einem Arbeits-Topf zeigen.
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
Begruendung mit `(Vermutung)`.

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
| Change unter `features/`, jeder andere Status | nicht erfuellt (blockiert nur bei `zwingend`, Regel 1 in 4.4) |
| Inbox-Idee `Offen`, im selben Lauf gerankt | **Reihenfolge-Kante** — Wirkung in 4.4 (Durchgang 2) |
| Inbox-Idee `Offen` ausserhalb der Teilmenge, oder `In Arbeit` | nicht erfuellt (blockiert nur bei `zwingend`, Regel 1 in 4.4) |
| Inbox-Idee `Ausgearbeitet` mit Change-Link (`→ features/{slug}/…`) | wie der verlinkte Change (Zeilen 1-2) |
| Inbox-Idee `Verworfen` | kein Blocker; `↪ Vorbedingung verworfen — Abhaengigkeit pruefen` |
| **nicht pruefbar** — Nummer steht nicht in `INBOX.md` · Change nicht unter `features/` · `Ausgearbeitet` ohne Change-Link · unbekannter Status | kein Blocker, keine Abhaengigkeit, Nummer **nicht** in den Report; `↪ {Grund} — Reihenfolge nicht pruefbar` mit {Grund} aus: `Verweis ausserhalb der Inbox` · `Verweis ausserhalb der laufenden Changes` · `Vorbedingung ausgearbeitet, Change nicht verlinkt` · `Vorbedingung mit unbekanntem Status` |

Warum `Ausgearbeitet` nicht pauschal erfuellt: der Status heisst „Change angelegt", nicht
„umgesetzt" — `dtb:idea-review` setzt ihn in der Task-Lane sogar vor `/dtb:task`.

Warum eine Nummer ausserhalb der Inbox nicht pruefbar ist: sie kann eine archivierte Idee oder
ein Becken-Eintrag sein — ohne das Becken zu lesen, ist das nicht entscheidbar, und ein
Becken-Eintrag darf in keiner Arbeitssicht erscheinen (§6.4). Ebenso unterscheidet der Skill
ohne `archive/` nicht zwischen archiviertem und nicht existentem Change.

### 4.3 Stufen je Idee

Jede Idee bekommt genau eine Aufwand- und eine Nutzen-Stufe mit 1-Satz-Begruendung. Grobe
Stufen, keine Zahlen oder Prozentwerte — eine Zahl suggeriert eine Messbarkeit, die kein Lauf
einloest.

**Aufwand** — Probe: „Was muesste man tun, um die Idee abzuschliessen?"

| Stufe | Merkmal |
|-------|---------|
| `klein` | in einer Session erledigt; eine bis wenige Dateien, kein neues Konzept, keine offene Design-Frage |
| `mittel` | eigener Change mit Plan (Fast-Track oder Voll-Schiene), hoechstens zwei Phasen; Design-Fragen sind benannt und eingrenzbar |
| `gross` | mehrere Phasen oder Changes, kit-weite Querwirkung, oder die Idee selbst ist noch eine offene Grundsatzfrage („pruefen, ob …", „wo passt …") |

**Nutzen** — Probe: „Was geht verloren, wenn die Idee nie umgesetzt wird?"

| Stufe | Merkmal |
|-------|---------|
| `hoch` | beseitigt einen belegt wiederkehrenden Schmerz oder eine Fehlerklasse (Beleg im Text: Datum, Anzahl, Session), oder ist ueber eine **zwingende** Abhaengigkeit aus 4.2 Vorbedingung anderer Ideen (eine `sinnvoll (Vermutung)`-Kante zaehlt nicht) |
| `mittel` | spuerbare Verbesserung eines regelmaessig genutzten Ablaufs, ohne belegte Wiederholung |
| `niedrig` | wuenschenswert, aber kein belegter Bedarf; Erkundung ohne konkreten Anlass |

Grenzfall zwischen zwei Stufen → die **niedrigere** Nutzen- bzw. die **hoehere**
Aufwand-Stufe waehlen. Die Rangliste soll eher zu vorsichtig empfehlen als eine Idee zum
Quick Win hochzureden.

### 4.4 Topf-Zuordnung (feste Reihenfolge, erster Treffer gilt)

Jede Idee landet in **genau einem** Topf. Die Zuordnung laeuft in zwei Durchgaengen.

**Durchgang 1** — pruefe je Idee die Regeln in dieser Reihenfolge (Reihenfolge-Kanten aus 4.2
bleiben hier unberuecksichtigt):

| # | Bedingung | Topf |
|---|-----------|------|
| 1 | Mindestens ein **zwingender**, nicht erfuellter Blocker nach 4.2 (jede **zwingende** Kante auf eine Zeile mit Wirkung `nicht erfuellt` aus der Tabelle „Vorbedingung → Wirkung" in 4.2, dazu externe Voraussetzungen) | **wartend/blockiert** |
| 2 | Nutzen `niedrig` | **wartend/blockiert** — Vorbedingung „Anlass/Bedarf" |
| 3 | Aufwand `gross` | **braucht eigenen Fokus** |
| 4 | Aufwand `klein` | **Quick Wins** |
| 5 | Aufwand `mittel` | **strategisch wertvoll** |

Warum diese Reihenfolge: Ein Blocker macht jede andere Einstufung gegenstandslos (Regel 1).
Eine Idee ohne belegten Bedarf lohnt auch bei kleinem Aufwand nicht vorab — sie wartet auf
einen Anlass (Regel 2; Praxis 2026-07-30: „#25/#18 warten auf Anlass"). Grosser Aufwand ist
nie nebenbei zu haben, auch bei hohem Nutzen (Regel 3). Erst danach entscheidet der Aufwand
allein zwischen den beiden Arbeits-Toepfen (Regeln 4/5).

**Durchgang 2** — zwingende Reihenfolge-Kanten `#A vor #B` zwischen zwei gerankten Ideen:

| Topf von `#A` nach Durchgang 1 | Wirkung auf `#B` |
|--------------------------------|------------------|
| ein Arbeits-Topf (Quick Wins, strategisch wertvoll, braucht eigenen Fokus) | `#B` bleibt in seinem Topf; `#A` rueckt in 4.5 vor `#B` |
| wartend/blockiert | `#B` → **wartend/blockiert**, `⏳ wartet auf: #A` |

Durchgang 2 wiederholen, bis sich kein Topf mehr aendert (Ketten `#A vor #B vor #C`).
`sinnvoll`-Abhaengigkeiten aendern den Topf nie — sie wirken nur auf die Reihenfolge (4.5).

Warum zwei Durchgaenge: Ist die Vorbedingung selbst arbeitsbereit, wird aus „#B wartet" die
brauchbarere Empfehlung „erst #A, dann #B"; wartet die Vorbedingung, darf `#B` nicht als
arbeitsbereit davor stehen.

### 4.5 Empfohlene Reihenfolge

Nummerierte Liste ueber die Ideen der drei Arbeits-Toepfe, gebildet so:

1. Quick Wins, dann strategisch wertvoll, dann braucht eigenen Fokus
2. Innerhalb eines Topfs: Nutzen `hoch` vor `mittel`; bei Gleichstand die aeltere Idee zuerst (Datum,
   bei gleichem Datum die niedrigere Nummer)
3. Jede Abhaengigkeit `#A vor #B`, bei der **beide** Ideen in der nummerierten Liste stehen,
   wird eingehalten — auch ueber Topf-Grenzen hinweg (dann rueckt `#A` vor `#B`, mit Vermerk).
   Kanten zu Ideen ausserhalb der Liste (wartend, ausserhalb der Teilmenge) erscheinen nur
   unter `## Abhaengigkeiten`

**Zyklus** (`#A vor #B` und `#B vor #A`, auch ueber Ketten): zuerst die `sinnvoll`-Kanten des
Zyklus verwerfen. Bleibt ein Zyklus aus zwingenden Kanten, gilt fuer die beteiligten Ideen nur
die Sortierung aus 4.5 Punkt 2 (Nutzen, dann Datum, dann Nummer), und unter `## Abhaengigkeiten` steht
`⚠ Zyklus #A ↔ #B — Reihenfolge widerspruechlich, im Review klaeren`.

Ideen aus **wartend/blockiert** erscheinen nicht in der nummerierten Liste; ihre
Freigabe-Bedingung steht nur in der ⏳-Zeile im Topf.

## Schritt 5: Ausgeben

Keine Rueckfragen — sofort ausgeben. Leere Toepfe erscheinen mit `_(leer)_`, damit sichtbar
ist, dass der Topf geprueft wurde.

```
# Ideen-Rangliste

**Stand:** {YYYY-MM-DD} · {N} offene Ideen bewertet{ (Teilmenge: #a, #b)}
{⚠-Hinweiszeilen aus Schritt 2, falls vorhanden}

## Quick Wins
- **#{N}** {Kurztitel} — Aufwand klein · Nutzen {Stufe} — {1-Satz-Begruendung}

## Strategisch wertvoll
- **#{N}** {Kurztitel} — Aufwand mittel · Nutzen {Stufe} — {1-Satz-Begruendung}

## Braucht eigenen Fokus
- **#{N}** {Kurztitel} — Aufwand gross · Nutzen {Stufe} — {1-Satz-Begruendung}

## Wartend/blockiert
- **#{N}** {Kurztitel} — Aufwand {Stufe} · Nutzen {Stufe} — {1-Satz-Begruendung}
  ⏳ wartet auf: {#A (Status) | Change {slug} | Anlass/Bedarf | externe Voraussetzung}

## Abhaengigkeiten
- {#A | Change {slug}} vor #{B} — {zwingend | sinnvoll (Vermutung)}: {Grund}
{⚠ Zyklus #A ↔ #B — Reihenfolge widerspruechlich, im Review klaeren}
{oder: _(keine erkannt)_}

## Empfohlene Reihenfolge
1. #{N} {Kurztitel}
2. #{N} {Kurztitel}{ — vorgezogen: Vorbedingung fuer #B}

---

Momentaufnahme — INBOX.md unveraendert. Entscheidungen je Idee: /dtb:idea-review
```

**Kurztitel:** der fett gesetzte Anfang des Idee-Texts, sonst dessen erste ~8 Woerter —
nicht umformulieren.

**Zusaetze je Idee-Zeile (alle Toepfe):**

- `(Rest nach Teil-Routing)` — direkt hinter den Kurztitel (Schritt 4.1)
- `↪ {Hinweis}` — eingerueckt unter der Idee-Zeile, je Hinweis eine Zeile; Wortlaut unveraendert
  aus der Tabelle „Vorbedingung → Wirkung" in 4.2
- `⏳ wartet auf: …` — nur im Topf wartend/blockiert, wie in der Vorlage

## Wichtig

- **Rein lesend:** Dieser Skill aendert keine Datei — kein Statuswechsel, kein Link, kein
  Vermerk in der Inbox. Entscheidungen trifft `/dtb:idea-review`
- **Kein zweiter Speicherort:** Die Rangliste ist ein Chat-Report, keine Datei. Sie veraltet
  mit jeder neuen Idee; jeder Aufruf bewertet frisch und schreibt keine fruehere Rangliste fort
- **Becken bleibt draussen:** `INBOX-BEFUNDE.md` wird nicht gelesen (§6.4)
- **Jede Idee in genau einem Topf:** die Zuordnung folgt den Tabellen in 4.4,
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
