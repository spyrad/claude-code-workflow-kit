# Review-Snapshot: commit-and-push
Scope: skills/dtb-commit-and-push/SKILL.md, CLAUDE.md, skills/CLAUDE.md, skills/dtb-repo-sync/SKILL.md · Geprueft bis: `adffe01` (+ Doku `d428b45`) · Datum: 2026-07-16
Gesamt-Verdikt: NEEDS ATTENTION (7 non-blocking/nit Findings, alle in Triage behoben)

## Verdikt-Achsen
| Achse | Verdikt | Findings |
|-------|---------|----------|
| Plan Adherence | PASS | 0 |
| Scope Discipline | PASS | 0 |
| Safety & Quality | WARNING | 3 (F2, F5, F6) |
| Architecture | WARNING | 3 (F3, F4, F7) |
| Pattern Consistency | WARNING | 1 (F1) |
| Rules | PASS | 0 |

## Findings

### F1 — Pattern Consistency — [S:Mittel × I:Hoch] — principled
SKILL.md:149 — PowerShell-Here-String-Beispiel ohne `git -C {root}` → Fehl-Commit im falschen Repo (Multi-Root-Kernfall).
Fix: `git -C {root} commit -m @'…'@`.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel] — principled
SKILL.md:160-161 — Auffaelligkeits-Stopp „anders als letzte Pushes" nicht ableitbar (git hat keine Push-Historie).
Fix: ableitbare Trigger — mehr als ein Remote (`git remote`) ODER Ziel-Remote ≠ `origin`.
Decision: FIXED

### F3 — Architecture — [S:Niedrig × I:Mittel] — torvalds
SKILL.md:84-86 — Zustand clean & behind fiel durch kein Raster; Sonderzeilen ahead/up-to-date kuenstlich.
Fix: Commit/Push konditional gemacht (Commit nur wenn gestaged, Push nur wenn ahead/committet) → ahead/behind/up-to-date kollabieren in einen Pfad.
Decision: FIXED

### F4 — Architecture — [S:Niedrig × I:Mittel] — torvalds
SKILL.md:158 — Push-Preview `2>/dev/null` reines Bash, nicht shell-agnostisch.
Fix: Redirection entfernt (fehlender Upstream ist ueber Edge Case „kein Tracking-Branch" abgedeckt).
Decision: FIXED

### F5 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled
SKILL.md:43 — Argument „Name oder Pfad" + keine Config = undefiniert.
Fix: Aufloesung benannt (Pfad direkt; Name via config.repos; ohne Config als Pfad; sonst Abbruch).
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled
SKILL.md:100 — Red-Flag „> 1 MB" ohne Pruefmethode.
Fix: mechanische Methode ergaenzt (`ls-files` + `find -size +1M`/`wc -c`).
Decision: FIXED

### F7 — Architecture — [S:Niedrig × I:Niedrig] — torvalds (nit)
SKILL.md:129-133 — Kopplungs-Hinweis einseitig (Mitigation schwach).
Fix: reziproken Zeiger in `dtb:implement` P7 gesetzt; Hinweis in commit-and-push aktualisiert (Kopplung von beiden Enden sichtbar).
Decision: FIXED

## Info
6 Workflow-Artefakte im Diff, bekannt — nicht bewertet.
