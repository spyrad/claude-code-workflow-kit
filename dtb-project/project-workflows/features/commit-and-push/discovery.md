# Discovery: commit-and-push
<!-- resume: done -->

**Erstellt:** 2026-07-16
**Idee-Referenz:** Inbox #21 — "`dtb:commit-and-push` bauen (Vorbild `10x-commit-and-push`): Routine-Commit+Push-Schritt, den das Kit nicht hat — `repo-sync` ist read-only Monitoring, kein Skill autorisiert Commits, obwohl das Progress-Modell Commit-SHAs als Beleg verlangt"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-commit-and-push/SKILL.md` | NEU — das Artefakt selbst (Skill mit `disable-model-invocation: true`, verhält sich wie ein Command) |
| `skills/dtb-implement/SKILL.md` | Grenzt Routine-Commits bereits an dieses Feature ab (Z. 218-219); teilt hartes Sicherheits-Regelwerk + heredoc/Here-String-Muster + SHA-Logik (§2) |
| `skills/dtb-repo-sync/SKILL.md` | Nachbar: read-only Multi-Repo-Status; Muster für `config.repos`-Iteration, commitet aber nie |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Committet Session-Logs; Abgrenzung nötig (Session-Commit ≠ Routine-Commit) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §2 (SHA-als-Verifikations-Beleg, Multi-Repo-Präfix `repo@SHA`) — commit-and-push berührt `## Progress` NICHT (Entkopplung, s.u.) |
| `workflow.config.yaml` | `config.repos` — Multi-Repo-Fähigkeit (ein Repo wählen oder alle) |
| `CLAUDE.md` + `skills/CLAUDE.md` | Doku/Gate-Tabelle; kit-sync-Klasse-A-Verteilung |
| `10x-devs-3.0/.claude/commands/10x-commit-and-push.md` | Vorbild (nur Referenz): 6 Schritte, `git add -A`, Red-Flag-Scan, non-fast-forward-Handling |

---

## Anforderungen

### Scope
**Enthalten:**
- **Form:** Skill (`skills/dtb-commit-and-push/SKILL.md`) mit `disable-model-invocation: true` — verhält sich wie ein Command, fügt sich aber ins Skill-/Pipeline-Modell ein (Frontmatter `stage`/`consumes`/`produces`) und ist aus `implement` referenzierbar
- Ablauf: paralleler Status-Check → Red-Flag-Scan **vor** `git add` → Stagen → Message-Vorschlag im Repo-Stil → Commit (harte Sicherheitsregeln) → Push (non-fast-forward-/kein-Tracking-Branch-Handling) → kompaktes Summary
- Multi-Repo über `config.repos`: ein Repo wählen oder alle; **pro Repo eigener Commit** (eigener Diff/Message/Push), am Ende ein Sammel-Summary

**Nicht enthalten:**
- Kein Feature-End-Review (das ist `dtb:impl-review`)
- Kein Aufteilen heterogener Diffs (→ Hinweis „manuell aufteilen", kein Auto-Split)
- Kein `--force`/`--no-verify`/`--amend`, kein Signing-Bypass
- Kein Session-Log-Schreiben (bleibt `dtb:workflow-checkpoint`)
- **Keine SHA-Rückschreibung in `## Progress`** (Entkopplung von #19 — s. Integrationspunkte)

### Gewuenschtes Verhalten
- Schnell und geführt: parallele Status-Checks vorweg, knapper Message-Vorschlag zur Bestätigung, Sicherheits-Stopps nur bei echten Red Flags
- **Bestätigungs-Muster aus `dtb:implement`** übernehmen (Message vorschlagen → „passt"/Korrekturen → erst dann Commit)
- Staging-Strategie: **Default `git add -A`** (Routine-Charakter, wie 10x), ABER der Red-Flag-Scan läuft zwingend davor und listet die zu stagenden Pfade zur Bestätigung
- Abgrenzung zu `implement`: dort explizites Set (verifikationsgebunden), hier `-A` (Routine) — beide dokumentiert nebeneinander
- Bei sauberem, aber lokal ahead-Zustand: direkt `git push`, kein Leer-Commit

### Randfaelle
- **Hook schlägt fehl** → nicht `--no-verify`; Fehler zeigen, Ursache fixen, NEUEN Commit (kein `--amend`)
- **Push abgelehnt (non-fast-forward)** → nicht `--force`; `git pull --rebase` vs. `git pull` (merge) vorschlagen, Entscheidung beim Nutzer
- **Kein Tracking-Branch** → `git push -u origin <branch>` zeigen und fragen
- **Nichts zu committen, aber lokal ahead** → direkt `git push`, kein Leer-Commit
- **Working tree clean & up-to-date** → „nichts zu tun", sauberer Abbruch
- **Heterogener Diff** → als Routine-Werkzeug flaggen, Hinweis „manuell aufteilen"
- **Detached HEAD** (kein Branch) → erkennen und abbrechen (kein Push-Ziel) — neu ggü. 10x
- **Red Flags** (Stopp & Rückfrage, außer `.gitignore` schließt sie aus): `.env*`, `secrets.*`, `credentials.*`, `*.pem`, `*.key`, `id_rsa*`; Dateien > 1 MB; plötzlich getracktes `.claude/settings.local.json`

### Einschraenkungen
- **Shell-agnostisch** (wie `implement`): mehrzeilige Message per Bash-heredoc, in reinen PowerShell-Kontexten Here-String; kein PowerShell-`&&`-Chaining
- **`git -C {repo.path}`** für alle Git-Aufrufe (Multi-Repo, kein `cd`)
- **`allowed-tools`:** `Read, Glob, Grep, Bash` (kein `Edit` — keine `## Progress`-Mutation)
- **Harte Sicherheitsregeln unverhandelbar** (identisch zu `implement:171`): nie `--force`/`--no-verify`/`--amend`, kein Signing-Bypass, nie Force-Push auf `main`/`master` — gemeinsame Formulierung mit `implement`, damit beide nicht driften

### Integrationspunkte
- **Zentrale Entkopplung von #19 (verifikations-gate):** #19 wurde als **Variante a** umgesetzt — das Phasen-Ende-Ritual inkl. SHA-Rückschreibung wohnt bereits vollständig in `dtb:implement` (`SKILL.md:177-181`, §2 Regel 4/5). Folge: `commit-and-push` bringt die SHA-Rückschreibung **NICHT** mit; es ist der Routine-Pfad daneben (Commits außerhalb des Phasen-Rhythmus). Kein `Edit`, keine Doppel-Logik, keine Drift-Gefahr bei der `## Progress`-Mutation
- Rollen-Abgrenzung: `implement` = verifikationsgebundene Phasen-Commits · `commit-and-push` = Routine-Commits · `workflow-checkpoint` = Session-Log-Commits · `repo-sync` = read-only Status
- **Externe Abhängigkeiten:** nur `git` + `config.repos` aus `workflow.config.yaml`. Kein Remote-API, kein `gh`

---

## Abhaengigkeiten

- **Konflikte:** keine (neues Terrain).
- **Überschneidungen:** `dtb:implement` teilt das harte Sicherheits-Regelwerk und das heredoc/Here-String-Muster → Koordination, kein Konflikt. Gemeinsame Formulierung anstreben, damit beide Skills nicht driften.
- **kit-sync:** neues Klasse-A-Artefakt (Skill) — nach Umsetzung global verteilen; `implement`-Abgrenzungs-Zeile (Z. 218-219) bleibt korrekt.

---

## Offene Punkte

- **Gemeinsame Sicherheits-Formulierung** mit `implement`: als geteilter Textblock/Verweis oder bewusst dupliziert? (Entscheidung in Spec/Plan.)
- **Pipeline-Frontmatter:** `stage`/`after`/`next` — commit-and-push steht außerhalb der Feature-Pipeline (Routine-Werkzeug wie `repo-sync`). Vorschlag: `stage: monitoring`/`utility` analog `repo-sync`; in `feature-plan` schärfen.
- **Monorepo-Scoping (OFFEN — vor Spec klären):** Der Entwurf ist mechanisch monorepo-*sicher* (`git -C {path}` + `git add -A` + ein Commit funktioniert bei einem Monorepo-Root identisch; `config.repos` hat dann einen Eintrag). Aber unser `config.repos`-Modell ist **Poly-Repo** (mehrere separate `.git`), nicht Monorepo (ein `.git`, viele Pakete). Lücke ist Monorepo-*Bewusstsein*: `git add -A` stag't den ganzen Repo inkl. unbeteiligter Pakete — der „heterogener Diff → manuell aufteilen"-Hinweis fängt das ab, wiegt im Monorepo aber schwerer. Paketweises Scoping (`git add packages/foo`) ist **nicht** MVP-Scope, wäre spätere Erweiterung (optionaler Pfad-Filter-Parameter). **Damian bringt in einer Folge-Session ein konkretes Monorepo-Projekt (anderer Rechner) als Anschauung** — danach entscheiden, ob der Scoping-Fall in den MVP muss oder Erweiterung bleibt.

---

**Erstellt mit:** `/dtb:feature-discover`
