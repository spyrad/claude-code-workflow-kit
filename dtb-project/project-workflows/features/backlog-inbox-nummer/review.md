# Review-Snapshot: backlog-inbox-nummer
Scope: skills/dtb-{project-init,feature-plan,feature-fast,task,bug-report,workflow-checkpoint,backlog-status}/SKILL.md, DERIVED_STATE_RULES.md, features/backlog-inbox-nummer/{discovery,spec,plan}.md · Geprueft bis: `06b8b6e` · Datum: 2026-10-06
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:455/464, DERIVED_STATE_RULES.md:182 — unklar, ob `—` als fehlend gilt; woertlich ist ein einmal geschriebenes `—` endgueltig, eine spaeter verlinkte Idee wird nie nachgefuellt
Fix: „`—`, leer oder fehlend = kein Wert → bei jedem Lauf neu ableiten; eine Zahl wird nie ueberschrieben" (Checkpoint + DSR)
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:455-463 — Quellen-Reihenfolge (INBOX vor ARCHIVE_LOG) kollidiert mit „kleinste Nummer"; Ergebnis haengt vom Archivierungszeitpunkt ab und bleibt dauerhaft
Fix: Treffer aus INBOX und ARCHIVE_LOG vereinigen, dann kleinste Nummer; `—` nur ohne jeden Treffer
Decision: FIXED

### F3 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-feature-fast/SKILL.md:256-257 — „wie dort" grammatisch mehrdeutig, Literal in feature-plan traegt `Spezifiziert` statt `Geplant`; einziger Schreiber ohne Inline-Literal
Fix: Literal `| {INBOX-Nr oder —} | {Feature-Name} | Geplant | {Prio} | features/{slug}/spec.md | {Ziel} |` + Alt-Kopf-Klausel woertlich inline
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:453-456 — einzelne Altformat-Zeile unter neuem Kopf wird nicht erkannt; Feature-Name landet als „vorhandene" Nummer in der #-Zelle
Fix: Zellen je Zeile zaehlen; weniger Zellen als der Kopf → erste Zelle voranstellen und ableiten
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-bug-report/SKILL.md:212, DERIVED_STATE_RULES.md:180 — „Bugs immer `—`" widerspricht DSR §8 (Idee darf auf bug.md verlinken); Alt-Kopf-Klausel im Wortlaut abweichend
Fix: „`—` als Startwert, Checkpoint fuellt nach, falls eine Idee auf bug.md verlinkt"; Klausel-Wortlaut angleichen
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:455-456 — Datei-Spalte `-`, `FEATURE_*.md`, Altlinks im ARCHIVE_LOG ungeregelt; Modell muesste Slug raten, Ergebnis dauerhaft
Fix: „Datei-Spalte ohne `features/<slug>/` bzw. `archive/<slug>/` → `—`, keinen Slug aus Altnamen raten"
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:451-466 — operative Kopie von DSR §3 ohne `Wartungs-Hinweis (Format-Kopplung)`, anders als die §9-/§8-Kopien
Fix: Wartungs-Hinweis im gleichen Format mit Grep-Anker `Spalte \`#\` in BACKLOG.md`
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:451-452, DERIVED_STATE_RULES.md:179 — „alle vier Tabellen" uebersieht den Alt-Abschnitt „Bugs" (dtb:archive kennt ihn)
Fix: „alle Tabellen mit Datei-Spalte (die vier Standardtabellen, ggf. Alt-Abschnitt „Bugs")"
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-backlog-status/SKILL.md:133 — `- #{Nr} {Feature}` ergibt bei `—` „#—"
Fix: „`#{Nr} ` nur bei Zahl, sonst weglassen"
Decision: FIXED

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig]
dtb-project/project-workflows/features/backlog-inbox-nummer/discovery.md:51 — Randfall nennt noch „offener Punkt, siehe unten", obwohl geklaert
Fix: „→ kleinste Nummer (geklaert im plan-review 2026-10-06)"
Decision: FIXED
