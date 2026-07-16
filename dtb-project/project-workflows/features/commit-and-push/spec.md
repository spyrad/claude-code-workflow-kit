# Feature: commit-and-push

**Erstellt:** 2026-07-16
**Ziel:** Ein geführter Routine-Skill, der Änderungen sicher committet und pusht — die heute unbegleitetste Stelle im Workflow.
**Prioritaet:** Mittel
**Status:** In Arbeit <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit hat keinen Skill, der Commits autorisiert: `repo-sync` ist read-only, `implement` committet nur im Phasen-Rhythmus, `workflow-checkpoint` nur Session-Logs. Der Routine-Commit ist damit der unbegleitetste Moment im Workflow, obwohl das Progress-Modell Commit-SHAs als Beleg verlangt. `commit-and-push` schließt diese Lücke als geführter Ablauf (Red-Flag-Scan → Staging → Message-Vorschlag → Commit → Push → Summary) mit harten, unverhandelbaren Sicherheitsregeln. Repo-Grenzen kommen aus git selbst (`rev-parse --show-toplevel`), nicht aus `config.repos` — dadurch verhält sich der Skill in Monorepos (ein `.git`, mehrere Pakete), Poly-Repos, Einzel-Repos und config-losen Verzeichnissen automatisch korrekt.

---

## Scope / Abgrenzung

### Enthalten

- **Form:** Skill `skills/dtb-commit-and-push/SKILL.md` mit `disable-model-invocation: true` — verhält sich wie ein Command, fügt sich aber ins Skill-/Pipeline-Modell ein (Frontmatter) und ist aus `implement` referenzierbar.
- **Ablauf:** paralleler Status-Check → Red-Flag-Scan **vor** dem Staging → Staging → Message-Vorschlag im Repo-Stil (imperativer Titel, Co-Authored-By) → Commit → Push → kompaktes Summary.
- **Repo-Grenzen aus git, nicht aus Config:** `config.repos` liefert nur die zu prüfenden **Pfade** (Startpunkt). Die tatsächliche Repo-Grenze bestimmt `git -C {path} rev-parse --show-toplevel`; Pfade werden nach eindeutigem toplevel **gruppiert**. Pro eindeutigem toplevel läuft **ein** Commit-Flow (eigener Diff/Message/Push), am Ende ein Sammel-Summary.
- **Läuft ohne `workflow.config.yaml`:** fehlt die Config, ist die Pfadmenge = aktuelles Verzeichnis → dessen toplevel → ein Commit-Flow (deckt normale Einzel-Verzeichnisse ab).
- **Default-Staging `git add -A`** (Routine-Charakter), aber der Red-Flag-Scan läuft zwingend davor und listet die zu stagenden Pfade zur Bestätigung.
- **Bestätigungs-Muster aus `implement`:** Message vorschlagen → „passt"/Korrektur → erst dann Commit.
- **Harte Sicherheitsregeln** (identisch zu `implement`): nie `--force`/`--no-verify`/`--amend`, kein Signing-Bypass, nie Force-Push auf `main`/`master`.
- **Randfall-Behandlung** (siehe Success Criteria): fehlgeschlagener Hook, non-fast-forward-Push, fehlender Tracking-Branch, nichts-zu-committen-aber-ahead, sauberer Working Tree, Detached HEAD.

### Nicht enthalten

- Kein Feature-End-Review (das ist `impl-review`).
- Kein Auto-Split heterogener Diffs (→ Hinweis „manuell aufteilen").
- **Kein paketweises Scoping innerhalb eines Monorepos** (getrennte Commits pro Paket im selben Repo): bewusster MVP-Schnitt. Der reale Referenz-Workflow (pkp) ist ein Commit über den ganzen Baum; Paket-Split ist später additiv nachrüstbar (optionaler Pfad-Filter), kein Umbau.
- Kein `--force`/`--no-verify`/`--amend`, kein Signing-Bypass.
- Kein Session-Log-Schreiben (bleibt `workflow-checkpoint`).
- **Keine SHA-Rückschreibung in `## Progress`** — bewusste Entkopplung von #19 (verifikations-gate). Das Phasen-Ende-Ritual inkl. SHA-Rückschreibung wohnt vollständig in `implement`; `commit-and-push` ist der Routine-Pfad daneben. Kein `Edit`-Tool, keine Doppel-Logik, keine Drift-Gefahr.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Naive `config.repos`-Iteration bricht bei Monorepo (Sammel-Commit + Leer-Commit + Doppel-Push) | Hoch (Referenzprojekt pkp ist genau so gebaut) | Hoch | Repo-Grenzen aus `rev-parse --show-toplevel`, Deduplizierung nach toplevel vor dem Commit-Flow |
| Versehentliches Committen von Secrets/großen Dateien durch `git add -A` | Mittel | Hoch | Red-Flag-Scan zwingend vor dem Staging; Stopp & Rückfrage bei Treffern; Pfad-Bestätigung |
| Sicherheitsregeln driften zwischen `commit-and-push` und `implement` | Mittel | Mittel | Gemeinsame Formulierung anstreben (geteilt vs. dupliziert — offener Punkt) |
| Zerstörerische Recovery-Aktion bei Push-Ablehnung (Force-Push) | Mittel | Hoch | Nie `--force`; bei non-fast-forward `pull --rebase` vs. merge vorschlagen, Entscheidung beim Nutzer |
| Heterogener Diff wird als ein Commit zusammengeworfen | Mittel | Niedrig | Als Routine-Werkzeug flaggen, Hinweis „manuell aufteilen" |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine harten Vorbedingungen — neues Terrain, keine Konflikte.

### Referenz-Dokumente

- `features/commit-and-push/discovery.md` — vollständige Discovery inkl. Monorepo-Entscheidung (2026-07-16)
- `skills/dtb-implement/SKILL.md` — Quelle für harte Sicherheitsregeln + heredoc/Here-String-Muster + Bestätigungs-Muster
- `skills/dtb-repo-sync/SKILL.md` — Nachbar: read-only Multi-Repo-Status, Muster für Pfad-Iteration
- `skills/dtb-workflow-checkpoint/SKILL.md` — Abgrenzung (Session-Commit ≠ Routine-Commit)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — §2 (SHA-als-Beleg); `commit-and-push` berührt `## Progress` NICHT
- `10x-devs-3.0/.claude/commands/10x-commit-and-push.md` — Vorbild (nur Referenz)
- `C:/Users/SpyraD/Desktop/Projekte/pkp` — reales Monorepo als Prüfstein (ein `.git`, Pakete `pkp-frontend`/`pkp-backend` als getrennte `config.repos`-Einträge)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] In einem Monorepo (pkp: zwei `config.repos`-Einträge, ein `.git`) entsteht **genau ein** Commit + **ein** Push — kein Leer-Commit, kein Doppel-Push
- [ ] In einem Poly-Repo (mehrere echte `.git`) entsteht pro Repo ein eigener Commit/Message/Push mit Sammel-Summary
- [ ] In einem normalen Einzel-Verzeichnis **ohne** `workflow.config.yaml` läuft der Skill (cwd → toplevel → ein Commit-Flow)
- [ ] Der Red-Flag-Scan läuft **vor** dem Staging und stoppt bei `.env*`/`secrets.*`/`credentials.*`/`*.pem`/`*.key`/`id_rsa*`, Dateien > 1 MB und neu getracktem `.claude/settings.local.json` (außer `.gitignore` schließt sie aus)
- [ ] Kein Pfad im Skill nutzt jemals `--force`/`--no-verify`/`--amend` oder Signing-Bypass
- [ ] Fehlgeschlagener Hook → Fehler zeigen, Ursache fixen, NEUER Commit (kein `--amend`)
- [ ] Push abgelehnt (non-fast-forward) → `pull --rebase` vs. merge vorschlagen, keine Auto-Entscheidung
- [ ] Kein Tracking-Branch → `git push -u origin <branch>` vorschlagen und fragen
- [ ] Nichts zu committen, aber lokal ahead → direkt Push, kein Leer-Commit
- [ ] Working Tree clean & up-to-date → „nichts zu tun", sauberer Abbruch
- [ ] Detached HEAD → erkennen und abbrechen (kein Push-Ziel)
- [ ] Der Message-Vorschlag wird vor dem Commit zur Bestätigung/Korrektur gezeigt (Muster aus `implement`)
- [ ] Der Skill mutiert `## Progress` **nicht** (kein `Edit`-Tool in `allowed-tools`)
- [ ] Shell-agnostisch: mehrzeilige Message per Bash-heredoc bzw. PowerShell-Here-String, kein PowerShell-`&&`-Chaining
- [ ] Nach Umsetzung als Klasse-A-Artefakt via `kit-sync` global verteilt

---

## Offene Punkte

- **Gemeinsame Sicherheits-Formulierung mit `implement`:** als geteilter Textblock/Verweis oder bewusst dupliziert? (Beide Skills tragen dieselben harten Regeln — Entscheidung im `plan.md`.)
- **Pipeline-Frontmatter (`stage`/`after`/`next`):** `commit-and-push` steht außerhalb der Feature-Pipeline (Routine-Werkzeug wie `repo-sync`). Vorschlag: `stage: monitoring`/`utility` analog `repo-sync` — im `plan.md` festlegen.
- **Priorität „Mittel"** ist eine erste Einschätzung (Routine-Nutzen vs. vier Features, die auf reale Abnahme warten) — bei Bedarf korrigieren.

---

**Erstellt mit:** `/dtb:feature-plan`
