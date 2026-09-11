# Discovery: Meeting-Agenda (dtb:meeting-agenda)
<!-- resume: done -->

**Erstellt:** 2026-08-02
**Idee-Referenz:** Inbox #25 — "Rein-lesender Fach-Agenda-Skill: sammelt offene [Fach]-Fragen aus features/*/{discovery,spec,plan}.md, gruppiert nach Feature → fertige Meeting-Agenda (abgeleitet, produces: [], kein zweiter Speicherort)."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-meeting-agenda/SKILL.md | NEU — der rein lesende Agenda-Skill |
| CLAUDE.md | Skill-Kategorien-Liste ("Knowledge management") um den neuen Skill ergaenzen |

---

## Anforderungen

### Scope
**Enthalten:**
- Rein lesende Agenda-Sicht: sammelt alle OFFENEN `[Fach]`-Fragen (`- [ ] [Fach] {Frage}`
  nach §6) aus `features/*/{discovery,spec,plan}.md`, gruppiert nach Feature
- Zwischenstaende (§6.1, `[ ]` + `→ Zwischenstand:`) erscheinen mit Markierung "in Klaerung"
- Leer-Fall: explizite Meldung "keine offenen [Fach]-Fragen" + Verweis auf /dtb:open-question

**Nicht enthalten:**
- Kein Schreiben (read-only, `produces: []`), kein zweiter Speicherort fuer Fragen
- Beantwortete `[x]`-Fragen standardmaessig ausgeblendet ("Zuletzt geklaert" nur auf
  explizites Argument)
- `archive/` wird nicht gescannt (abgeschlossene Changes gehoeren nicht auf die Agenda)
- Kein Antwort-Rueckfluss (das ist dtb:meeting-dump, #24) und keine Einzel-Erfassung
  (das ist dtb:open-question, #26)

### Gewuenschtes Verhalten
- Ein Aufruf vor dem Fach-Meeting → fertige, nach Feature gruppierte Agenda im Chat
- Muster der bestehenden read-only Skills (workflow-next, backlog-status):
  `disable-model-invocation: false`, kompakter Report

### Randfaelle
- Keine offenen Fragen → Leer-Meldung (kein stiller Leer-Report)
- Nicht-§6-konforme Zeilen werden ignoriert (nur getaggte Checkbox-Fragen zaehlen)

### Einschraenkungen
- §6 (`DERIVED_STATE_RULES.md`) ist der Format-Kanon — der Skill implementiert keine
  eigene Format-Logik, sondern referenziert §6

### Integrationspunkte
- Fachfragen-Kette: dtb:open-question (Erfassung, #26) → **dtb:meeting-agenda (Sicht, #25)**
  → dtb:meeting-dump (Antwort-Rueckfluss, #24)
- Frontmatter: stage `monitoring`, after `[dtb:open-question]`, next `[dtb:meeting-dump]`

---

## Abhaengigkeiten

- Keine Konflikte: §6-Konvention (#13) und beide Nachbar-Skills (#26, #24) sind gebaut;
  die Luecke in der Kettenmitte wird geschlossen

---

## Offene Punkte

- Name des Arguments fuer den "Zuletzt geklaert"-Modus (Detail, im Plan-Schritt 1.1 festlegen)

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-02)
