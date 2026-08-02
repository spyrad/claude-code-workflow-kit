# Implementierungsplan: Meeting-Agenda (dtb:meeting-agenda)

**Erstellt:** 2026-08-02
**Feature-Spec:** `features/meeting-agenda/spec.md`
**Geschaetzte Dauer:** 1-1.5h (1 Phase)
**Status:** Entwurf <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill bauen, dokumentieren, verteilen, Probelauf | 1-1.5h | Geplant |

---

## Ist-Analyse

> Quelle: Fast-Track-Erhebung 2026-08-02 (gegrepte Befunde).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-meeting-agenda/SKILL.md | Existiert nicht — Neubau-Ziel, keine Kollision |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §6 mit §6.1 (Zwischenstaende) und §6.3 (Antwort-Formen) vorhanden — der Format-Kanon |
| skills/dtb-workflow-next/SKILL.md, skills/dtb-backlog-status/SKILL.md | Read-only-Muster: `disable-model-invocation: false`, `produces: []` (Z. 8/16 bzw. 7/14) |
| CLAUDE.md | Kategorie "Knowledge management" listet docs-extract, lesson, open-question — Andock-Stelle |

---

## Phase 1: Skill bauen, dokumentieren, verteilen, Probelauf

### Ziel
`dtb:meeting-agenda` existiert, ist dokumentiert, auf der Maschine installiert und hat
eine echte Agenda erzeugt.

### Schritte

#### Schritt 1.1: SKILL.md schreiben
- **Zweck:** Der Agenda-Skill selbst
- **Dateien:** skills/dtb-meeting-agenda/SKILL.md (neu)
- **Input:** §6-Kanon, Read-only-Muster (Ist-Analyse)
- **Output:** Frontmatter (`disable-model-invocation: false`, stage `monitoring`,
  `after: [dtb:open-question]`, `next: [dtb:meeting-dump]`, `consumes:
  [features/*/discovery.md, features/*/spec.md, features/*/plan.md]`, `produces: []`);
  Scan-Logik (nur `- [ ] [Fach]`-Zeilen nach §6, `archive/` ausgeschlossen);
  Agenda-Report gruppiert nach Feature, Zwischenstaende (§6.1) markiert "in Klaerung";
  Leer-Fall-Meldung mit /dtb:open-question-Verweis; Argument-Modus "Zuletzt geklaert"
  (Argument-Name hier festlegen, z.B. `voll`)

#### Schritt 1.2: CLAUDE.md ergaenzen
- **Zweck:** Kit-Doku aktuell halten
- **Dateien:** CLAUDE.md (Repo-Root)
- **Input:** Kategorie "Knowledge management"
- **Output:** meeting-agenda in der Kategorien-Zeile (Lese-Ansicht der Fachfragen-Kette
  #13→#26→#25→#24)

#### Schritt 1.3: Distribution (kit-sync)
- **Zweck:** Skill auf die Maschine(n) bringen
- **Dateien:** ~/.claude/skills/dtb-meeting-agenda/SKILL.md, ~/.claude/dtb-lock.json
- **Input:** dtb:kit-sync (Klasse-A-Muster erfasst den Skill automatisch)
- **Output:** `/dtb:kit-sync sync` gelaufen, Lock-Eintrag vorhanden, kein Drift

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Probelauf mit echten Fragen
- **Zweck:** Agenda am lebenden Bestand beweisen
- **Dateien:** keine (read-only Lauf)
- **Input:** offene `[Fach]`-Fragen im Bestand; existiert keine, zuerst eine echte Frage
  per /dtb:open-question erfassen
- **Output:** Agenda-Report korrekt gruppiert; Leer-Fall einmal gezeigt (vor der
  Erfassung) — beide Ausgaben im Session-Log festgehalten

### Deliverables
- [ ] dtb:meeting-agenda gebaut, dokumentiert, installiert, einmal real gelaufen

### Checkpoint-Kriterien

#### Automated
- [ ] Datei existiert: `skills/dtb-meeting-agenda/SKILL.md`
- [ ] Grep Frontmatter: `disable-model-invocation: false`, `produces: []`, `after: [dtb:open-question]`, `next: [dtb:meeting-dump]`
- [ ] Grep CLAUDE.md: `meeting-agenda` in der Knowledge-management-Zeile
- [ ] `/dtb:kit-sync check`: dtb-meeting-agenda im Lock, Status synced

#### Manual
- [ ] Agenda-Ausgabe im Probelauf: korrekt gruppiert, lesbar, nichts Falsches eingesammelt

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Beantwortete `[x]`-Fragen | immer zeigen / nie / per Argument | per Argument (Standard: ausgeblendet) | Agenda kurz halten; Antworten stehen im Artefakt (Fast-Track A3, bestaetigt) |
| Zwischenstaende §6.1 | ausblenden / markiert zeigen | markiert "in Klaerung" | offen = meeting-relevant (A4, bestaetigt) |
| Scan-Reichweite | inkl. archive/ / nur features/ | nur features/ | abgeschlossene Changes gehoeren nicht auf die Agenda (A5, bestaetigt) |
| Pipeline-Einordnung | stage session / monitoring | monitoring, after open-question, next meeting-dump | Kette im Graph sichtbar (A7, bestaetigt) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [ ] 1.1 SKILL.md schreiben
- [ ] 1.2 CLAUDE.md ergaenzen
- [ ] 1.3 Distribution (kit-sync)
- [ ] 1.4 Probelauf mit echten Fragen

---

## Umsetzung

Umsetzung mit `/dtb:implement meeting-agenda` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/meeting-agenda/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-02)
