# Feature: Meeting-Agenda (dtb:meeting-agenda)

**Erstellt:** 2026-08-02
**Ziel:** Vor dem Fach-Meeting eine fertige Agenda aller offenen [Fach]-Fragen ohne Handarbeit — die fehlende Lese-Ansicht der Fachfragen-Kette.
**Prioritaet:** Mittel
**Status:** Geplant <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Fach-Fragen werden heute §6-konform in den Feature-Artefakten erfasst (dtb:open-question)
und nach dem Meeting beantwortet zurueckgespielt (dtb:meeting-dump) — aber es gibt keine
Sicht, die VOR dem Meeting alle offenen Fragen einsammelt. dtb:meeting-agenda schliesst
diese Luecke: ein rein lesender Skill, der `features/*/{discovery,spec,plan}.md` scannt
und die offenen `[Fach]`-Fragen als nach Feature gruppierte Agenda im Chat ausgibt.

---

## Scope / Abgrenzung

### Enthalten
- Scan von `features/*/{discovery,spec,plan}.md` nach offenen `[Fach]`-Fragen (§6-Format)
- Agenda-Report im Chat: gruppiert nach Feature, Zwischenstaende (§6.1) markiert als
  "in Klaerung"
- Leer-Fall-Meldung mit Verweis auf /dtb:open-question
- Optionales Argument fuer einen Abschnitt "Zuletzt geklaert" (beantwortete `[x]`-Fragen)

### Nicht enthalten
- Kein Schreiben in Artefakte (read-only, `produces: []`, kein zweiter Speicherort)
- Kein Scan von `archive/`
- Kein Antwort-Rueckfluss (dtb:meeting-dump) und keine Frage-Erfassung (dtb:open-question)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Format-Drift: Agenda uebersieht Fragen, die nicht exakt §6-konform erfasst sind | Niedrig | Mittel | §6 als einziger Kanon referenziert (keine eigene Format-Logik); nicht-konforme Zeilen bewusst ignoriert — Erfassung laeuft ueber dtb:open-question |
| Agenda veraltet zwischen Aufruf und Meeting | Niedrig | Niedrig | Chat-only-Report ohne Persistenz — jeder Aufruf liest frisch (kein zweiter Speicherort) |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — §6-Kanon (#13), dtb:open-question (#26) und dtb:meeting-dump (#24) sind gebaut

### Referenz-Dokumente
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` §6 - Format-Kanon der Fach-Fragen
- `features/meeting-agenda/discovery.md` - Fast-Track-Discovery (2026-08-02)
- `skills/dtb-workflow-next/SKILL.md`, `skills/dtb-backlog-status/SKILL.md` - Read-only-Muster

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Aufruf liefert alle offenen `[Fach]`-Fragen aus `features/*/{discovery,spec,plan}.md`,
      nach Feature gruppiert — ohne ein Artefakt zu veraendern
- [ ] Zwischenstaende (§6.1) erscheinen markiert; beantwortete `[x]`-Fragen erscheinen
      standardmaessig nicht
- [ ] Leer-Fall erzeugt die explizite Meldung mit /dtb:open-question-Verweis
- [ ] Frontmatter macht die Kette sichtbar (after open-question, next meeting-dump);
      project-health meldet keine neuen Befunde

---

## Offene Punkte

- Name des Arguments fuer den "Zuletzt geklaert"-Modus — im Implementierungsplan festlegen

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-02)
