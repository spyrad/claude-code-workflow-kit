# Review-Snapshot: opportunity-map
Scope: dtb-opportunity-map/SKILL.md (NEU) · dtb-pipeline-graph, dtb-greenfield-prd, README, CLAUDE.md · spec.md (SC-Abschluss) · Geprueft bis: `c0b0c0f` · Datum: 2026-07-18
Gesamt-Verdikt: NEEDS ATTENTION

Dimensionen: Drift alle MATCH (kein EXTRA) · Craft 5 Findings (0 blocking) · Rules uebersprungen (keine Coding-Rules) · SHA-Check: 3.3 committet (c0b0c0f), aber SHA nicht in Progress-Zeile zurueckgeschrieben
Lektionen-Prior: #1, #2 (Legacy-Alias code-review) beruecksichtigt — kein Treffer im Scope

## Findings

### F1 — Safety & Quality / Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-opportunity-map/SKILL.md:231 — Selbst-Review-Struktur-Check (Hard-Block) listet Sektion `## Naechste Richtung`, das Template (Z.215) erzeugt aber `## Naechste Richtung, falls wertvoll`. Der Kontrakt-Check prueft gegen einen Namen, den das eigene Template nicht traegt.
Fix: In Z.231 `## Naechste Richtung` → `## Naechste Richtung, falls wertvoll` (exakt wie Template Z.215).
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-opportunity-map/SKILL.md:259 — Hand-off (Schritt 5) verzweigt „je nach Richtung des Kandidaten" (build/buy/complement/wait). Der kandidatenlose Ausgang „Kein Bau empfohlen" (Schritt 3 Z.157 / Template Z.210) hat keinen zutreffenden Hand-off-Zweig — gebrochener Kontrakt (jeder gueltige Ausgang braucht ein Hand-off-Verhalten).
Fix: In Schritt 5 einen Fall „Kein Bau empfohlen" ergaenzen (analog buy/wait: welches bestehende Tool zuerst, kein PRD).
Decision: FIXED

### F3 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-opportunity-map/SKILL.md:69-72 — Quellmaterial-Glob (Schritt 1) schliesst PRD-MVP/ROADMAP/TECH-STACK aus, aber NICHT die eigene Ausgabe `OPPORTUNITY-MAP.md`. Beim Kollisions-/Zweitlauf (Schritt 4c vorgesehen) wird die eigene fruehere Map als frisches Ausgangsmaterial angeboten → Anchoring. greenfield-prd schliesst seine eigene Ausgabe PRD-MVP.md konsequent aus (Muster ueber Distanz).
Fix: Ausschlussliste in Schritt 1 um `OPPORTUNITY-MAP.md` ergaenzen.
Decision: FIXED

### F4 — Plan Adherence — [S:Niedrig × I:Niedrig]
plan.md `## Progress` Zeile 3.3 — geflippt, aber ohne SHA-Rueckschreibung. Die Arbeit (kit-sync + SC1–9-Abschluss) ist in `c0b0c0f` committet; die Zeile traegt den Verifikations-Beleg nur nicht (§2 Regel 4: SHA am Phasen-Ende nachtragen). Gate nachweislich durchlaufen — reiner Beleg-Nachtrag.
Fix: In plan.md 3.3-Zeile ` — `c0b0c0f`` anhaengen.
Decision: FIXED

### F5 — Architecture — [S:Niedrig × I:Niedrig] (nit)
skills/dtb-opportunity-map/SKILL.md:15 — Pipeline-Reziprozitaet einseitig: `opportunity-map.next = [dtb:greenfield-prd]`, aber `greenfield-prd.after = null`. Plausibel gewollt (optionales Vorfeld, greenfield-prd soll ohne Map lauffaehig bleiben, kein geerbtes Hard-Gate) — daher nit.
Fix (nur falls Reziprozitaet gewuenscht): einseitigen Vorfeld-Edge bewusst dokumentieren ODER `greenfield-prd.after` konsistent nachziehen (Hard-Gate-Ableitung mitdenken). Sonst SKIP.
Decision: SKIPPED (bewusst einseitig — greenfield-prd bleibt ohne Map lauffaehig, kein geerbtes Hard-Gate)

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig] (nit)
skills/dtb-opportunity-map/SKILL.md:245,250 — Cross-Skill-Drift zum gekoppelten greenfield-prd: „(Empfohlen)" hier vs. „(Recommended)" dort; Archivpfad hier voller Prefix `dtb-project/project-strategy/archive/…` vs. dort `project-strategy/…`. In DIESER Datei ist beides intern konsistent und die sauberere Variante — Fix gehoert bei naechster Beruehrung in greenfield-prd, nicht in den Neubau.
Fix: Keiner in dieser Datei; bei naechster greenfield-prd-Beruehrung angleichen. Empfehlung: SKIP hier.
Decision: SKIPPED (Angleichung gehoert bei naechster Beruehrung in greenfield-prd)
