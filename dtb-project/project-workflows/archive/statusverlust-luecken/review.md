# Review-Snapshot: statusverlust-luecken
Scope: DERIVED_STATE_RULES.md, 11 Skills (archive, backlog-status, idea-rank, idea-review, project-health, project-init, task, workflow-checkpoint, workflow-next, workflow-resume, workflow-status), CLAUDE.md, README.md, workflow.config.yaml, beispielausgaben.md, probelaeufe.md · Geprueft bis: `83b4ce2` · Datum: 2026-09-23
Gesamt-Verdikt: NEEDS ATTENTION

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Hoch]
DERIVED_STATE_RULES.md §10.3 + §10-Block in workflow-resume/workflow-next/backlog-status (Zustand 3) — `frisch` ohne n-Pruefung: Branch mit Commits gegenueber dem Hauptbranch erscheint als `frisch` (Reflog fehlt/abgelaufen, Abzweig vor dem Hauptbranch), „+n Commits" verschwindet.
Fix: zuerst n pruefen — n > 0 → laufend; n = 0 und Reflog > 1 → gemergt; sonst frisch.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:173/487 gegen §9.2 — harte 60-80-Zeilen-Grenze ohne Vorrangregel gegenueber „nie still streichen"; bei Ueberlauf kuerzt das Modell still.
Fix: `## Offene Aufgaben` hat Vorrang vor der Zeilengrenze; Abbau nur ueber die ⏳-Vorlage (§9.1 + Kopie, ohne Zeilenzuwachs).
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-workflow-next/SKILL.md:184/231 — „Change fehlt"-Zeilen ganz am Ende bei 15-Zeilen-Limit; ab ~7 Items abgeschnitten und wieder unsichtbar.
Fix: Sammelzeile `{K} Ideen Ausgearbeitet, Change fehlt → /dtb:project-health`, zaehlt nicht aufs Limit.
Decision: FIXED

### F4 — Architecture — [S:Mittel × I:Mittel]
§10-Block in den 3 Sichten — „Kommando scheitert → Block entfaellt still" (nicht im Kanon §10.1); ein geschluckter git-Fehler macht Worktree-Arbeit unsichtbar.
Fix: genau eine Zeile `In Worktrees: nicht lesbar ({Fehler})`, in Kanon und Kopien.
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:491 — Archiv-Hinweis zaehlt jedes `Ausgearbeitet` als archivierbar, widerspricht §8.
Fix: nur `Ausgearbeitet` mit gueltigem Change-Link (§8) zaehlen, in derselben Zeile.
Decision: FIXED

### F6 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-task/SKILL.md:68 — `/dtb:task {N}` uebergibt eine Nummer, Schritt 1 behandelt sie als Freitext („zu knapp").
Fix: reine Zahl als Argument → INBOX-Zeile #N als Beschreibung laden (Herkunft fuer 4b merken).
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Mittel]
DERIVED_STATE_RULES.md §10.3 `gemergt` — Squash-/Rebase-Merges werden nie erkannt, Worktree bleibt `laufend` mit ⏳.
Fix: Grenze in §10.3 benennen („squash-gemergt → bleibt laufend, Mensch raeumt auf").
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Mittel]
DERIVED_STATE_RULES.md §9.3 + Checkpoint-Kopie — „ersetzt (auch 1:1)" ohne Kriterium; Folgeschritt kann faelschlich das alte `seit` erben.
Fix: „ersetzt" nur bei ausdruecklich genannter Abloesung; sonst erledigt + neu; bei Unsicherheit Rueckfrage.
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
DERIVED_STATE_RULES.md §10.3 + 3 Kopien — „aelter als" (>) vs. §9.4/Config/project-init (≥) beim selben Key.
Fix: §10 auf „≥ `status.alter_schwelle_tage` Tage" angleichen.
Decision: FIXED

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig]
plan.md Schritt 1.3 — Fortschritt laut Plan per `git show {branch}:…`, umgesetzt aus dem Worktree-Pfad (abgenommen in Beispiel (a)), aber nicht als Abweichung vermerkt.
Fix: Satz in probelaeufe.md ergaenzen (Plan-Block bleibt read-only).
Decision: FIXED
