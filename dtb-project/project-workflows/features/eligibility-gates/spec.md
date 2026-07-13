# Feature: Eligibility-Gates

**Erstellt:** 2026-07-10
**Ziel:** Schreibende Skills prüfen am Eingang, ob ihr kritisches Eingabe-Artefakt existiert, und verweigern bei Nichteignung konstruktiv mit Verweis auf den erzeugenden Skill.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- expliziter Zustand (ueberschreibt Ableitung), gesetzt 2026-07-10 nach Testbett-Verprobung pkp + Fixture 10/10 -->

---

## Executive Summary

Heute laufen Skills auch dann durch, wenn ihre fachliche Grundlage fehlt — `impl-plan` ohne
`spec.md`, `plan-review` ohne `plan.md` — und erzeugen Artefakte auf falscher Basis. Dieses Feature
stattet in **v1 die sechs Hard-Gate-Skills** mit einem Eingangs-Gate aus: ein deklarativer
Fit-Check aus dem vorhandenen `pipeline`-Frontmatter (existiert das kritische `consumes`-Artefakt?),
bei Nichteignung eine konstruktive Weigerung **mit Redirect** auf den Skill, der es erzeugt. Vorbild
ist die harte Test-zuerst-Weigerung von 10x-tdd. Git-Gates und Soft-Gates sind bewusst als
Folge-Feature ausgelagert (Blast-Radius klein halten, Prompt-Gate-Konzept erst am kleinsten
wertvollen Schnitt beweisen).

---

## Scope / Abgrenzung

### Enthalten (v1)

**Hard-Gate an sechs schreibenden Skills**
- Fit-Check der **explizit benannten kritischen Vorbedingung** je Skill (nicht positional-first)
- Bei Nichteignung: harte Weigerung mit Meldeblock (Muster wie `feature-discover` Schritt 1) statt
  stillem Abbruch oder Weiterarbeiten
- Der Meldeblock zeigt den **geprüften Pfad** und einen **bewussten Fortfahren-Weg** (Escape-Hatch
  gegen Fehlalarm)

**Redirect auf den erzeugenden Skill**
- Ableitung über **`produces`-Rückwärtssuche** (welcher Skill trägt das fehlende Artefakt in `produces`?)
- Bei **mehreren Erzeugern**: alle nennen, den `after`-Match als empfohlenes Erstziel voran
- Kein Erzeuger ableitbar → ehrliche Meldung ohne erfundenes Ziel

**Mechanik + Konvention einmal komplett**
- Referenztext (Fit-Check, Redirect inkl. Tie-Break, Meldeblock, Escape-Hatch) in `skills/CLAUDE.md`
- Korrigierte Einteilungsregel als Fixpunkt (siehe unten) — trägt auch die späteren Git-/Soft-Gates

**Abnahme + Verteilung**
- Fixture-Abnahme, **Vorlauf am realen Testbett `pkp`** (git-gestützt) und globaler `dtb:kit-sync` (Sync lief vor der Verprobung, da Gate-Skills global-shared)

### Nicht enthalten (Folge-Feature)
- **Git-Gates** (`code-review`, `build-check`) — eigene Mechanik (Git-Zustand statt Artefakt) + Nicht-Git-Fallback
- **Soft-Gates** (`feature-plan`, `feature-discover`, `idea-review`, `generate-rules`, `repo-sync`, `docs-extract`) inkl. Soft-Gate-Verhalten (Warnung vs. interaktive Rückfrage)
- **Argument-Check** als Gate-Quelle (untergräbt bestehende Ableitungs-Fallbacks)
- required/optional-Markierung im `consumes`-Schema
- `dtb-project-health`-Drift-Wächter, `dtb-pipeline-graph`-Gate-Visualisierung
- Keine Änderung der Pipeline-Struktur/-Semantik, keine neuen Skills

---

## Einteilungsregel (Fixpunkt, korrigiert nach Frontmatter-Verifikation)

> Ein Skill bekommt ein **Hard-Gate**, wenn er **eine zwingende Eingabe braucht** (ohne die sein
> Output sinnlos/falsch wäre). Das Kriterium ist NICHT „`produces` ≠ leer" (mehrere Skills schreiben
> nur, ohne `produces`-Artefakt) und NICHT die Position in `consumes` (die Reihenfolge ist kein
> verlässlicher Indikator). Das kritische Artefakt wird **pro Skill explizit** benannt.

**Verbindliche Hard-Gate-Zuordnung v1** (Frontmatter-verifiziert 2026-07-10):

| Skill | Kritische Vorbedingung | Redirect-Ziel |
|-------|------------------------|---------------|
| `impl-plan` | `features/*/spec.md` | `feature-plan` (eindeutig) |
| `plan-review` | `features/*/plan.md` | `impl-plan` **und** `feature-start` erzeugen `plan.md` → beide nennen, `after`-Match `impl-plan` voran |
| `feature-start` | `features/*/plan.md` | `impl-plan` (nach Selbst-Ausschluss eindeutig) |
| `debug-plan` | `features/*/bug.md` | `bug-report` (nach Selbst-Ausschluss eindeutig) |
| `archive` | archivierbare Kandidaten vorhanden | kein Redirect (`after: null`) → ehrliche Meldung (nativ vorhanden) |
| `migrate-change-folders` | flache Alt-Dateien (`features/*.md`) | kein Redirect (`after: null`) → ehrliche Meldung (nativ vorhanden) |

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Prompt-Gate greift unter Kontextdruck nicht zuverlässig (Anweisung, kein Code) | Mittel | Mittel | Kleinster Schnitt v1; Fixture-Abnahme + Testbett-Vorlauf vor globalem Rollout |
| Fehlalarm blockt legitime Arbeit projektübergreifend | Mittel | Hoch | **Escape-Hatch** (bewusster Fortfahren-Weg) + geprüfter Pfad im Meldeblock |
| Mehrdeutiger Redirect (`plan.md` von zwei Skills erzeugt) | Hoch (1 Fall) | Niedrig | Beide nennen, `after`-Match voran — keine fragile zweite Ableitungsregel |
| Gate-Logik in 6 Prompts dupliziert → Drift | Mittel | Mittel | Ein Referenztext in `skills/CLAUDE.md`, jeder Skill verweist darauf |
| Globaler Big-Bang-Rollback nur global | Niedrig | Hoch | Testbett-Vorlauf `pkp`; `kit-sync` lock-basiert + per `git revert` reversibel |
| Gate feuert fälschlich bei Resume-Läufen (`feature-discover`-Marker etc.) | Niedrig | Mittel | Abnahme prüft Resume-Marker-Interaktion explizit |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine harten Vorbedingungen — `frontmatter-pfad-hygiene` (Listen-Format `after`/`next`) ist umgesetzt und Grundlage der Redirect-Ableitung

### Referenz-Dokumente
- `features/eligibility-gates/discovery.md` - Discovery-Ergebnisse
- `features/eligibility-gates/plan.md` - Implementierungsplan (Frontmatter-Verifikation Fund A–D)
- `features/spec-haertung/spec.md` - Herkunft (Baustein C hierher abgetrennt)
- `features/frontmatter-pfad-hygiene/spec.md` - Listen-Format `after`/`next`
- `skills/CLAUDE.md` - Frontmatter-/Pipeline-Konventionen, Ziel der Doku-Ergänzung

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Hard-Gate-Skill mit fehlendem kritischem Artefakt verweigert die Ausführung und nennt den korrekten Redirect-Skill (via `produces`-Rückwärtssuche)
- [ ] Bei mehrdeutigem Redirect (`plan-review` ohne `plan.md`) werden beide Erzeuger genannt, `impl-plan` (`after`-Match) voran
- [ ] Der Meldeblock zeigt den geprüften Pfad; ein bewusster Fortfahren-Weg (Escape-Hatch) existiert
- [ ] Ein Resume-Lauf wird nicht fälschlich gegated
- [ ] Einteilungsregel + Konvention + Zuordnung stehen in `skills/CLAUDE.md`
- [ ] Gates am Testbett `pkp` verprobt (Happy-Path + real ausgeführter Block-Pfad), per `dtb:kit-sync` global verteilt

---

## Offene Punkte

- Genauer Wortlaut/Format des Meldeblocks inkl. Escape-Hatch — in `impl-plan`/Umsetzung konkretisieren.
- Form der Escape-Hatch (explizites `--force`-Argument vs. Bestätigungs-Rückfrage) — bei Schritt 2.1 festlegen.
- Folge-Feature Git-/Soft-Gates: erst nach Praxiserprobung der Hard-Gates aufsetzen.

---

**Erstellt mit:** `/dtb:feature-plan`
