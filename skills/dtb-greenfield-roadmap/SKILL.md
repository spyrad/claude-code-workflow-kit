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

> **3x3-Block-Grenze:** Nach Schritt 5 endet der aktuelle Umsetzungsblock (2.3).

### Schritt 6: ROADMAP-Template + Selbst-Review + Kollision + Hand-off

> **In Arbeit (Implementierungsplan-Schritt 2.4):** ROADMAP.md-Template (At-a-glance-Tabelle,
> Slices/Foundations, Status-Vokabular `proposed/ready/blocked/in-progress/done`,
> abgeleitete Statusspalte), Selbst-Review VOR Write, Kollisions-Dialog und der Hand-off
> `/dtb:feature-discover <change-id>` werden in diesem Schritt ergaenzt. Bis dahin ist der
> Autoren-Modus **noch nicht** vollstaendig lauffaehig.

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
