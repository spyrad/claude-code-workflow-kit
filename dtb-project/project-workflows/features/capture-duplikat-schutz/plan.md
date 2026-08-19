# Implementierungsplan: Capture-Duplikat-Schutz

**Erstellt:** 2026-08-19
**Feature-Spec:** `features/capture-duplikat-schutz/spec.md`
**Geschaetzte Dauer:** 3-3,5 h (3 Phasen)
**Status:** Reviewed (plan-review 2026-08-19: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Kanon: Ersetzungsprobe heben + Konventions-Sektion in `skills/CLAUDE.md` | 60-75 min | Geplant |
| Phase 2 | Haertung der drei Capture-Skills + mechanische Selbstpruefung | 60-75 min | Geplant |
| Phase 3 | Belege (Mechanik gegen echte Daten) + Uebergabe an den Orchestrator | 45-60 min | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` → `## Betroffene Module`, alle 13 Pfade per Glob verifiziert (Stand `49e1b55`).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-idea/SKILL.md` | 121 Zeilen. `allowed-tools: Read, Write` — **keine Stichwort-Suche deklariert**. Schritt 1 erfasst, Schritt 2 schreibt bedingungslos. Traegt den Worktree-Guard als **Referenz-Instanz** |
| `skills/dtb-task/SKILL.md` | 222 Zeilen. `allowed-tools: Read, Write, Glob, Grep`. Schritt 3 vergibt Slug, Schritt 4 prueft nur Datei-Existenz, Schritt 5 schreibt `BACKLOG.md` |
| `skills/dtb-bug-report/SKILL.md` | 202 Zeilen. Werkzeuge wie `task`. Struktur identisch: Schritt 3 Slug, Schritt 4 Datei, Schritt 5 Backlog |
| `skills/CLAUDE.md` | 374 Zeilen, 20 Sektionen. `## Eligibility-Gates` (Formvorbild), `## Parallele Sessions` mit `### Worktree-Guard (kanonische Vorlage)`, `### Kopplungs-Hinweise: Spiegel mitziehen und verifizieren`. Heisseste Datei des Repos |
| `skills/dtb-lesson/SKILL.md` | „Schritt 3: Duplikat-Check" — Stichwort-Suche, weicher Hinweis, „Trotzdem speichern? (Ja/Abbrechen)", ausdruecklich „nicht hart blocken" |
| `skills/dtb-open-question/SKILL.md` | Schritt 4 Punkt 2 — exakter Textvergleich ueber `spec.md` UND `discovery.md`, „warnen und ueberspringen", „nur exakter Vergleich — kein Fuzzy-Matching" |
| `skills/dtb-meeting-dump/SKILL.md` | Zwei Schutzstellen: Doppel-Lauf-Schutz (identischer Dump-Text) und §6.1 „je Meeting einer" im Frage-Block |
| `skills/dtb-no-loss-check/SKILL.md` | `### Die Unterdrueckungs-Regel: Ersetzungsprobe` — der zu hebende Kanon, inkl. Beispieltabelle (Zeile mit `#48`) und der Begruendung gegen eine Prozent-Schwelle |
| `skills/dtb-project-health/SKILL.md` | Prueft „Skill-Body referenziert `Write`/`Bash`, aber Werkzeug nicht deklariert → WARNUNG" und gibt eine Konsistenz-Quote aus |
| `skills/dtb-kit-sync/SKILL.md` | Klassen-Tabelle: Klasse A = `skills/dtb-*/SKILL.md`, `agents/*.md`, `commands/dtb-*.md`, `output-styles/dtb-*.md`. **`skills/CLAUDE.md` ist NICHT Klasse A.** Kein Worktree-Guard vorhanden |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §4 „Eindeutigkeit / Kollision" regelt die **Namens**-Kollision (Abbruch, kein Auto-Suffix). Inhalts-Dublette ungeregelt |
| `dtb-project/project-workflows/INBOX.md` | 33 Eintraege, Tabellenform `\| # \| Datum \| Idee \| Status \|`. Laengste Zeile **5944 Zeichen** — Kuerzung im Hinweis ist Pflicht |
| `dtb-project/project-workflows/BACKLOG.md` | Sektionen „Aktive Features", „Aufgaben", „Ideen / Backlog". Aktive Changes tragen **0 `task.md` und 0 `bug.md`** (Bestand nur im Archiv: 5 + 3) |
| `CLAUDE.md` (Repo-Root) | Skill-Katalog. Beruehrung nur optional (Katalogtext), nicht Teil der Pflicht-Schritte |

---

## Phase 1: Kanon

### Ziel

Die Regel hat genau eine kanonische Fassung an der richtigen Stelle: die Ersetzungsprobe als Kanon
in `skills/CLAUDE.md` (mit deklariertem Laufzeit-Spiegel in `no-loss-check`), und darauf aufbauend
eine Konventions-Sektion, die Einteilung, Meldeform, Zuordnung und Laufzeit-Autarkie verbindlich
festlegt. Nach dieser Phase ist die Regel vollstaendig — auch ohne dass ein einziger Skill schon
gehaertet waere.

### Schritte

#### Schritt 1.1: Ersetzungsprobe nach `skills/CLAUDE.md` heben (Kanon + deklarierter Spiegel)
- **Zweck:** Den Kanon dorthin bringen, wo Autoren-Konventionen leben — OHNE die Laufzeit-Autarkie
  des installierten Skills zu brechen. **Autarkie-Anforderung (Review-Befund):** `no-loss-check` ist
  Klasse A und laeuft installiert in Zielprojekten, wo `skills/CLAUDE.md` nicht existiert — ein
  Verweis ersetzt die Regel zur Laufzeit nicht. Muster ist der Worktree-Guard: kanonische Vorlage im
  Contributor-Guide, vollstaendige operative Fassung im Skill, Spiegel-Verifikation dazwischen
- **Dateien:** `skills/CLAUDE.md` (neue Kanon-Stelle), `skills/dtb-no-loss-check/SKILL.md`
  (behaelt operative Fassung, wird deklarierter Spiegel)
- **Input:** `### Die Unterdrueckungs-Regel: Ersetzungsprobe` aus `no-loss-check` — die
  Schwellen-Formulierung („gleicher Gegenstand UND gleiche Aussage", „im Zweifel melden") und die
  Begruendung gegen eine Prozent-Schwelle
- **Output:** Kanon-Fassung in `skills/CLAUDE.md` (verbindlicher Wortlaut + Begruendung); in
  `no-loss-check` bleibt die **vollstaendige operative Fassung** samt skill-eigenen Beispielen und
  skill-spezifischer Richtung — neu ist dort nur der Spiegel-Hinweis auf den Kanon.
  **Beide Stellen tragen einen Kopplungs-Hinweis in je ihre Richtung** („Aenderung hier → Spiegel
  mitziehen", Spiegel-Regel). Verifikation: Suche nach dem Kern-Wortlaut der Probe trifft **genau
  zwei** deklarierte Stellen (Kanon + Spiegel), keine dritte

#### Schritt 1.2: Konventions-Sektion anlegen — Einteilung, Kopplung, Meldeform
- **Zweck:** Die drei Teile, die skill-uebergreifend gelten, einmal verbindlich formulieren
- **Dateien:** `skills/CLAUDE.md`
- **Input:** Form der Sektion `## Eligibility-Gates` (Einteilungsregel + Mechanik + Zuordnung);
  Scope-Block der Spec
- **Output:** Neue Sektion mit fuenf Bestandteilen: (a) **Einteilungsregel** mit mechanisch pruefbarem
  Kriterium in der Richtung *erfasst einen vom Menschen formulierten Freitext-Eintrag in eine
  Sammel-Datei, ohne vorher eine Identitaet zu vergeben* — scharf genug, um ohne Ermessen ueber einen
  neuen Skill zu entscheiden; (b) **Kopplungsregel** Meldeform ↔ Vergleichsschaerfe im Wortlaut der
  Spec; (c) **Meldeform-Schema** mit benannten Slots (Fundstelle → gekuerzter Bestandstext →
  Entscheidungsfrage) plus Kuerzungs-Regel (~120 Zeichen + Auslassungszeichen) und Kappung bei drei
  Treffern; (d) **Abgrenzung** Namens-Kollision (§4, geregelt) vs. Inhalts-Dublette (neu), inklusive
  des Hinweises, dass beide gleichzeitig auftreten koennen; (e) **Laufzeit-Autarkie:** jeder
  Capture-Skill traegt alles zur Laufzeit Noetige (Kriterium, Suchraum, Meldeform) **inline** —
  installierte Skills laufen in Zielprojekten ohne `skills/CLAUDE.md`; Verweise auf die Konvention
  sind Autoren-Doku, nie Laufzeit-Pfad
- Zusaetzlich: die Aussage „kein Treffer → keine Ausgabe" und „Wiederkehr ist legitim, niemals hart
  blocken" gehoeren in diese Sektion, nicht in die Einzelskills

#### Schritt 1.3: Zuordnungstabelle + Grep-Anker festlegen
- **Zweck:** Die Konvention pruefbar machen. Ohne Zuordnungstabelle und Anker bleibt sie Fliesstext —
  genau der Fehler, den die Spiegel-Regel als Praxisfall dokumentiert
- **Dateien:** `skills/CLAUDE.md`
- **Input:** Die sechs Capture-Skills mit ihrem jeweiligen Ist-Zustand aus der Ist-Analyse
- **Output:** Tabelle mit **allen sechs** Skills, je Zeile: Skill · Vergleichsziel (konkreter
  Suchraum) · Vergleichsschaerfe · daraus folgende Meldeform · Anker vorhanden ja/nein. Die drei
  bestehenden Formen (`lesson` unscharf/fragen, `open-question` exakt/ueberspringen, `meeting-dump`
  exakt/ueberspringen) muessen von der Kopplungsregel **erklaert** werden — tut sie das an einer
  Zeile nicht, ist das ein Befund und die Regel ist falsch, nicht der Bestand. Ausserdem: Ankerzeile
  `## Duplikat-Check` als Grep-Anker definiert, mit Zielzahl = Anzahl Zeilen mit Check-Pflicht, und
  die Begruendung fuer „ohne Schritt-Nummer"

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Ersetzungsprobe als Kanon in `skills/CLAUDE.md`; `no-loss-check` behaelt die operative Fassung
      als deklarierter Spiegel (Kopplungs-Hinweise in beide Richtungen)
- [ ] Konventions-Sektion mit Einteilungsregel, Kopplungsregel, Meldeform-Schema, Abgrenzung zu §4,
      Laufzeit-Autarkie
- [ ] Zuordnungstabelle mit sechs Skills + definierter Grep-Anker und Zielzahl

### Checkpoint-Kriterien

#### Automated
- [ ] Suche nach dem Kern-Wortlaut der Ersetzungsprobe trifft in `skills/` **genau zwei** deklarierte
      Stellen: Kanon (`skills/CLAUDE.md`) und Spiegel (`dtb-no-loss-check`), keine dritte
- [ ] Beide Stellen tragen den Kopplungs-Hinweis in je ihre Richtung (Suche nach dem Hinweis-Anker =
      2 Treffer); die Beispieltabelle in `no-loss-check` ist noch vorhanden (Zeile mit `#48` findet
      sich weiterhin)
- [ ] Die neue Sektion existiert in `skills/CLAUDE.md` (Ueberschriften-Suche = 1 Treffer) und enthaelt
      alle fuenf Bestandteile (je ein Treffer fuer Einteilungsregel, Kopplungsregel, Meldeform-Schema,
      §4-Abgrenzung, Laufzeit-Autarkie)
- [ ] Die Zuordnungstabelle nennt alle sechs Skillnamen (`idea`, `task`, `bug-report`, `lesson`,
      `open-question`, `meeting-dump`) — Trefferzahl 6, kein „…" am Tabellenende
- [ ] `skills/CLAUDE.md` bleibt in sich konsistent: keine Datei ausserhalb `skills/CLAUDE.md` und
      `skills/dtb-no-loss-check/SKILL.md` ist in dieser Phase geaendert (Aenderungsliste = 2 Dateien)

#### Manual
- [ ] Die Einteilungsregel ist scharf genug, um ohne Ermessen ueber einen neuen Skill zu entscheiden —
      Probe an zwei Grenzfaellen aus dem Bestand (`docs-extract` schreibt extrahierte Fakten,
      `workflow-checkpoint` schreibt einen Session-Log: beide duerfen **nicht** unter die Regel fallen)
- [ ] Die Kopplungsregel erklaert alle drei Bestandsformen widerspruchsfrei

---

## Phase 2: Haertung der drei Capture-Skills

### Ziel

Die drei Skills tragen den Check an der richtigen Stelle, in der von der Konvention vorgegebenen
Form — und die Aenderung ist nachweislich chirurgisch: der Worktree-Guard in `dtb:idea` unberuehrt,
die drei geschuetzten Skills unberuehrt.

### Schritte

#### Schritt 2.1: `dtb:idea` haerten (inkl. Frontmatter-Nachzug)
- **Zweck:** Der Skill mit dem dokumentierten Beinahe-Fall und dem hoechsten Erfassungs-Volumen
- **Dateien:** `skills/dtb-idea/SKILL.md`
- **Input:** Meldeform-Schema und Kopplungsregel aus Phase 1; INBOX-Tabellenformat aus der Ist-Analyse
- **Output:** (a) Frontmatter: Stichwort-Suche in den deklarierten Werkzeugen ergaenzt — sonst laeuft
  der Check ins Leere und `project-health` warnt; (b) neue Sektion `## Duplikat-Check` **nach** Schritt
  1 (Erfassung) und **vor** Schritt 2 (Schreiben), mit unscharfem Vergleich der erfassten Idee gegen
  die `Idee`-Spalte der Sammel-Datei nach der Ersetzungsprobe, Fundstelle = Eintragsnummer,
  Bestandstext gekuerzt, Entscheidung Ja/Abbrechen; (c) kein Treffer → keine Ausgabe
- **Randbedingung:** Der Worktree-Guard-Block bleibt unangetastet — `dtb:idea` ist seine
  Referenz-Instanz, jede Abweichung waere ein Befund und wuerde ueber die Verteilung mitreisen

#### Schritt 2.2: `dtb:task` haerten
- **Zweck:** Zweiter Kollisionsort mit anderem Suchraum — Inhalts-Dublette ueber Change-Ordner hinweg
- **Dateien:** `skills/dtb-task/SKILL.md`
- **Input:** Konvention aus Phase 1; Struktur von `task.md` (`## Beschreibung`, `## Begruendung`,
  `## Bereich`)
- **Output:** Sektion `## Duplikat-Check` nach Schritt 1 (Erfassung) und **vor** Schritt 3
  (Slug-Vergabe) — bei erkanntem Duplikat wird kein Name mehr gebraucht. Verglichen wird der erfasste
  Text unscharf gegen die Beschreibungs-Abschnitte vorhandener Aufgaben-Dateien der aktiven Changes;
  `archive/` bleibt ausgeschlossen. Fundstelle = Ordnerpfad. Die bestehende Datei-Existenz-Pruefung in
  Schritt 4 bleibt unveraendert daneben stehen (Namens-Kollision, §4) — die Abgrenzung wird an der
  Stelle mit einem Satz benannt

#### Schritt 2.3: `dtb:bug-report` haerten
- **Zweck:** Dritter Kollisionsort, gleiche Struktur wie `task`, anderer Vergleichsanker
- **Dateien:** `skills/dtb-bug-report/SKILL.md`
- **Input:** Konvention aus Phase 1; Struktur von `bug.md` (`## Symptom`, `## Erwartetes Verhalten`,
  `## Reproduktion`)
- **Output:** Sektion `## Duplikat-Check` an derselben relativen Position wie in `task`; verglichen
  wird gegen die Symptom-Abschnitte vorhandener Bug-Dateien der aktiven Changes. Zusaetzlich der
  Hinweis, dass ein wiederkehrender Fehler legitim erneut erfasst werden darf (Entscheidung beim
  Menschen) — und dass ein Treffer im Archiv bewusst **nicht** geprueft wird

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Mechanische Selbstpruefung der Aenderung
- **Zweck:** Die drei Risiken mit hohem Impact abfangen, bevor sie in Phase 3 teuer werden
- **Dateien:** keine (nur Pruefung); Ergebnis wandert in den Session-Log
- **Input:** Zielzahl aus der Zuordnungstabelle; Guard-Vorlage aus `skills/CLAUDE.md`;
  **Vergleichspunkt ist der Phase-1-Ende-Commit-SHA** (aus `## Progress` nach dem SHA-Nachtrag) —
  „Aenderungsliste dieser Phase" heisst: Diff gegen genau diesen SHA, nicht gegen Gefuehl
- **Output:** Vier Nachweise: (1) Anker-Suche erreicht die Zielzahl; (2) `dtb:project-health` meldet
  fuer keinen der drei Skills eine Werkzeug-Warnung; (3) der Guard-Block in `dtb:idea` ist gegenueber
  dem Ausgangsstand unveraendert; (4) die Aenderungsliste enthaelt `lesson`, `open-question`,
  `meeting-dump` **nicht**

### Deliverables
- [ ] `## Duplikat-Check` in allen drei Zielskills, an der richtigen relativen Position
- [ ] Frontmatter von `dtb:idea` nachgezogen
- [ ] Vier Nachweise aus Schritt 2.4 dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] Anker-Suche `^## Duplikat-Check` ueber `skills/` erreicht die Zielzahl aus der
      Zuordnungstabelle (3 neue Treffer in `idea`/`task`/`bug-report`)
- [ ] `skills/dtb-idea/SKILL.md` deklariert die Stichwort-Suche in seinen Werkzeugen
- [ ] `dtb:project-health` laeuft und meldet fuer keinen der drei Skills eine Werkzeug-Warnung
- [ ] Der Worktree-Guard-Block in `dtb:idea` (Bash-Block + Abbruch-Fence) ist gegenueber `49e1b55`
      unveraendert — Vergleich zeigt keine Aenderung innerhalb der Guard-Sektion
- [ ] Die Aenderungsliste dieser Phase (Diff gegen den Phase-1-Ende-SHA) enthaelt genau drei
      Dateien; `dtb-lesson`, `dtb-open-question` und `dtb-meeting-dump` sind nicht darunter
- [ ] In allen drei Skills steht der Check-Abschnitt **vor** dem ersten schreibenden Schritt
      (bei `task`/`bug-report` zusaetzlich vor der Slug-Vergabe) — Positions-Pruefung ueber die
      Reihenfolge der Ueberschriften

#### Manual
- [ ] Die drei Meldeformen lesen sich als dieselbe Form mit anderen Slots, nicht als drei
      Eigenkonstruktionen
- [ ] Das Stoerungsfreiheits-Versprechen ist in keinem der drei Skill-Texte relativiert worden

---

## Phase 3: Belege und Uebergabe

### Ziel

Belegen, dass die Mechanik an echten Daten das Richtige tut — und ehrlich abgrenzen, was in diesem
Arbeitsplatz **nicht** belegbar ist, damit die Abnahme nicht auf einer Luecke stattfindet.

> **Warum kein echter Skill-Lauf hier:** `idea`, `task` und `bug-report` sind Voll-Guard-Skills und
> brechen im verlinkten Worktree ab, bevor der neue Check erreicht wird. Der End-zu-End-Lauf gehoert
> deshalb nach dem Zusammenfuehren in den Haupt-Checkout. `dtb:kit-sync` hat **keinen** Guard, wuerde
> hier also durchlaufen und den Branch-Stand global installieren — es gehoert zwingend hinter das
> Zusammenfuehren.

> **Protokoll-Format (verbindlich fuer 3.1-3.3, Review-Befund):** Ein Mechanik-Beleg ist KEINE
> Behauptungs-Prosa, sondern je Fall ein nachlesbarer Vier-Zeilen-Block im Session-Log:
> (1) das tatsaechlich ausgefuehrte Such-Kommando gegen die echte Datei, (2) die Trefferliste
> (oder „0 Treffer"), (3) die angewandte Ersetzungsprobe mit Ein-Satz-Begruendung,
> (4) die erwartete Meldung im Schema der Konvention (bzw. „keine Ausgabe" im Blind-Fall).

### Schritte

#### Schritt 3.1: Mechanik-Beleg unscharfer Vergleich (`idea`) gegen echte Daten
- **Zweck:** Zeigen, dass die Ersetzungsprobe an realem Bestand trennscharf ist — Treffer- und
  Blind-Fall
- **Dateien:** keine Aenderung; gelesen wird `dtb-project/project-workflows/INBOX.md`
- **Input:** Zwei Kandidaten-Texte: einer, der sachlich einem vorhandenen Eintrag entspricht (der
  Bestand koennte ihn ohne Informationsverlust ersetzen), und einer, der denselben Gegenstand mit
  **anderer Aussage** trifft (muss durchlaufen)
- **Output:** Protokoll beider Faelle: erwartete Fundstelle bzw. erwartete Nicht-Meldung, gekuerzter
  Bestandstext, und der Nachweis, dass die Kuerzung die 5944-Zeichen-Zeile auf Hinweis-Laenge bringt

#### Schritt 3.2: Mechanik-Beleg `task`/`bug-report` mit angelegter Test-Situation
- **Zweck:** Das Hoch-Wahrscheinlichkeits-Risiko der Spec aufloesen — aktive Changes tragen 0
  Aufgaben- und 0 Bug-Dateien, es gibt keinen natuerlichen Belegfall
- **Dateien:** temporaere Test-Change-Ordner unter
  `dtb-project/project-workflows/features/` mit **Erkennungs-Praefix `zz-test-`** im Slug (je eine
  Aufgaben- und eine Bug-Datei), **nach dem Beleg vollstaendig zurueckgenommen** — das Praefix stellt
  sicher, dass ein fehlgeschlagenes Aufraeumen keine echten Changes vortaeuscht
- **Input:** Je ein Kandidat, der die Test-Datei sachlich doppelt, und je einer, der es nicht tut
- **Output:** Protokoll je Skill (Treffer + Blind), Nachweis dass der Vergleich vor der Slug-Vergabe
  greift, und Nachweis dass die Test-Artefakte restlos entfernt sind

#### Schritt 3.3: Ausschluss-Nachweise
- **Zweck:** Die bewusst gezogenen Grenzen belegen, damit sie nicht als Versehen gelesen werden
- **Dateien:** keine Aenderung
- **Input:** Archiv-Bestand (5 Aufgaben-, 3 Bug-Dateien), Kappungs-Regel aus der Konvention
- **Output:** Drei Nachweise: (1) kein Check durchsucht `archive/` — belegt an einem Kandidaten, der
  eine archivierte Aufgabe sachlich doppelt und **nicht** gemeldet wird; (2) bei mehr als drei
  Treffern wird gekappt und der Rest gezaehlt; (3) kein Treffer erzeugt keine Ausgabe

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Uebergabe-Notiz fuer den Orchestrator
- **Zweck:** Alles benennen, was dieser Arbeitsplatz strukturell nicht erledigen darf — sonst faellt
  es zwischen die Sessions
- **Dateien:** `features/capture-duplikat-schutz/plan.md` (Ergaenzung am Ende) bzw. der Hand-off-Block
- **Input:** Schreibgrenzen-Regel; die uebersprungenen Schritte aus Discovery und Spec
- **Output:** Liste mit sechs Punkten: (1) echter Lauf je Skill im Haupt-Checkout nach dem
  Zusammenfuehren; (2) `dtb:kit-sync` danach, Drift der drei verteilten Artefakte aufloesen;
  (3) Eintrag #48 auf `Ausgearbeitet` setzen und beide Artefakt-Links anhaengen; (4) Backlog-Zeile
  fuer das Feature; (5) Folge-Idee „Regressions-Erkennung fuer `bug-report`" erfassen; (6) Folge-Idee
  „`dtb:project-health` prueft die Duplikat-Schutz-Konvention" erfassen (Pre-Mortem-Restluecke: ein
  **siebter** Capture-Skill wird von Zuordnungstabelle und Anker-Zielzahl nicht erfasst — nur eine
  Pruefung „erfuellt Einteilungskriterium, traegt aber keinen Anker → WARNUNG" erwischt ihn
  automatisch)

### Deliverables
- [ ] Protokoll Treffer-/Blind-Fall fuer alle drei Skills (Vier-Zeilen-Format)
- [ ] Drei Ausschluss-Nachweise (Archiv, Kappung, Stille)
- [ ] Uebergabe-Notiz mit sechs Punkten

### Checkpoint-Kriterien

#### Automated
- [ ] Fuer jeden der drei Skills liegt ein Treffer- **und** ein Blind-Protokoll vor (6 Faelle),
      jedes im verbindlichen Vier-Zeilen-Format (Kommando → Treffer → Ersetzungsprobe mit
      Begruendung → erwartete Meldung)
- [ ] Der Kuerzungs-Nachweis zeigt: die 5944-Zeichen-Zeile erscheint im Hinweis auf ~120 Zeichen
      gekuerzt
- [ ] Der Archiv-Kandidat aus Schritt 3.3 erzeugt **keine** Meldung
- [ ] Die Test-Artefakte aus Schritt 3.2 existieren nicht mehr; der Arbeitsbaum enthaelt ausser den
      drei Skill-Dateien, `skills/CLAUDE.md`, `dtb-no-loss-check` und den drei Change-Artefakten
      keine Aenderung
- [ ] Die Uebergabe-Notiz nennt alle sechs Punkte

#### Manual
- [ ] Die Trennung „hier belegt" vs. „nach dem Zusammenfuehren zu belegen" ist im Hand-off
      unmissverstaendlich — die Abnahme darf den Mechanik-Beleg nicht fuer den End-zu-End-Lauf halten

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger der Haertung | A: drei Skills einzeln · B: gemeinsame Konvention · C: nur Konvention | **B + Umsetzung** | Die Luecke ist erblich — ohne Konvention erbt sie der siebte Capture-Skill erneut |
| Form der Konvention | A: `Eligibility-Gates`-Form (Mechanik + Zuordnungstabelle) · B: Worktree-Guard-Form (byte-identische Kopie) | **A** | Byte-identische Kopie ist unmoeglich: jedes Ziel hat einen eigenen Suchraum. Geteilt sind nur Kriterium, Meldeform, Einteilungsregel |
| Meldeform | A: eine fuer alle · B: an Vergleichsschaerfe gekoppelt | **B** | Unscharfer Vergleich hat Falsch-Positive per Konstruktion und darf nicht allein entscheiden; exakter hat keine. Erklaert den Bestand ohne Umbau |
| Kanon der Ersetzungsprobe | A: Konvention verweist auf `no-loss-check` · B: nach `skills/CLAUDE.md` heben · C: neu formulieren | **B, mit deklariertem Laufzeit-Spiegel im Skill** | A laesst einen Skill zum Kanon einer Autoren-Konvention werden (Verweis zeigt bergab); C erzeugt zwei ungekoppelte Wortlaute. Reiner Verweis ohne Spiegel schied im Review aus: installierte Klasse-A-Skills laufen ohne `skills/CLAUDE.md` (Autarkie) |
| Vergleichsschaerfe `task`/`bug-report` | A: exakt · B: unscharf | **B** | Gleiche Begruendung wie bei `idea`: dieselbe Sache wird selten woertlich gleich formuliert, exakt waere bei Freitext wertlos |
| Suchraum | A: `archive/` einbeziehen · B: ausschliessen | **B** | Kit-konform (drei Skills schliessen es aus) und sachlich: Wiederkehr ist bei Housekeeping normal, ein Archiv-Treffer meist ein Falsch-Positiv |
| Anker-Form | A: `## Duplikat-Check` ohne Nummer · B: numerierter Schritt | **A** | Die Skills haben 3/6/6 Schritte, `lesson` nennt es „Schritt 3", `open-question` faltet es ein — eine feste Nummer kann es nicht geben |
| E2E-Beleg | A: echter Skill-Lauf hier · B: Mechanik-Beleg hier + echter Lauf nach dem Zusammenfuehren · C: Guard umgehen | **B** | Alle drei Skills sind Voll-Guard und brechen hier ab; C ist ausgeschlossen (Schreibgrenzen-Regel) |
| Zeitpunkt der Verteilung | A: in dieser Session · B: nach dem Zusammenfuehren | **B** | `dtb:kit-sync` hat keinen Guard und wuerde hier den Branch-Stand global installieren |
| Beruehrung `CLAUDE.md` (Repo-Root) | A: Konvention im Katalogtext erwaehnen · B: nicht anfassen | **Offen** | Niedrige Relevanz; entscheidbar am Ende von Phase 1, wenn der Wortlaut der Konvention steht |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Ersetzungsprobe heben + Rueckverweis
- [x] 1.2 Konventions-Sektion (Einteilung, Kopplung, Meldeform, §4-Abgrenzung)
- [x] 1.3 Zuordnungstabelle + Grep-Anker
- [ ] 2.1 `dtb:idea` haerten (inkl. Frontmatter)
- [ ] 2.2 `dtb:task` haerten
- [ ] 2.3 `dtb:bug-report` haerten
- [ ] 2.4 Mechanische Selbstpruefung
- [ ] 3.1 Mechanik-Beleg `idea`
- [ ] 3.2 Mechanik-Beleg `task`/`bug-report` (angelegte Test-Situation)
- [ ] 3.3 Ausschluss-Nachweise
- [ ] 3.4 Uebergabe-Notiz

---

## Umsetzung

Umsetzung mit `/dtb:implement Capture-Duplikat-Schutz` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/capture-duplikat-schutz/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
