# Review-Snapshot: plan-review-subagenten
Scope: skills/dtb-plan-review/SKILL.md, skills/dtb-project-init/SKILL.md, workflow.config.yaml, agents/CLAUDE.md, CLAUDE.md, README.md (+ plan.md) · Geprueft bis: `5f9e7c1` · Datum: 2026-11-27
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-plan-review/SKILL.md:43 — Formal-Check `## Progress` soll „als Finding in Runde 2" erscheinen, der Haupt-Skill darf den Runden aber nichts mehr hinzufuegen; ohne eigene Kopfzeile kann der Befund spurlos verschwinden
Fix: Kopfzeile `📋 Formal-Check Progress: {ok | Befund}` im Output-Format neben 🔎/⚔; :43 auf „→ Kopfzeile + Input der Rollen-Runde 2 (3a)" umformulieren
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Hoch]
skills/dtb-plan-review/SKILL.md:224-227 — Verdikt fuer fremde Dimension erzwingt Rueckfall in den Hauptkontext (Isolationsverlust), Einspruch gegen Nicht-Dimension wird tolerant zum Hinweis — gegensaetzliche Behandlung gleich schwerer Fehlformen
Fix: Verdikt fuer fremde Dimension als `EINSPRUCH {Dimension}: {Satz}` uebernehmen, kein Rueckfall; Rueckfall nur bei fehlendem eigenen oder widerspruechlichem Verdikt
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-plan-review/SKILL.md:266-269 — Einspruch-Reaktion ungeregelt, wenn die zustaendige Rolle den Punkt weder abdeckt noch widerlegt
Fix: Default „→ `bestaetigt — von {Rolle} nicht behandelt`" (billigerer Fehler)
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-plan-review/SKILL.md:224-230 — Unbrauchbar-Liste prueft nur Verdikt-Defekte; Rueckgabe ohne RUNDE 3 gilt als verwertbar
Fix: „fehlende `RUNDE 1`–`RUNDE 3`" in die Unbrauchbar-Liste
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-plan-review/SKILL.md:224-231 — jeder Rueckfall laeuft sofort im Hauptkontext, der alle anderen Rueckgaben kennt
Fix: einmal erneut dispatchen (gleicher Auftrag + Formfehler-Hinweis), erst beim zweiten Fehlschlag Hauptkontext; ⚠-Zeile `(nach Neustart)`
Decision: FIXED

### F6 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-project-init/SKILL.md:137 — Regeln-Liste ohne Eintrag fuer den optionalen Block `plan_review.modelle`
Fix: Eintrag „Optional (Default `null` = Session-Modell erben …; unbekannt → erben + ⚠, `dtb:plan-review` Schritt 0)"
Decision: FIXED

### F7 — Architecture — [S:Mittel × I:Niedrig]
skills/dtb-plan-review/SKILL.md:250-255 — Dimensions-Zuordnung dreifach (Rollen-Tabelle, Schritt-4-Tabelle, Output-Tabelle), Schreibweise `Scope/MVP-Schnitt` vs. `Scope / MVP-Schnitt` (:427)
Fix: Schritt-4-Tabelle durch Verweis auf die Rollen-Tabelle ersetzen, Output-Schreibweise angleichen
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-plan-review/SKILL.md:33-34 — unbekannter Schluessel und unbekannter Wert teilen eine Meldung; Tippfehler im Schluessel meldet falschen Wert, Zielrolle erbt still
Fix: eigene Zeile `⚠ plan_review.modelle.{schluessel}: Schluessel unbekannt (erwartet: architekt, pragmatiker, senior-dev, betriebs-waechter) — ignoriert`
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Mittel]
agents/{architekt,pragmatiker,betriebs-waechter}.md:17, agents/senior-dev.md:18 — „in der Review-Zusammenfassung … (Regel im Skill)" passt nicht mehr zum Subagenten-Prompt
Fix: „in seinen Verdikt-Zeilen" / „(Form im Auftrag)"
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-plan-review/SKILL.md:235-236 vs. :468 — Streichverbot in 3d widerspricht der Kappung auf 3 Fragen
Fix: 3d: „ueber 3 Fragen → die ersten 3, `⚠ Rolle {Rolle}: {n} Fragen, auf 3 gekappt`"
Decision: FIXED

(4 weitere Findings unterhalb des Caps: Explore-Begruendung, Lektionen-Slot-Form, Warte-Regel harness-neutral, Begriffs-Mischung — erneut ausfuehren nach Behebung)
