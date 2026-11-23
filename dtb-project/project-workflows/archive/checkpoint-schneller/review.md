# Review-Snapshot: checkpoint-schneller
Scope: skills/dtb-workflow-checkpoint/SKILL.md, checkpoint-phasen.py, Doku (CLAUDE.md, README.md, skills/CLAUDE.md, 6 Skills), discovery.md, probelauf.md · Geprueft bis: `2de4f18` · Datum: 2026-11-02
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:661 — „Teil C ohne Angabe = passt" schreibt still `· behalten`, auch wenn nur zu A/B geantwortet wird; widerspricht „Nie automatisch" (Z. 598) und DSR §9.4 „Keine automatische Entscheidung".
Fix: Teil C ohne Angabe wirkt wie `Abbruch C` (keine Entscheidung, ⏳ bleibt, Frage beim naechsten Mal); „Ok"/„passt" bleibt ausdrueckliche Bestaetigung.
Decision: FIXED

### F2 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:657-660 — Teil B ohne Angabe hinterlaesst zwei alte Punkte; §9.2 vergleicht nur neue Chat-Punkte gegen alte, die Dublette bleibt still bestehen; die Begruendung „Frage kommt erneut" ist falsch.
Fix: A (Empfehlung) — Teil B ohne Angabe gilt als unklar und geht in die eine Fallback-Rueckfrage. B — Marker `· Zuordnung offen zu „…"`, markierte Zeilen gehen im naechsten Lauf wieder in Teil B (aendert das Zeilenformat §9.1).
Decision: FIXED

### F3 — Pattern Consistency — [S:Mittel × I:Hoch]
dtb-project/project-rules/DERIVED_STATE_RULES.md §9.2/§9.4 — Kanon unveraendert (eigene ⏳-Vorlage, Rueckfrage bei anderer Antwort, Pruefung nach den Zuordnungsfragen); die Kopie im Checkpoint weicht in vier Punkten ab, ihr Wartungs-Hinweis sagt „Details nur dort".
Fix: §9.2/§9.4 im selben Change um einen Absatz ergaenzen (eine gemeinsame Runde, Ausschluss offener Zuordnungen aus ⏳, Defaults je Teil).
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py:61 — Kategorie „Commit/Push danach" trifft kuenftig die feste Zeile `→ Weiter mit: /dtb:commit-and-push`; die Nachmessung kann den Rueckgang nicht zeigen.
Fix: vor der Einordnung alle Zeilen entfernen, die mit `→ Weiter mit:` beginnen.
Decision: FIXED

### F5 — Plan Adherence — [S:Mittel × I:Mittel]
CLAUDE.md:60, CLAUDE.md:88, skills/dtb-workflow-checkpoint/SKILL.md:805 — Dashboard-Bedingung „Seite existiert" fehlt (Schritt 2.2 nicht vollstaendig).
Fix: „once the page exists" in beiden CLAUDE.md-Zeilen; im Schritt-6-Template „| Seite fehlt → keine Zeile".
Decision: FIXED

### F6 — Architecture — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:807-812 — Weiter-Zeile auch ohne Git (z. B. dtb-assistant) und mitten im Block statt als eine Abschlusszeile.
Fix: nur bei Guard-Ergebnis `HAUPT-CHECKOUT` ausgeben, als letzte Zeile des Blocks.
Decision: FIXED

### F7 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:638-666 — Abgangs-Zeilen in B: „5 ja" undefiniert, `verwerfen: {Grund}` fehlt (§9.3); Fallback ohne Regel fuer Verben an Nummern eines anderen Teils.
Fix: B einheitlich ja/nein (Abgang: ja = erledigt, nein = weiter) plus `{Nr} verwerfen: {Grund}`; allgemeine Regel: Verb passt nicht zum Teil der Nummer → Nummer unklar, in die eine Rueckfrage.
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Mittel]
dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py:192-193 — `worktree` greift schon bei „WORKTREE-HANDOFF (dtb)" im Modelltext; Hand-off-Empfaenge fallen aus der Auswertung.
Fix: `worktree` nur am Guard-Text `⛔ dtb:workflow-checkpoint` erkennen.
Decision: FIXED

### F9 — Safety & Quality — [S:Niedrig × I:Niedrig]
dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py:213-218 — das eine Ereignis nach dem Kern ist das Werkzeug-Ergebnis, nicht die Bestaetigung; Docstring verspricht anderes.
Fix: Kern bis zum ersten Modell-Ereignis mit Text nach `core_end` verlaengern.
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:486/501/517/654, 593, 616/627, 763 — Begriffsreste „Vorlage"; Kopfzeile/Legende bei fehlenden Teilen ungeregelt; „bekommen nur ⏳" unbedingt; „Seite vorhanden?" klebt im Absatz.
Fix: „Vorlage" → „Teil A"; „Kopfzeile und Legende nennen nur vorhandene Teile"; „⏳, falls dann faellig"; Existenzpruefung als eigener Unterpunkt.
Decision: FIXED
