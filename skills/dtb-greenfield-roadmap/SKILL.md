---
name: dtb:greenfield-roadmap
description: >-
  Use when: "Roadmap erstellen", "Roadmap ableiten", "Projekt-Roadmap planen",
  "Tech-Stack besprechen", "Roadmap zeigen", "Meilensteine". Two-mode greenfield
  skill: authors project-strategy/ROADMAP.md (plus TECH-STACK.md) from the PRD via
  a stack discussion and a lean interview, otherwise summarizes the existing roadmap.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: greenfield
  after: [dtb:greenfield-prd]
  next: [dtb:feature-discover]
  consumes: [PRD-MVP.md, TECH-STACK.md, ROADMAP.md, workflow.config.yaml]
  produces: [ROADMAP.md, TECH-STACK.md]
---

# Greenfield Roadmap

Zwei-Modus-Skill fuer die Aufbauphase:

- **Autoren-Modus** (kein `ROADMAP.md`): fuehrt eine kompakte Stack-Besprechung
  (→ `TECH-STACK.md`) und ein Lean-Interview, zerlegt das PRD in vertikale Slices mit
  Change-IDs und schreibt `project-strategy/ROADMAP.md`.
- **Report-Modus** (`ROADMAP.md` existiert): fasst die vorhandene Roadmap zusammen.

> **Brownfield-Hinweis:** fuer die Aufbauphase gedacht. In einem bestehenden Projekt
> laeuft der Skill trotzdem (kein Auto-Detect, keine Verweigerung).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root fuer den Projektnamen.
Falls nicht vorhanden: Frage den Projektnamen ab.

Pfade: PRD = `dtb-project/project-strategy/PRD-MVP.md`,
Stack = `dtb-project/project-strategy/TECH-STACK.md`,
Roadmap = `dtb-project/project-strategy/ROADMAP.md`.

---

## Schritt 1: Eligibility-Gate (PRD-MVP.md)

Die Roadmap wird aus dem PRD abgeleitet — ohne PRD ist sie sinnlos. Pruefe, ob
`dtb-project/project-strategy/PRD-MVP.md` existiert. Fehlt es → Hard-Gate, **nicht**
weiterarbeiten, bis der Nutzer die Escape-Hatch bestaetigt:

```
⛔ greenfield-roadmap braucht ein PRD, das fehlt.
   Geprueft: dtb-project/project-strategy/PRD-MVP.md — nicht gefunden.
   → Erstelle es zuerst: /dtb:greenfield-prd

   Fehlalarm (PRD existiert doch) oder bewusst ohne fortfahren? „trotzdem fortfahren" bestaetigen.
```

Bei Bestaetigung: normal fortfahren. Sonst: hier stoppen.

---

## Schritt 2: Modus-Weiche (dreistufig)

Pruefe, ob `ROADMAP.md` existiert, und lies bei Existenz die Zeile nach dem Header auf
`<!-- resume: {Kategorie} -->`.

> **Vorrang-Regel:** Ein Resume-Marker ≠ `done` hat **Vorrang vor der Existenz-Regel** —
> ein angefangenes Interview wird fortgesetzt, nicht in den Report-Modus umgeleitet.

1. **ROADMAP.md MIT Marker ≠ `done`** → Autoren-Modus ab der Kategorie nach `{K}` fortsetzen.
2. **ROADMAP.md vorhanden (kein Marker / `done`)** → **Report-Modus** (Schritt R).
   Neuerzeugung nur auf expliziten Wunsch → Kollisions-Dialog (Schritt 6).
3. **ROADMAP.md fehlt** → **Autoren-Modus neu** (Schritt 3).

---

## Autoren-Modus

### Schritt 3: Readiness-Check des PRD

Bevor die Roadmap entsteht, pruefe mechanisch, ob das PRD tragfaehig ist —
**4 Signale, je 1 Punkt** (Entscheidung C):

1. **Vision nicht-trivial** — `## Produkt-Vision` hat mehr als eine Platzhalter-/Leerzeile
2. **≥ 1 User Story** — `## User Stories` enthaelt mindestens eine „Als … moechte ich …"
3. **≥ 1 Must-Have-Feature** — `## Features` fuehrt mindestens ein Must-Have
4. **Out of Scope befuellt** — `## Out of Scope` ist nicht leer

**Schwelle ≥ 3.** Unter der Schwelle: Warnung, die die **fehlenden Signale konkret**
benennt (nicht generisch) + Konsequenz, und „Trotzdem fortfahren" anbietet:

```
⚠ PRD-Readiness {Score}/4 — folgende Signale fehlen:
  - {konkretes Signal}: {Konsequenz fuer die Roadmap}
Trotzdem eine Roadmap ableiten? (ja / erst PRD nachschaerfen)
```

Ein hohles PRD wird **nicht** automatisch neu geoeffnet (das ist Sache von `greenfield-prd`).

### Schritt 4: Stack-Besprechung → TECH-STACK.md

Der schlanke Ersatz fuer eine Stack-Auswahl: Stack-Entscheidungen bekommen ein Zuhause,
damit das PRD technikfrei bleiben konnte.

- **`TECH-STACK.md` existiert** → sichtbare Skip-Zeile, dann konsumieren:
  ```
  📂 TECH-STACK.md vorhanden → Besprechung uebersprungen (wird als Kontext gelesen)
  ```
- **fehlt** → kompakte gefuehrte Besprechung (4-6 Fragen): Team-Skills / vorhandenes
  Know-how, Sprach- und Framework-Praeferenzen, **Avoid-List** (was bewusst nicht),
  Deployment-Ziel. Ergebnis nach `project-strategy/TECH-STACK.md` als **Living Doc**
  schreiben (Ordner bei Bedarf anlegen).

**Kollision (Entscheidung D):** `TECH-STACK.md` ist ein Living Doc — bei erneuter
Besprechung **edit-in-place** (kein Archiv-Dialog wie beim PRD; nur PRD/ROADMAP werden
„ganz regeneriert"). Bestehende Eintraege inkrementell erweitern, nicht ueberschreiben.

### Schritt 5: Lean-Interview + Slice-Zerlegung

**Lean-Interview — max. 3 Ankerfragen.** Jede mit einer aus PRD/TECH-STACK **zitierten**
„(Recommended)"-Option zuerst, plus 1-2 begruendeten Alternativen. Investment-Schwerpunkte
werden **abgeleitet**, nicht erfragt.

1. **Hauptziel des MVP** — was muss der erste nutzbare Stand koennen? (Recommended: aus `## Produkt-Vision`)
2. **North-Star-Slice** — welcher vertikale Slice liefert zuerst echten Nutzerwert? (Recommended: aus einem Must-Have + zugehoeriger User Story)
3. **Top-Blocker / groesste Unbekannte** — was gefaehrdet den Weg am meisten? (Recommended: aus `## Risiken`/`## Abhaengigkeiten`)

**Slice-Zerlegung:**
- **Vertikale Slices** formulieren als „Nutzer kann …" (jede Schicht durchgaengig), nicht
  als technische Schicht-Phasen. Jeder Slice hat ein sichtbares **Outcome**.
- **Foundations** nur als benannte Enabler mit explizitem **Unlocks** (welche Slices sie
  freischalten) — kein Selbstzweck.
- **Reihenfolge = Dependency-Graph** (Prerequisites), **keine Zeitschaetzungen**
  (keine Kalenderwochen/Story Points/Groessenklassen). **Ausnahme:** extern gesetzte
  Termine als Constraints (Fakten, keine Schaetzung), z.B. „Pilot-Demo 2026-09-01".
- **Change-ID je Slice/Foundation** in **kebab-case nach §4** der `DERIVED_STATE_RULES.md`
  (deterministisch; leiten zwei Namen denselben Slug ab → **Abbruch** + Meldung, kein
  Auto-Suffix). Die Change-ID ist zugleich der kuenftige Feature-Slug — die Bruecke in die
  Change-Pipeline (Hand-off) und in die Statusableitung (§5).

### Schritt 6: ROADMAP-Template

Das erzeugte `ROADMAP.md` ist **deutsch** (Statuswerte englisch) und folgt dieser Struktur:

```markdown
# Roadmap: {config.project_name}
<!-- resume: done -->

**Stand:** {YYYY-MM-DD}

## Vision
[1-2 Saetze Vision-Recap aus dem PRD]

## Ueberblick
> Status = **abgeleitete Anzeige**, nicht manuell pflegen (DERIVED_STATE_RULES §5).
> Legende: proposed = vorgeschlagen · ready = startbereit · blocked = blockiert ·
> in-progress = in Arbeit · done = abgeschlossen.

| ID | Change-ID | Outcome (Nutzer kann …) | Prerequisites | Status |
|----|-----------|-------------------------|---------------|--------|
| S-1 | {change-id} | {sichtbares Outcome} | {IDs oder —} | proposed |
| F-1 | {change-id} | (Foundation) schaltet {S-x} frei | — | proposed |

## Slices
### S-1: {Titel} — `{change-id}`
**Outcome:** Nutzer kann …
**Prerequisites:** {IDs oder „keine"}
**PRD-Bezug:** {Feature/User Story aus dem PRD}

## Foundations
### F-1: {Titel} — `{change-id}`
**Schaltet frei:** {Slice-IDs}
**Prerequisites:** {IDs oder „keine"}

## Externe Termine
[Extern gesetzte Termine als Constraints (Fakten) — oder „keine"]

## Open Roadmap Questions
[Woertlich jede offene Frage, nummeriert — nie erfinden]
```

Status-Vokabular einheitlich **englisch** `proposed / ready / blocked / in-progress / done`
(konsistent zu den `S-NN`/`F-NN`-IDs); die deutsche Erklaerung steht **einmal** in der
Legenden-Zeile. Keine `Zeitraum`-Felder, keine Ressourcen-/Kapazitaetstabelle.

> **Format-Kopplung (Gegen-Hinweis):** Die `PRD-Bezug`-Zeilen und die Slice-Ableitung
> lesen die Sektionsnamen aus `PRD-MVP.md` (`## Produkt-Vision`, `## Features`,
> `## User Stories`, `## Out of Scope`). Aenderst du das PRD-Template in
> `dtb:greenfield-prd`, diese Roadmap-Ableitung mitdenken (L5-Muster) — dort steht der
> Gegen-Hinweis in Gegenrichtung.

### Schritt 7: Selbst-Review VOR dem Schreiben

Hard-Block vor jedem Write: Bei einem Verstoss **nicht** schreiben, den konkreten Befund
melden, auf Korrektur warten (kein stilles Umschreiben). Pruefe:

- **Struktur:** alle Template-Sektionen vorhanden und in Reihenfolge.
- **Jeder Slice hat ein Outcome** („Nutzer kann …") — kein Slice ohne sichtbaren Wert.
- **Jeder Slice/jede Foundation hat einen PRD-Bezug** — nichts frei Erfundenes.
- **Jede Foundation nennt Unlocks** (welche Slices sie freischaltet).
- **Change-IDs eindeutig** und §4-konform; keine Kollision (sonst Abbruch, Meldung).
- **Prerequisites konsistent** — kein Item haengt an einem spaeteren; keine Zeitschaetzung
  (externe Termine nur unter `## Externe Termine`).

```
❌ Selbst-Review: {N} Befund(e), Write abgebrochen
  {Sektion/ID}: {konkreter Befund}
```

### Schritt 8: Speichern + Kollisions-Dialog

- **ROADMAP.md existierte nicht (oder Resume-Fortsetzung):** nach bestandenem Review
  schreiben, Resume-Marker final `<!-- resume: done -->`. Ordner lazy anlegen.
- **Explizite Neuerzeugung bei vorhandener, fertiger ROADMAP.md:** erst Kollisions-Dialog:

  ```
  ROADMAP.md existiert bereits. Wie vorgehen?
    1. Archivieren + ersetzen (Recommended)
    2. Ueberschreiben (alte Version geht verloren)
    3. Abbrechen
  ```

  Bei **1**: bestehende Roadmap nach `project-strategy/archive/YYYY-MM-DD-ROADMAP.md`
  verschieben (`archive/` lazy; Zweitlauf am selben Tag → `-2`/`-3`), dann neu schreiben.
  **Nicht-Git-Projekt:** einfacher Filesystem-Move genuegt (das Archiv ist die Sicherung).
  Bei **2**: ueberschreiben. Bei **3**: nichts schreiben.

### Schritt 9: Hand-off

Genau **eine** Empfehlung, **kein** Auto-Chaining — der erste startbereite Slice
(ohne offene Prerequisites):

```
ROADMAP.md erstellt: dtb-project/project-strategy/ROADMAP.md

Naechster Schritt: /dtb:feature-discover {change-id des ersten Slice}
  ({1-Zeilen-Begruendung: warum dieser Slice zuerst — z.B. „keine Prerequisites, liefert die North-Star"})
```

---

## Report-Modus

Existiert eine vollstaendige `ROADMAP.md`, fasse sie zusammen (keine Neuerhebung):
Vision-Recap, die Slices/Foundations in Dependency-Reihenfolge mit Status, offene
Roadmap-Fragen. Leite den Status je Slice nach `DERIVED_STATE_RULES.md` §5 aus den
Change-Ordnern ab und **melde Konflikte** (Artefakt gewinnt, 1 Hinweiszeile). Schliesse
mit dem naechsten empfohlenen `/dtb:feature-discover <change-id>`.

---

## Richtlinien

- **PRD-getrieben:** Slices leiten sich aus PRD-Sektionen ab, nicht frei erfunden
- **Keine Zeitschaetzungen:** Reihenfolge im Dependency-Graph; externe Termine = Constraints
- **Change-ID = Slug:** §4-konform, Bruecke in Pipeline + Statusableitung (§5)
- **Kein Auto-Chaining:** Hand-off als Empfehlung, nie automatische Skill-Invokation
- **Deutsch:** erzeugte Texte deutsch; Statuswerte englisch (`proposed`/`ready`/…)

## Verwandte Commands

- `/dtb:greenfield-prd` — erzeugt das PRD (Pflicht-Eingabe)
- `/dtb:feature-discover` — vertieft einen einzelnen Roadmap-Slice (Hand-off-Ziel)
