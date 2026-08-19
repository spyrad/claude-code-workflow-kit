# Skills — Contributor Guide

## Frontmatter (Pflichtfelder)

Every skill file must have YAML frontmatter with these fields:

```yaml
---
name: dtb:<skill-name>
description: >-
  Use when: "<trigger phrases>". <English summary of what the skill does>.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash   # subset as needed
pipeline:
  stage: idea | capture | planning | implementation | execution | development | session | monitoring | setup | greenfield
  after: [dtb:<predecessor>]  # list, or null if entry point
  next: [dtb:<successor>]     # list, or null if terminal
  consumes: [features/*/spec.md]   # artifacts read by this skill (features/*/{spec,plan,bug,task}.md, etc.)
  produces: [features/*/plan.md]   # artifacts written by this skill
---
```

### Field details

- **name**: `dtb:<kebab-case-name>` — must match directory name without `dtb-` prefix
- **description**: starts with `Use when:` trigger phrases (German), ends with English summary
- **disable-model-invocation**: `true` unless the skill should be auto-triggered by the model
- **allowed-tools**: comma-separated list of tools the skill is permitted to use
- **pipeline**: declares where the skill sits in the workflow pipeline (see below)

### Pipeline block

| Field | Type | Description |
|-------|------|-------------|
| `stage` | enum | Workflow phase: `idea`, `planning`, `implementation`, `development`, `session`, `monitoring`, `setup`, `greenfield` |
| `after` | list/null | Predecessor skills (`[dtb:<name>, …]`) or `null` if entry point — a **list** even with a single element (`dtb:project-health` lints every element) |
| `next` | list/null | Successor skills (`[dtb:<name>, …]`) or `null` if terminal — same list rule |
| `consumes` | list | Artifact patterns this skill reads (e.g. `features/*/spec.md`, `INBOX.md`) |
| `produces` | list | Artifact patterns this skill writes (e.g. `features/*/plan.md`) |

### Artifact status values (Derived State)

Status is **derived from artifacts**, not maintained in fields — rules in
`dtb-project/project-rules/DERIVED_STATE_RULES.md` (single source; read-side skills must
reference it instead of implementing their own logic). Status fields/columns are derived
displays synced by `dtb:workflow-checkpoint`. `IMPL_STATUS_*.md` is abolished.

Changes live in `features/<slug>/` folders (kebab-case slug, fixed filenames). Status derives from
which files are present + `plan.md` `## Progress` (see `DERIVED_STATE_RULES.md`).

| File in `features/<slug>/` | Status values (derivation source) |
|----------------------------|-----------------------------------|
| `spec.md` | Derived: Spezifiziert, Geplant, In Arbeit, Fertig zum Testen (from `plan.md` `## Progress` checkboxes). Explicit only: Abgenommen, Abgeschlossen, Pausiert |
| `plan.md` | Head status field = **review evidence only**, exactly two values `Entwurf`/`Reviewed`, defined as the `**Status:**` line within the first 10 lines; sole writer is `dtb:plan-review` (writes on every verdict; manual flip needs an `(manuell {date}: …)` note) — canon in `DERIVED_STATE_RULES.md` §7. Progress via mandatory `## Progress` section (one checkbox per step N.M; flips gated by checkpoint criteria, SHA written back at phase-end commit — verification evidence, §2) |
| `bug.md` | Derived from `## Fix-Schritte` checklist: Offen, Analysiert, In Arbeit, Behoben. Explicit only: Pausiert, Abgenommen (§1.2/§1.5) |
| `task.md` | Derived from `## Schritte` checklist: Offen, In Arbeit, Erledigt. Explicit only: Pausiert, Abgenommen (§1.2/§1.5) |
| `INBOX.md` entries | Offen, In Arbeit, Ausgearbeitet, Verworfen (maintained by idea skills) |

## Eligibility-Gates

A **schreibender Skill mit zwingender Eingabe** prüft am Eingang, ob sein kritisches Eingabe-Artefakt
existiert. Fehlt es, verweigert er konstruktiv statt auf falscher Basis weiterzuarbeiten, und verweist
auf den Skill, der das Artefakt erzeugt. Vorbild: die Test-zuerst-Weigerung von 10x-tdd.

### Einteilungsregel (welcher Skill bekommt ein Gate)

> Ein Skill bekommt ein **Hard-Gate**, wenn er eine **zwingende Eingabe** braucht (ohne die sein
> Output sinnlos/falsch wäre). Das Kriterium ist **NICHT** `produces` ≠ leer (mehrere Skills
> schreiben nur, ohne eigenes `produces`-Artefakt) und **NICHT** die Position in `consumes`
> (die Reihenfolge ist kein verlässlicher Indikator). Das kritische Artefakt wird **pro Skill
> explizit** benannt — nie positional aus `consumes` abgeleitet.

Read-only-Skills, Entry-Points (`consumes: []`) und Skills ohne zwingende Eingabe bekommen kein
Hard-Gate. Git-Gates (Git-Zustand statt Artefakt) und Soft-Gates (nur empfohlene Eingabe) sind
ein geplantes Folge-Feature — diese Konvention trägt sie bereits. Beispiel ohne Gate:
`commit-and-push` wirkt auf den **Git-Zustand** (kein zwingendes `features/`-Artefakt) und läuft
sogar ohne `workflow.config.yaml` — daher kein Hard-Gate.

### Fit-Check + Redirect (Mechanik)

1. **Fit-Check:** existiert das explizit benannte kritische Artefakt am **slug-spezifischen Pfad**
   `features/{slug}/<artefakt>` (z.B. `features/{slug}/spec.md`)? **Nicht** den `*`-Wildcard
   (`features/*/spec.md`) prüfen — der träfe ein fremdes Feature und erzeugte ein False Negative.
   Ja → Skill läuft normal. Nein → Gate greift.
2. **Redirect-Ableitung** (fehlendes Artefakt → erzeugender Skill), Reihenfolge:
   1. **Selbst-Ausschluss:** den aktuellen Skill aus den Erzeugern streichen (viele Skills führen
      ein Artefakt in `produces`, weil sie es nur *aktualisieren*, nicht erstellen).
   2. **`after`-Match bevorzugen:** bleibt mehr als ein Erzeuger, den nennen, der im `after` des
      aktuellen Skills steht (der Pipeline-Vorgänger/Ersteller) — als empfohlenes Erstziel voran.
   3. **verbleibende nennen:** weitere Erzeuger als Alternative anhängen; ist keiner ableitbar →
      ehrliche Meldung ohne erfundenes Ziel (nie raten).
3. **Meldeblock:** kurzer Block (Muster wie `feature-discover` Schritt 1), der (a) das fehlende
   Artefakt + den **geprüften Pfad** ausgibt, (b) den/die Redirect-Befehl(e) nennt, (c) eine
   **Escape-Hatch** anbietet (bewusster Fortfahren-Weg gegen Fehlalarm — der Nutzer muss ihn
   explizit wählen, kein stilles Durchrutschen).
4. **Nicht-Git-Projekt:** ein späterer Git-Zustand-Check (Folge-Feature) wird still übersprungen.

### Verbindliche Hard-Gate-Zuordnung (v1)

Frontmatter-verifiziert 2026-07-10 (`produces`-Rückwärtssuche per Grep belegt):

| Skill | Kritisches Artefakt | Redirect (nach Selbst-Ausschluss + `after`-Match) |
|-------|---------------------|----------------------------------------------------|
| `impl-plan` | `features/*/spec.md` | `feature-plan` (`workflow-checkpoint` nur Status-Updater) |
| `plan-review` | `features/*/plan.md` | `impl-plan` (einziger Erzeuger; `feature-start` ergaenzt nur `## Progress` in einem VORHANDENEN Plan und verweigert bei fehlendem selbst) |
| `feature-start` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss) |
| `implement` | `features/*/plan.md` | `impl-plan` (`after`-Match ueber `feature-start` hinweg: feature-start erstellt keinen Plan, es laedt nur Kontext und ruestet allenfalls `## Progress` nach; zusaetzlich harte Archiv-Weigerung ohne Escape-Hatch) |
| `impl-review` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss; zusaetzlich harte Archiv-Weigerung ohne Escape-Hatch) |
| `greenfield-roadmap` | `project-strategy/PRD-MVP.md` | `greenfield-prd` (`after`-Match; Pfad ist kein `features/`-Slug, sondern der feste Strategie-Pfad) |
| `debug-plan` | `features/*/bug.md` | `bug-report` (nach Selbst-Ausschluss; `debug-plan` nur Fix-Updater) |
| `feature-fast` | INBOX-Eintrag zur Idee (kein `features/`-Artefakt) | `idea` voran, `idea-review` als Alternative — **ohne Escape-Hatch** (begruendete Abweichung: die INBOX ist die einzige Erhebungsquelle des Fast-Track; ein Durchrutschen ohne Eintrag waere ein Ad-hoc-Einstieg, den die Spec explizit ausschliesst) |
| `archive` | archivierbare Kandidaten vorhanden | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu archivieren" (nativ in Schritt 3) |
| `migrate-change-folders` | flache Alt-Dateien (`features/*.md`) | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu migrieren" (nativ in Schritt 1) |

## Autonomie-Regel (dtb:worker)

Autonome Ausfuehrung gilt ausschliesslich **zwischen expliziter Freigabe und Abnahme**.
`dtb:worker` ist schreibend und damit `disable-model-invocation: true` — der Mensch startet
jeden Lauf; das Modell entscheidet nie selbst, DASS gearbeitet wird. Worker schreiben
ausschliesslich INNERHALB ihres eigenen Worktrees — dort in ihren Change-Ordner
(`## Schritte` abhaken; Subagenten-Traeger: `worker-report.md`, Pane-Traeger:
Hand-off-Block statt Report — beides status-neutral nach `DERIVED_STATE_RULES.md`
§1.1); das Haupt-Repo erreichen die Aenderungen erst mit der Abnahme. Niemals:
pushen, zentrale Dateien (WORKFLOW_STATUS.md, INBOX.md, BACKLOG.md),
Status-/Anzeigefelder, Schreibzugriffe ausserhalb des eigenen Worktrees. Committen:
der Subagenten-Traeger nie; der Pane-Traeger ausschliesslich auf seinem eigenen
Task-Branch (Traeger-Weiche: `skills/dtb-worker/SKILL.md`). Die Deckelung
(`worker.max_attempts`/`worker.max_minutes` in `workflow.config.yaml`, Defaults 3/30) ist
Anweisungs-Ebene — kein harter Timer; der Bericht weist die Laufzeit je Versuch aus.
Die Worktree-Grenze der Worker ist die Worker-Instanz der kitweiten
**Schreibgrenzen-Regel** (naechste Sektion) — dort ist sie kanonisch formuliert.

**Abgrenzung `dtb:pane-start`:** Der interaktive Pane-Start faellt NICHT unter diese Regel —
er stellt keinen autonomen Auftrag zu, sondern einen Begruessungstext an eine Session, in der
ein **Mensch** arbeitet. Deckelung, Tauglichkeitsraster und Berichtspflicht entfallen dort
ersatzlos; es gelten nur Schreibgrenzen-Regel und Worktree-Guard wie fuer jede
Orchestrator-Session.

## Parallele Sessions (Schreibgrenze, Orchestrator-Muster, Worktree-Guard)

### Schreibgrenzen-Regel (die eine Quelle)

**Global geteilte Dateien haben genau einen Schreiber: die Session im Haupt-Checkout
(Orchestrator).** Global geteilt ist alles ausserhalb des eigenen Change-Ordners
`features/<slug>/`: `WORKFLOW_STATUS.md`, `BACKLOG.md`, `INBOX.md`,
Changelog-Tagesdateien, `project-rules/lessons.md`, `project-meetings/`, `archive/`.
In einem verlinkten Worktree entstehen ausschliesslich Feature-Artefakte des eigenen
Changes; alles Globale erreicht das Projekt erst ueber den Orchestrator (Hand-off) bzw.
die Abnahme.

Diese Regel ist bewusst NUR hier ausformuliert — die Worktree-Guards der Skills und die
Autonomie-Regel von `dtb:worker` verweisen hierher, kein zweiter gepflegter Wortlaut.

### Orchestrator-Muster

- Genau EINE Orchestrator-Session pro Projekt-Checkout: sie fuehrt alle global
  schreibenden Skills aus (Checkpoint, INBOX, Backlog, Archiv, Lektionen, Meetings)
- N Worker-Sessions, je eine pro Change, je in einem eigenen Worktree — empfohlener Weg
  sind die nativen CC-Worktree-Tools (`EnterWorktree`/`ExitWorktree`, Subagents mit
  `isolation: worktree`); sie uebernehmen Pfad, Branch-Anlage und Aufraeumen
- Worker-Sessions uebergeben ihre Session-Inhalte am Ende als Hand-off an die
  Orchestrator-Session, die den Checkpoint ausfuehrt (Transport z.B.
  Herdr-Session-Kommunikation; Fallback: Text der Guard-Abbruchmeldung manuell tragen).
  Format und Empfangsseite: `skills/dtb-workflow-checkpoint/SKILL.md` → „Hand-off-Block"
  (die eine Quelle — hier nur der Verweis)
- **Pane-Worker (automatisierte Variante):** `dtb:worker` kann Worker als echte
  Claude-Code-Sessions in Herdr-Panes fuehren (Traeger `pane` statt Subagent) —
  Worktree-Anlage, Beauftragung und Rueckweg des Hand-off-Blocks laufen dann
  automatisiert; der Mensch behaelt Freigabe und Diff-Abnahme. Mechanik, Auftragstext
  und Gate: `skills/dtb-worker/SKILL.md` → „Traeger-Weiche" / „Pane-Auftrag"
  (die eine Quelle — hier nur der Verweis)
- **Bekannte Grenze:** Der Guard erkennt nur verlinkte Worktrees. Zwei Sessions im
  SELBEN Checkout oder Schreiber aus fremden Projekten verletzen das Muster, ohne dass
  der Guard feuert — Leitplanke ist diese Konvention, Auffangnetz die Lesestand-Pruefung
  der lesend-entscheidenden Skills (`idea-review`, `workflow-resume`)

### Skill-Kategorien (Worktree-Verhalten)

| Kategorie | Verhalten im verlinkten Worktree | Skills |
|-----------|----------------------------------|--------|
| **Voll-Guard** (nur Orchestrator) | Harter Abbruch vor dem ersten Schreiben (Vorlage unten) | `workflow-checkpoint`, `idea`, `idea-review`, `archive`, `lesson`, `meeting-dump`, `task`, `bug-report`, `pane-start` (Sonderfall: `produces` leer — Voll-Guard aus betrieblichem Grund, verlinkte Worktrees legt man nur vom Haupt-Checkout aus an) |
| **Teil-Guard** (hybrid) | Laeuft normal am EIGENEN Change, ueberspringt aber die globalen Schreibschritte (INBOX-Status/-Link, BACKLOG-Eintrag) mit einer Hinweiszeile; das Uebersprungene gehoert in den Hand-off | `feature-discover`, `feature-plan`, `feature-fast` |
| **Worktree-faehig** | Unveraendert (schreiben nur `features/<slug>/` des eigenen Changes) | `impl-plan`, `implement`, `feature-start`, `debug-plan`, `impl-review`, `open-question` |
| **Read-only-Sichten** | Unveraendert — Lesen ist ungefaehrlich (Lesestand kann veraltet sein) | `workflow-next`, `workflow-status`, `backlog-status`, `session-summary`, `meeting-agenda`, `no-loss-check`, `pipeline-graph`, … |

Einteilungs-Kriterium ist das `produces:`-Frontmatter — mechanisch pruefen, nie
schaetzen: Erzeugt ein Skill NEUE Change-Ordner oder schreibt er quer (zentrale Dateien,
fremde Changes) → **Voll-Guard**. Arbeitet er am eigenen Change und zieht global nur
Status/Links nach → **Teil-Guard**. Schreibt er nur den eigenen Change-Ordner →
**worktree-faehig**. Ein NEUER Skill mit globalen `produces`-Eintraegen uebernimmt die
Guard-Vorlage ab dem ersten Tag.

### Worktree-Guard (kanonische Vorlage)

Jeder **Voll-Guard**-Skill traegt frueh (vor seinem ersten schreibenden Schritt) eine
Sektion, die mit der Zeile `## Worktree-Guard` beginnt — sie ist der Grep-Anker der
Spiegel-Verifikation (bewusst OHNE Schritt-Nummer: die Skills haben eigene
Schritt-0-Sektionen, eine zweite Null waere ambig). **Bash-Block und ⛔-Fence sind
byte-identisch zu uebernehmen** (im Fence variiert nur der Skill-Name); Rahmenprosa und
Echo-Absatz gemaess der Referenz-Instanz `skills/dtb-idea/SKILL.md` — bei Abweichung
zwischen dieser Vorlage und der Referenz-Instanz gilt die Referenz-Instanz, und die
Abweichung ist ein Befund:

Pruefung in EINEM selbstaendigen Bash-Block (eigene Shell — Setup nie auslagern; die
cd/pwd-Normalisierung ist Pflicht: ohne sie liefert der Vergleich in Unterverzeichnissen
des Haupt-Checkouts False Positives, und `--path-format` existiert erst ab Git 2.31):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(cd "$C" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → **Durchlass, kein
  Output** (der Guard ist im Normalfall unsichtbar — keine Bestaetigungszeile; jeder
  Fehlschlag der Erkennung failt einheitlich offen und markiert als `DURCHLASS-NOGIT`)
- **Branch-Pruefung (optional, nur im `HAUPT-CHECKOUT`-Fall):** Ist `parallel.default_branch`
  in `workflow.config.yaml` gesetzt (nicht `null`) und `git branch --show-current` ungleich
  diesem Wert → Abbruch mit Hinweis „globale Dateien gehoeren auf `{default_branch}`".
  Bei `null` oder fehlendem Key entfaellt die Pruefung ersatzlos (Bestandsprojekte
  verhalten sich unveraendert)
- `WORKTREE` (verlinkter Worktree) → **harter Abbruch** vor jedem Schreiben:

```
⛔ {skill} schreibt globale Dateien und laeuft nur in der Orchestrator-Session
   (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
   die Session im Haupt-Checkout).
   Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
   {Capture-Skills mit uebergebenem Text: „Dein Text geht nicht verloren — dort absetzen:"
    + fertiger Befehl `/dtb:{skill} "{erfasster Text}"`}
```

- **Echo-Verhalten:** Nur bereits uebergebener/erfasster Text wird geechot. Greift der
  Abbruch VOR einem Erfassungs-Dialog, gibt es nichts zu echoen — die Meldung nennt nur
  den Befehl ohne Text-Anteil
- **Teil-Guard-Variante:** Teil-Guard-Skills fuehren dieselbe Pruefung aus, brechen aber
  NICHT ab — im Worktree ueberspringen sie ihre globalen Schreibschritte mit genau einer
  Hinweiszeile `↷ {Datei}-Update uebersprungen (Worktree) — in den Hand-off aufnehmen`
  und arbeiten normal weiter. Ihr Grep-Anker ist die Zeile `**Teil-Guard (Worktree):**`
  an der uebersprungenen Schreibstelle (zusaetzlich in `open-question` fuer den
  Slug-Override auf fremde Changes — die worktree-faehig-Einstufung gilt nur fuer den
  abgeleiteten Default-Fall)

### Lesestand-Pruefung (Spiegel-Anker)

Die lesend-entscheidenden Skills tragen eine Sektion mit der Anker-Zeile
`Lesestand-Pruefung (Lese-Seite)` — Ueberschriftsebene folgt der lokalen Konvention des
Skills, der Anker ist der Zeilentext. Spiegel: `dtb-idea-review`, `dtb-workflow-resume`.
Woertlich gespiegelte 3-Schritte-Struktur: (1) beim Einlesen mtime der Steuer-Dateien
merken, (2) unmittelbar vor dem Trigger erneut pruefen — bei Abweichung Re-Read +
genau eine ⚠-Zeile nur bei tatsaechlicher Inhaltsabweichung (mtime-only = still,
geloeschte Datei = Abweichung), (3) bewusste Restluecke (kein Locking) benennen.
Deklarierte Anpassungspunkte je Skill: der **Trigger** (idea-review: vor jeder
Statusentscheidung; workflow-resume: vor der Report-Ausgabe) und die **Dateiliste**.

## Directory & naming conventions

- Each skill lives in `skills/dtb-<name>/SKILL.md`
- Directory names: kebab-case, lowercase
- Template placeholders: `[PLACEHOLDER]` syntax
- File paths: forward slashes, relative to target project root
- Dates: `YYYY-MM-DD`, never relative terms
- `project-rules/` files use UPPER_SNAKE_CASE (e.g. `FRONTEND.md`, `BACKEND.md`)
- **Change folders:** `features/<slug>/` with kebab-case slug (derived from the feature name, no running numbers) and fixed filenames `discovery.md`/`spec.md`/`plan.md`/`bug.md`/`task.md` — slug rules in `DERIVED_STATE_RULES.md` §4

## Mechanik-Regeln (aus Praxisfehlern)

Diese Regeln entstanden aus konkreten Defekten in diesem Kit und gelten fuer **alle** Skills, nicht
nur den anlassgebenden. Die Analysen liegen unter dem genannten Datum in
`dtb-project/project-changelog/`.

### Bash-Bloecke sind eigene Shells

Jeder Bash-Aufruf eines Skills laeuft in einer **eigenen Shell** — Variablen ueberleben den
Blockwechsel nicht.

- **Jeden Block selbststaendig halten:** gemeinsames Setup (Pfad-/Lock-Aufloesung) im Block
  wiederholen, statt es in einen Vor-Block zu ziehen. „Einmal aufloesen, mehrfach nutzen" ist hier
  der Fehler, nicht die Optimierung.
- Ein Vor-Block darf nur **Gate oder Diagnose** sein — nie Zustand aufbauen, den Folgebloecke brauchen.
- Wird Setup dennoch geteilt, die Wiederholung im Text **als Absicht kennzeichnen**, damit sie
  niemand als Redundanz wieder herauskuerzt.
- **Testen:** jeden Block **einzeln in frischer Shell** ausfuehren, nie gebuendelt. Wer die Bloecke
  extrahiert und zusammen ausfuehrt, laesst die **Naht zwischen** ihnen ungetestet — genau dort
  sitzt dieser Defekt.

Praxisfall 2026-07-29 (`project-init`, Seed-Mechanik): `$KIT` wurde in einen Vor-Block gezogen und
war in den Folgebloecken leer — beide Seeds meldeten „nicht gefunden" bei vorhandenem, korrektem
Kit. Der Testplan war 5/6 gruen, weil er die Bloecke gebuendelt ausfuehrte.

### Datei-Erzeugung: Nachbarschaft mitpruefen

Wird eine Datei-Erzeugung in einem Skill gehaertet (Zielpfad, `mkdir -p`, Hash-Verifikation), immer
**alle benachbarten Erzeugungs-Anweisungen im selben Abschnitt** mitpruefen — nie nur die
anlassgebende Zeile.

Praxisfall 2026-07-28 (`project-init`): eine Haertung am Seed-Absatz liess zwei Zeilen darueber
`WORKFLOW_STATUS.md`/`BACKLOG.md` ohne Zielpfad und ohne `mkdir` — 18 Tage lang landeten sie im
Projekt-Root. Dieselbe Klasse, im selben Blickfeld, nicht mitgeprueft.

### Kopplungs-Hinweise: Spiegel mitziehen und verifizieren

Traegt eine Stelle einen Kopplungs-/Wartungs-Hinweis („Aenderung hier → X mitziehen"), die
genannten Spiegel im **selben Zug** mitziehen — und die Spiegelung **mechanisch verifizieren**:
Grep auf den neuen Wortlaut ueber alle genannten Dateien, Zielzahl = Anzahl der Spiegel. Ein
Hinweis im Fliesstext ist keine Absicherung; beim fokussierten Einzelfix liest man ihn ueber.

Verallgemeinert die Nachbarschafts-Regel darueber auf **explizite Verweise ueber Dateigrenzen**.

Praxisfall 2026-07-30/31 (`DERIVED_STATE_RULES.md` §7.3): Ein Triage-Fix schrieb den „Vorrang der
Still-Regel" nur in den Kanon; der Hinweis „Aenderung hier → beide Skills mitziehen" stand zwei
Zeilen darueber. `workflow-next`/`workflow-status` blieben ungefixt — und weil der Kanon ein
Klasse-B-Seed ist, waere in Bestandsprojekten genau der Text weitergelaufen, gegen den die Spiegel
ueberhaupt angelegt wurden. Gefunden erst vom impl-review am Folgetag.

### Multi-Root: `git -C` in jeder Variante

In Skills, die ueber mehrere Git-Roots operieren, jedes git-Kommando explizit mit `git -C {root}`
schreiben — **inklusive aller alternativen Shell-Varianten** (Bash-heredoc *und*
PowerShell-Here-String), nie nur der primaeren.

Praxisfall 2026-07-16: eine Here-String-Variante ohne `git -C` haette im Multi-Root-Fall ins
falsche Repo committet; sie blieb unsichtbar, weil die primaere Variante korrekt war.

### Werkzeug-Fehlschlag ist kein Datenbefund

Bei Mehr-Punkte-Vergleichen (z.B. Repo ↔ Lock ↔ installierte Kopie) vor der Auswertung mechanisch
belegen, dass **jede Seite gefuellt ist** — Zeilenzahl > 0 als hartes Gate, sonst Abbruch mit
„Werkzeug-Fehlschlag, kein Datenbefund". Verbindliche Vergleichs-Sequenzen eines Skills nie durch
eigene Hash-/Grep-Methoden ersetzen.

Praxisfall 2026-07-29 (`kit-sync`): `grep -P` scheiterte am Locale, die Lock-Seite blieb dadurch
leer, und der Lauf meldete **41 Schein-Abweichungen** gegen den Leer-Hash — ein Werkzeug-Fehler
las sich wie „41 Artefakte kaputt".

### Negativ-Kriterien auf die Wirkstelle ankern

Ein Kriterium der Form „Begriff X kommt nicht mehr vor" nie ueber die **ganze Datei** formulieren
(`grep -c "X" = 0`), sondern auf die **Wirkstelle** ankern — die Zeile oder Sektion, die X
tatsaechlich loswerden soll. Sonst wird das Kriterium rot, obwohl die Umsetzung stimmt:
Abschaffungs-Notizen, Toleranz-Matrizen und Migrations-Hinweise **muessen** den abgeschafften
Begriff nennen.

Praxisfall 2026-07-30/31 (Feature plan-status-feld): `grep -c "In Umsetzung" … = 0` stand als
Checkpoint-Kriterium, waehrend derselbe Schritt die Altwert-Nennung in der Toleranz-Matrix
ausdruecklich forderte — das Kriterium widersprach dem eigenen Schritt-Output und war ab dem
Moment der korrekten Umsetzung dauerhaft rot.

## Distribution (kit-sync)

Skills are distributed to `~/.claude/skills/` by `dtb:kit-sync` (modes: check/sync/install).
A lock file `~/.claude/dtb-lock.json` records source, ref, and a content hash per artifact
(three-point drift detection: repo ↔ lock ↔ installed copy; hashing normalizes line endings).

- **Class A (`mode: synced`, drift-checked):** `skills/dtb-*/SKILL.md`, `agents/*.md`,
  `commands/dtb-*.md`, `output-styles/dtb-*.md` — a NEW skill is covered automatically by the
  pattern, no registration needed
- **Class B (`mode: seed`, copied once, never drift-checked):** `frameworks/` templates,
  `settings.json`, `DERIVED_STATE_RULES.md` (distributed per project by `dtb:project-init`)
- Personas are not part of the kit (removed 2026-07-23) — they live in the separate
  `oma-personas` repository; the kit carries only inline distillates (see root `CLAUDE.md`)

Lock schema and fixed command sequences live in `skills/dtb-kit-sync/SKILL.md` — do not
duplicate that logic in other skills; reference it (like `dtb:project-health` check 11 does).

## Language

- **Frontmatter keys**: English
- **Skill body** (instructions, templates, output): German
- **description field**: German trigger phrases + English summary sentence
