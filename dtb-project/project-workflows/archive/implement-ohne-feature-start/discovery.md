# Discovery: implement ohne feature-start
<!-- resume: done -->

**Erstellt:** 2026-11-10
**Idee-Referenz:** Inbox #179 — "Kette straffen (3/4): `dtb:feature-start` vor `dtb:implement` überflüssig machen."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-implement/SKILL.md` | Uebernimmt die Auswahl ohne Argument (Schritt 1) und zeigt Ziel/Scope aus der Spec in der Statusanzeige (Schritt 2 Punkt 5); `after` wird `[dtb:plan-review]`; Rhythmus-Hinweis und „Verwandte Skills" nennen feature-start nicht mehr als Uebergeber |
| `skills/dtb-feature-start/SKILL.md` | Verliert den Feature-Zweig: listet nur noch analysierte Bugs und offene Aufgaben; Feature-Nennung → Verweis-Zeile auf `/dtb:implement`; `after` wird `[dtb:debug-plan]` |
| `skills/dtb-plan-review/SKILL.md` | `next: [dtb:feature-start]` → `[dtb:implement]` |
| `skills/dtb-impl-plan/SKILL.md` | Bestaetigungs-Block („Feature starten") und „Verwandte Skills" nennen `/dtb:implement` |
| `skills/dtb-workflow-next/SKILL.md` | Zeile „Start ausstehend" (Plan `Reviewed`, 0/Y) → `/dtb:implement [NAME]` |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Handoff-Regel „Geplant (0/Y)" und Beispiel im Handoff-Template → `/dtb:implement {NAME}` |
| `skills/dtb-workflow-status/SKILL.md` | Queue-Zeile „Backlog (Geplant)" und Uebergangstabelle „Feature starten" → `/dtb:implement` |
| `skills/dtb-workflow-resume/SKILL.md` | Fall C („kein aktives Feature") nennt `/dtb:implement` fuer Features und `/dtb:feature-start` fuer Bugs/Aufgaben |
| `skills/dtb-pipeline-graph/SKILL.md` | Beispiel-Kette der Feature-Pipeline ohne feature-start; Vorgaenger-Zaehlung von feature-start im Kanten-Beispiel |
| `skills/CLAUDE.md` | Hard-Gate-Tabelle (Zeilen plan-review, feature-start, implement) und Rueckfragen-Tabelle Zeile 15 |
| `README.md` | Skill-Tabelle: Beschreibung von `/dtb:feature-start` |
| `CLAUDE.md` | Skill-Kategorien: Beschreibung von `feature-start` und `implement` |

---

## Anforderungen

### Scope
**Enthalten:**
- `implement` uebernimmt, was `feature-start` fuer Features zusaetzlich leistet: Auswahlliste ohne Argument und 2-3 Zeilen Ziel/Scope aus der Spec
- `feature-start` beschraenkt sich auf analysierte Bugs und offene Aufgaben
- Alle Feature-Verweise auf `feature-start` zeigen auf `implement`

**Nicht enthalten:**
- Aenderungen am Bug- und Aufgaben-Weg (debug-plan, task, Bug-/Aufgaben-Zeilen in workflow-next und workflow-status)
- Aenderung an `DERIVED_STATE_RULES.md` (nennt feature-start nicht — gegrept)
- Die Schwester-Ideen der Reihe „Kette straffen" (#177, #178, #180) und die Autonomie-Idee #182

### Gewuenschtes Verhalten
- Nach `plan-review` fuehrt genau ein Befehl in die Umsetzung: `/dtb:implement {Name}`
- `implement` ohne Argument und ohne erkennbaren Chat-Kontext zeigt eine Auswahlliste der Features mit `plan.md` und offenen Progress-Zeilen (Geplant und In Arbeit), statt nur nach dem Namen zu fragen
- Die kompakte Statusanzeige von `implement` enthaelt 2-3 Zeilen Ziel/Scope aus `spec.md`
- `feature-start` mit einem Feature → genau eine Zeile `→ Features startet /dtb:implement {Name} direkt`

### Randfaelle
- Kein Feature mit offenen Progress-Zeilen → `implement` meldet das ehrlich und verweist auf `/dtb:feature-start` (Bug, Aufgabe) bzw. `/dtb:impl-plan`
- Plan ohne `## Progress` (Altbestand) → bestehende Nachruestung in `implement` Schritt 2 Punkt 2 greift (unveraendert)
- `spec.md` fehlt → Statusanzeige ohne Ziel-Zeilen, kein Abbruch (das Gate prueft nur `plan.md`)
- `feature-start` ohne Bugs und Aufgaben → Meldung „nichts zu starten" ohne Feature-Erwaehnung

### Einschraenkungen
- `implement` bleibt `disable-model-invocation: true` — feature-start ruft es weiterhin nicht selbst auf
- Rueckfragen-Kanon (Veto-Form): die neue Auswahl ist eine echte Wahl ohne Default, keine neue Leerlauf-Rueckfrage
- Rueckfragen-Tabelle Zeile 15 bleibt als Geschichte stehen (Vermerk „seit 2026-11-10 entfallen"), Zeile E bleibt gueltig

### Integrationspunkte
- Pipeline-Frontmatter (`after`/`next`) speist `pipeline-graph`, `workflow-status` und `project-health` — Kanten muessen konsistent bleiben
- Installierte Kopien erreichen Zielprojekte erst per `dtb:kit-sync` nach dem Merge

---

## Abhaengigkeiten

- Keine Konflikte. Schwester-Idee #178 (feature-plan ruft impl-plan mit auf) ist gemergt und beruehrt dieselben Abschluss-Bloecke nicht.

---

## Offene Punkte

- — keine —

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-10)
