# Discovery: Frontmatter- und Pfad-Hygiene
<!-- resume: done -->

**Erstellt:** 2026-07-09
**Idee-Referenz:** Inbox #8 + #9 (gebuendelte Hygiene-Runde)
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-plan-review/SKILL.md` | agents/-Pfad auf `~/.claude/agents/` + Projekt-Root-Fallback (`consumes` + Z. 48-51, 76) |
| `commands/dtb-pitch-coach.md` | Persona-Referenz: Repo zeigt bereits auf `@personas/…` — nur globale Divergenz benennen (Grenze zu #10) |
| `skills/dtb-pipeline-graph/SKILL.md` | Dreifach: globbt `.claude/agents/*.md` (Z. 49) → `agents/`; Stage-Enum-Eintrag `bug` entfernen (Z. 36, 87); `after/next`-Listen rendern |
| `skills/dtb-build-check/SKILL.md` | Nicht-Standard-Frontmatter `context: fork` (Z. 9) bereinigen |
| `skills/dtb-debug-plan/SKILL.md` | Ausgabe `#### Schritte`/`#### Testplan` (H4) → `## Fix-Schritte` (H2) |
| 8 Skills mit `after/next`-Asymmetrie | `project-init`, `workflow-resume`, `code-review`, `workflow-checkpoint`, `debug-plan`, `feature-start`, `generate-rules`, `project-team` → Felder zu Listen |
| `skills/dtb-workflow-status/SKILL.md` | Reader von `after/next` → Listen-Format; Reader von `## Fix-Schritte` (unveraendert) |
| `skills/dtb-workflow-next/`, `dtb-archive/` SKILL.md | Reader von `## Fix-Schritte` — bleiben unveraendert (Ausgabe zieht zu ihnen hin) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §1.5 `## Fix-Schritte`-Ableitung — Referenz, bleibt Ziel-Format |

---

## Anforderungen

### Scope
**Enthalten:**
- **Block A (#8):** `plan-review` liest Agenten aus `~/.claude/agents/` mit Projekt-Root-`agents/`-Fallback; klare Fehlermeldung, wenn beide leer
- **Block B (#9):** `pipeline-graph`-Glob auf `agents/`; `context: fork` in `build-check` bereinigen; Stage-Enum-Eintrag `bug` **entfernen**; `after/next` zu **Listen** erweitern + Reader (`pipeline-graph`, `workflow-status`) anpassen
- **Block C (#9):** `debug-plan` schreibt kuenftig `## Fix-Schritte` (H2) statt `#### Schritte`/`#### Testplan` — behebt aktiven Ableitungs-Bug (§1.5 + 3 Reader erwarten `## Fix-Schritte`)

**Nicht enthalten:**
- Kein Umbau der Pipeline-Semantik, keine neuen Skills
- Kein Eingriff in #10 (kit-sync pinned/hold) — globale pitch-coach-Divergenz wird nur benannt, nicht geloest
- Keine Auto-Migration bestehender `bug.md` mit altem `#### Schritte`-Format (nur benennen)

### Gewuenschtes Verhalten
- Rein interne/technische Aenderung, keine sichtbare Nutzer-UX
- `pipeline-graph`/`workflow-status` rendern nach dem Fix mehrere `after/next`-Kanten pro Skill (statt genau einer); Diagramm-Struktur sonst unveraendert
- `debug-plan`-Bugs werden korrekt aus `## Fix-Schritte` abgeleitet (Offen/Analysiert → In Arbeit → Behoben)

### Randfaelle
- Leere/`null`-`after`-Liste: Reader behandelt wie bisher (Monitoring-Skills bleiben kantenlos)
- Bestehende `bug.md` mit altem `#### Schritte`: **nur benennen**, keine Auto-Migration (Non-Guess-Prinzip)
- `plan-review`-Fallback greift ins Leere (kein `agents/` UND kein `~/.claude/agents/`): klare Meldung statt stiller Fehlschlag

### Einschraenkungen
- Zeilen-Budget je Skill < 500 (v.a. `pipeline-graph`, `debug-plan`)
- Nach Merge `kit-sync` noetig, damit globale Class-A-Kopien nachziehen
- Listen-Format darf `project-health`/`pipeline-graph`-Parsing nicht brechen

### Integrationspunkte
- Frontmatter-Reader: `pipeline-graph` + `workflow-status` → Listen-Format-faehig
- `## Fix-Schritte`-Reader: `workflow-next`, `archive`, `workflow-status`, `DERIVED_STATE_RULES.md` §1.5 → unveraendert (Ziel-Format)
- agents/-Pfad-Reader: `plan-review` + `pipeline-graph` → `~/.claude/agents/` + Projekt-Root-Fallback
- Externe Abhaengigkeiten: keine

---

## Abhaengigkeiten

- **Ueberschneidung (kein Konflikt):** `skill-10x-optimierungen` (Fertig zum Testen) haerte `debug-plan` — diese Runde aendert es additiv erneut; `change-folder-modell` (Fertig zum Testen) etablierte `DERIVED_STATE_RULES.md` + `after/next`, worauf diese Runde aufbaut. Beide noch nicht abgenommen → Abnahme sollte diese Aenderungen einschliessen.
- Konflikte: keine.

---

## Offene Punkte

- **Persona-Quellen (#8):** Repo-Command referenziert bereits die Kit-Kopie; die globale pitch-coach-Divergenz + kit-sync-Skip-Verhalten gehoert zu #10 (kit-sync pinned/hold) — hier nur benennen, Scope-Grenze in impl-plan/feature-plan sauber halten
- **`feature-discover`-Luecke** in der `pipeline-graph`-Beispielkette (Z. 198, ueberspringt `feature-discover`): als kleiner Zusatz in Block B mitnehmbar — im Plan als Low-Prio markieren

---

**Erstellt mit:** `/dtb:feature-discover`
