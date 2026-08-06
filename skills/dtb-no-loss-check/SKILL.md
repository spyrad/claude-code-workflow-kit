---
name: dtb:no-loss-check
description: >-
  Use when: "bevor ich Schluss mache", "no loss check", "geht was verloren",
  "Verlustpruefung", "was ist noch nicht erfasst", "Session-Hygiene". Compares the
  active conversation against the artifact state and reports lessons, subject-matter
  questions and decisions that surfaced but were never captured — read-only, each
  finding with a ready-to-run capture command.
disable-model-invocation: false
allowed-tools: Read, Glob, Grep
pipeline:
  stage: session
  after: null
  next: [dtb:workflow-checkpoint]
  consumes: [workflow.config.yaml, project-rules/lessons.md, features/*/spec.md, features/*/discovery.md, INBOX.md]
  produces: []
---

# Verlustpruefung vor dem Session-Ende (no-loss-check)

Du vergleichst den **Gespraechsverlauf** dieser Sitzung gegen den **Artefakt-Stand** des Projekts
und meldest, was nur im Gespraech lebt und in keiner Datei gelandet ist. Drei Sorten Delta:

| Delta | Zielartefakt | Erfassungs-Befehl |
|-------|--------------|-------------------|
| Lektion aufgetaucht | `{config.paths.rules}/lessons.md` | `/dtb:lesson` |
| Fach-Frage aufgetaucht | `features/*/{discovery,spec}.md` → `## Offene Punkte` | `/dtb:open-question` |
| Idee/Entscheidung ohne Ablage | `{config.paths.workflows}/INBOX.md` | `/dtb:idea` |

## Strenge: empfehlend — dieser Skill blockiert nichts

Er meldet, benennt die dringenden Funde und fragt **einmal** nach. Er haelt den Checkpoint nicht
auf, verlangt keine Bestaetigung und wertet ein „egal, weiter" nicht als Fehler. Der Name sagt
`check`, nicht `gate`: die Pruefung ist verbindlich formuliert, die **Konsequenz** bleibt beim
Menschen — er koennte sie ohnehin nicht erzwingen, weil `dtb:workflow-checkpoint`
`disable-model-invocation: true` traegt und nur der Mensch ihn startet.

Sein Wert liegt woanders: Er **nimmt die Formulierungsarbeit ab**. Jeder Fund kommt als
kopierfertige Befehlszeile mit ausformuliertem Argument — abschicken statt nachdenken.

## Was dieser Skill NICHT ist

- **Kein Recap.** „Was haben wir heute gemacht" beantwortet `dtb:session-summary` (read-only,
  rueckblickend). Dieser Skill beantwortet die andere Frage: **was droht verloren zu gehen**.
- **Kein Schreiber.** Er ruft die drei Erfassungs-Skills nicht auf und schreibt ihre Artefakte
  nicht selbst — `allowed-tools` enthaelt bewusst kein `Write`/`Edit`. Zwei Schreiber pro
  Artefakt waeren genau die Spiegel-Kopplung, die dieses Kit schon zweimal Folgefehler gekostet hat.
- **Kein Ersatz fuer den Checkpoint.** Er sitzt davor; `dtb:workflow-checkpoint` bleibt
  eigenstaendig.

## Vertraulichkeit (Contract-Regel, gilt fuer jede Ausgabe)

Zugangsdaten, Schluessel, Tokens und personenbezogene Daten werden **nie woertlich** in eine
Vorschlagszeile uebernommen. Der Fund wird gemeldet, die heikle Stelle durch einen Platzhalter
ersetzt (`<Token>`, `<Kundenname>`). Grund: dieser Skill ist der Trichter vom fluechtigen
Gespraech in dauerhafte, oft **versionierte** Artefakte — `/dtb:idea` schreibt ungefiltert in
`INBOX.md`, und die reist ueber jeden Push mit.

---

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende die Fallback-Pfade `dtb-project/project-workflows/` und
`dtb-project/project-rules/`. Kein Abbruch — ohne Config laeuft die Pruefung auf den
Standardpfaden weiter.

---

## Stufe 1: Kandidaten erkennen

Gehe den Gespraechsverlauf dieser Sitzung durch und sammle **Kandidaten** je Delta-Sorte. Diese
Stufe erzeugt Verdachtsfaelle — gefiltert wird erst in Stufe 2.

### Signalklassen

**Lektion** — eine Regel, die kuenftig gilt (nicht: was heute passiert ist):

- Ein **Ursachenbefund nach einem Fehlschlag**: etwas ging schief, die Ursache wurde benannt
- Eine als **allgemein erkannte Regel** („kuenftig zuerst X pruefen", „nie wieder Y ohne Z")
- Eine **Korrektur, die beim zweiten Mal Zeit gespart haette** — der Umweg ist erkannt, aber nur
  im Gespraech beschrieben

**Fach-Frage** — eine Frage, die ins Meeting gehoert (nicht sofort/allein beantwortbar):

- Eine Frage wurde gestellt und **vertagt statt beantwortet** („das klaeren wir spaeter",
  „muss ich nachfragen")
- Ein **bewusst offen gelassener Punkt ohne Zustaendigen** — die Entscheidung wurde verschoben,
  ohne dass jemand sie uebernommen hat

**Idee / Entscheidung ohne Ablage:**

- Ein **Verbesserungsvorschlag**, der im Gespraech auftauchte und in keinem INBOX-Eintrag steht
- Eine **getroffene Festlegung**, die in keinem Artefakt steht und beim naechsten Mal neu
  verhandelt wuerde („wir machen das ab jetzt so…")

### Recall vor Precision (verbindlich)

Im Zweifel **melden**. Ein Falsch-Positiv kostet eine Zeile, die der Nutzer ueberliest; ein
uebersehener Fund ist der Schaden, gegen den dieser Skill ueberhaupt existiert. Die Heuristik
wird bewusst weit gefasst — die Verengung leistet Stufe 2, nicht diese Stufe.

Formuliere jeden Kandidaten schon hier so, wie er im Artefakt stehen wuerde (ein Satz, ohne
Gespraechs-Kontext wie „wie du vorhin sagtest") — Stufe 2 vergleicht diese Formulierung gegen
den Bestand, und der Report gibt sie unveraendert als Befehls-Argument aus.

---

## Stufe 2: Abgleich gegen den Artefakt-Stand

Jeder Kandidat aus Stufe 1 wird gegen den Bestand geprueft. Was dort schon steht, wird
**unterdrueckt** — aber nie stillschweigend: die Zahl der unterdrueckten Kandidaten erscheint als
eine Sammelzeile im Report.

### Lesequellen je Delta-Sorte

| Delta | Wo gelesen wird | Was verglichen wird |
|-------|-----------------|---------------------|
| Lektion | `{config.paths.rules}/lessons.md` (Fallback `dtb-project/project-rules/lessons.md`) | Spalte `Rule` jeder Datenzeile unter der `\|---\|`-Trennzeile |
| Fach-Frage | `{config.paths.workflows}/features/*/spec.md` und `.../discovery.md` | **Alle** Inhaltszeilen innerhalb von `## Offene Punkte` — die §6-Kanonform `- [ ] [Fach] …`, ihre beantwortete Form `- [x] [Fach] …` **und** untagged Bullets |
| Idee/Entscheidung | `{config.paths.workflows}/INBOX.md` | Idee-Spalte **jeder** Zeile, unabhaengig vom Status |

**Drei Ausschluesse — jeder mit Grund:**

1. **`archive/` bleibt draussen.** Ein archivierter Change ist abgeschlossen; taucht sein Thema
   erneut auf, ist das ein legitimer neuer Fund und keine Dublette. Gleiche Grenze wie
   `dtb:meeting-agenda`.
2. **Code-Fences bleiben draussen.** Beispiel-Zeilen in Doku (` ```- [ ] [Fach] … ``` `) sind
   keine erfassten Fragen — sonst filtert der Skill echte Funde anhand von Dokumentation weg.
3. **`## Progress`, Statusfelder und Plan-Bloecke werden nicht gelesen.** Sie tragen keine
   erfassten Inhalte, nur Zustaende.

> **Warum beim Fach-Fragen-Abgleich auch untagged Bullets zaehlen** (Kalibrier-Befund
> 2026-08-06): Fuer die Frage „steht das schon irgendwo?" ist das `[Fach]`-Tag irrelevant — der
> Ablage-Ort ist derselbe. Wer nur die Kanonform liest, meldet jede als normalen Bullet
> festgehaltene Frage bei **jedem** Lauf erneut. Das Tag entscheidet, ob eine Frage ins Meeting
> geht (§6), nicht ob sie erfasst ist.

**Status ist beim Abgleich egal — mit einer Nuance:** Ein INBOX-Eintrag auf `Verworfen` gilt als
**erfasst** (die Entscheidung ist gefallen, erneutes Melden waere Rauschen). Er wird aber in der
Sammelzeile mit dem Zusatz `davon {N} bewusst verworfen` ausgewiesen — sonst sieht niemand, dass
ein Fund einer frueheren Entscheidung widerspricht.

**Fehlende Dateien sind kein Fehler.** `lessons.md` ist ein Laufzeit-Artefakt und im Kit
ungetrackt; existiert sie nicht, sind **alle** Lektions-Kandidaten neu. Gleiches gilt fuer eine
fehlende `INBOX.md` oder ein Projekt ohne `features/`-Ordner. Nie abbrechen, nie als Warnung
melden.

### Die Unterdrueckungs-Regel: Ersetzungsprobe

Der Check formuliert Funde neu — ein exakter Textvergleich (wie ihn `dtb:open-question` fuehrt)
griffe hier nie. Der Vergleich ist deshalb unscharf, und die Schwelle lautet:

> **Unterdruecke einen Kandidaten nur dann, wenn der vorhandene Eintrag ihn ohne
> Informationsverlust ersetzen koennte** — gleicher Gegenstand **und** gleiche Aussage.
> Trifft der Bestand denselben Gegenstand, aber eine **andere** Aussage → melden.

Beispiele:

| Kandidat | Bestand | Ergebnis |
|----------|---------|----------|
| „Der Checkpoint macht den Arbeitsbaum selbst schmutzig" | `#35` „Handoff-Block behauptet Zustaende, die nicht stimmen" | **Melden** — gleicher Gegenstand, andere Aussage (Ursache vs. Symptom) |
| „3 von 6 Capture-Skills haben keinen Duplikat-Schutz" | `#48` „fehlender Duplikat-Schutz in `idea`/`task`/`bug-report`" | **Unterdruecken** → Sammelzeile |

**Warum keine Prozent-Schwelle:** Eine Quote („ab 60 % Stichwort-Ueberlappung") suggeriert eine
Messbarkeit, die es hier nicht gibt — zwei Laeufe zaehlen Inhaltswoerter unterschiedlich, und
niemand rechnet die Zahl nach. Die Ersetzungsprobe ist dagegen eine Frage, die bei jedem Lauf
gleich gestellt und vom Menschen nachvollzogen werden kann.

**Im Zweifel gilt Stufe 1:** Laesst sich die Ersetzungsfrage nicht klar mit „ja" beantworten,
wird gemeldet. Eine zu strenge Unterdrueckung faellt niemandem auf — das ist der teurere Fehler.

---

## Report: Funde melden

Der Report kommt **am Stueck** — kein interaktiver Durchlauf, keine Rueckfrage pro Fund. Ein Fund
ist erfassenswert oder nicht, und das sieht man in einer Zeile.

### Zwei Gruppen nach Verlustrisiko

| Gruppe | Was hineingehoert |
|--------|-------------------|
| **Vor dem Checkpoint erledigen** | Der Inhalt existiert **nur** im Gespraech und waere danach nicht rekonstruierbar — z.B. ein Ursachenbefund nach langer Fehlersuche, eine muendlich getroffene Festlegung |
| **Kann warten** | Der Inhalt liesse sich notfalls aus Artefakten, Commits oder Logs rekonstruieren — die Erfassung spart Arbeit, verhindert aber keinen Verlust |

Im Zweifel gehoert ein Fund in die erste Gruppe.

### Format je Fund

```
[Gruppe] {Ein-Satz-Fund}
  → /dtb:{skill} {fertiges Argument}
  Ziel: {pfad} ({versioniert|nicht versioniert})
```

**Die Befehlszeile muss ohne Nacharbeit absetzbar sein.** Das heisst konkret:

- `/dtb:lesson <Freitext>` — der Freitext nennt Situation, Falle und die kuenftige Regel in einem
  Satz; `dtb:lesson` leitet daraus selbst die vier Felder ab
- `/dtb:open-question <slug> "<Frage>"` — **der Slug ist Pflicht.** `dtb:open-question` erkennt das
  erste Token nur dann als Slug, wenn es exakt einen vorhandenen Feature-Ordner matcht; ohne Slug
  wird das erste Fragewort verschluckt. Ermittle den Ziel-Slug aus dem Gespraechszusammenhang
- `/dtb:idea <Freitext>` — ein Satz, wie er in der INBOX stehen soll

### Versioniert oder nicht (Pflichtangabe je Fund)

Vor dem Absetzen muss sichtbar sein, wohin der Inhalt wandert. Bestimme den Zustand durch einen
Blick in die `.gitignore` des Projekts:

- Zielpfad steht dort → `nicht versioniert` (bleibt lokal; `lessons.md` ist im Kit selbst so
  gefuehrt — Idee #34)
- Zielpfad steht dort nicht → `versioniert` (reist ueber jeden Push mit — das gilt insbesondere
  fuer `INBOX.md` und alles unter `features/`)
- Keine `.gitignore` vorhanden oder Projekt ohne Git → Angabe weglassen, **nicht raten**

### Ausgabe-Muster (feste Ueberschriften, woertlich uebernehmen)

```
Verlustpruefung — {N} Fund(e)

## Vor dem Checkpoint erledigen

- Der Checkpoint liest den Git-Stand vor dem eigenen Schreiben und hinterlaesst
  deshalb immer einen schmutzigen Arbeitsbaum.
  → /dtb:lesson "Checkpoint liest Git in Schritt 1 und schreibt in 3/4 — eine
    'Arbeitsbaum sauber'-Aussage im Handoff ist im Moment des Schreibens falsch,
    ausser es folgt ein Commit."
  Ziel: dtb-project/project-rules/lessons.md (nicht versioniert)

## Kann warten

- Reziprozitaet der Pipeline-Kanten wird nirgends geprueft.
  → /dtb:idea "Lint fuer halbseitige Pipeline-Kanten in dtb:project-health."
  Ziel: dtb-project/project-workflows/INBOX.md (versioniert)

2 Kandidaten als bereits erfasst gefiltert
```

Ist eine Gruppe leer, entfaellt ihre Ueberschrift — nie eine leere Ueberschrift ausgeben.

### Sammelzeile fuer Unterdruecktes (Pflicht, auch bei 0)

Genau eine Zeile am Ende des Reports:

```
{N} Kandidaten als bereits erfasst gefiltert{, davon {M} bewusst verworfen}
```

Sie macht eine zu strenge Schwelle sichtbar. Ohne sie wirkt jede Fehlkalibrierung wie ein sauberer
Lauf — derselbe Fehler, gegen den die Kompressions-Meldung unten existiert.

---

## Leer-Fall: nichts gefunden

Der Normalfall ist „nichts offen", und dieser Skill laeuft potenziell vor jedem Checkpoint. Ein
teurer Leerlauf wird uebersprungen — also **eine** Zeile plus Freigabe, nichts weiter:

```
Nichts Unerfasstes gefunden ({N} Kandidaten als bereits erfasst gefiltert).
Weiter mit /dtb:workflow-checkpoint.
```

**Verboten im Leer-Fall:** Aufzaehlung der geprueften Quellen, Wiederholung der Signalklassen,
Zusammenfassung der Sitzung (das ist `dtb:session-summary`). Wer hier auswalzt, sorgt dafuer, dass
der Skill beim naechsten Mal uebersprungen wird.

---

## Randfaelle

### 1. Komprimierter Verlauf — die eigene Blindheit melden

Bei langen Sitzungen fasst das Harness den Verlauf zusammen. Der Check sieht dann eine
Zusammenfassung statt des Gespraechs — ausgerechnet in der langen Sitzung, in der am meisten
aufgelaufen ist. Betroffen ist **nur Stufe 1**; der Abgleich in Stufe 2 liest Dateien und bleibt
unberuehrt.

Gibt es Anzeichen fuer eine Kompression (Hinweis im Verlauf, erkennbar zusammengefasste
Vorgeschichte, fehlende Anfangsphase), gehoert **oben in den Report**:

```
⚠ Verlauf komprimiert — Erkennung unvollstaendig. Ein frueherer Lauf haette mehr gesehen;
  bei langen Sitzungen mehrfach laufen lassen statt nur am Ende.
```

Diese Zeile wird **nie** weggelassen, um den Report sauber aussehen zu lassen. Ein Waechter, der
seine eigene Blindheit verschweigt, ist schlimmer als keiner.

### 2. Kein Ablage-Ort fuer eine Fach-Frage

`dtb:open-question` bricht ab, wenn das Ziel-Feature weder `spec.md` noch `discovery.md` hat —
`## Offene Punkte` gehoert nicht in `plan.md`/`bug.md`/`task.md`. Pruefe das **vor** dem Vorschlag:

- Ziel-Ordner hat `spec.md` oder `discovery.md` → normaler `/dtb:open-question`-Vorschlag
- Ziel-Ordner hat keine der beiden **oder** es gibt gar kein passendes Feature → **umleiten** auf
  `/dtb:idea`, mit sichtbarem Vermerk im Fund-Text, damit die Frage nicht als Idee verschwindet:

```
- {Frage} — urspruenglich eine Fach-Frage; kein Feature mit spec.md/discovery.md als Ablage-Ort.
  → /dtb:idea "[Fach-Frage ohne Ablage-Ort] {Frage}"
  Ziel: dtb-project/project-workflows/INBOX.md (versioniert)
```

### 3. Zweiter Lauf in derselben Sitzung

**Der eigene frueherer Report ist nie eine Kandidatenquelle.** Steht im Verlauf bereits eine
Ausgabe dieses Skills, wird sie beim Sammeln in Stufe 1 uebersprungen — sonst meldet der Check
seine eigenen Formulierungen als Funde und vergiftet sich selbst.

Erkennst du einen frueheren eigenen Lauf, gehoert eine Kopfzeile in den Report:

```
Zweiter Lauf dieser Sitzung — {N} Funde aus dem ersten sind erledigt oder verworfen.
```

**Bewusst verworfene Funde werden nicht unveraendert wiederholt.** Hat der Fund inzwischen neue
Substanz (weitere Belege, praezisere Formulierung), darf er erneut erscheinen — dann aber mit dem,
was neu ist. Ueber Sitzungsgrenzen hinweg ist jeder Fund wieder legitim: Was in einer anderen
Sitzung verworfen wurde, weiss dieser Lauf nicht, und Raten waere schlimmer als Wiederholen.

---

**Erstellt mit:** `/dtb:impl-plan` → `/dtb:implement` (Feature `no-loss-check`)
