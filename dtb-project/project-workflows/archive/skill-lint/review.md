# Review-Snapshot: skill-lint
Scope: scripts/lint-skills.py, scripts/tests/test_lint_skills.py, .github/workflows/lint-skills.yml, skills/dtb-project-health/SKILL.md, CLAUDE.md, skills/CLAUDE.md, .gitignore, 7 Skill-Frontmatter (17 Dateien, 2 Commits) · Geprueft bis: `5812e39` · Datum: 2026-11-26
Gesamt-Verdikt: NEEDS ATTENTION

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
### F1 — Safety & Quality — [S:Hoch × I:Mittel]
scripts/lint-skills.py:173-181 — Laengenregel nur bei `disable-model-invocation is False`; fehlendes Feld, String `"false"` oder anderer Nicht-Bool rutschen durch, obwohl die Beschreibung dann in jede Session geladen wird (Falsch-Negativ der Zielklasse).
Fix: Nicht-Bool als FEHLER `dmi-typ`; Laengenpruefung bei `data.get("disable-model-invocation", False) is not True`; Tests fuer „fehlt" und `"false"`.
Decision: FIXED

### F2 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-project-health/SKILL.md:218-224 — Die Restpruefungen nach dem Skript scannen `.claude/skills/dtb-*`, das es im Kit-Repo nicht gibt — sie laufen dort ueber null Dateien.
Fix: Im Absatz festlegen: im Kit-Repo laufen die Restpruefungen ueber `skills/dtb-*/SKILL.md`.
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
scripts/lint-skills.py:208-230 — Kantenfeld als String statt Liste erzeugt zusaetzlich einen falschen FEHLER `gegenkante` beim Ziel-Skill.
Fix: In `check_edges` die Gegenkanten-Pruefung ueberspringen, wenn das Gegenfeld weder Liste noch null ist.
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig]
scripts/lint-skills.py:126-127, 263-273 — Unerwartete Ausnahmen enden mit Exit 1 (= „FEHLER gefunden") statt 2; `lint()` ruft selbst `sys.exit(2)`.
Fix: `lint()` wirft `UsageError`; `main()` faengt `UsageError` und `Exception`, schreibt nach stderr, gibt 2 zurueck.
Decision: FIXED

### F5 — Architecture — [S:Mittel × I:Niedrig]
scripts/lint-skills.py:252-253 — Skip „fremder Baum" ist ein Test-Sonderfall in der Produktivlogik und macht eine Ausnahme stumm, wenn beide Skills verschwunden sind.
Fix: `lint(root, exceptions=EDGE_EXCEPTIONS)`; Tests uebergeben eine eigene Liste, Subprocess-Laeufe ueber einen Test-Einstieg; Skip und Global-Patch streichen.
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-project-health/SKILL.md:239 — Modell-Sicht stuft „Bash fehlt in allowed-tools" als WARNUNG ein, das Skript als FEHLER.
Fix: In der Modell-Sicht `Bash` bei Shell-Block oder Guard-Anker auf FEHLER heben (`Write` bleibt WARNUNG).
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Mittel]
scripts/tests/test_lint_skills.py:77-81 — `assert_finding` prueft nur Vorkommen, nicht Exklusivitaet (verdeckte F3); ungetestet: after-Seite der Gegenkante, Ausnahme auf `after`, `description` als Nicht-Text, `allowed-tools` als Liste, Zweig „Ausnahme deckt keine Kante" bei vorhandener Quelle.
Fix: Exakte Befundmenge pruefen (`assert_findings`) und die fehlenden Faelle ergaenzen.
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Niedrig]
scripts/lint-skills.py:61-62, 103-108 — Anker-/Werkzeug-Erkennung zu eng: kein `sh`/`shell`/`~~~bash`, kein `### Worktree-Guard`, `Bash(git:*)` gibt falschen FEHLER.
Fix: Fence-Regex `(?:```|~~~)(?:bash|sh|shell)\b`, Guard-Regex `^#{2,3} Worktree-Guard\b`, `tool_list` kuerzt auf den Teil vor `(`; Fence-Zitat als akzeptiertes Falsch-Positiv kommentieren.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
scripts/lint-skills.py:111-112, 226, 251-255 — `folded()` faltet jeden Leerraum statt nur Umbruch+Einrueckung; `kanten-ziel`-Detail enthaelt ein zweites ` — `; vertipptes Ausnahme-Feld nur WARNUNG.
Fix: `re.sub(r"\n[ \t]*", " ", …)`; `:` statt ` — ` im Detail; unbekanntes Feld als FEHLER `ausnahme-feld`.
Decision: FIXED

### F10 — Architecture — [S:Niedrig × I:Niedrig]
.github/workflows/lint-skills.yml:19 — `checkout@v4` legt das Token im Checkout ab, das der Job nicht braucht.
Fix: `with: persist-credentials: false`.
Decision: FIXED
