---
name: dtb:meeting-agenda
description: >-
  Use when: "Meeting-Agenda", "Agenda fuers Fach-Meeting", "offene Fachfragen",
  "was besprechen wir", "Fach-Fragen zeigen", "meeting agenda". Read-only skill
  collecting all open [Fach] questions from features/*/{discovery,spec,plan}.md
  and printing them grouped by feature as a ready-to-use meeting agenda.
disable-model-invocation: false
argument-hint: "[alle]"
allowed-tools: Read, Glob, Grep
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [features/*/discovery.md, features/*/spec.md, features/*/plan.md, project-rules/DERIVED_STATE_RULES.md]
  produces: []
---

# DTB Meeting-Agenda

Sammelt die offenen `[Fach]`-Fragen aus allen aktiven Changes und gibt sie als fertige
Agenda fuer das Fach-Meeting aus — nach Feature gruppiert, rein lesend.

Die Lese-Ansicht der Fachfragen-Kette: `dtb:open-question` erfasst die Fragen,
dieser Skill sammelt sie vor dem Meeting ein, `dtb:meeting-dump` spielt die Antworten
danach zurueck.

## Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 2: Format-Kanon lesen

Lies `{config.paths.rules}/DERIVED_STATE_RULES.md` §6 (Fallback:
`dtb-project/project-rules/DERIVED_STATE_RULES.md`).

**Dieser Skill traegt keine eigene Format-Logik** — §6 ist die einzige Quelle fuer die
Fach-Frage-Grammatik. Fehlt die Regel-Datei, arbeite nach der unten beschriebenen
Kanonform weiter und gib eine Hinweiszeile aus:
`⚠ DERIVED_STATE_RULES.md nicht gefunden — Kanonform aus dem Skill verwendet`

## Schritt 3: Argument auswerten

| Argument | Modus |
|----------|-------|
| _(leer)_ | **Standard** — nur offene Fragen, je Frage nur der **letzte** Zwischenstand |
| `alle` | **Voll** — zusaetzlich der Abschnitt „Zuletzt geklaert" (beantwortete Fragen) und je Frage der **volle** Zwischenstands-Verlauf |

Ein anderes Argument → wie Standard behandeln, plus Hinweiszeile:
`Unbekanntes Argument "{X}" — ignoriert (bekannt: alle)`

## Schritt 4: Scannen

**Quellen:** `{config.paths.workflows}/features/*/discovery.md`, `spec.md`, `plan.md`.
`archive/` wird **nicht** gescannt — abgeschlossene Changes gehoeren nicht auf die Agenda.

**Aufnahmekriterium (verbindlich, beide Bedingungen):**

1. Die Zeile steht **innerhalb einer `## Offene Punkte`-Sektion** (ab der Ueberschrift
   bis zur naechsten `## `-Ueberschrift bzw. zum Dateiende)
2. Die Zeile hat die Kanonform `- [ ] [Fach] <Frage>` bzw. `- [x] [Fach] <Frage>`
   (je ein Leerzeichen zwischen Checkbox, Tag und Frage, §6)

> **Die Sektions-Bedingung ist kein Feinschliff, sondern der Kern der Korrektheit.**
> Im Bestand stehen `[Fach]`-Zeichenketten auch in Fliesstext, der die Konvention
> *dokumentiert* (z.B. `features/fachfragen-erfassung/discovery.md`). Ein Scan, der nur
> auf die Zeilenform prueft, sammelt diese Doku-Zeilen als vermeintliche Fragen ein.
> Beide Bedingungen zusammen schliessen das aus.

**Fortsetzungszeilen:** Eingerueckte Zeilen unmittelbar unter einem Frage-Bullet gehoeren
zu dieser Frage. Es gibt **drei** Formen — die ersten beiden sind Meeting-Nachtraege (§6.1),
die dritte ist blosser Zeilenumbruch:

- `→ Zwischenstand: … (Meeting YYYY-MM-DD)` — Frage bleibt offen, mehrere sind erlaubt
  und akkumulieren
- `→ Antwort: … (Meeting YYYY-MM-DD)` — steht unter einer abgehakten Frage
- **eingerueckte Zeile ohne `→`-Praefix** — Umbruch des Fragetexts: an den Fragetext
  anfuegen (mit einem Leerzeichen verbunden), nicht als eigener Eintrag behandeln

> **Umbrueche sind der Normalfall, nicht die Ausnahme** (Befund Probelauf 2026-08-02):
> Lange Fragen werden beim Erfassen umgebrochen. Wer nur die erste Zeile nimmt,
> schneidet sie mitten im Satz ab — im Bestand traf das die einzige echte Frage, deren
> zweite Zeile die Einschraenkung „aber selbst kein Blocker" traegt. Das Abschneiden
> wuerde der Richtlinie „Fragen woertlich uebernehmen" widersprechen.

**Nicht aufnehmen:** untagged Bullets (normale offene Punkte, §6.3), Zeilen ausserhalb
von `## Offene Punkte`, alles unter `archive/`.

## Schritt 5: Gruppieren & ausgeben

Gruppiere nach Change-Ordner (Slug), innerhalb einer Gruppe nach Datei-Reihenfolge
`discovery.md` → `spec.md` → `plan.md`. Features ohne offene Frage erscheinen nicht.

Eine Frage mit mindestens einem `→ Zwischenstand:` wird mit `[in Klaerung]` markiert.

### Standard-Ausgabe

```
# Meeting-Agenda

**Stand:** {YYYY-MM-DD} · {N} offene Fragen aus {M} Changes

## {feature-slug}

- [ ] {Frage}
- [ ] {Frage}  [in Klaerung]
      → Zwischenstand: {Text} (Meeting {YYYY-MM-DD})

## {feature-slug}

- [ ] {Frage}

---

Antworten nach dem Meeting zurueckspielen: /dtb:meeting-dump
```

Bei `[in Klaerung]` erscheint im Standard **nur der letzte** Zwischenstand — der Verlauf
bleibt im Artefakt und ist ueber `alle` abrufbar. Sonst waechst die Agenda mit jedem
Meeting, obwohl sie das Meeting vorbereiten soll.

### Zusaetzlich im `alle`-Modus

Je Frage der **volle** Zwischenstands-Verlauf (alle `→ Zwischenstand:`-Zeilen in
Datei-Reihenfolge), und am Ende:

```
## Zuletzt geklaert

### {feature-slug}
- [x] {Frage}
      → Antwort: {Text} (Meeting {YYYY-MM-DD})
```

**Keine beantworteten Fragen im Bestand:** Der Abschnitt erscheint trotzdem, mit der Zeile
`_(keine beantworteten [Fach]-Fragen im Bestand)_`. Er wird **nicht** stillschweigend
weggelassen — sonst sieht der `alle`-Modus aus wie der Standard-Modus, und der Nutzer
weiss nicht, ob sein Argument gewirkt hat.

### Leer-Fall (keine offene Frage gefunden)

```
Keine offenen [Fach]-Fragen — die Agenda ist leer.

Fragen fuers Fach-Meeting erfasst du mit:
  /dtb:open-question [feature-slug] {Frage}

Geprueft: {config.paths.workflows}/features/*/{discovery,spec,plan}.md
          (## Offene Punkte, archive/ ausgeschlossen)
```

Den geprueften Umfang immer mit ausgeben — sonst ist nicht unterscheidbar, ob nichts
offen ist oder der Scan ins Leere lief.

## Richtlinien

- **Read-Only:** Dieser Skill aendert keine Datei. Er legt keine Fragen an
  (`/dtb:open-question`) und traegt keine Antworten nach (`/dtb:meeting-dump`)
- **Kein zweiter Speicherort:** Die Agenda ist ein Chat-Report, keine Datei — die Fragen
  leben im Artefakt, jeder Aufruf liest frisch
- **Fragen woertlich uebernehmen:** nicht umformulieren, kuerzen oder zusammenfassen —
  die Formulierung ist die des Fragestellers
- **Keine Rueckfragen:** sofort ausgeben
- **Kompakt:** eine Zeile pro Frage plus ggf. Zwischenstand
- **Deutsch:** alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:open-question` — erfasst eine Fach-Frage im Artefakt (Eingabe-Seite)
- `/dtb:meeting-dump` — spielt die Antworten nach dem Meeting zurueck (Rueckfluss)
- `/dtb:workflow-next` — naechster Schritt pro Feature (andere Lese-Ansicht)

---

Scanne jetzt die Change-Ordner und gib die Agenda aus.
