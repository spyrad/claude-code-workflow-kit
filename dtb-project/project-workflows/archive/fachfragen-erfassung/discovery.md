# Discovery: Fachfragen-Erfassung
<!-- resume: done -->

**Erstellt:** 2026-07-17
**Idee-Referenz:** Inbox #13 — "Fachfragen-/Stakeholder-Fragen-Agenda: offene Fragen aus der Entwicklung, die ins woechentliche Fach-Meeting gehoeren, Derived-State-konform erfassen"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-feature-discover/SKILL.md` | Schreibt `## Offene Punkte` in `discovery.md` — Template + Anleitung um `[Fach]`-Konvention ergaenzen |
| `skills/dtb-feature-plan/SKILL.md` | Schreibt `## Offene Punkte` in `spec.md` — gleiche Konvention; harte "nie erfinden → als Frage eintragen"-Regel erzeugt diese Fragen |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Verankerung der Fach-Frage-Konvention (Tag `[Fach]` + Checkbox = Status offen/beantwortet), damit spaetere Lese-Ansicht + `project-health` sie kennen |
| `skills/dtb-impl-plan/SKILL.md` | NICHT im Scope (MVP) — `plan.md` bekommt keine Offene-Punkte-Sektion; die spaetere Lese-Ansicht scannt `plan.md` dennoch mit |

---

## Anforderungen

### Scope
**Enthalten:**
- Die **Erfassung** offener Fach-Fragen haerten: statusfaehige, kategorisierte Frage direkt im bestehenden `## Offene Punkte`-Kontext des Feature-Artefakts.
- Konvention: `- [ ] [Fach] {Frage}` (Checkbox = Status offen/beantwortet; Antwort im selben Bullet nachgetragen).
- Verankerung in `discovery.md` (via `feature-discover`) und `spec.md` (via `feature-plan`).
- Zentrale Regel-Definition in `DERIVED_STATE_RULES.md`, damit die Ableitung (offen/beantwortet, Fach vs. selbst-zu-klaeren) kitweit einheitlich ist.

**Nicht enthalten:**
- **Lese-Ansicht / Meeting-Agenda** (Einsammeln der `[Fach]`-Fragen ueber `features/*` hinweg, gruppiert pro Feature) → bewusst ausgelagert in einen **spaeteren, separaten Skill** (Folge-Idee, siehe Offene Punkte).
- Ein zweiter Speicherort fuer Fragen (kein eigenes Fragen-Artefakt, kein Duplizieren ins BACKLOG) — waere Derived-State-Drift.
- `plan.md` / `impl-plan`-Aenderung (MVP-Schnitt, Entscheidung A).
- `[Stakeholder]` als zweite Tag-Variante (nicht MVP).

### Gewuenschtes Verhalten
- Kommt waehrend Discovery/Spec eine Frage auf, die nicht sofort/allein beantwortbar ist (gehoert ins Fach-Meeting), wird sie als `- [ ] [Fach] {Frage}` in `## Offene Punkte` erfasst.
- Antwort wird spaeter im selben Bullet nachgetragen, Checkbox abgehakt (`- [x]`) = beantwortet; der Eintrag bleibt als Beleg stehen (nicht loeschen).
- Uebernommene Muster: das offen/erledigt-Muster aus `## Progress` und die "nie erfinden → als Frage eintragen"-Regel aus `feature-plan`.

### Randfaelle
- Bullet **ohne** `[Fach]`-Tag = normaler offener Punkt (selbst zu klaeren), nicht fuers Meeting → bestehende Prosa-Bullets bleiben gueltig (rueckwaertskompatibel).
- Keine offenen Punkte → Sektion bleibt "— keine —" (heutiges Verhalten unveraendert).
- Beantwortete Fach-Frage: abgehakt + Antwort inline, bleibt als Nachweis erhalten.
- Getaggte + untagged Bullets mischen sich in derselben Sektion → Tag-Erkennung muss robust sein (spaetere Lese-Ansicht parst nur Zeilen mit `[Fach]`).

### Einschraenkungen
- **Strikt Derived-State:** Quelle bleibt die Frage im Artefakt; kein zweiter Speicherort, kein Duplizieren ins BACKLOG.
- Konvention MUSS in `DERIVED_STATE_RULES.md` verankert werden (Voraussetzung fuer die spaetere Lese-Ansicht und fuer `project-health`).
- Spec-Zeilenlimit (max. 500) gilt weiter.
- Aenderung an `feature-discover`/`feature-plan` betrifft nur Template/Anleitung, nicht die Pipeline-Frontmatter (`## Offene Punkte` wird von `project-health`/`pipeline-graph` bereits ignoriert).

### Integrationspunkte
- `feature-discover` + `feature-plan`: Template und Anleitung um die `[Fach]`-Konvention ergaenzen.
- `DERIVED_STATE_RULES.md`: neue Regel-Sektion fuer die Fach-Frage-Konvention.
- **Nachgelagert (spaeteres Feature):** Lese-Ansicht-Skill konsumiert diese Konvention; verwandt mit Idee #24 (Besprechungs-Nachbereitung / Antwort-Rueckfluss).
- Keine externen Abhaengigkeiten.

---

## Abhaengigkeiten

- Bestehende Features: 5 (alle "Fertig zum Testen") — keine Slug-Kollision, kein Scope-Konflikt.
- **Fundament fuer** die ausgelagerte Lese-Ansicht und Idee #24: beide bauen auf der hier definierten `[Fach]`-Konvention auf. Dieses Feature muss zuerst stehen.

---

## Offene Punkte

- **Folge-Idee anlegen:** separater Lese-Skill (z.B. `/dtb:fach-agenda`), der offene `[Fach]`-Fragen aus `features/*/{discovery,spec,plan}.md` einsammelt und als nach Feature gruppierte Meeting-Agenda ausgibt (rein lesend, `produces: []`). Verwandt/abzugrenzen mit #24.
- Genaue Formulierung der Regel-Sektion in `DERIVED_STATE_RULES.md` (Tag-Grammatik, Antwort-Nachtrag-Format) → Spec/Umsetzung.
- Spaeter zu entscheiden: `[Stakeholder]` als zweite Tag-Variante neben `[Fach]`.

---

**Erstellt mit:** `/dtb:feature-discover`
