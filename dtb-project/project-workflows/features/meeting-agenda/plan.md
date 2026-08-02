# Implementierungsplan: Meeting-Agenda (dtb:meeting-agenda)

**Erstellt:** 2026-08-02
**Feature-Spec:** `features/meeting-agenda/spec.md`
**Geschaetzte Dauer:** 1.5-2h (1 Phase)
**Status:** Reviewed (plan-review 2026-08-02: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill bauen, Kette verdrahten, dokumentieren, verteilen, Probelauf | 1.5-2h | Geplant |

---

## Ist-Analyse

> Quelle: Fast-Track-Erhebung 2026-08-02 (gegrepte Befunde), ergaenzt um die Grounding- und
> Challenger-Befunde des plan-review 2026-08-02.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-meeting-agenda/SKILL.md | Existiert nicht — Neubau-Ziel, keine Kollision |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §6 mit §6.1 (Zwischenstaende, akkumulierend) und §6.3 (Antwort-Formen) vorhanden — der Format-Kanon; §6 bindet die Grammatik an `## Offene Punkte` |
| skills/dtb-workflow-next/SKILL.md, skills/dtb-backlog-status/SKILL.md | Read-only-Muster: `disable-model-invocation: false`, `produces: []` (Z. 8/17 bzw. 7/15) |
| **alle 11 `stage: monitoring`-Skills** | Tragen ausnahmslos `after: null` / `next: null` — durchgehende Konvention, deckungsgleich mit `pipeline-graph:188` („Monitoring-Skills haben keine Kanten") |
| skills/dtb-open-question/SKILL.md | `stage: capture`, `next: [dtb:workflow-next]` — zeigt bereits auf einen Monitoring-Skill; **eingehende** Kanten auf Monitoring sind etabliert |
| skills/dtb-meeting-dump/SKILL.md | `stage: capture`, `after: null`, `next: [dtb:workflow-next]` |
| skills/dtb-pipeline-graph/SKILL.md | Z. 97-99: Kanten werden aus `next` **und** `after` erzeugt und dedupliziert — eine Gegenkante im Nachbarn genuegt fuer die Sichtbarkeit |
| CLAUDE.md | Kategorie "Knowledge management" (Z. 58) listet docs-extract, lesson, open-question und verweist bereits auf „the Fach-Agenda #25" — Andock-Stelle |
| features/fachfragen-erfassung/spec.md:90 | **Einzige echte offene `[Fach]`-Frage im Bestand** (in `## Offene Punkte`) — der Testfall fuer den Probelauf |
| features/fachfragen-erfassung/discovery.md:26,37,45 | Enthalten `- [ ] [Fach] {Frage}` als **Doku-Zeilen** in der Prosa, ausserhalb von `## Offene Punkte` — die belegten False-Positive-Kandidaten des Scans |

---

## Phase 1: Skill bauen, Kette verdrahten, dokumentieren, verteilen, Probelauf

### Ziel
`dtb:meeting-agenda` existiert, ist in der Pipeline sichtbar, dokumentiert, auf der Maschine
installiert und hat eine echte Agenda erzeugt.

> **Vor Schritt 1.1 (Pflicht):** `/dtb:project-health` als Baseline laufen lassen und die
> bekannten Warnungen notieren — das Abschluss-Kriterium vergleicht gegen diese Baseline,
> nicht gegen null.

### Schritte

#### Schritt 1.1: SKILL.md schreiben
- **Zweck:** Der Agenda-Skill selbst
- **Dateien:** skills/dtb-meeting-agenda/SKILL.md (neu)
- **Input:** §6-Kanon, Read-only-Muster (Ist-Analyse)
- **Output:**
  - Frontmatter: `disable-model-invocation: false`, `argument-hint: "[alle]"`, stage `monitoring`,
    **`after: null`, `next: null`** (Konvention aller 11 monitoring-Skills — die Ketten-Sichtbarkeit
    liefern die Gegenkanten aus Schritt 1.2), `consumes: [features/*/discovery.md,
    features/*/spec.md, features/*/plan.md]`, `produces: []`
  - **Scan-Logik (verbindlich praezisiert):** nur Zeilen der Form `- [ ] [Fach] <Frage>`
    **innerhalb einer `## Offene Punkte`-Sektion** in `features/*/{discovery,spec,plan}.md`;
    `archive/` ausgeschlossen. Die Sektions-Ankerung ist Pflicht, nicht Kuer — ohne sie
    landen die Doku-Zeilen aus `fachfragen-erfassung/discovery.md` auf der Agenda
  - Agenda-Report gruppiert nach Feature; Zwischenstaende (§6.1) markiert `[in Klaerung]`,
    im Standard **nur der letzte** `→ Zwischenstand:`, im `alle`-Modus der volle Verlauf
  - Leer-Fall-Meldung mit `/dtb:open-question`-Verweis
  - Argument `alle`: zusaetzlicher Abschnitt „Zuletzt geklaert" (beantwortete `[x]`-Fragen
    mit `→ Antwort:`) plus voller Zwischenstands-Verlauf

#### Schritt 1.2: Gegenkanten in den Nachbar-Skills
- **Zweck:** Kette #26 → #25 → #24 im Pipeline-Graph sichtbar machen, ohne die
  Monitoring-Konvention zu brechen
- **Dateien:** skills/dtb-open-question/SKILL.md, skills/dtb-meeting-dump/SKILL.md
- **Input:** Ist-Stand der beiden Frontmatter (Ist-Analyse)
- **Output:**
  - `open-question`: `next: [dtb:workflow-next, dtb:meeting-agenda]` (Eintrag ergaenzt,
    bestehender bleibt)
  - `meeting-dump`: `after: [dtb:meeting-agenda]` (war `null`)
  - Damit erzeugt `pipeline-graph` die Kette beidseitig; `meeting-agenda` selbst bleibt
    `null`/`null` wie `workflow-next`, das heute schon zwei Eingangskanten hat

#### Schritt 1.3: CLAUDE.md ergaenzen
- **Zweck:** Kit-Doku aktuell halten
- **Dateien:** CLAUDE.md (Repo-Root)
- **Input:** Kategorie "Knowledge management" (Z. 58)
- **Output:** meeting-agenda in der Kategorien-Zeile (Lese-Ansicht der Fachfragen-Kette
  #13→#26→#25→#24); der dortige Vorverweis „later read by the Fach-Agenda #25" wird auf den
  jetzt existierenden Skill umgestellt

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Distribution (kit-sync)
- **Zweck:** Skill **und die geaenderten Nachbarn** auf die Maschine(n) bringen
- **Dateien:** ~/.claude/skills/dtb-meeting-agenda/SKILL.md, ~/.claude/skills/dtb-open-question/SKILL.md,
  ~/.claude/skills/dtb-meeting-dump/SKILL.md, ~/.claude/dtb-lock.json
- **Input:** dtb:kit-sync (Klasse-A-Muster erfasst den neuen Skill automatisch)
- **Output:** `/dtb:kit-sync sync` gelaufen; **3 Artefakte** betroffen (1 neu, 2 aktualisiert),
  Lock-Eintraege vorhanden, kein Drift. Ohne diesen Schritt liefe der Probelauf gegen die
  alte installierte Kopie der Nachbar-Skills

#### Schritt 1.5: Probelauf mit echten Fragen
- **Zweck:** Agenda am lebenden Bestand beweisen
- **Dateien:** keine (read-only Lauf)
- **Input:** die echte offene Frage in `features/fachfragen-erfassung/spec.md:90`
  (`- [ ] [Fach] Prioritaet bestaetigen …`) — sie existiert bereits, es muss keine
  kuenstliche Frage erfasst werden
- **Output:** Beide Modi einmal gezeigt (`/dtb:meeting-agenda` und `/dtb:meeting-agenda alle`),
  Ausgaben im Session-Log festgehalten; Negativ-Befund ausdruecklich geprueft (siehe
  Manual-Kriterien)

### Deliverables
- [ ] dtb:meeting-agenda gebaut, Kette verdrahtet, dokumentiert, installiert, einmal real gelaufen

### Checkpoint-Kriterien

#### Automated
- [ ] Datei existiert: `skills/dtb-meeting-agenda/SKILL.md`
- [ ] Grep Frontmatter meeting-agenda: `disable-model-invocation: false`, `produces: []`,
      `after: null`, `next: null`, `argument-hint: "[alle]"`
- [ ] Grep Gegenkanten: `skills/dtb-open-question/SKILL.md` enthaelt `dtb:meeting-agenda` in der
      `next:`-Zeile **und** `skills/dtb-meeting-dump/SKILL.md` enthaelt `dtb:meeting-agenda` in der
      `after:`-Zeile (auf die Frontmatter-Zeile ankern, nicht auf das blosse Stichwort — L2)
- [ ] Grep CLAUDE.md: `meeting-agenda` in der Knowledge-management-Zeile
- [ ] `/dtb:kit-sync check`: dtb-meeting-agenda im Lock (Status synced), dtb-open-question und
      dtb-meeting-dump ohne Drift
- [ ] `/dtb:project-health`: keine neuen Befunde gegenueber der Baseline vor Schritt 1.1

#### Manual
- [ ] Agenda-Ausgabe im Probelauf: korrekt nach Feature gruppiert, lesbar, nichts Falsches
      eingesammelt
- [ ] **Negativ-Test:** Die `[Fach]`-Doku-Zeilen aus `features/fachfragen-erfassung/discovery.md`
      (Z. 26, 37, 45) erscheinen **nicht** auf der Agenda — sie stehen ausserhalb von
      `## Offene Punkte`
- [ ] Leer-Fall-Pfad im SKILL.md definiert (Meldung + `/dtb:open-question`-Verweis); real nicht
      ausloesbar, da der Bestand eine offene Frage fuehrt → Abnahme per Inspektion

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Beantwortete `[x]`-Fragen | immer zeigen / nie / per Argument | per Argument (Standard: ausgeblendet) | Agenda kurz halten; Antworten stehen im Artefakt (per Veto-Vorlage bestaetigt 2026-08-02) |
| Zwischenstaende §6.1 | ausblenden / markiert zeigen | markiert "in Klaerung" | offen = meeting-relevant (per Veto-Vorlage bestaetigt 2026-08-02) |
| Scan-Reichweite | inkl. archive/ / nur features/ | nur features/ | abgeschlossene Changes gehoeren nicht auf die Agenda (per Veto-Vorlage bestaetigt 2026-08-02) |
| Pipeline-Einordnung | Kanten am Skill / Gegenkanten in den Nachbarn / standalone | **monitoring + `null`/`null`, Kette ueber Gegenkanten in open-question und meeting-dump** | Alle 11 monitoring-Skills tragen `null`/`null`; `pipeline-graph` erzeugt Kanten aus beiden Richtungen (Z. 97-99), eingehende Kanten auf Monitoring sind etabliert (`open-question → workflow-next`). So bleiben Konvention und Ketten-Sichtbarkeit beide erhalten (plan-review 2026-08-02, Variante C) |
| Argument-Name „Zuletzt geklaert" | `alle` / `geklaert` / Modus streichen | **`alle`** | Praezedenz `dtb:generate-rules` ('alle' als Sammelmodus), umlautfrei, konsistente Semantik mit dem Zwischenstands-Verlauf (plan-review 2026-08-02) |
| Scan-Ankerung | Zeilenform genuegt / Sektions-Ankerung | **nur innerhalb `## Offene Punkte`** | §6 bindet die Grammatik an die Sektion; der Bestand enthaelt 3 Doku-Zeilen mit `[Fach]` ausserhalb davon — ohne Ankerung waeren sie False Positives (plan-review 2026-08-02) |
| Mehrere Zwischenstaende | alle / nur letzter / keiner | **Standard nur der letzte, `alle`-Modus voller Verlauf** | Agenda darf nicht mit jedem Meeting wachsen; der Verlauf bleibt im Artefakt und auf Wunsch abrufbar (plan-review 2026-08-02) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 SKILL.md schreiben
- [x] 1.2 Gegenkanten in den Nachbar-Skills
- [x] 1.3 CLAUDE.md ergaenzen
- [ ] 1.4 Distribution (kit-sync)
- [ ] 1.5 Probelauf mit echten Fragen

---

## Umsetzung

Umsetzung mit `/dtb:implement meeting-agenda` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/meeting-agenda/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-02)
**Reviewed mit:** `/dtb:plan-review` (2026-08-02, REVISE → 4 WARNs behoben)
