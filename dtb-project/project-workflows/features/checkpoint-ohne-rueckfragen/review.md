# Review-Snapshot: checkpoint-ohne-rueckfragen
Scope: 14 Dateien (Checkpoint-, no-loss-check-, lesson/idea/idea-triage/impl-plan/debug-plan-Skills, skills/CLAUDE.md, CLAUDE.md, README.md, DERIVED_STATE_RULES.md, Feature-Dokumente) · Geprueft bis: `5e41cfc` · Datum: 2026-11-03
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
skills/dtb-workflow-checkpoint/SKILL.md:482 — Der Eingang zaehlt auch Fach-Fragen (open-question), die nie geschrieben und nie gefragt werden; Mengenprobe „zu schreiben + Duplikat-Treffer = Eingang" geht nicht auf → „neu zaehlen statt schreiben", nichts wird erfasst; auch > 10 und Pfeil-Slot zaehlen falsch
Fix: Eingang auf Funde mit `/dtb:lesson`- oder `/dtb:idea`-Zeile beschraenken; Fach-Fragen „zaehlen in {D}, nie im Eingang"
Decision: FIXED

### F2 — Plan Adherence — [S:Mittel × I:Mittel]
CLAUDE.md:50, DERIVED_STATE_RULES.md §9.4 letzter Bullet + Aenderungs-Absatz — Runde „nur Zuordnungs- und Abgangsfragen", Duplikat-Frage fehlt; §9.4 ohne „Rueckfrage unklar → wie nein"
Fix: an allen drei Stellen „(der Checkpoint legt moegliche Duplikate in dieselbe Runde)" ergaenzen, §9.4 zusaetzlich „bleibt die Rueckfrage unklar → wie nein"
Decision: FIXED

### F3 — Plan Adherence — [S:Mittel × I:Mittel]
skills/dtb-no-loss-check/SKILL.md:255, 303, 409 — „ueber die Checkpoint-Vorlage", obwohl es keine Vorlage mehr gibt (303/409 im Ausgabe-Muster)
Fix: „ueber den Checkpoint (Schritt 0, ohne Rueckfrage)"
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:646 — „Abbruch" im Kontrollpunkt undefiniert → unklar → wie nein → Duplikat-Fund wird trotz Abbruch geschrieben
Fix: Zeile „`Abbruch` → Duplikat-Funde nicht erfassen (bleiben Befehle im Report), Zuordnung/Abgang wie `nein`"
Decision: FIXED

### F5 — Architecture — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:517–549, 801 — „nicht erfasst" uneinheitlich: nur > 10 hat eine Zeile in Schritt 6; Quellen-Rueckfall und Schreibfehler nur verstreut im Lauf, im Log nicht
Fix: allgemeine Zeile `⚠ {n} Fund(e) nicht erfasst ({>10 Funde|Rueckfall Pfad 1|Rueckfall Pfad 2|Schreibfehler}) — Befehle im Report` in Schritt 6; Log-Pfeil-Slot auf dieselbe Aufzaehlung; ersetzt `{V}`
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:801–802 — `{V}` undefiniert, `{S}` doppelt belegt (Schwelle vs. gefiltert)
Fix: ⏳-Zeile `{Schwelle}` statt `{S}`; `{V}` entfaellt mit F5
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:325 — Log-Format „{W} kann warten (Befehle im Report)", Kann-warten-Ideen werden aber geschrieben
Fix: `· {W} kann warten (Ideen ins Becken, Rest Befehle im Report)`
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:609 — `{K}` vor dem Kontrollpunkt gezaehlt; Punkte mit offener Zuordnung bekommen ⏳ erst danach → Anzeige zu niedrig
Fix: `{K}` = „⏳-Zeilen der neuen Liste, gezaehlt nach dem Kontrollpunkt"
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:637–638 — Duplikat-Zeile ohne Status und nur ein Treffer; `dtb:idea` `## Duplikat-Check` zeigt bis zu 3 Treffer mit Status
Fix: `… — dasselbe wie #{N} ({Status}) „{Bestand}"{ +N weitere}?`
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:408 — WORKFLOW_STATUS-Template zeigt `· behalten YYYY-MM-DD` als fuellbaren Platzhalter
Fix: `(seit YYYY-MM-DD[ · behalten YYYY-MM-DD — nur Altbestand])`
Decision: FIXED
