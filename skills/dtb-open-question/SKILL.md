---
name: dtb:open-question
description: >-
  Use when: "Fach-Frage festhalten", "offene Frage erfassen", "open question",
  "Frage fuers Meeting notieren", "[Fach]-Frage erfassen". Captures a
  subject-matter question as a §6-conform `- [ ] [Fach] {Frage}` entry in the
  active feature's `## Offene Punkte` — quick, without interrupting the work.
disable-model-invocation: true
argument-hint: "[<feature-slug>] <Fach-Frage>"
allowed-tools: Read, Glob, Grep, Edit
pipeline:
  stage: capture
  after: null
  next: [dtb:workflow-next, dtb:meeting-agenda]
  consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]
  produces: [features/*/spec.md, features/*/discovery.md]
---

# Fach-Frage erfassen (open-question)

Du erfasst eine waehrend der Arbeit auftauchende **Fach-Frage** (gehoert ins Meeting, nicht
sofort/allein beantwortbar) direkt im aktiven Feature-Artefakt — als statusfaehige, getaggte
Checkbox nach der Fach-Frage-Konvention (`{config.paths.rules}/DERIVED_STATE_RULES.md` §6). Reibungslos wie
`/dtb:idea`, aber mit kurzer Ziel-Bestaetigung vor dem Schreiben.

> **Wartungs-Hinweis (Format-Kopplung):** Die `## Offene Punkte`-Sektion hat **vier Akteure**
> auf derselben §6-Kanonform (`- [ ] [Fach] {Frage}`): drei **Erzeuger** — `dtb:feature-discover`
> (schreibt in `discovery.md`), `dtb:feature-plan` (in `spec.md`) und open-question (in beide) —
> plus einen **Mutator**, `dtb:meeting-dump` (Meeting-Rueckfluss #24: legt keine neuen
> `[Fach]`-Fragen an, sondern kippt die Checkbox und haengt `→ Antwort:`/`→ Zwischenstand:`
> an bestehende an). Single Source der Grammatik ist `{config.paths.rules}/DERIVED_STATE_RULES.md` §6 —
> aenderst du sie dort, ziehe alle vier Akteure mit.

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

## Schritt 2: Ziel-Feature ermitteln (Ableiten oder Slug-Override)

Die Frage wird im `## Offene Punkte` **eines** Feature-Ordners abgelegt. Das Ziel wird so bestimmt:

### a) Expliziter Slug-Override
Matcht das **erste Token** des Arguments **exakt einen vorhandenen, nicht-leeren** Ordner
`{config.paths.workflows}/features/<slug>/`, gilt es als Slug-Override: dieser Ordner ist das Ziel,
der Rest des Arguments ist die Frage.
**Andernfalls liegt KEIN Override vor** — das **gesamte** Argument ist die Frage, weiter zu (b).
Ein absichtlich gemeinter, aber ungueltiger Slug wird so zunaechst zur Frage; die
Variante-B-Bestaetigung (Schritt 4.3) macht das ermittelte Ziel sichtbar, bevor geschrieben wird,
und ein Ziel ohne `spec.md`/`discovery.md` landet ueber Schritt 3 im definierten Abbruch.

### b) Kein Slug → aktives Feature ableiten
Ableitung nach `{config.paths.rules}/DERIVED_STATE_RULES.md` §1.1: scanne
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

## Schritt 3: Ziel-Datei waehlen

Im Ziel-Feature-Ordner wird die **am weitesten fortgeschrittene** Datei mit `## Offene Punkte`
beschrieben:

1. `spec.md` vorhanden → **`spec.md`**
2. sonst `discovery.md` vorhanden → **`discovery.md`**
3. sonst (nur `plan.md`/`bug.md`/`task.md`) → **abbrechen** — `## Offene Punkte` gehoert nicht in
   diese Dateien (MVP-Schnitt, Feature `fachfragen-erfassung` #13):
   ```
   Feature „<slug>" hat weder spec.md noch discovery.md — kein Ablage-Ort fuer die Fach-Frage.
   Lege zuerst eine Spec an:  /dtb:feature-plan <Feature-Name>
   ```

> **Kein formales Eligibility-Gate (bewusst):** open-question ist ein Capture-Tool wie `/dtb:idea`
> (`disable-model-invocation: true`). Der Abbruch oben ist ein **weicher Redirect**, kein Hard-Gate
> nach `skills/CLAUDE.md` — der Ablage-Ort ist nicht erzwingbar, es gibt keine Escape-Hatch.

---

## Schritt 4: Zeile formatieren, Duplikat pruefen, Ziel bestaetigen

1. **§6-Kanonform bilden** (nur diese Form matcht die spaetere Agenda-Ansicht exakt):
   `- [ ] [Fach] <normalisierte Frage>` — genau ein Leerzeichen zwischen Checkbox, Tag und Frage.

2. **Duplikat-Schutz (exakter Textvergleich):** Lies die `## Offene Punkte`-Sektion **beider**
   vorhandenen Dateien des Feature-Ordners (`spec.md` **und** `discovery.md`) — die Fach-Frage-
   Konvention ist dateiunabhaengig (§6.3). Steht in einer davon bereits eine **offene**
   `- [ ] [Fach] …`-Zeile mit identischem Fragetext (nach derselben Normalisierung) → **warnen und
   ueberspringen**, nicht doppelt schreiben:
   ```
   Diese Fach-Frage steht schon offen in features/<slug>/<datei>:
     - [ ] [Fach] <Frage>
   Nichts geschrieben.
   ```
   (Nur exakter Vergleich — kein Fuzzy-Matching.)

3. **Ziel bestaetigen (Variante B — immer):** Ziel + formatierte Zeile anzeigen, auf kurze Freigabe
   warten. Kam das Ziel aus einem Slug-Override (2a), die Herkunft ausweisen — so faellt eine
   Fehl-Trennung (Fragewort als Slug interpretiert) vor dem Schreiben auf. Erst nach Freigabe zu Schritt 5:
   ```
   → Schreibe nach features/<slug>/<datei> (## Offene Punkte):
     - [ ] [Fach] <Frage>
   [nur bei Slug-Override] Ziel-Slug: <slug> (aus 1. Token uebernommen)
   Passt das? (ok / abbrechen)
   ```

---

## Schritt 5: Schreiben + Abschluss

1. **Platzierung (robust):** Bestimme das **Ende des Textblocks** der `## Offene Punkte`-Sektion =
   die **letzte echte Inhaltszeile** (letzter Bullet) der Sektion. Die naechste `##`-Ueberschrift,
   ein abschliessender `---`-Separator, der `**Erstellt mit:**`-Footer und das Dateiende sind nur
   **End-Grenzen** der Sektion — **nie** der Einfuegepunkt. Fuege die neue Zeile **direkt nach der
   letzten Inhaltszeile** ein, oberhalb evtl. folgender Leerzeilen/`---`/Footer.
2. **Fehlt die Sektion** → `## Offene Punkte` neu anlegen (Header + Leerzeile + Zeile). Platziere den
   Block **nach der letzten Inhaltssektion**, oberhalb eines abschliessenden `---`/`**Erstellt mit:**`-
   Footers; fehlt beides, ans Dateiende.
3. **Bestehende Eintraege unangetastet:** beantwortete `- [x] [Fach] …`-Zeilen und eingerueckte
   `→ Antwort: …`-Fortsetzungszeilen bleiben an Ort und Stelle — **nur anhaengen, nie umsortieren
   oder verschieben**.
4. **Status-Neutralitaet (Invariante):** ausschliesslich `## Offene Punkte` schreiben. **Nie**
   `## Progress`, dortige Checkboxen oder Statusfelder beruehren — das Erfassen aendert den
   abgeleiteten Feature-Status nicht (§6.2).
5. **Abschluss-Bestaetigung (kompakt):**
   ```
   Fach-Frage erfasst → features/<slug>/<datei>:
     - [ ] [Fach] <Frage>

   Sammelansicht spaeter via /dtb:meeting-agenda (Agenda aller offenen Fach-Fragen).
   ```

---

**Erstellt mit:** `/dtb:open-question`
