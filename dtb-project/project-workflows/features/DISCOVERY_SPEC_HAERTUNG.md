# Discovery: SPEC_HAERTUNG

**Erstellt:** 2026-07-09
**Idee-Referenz:** Inbox #5 — "Skill-Robustheit: Technical-Leak-Lint in feature-plan/greenfield-prd (7 Kategorien) + „nie erfinden → ## Open Questions" + Eligibility-Gates mit Redirect (Vorbild: 10x-prd/10x-tdd)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-feature-plan/SKILL.md` | **Primär** — bekommt Technical-Leak-Lint (Baustein A) vor dem Write und ersetzt `[TODO: …]` durch `## Offene Punkte` (Baustein B) |
| `skills/dtb-feature-discover/SKILL.md` | Referenz/Vorbild — liefert die Benennung `## Offene Punkte`; wird NICHT umgebaut |

---

## Anforderungen

### Scope

**Enthalten:**
- **Baustein A — Technical-Leak-Lint** in `feature-plan`: prüft den Spec-Text vor dem Schreiben auf technische Lecks in **7 Kategorien** (1 Vendor-/Produktnamen, 2 ORM-/Query-Notation, 3 Transport/Protokoll, 4 Implementierungs-Verben, 5 konkrete Datenstrukturen, 6 Framework-/Library-Namen, 7 Datei-/Pfad-/Klassennamen). Treffer → **Hard-Block mit Override** (Write abgebrochen, Fundstellen mit Zeile + Kategorie gemeldet; bewusstes Überstimmen mit kurzer Begründung möglich)
- **Baustein B — „nie erfinden → `## Offene Punkte`"** in `feature-plan`: fehlende Information wird NICHT plausibel gefüllt, sondern als explizite Frage in `## Offene Punkte` geparkt. **Ersetzt** das heutige `[TODO: …]`-Muster vollständig; Abschnittsname **einheitlich deutsch** wie in `feature-discover`

**Nicht enthalten:**
- `greenfield-prd`/`greenfield-roadmap` — read-only, kein Write zum Abbrechen → Greenfield-Redesign separat (**Idee #11**)
- **Eligibility-Gates / Redirect** (ursprünglicher Baustein C) → eigenes Feature (**Idee #12**), großer Blast-Radius
- `impl-plan`, `bug-report`, `task` — bewusst außen vor (impl-plan enthält legitim technische Details); engster, sicherster Scope = nur `feature-plan`
- Lint prüft nur **Spec-Text**, nicht Code (das macht `code-review`)
- Kein automatisches Umschreiben durch den Lint — er blockiert und meldet, korrigiert wird durch Mensch/Skill

### Gewünschtes Verhalten
- Der Lint läuft als **Heuristik im Skill-Prompt** (kein externes Tool) unmittelbar vor dem Write-Schritt
- Bei Lecks: klare Meldung `❌ Technical-Leak-Lint: N Lecks, Write abgebrochen` mit Zeile + Kategorie + lösungsneutraler Umformulierungs-Hinweis pro Fund
- Override bewusst möglich (echter Fachbegriff/Vendor als Teil der Anforderung, z.B. „Export nach SAP") — mit kurzer Begründung
- `## Offene Punkte` als echte Fragen formuliert, gebündelt am Spec-Ende; bei keinen Lücken „— keine —"

### Randfälle
- **Fehlalarm** (legitimer Fachbegriff): über Override bewusst behaltbar; Begründung erwünscht, damit Override nicht zum Reflex wird
- **Keine Lücken:** `## Offene Punkte` = „— keine —", kein leerer Abschnitt
- **Override-Missbrauch** (alles wird überstimmt → Lint wertlos): offen, ob Override sichtbar/protokolliert bleibt (in Spec zu entscheiden)

### Einschränkungen
- **Kein echter Parser:** Heuristik im Prompt (`feature-plan` hat nur `Read, Write, Glob, Grep`, kein Bash) → Fehlalarme und übersehene Lecks möglich, keine 100%-Garantie
- **Aufblähungs-Risiko:** Kategorien + Beispiele dürfen `feature-plan` (heute ~184 Zeilen) nicht überladen — Lehre aus REVIEW_HAERTUNG: Skill kompakt halten
- Keine neue Dependency, keine Tool-Änderung nötig

### Integrationspunkte
- `feature-discover` liefert die Benennung `## Offene Punkte` (Angleichung) — Vorbild, kein Umbau
- `plan-review` könnte offene Punkte perspektivisch als Review-Input aufgreifen — Notiz, nicht Teil von #5
- Unberührt: BACKLOG, `workflow-checkpoint`, `impl-plan`

---

## Abhängigkeiten

- Bestehende Features: 1 (`FEATURE_REVIEW_HAERTUNG.md`)
- Konflikte/Überschneidungen: **keine** — REVIEW_HAERTUNG härtet `plan-review`/`code-review`, SPEC_HAERTUNG härtet `feature-plan` (disjunkte Ziel-Dateien; nur thematisch verwandt)

---

## Offene Punkte

- Exakte Wortlaute/Beispiele je der 7 Kategorien final in der Feature-Spec festlegen (inkl. Abgrenzung legitimer Fachbegriffe)
- Override-Sichtbarkeit: soll ein bewusstes Überstimmen in der Spec dokumentiert/markiert werden?

---

**Erstellt mit:** `/dtb:feature-discover`
