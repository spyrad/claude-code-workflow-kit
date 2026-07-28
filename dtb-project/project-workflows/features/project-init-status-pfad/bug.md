# Bug: project-init legt Statusdateien im Projekt-Root an

**Erstellt:** 2026-07-28
**Severity:** Mittel
**Status:** Behoben im Kit-Repo (alle Fix-Schritte abgehakt, blinde Abnahme bestanden) — die global installierte Kopie traegt den Fix erst nach `/dtb:kit-sync sync`
**Betroffene Komponente:** `skills/dtb-project-init/SKILL.md:248` (Erzeugung — einzige Ursache; `:14` `produces` wurde in der Analyse als Ursache widerlegt)

---

## Symptom

`/dtb:project-init` legt `WORKFLOW_STATUS.md` und `BACKLOG.md` im **Projekt-Root** an.
Alle konsumierenden Skills lesen sie aber unter `{config.paths.workflows}/`
(= `dtb-project/project-workflows/`). Beide Seiten nehmen unterschiedliche Orte an.

Folge in einem frisch initialisierten Projekt:

1. `/dtb:workflow-resume` meldet „WORKFLOW_STATUS.md nicht gefunden" — obwohl `project-init`
   sie erzeugt hat
2. `/dtb:workflow-checkpoint` legt beim ersten Lauf eine **zweite** Datei am richtigen Ort an
3. Das Projekt traegt danach ein **totes Artefakt im Root**, das nie wieder gelesen wird und
   im Zweifelsfall einen aelteren Stand zeigt als die echte Datei

`BACKLOG.md` ist genauso betroffen (dieselbe Anweisungszeile) — faellt nur spaeter auf, weil
`backlog-status` seltener laeuft als `workflow-resume`.

## Erwartetes Verhalten

`project-init` schreibt beide Dateien nach `{config.paths.workflows}/` — analog zum
Regel-Datei-Seed, der direkt darunter (`:252`) korrekt
`{config.paths.rules}/DERIVED_STATE_RULES.md` verwendet.

## Reproduktion

1. In einem leeren Projektverzeichnis `/dtb:project-init` ausfuehren und durchlaufen lassen
2. `ls` im Projekt-Root → `WORKFLOW_STATUS.md` und `BACKLOG.md` liegen dort
3. `ls dtb-project/project-workflows/` → beide Dateien fehlen
4. `/dtb:workflow-resume` ausfuehren → „WORKFLOW_STATUS.md nicht gefunden"

## Kontext

- **Umgebung:** Kit-Version `54fbade`; beobachtet in einem Zielprojekt am 2026-07-28
- **Erstmals bemerkt:** 2026-07-28, bei einem `project-init`-Lauf in einem neuen Projekt
- **Frequenz:** Immer (deterministisch, betrifft jeden `project-init`-Lauf)

### Ursache (belegt, ohne Root-Cause-Analyse vorwegzunehmen)

`SKILL.md:248` lautet vollstaendig:

> Erstelle eine leere `WORKFLOW_STATUS.md` und `BACKLOG.md` falls sie nicht existieren.

**Kein Pfad.** Verstaerkend: die Zeile steht im CLAUDE.md-Abschnitt, weit hinter Schritt 4
(Verzeichnisstruktur, `:112`) — an der Stelle ist kein Verzeichnis-Kontext praesent, also
landet die Datei im cwd (= Projekt-Root).

Die Asymmetrie ist im Skill selbst sichtbar:

| Stelle | Pfadangabe |
|--------|-----------|
| `:248` `WORKFLOW_STATUS.md` + `BACKLOG.md` | **keine** |
| `:252` `DERIVED_STATE_RULES.md` | `{config.paths.rules}/…`, mit `mkdir -p "$(dirname "$DST")"` + Hash-Verifikation |
| `:84` `workflow.config.yaml` | „im Projekt-Root" — dort korrekt und explizit |

> **Korrektur (Analyse 2026-07-28):** Die Erst-Erfassung zaehlte auch das `produces`-Frontmatter
> (`:14`) als Teil der Asymmetrie. Das ist **falsch** — siehe Hypothese 2 unten. Die
> Frontmatter-Ebene fuehrt bewusst bare Artefakt-Namen; ein Pfad dort waere ein Regressionsrisiko,
> keine Verbesserung.

### Gegenprobe: wer liest wo

Konsumierende Skills verwenden konsequent `{config.paths.workflows}/WORKFLOW_STATUS.md` —
`workflow-resume`, `workflow-checkpoint`, `project-health`, `feature-start`, `archive`,
`impl-review`, `pipeline-graph`, `migrate-change-folders`. Kein Skill erwartet die Datei im Root.

### Offene Punkte fuer den Fix

Durch die Analyse unten beantwortet bzw. praezisiert — siehe `## Fix-Schritte`.

---

**Erfasst mit:** `/dtb:bug-report`

---

## Analyse

**Analysiert:** 2026-07-28
**Status:** Offen → Analysiert

### Root-Cause-Hypothesen

| # | Hypothese | Wo (Datei:Zeile) | Evidenz | Staerke |
|---|-----------|------------------|---------|---------|
| 1 | Die einzige Erzeugungs-Anweisung nennt kein Zielverzeichnis → das Modell schreibt ins cwd (Projekt-Root) | `skills/dtb-project-init/SKILL.md:248` | Zeilentext ohne `{config.paths.*}`-Praefix und ohne `mkdir`; direkter Kontrast zu `:251` (Seed, mit Pfad + `mkdir -p` + Hash-Verifikation) und `:84` (`workflow.config.yaml`, „im Projekt-Root" explizit gewollt). Erklaert das Symptom vollstaendig | **STRONG** |
| 2 | ~~`produces`-Frontmatter (`:14`) traegt dieselbe Asymmetrie~~ | `:14` | **WIDERLEGT.** Alle 12 Skills mit `WORKFLOW_STATUS`/`BACKLOG` im Frontmatter nennen sie **bare, ohne Pfad** (`archive`, `backlog-status`, `bug-report`, `feature-plan`, `feature-start`, `project-health`, `project-init`, `task`, `workflow-checkpoint`, `workflow-next`, `workflow-resume`, `workflow-status`). `pipeline-graph:40/:103` behandelt sie ausdruecklich als **„Artefakt-Patterns"**, nicht als Dateipfade; `project-health:199` matcht `consumes` gegen `produties` ueber genau diese Namen. `project-init` ist hier also **konform** — ein Pfad dort wuerde den Verwaisungs-Check brechen | **NONE** (als Ursache widerlegt) |
| 3 | Fehlender Sekundaer-Kontext verstaerkt H1: der Verzeichnisbaum (`:115-133`) listet nur Ordner, keine Dateiplatzierungen, und die eingebetteten Templates (`:287` ff.) tragen keine Pfadzeile im Kopf | `:115-133`, `:287` | Baum und Templates enthalten keine Zuordnung Datei→Ordner; zwischen Baum und `:248` liegen 136 Zeilen (dazwischen der komplette CLAUDE.md-Sentinel-Abschnitt). Verstaerker, nicht eigenstaendige Wurzel | **WEAK** |

**Begruendung H1:** `:248` steht formal in Schritt 4 („Verzeichnisstruktur anlegen", ab `:112`),
faktisch aber im CLAUDE.md-Unterabschnitt. An dieser Stelle ist kein Verzeichnis-Kontext praesent —
der Baum liegt 136 Zeilen davor. Ohne Praefix ist das cwd der einzige Anker, und das ist der
Projekt-Root.
**Pruefung H1:** Blinder Agenten-Lauf (nur Skill + leeres Verzeichnis, kein Autor-Kontext) →
`ls` im Root zeigt beide Dateien. Genau so beobachtet am 2026-07-28.

**Pruefung H3:** Nach dem Fix an `:248` in einem zweiten blinden Lauf pruefen, ob der Pfad
zuverlaessig getroffen wird — wenn ja, ist H3 folgenlos und braucht keinen eigenen Eingriff.

### Nebenbefunde (nicht Teil dieses Bugs)

- **`project-health` hat keinen Ort-Check.** Die Check-Kategorien sind Config-Integritaet,
  Querverweise, Status-Konsistenz, Namenskonventionen, Frische, CLAUDE.md, Git,
  Skill-Frontmatter, Memory, Rules, Kit-Drift — **kein** „Artefakt am falschen Ort". Eine
  Root-`WORKFLOW_STATUS.md` bleibt deshalb dauerhaft unsichtbar. Das ist der Grund, warum der
  Bug erst im Zielprojekt auffiel.
- **`:137` und `:157`** („Lege in `integrations/vendor-x/input/` …", „Lege in `project-design/` …")
  nennen relative Pfade ohne `dtb-project/`-Basis — derselbe Defekt-Typ wie H1, aber nur 5-25
  Zeilen hinter dem Baum, daher deutlich schwaecher exponiert.
- **CLAUDE.md `:99` widerspricht dem project-init-Baum:** dort `integrations/<vendor-name>/input/`
  auf Projektwurzel-Ebene, im Baum (`:132`) unter `dtb-project/`. Eigener Widerspruch, eigener Fix.

---

## Fix-Schritte

> **Diese Checkliste ist die Status-Quelle** (DERIVED_STATE_RULES §1.5): 0 abgehakt = Analysiert,
> teilweise = In Arbeit, alle = Behoben.

- [x] `skills/dtb-project-init/SKILL.md:248` umschreiben: beide Dateien mit
      `{config.paths.workflows}/`-Praefix benennen und das Anlegen des Verzeichnisses absichern
      (`mkdir -p`), Formulierung am bereits gehaerteten Seed-Absatz `:251` orientieren
      — erledigt 2026-07-28: Abschnitt „Status-Dateien anlegen" mit Praefix, `mkdir -p`-Block,
      expliziter Negativregel („**Nicht** in den Projekt-Root — dort gehoert allein
      `workflow.config.yaml` hin") und Konsumenten-Liste
- [x] Template-Koepfe (`WORKFLOW_STATUS.md`, `BACKLOG.md`) mit einer Zielpfad-Zeile versehen,
      damit der Ort auch am Template ablesbar ist (adressiert H3) — erledigt 2026-07-28:
      beide Koepfe tragen jetzt `→ Zielpfad {config.paths.workflows}/…`
- [x] `produces`-Frontmatter `:14` **bewusst NICHT anfassen** — verifiziert: `git diff` zeigt
      keine Aenderung an der `produces`-Zeile; Begruendung in der Commit-Message, damit ein
      spaeterer Lauf die scheinbare Asymmetrie nicht „korrigiert"
- [x] Blinden Agenten-Lauf als Abnahme fahren (Lektion 7): nur Skill + leeres Verzeichnis,
      kein Autor-Kontext — **durchgefuehrt 2026-07-28, bestanden.** Ergebnis (selbst per `find`
      nachgeprueft, nicht nur dem Agenten-Bericht entnommen): Projekt-Root enthaelt ausschliesslich
      `CLAUDE.md` + `workflow.config.yaml`; `WORKFLOW_STATUS.md` und `BACKLOG.md` liegen unter
      `dtb-project/project-workflows/`; Gegenprobe `find -name` findet **keine** Kopie an falscher
      Stelle. Der Agent nannte den neuen Wortlaut ausdruecklich als Grund („Zielort: Ja, doppelt")
- [x] **Nachkorrektur aus dem blinden Lauf** (Fehler im eigenen Fix): Die Negativregel lautete
      „dort gehoert **allein** `workflow.config.yaml` hin" — falsch, denn `CLAUDE.md` gehoert
      ebenfalls in den Root, und fuer sie nennt der Skill **keinen** Zielort. Der Agent musste
      raten und protokollierte: „Annahme: Projekt-Root, weil der Satz sich im Text auf die
      Status-Dateien bezieht." Korrigiert zu „dort liegen nur `workflow.config.yaml` (Schritt 3)
      und `CLAUDE.md`"

### Verifikation der umgesetzten Schritte (2026-07-28, ohne blinden Lauf)

- `produces`-Frontmatter unveraendert (Regressionsrisiko 1 ausgeschlossen)
- Seed-Absatz `:251` unveraendert — keine Beruehrung der durch Lektion 4 gehaerteten Stelle
- Grep nach verbleibenden Erzeugungs-Anweisungen ohne Pfadangabe in `project-init`: **0 Treffer**
- Umfang: +14/−3 Zeilen, ausschliesslich im Anweisungstext

**Grenze dieser Verifikation:** Sie ist im Autor-Kontext entstanden und damit genau die Pruefart,
die Lektion 7 als unzureichend beschreibt — der Basispfad wird beim Lesen im Kopf mitkorrigiert.
Erst der blinde Lauf belegt, dass die Anweisung ohne diesen Kontext trifft.

**Regressionsrisiko:**

- **Hoch, falls `produces:14` mitgeaendert wird:** `project-health:199` prueft, ob jedes
  `consumes`-Artefakt von mindestens einem Skill in `produces` gelistet wird. Alle 11 anderen
  Skills nennen `WORKFLOW_STATUS.md`/`BACKLOG.md` bare — ein Pfad in `project-init.produces`
  wuerde diesen Match brechen und eine **falsch-positive Verwaisungs-Warnung** erzeugen. Ebenso
  bekaeme `pipeline-graph` (`:103`, Artefakt-Matrix) eine zusaetzliche Spalte fuer dasselbe
  Artefakt.
- **Gering bei `:248` selbst:** die Zeile hat keine Konsumenten; sie ist reine Anweisung.
- **Seed-Absatz `:251` nicht beruehren** — er ist durch Lektion 4 gehaertet (mechanisches `cp`
  ueber `localPath` + Hash-Verifikation).

## Testplan

- [ ] Reproduktion gegenpruefen: blinder Lauf in leerem Verzeichnis → `WORKFLOW_STATUS.md` und
      `BACKLOG.md` liegen unter `dtb-project/project-workflows/`, **nicht** im Root
- [ ] Anschluss pruefen: danach `/dtb:workflow-resume` → findet die Datei, keine
      „nicht gefunden"-Meldung mehr
- [ ] Regression Seed: `DERIVED_STATE_RULES.md` landet weiter unter `{config.paths.rules}/`
      mit bestandener Hash-Verifikation
- [ ] Regression Frontmatter: `/dtb:project-health` zeigt **keine** neue Verwaisungs-Warnung zu
      `WORKFLOW_STATUS.md`/`BACKLOG.md` (belegt, dass `produces` unangetastet blieb)

---

## Bestandsprojekte (bewusst NICHT Teil der Fix-Schritte)

Der Fix verhindert Neuentstehung, bereinigt aber keinen Bestand. Fuer bestehende Projekte gibt es
zwei Lagen, die sich nicht pauschal behandeln lassen:

- **Beide Dateien vorhanden** (Root + `project-workflows/`): die Root-Datei ist in der Regel das
  leere `project-init`-Template und die aeltere → loeschen. `workflow-checkpoint` ueberschreibt
  `WORKFLOW_STATUS.md` **immer** (`:77`), hat die echte Datei also schon angelegt.
- **Nur die Root-Datei vorhanden** (nie ein Checkpoint gelaufen, ggf. manuell gepflegt) →
  verschieben, nicht loeschen.

Eine automatische Bereinigung braucht diese Unterscheidung und gehoert damit nicht in
`project-init` (laeuft nur einmal, meist vor dem Entstehen des Problems), sondern in einen
**neuen `project-health`-Check „Artefakt am falschen Ort"** — der dort heute fehlt (Nebenbefund
oben). Das ist ein eigener Change; als Idee zu erfassen, nicht in diesem Bug mitzufixen.

---

**Analysiert mit:** `/dtb:debug-plan`
