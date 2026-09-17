# Review-Snapshot: idea-rank
Scope: skills/dtb-idea-rank/SKILL.md, skills/dtb-idea-review/SKILL.md, CLAUDE.md, skills/CLAUDE.md, README.md, features/idea-rank/{discovery,spec,plan}.md · Geprueft bis: `8f2b197` + uncommittete Triage-Fixes Lauf 3 · Datum: 2026-09-17
Gesamt-Verdikt: NEEDS ATTENTION (0 blocking; Lauf 4 = Folgelauf nach strukturellen Fixes, L62 — Lauf 3: 10 FIXED, Vorlaeufe 1+2: 20 FIXED, Snapshots ueberschrieben)

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-idea-rank/SKILL.md:195-203 — Wichtigkeit weiter nicht trennscharf: „>=2 Daten" grammatisch nur an „Schmerz"; „falsche Ergebnisse" ohne Belegpflicht (umgekehrtes Beleg-Gefaelle zu mittel-hoch); Fussnote deckelt woertlich auch hoch, Skill-Liste unvollstaendig, Zielprojekte pauschal niedrig-mittel.
Fix: hoch = falsche Ergebnisse/Fehlerklasse/Schmerz jeweils mit Beleg >=2 Daten/Sessions, ein Beleg → mittel-hoch; Fussnoten-Deckel nur fuer mittel-hoch/mittel; regelmaessig genutzt = pipeline.stage ∈ {idea, planning, implementation, development, session} bzw. im Zielprojekt laut Idee-Text.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:283 ↔ 95-97 — sinnvoll-Kanten auf Ziele ausserhalb der Tabelle (laufender Change, Idee ausserhalb Teilmenge) erscheinen nirgends; Schritt 2 verspricht „trotzdem genannt".
Fix: Ziel ausserhalb: zwingend → Teil 1 Blocker; sinnvoll → `Sinnvoll erst nach {#A|Change {slug}} (Vermutung)`; Vorbedingung fuer Idee ausserhalb → `Vorbedingung fuer #B`.
Decision: FIXED

### F3 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:231-235 — Zyklus-Fallback markiert Nicht-Beteiligte und verletzt gueltige Kanten; Lesart „Vorgaenger alle schon stehen" bei Vorgaengern ausserhalb der Tabelle mehrdeutig.
Fix: Zyklus-Kanten vor dem Aufbau als nicht zwingend behandeln, alle Beteiligten mit `⚠ Zyklus mit #…` markieren, Fallback entfaellt; „Vorgaenger unter den Tabellen-Ideen".
Decision: FIXED

### F4 — Plan Adherence — [S:Mittel × I:Mittel]
features/idea-rank/plan.md Schritt 3.1/3.2, Ziel-Absatz Phase 3, Phase-1-Manual-Kriterium, Schritt 1.1 (consumes-Erweiterung aus 19a7ea0 undokumentiert); spec.md:70 `nach #A` — Plan beschreibt durch Lauf-3-Fixes abgeloeste Regeln.
Fix: Abloese-Vermerke (impl-review Lauf 3, F…) an 3.1/3.2/Ziel/Phase-1-Manual; consumes-Nachtrag 1.1; spec „Erst nach #A".
Decision: FIXED

### F5 — Plan Adherence — [S:Mittel × I:Niedrig]
features/idea-rank/plan.md `## Probelauf 2026-09-17 (Phase 3)` — inhaltlich veraltet (#39/#45 Aufwand, Sortierung #15, #95-Stufe/Bemerkungsformat, Auffaelligkeit 1 behoben).
Fix: Vermerk „durch impl-review Lauf 3 ueberholt — neuer Stand im Abnahme-Lauf"; Auffaelligkeit 1 als erledigt (F2 Lauf 3) markieren.
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:176-177 — `0,5–1 Tag` (Fast-Track) vs. `1–2 Tage` (bis zwei Phasen) ueberlappen (Unter-Cap-Finding Lauf 3).
Fix: `0,5–1 Tag` = eigener Change, eine Phase; `1–2 Tage` = eigener Change, zwei Phasen; „Fast-Track" als Merkmal streichen.
Decision: FIXED

### F7 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:180-183 ↔ 190 — bei Grundsatzfragen offen, ob Wichtigkeit Entscheidung oder Gegenstand bewertet.
Fix: Satz „Die Wichtigkeit bewertet den Gegenstand der Frage, nicht die Entscheidungsarbeit."
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:147, 149, 212-215 — Blocker-Definition steht in 4.3, Verweise zeigen auf 4.3 statt Schritt 5 Teil 1.
Fix: Definition unter die 4.2-Tabelle, Verweise auf „Schritt 5, Teil 1".
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:151-152 ↔ 284 — `↪` in 4.2 ist tote Notation (Teil 4 zieht es ab).
Fix: `↪` in 4.2 streichen, Teil 4 „im Wortlaut der Tabelle".
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:272 — kein Trenner fuer mehrere Blocker, `Change {slug}` ohne Status.
Fix: `Blockiert: {Liste mit ", "; je #A (Status) / Change {slug} (Status) / externe Voraussetzung}`.
Decision: FIXED
