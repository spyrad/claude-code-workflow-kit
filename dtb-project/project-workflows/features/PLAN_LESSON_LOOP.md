# Implementierungsplan: Lesson Loop

**Erstellt:** 2026-07-08
**Feature-Spec:** `features/FEATURE_LESSON_LOOP.md`
**Geschätzte Dauer:** ~1-2 Sessions (3 Phasen, 15 Schritte)
**Status:** Reviewed

---

## Phasen-Übersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill `dtb:lesson` + `lessons.md`-Format (Fundament) | ~S | Geplant |
| Phase 2 | Prior-Verdrahtung in 4 Konsumenten + Vorschlager + Globber-Audit | ~M | Geplant |
| Phase 3 | Ablösung pitfalls.md, Doku, kit-sync, Abnahme | ~M | Geplant |

---

## Phase 1: Skill `dtb:lesson` + `lessons.md`-Format

### Ziel
Der neue Skill kann eine Freitext-Lektion strukturiert und append-only in `dtb-project/project-rules/lessons.md` erfassen — inklusive Format-Definition, Applies-to-Handling und Randfällen.

### Schritte

#### Schritt 1.1: `lessons.md`-Format definieren
- **Zweck:** Verbindliche Struktur, bevor Erfasser/Konsumenten sie nutzen
- **Dateien:** (Referenz-Definition im späteren `skills/dtb-lesson/SKILL.md`; keine eigene Datei)
- **Input:** Discovery (4 Felder Context/Problem/Rule/Applies-to), MEMORY.md-Größenregel als Vorbild
- **Output:** Festes Eintragsformat (Tabelle oder Block je Eintrag), Header mit Format-Erklärung, `Applies-to`-Enum (`impl-plan`, `debug-plan`, `plan-review`, `code-review`, `alle`), Soft-Limit-Hinweis ~150 Zeilen

#### Schritt 1.2: Skill `dtb:lesson` erstellen (Capture-Flow)
- **Zweck:** Kern des Features — schnelles Erfassen wie `dtb:idea`
- **Dateien:** `skills/dtb-lesson/SKILL.md` (neu)
- **Input:** Frontmatter-Konvention (skills/CLAUDE.md), `dtb:idea` als UX-Vorbild
- **Output:** Frontmatter (`name: dtb:lesson`, `stage: development`, `produces: [lessons.md]`, `allowed-tools: Read, Write, Grep`); Flow: Freitext → 4 Felder ableiten → Applies-to bestimmen → append-only Write → Datei bei Bedarf anlegen

#### Schritt 1.3: Duplikat-Check + Randfälle in `dtb:lesson`
- **Zweck:** append-only Datei kuratiert halten
- **Dateien:** `skills/dtb-lesson/SKILL.md`
- **Input:** Randfälle aus Feature-Spec
- **Output:** grep nach ähnlichem Rule-Text (Hinweis statt Block), Applies-to-Default-Regel (leer → `alle`), Größen-Soft-Warnung ab ~150 Zeilen

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-lesson/SKILL.md` funktionsfähig (erfasst append-only)
- [ ] Format + Applies-to-Enum + Größenregel dokumentiert

### Checkpoint-Kriterien
- [ ] Ein manueller Testaufruf erzeugt einen korrekt strukturierten Eintrag; Datei wird bei Fehlen angelegt

---

## Phase 2: Prior-Verdrahtung + Vorschlager-Rolle

### Ziel
Die vier Konsumenten lesen `lessons.md` als Prior (einheitlicher Baustein), die drei produzierenden schlagen Lektion-Kandidaten vor.

### Schritte

#### Schritt 2.1: Wiederverwendbaren Prior-Lese-Baustein formulieren
- **Zweck:** Konsistenz über alle vier Skills (Risiko „Inkonsistenz" mitigieren)
- **Dateien:** (Textbaustein, wird in 2.2–2.5 identisch eingesetzt)
- **Input:** Read-Mechanismus „ganze Datei + Applies-to-Filter"
- **Output:** Einheitlicher Block: `lessons.md` lesen → nach `Applies-to` (Skill-Name oder `alle`) filtern → Regeln still anwenden → kompakter Hinweis „📚 X Lektionen berücksichtigt" → fehlend/leer = still überspringen → Widerspruch = beide zeigen + melden (nicht auflösen). Plus Vorschlager-Baustein: „💡 Lektion-Kandidat: … übernehmen? (`/dtb:lesson` oder ja/nein)"
- **Konflikt-Definition (mechanisch):** Zwei Lektionen gelten als widersprüchlich, wenn sie **überlappendes `Applies-to`** haben UND ihre `Rule`-Aussagen gegensätzlich sind (z.B. „immer X" vs. „nie X" zum selben Gegenstand). Nur dann greift „beide zeigen + melden"; ansonsten alle passenden Lektionen kumulativ anwenden

#### Schritt 2.2: `impl-plan` verdrahten
- **Zweck:** Prior + Vorschlager im Planungs-Skill
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`
- **Input:** Baustein aus 2.1
- **Output:** Prior-Lese-Schritt (nach Config-Laden, vor Analyse) + Vorschlager-Hinweis + Frontmatter `consumes` um `lessons.md` ergänzt

#### Schritt 2.3: `debug-plan` verdrahten
- **Zweck:** Prior + Vorschlager im Debug-Skill
- **Dateien:** `skills/dtb-debug-plan/SKILL.md`
- **Input:** Baustein aus 2.1
- **Output:** Prior-Lese-Schritt (vor Hypothesen) + Vorschlager-Hinweis + Frontmatter `consumes`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: `code-review` verdrahten (mit Rules-Abgrenzung)
- **Zweck:** Prior + Vorschlager; `lessons.md` NICHT als Coding-Rule behandeln
- **Dateien:** `skills/dtb-code-review/SKILL.md`
- **Input:** Baustein aus 2.1; bestehende „Rules laden"-Logik (Schritt 2, `project-rules/*.md`)
- **Output:** `lessons.md` aus dem generischen `project-rules/*.md`-Rules-Glob ausschließen + separater Prior-Schritt; Vorschlager-Hinweis; Frontmatter `consumes` präzisieren

#### Schritt 2.5: `plan-review` verdrahten (nur Leser)
- **Zweck:** Agenten ziehen Lektionen als Prior heran (kein Vorschlager)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Baustein aus 2.1
- **Output:** Prior-Lese-Schritt (nach Agent-Definitionen laden); Agenten berücksichtigen relevante Lektionen in der Diskussion; Frontmatter `consumes` um `lessons.md`

#### Schritt 2.6: Konsistenz-Check der vier Verdrahtungen
- **Zweck:** Identischer Wortlaut/Verhalten sicherstellen
- **Dateien:** alle vier Konsumenten-Skills
- **Input:** 2.2–2.5
- **Output:** Verifiziert: gleicher Baustein-Text, gleiche Hinweis-Formulierung, Vorschlager nur in den 3 produzierenden

> **3x3-Block:** Nach Schritt 2.6 → Zusammenfassung + Feedback einholen

#### Schritt 2.7: project-rules/-Globber-Audit (alle Skills)
- **Zweck:** `lessons.md` liegt in `project-rules/` — verhindern, dass *irgendein* Skill es fälschlich als Coding-Rule/Kit-Seed behandelt (Kollision mit „nur DERIVED_STATE_RULES.md ist dort versioniert")
- **Dateien:** `skills/dtb-project-health/SKILL.md`, `skills/dtb-generate-rules/SKILL.md`, `skills/dtb-kit-sync/SKILL.md` (+ ggf. weitere `project-rules/*.md`-Leser)
- **Input:** grep über alle Skills nach `project-rules/*.md` / `project-rules/` Globbing
- **Output:** Jeder gefundene Globber schließt `lessons.md` aus bzw. behandelt es korrekt (nicht als Rule, nicht als Seed); Ergebnis dokumentiert (welche Skills betroffen, welche Anpassung)

### Deliverables
- [ ] 4 Konsumenten lesen `lessons.md` als Prior (einheitlich)
- [ ] 3 produzierende Skills schlagen Lektion-Kandidaten vor
- [ ] Frontmatter `consumes` in allen vier gesetzt
- [ ] Kein `project-rules/`-Globber behandelt `lessons.md` falsch

### Checkpoint-Kriterien
- [ ] Baustein-Text in allen vier Skills identisch; code-review-Abgrenzung greift
- [ ] Globber-Audit abgeschlossen, keine Fehlbehandlung von `lessons.md`

---

## Phase 3: Ablösung, Doku, Frontmatter, Abnahme

### Ziel
Totes `pitfalls.md`-Konzept ablösen, Doku/Graph aktualisieren, Feature abnehmen.

### Schritte

#### Schritt 3.1: `pitfalls.md` als abgelöst markieren
- **Zweck:** Konzept sauber überführen ohne Datenverlust
- **Dateien:** `frameworks/claude-code-memory-framework/templates/pitfalls.md`
- **Input:** —
- **Output:** Header-Hinweis „→ ersetzt durch `dtb:lesson` / `lessons.md`"; Datei bleibt erhalten (Drittanbieter-Framework)

#### Schritt 3.2: Doku aktualisieren (CLAUDE.md, README.md)
- **Zweck:** Skill auffindbar/dokumentiert
- **Dateien:** `CLAUDE.md` (Root), `README.md`
- **Input:** —
- **Output:** `dtb:lesson` unter „Knowledge management" + Output-Location `lessons.md` in CLAUDE.md; Skill-Liste in README.md ergänzt

#### Schritt 3.3: Pipeline-Graph regenerieren
- **Zweck:** Neuer Skill + `consumes`/`produces`-Kanten sichtbar
- **Dateien:** Output von `dtb:pipeline-graph`
- **Input:** aktualisierte Frontmatter aller betroffenen Skills
- **Output:** regenerierter Graph (Skill-Zahl +1, lessons.md-Kanten)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Geänderte Klasse-A-Artefakte via kit-sync abgleichen
- **Zweck:** Neuer Skill `dtb:lesson` + 4 geänderte Konsumenten + 3 geänderte Globber sind Klasse-A-Artefakte → installierte Kopien unter `~/.claude/` driften sonst sofort nach Merge
- **Dateien:** `~/.claude/dtb-lock.json`, installierte Skill-Kopien (via `/dtb:kit-sync`)
- **Input:** gemergter Repo-Stand
- **Output:** `/dtb:kit-sync check` → `sync`: neuer Skill installiert, geänderte Skills aktualisiert, Lock auf neuen Ref; kein stiller Skip außer bewusst gepinnten

#### Schritt 3.5: Fixture-/Praxis-Abnahme (isoliert)
- **Zweck:** Success Criteria verifizieren, ohne das echte `project-rules/lessons.md` zu verschmutzen
- **Dateien:** **isoliertes Fixture-Verzeichnis** (Muster KIT_SYNC, temporär) + betroffene Skills
- **Input:** alle vorherigen Schritte
- **Output:** Unabhängiger Agent testet in Isolation den Zyklus erfassen → konsumieren; explizite Testfälle: (a) **fehlende** `lessons.md`, (b) **leere** Datei, (c) Duplikat, (d) Konflikt (überlappendes Applies-to + gegensätzliche Rule), (e) Applies-to-Filter greift pro Skill; Ergebnis-Protokoll; Feature-Abnahme

### Deliverables
- [ ] pitfalls.md abgelöst, Doku + Graph aktuell
- [ ] Klasse-A-Artefakte via kit-sync installiert/aktualisiert (Lock auf neuen Ref)
- [ ] Abnahme-Protokoll (alle 7 Success Criteria, isoliert getestet)

### Checkpoint-Kriterien
- [ ] Voller Zyklus erfassen → konsumieren bestanden (isoliert); alle Success Criteria erfüllt
- [ ] kit-sync-Abgleich sauber (kein ungewollter Drift)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begründung |
|-------|----------|-------------|-------------|
| Speicherort `lessons.md` | project-rules / project-workflows / config | **project-rules/lessons.md** | In Discovery gewählt; Lektion = gepflegte Regel-Quelle |
| Read-Mechanismus | ganze Datei+Filter / grep / Frontmatter | **ganze Datei + Applies-to-Filter** | Discovery; einfach solange Datei klein |
| Distribution | Seed / Laufzeit | **Laufzeit-Artefakt** | Discovery; projektspezifischer Inhalt wie INBOX.md |
| Applies-to-Default bei leer | Rückfrage / `alle` | **`alle`** | Kein Reibungsverlust beim Erfassen; Nutzer kann eingrenzen |
| Größenlimit-Härte | hart / soft | **Soft-Warnung ab ~150 Zeilen** | Analog MEMORY.md; append-only nie hart blocken |
| `project-rules/*.md`-Globber (code-review u.a.) | ignorieren / ausschließen | **`lessons.md` in ALLEN Globbern ausschließen + separater Prior** (Audit in 2.7) | Sonst würde Lesson doppelt/als Coding-Rule/Seed behandelt |
| Vorschlager-Umfang | alle 4 / nur produzierende | **nur impl-plan, debug-plan, code-review** | plan-review ist reiner Review-Kontext, produziert nichts |

---

## Progress

> Single Source of Truth für den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg.

- [x] 1.1 lessons.md-Format definieren
- [x] 1.2 Skill dtb:lesson erstellen (Capture)
- [x] 1.3 Duplikat-Check + Randfälle
- [x] 2.1 Prior-Lese-Baustein formulieren
- [x] 2.2 impl-plan verdrahten
- [x] 2.3 debug-plan verdrahten
- [x] 2.4 code-review verdrahten (Rules-Abgrenzung)
- [x] 2.5 plan-review verdrahten (nur Leser)
- [x] 2.6 Konsistenz-Check der vier Verdrahtungen
- [x] 2.7 project-rules/-Globber-Audit (alle Skills)
- [x] 3.1 pitfalls.md ablösen
- [x] 3.2 Doku (CLAUDE.md, README.md)
- [x] 3.3 Pipeline-Graph regenerieren
- [ ] 3.4 Klasse-A-Artefakte via kit-sync abgleichen
- [ ] 3.5 Fixture-/Praxis-Abnahme (isoliert)

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist für die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die nächsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_LESSON_LOOP.md` laden; der erste nicht abgehakte Schritt ist der nächste.
Erkenntnisse/Abweichungen gehören in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
