# Implementierungsplan: No-Loss-Check

**Erstellt:** 2026-08-06
**Feature-Spec:** `features/no-loss-check/spec.md`
**Geschaetzte Dauer:** ca. 6 h Arbeitszeit (3 Phasen) — der echte Lauf am Sitzungsende ist
**kein** Plan-Schritt, sondern Abnahme-Kriterium der Phase 3 und wartet auf eine reale Sitzung
**Status:** Reviewed (plan-review 2026-08-06: REVISE → 7 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Vorabproben + Skill-Geruest + zweistufige Erkennung | ~3 h | Abgeschlossen (`110c208`) |
| Phase 2 | Report, Leer-Fall und Randfaelle | ~1,5 h | Abgeschlossen (`471a0e7`) |
| Phase 3 | Verdrahtung, Distribution, Kalibrierung | ~1,5 h | Abgeschlossen (`1110b09`, `926ec71`) |

---

## Ist-Analyse

> Quelle: `discovery.md` `## Betroffene Module`, Pfade am 2026-08-06 verifiziert. Der einzige
> fehlende Pfad ist das Neubau-Ziel selbst — nach Lektion 5 kein Scan-Ausloeser.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-no-loss-check/SKILL.md` | Existiert nicht — Neubau, Deliverable von Phase 1 |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 254 Zeilen. `after: [dtb:impl-review]`, `next: [dtb:workflow-resume]`, gesperrt gegen Modell-Aufruf. Ablauf beginnt bei `## Ausfuehrung` → `### Schritt 1: Informationen sammeln`; davor stehen nur Templates. Dort haengt der Aufruf ein |
| `skills/dtb-lesson/SKILL.md` | 176 Zeilen, `after: null`. Nimmt Freitext (`argument-hint: [Lektion als Freitext]`), strukturiert selbst in 4 Felder, Duplikat-Check ist ein weicher Grep auf `Rule`-Stichworte. Ziel-Datei `project-rules/lessons.md` (Spalte `Rule` = Abgleichsflaeche) |
| `skills/dtb-open-question/SKILL.md` | 171 Zeilen, `after: null`. `argument-hint: [<feature-slug>] <Fach-Frage>` — erstes Token wird nur als Slug erkannt, wenn es exakt einen nicht-leeren Feature-Ordner matcht. Duplikat-Schutz ist ein **exakter** Textvergleich (§6-Kanonform). Schritt 3 bricht weich ab, wenn weder `spec.md` noch `discovery.md` existiert |
| `skills/dtb-idea/SKILL.md` | 86 Zeilen, `after: null`. Freitext-Argument, **kein** Duplikat-Schutz (Beleg fuer #48). Schreibt Tabellenzeile in `INBOX.md` mit Status `Offen` |
| `skills/dtb-session-summary/SKILL.md` | 180 Zeilen, `disable-model-invocation: false`, `after: null`, `next: null`, `produces: []` — das Vorbild fuer den Contract des Checks. Braucht nur einen Abgrenzungs-Hinweis, keine Kante |
| `CLAUDE.md` | 115 Zeilen. Kategorie-Zeile „Session lifecycle" listet die Kette; dort wird der Check ergaenzt |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | 419 Zeilen. §6 definiert die Fach-Frage-Grammatik, gegen die der Abgleich liest. **Wird nicht geaendert** — der Check kanonisiert keine Ableitungsregel, also kein Seed-Skew nach #22 |

Zusaetzlich als Lesequelle (nicht als Aenderungsziel) verifiziert: `skills/CLAUDE.md` (Frontmatter-Pflichtfelder, Eligibility-Gate-Konvention, Distribution Klasse A).

---

## Phase 1: Skill-Geruest + zweistufige Erkennung

### Ziel

Der Skill existiert mit korrektem Contract und erzeugt aus einem Gespraechsverlauf eine
gefilterte Fund-Liste — die inhaltliche Haelfte des Features.

### Schritte

#### Schritt 1.0: Zwei Vorabproben, bevor gebaut wird
- **Zweck:** die tragende Annahme des Ausloesers pruefen, solange ein Fehlschlag noch nichts
  gekostet hat — und die Vergleichsgrundlage fuer das Phase-3-Gesundheitskriterium schaffen
- **Dateien:** keine (Messung; beide Ergebnisse in den Session-Log)
- **Input:** `/dtb:project-health` im Ist-Zustand; eine Wegwerf-Probe zur Frage, ob ein gegen
  Modell-Aufrufe **gesperrter** Skill in seinem Ablauf einen **ungesperrten** anstossen kann
- **Output:** (a) Baseline-Befundliste festgehalten (Vergleichswert fuer Phase 3), (b) belegte
  Antwort auf die Ausloeser-Frage. **Traegt die Annahme nicht**, bricht die Umsetzung hier ab —
  dann steht die Entscheidung an, auf die reine Modell-Erkennung zurueckzuschneiden oder auf
  Idee #45 (Hooks) zu warten. Der restliche Plan setzt ein positives Ergebnis voraus

#### Schritt 1.1: Skill-Datei mit Contract und Selbstbeschreibung
- **Zweck:** Rahmen setzen, bevor Logik entsteht; der Contract ist die Zusage „liest nur"
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md` (neu)
- **Input:** Contract-Vorgaben aus `spec.md` (lesend, nichts erzeugt, nicht gegen Modell-Aufruf
  gesperrt), Frontmatter-Pflichtfelder aus `skills/CLAUDE.md`, `session-summary` als Vorbild
- **Output:** Frontmatter (`stage: session`, `after: null`, `next: [dtb:workflow-checkpoint]`,
  `consumes: [workflow.config.yaml, project-rules/lessons.md, features/*/spec.md,
  features/*/discovery.md, INBOX.md]`, `produces: []`, `allowed-tools: Read, Glob, Grep`,
  `disable-model-invocation: false`), Kopfabschnitt mit **woertlicher Strenge-Aussage**
  („empfehlend — meldet und fragt einmal nach, blockiert den Checkpoint nicht") und Abgrenzung
  zu `dtb:session-summary`. **Kein Eligibility-Gate** (read-only, keine zwingende Eingabe).
  Zusaetzlich die **Vertraulichkeits-Regel** aus der Spec: Zugangsdaten, Schluessel und
  personenbezogene Daten werden nie woertlich in eine Vorschlagszeile uebernommen — der Fund
  wird gemeldet, die heikle Stelle durch einen Platzhalter ersetzt

#### Schritt 1.2: Erkennungsstufe 1 — Signalklassen
- **Zweck:** Kandidaten aus dem Gespraechsverlauf gewinnen, reproduzierbar beschrieben
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** die drei Delta-Sorten und ihre Signalklassen aus `spec.md` `## Scope`
- **Output:** Abschnitt „Stufe 1: Kandidaten erkennen" mit je Delta-Sorte den Signalklassen als
  Aufzaehlung, plus der Recall-Regel („im Zweifel melden") als ausdrueckliche Anweisung

#### Schritt 1.3: Erkennungsstufe 2 — Abgleich gegen den Artefakt-Stand
- **Zweck:** bereits Erfasstes herausfiltern, ohne echte Funde still zu verlieren
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** Ist-Befunde zu den drei Abgleichsflaechen — `lessons.md` Spalte `Rule`,
  `features/*/{spec,discovery}.md` innerhalb `## Offene Punkte` (`archive/` ausgeschlossen —
  urspruenglich nur `- [ ] [Fach]`-Zeilen, siehe die Nachschaerfung unten), `INBOX.md` Idee-Spalte
- **Output:** Abschnitt „Stufe 2: Abgleich" mit je Delta-Sorte Lesequelle und Vergleichsregel;
  **Schwellwert des unscharfen Vergleichs hier festgelegt** (technische Entscheidung 1) und
  begruendet; fehlende Datei = alles neu (kein Fehler)
- **Nachschaerfung 2026-08-06** (Kalibrier-Befund aus Schritt 3.4, im impl-review als F6
  nachgezogen): Der Fach-Fragen-Abgleich liest **alle** Inhaltszeilen innerhalb von
  `## Offene Punkte` — §6-Kanonform, beantwortete Form **und** untagged Bullets. Nur die
  Kanonform zu lesen hiesse, jede als normaler Bullet festgehaltene Frage bei jedem Lauf erneut
  zu melden (in diesem Projekt sofort 5 Falsch-Positive)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen (1.0 ist eine Messung
> vor dem Bau und zaehlt im Rhythmus nicht mit — die drei Bau-Schritte sind 1.1 bis 1.3)

### Deliverables
- [ ] Baseline-Befundliste und Ausloeser-Beleg im Session-Log (aus 1.0)
- [ ] `skills/dtb-no-loss-check/SKILL.md` mit Contract, Stufe 1 und Stufe 2

### Checkpoint-Kriterien

#### Automated
- [ ] Baseline aus 1.0 liegt im Session-Log vor (Befundliste, nicht nur „lief durch")
- [ ] `test -f skills/dtb-no-loss-check/SKILL.md`
- [ ] Frontmatter (Zeilen 1-25) enthaelt `produces: []` und `disable-model-invocation: false`
- [ ] Frontmatter enthaelt `next: [dtb:workflow-checkpoint]` (auf der `next:`-Zeile verankert,
      nicht dateiweit — Lektion 2)
- [ ] Grep `allowed-tools:`-Zeile: enthaelt weder `Write` noch `Edit` noch `Bash`
- [ ] Grep Abschnittsueberschriften: „Stufe 1" und „Stufe 2" beide vorhanden
- [ ] Grep im Stufe-2-Abschnitt: alle drei Lesequellen genannt (`lessons.md`, `## Offene Punkte`,
      `INBOX.md`)
- [ ] Grep Contract-Abschnitt: die Vertraulichkeits-Regel (Platzhalter statt woertlicher
      Uebernahme) ist vorhanden

#### Manual
- [ ] **Trockenlauf:** Stufe 1 und 2 sind an mindestens einem Fall der Kalibrier-Menge (siehe
      Schritt 3.4) von Hand durchgespielt; der in 1.3 gewaehlte Schwellwert ist daran plausibel.
      Faellt der Trockenlauf durch, wird 1.2/1.3 nachgeschaerft, bevor Phase 2 beginnt
- [ ] Die Signalklassen sind so formuliert, dass zwei Durchlaeufe ueber denselben Verlauf
      dieselben Kandidaten liefern wuerden — kein reines Bauchgefuehl
- [ ] Die Strenge-Aussage im Kopf ist unmissverstaendlich (Namens-Vorbehalt aus der Discovery)

---

## Phase 2: Report, Leer-Fall und Randfaelle

### Ziel

Aus der Fund-Liste wird eine Ausgabe, die Arbeit abnimmt statt Arbeit zu machen — und die ihre
eigenen Grenzen offenlegt.

### Schritte

#### Schritt 2.1: Report-Format mit kopierfertigen Befehlen
- **Zweck:** die Formulierungsarbeit erledigen; nur so ist der Fund billiger als das Vergessen
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** die realen Argument-Formen der drei Ziel-Skills aus der Ist-Analyse —
  `/dtb:lesson <Freitext>`, `/dtb:open-question <slug> "<Frage>"` (Slug ist **unbedingt** Pflicht:
  ohne ihn bricht `open-question` bei 0 aktiven Features ab und fragt bei >1 zurueck — der Befehl
  waere dann nicht ohne Nacharbeit absetzbar), `/dtb:idea <Freitext>`
- **Output:** Report-Abschnitt: zwei Gruppen („vor dem Checkpoint erledigen" / „kann warten"),
  je Fund eine Zeile mit fertig formuliertem Befehl; **eine** Sammelzeile fuer unterdrueckte
  Kandidaten (`{N} Kandidaten als bereits erfasst gefiltert`); je Fund die Kennzeichnung, ob das
  Zielartefakt **versioniert** ist (`INBOX.md`, `features/*`) oder nicht (`lessons.md`) — damit
  vor dem Absetzen sichtbar ist, wohin der Inhalt wandert

#### Schritt 2.2: Leer-Fall und Freigabe
- **Zweck:** der Normalfall ist „nichts gefunden" — ein teurer Leerlauf wird uebersprungen
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** Vorbild `idea-review` („Keine offenen Ideen in der Inbox. Alles aufgeraeumt.")
- **Output:** Leer-Fall-Abschnitt: eine Zeile plus Verweis auf `/dtb:workflow-checkpoint`,
  ausdrueckliches Verbot einer laengeren Ausgabe

#### Schritt 2.3: Drei Randfaelle
- **Zweck:** die bekannten Grenzen sichtbar machen, statt sie zu verschweigen
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** Randfaelle aus `discovery.md` und `spec.md`
- **Output:** (a) **Kontext-Kompression** — erkennbar komprimierter Verlauf wird gemeldet
  („Erkennung unvollstaendig, frueherer Lauf empfohlen"), (b) **kein Ablage-Ort fuer eine
  Fach-Frage** — vor dem Vorschlag pruefen, ob das Ziel-Feature `spec.md`/`discovery.md` hat;
  sonst Umleitung auf `/dtb:idea` mit sichtbarem Vermerk „urspruenglich Fach-Frage",
  (c) **zweiter Lauf in derselben Session** — bewusst verworfene Funde nicht unveraendert
  wiederholen

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Report-, Leer-Fall- und Randfall-Abschnitte im Skill

### Checkpoint-Kriterien

#### Automated
- [ ] Grep im Report-Abschnitt: alle drei Befehlsformen woertlich vorhanden (`/dtb:lesson`,
      `/dtb:open-question`, `/dtb:idea`)
- [ ] Grep im Report-Abschnitt: die Sammelzeile fuer gefilterte Kandidaten ist als Pflichtbestandteil
      benannt
- [ ] Grep: beide Prioritaets-Gruppen als feste Ueberschriften vorhanden
- [ ] Grep Randfall-Abschnitt: die drei Faelle Kompression, fehlender Ablage-Ort, Zweitlauf je
      einmal benannt
- [ ] Grep: die `/dtb:open-question`-Beispielzeile enthaelt einen Slug-Platzhalter vor der Frage
      (ohne Slug leitet `open-question` das Ziel aus dem aktiven Feature ab — bei 0 aktiven
      bricht es ab, bei >1 fragt es zurueck; der Befehl waere dann nicht ohne Nacharbeit
      absetzbar. Korrigiert 2026-08-06 im impl-review, Finding F3)
- [ ] Grep Report-Abschnitt: die Versioniert-Kennzeichnung je Fund ist als Pflichtbestandteil
      benannt

#### Manual
- [ ] Ein Beispiel-Report ist an einem echten Gespraechsausschnitt gelesen worden und liest sich
      handlungsfaehig — Befehle waeren ohne Nacharbeit absetzbar

---

## Phase 3: Verdrahtung, Distribution, Kalibrierung

### Ziel

Der Check ist im Kit verankert, verteilt und an dokumentierten Verlustfaellen gemessen.

### Schritte

#### Schritt 3.1: Verankerung im Checkpoint (beide Richtungen)
- **Zweck:** die verlaessliche Untergrenze des Ausloesers herstellen
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Ist-Befund — der Ablauf beginnt bei `## Ausfuehrung` → `### Schritt 1: Informationen
  sammeln`; der Check ist nicht gegen Modell-Aufrufe gesperrt und darf daher von dort angestossen
  werden
- **Output:** (a) neuer Ablauf-Schritt vor „Informationen sammeln", der den Check aufruft —
  **weich**: fehlt der Skill im Projekt, laeuft der Checkpoint unveraendert weiter und weist
  einzeilig darauf hin; (b) Frontmatter-Gegenkante `after: [dtb:impl-review, dtb:no-loss-check]`

#### Schritt 3.2: Nachbarschaft und Doku
- **Zweck:** Kopplungs-Hinweise im selben Zug mitziehen, statt sie liegen zu lassen
- **Dateien:** `skills/dtb-session-summary/SKILL.md`, `CLAUDE.md`
- **Input:** Lektion 3 — Uebersichts-Skills referenzieren Pipeline-Schritte ausserhalb der
  Frontmatter; vor dem Umbau repo-weit nach dem Skill-Namen greppen
- **Output:** Abgrenzungs-Hinweis in `session-summary` (Recap „was war" vs. Check „was droht
  verloren zu gehen", **keine** Kante); Ergaenzung der Session-lifecycle-Zeile in `CLAUDE.md`;
  Ergebnis des repo-weiten Greps ausgewertet und ggf. nachgezogene Fundstellen dokumentiert

#### Schritt 3.3: Distribution
- **Zweck:** der Skill muss dort liegen, wo er gebraucht wird
- **Dateien:** keine Repo-Datei — `~/.claude/` und `~/.claude/dtb-lock.json`
- **Input:** `/dtb:kit-sync` in der dort festgelegten Kommando-Sequenz (Lektion 7: nicht
  improvisieren, keine eigenen Hash-Methoden)
- **Vorbedingung (hartes Gate, Lektion 7):** Vor der Auswertung mechanisch belegen, dass **alle
  drei** Vergleichsseiten gefuellt sind (Repo, Lock, installierte Kopie — Zeilenzahl > 0). Ist
  eine Seite leer oder der Stand dieser Maschine unklar (offene Aufgabe: S4 meldete
  43/43 @ `71b6404`, die andere Maschine notierte `18a92da`), **abbrechen** mit
  „Werkzeug-Fehlschlag, kein Datenbefund" — nicht weiterarbeiten und nicht improvisieren
- **Output:** Skill unter `~/.claude/skills/` installiert, im Lock als `synced` gefuehrt;
  Klasse-A-Muster greift ohne Registrierung

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Kalibrierung gegen die festgelegte Fall-Menge
- **Zweck:** belegen, dass der Check das Richtige findet — nicht nur, dass er etwas findet
- **Dateien:** keine (Auswertung; Ergebnis in den Session-Log)
- **Input:** die **hier verbindlich festgeschriebene** Kalibrier-Menge (Festlegung 2026-08-06 im
  Plan-Review — bewusst vor der Auswertung, nicht waehrend):

  | # | Fall (Quelle) | Soll-Ergebnis |
  |---|---------------|---------------|
  | 1 | `#35`-Ursachenbefund 2026-08-06: Checkpoint liest Git in Schritt 1, schreibt in 3/4 | Lektion |
  | 2 | Vollscan-Befund `#46` (sechs halbseitige Pipeline-Kanten) | Idee ohne Ablage |
  | 3 | Vollscan-Befund `#48` (3 von 6 Capture-Skills ohne Duplikat-Schutz) | Idee ohne Ablage |
  | 4 | Vertagte Frage „Wann springt der Detektor an?" (Discovery no-loss-check) | Fach-Frage |
  | 5 | Der `#35`-Nachtrag, **nachdem** er in der INBOX stand (Beinahe-Dublette 2026-08-06) | **Nicht** melden → erscheint in der Sammelzeile |

  Fall 5 ist der Gegen-Test: er prueft Stufe 2 (Abgleich). Ohne ihn misst die Kalibrierung nur,
  ob der Check etwas findet — nicht, ob er Bekanntes korrekt weglaesst
- **Output:** je Fall dokumentiert, ob der Check den richtigen Delta-Typ gemeldet haette bzw.
  Fall 5 korrekt unterdrueckt haette; Abweichungen benannt, nicht wegerklaert

### Deliverables
- [ ] Checkpoint ruft den Check auf, Gegenkante gesetzt
- [ ] Abgrenzungs-Hinweis, `CLAUDE.md`-Eintrag, Grep-Ergebnis ausgewertet
- [ ] Skill verteilt und im Lock gefuehrt
- [ ] Kalibrier-Ergebnis je Fall der Fall-Menge dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] Grep `skills/dtb-workflow-checkpoint/SKILL.md`: `dtb:no-loss-check` steht auf der
      `after:`-Zeile der Frontmatter (auf die Zeile verankert, nicht dateiweit — Lektion 2)
- [ ] Grep `skills/dtb-workflow-checkpoint/SKILL.md` im `## Ausfuehrung`-Block: der Aufruf steht
      **vor** „Schritt 1: Informationen sammeln" und nennt das Weiterlaufen bei fehlendem Skill
- [ ] Grep `skills/dtb-session-summary/SKILL.md`: Abgrenzungs-Hinweis vorhanden **und** die
      Frontmatter-Zeilen `after:`/`next:` unveraendert `null` (Gegenprobe: keine versehentliche Kante)
- [ ] Grep `CLAUDE.md` Session-lifecycle-Zeile: enthaelt `no-loss-check`
- [ ] Repo-weiter Grep `no-loss-check` ausgefuehrt; jede Fundstelle ausserhalb der geplanten
      Dateien ist entweder nachgezogen oder als bewusst unveraendert vermerkt
- [ ] `/dtb:kit-sync check`: alle drei Vergleichsseiten gefuellt (Gate aus 3.3), danach
      `dtb-no-loss-check` im Lock, Status `synced`, kein Drift
- [ ] `/dtb:project-health`: **keine Regression** gegenueber der in **Schritt 1.0** erhobenen
      Baseline. Bauartbedingte Befunde sind zulaessig und im Session-Log zu begruenden — konkret
      der Anzeige-Drift, den ein frisch fertiggestelltes Feature bis zum naechsten
      `workflow-checkpoint` zwangslaeufig erzeugt. Ein Kriterium, das diesen Fall verbietet,
      waere dauerhaft rot (belegt: Vergleichslauf 7/5/0 gegen Baseline 8/4/0)

#### Manual
- [ ] Kalibrierung: der Check haette an den Faellen 1-4 jeweils den richtigen Delta-Typ gemeldet
      und Fall 5 unterdrueckt — abweichende Faelle sind benannt, nicht wegerklaert
- [ ] **Abnahme-Kriterium (wartet auf eine reale Sitzung, kein Plan-Schritt):** Ein echter Lauf
      am Sitzungsende hat einen Fund gemeldet, der sonst vergessen worden waere — oder glaubhaft
      bestaetigt, dass nichts offen war
- [ ] **Abnahme-Kriterium:** Fund-Rate des ersten echten Laufs festgehalten (wie viele der
      gemeldeten Funde waren tatsaechlich erfassenswert, z.B. „3 von 5") — Grundlage fuer eine
      spaetere Entscheidung ueber eine schaerfere Schwelle
- [ ] Der Aufruf aus dem Checkpoint hat sich im Lauf nicht als stoerend erwiesen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Schwellwert des unscharfen Vergleichs | A: Ueberlappung der Inhaltswoerter oberhalb einer festen Quote · B: Kern-Stichwort muss vorkommen · C: **Ersetzungsprobe** (koennte der Bestandseintrag den Kandidaten ohne Informationsverlust ersetzen?) | **C — entschieden 2026-08-06 in Schritt 1.3** | Eine Prozent-Quote suggeriert eine Messbarkeit, die ein Prompt-Skill nicht einloest — zwei Laeufe zaehlen Inhaltswoerter unterschiedlich. Die Ersetzungsprobe ist bei jedem Lauf gleich stellbar und vom Menschen nachvollziehbar; die asymmetrische Tie-break-Regel („nicht klar ja → melden") macht die Richtung deterministisch |
| Doppellauf in derselben Session | A: nur ueber den Gespraechsverlauf · B: der Check nennt im Report seinen eigenen vorherigen Lauf · C: gar nicht behandeln | **A+B — entschieden 2026-08-06 in Schritt 2.3** | Zwei Regeln: der eigene frueherer Report ist nie Kandidatenquelle (sonst Selbstvergiftung), und ein erkannter Zweitlauf wird im Report-Kopf ausgewiesen |
| Form der Verankerung im Checkpoint | A: eigener Ablauf-Schritt vor „Informationen sammeln" · B: Zeile innerhalb von Schritt 1 · C: nur Hinweis in der Abschluss-Bestaetigung | **A** | C kommt zu spaet (nach dem Schreiben), B versteckt den Aufruf in einem Sammel-Schritt. A ist die einzige Stelle, an der ein Fund den Checkpoint-Inhalt noch beeinflussen kann |
| Verhalten bei fehlendem Check im Zielprojekt | A: Checkpoint bricht ab · B: Checkpoint laeuft weiter mit Hinweis · C: stilles Ueberspringen | **B** | A macht den Checkpoint von einem empfehlenden Skill abhaengig — das widerspricht seiner Strenge. C verschweigt eine Luecke, dasselbe Muster wie #35 |
| Kalibrier-Menge | A: im Plan festschreiben · B: zu Beginn von 3.4 · C: waehrend der Auswertung | **A — erledigt (Plan-Review 2026-08-06, Tabelle in Schritt 3.4)** | Wer die Faelle waehlt, nachdem er die Ergebnisse kennt, misst nichts. Die Spec verlangt die Festlegung ausdruecklich im Plan |
| Umgang mit sensiblen Verlaufsinhalten | A: Platzhalter + Versioniert-Kennzeichnung · B: nur Platzhalter · C: nicht behandeln | **A (Spec-Nachtrag 2026-08-06)** | Der Check ist der Trichter vom Verlauf in geteilte Artefakte; `/dtb:idea` schreibt ungefiltert in eine versionierte Datei |
| Echter Lauf am Sitzungsende | A: eigener Plan-Schritt · B: Manual-Abnahmekriterium | **B** | Der Lauf wartet auf ein Ereignis und ist nicht planbar. Als Abnahmekriterium greift die Beleg-Rueckfrage von `dtb:workflow-checkpoint`, ohne dass eine Progress-Zeile ohne SHA haengt |
| Pipeline-Kanten zu den drei Ziel-Skills | A: `after`-Kanten setzen · B: bewusst weglassen | **B (aus der Discovery uebernommen)** | Die drei sind Capture-Tools ohne feste Vorstufe; eine Kante wuerde in `pipeline-graph` und `workflow-status` eine Reihenfolge zeichnen, die es nicht gibt |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.0 Vorabproben (Baseline + Ausloeser) — `110c208`
- [x] 1.1 Skill-Datei mit Contract — `110c208`
- [x] 1.2 Signalklassen (Stufe 1) — `110c208`
- [x] 1.3 Abgleich + Schwellwert (Stufe 2) — `110c208`
- [x] 2.1 Report mit kopierfertigen Befehlen — `471a0e7`
- [x] 2.2 Leer-Fall + Freigabe — `471a0e7`
- [x] 2.3 Drei Randfaelle — `471a0e7`
- [x] 3.1 Verankerung im Checkpoint — `1110b09`
- [x] 3.2 Nachbarschaft + Doku — `1110b09`
- [x] 3.3 Distribution (kit-sync) — `926ec71`
- [x] 3.4 Kalibrierung gegen die Fall-Menge — `926ec71`

---

## Umsetzung

Umsetzung mit `/dtb:implement no-loss-check` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/no-loss-check/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

**Reihenfolge-Vorbehalt aus der Spec:** nicht parallel zum Task `gitattributes-eol` umsetzen —
beide veraendern die Pruefsummen der Kit-Verteilung. Der unklare kit-sync-Stand dieser Maschine
blockiert Schritt 3.3 ueber dessen hartes Gate; er muss nicht vorab geloest, aber dort sichtbar
werden.

**Abbruchpunkt:** Schritt 1.0 ist bewusst der erste. Faellt die Ausloeser-Probe negativ aus,
endet die Umsetzung dort — der Rest des Plans setzt ein positives Ergebnis voraus.

---

**Erstellt mit:** `/dtb:impl-plan`
