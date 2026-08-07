# Discovery: No-Loss-Check
<!-- resume: done -->

> **Umbenannt 2026-08-06** (`/dtb:feature-plan`): `no-loss-gate` → `no-loss-check`. Grund: der
> Namens-Vorbehalt aus `## Offene Punkte` wurde entschieden — „Gate" versprach eine Blockade, die
> der Skill laut `## Gewuenschtes Verhalten` bewusst nicht leistet. Der Ordner wurde per `git mv`
> umbenannt, INBOX #29 nachgezogen. Der Idee-Titel in #29 bleibt historisch „No-Loss-Gate".

**Erstellt:** 2026-08-05
**Idee-Referenz:** Inbox #29 — "Session-Hygiene-/No-Loss-Gate: neuer eigener Skill, der als
Vorstufe zu `workflow-checkpoint` sitzt und die aktive Session auf nicht-persistierten Stand
absucht, bevor eine neue Session sauber („ohne Verluste") starten kann."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-no-loss-check/SKILL.md` | Neu — der zu bauende Detektor-Skill |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Pipeline-Gegenkante: heute `after: [dtb:impl-review]`, `next: [dtb:workflow-resume]`; die Vorstufe wird hier eingehaengt |
| `skills/dtb-lesson/SKILL.md` | Routing-Ziel „Lektion nur im Chat"; heute `after: null` |
| `skills/dtb-open-question/SKILL.md` | Routing-Ziel „Fach-Frage nicht in `## Offene Punkte`"; heute `after: null` |
| `skills/dtb-idea/SKILL.md` | Routing-Ziel „Idee/Entscheidung ohne Ablage"; heute `after: null` |
| `skills/dtb-session-summary/SKILL.md` | Abgrenzung: read-only Recap „was war" vs. handelnder Detektor „was droht verloren zu gehen" — ggf. reziproker Gegen-Hinweis |
| `CLAUDE.md` | Skill-Kategorien, Zeile „Session lifecycle" listet die Kette |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Nur falls der Detektor eine Ableitungsregel kanonisiert — erzeugt dann Seed-Skew nach #22 (siebter Fall) |

> Bewusst NICHT aufgenommen: `skills/dtb-kit-sync/SKILL.md` (ein neuer Skill faellt automatisch
> unter das Klasse-A-Muster `skills/dtb-*/SKILL.md`) und `skills/dtb-workflow-resume/SKILL.md`
> (siehe Scope, offener Punkt 5 ausgeschlossen). Die Changelog-Belege aus dem Idee-Text sind
> Lesequellen, keine Aenderungsziele — nach #32 gehoeren sie nicht in diesen Abschnitt.

---

## Anforderungen

### Scope

**Enthalten:**

- Vergleich des aktiven Gespraechsverlaufs gegen den Artefakt-Stand; erkennt drei Sorten Delta:
  | Delta | Zielartefakt | Routing-Ziel |
  |---|---|---|
  | Lektion aufgetaucht | `project-rules/lessons.md` | `/dtb:lesson` |
  | Fach-Frage aufgetaucht | `features/*/{discovery,spec}.md` → `## Offene Punkte` | `/dtb:open-question` |
  | Idee/Entscheidung ohne Ablage | `INBOX.md` | `/dtb:idea` |
- **Zweistufige Erkennungsmechanik** (offener Punkt 1 des Eintrags entschieden): Heuristik ueber
  den Chat-Kontext erzeugt Kandidaten, der Abgleich gegen den Artefakt-Stand filtert bereits
  erfasste weg. Beide Haelften noetig — die Heuristik allein ist nicht reproduzierbar, der
  Abgleich allein findet nur bereits Benanntes.
- **Meldung mit fertig formuliertem Befehl je Fund** (offener Punkt 2 entschieden): pro Delta eine
  kopierfertige Zeile inkl. vorformuliertem Argument, z. B. `/dtb:lesson <fertige Formulierung>`.
  Die Formulierungsarbeit ist erledigt, die Ausloesung bleibt beim Menschen.
- **Priorisierung statt Blockade:** Funde werden nach Verlustrisiko sortiert und markiert, welche
  vor dem Checkpoint zwingend sind und welche warten koennen. Der Waechter blockiert den
  Checkpoint nicht.
- Ist nichts offen, gibt der Skill den Weg zu `/dtb:workflow-checkpoint` frei.

**Nicht enthalten:**

- **Selbst schreiben.** Der Detektor bleibt read-only (`allowed-tools: Read, Glob, Grep`). Grund:
  er muesste sonst die Erfassungslogik der drei Ziel-Skills nachbauen (`open-question` mit
  Variante-c-Zielroutung und §6-Formatierung, `lesson` append-only mit eigener Nummerierung) —
  zwei Schreiber pro Artefakt ist genau die Spiegel-Kopplung, die am 30./31.07. zweimal
  Folgefehler erzeugt hat.
- **Skills selbst aufrufen.** Architektonisch ausgeschlossen: `dtb:lesson`, `dtb:open-question`,
  `dtb:idea` und `dtb:workflow-checkpoint` tragen alle `disable-model-invocation: true` — nur der
  Mensch kann sie ausloesen.
- **Recap „was war".** Das ist `dtb:session-summary` (read-only, Contract `produces: []`).
- **Rechner-Divergenz** (offener Punkt 5 des Eintrags — **entschieden: draussen**). Begruendung:
  Der Beleg vom 2026-08-03 (der 31.07. existierte in zwei Fassungen) ist kein Chat-Verlust — das
  Wissen war als Datei persistiert, nur der anderen Maschine unbekannt. Ein Chat-Detektor kann
  das prinzipiell nicht fangen, weil auf der zweiten Maschine kein Chat-Kontext existiert, in dem
  etwas fehlt. Sichtbar wird der Fall nur ueber `git fetch` — also am Session-**Anfang** in
  `workflow-resume`, nicht am Session-**Ende**. Der Mechanismus existiert dort bereits (fetch,
  behind-Meldung, Kollisionsrisiko-Warnung). Thematisch gehoert die Divergenz zu #34.
- **Der Checkpoint selbst.** Bleibt eigenstaendig; der Detektor sitzt davor.

### Gewuenschtes Verhalten

- **Strenge: empfehlend** (Mittelstufe von drei). Der Skill meldet, benennt die zwingenden Funde
  und fragt einmal nach („trotzdem zum Checkpoint?"). Kein hartes Gate — er kann es ohnehin nicht
  durchsetzen, weil `workflow-checkpoint` nur vom Menschen ausloesbar ist
  (`disable-model-invocation: true`); rein informativ waere zu schwach, ein Lauf am Session-Ende
  wird sonst weggeklickt. Der Ideen-Titel sagt „Gate", der Text „Detektor" — die Aufloesung ist
  die Mitte.
- **Recall vor Precision:** Im Zweifel melden. Falsch-Positive sind billig (eine Zeile im Report,
  die der Nutzer ueberliest), uebersehene Funde sind der eigentliche Schaden — der Skill
  existiert genau gegen sie. Die Heuristik wird entsprechend weit gebaut.
- **Leerlauf muss billig sein.** Der Normalfall ist „nichts gefunden", und der Skill laeuft
  potenziell vor jedem Checkpoint. Leer-Fall = eine Zeile plus Freigabe (Vorbild: `idea-review`
  „Keine offenen Ideen in der Inbox. Alles aufgeraeumt."). Ein teurer Leerlauf wird uebersprungen.
- **Report am Stueck, kein interaktiver Durchlauf.** Gruppiert nach Prioritaet (zwingend vor dem
  Checkpoint / kann warten), innerhalb der Gruppe je Fund die kopierfertige Befehlszeile.
  Abgrenzung zu `idea-review`: dort faellt pro Idee eine echte Entscheidung, hier nicht — ein Fund
  ist erfassenswert oder nicht, und das sieht man in einer Zeile.

### Randfaelle

- **Kontext-Kompression (strukturelle Grenze, kein Bug).** Bei langen Sessions fasst das Harness
  den Verlauf zusammen — der Detektor sieht dann eine Zusammenfassung statt des Chats, und zwar
  ausgerechnet in der langen Session, in der am meisten auflaeuft. Betroffen ist nur die
  Kandidatenerzeugung (Heuristik), nicht der Abgleich gegen den Artefakt-Stand.
  **Verhalten:** transparent melden („Kontext wurde komprimiert — Erkennung unvollstaendig,
  frueherer Lauf empfohlen") **und** mehrfache Laeufe pro Session empfehlen statt nur am Ende.
  Begruendung: Ein Waechter, der seine eigene Blindheit verschweigt, ist schlimmer als keiner —
  dasselbe Muster wie #35.
- **Kein Ablage-Ort fuer Fach-Fragen.** Existiert kein Feature-Ordner mit `spec.md`/`discovery.md`,
  bricht `open-question` ab (Schritt 3 dort, weicher Redirect). Der Detektor prueft das **vor** dem
  Vorschlag und leitet den Fund dann in die INBOX um (`/dtb:idea`) — mit sichtbarem Vermerk, dass
  es urspruenglich eine Fach-Frage war, damit sie nicht verschwindet.
- **Beinahe-Dubletten.** Der Detektor formuliert Funde neu; der Duplikat-Schutz von
  `open-question` ist ein **exakter** Textvergleich und greift dann nicht. Der Abgleich muss
  deshalb unscharf vergleichen (Stichwort-Ueberlappung), sonst meldet der Skill Dinge, die
  bereits erfasst sind.
- **Fehlende Artefakte sind kein Fehler.** `lessons.md` existiert oft nicht (Laufzeit-Artefakt,
  im Kit ungetrackt — #34). Fehlende Datei = alle Lektionen sind neu.
- **Zweiter Lauf in derselben Session.** Bewusst verworfene Funde duerfen nicht unveraendert
  wiederkommen; innerhalb der Session traegt das der Gespraechskontext. Ueber Sessions hinweg
  sind sie wieder legitim.

### Einschraenkungen

**Technisch:**

- **Read-only-Contract:** `allowed-tools: Read, Glob, Grep`, `produces: []` — folgt aus der
  Scope-Entscheidung „schreibt nichts selbst".
- **Kein Hard-Gate** (Konvention `skills/CLAUDE.md`: „Read-only-Skills, Entry-Points und Skills
  ohne zwingende Eingabe bekommen kein Hard-Gate"). Eine Session ohne Funde ist ein gueltiges
  Ergebnis, keine fehlende Eingabe.
- **Kein `disable-model-invocation`** — der Skill ist modellaufrufbar. Belegte Kit-Konvention:
  von 38 Skills tragen genau 5 keine Sperre (`backlog-status`, `meeting-agenda`,
  `session-summary`, `workflow-next`, `workflow-status`) — exakt die read-only Skills.
  **Fachlicher Gewinn:** Der Skill existiert gegen das Vergessen; waere er nur menschlich
  ausloesbar, muesste der Mensch an ihn denken — genau die Schwachstelle, die er schliessen soll.
  So springt der Waechter an, wenn das Modell das Session-Ende erkennt. Kehrseite (akzeptiert):
  er kann zur Unzeit anspringen — bei einem read-only Report ist der Schaden ein paar Zeilen
  unpassende Ausgabe.
- **Distribution automatisch:** `skills/dtb-*/SKILL.md` ist Klasse-A-Muster, `kit-sync` nimmt den
  Skill ohne Aenderung mit.

**Fachlich (Kit-Regeln):**

- **Derived State bleibt unberuehrt.** Der Detektor leitet keinen Feature-Status ab und schreibt
  keinen — er vergleicht Gespraechsinhalt gegen Artefaktinhalt.
- **Kein zweiter Speicherort.** Funde leben im Chat-Report, nicht in einer Datei — sonst entsteht
  ein Artefakt, das veraltet und gepflegt werden muesste (Begruendung analog #33 Punkt 2).
- **Spiegel-Kopplung ueber 6 Dateien** (`workflow-checkpoint`, `lesson`, `open-question`, `idea`,
  `session-summary`, `CLAUDE.md`) — die Konstellation, die am 30./31.07. zweimal Folgefehler
  erzeugt hat. `plan-review` ist bei diesem Feature nicht optional.

### Integrationspunkte

- **Externe Abhaengigkeiten: keine.** Kein API, kein Service — nur Dateisystem und
  Gespraechskontext.
- **Pipeline-Kanten (offener Punkt 3 des Eintrags entschieden).** Das Kit notiert Kanten
  reziprok (`workflow-checkpoint.next: [dtb:workflow-resume]` **+**
  `workflow-resume.after: [dtb:workflow-checkpoint]`) — eine Kante sind zwei Eintraege.
  | Skill | Aenderung |
  |---|---|
  | Detektor | `stage: session`, `next: [dtb:workflow-checkpoint]` |
  | `workflow-checkpoint` | `after: [dtb:impl-review]` → `after: [dtb:impl-review, dtb:no-loss-check]` |
  | `session-summary` | keine Kante — nur reziproker Abgrenzungs-Hinweis (Recap „was war" vs. Detektor „was droht verloren zu gehen") |
- **Die drei Routing-Kanten werden bewusst NICHT gesetzt** (Detektor → `lesson`,
  → `open-question`, → `idea`; alle drei Ziele stehen heute auf `after: null`). Begruendung: Eine
  `after`-Kante behauptet „kommt normalerweise nach jenem" — das stimmt nicht, alle drei sind
  Capture-Tools, die ueberwiegend spontan mitten in der Arbeit aufgerufen werden. Der Detektor
  ist ein Ausloeser unter vielen, nicht ihre Vorstufe; `pipeline-graph` und `workflow-status`
  wuerden eine Reihenfolge zeichnen, die es nicht gibt. Das Routing wird stattdessen in Prosa
  beschrieben. **Preis (akzeptiert):** die Routing-Beziehung ist nicht maschinenlesbar und fehlt
  im Pipeline-Graph — eine falsche Kante ist teurer als eine fehlende.

---

## Abhaengigkeiten

**Konflikte:** keine. **Ueberschneidungen:** 4, alle komplementaer.

- **`meeting-agenda`** (aktiv, Fertig zum Testen) — liest offene `[Fach]`-Fragen aus
  `discovery.md`/`spec.md`. Der Detektor erzeugt solche Zeilen indirekt ueber `open-question`:
  der eine fuellt, der andere liest.
- **`archive/fachfragen-erfassung`** — hat §6 und `open-question` gebaut; sein Ziel lautet
  woertlich „Derived-State-konform, ohne zweiten Speicherort" und bestaetigt damit die
  Einschraenkung aus 3d.
- **`archive/lesson-loop`** — hat `lessons.md` gebaut, eines der drei Zielartefakte.
- **`archive/meeting-dump`** — **Praezedenzfall, bewusst notiert:** gleicht Meeting-Notizen gegen
  offene `[Fach]`-Fragen ab und traegt Antworten §6-konform nach — dasselbe Grundmuster
  (Input gegen Artefaktstand), aber **schreibend**. Der Unterschied, der die Read-only-Entscheidung
  traegt: `meeting-dump` schreibt in EINE Artefaktsorte mit EINEM kanonisierten Format, der
  Detektor muesste in drei mit drei verschiedenen Logiken schreiben. Bei `plan-review` gegenpruefen
  lassen.

**Reihenfolge:** Der Task `gitattributes-eol` beruehrt die kit-sync-Hashes; dieses Feature fuegt
eine neue Klasse-A-Datei hinzu und aendert den Lock ebenfalls. Kein Konflikt, aber nicht
gleichzeitig laufen lassen — sonst ist unklar, welche Hash-Aenderung woher kommt.

**Ideen-Bezuege** (ausserhalb des Change-Ordner-Scans): #35 komplementaer (Detektor VOR dem
Checkpoint vs. Auffangen beim Resume, wenn der Checkpoint gar nicht lief) · #44 gleiche Familie
„Zustand ohne Leser" · #34 traegt die hier ausgeschlossene Rechner-Divergenz.

---

## Offene Punkte

> **Stand 2026-08-06:** Die ersten vier Punkte sind in `spec.md` entschieden (Ausloeser,
> Name, Signalklassen, Unterdrueckungs-Schwelle). Sie bleiben hier als Herleitung stehen —
> massgeblich ist die Spec. Punkt 5 ist als Idee #46 erfasst.

- **Wann springt der Detektor an?** Er ist modellaufrufbar (3d), aber welches Signal gilt als
  „Session geht zu Ende"? Kandidaten: explizite Nutzeraeusserung („machen wir Schluss"), Aufruf von
  `/dtb:workflow-checkpoint`, laengere Inaktivitaet. Ohne belastbares Signal bleibt der Skill
  faktisch doch menschlich ausgeloest — und damit auf der Schwachstelle, die er schliessen soll.
  **Bezug INBOX #45 (2026-08-06):** „wo im Kit Claude-Code-Hooks passen" — ein Hook waere genau
  der fehlende Ausloeser. Vorbefund beachten: #35 hat einen SessionEnd-/Stop-Hook bereits als
  Option (d) **verworfen** (das Harness unterscheidet Session-Ende nicht von einer Pause; ein bei
  jedem Stop feuernder Hook wird ignoriert). Wer den Punkt aufgreift, muss gegen diesen Befund
  argumentieren, nicht an ihm vorbei.
- **Namens-Vorbehalt:** „Gate" verspricht eine Blockade, die der Skill bewusst nicht leistet
  (3b: empfehlend). Der Skill-Text muss die Strenge explizit machen, sonst entsteht genau die
  Prosa-Ungenauigkeit, gegen die #35 arbeitet.
- **Konkrete Heuristik-Signale:** Welche Chat-Muster gelten als Kandidat fuer Lektion / Fach-Frage /
  Idee? In 3a ist der zweistufige Mechanismus entschieden, nicht seine Fuellung.
- **Schwelle des unscharfen Vergleichs:** Ab welcher Stichwort-Ueberlappung gilt ein Fund als
  „bereits erfasst"? Zu streng erzeugt Dubletten, zu locker unterdrueckt echte Funde.
- **Halbseitige Pipeline-Kanten im Kit** (Nebenbefund dieser Discovery, gehoert nicht in dieses
  Feature): `open-question.next: [dtb:workflow-next, dtb:meeting-agenda]` steht einseitig — beide
  Ziele tragen `after: null`. Als eigene Idee erfassen.

---

**Erstellt mit:** `/dtb:feature-discover`
