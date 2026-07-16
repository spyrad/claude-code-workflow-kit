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

<!-- PHASE-2-FORTSETZUNG: Red-Flag-Scan, Staging+Message, Commit, Push+Summary, Wichtig/Verwandte -->
