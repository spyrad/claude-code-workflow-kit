# Implementierungsplan: commit-and-push

**Erstellt:** 2026-07-16
**Feature-Spec:** `features/commit-and-push/spec.md`
**Geschaetzte Dauer:** ~4-5 h (1 Skill + Doku + Verteilung)
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Geruest + Repo-Root-Ermittlung + Status-Check | ~2 h | Geplant |
| Phase 2 | Red-Flag-Scan → Commit → Push → Summary | ~1.5 h | Geplant |
| Phase 3 | Doku/Abgrenzung + Selbst-Test + Verteilung | ~1 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md ## Betroffene Module`, Bestandspfade verifiziert (Lektion #1/#2).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-commit-and-push/SKILL.md` | Existiert NICHT — das zu erstellende Artefakt |
| `skills/dtb-implement/SKILL.md` | Sicherheitsregeln + heredoc/Here-String real in Ritual P7 (Z. 171-175); Abgrenzung zu diesem Feature schon vorhanden (Z. 218-219); nutzt bewusst KEIN `git add -A` (Z. 163-164, explizites Set) → Staging gegensaetzlich, nur Sicherheitsregeln teilbar |
| `skills/dtb-repo-sync/SKILL.md` | Frontmatter-Peer: `stage: monitoring`, `after/next: null`, `consumes: [workflow.config.yaml]`, `produces: []`, `allowed-tools: Read, Glob, Grep, Bash`; iteriert `config.repos` mit `git -C {path}` (read-only) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Nachbar: committet Session-Logs — Abgrenzung noetig (Session-Commit ≠ Routine-Commit) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §2 SHA-Format; commit-and-push beruehrt `## Progress` NICHT (kein Edit) |
| `workflow.config.yaml` | `config.repos` = Pfad-Startpunkt, NICHT Repo-Grenze (die kommt aus git) |
| `CLAUDE.md`, `skills/CLAUDE.md` | Doku + Gate-Tabelle; Klasse-A-Verteilung (neuer Skill automatisch vom Muster erfasst) |
| `10x-devs-3.0/.claude/commands/10x-commit-and-push.md` | Vorbild (Referenz): 6-Schritt-Ablauf, `git add -A`, Red-Flag-Scan, non-fast-forward-Handling |

---

## Phase 1: Skill-Geruest + Repo-Root-Ermittlung + Status-Check

### Ziel
Der Skill existiert mit korrektem Frontmatter, ermittelt die echten Git-Roots (Kern-USP) und liefert pro Root einen sauberen Status-Befund inkl. Sonderzustaende.

### Schritte

#### Schritt 1.1: Skill-Geruest + Frontmatter + Config-Laden
- **Zweck:** Grundgeruest nach Kit-Konvention; Frontmatter legt Stage/Tools fest
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md` (NEU)
- **Input:** `skills/CLAUDE.md` (Frontmatter-Pflichtfelder), `repo-sync` als Peer
- **Output:** Frontmatter (`name: dtb:commit-and-push`, `disable-model-invocation: true`, `allowed-tools: Read, Glob, Grep, Bash` — **kein** Edit/Write, `stage: monitoring`, `after/next: null`, `consumes: [workflow.config.yaml]`, `produces: []`) + Schritt-0-Config-Laden (mit Fallback auf cwd, wenn keine Config)

#### Schritt 1.2: Repo-Root-Ermittlung (toplevel-Gruppierung)
- **Zweck:** Der Kern des Features — Repo-Grenzen aus git, nicht aus `config.repos`
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** `config.repos`-Pfade (oder cwd bei fehlender Config)
- **Output:** Ablauf, der pro Pfad `git -C {path} rev-parse --show-toplevel` ausfuehrt, Ergebnisse nach eindeutigem toplevel **gruppiert/dedupliziert**, und die Menge der zu bearbeitenden Roots bestimmt (Nicht-Git-Pfad → melden, ueberspringen). **Pfad-Normalisierung vor dem Gruppieren** (Windows): `rev-parse` liefert Forward-Slashes — Vergleich case-insensitiv auf dem Laufwerksbuchstaben und einheitliche Trennzeichen, damit zwei Config-Pfade desselben Roots nicht faelschlich als zwei Roots gelten (sonst kehrt der Doppel-Commit zurueck)

#### Schritt 1.3: Pro-Root Status-Check + Sonderzustaende
- **Zweck:** Ausgangslage je Root feststellen, triviale/gefaehrliche Zustaende frueh abfangen
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** Root-Menge aus 1.2
- **Output:** paralleler Status-Check je Root (`git -C {root} status --short` / `diff --stat` / `log --oneline -3` / `status -sb`); Sonderzustaende: Working Tree clean & up-to-date → sauberer Abbruch; clean aber ahead → direkt Push (kein Leer-Commit); **Detached HEAD → erkennen und abbrechen** (kein Push-Ziel)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-commit-and-push/SKILL.md` mit Frontmatter + Schritten 0-1.3

### Checkpoint-Kriterien

#### Automated
- [ ] `skills/dtb-commit-and-push/SKILL.md` existiert (Glob)
- [ ] Frontmatter enthaelt `stage: monitoring` und `allowed-tools` **ohne** `Edit`/`Write` (Grep)
- [ ] Skill-Text enthaelt `rev-parse --show-toplevel` (Grep — Kern-Mechanismus verankert)

#### Manual
- [ ] Gruppierungslogik deckt Monorepo (1 Root aus n Pfaden), Poly-Repo (n Roots) und config-loses Verzeichnis (cwd → 1 Root) korrekt ab

---

## Phase 2: Red-Flag-Scan → Commit → Push → Summary

### Ziel
Der vollstaendige geführte Commit+Push-Ablauf je Root mit harten Sicherheitsregeln und allen Randfaellen.

### Schritte

#### Schritt 2.1: Red-Flag-Scan vor dem Staging
- **Zweck:** Sicherheit vor Routine — Secrets/Grossdateien nie versehentlich stagen. Da `add -A` (2.2) blind alles staged, ist diese Liste die **einzige** Secret-Barriere → als benannte, erweiterbare Konvention im Skill gestalten, nicht als beilaeufige Aufzaehlung
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** Status-Befund je Root (1.3), Vorbild 10x Krok 2
- **Output:** klar benannte **Red-Flag-Liste** (im Skill als eigener, kommentierter Block, damit erweiterbar): `.env*`, `secrets.*`, `credentials.*`, `*.pem`, `*.key`, `id_rsa*`, `*.p12`, `*.pfx`, `*.keystore`, `.npmrc`; zusaetzlich Dateien > 1 MB und neu getracktes `.claude/settings.local.json` (Ausnahme: `.gitignore` schliesst aus). Scan der untracked+modified Pfade → Stopp & Rueckfrage bei Treffern, sonst Pfad-Liste zur Bestaetigung

#### Schritt 2.2: Staging + Message-Vorschlag (Bestaetigungs-Muster)
- **Zweck:** Routine-Staging + Message im Repo-Stil, vor Commit bestaetigt
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** bestaetigte Pfade (2.1), `git log --oneline -5` je Root fuer den Stil
- **Output:** `git -C {root} add -A` (Default Routine), danach `status --short` zeigen; Message-Vorschlag (imperativer Titel, optionaler Body, Repo-Stil) → Nutzer bestaetigt/korrigiert erst dann Commit (Muster aus `implement` Ritual P2); shell-agnostisch (Bash-heredoc bzw. PowerShell-Here-String, `'@` auf Spalte 0)

#### Schritt 2.3: Commit mit harten Sicherheitsregeln
- **Zweck:** Commit ausfuehren, unverhandelbare Regeln, Hook-Fehler sauber behandeln
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** bestaetigte Message (2.2)
- **Output:** `git -C {root} commit` per heredoc/Here-String; **NIE** `--force`/`--no-verify`/`--amend`/Signing-Bypass; Hook-Fehler → Ursache zeigen+fixen, NEUER Commit (kein `--amend`). Regel-Block **dupliziert** aus `implement` P7 + Kopplungs-Hinweis (Wartung, s. Technische Entscheidungen)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Push mit Edge Cases + Sammel-Summary
- **Zweck:** Push je Root robust, dann ein Gesamt-Ueberblick
- **Dateien:** `skills/dtb-commit-and-push/SKILL.md`
- **Input:** Commit-Ergebnis(se) je Root
- **Output:** **vor dem Push** Ziel-Remote + Branch + Commit-Range je Root zur Sicht anzeigen (kein harter Extra-Stopp bei Routine — Push laeuft direkt wie im 10x-Vorbild); **Auffaelligkeits-Stopp** nur bei ungewohntem/neuem Remote (dann Rueckfrage). Dann `git -C {root} push`; non-fast-forward → **kein** `--force`, `pull --rebase` vs. merge vorschlagen (Nutzer entscheidet); kein Tracking-Branch → `push -u origin <branch>` zeigen+fragen; heterogener Diff → Hinweis „manuell aufteilen"; am Ende **ein** Sammel-Summary ueber alle Roots (Commit-Hash, geaenderte Dateien, Push-Range je Root)

### Deliverables
- [ ] Vollstaendiger Ablauf 2.1-2.4 im Skill

### Checkpoint-Kriterien

#### Automated
- [ ] Grep: Skill enthaelt `git add -A`, die Red-Flag-Muster (`.env`, `*.pem`, `id_rsa`) und `heredoc`/Here-String-Muster
- [ ] Grep-Gegencheck: `--force`, `--no-verify`, `--amend` erscheinen im Skill **nur** in Verbots-Formulierung (jede Fundzeile enthaelt ein Verbotswort — sprachagnostisch: „nie"/„NICHT"/„kein"/„never"; die englische `description` zaehlt mit)

#### Manual
- [ ] Alle Randfaelle aus der Spec sind abgedeckt (non-fast-forward, kein Tracking-Branch, clean+ahead, clean+up-to-date, Detached HEAD, heterogener Diff)
- [ ] Message-Bestaetigungs-Muster entspricht `implement` (Vorschlag → passt/Korrektur → Commit)

---

## Phase 3: Doku/Abgrenzung + Selbst-Test + Verteilung

### Ziel
Der Skill ist dokumentiert, gegen echtes Material getestet und global verteilt.

### Schritte

#### Schritt 3.1: Abgrenzung + Doku
- **Zweck:** Rollen-Abgrenzung sichtbar machen, Kit-Doku nachziehen
- **Dateien:** `CLAUDE.md`, `skills/CLAUDE.md`, `skills/dtb-repo-sync/SKILL.md` (Verwandte), `skills/dtb-workflow-checkpoint/SKILL.md` (Abgrenzung); `implement` Z. 218-219 ist bereits korrekt (nur verifizieren)
- **Input:** fertiger Skill (Phase 1+2)
- **Output:** commit-and-push in Kit-`CLAUDE.md` (Skill-Kategorien) + `skills/CLAUDE.md` erwaehnt; „Verwandte"-Querverweise gesetzt; kein Eligibility-Gate noetig (keine zwingende Artefakt-Eingabe — s. Einteilungsregel)

#### Schritt 3.2: Selbst-Test (nicht-mutierender Nachweis)
- **Zweck:** Kern-Mechanik gegen reale Layouts pruefen, OHNE fremde Repos zu veraendern (Lektionen #5/#6/#7)
- **Dateien:** — (Verifikation, kein Code-Change; Beleg in den Session-Log)
- **Input:** fertiger Skill; Layouts: Einzel-Repo (dieses Kit), Monorepo (`C:/Users/SpyraD/Desktop/Projekte/pkp`), config-los
- **Output:** **nicht-mutierender** Beleg — nur `rev-parse --show-toplevel` + Gruppierung je Layout protokollieren, **kein** `add`/`commit`/`push`. Nachweise: Kit → 1 Root; pkp → 2 Config-Pfade (`pkp-frontend`/`pkp-backend`) gruppieren zu **1** Root; config-los → cwd → 1 Root. **Windows-Pfad-Normalisierungs-Fall explizit** (Laufwerksbuchstabe-Case + Trennzeichen ergeben denselben Root, nicht zwei). Red-Flag-Scan + Sonderzustaende (clean/ahead/detached) an einem realen Lese-Zustand exerciert (Scan liest nur, mutiert nicht)

#### Schritt 3.3: Push nach origin + Verteilung via kit-sync
- **Zweck:** neuen Klasse-A-Skill global verfuegbar machen
- **Dateien:** `~/.claude/` (via `/dtb:kit-sync`, kein Repo-Change)
- **Input:** committeter Skill (Phasen-Commits aus `implement`)
- **Vorbedingung (explizit):** Skill-Commits nach `origin/master` **pushen** — kit-sync bezieht die Quelle aus GitHub, nicht aus dem lokalen Repo; ohne Push sieht kit-sync den neuen Skill nicht (Beleg: impl-review S2 2026-07-16)
- **Output:** `/dtb:kit-sync` (check → sync) installiert `dtb-commit-and-push` global; Lock aktualisiert; Verifikations-check 0 Abweichung

### Deliverables
- [ ] Doku aktualisiert, Selbst-Test-Beleg, Skill global installiert

### Checkpoint-Kriterien

#### Automated
- [ ] Grep: `CLAUDE.md` und `skills/CLAUDE.md` erwaehnen `commit-and-push`
- [ ] Grep: Abgrenzungszeile zu commit-and-push in `implement` vorhanden (Z. ~218)
- [ ] Nach 3.3: `~/.claude/skills/dtb-commit-and-push/SKILL.md` existiert (Glob)

#### Manual
- [ ] Selbst-Test-Beleg zeigt korrekte Root-Gruppierung je Layout (inkl. Monorepo pkp + Windows-Pfad-Normalisierung), nicht-mutierend
- [ ] Skill nach `origin` gepusht (Vorbedingung kit-sync)
- [ ] kit-sync-Lauf meldet Skill installiert, Lock synchron

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Repo-Grenzen-Quelle | config.repos-Iteration / git toplevel-Gruppierung | **git toplevel** (`rev-parse --show-toplevel`) | config.repos ist Poly-Repo-gepraegt und bricht bei Monorepo (pkp: 2 Eintraege, 1 `.git`) → Sammel-Commit + Leer-Commit + Doppel-Push. git-Realitaet schlaegt Config |
| Staging-Strategie | `add -A` / explizites Set | **`add -A`** (Routine) | bewusst gegensaetzlich zu `implement` (explizites verifikationsgebundenes Set); Red-Flag-Scan davor sichert ab |
| Sicherheitsregeln-Formulierung | geteilt / dupliziert | **dupliziert + Kopplungs-Hinweis** | kein Import-Mechanismus zwischen Skills (je eigenstaendige SKILL.md); Muster wie Leak-Lint feature-plan↔greenfield-prd; Skill muss autark lesbar sein (auch config-los ohne implement-Kontext) |
| Pipeline-Frontmatter | — | **`stage: monitoring`, `after/next: null`, `consumes: [workflow.config.yaml]`, `produces: []`** | repo-sync-Peer (Routine-Werkzeug ausserhalb Feature-Pipeline); `utility` ist kein gueltiger stage-Enum-Wert |
| Eligibility-Gate | ja / nein | **nein** | keine zwingende Artefakt-Eingabe (Einteilungsregel skills/CLAUDE.md); wirkt auf Git-Zustand, nicht auf ein features/-Artefakt |
| Multi-Repo-Begriff vs. §2 Regel 5 | angleichen / dokumentieren | **dokumentieren (bewusste Grenze)** | `implement`/DERIVED_STATE_RULES §2 Regel 5 definieren Multi-Repo ueber die `config.repos`-Anzahl (`repo@SHA`-Praefix); commit-and-push nutzt den toplevel. Divergenz bei pkp (2 Eintraege, 1 Root) — aber commit-and-push beruehrt `## Progress`/SHA NICHT → kein direkter Konflikt. Angleichung von `implement`/§2 auf toplevel ist eine separate Idee (INBOX), nicht Teil dieses Features |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Skill-Geruest + Frontmatter + Config-Laden — `1a161f4`
- [x] 1.2 Repo-Root-Ermittlung (toplevel-Gruppierung) — `1a161f4`
- [x] 1.3 Pro-Root Status-Check + Sonderzustaende — `1a161f4`
- [x] 2.1 Red-Flag-Scan vor dem Staging
- [x] 2.2 Staging + Message-Vorschlag (Bestaetigungs-Muster)
- [x] 2.3 Commit mit harten Sicherheitsregeln
- [x] 2.4 Push mit Edge Cases + Sammel-Summary
- [ ] 3.1 Abgrenzung + Doku
- [ ] 3.2 Selbst-Test (blinder Lauf an echtem Material)
- [ ] 3.3 Verteilung via kit-sync

---

## Umsetzung

Umsetzung mit `/dtb:implement commit-and-push` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/commit-and-push/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
