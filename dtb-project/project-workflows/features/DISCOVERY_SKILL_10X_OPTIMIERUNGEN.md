# Discovery: SKILL_10X_OPTIMIERUNGEN

**Erstellt:** 2026-07-09
**Idee-Referenz:** Inbox #6 — "10x-Optimierungen fuer Bestands-Skills (Sammelidee): project-health → Kategorie A/B (jetzt/spaeter) + WARN-AND-CONTINUE + Fixes mit Kommando/Aufwand; debug-plan → Hypothesen-Tabelle mit Evidenzstaerke STRONG/WEAK/NONE + „Framing war korrekt" als valides Ergebnis; greenfield-roadmap → vertikale Slices + Foundations mit Unlocks-Feld + Selbst-Review-Checkliste; feature-discover → Checkpoint-Frontmatter (resumebar) + „(Recommended)"-Option-Muster; workflow-checkpoint/-resume → Handoff mit naechstem Befehl + /clear-Hinweis"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-project-health/SKILL.md` (344 Z.) | Kategorie A/B (jetzt/spaeter), WARN-AND-CONTINUE, Fixes mit Kommando/Aufwand |
| `skills/dtb-debug-plan/SKILL.md` (173 Z.) | Hypothesen-Tabelle mit Evidenzstaerke STRONG/WEAK/NONE, „Framing war korrekt" als valides Ergebnis |
| `skills/dtb-greenfield-roadmap/SKILL.md` (208 Z.) | Vertikale Slices + Foundations mit Unlocks-Feld + Selbst-Review-Checkliste (read-only, keine Write-Faehigkeit) |
| `skills/dtb-feature-discover/SKILL.md` (227 Z.) | Checkpoint-Frontmatter (resumebar), „(Recommended)"-Option-Muster |
| `skills/dtb-workflow-checkpoint/SKILL.md` (222 Z.) | Handoff mit naechstem Befehl + /clear-Hinweis (Sende-Seite) |
| `skills/dtb-workflow-resume/SKILL.md` (173 Z.) | Gegenstueck zum Handoff (Empfangs-Seite) |

---

## Anforderungen

### Scope
**Enthalten:**
- Alle 5 Bloecke der Sammelidee als **ein** Feature (Nutzer-Entscheidung 2026-07-09)
- Block 1 — project-health: Kategorie A/B (jetzt/spaeter), WARN-AND-CONTINUE, Fixes mit Kommando/Aufwand
- Block 2 — debug-plan: Hypothesen-Tabelle mit Evidenzstaerke STRONG/WEAK/NONE, „Framing war korrekt" als valides Endergebnis
- Block 3 — greenfield-roadmap: vertikale Slices, Foundations mit Unlocks-Feld, Selbst-Review-Checkliste — als Verbesserung der bestehenden read-only-Uebersicht (Nutzer-Entscheidung: drin lassen, kollisionsfrei zu #11)
- Block 4 — feature-discover: Checkpoint-Frontmatter (resumebar), „(Recommended)"-Option-Muster
- Block 5 — workflow-checkpoint/-resume: Handoff mit naechstem Befehl + /clear-Hinweis (beidseitig konsistent)

**Nicht enthalten:**
- Keine anderen Skills anfassen (Konsistenz-Rundumschlag = Idee #9)
- Keine strukturellen Umbauten, nur additive Haertung im bestehenden Skill-Format
- Keine Write-Faehigkeit fuer greenfield-roadmap (Autoren-Rolle = Idee #11)
- Kein erzwungenes globales kit-sync als Umsetzungsschritt (separater Abschlussschritt wie gehabt)

### Gewuenschtes Verhalten
- Alle Aenderungen additiv im bestehenden Skill-Format (YAML-Frontmatter + Markdown-Schritte), keine Umnummerierung bestehender Kern-Schritte wo vermeidbar
- Uebernahme der 10x-Muster als Vorbild, angepasst an DTB-Konventionen (deutsch, `YYYY-MM-DD`, relative Pfade)
- „(Recommended)"-Muster = erste Option markiert (konsistent mit AskUserQuestion-Nutzung in DTB)

### Randfaelle
- project-health WARN-AND-CONTINUE: ein fehlgeschlagener Einzel-Check bricht den Gesamt-Report nicht ab, sondern wird als WARN gelistet
- debug-plan „Framing war korrekt": explizit valides Endergebnis (keine Hypothese bestaetigt → Problem-Framing selbst war falsch/schon geloest)
- checkpoint/resume Handoff: wenn kein naechster Befehl ableitbar ist, neutraler Fallback statt erfundener Empfehlung

### Einschraenkungen
- Zeilen-Budget: 500-Zeilen-Obergrenze gilt; project-health ist mit 344 Z. am vollsten — additive Bloecke muessen knapp bleiben
- Keine neuen Runtime-Abhaengigkeiten (reine Prompt-/Markdown-Aenderungen)

### Integrationspunkte
- Pipeline-Frontmatter (`stage/after/next/consumes/produces`) bleibt konsistent; `workflow-status` und `pipeline-graph` lesen es
- checkpoint ↔ resume Handoff koppelt zwei Skills — Format muss auf beiden Seiten zueinander passen
- DERIVED_STATE_RULES.md nicht betroffen (keine Statusableitungs-Aenderung)

---

## Abhaengigkeiten

- Bestehende Features: 2 (REVIEW_HAERTUNG, SPEC_HAERTUNG) — beide betreffen andere Skills, **keine Konflikte, keine Ueberschneidungen**
- Methodik-Vorbild: additive Haertung + Fixture-basierte Abnahme durch unabhaengigen Agenten (aus REVIEW/SPEC_HAERTUNG uebernehmen)
- Idee #11 (Greenfield-Redesign): kollisionsfrei, da roadmap-Block hier bewusst read-only bleibt

---

## Offene Punkte

- Umsetzungs-Reihenfolge der 5 Bloecke (unabhaengig; Vorschlag: nach Blast-Radius/Nutzen in impl-plan festlegen)
- Ob die 5 Bloecke je einen eigenen Zwischen-Meilenstein in `## Progress` bekommen (empfohlen, da unabhaengig abnehmbar)
- Genaue Abnahme-Strategie pro Skill (Fixture vs. Praxiserprobung) — in feature-plan/impl-plan klaeren

---

**Erstellt mit:** `/dtb:feature-discover`
