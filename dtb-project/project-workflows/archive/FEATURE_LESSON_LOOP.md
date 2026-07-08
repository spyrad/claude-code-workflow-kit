# Feature: Lesson Loop

**Erstellt:** 2026-07-08
**Ziel:** Ein manuell kuratierter, append-only Lektionen-Speicher (`lessons.md`), den die Plan- und Review-Skills als Prior lesen — damit einmal gelernte, nicht-offensichtliche Regeln nicht in vergänglichen Session-Logs verloren gehen.
**Priorität:** Mittel
**Status:** Abgeschlossen (2026-07-08) <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit hat ein `pitfalls.md`-Template, das nie in einen Skill verdrahtet wurde — Erkenntnisse landen heute nur im Session-Log und werden nie wieder aktiv herangezogen. Dieses Feature führt einen neuen Skill `dtb:lesson` ein, der Lektionen (Context/Problem/Rule/Applies-to) schnell und append-only in `dtb-project/project-rules/lessons.md` erfasst, und verdrahtet vier Bestands-Skills (`impl-plan`, `debug-plan`, `plan-review`, `code-review`), sodass sie relevante Lektionen als Prior lesen und anwenden. Lektionen kommen über zwei Kanäle rein — manuell oder als Agent-Vorschlag während der Arbeit — beide immer mit Bestätigung, nie stiller Auto-Write.

---

## Scope / Abgrenzung

### Enthalten
- **Neuer Skill `dtb:lesson`:** Freitext-Erfassung → strukturiert in 4 Felder (Context / Problem / Rule / Applies-to), append-only nach `dtb-project/project-rules/lessons.md`; Capture-Speed wie `dtb:idea` (max. 1 Rückfrage: Applies-to, falls nicht ableitbar)
- **Zwei Eingangskanäle:** (1) manuell `/dtb:lesson "..."`; (2) Agent-Vorschlag während der Arbeit („💡 Lektion-Kandidat: ... übernehmen?") — beide mit Bestätigung, nie stiller Auto-Write
- **Prior-Verdrahtung in 4 Konsumenten** (`impl-plan`, `debug-plan`, `plan-review`, `code-review`): ganze `lessons.md` lesen, nach `Applies-to` passend zum Skill filtern, Regeln still anwenden, kompakter Hinweis „📚 X Lektionen berücksichtigt"
- **Vorschlager-Rolle** in den drei produzierenden Konsumenten (`impl-plan`, `debug-plan`, `code-review`): „Lektion-Kandidat erkennen"-Hinweis am Ende relevanter Schritte
- **Ablösung `pitfalls.md`:** Header-Hinweis „→ ersetzt durch dtb:lesson / lessons.md" (nicht löschen — Drittanbieter-Framework)
- **Pipeline-Frontmatter:** `dtb:lesson` mit `produces: lessons.md`; 4 Konsumenten mit `consumes: lessons.md`
- **Doku:** `CLAUDE.md` (Skill-Kategorie + Output-Location), `README.md` (Skill-Liste), `pipeline-graph` regenerieren

### Nicht enthalten
- Keine automatische Extraktion ohne Bestätigung (kein stiller Auto-Learning-Write)
- Kein Editieren/Löschen bestehender Einträge via Skill (append-only)
- Kein Ersetzen von Session-Logs oder der Code-Regeln in `project-rules/` (STYLE.md etc.)
- Kein Aufräum-/Archivierungs-Mechanismus für `lessons.md` (spätere `dtb:archive`-Erweiterung)
- Kein grep-basierter/Frontmatter-gesteuerter Read-Mechanismus (bewusst „ganze Datei + filtern" gewählt, solange Datei klein bleibt)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| `lessons.md` wächst und verwässert den Kontext | Mittel | Hoch | Soft-Limit ~150 Zeilen mit Hinweis (analog MEMORY.md); kompaktes 4-Felder-Format; append-only zwingt zu Bewusstsein |
| Rauschen: triviale/duplizierte Lektionen | Mittel | Mittel | Bestätigungspflicht (nie Auto-Write); Duplikat-Check via grep beim Erfassen; klare Trigger-Frage Session-Log vs. Lesson |
| Prior-Schritt bläht Konsumenten-Output auf | Mittel | Mittel | Nur kompakter Hinweis „📚 X berücksichtigt", Regeln still angewendet — keine Roman-Ausgabe |
| Vier Skills gleichzeitig zu ändern → Inkonsistenz | Mittel | Mittel | Einheitlicher, wiederverwendbarer Prior-Lese-Baustein; identische Formulierung in allen vier Skills |
| Widersprüchliche Lektionen | Niedrig | Mittel | Beim Konsumieren beide zeigen + Konflikt melden (nicht auflösen), analog Derived-State-Prinzip |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine (rein dateibasiert, keine externen Abhängigkeiten, keine aktiven Feature-Konflikte)

### Referenz-Dokumente
- `dtb-project/project-workflows/features/DISCOVERY_LESSON_LOOP.md` — Discovery-Ergebnisse (Scope, Randfälle, offene Punkte)
- `frameworks/claude-code-memory-framework/templates/pitfalls.md` — abzulösendes Konzept (Vorbild-Struktur)
- `skills/dtb-idea/SKILL.md` — Vorbild für Capture-Speed/UX
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — Vorbild „Konflikt melden, nicht auflösen"
- `frameworks/claude-code-memory-framework/templates/MEMORY.md` — Vorbild Größenlimit-Regel

---

## Offene Punkte (für impl-plan zu klären)

- `Applies-to`-Default-Regel: leer → „alle vier Konsumenten" vs. Rückfrage
- Größenlimit als harter Hinweis vs. Soft-Warnung (Vorschlag: Soft-Warnung ab ~150 Zeilen)
- Genauer Wortlaut/Trigger-Zeitpunkt des Agent-Vorschlags

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `dtb:lesson` erfasst eine Freitext-Lektion strukturiert (4 Felder) append-only in `dtb-project/project-rules/lessons.md`; Datei wird bei Bedarf angelegt
- [ ] Duplikat-Check und Applies-to-Handling funktionieren wie spezifiziert
- [ ] Alle vier Konsumenten lesen `lessons.md`, filtern nach `Applies-to` und zeigen den kompakten „📚 X Lektionen berücksichtigt"-Hinweis; fehlende/leere Datei bricht nicht ab
- [ ] Die drei produzierenden Skills schlagen Lektion-Kandidaten mit Bestätigung vor (kein Auto-Write)
- [ ] `pitfalls.md` trägt den Ablösungs-Hinweis; kein Datenverlust
- [ ] Pipeline-Frontmatter (`produces`/`consumes`) gesetzt; `pipeline-graph` regeneriert; `CLAUDE.md` + `README.md` aktualisiert
- [ ] Abnahme durch Praxis-/Fixture-Test (Muster DERIVED_STATE/KIT_SYNC): mind. ein voller Zyklus erfassen → konsumieren

---

**Erstellt mit:** `/dtb:feature-plan`
