# Review-Snapshot: implement-ohne-feature-start
Scope: 12 Dateien (skills/dtb-implement, dtb-feature-start, dtb-plan-review, dtb-impl-plan, dtb-workflow-{next,checkpoint,status,resume}, dtb-pipeline-graph, skills/CLAUDE.md, README.md, CLAUDE.md) aus 0701707, d5c592d, 52efdd8 (Folgelauf nach Triage) · Geprueft bis: `52efdd8` · Datum: 2026-11-10
Gesamt-Verdikt: NEEDS ATTENTION
Vorlauf: Erstlauf bis `d5c592d` — 8 Findings, alle FIXED in `52efdd8`

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-workflow-status/SKILL.md:212 — `Bugs (In Arbeit) → /dtb:implement` widerspricht dem Erstlauf-Fix F1 (Bugs haben kein plan.md, implement-Gate); Gegenprobe fand die Zeile nicht (kein „feature-start" darin).
Fix: Zelle auf `naechsten Fix-Schritt umsetzen` (wie workflow-next).
Decision: FIXED

### F2 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-implement/SKILL.md:60-64 — Gruppe „In Arbeit" zeigt bei Altplaenen ohne Statusfeld `Plan: Entwurf`; Review-Stand hat laut §7.3-Guard-Pflicht nur bei 0/Y Aussagekraft.
Fix: Review-Stand nur in „Geplant" und „Progress fehlt" zeigen; in der „In Arbeit"-Vorlage `, Plan: {…}` streichen.
Decision: FIXED

### F3 — Architecture — [S:Niedrig × I:Mittel]
skills/dtb-implement/SKILL.md:54-59 — „Progress fehlt" nimmt auch laengst umgesetzte, nie archivierte Altplaene dauerhaft auf; erster Kandidaten-Satz widerspricht der Erweiterung.
Fix: Kandidaten einmal umfassend definieren (offene Zeile ODER Progress fehlt/0 Zeilen) und Ordner mit explizitem Zustand §1.2 (`Abgenommen`/`Pausiert` im Kopf von spec.md) ausschliessen.
Decision: FIXED

### F4 — Pattern Consistency — [S:Niedrig × I:Niedrig]
dtb-project/project-rules/DERIVED_STATE_RULES.md:386-394 — §7.3 nennt als Leser nur workflow-next/-status; implement traegt eine Kurzkopie der Matrix, workflow-checkpoint liest per Referenz.
Fix: implement (Teilspiegel, nur Anzeige) und workflow-checkpoint (Referenz) als Leser in §7.3 ergaenzen, implement im Wartungs-Hinweis nennen.
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-plan-review/SKILL.md:46 — Laufzeit-Meldeblock sagt weiter „(einziger Erzeuger)".
Fix: `(Erzeuger; auch via /dtb:feature-plan oder /dtb:feature-fast)`.
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md (Frontmatter after) — feature-start fehlt, obwohl alle anderen Skills mit `next: [dtb:workflow-checkpoint]` dort stehen.
Fix: `dtb:feature-start` in `after` von workflow-checkpoint ergaenzen.
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/CLAUDE.md:327,352 — Zeile J steht vor I, fehlt in der Legende, Datum in der Spalte „Frueher".
Fix: J hinter I, Zelle `— (neu)`, Legende um „J = Zusatz `implement-ohne-feature-start` 2026-11-10" ergaenzen.
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-implement/SKILL.md:48-50 — „auch wenn das Argument nur `phase N` ist → Auswahl" ist bei eindeutigem Kontext mehrdeutig.
Fix: „Ist das Argument nur `phase N`, gilt es als Phase, nicht als Slug; der Slug kommt dann aus dem Kontext, sonst → Auswahl."
Decision: FIXED
