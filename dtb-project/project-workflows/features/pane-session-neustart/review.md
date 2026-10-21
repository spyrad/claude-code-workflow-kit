# Review-Snapshot: pane-session-neustart
Scope: CLAUDE.md, skills/CLAUDE.md, skills/dtb-{implement,pane-start,worker,workflow-checkpoint,workflow-resume}/SKILL.md · Geprueft bis: `ef74cac` · Datum: 2026-10-21
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | PASS |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | PASS |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:82-84, 99-100 — Schreib-Bloecke (Abschnitt anhaengen, Ende-Marker) nicht woertlich vorgegeben; bei fehlgeschlagener Pfad-Aufloesung erscheint trotzdem `→ Uebergabe-Notiz`, nach `/clear` ist die Notiz still verloren
Fix: beide Schreib-Bloecke woertlich vorgeben, `exit 1` bei fehlendem Pfad, nach dem Schreiben per grep pruefen; Erfolgszeile nur bei GESCHRIEBEN
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-worker/SKILL.md:466-480 — Pruefung auf ungesendete Notiz erst in Punkt 4 (nach Merge und Checkpoint); Ungemeldetes fehlt schon in Abnahme und Log
Fix: Pruefung vor Punkt 1 (Merge) ziehen
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:183, 209 — Zeitstempel in `## Wechsel …`/`## Ende-Block erzeugt …` fuellt das Modell, das die Uhrzeit nicht kennt
Fix: Ueberschrift per Shell schreiben (`printf … "$(date '+%Y-%m-%d %H:%M')"`), Ende-Marker ebenso
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:472 — Aufloesungsfehler meldet `KEINE-NOTIZ` (fail-open Richtung Datenverlust)
Fix: eigenes Token `NOTIZ-UNGEPRUEFT` mit derselben ⚠-Zeile wie UNGESENDET
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:90-91 — „plus die aktuelle Session" unscharf; Weiterarbeit ohne `/clear` nach Wechsel/Ende fuehrt zu doppelten Inhalten beim Orchestrator
Fix: „aktuelle Session" = seit dem letzten in diesem Verlauf geschriebenen Abschnitt/Marker, sonst ab Session-Beginn
Decision: FIXED

### F6 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-workflow-resume/SKILL.md:68, skills/dtb-worker/SKILL.md:475 — Token `GESENDET` behauptet Zustellung, belegt ist nur „erzeugt"
Fix: Token in `ERZEUGT` umbenennen
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Mittel]
checkpoint:62-64, resume:59-70, worker:472-475 — Pfad-Aufloesung in drei, Marker-Erkennung in zwei Varianten
Fix (angepasst in der Sammelliste): dieselbe `case`-Fallunterscheidung auch im Checkpoint-Lese-Block (`ZUSTAND OFFEN|ERZEUGT`), Kopplungs-Hinweis mit Grep-Zielzahl 3; Fehlerpfade bleiben bewusst verschieden (F1/F4)
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-pane-start/SKILL.md:324-325 — „am Session-Ende" veraltet, Block entsteht nur bei „Ende"
Fix: „bei der Wahl „Ende""
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
resume:85 vs. checkpoint:95-97 — `Uncommittet:` unterschiedlich gelesen
Fix: Regel ins Notiz-Format (juengster Abschnitt = Momentaufnahme), beide Leser verweisen
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-checkpoint/SKILL.md:46 vs. :55 — „nichts schreiben" im Guard-Bullet vs. Notiz-Schreiben
Fix: Satz: „nichts schreiben" heisst hier keine Datei im Arbeitsbaum
Decision: FIXED
