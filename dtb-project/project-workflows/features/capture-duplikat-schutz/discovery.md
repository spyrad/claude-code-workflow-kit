# Discovery: Capture-Duplikat-Schutz
<!-- resume: done -->

**Erstellt:** 2026-08-19
**Idee-Referenz:** Inbox #48 — "Die drei Capture-Skills des Grundbestands haben keinen Duplikat-Schutz — `idea`, `task` und `bug-report` schreiben bedingungslos."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-idea/SKILL.md` | Haertungsziel 1 — schreibt bedingungslos in die INBOX-Tabelle (Schritt 2); `allowed-tools: Read, Write` (kein Grep, muss ergaenzt werden) |
| `skills/dtb-task/SKILL.md` | Haertungsziel 2 — Schritt 4 prueft nur Datei-Existenz (Slug), Schritt 5 schreibt BACKLOG; Inhalts-Dublette ungeprueft |
| `skills/dtb-bug-report/SKILL.md` | Haertungsziel 3 — identisch zu task; Symptom/Reproduktion als Vergleichsanker |
| `skills/CLAUDE.md` | Traeger der neuen Konvention; Zeilen 59-114 (Eligibility-Gates) als Formvorbild, 177-247 (Worktree-Guard/Kategorien) als Gegenvorbild |
| `skills/dtb-lesson/SKILL.md` | Vorlage: Stichwort-`grep` + weicher Hinweis + Ja/Abbrechen — Referenz, kein Umbau |
| `skills/dtb-open-question/SKILL.md` | Vorlage: exakter Textvergleich + warnen/ueberspringen — Referenz, kein Umbau |
| `skills/dtb-meeting-dump/SKILL.md` | Vorlage: Doppel-Lauf-Schutz (Z.121) + §6.1-Schutz (Z.204) — Referenz, kein Umbau |
| `skills/dtb-no-loss-check/SKILL.md` | **Wird geaendert (+1 Verweiszeile, Variante b):** die Ersetzungsprobe (Z.158-181) wird nach `skills/CLAUDE.md` gehoben, hier bleibt der Verweis + die skill-eigenen Beispiele; #48 steht dort als Beispielzeile |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §4 (Z.200-203) regelt Slug-Kollision, NICHT Inhalts-Dublette — Abgrenzung muss benannt werden |
| `dtb-project/project-workflows/INBOX.md` | Zielartefakt von `idea` — Tabellenformat bestimmt die Greppbarkeit |
| `dtb-project/project-workflows/BACKLOG.md` | Zielartefakt von `task`/`bug-report` — zweiter Kollisionsort |
| `skills/dtb-project-health/SKILL.md` | Nur lesend genutzt, **kein Umbau** — prueft `allowed-tools` gegen den Body (`:205-206`) und ist damit der mechanische Verifizierer der `idea`-Frontmatter-Aenderung |
| `CLAUDE.md` (Repo-Root) | Optional, niedrige Relevanz — nur falls die Konvention im Katalogtext erwaehnt werden soll |

---

## Anforderungen

### Scope
**Enthalten:**
- **Variante (a) — Konvention UND Umsetzung**, in der **Eligibility-Gates-Form** (`skills/CLAUDE.md:59-114`),
  nicht in der Worktree-Guard-Form: geteilte Mechanik zentral, pro Skill eine verbindliche
  Tabellenzeile mit dem konkreten Vergleichsziel. Begruendung: der Worktree-Guard ist
  byte-identisch kopierbar, weil sein Kern wortgleich ist (`git rev-parse`-Block); der
  Duplikat-Check ist es nicht — `idea` greppt eine INBOX-Tabellenzeile, `task`/`bug-report`
  greppen ueber `features/*/task.md` bzw. `BACKLOG.md`-Zeilen. Geteilt ist nur das
  Entscheidungs-Kriterium, die Meldeform und die Einteilungsregel.
- **Neue Konventions-Sektion in `skills/CLAUDE.md`** mit (1) Einteilungsregel mit mechanisch
  pruefbarem Kriterium (Vorbild: die `produces:`-Pruefung der Guard-Kategorien, "mechanisch
  pruefen, nie schaetzen"); Richtung akzeptiert: *schreibt einen vom Menschen formulierten
  Freitext-Eintrag in eine Sammel-Datei, ohne vorher eine Identitaet zu vergeben* — Wortlaut
  ist Feature-Arbeit; (2) Mechanik/Meldeform; (3) verbindliche Zuordnungstabelle.
- **Kopplungsregel Meldeform ↔ Vergleichsschaerfe** (entschieden):
  > Unscharfer Vergleich → **Treffer melden und fragen** (Ja/Abbrechen), nie selbst entscheiden.
  > Exakter Vergleich → **melden und ueberspringen** ist zulaessig, weil ein Falsch-Positiv
  > ausgeschlossen ist.
  Begruendung unabhaengig vom Bestand: ein unscharfer Vergleich hat Falsch-Positive per
  Konstruktion (die Ersetzungsprobe ist Ermessen, kein Messwert — `no-loss-check` begruendet
  genau deshalb, warum es keine Prozent-Schwelle gibt), ein Mechanismus der sich irren kann
  darf nicht allein entscheiden; ein exakter Vergleich hat keine Falsch-Positiven, die
  Rueckfrage waere Zeremonie. Nebeneffekt: die zwei abweichenden Meldeformen im Bestand
  (`lesson` fragt, `open-question` ueberspringt) werden dadurch *erklaert*, nicht geaendert.
- **Haertung der drei Skills** `idea`, `task`, `bug-report` nach dieser Konvention.
- **Eintragung aller sechs Capture-Skills in die Zuordnungstabelle** — auch der drei bereits
  geschuetzten, damit die Tabelle vollstaendig gelesen werden kann.

**Nicht enthalten:**
- **Kein Umbau** an `lesson`, `open-question`, `meeting-dump` — sie kommen nur in die
  Zuordnungstabelle; ihre bestehenden Formen werden durch die Kopplungsregel erklaert.
- **Kein hartes Blocken** — bei unscharfem Vergleich entscheidet immer der Mensch.
- **Keine Aenderung an §4 DERIVED_STATE_RULES** — Slug-Kollision bleibt unveraendert; nur die
  Abgrenzung "Namens-Kollision (§4, geregelt) vs. Inhalts-Dublette (neu)" wird benannt.
- **Kein Aufraeumen des Bestands** — vorhandene Dubletten in INBOX/BACKLOG werden nicht
  nachbearbeitet.

### Gewuenschtes Verhalten
- **Stoerungsfreiheit bleibt das Versprechen — kein Treffer, keine Ausgabe.** Alle drei Zielskills
  versprechen ausdruecklich Stoerungsfreiheit (`idea`: "Keine Rueckfragen, keine Ausarbeitung — nur
  speichern"; `task`/`bug-report`: "soll den Flow nicht unterbrechen — max. 1-2 Rueckfragen"). Der
  Check darf im Normalfall exakt nichts kosten: **kein** "Duplikat-Check: ok", keine
  Bestaetigungszeile. Wortlaut-Vorbild ist der Worktree-Guard (`skills/CLAUDE.md:214-217`: "der
  Guard ist im Normalfall unsichtbar — keine Bestaetigungszeile"). So muss das Versprechen in
  keinem der drei Skills relativiert werden.
- **Meldeform-Muster: die `lesson`-Form** (von #48 selbst als 1:1-Vorlage benannt), Beispiel `idea`:
  ```
  Aehnliche Idee steht schon in der INBOX (#48): "{Kurztext des Bestands}"
  Trotzdem als neuen Eintrag speichern? (Ja / Abbrechen)
  ```
- **Schema statt Wortlaut (kein byte-identischer Spiegel).** Die erste Zeile muss pro Skill
  abweichen (INBOX-Nummer vs. Change-Ordner-Pfad) — byte-identische Kopie ist unmoeglich, und
  jeder zusaetzliche woertliche Spiegel waere Wartungsschuld (L14 / Spiegel-Regel
  `skills/CLAUDE.md:305-319`). Die Konvention gibt daher ein **Meldeform-Schema mit benannten
  Slots** vor: Fundstelle → Bestandstext → Entscheidungsfrage. Jeder Skill fuellt es.
- **Grep-Anker `## Duplikat-Check`, bewusst OHNE Schritt-Nummer** — Begruendung analog
  Worktree-Guard ("eine zweite Null waere ambig"): `idea` hat 3 Schritte, `task`/`bug-report` je 6,
  `lesson` nennt es "Schritt 3", `open-question` faltet es in Schritt 4 ein. Eine feste Nummer kann
  es nicht geben. **Position:** nach der Erfassung, vor dem ersten Schreiben (anders als der
  Worktree-Guard, der ganz vorne sitzt — der Check braucht den erfassten Text).
- **Verifikation:** Grep auf den Anker `## Duplikat-Check`, Zielzahl = Anzahl Zeilen der
  Zuordnungstabelle mit Check-Pflicht (Spiegel-Regel: mechanisch verifizieren, nie im Fliesstext
  verlassen).

### Randfaelle
- **Suchraum: `archive/` bleibt AUSSEN (Variante a, entschieden).** Kit-konform
  (`meeting-agenda:66`, `meeting-dump:144`, `worker:64` schliessen `archive/` ebenfalls aus).
  Verworfen: (b) `bug-report` mit separatem Regressions-Hinweis — eigenes Feature, als Folge-Idee
  zu erfassen; (c) `archive/` einbeziehen — bricht mit drei bestehenden Skills und produziert viele
  Falsch-Positive, weil Wiederkehr bei Housekeeping-Tasks normal ist.
  **Bewusst akzeptierte Restluecke:** die Wiedererfassung einer schon umgesetzten Sache wird nicht
  erkannt — bei `idea` real belegt (#29 und #42 sind aus der INBOX verschwunden; ein erneutes
  `/dtb:idea` dazu liefe kommentarlos durch).
  **Befund fuer die Planung:** aktive Changes haben heute **0 `task.md` und 0 `bug.md`** (der ganze
  Bestand liegt im Archiv: 5 Tasks, 3 Bugs) — der Check hat fuer `task`/`bug-report` derzeit keinen
  natuerlichen Belegfall. Der E2E-Beleg braucht eine **angelegte** Test-Situation. Kein
  Konzeptfehler, ein Plan-Problem.
- **Wiederkehr ist legitim.** Housekeeping-Tasks ("Schema-Audit") und Regressions-Bugs wiederholen
  sich naturgemaess. Die Ja/Abbrechen-Form traegt das; die Konvention benennt es ausdruecklich,
  damit niemand spaeter "hart blocken" nachruestet.
- **Bestandstext kuerzen (Pflicht).** Laengste INBOX-Zeile: **5944 Zeichen** (#48 selbst > 3200).
  Erste ~120 Zeichen + `…`; der Anker im Hinweis ist die Nummer bzw. der Pfad, nicht der Text.
- **Fehlendes/leeres Ziel** (`INBOX.md` fehlt, `features/` leer) → Check **still uebersprungen**,
  kein Fehler, kein Hinweis. Fail-open wie `DURCHLASS-NOGIT` beim Guard; `no-loss-check` formuliert
  dasselbe als "Nie abbrechen, nie als Warnung melden".
- **Regex-Metazeichen im Freitext** (`(`, `*`, `[`) → literal vergleichen bzw. stichwortbasiert
  gehen, nicht ueber die Volltextzeile. Der unscharfe Vergleich laeuft ohnehin ueber Stichworte.
- **Mehrere Treffer** → kappen: max. 3 zeigen, Rest als "+N weitere".
- **Worktree ist ein Nicht-Fall** — alle drei Skills sind Voll-Guard und brechen ab, bevor der Check
  erreicht wird. Ausdruecklich als Nicht-Fall festhalten, damit die Konvention nicht doppelt guardet.
- **Reihenfolge bei `task`/`bug-report`:** Inhalts-Check **vor** der Slug-Vergabe (vor Schritt 3),
  nicht danach — bei erkanntem Duplikat braucht es gar keinen Namen mehr. Deckt sich mit der
  Position "nach Erfassung, vor erstem Schreiben".

### Einschraenkungen
**Technisch:**
- **`dtb:idea` hat `allowed-tools: Read, Write` — kein `Grep`.** Einziger der sechs Capture-Skills
  ohne Grep (`task`/`bug-report`: `Read, Write, Glob, Grep`; `lesson`: `Read, Write, Edit, Grep`;
  `open-question`: `Read, Glob, Grep, Edit`; `meeting-dump`: `Read, Glob, Grep, Edit, Write`). Der
  Check erfordert bei `idea` also eine **Frontmatter-Aenderung**, nicht nur Text.
- **Die Konvention wird NICHT verteilt.** `dtb:kit-sync` synct als Klasse A nur
  `skills/dtb-*/SKILL.md`, `agents/*.md`, `commands/dtb-*.md`, `output-styles/dtb-*.md`
  (`kit-sync:74-77`, Praefix-Klassenmuster `:151`) — `skills/CLAUDE.md` ist Contributor-Guide dieses
  Repos, kein Klasse-A-Artefakt. Die Konvention wirkt auf **Autorenschaft**; die Wirkung reist ueber
  die drei gehaerteten `SKILL.md` mit. Folge: drei Klasse-A-Hashes aendern sich → die
  Drift-Erkennung meldet die installierten Kopien, **`dtb:kit-sync` ist ein Abschluss-Schritt** des
  Features, kein Nebeneffekt.
- **Der Worktree-Guard-Block in `dtb-idea` bleibt unangetastet.** `dtb:idea` ist die benannte
  **Referenz-Instanz** des Guards (`skills/CLAUDE.md:206`) — bei Abweichung zur Vorlage gilt die
  Referenz-Instanz, jede Abweichung ist ein Befund. Die neue Sektion kommt NACH dem Guard, ohne
  dessen Bash-Block oder ⛔-Fence zu beruehren.
- **Kein Performance-Thema.** 33 INBOX-Eintraege, groesste Zeile 5944 Zeichen — die Einschraenkung
  ist Lesbarkeit (siehe Randfaelle: Bestandstext kuerzen), nicht Laufzeit.

**Fachlich:**
- Keine — keine Regulatorik, keine Business-Rule beruehrt. Einzige Sorgfaltspflicht: Beispiele in der
  Konvention stammen aus dem Kit selbst, keine internen Projektinhalte (dieses Repo geht auf
  oeffentliches GitHub).

### Integrationspunkte
- **Kanon der Ersetzungsprobe: Variante (b) — heben (entschieden).** Sie existiert heute genau einmal,
  inline in `dtb-no-loss-check/SKILL.md:158-181`; kein anderer Ort verweist darauf. Sie wird nach
  `skills/CLAUDE.md` gehoben (dort Kanon), `no-loss-check` bekommt eine **Verweiszeile** und behaelt
  seine skill-eigenen Beispiele. Begruendung: das Kit hat diesen Zug schon gemacht ("L7, L8 und L14
  nach `skills/CLAUDE.md` gehoben", Changelog 2026-07-31) und `dtb:lesson` empfiehlt das Heben
  dauerhafter Konventionen ausdruecklich. Verworfen: (a) Konvention verweist auf den Skill — ein
  Skill waere Kanon fuer eine Autoren-Konvention, der Verweis zeigt bergab; (c) eigenstaendig neu
  formulieren — zwei gepflegte Wortlaute, genau die L14-Schuld.
- **`dtb:project-health` ist der mechanische Verifizierer** der `idea`-Frontmatter-Aenderung: es
  prueft "Skill-Body referenziert `Write`/`Bash`, aber `allowed-tools` enthaelt es nicht → WARNUNG"
  (`:205-206`). Ein grep-basierter Check ohne Frontmatter-Nachzug faellt damit automatisch auf.
  Nur nutzen, kein Umbau.
- **Geprueft, kein Fall:** `dtb:task` Schritt 4b (INBOX-Herkunft) kollidiert nicht — ein aus einer
  Idee geroutetes Task ist textlich fast identisch mit dem INBOX-Eintrag, aber `task` vergleicht
  gegen `features/*/task.md`, nicht gegen die INBOX.
- **Geprueft, kein Fall:** `dtb:idea-review` bleibt unveraendert — profitiert (weniger Triage-Last),
  hat aber keine Kopplung; seine Lesestand-Pruefung betrifft Statusentscheidungen, nicht das Schreiben.
- **Geprueft, kein Fall:** der `pipeline:`-Block bleibt in allen drei Skills unveraendert
  (`stage/after/next/consumes/produces`) → keine Aenderung an `workflow-status`/`pipeline-graph`.
- **Geprueft, kein Fall:** `dtb:feature-fast` unberuehrt — sein Hard-Gate ist die **Existenz** eines
  INBOX-Eintrags, nicht dessen Eindeutigkeit.
- **Externe Abhaengigkeiten:** keine. Nur `git`/`grep`, beides in Gebrauch.

---

## Abhaengigkeiten

Stand `49e1b55` (2026-08-19). Bestehende Change-Ordner: 5 — `feature-fast`,
`feature-start-statusfeld`, `meeting-agenda`, `output-style-gezielt`, `pane-start`. **Alle fuenf
sind umgesetzt und reviewt** (Progress 11/11, 5/5, 5/5, 11/11, 8/8; `review.md` je vorhanden),
keiner in Arbeit.

- **Konflikte: keine gleichzeitige Bearbeitung.** Die `skills/CLAUDE.md`-Aenderungen der vier
  betreffenden Changes sind bereits in der Datei (374 Zeilen).
- **Ueberschneidung: `skills/CLAUDE.md` ist die heisseste Datei des Repos** — zuletzt heute geaendert
  (`aa8e321`, `cad078f` fuer `pane-start`), davor `herdr-worker-automation` und
  `parallele-sessions`. `git worktree list` zeigt nur den Haupt-Checkout und diesen Worktree, beide
  auf `49e1b55` — kein zweiter Feature-Worktree. **Restrisiko:** arbeitet die Orchestrator-Session
  im Haupt-Checkout parallel an `skills/CLAUDE.md`, entsteht beim Zusammenfuehren genau dort ein
  Konflikt. Einziges nennenswertes Abhaengigkeitsrisiko.
- **Zeilennummern-Bezuege sind aktuell, aber verderblich.** Die Belege dieser Discovery
  (`kit-sync:74-77`, `project-health:205-206`, `no-loss-check:158-181`,
  `skills/CLAUDE.md:59-114/195-247/305-319`) gelten fuer `49e1b55`. In der Spec besser ueber
  **Anker-Text** als ueber Zeilennummer verweisen; werden die fuenf fertigen Changes vorher
  archiviert oder nachgebessert, sind die Nummern neu zu pruefen.

---

## Offene Punkte

- Wortlaut der Einteilungsregel (Kriterium ist richtungsentschieden, Formulierung offen)
- **`dtb:impl-review` erfasst die Konvention nicht automatisch.** Es liest seine Regel-Dimension aus
  `{config.paths.rules}/` — dort liegt nur `DERIVED_STATE_RULES.md`; `skills/CLAUDE.md` wird nicht
  gelesen. Gilt heute schon fuer alle Mechanik-Regeln dort, ist also kein neues Problem — heisst
  aber: die Einhaltung haengt am Grep-Anker plus `dtb:project-health`, nicht am Review.
- **Folge-Idee zu erfassen (Orchestrator, nicht hier — `dtb:idea` ist Voll-Guard):**
  Regressions-Erkennung fuer `bug-report` — Treffer im `archive/` auf gleiches Symptom bei
  geschlossenem Bug ist kein Duplikat, sondern ein Regressions-Signal. Bewusst aus #48
  ausgeschlossen (Variante b verworfen).

---

**Erstellt mit:** `/dtb:feature-discover`
