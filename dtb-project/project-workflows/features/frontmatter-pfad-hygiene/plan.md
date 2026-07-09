# Implementierungsplan: Frontmatter- und Pfad-Hygiene

**Erstellt:** 2026-07-09
**Feature-Spec:** `features/frontmatter-pfad-hygiene/spec.md`
**Geschaetzte Dauer:** ~3,5 h (4 Phasen)
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Pfad-Konvention (agents/) — Block A + B-Pfadteil | ~30 min | Geplant |
| Phase 2 | Frontmatter-Format — Block B (Listen, Reader, Enum, Doku) | ~80 min | Geplant |
| Phase 3 | debug-plan-Ausgabe — Block C | ~25 min | Geplant |
| Phase 4 | Abnahme + kit-sync | ~70 min | Geplant |

**Reihenfolge-Begruendung:** Phase 1 zuerst, weil #8∩#9 sich am agents/-Pfad ueberlappen
(einmal loesen, beide Skills gleich). Phase 2 (Format) vor Phase 3 nicht zwingend, aber
gruppiert die risikoreichste Reader-Anpassung. Phase 4 buendelt Abnahme + Rollout wie in den
Vorgaenger-Features.

---

## Phase 1: Pfad-Konvention (agents/)

### Ziel
`plan-review` und `pipeline-graph` lesen Agenten aus derselben Quelle: `~/.claude/agents/`
mit Projekt-Root-`agents/`-Fallback.

### Schritte

#### Schritt 1.1: plan-review auf global + Fallback
- **Zweck:** Zielprojekte ohne eigenen `agents/`-Ordner laufen nicht mehr ins Leere (#8)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** die 4 namentlichen Referenzen (Z. 48-51, 76) + `consumes` (Z. 14)
- **Output:** Agenten-Ladeanweisung „aus `~/.claude/agents/{name}.md`, Fallback Projekt-Root
  `agents/{name}.md`"; klare Meldung, wenn beide fehlen; `consumes` nachgezogen

#### Schritt 1.2: pipeline-graph-Glob umstellen
- **Zweck:** Konsistenz mit 1.1; kein `.claude/agents/*.md` mehr (#9-Ueberlappung)
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`
- **Input:** Glob Z. 49 + Artefakt-Tabelle Z. 268
- **Output:** Glob auf `~/.claude/agents/*.md` mit Projekt-Root-`agents/`-Fallback;
  **`CLAUDE.md`-Ausnahme beibehalten** (Z. 52); Tabelle konsistent

#### Schritt 1.3: Pfad-Konsistenz verifizieren
- **Zweck:** Beide Skills nennen exakt denselben Pfad + dieselbe Fallback-Regel
- **Dateien:** beide o. g. + Grep-Gegenprobe ueber alle Skills nach `.claude/agents`
- **Input:** Ergebnis 1.1/1.2
- **Output:** kein `.claude/agents/`-Rest ausser der bewussten CLAUDE.md-Ausnahme; Notiz falls
  weitere Fundstellen

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] plan-review + pipeline-graph lesen global mit Fallback
- [ ] CLAUDE.md-Ausnahme intakt

### Checkpoint-Kriterien
- [ ] Grep nach `.claude/agents` liefert nur die dokumentierte CLAUDE.md-Ausnahme
- [ ] Fehler-Meldung bei fehlenden Agenten beschrieben

---

## Phase 2: Frontmatter-Format

### Ziel
`after`/`next` bilden die reale 1:n-Pipeline ab; tote Enum-/Frontmatter-Eintraege entfernt;
Reader verstehen das Listen-Format.

### Schritte

#### Schritt 2.1: after/next zu Listen erweitern
- **Zweck:** 1:n-Verzweigung abbildbar (`project-init → {generate-rules, project-team,
  workflow-resume}`; `{plan-review, debug-plan} → feature-start`) (#9)
- **Dateien:** alle Skills mit Kanten — mind. `project-init`, `workflow-resume`, `code-review`,
  `workflow-checkpoint`, `debug-plan`, `feature-start`, `generate-rules`, `project-team`
  (plus die uebrigen mit Einzelkante, einheitlich als 1-Element-Liste)
- **Input:** Frontmatter-Kanten-Landschaft (siehe Technische Entscheidungen)
- **Output:** `after`/`next` durchgaengig Listen-Syntax; verzweigende Kanten vollstaendig

#### Schritt 2.2: Reader auf Listen-Format anpassen
- **Zweck:** die *tatsaechlichen* `after/next`-Reader rendern/validieren Listen korrekt
- **Reader-Kartierung (Grounding, verifiziert):** echte Konsumenten sind `pipeline-graph`
  (Kanten-Ableitung Z. 202) und **`project-health`** (validiert `pipeline.after`/`pipeline.next`
  gegen existierende Skills + Zyklen-Check, Z. 198-201). `workflow-status` ist **kein** Reader
  (Z. 61 = `bug.md`-Ableitung, kein Frontmatter-Kanten-Lesen) → NICHT anfassen
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`, `skills/dtb-project-health/SKILL.md`
- **Input:** neues Listen-Format aus 2.1
- **Output:** `pipeline-graph` iteriert ueber Kanten-Listen (Diagramm zeigt Verzweigungen);
  `project-health` prueft jedes Listen-Element als existierenden Skill + Zyklen ueber alle Kanten
  (bricht nicht an Liste-statt-String)

#### Schritt 2.3: context:fork + Stage-Enum `bug` bereinigen
- **Zweck:** tote/nicht-standard Frontmatter entfernen (#9)
- **Dateien:** `skills/dtb-build-check/SKILL.md` (Z. 9), `skills/dtb-pipeline-graph/SKILL.md`
  (Enum Z. 36 + Stage-Tabelle Z. 87)
- **Input:** Bestand
- **Output:** `context: fork` entfernt; Stage `bug` aus Enum + Tabelle raus; kein Skill referenziert
  `stage: bug`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Doku-Konsistenz (Nebenbefunde)
- **Zweck:** zwei triviale Migrations-/Doku-Reste in derselben Datei-Familie schliessen
- **Dateien:** `BACKLOG.md` (Status-Legende Z. 53-54), `skills/dtb-pipeline-graph/SKILL.md`
  (Beispielkette Z. 198)
- **Input:** Nebenbefunde aus Scan + Review (Nutzer-Entscheid: in-scope)
- **Output:** Legende nennt `discovery.md`/`spec.md`/`plan.md` statt `DISCOVERY_*/FEATURE_*/PLAN_*`;
  Beispielkette Z. 198 ergaenzt `feature-discover` (zwischen `idea-review` und `feature-plan`)

> **3x3-Block:** Nach Schritt 2.4 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Listen-Format ueberall; 1:n-Kanten vollstaendig
- [ ] `pipeline-graph` + `project-health` Listen-faehig; Enum/context bereinigt; Doku-Reste geschlossen

### Checkpoint-Kriterien
- [ ] Testweise `pipeline-graph`-Ableitung zeigt `project-init` mit 3 Nachfolgern, `feature-start`
      mit 2 Vorgaengern
- [ ] `project-health` validiert die Listen-Kanten ohne Parse-/Typfehler
- [ ] Grep nach `context: fork` und `stage: bug` liefert 0 Treffer

---

## Phase 3: debug-plan-Ausgabe

### Ziel
`debug-plan` schreibt eine Struktur, aus der der Bug-Status regelkonform (§1.5) ableitbar ist.

### Schritte

#### Schritt 3.1: Ausgabe-Template auf `## Fix-Schritte`
- **Zweck:** aktiven Ableitungs-Bug beheben — `#### Schritte`/`#### Testplan` (H4) → `## Fix-Schritte`
  (H2) als abhakbare Checkliste (Block C, 2a)
- **Dateien:** `skills/dtb-debug-plan/SKILL.md` (Template Z. 105-134, Anleitung Z. 97/148-152)
- **Input:** DERIVED_STATE_RULES §1.5 (Ziel-Format), aktuelles Template
- **Output:** `bug.md`-Ausgabe enthaelt `## Fix-Schritte` als Checkliste; Testplan als **eigener H2
  ausserhalb** der `## Fix-Schritte`-Checkliste (Entscheidung B — schuetzt die §1.5-Zaehlung)

#### Schritt 3.2: Konsistenz gegen Reader verifizieren
- **Zweck:** sicherstellen, dass `workflow-next`/`archive`/`workflow-status`/§1.5 das neue Format
  korrekt ableiten — diese bleiben unveraendert
- **Dateien:** Gegenprobe (kein Write): `workflow-next` Z. 41, `archive` Z. 51, `workflow-status`
  Z. 61 ff., `DERIVED_STATE_RULES.md` §1.5
- **Input:** Ergebnis 3.1
- **Output:** bestaetigte Uebereinstimmung; Abweichung → als Finding vermerken

> **3x3-Block:** Nach Schritt 3.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] debug-plan schreibt `## Fix-Schritte`
- [ ] Reader-Konsistenz bestaetigt

### Checkpoint-Kriterien
- [ ] Ein Beispiel-`bug.md` aus debug-plan wird von der §1.5-Ableitung korrekt eingestuft

---

## Phase 4: Abnahme + kit-sync

### Ziel
Unabhaengige Abnahme der drei Bloecke, Budget-Check, globaler Rollout.

### Schritte

#### Schritt 4.1: Unabhaengige Abnahme
- **Zweck:** Verhalten wortlautkonform pruefen (Vorbild: Vorgaenger-Features)
- **Dateien:** Fixtures im Scratchpad (kein Commit)
- **Input:** geaenderte Skills
- **Output:** unabhaengiger Agent prueft: (a) pipeline-graph rendert 1:n-Kanten + keine leere
  Bug-Gruppe, (b) debug-plan-`bug.md` wird korrekt abgeleitet, (c) plan-review-Fallback +
  Leer-Meldung; Ergebnis PASS/FAIL je Block

#### Schritt 4.2: Findings beheben + Budget-Check
- **Zweck:** Ambiguitaeten schliessen, Zeilen-Budget wahren
- **Dateien:** je nach Findings
- **Input:** Abnahme-Ergebnis
- **Output:** Findings eingearbeitet; jeder geaenderte Skill < 500 Zeilen (Nachweis)

#### Schritt 4.3: kit-sync global
- **Zweck:** globale Class-A-Kopien nachziehen
- **Dateien:** `~/.claude/` (betroffene Skills + Lock)
- **Input:** gemergter Stand
- **Output:** `kit-sync` check → sync; R=L=K verifiziert; Lock aktualisiert; pitch-coach-Umgang
  wie gehabt

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Abschluss

### Deliverables
- [ ] Abnahme PASS je Block
- [ ] Global ausgerollt, Lock aktuell

### Checkpoint-Kriterien
- [ ] Alle 8 Success-Kriterien der Spec erfuellt
- [ ] Budget < 500 Z. je Skill nachgewiesen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| after/next-Format | A: nur verzweigende Kanten zu Listen; B: alle Kanten einheitlich Listen (auch 1-Element) | **B** | Reader muss nur ein Format kennen; keine Sonderfall-Logik |
| debug-plan Header-Status-Feld | A: beibehalten als abgeleitete Anzeige; B: entfernen | **A** | Konsistent mit spec.md-Muster (abgeleitete Anzeige); Ableitung kommt aus `## Fix-Schritte`, Feld nur Anzeige |
| Testplan in debug-plan | A: als Unterpunkt in `## Fix-Schritte`; B: eigener H2 ausserhalb der Checkliste | **B** | Testplan-Zeilen duerfen die Fix-Schritte-Zaehlung (§1.5) nicht verfaelschen |
| CLAUDE.md bei global-Glob | ignorieren | ignorieren | pipeline-graph tut das bereits (Z. 52); plan-review nennt Agenten namentlich → unkritisch |
| after/next-Reader | pipeline-graph / +project-health / +workflow-status | **pipeline-graph + project-health** | Grounding: workflow-status liest keine Frontmatter-Kanten; project-health validiert sie (Z. 198-201) — beide muessen Listen koennen |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg.

- [x] 1.1 plan-review global + Fallback — `224bba9` (Schritt 2 auf `~/.claude/agents/`+Fallback+Leer-Meldung, betriebs-waechter-Ladezeile nachgezogen)
- [x] 1.2 pipeline-graph-Glob umstellen — `224bba9` (Glob + Artefakt-Tabelle auf `~/.claude/agents/`+Fallback, CLAUDE.md-Ausnahme erhalten)
- [x] 1.3 Pfad-Konsistenz verifizieren — `224bba9` (Grep: kein `.claude/agents/*.md`-Rest, nur beabsichtigte globale Pfade)
- [x] 2.1 after/next zu Listen (einheitlich) — alle Einzelwerte + 1:n (project-init→3, feature-start←2, checkpoint/resume-Symmetrie)
- [x] 2.2 Reader (pipeline-graph + project-health) Listen-faehig — Kanten-Iteration + Element-weise Validierung
- [x] 2.3 context:fork + Stage-Enum `bug` bereinigen — Grep 0 Treffer
- [ ] 2.4 Doku-Konsistenz (BACKLOG-Legende + pipeline-graph-Beispielkette)
- [ ] 3.1 debug-plan Ausgabe auf `## Fix-Schritte`
- [ ] 3.2 Reader-Konsistenz verifizieren
- [ ] 4.1 Unabhaengige Abnahme
- [ ] 4.2 Findings beheben + Budget-Check
- [ ] 4.3 kit-sync global

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/frontmatter-pfad-hygiene/plan.md` laden; der erste nicht abgehakte
Schritt ist der naechste. Erkenntnisse/Abweichungen gehoeren in den Session-Log
(`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
