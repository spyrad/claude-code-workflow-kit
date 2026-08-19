# Review-Snapshot: pane-start
Scope: skills/dtb-pane-start/SKILL.md, skills/dtb-worker/SKILL.md, skills/CLAUDE.md, CLAUDE.md, features/pane-start/{discovery,spec}.md · Geprueft bis: `585574a` · Datum: 2026-08-19
Gesamt-Verdikt: NEEDS ATTENTION
Achsen: Plan Adherence PASS (8/8 MATCH) · Scope WARNING (1) · Safety WARNING (3) · Architecture WARNING (2) · Pattern WARNING (4) · Rules PASS

## Findings

### F1 — Pattern Consistency — [S:Mittel × I:Hoch]
skills/dtb-pane-start/SKILL.md:289 — Rueckweg-Zeile `herdr agent prompt {orchestrator-pane} …` im Begruessungstext ist ein dritter gepflegter Ort des Kommandos; „niemals kopiert" (Z. 32-33) und Workers „nirgendwo sonst" (Z. 180) sind faktisch falsch. K3-Entscheidung erlaubte die Zeile bewusst — die Deklaration als Spiegel fehlt.
Fix: Rueckweg-Zeile in den „Regeln zur Vorlage" als deklarierten Spiegel kennzeichnen + „nirgendwo sonst"-Satz in dtb:worker um die dritte Instanz ergaenzen
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-pane-start/SKILL.md:302-305 — Vorlagen-Regel Bullet 3 („ruft den Skill nicht auf") ist importierter Worker-Wortlaut und widerspricht der Vorlage, die den Checkpoint-Aufruf anweist (Guard erzeugt den Block).
Fix: Bullet 3 auf die tatsaechliche Mechanik umformulieren (Block entsteht ueber den Checkpoint-Aufruf; Format wird nie separat gelesen, gepflegt nur dort)
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-pane-start/SKILL.md:154 — Startbefehl-Tabelle ignoriert das §7-Review-Feld: fuer einen Entwurf-Plan wird /dtb:implement statt /dtb:plan-review vorgeschlagen.
Fix: Zeile splitten (Entwurf → plan-review; Reviewed → implement)
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:159-160 — Gate-Asymmetrie: worker nutzt $HERDR_PANE_ID (Pane-Auftrag, Vorbedingung 2), gated es aber nicht.
Fix: $HERDR_PANE_ID-Bedingung wortgleich ins Eligibility-Gate des Pane-Traegers uebernehmen
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-pane-start/SKILL.md:16-17 — Pipeline-Kanten einseitig: idea-review.next und feature-discover/feature-fast.after nennen dtb:pane-start nicht (#46-Fehlerklasse).
Fix: die drei Gegenkanten nachziehen
Decision: FIXED

### F6 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/CLAUDE.md:186-191 — Einteilungs-Kriterium („mechanisch pruefen") hat jetzt ein brechendes Mitglied; Ausnahme steht nur in der Tabellenzeile, nicht an der Regel.
Fix: ein Satz am Kriteriums-Absatz (betrieblich begruendete Ausnahmen schlagen das Frontmatter-Kriterium)
Decision: FIXED

### F7 — Scope Discipline — [S:Niedrig × I:Mittel]
features/pane-start/{discovery,spec}.md — formales EXTRA: Fast-Track-Artefakte des eigenen Change, in keinem Plan-Schritt; kein Scope-Creep (Pipeline-Nebenprodukte, Commit-Buendelung war E2E-Vorbedingung).
Fix: keine Code-Aktion — Kandidat: Ausnahmeliste von dtb:impl-review um Erhebungs-Artefakte des eigenen Change ergaenzen (fremder Skill)
Decision: SKIPPED (Pipeline-Nebenprodukt des eigenen Change; Listen-Erweiterung waere ein Change an dtb:impl-review)

### F8 — Architecture — [S:Niedrig × I:Mittel]
skills/dtb-pane-start/SKILL.md:59,55,70-76 — Guard-Fence behauptet „schreibt globale Dateien" (hier falsch) + Erklaer-Fussnote; der kanonischen Vorlage fehlt ein Begruendungs-Slot.
Fix: {Grund}-Platzhalter in der kanonischen Vorlage (skills/CLAUDE.md) — Kit-Design-Aenderung, eher Lesson/INBOX
Decision: LESSON (INBOX-Kandidat beim Checkpoint: {Grund}-Platzhalter in der Guard-Vorlage; kein Nebenbei-Fix)

### F9 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-pane-start/SKILL.md:88-90 — Gate-Alternative empfiehlt pauschal feature-discover/fast; bei Slug mitten in der Umsetzung waere implement/impl-review richtig.
Fix: neutral formulieren („Befehl je nach Stand — Tabelle Schritt 1b")
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-pane-start/SKILL.md:251 — interaktiver Arbeitsplatz heisst worker-{slug}; das Feature trennt interaktiv von autonom.
Fix: dritte Zeile in der Abweichungs-Tabelle: Pfad pane-{slug}
Decision: FIXED

### F11 — Pattern Consistency — [S:Niedrig × I:Niedrig] (unterhalb Cap gelistet)
skills/dtb-pane-start/SKILL.md:178-181 — ⚠-Block „Weitere Session im Haupt-Checkout" ist undeklarierte Byte-Kopie aus skills/dtb-worker/SKILL.md:242-244.
Fix: eine Spiegel-Zeile an einer der beiden Stellen
Decision: FIXED

### F12 — Pattern Consistency — [S:Niedrig × I:Niedrig] (unterhalb Cap gelistet)
skills/dtb-pane-start/SKILL.md:136 — „unauflösbarem" mit echtem ö — einziger Umlaut-Ausreisser der Datei.
Fix: „unaufloesbarem"
Decision: FIXED

### F13 — Pattern Consistency — [S:Niedrig × I:Niedrig] (unterhalb Cap gelistet)
skills/dtb-pane-start/SKILL.md:18 — Schritt 1b leitet aus discovery.md-Existenz ab, consumes deklariert features/*/discovery.md nicht.
Fix: in consumes ergaenzen
Decision: FIXED
