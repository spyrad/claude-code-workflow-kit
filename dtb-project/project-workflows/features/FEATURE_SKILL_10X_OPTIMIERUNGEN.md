# Feature: SKILL_10X_OPTIMIERUNGEN

**Erstellt:** 2026-07-09
**Ziel:** Fuenf Bestands-Skills nach 10x-Vorbild additiv haerten, ohne ihre Struktur umzubauen.
**Prioritaet:** Mittel
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Fuenf bestehende Skills bekommen je eine gezielte Qualitaets-Verbesserung, die sich am
10x-3.0-Vorbild orientiert: bessere Report-Struktur (project-health, debug-plan,
greenfield-roadmap) und bessere Session-Uebergaenge (feature-discover, checkpoint/resume).
Alle Aenderungen sind additiv im bestehenden Skill-Format — keine strukturellen Umbauten,
kein neuer Runtime-Code. Ziel ist hoehere Ergebnis-Qualitaet und Wiederaufnahme-Sicherheit
der bestehenden Workflows.

---

## Scope / Abgrenzung

### Enthalten

Fuenf unabhaengige Bloecke ueber sechs Skill-Dateien (Nutzer-Entscheidung 2026-07-09: alle als **ein** Feature):

- **Block 1 — project-health:** Befund-Kategorisierung A/B (jetzt/spaeter), WARN-AND-CONTINUE
  (ein fehlgeschlagener Einzel-Check bricht den Gesamt-Report nicht ab), Fixes mit konkretem
  Kommando + Aufwandsangabe
- **Block 2 — debug-plan:** Hypothesen-Tabelle mit Evidenzstaerke STRONG/WEAK/NONE;
  „Framing war korrekt" als explizit valides Endergebnis (keine Hypothese bestaetigt →
  Problem-Framing war falsch oder schon geloest)
- **Block 3 — greenfield-roadmap:** vertikale Slices, Foundations mit Unlocks-Feld,
  Selbst-Review-Checkliste — als Verbesserung der bestehenden **read-only**-Uebersicht
- **Block 4 — feature-discover:** Checkpoint-Frontmatter (Discovery resumebar),
  „(Recommended)"-Option-Muster (erste Option markiert)
- **Block 5 — workflow-checkpoint/-resume:** Handoff-Block mit naechstem Befehl + /clear-Hinweis,
  beidseitig konsistent (Sende-Seite checkpoint, Empfangs-Seite resume)

### Nicht enthalten

- Keine anderen Skills anfassen (allgemeiner Konsistenz-Rundumschlag = Idee #9)
- Keine strukturellen Umbauten; keine Umnummerierung bestehender Kern-Schritte wo vermeidbar
- Keine Write-/Autoren-Faehigkeit fuer greenfield-roadmap (Redesign des Greenfield-Strangs = Idee #11)
- Kein erzwungenes globales kit-sync als Umsetzungsschritt (separater Abschlussschritt)
- Keine neuen Runtime-Abhaengigkeiten (reine Prompt-/Markdown-Aenderungen)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| project-health (344 Z.) sprengt mit additivem Block das 500-Zeilen-Budget | Mittel | Mittel | Block knapp halten; ggf. Tabellen statt Prosa; Zeilenzahl vor Save pruefen |
| Handoff-Format checkpoint ↔ resume driftet auseinander (nur eine Seite geaendert) | Mittel | Hoch | Beide Skills im selben Block/Meilenstein aendern; Format gegenseitig referenzieren |
| Breiter Blast-Radius (6 Dateien) erschwert Abnahme | Mittel | Mittel | Pro Block eigener Zwischen-Meilenstein in `## Progress`, einzeln abnehmbar |
| roadmap-Block kollidiert mit spaeterem #11-Redesign | Niedrig | Mittel | Bewusst read-only halten; nur Ausgabe-Struktur verbessern, keine Rolle aendern |
| „(Recommended)"/Frontmatter-Aenderung bricht pipeline-graph/workflow-status-Parsing | Niedrig | Mittel | Frontmatter-Schema unveraendert lassen; nur bekannte Felder nutzen |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine harten Vorbedingungen — alle fuenf Bloecke sind unabhaengig umsetzbar

### Referenz-Dokumente
- `dtb-project/project-workflows/features/DISCOVERY_SKILL_10X_OPTIMIERUNGEN.md` - Discovery-Grundlage
- `dtb-project/project-rules/lessons.md` - Lektion L1 (vor Skill-Haertung reale `allowed-tools`/`produces` pruefen) als Prior
- `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-plan-review/SKILL.md`, `skills/dtb-code-review/SKILL.md` - Methodik-Vorbild (additive Haertung, Fixture-Abnahme durch unabhaengigen Agenten) aus SPEC/REVIEW_HAERTUNG

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Block 1: project-health kategorisiert Befunde A/B, setzt WARN-AND-CONTINUE um und nennt pro Fix Kommando + Aufwand
- [ ] Block 2: debug-plan fuehrt Hypothesen mit Evidenzstaerke STRONG/WEAK/NONE und akzeptiert „Framing war korrekt" als Endergebnis
- [ ] Block 3: greenfield-roadmap gibt vertikale Slices + Foundations mit Unlocks-Feld aus und enthaelt eine Selbst-Review-Checkliste (bleibt read-only)
- [ ] Block 4: feature-discover ist per Checkpoint-Frontmatter resumebar und nutzt das „(Recommended)"-Muster
- [ ] Block 5: checkpoint erzeugt einen Handoff (naechster Befehl + /clear-Hinweis), resume nimmt ihn konsistent auf; Fallback ohne erfundene Empfehlung
- [ ] Jeder Skill bleibt <= 500 Zeilen und behaelt gueltiges Pipeline-Frontmatter
- [ ] Abnahme jedes Blocks (Fixture oder Praxiserprobung) bestanden, danach kit-sync

---

## Offene Punkte

- Umsetzungs-Reihenfolge der fuenf Bloecke (Vorschlag: nach Nutzen/Blast-Radius in impl-plan festlegen)
- Abnahme-Strategie pro Block: Fixture-basiert (wie SPEC/REVIEW_HAERTUNG) vs. reine Praxiserprobung — je Block entscheiden
- Prioritaet „Mittel" ist eine Setzung ohne explizite Nutzer-Angabe — bei Backlog-Eintrag bestaetigen

---

**Erstellt mit:** `/dtb:feature-plan`
