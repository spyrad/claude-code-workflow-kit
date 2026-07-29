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
  consumes: [WORKFLOW_STATUS.md, BACKLOG.md, features/*/spec.md, features/*/plan.md, features/*/task.md, session-log, project-rules/DERIVED_STATE_RULES.md]
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
  betroffenen Dateien nennen (`git -C {repo.path} diff --stat HEAD..@{u}`, gekuerzt).
  Zusaetzlich pruefen, ob ungepullte Commits **dieselben** Dateien anfassen wie uncommittete
  lokale Aenderungen (`git status --short` gegen die Diff-Liste) → wenn ja, als
  ⚠ Kollisionsrisiko melden, inkl. Empfehlung: lokale Aenderungen erst committen/stashen,
  dann zusammenfuehren
- **Ahead > 0** → 1 Zeile („X lokale Commits nicht gepusht")

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
4. **Bei Behind > 0 aus Schritt 3:** Die Ableitung liest die Artefakte im **Arbeitsbaum**, ist
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

### Schritt 5: Resume-Report

Halte den Report **kompakt** (max 60 Zeilen Output). Fokus auf Actionable Info.

**Fall A: Mit aktivem Feature**

```
# Resume: {config.project_name}

**Feature:** {Feature-Name} (Status: In Arbeit)
**Letzte Session:** {Datum}

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

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}
{Falls behind: "⚠ X ungepullte Commits auf {upstream}:" + `--oneline`-Liste + betroffene Dateien}
{Falls ahead: "X lokale Commits nicht gepusht"}
{Falls Kollisionsrisiko: "⚠ Ungepullte Commits fassen dieselben Dateien an wie lokale Aenderungen: {Dateien}"}
{Falls Remote nicht erreichbar: "Remote nicht erreichbar — Stand nur lokal"}

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

## Letzte Session

- [2-3 Bullet Points: Was wurde gemacht]

## Git

{repo.name}: `{branch}` — {letzter Commit} {uncommitted: "X Aenderungen"}
{Falls behind: "⚠ X ungepullte Commits auf {upstream}:" + `--oneline`-Liste + betroffene Dateien}
{Falls ahead: "X lokale Commits nicht gepusht"}
{Falls Kollisionsrisiko: "⚠ Ungepullte Commits fassen dieselben Dateien an wie lokale Aenderungen: {Dateien}"}
{Falls Remote nicht erreichbar: "Remote nicht erreichbar — Stand nur lokal"}

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
