---
name: dtb:lesson
description: >-
  Use when: "Lektion festhalten", "lesson", "das merken wir uns", "nie wieder
  diesen Fehler", "Erkenntnis speichern", "als Regel festhalten". Captures a
  non-obvious, reusable lesson (Context/Problem/Rule/Applies-to) append-only into
  project-rules/lessons.md, read later as a prior by the plan/review skills.
disable-model-invocation: true
argument-hint: "[Lektion als Freitext]"
allowed-tools: Read, Write, Edit, Grep
pipeline:
  stage: development
  after: null
  next: null
  consumes: [project-rules/lessons.md]
  produces: [project-rules/lessons.md]
---

# Lektion erfassen

Du haeltst eine nicht-offensichtliche, wiederverwendbare Erkenntnis fest — append-only in
`lessons.md`. Spaeter lesen `impl-plan`, `debug-plan`, `plan-review` und `impl-review` diese
Datei als **Prior** und wenden passende Lektionen an. Ziel: Schnelligkeit wie bei `dtb:idea`,
kein Formular.

**Abgrenzung Session-Log ↔ Lektion:** Ein Session-Log haelt fest, *was diese Session passiert
ist* (vergaenglich). Eine Lektion ist eine *Regel, die kuenftig gilt* (dauerhaft). Trigger-Frage:
„Wuerde ich denselben Fehler nochmal machen, wenn das nur im Session-Log stuende?" → dann Lektion.

## Worktree-Guard (Schritt 0)

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions". (`lessons.md` ist
ungetrackt: in einem Worktree geschrieben ginge die Lektion beim Aufraeumen ersatzlos
verloren.)

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" && pwd); C=$(cd "$C" && pwd)
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar. Zusatz nur bei gesetztem `parallel.default_branch`
  (nicht `null`) in `workflow.config.yaml`: aktueller Branch ungleich dem Wert → Abbruch
  mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:lesson schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele Sessions").
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Wurde bereits Text uebergeben/erfasst, haengt die Meldung ihn als fertigen Befehl an —
  „Dein Text geht nicht verloren — dort absetzen: `/dtb:lesson "{erfasster Text}"`".
  Greift der Abbruch VOR dem Erfassungs-Dialog, gibt es nichts zu echoen — nur den
  Befehl ohne Text-Anteil nennen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

- Lektionen-Pfad: `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`)
- Falls `config.paths.rules` fehlt: Fallback-Pfad verwenden, kein Abbruch

---

## Schritt 1: Lektion erfassen

**Input:** Der Freitext nach dem Command-Aufruf ist die rohe Lektion. Er darf auch aus einem
Agent-Vorschlag stammen (siehe „Zwei Eingangskanaele" unten).

Falls kein Freitext angegeben wurde:
```
Welche Lektion moechtest du festhalten? (Freitext — was ist passiert, was gilt kuenftig?)
```

### Zwei Eingangskanaele
1. **Manuell:** `/dtb:lesson "..."` — der bewusste Fall.
2. **Agent-Vorschlag:** Ein anderer Skill (impl-plan/debug-plan/impl-review) hat waehrend der
   Arbeit einen Lektion-Kandidaten erkannt und dich gefragt. Bei „ja" landet der vorgeschlagene
   Text hier.

**Immer mit Bestaetigung — nie stiller Auto-Write.** Der Skill schreibt erst, nachdem der
strukturierte Eintrag (Schritt 2) gezeigt und bestaetigt wurde.

---

## Schritt 2: In 4 Felder strukturieren

Leite aus dem Freitext die vier Felder ab. Halte jedes Feld **knapp** (1 Satz).

**Feld-Hygiene (Pflicht — sonst bricht die Tabelle):** Jedes Feld muss einzeilig sein.
- Literale `|` (z.B. Shell-Pipes) im Text als `\|` escapen
- Keine Zeilenumbrueche im Feld (Backticks/Code mit Pipe umschreiben oder Pipe escapen)
- Beispiel Rule mit Pipe: `` `tr -d '\r' \| git -c core.autocrlf=false hash-object --stdin` ``

| Feld | Bedeutung |
|------|-----------|
| **Context** | In welcher Situation/Technologie trat es auf? |
| **Problem** | Was war die nicht-offensichtliche Falle? |
| **Rule** | Die kuenftig geltende Regel (imperativ: „Immer …", „Nie …", „… statt …") |
| **Applies-to** | Welche Skills sollen diese Lektion als Prior anwenden? |

### Applies-to (festes Enum)
Erlaubte Werte: `impl-plan`, `debug-plan`, `plan-review`, `impl-review`, `alle`.
- `code-review` (Legacy) wird beim **Lesen** weiter akzeptiert, aber **nicht neu vergeben** —
  `impl-review` ist der Nachfolger.
- Mehrfachnennung erlaubt (kommagetrennt), z.B. `impl-plan, impl-review`
- **Nicht ableitbar/leer → Default `alle`** (kein Reibungsverlust; kann spaeter eingegrenzt werden)
- Nur bei echter Unklarheit **eine** kurze Rueckfrage stellen, sonst `alle` setzen

Zeige den strukturierten Entwurf und hole 1 Bestaetigung ein:
```
Neue Lektion:
  Context:    {…}
  Problem:    {…}
  Rule:       {…}
  Applies-to: {…}

Speichern? (Ja / Anpassen)
```

---

## Schritt 3: Duplikat-Check

Vor dem Schreiben: `grep` in `lessons.md` nach dem Kern der `Rule` (Stichworte).
- **Aehnlicher Eintrag gefunden:** Hinweis zeigen, aber **nicht hart blocken** —
  ```
  Aehnliche Lektion existiert bereits (L{N}): "{Rule}"
  Trotzdem als neuen Eintrag speichern? (Ja / Abbrechen)
  ```
- Kein Treffer: direkt weiter zu Schritt 4.

---

## Schritt 4: Append-only speichern

### Datei
- Pfad: `{config.paths.rules}/lessons.md`
- Falls Datei nicht existiert: mit Header anlegen (Format unten)

### Format bei neuer Datei
```markdown
# Lektionen (lessons.md)

> Append-only Sammlung nicht-offensichtlicher, wiederverwendbarer Regeln.
> Erfasst mit `/dtb:lesson`, gelesen als Prior von impl-plan, debug-plan, plan-review, impl-review.
> **Nicht** manuell editieren/loeschen (append-only); Kuratierung geschieht bewusst.
> Kompakt halten — Soft-Limit ~150 Zeilen (danach aeltere, ueberholte Lektionen aussortieren).

| # | Datum | Context | Problem | Rule | Applies-to |
|---|-------|---------|---------|------|------------|
| 1 | YYYY-MM-DD | {Context} | {Problem} | {Rule} | {Applies-to} |
```

### Format bei bestehender Datei
- Neue Zeile ans Tabellenende anfuegen — **mit `Edit`** (letzte Datenzeile als Anker, neue
  Zeile dahinter einfuegen), NICHT die Datei per `Write` komplett neu schreiben. So bleiben
  bestehende Zeilen garantiert unveraendert (append-only)
- Naechste laufende Nummer vergeben
- Datum: aktuelles Datum (`YYYY-MM-DD`)

### Groessen-Warnung (Soft-Limit)
Nach dem Schreiben: Falls `lessons.md` **> ~150 Zeilen** — Hinweis ausgeben (nicht blocken):
```
Hinweis: lessons.md hat jetzt {N} Zeilen (Soft-Limit ~150). Erwaege, ueberholte
Lektionen bei Gelegenheit auszusortieren, damit der Prior kompakt bleibt.
```

### Hebe-Hinweis bei `Applies-to: alle`
Ist `Applies-to` = `alle` **und** beschreibt die `Rule` eine dauerhafte Autoring-/Projekt-Konvention
(keinen Einzelfall), zusaetzlich diesen Hinweis ausgeben (**nicht** blocken, keine Rueckfrage):
```
Hinweis: Applies-to = "alle" — dauerhafte Konvention? Dann die Regel zusaetzlich in eine
versionierte Regel-Datei heben (Kit-Repo: skills/CLAUDE.md; Projekt: {config.paths.rules}/<BEREICH>.md).
lessons.md kann per .gitignore lokal sein und reist dann nicht ueber Klone/Arbeitsorte mit.
```
Grund (Praxisfall 2026-07-29): der Lektionen-Prior lief auf **0 Treffer**, obwohl eine passende
`alle`-Lektion existierte — sie lag auf einer anderen Maschine. `lessons.md` bleibt die
append-only Historie; die verbindliche Fassung gehoert in die versionierte Regel-Datei.

---

## Schritt 5: Bestaetigung

```
Lektion L{N} gespeichert: {config.paths.rules}/lessons.md

  Rule: "{Rule}"
  Gilt fuer: {Applies-to}
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.

---

## Richtlinien

- **Schnell:** Wie `dtb:idea` — max. 1 Rueckfrage (Applies-to), sonst durchziehen
- **Kuratiert:** Duplikat-Hinweis + bewusste Bestaetigung halten die Datei rauscharm
- **Append-only:** Nie bestehende Eintraege aendern/loeschen
- **Nie stiller Auto-Write:** Immer Bestaetigung vor dem Schreiben
- **Deutsch:** Alle Texte auf Deutsch
