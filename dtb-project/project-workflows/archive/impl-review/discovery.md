# Discovery: impl-review
<!-- resume: done -->

**Erstellt:** 2026-07-15
**Idee-Referenz:** Inbox #20 — "`dtb:impl-review` nach 10x-Vorbild (`10x-impl-review`) statt `dtb:code-review`: EIN Review-Skill mit drei Dimensionen — Plan-Drift mechanisch, Craft-Urteil, Rules-Konformität; danach `dtb:code-review` aus dem Workflow entfernen"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-impl-review/SKILL.md | **Neu** — der Ziel-Skill (3 Sub-Agents, 6 Verdikt-Achsen, Triage, review.md) |
| skills/dtb-code-review/SKILL.md | **Entfernt** — Rules-Logik faltet als Dimension 3 ein; kit-sync „verwaist"-Pfad deckt die Entfernung in installierten Kopien |
| skills/dtb-implement/SKILL.md | `next:` im Frontmatter + 2 Textstellen (Ritual Punkt 11, Schritt 5 Punkt 2) auf `impl-review` umbiegen |
| skills/dtb-workflow-checkpoint/SKILL.md | Handoff schreibt bei „Fertig zum Testen" ohne Review `/dtb:impl-review` als Naechster Befehl |
| skills/dtb-pipeline-graph/SKILL.md | Pipeline-Referenz `code-review` → `impl-review` |
| skills/dtb-workflow-status/SKILL.md | Pipeline-Referenz `code-review` → `impl-review` |
| skills/dtb-lesson/SKILL.md | `Applies-to`-Vokabular: neuer Wert `impl-review` statt `code-review` (Schreib-Seite); 3 Textstellen |
| skills/dtb-generate-rules/SKILL.md | 2 Verweise „code-review nutzt diese Rules" → `impl-review` |
| CLAUDE.md (Kit-Root) | 5 Verweise (Workflow-Beschreibung, Skill-Kategorien, lessons-Prior-Liste) |
| skills/CLAUDE.md | Eligibility-Gate-Tabelle: Eintrag `impl-review` (kritisches Artefakt `features/*/plan.md`, Redirect `impl-plan`) |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | `review.md` als status-neutrale Datei im Change-Ordner deklarieren (Seed-Aenderung — beruehrt INBOX #22) |
| oma-personas/persona-{principled,torvalds}-reviewer/COGNITIVE.md | **Nur-Lese-Quelle** fuer die Linsen-Destillate — wird NICHT kopiert/vendored |

---

## Anforderungen

### Scope

**Enthalten:**
- Neuer Skill `dtb:impl-review` als Feature-End-Review (Pipeline-Position des heutigen `code-review`: nach `implement`/„Fertig zum Testen", vor Checkpoint/Abnahme)
- **3 Sub-Agents als Bau-Struktur:**
  1. **Drift** (mechanisch, keine Linse): Plan↔Code-Abgleich mit Verdikten MATCH/DRIFT/MISSING/EXTRA; enthaelt den **SHA-Vollstaendigkeits-Check** (alle geflippten `## Progress`-Zeilen tragen ihre Commit-SHA? Fehlend → Hinweis „Gate nicht durchlaufen?" — mechanischer Rubber-Stamping-Ersatz ohne Kommando-Re-Run)
  2. **Craft** (beide Linsen inline): principled-Linse (Konsistenz ueber Distanz, Prinzip-Treue, Detail-Treue, Blocker/non-blocking/nit-Label) + torvalds-Linse (Abstraktions-Rechtfertigung ≥2 reale Konsumenten, Sonderfall-Eleganz, Maintainer-Lens, Kontrakt-Bruch = Blocker, Performance nur im kritischen Pfad, Geschmack als nit/taste labeln)
  3. **Rules** (Regel-Abgleich, keine Linse): faltet den heutigen `code-review` ein — prueft gegen `project-rules/*.md`; **fehlen Rules → still ueberspringen statt Abbruch** (Unterschied zu heute)
- **6 Verdikt-Achsen im Report** (Lese-Struktur): Plan Adherence · Scope Discipline · Safety & Quality · Architecture · Pattern Consistency · Rules — je PASS/WARNING/FAIL + Gesamt-Verdikt APPROVED / NEEDS ATTENTION / REJECTED
- **Report-Persistenz:** `features/{slug}/review.md` (fester Dateiname im Change-Folder-Modell, KEIN Unterordner). Ein Snapshot — jeder Lauf ueberschreibt (Header: Scope, Datum, gepruefte SHA). Resume ueber `Decision: PENDING` pro Finding in der Datei (ersetzt den Chat-Marker-Resume des heutigen code-review). Bei 0 Findings: keine Datei, nur Konsolen-Verdikt
- **Interaktive Triage** via AskUserQuestion pro Finding: Fix anwenden / anders fixen / Skip / als Lektion erfassen (Pre-Fill-Anschluss an `/dtb:lesson`); nach Report Dreiwahl: Triage jetzt / Speichern & spaeter / Nur speichern
- **Diff-Scope-Erkennung ueber Progress-SHAs** (praeziser als 10x' Plan-Datum-Heuristik): die zurueckgeschriebenen SHAs liefern die exakte Commit-Menge des Features; Multi-Repo-Praefixe nach DERIVED_STATE_RULES §2 Regel 5
- Lessons-Prior wie ueblich (`📚 N Lektion(en)`-Hinweis); Lektion-Kandidat-Vorschlag; Severity×Impact-Doppelachse; Cap 10 Findings
- Optionales Argument `[phase N]` als Notausgang fuer lange Plaene (phasen-scoped Review) — nie automatisch
- `dtb:code-review` vollstaendig aus Pipeline, Doku und Distribution entfernen

**Nicht enthalten:**
- **Kein Persona-Vendoring** (Modell C — bewusste Abweichung von der Idee #20, die Vendoring als Vorbedingung nannte): Linsen leben als Destillate (~8 Zeilen je) inline im SKILL.md; keine neue kit-sync-Klasse; #8/#10 bleiben entkoppelt und offen
- **Kein Plan-Review:** `plan-review` + seine 4 Agenten bleiben unberuehrt (anderes Objekt: Plan vor Umsetzung vs. Code nach Umsetzung)
- **Keine Verifikations-Wiederholung:** fuehrt keine Plan-Kommandos aus — Success Criteria bleiben beim Verifikations-Gate in `implement` (kein Doppel)
- **Keine Auto-Fixes** ausserhalb explizit gewaehlter Triage-Fixes; strikt read-only sonst
- **Kein Abnahme-Recht:** „Abgenommen" vergibt nur der Nutzer im Checkpoint — APPROVED ≠ Abnahme
- **Kein Commit:** Triage-Fixes bleiben im Working Tree (Routine-Commit → INBOX #21)
- **Keine `kent-beck`-Linse** (Dialog-Persona, laeuft im automatisierten Artefakt-Review ins Leere)

### Gewuenschtes Verhalten
- Aufruf → 3 Sub-Agents parallel → kompakter Konsolen-Report (6 Achsen + Findings) → Dreiwahl → ggf. Triage
- **Vorgeschlagen, nie automatisch** — an 3 verdrahteten Stellen: (1) `implement` nach letzter Phase, (2) Phasen-Ende-Ritual Punkt 11 „(3) erst Review", (3) Checkpoint-Handoff → WORKFLOW_STATUS.md → workflow-resume. Standard-Taktung: EIN Review am Feature-Ende, ein Aufruf
- Bestehende Kit-UX-Muster uebernommen: Lessons-Prior-Hinweis, Lektion-Kandidat, Doppelachse, Deutsch

### Randfaelle
- `plan.md` fehlt → Hard-Gate, Redirect `/dtb:impl-plan` (+ Escape-Hatch)
- Change archiviert → harte Weigerung ohne Escape-Hatch (wie `implement`)
- Geflippte Zeilen ohne SHA → Hinweis „Gate nicht durchlaufen?" (Dimension 1)
- `## Progress` fehlt (Altbestand) → Scope nicht ableitbar: melden, Nachruestung anbieten
- Keine Rules → Dimension 3 still ueberspringen (kein Abbruch)
- `lessons.md` fehlt/leer → Prior still ueberspringen
- 0 Findings → Konsolen-Verdikt APPROVED, keine review.md
- Kein Diff ermittelbar → ehrlich melden, Scope erfragen — nie raten
- Multi-Repo → SHA-Praefixe (§2 Regel 5) in der Diff-Scope-Erkennung

### Einschraenkungen
- `review.md` = ueberschriebener Snapshot, **status-neutral** in DERIVED_STATE_RULES (Status bleibt allein bei `## Progress`)
- **Legacy-Alias dauerhaft:** Lese-Seite akzeptiert `Applies-to: impl-review`, `code-review` (Legacy) und `alle`; Schreib-Seite (`dtb:lesson`) vergibt nur noch `impl-review`. KEINE Migration bestehender lessons.md (append-only Laufzeit-Artefakt, kit-sync fasst es nie an)
- Novum `allowed-tools`: `Agent` + `AskUserQuestion` erstmals in einem dtb-Skill (Konvention „subset as needed" erlaubt es)
- Linsen-Destillate sind **Momentaufnahmen** — Divergenz zu oma-personas bewusst akzeptiert (Kit-Kopie = Quelle der Wahrheit, Entscheidung 2026-07-15)
- Deutsch; Pipeline-Frontmatter: stage development, after `dtb:implement`, next `dtb:workflow-checkpoint`

### Integrationspunkte
- Siehe Betroffene Module (12 Eintraege) — Kern: `implement`-Verdrahtung (3 Vorschlags-Stellen), lesson-Vokabular, Gate-Tabelle, DERIVED_STATE_RULES-Ergaenzung
- kit-sync: neuer Skill automatisch Klasse A; code-review-Entfernung ueber „verwaist"-Zustand (in S1 2026-07-15 verifiziert)
- 10x-Vorbild: `10x-devs-3.0/.claude/skills/10x-impl-review/SKILL.md` (existiert, vollstaendig gelesen) — uebernommen: 2-Agent-Grundriss (bei uns 3), Verdikt-Achsen, Impact-Semantik (decision effort), Triage-Loop, Report-Resume; NICHT uebernommen: Success-Criteria-Re-Run, Plan-Datum-Heuristik, reviews/-Unterordner

---

## Abhaengigkeiten

- **Fundament:** Feature `verifikations-gate` (fertig, 18/18) — impl-review konsumiert dessen SHA-Semantik (SHA = Verifikations-Beleg) fuer Diff-Scope und Rubber-Stamping-Check
- **Verwandt, unabhaengig:** INBOX #21 (`commit-and-push` — Routine-Pfad daneben, keine Kopplung), INBOX #22 (Seed-Skew — die DERIVED_STATE_RULES-Ergaenzung verschaerft dessen Relevanz), INBOX #10 (bleibt offen: mit Modell C findet KEINE Persona-Distribution statt — Korrektur der S1-Notiz, die die Aufloesung von #10 an die Distribution knuepfte)
- **Konflikte:** keine (opportunity-map, greenfield-autoren-skills: kein Beruehrungspunkt)

---

## Offene Punkte

- Exaktes Report-Layout (Box-Drawing wie 10x vs. Markdown-Tabellen wie heutiger code-review) → Spec
- Genaue Formulierung der beiden Linsen-Destillate (Entwuerfe aus der Discovery-Session vorhanden) → Umsetzungsschritt
- Ob `review.md` einen eigenen Eintrag in der pipeline-Frontmatter `produces` bekommt (ja, vorbehaltlich Spec)

---

**Erstellt mit:** `/dtb:feature-discover`
