# Feature: open-question

**Erstellt:** 2026-07-18
**Ziel:** Ein aktiver Erfassungs-Skill `/dtb:open-question`, der eine Fach-Frage per Text-Argument §6-konform als `- [ ] [Fach] {Frage}` in die `## Offene Punkte` des aktiven Feature-Artefakts schreibt — das Eingabe-Werkzeug, das die Fachfragen-Konvention (#13) bisher offenliess.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Fachfragen-Konvention (§6, Feature `fachfragen-erfassung` #13) definierte das Format
`- [ ] [Fach] {Frage}` samt passiver Anleitung in `feature-discover`/`feature-plan` — aber **kein
aktives Eingabe-Werkzeug**. `open-question` schliesst diese Luecke: ein leichtgewichtiger
Capture-Skill nach Vorbild `/dtb:idea`, der eine waehrend der Arbeit auftauchende Fach-Frage sofort
und Derived-State-konform im laufenden Feature ablegt — mit kurzer Ziel-Bestaetigung vor dem
Schreiben. Er ist die **Erfassungs-Stufe** der Fachfragen-Kette: Format (#13) -> **Erfassung (#26,
dieses Feature)** -> Lese-Agenda (#25) -> Antwort-Rueckfluss (#24).

---

## Scope / Abgrenzung

### Enthalten
- **Skill `/dtb:open-question "{Frage}"`** — erfasst eine Fach-Frage §6-konform als
  `- [ ] [Fach] {Frage}` in der `## Offene Punkte`-Sektion eines Change-Artefakts. Reibungslos
  wie `/dtb:idea` (`disable-model-invocation: true`), aber mit Ziel-Bestaetigung.
- **Ziel-Feature — Variante (c):** Default = das aktive „In Arbeit"-Feature ableiten
  (§1.1: `plan.md` teilweise abgehakt); Override per optionalem Slug-Argument
  (`/dtb:open-question <slug> "{Frage}"`).
- **Ziel-Datei:** die am weitesten fortgeschrittene vorhandene — `spec.md` falls vorhanden, sonst
  `discovery.md`; `## Offene Punkte` anlegen, falls die Sektion fehlt. (`plan.md` bleibt aussen vor,
  MVP-Schnitt #13.)
- **Verhalten — Variante (B):** ermitteltes Ziel (`features/<slug>/<datei>`) + die formatierte
  `[Fach]`-Zeile anzeigen, kurze Freigabe abwarten, *dann* schreiben. Danach kompakte Bestaetigung
  mit Verweis auf die spaetere Agenda-Ansicht (#25) / `/dtb:workflow-next`.
- **Randfall-Verhalten:** 0 aktive Features + kein Slug -> abbrechen mit Hinweis + waehlbare Slugs;
  >1 aktiv -> Auswahlliste; Slug ungueltig/leerer Ordner -> abbrechen + Liste vorhandener Ordner
  (kein Auto-Anlegen); Ziel nur mit `plan.md`/`bug.md`/`task.md` -> in `spec.md` schreiben falls
  vorhanden, sonst abbrechen; leeres Frage-Argument -> nachfragen; Sonderzeichen -> 1:1 uebernehmen,
  mehrzeilig zu einer Bullet-Zeile normalisieren.
- **Pipeline-Einordnung:** `stage: capture`, `after: null` (jederzeit aufrufbar),
  `consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]`,
  `produces: [features/*/spec.md, features/*/discovery.md]`, `next: [dtb:workflow-next]`.
- **Katalog + Distribution:** Eintrag in `CLAUDE.md`; Klasse-A-Verteilung via `kit-sync` + Lock-Eintrag.

### Nicht enthalten
- **Beantworten/Abhaken** von Fragen -> Idee #24.
- **Lese-/Agenda-Ansicht** (`[Fach]`-Fragen einsammeln) -> Idee #25.
- **`[Stakeholder]`-Tag** als zweite Variante -> spaeter.
- **Zweiter Speicherort** (eigenes Fragen-Postfach, BACKLOG-Duplikat) — waere Derived-State-Drift,
  widerspricht §6.
- **Schreiben in `plan.md`/`bug.md`/`task.md`** — kein Ziel dieser Sektion.
- **Aendern von Status/`## Progress`** — der Skill ist strikt status-neutral (§6.2).

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Format-Kopplung: drei Schreiber von `## Offene Punkte` (open-question, feature-discover, feature-plan) driften bei §6-Aenderungen auseinander | Mittel | Hoch | §6 als Single Source referenzieren; Wartungs-Hinweis (Format-Kopplung) im Skill, analog den bestehenden Kopplungs-Hinweisen |
| Fehl-Ablage: bei abgeleitetem Ziel landet die Frage im falschen Feature | Mittel | Mittel | Variante (B) — Ziel vor dem Schreiben bestaetigen; bei >1 aktiven Features Auswahlliste statt Raten |
| Seed-Skew: Skill = Klasse A (verteilt), liest §6 aus `DERIVED_STATE_RULES.md` (Klasse-B-Seed) — Bestandsprojekte tragen evtl. alten Seed | Niedrig | Niedrig | Skill garantiert die §6-Kanonform selbst (nicht aus dem Projekt-Seed ableiten); deckt sich mit #22 (Seed-Skew aktiv melden) |
| Adoption bleibt aus (Werkzeug wird nicht genutzt) | Mittel | Mittel | Reibungslos wie `/dtb:idea` halten; nur eine Freigabe, kein Interview |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — Discovery abgeschlossen; §6-Konvention, `/dtb:idea`-Vorbild und die betroffenen
      Skills existieren bereits.

### Referenz-Dokumente
- `features/open-question/discovery.md` - Discovery mit allen Entscheidungen (Variante c/B, Randfaelle)
- `skills/dtb-idea/SKILL.md` - Struktur-Vorbild (Config -> Input -> Write -> Confirm)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - §6 (`[Fach]`-Grammatik) + §1.1 (aktives-Feature-Ableitung)
- `skills/dtb-feature-discover/SKILL.md` + `skills/dtb-feature-plan/SKILL.md` - die anderen zwei Schreiber von `## Offene Punkte`
- `skills/dtb-kit-sync/SKILL.md` - Klasse-A-Distribution nach dem Bau

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `/dtb:open-question "…"` schreibt eine korrekte `- [ ] [Fach] …`-Zeile ans Ende der
      `## Offene Punkte`-Sektion des Ziel-Features (belegt an einem Beispiel).
- [ ] Variante-(c)-Routing belegt: Default leitet das aktive Feature ab; Slug-Override greift;
      0 aktive und >1 aktive Features werden sauber behandelt (je ein Fall gezeigt).
- [ ] Variante (B) belegt: Ziel + formatierte Zeile werden vor dem Schreiben angezeigt und die
      Freigabe abgewartet.
- [ ] Derived-State-Neutralitaet belegt: das Erfassen einer Frage in ein „Fertig zum Testen"-Feature
      aendert dessen abgeleiteten Status nicht.
- [ ] Die erzeugte Zeile ist maschinell eindeutig als `[Fach]`-Frage erkennbar (§6-Grammatik) —
      Voraussetzung fuer die spaetere Lese-Ansicht #25.
- [ ] Duplikat-Schutz belegt: identische offene `[Fach]`-Frage wird gemeldet und nicht doppelt geschrieben.
- [ ] Skill global verteilt (`kit-sync`, Lock-Eintrag) und im `CLAUDE.md`-Katalog gelistet.

---

## Offene Punkte

- Genauer Wortlaut der Ziel-Bestaetigung (Variante B) und der Duplikat-Warnung final in `impl-plan` festlegen.
- `next: [dtb:fach-agenda]` erst verdrahten, wenn die Lese-Ansicht (#25) existiert (bis dahin `dtb:workflow-next`).
- Keine Fach-Meeting-Fragen offen (rein kit-internes Werkzeug, alles selbst entscheidbar).

---

**Erstellt mit:** `/dtb:feature-plan`
