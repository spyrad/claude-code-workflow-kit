---
name: dtb:workflow-resume
description: >-
  Use when: "Session fortsetzen", "workflow resume", "wo war ich",
  "Kontext wiederherstellen". Restores workflow context after a session break
  by reading WORKFLOW_STATUS.md, session logs, and git status.
disable-model-invocation: true
allowed-tools: Read, Bash
pipeline:
  stage: session
  after: [dtb:workflow-checkpoint, dtb:project-init]
  next: null
  consumes: [WORKFLOW_STATUS.md, BACKLOG.md, features/*/spec.md, features/*/plan.md, features/*/task.md, features/*/worker-report.md, session-log, project-rules/DERIVED_STATE_RULES.md, workflow.config.yaml, dtb-session-uebergabe.md]
  produces: []
---

# Workflow fortsetzen (Resume)

Du stellst den Workflow-Kontext nach einem Session-Break wieder her.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden.
Erstelle eine Config-Datei mit /dtb:project-init.
```

### Schritt 2: Status & Session-Log lesen

1. **Lies die Status-Datei:** `{config.paths.workflows}/WORKFLOW_STATUS.md`
   — inkl. `## Handoff`-Block (Empfangs-Seite des Uebergangs, geschrieben von `dtb:workflow-checkpoint`):
   lies die Zeilen `**Naechster Befehl:**` und `**Empfehlung:**`, falls vorhanden. Fehlt der Block
   (aeltere Status-Datei) → still ueberspringen, `## Naechster Schritt` wie bisher aus Ableitung fuellen
2. **Lies den neuesten Session-Log:** `{config.paths.changelog}/` (neueste Datei im neuesten Monats-Ordner)
3. **Lies das Backlog:** `{config.paths.workflows}/BACKLOG.md`

Falls WORKFLOW_STATUS.md nicht existiert:
```
WORKFLOW_STATUS.md nicht gefunden.
Empfehlung: Am Ende dieser Session /dtb:workflow-checkpoint ausfuehren.
```

### Schritt 2a: Pane-Uebergabe (nur im verlinkten Worktree)

Nach `/clear` in einem verlinkten Worktree steht der Kontext der Vorsession nicht in
`WORKFLOW_STATUS.md` (dort liegt nur die Branch-Kopie, veraltet), sondern in der
Uebergabe-Notiz, die `dtb:workflow-checkpoint` beim „Wechsel" schreibt (Format:
`dtb:workflow-checkpoint` → `### Uebergabe-Notiz (Format — die eine Quelle)`). Dieser
Schritt liest sie nur — er schreibt die Notiz nie.

In EINEM selbstaendigen Bash-Block (Worktree-Erkennung wie der Worktree-Guard; die
cd/pwd-Normalisierung ist Pflicht):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo KEIN-WORKTREE; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo KEIN-WORKTREE; exit 0; }
G=$(cd "$G" 2>/dev/null && pwd) || { echo KEIN-WORKTREE; exit 0; }
C=$(cd "$C" 2>/dev/null && pwd) || { echo KEIN-WORKTREE; exit 0; }
[ "$G" = "$C" ] && { echo KEIN-WORKTREE; exit 0; }
N="$G/dtb-session-uebergabe.md"
[ -f "$N" ] || { echo KEINE-NOTIZ; exit 0; }
L=$(grep '^## ' "$N" | tail -1)
case "$L" in "## Ende-Block erzeugt"*) echo "ERZEUGT $L"; exit 0;; esac
echo "NOTIZ $N"; cat "$N"
```

- `KEIN-WORKTREE`, `KEINE-NOTIZ` oder `ERZEUGT …` → der Report-Abschnitt `## Pane-Uebergabe`
  entfaellt still; der Resume laeuft unveraendert weiter
- `NOTIZ` → aus dem Kopf und allen `## Wechsel`-Abschnitten seit dem letzten Ende-Marker den
  Report-Abschnitt `## Pane-Uebergabe` fuellen (Vorlagen in Schritt 5) — Zeilen in dieser
  Reihenfolge:

  ```
  Rolle: {Rolle aus dem Kopf} · Schreibgrenzen: {aus dem Kopf, gekuerzt}
  Orchestrator: {pane-id} ({erreichbar | ungeprueft}) | ⚠ Orchestrator-Pane {pane-id} nicht erreichbar | — (Block manuell tragen)
  Rueckweg: am Ende der Arbeit /dtb:workflow-checkpoint → „Ende", Block woertlich inkl. Kopfzeile senden:
    {Rueckweg-Zeile — entfaellt bei „—"}
  Offen ({K} Wechsel seit {Datum des ersten}):
  - {Offene Punkte / Naechste Schritte und Uebersprungene globale Updates aller Abschnitte, chronologisch, Dubletten bleiben, „- keine" weglassen}
  Uncommittet: {aus dem juengsten Abschnitt — Momentaufnahme-Regel im Notiz-Format —, oder „—"}
  Lektion-Kandidaten: {alle Abschnitte, oder „—"}
  Naechster Befehl: {aus dem juengsten Abschnitt}
  ```

- **Vorrang:** Im Worktree ersetzt der `Naechster Befehl:` der Notiz den
  `**Naechster Befehl:**` aus `## Handoff` (Branch-Kopie, veraltet) im Abschnitt
  `## Naechster Schritt`. Widerspricht er der Artefakt-Ableitung (Schritt 4), gewinnt
  weiterhin die Ableitung (1 ⚠-Zeile)

**Adress-Pruefung (deklarierte Herdr-Ausnahme):** Der juengste `Orchestrator:`-Wert ist eine
fluechtige Momentaufnahme. Ist er nicht `—`, in EINEM selbstaendigen Bash-Block pruefen — nur
der Exit-Code zaehlt, die Ausgabe wird nicht per Regex gelesen:

```bash
[ "$HERDR_ENV" = "1" ] && command -v herdr >/dev/null 2>&1 || { echo HERDR-AUS; exit 0; }
herdr agent get "{pane-id}" >/dev/null 2>&1 && echo ERREICHBAR || echo NICHT-ERREICHBAR
```

- `ERREICHBAR` → `(erreichbar)`; `HERDR-AUS` → Pruefung still ueberspringen, `(ungeprueft)`
  — Sichern und Wiederfinden laufen ohne Herdr weiter
- `NICHT-ERREICHBAR` (`agent_not_found`, Exit 1 — z.B. Orchestrator neu gestartet) → die
  ⚠-Zeile im Abschnitt, darunter die Textzeile
  `Neue Orchestrator-Adresse? · weiter = ohne (Block manuell tragen)`. Die Antwort gilt fuer
  diese Session; der naechste Checkpoint uebernimmt sie aus dem Verlauf in seinen Abschnitt
  (dieser Skill schreibt nichts)
- **Rueckweg-Zeile** (mit der geprueften bzw. neu genannten Adresse eingesetzt):
  `herdr agent prompt {orchestrator-pane} "<der komplette Block>"`

> **Kopplungs-Hinweis (Herdr-Kanon):** Herdr-Kommandos leben sonst nur in `dtb:worker`
> (`### Pane-Auftrag` / `### Pane-Ausfuehrung`). Dieser Schritt ist dort als zweite
> deklarierte Ausnahme registriert: die Adress-Pruefung und die Rueckweg-Zeile spiegeln
> `### Pane-Auftrag`. Zustell-Syntax dort geaendert → hier mitziehen; dieser Schritt
> geaendert → die Ausnahmen-Liste dort pruefen.

### Schritt 3: Git-Status pruefen (inkl. Remote-Stand)

Fuer jeden Eintrag in `config.repos` zuerst den lokalen Stand:
```bash
git -C {repo.path} branch --show-current && git -C {repo.path} log --oneline -3 && git -C {repo.path} status --short
```

Dann **immer** den Remote-Stand holen — bei Parallelarbeit ist ungepullte Fremdarbeit die
haeufigste Ursache fuer Doppelarbeit, und der lokale Stand allein zeigt sie nicht:
```bash
git -C {repo.path} fetch --all --prune
git -C {repo.path} rev-list --left-right --count HEAD...@{u}
git -C {repo.path} log --oneline HEAD..@{u}
```
`fetch` ist lesend (aendert Arbeitsbaum und Branches nicht) und daher hier erlaubt.
**Niemals selbst `git pull`, `merge`, `stash`, `reset` oder `checkout`** — dieser Skill ist
read-only, Zusammenfuehren entscheidet der Benutzer.

Auswertung:
- Kein Upstream (`@{u}` schlaegt fehl) oder `fetch` scheitert (offline/kein Zugang) →
  1 Hinweiszeile im Report („Remote nicht erreichbar, Stand nur lokal"), sonst weiter wie bisher
- **Behind > 0** → im Report unter `## Git` die neuen Commits mit `--oneline` auflisten und die
  betroffenen Dateien nennen (`git -C {repo.path} diff --stat HEAD...@{u}` — **drei** Punkte,
  diffed gegen den Merge-Base und zeigt nur die fremde Seite; mit zwei Punkten erscheinen bei
  divergierten Branches die eigenen ungepushten Commits als Loeschungen).
  Zusaetzlich pruefen, ob ungepullte Commits **dieselben** Dateien anfassen wie uncommittete
  lokale Aenderungen (`git status --short` gegen die Diff-Liste) → wenn ja, als
  ⚠ Kollisionsrisiko melden, inkl. Empfehlung: lokale Aenderungen erst committen/stashen,
  dann zusammenfuehren
- **Ahead > 0** → 1 Zeile („X lokale Commits nicht gepusht")

### Schritt 3b: Worktree-Stand (laufende Arbeit ausserhalb des Haupt-Checkouts)

Beim Wiedereinstieg soll Arbeit in Pane-/Worker-Worktrees sichtbar sein — sie liegt bis zum Merge
nicht im Arbeitsbaum, den Schritt 4 ableitet.

**Worktree-Stand (operative Kopie von Regel-Datei §10 — rein lesend).**
Kernsatz: Die Sichten zeigen unter `In Worktrees` je verlinktem Worktree genau eine Zeile — gelesen, nie beschrieben.
- **Quelle:** `git worktree list --porcelain`; der **erste** Eintrag ist der Haupt-Checkout und wird nicht
  gelistet; die Zeilen folgen der Reihenfolge der Liste. Kein Git-Repo (`git rev-parse --git-dir` scheitert) oder
  kein weiterer Worktree → Block entfaellt still (kein „keine"); scheitert `worktree list` IM Git-Repo → genau eine
  Zeile `In Worktrees: nicht lesbar ({Fehler})` — nie still schlucken
- **Slug / Art:** Verzeichnisname ohne Praefix `pane-`/`worker-`. `pane-` → `interaktiv (pane)`; `worker-` mit
  Branch → `autonom (pane)`; `worker-` detached → `autonom (subagent)`; alles andere → `manuell`
- **Hauptbranch:** `parallel.default_branch` aus `workflow.config.yaml`, sonst Branch des ersten Eintrags — nie
  zwischen master/main raten
- **Stand** — erster zutreffender Zustand gilt; n = `git rev-list --count {haupt}..{branch}`, Reflog =
  `git reflog show refs/heads/{branch}`:
  1. Eintrag traegt `prunable` oder Pfad fehlt → `verwaist → git worktree prune` (Rest der Zeile entfaellt)
  2. n > 0 → `+{n} Commits, zuletzt YYYY-MM-DD` (`git log -1 --format=%cs {branch}`) — `laufend`
  3. n = 0 UND Reflog hat mehr als den Anlage-Eintrag → `gemergt → aufraeumen (git worktree remove "{pfad}")`;
     bei uncommitted > 0 stattdessen `gemergt, {N} uncommitted → erst sichern` (nie zum Entfernen raten, solange
     Arbeit ungesichert ist); in beiden Faellen entfaellt der Rest der Zeile
  4. sonst (n = 0, Reflog nur mit Anlage-Eintrag oder fehlend) → `frisch` — nie „aufraeumen"
- **uncommitted:** Zeilen von `git -C {pfad} status --porcelain`. **Fortschritt** aus dem Worktree-Pfad (inkl.
  uncommitteter Flips): `{pfad}/{config.paths.workflows}/features/{slug}/plan.md` `## Progress` → `Progress X/Y` ·
  sonst `task.md` `## Schritte` → `Schritte X/Y` · sonst Stage-Name (Regel-Datei §1.1, z.B. `Discovery`) · sonst `—`
- **Detached** (Subagent-Worker): Branch-Feld `detached @{sha7}`, Feld „Stand" entfaellt, statt Fortschritt
  `worker-report {vorhanden | fehlt}` (Datei im Change-Ordner unter `{pfad}`)
- **⏳** am Zeilenende bei `laufend` und `frisch`, wenn der letzte Commit (bei `frisch`: der Anlage-Eintrag im
  Reflog) ≥ `status.alter_schwelle_tage` Tage alt ist (Default 7)
- **Nur lesend:** erlaubt sind ausschliesslich die Kommandos oben (`worktree list`, `rev-list --count`,
  `log -1`, `reflog show`, `rev-parse --git-dir`, `-C {pfad} status --porcelain`) und das Lesen von Dateien unter `{pfad}`. Nie
  `checkout`, `add`, `commit`, `stash`, `worktree remove`/`prune` — „aufraeumen"/„prune" sind Hinweise an den Menschen

```
In Worktrees:
  {slug}  {Art}  {branch | detached @sha7}  {Stand}  {N} uncommitted  {Fortschritt}[  ⏳]
```

> **Wartungs-Hinweis (Format-Kopplung):** spiegelt §10 (Kopie ist Absicht, §10 — Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22);
> Aenderung dort → hier UND in den beiden anderen Sichten mitziehen (`dtb:workflow-resume`, `dtb:workflow-next`,
> `dtb:backlog-status` — der Block ist in allen dreien wortgleich; Grep-Anker: `In Worktrees`).

### Schritt 4: Feature-Kontext bestimmen (abgeleitet)

**Ableitungsregel:** "In Arbeit" wird aus Artefakten ABGELEITET, nicht aus Statusfeldern —
verbindliche Regeln in `{config.paths.rules}/DERIVED_STATE_RULES.md`
(Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`).

1. Scanne `{config.paths.workflows}/features/*/plan.md`: Ein Feature ist **"In Arbeit"**,
   wenn seine `## Progress`-Sektion teilweise abgehakt ist (X von Y, 0 < X < Y)
2. WORKFLOW_STATUS.md ("Laufende Arbeit") und BACKLOG.md dienen nur als Kontext und
   zur Konflikterkennung: Widerspricht ein Statusfeld der Ableitung, gewinnt das Artefakt —
   melde den Widerspruch mit 1 Hinweiszeile im Report (nicht selbst korrigieren)
3. Fallbacks (Regel-Datei §1.4): `plan.md` ohne `## Progress` → "Fortschritt unbekannt" +
   Nachruestung anbieten; flache Alt-Dateien/`IMPL_STATUS_*.md` (Altbestand) → ignorieren, Migrations-Hinweis;
   explizit "Pausiert" markierte Features → nicht als aktiv zeigen
4. **Explizit `Abgenommen` (Regel-Datei §1.2, gespiegelte Lese-Regel — Grep-Anker, eine Zeile):**
   Ein gesetztes `Abgenommen` ueberschreibt die Ableitung „Fertig zum Testen" und ist KEIN Konflikt nach §1.3 (analog `Pausiert`).
   Abgenommene Features sind NICHT aktiv (kein Fall A/B), verschwinden aber nicht still: im
   Resume-Report als genau 1 Zeile zeigen — `{N} Feature(s) abgenommen — warten auf /dtb:archive`
   (nur wenn N > 0). `Abgenommen` bei unvollstaendigem Progress (< Y/Y) → ⚠ Feld-Konflikt melden
   (Artefakt gewinnt, 1 Zeile), nicht als abgenommen zeigen
5. **Bei Behind > 0 aus Schritt 3:** Die Ableitung liest die Artefakte im **Arbeitsbaum**, ist
   also nur so aktuell wie der letzte Pull. Betreffen die ungepullten Commits Dateien unter
   `{config.paths.workflows}/` (Plan/Spec/Backlog/Status/`archive/`), dann den abgeleiteten Stand
   gegen den Remote-Stand gegenpruefen (`git show @{u}:<pfad>`) und Abweichungen als ⚠ Zeile
   melden — Fortschritt und `## Naechster Schritt` nach dem **Remote**-Stand angeben, denn der
   Handoff-Befehl kann dort schon erledigt sein

**Fall A: Feature "In Arbeit" erkannt (abgeleitet)**
- Lies die zugehoerige Feature-Spec (`features/{slug}/spec.md`)
- Lies den Implementierungsplan (`features/{slug}/plan.md`)
- Naechster Schritt = erster nicht abgehakter Eintrag in `## Progress`
- Zeige Feature-Kontext im Resume-Report (Ziel aus Feature-Spec, Fortschritt X/Y, naechster Schritt)

**Fall B: Mehrere Features "In Arbeit"**
- Zeige Auswahlliste der laufenden Features
- User waehlt welches Feature fortgesetzt wird

**Fall C: Kein Feature "In Arbeit"**
- Hinweis: "Kein aktives Feature. Starte eines mit `/dtb:feature-start`"

### Lesestand-Pruefung (Lese-Seite)

Parallele Sessions koennen gelesene Dateien zwischen Einlesen und Report veraendern
(Orchestrator-Muster: `skills/CLAUDE.md` → „Parallele Sessions" — dieser Skill ist
lesend-entscheidend: sein Report ist eine Handlungsempfehlung).

1. **Beim Einlesen merken:** mtime der gelesenen Steuer-Dateien festhalten
   (`WORKFLOW_STATUS.md`, `BACKLOG.md`, die in Schritt 2 gelesene neueste
   Changelog-Tagesdatei, die in Schritt 4 gelesenen `features/*/plan.md`) — in EINEM
   selbstaendigen Bash-Block:
   ```bash
   ls -l --time-style=full-iso {datei...}
   ```
2. **Unmittelbar vor der Report-Ausgabe (Schritt 5)** dieselbe Abfrage erneut
   ausfuehren und vergleichen:
   - mtime unveraendert → still weiterarbeiten (kein Output)
   - mtime veraendert → Datei NEU lesen und den Inhalt vergleichen:
     - Inhalt tatsaechlich abweichend → genau eine Zeile im Report
       `⚠ {Datei} wurde seit dem Einlesen geaendert ({neue mtime}) — Stand neu geladen`
       und den Report auf dem FRISCHEN Stand aufbauen (kein Abbruch, keine Nachfrage)
     - Inhalt identisch (nur mtime, z.B. touch/Checkout) → keine Warnung
   - Datei existiert nicht mehr → wie Abweichung behandeln:
     `⚠ {Datei} seit dem Einlesen entfernt/verschoben — Ableitung ggf. hinfaellig`
3. **Bewusste Restluecke:** Das Fenster zwischen Pruefung und Ausgabe bleibt
   (kein Locking) — Konvention: `skills/CLAUDE.md` → „Parallele Sessions".

### Schritt 5: Resume-Report

Halte den Report **kompakt** (max 60 Zeilen Output). Fokus auf Actionable Info.

**Fall A: Mit aktivem Feature**

```
# Resume: {config.project_name}

**Feature:** {Feature-Name} (Status: In Arbeit)
**Letzte Session:** {Datum}

## Pane-Uebergabe

{Zeilen aus Schritt 2a — Abschnitt entfaellt still ohne offene Notiz}

## Feature-Stand

[Ziel aus Feature-Spec]
**Fortschritt:** X/Y Schritte (aus `## Progress`) — naechster: {erster nicht abgehakter Schritt N.M}
[Falls kein `plan.md`: "Kein Implementierungsplan vorhanden → /dtb:impl-plan"]
[Falls Konflikt: ⚠ {Feld-Quelle} sagt "{Feld}", Artefakte zeigen "{abgeleitet}"]

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}
{Falls behind: "⚠ X ungepullte Commits auf {upstream}:" + `--oneline`-Liste + betroffene Dateien}
{Falls ahead: "X lokale Commits nicht gepusht"}
{Falls Kollisionsrisiko: "⚠ Ungepullte Commits fassen dieselben Dateien an wie lokale Aenderungen: {Dateien}"}
{Falls Remote nicht erreichbar: "Remote nicht erreichbar — Stand nur lokal"}
{Falls abgenommen: "{N} Feature(s) abgenommen — warten auf /dtb:archive"}

## In Worktrees

{Zeilen aus Schritt 3b ohne Kopfzeile — Abschnitt entfaellt still, wenn der Block entfaellt}

## Naechster Schritt

[Konkret: Was jetzt tun, welche Dateien — bevorzugt der `**Naechster Befehl:**` aus dem Handoff-Block]
[Falls Handoff-Befehl dem abgeleiteten naechsten Schritt widerspricht: ⚠ Hinweis, Ableitung gewinnt]

Bereit? Sage "Los" oder stelle Fragen.
```

**Fall B: Mehrere Features "In Arbeit"**

```
# Resume: {config.project_name}

**Letzte Session:** {Datum}
**Zusammenfassung:** [1 Satz aus WORKFLOW_STATUS "Laufende Arbeit"]

## Pane-Uebergabe

{Zeilen aus Schritt 2a — Abschnitt entfaellt still ohne offene Notiz}

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}
{Falls behind: "⚠ X ungepullte Commits auf {upstream}:" + `--oneline`-Liste + betroffene Dateien}
{Falls ahead: "X lokale Commits nicht gepusht"}
{Falls Kollisionsrisiko: "⚠ Ungepullte Commits fassen dieselben Dateien an wie lokale Aenderungen: {Dateien}"}
{Falls Remote nicht erreichbar: "Remote nicht erreichbar — Stand nur lokal"}
{Falls abgenommen: "{N} Feature(s) abgenommen — warten auf /dtb:archive"}

## In Worktrees

{Zeilen aus Schritt 3b ohne Kopfzeile — Abschnitt entfaellt still, wenn der Block entfaellt}

## Feature fortsetzen

Folgende Features sind in Arbeit:
  1. {Feature-Name} ({Prio})
  2. {Feature-Name} ({Prio})

Welches Feature moechtest du fortsetzen?
```

**Bei Feature-Auswahl durch den Benutzer:**
1. Lies die Feature-Spec (`features/{slug}/spec.md`)
2. Lies den Implementierungsplan (`features/{slug}/plan.md`), falls vorhanden
3. Zeige Feature-Kontext (Ziel aus Spec, aktuelle Phase/naechster Schritt aus Plan)

**Fall C: Kein Feature "In Arbeit"**

```
# Resume: {config.project_name}

**Letzte Session:** {Datum}
**Zusammenfassung:** [1 Satz aus WORKFLOW_STATUS "Laufende Arbeit"]

## Pane-Uebergabe

{Zeilen aus Schritt 2a — Abschnitt entfaellt still ohne offene Notiz}

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}
{Falls behind: "⚠ X ungepullte Commits auf {upstream}:" + `--oneline`-Liste + betroffene Dateien}
{Falls ahead: "X lokale Commits nicht gepusht"}
{Falls Kollisionsrisiko: "⚠ Ungepullte Commits fassen dieselben Dateien an wie lokale Aenderungen: {Dateien}"}
{Falls Remote nicht erreichbar: "Remote nicht erreichbar — Stand nur lokal"}
{Falls abgenommen: "{N} Feature(s) abgenommen — warten auf /dtb:archive"}

## In Worktrees

{Zeilen aus Schritt 3b ohne Kopfzeile — Abschnitt entfaellt still, wenn der Block entfaellt}

---

Kein aktives Feature. Starte eines mit `/dtb:feature-start`.
```

---

## Wichtig

- **Actionable:** Benutzer muss sofort wissen was zu tun ist
- **Kompakt:** Max 60 Zeilen Report, keine Detail-Tabellen
- **Feature-Kontext:** Bei aktivem Feature die Spec lesen und relevante Phase zeigen
- **Deutsch:** Alle Texte auf Deutsch
- **Handoff:** Den `**Naechster Befehl:**` aus dem Handoff-Block als naechsten Schritt bevorzugen; bei Widerspruch zur Artefakt-Ableitung gewinnt die Ableitung (Konflikt als 1 Zeile melden)
- **Remote zuerst:** `git fetch` gehoert zu jedem Resume. Ungepullte Fremdarbeit kann den
  Handoff-Befehl bereits erledigt haben — dann ist er kein naechster Schritt, sondern eine
  Zusammenfuehrungs-Aufgabe. Nie `pull`/`merge` selbst ausfuehren, nur melden und empfehlen
- Am Ende immer fragen ob Benutzer starten oder Fragen hat
