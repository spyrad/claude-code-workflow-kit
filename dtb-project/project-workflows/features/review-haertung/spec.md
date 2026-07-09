# Feature: Review-Härtung

**Erstellt:** 2026-07-08
**Ziel:** plan-review und code-review liefern belastbare, mechanisch geprüfte Verdikte statt weicher Diskussions-Prosa — Pläne werden gegen die echte Codebase verifiziert, Findings priorisiert gecappt und Reviews wiederaufnehmbar.
**Priorität:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die beiden Review-Skills vertrauen heute darauf, dass die Agenten-Diskussion Probleme findet — Behauptungen des Plans über die Codebase werden geglaubt, Bewertungen bleiben unverbindlich (✅/⚠️/❌ ohne Konsequenz), und code-review-Findings haben weder Priorisierungs-Doppelachse noch Cap noch Wiederaufnahme-Möglichkeit. Dieses Feature härtet beide Skills mit fünf Bausteinen aus dem 10x-Vorbild: Challenger-Pass und ls/grep-Grounding machen plan-review mechanisch überprüfbar, Dimensions-Verdikte mit fester Aggregations-Regel (SOUND/REVISE/RETHINK) machen das Ergebnis verbindlich; Severity×Impact-Doppelachse, Findings-Cap 10 mit Fix-Optionen und Resume-Marker machen code-review fokussiert und unterbrechbar.

---

## Scope / Abgrenzung

### Enthalten

**plan-review (`skills/dtb-plan-review/SKILL.md`):**
1. **Challenger-Pass** — mechanische Konsistenz-Prüfung des Plans: Widersprüche zwischen Schritten, Promise-Gaps (Plan verspricht X, kein Schritt liefert es)
2. **ls/grep-Grounding** — Codebase-Behauptungen des Plans (Dateien, Funktionen, Strukturen) werden per Glob/Grep verifiziert; still bei Erfolg (`🔎 Grounding: N Referenzen geprüft, alle gefunden`), Abweichungen einzeln gemeldet
3. **Dimensions-Verdikte** — jeder aktive Agent (3 oder 4, je nach Betriebs-Wächter-Aktivierung) gibt PASS/WARN/FAIL pro Dimension in der Review-Zusammenfassung; Gesamt-Verdikt deterministisch: alle PASS → SOUND, ≥1 WARN ohne FAIL → REVISE, ≥1 FAIL → RETHINK

**code-review (`skills/dtb-code-review/SKILL.md`):**
4. **Findings-Härtung** — Severity×Impact-Doppelachse ersetzt einachsige Prio 1–5; Cap bei 10 Findings (Überlauf: „N weitere unterhalb des Caps"); Fix-Optionen mit Tradeoff + Confidence pro Finding
5. **Resume-Marker** — Triage-Stand als kopierbarer Textblock am Report-Ende (inkl. Commit-SHA des Review-Stands); beim nächsten Aufruf als Argument übergebbar, bei SHA-Abweichung Warnung + Rückfrage

**Flankierend:** minimale Ergänzung der 4 Agenten-Dateien (Verdikt-Pflicht), Verdikt-Dimensionen und Aggregations-Regel leben im Skill; nach Abschluss `dtb:kit-sync`.

### Nicht enthalten

- Kein Umbau der Runden-Struktur von plan-review (4 Runden + Betriebs-Wächter-Schritt 2c bleiben)
- Kein automatisches Fixen — beide Reviews bleiben read-only
- Resume-Marker ist kein persistentes Pipeline-Artefakt (keine Datei, kein neues `produces`)
- Keine Änderung am Lektionen-Prior (Schritt 2b) oder an `dtb-lesson`
- Keine Verdikte innerhalb der Diskussions-Runden (nur in der Zusammenfassung)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Skill-Aufblähung: plan-review (~206 Zeilen) wird durch 3 Bausteine unlesbar, Prompt-Qualität degradiert | Mittel | Hoch | Kompakte Formulierung, Templates straffen statt anbauen; Zeilen-Budget im Plan prüfen |
| Verdikt-Inflation: Agenten vergeben reflexhaft PASS (Leniency-Bias), Verdikte werden Theater | Mittel | Hoch | Feste Aggregations-Regel ohne Modell-Freiheit; Verdikte erst NACH der Challenge-Runde; Dimensionen eng definiert |
| Grounding-Fehlalarme: Grep findet dynamische/implizite Referenzen nicht → falsches „nicht gefunden" | Mittel | Mittel | Nur eindeutig prüfbare Referenzen werten; Unsicheres als Hinweis, nie als FAIL-Treiber |
| Regression an Betriebs-Wächter (2c) oder Lektionen-Prior (2b) beim Umbau | Niedrig | Hoch | Isolierte Abnahme durch unabhängigen Agenten mit Regressions-Szenarien (Muster DERIVED_STATE/LESSON_LOOP) |
| Doppelachse + Fix-Optionen machen code-review-Reports länger statt schärfer | Mittel | Mittel | Cap 10 wirkt als Gegengewicht; Fix-Optionen kompakt (1 Zeile pro Option) |
| Resume-Marker wird auf verändertem Stand eingelöst → Triage passt nicht mehr zum Code | Mittel | Mittel | Commit-SHA im Marker; bei Abweichung Warnung + Frage ob frisches Review |

---

## Dependencies

### Erforderlich vor Start

- [x] Discovery abgeschlossen (`DISCOVERY_REVIEW_HAERTUNG.md`)
- [x] Betriebs-Wächter-Umbau von plan-review abgeschlossen (Commit `4ee4a9a`) — dieses Feature baut darauf auf
- [ ] Keine weiteren — Pipeline ist leer, keine konkurrierenden Änderungen an den Ziel-Dateien

### Referenz-Dokumente

- `dtb-project/project-workflows/features/DISCOVERY_REVIEW_HAERTUNG.md` — Discovery mit allen Verhaltens-Entscheidungen und Randfall-Regeln
- `skills/dtb-plan-review/SKILL.md` — Ziel-Datei Bausteine 1–3 (Ist-Zustand: 4 Runden, Schritt 2b Prior, Schritt 2c Betriebs-Wächter)
- `skills/dtb-code-review/SKILL.md` — Ziel-Datei Bausteine 4–5 (Ist-Zustand: einachsige Prio 1–5, Konsolen-Report)
- `agents/{architekt,pragmatiker,senior-dev,betriebs-waechter}.md` — Agenten-Definitionen (Verdikt-Pflicht ergänzen)
- 10x-devs-3.0 Kurs-Repo (`10x-impl-review`/`10x-plan-review`) — Vorbild, wird nicht eingebunden

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] **SC1 Grounding:** plan-review prüft Codebase-Referenzen eines Fixture-Plans; eine eingebaute Fake-Referenz wird gemeldet, echte Referenzen erzeugen genau eine stille Erfolgszeile
- [ ] **SC2 Challenger-Pass:** ein eingebauter Widerspruch und ein Promise-Gap im Fixture-Plan werden als Findings gemeldet
- [ ] **SC3 Verdikte:** Review-Zusammenfassung enthält Verdikt-Matrix (Agent × Dimension, PASS/WARN/FAIL) + Gesamt-Verdikt nach fester Regel — korrekt bei 3 UND 4 aktiven Agenten
- [ ] **SC4 Randfall Grounding-leer:** Plan ohne prüfbare Referenzen → `🔎 Grounding: keine prüfbaren Referenzen`, kein Abbruch
- [ ] **SC5 Doppelachse + Cap:** code-review-Report priorisiert nach Severity×Impact; bei >10 Findings werden Top 10 gezeigt + Überlauf-Zeile
- [ ] **SC6 Fix-Optionen:** jedes Finding hat mindestens eine Fix-Option mit Tradeoff und Confidence
- [ ] **SC7 Resume:** abgebrochenes code-review gibt Resume-Marker aus; Wiederaufnahme mit Marker überspringt triagierte Findings; SHA-Abweichung erzeugt Warnung + Rückfrage
- [ ] **SC8 Regression:** Betriebs-Wächter-Aktivierung (2c) und Lektionen-Prior (2b) funktionieren unverändert (beide Skills)
- [ ] **SC9 Abnahme:** isolierte Fixture-Abnahme durch unabhängigen Agenten ohne Session-Kenntnis bestanden
- [ ] **SC10 Verteilung:** `dtb:kit-sync` check → sync durchgeführt, Lock aktualisiert

---

**Erstellt mit:** `/dtb:feature-plan`
