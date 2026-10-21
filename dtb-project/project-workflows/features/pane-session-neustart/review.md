# Review-Snapshot: pane-session-neustart
Scope: CLAUDE.md, skills/CLAUDE.md, skills/dtb-{implement,pane-start,worker,workflow-checkpoint,workflow-resume}/SKILL.md · Geprueft bis: `1095623` · Datum: 2026-10-21
Gesamt-Verdikt: NEEDS ATTENTION

Vorlauf: erster Review-Lauf (bis `ef74cac`, REJECTED) — 10 Findings, alle FIXED in `1095623`.

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
### F1 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:80-81, skills/CLAUDE.md:350 — Ende-Kriterium sucht `**Gesamt-Verdikt:** REJECTED` (fett), review.md schreibt ohne Fett; REJECTED bleibt zudem nach erledigter Triage stehen
Fix: Kriterium „review.md traegt kein `Decision: PENDING` mehr"
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-workflow-checkpoint/SKILL.md:98-112 — Schreib-Nachweis prueft nur die Ueberschrift; eingerueckte EOF-Marke, `EOF` im Inhalt, zwei Wechsel in derselben Minute rutschen durch
Fix: Delimiter `DTB_NOTIZ_EOF`; GESCHRIEBEN nur bei +1 `## Wechsel` und letzter Zeile `Naechster Befehl:`; Satz „ohne Listen-Einrueckung ausfuehren; keine Statuszeile = SCHREIBFEHLER"
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-worker/SKILL.md:468-474 — `ERZEUGT` gilt als stilles OK; nie gesendeter Block wird beim Abbau mitgeloescht
Fix: bei ERZEUGT pruefen, ob ein WORKTREE-HANDOFF fuer den Slug in dieser Orchestrator-Session eingetroffen ist, sonst ⚠
Decision: FIXED

### F4 — Safety & Quality — [S:Niedrig × I:Mittel]
skills/dtb-workflow-checkpoint/SKILL.md:115 — Ende-Zweig liest die Notiz nur per Hinweis `cat "$N"`
Fix: woertlicher Lese-Block mit eigener Pfad-Aufloesung
Decision: FIXED

### F5 — Architecture — [S:Niedrig × I:Mittel]
skills/dtb-workflow-resume/SKILL.md:68-72 — bei ERZEUGT entfallen auch Rolle und Orchestrator (Nacharbeit nach „Ende" startet ohne Rollen-Kontext)
Fix: bei ERZEUGT Rolle + Orchestrator (mit Adress-Pruefung) zeigen, nur „Offen …" weglassen
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-workflow-resume/SKILL.md:113-118 — Kopplungs-Hinweis nennt `### Pane-Auftrag`, `herdr agent get` steht in `### Pane-Ausfuehrung`
Fix: beide Sektionen nennen
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-worker/SKILL.md:472-473 — NOTIZ-UNGEPRUEFT-Hinweis empfiehlt den gerade gescheiterten Befehl
Fix: `$(git rev-parse --git-common-dir)/worktrees/$(basename "{pfad}")/dtb-session-uebergabe.md` (Name meist = Ordnername)
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-worker/SKILL.md:187-189 — Ausnahme (2) endet mit Doppelpunkt, Worker-Vorlage liest sich als Resume-Teil
Fix: Liste mit Punkt beenden, Vorlage eigens einleiten
Decision: FIXED

### F9 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-pane-start/SKILL.md:348 — Reihenfolge-Kurzfassung des Abschlusses ohne Notiz-Pruefung
Fix: „Notiz-Pruefung → " vorne ergaenzen
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-workflow-resume/SKILL.md:90-93 — Vorrang des Notiz-Befehls nur fuer Fall A definiert
Fix: Satz in Schritt 2a: in Fall B/C steht der Befehl im Abschnitt Pane-Uebergabe
Decision: FIXED

Unterhalb des Caps (nicht triagiert): skills/CLAUDE.md „derzeit nur pane-start" unter der Kategorien-Tabelle missverstaendlich; pane-start:277-279 Persistenz-Verzicht ohne Hinweis auf die Notiz (T8).
