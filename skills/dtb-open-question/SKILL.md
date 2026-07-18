---
name: dtb:open-question
description: >-
  Use when: "Fach-Frage festhalten", "offene Frage erfassen", "open question",
  "Frage fuers Meeting notieren", "[Fach]-Frage erfassen". Captures a
  subject-matter question as a §6-conform `- [ ] [Fach] {Frage}` entry in the
  active feature's `## Offene Punkte` — quick, without interrupting the work.
disable-model-invocation: true
argument-hint: "[<feature-slug>] <Fach-Frage>"
allowed-tools: Read, Glob, Grep, Edit, Write
pipeline:
  stage: capture
  after: null
  next: [dtb:workflow-next]
  consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]
  produces: [features/*/spec.md, features/*/discovery.md]
---

# Fach-Frage erfassen (open-question)

Du erfasst eine waehrend der Arbeit auftauchende **Fach-Frage** (gehoert ins Meeting, nicht
sofort/allein beantwortbar) direkt im aktiven Feature-Artefakt — als statusfaehige, getaggte
Checkbox nach der Fach-Frage-Konvention (`DERIVED_STATE_RULES.md` §6). Reibungslos wie
`/dtb:idea`, aber mit kurzer Ziel-Bestaetigung vor dem Schreiben.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Fach-Frage erfassen

**Input:** Das Argument nach dem Command-Aufruf. Ein optionaler fuehrender **Feature-Slug**
(siehe Schritt 2 a) wird abgetrennt; der Rest ist die Frage.

- **Leeres/fehlendes Frage-Argument** → nachfragen (nicht abbrechen):
  ```
  Welche Fach-Frage moechtest du festhalten?
  ```
- **Sonderzeichen/Markdown** in der Frage (z.B. `[...]`, Backticks) → 1:1 als Inline-Text
  uebernehmen; nichts escapen.
- **Mehrzeilige Eingabe** → zu **einer** Zeile normalisieren (Zeilenumbrueche durch Leerzeichen
  ersetzen, Mehrfach-Leerzeichen zusammenfassen). Die §6-Grammatik verlangt genau **eine**
  Bullet-Zeile.

---

## Schritt 2: Ziel-Feature ermitteln (Variante c)

Die Frage wird im `## Offene Punkte` **eines** Feature-Ordners abgelegt. Das Ziel wird so bestimmt:

### a) Expliziter Slug-Override
Entspricht das **erste Token** des Arguments exakt einem vorhandenen Ordner
`{config.paths.workflows}/features/<slug>/`, ist das das Ziel; der Rest des Arguments ist die Frage.
- Ordner fehlt oder ist leer → **abbrechen** (kein Auto-Anlegen — das ist `feature-discover`s Job):
  ```
  Feature „<slug>" nicht gefunden. Vorhandene Feature-Ordner:
    - <slug-1>
    - <slug-2>
  Nutzung:  /dtb:open-question <slug> "<Frage>"
  ```

### b) Kein Slug → aktives Feature ableiten
Ableitung nach `DERIVED_STATE_RULES.md` §1.1: scanne
`{config.paths.workflows}/features/*/plan.md` und zaehle in `## Progress` die Checkboxen —
ein Feature ist **„In Arbeit"**, wenn `0 < abgehakt < gesamt`.

- **Genau 1 aktiv** → dieses Feature ist das Ziel.
- **0 aktiv + kein Slug** → **abbrechen** (kein Schreiben ins Blaue):
  ```
  Kein aktives Feature. Ziel angeben:  /dtb:open-question <slug> "<Frage>"
  Waehlbare Feature-Ordner:
    - <slug-1>
    - <slug-2>
  ```
- **>1 aktiv** → **Auswahlliste** zeigen, Nutzer waehlt (kein stilles Raten):
  ```
  Mehrere Features in Arbeit — wohin gehoert die Frage?
    1. <slug-1> (X/Y)
    2. <slug-2> (X/Y)
  ```

Das ermittelte Ziel-Feature (Slug) geht in Schritt 3.

---

> **In Umsetzung (Phase 2 dieses Plans):** Ziel-Datei-Wahl, Variante-B-Bestaetigung,
> §6-konformes Schreiben in `## Offene Punkte`, Duplikat-Schutz und Abschluss-Bestaetigung
> folgen als Schritt 3–5.

---

**Erstellt mit:** `/dtb:impl-plan` → `/dtb:implement`
