# Review-Snapshot: idea-rank-schiene
Scope: skills/dtb-idea-rank, dtb-idea-review, dtb-worker (SKILL.md), CLAUDE.md, README.md, features/idea-rank-schiene/beispiel-ausgabe.md · Geprueft bis: `b78bc08` · Datum: 2026-10-29
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | FAIL |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Hoch × I:Hoch]
skills/dtb-idea-rank/SKILL.md:139-140 — Anker der Dreier-Weiche ist als Regex ungueltig; das Grep-Werkzeug hat keinen woertlichen Modus, Bash ist nicht erlaubt (allowed-tools) → Werkzeugfehler, die ganze Spalte „Schiene" zeigt `?`
Fix: Anker-Tabelle traegt fertige, escapte, mit `^` verankerte Regex-Muster (ohne `$`, CRLF): `^\*\*Ausarbeiten \(2\) — Dreier-Weiche \(Groesseneinschaetzung\):\*\*` und `^### Schritt 2: Urteil je Eintrag \(Bewertungsraster: Worker-Tauglichkeit\)`
Decision: FIXED

### F2 — Architecture — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:140, 147, 303-307 — Check prueft die Fett-Zeile mit Menue-Nummer „(2)", 4.5 haengt aber an den Tabellenzeilen-Namen und an `**Urteil:**`; Umbenennung bleibt gruen, Umnummerierung wird rot; „Abschnitt unter dem Anker lesen" hat kein Ende
Fix: Anker-Tabelle um `^\| Operative Aufgabe \|`, `^\| Kleines Feature \|`, `^\| Sonst \|` (idea-review) und `^\*\*Urteil:\*\*` (worker) ergaenzen; Lese-Ende = Tabellenende bzw. Urteilszeile
Decision: FIXED

### F3 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-idea-rank/SKILL.md:144-145 — Aufloesung installierte Kopie zuerst; die juengeren Checks lesen die Repo-Fassung zuerst (dtb-workflow-checkpoint/SKILL.md:499, „Stand von gestern"); im Kit-Repo rankt idea-rank sonst nach veralteten Regeln
Fix: zuerst `skills/dtb-*/SKILL.md`, dann `~/.claude/skills/…`, mit der Ein-Satz-Begruendung aus workflow-checkpoint
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:160-162 — Werkzeugfehler-Meldung erbt aus Fall 2 die Abhilfe „an die neue Struktur anpassen" — falsche Abhilfe
Fix: eigene Zeile `⚠ Struktur-Check: {Quelle} nicht lesbar (Werkzeugfehler, kein Befund) — Einstufung als „?" → Lauf wiederholen`
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:373-374 — Beispiel `Worker: Zielzustand nicht mechanisch pruefbar` widerspricht dem Raster (`teilweise` = eine Luecke, die EINE kurze Antwort schliesst)
Fix: Beispiel `Worker: Scope offen (Stelle nennen)` aus Probelauf (d)
Decision: FIXED

### F6 — Plan Adherence — [S:Mittel × I:Niedrig]
features/idea-rank-schiene/spec.md:24, 26, 35 — Spec nennt noch „sonst `—`" und „Grundsatzfrage → Default Voll-Schiene"; ersetzt durch die Gate-Entscheidungen (beispiel-ausgabe.md:60, 80)
Fix: die drei Stellen angleichen (Task, eine Spalte) mit Verweis auf beispiel-ausgabe.md
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:314 — Ueberschrift „Mehrere Phasen sind nie Fast-Track" falsch (2 Phasen erlaubt)
Fix: „Mehr als zwei Phasen sind nie Fast-Track"
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:147-148 — Erfolg ohne Ausgabe, Geschwister melden `🧩 Struktur-Check`; Schweigen unbegruendet
Fix: ein Satz Begruendung (strenge Vorlage — der Check meldet sich nur im Fehlerfall)
Decision: FIXED

### F9 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:343 — Vorlage nennt ⚠-Zeilen „aus Schritt 2 und 3a", Schritt 3 gibt auch eine aus
Fix: „aus Schritt 2, 3 und 3a"
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-idea-rank/SKILL.md:152-153 — „Je Fall genau eine Hinweiszeile" mehrdeutig bei Ausfall beider Quellen
Fix: „je betroffener Quelle genau eine Hinweiszeile"
Decision: FIXED
