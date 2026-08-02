# Feature: Fast-Track-Schiene (dtb:feature-fast)

**Erstellt:** 2026-08-01
**Ziel:** Kleine Features durchlaufen die Erhebungsphase in EINEM Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews.
**Prioritaet:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Voll-Kette (idea-review → feature-discover → feature-plan → impl-plan) macht auch kleine
Features zeitaufwendig: drei Interview-Stationen mit zusammen ~15 Fragen. Der neue Skill
`dtb:feature-fast` buendelt diese Erhebung zu einem Durchgang: er befuellt alle drei Artefakte
mit begruendeten Default-Annahmen vor, stellt hoechstens 3 Kernfragen und legt EINE vetobare
Sammelvorlage vor. Erst nach dem Nutzer-Ok werden `discovery.md`, `spec.md` und `plan.md`
geschrieben — die nachgelagerte Kette (plan-review, implement, impl-review) laeuft unveraendert.

---

## Scope / Abgrenzung

### Enthalten
- Neuer Orchestrator-Skill `dtb:feature-fast`: buendelt die Erhebung von feature-discover,
  feature-plan und impl-plan zu einem Durchgang mit begruendeten Default-Annahmen
- Maximal 3 Kernfragen vor der Sammelvorlage — nur bei echten Informationsluecken; alle
  uebrigen Luecken werden zu markierten Annahmen (gekennzeichnet als verifiziert vs. Vermutung)
- EINE Sammelvorlage vor dem Schreiben: Annahmen nummeriert (A1, A2, ...), Korrektur per
  Freitext ("A2: stattdessen ..."), Unkommentiertes gilt als angenommen; erst nach Ok
  entstehen die Artefakte (Schreibreihenfolge discovery → spec → plan)
- Alle drei Artefakte entstehen vollstaendig und konventionskonform (inkl. `## Progress`
  in plan.md und `Status: Entwurf` im plan.md-Kopf nach §7)
- Keine eigenen Templates: die drei bestehenden SKILL.md bleiben Single Source; der
  Orchestrator liest sie zur Laufzeit aus den installierten Kopien unter `~/.claude/skills/`
- Struktur-Check vor dem Buendeln: fehlen erwartete Template-Anker in den Quell-Skills →
  Warnung und Stopp statt stilles Falsch-Buendeln
- Wartungs-Hinweis in den drei Quell-Skills ("dieses Template wird von dtb:feature-fast
  referenziert") — einzige Aenderung dort, Templates selbst unangetastet
- Eingangsweiche als Dreier-Weiche in idea-review (Aktion "Ausarbeiten"): Groesseneinschaetzung
  unterscheidet Task / Fast-Track / Voll-Schiene, immer Vorschlag + Nutzer-Bestaetigung;
  zusaetzlich Umleitungs-Angebot in feature-discover Schritt 1 bei erkannten Kleinfaellen
- Selbst-Eskalation: braucht der Entwurf mehr als 10 Annahmen oder mehr als 2 Plan-Phasen,
  empfiehlt der Skill die Voll-Schiene (benannte Schwellwerte); Nutzer kann jederzeit eskalieren
- Eskalationspfad in v1: geordneter Wechsel auf die Voll-Schiene mitten im Lauf — entstandene
  Artefakte bleiben gueltig, ab Wechselpunkt normal weiterfragen
- Wiederaufnahme: bei Abbruch vor dem Ok wird die Sammelvorlage als Entwurf zwischengespeichert
- Uebernahme vorhandener Artefakte: existiert der Change-Ordner teilweise (angefangene
  Voll-Schiene), werden vorhandene Dateien uebernommen und nur fehlende vorbefuellt

### Nicht enthalten
- Keine Aenderung an DERIVED_STATE_RULES.md, Hard-Gates oder den beiden Reviews
  (plan-review und impl-review laufen unveraendert und vollstaendig)
- Kein automatisches Routing ueber harte Kriterien — die Weiche schlaegt vor, der Mensch
  bestaetigt
- Keine Artefakt-Verschmelzung, keine Review-Verschlankung (Brainstorming 2026-08-01 verworfen)
- Kein Ad-hoc-Einstieg: INBOX-Eintrag ist Pflicht-Vorstufe
- Keine Aenderung an den Templates der drei Quell-Skills (nur Hinweis-Kommentare)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Durchwinken: Sammelvorlage wird abgenickt statt gelesen | Mittel | Hoch | Laengen-Budget (max. ~10 Annahmen, Vorlage kompakt als Kurzfassung je Artefakt); Annahmen nummeriert und einzeln vetobar; Selbst-Eskalation statt langer Vorlage |
| Kopplungs-Drift: Quell-Skills aendern sich, Orchestrator buendelt still falsch | Mittel | Mittel | Struktur-Check zur Laufzeit (Warnung + Stopp bei fehlenden Ankern) + Wartungs-Hinweis in den Quell-Skills |
| Falsche Kern-Annahme entwertet die ganze Vorlage | Mittel | Mittel | Bis zu 3 Kernfragen bei echten Luecken; Kennzeichnung verifiziert vs. Vermutung (Lektion Inbox #36b) |
| Fehleinstufung an der Weiche (zu gross fuer Fast-Track) | Mittel | Niedrig | Eskalationspfad in v1: Wechsel auf Voll-Schiene, Artefakte bleiben gueltig; Selbst-Eskalation an benannten Schwellen |
| Fast-Track-Artefakte fallen bei nachgelagerten Skills durch (Gates, Ableitung) | Niedrig | Hoch | Artefakte entstehen vollstaendig konventionskonform (§2/§4/§7); Erfolgskriterium: project-health ohne neue Befunde |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — §7 (plan.md-Kopf-Statusfeld) ist mit Feature plan-status-feld bereits etabliert

### Referenz-Dokumente
- `features/feature-fast/discovery.md` - Discovery mit allen Einzelentscheidungen (2026-08-01)
- `INBOX.md` #37 - Brainstorming-Ergebnis inkl. verworfener Alternativen (A/B) und Begruendung
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - §2 (Progress), §4 (Slug), §7 (plan.md-Kopf)
- `skills/CLAUDE.md` - Skill-Konventionen (Frontmatter, Eligibility-Gates, Mechanik-Regeln)
- `skills/dtb-feature-discover/SKILL.md`, `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-impl-plan/SKILL.md` - die drei Template-Quellen (Single Source)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein kleines Feature durchlaeuft die Erhebung in einem Durchgang: ein Aufruf, hoechstens
      3 Kernfragen, eine Sammelvorlage, ein Ok — danach existieren discovery.md, spec.md
      und plan.md im Change-Ordner
- [ ] Die erzeugten Artefakte sind von Voll-Schienen-Artefakten aus Sicht der nachgelagerten
      Skills nicht unterscheidbar: impl-plan-Gate erfuellt, plan.md-Kopf nach §7
      (`Status: Entwurf`), `## Progress` nach §2, project-health meldet keine neuen Befunde
- [ ] Annahmen erscheinen nummeriert und als verifiziert/Vermutung gekennzeichnet;
      Freitext-Vetos ("A2: stattdessen ...") werden in die Artefakte uebernommen
- [ ] Selbst-Eskalation greift bei mehr als 10 Annahmen oder mehr als 2 Plan-Phasen mit
      Empfehlung Voll-Schiene; der Wechsel erhaelt bereits entstandene Artefakte
- [ ] Abbruch vor dem Ok: beim Neustart wird die zwischengespeicherte Vorlage angeboten
      statt von vorn zu beginnen
- [ ] Struktur-Check: fehlt ein erwarteter Template-Anker in einer Quell-SKILL.md, stoppt
      der Skill mit Warnung statt zu buendeln
- [ ] Dreier-Weiche in idea-review und Umleitung in feature-discover vorhanden — beide als
      Vorschlag mit Bestaetigung, inkl. Task-Erkennung ("gar kein Feature → dtb:task")
- [ ] plan-review und impl-review laufen nach dem Fast-Track unveraendert durch

---

## Offene Punkte

- Ablageort und Format der zwischengespeicherten Sammelvorlage (Wiederaufnahme-Mechanik) —
  im Implementierungsplan festlegen
- Welche Anker-Abschnitte der drei Quell-SKILL.md prueft der Struktur-Check konkret —
  im Implementierungsplan festlegen
- Formulierung der beiden Weichen-Texte (idea-review Dreier-Weiche, feature-discover
  Schritt-1-Umleitung) — im Implementierungsplan festlegen

---

**Erstellt mit:** `/dtb:feature-plan`
