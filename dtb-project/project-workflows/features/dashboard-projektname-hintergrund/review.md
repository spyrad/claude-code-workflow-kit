# Review-Snapshot: dashboard-projektname-hintergrund
Scope: skills/dtb-project-dashboard/SKILL.md, features/dashboard-projektname-hintergrund/plan.md · Geprueft bis: `ece7ea3` · Datum: 2026-10-27
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | WARNING |
| Pattern Consistency | PASS |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality / Architecture — [S:Mittel × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:47 — Fallback-Name per `dirname` von `--git-common-dir` liefert im Submodul `modules` und bei `--separate-git-dir` einen falschen Ordner; rechnet zudem dasselbe wie Schritt 1 mit anderem Fehlerstil nach
Fix: Einzeiler ersetzen durch die erste Zeile von `git worktree list --porcelain` (immer der Haupt-Checkout): `W=$(git worktree list --porcelain 2>/dev/null | sed -n '1s/^worktree //p') && [ -n "$W" ] && basename "$W" || basename "$PWD"`
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:305–306 — langer Projektname ohne Umbruchstelle laeuft auf schmalen Viewports ueber und verdraengt den Theme-Schalter
Fix: `header > div { min-width: 0; }` ergaenzen, im `h1`-Stil `overflow-wrap: anywhere;`
Decision: FIXED

### F3 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:389 — Tab-Titel haengt am ersten `h1` im Dokument, das uebrige Skript greift per ID zu
Fix: `<h1 id="projekt">` und `document.getElementById('projekt')`
Decision: FIXED

### F4 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:269 — dunkle Raster-Tokens als `hsl(…)` mit sechs Nachkommastellen, Rest des Blocks Hex
Fix: `#adc4eb02` / `#adc4eb07` / `#adc4eb13`
Decision: FIXED

### F5 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:276 — helle Vignette `#ebe7e426` ist eine Kopie der Seitenfarbe mit Alpha, zieht bei Aenderung nicht mit
Fix: `--vignette: color-mix(in srgb, var(--page) 15%, transparent);` (nur hell)
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:245 — Slot-Liste nennt `{{PROJEKT}}` vor `{{STAND_DATUM}}`, im Geruest umgekehrt
Fix: Reihenfolge in der Slot-Liste tauschen
Decision: FIXED

### F7 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:288 — `background-color: var(--page)` in `body::before` wirkt doppelt zu `html`, haelt aber die Kreuz-Maske farbgleich
Fix: Kurzkommentar `/* gleiche Farbe wie die Kreuz-Maske */`
Decision: FIXED
