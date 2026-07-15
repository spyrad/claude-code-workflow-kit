# Discovery: Verifikations-Gate
<!-- resume: done -->

**Erstellt:** 2026-07-15
**Idee-Referenz:** Inbox #19 — „Verifikations-Gate in den Umsetzungs-Loop einbetten (Vorbild `10x-implement` ‚Verification Approach'): Progress-Checkbox darf erst flippen, wenn die Checkpoint-Kriterien der Phase grün sind — SHA wird Verifikations-Beleg statt nur Commit-Beleg."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §2 härten (Hybrid-Teil b): Checkbox-Flip an grüne Checkpoint-Kriterien koppeln; SHA-Timing an das Phasen-Ritual anpassen (Flip mid-phase ohne SHA, SHA-Nachtrag beim Phasen-Commit — Widerspruch zum heutigen §2.7 „sofort mit SHA") |
| `skills/dtb-implement/SKILL.md` (NEU) | Träger (a): Treiber-Skill nach 10x-Vorbild — Plan phasenweise umsetzen, Phasen-Ende-Ritual (Checks → manuelles Gate → Commit → SHA-Rückschreibung) |
| `skills/dtb-feature-start/SKILL.md` | `next:` von `dtb:build-check` auf `dtb:implement` umhängen (Frontmatter Z. 14); 3x3-/Checkbox-Beschreibung mit implement abstimmen (Drift-Gefahr: dritter Beschreibungsort) |
| `skills/dtb-build-check/SKILL.md` | Entkernen: Verifikation wandert in den implement-Loop. Restfunktionen bewusst verorten — Multi-Repo-„deploy-ready"-Sammel-Check (für pkp real nützlich) behalten/umbenennen oder streichen; Event-Konsistenz-Check (FastWS-spezifisch) → Projekt-Rule statt Kit-Skill |
| `skills/dtb-impl-plan/SKILL.md` | `### Checkpoint-Kriterien` existieren bereits pro Phase (Z. 148) — echte Änderung: **Automated/Manual-Trennung** nach 10x-Vorbild, damit das Gate weiß, was der Skill selbst prüft und was der Mensch bestätigen muss |
| `skills/dtb-code-review/SKILL.md` | Nur Pipeline-Verweis: `after: [dtb:build-check]` umziehen. Inhaltlich unberührt (Ablösung ist #20) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Abnahme-Härtung (im Scope): Auswahloption „Abgenommen" (Schritt 2.3) verlangt heute keinen Test-Nachweis → Beleg-Rückfrage ergänzen. Zudem Referenz „Checkbox-Pflicht aus dtb:feature-start" (Schritt 2.1) auf implement umziehen |
| `skills/CLAUDE.md` | Hard-Gate-Tabelle v1 um `implement` erweitern (kritisches Artefakt `features/*/plan.md`, Redirect `impl-plan`); Pipeline-Kette aktualisieren |

Verifiziert 2026-07-15 gegen die Artefakte (Zeilenangaben) und `10x-devs-3.0/.claude/skills/10x-implement/SKILL.md`.

---

## Anforderungen

### Scope

**Enthalten:**
- **Träger-Entscheidung: Variante (a) als Hybrid** — neuer Skill `dtb:implement` führt das Gate aus, gehärtete Regel §2 begründet es; beide zeigen auf dieselbe Wahrheit
- `dtb:implement`: liest `plan.md`, Einstieg = erster offener `## Progress`-Schritt (abgeleitet, kein Sidecar), setzt phasenweise um
- **Phasen-Ende-Ritual** (10x-Vorbild): Checkpoint-Kriterien prüfen → manuelles Bestätigungs-Gate → Commit → SHA-Rückschreibung in die geflippten Progress-Zeilen (SHA = Verifikations-Beleg)
- Regel-Härtung DERIVED_STATE_RULES §2 (Checkbox-Flip erst bei grünen Kriterien; SHA-Timing)
- impl-plan: Checkpoint-Kriterien in Automated/Manual trennen
- build-check entkernen (Restfunktionen-Entscheidung im Plan)
- workflow-checkpoint: Beleg-Rückfrage bei „Abgenommen" (Abnahme-Härtung)
- Pipeline-Folgeänderungen (feature-start.next, code-review.after, checkpoint-Referenz, Hard-Gate-Tabelle)

**Nicht enthalten:**
- Kein vollautonomer Durchlauf — das manuelle Bestätigungs-Gate bleibt immer
- Keine code-review-Ablösung (= #20 `dtb:impl-review`; hier nur Verweis-Umzug)
- Kein `plan-review`-Eingriff (anderes Objekt: Plan, nicht Code)
- Kein Routine-Commit-Werkzeug (= #21 `dtb:commit-and-push`; das Ritual hier ist der Phasen-Abschluss, #21 bleibt Routine-Pfad daneben — kommt (a), wohnt das Phase-Ende-Ritual im implement-Skill)

### Gewuenschtes Verhalten
- Vertrauter 3x3-Rhythmus bleibt (max. 3 Schritte → Zusammenfassung → Feedback), implement übernimmt den Loop, den `feature-start` heute nur ankündigt
- Mid-phase: Checkbox-Flip ohne SHA (gültiger Zwischenzustand); SHA kommt beim Phasen-Commit auf alle in der Phase geflippten Zeilen
- SHA-Format bleibt §2-konform: nach ` — ` als Inline-Code, 7 Zeichen
- Wiedereinstieg jederzeit über `## Progress` (Kontextverlust-sicher, wie heute)

### Randfaelle
- **Plan ≠ Realität** → stoppen, Mismatch zeigen (Erwartet/Gefunden/Warum), fragen: anpassen / überspringen / neu planen (10x-Muster)
- **Phase ohne Code** (Doku/Verifikation) → leerer Commit-Diff erlaubt, Zeilen bleiben SHA-los (§2 Regel 3 deckt das heute schon)
- **`plan.md` ohne `## Progress`** (Altbestand) → Nachrüstung anbieten, kein Abbruch (§1.4)
- **Kein `plan.md`** → Hard-Gate: konstruktiv verweigern, Redirect `/dtb:impl-plan`, Escape-Hatch (Konvention skills/CLAUDE.md)
- **Archivierter Change** (`archive/<slug>/`) → verweigern wie 10x („archiviert — neuen Change starten")
- **Unrelated dirty paths** beim Phasen-Commit → melden und fragen (nur geplante Menge stagen / alles / abbrechen), nie still mitbündeln

### Einschraenkungen
- Multi-Repo (`config.repos`): Checks und Commit im richtigen Repo
- Git-Sicherheit hart: nie `--force`/`--no-verify`/`--amend`; explizite Pfade beim Stagen (kein `git add -A`)
- SKILL.md schlank halten (Skill-Konventionen); `plan.md`-Limit 500 Zeilen unberührt
- Sprache: Skill-Body Deutsch, Frontmatter-Keys Englisch (skills/CLAUDE.md)

### Integrationspunkte
- `feature-start` → übergibt an `implement` (statt build-check); 3x3-Beschreibung existiert dann an drei Orten (feature-start, impl-plan-Template, implement) → im Plan konsolidieren (eine Quelle, andere verweisen)
- `impl-plan` → liefert die prüfbaren Checkpoint-Kriterien (Automated/Manual)
- `workflow-checkpoint` → Abnahme-Härtung + Referenz-Umzug
- Neuer Skill automatisch: kit-sync Klasse A (`skills/dtb-*/SKILL.md`-Pattern), Pipeline-Graph/workflow-status lesen Frontmatter — keine Registrierung nötig
- Abgrenzung: #20 (impl-review) und #21 (commit-and-push) bleiben eigenständige Ideen; #21-Schnittstelle: Phase-Ende-Ritual wohnt in implement, commit-and-push wird Routine-Pfad daneben

---

## Abhaengigkeiten

- Keine Konflikte mit bestehenden Change-Ordnern (`greenfield-autoren-skills`, `opportunity-map` — beide Fertig zum Testen, anderer Strang)
- Überschneidung nur ideell mit INBOX #20/#21 (abgegrenzt, siehe Scope/Integrationspunkte)

---

## Offene Punkte

- [ ] build-check-Restfunktionen: Multi-Repo-Sammel-Check behalten/umbenennen oder streichen? Event-Konsistenz-Check als Projekt-Rule-Vorlage mitliefern oder ersatzlos? (Entscheidung im Plan)
- [ ] 3x3-Konsolidierung: welcher Ort wird die eine Quelle (implement naheliegend), wie verweisen feature-start/impl-plan-Template?
- [ ] Ausgestaltung der Beleg-Rückfrage bei „Abgenommen" in workflow-checkpoint (Freitext-Beleg vs. Verweis auf Manual-Kriterien der Phase)

---

**Erstellt mit:** `/dtb:feature-discover`
