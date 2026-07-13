# Feature: Frontmatter- und Pfad-Hygiene

**Erstellt:** 2026-07-09
**Ziel:** Konsistenz-Lecks im Kit schliessen — Agenten-Pfad, Frontmatter-Kanten und die debug-plan-Ausgabe an die real gelesenen Konventionen angleichen.
**Prioritaet:** Hoch
**Status:** Abgeschlossen (archiviert 2026-07-13) <!-- expliziter Zustand (ueberschreibt Ableitung), gesetzt 2026-07-10 nach Realtest Block A/B (pipeline-graph + plan-review, Agenten global geladen, 1:n-Kanten gerendert) + Block C (realer debug-plan-Lauf, ## Fix-Schritte korrekt ableitbar) -->

---

## Executive Summary

Gebuendelte Hygiene-Runde aus Inbox #8 + #9. Drei verifizierte Inkonsistenzen werden behoben:
`plan-review` liest Agenten aus dem Projekt-Root, obwohl sie global installiert sind; die
Pipeline-Frontmatter (`after`/`next`) kann die real verzweigte Pipeline nicht abbilden und enthaelt
tote Eintraege; und `debug-plan` schreibt eine Struktur, aus der der Bug-Status **nie korrekt
abgeleitet** wird. Letzteres ist kein Kosmetik-Punkt, sondern ein aktives Loch in der
Derived-State-Kette — daher Prioritaet Hoch.

---

## Scope / Abgrenzung

### Enthalten

**Block A — agents/-Pfad (#8)**
- `plan-review` liest Agenten aus `~/.claude/agents/` mit Projekt-Root-`agents/` als Fallback
- Klare Meldung, wenn beide Quellen leer sind (statt stiller Fehlschlag)

**Block B — Frontmatter-Hygiene (#9)**
- `pipeline-graph`-Glob von `.claude/agents/*.md` auf `agents/` (bzw. denselben Pfad wie Block A)
- Nicht-Standard-Feld `context: fork` in `build-check` bereinigen
- Stage-Enum-Eintrag `bug` **entfernen** (kein Skill nutzt ihn; Gruppe bliebe leer)
- `after`/`next` zu **Listen** erweitern, sodass die reale 1:n-Verzweigung abbildbar wird
  (`project-init → {generate-rules, project-team, workflow-resume}`;
  `{plan-review, debug-plan} → feature-start`); Reader `pipeline-graph` und `workflow-status`
  auf das Listen-Format anpassen

**Block C — debug-plan-Mismatch (#9)**
- `debug-plan` schreibt kuenftig `## Fix-Schritte` (H2) statt `#### Schritte`/`#### Testplan` (H4),
  damit der Bug-Status regelkonform aus `## Fix-Schritte` abgeleitet wird (DERIVED_STATE_RULES §1.5)

### Nicht enthalten
- Kein Umbau der Pipeline-Semantik, keine neuen Skills
- Kein Eingriff in #10 (kit-sync pinned/hold) — die globale pitch-coach-Divergenz wird nur benannt
- Keine Auto-Migration bestehender `bug.md` im alten `#### Schritte`-Format (nur benennen)
- Keine Umstellung der `## Fix-Schritte`-Reader (`workflow-next`, `archive`, `workflow-status`,
  §1.5) — sie sind das Ziel-Format, die Ausgabe zieht zu ihnen hin

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Listen-Format bricht das Parsing der Frontmatter-Reader (`pipeline-graph`, `workflow-status`, `project-health`) | Mittel | Hoch | Reader in derselben Phase wie das Format anpassen; Rendering-Check des Diagramms nach Umstellung als Success-Kriterium |
| debug-plan-Aenderung beruehrt ein „Fertig zum Testen"-Skill (skill-10x-optimierungen) vor dessen Abnahme | Mittel | Mittel | Abnahme von skill-10x muss diese additive Aenderung einschliessen; im Changelog vermerken |
| Zeilen-Budget < 500 bei `pipeline-graph`/`debug-plan` ueberschritten | Niedrig | Mittel | Budget-Check je geaendertem Skill als Success-Kriterium |
| `plan-review`-Fallback greift ins Leere (weder global noch Projekt-Root) | Niedrig | Niedrig | Explizite Fehlermeldung mit Verweis auf Installation/`agents/` |
| Scope-Ueberlappung Persona-Quellen (#8) ↔ #10 fuehrt zu Doppelarbeit | Niedrig | Niedrig | Grenze in `## Offene Punkte` fixiert: hier nur benennen |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine harten Vorbedingungen — `change-folder-modell` (Ordner-Modell, `after/next`, §1.5)
      und `skill-10x-optimierungen` (debug-plan-Haertung) sind implementiert und ausgerollt

### Referenz-Dokumente
- `features/frontmatter-pfad-hygiene/discovery.md` - Discovery mit betroffenen Modulen und Randfaellen
- `project-rules/DERIVED_STATE_RULES.md` - §1.5 (`## Fix-Schritte`-Ableitung), §4 (Slug-Regel)
- `skills/dtb-pipeline-graph/SKILL.md` - Stage-Enum + Frontmatter-Reader + agents/-Glob
- `skills/dtb-debug-plan/SKILL.md` - aktuelles Ausgabe-Template

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `plan-review` laedt Agenten aus `~/.claude/agents/` und faellt auf Projekt-Root-`agents/` zurueck; fehlen beide, erscheint eine klare Meldung
- [ ] `pipeline-graph` globbt denselben Agenten-Pfad wie `plan-review` (kein `.claude/agents/*.md` mehr)
- [ ] `context: fork` ist aus `build-check` entfernt
- [ ] Stage-Enum enthaelt kein `bug` mehr; das generierte Diagramm zeigt keine leere Bug-Gruppe
- [ ] `after`/`next` sind Listen; `pipeline-graph` und `workflow-status` rendern mehrere Kanten pro Skill korrekt (verifiziert an `project-init` und `feature-start`)
- [ ] `debug-plan` schreibt `## Fix-Schritte`; ein damit analysierter Bug wird von `workflow-next`/`archive`/`workflow-status` regelkonform als Offen→Analysiert→In Arbeit→Behoben abgeleitet
- [ ] Jeder geaenderte Skill bleibt < 500 Zeilen
- [ ] Nach Merge zieht `kit-sync` die globalen Class-A-Kopien nach

---

## Offene Punkte

- **Persona-Quellen-Grenze (#8 ↔ #10):** Der Repo-Command referenziert bereits die Kit-Kopie
  (`@personas/…`). Soll die globale pitch-coach-Divergenz in dieser Runde nur dokumentiert werden,
  oder ist selbst die Dokumentation Sache von #10? (Aktuelle Annahme: hier nur benennen.)
- **`feature-discover`-Luecke in der `pipeline-graph`-Beispielkette** (Z. 198 ueberspringt
  `feature-discover`): als Low-Prio-Zusatz in Block B mitnehmen, oder als eigener Mini-Fix
  ausklammern?

---

**Erstellt mit:** `/dtb:feature-plan`
