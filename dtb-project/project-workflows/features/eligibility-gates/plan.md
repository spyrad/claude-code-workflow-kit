# Implementierungsplan: Eligibility-Gates

**Erstellt:** 2026-07-10
**Feature-Spec:** `features/eligibility-gates/spec.md`
**Geschaetzte Dauer:** ~5-7 h (6 Hard-Gates, verteilt über mehrere 3x3-Blöcke)
**Status:** Reviewed

---

## Scope v1 (nach plan-review 2026-07-10)

**Nur Hard-Gates** (Entscheidung A). Git-Gates (`code-review`, `build-check`) und Soft-Gates
(`feature-plan`, `feature-discover`, `idea-review`, `generate-rules`, `repo-sync`, `docs-extract`)
sind Folge-Feature. Spec ist auf diesen Scope nachgezogen.

## Frontmatter-Verifikation (Prior: L1/L2 — reale `consumes`/`produces` geprüft)

Vier Spec-Annahmen widerlegt und in der Spec korrigiert:
- **A** „erstes `consumes` = kritisch" unzuverlässig (`feature-start` führt `BACKLOG.md` zuerst) →
  kritisches Artefakt **explizit pro Skill**.
- **B** `produces: []` ≠ „kein Gate" → Kriterium „braucht zwingende Eingabe".
- **C** `feature-plan` braucht `discovery.md` nicht hart (eigener Text: „optional") → Soft-Gate → Folge-Feature.
- **D** `docs-extract` hat `consumes: []` → Soft-Gate-Sonderfall → Folge-Feature.
- **E** (Umsetzung 2.5/2.6) `archive` ist ein **Scanner**, kein Argument-Skill (Plan-Annahme „Ziel-Ordner
  aus Argument" widerlegt) — kritisch = archivierbare Kandidaten; `archive` (Schritt 3) und `migrate`
  (Schritt 1) haben ihren Gate **bereits nativ** (`after: null` → ehrliche Meldung, kein Redirect).
  Nur Konventions-Querverweis ergänzt, keine neue Logik.

## Review-Entscheidungen (eingearbeitet)

- **B Tie-Break:** mehrdeutiger Redirect → beide Erzeuger nennen, `after`-Match voran (betrifft nur `plan-review`)
- **D Escape-Hatch:** Meldeblock zeigt geprüften Pfad + bewussten Fortfahren-Weg
- **E Testbett:** realer Vorlauf am Testbett vor globalem `kit-sync` — final **`pkp`** (git-gestützt) statt
  `dtb-assistant`. Reihenfolge in der Praxis **getauscht**: globaler `kit-sync` (3.4) lief VOR der Verprobung
  (3.3), da die Gate-Skills global-shared sind und der Sync vor dem Dogfooding aktiv sein muss.

---

## Verbindliche Hard-Gate-Zuordnung

| Skill | Kritische Vorbedingung | Redirect-Ziel (verifiziert) |
|-------|------------------------|------------------------------|
| `impl-plan` | `features/*/spec.md` | `feature-plan` (eindeutig) |
| `plan-review` | `features/*/plan.md` | `impl-plan` + `feature-start` → beide, `impl-plan` voran |
| `feature-start` | `features/*/plan.md` | `impl-plan` (Selbst-Ausschluss) |
| `debug-plan` | `features/*/bug.md` | `bug-report` (Selbst-Ausschluss) |
| `archive` | archivierbare Kandidaten vorhanden (Scanner, kein Argument) | kein Redirect (`after: null`) → ehrliche Meldung — **nativ in Schritt 3** |
| `migrate-change-folders` | flache Alt-Dateien (`features/*.md`) | kein Redirect (`after: null`) → ehrliche Meldung — **nativ in Schritt 1** |

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Mechanik & Konvention festlegen + dokumentieren | ~1.5 h | Geplant |
| Phase 2 | 6 Hard-Gates umsetzen | ~2.5 h | Geplant |
| Phase 3 | Abnahme (Fixtures + Testbett) + globale Verteilung | ~2 h | Geplant |

---

## Phase 1: Mechanik & Konvention festlegen

### Ziel
Gate-Mechanik + Einteilungsregel einmal präzise definieren, damit die Skill-Edits schematisch sind.

### Schritte

#### Schritt 1.1: Gate-Mechanik als Referenztext spezifizieren
- **Zweck:** Fit-Check + Redirect + Meldeblock + Escape-Hatch an einer Stelle festnageln
- **Dateien:** `skills/CLAUDE.md` (neuer Abschnitt „Eligibility-Gates")
- **Output:** (1) Fit-Check der kritischen Vorbedingung; (2) Redirect = `produces`-Rückwärtssuche,
  bei Mehrdeutigkeit beide nennen mit `after`-Match voran, sonst ehrliche Meldung; (3)
  Meldeblock-Wortlaut **inkl. geprüftem Pfad**; (4) **Escape-Hatch** (bewusster Fortfahren-Weg);
  Form (`--force`-Argument vs. Bestätigung) hier festlegen

#### Schritt 1.2: Einteilungsregel (korrigiert) + Zuordnung festschreiben
- **Zweck:** Fund A/B in die Regel gießen (Kriterium „braucht zwingende Eingabe", kritisches Artefakt explizit)
- **Dateien:** `skills/CLAUDE.md`
- **Output:** Regeltext + Hard-Gate-Zuordnungstabelle; Notiz „Git-/Soft-Gates Folge-Feature"

#### Schritt 1.3: Redirect-`produces`-Index verifizieren
- **Zweck:** je fehlendem kritischem Artefakt die Erzeuger per Grep belegen (nicht annehmen)
- **Dateien:** keine (Analyse per Grep über alle `produces`)
- **Output:** bestätigte Redirect-Ziele; `plan.md`-Mehrdeutigkeit (`impl-plan`+`feature-start`) belegt

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/CLAUDE.md` enthält Gate-Mechanik (inkl. Tie-Break + Escape-Hatch) + Einteilungsregel + Zuordnung

### Checkpoint-Kriterien
- [ ] Redirect-Ziel jedes Hard-Gate-Skills per `produces`-Grep belegt (nicht angenommen)

---

## Phase 2: 6 Hard-Gates umsetzen

### Ziel
Jeder der sechs Skills erhält einen Eingangs-Schritt (harte Weigerung + Redirect + Escape-Hatch).

### Schritte

#### Schritt 2.1: `impl-plan` Gate (spec.md) — Referenz-Umsetzung inkl. Escape-Hatch-Form
- **Dateien:** `skills/dtb-impl-plan/SKILL.md` (bestehende Spec-Fehlermeldung zum Gate ausbauen)
- **Output:** fehlt `features/{slug}/spec.md` → Weigerung + Redirect `feature-plan` + Pfad + Escape-Hatch

#### Schritt 2.2: `plan-review` Gate (plan.md) — mehrdeutiger Redirect
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Output:** fehlt `plan.md` → Weigerung + „erzeugt von `impl-plan` oder `feature-start`", `impl-plan` voran

#### Schritt 2.3: `feature-start` Gate (plan.md)
- **Dateien:** `skills/dtb-feature-start/SKILL.md`
- **Output:** fehlt `plan.md` (NICHT das erste consumes `BACKLOG.md`, Fund A) → Weigerung + Redirect `impl-plan`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: `debug-plan` Gate (bug.md)
- **Dateien:** `skills/dtb-debug-plan/SKILL.md`
- **Output:** fehlt `features/{slug}/bug.md` → Weigerung + Redirect `bug-report`

#### Schritt 2.5: `archive` Gate (Ziel-Ordner)
- **Dateien:** `skills/dtb-archive/SKILL.md`
- **Output:** Ziel-Slug fehlt/Ordner nicht vorhanden → Weigerung + Hinweis Slug angeben

#### Schritt 2.6: `migrate-change-folders` Gate (flache Alt-Dateien)
- **Dateien:** `skills/dtb-migrate-change-folders/SKILL.md`
- **Output:** keine `features/*.md` (flach) → ehrliche Meldung „nichts zu migrieren"

> **3x3-Block:** Nach Schritt 2.6 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 6 Hard-Gate-Skills mit Eingangs-Gate, korrektem Redirect, Pfad-Ausgabe und Escape-Hatch

### Checkpoint-Kriterien
- [ ] Jeder Gate prüft das in der Tabelle benannte kritische Artefakt (nicht positional-first)

---

## Phase 3: Abnahme + Verteilung

### Ziel
Success Criteria fixture-basiert verifizieren, am realen Testbett verproben, dann global verteilen.

> **Praxis-Reihenfolge (2026-07-10):** 3.4 (globale Verteilung) lief VOR 3.3 (Testbett-Verprobung) —
> die Gate-Skills sind global-shared, der `kit-sync` muss vor dem Dogfooding aktiv sein. Nummerierung
> hier belassen (N.M-Referenzen stabil); die Progress-Belege sind entsprechend datiert.

### Schritte

#### Schritt 3.1: Fixture-Abnahme (unabhängiger Agent)
- **Zweck:** Success Criteria der Spec prüfen
- **Dateien:** Fixtures im Scratchpad
- **Output:** Report PASS/FAIL je Kriterium; Fixtures decken ab: (a) kritisches Artefakt fehlt →
  blockt; (b) vorhanden → läuft; (c) **mehrdeutiger Redirect** (`plan-review` ohne `plan.md`) →
  beide genannt, `impl-plan` voran; (d) **Escape-Hatch** greift; (e) **Resume-Marker**
  (`feature-discover`) wird nicht fälschlich gegated

#### Schritt 3.2: Nachschärfung aus Abnahme
- **Dateien:** betroffene SKILL.md / `skills/CLAUDE.md`
- **Output:** gemeldete Mehrdeutigkeiten eingearbeitet

> **3x3-Block:** Nach Schritt 3.2 → Zusammenfassung + Feedback einholen

#### Schritt 3.3: Testbett-Vorlauf `pkp`
- **Zweck:** reale Slug-/Pfad-Situationen prüfen vor/nach globalem Rollout (Entscheidung E)
- **Dateien:** Zielprojekt `pkp` (git-gestützt, `features/` leer → keine `/dtb:migrate-change-folders` nötig)
- **Output:** Hard-Gates an echten Change-Ordnern verprobt (Happy-Path + Block-Pfad); Findings zurück in 3.2 falls nötig

#### Schritt 3.4: Globale Verteilung
- **Zweck:** geänderte Klasse-A-Skills global aktiv
- **Dateien:** `~/.claude/` via `dtb:kit-sync` (check → sync), Lock aktualisiert
- **Output:** Lock-Eintrag mit neuem Ref/Hash je geändertem Skill

### Deliverables
- [ ] Abnahme-Report; Testbett-Verprobung; global verteilte Skills

### Checkpoint-Kriterien
- [ ] Alle Spec-Success-Criteria PASS; Testbett-Vorlauf ohne offene Findings; Lock aktualisiert

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Kritisches Artefakt bestimmen | positional-first / explizit pro Skill | **explizit pro Skill** | Fund A |
| Einteilungs-Kriterium | `produces` ≠ leer / braucht zwingende Eingabe | **zwingende Eingabe** | Fund B |
| Scope v1 | alle 14 / nur Hard-Gates | **nur Hard-Gates** | Entscheidung A (Blast-Radius) |
| Tie-Break mehrdeutiger Redirect | Kontext-nächster / beide nennen | **beide, `after`-Match voran** | Entscheidung B |
| Fehlalarm-Schutz | ohne / Escape-Hatch | **Escape-Hatch + Pfad** | Entscheidung D |
| Rollout | direkt global / Testbett-Vorlauf | **Testbett `pkp`** (final; `dtb-assistant` verworfen — kein Git) | Entscheidung E |
| Escape-Hatch-Form | `--force`-Argument / Bestätigung | **Bestätigungs-Rückfrage** | konsistent mit interaktivem Skill-Stil, kein neues Argument-Schema (Schritt 2.1) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg.

- [x] 1.1 Gate-Mechanik-Referenztext (inkl. Tie-Break + Escape-Hatch) — `a4ee4ad`
- [x] 1.2 Einteilungsregel + Zuordnung — `a4ee4ad`
- [x] 1.3 Redirect-produces-Index verifizieren — `a4ee4ad`
- [x] 2.1 impl-plan Gate — `5772553`
- [x] 2.2 plan-review Gate (mehrdeutiger Redirect) — `5772553`
- [x] 2.3 feature-start Gate — `5772553`
- [x] 2.4 debug-plan Gate — `c6e8fca`
- [x] 2.5 archive Gate — `c6e8fca`
- [x] 2.6 migrate-change-folders Gate — `c6e8fca`
- [x] 3.1 Fixture-Abnahme — `6efe843` (PASS 10/10)
- [x] 3.2 Nachschärfung — `6efe843`
- [x] 3.3 Testbett-Verprobung — pkp Happy-Path real (`simulationsmaske-grunddaten`) + Block-Pfad **real ausgeführt** (blinde Agenten 2026-07-13: `impl-plan`/`plan-review` blocken bei fehlendem spec.md/plan.md mit korrektem Redirect inkl. mehrdeutigem Fall; 2 Positiv-Kontrollen ohne Fehlalarm); Fixture 10/10
- [x] 3.4 Globale Verteilung — kit-sync, Lock `8c1c906` (Reihenfolge getauscht: lief vor 3.3, s. Phase-3-Notiz)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `features/eligibility-gates/plan.md` laden; der erste nicht abgehakte Schritt
ist der naechste. Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
