# Review-Snapshot: plan-in-einem-befehl
Scope: skills/dtb-feature-plan, skills/dtb-impl-plan, skills/dtb-feature-discover, CLAUDE.md, README.md, probelauf.md (+ plan.md) · Geprueft bis: `eef1b3a` · Datum: 2026-11-09
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-feature-plan/SKILL.md:24-26 — Einleitung sagt bei `nur-spec` „endest du nach der Spec", Punkt 8a(a) sagt „weiter mit Punkt 9"; ein frisches LLM koennte INBOX/BACKLOG/Bestaetigung (Punkt 9–11) auslassen.
Fix: Einleitung umformulieren: „…ueberspringst du den Plan-Teil (Punkt 8a); Punkt 9–11 laufen normal, naechster Schritt `/dtb:impl-plan`".
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-feature-plan/SKILL.md:224-233, 260-262, 294-301 — Ausgang haengt am Pfad statt am Artefakt: lehnt der Mensch die Ueberschreib-Frage bei vorhandenem plan.md ab, meldet Punkt 11 faelschlich „Implementierungsplan gespeichert"; bei „aktualisieren" eines Plans mit Haken traegt Punkt 10 `Geplant` statt des abgeleiteten Status ein.
Fix: Ausgang an das Artefakt binden („Durchlauf ⇔ plan.md wurde in diesem Lauf geschrieben"); `{Status}` nach DERIVED_STATE_RULES aus vorhandenen Dateien + `## Progress` ableiten (Geplant/Spezifiziert als Normalfall-Beispiele).
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-feature-plan/SKILL.md:219-228 — `## Wichtig - Anweisungen fuer die Ausfuehrung` existiert in beiden Dateien, und „Slug-Ermittlung"/„eigene Bestaetigung" passen auf beide; die Bindung an impl-plan haengt nur am Pronomen „ihre".
Fix: Explizit: „`## Wichtig - Anweisungen fuer die Ausfuehrung` der impl-plan-Datei (nicht der gleichnamige Abschnitt dieses Skills), ausgenommen deren Punkte **Feature-Name / Slug ermitteln** und **Bestaetige**".
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-feature-plan/SKILL.md:24-25 — Nicht festgelegt, dass `nur-spec` vor der Slug-Ableitung entfernt wird; der Freitext-Ausloeser „nur spec" trifft auch Feature-Namen mit diesen Woertern.
Fix: Festlegen: nur `nur-spec` als letztes Argument-Token zaehlt und wird vor der Slug-Ableitung entfernt; Freitext-Bitte zaehlt nur ausserhalb des Feature-Namens.
Decision: FIXED

### F5 — Architecture — [S:Niedrig × I:Mittel]
skills/dtb-feature-plan/SKILL.md:222-227 — Codebase-Research steht als eigener Listenpunkt UND wird ueber „alles aus Wichtig" (impl-plan Punkt 3) erneut gezogen → moeglicher zweiter Scan mit zweiter Bestaetigung.
Fix: Bei „aus Wichtig alles ausser …" ergaenzen: „…der Punkt Codebase-Research ist durch den Listenpunkt oben bereits erledigt".
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-feature-plan/SKILL.md:192-200 — „Anker woertlich" widerspricht den Regex-Zellen (`^`, `\(`, `\.`); in BRE/`grep -F` ergaebe das Schein-Drift.
Fix: „Regex fuer das Grep-Werkzeug (ripgrep), zeilenverankert" statt „woertlich". (feature-fast nutzt fuer denselben Anker eine unverankerte Form — separater Change.)
Decision: FIXED

### F7 — Plan Adherence — [S:Niedrig × I:Niedrig]
skills/dtb-feature-plan/SKILL.md:250 — Spec: „INBOX-Link passt zum tatsaechlichen Ausgang"; Punkt 9 verlinkt in beiden Ausgaengen nur spec.md.
Fix: Im Ausgang Durchlauf zusaetzlich `→ features/{slug}/plan.md` anhaengen.
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-impl-plan/SKILL.md:296 — „Verwandte Commands" nennt `/dtb:feature-plan — Feature-Spec erstellen`; erzeugt jetzt standardmaessig auch plan.md (Verweis-Sweep stufte die Stelle als „bleibt richtig" ein).
Fix: „Feature-Spec erstellen (standardmaessig samt plan.md)"; Sweep-Zeile in probelauf.md nachziehen.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-impl-plan/SKILL.md:103, 86-87 — „Ausserdem wird er" bezieht sich auf „Diese Sektion" (→ „sie"); der Codebase-Research-Hinweis steht am Abschnittsende, die anderen vier direkt unter der Ueberschrift.
Fix: „er" → „sie"; Codebase-Research-Hinweis an den Abschnittskopf (Format-Kopplungs-Hinweis bleibt unten).
Decision: FIXED

## Triage-Abschluss (2026-11-09)

9 Fixed · 0 Lesson · 0 Skipped — alle per Sammelliste uebernommen.

Folge fuer ein Phase-1-Kriterium: Der Fix zu F8 aendert in `skills/dtb-impl-plan/SKILL.md` eine
Nicht-Hinweis-Zeile („Verwandte Commands"). Das Diff-Kriterium „impl-plan bekommt nur
Hinweis-Zeilen" zeigt seither genau diese eine Doku-Zeile — bewusst, per Review-Entscheid; das
Verhalten von impl-plan (alle Abschnitte, Template, Regeln) bleibt unveraendert. Alle uebrigen
Phase-1-/Phase-2-Kriterien nach den Fixes erneut gruen.
