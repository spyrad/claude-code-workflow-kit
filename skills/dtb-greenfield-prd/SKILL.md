---
name: dtb:greenfield-prd
description: >-
  Use when: "PRD erstellen", "Produkt-Anforderungen erarbeiten", "PRD-Interview",
  "PRD zeigen", "Anforderungen", "MVP requirements", "Product Requirements".
  Two-mode greenfield skill: authors project-strategy/PRD-MVP.md through a
  structured product interview when it is missing, otherwise summarizes the
  existing PRD (report mode).
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: greenfield
  after: null
  next: [dtb:greenfield-roadmap]
  consumes: [PRD-MVP.md, project-strategy/*.md, INBOX.md, workflow.config.yaml]
  produces: [PRD-MVP.md]
---

# Greenfield PRD

Zwei-Modus-Skill fuer die Aufbauphase eines Projekts:

- **Autoren-Modus** (kein `PRD-MVP.md`): fuehrt ein gruendliches, unterbrechbares
  Produkt-Interview und erzeugt ein technikfreies `project-strategy/PRD-MVP.md`.
- **Report-Modus** (`PRD-MVP.md` existiert): fasst das vorhandene PRD zusammen.

Fehlende Inhalte werden **nie erfunden**, sondern woertlich als `## Open Questions`
gefuehrt. Technische Festlegungen gehoeren nicht ins PRD (Redirect → `TECH-STACK.md`).

> **Brownfield-Hinweis:** Dieser Skill ist fuer die Aufbauphase gedacht. In einem
> bestehenden Projekt aufgerufen laeuft er trotzdem (keine Verweigerung, kein
> Auto-Detect) — pruefe nur, ob ein PRD hier ueberhaupt der richtige Einstieg ist.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root fuer den Projektnamen.
Falls nicht vorhanden: Frage den Projektnamen ab.

Zielpfad des PRD: `dtb-project/project-strategy/PRD-MVP.md` (im Folgenden „das PRD").

---

## Schritt 1: Modus-Weiche (dreistufig)

Pruefe, ob das PRD existiert, und lies bei Existenz die erste Zeile nach dem Header
auf einen Resume-Marker `<!-- resume: {Kategorie} -->`.

> **Vorrang-Regel (verbindlich):** Ein Resume-Marker ungleich `done` hat **Vorrang
> vor der Existenz-Regel**. Ein angefangenes Interview wird fortgesetzt, nicht als
> „vorhandenes PRD" in den Report-Modus umgeleitet.

1. **PRD existiert MIT `<!-- resume: {K} -->`-Marker ≠ `done`**
   → **Autoren-Modus fortsetzen** ab der Kategorie *nach* `{K}` (Schritt 2).
   Bereits beantwortete Kategorien nicht erneut fragen.
2. **PRD existiert (kein Marker oder Marker = `done`)**
   → **Report-Modus** (Schritt R). Eine Neuerzeugung erfolgt nur auf **expliziten
   Wunsch** des Nutzers und dann ueber den Kollisions-Dialog (Schritt 4).
3. **PRD fehlt**
   → **Autoren-Modus neu** (Schritt 2).

Es gibt **keinen vierten Zweig**: Ein vorhandenes, aber inhaltlich duennes PRD wird
nicht automatisch wieder geoeffnet (das ist Sache des Readiness-Checks in
`greenfield-roadmap`).

---

## Autoren-Modus

### Schritt 2·0: build/buy-Nudge (nur frischer Start, kein Resume)

**Nur wenn dieser Lauf ein frischer Autoren-Modus ist (Modus-Weiche Zweig 3: PRD fehlt) —
NICHT bei Resume-Fortsetzung (Zweig 1) und NICHT im Report-Modus (Zweig 2).** Pruefe, ob
`dtb-project/project-strategy/OPPORTUNITY-MAP.md` existiert:

- **Map existiert** → diesen Schritt **still ueberspringen** (build/buy wurde bereits gesichtet;
  die Map wird in Schritt 2a ohnehin als Quellmaterial aufgegriffen).
- **Keine Map** → **genau einen** Hinweis ausgeben (kein Zwang, kein Hard-Gate, keine Wiederholung):

  ```
  Bevor wir das PRD schreiben: Ist die build/buy-Frage geklaert?
  Fuer ein Greenfield-MVP lohnt oft ein kurzer Blick, ob ein bestehendes Produkt den Bedarf
  schon deckt (kaufen/komplementieren) statt neu zu bauen.
    1. Zuerst build/buy sichten → /dtb:opportunity-map  (kein Auto-Start, nur Empfehlung)
    2. Weiter mit dem PRD-Interview
  ```

  Waehlt der Nutzer **2** → normal mit Schritt 2a fortfahren. Waehlt er **1** → hier stoppen und
  `/dtb:opportunity-map` empfehlen (Hand-off, **kein** Auto-Chaining). Der Nudge blockiert nie.

<!-- L5-Gegen-Hinweis (Format-Kopplung, Gegenrichtung): Nudge-Bedingung + Quellmaterial-Glob
     (Schritt 2a) sind an `dtb:opportunity-map` gekoppelt — Artefaktname `OPPORTUNITY-MAP.md`,
     Ort `dtb-project/project-strategy/`. Aenderst du Name/Ort/Ausschlussliste, den
     opportunity-map-Skill mitdenken (dort steht die Gegenrichtung). -->

### Schritt 2a: Quellmaterial anbieten

Bevor das Interview startet, sammle vorhandenes Material und biete es als Input an:

1. `Glob project-strategy/*.md` — **ohne** `PRD-MVP.md`, `ROADMAP.md`, `TECH-STACK.md`
   (das sind `docs-extract`-Ergebnisse und andere Strategie-Notizen).
2. Lies `dtb-project/project-workflows/INBOX.md`, falls vorhanden, und sammle offene Ideen.

Zeige die Funde und frage, was als Ausgangsmaterial einfliessen soll:

```
Gefundenes Quellmaterial:
  Strategie-Dokumente:
    1. project-strategy/{DATEI}.md — {1-Zeilen-Inhalt}
  INBOX-Ideen:
    2. #{N} — {Idee-Text}

Welche dieser Quellen soll ich als Ausgangsmaterial verwenden? (Nummern, "alle" oder "keine")
```

Gibt es kein Quellmaterial: eine Zeile Hinweis, dann direkt ins Interview.

### Schritt 2b: Produkt-Interview (6 Kategorien)

Gehe **Kategorie fuer Kategorie** vor: stelle die Fragen einer Kategorie, warte auf
Antwort, dann die naechste. Die 6 Kategorien spiegeln 1:1 die Template-Sektionen
(Schritt 3) — nichts wird erhoben, das keinen Zielort im PRD hat:

- **(a) Vision & Problem:** Welches Problem loest das Produkt fuer wen? Was ist die
  Produkt-Vision in 1-2 Saetzen? Woran misst sich Erfolg (Erfolgskriterien)?
- **(b) Zielgruppen / Personas:** Wer nutzt das Produkt? Beduerfnis und Hauptnutzen je Persona.
- **(c) Feature-Priorisierung:** Welche Funktionen sind Must-Have (MVP-kritisch),
  welche Should-Have, welche Nice-to-Have?
- **(d) User Stories + Akzeptanzkriterien:** Die wichtigsten Nutzer-Ablaeufe als
  „Als … moechte ich … damit …", je mit pruefbaren Akzeptanzkriterien.
- **(e) Nicht-funktionale Anforderungen:** Performance, Sicherheit, Usability,
  Verfuegbarkeit — soweit fuer das MVP relevant.
- **(f) Scope-Abgrenzung:** Was ist bewusst **nicht** Teil des MVP? Abhaengigkeiten, Risiken.

**Resume-Marker (Pflicht):** Speichere nach **jeder** beantworteten Kategorie den bis
dahin befuellten PRD-Entwurf (Template aus Schritt 3) in das PRD und setze in der Zeile
direkt unter dem Header `<!-- resume: {zuletzt beantwortete Kategorie, z.B. c} -->`.
So ist das Interview unterbrechbar und ohne Doppelfragen wiederaufnehmbar (bewusst ein
HTML-Kommentar, damit `project-health`/`pipeline-graph` unveraendert bleiben).

**Thin-Input-Warnung:** Liefert eine Kategorie fast nichts, benenne **konkret** das
fehlende Signal und seine Konsequenz (z.B. „Ohne Personas kann `greenfield-roadmap`
keine North-Star-Slice empfehlen") und biete „Trotzdem weiter" an. Ein duennes PRD mit
grossem `## Open Questions` ist gueltig — **kein Abbruch**, Luecken sichtbar machen.

### Schritt 3: PRD-Template + „Nie erfinden"-Hard-Rule

Das erzeugte `PRD-MVP.md` ist **deutsch und technikfrei** und folgt exakt dieser
Sektionsstruktur (kompatibel zum Report-Modus):

```markdown
# PRD-MVP: {config.project_name}
<!-- resume: done -->

**Stand:** {YYYY-MM-DD}

## Produkt-Vision
[Elevator Pitch (1-2 Saetze) + Erfolgskriterien]

## Zielgruppen
[Personas: Beduerfnis + Hauptnutzen]

## Features
[Must-Have / Should-Have / Nice-to-Have]

## User Stories
[US-N: Als … moechte ich … damit … + Akzeptanzkriterien]

## Nicht-funktionale Anforderungen
[Performance / Sicherheit / Usability / …]

## Out of Scope
[Was bewusst NICHT zum MVP gehoert]

## Abhaengigkeiten
[Externe/interne Abhaengigkeiten]

## Risiken
[Risiko / Wahrscheinlichkeit / Impact / Mitigation]

## Open Questions
[Woertlich jede offene Frage, nummeriert — siehe Hard-Rule]
```

> **Format-Kopplung (Gegen-Hinweis):** Die Sektionsnamen dieses Templates
> (`## Produkt-Vision`, `## Zielgruppen`, `## Features`, `## User Stories`,
> `## Out of Scope`) werden von `dtb:greenfield-roadmap` geparst (Readiness-Check +
> Slice-Ableitung). Aenderst du die Sektionsnamen, den Parser dort mitdenken (L5-Muster).

**„Nie erfinden"-Hard-Rule:** Fehlt eine Information, fuelle sie **nicht** mit einer
plausiblen Annahme. Trage sie stattdessen **woertlich** als nummerierte Frage unter
`## Open Questions` ein. Eine sichtbare Luecke ist besser als ein verstecktes
Rateergebnis. Kein `[TODO]`-Platzhalter — eine echte Frage.

**Technikfrei:** Vendor-/Framework-/Datenstruktur-/Pfad-Nennungen gehoeren nicht ins
PRD, sondern nach `TECH-STACK.md`. Der Selbst-Review vor dem Schreiben (Schritt 4)
prueft das mit dem Technical-Leak-Lint.

### Schritt 4: Selbst-Review VOR dem Schreiben

Bevor irgendetwas auf Platte geschrieben wird, pruefe den fertigen PRD-Entwurf. Beide
Pruefungen sind **Hard-Blocks**: Bei einem Verstoss wird **nicht** geschrieben, der
konkrete Befund gemeldet und (kein stilles Umschreiben) auf Korrektur gewartet.

**4a) Struktur-Check:** Alle Template-Sektionen aus Schritt 3 vorhanden und in der
richtigen Reihenfolge (`## Produkt-Vision` → `## Zielgruppen` → `## Features` →
`## User Stories` → `## Nicht-funktionale Anforderungen` → `## Out of Scope` →
`## Abhaengigkeiten` → `## Risiken` → `## Open Questions`)? Fehlt eine Sektion oder ist
die Reihenfolge verletzt → Abbruch mit Nennung der fehlenden/verschobenen Sektion.

**4b) Technical-Leak-Lint:** Das PRD beschreibt das **Was/Warum**, nicht das **Wie**.
Ein Treffer = eine leckende Phrase (nicht pro Wort); trifft eine Phrase mehrere
Kategorien, nur die zutreffendste melden. Anker ist die PRD-Sektion + Zitat.

| # | Kategorie | Leck (verboten) | Stattdessen |
|---|-----------|-----------------|-------------|
| 1 | Vendor-/Produktname | „in PostgreSQL/Redis/S3 speichern" | „persistent speichern" |
| 2 | ORM-/Query-Notation | „`User.objects.filter()`", „`SELECT …`" | „Nutzer nach Kriterium finden" |
| 3 | Transport/Protokoll | „per REST `POST /users`", „WebSocket" | „Nutzer legt Datensatz an" |
| 4 | Implementierungs-Verb | „instanziiere", „iteriere", „caste" | „das System verarbeitet …" |
| 5 | Konkrete Datenstruktur | „`Dict[str, List]`", „Array von Objekten" | „Zuordnung von X zu Y" |
| 6 | Framework-/Library-Name | „mit React/FastAPI/Pydantic" | „Oberflaeche/Schnittstelle …" |
| 7 | Datei-/Pfad-/Klassenname | „`services/auth.py`", Klasse `AuthManager` | „im Authentifizierungs-Teil" |

> **Bewusste Kopie (Entscheidung E):** Diese 7 Kategorien sind eine bewusste Kopie des
> Leak-Lints aus `dtb:feature-plan` (kein Import-Mechanismus). Aenderst du hier die
> Kategorien, den Lint in `feature-plan` mitdenken — dort steht der Gegen-Hinweis.

**Redirect statt bloss Fehler:** Ein Leck ist meist eine Stack-Entscheidung am falschen
Ort. Melde konstruktiv: „gehoert in `TECH-STACK.md`" (Zustaendigkeit von `greenfield-roadmap`).

**Meldeformat bei Verstoss** (Write abgebrochen, Datei NICHT geschrieben):
```
❌ Selbst-Review: {N} Befund(e), Write abgebrochen
  Struktur: {fehlende/verschobene Sektion}
  Leak [{Kategorie}] in {## Sektion}: „{Fund}" → gehoert in TECH-STACK.md
```
Danach korrigieren und erneut pruefen. Ein **fachlich echter** Begriff (z.B. „Export nach
SAP" als Anforderung) ist zulaessig — nur mit Markierung `<!-- Lint-Override: {Begruendung} -->`
an der Stelle; eine markierte Stelle zaehlt beim erneuten Pruefen nicht mehr als Leck.

### Schritt 5: Speichern + Kollisions-Dialog

- **Autoren-Modus, PRD existierte nicht (oder Resume-Fortsetzung):** Nach bestandenem
  Selbst-Review das PRD schreiben und den Resume-Marker final auf `<!-- resume: done -->`
  setzen. Ordner `project-strategy/` bei Bedarf anlegen.
- **Explizite Neuerzeugung bei vorhandenem, fertigem PRD:** Erst der Kollisions-Dialog:

  ```
  PRD-MVP.md existiert bereits. Wie vorgehen?
    1. Archivieren + ersetzen (Recommended)
    2. Ueberschreiben (alte Version geht verloren)
    3. Abbrechen
  ```

  Bei **1**: bestehendes PRD nach `project-strategy/archive/YYYY-MM-DD-PRD-MVP.md`
  verschieben (Ordner `archive/` lazy anlegen; zweiter Lauf am selben Tag →
  `-2`/`-3`-Suffix), dann neues PRD schreiben. In einem **Nicht-Git-Projekt** genuegt ein
  einfacher Filesystem-Move — das Archiv **ist** die Sicherung, kein zusaetzliches Backup.
  Bei **2**: direkt ueberschreiben. Bei **3**: nichts schreiben.

### Schritt 6: Hand-off

Nach dem Schreiben genau **eine** Empfehlung, **kein** Auto-Chaining:

```
PRD-MVP.md erstellt: dtb-project/project-strategy/PRD-MVP.md

Naechster Schritt: /dtb:greenfield-roadmap
  (fuehrt die Stack-Besprechung und leitet die Roadmap aus dem PRD ab)
```

---

## Report-Modus

Existiert ein vollstaendiges PRD (Marker `done` oder keiner), erstelle eine kompakte
Zusammenfassung — keine Neuerhebung. Lies `PRD-MVP.md` und fasse zusammen:

- **Produkt-Vision:** Elevator Pitch + Erfolgskriterien
- **Zielgruppen:** Personas mit Beduerfnis/Hauptnutzen
- **Features:** Must-Have (MVP-kritisch), Should-Have, Nice-to-Have — je 1 Zeile
- **User Stories:** die wichtigsten mit Akzeptanzkriterien
- **Nicht-funktionale Anforderungen:** Performance, Sicherheit, Usability
- **Out of Scope, Abhaengigkeiten, Risiken:** je kompakt
- **Open Questions:** offene Punkte hervorheben (Signal fuer Readiness in der Roadmap)

Schliesse mit dem Hinweis, dass eine Neuerzeugung nur auf expliziten Wunsch ueber den
Kollisions-Dialog (Schritt 4) laeuft, und mit dem naechsten Schritt
`/dtb:greenfield-roadmap`.

---

## Richtlinien

- **Nie erfinden:** Luecken → `## Open Questions`, nicht plausibel auffuellen
- **Technikfrei:** technische Festlegungen → `TECH-STACK.md`
- **Unterbrechbar:** Resume-Marker nach jeder Interview-Kategorie
- **Kein Auto-Chaining:** Hand-off als Empfehlung, nie automatische Skill-Invokation
- **Deutsch:** Alle erzeugten Texte auf Deutsch

## Verwandte Commands

- `/dtb:greenfield-roadmap` — Stack-Besprechung + Lean-Roadmap (konsumiert das PRD)
- `/dtb:docs-extract` — extrahiert Quellmaterial nach `project-strategy/`
