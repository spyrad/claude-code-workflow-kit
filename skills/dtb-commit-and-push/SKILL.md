---
name: dtb:commit-and-push
description: >-
  Use when: "committen", "commit and push", "pushen", "Aenderungen einchecken",
  "commit-and-push", "commit + push". Guided routine commit+push: groups paths by
  their real git root (rev-parse --show-toplevel, not config.repos), runs a red-flag
  scan before staging, proposes a repo-style message, commits with hard safety rules
  (never --force/--no-verify/--amend) and pushes with edge-case handling.
disable-model-invocation: true
argument-hint: "[optional: Repo-Name oder Pfad]"
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [workflow.config.yaml]
  produces: []
---

# Routine-Commit & Push

Du committest und pushst Aenderungen als gefuehrten Routine-Ablauf — die sonst
unbegleitetste Stelle im Workflow. Kern: **Repo-Grenzen kommen aus git selbst**
(`git rev-parse --show-toplevel`), nicht aus `config.repos`. Dadurch verhaelt sich der
Skill in Monorepos (ein `.git`, mehrere Pakete), Poly-Repos (mehrere `.git`),
Einzel-Repos und config-losen Verzeichnissen automatisch korrekt.

> **Abgrenzung:** Dies ist der **Routine-Pfad** ausserhalb des Phasen-Rhythmus.
> Verifikationsgebundene Phasen-Commits macht `dtb:implement` (mit SHA-Rueckschreibung
> in `## Progress`); Session-Log-Commits macht `dtb:workflow-checkpoint`; read-only
> Multi-Repo-Status liefert `dtb:repo-sync`. Dieser Skill beruehrt **kein**
> `## Progress` und schreibt **keine** SHA zurueck (kein `Edit`/`Write`).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

- **Vorhanden:** die Pfade aus `config.repos` (`repo.path`) sind der **Startpunkt** der
  Root-Ermittlung (Schritt 1) — NICHT die Repo-Grenze selbst.
- **Nicht vorhanden:** kein Abbruch. Startpunkt ist das aktuelle Verzeichnis (`.`).
  Der Skill laeuft in jedem Git-Verzeichnis, auch ohne DTB-Config.

Optionales Argument (Repo-Name/Pfad) → nur diesen einen Startpfad verwenden.

## Schritt 1: Repo-Roots ermitteln (git-Realitaet, nicht Config)

`config.repos` ist Poly-Repo-gepraegt; ein Monorepo listet mehrere Pakete als getrennte
Eintraege, die sich **ein** `.git` teilen. Deshalb entscheidet git, nicht die Config:

1. **Pro Startpfad** den echten Git-Root bestimmen:
   ```bash
   git -C {path} rev-parse --show-toplevel
   ```
   - Nicht-Git-Pfad (Kommando schlaegt fehl) → melden und diesen Pfad **ueberspringen**
     (kein Abbruch der uebrigen).
2. **Pfad-Normalisierung vor dem Gruppieren (Windows):** `rev-parse` liefert
   Forward-Slashes. Vergleiche Roots **case-insensitiv auf dem Laufwerksbuchstaben** und
   mit einheitlichen Trennzeichen, damit zwei Startpfade desselben Roots nicht
   faelschlich als zwei Roots gelten (sonst kehrt der Doppel-Commit zurueck).
3. **Nach eindeutigem Root gruppieren/deduplizieren.** Die Menge der eindeutigen Roots
   ist die Arbeitsmenge — **pro Root laeuft der Ablauf (Schritte 2 ff.) genau einmal**.
   - Beispiel Monorepo: `config.repos` = `pkp-frontend` + `pkp-backend` → beide melden
     `…/pkp` → **1 Root** → 1 Commit/Push (nicht zwei).
   - Beispiel Poly-Repo: getrennte `.git` → n Roots → n Ablaeufe.

Gib die ermittelte Root-Menge kompakt aus (welche Startpfade zu welchem Root gehoeren),
bevor es weitergeht.

## Schritt 2: Status je Root + Sonderzustaende

Fuer jeden eindeutigen Root **parallel** den Ist-Zustand erheben:
```bash
git -C {root} status --short
git -C {root} status -sb
git -C {root} diff --stat
git -C {root} log --oneline -3
```

Werte pro Root aus und behandle die Sonderzustaende, **bevor** ein Commit-Ablauf startet:

| Zustand | Verhalten |
|---------|-----------|
| **Detached HEAD** (kein aktueller Branch) | erkennen (`git -C {root} symbolic-ref -q HEAD` leer / `branch --show-current` leer) → **abbrechen** fuer diesen Root (kein Push-Ziel), melden |
| **Working Tree clean & up-to-date** | „nichts zu tun" — sauberer Abschluss fuer diesen Root |
| **Working Tree clean, aber lokal ahead** | kein Leer-Commit → direkt zum **Push** (spaeterer Schritt), Commit-Teil ueberspringen |
| **Aenderungen vorhanden** | regulaerer Ablauf (Red-Flag-Scan → Staging → Commit → Push, folgende Schritte) |

Zeige den Status je Root knapp (Branch, Anzahl Aenderungen, ahead/behind), dann weiter
mit dem Commit-Ablauf fuer die Roots im Zustand „Aenderungen vorhanden".

## Schritt 3: Red-Flag-Scan (vor dem Staging)

Der Default-Stage ist `git add -A` (Schritt 4) — er staged **blind alles**. Deshalb ist
diese Liste die **einzige** Barriere gegen versehentlich eingecheckte Secrets/Grossdateien.
Sie ist bewusst als benannter, erweiterbarer Block gehalten:

```
# Red-Flags (Stopp & Rueckfrage, ausser .gitignore schliesst den Pfad aus):
#   Secrets/Keys : .env*  secrets.*  credentials.*  *.pem  *.key  id_rsa*
#                  *.p12  *.pfx  *.keystore  .npmrc
#   Grosse Datei : jede Datei > 1 MB (Binaries, DB-Dumps) — bewusst? nachfragen
#   Sonderfall   : neu getracktes .claude/settings.local.json (sollte in .gitignore sein)
```

Ablauf pro Root:
1. Untracked + modifizierte Pfade aus `git -C {root} status --short` gegen die Liste pruefen.
   `.gitignore`-ausgeschlossene Pfade sind kein Treffer (bleiben ohnehin ungestaged).
2. **Treffer → STOPP & Rueckfrage** (nie automatisch mitstagen): Pfad(e) zeigen, fragen ob
   bewusst gewollt. Erst nach expliziter Bestaetigung weiter.
3. Kein Treffer → die zu stagenden Pfade zur Sicht auflisten, dann Schritt 4.

## Schritt 4: Staging + Commit-Message-Vorschlag

1. **Stagen (Routine-Default):**
   ```bash
   git -C {root} add -A
   ```
   Danach `git -C {root} status --short` zeigen, damit der Nutzer den Index sieht.
   `.gitignore`-Pfade bleiben ungestaged — das ist korrekt.
2. **Message vorschlagen (Repo-Stil):** aus `git -C {root} log --oneline -5` den Stil ableiten
   (Sprache, Conventional-Commits-Praefix o. ä.). Format:
   - Titel: imperativ, knapp, ohne Punkt am Ende, kein Emoji
   - optionaler Body: 2-5 Bullets „was + warum", nur wenn der Titel nicht reicht
3. **Bestaetigungs-Muster** (wie `dtb:implement`): Vorschlag zeigen → Nutzer bestaetigt
   („passt") oder korrigiert → **erst dann** committen. Kein Commit ohne Bestaetigung.

## Schritt 5: Commit (harte Sicherheitsregeln)

> **Sicherheitsregeln — dupliziert aus `dtb:implement` (Ritual P7).** Kein Import-Mechanismus
> zwischen Skills (je eigenstaendige SKILL.md); der Skill muss autark sicher sein, auch
> config-los ohne `implement`-Kontext. **Format-Kopplung:** Aenderst du die Regeln hier,
> die Formulierung in `dtb:implement` mitdenken (dort steht der Gegen-Hinweis nicht — beim
> naechsten gemeinsamen Touch angleichen).

- **NIE** `--force`, `--no-verify`, `--amend` oder Signing-Bypass. **NIE** Force-Push auf
  `main`/`master`.
- **Hook schlaegt fehl** → nicht mit `--no-verify` umgehen: Fehler zeigen, Ursache fixen
  (z. B. Lint), einen **NEUEN** Commit machen (kein `--amend` — der vorige entstand nicht).
- **Shell-agnostisch**, mehrzeilige Message:
  - Bash-heredoc:
    ```bash
    git -C {root} commit -m "$(cat <<'EOF'
    <Titel>

    <Body falls noetig>
    EOF
    )"
    ```
  - reiner PowerShell-Kontext: Here-String (`git commit -m @'…'@`, schliessendes `'@` auf
    Spalte 0); kein PowerShell-`&&`-Chaining.

## Schritt 6: Push + Sammel-Summary

**Vor dem Push je Root** Ziel zur Sicht zeigen (kein harter Routine-Stopp):
```bash
git -C {root} rev-parse --abbrev-ref HEAD          # aktueller Branch
git -C {root} config --get branch.<branch>.remote  # Tracking-Remote (falls vorhanden)
git -C {root} log @{u}.. --oneline 2>/dev/null     # zu pushende Commits (falls Upstream)
```
Anzeigen: Ziel-Remote + Branch + Commit-Range. **Auffaelligkeits-Stopp** nur bei
ungewohntem/neuem Remote (z. B. anderes Remote als in den letzten Pushes) → Rueckfrage.

**Push:**
```bash
git -C {root} push
```

Edge Cases:

| Fall | Verhalten |
|------|-----------|
| **non-fast-forward** (Push abgelehnt, Remote divergiert) | **NIE** `--force`. Lage zeigen, `git pull --rebase` vs. `git pull` (merge) vorschlagen — **Nutzer entscheidet** |
| **kein Tracking-Branch** | `git -C {root} push -u origin <branch>` zeigen und fragen, nicht automatisch ausfuehren |
| **heterogener Diff** (mehrere Themen im selben Commit) | als Routine-Werkzeug flaggen: Hinweis „fuer getrennte Historie manuell aufteilen" — kein Auto-Split |

**Sammel-Summary** (ein Block ueber alle bearbeiteten Roots):
```
✓ {root}: {commit-hash} {titel} — {N} Dateien — Push {lokal→remote range}
… (weitere Roots)
○ {root}: nichts zu tun (clean & up-to-date)   |   uebersprungen (detached HEAD)
```
Untracked `.gitignore`-Pfade kurz erwaehnen, falls vorhanden („N in .gitignore, unveraendert — OK").

---

## Wichtig

- **git-Realitaet schlaegt Config:** Repo-Grenzen IMMER aus `rev-parse --show-toplevel` +
  Gruppierung, nie aus der Zahl der `config.repos`-Eintraege. Ein Commit pro eindeutigem Root.
- **Kein `## Progress`, keine SHA:** dieser Skill traegt bewusst keine SHA in Plaene zurueck
  (`allowed-tools` ohne `Edit`/`Write`) — das ist `dtb:implement` (Phasen-Ritual).
- **Sicherheitsregeln unverhandelbar:** nie `--force`/`--no-verify`/`--amend`/Signing-Bypass;
  nie Force-Push auf `main`/`master`. Hook rot → fixen + NEUER Commit.
- **Routine, aber nicht blind:** Red-Flag-Scan (Schritt 3) laeuft immer vor `add -A`.
- **Kompakt & Deutsch:** Ausgaben knapp; alle Texte auf Deutsch.

## Verwandte Skills

- `/dtb:implement` — verifikationsgebundene Phasen-Commits mit SHA-Rueckschreibung (nicht Routine)
- `/dtb:workflow-checkpoint` — Session-Log-Commit am Session-Ende
- `/dtb:repo-sync` — read-only Multi-Repo-Status (committet nie)
