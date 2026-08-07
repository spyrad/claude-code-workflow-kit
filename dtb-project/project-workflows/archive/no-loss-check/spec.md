# Feature: No-Loss-Check

**Erstellt:** 2026-08-06
**Ziel:** Vor dem Session-Ende erkennen, welches Wissen nur im Gespraechsverlauf lebt und in keinem Artefakt gelandet ist — und es mit fertig formulierten Erfassungs-Befehlen melden.
**Prioritaet:** Hoch
**Status:** Abgeschlossen <!-- explizit gesetzt 2026-08-07 durch dtb:archive; Abnahme 2026-08-06 (Beleg im Session-Log S3) -->

**Idee-Referenz:** INBOX #29 (2026-07-21, Titel dort historisch „No-Loss-Gate")
**Discovery:** `features/no-loss-check/discovery.md`

---

## Executive Summary

In einer Arbeitssitzung entstehen Lektionen, Fach-Fragen und Entscheidungen, die im Gespraech
fallen und dort auch bleiben — die Erfassungs-Skills (`dtb:lesson`, `dtb:open-question`,
`dtb:idea`) muss der Mensch von sich aus aufrufen, und genau daran scheitert es wiederholt.
Der No-Loss-Check vergleicht den Gespraechsverlauf gegen den Artefakt-Stand, meldet jedes
nicht persistierte Delta mit einer kopierfertigen Befehlszeile und gibt den Weg zum Checkpoint
frei, wenn nichts offen ist.

Er ist **empfehlend, nicht blockierend**: Er kann einen Checkpoint ohnehin nicht verhindern, und
ein Waechter, der sich in den Weg stellt, wird weggeklickt. Sein Wert liegt darin, die
Formulierungsarbeit abzunehmen — die Ausloesung bleibt beim Menschen.

---

## Scope / Abgrenzung

### Enthalten

- **Drei Sorten Delta**, jede mit eigenem Zielartefakt und eigenem Routing-Ziel:

  | Delta | Zielartefakt | Routing-Ziel |
  |---|---|---|
  | Lektion aufgetaucht | `project-rules/lessons.md` | `/dtb:lesson` |
  | Fach-Frage aufgetaucht | `features/*/{discovery,spec}.md` → `## Offene Punkte` | `/dtb:open-question` |
  | Idee/Entscheidung ohne Ablage | `INBOX.md` | `/dtb:idea` |

- **Zweistufige Erkennung:** Eine Heuristik ueber den Gespraechsverlauf erzeugt Kandidaten, der
  Abgleich gegen den Artefakt-Stand filtert bereits Erfasstes weg. Beide Haelften sind noetig —
  die Heuristik allein ist nicht reproduzierbar, der Abgleich allein findet nur bereits Benanntes.

- **Signalklassen je Delta-Sorte** (Entscheidung 2026-08-06). Was als Kandidat gilt, ist hier
  fachlich festgelegt; die konkrete Ausformulierung gehoert in `plan.md`:

  | Delta | Signalklassen (was den Verdacht ausloest) |
  |---|---|
  | Lektion | Ursachenbefund nach einem Fehlschlag · eine als allgemein erkannte Regel („kuenftig zuerst X pruefen") · eine Korrektur, die beim zweiten Mal Zeit gespart haette |
  | Fach-Frage | eine Frage, die im Gespraech gestellt und vertagt statt beantwortet wurde · ein bewusst offen gelassener Punkt ohne Zustaendigen |
  | Idee/Entscheidung | ein Verbesserungsvorschlag ohne INBOX-Eintrag · eine getroffene Festlegung, die in keinem Artefakt steht und beim naechsten Mal neu verhandelt wuerde |

- **Meldung mit fertig formuliertem Befehl je Fund:** pro Delta eine kopierfertige Zeile
  einschliesslich vorformuliertem Argument (z. B. `/dtb:lesson <fertige Formulierung>`).

- **Priorisierung statt Blockade:** Funde werden nach Verlustrisiko gruppiert und markiert, welche
  vor dem Checkpoint zwingend sind und welche warten koennen.

- **Sichtbare Unterdrueckung** (Entscheidung 2026-08-06): Der Abgleich vergleicht unscharf, weil
  der Check Funde neu formuliert und ein exakter Textvergleich dann nicht greift. Unterdrueckt
  wird nur bei hoher Uebereinstimmung — im Zweifel wird gemeldet. Die Zahl der als „bereits
  erfasst" gefilterten Kandidaten erscheint als **eine** Sammelzeile im Report, damit eine falsch
  kalibrierte Schwelle auffaellt statt still zu wirken.

- **Sensible Inhalte bleiben draussen** (Nachtrag 2026-08-06 aus dem Plan-Review): Zugangsdaten,
  Schluessel und personenbezogene Daten werden **nie woertlich** in eine Vorschlagszeile
  uebernommen — der Fund wird gemeldet, die heikle Stelle durch einen Platzhalter ersetzt.
  Zusaetzlich weist der Report je Fund aus, ob das Zielartefakt **versioniert** ist (`INBOX.md`,
  `features/*`) oder nicht (`lessons.md`), damit vor dem Absetzen sichtbar ist, wohin der Inhalt
  wandert. Anlass: der Check liest den gesamten Verlauf und ist damit der Trichter in Artefakte,
  die geteilt werden.

- **Zwei Ausloeser** (Entscheidung 2026-08-06):
  1. **Als Vorstufe des Checkpoints:** `dtb:workflow-checkpoint` ruft den Check zu Beginn seines
     Ablaufs auf. Das ist moeglich, weil der Check — anders als der Checkpoint selbst — nicht
     gegen Modell-Aufrufe gesperrt ist. Das ergibt die verlaessliche Untergrenze.
  2. **Modell-initiiert**, wenn ein Session-Ende oder ein Themenwechsel erkennbar ist. Das deckt
     den Fall ab, in dem gar kein Checkpoint mehr kommt — der eigentliche Verlustfall.

- **Freigabe im Leer-Fall:** Ist nichts offen, sagt der Check das in einer Zeile und verweist auf
  `/dtb:workflow-checkpoint`.

### Nicht enthalten

- **Selbst schreiben.** Der Check bleibt lesend. Sonst muesste er die Erfassungslogik der drei
  Ziel-Skills nachbauen (Ziel-Routung und §6-Formatierung bei `open-question`, fortlaufende
  Nummerierung bei `lesson`) — zwei Schreiber pro Artefakt ist genau die Kopplung, die am
  30./31.07. zweimal Folgefehler erzeugt hat.
- **Die Ziel-Skills selbst aufrufen.** `dtb:lesson`, `dtb:open-question`, `dtb:idea` und
  `dtb:workflow-checkpoint` sind alle gegen Modell-Aufrufe gesperrt — nur der Mensch startet sie.
- **Recap „was war".** Das ist `dtb:session-summary`. Der Check beantwortet die andere Frage:
  „was droht verloren zu gehen".
- **Rechner-Divergenz** (INBOX #29, offener Punkt 5 — entschieden: draussen). Auf der zweiten
  Maschine existiert kein Gespraech, in dem etwas fehlen koennte; sichtbar wird der Fall nur beim
  Abgleich mit dem entfernten Stand, also am Session-**Anfang** in `dtb:workflow-resume`, wo der
  Mechanismus bereits existiert. Thematisch gehoert das zu #34.
- **Der Checkpoint selbst.** Bleibt eigenstaendig; der Check sitzt davor.
- **Ein Hook als Ausloeser.** Verworfen mit dem Vorbefund aus #35 Option (d): das Harness
  unterscheidet Session-Ende nicht von einer Pause. Bleibt bei #45 aufgehoben.
- **Ein eigener Speicherort fuer Funde.** Funde leben im Report, nicht in einer Datei — sonst
  entstuende ein Artefakt, das veraltet und gepflegt werden muesste.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Kontext-Kompression macht die Heuristik blind — ausgerechnet in der langen Sitzung, in der am meisten auflaeuft | Hoch | Hoch | Transparent melden („Verlauf komprimiert — Erkennung unvollstaendig") und mehrfache Laeufe pro Sitzung empfehlen statt nur einen am Ende. Der Abgleich gegen den Artefakt-Stand bleibt unbeeintraechtigt |
| Heuristik meldet zu wenig — uebersehene Funde fallen niemandem auf | Mittel | Hoch | Recall vor Precision: im Zweifel melden. Kalibrierung an dokumentierten Verlustfaellen als Abnahmekriterium |
| Unscharfer Abgleich unterdrueckt echte Funde still | Mittel | Hoch | Unterdrueckung nur bei hoher Uebereinstimmung; Zahl der gefilterten Kandidaten als Sammelzeile sichtbar |
| Falsch-Positive nerven und entwerten den Report | Mittel | Niedrig | Bewusst akzeptiert: eine ueberlesene Zeile ist billiger als ein verlorener Befund. Gruppierung nach Verlustrisiko haelt den Kopf des Reports sauber |
| Der Check springt zur Unzeit an, weil er modellaufrufbar ist | Mittel | Niedrig | Er ist lesend und im Leer-Fall eine Zeile lang; der Schaden ist etwas unpassende Ausgabe |
| Kopplung ueber sechs Nachbardateien erzeugt Folgefehler | Mittel | Hoch | `dtb:plan-review` ist bei diesem Feature **nicht optional**. Die drei Routing-Kanten werden bewusst nicht als Pipeline-Kanten gesetzt |
| Der Aufruf aus dem Checkpoint laeuft ins Leere, wenn der Check im Zielprojekt nicht installiert ist | Mittel | Mittel | Der Aufruf muss weich sein: fehlt der Check, laeuft der Checkpoint unveraendert weiter und weist einzeilig darauf hin |
| Doppellauf, wenn der Check kurz vor dem Checkpoint schon einmal lief | Hoch | Niedrig | Innerhalb der Sitzung traegt das der Gespraechsverlauf; der zweite Lauf darf verworfene Funde nicht unveraendert wiederholen |
| Der Check hebt Zugangsdaten oder personenbezogene Daten aus dem Verlauf in eine Vorschlagszeile, die anschliessend in eine versionierte Datei geschrieben wird | Mittel | Hoch | Platzhalter statt woertlicher Uebernahme; der Report weist je Fund aus, ob das Ziel versioniert ist |
| Der Check wird nach einigen Sitzungen ueberlesen, weil er zu viel Rauschen meldet | Mittel | Hoch | Beim ersten echten Lauf wird die Fund-Rate festgehalten (wie viele Meldungen waren erfassenswert) — Grundlage fuer eine spaetere Verschaerfung der Schwelle |

---

## Dependencies

### Erforderlich vor Start

- [ ] Task `gitattributes-eol` **nicht gleichzeitig** laufen lassen — beide veraendern die
      Pruefsummen der Kit-Verteilung, sonst ist unklar, welche Aenderung woher kommt
- [ ] Stand der Kit-Verteilung auf dieser Maschine geklaert (`/dtb:kit-sync check`) — seit der
      Parallelarbeit widerspruechlich
- [x] Slug-Umbenennung `no-loss-gate` → `no-loss-check` vollzogen (2026-08-06, `git mv`)

### Referenz-Dokumente

- `features/no-loss-check/discovery.md` — Herleitung aller Scope-Entscheidungen, Randfaelle,
  Abhaengigkeits-Analyse
- `dtb-project/project-workflows/INBOX.md` — #29 (Ursprung), #35 (komplementaer: greift, wenn gar
  kein Checkpoint lief), #44 (gleiche Familie „Zustand ohne Leser"), #45 (Hook-Ausloeser),
  #48 (fehlender Duplikat-Schutz in drei Erfassungs-Skills)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — §6 regelt das Format der Fach-Fragen, die
  der Check als Delta erkennt
- `dtb-project/project-changelog/2026-07/` und `2026-08/` — Kalibrier-Menge: die dort
  dokumentierten Verlustfaelle sind der Massstab fuer die Erkennungsguete

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] **Kalibrierung:** Der Check erkennt an einer vorab benannten Menge dokumentierter
      Verlustfaelle aus den Changelogs jeweils den richtigen Delta-Typ. Die Menge wird in
      `plan.md` festgelegt und im Abnahmelauf gegengeprueft
- [ ] Jeder Fund traegt eine kopierfertige Befehlszeile mit vorformuliertem Argument — ohne dass
      der Mensch nachformulieren muss
- [ ] Funde sind nach Verlustrisiko gruppiert; zwingend vor dem Checkpoint ist von „kann warten"
      unterscheidbar
- [ ] Bereits erfasste Kandidaten werden herausgefiltert; ihre Zahl erscheint als eine Sammelzeile
- [ ] Leer-Fall: eine Zeile plus Freigabe zum Checkpoint, nichts weiter
- [ ] Der Check schreibt nichts — kein erzeugtes Artefakt, lesende Werkzeuge
- [ ] Keine Vorschlagszeile uebernimmt Zugangsdaten, Schluessel oder personenbezogene Daten
      woertlich; je Fund ist erkennbar, ob das Zielartefakt versioniert ist
- [ ] `dtb:workflow-checkpoint` ruft den Check zu Beginn auf; fehlt der Check im Projekt, laeuft
      der Checkpoint unveraendert weiter
- [ ] Fehlt jeder Ablage-Ort fuer eine Fach-Frage, wird der Fund in die INBOX umgeleitet — mit
      sichtbarem Vermerk, dass es urspruenglich eine Fach-Frage war
- [ ] Komprimierter Verlauf wird im Report offengelegt statt verschwiegen
- [ ] `dtb:plan-review` ist durchlaufen (bei diesem Feature nicht optional)
- [ ] Ein echter Lauf am Ende einer realen Arbeitssitzung hat mindestens einen Fund gemeldet, den
      der Mensch ohne ihn vergessen haette — oder glaubhaft bestaetigt, dass nichts offen war

---

## Offene Punkte

- Wie erkennt der Check beim Aufruf aus dem Checkpoint, dass er in derselben Sitzung bereits lief?
  Innerhalb der Sitzung traegt das der Gespraechsverlauf — verlaesslich ist das nicht, und ein
  Doppellauf mit identischem Report entwertet den zweiten.
- Wie genau wird der Aufruf im Checkpoint verankert, ohne dass dieser bei fehlendem Check bricht?
  Die weiche Variante ist entschieden, ihre Form noch nicht.
- Welche konkreten Verlustfaelle bilden die Kalibrier-Menge? Kandidaten stehen in den Changelogs
  vom 30./31.07. und 2026-08-06 (Beinahe-Dublette beim #35-Nachtrag) — die Auswahl gehoert in
  `plan.md`.
- Bewusst nach `plan.md` verschoben: der Schwellwert des unscharfen Vergleichs. Vor dem ersten
  Lauf laesst sich kein Wert begruenden.

---

**Erstellt mit:** `/dtb:feature-plan`
