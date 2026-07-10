# Feature: SPEC_HAERTUNG

**Erstellt:** 2026-07-09
**Ziel:** `feature-plan`-Specs lösungsneutral und ehrlich halten — technische Lecks vor dem Speichern blockieren, fehlendes Wissen sichtbar parken statt erfinden.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- expliziter Zustand (ueberschreibt Ableitung), gesetzt 2026-07-10 nach 2 blinden feature-plan-Abnahmelaeufen (unabh. Agenten): SC1-8 belegt, Hard-Block feuert bei Leck-Spec, Baustein B parkt fehlendes Wissen in Offene Punkte -->

---

## Executive Summary

`dtb:feature-plan` erzeugt Feature-Specs, die das **Was/Warum** beschreiben sollen — nicht das **Wie**. In der Praxis lecken technische Details (Vendor-Namen, ORM-Notation, Protokolle) in die Spec und das Modell füllt ungeklärte Lücken mit plausiblen Erfindungen. SPEC_HAERTUNG ergänzt `feature-plan` um zwei Schutzmechanismen aus dem 10x-Vorbild: einen **Technical-Leak-Lint** (blockiert den Write bei technischen Lecks, Override möglich) und eine **„nie erfinden"-Regel** (fehlendes Wissen wandert in `## Offene Punkte` statt in geratene Fakten). Beide sorgen dafür, dass eine Spec nur gesichertes, lösungsneutrales Wissen enthält.

---

## Scope / Abgrenzung

### Enthalten

**Baustein A — Technical-Leak-Lint** in `dtb:feature-plan`
- Prüft den erzeugten Spec-Text unmittelbar **vor dem Write** auf technische Lecks in **7 Kategorien**:
  1. Vendor-/Produktnamen (z.B. PostgreSQL, Redis, AWS S3)
  2. ORM-/Query-Notation (z.B. `User.objects.filter()`, `SELECT * FROM`)
  3. Transport/Protokoll (z.B. REST-Endpoint `POST /users`, WebSocket, gRPC)
  4. Implementierungs-Verben (z.B. instanziieren, iterieren, casten)
  5. Konkrete Datenstrukturen (z.B. `Dict[str, List]`, Array von Objekten)
  6. Framework-/Library-Namen (z.B. React, FastAPI, Pydantic)
  7. Datei-/Pfad-/Klassennamen (z.B. `services/auth.py`, Klasse `AuthManager`)
- **Hard-Block mit Override:** Treffer → Write abgebrochen, Fundstellen mit **Zeile + Kategorie + lösungsneutralem Umformulierungs-Hinweis** gemeldet. Bewusstes Überstimmen möglich (echter Fachbegriff als Teil der Anforderung), **mit kurzer Begründung**
- Läuft als **Heuristik im Skill-Prompt** (kein externes Tool)

**Baustein B — „nie erfinden → `## Offene Punkte`"** in `dtb:feature-plan`
- Fehlende Information wird **nicht** plausibel gefüllt, sondern als **explizite Frage** in `## Offene Punkte` geparkt
- **Ersetzt** das heutige `[TODO: …]`-Muster (Schritt 6, Zeile 139 der SKILL.md) vollständig
- Abschnittsname **einheitlich deutsch** (`## Offene Punkte`, wie `feature-discover`)
- Keine Lücken → „— keine —", kein leerer Abschnitt

### Nicht enthalten
- `greenfield-prd`/`greenfield-roadmap` (read-only, kein Write) → Greenfield-Redesign separat (**Idee #11**)
- Eligibility-Gates / Redirect (ursprünglicher Baustein C) → eigenes Feature (**Idee #12**)
- `impl-plan`, `bug-report`, `task`, `feature-discover` als Lint-Ziele — nur `feature-plan` wird gehärtet
- Lint prüft ausschließlich **Spec-Text**, nicht Code (das macht `code-review`)
- Kein automatisches Umschreiben durch den Lint — er blockiert und meldet; korrigiert wird durch Mensch/Skill

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Fehlalarm: legitimer Fachbegriff/Vendor ist Teil der Anforderung (z.B. „Export nach SAP") wird blockiert | Hoch | Mittel | Override mit Begründung; Kategorien-Beispiele grenzen legitime Fachbegriffe ab |
| Heuristik übersieht Lecks oder meldet falsch (kein echter Parser) | Mittel | Niedrig | Bewusst als Prompt-Heuristik akzeptiert; keine 100%-Garantie, Netz nicht Mauer — plan-review fängt Rest |
| Skill-Aufblähung durch Kategorien + Beispiele (feature-plan heute ~184 Z.) | Mittel | Mittel | Kompakte Kategorien-Liste mit je 1 Beispiel; Lehre aus REVIEW_HAERTUNG; Zeilen-Budget als Success Criterion |
| Override wird zum Reflex → Lint wertlos | Niedrig | Mittel | Begründungspflicht beim Override; Sichtbarkeit in Spec (siehe Offene Punkte) |
| Zwei Open-Questions-Benennungen driften (`feature-discover` vs. `feature-plan`) | Niedrig | Niedrig | Einheitlich `## Offene Punkte` festgeschrieben |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — betrifft nur eine Skill-Datei, keine Vorarbeiten nötig

### Referenz-Dokumente
- `dtb-project/project-workflows/features/DISCOVERY_SPEC_HAERTUNG.md` - Discovery-Grundlage
- `skills/dtb-feature-plan/SKILL.md` - Ziel-Skill (Lint vor Write-Schritt 7, Open-Punkte ersetzt Schritt 6)
- `skills/dtb-feature-discover/SKILL.md` - Vorbild-Benennung `## Offene Punkte`
- `dtb-project/project-workflows/features/FEATURE_REVIEW_HAERTUNG.md` - Muster für „Skill-Härtung" + Aufblähungs-Lehre
- `skills/dtb-kit-sync/SKILL.md` - nach Umsetzung: geänderter feature-plan-Skill global synchronisieren

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `feature-plan` prüft vor dem Write auf die 7 Leck-Kategorien und bricht bei Treffer ab (Hard-Block)
- [x] Fund-Meldung nennt je Leck Anker (Sektion `## …` + Zitat, KEINE Zeilennummer — der Text ist beim Prüfen noch nicht gespeichert) + Kategorie + lösungsneutralen Umformulierungs-Hinweis
- [ ] Override mit Begründung ist möglich und dokumentiert dessen Verhalten
- [ ] `[TODO: …]`-Muster ist vollständig durch `## Offene Punkte` ersetzt (Schritt 6 der SKILL.md)
- [ ] `## Offene Punkte` verwendet dieselbe Benennung wie `feature-discover`; „— keine —" bei fehlenden Lücken
- [ ] `feature-plan` bleibt kompakt (Richtwert: keine Verdopplung, < ~280 Zeilen analog REVIEW_HAERTUNG)
- [ ] Abnahme an einem Fixture: eine Spec mit bewusst platzierten Lecks + Wissenslücken wird korrekt geblockt bzw. in Offene Punkte überführt
- [ ] Geänderter Skill via `dtb:kit-sync` global synchronisiert

---

## Offene Punkte

- Exakte Wortlaute/Beispiele je der 7 Kategorien in `impl-plan` final festlegen (inkl. Abgrenzung legitimer Fachbegriffe)
- Override-Sichtbarkeit: soll ein bewusstes Überstimmen in der erzeugten Spec markiert/dokumentiert werden, oder reicht die Begründung im Dialog?

---

**Erstellt mit:** `/dtb:feature-plan`
