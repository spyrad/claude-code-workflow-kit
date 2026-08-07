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
  stage: idea | planning | implementation | development | session | monitoring | setup | greenfield
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
| `plan-review` | `features/*/plan.md` | `impl-plan` voran, `feature-start` als Alternative |
| `feature-start` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss) |
| `implement` | `features/*/plan.md` | `impl-plan` (`after`-Match ueber `feature-start` hinweg: feature-start nur Status-Updater; zusaetzlich harte Archiv-Weigerung ohne Escape-Hatch) |
| `impl-review` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss; zusaetzlich harte Archiv-Weigerung ohne Escape-Hatch) |
| `greenfield-roadmap` | `project-strategy/PRD-MVP.md` | `greenfield-prd` (`after`-Match; Pfad ist kein `features/`-Slug, sondern der feste Strategie-Pfad) |
| `debug-plan` | `features/*/bug.md` | `bug-report` (nach Selbst-Ausschluss; `debug-plan` nur Fix-Updater) |
| `feature-fast` | INBOX-Eintrag zur Idee (kein `features/`-Artefakt) | `idea` voran, `idea-review` als Alternative — **ohne Escape-Hatch** (begruendete Abweichung: die INBOX ist die einzige Erhebungsquelle des Fast-Track; ein Durchrutschen ohne Eintrag waere ein Ad-hoc-Einstieg, den die Spec explizit ausschliesst) |
| `archive` | archivierbare Kandidaten vorhanden | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu archivieren" (nativ in Schritt 3) |
| `migrate-change-folders` | flache Alt-Dateien (`features/*.md`) | kein Redirect (`after: null`) → ehrliche Meldung „nichts zu migrieren" (nativ in Schritt 1) |

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
