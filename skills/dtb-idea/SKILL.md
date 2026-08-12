---
name: dtb:idea
description: >-
  Use when: "Idee notieren", "idea", "Gedanke festhalten", "Einfall",
  "kurz notieren", "Idee speichern". Captures a quick idea or thought
  into the project inbox without interrupting the current workflow.
disable-model-invocation: true
argument-hint: "[Idee als Freitext]"
allowed-tools: Read, Write
pipeline:
  stage: idea
  after: null
  next: [dtb:idea-review]
  consumes: [INBOX.md]
  produces: [INBOX.md]
---

# Idee schnell erfassen

Du erfasst eine Idee oder einen Gedanken in der Projekt-Inbox. Keine Rueckfragen, keine Ausarbeitung — nur speichern.

## Worktree-Guard (Schritt 0)

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions".

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" && pwd); C=$(cd "$C" && pwd)
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar. Zusatz nur bei gesetztem `parallel.default_branch`
  (nicht `null`) in `workflow.config.yaml`: aktueller Branch ungleich dem Wert → Abbruch
  mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:idea schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele Sessions").
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Wurde bereits Text uebergeben/erfasst, haengt die Meldung ihn als fertigen Befehl an —
  „Dein Text geht nicht verloren — dort absetzen: `/dtb:idea "{erfasster Text}"`".
  Greift der Abbruch VOR dem Erfassungs-Dialog, gibt es nichts zu echoen — nur den
  Befehl ohne Text-Anteil nennen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Idee erfassen

**Input:** Der Freitext nach dem Command-Aufruf ist die Idee.

Falls kein Freitext angegeben wurde:
```
Welche Idee moechtest du festhalten? (Freitext)
```

---

## Schritt 2: In INBOX.md speichern

### Datei
- Pfad: `{config.paths.workflows}/INBOX.md`
- Falls Datei nicht existiert: Erstelle sie mit Header

### Format bei neuer Datei

```markdown
# Ideen-Inbox

> Schnell erfasste Ideen und Gedanken. Ausarbeitung mit `/dtb:feature-discover`.

---

| # | Datum | Idee | Status |
|---|-------|------|--------|
| 1 | YYYY-MM-DD | [Idee-Text] | Offen |
```

### Format bei bestehender Datei

- Fuege eine neue Zeile in die Tabelle ein
- Naechste laufende Nummer vergeben
- Status: `Offen`
- Datum: Aktuelles Datum

### Status-Werte
- **Offen** — Noch nicht bearbeitet
- **In Arbeit** — Wird gerade mit `/dtb:feature-discover` ausgearbeitet
- **Ausgearbeitet** — Feature-Plan erstellt → `features/<slug>/spec.md`
- **Verworfen** — Bewusst nicht weiterverfolgt

---

## Schritt 3: Bestaetigung

```
Idee #{N} gespeichert: {config.paths.workflows}/INBOX.md

  "{Idee-Text}"

Ausarbeiten: /dtb:feature-discover
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.
