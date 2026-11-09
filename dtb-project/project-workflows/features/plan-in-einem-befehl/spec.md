# Feature: Plan in einem Befehl

**Erstellt:** 2026-11-09
**Ziel:** In der vollen Spur führt nach der Discovery ein einziger Befehl bis zum fertigen Implementierungsplan.
**Prioritaet:** Mittel
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

`feature-discover → feature-plan → impl-plan → plan-review` lief auf dem Arbeitsrechner 10 von 10 Mal genau in dieser Folge. feature-plan und impl-plan stellten dabei so gut wie keine Auswahlfragen (0,0 bzw. 0,1 je Lauf) — der zweite Befehl ist eine reine Übergabe. Künftig führt `feature-plan` nach der Spec den Ablauf von `impl-plan` per Referenz mit aus. Beide Skills bleiben eigenständig, und wer bewusst nur die Spec will, kann nach ihr stoppen.

---

## Scope / Abgrenzung

### Enthalten
- `feature-plan` erstellt die Spec und danach den Implementierungsplan, indem es die Anweisungen von `impl-plan` liest und anwendet (Referenz, keine Kopie)
- Stopp-Möglichkeit „nur spec.md" beim Aufruf; ohne diese Angabe läuft der Plan immer mit, ohne neue Rückfrage
- Absicherung der Kopplung: vor der ersten Nutzung wird geprüft, ob die genutzten Abschnitte von `impl-plan` noch da sind; fehlen sie, bleibt die Spec gültig und der Lauf verweist auf `/dtb:impl-plan`
- Backlog-Status, INBOX-Link und Abschlussmeldung passen zum tatsächlichen Ausgang (mit oder ohne Plan)
- Pipeline-Angaben von `feature-plan` (Nachfolger, gelesene und erzeugte Artefakte) und die Kit-Doku nachgezogen

### Nicht enthalten
- Zusammenlegen der beiden Skills
- `plan-review` mitlaufen lassen — bleibt eigener Schritt mit frischem Blick
- Änderungen an `feature-fast` und am Übergang `feature-start`/`implement` (eigene Idee #179)
- Umbau der Sichten, die bei „Spec ohne Plan" `/dtb:impl-plan` empfehlen — der Fall bleibt durch „nur spec.md" möglich, die Empfehlung bleibt richtig

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| `impl-plan` wird umgebaut, `feature-plan` arbeitet auf veralteter Grundlage weiter | Mittel | Mittel | Struktur-Check auf die genutzten Abschnitte vor der ersten Nutzung; Wartungs-Hinweise an diesen Abschnitten nennen `feature-plan` als zweiten Leser |
| Der Plan weicht inhaltlich von einem Einzel-Lauf ab (z.B. Lektionen-Prior oder Ist-Analyse fallen weg) | Mittel | Hoch | Ausdrückliche Liste, welche Teile von `impl-plan` mitlaufen und welche entfallen; Probelauf an einem Wegwerf-Ordner |
| Backlog zeigt „Spezifiziert", obwohl schon ein Plan existiert | Hoch ohne Anpassung | Niedrig | Backlog-Status nach dem tatsächlichen Ausgang (Geplant / Spezifiziert) |
| Wer nur eine Spec wollte, bekommt ungefragt einen Plan | Niedrig | Niedrig | Stopp-Angabe beim Aufruf; ein ungewollter Plan ist ein einzelner, löschbarer Ordner-Eintrag |

---

## Dependencies

### Erforderlich vor Start
- [ ] keine

### Referenz-Dokumente
- `skills/dtb-feature-plan/SKILL.md` - der umzubauende Skill
- `skills/dtb-impl-plan/SKILL.md` - der per Referenz ausgeführte Skill
- `skills/dtb-feature-fast/SKILL.md` - Vorbild für das Referenz-Muster (Struktur-Check, zwei getrennte Fehlerpfade)
- `dtb-project/project-workflows/features/plan-in-einem-befehl/discovery.md` - Anforderungen und Randfälle

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Nach der Discovery erzeugt `/dtb:feature-plan {Name}` in einem Lauf `spec.md` und `plan.md` und nennt als nächsten Schritt `/dtb:plan-review`
- [ ] `spec.md` und `plan.md` haben dieselbe Struktur wie bei getrennten Läufen (Templates, Lektionen-Prior, Ist-Analyse, `## Progress`, Kopf-Status `Entwurf`)
- [ ] Mit der Stopp-Angabe „nur spec.md" entsteht nur `spec.md`, nächster Schritt `/dtb:impl-plan`
- [ ] `/dtb:impl-plan` funktioniert allein unverändert
- [ ] Fehlt die `impl-plan`-Kopie oder ein genutzter Abschnitt, bricht nur der Plan-Teil mit klarer Meldung ab; die Spec bleibt gespeichert
- [ ] Der Lauf stellt keine Rückfrage, die es in den getrennten Läufen nicht auch gab

---

## Offene Punkte

- — keine —

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)
