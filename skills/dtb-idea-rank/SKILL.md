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
  consumes: [INBOX.md, BACKLOG.md, features/*/spec.md, features/*/plan.md, workflow.config.yaml]
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

- **Datei fehlt oder hat keine Datenzeile** →
  ```
  Keine Inbox vorhanden — nichts zu ranken. Ideen erfassen mit /dtb:idea
  ```
  Ende.
- **Kandidaten:** alle Eintraege mit Status `Offen`. „Offen" ist genau dieser Status-Wert
  der Inbox — keine eigene Auslegung (weder `In Arbeit` noch `Ausgearbeitet` zaehlen).
- **Keine `Offen`-Eintraege** →
  ```
  Keine offenen Ideen in der Inbox — nichts zu ranken.
  Geprueft: {config.paths.workflows}/INBOX.md (Status "Offen")
  ```
  Ende.
- **Eintraege mit Status `In Arbeit`** merken — sie werden nicht gerankt, dienen aber als
  Blocker-Kontext (Schritt 4).

**Das Befund-Becken `INBOX-BEFUNDE.md` wird NICHT gelesen.** Becken-Eintraege sind bis zu
ihrer Befoerderung fuer keine Arbeitssicht sichtbar (`DERIVED_STATE_RULES.md` §6.4). Weil das
Becken ungelesen bleibt, ist eine Becken-Nummer im Idee-Text nicht von einer archivierten
Idee unterscheidbar — beide behandelt Schritt 4.3 als **Verweis ausserhalb der Inbox**.

## Schritt 2: Argument auswerten

| Argument | Umfang |
|----------|--------|
| _(leer)_ | alle `Offen`-Ideen |
| Nummern (`27 33 45`, auch `#27, #33`) | nur diese Ideen |

Je Nummer des Arguments, die nicht zu einer `Offen`-Idee gehoert, eine Hinweiszeile vor dem
Report — der Rest wird normal gerankt:

- existiert nicht → `⚠ #{N} nicht in der Inbox — uebersprungen`
- anderer Status → `⚠ #{N} hat Status "{Status}" — nur "Offen" wird gerankt`

Bleibt keine Idee uebrig → nur die Hinweiszeilen ausgeben, Ende.

Bei einer Teilmenge werden Abhaengigkeiten zu Ideen **ausserhalb** der Teilmenge trotzdem
genannt (mit Nummer), nur nicht selbst gerankt.

## Schritt 3: Querbelege lesen

Lies read-only, um Blocker und Ueberschneidungen zu erkennen:

- `{config.paths.workflows}/features/*/spec.md` und `plan.md` — laufende Changes (Ziel,
  Scope, `## Progress`-Stand grob: begonnen / nicht begonnen)
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

### 4.2 Stufen je Idee

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
| `hoch` | beseitigt einen belegt wiederkehrenden Schmerz oder eine Fehlerklasse (Beleg im Text: Datum, Anzahl, Session), oder ist Vorbedingung anderer Ideen |
| `mittel` | spuerbare Verbesserung eines regelmaessig genutzten Ablaufs, ohne belegte Wiederholung |
| `niedrig` | wuenschenswert, aber kein belegter Bedarf; Erkundung ohne konkreten Anlass |

Grenzfall zwischen zwei Stufen → die **niedrigere** Nutzen- bzw. die **hoehere**
Aufwand-Stufe waehlen. Die Rangliste soll eher zu vorsichtig empfehlen als eine Idee zum
Quick Win hochzureden.

### 4.3 Abhaengigkeiten erkennen

Eine Abhaengigkeit ist ein gerichtetes Paar `#A vor #B` mit Grund. Quellen:

- **ausdruecklich im Text** — Nennung einer anderen Nummer mit Reihenfolge-Aussage („nach",
  „setzt voraus", „blockiert", „erst wenn") → `zwingend`
- **Querbeleg** — die Idee aendert, was ein laufender Change gerade baut, oder braucht
  dessen Ergebnis → `zwingend`, wenn der Text es sagt; sonst `sinnvoll (Vermutung)`
- **inhaltlich geschlossen** — zwei Ideen beruehren dieselbe Stelle, eine sollte zuerst
  → `sinnvoll (Vermutung)`

Ein Blocker ist **erfuellt**, wenn die benannte Idee `Ausgearbeitet` ist bzw. der benannte
Change abgeschlossen ist (`## Progress` vollstaendig). `In Arbeit` und laufende Changes
blockieren weiter.

**Verweis ausserhalb der Inbox** (die genannte Nummer steht nicht in `INBOX.md`): daraus
entsteht **keine** Abhaengigkeit und kein Blocker, und die Nummer wird **nicht** in den Report
uebernommen. Die Nummer kann eine archivierte Idee oder ein Becken-Eintrag sein — ohne das
Becken zu lesen, ist das nicht entscheidbar, und ein Becken-Eintrag darf in keiner Arbeitssicht
erscheinen (§6.4). Stattdessen traegt die Zeile der verweisenden Idee den Zusatz
`↪ Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar`. Probelauf 2026-09-17: ohne diese
Regel stand eine Idee dauerhaft als „blockiert, Stand unklar" hinter einem nie befoerderten
Becken-Eintrag.

### 4.4 Topf-Zuordnung (feste Reihenfolge, erster Treffer gilt)

Jede Idee landet in **genau einem** Topf. Pruefe die Regeln in dieser Reihenfolge:

| # | Bedingung | Topf |
|---|-----------|------|
| 1 | Mindestens ein **zwingender**, nicht erfuellter Blocker (Idee, laufender Change, externe Voraussetzung) | **wartend/blockiert** |
| 2 | Nutzen `niedrig` | **wartend/blockiert** — Vorbedingung „Anlass/Bedarf" |
| 3 | Aufwand `gross` | **braucht eigenen Fokus** |
| 4 | Aufwand `klein` | **Quick Wins** |
| 5 | Aufwand `mittel` | **strategisch wertvoll** |

Warum diese Reihenfolge: Ein Blocker macht jede andere Einstufung gegenstandslos (Regel 1).
Eine Idee ohne belegten Bedarf lohnt auch bei kleinem Aufwand nicht vorab — sie wartet auf
einen Anlass (Regel 2; Praxis 2026-07-30: „#25/#18 warten auf Anlass"). Grosser Aufwand ist
nie nebenbei zu haben, auch bei hohem Nutzen (Regel 3). Erst danach entscheidet der Aufwand
allein zwischen den beiden Arbeits-Toepfen (Regeln 4/5). `sinnvoll`-Abhaengigkeiten aendern
den Topf nicht — sie wirken nur auf die Reihenfolge (Schritt 4.5).

### 4.5 Empfohlene Reihenfolge

Nummerierte Liste ueber die Ideen der drei Arbeits-Toepfe, gebildet so:

1. Quick Wins, dann strategisch wertvoll, dann braucht eigenen Fokus
2. Innerhalb eines Topfs: Nutzen `hoch` vor `mittel`; bei Gleichstand die aeltere Idee zuerst
3. Jede Abhaengigkeit `#A vor #B` wird eingehalten — auch ueber Topf-Grenzen hinweg
   (dann rueckt `#A` vor `#B`, mit Vermerk)

Ideen aus **wartend/blockiert** erscheinen nicht in der nummerierten Liste, sondern darunter
mit ihrer Freigabe-Bedingung („nach #A", „bei Anlass").

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
  {↪ Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar   ← nur falls zutreffend, in jedem Topf}

## Abhaengigkeiten
- #{A} vor #{B} — {zwingend | sinnvoll (Vermutung)}: {Grund}
{oder: _(keine erkannt)_}

## Empfohlene Reihenfolge
1. #{N} {Kurztitel}
2. #{N} {Kurztitel}{ — vorgezogen: Vorbedingung fuer #B}

Danach, sobald freigegeben:
- #{N} — {Freigabe-Bedingung}

---

Momentaufnahme — INBOX.md unveraendert. Entscheidungen je Idee: /dtb:idea-review
```

**Kurztitel:** der fett gesetzte Anfang des Idee-Texts, sonst dessen erste ~8 Woerter —
nicht umformulieren.

## Wichtig

- **Rein lesend:** Dieser Skill aendert keine Datei — kein Statuswechsel, kein Link, kein
  Vermerk in der Inbox. Entscheidungen trifft `/dtb:idea-review`
- **Kein zweiter Speicherort:** Die Rangliste ist ein Chat-Report, keine Datei. Sie veraltet
  mit jeder neuen Idee; jeder Aufruf bewertet frisch und schreibt keine fruehere Rangliste fort
- **Becken bleibt draussen:** `INBOX-BEFUNDE.md` wird nicht gelesen (§6.4)
- **Jede Idee genau einmal:** in genau einem Topf; die Zuordnung folgt der Tabelle in 4.4,
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
