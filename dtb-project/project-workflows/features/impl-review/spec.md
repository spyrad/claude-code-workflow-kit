# Feature: impl-review

**Erstellt:** 2026-07-15
**Ziel:** Ein Implementierungs-Review-Skill (`dtb:impl-review`) ersetzt `dtb:code-review` als Feature-End-Review — drei Dimensionen (Plan-Drift, Craft, Rules) statt reinem Rules-Check.
**Prioritaet:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit prueft umgesetzten Code heute nur gegen Projekt-Rules (`dtb:code-review`) — ob der Code
dem **Plan** entspricht (Drift, Scope-Creep, fehlende Schritte) und ob er **handwerklich** traegt
(Konsistenz, Abstraktion, Wartbarkeit), prueft niemand. `dtb:impl-review` schliesst diese Luecke
nach dem Vorbild von `10x-impl-review`: drei Sub-Agents (Drift mechanisch, Craft mit zwei
destillierten Reviewer-Linsen, Rules-Abgleich), ein Report mit sechs Verdikt-Achsen, interaktive
Triage mit gespeichertem Wiederaufnahme-Stand. `dtb:code-review` wird danach vollstaendig aus
Pipeline, Doku und Distribution entfernt.

---

## Scope / Abgrenzung

### Enthalten

- **Neuer Skill `skills/dtb-impl-review/SKILL.md`** an der Pipeline-Position des heutigen
  `code-review` (nach `implement` / „Fertig zum Testen", vor Checkpoint/Abnahme)
- **3 Sub-Agents (Bau-Struktur):**
  1. **Drift** — mechanischer Plan↔Code-Abgleich (MATCH/DRIFT/MISSING/EXTRA); enthaelt den
     SHA-Vollstaendigkeits-Check (geflippte `## Progress`-Zeilen ohne SHA → Hinweis
     „Gate nicht durchlaufen?") als Rubber-Stamping-Ersatz ohne Kommando-Re-Run
  2. **Craft** — zwei inline destillierte Linsen (Modell C, kein Persona-Vendoring):
     principled-Linse (Konsistenz ueber Distanz, Prinzip-/Detail-Treue, Blocker/non-blocking/nit)
     + torvalds-Linse (Abstraktions-Rechtfertigung, Sonderfall-Eleganz, Maintainer-Lens,
     Kontrakt-Bruch = Blocker, Performance nur im kritischen Pfad, Geschmack als nit/taste)
  3. **Rules** — faltet den heutigen `code-review` ein: Abgleich gegen `project-rules/*.md`;
     fehlen Rules → still ueberspringen (kein Abbruch wie heute)
- **Report mit 6 Verdikt-Achsen** (Lese-Struktur): Plan Adherence · Scope Discipline ·
  Safety & Quality · Architecture · Pattern Consistency · Rules — je PASS/WARNING/FAIL,
  Gesamt-Verdikt APPROVED / NEEDS ATTENTION / REJECTED; Severity×Impact-Doppelachse,
  Cap 10 Findings
- **Report-Persistenz:** `features/{slug}/review.md` — fester Dateiname im Change-Folder-Modell,
  ueberschriebener Snapshot (Header: Scope, Datum, gepruefte SHA); Resume ueber
  `Decision: PENDING` pro Finding (ersetzt den Chat-Marker-Resume); bei 0 Findings keine Datei
- **Interaktive Triage** pro Finding (Fix anwenden / anders fixen / Skip / als Lektion erfassen
  mit Pre-Fill-Anschluss an `/dtb:lesson`); nach dem Report Dreiwahl: Triage jetzt /
  Speichern & spaeter / Nur speichern
- **Diff-Scope aus Progress-SHAs** (exakte Commit-Menge des Features statt Datums-Heuristik);
  Multi-Repo-Praefixe nach DERIVED_STATE_RULES §2 Regel 5
- **Lessons-Prior** mit Legacy-Alias: liest `Applies-to: impl-review`, `code-review` (Legacy)
  und `alle`; Lektion-Kandidat-Vorschlag wie gehabt
- Optionales Argument `[phase N]` als Notausgang fuer lange Plaene — nie automatisch
- **Verdrahtung „vorgeschlagen, nie automatisch"** an 3 Stellen: `implement` nach letzter Phase,
  Phasen-Ende-Ritual Punkt 11, Checkpoint-Handoff (→ WORKFLOW_STATUS.md → workflow-resume)
- **Vollstaendige Abloesung von `dtb:code-review`:** Skill-Ordner entfernen; alle aktiven
  Referenzen umbiegen (implement, workflow-checkpoint, pipeline-graph, workflow-status, lesson,
  generate-rules, Kit-CLAUDE.md, skills/CLAUDE.md-Gate-Tabelle); Entfernung installierter
  Kopien ueber den kit-sync-„verwaist"-Pfad
- **DERIVED_STATE_RULES-Ergaenzung:** `review.md` als status-neutrale Datei im Change-Ordner
  (Status bleibt allein bei `## Progress`)
- **Eligibility-Hard-Gate:** kritisches Artefakt `features/{slug}/plan.md`, Redirect
  `/dtb:impl-plan`; Archiv-Weigerung ohne Escape-Hatch (wie `implement`)

### Nicht enthalten

- **Kein Persona-Vendoring** (bewusste Abweichung von Idee #20, die Vendoring als Vorbedingung
  nannte): Linsen leben als Destillate (~8 Zeilen je) inline im SKILL.md; keine neue
  kit-sync-Klasse; INBOX #8/#10 bleiben entkoppelt und offen
- **Kein Plan-Review:** `plan-review` + seine 4 Agenten-Rollen bleiben unberuehrt
  (anderes Objekt: Plan vor Umsetzung vs. Code nach Umsetzung)
- **Keine Verifikations-Wiederholung:** keine Ausfuehrung von Plan-Kommandos — Success
  Criteria gehoeren dem Verifikations-Gate in `implement` (kein Doppel)
- **Keine Auto-Fixes** ausserhalb explizit gewaehlter Triage-Fixes; sonst strikt read-only
- **Kein Abnahme-Recht:** APPROVED ≠ Abgenommen — Abnahme vergibt nur der Nutzer im Checkpoint
- **Kein Commit:** Triage-Fixes bleiben im Working Tree (Routine-Commit → Idee #21)
- **Keine kent-beck-Linse** (Dialog-Persona, laeuft im automatisierten Artefakt-Review ins Leere)
- **Keine Migration bestehender lessons.md** (append-only Laufzeit-Artefakt; Legacy-Alias
  statt Datenaenderung)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Craft-Linsen erzeugen Geschmacks-Noise statt Substanz (Findings-Flut, Bikeshedding) | Mittel | Mittel | nit/taste-Label + Blocker-Trennung aus den Linsen-Filtern; Cap 10; Selbst-Test des Skills auf einem echten Feature vor Abnahme |
| Vergessene `code-review`-Referenz bleibt aktiv (Pipeline schlaegt widerspruechliche Schritte vor) | Mittel | Hoch | Sweep-Grep als Automated-Kriterium — praezise auf Zielorte geankert (`after:`/`next:`-Frontmatter, Skill-Verweise), nicht auf blosse Stichwoerter (Lektion #2); Changelog/INBOX-Historie bleibt bewusst unangetastet |
| Diff-Scope-Ableitung scheitert bei SHA-losen Zeilen (leere Diff-Phasen, §2 Regel 4) | Mittel | Niedrig | Ehrlich melden + Scope erfragen — nie raten (Randfall aus Discovery) |
| Re-Run ueberschreibt review.md mit offenen `Decision: PENDING`-Findings (Triage-Stand weg) | Niedrig | Mittel | Vor dem Ueberschreiben pruefen: existiert review.md mit PENDING-Eintraegen → warnen und bestaetigen lassen |
| Seed-Aenderung (DERIVED_STATE_RULES) erreicht Bestandsprojekte nicht | Hoch | Niedrig | Bekanntes, bewusstes Verhalten (Klasse B); verschaerft INBOX #22 — dort loesen, nicht hier |
| Sub-Agent-Nutzung (Novum in dtb-Skills) blaeht Kontext/Kosten auf | Niedrig | Mittel | Gezielter Kontext pro Agent wie im 10x-Vorbild (Plan-Auszuege + Dateiliste, nicht alle Quelldateien in den Hauptkontext) |

---

## Dependencies

### Erforderlich vor Start

- [x] Feature `verifikations-gate` fertig (18/18) — liefert SHA-Semantik (SHA = Verifikations-Beleg) fuer Diff-Scope und SHA-Vollstaendigkeits-Check
- [x] Discovery abgeschlossen (`features/impl-review/discovery.md`)
- [x] Persona-Quellen lesbar (`oma-personas/persona-{principled,torvalds}-reviewer/COGNITIVE.md` — Nur-Lese-Quelle fuer Destillate)

### Referenz-Dokumente

- `features/impl-review/discovery.md` — vollstaendige Anforderungen, Randfaelle, 12 betroffene Module
- `../10x-devs-3.0/.claude/skills/10x-impl-review/SKILL.md` — Vorbild (2-Agent-Grundriss, Verdikt-Achsen, Impact-Semantik, Triage-Loop, Report-Resume)
- `skills/dtb-code-review/SKILL.md` — Bestand (Rules-Logik, Lessons-Prior, Doppelachse, Cap — wird eingefaltet)
- `skills/dtb-implement/SKILL.md` — Verdrahtungs-Stellen + SHA-Ritual (§2-Bezug)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — §2 (SHA-Semantik, Multi-Repo-Praefix), §4 (Slug); Ergaenzungs-Ort fuer review.md
- `skills/CLAUDE.md` — Frontmatter-Konventionen, Eligibility-Gate-Tabelle, Distributions-Klassen

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] `skills/dtb-impl-review/SKILL.md` existiert mit 3 Sub-Agents, 6 Verdikt-Achsen, Triage-Loop und regelkonformem Frontmatter (inkl. `Agent` + `AskUserQuestion` in allowed-tools)
- [ ] Beide Craft-Linsen sind als Inline-Destillate enthalten (principled + torvalds, je Kerndenken + Entscheidungsfilter, ohne Stimme/Tonfall)
- [ ] Drift-Agent enthaelt den SHA-Vollstaendigkeits-Check; kein Sub-Agent fuehrt Plan-Kommandos aus
- [ ] `review.md`-Persistenz funktioniert wie spezifiziert: Snapshot ueberschrieben, `Decision: PENDING`-Resume, keine Datei bei 0 Findings, PENDING-Warnung vor Ueberschreiben
- [ ] Rules-Dimension laeuft ohne `project-rules/*.md` still weiter (kein Abbruch)
- [ ] Lessons-Prior liest `impl-review`, `code-review` (Legacy) und `alle`; `dtb:lesson`-Vokabular vergibt nur noch `impl-review`
- [ ] `skills/dtb-code-review/` ist entfernt; Sweep-Grep findet keine aktive Referenz mehr in `skills/**` (Frontmatter `after:`/`next:` + Verweis-Texte), Kit-CLAUDE.md und skills/CLAUDE.md
- [ ] Alle 3 Vorschlags-Stellen zeigen auf `impl-review` (implement ×2, Checkpoint-Handoff)
- [ ] Eligibility-Gate-Tabelle in skills/CLAUDE.md hat den impl-review-Eintrag; DERIVED_STATE_RULES deklariert review.md als status-neutral
- [ ] Selbst-Test: ein Lauf auf einem echten umgesetzten Feature erzeugt Report + Triage ohne Erfindungen (ehrliche Meldung bei nicht ermittelbarem Scope)

---

## Offene Punkte (entschieden mit Phase 4.3, 2026-07-16)

- ~~Report-Layout: Box-Drawing (10x-Stil) vs. Markdown-Tabellen (Kit-Stil)~~ → **Markdown-Tabellen** (Kit-Konsistenz; Entscheidungstabelle plan.md)
- ~~Bekommt `review.md` einen Eintrag in der pipeline-Frontmatter `produces`?~~ → **Ja** (`produces: [features/*/review.md]`; pipeline-graph/workflow-status lesen Frontmatter)
- ~~Exakte Formulierung der beiden Linsen-Destillate~~ → **Final** in `skills/dtb-impl-review/SKILL.md` (principled + torvalds, je Kerndenken + Filter, ohne Stimme/Tonfall)

---

**Erstellt mit:** `/dtb:feature-plan`
