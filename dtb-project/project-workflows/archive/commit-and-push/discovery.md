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
| `workflow.config.yaml` | `config.repos` — liefert die zu prüfenden **Pfade** (Startpunkt), nicht die Repo-Grenzen; letztere via `git rev-parse --show-toplevel`. Optional (Skill läuft auch ohne Config) |
| `CLAUDE.md` + `skills/CLAUDE.md` | Doku/Gate-Tabelle; kit-sync-Klasse-A-Verteilung |
| `10x-devs-3.0/.claude/commands/10x-commit-and-push.md` | Vorbild (nur Referenz): 6 Schritte, `git add -A`, Red-Flag-Scan, non-fast-forward-Handling |

---

## Anforderungen

### Scope
**Enthalten:**
- **Form:** Skill (`skills/dtb-commit-and-push/SKILL.md`) mit `disable-model-invocation: true` — verhält sich wie ein Command, fügt sich aber ins Skill-/Pipeline-Modell ein (Frontmatter `stage`/`consumes`/`produces`) und ist aus `implement` referenzierbar
- Ablauf: paralleler Status-Check → Red-Flag-Scan **vor** `git add` → Stagen → Message-Vorschlag im Repo-Stil → Commit (harte Sicherheitsregeln) → Push (non-fast-forward-/kein-Tracking-Branch-Handling) → kompaktes Summary
- Multi-Repo über **echte Git-Roots**: `config.repos` liefert die zu prüfenden Pfade, die tatsächliche Repo-Grenze aber `git -C {path} rev-parse --show-toplevel`. Pfade werden nach eindeutigem toplevel **gruppiert** → **pro echtem Git-Root ein Commit** (eigener Diff/Message/Push), am Ende ein Sammel-Summary. (Verhindert bei Monorepos den kaputten Doppellauf: Sammel-Commit + Leer-Commit + zweiter Push.)

**Nicht enthalten:**
- Kein Feature-End-Review (das ist `dtb:impl-review`)
- Kein Aufteilen heterogener Diffs (→ Hinweis „manuell aufteilen", kein Auto-Split)
- **Kein paketweises Scoping innerhalb eines Monorepos** (`git add packages/foo` → getrennte Commits pro Paket im selben Repo): bewusster MVP-Schnitt. Der reale pkp-Workflow ist ein Commit über den ganzen Baum; Paket-Split ist später additiv nachrüstbar (optionaler Pfad-Filter), kein Umbau
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
- **`git -C {path}`** für alle Git-Aufrufe (Multi-Repo, kein `cd`); Repo-Grenzen NICHT aus `config.repos` ableiten, sondern per `git -C {path} rev-parse --show-toplevel` bestimmen und Pfade nach eindeutigem toplevel gruppieren (git-Realität schlägt Config)
- **Funktioniert ohne `workflow.config.yaml`:** fehlt die Config, ist die Menge der Pfade = cwd → dessen toplevel → ein Commit-Flow (deckt normale Einzel-Verzeichnisse ab)
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
- **Monorepo-Scoping (ENTSCHIEDEN 2026-07-16 — Vorbild pkp):** Prüfstein war das reale Monorepo `pkp` (ein `.git` im Root, zwei Pakete `pkp-frontend`/`pkp-backend`, die in `config.repos` als **zwei getrennte Einträge** stehen, physisch aber **ein** Repo sind). Der ursprüngliche „pro `config.repos`-Eintrag ein Commit"-Ansatz bricht dort: `git -C pkp-frontend add -A` findet über Aufwärtssuche das Root-`.git` und stag't den ganzen Baum → Sammel-Commit, dann Leer-Commit für `pkp-backend`, zwei Pushes ans selbe Remote. Damian bedient pkp real ohnehin mit **einem** `commit` + `push` über alles.
  - **Entscheidung:** Repo-Grenzen kommen aus git, nicht aus der Config — Pfade nach `git rev-parse --show-toplevel` gruppieren, ein Commit pro eindeutigem toplevel (siehe Scope + Einschränkungen). Fällt für Monorepo (1 Flow), Poly-Repo (n Flows), Einzel-Repo und config-loses Verzeichnis automatisch richtig aus.
  - **Kein** Config-Schema-Change, **kein** Eingriff in `repo-sync`/`implement`. Paketweises Scoping bleibt bewusst außerhalb des MVP (s. „Nicht enthalten").

---

**Erstellt mit:** `/dtb:feature-discover`
