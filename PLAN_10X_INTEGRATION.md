# Plan: 10xDevs-Methodik Integration in DTB-Workflow

Erstellt: 2026-03-19
Quelle: `usb-spec-driven-method/referenzen/` (Lektionen, Checklisten, Prompt-Library)

---

## Analyse-Ergebnis

### Was der DTB-Workflow bereits gut abdeckt
- Session-Lifecycle (checkpoint/resume/status)
- Feature-Pipeline (discover -> plan -> impl -> review)
- Agent-Rollen (Architekt, Pragmatiker, Senior-Dev)
- Ideen-Management (inbox, idea-review, archive)
- Workflow-Visualisierung und Next-Action

---

## Uebernahme-Kandidaten

### 1. 3x3 Workflow als explizites Implementierungsmuster
**Quelle:** Modul 2 Checkliste, endpoint-implementation-33-workflow.md

Der wichtigste Fund. Die 10x-Methodik definiert ein hartes Limit: max. 3 Schritte implementieren, zusammenfassen, naechste 3 beschreiben, auf Feedback warten. Verhindert Scope-Creep und Kontextverlust.

**Umsetzung:** `impl-plan` und `feature-start` erhalten das 3x3-Muster als feste Regel. Der Implementierungsplan wird in 3er-Bloecke geschnitten, nach jedem Block ein Mini-Checkpoint.

---

### 2. Context-Hygiene-Regeln
**Quelle:** general-guidelines---10xworkflow.md, 1x3-wspopraca-z-ai-w-terminalu.md

Klare Regeln wann `/compact` und `/clear` eingesetzt werden:
- `/compact` nach Abschluss einer Feature-Phase
- `/clear` zwischen unabhaengigen Features
- `/context` regelmaessig pruefen (max. 70-80% Auslastung)
- **Rule of Three:** Wenn der 3. Fix-Versuch neue Bugs einfuehrt, Reset mit Summary

**Umsetzung:** `workflow-checkpoint` erhaelt einen Context-Hygiene-Hinweis.

---

### 3. Anti-Hallucination / Anti-Bias Patterns
**Quelle:** general-guidelines---10xworkflow.md, 1x5/1x6 Lektionen

Fuenf Techniken systematisch eingebaut:
- Devil's Advocate (Schwaechen finden)
- Alternativen-Vergleich (3+ Optionen erzwingen)
- Pre-Mortem ("Was ist schiefgegangen?")
- Multi-Perspektiven-Review (5+ Rollen)
- Unknown Unknowns identifizieren

**Umsetzung:** `plan-review` nutzt schon Agent-Rollen, aber ein expliziter "Challenge"-Modus fehlt. Die Agenten koennten gezielt Devil's-Advocate und Pre-Mortem anwenden.

---

### 4. Quality Gates pro Pipeline-Stage
**Quelle:** Alle Modul-Checklisten (2, 3, 4)

Explizite Pruefpunkte:
- Vor Bootstrap: MVP-Definition reviewed, Stack justified
- Vor Implementation: Plan reviewed, DB-Schema validiert
- Vor PR/Merge: Lint + Tests gruen
- Vor Deploy: Master-Pipeline gruen, Monitoring aktiv

**Umsetzung:** `workflow-status` zeigt Gate-Status an (z.B. "Feature X: Plan ok -> Review ok -> Impl laeuft -> Tests fehlen")

---

### 5. Socratic Discovery (Fragen statt Befehle)
**Quelle:** 1x5-efektywna-praca-z-ai-czesc-1.md

Statt direkt Specs zu schreiben: "Bevor du anfaengst, stelle mir 5-10 Fragen..."

**Umsetzung:** `feature-discover` macht das teilweise. Die 10x-Methodik betont es als universelles Pattern fuer jede Planungsphase (DB, API, UI jeweils eigene Discovery-Session). Koennte verstaerkt werden.

---

### 6. Feature-Level-Status bei Kontextverlust
**Quelle:** 2x5-generowanie-interfejsu-uzytkownika.md, 2x6 Lektion

Wenn der Kontext zu gross wird: Status-Dokument erstellen mit:
- Erledigte Schritte
- Offene Schritte laut Plan
- Erkannte Scope-Creep-Risiken

**Umsetzung:** `WORKFLOW_STATUS.md` deckt Projekt-Ebene ab, aber ein Feature-Level-Status bei langen Implementierungen fehlt. Koennte in `feature-start` eingebaut werden als optionales `IMPL_STATUS_*.md`.

---

### 7. Code-Review-Prioritaeten-Hierarchie
**Quelle:** code-review-command.md

Klare Reihenfolge:
1. Logik-Fehler / Bugs
2. Sicherheitsluecken
3. Performance
4. Wartbarkeit
5. Code-Style (letzte Prioritaet)

**Umsetzung:** `code-review` Skill erhaelt diese Hierarchie als explizite Pruefreihenfolge.

---

### 8. Spec-Files unter 500 Zeilen halten
**Quelle:** Modul 2 Checkliste

Jede Planungsdatei (PRD, DB-Plan, API-Plan, UI-Plan) max. 500 Zeilen fuer optimale AI-Verarbeitung.

**Umsetzung:** Fuer `FEATURE_*.md` und `PLAN_*.md` eine Obergrenze definieren (analog zur 60-80 Zeilen-Regel fuer `WORKFLOW_STATUS.md`).

---

### 9. Separate Analyse- vs. Implementierungsphase
**Quelle:** 3x4-refaktoryzacja-projektu-z-ai.md, 2x1 Lektion

Erst Analyse in eigenem Gespraech/Modus, dann Implementation in neuem Kontext. Verhindert Kontextverschmutzung.

**Umsetzung:** Unser Flow geht discover -> plan -> impl, aber die 10x-Methodik betont explizit: Plan-Konversation ist nicht gleich Impl-Konversation. Als Best Practice dokumentieren und in `workflow-next` als Hinweis einbauen.

---

### 10. Conventional Commits als Standard
**Quelle:** 2x2-przygotowanie-regu-dla-ai-i-bootstrap-projektu.md

`feat:`, `fix:`, `chore:`, `docs:`, `refactor:` nach jedem funktionierenden Inkrement.

**Umsetzung:** Als Regel in `project-rules/` Template aufnehmen.

---

## Nicht relevant fuer uns

- Stack-spezifische Details (Supabase RLS, Astro-Starter, React 19) — zu technologie-gebunden
- Kosten-Optimierung (Polish vs English Tokens) — nicht workflow-relevant
- Model-Empfehlungen (Gemini 2.5 Pro etc.) — veraltet schnell, nicht in Skills fixieren
- CI/CD und Deployment Details — zu projektspezifisch

---

## Priorisierung

| Prio | Massnahme | Aufwand | Impact | Betroffene Skills |
|------|-----------|---------|--------|-------------------|
| 1 | 3x3-Workflow in impl-plan/feature-start | Mittel | Hoch | impl-plan, feature-start |
| 2 | Quality Gates in workflow-status | Mittel | Hoch | workflow-status |
| 3 | Code-Review-Hierarchie | Klein | Mittel | code-review |
| 4 | Context-Hygiene-Regeln | Klein | Mittel | workflow-checkpoint |
| 5 | Anti-Bias-Modus in plan-review | Mittel | Mittel | plan-review, Agenten |
| 6 | Feature-Level-Status | Klein | Mittel | feature-start |
| 7 | 500-Zeilen-Limit fuer Specs | Klein | Klein | CLAUDE.md Konvention |
| 8 | Conventional Commits Template | Klein | Klein | project-rules/ |
| 9 | Separate Analyse/Impl-Phasen | Klein | Klein | workflow-next |
| 10 | Socratic Discovery verstaerken | Klein | Klein | feature-discover |
