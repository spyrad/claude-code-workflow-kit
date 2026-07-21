# Implementierungsplan: meeting-dump

**Erstellt:** 2026-07-21
**Feature-Spec:** `features/meeting-dump/spec.md`
**Geschaetzte Dauer:** ~1–1.5 Sessions
**Status:** Reviewed (plan-review 2026-07-21: REVISE → Findings eingearbeitet)

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | §6-Kanon-Fundament + Kopplungs-Hinweise | ~0.25 Session | Geplant |
| Phase 2 | Skill-Geruest: Kopf, Eingabe, Beleg-Ablage (+ Sensibilitaets-Hinweis) | ~0.25 Session | Geplant |
| Phase 3 | Kern-Logik: Scan, Abgleich+Freigabe, Rueckschreib-Mechanik + blinde Fixture (Schwerpunkt) | ~0.75 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (`## Betroffene Module`, Pfade per Glob verifiziert). Zusatz-Info, keine Status-Quelle.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-meeting-dump/SKILL.md` | **Neubau-Ziel** — existiert noch nicht |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §6 Fach-Frage-Konvention vorhanden; §6.1 kennt nur `→ Antwort:` unter `[x]`; §6.3 sagt „kein schreibender Konsument"; Fussblock mit Seed-Vermerken |
| `skills/dtb-open-question/SKILL.md` | Vorbild; real `allowed-tools: Read, Glob, Grep, Edit`; Wartungs-Hinweis „drei Schreiber" (Schritt-4/5-Logik: §6-Kanonform, Duplikat-Schutz, robuste Platzierung, Status-Neutralitaet) |
| `skills/dtb-feature-discover/SKILL.md` | §6-Schreiber (discovery.md, `## Offene Punkte`-Template) — kein eigener Kopplungs-Hinweis (bleibt so) |
| `skills/dtb-feature-plan/SKILL.md` | §6-Schreiber (spec.md) + „nie erfinden"-Regel — kein eigener Kopplungs-Hinweis (bleibt so) |
| `skills/CLAUDE.md` | Frontmatter-/Pipeline-Konventionen, Eligibility-Gate-Einteilung + Hard-Gate-Tabelle (kein neuer Eintrag noetig) |
| `skills/dtb-idea/SKILL.md` | Referenz fuer Capture-Muster (`disable-model-invocation: true`) |

---

## Phase 1: §6-Kanon-Fundament + Kopplungs-Hinweise

### Ziel
Die Grammatik-Basis schaffen, auf die der Skill sich beruft: §6.1 um die Teilantwort-Form
erweitern, §6.3 auf den ersten schreibenden Konsumenten umstellen, den Kopplungs-Knoten
`open-question` mitziehen. Zuerst, weil der Skill diese Kanonform zitiert.

### Schritte

#### Schritt 1.1: §6.1 um `→ Zwischenstand:`-Form erweitern
- **Zweck:** Teilantworten (Frage bleibt offen) bekommen eine kanonische Fortsetzungszeile.
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** bestehende §6.1-Grammatik (`→ Antwort:` unter `[x]`)
- **Output:** zweite Form dokumentiert — `→ Antwort:` nur unter `[x]`, `→ Zwischenstand:` nur
  unter `[ ]` (mehrere Zwischenstaende ueber die Zeit erlaubt, je Meeting einer; erst haken bei
  echter Antwort). Beispielblock ergaenzt; Seed-Vermerk im Fussblock („Seed-Aenderung … vgl. #22").

#### Schritt 1.2: §6.3 auf schreibenden Konsumenten umstellen
- **Zweck:** Der Satz „kein schreibender Konsument in diesem Feature" ist nach #24 falsch.
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** §6.3-Abgrenzungstext
- **Output:** zwei Konsumenten benannt — lesend die Agenda-Ansicht (#25, offen), schreibend der
  Rueckfluss `dtb:meeting-dump` (nur Checkbox-Flip + Fortsetzungszeile, status-neutral §6.2).

#### Schritt 1.3: `open-question`-Wartungs-Hinweis auf „vier Akteure" erweitern
- **Zweck:** Kopplungs-Knoten aktuell halten; Rolle von meeting-dump differenzieren.
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** bestehender Hinweis „dritter Schreiber … drei muessen dieselbe §6-Kanonform erzeugen"
- **Output:** „vier Akteure" — drei Erzeuger (feature-discover, feature-plan, open-question) +
  ein **Mutator** (meeting-dump: legt keine neuen `[Fach]`-Fragen an, mutiert bestehende).

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] §6.1 kennt beide Fortsetzungsformen; §6.3 nennt beide Konsumenten; open-question-Hinweis aktuell

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -q "→ Zwischenstand:" DERIVED_STATE_RULES.md` trifft
- [ ] `grep "kein schreibender Konsument" DERIVED_STATE_RULES.md` trifft NICHT mehr
- [ ] `grep -qi "meeting-dump" skills/dtb-open-question/SKILL.md` trifft (Hinweis erweitert)

#### Manual
- [ ] §6 liest sich kohaerent; `→ Zwischenstand:` (unter `[ ]`) ist klar von `→ Antwort:` (unter `[x]`) abgegrenzt, keine Doppeldeutigkeit fuer die vier Akteure

---

## Phase 2: Skill-Geruest — Kopf, Eingabe, Beleg-Ablage

### Ziel
Den neuen Skill anlegen: korrektes Frontmatter, Dump-Eingabe (schneller Chat-Pfad) und die
Beleg-Persistierung nach `project-meetings/` inkl. Datums- und Doppel-Lauf-Behandlung.

### Schritte

#### Schritt 2.1: Frontmatter + Kopf + reziproker Kopplungs-Hinweis
- **Zweck:** Skill korrekt in Pipeline/kit-sync/Gate-Konvention einordnen.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md` (neu)
- **Input:** `skills/CLAUDE.md` (Frontmatter-Regeln), `open-question`-Frontmatter als Muster
- **Output:** `name: dtb:meeting-dump`, deutsche Trigger + engl. Summary,
  `disable-model-invocation: true`, `allowed-tools: Read, Glob, Grep, Edit, Write`,
  pipeline-Block (`stage: capture`, `after: null`, `next: [dtb:workflow-next]`,
  `consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]`,
  `produces: [features/*/spec.md, features/*/discovery.md, project-meetings/*.md]`).
  Reziproker Wartungs-Hinweis (Gegenstueck zu 1.3, Muster implement ↔ commit-and-push).

#### Schritt 2.2: Config laden + Dump-Eingabe
- **Zweck:** Eingabe robust entgegennehmen.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** Command-Argument / Chat-Freitext
- **Output:** Schritt „Config laden" (Fallback-Pfade, config-los lauffaehig); Dump-Eingabe als
  Freitext im Chat; leerer Aufruf → nachfragen (nicht abbrechen); Markdown/Sonderzeichen 1:1
  uebernehmen (nichts escapen).

#### Schritt 2.3: Beleg persistieren nach `project-meetings/`
- **Zweck:** Roh-Dump als Quelle/Beleg dauerhaft ablegen.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** Roh-Dump, Meeting-Datum
- **Output:** Beschreibung: Ordner `dtb-project/project-meetings/` bei Bedarf anlegen; **eine
  Datei pro Kalendertag** `YYYY-MM-DD.md`; Meeting-Datum erfragen (Default heute); nur Header +
  Roh-Dump (NIE Abgleich-Ergebnisse); zweites Meeting am selben Tag → `## Besprechung 2 – HH:MM`
  an dieselbe Tagesdatei anhaengen; Doppel-Lauf mit identischem Dump → warnen, nicht doppelt
  anhaengen.
- **Sensibilitaets-Hinweis (schlank):** Beim Persistieren einen sichtbaren Einzeiler ausgeben —
  der Beleg ist git-getrackt und mit dem naechsten `commit-and-push` im Repo/Remote (z.B.
  „⚠ Meeting-Klartext landet in project-meetings/{datum}.md und ist versionierbar — Sensibles
  vorher entfernen?"). Kein Gate, kein Extra-Schritt an `commit-and-push` (bewusst: Inhalt ist
  i.d.R. technische Fach-Klaerung, Risikoklasse wie discovery.md/spec.md).

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-meeting-dump/SKILL.md` mit gueltigem Frontmatter + Eingabe- + Beleg-Ablauf

### Checkpoint-Kriterien

#### Automated
- [ ] Datei `skills/dtb-meeting-dump/SKILL.md` existiert
- [ ] Frontmatter enthaelt `allowed-tools:` mit `Write` und `stage: capture` (Grep beide)
- [ ] `produces:` enthaelt `project-meetings/*.md` (Grep)
- [ ] Abschnitt zur Beleg-Ablage nennt `project-meetings/` und `## Besprechung 2` (Grep)
- [ ] Sensibilitaets-Hinweis vorhanden (Grep auf Warn-Text „Sensibles" bzw. „Klartext" im Beleg-Abschnitt)

#### Manual
- [ ] Frontmatter-Konventionen aus `skills/CLAUDE.md` erfuellt (name↔Verzeichnis, description-Form); Eingabe-/Beleg-Text eindeutig

---

## Phase 3: Kern-Logik — Scan, Abgleich+Freigabe, Rueckschreiben

### Ziel
Der eigentliche Rueckfluss: offene `[Fach]`-Fragen finden, Abgleich-Vorschlag mit Freigabe,
§6-konformes Rueckschreiben mit Status-Neutralitaet, Rest-Input ausweisen.

### Schritte

#### Schritt 3.1: Scan offener `[Fach]`-Fragen
- **Zweck:** Deterministisch die Abgleich-Basis finden.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** `features/*/{discovery,spec}.md`
- **Output:** Beschreibung: exakte §6-Kanonform `- [ ] [Fach] …` in `## Offene Punkte` matchen
  („liest, wo die §6-Schreiber schreiben"); `archive/` ausschliessen; kein Fuzzy-Matching;
  0 offene Fragen = definierter Pfad (Beleg trotzdem gespeichert, alles → „Nicht zugeordnet").

#### Schritt 3.2: Abgleich-Vorschlag + Freigabe + Konflikte
- **Zweck:** Keine Fehlzuordnung ohne menschliche Freigabe (Variante B als Liste).
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** Dump-Aussagen, gescannte offene Fragen
- **Output:** Tabelle (Frage, Feature/Datei, Antwort-Kandidat) — **keine Konfidenz-Spalte**
  (die Freigabe IST das Urteil; eine Konfidenz-Angabe vom Skill waere Scheingenauigkeit);
  Freigabe (alle / Nummern / abbrechen) VOR dem Schreiben; Konflikte ausweisen statt still
  handeln: Mehrfach-Match, Dump-Widerspruch, bereits `[x]`-beantwortet (nicht ueberschreiben).

#### Schritt 3.3: Rueckschreiben §6-konform (Status-neutral)
- **Zweck:** Antworten kanonisch in `## Offene Punkte` zurueckschreiben.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** freigegebene Zuordnungen
- **Output:** Vollantwort → `[ ]`→`[x]` + `→ Antwort: … (Meeting YYYY-MM-DD)`; Teilantwort →
  `[ ]` bleibt + `→ Zwischenstand: … (Meeting YYYY-MM-DD)`; nur `## Offene Punkte` anfassen
  (NIE `## Progress`/Statusfelder, §6.2); bestehende Eintraege/Reihenfolge unangetastet.
- **Platzierungs-Mechanik (eigene Logik — NICHT open-question Schritt 5):** Das
  open-question-Muster haengt neue Bullets ans **Sektionsende** — hier falsch. Einfuegepunkt =
  unmittelbar **nach der gematchten `- [ ] [Fach] …`-Zeile** UND nach allen bereits eingerueckten
  `→`-Fortsetzungszeilen, die schon zu **dieser** Frage gehoeren (Frage-Block, nicht Einzel-Bullet).
  Einrueckung konsistent zum §6.1-Beispiel. Bei Vollantwort zusaetzlich die Checkbox **derselben**
  Zeile kippen.
- **Mehrere Zwischenstaende akkumulieren:** jeder Lauf haengt eine weitere
  `→ Zwischenstand: … (Meeting <Datum>)` unter die Frage (Verlauf bleibt als Beleg, §6.1);
  spaetere Vollantwort ergaenzt `→ Antwort:` als letzte Zeile, Zwischenstaende bleiben stehen.

#### Schritt 3.4: Rest-Input ausweisen + Abschluss-Summary
- **Zweck:** Nichts geht verloren, ohne Erfassungs-Logik zu duplizieren.
- **Dateien:** `skills/dtb-meeting-dump/SKILL.md`
- **Input:** nicht zugeordnete Dump-Anteile, geschriebene Zuordnungen
- **Output:** „Nicht zugeordnet"-Block mit Werkzeug-Hinweis (`/dtb:idea`,
  `/dtb:open-question <slug>`); kompaktes Summary (Beleg-Pfad, N Antworten, M Zwischenstaende,
  K Konflikte, Rest); Footer.

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Vollstaendiger Kern-Ablauf im Skill (Scan → Vorschlag → Freigabe → Rueckschreiben → Rest)

### Checkpoint-Kriterien

#### Automated
- [ ] SKILL.md nennt die Scan-Kanonform `- [ ] [Fach]` und schliesst `archive/` aus (Grep)
- [ ] SKILL.md enthaelt beide Rueckschreibformen `→ Antwort:` UND `→ Zwischenstand:` (Grep)
- [ ] SKILL.md enthaelt Freigabe-Muster (`alle` / `Nummern` / `abbrechen`) und „Nicht zugeordnet" (Grep)
- [ ] Status-Neutralitaet explizit: Grep auf „nie `## Progress`" bzw. §6.2-Verweis trifft

- [ ] **Blinde Rueckschreib-Fixture (deterministische Mechanik):** Eingabe-Fixture = `## Offene Punkte`
      mit mehreren offenen `[Fach]`-Fragen (eine schon mit `→ Zwischenstand:`) + freigegebene Zuordnung;
      Erwartung = exakte Datei nach dem Schreiben (richtige Zeile gekippt, Fortsetzungszeile unter der
      korrekten Frage, andere Fragen/Reihenfolge unangetastet). Vergleich **EOL-normalisiert**
      (CRLF↔LF, vgl. Idee #28) — sonst scheitert die byte-genaue Erwartung vor der Logik

#### Manual
- [ ] **Abgleich separat (nicht-deterministisch):** beobachteter Probelauf gegen ein reales Feature —
      Struktur der Vorschlags-Tabelle + Freigabe-Gate greift, nicht der konkrete Match-Inhalt;
      dazu der 0-Fragen-Pfad (Beleg gespeichert, alles „Nicht zugeordnet")
- [ ] Trockener Durchgang: Rueckschreiben §6-konform, Status unveraendert (echte Abnahme spaeter via impl-review/implement-Gate)
- [ ] Konflikt- und 0-Fragen-Pfade lesen sich eindeutig, kein stilles Raten

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger | eigener Skill / #13-Anbau | eigener Skill | Dritter Verb-Schritt der Kette, eigener Trigger (Discovery) |
| Eingabeweg | nur Datei / Chat-Freitext | Chat-Freitext | Schneller Pfad (Discovery 3a) |
| Beleg-Ort | project-meetings/ / requirements-input / workflows | `project-meetings/` | Neuer flacher Ordner, Datums-Rueckverfolgung (Discovery 3c) |
| Scan-Reichweite | +plan/bug/task / nur discovery+spec | discovery+spec | #13-MVP-Schnitt; „liest, wo §6-Schreiber schreiben" |
| Teilantwort-Form | keine / `→ Zwischenstand:` unter `[ ]` | `→ Zwischenstand:` (akkumulierend) | §6.1-Erweiterung (Discovery 3c); Verlauf bleibt als Beleg (plan-review 2b) |
| Konfidenz-Spalte | ohne / 2-stufig / 3-stufig | ohne | Freigabe ist das Urteil; Konfidenz vom Skill = Scheingenauigkeit (plan-review P4) |
| Beleg-Tracking | getrackt / .gitignore | getrackt + Sensibilitaets-Hinweis | Inhalt i.d.R. technische Fach-Klaerung, Risikoklasse wie discovery/spec (plan-review P1) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 §6.1 `→ Zwischenstand:`-Form — `317a959`
- [x] 1.2 §6.3 schreibender Konsument — `317a959`
- [x] 1.3 open-question Hinweis „vier Akteure" — `317a959`
- [x] 2.1 Frontmatter + Kopf + reziproker Hinweis — `757cb7f`
- [x] 2.2 Config + Dump-Eingabe — `757cb7f`
- [x] 2.3 Beleg-Ablage project-meetings/ — `757cb7f`
- [x] 3.1 Scan offener [Fach]-Fragen
- [x] 3.2 Abgleich-Vorschlag + Freigabe + Konflikte
- [x] 3.3 Rueckschreiben §6-konform (status-neutral)
- [x] 3.4 Rest-Input + Summary

---

## Umsetzung

Umsetzung mit `/dtb:implement meeting-dump` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/meeting-dump/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
