# Feature: plan-review mit Subagenten

**Erstellt:** 2026-11-27
**Ziel:** Die Rollen von `dtb:plan-review` urteilen unabhaengig voneinander, statt dass ein Modell alle Rollen nacheinander im selben Kontext spielt.
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Heute spielt `dtb:plan-review` Architekt, Pragmatiker und Senior Dev in einem Kontext — die zweite Stimme hat die erste schon gelesen, die Perspektiven verschmelzen. Kuenftig bekommt jede aktive Rolle einen eigenen, isolierten Lauf mit ihrer Rollendefinition und denselben Eingaben, ohne die Befunde der anderen; der Skill fuehrt die Ergebnisse danach im bekannten Report-Format zusammen. Ein optionales Modell je Rolle erlaubt zusaetzlich verschiedene Modelle im Ensemble.

---

## Scope / Abgrenzung

### Enthalten
- Je aktiver Rolle ein eigener, isolierter Review-Lauf; alle Laeufe starten gleichzeitig
- Jede Rolle erhaelt nur: ihre Rollendefinition, den Plan und die Spec des Features, die Ergebnisse von Grounding und Challenger-Pass, die gefilterten Lektionen
- Jede Rolle liefert alle vier Runden und die Verdikte ihrer eigenen Dimensionen, optional Einsprueche zu fremden Dimensionen
- Zusammenfuehrung im Skill: bestehendes Report-Format, feste Gesamt-Verdikt-Regel, Einspruch-Reaktion in einem gekennzeichneten Satz
- Optionale Modellwahl je Rolle in der Projekt-Konfiguration, Default: das Modell der laufenden Session
- Sichtbarer Rueckfall auf den heutigen Ablauf, wenn ein isolierter Lauf nicht moeglich ist oder scheitert
- Nachgezogene Doku (Rollen-Leitfaden, Kit-Uebersicht, README, Konfigurationsvorlage von `dtb:project-init`)

### Nicht enthalten
- Rollendefinitionen als eigenstaendig registrierte Agenten-Typen (Kernfrage 2026-11-27: bleiben reine Prompt-Texte)
- Eine zweite Modellfamilie (bleibt #182)
- Eine zweite Runde, in der die zustaendige Rolle auf Einsprueche antwortet
- Aenderungen an Verdikt-Semantik, Finding-Runde und Kopf-Statusfeld

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Isolierte Rolle liefert ein Ergebnis, das nicht ins Report-Format passt (Verdikt fehlt, fremde Dimension bewertet) | Mittel | Mittel | Festes Rueckgabeformat im Auftrag; unbrauchbare Rueckgabe → Rolle im Hauptkontext nachholen, ⚠-Zeile |
| Einspruch-Reaktion im Hauptkontext fuehrt das Rollenspiel-Problem durch die Hintertuer wieder ein | Mittel | Niedrig | Reaktion ist auf einen Satz begrenzt und gekennzeichnet; Beurteilung am Manual-Gate von Phase 1 (Offener Punkt) |
| Hoehere Kosten und Laufzeit (bis zu vier Laeufe statt einem) | Hoch | Niedrig | Laeufe parallel; Kosten sind der bewusste Preis unabhaengiger Urteile |
| Isolierte Rolle schreibt Dateien | Niedrig | Hoch | Auftrag ist ausdruecklich read-only; geschrieben wird nur im Hauptkontext |
| Installierte Kopie veraltet gegen die Repo-Fassung im Probelauf | Mittel | Mittel | Probelauf gegen die Repo-Fassung (`skills/dtb-plan-review/SKILL.md`), nicht gegen `~/.claude/` (L74/L133) |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine

### Referenz-Dokumente
- `skills/dtb-plan-review/SKILL.md` - der umzubauende Skill
- `skills/dtb-impl-review/SKILL.md` - Vorbild fuer isolierte Review-Laeufe (Schritte 4–6)
- `agents/*.md` - die vier Rollendefinitionen
- `dtb-project/project-workflows/features/plan-review-subagenten/discovery.md` - Discovery

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Jede aktive Rolle laeuft isoliert und sieht die Befunde der anderen Rollen nicht
- [ ] Der Report hat dasselbe Format wie heute plus eine Kopfzeile, die zeigt, wie viele Rollen isoliert liefen
- [ ] Gesamt-Verdikt, Finding-Runde und Kopf-Statusfeld verhalten sich unveraendert
- [ ] Faellt ein isolierter Lauf aus, laeuft das Review trotzdem zu Ende und meldet den Ausfall sichtbar
- [ ] Ohne Modell-Konfiguration erben alle Rollen das Session-Modell; mit Konfiguration nutzt jede Rolle ihr Modell
- [ ] Ein Probelauf an einem echten (kopierten) Plan liefert einen Report, den der Mensch als brauchbar abnimmt

---

## Offene Punkte

- Reicht die gekennzeichnete Ein-Satz-Reaktion des Skills auf Einsprueche, oder braucht es spaeter doch eine Rueckfrage an die zustaendige Rolle? — am Manual-Gate von Phase 1 beurteilen

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-27)
