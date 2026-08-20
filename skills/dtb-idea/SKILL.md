---
name: dtb:idea
description: >-
  Use when: "Idee notieren", "idea", "Gedanke festhalten", "Einfall",
  "kurz notieren", "Idee speichern". Captures a quick idea or thought
  into the project inbox without interrupting the current workflow.
disable-model-invocation: true
argument-hint: "[Idee als Freitext]"
allowed-tools: Read, Write, Grep, Bash
pipeline:
  stage: idea
  after: null
  next: [dtb:idea-review]
  consumes: [INBOX.md]
  produces: [INBOX.md]
---

# Idee schnell erfassen

Du erfasst eine Idee oder einen Gedanken in der Projekt-Inbox. Keine Rueckfragen (einzige Ausnahme: ein Duplikat-Treffer fragt genau einmal), keine Ausarbeitung — nur speichern.

## Worktree-Guard

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions".

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(cd "$C" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar
- **Branch-Pruefung (optional, nur im `HAUPT-CHECKOUT`-Fall):** Ist `parallel.default_branch`
  in `workflow.config.yaml` gesetzt (nicht `null`) und `git branch --show-current` ungleich
  diesem Wert → Abbruch mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:idea schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
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

## Duplikat-Check

Vor dem Schreiben: pruefe die erfasste Idee **unscharf** gegen die Spalte „Idee" ALLER Zeilen in
`{config.paths.workflows}/INBOX.md` — alle Status, `archive/` wird NIE durchsucht. Vergleich per
Grep nach dem Kern der Idee (Stichworte), Bewertung je Kandidat:

> Gleicher Gegenstand **und** gleiche Aussage — der bestehende Eintrag koennte die neue Erfassung
> vollstaendig ersetzen → Treffer. Gleicher Gegenstand, andere Aussage → kein Duplikat.
> Im Zweifel: kein Duplikat, still durchlassen.

- **Treffer** (max. 3 zeigen, Rest als `+N weitere`; Bestandstext auf ~120 Zeichen + `…` kuerzen):
  ```
  Aehnliche Idee steht schon in der INBOX (#{N}, {Status}): "{Bestandstext, gekuerzt}"
  Trotzdem als neuen Eintrag speichern? (Ja / Abbrechen)
  ```
  Den **Status mitnennen** (`Offen` / `In Arbeit` / `Ausgearbeitet` / `Verworfen`) — ob ein Treffer
  noch offen, laengst ausgearbeitet oder bewusst verworfen ist, entscheidet der Mensch anders.
  Die Entscheidung liegt beim Menschen — **nie hart blocken** (Wiederkehr kann legitim sein).
- **Kein Treffer → keine Ausgabe**, direkt weiter zu Schritt 2 — der Check ist im Normalfall
  unsichtbar; im Trefferfall kommt genau eine Rueckfrage hinzu (der Skill-Kopf nennt diese
  Ausnahme).
- **Fail-open:** `INBOX.md` fehlt oder ist leer → Check still ueberspringen, kein Hinweis.

(Autoren-Doku: Konvention in `skills/CLAUDE.md` → „Duplikat-Schutz (Capture-Skills)" — dieser
Abschnitt ist zur Laufzeit autark.)

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
