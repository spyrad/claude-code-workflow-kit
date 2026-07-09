# Discovery: Lesson Loop

**Erstellt:** 2026-07-08
**Idee-Referenz:** Inbox #2 — "Neuer Skill `dtb:lesson` + Lern-Feedback-Loop: append-only `lessons.md` (Context/Problem/Rule/Applies-to), wird von impl-plan, debug-plan, plan-review und code-review als Prior gelesen; verdrahtet das bisher tote pitfalls.md-Konzept (Vorbild: 10x-lesson)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-lesson/SKILL.md` | **Neu** — Capture-Skill, schreibt append-only nach `lessons.md` (Struktur Context/Problem/Rule/Applies-to) |
| `skills/dtb-impl-plan/SKILL.md` | Konsument (Prior-Lese-Schritt) + Vorschlager (Lektion-Kandidat erkennen) |
| `skills/dtb-debug-plan/SKILL.md` | Konsument (Prior-Lese-Schritt) + Vorschlager (Lektion-Kandidat erkennen) |
| `skills/dtb-code-review/SKILL.md` | Konsument (Prior-Lese-Schritt) + Vorschlager (Lektion-Kandidat erkennen) |
| `skills/dtb-plan-review/SKILL.md` | Konsument (Agenten ziehen Lektionen als Prior heran) |
| `dtb-project/project-rules/lessons.md` | **Neu (Laufzeit)** — append-only Lektionen-Datei, beim ersten `dtb:lesson`-Aufruf angelegt |
| `frameworks/claude-code-memory-framework/templates/pitfalls.md` | Als abgelöst markieren (Header-Hinweis → `dtb:lesson`/`lessons.md`); nicht löschen (Drittanbieter-Framework) |
| `CLAUDE.md` (Root) | Skill-Kategorie „Knowledge management" + Output-Location `lessons.md` ergänzen |
| `README.md` | Skill-Liste ergänzen |
| `skills/dtb-pipeline-graph` (Output) | Pipeline-Graph regenerieren (neuer Skill + `consumes`/`produces`-Kanten) |

---

## Anforderungen

### Scope
**Enthalten:**
- Neuer Skill `dtb:lesson`: schnelles Erfassen einer Lektion (Freitext rein → strukturiert in 4 Felder: Context / Problem / Rule / Applies-to), append-only nach `dtb-project/project-rules/lessons.md`
- **Zwei Eingangskanäle:** (1) manuell via `/dtb:lesson "..."`; (2) Agent-Vorschlag während der Arbeit („💡 Lektion-Kandidat: ... übernehmen?") — beide immer mit Bestätigung, **nie stiller Auto-Write**
- Vier Bestands-Skills lesen `lessons.md` als **Prior**: ganze Datei lesen, nach `Applies-to` passend zum Skill filtern, relevante Regeln still anwenden, kompakter Hinweis „📚 X Lektionen berücksichtigt"
- Die drei produzierenden Konsumenten (`impl-plan`, `debug-plan`, `code-review`) bekommen zusätzlich einen „Lektion-Kandidat erkennen"-Hinweis (Vorschlager-Rolle)
- Das tote `pitfalls.md`-Konzept wird durch `lessons.md` abgelöst und verdrahtet

**Nicht enthalten:**
- Keine automatische Extraktion ohne Bestätigung (kein stiller Auto-Learning-Write)
- Kein Editieren/Löschen bestehender Einträge via Skill (append-only)
- Kein Ersetzen von Session-Logs oder der Code-Regeln in `project-rules/` (STYLE.md etc.)
- Kein Aufräum-/Archivierungs-Mechanismus für `lessons.md` (spätere `dtb:archive`-Erweiterung, nicht Teil dieses Features)

### Gewünschtes Verhalten
- Erfassen fühlt sich an wie `dtb:idea`: Speed, kein Formular, max. 1 Rückfrage (Applies-to, falls nicht ableitbar)
- Konsumenten zeigen kompakt „📚 X relevante Lektionen berücksichtigt" und wenden Regeln still an — keine Roman-Ausgabe
- Übernommene UX-Muster: Capture-Speed von `dtb:idea`, append-only-Tabellenmuster von `INBOX.md`
- `Applies-to`-Werte = feste, ableitbare Skill-Namen (`impl-plan`, `debug-plan`, `plan-review`, `code-review`)

### Randfälle
- `lessons.md` fehlt beim Konsumieren → Skill läuft normal weiter (kein Abbruch), Hinweis „keine Lektionen vorhanden"; beim Erfassen fehlend → Datei wird angelegt
- Leere `lessons.md` (nur Header) → Konsumenten überspringen Prior-Schritt still
- Duplikat-Lektion beim Erfassen → grep nach ähnlichem Rule-Text, Hinweis statt hartem Block
- `Applies-to` unklar/leer → Default „alle vier Konsumenten" oder Rückfrage
- Widersprüchliche Lektionen → beim Konsumieren beide zeigen, Konflikt melden (nicht selbst auflösen — analog Derived-State-Prinzip)

### Einschränkungen
- **Technisch:** `lessons.md` klein halten (AI-Kontext-Qualität) — Soft-Limit ~150 Zeilen, Hinweis bei Überschreitung (analog MEMORY.md-Regel); kompaktes Format (4 Felder/Eintrag); rein dateibasiert, kein Netz, keine neuen Tools
- **Fachlich:** append-only; Kuratierung/Aufräumen manuell (nicht Teil dieses Features)

### Integrationspunkte
- Betroffen: `impl-plan`, `debug-plan`, `plan-review`, `code-review` (je +1 Prior-Lese-Schritt; drei davon +1 Vorschlager-Hinweis)
- `pitfalls.md` als abgelöst markieren; `CLAUDE.md` + `README.md` Skill-Liste/Output-Locations ergänzen; `pipeline-graph` regenerieren
- Pipeline-Frontmatter: `dtb:lesson` mit `produces: lessons.md`; vier Konsumenten mit `consumes: lessons.md` (dokumentiert Abhängigkeit für `project-health`/`pipeline-graph`)
- Externe Abhängigkeiten: keine

---

## Abhängigkeiten

- Keine aktiven Features in der Pipeline (0 in `features/`, alle archiviert) → keine Feature-Konflikte
- Konzeptionelle Überschneidung Session-Log ↔ Lesson geklärt: Session-Log = vergänglich („was ist diese Session passiert"), Lesson = dauerhafte Regel („gilt künftig"). Trigger-Frage für Vorschlag: „Würde ich denselben Fehler nochmal machen, wenn es nur im Session-Log steht?"
- Verwandte offene Ideen: #6 (10x-Optimierungen Bestands-Skills — berührt teils dieselben Skills), #3 (Review-Härtung — plan-review/code-review). Kein Blocker, aber bei Umsetzung koordinieren.

---

## Offene Punkte

- Konkrete `Applies-to`-Default-Regel (alle vier vs. Rückfrage) — final im Feature-Spec festlegen
- Ob `lessons.md`-Größenlimit als harter Hinweis oder nur Soft-Warnung — im Spec präzisieren
- Genaues Format des Agent-Vorschlags (Wortlaut/Trigger-Zeitpunkt) — im Spec/impl-plan festzurren

---

**Erstellt mit:** `/dtb:feature-discover`
