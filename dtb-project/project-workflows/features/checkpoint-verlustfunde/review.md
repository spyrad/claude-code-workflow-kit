# Review-Snapshot: checkpoint-verlustfunde
Scope: skills/dtb-{workflow-checkpoint,lesson,idea,no-loss-check}/SKILL.md, CLAUDE.md, skills/CLAUDE.md, README.md, lessons.md, spec.md · Geprueft bis: `96a7b3f` · Datum: 2026-09-08
Gesamt-Verdikt: REJECTED (1 blocking) → Triage 2026-09-08: 9 FIXED, 1 SKIPPED, 0 LESSON (Snapshot-Verdikt eingefroren) — Plan Adherence WARNING, Scope PASS, Safety & Quality FAIL, Architecture WARNING, Pattern Consistency WARNING, Rules uebersprungen

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:332 — Anker-Grep nicht zeilenverankert; jeder Titel steht 2x in der Quelle (Ueberschrift + Kopplungs-Hinweis), Substring-Grep meldet falsches Gruen bei Umbenennung nur der Ueberschrift
Fix: „Anker-Grep zeilenverankert auf den ganzen Titel (`tr -d '\r' | grep -x -F`), nie als Substring — die Kopplungs-Hinweise zitieren den Titel selbst"
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:331/344 — Aufloesung typweise, Rueckfall global; intakter Typ verliert seine Vorlage (Lauf 7)
Fix: Verdikt je Quelle; Vorlage traegt Typen mit gruener Quelle, gefallener Typ bekommt Warnzeile + Befehle
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:283 — Null-Pfad: dringende `→ /dtb:open-question`-Zeile ohne definiertes Verhalten
Fix: Eingang ergaenzen: andere Skills bleiben Befehle, zaehlen in `{D}`, erscheinen nicht unter „erfasst"
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:135/153 — Log-Zeilen-Format deckt Abbruch/Rueckfall/D=0 nicht; 3 improvisierte Varianten in den Wirklaeufen
Fix: Pfeil-Slot enumerieren: `→ {L…, #…} erfasst | → nichts erfasst ({Abbruch|alle gestrichen|Rueckfall Pfad 1|Rueckfall Pfad 2|>10 Funde})`; bei D=0 Pfeil-Teil weglassen
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-lesson/SKILL.md:141 vs skills/dtb-idea/SKILL.md:78 — Kopplungs-Hinweise ungleich (nur idea nennt die Vorstreichung als Ersatz der Rueckfrage)
Fix: Satz wortgleich in den Hinweis an lesson Schritt 3 uebernehmen
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:342 — Vorlage verspricht `L{naechste}`, Nummer kippt bei Streichen
Fix: Nummern nur in der Meldung, Vorlage zeigt nur das Ziel
Decision: FIXED

### F7 — Architecture — [S:Mittel × I:Niedrig]
skills/dtb-no-loss-check/SKILL.md:304 + skills/dtb-workflow-checkpoint/SKILL.md:345 — zwei Fragen, eine Antwort; `ja` faellt in den Fallback (INBOX #73)
Fix: Checkpoint: „Die Vorlage ersetzt die Abschlussfrage"; no-loss-check: Nebensatz „entfaellt beim Aufruf aus dem Checkpoint"
Decision: FIXED

### F8 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:349 — `streiche` = verwerfen (Randfall 3), Kontrakt sagt es nicht (L41)
Fix: Antwortregel ergaenzen: „`streiche` = verwerfen, nicht vertagen — vertagen per Befehl aus dem Report"
Decision: FIXED

### F9 — Plan Adherence — [S:Niedrig × I:Mittel]
features/checkpoint-verlustfunde/spec.md:28 — sagt noch „installierte Kopie, Fallback Repo"; Plan/Umsetzung: Repo zuerst
Fix: Satz auf „Repo zuerst, sonst installierte Kopie (plan-review 2026-09-08)" ziehen
Decision: FIXED

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig]
plan.md 3.3 — 9 statt 5 Laeufe, 3 Extra-Eintraege (#74, L41, #75); Intent erfuellt, Kriterium „6 Bloecke" ist 9
Fix: keiner am Code; bewusste Abweichung, in S3-S6 dokumentiert
Decision: SKIPPED

### Unterhalb des Caps (3)
- nit: `Ok` als No-op bei nur vorgestrichenen Zeilen (#74-Familie)
- nit: Abbruch-Meldezeile ohne Wortlaut — dieselbe Zeile wie „alle gestrichen"
- nit/taste: Datierungen „seit 2026-09-08" in CLAUDE.md/skills/CLAUDE.md
