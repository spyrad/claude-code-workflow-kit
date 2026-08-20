---
name: dtb:no-loss-check
description: >-
  Use when: "bevor ich Schluss mache", "no loss check", "geht was verloren",
  "Verlustpruefung", "was ist noch nicht erfasst", "Session-Hygiene". Compares the
  active conversation against the artifact state and reports lessons, subject-matter
  questions and decisions that surfaced but were never captured — read-only, each
  finding with a ready-to-run capture command. Trigger this proactively when the
  session appears to be ending or the topic shifts: the loss this skill guards
  against happens precisely in sessions that end without a checkpoint.
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

Er meldet, benennt die dringenden Funde und fragt **einmal** nach (Abschlussfrage im
Ausgabe-Muster). Er haelt den Checkpoint nicht auf, verlangt keine Bestaetigung und wertet ein
„egal, weiter" nicht als Fehler. Der Name sagt `check`, nicht `gate`: die Pruefung ist verbindlich
formuliert, die **Konsequenz** bleibt beim Menschen.

Das ist eine **bewusste Design-Entscheidung, keine technische Grenze.** Aus dem Schritt-0-Aufruf
heraus koennte dieser Skill den Checkpoint sehr wohl anhalten — er tut es nicht, weil ein
Waechter, der sich in den Weg stellt, nach wenigen Sitzungen weggeklickt wird und weil der Mensch
eine Sitzung jederzeit beenden koennen muss.

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
| Fach-Frage | `{config.paths.workflows}/features/*/spec.md` und `.../discovery.md` | **Alle** Inhaltszeilen innerhalb von `## Offene Punkte` — die §6-Kanonform `- [ ] [Fach] …`, ihre beantwortete Form `- [x] [Fach] …` **und** untagged Bullets. Sektionsgrenze wie in `dtb:meeting-agenda`: ab der Ueberschrift bis zur naechsten `## `-Ueberschrift bzw. zum Dateiende |
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

**Status ist beim Abgleich egal — mit einer Nuance:** Ein INBOX-Eintrag mit Status `Verworfen`
gilt als **erfasst** (die Entscheidung ist gefallen, erneutes Melden waere Rauschen) und zaehlt
damit dateiseitig mit. Er wird in der Sammelzeile zusaetzlich mit dem Zusatz
`davon {M} bewusst verworfen` ausgewiesen — sonst sieht niemand, dass ein Fund einer frueheren
Entscheidung widerspricht. **Nicht verwechseln** mit im Gespraech verworfenen Funden
(Randfall 3): die sind dateiseitig gar nicht vorhanden und zaehlen nirgends.

**Fehlende Dateien sind kein Fehler.** `lessons.md` ist ein Laufzeit-Artefakt und im Kit
ungetrackt; existiert sie nicht, sind **alle** Lektions-Kandidaten neu. Gleiches gilt fuer eine
fehlende `INBOX.md` oder ein Projekt ohne `features/`-Ordner. Nie abbrechen, nie als Warnung
melden.

### Die Unterdrueckungs-Regel: Ersetzungsprobe

> **Kopplungs-Hinweis (Spiegel):** Der Kanon dieser Probe steht in `skills/CLAUDE.md` →
> „Duplikat-Schutz (Capture-Skills)" → „Ersetzungsprobe (Kanon)" (Kit-Repo; in Zielprojekten
> existiert die Datei nicht — dieser Abschnitt bleibt deshalb die vollstaendige operative
> Fassung, bewusst aus der **Unterdrueckungs-Richtung** formuliert: „unterdruecken"/„melden"
> statt „Dublette"). Aenderung am Kanon → diesen Spiegel im selben Zug mitziehen: Schwelle UND
> Begruendung vollstaendig, Wortlaut darf kontextangepasst bleiben, die Aussage muss
> deckungsgleich sein.
>
> Verifikation: Grep `Informationsverlust ersetzen koennte` ueber `skills/` → **Zielzahl 4**
> = Kanon-Regelsatz + Kanon-Hinweiszeile (dortige Stufe 1) + dieser Spiegel-Regelsatz + diese
> Hinweiszeile. Die beiden Hinweiszeilen nennen den Anker woertlich und zaehlen deshalb mit —
> beim Nachzaehlen nicht als weitere Regel-Fassungen missdeuten. Es gibt genau **zwei**
> Regel-Fassungen (Kanon + dieser Spiegel).

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
- {Ein-Satz-Fund}
  → /dtb:{skill} {fertiges Argument}
  Ziel: {pfad} ({versioniert|nicht versioniert})
```

Die Gruppe wird ueber die **Ueberschrift** ausgedrueckt (siehe Ausgabe-Muster), nie ueber ein
Praefix in der Fund-Zeile.

**Die Befehlszeile muss ohne Nacharbeit absetzbar sein.** Das heisst konkret:

- `/dtb:lesson <Freitext>` — der Freitext nennt Situation, Falle und die kuenftige Regel in einem
  Satz; `dtb:lesson` leitet daraus selbst die vier Felder ab
- `/dtb:open-question <slug> "<Frage>"` — **der Slug ist Pflicht.** Ohne ihn leitet
  `dtb:open-question` das Ziel aus dem aktiven Feature ab: bei 0 aktiven Features bricht es ab,
  bei mehr als einem fragt es zurueck. Der vorformulierte Befehl waere dann nicht ohne Nacharbeit
  absetzbar — und genau das ist der Zweck dieser Zeile. (Verschluckt wird nichts: matcht das erste
  Token keinen vorhandenen Ordner, ist das gesamte Argument die Frage.) Ermittle den Ziel-Slug aus
  dem Gespraechszusammenhang
- `/dtb:idea <Freitext>` — ein Satz, wie er in der INBOX stehen soll

### Versioniert oder nicht (Pflichtangabe je Fund)

Vor dem Absetzen muss sichtbar sein, wohin der Inhalt wandert. Die Zuordnung ist **fest**:

| Zielartefakt | Zustand |
|--------------|---------|
| `INBOX.md` | versioniert — reist ueber jeden Push mit |
| `features/*` | versioniert |
| `project-rules/lessons.md` | nicht versioniert — bleibt lokal (Idee #34) |

**Vorbehalt (Hinweis an den Menschen, keine Anweisung an diesen Skill):** Das ist die
Standardverteilung des Kits. Traegt ein Zielprojekt eine abweichende `.gitignore`, kann die Angabe
danebenliegen — der Check kann das nicht erkennen und soll es auch nicht versuchen; die Korrektur
faellt dem Menschen zu.

**Nicht selbst per Datei-Lookup ermitteln.** `.gitignore` enthaelt Glob-Muster mit
Last-Match-wins und Negationen; ein blosser Pfad-Vergleich beantwortet die Frage nicht. Im Kit
selbst wird `lessons.md` z.B. ueber das Muster `dtb-project/project-rules/*` ignoriert — der
Klartext `lessons.md` steht dort nur in einem Kommentar. Verlaesslich waere allein
`git check-ignore`, und das liegt ausserhalb der lesenden Werkzeuge dieses Skills.

### Ausgabe-Muster (feste Ueberschriften, woertlich uebernehmen)

```
[nur bei komprimiertem Verlauf, Randfall 1 — immer ganz oben:]
⚠ Verlauf komprimiert — Erkennung unvollstaendig. Ein frueherer Lauf haette mehr gesehen;
  bei langen Sitzungen mehrfach laufen lassen statt nur am Ende.

[nur bei einem weiteren Lauf derselben Sitzung, Randfall 3 — direkt darunter:]
Weiterer Lauf dieser Sitzung — der vorige Report ist keine Kandidatenquelle;
bereits Erfasstes ist ueber Stufe 2 gefiltert.

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

Trotzdem weiter zum Checkpoint? (ja / erst erfassen)
```

Ist eine Gruppe leer, entfaellt ihre Ueberschrift — nie eine leere Ueberschrift ausgeben.
Die beiden bedingten Kopfzeilen stehen in genau dieser Reihenfolge **ueber** der Titelzeile;
trifft keine zu, beginnt der Report mit `Verlustpruefung — {N} Fund(e)`.

**Platzhalter (nicht verwechseln):** `{N}` ist die Zahl der **gemeldeten Funde** (Titelzeile),
`{S}` die Zahl der **unterdrueckten Kandidaten** (Sammelzeile).

**Die Abschlussfrage ist Pflicht, das Warten darauf nicht.** Sie ist der eine Moment, an dem der
Mensch innehaelt — aber der Skill blockiert nichts: Kommt keine Antwort, gilt das als „ja". Im
Leer-Fall entfaellt sie (dort gibt es nichts zu erfassen).

### Sammelzeile fuer Unterdruecktes (Pflicht, auch bei 0)

Genau eine Zeile am Ende des Reports:

```
{S} Kandidaten als bereits erfasst gefiltert{, davon {M} bewusst verworfen}
```

Sie macht eine zu strenge Schwelle sichtbar. Ohne sie wirkt jede Fehlkalibrierung wie ein sauberer
Lauf — derselbe Fehler, gegen den die Kompressions-Meldung unten existiert.

Der `{M}`-Zusatz erscheint **nur bei `M > 0`** (anders als `{S}`, das auch bei 0 steht). Dieselbe
Zeile — samt Zusatz — gilt woertlich auch im Leer-Fall.

**Was `{S}` zaehlt:** ausschliesslich **dateiseitige** Unterdrueckungen aus Stufe 2
(Ersetzungsprobe gegen den Artefakt-Stand). Funde, die im Gespraech bewusst verworfen wurden
(Randfall 3), zaehlen **nicht** mit — sie waren nie „erfasst", und die Zeile wuerde sonst etwas
Falsches behaupten. Sie werden auch **nirgends sonst** nachgehalten: die Entscheidung fiel in
dieser Sitzung und steht im Verlauf; ueber Sitzungsgrenzen hinweg sind sie ohnehin wieder
legitime Funde.

---

## Leer-Fall: nichts gefunden

Der Normalfall ist „nichts offen", und dieser Skill laeuft potenziell vor jedem Checkpoint. Ein
teurer Leerlauf wird uebersprungen — also **eine** Zeile plus Freigabe, nichts weiter:

```
[nur bei komprimiertem Verlauf, siehe Randfall 1:]
⚠ Verlauf komprimiert — Erkennung unvollstaendig. Ein frueherer Lauf haette mehr gesehen;
  bei langen Sitzungen mehrfach laufen lassen statt nur am Ende.

Nichts Unerfasstes gefunden ({S} Kandidaten als bereits erfasst gefiltert{, davon {M} bewusst verworfen}).
[nur bei eigenstaendigem Aufruf:] Weiter mit /dtb:workflow-checkpoint.
```

**Ausnahme:** Die Kompressions-Zeile aus Randfall 1 steht auch hier — ueber der Freigabe. Ein
Leer-Verdikt auf komprimiertem Verlauf ist die schwaechste Aussage, die dieser Skill treffen
kann; sie ohne Vorbehalt auszugeben waere genau das Verschweigen, gegen das Randfall 1 existiert.

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

### 3. Weiterer Lauf in derselben Sitzung

**Der eigene frueherer Report ist nie eine Kandidatenquelle.** Steht im Verlauf bereits eine
Ausgabe dieses Skills, wird beim Sammeln in Stufe 1 nichts daraus geerntet — sonst meldet der
Check seine eigenen Formulierungen als Funde und vergiftet sich selbst.

**Als Kontext darf er gelesen werden.** Der Unterschied ist wichtig: Nicht-Quelle heisst, dass
keine Formulierung von dort zum Kandidaten wird; es heisst nicht, dass der Report unsichtbar ist.
Eine im Verlauf ausgesprochene Ablehnung („den brauchen wir nicht") darf deshalb einem neu
abgeleiteten Kandidaten zugeordnet werden — nur so ist die Regel unten ueberhaupt ausfuehrbar.

Erkennst du einen frueheren eigenen Lauf, gehoert eine Kopfzeile in den Report:

```
Weiterer Lauf dieser Sitzung — der vorige Report ist keine Kandidatenquelle;
bereits Erfasstes ist ueber Stufe 2 gefiltert.
```

Die Zeile ist bewusst **zahl- und zustandsfrei**: Eine Bilanz „X erledigt, Y verworfen" waere
eine Behauptung ueber den Bearbeitungsstand fremder Funde, den dieser Skill nicht kennt — er
sieht Artefakte und Verlauf, nicht was der Mensch mit einem Vorschlag vorhatte. „Weiterer" statt
„Zweiter", damit die Zeile auch beim dritten Lauf stimmt.

**Bewusst verworfene Funde werden nicht unveraendert wiederholt.** Hat der Fund inzwischen neue
Substanz (weitere Belege, praezisere Formulierung), darf er erneut erscheinen — dann aber mit dem,
was neu ist. Ueber Sitzungsgrenzen hinweg ist jeder Fund wieder legitim: Was in einer anderen
Sitzung verworfen wurde, weiss dieser Lauf nicht, und Raten waere schlimmer als Wiederholen.

---

**Erstellt mit:** `/dtb:impl-plan` → `/dtb:implement` (Feature `no-loss-check`)
