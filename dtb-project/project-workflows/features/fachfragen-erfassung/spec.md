# Feature: Fachfragen-Erfassung

**Erstellt:** 2026-07-17
**Ziel:** Waehrend der Feature-Arbeit auftauchende Fach-Fragen (fuers Meeting) werden statusfaehig und maschinell erkennbar direkt im Feature-Artefakt erfasst — Derived-State-konform, ohne zweiten Speicherort.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Offene Fragen, die im Lauf der Entwicklung entstehen und nicht sofort/allein beantwortbar sind
(sie gehoeren ins woechentliche Fach-Meeting), werden heute nur als formlose Prosa-Bullets in
`## Offene Punkte` erfasst — ohne Status und ohne Kategorie. Dieses Feature haertet die
**Erfassung**: Eine Fach-Frage wird zu `- [ ] [Fach] {Frage}` — Checkbox als Status
(offen/beantwortet), Inline-Tag `[Fach]` als Kategorie, Antwort im selben Bullet nachgetragen.
Die Konvention wird zentral in den Statusableitungs-Regeln verankert und in den Anleitungen der
schreibenden Skills (`feature-discover`, `feature-plan`) verankert. Das legt das Fundament fuer
einen spaeteren, rein-lesenden Skill, der diese Fragen zu einer Meeting-Agenda einsammelt.

---

## Scope / Abgrenzung

### Enthalten
- **Konvention definieren:** `- [ ] [Fach] {Frage}` in der bestehenden `## Offene Punkte`-Sektion.
  Checkbox = Status (offen `[ ]` / beantwortet `[x]`); Antwort wird im selben Bullet nachgetragen,
  der Eintrag bleibt als Beleg stehen.
- **Zentrale Verankerung** der Konvention in `DERIVED_STATE_RULES.md` (Tag-Grammatik + Ableitung
  offen/beantwortet + Antwort-Nachtrag-Format), damit spaetere Konsumenten und `project-health`
  sie einheitlich kennen.
- **Anleitung ergaenzen** in `feature-discover` (schreibt `## Offene Punkte` in `discovery.md`)
  und `feature-plan` (schreibt sie in `spec.md`): wann eine offene Frage als `[Fach]` zu markieren
  ist statt als formloser Punkt.
- **Rueckwaertskompatibilitaet:** untagged Bullets bleiben gueltige „selbst-zu-klaeren"-Punkte.

### Nicht enthalten
- **Lese-Ansicht / Meeting-Agenda** (Einsammeln der `[Fach]`-Fragen ueber `features/*` hinweg,
  gruppiert pro Feature) → bewusst ausgelagert in einen spaeteren, separaten Skill (Folge-Idee).
- **Antwort-Rueckfluss aus einem Meeting** (Antworten strukturiert zurueckschreiben) → verwandte
  Idee #24, separat.
- **`plan.md` / `impl-plan`** — MVP-Schnitt (Entscheidung A): `plan.md` erhaelt keine
  `## Offene Punkte`-Sektion; die spaetere Lese-Ansicht scannt `plan.md` dennoch mit.
- **Zweiter Speicherort** fuer Fragen (eigenes Artefakt, Duplikat im BACKLOG) — waere
  Derived-State-Drift.
- **`[Stakeholder]`** als zweite Tag-Variante — spaeter, nicht MVP.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Getaggte + untagged Bullets mischen sich → spaeterer Scan erkennt Fach-Fragen unzuverlaessig | Mittel | Hoch | Eindeutige Grammatik in `DERIVED_STATE_RULES.md`: Tag `[Fach]` unmittelbar nach der Checkbox am Bullet-Anfang; Scan matcht nur diese Form |
| Konvention wird nicht genutzt (Adoption bleibt aus) | Mittel | Mittel | In `feature-discover`/`feature-plan` als aktiven Anleitungs-Prompt verankern, nicht nur als Doku-Fussnote |
| Seed-Skew: `DERIVED_STATE_RULES.md` ist Klasse-B-Seed (copied once) → Bestandsprojekte erhalten die neue Regel nicht automatisch | Hoch | Niedrig | Als bekannte Einschraenkung dokumentieren; deckt sich mit Idee #22 (Seed-Skew aktiv melden) — dort die generische Loesung |
| Antwort-Nachtrag-Format uneinheitlich (jeder traegt Antworten anders nach) | Mittel | Niedrig | Ein verbindliches Nachtrag-Format in den Regeln festlegen (eingerueckter `→ Antwort:`-Zusatz) |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — Discovery abgeschlossen, betroffene Skills existieren.

### Referenz-Dokumente
- `features/fachfragen-erfassung/discovery.md` - Discovery mit beiden Design-Entscheidungen (A/B)
- `skills/dtb-feature-discover/SKILL.md` - schreibt `## Offene Punkte` in `discovery.md`
- `skills/dtb-feature-plan/SKILL.md` - schreibt `## Offene Punkte` in `spec.md`
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - zentrale Statusableitungs-Regeln (Verankerungsort)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Die `[Fach]`-Konvention ist in `DERIVED_STATE_RULES.md` als eigene Regel verankert
      (Tag-Grammatik, Ableitung offen/beantwortet, Antwort-Nachtrag-Format).
- [ ] `feature-discover` und `feature-plan` weisen in ihrer Anleitung aktiv an, geeignete offene
      Fragen als `- [ ] [Fach] …` zu erfassen.
- [ ] Eine `[Fach]`-Frage ist maschinell eindeutig von einem untagged Bullet unterscheidbar
      (belegt an einem Beispiel) — Voraussetzung fuer die spaetere Lese-Ansicht.
- [ ] Bestehende untagged Bullets bleiben gueltig (Rueckwaertskompatibilitaet belegt).
- [ ] Die Folge-Idee (Lese-Skill fuer die Meeting-Agenda) ist in der INBOX erfasst.

---

## Offene Punkte

- [ ] [Fach] Prioritaet bestaetigen — vorgeschlagen „Mittel" (Fundament fuer spaetere Lese-Ansicht/#24,
      aber selbst kein Blocker). Bei abweichender Einschaetzung im BACKLOG korrigieren.
- Genaues Antwort-Nachtrag-Format final in `impl-plan`/Umsetzung festlegen (Entwurf: eingerueckter
  `→ Antwort: … (Meeting YYYY-MM-DD)`-Zusatz unter dem abgehakten Bullet).
- Folge-Idee (rein-lesender Skill fuer die Meeting-Agenda) via `/dtb:idea` in die INBOX schreiben.
- Spaeter zu entscheiden: `[Stakeholder]` als zweite Tag-Variante neben `[Fach]`.

---

**Erstellt mit:** `/dtb:feature-plan`
