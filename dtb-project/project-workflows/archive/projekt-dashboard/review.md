# Review-Snapshot: projekt-dashboard
Scope: CLAUDE.md, README.md, spec.md, skills/CLAUDE.md, skills/dtb-{project-dashboard,project-init,workflow-checkpoint,workflow-next}/SKILL.md, workflow.config.yaml · Geprueft bis: `8a59410` · Datum: 2026-10-27
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
### F1 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:168 — „Kuratierung faellig → INBOX #141" verweist auf die Kit-INBOX; in Zielprojekten falsche oder fehlende Idee (Laufzeit-Autarkie)
Fix: „Kuratierung faellig (Soft-Limit ~150 Zeilen, siehe /dtb:lesson)"
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:189 — Geruest-Kopie ueberschreibt die Zielseite direkt; Abbruch zerstoert die letzte gute Seite
Fix: in `project-dashboard.html.tmp` kopieren und fuellen, nach Null-Slot-Check per `mv` ersetzen
Decision: FIXED

### F3 — Pattern Consistency — [S:Mittel × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:144, 187; skills/dtb-workflow-checkpoint/SKILL.md:714 — Quelle installiert zuerst, Checkpoint Schritt 0 Repo zuerst; im Kit-Repo kopiert ein Probelauf still das alte Geruest
Fix: A (Empfehlung) Repo zuerst an allen drei Stellen · B so lassen mit Begruendung
Decision: FIXED (Option A)

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-project-dashboard/SKILL.md:178, 361 — Escaping neutralisiert `{{…}}` in Quelltexten nicht; Slot-Edit wird mehrdeutig
Fix: Escaping-Regel um `{` → `&#123;` ergaenzen
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:129 — Karte „Aktiver Change" kennt nur Progress; task/bug ohne Plan ohne Zaehler, 0/0 teilt durch null
Fix: Zaehler wie Backlog-Spalte (Progress/Schritte/Fix-Schritte); Y = 0 → nur Warnchip, kein Balken
Decision: FIXED

### F6 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:89 — Kennzahl „Aktive Changes" zaehlt Ordner inkl. leerer/abgenommener ≠ Summe der Backlog-Spalten
Fix: Kennzahl = Anzahl der Eintraege im Backlog-Block
Decision: FIXED

### F7 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:91 — Kennzahl Worktrees zeigt 0 statt `—`, wenn unbekannt (Drift, fehlende Quelle, kein Git)
Fix: in diesen Faellen `—` mit Zusatzzeile
Decision: FIXED

### F8 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:16 — `consumes` nennt `project-changelog/*/*.md` statt Kit-Token `session-log`
Fix: durch `session-log` ersetzen
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:208 — `start "" …` ohne Shell-Angabe; in PowerShell Fehler
Fix: Shell ausdruecklich nennen (Bash-Werkzeug / Git Bash)
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig]
skills/dtb-project-dashboard/SKILL.md:201 — „Kein Git-Repo" nicht als Bedingung definiert; Exit 128 von check-ignore koennte als „nicht ignoriert" gelesen werden
Fix: nur Exit 1 = nicht ignoriert; kein Git = Schritt 1 lieferte `DURCHLASS-NOGIT`
Decision: FIXED
