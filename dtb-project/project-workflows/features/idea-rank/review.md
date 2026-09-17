# Review-Snapshot: idea-rank
Scope: skills/dtb-idea-rank/SKILL.md, skills/dtb-idea-review/SKILL.md, CLAUDE.md, skills/CLAUDE.md, README.md, features/idea-rank/{discovery,spec,plan}.md · Geprueft bis: `3563fce` + Triage-Fixes Lauf 1 (Working Tree) · Datum: 2026-09-17
Gesamt-Verdikt: NEEDS ATTENTION
Vorlauf: Lauf 1 (2026-09-17, REJECTED) — 10 Findings, 10 FIXED

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:199 vs. 133-150 — Klammer in Topf-Regel 1 wirkt abschliessend, ist es nicht: `Ausgearbeitet` mit unfertigem Change fehlt; „externe Voraussetzung" hat in 4.2 keine Quelle.
Fix: Klammer → „(jede Zeile mit Wirkung `blockiert` aus den Tabellen in 4.2)"; in 4.2 Quelle „im Text genannte externe Voraussetzung → `zwingend`, nicht erfuellt" ergaenzen.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:182 — Nutzen `hoch` fuer „Vorbedingung anderer Ideen" zaehlt auch `sinnvoll (Vermutung)`-Kanten; eine Vermutung hebt eine Idee an Regel 2 vorbei.
Fix: „… oder ist ueber eine **zwingende** Abhaengigkeit aus 4.2 Vorbedingung anderer Ideen".
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:128-129, 138, 270 — Kanten zu einem laufenden Change haben keinen Ausgabeort (Template nur `#A vor #B`); beide Blocker-Tabellen sagen pauschal „blockiert", obwohl Regel 1 nur zwingende Kanten zaehlt.
Fix: Template `- {#A | Change {slug}} vor #{B} — …`; in den Tabellen „blockiert" → „nicht erfuellt (blockiert nur bei `zwingend`, Regel 1)".
Decision: FIXED

### F4 — Plan Adherence — [S:Niedrig × I:Mittel]
features/idea-rank/plan.md Schritt 1.2, Z.170/188 — Regel-Reihenfolge weicht vom Plan ab („Nutzen niedrig → wartend" vor „Aufwand gross → Fokus"), begruendet im Skill, aber nicht in Plan/Technischen Entscheidungen; Protokoll verweist noch auf alte Nummer 4.3.
Fix: Zeile „Regel-Reihenfolge" in Technische Entscheidungen; beide Verweise auf 4.2 korrigieren.
Decision: FIXED

### F5 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:238-239 — Zyklus-Regel „gilt nur Regel 2" kollidiert mit „Regel 2" aus 4.4 (Nutzen niedrig → wartend).
Fix: „… gilt nur die Sortierung aus 4.5 Punkt 2 (Nutzen, dann Datum)".
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:53-57 — `INBOX.md` ohne Datenzeile → falsche Meldung „Keine Inbox vorhanden" und Abbruch vor Schritt 2 (keine ⚠-Zeilen fuer genannte Nummern).
Fix: Schritt 1 bricht nur bei fehlender Datei ab; leere Datei laeuft in „nichts zu ranken" von Schritt 2.
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:146 vs. 221-223 — Dieselbe Idee #B landet mit bzw. ohne Teilmenge in verschiedenen Toepfen (Reihenfolge-Kante vs. Blocker); vertretbar, aber nicht als Absicht benannt.
Fix: Satz mit Begruendung in Schritt 2 (Arbeitsbereitschaft von #A ungeprueft).
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:242-243, 265-267, 278-279, 304-305 — Wartende Ideen erscheinen doppelt mit verschiedenem Wortlaut (⏳ im Topf + „Danach, sobald freigegeben"); „Wichtig" sagt „Jede Idee genau einmal".
Fix: Block „Danach, sobald freigegeben" streichen; „Wichtig" → „in genau einem Topf".
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:133-162 — 4.2 verteilt auf zwei Tabellen, Prosa-Absatz mit Probelauf-Anekdote und vier ↪-Varianten (drei davon inhaltsgleich).
Fix: Eine Tabelle „Vorbedingung → Wirkung" (erfuellt / nicht erfuellt / Reihenfolge-Kante / nicht pruefbar mit Grund aus fester Liste); Anekdote nach plan.md.
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig]
CLAUDE.md:51 — idea-rank-Eintrag nennt `produces: []`, wiederholt die idea-triage-Abgrenzung, ~3x laenger als Nachbarn.
Fix: Kuerzen auf „read-only effort×value ranking of open `INBOX.md` ideas into four pots with dependencies and a recommended order; optional precursor of `idea-review`".
Decision: FIXED
