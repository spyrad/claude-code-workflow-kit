---
name: dtb:bug-report
description: >-
  Use when: "Bug melden", "bug report", "Fehler gefunden", "Bug erfassen",
  "das geht nicht", "Fehler notieren". Captures a bug report with reproduction
  steps and saves it as features/<slug>/bug.md in the features directory.
disable-model-invocation: true
argument-hint: "[Bug-Beschreibung als Freitext]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: idea
  after: null
  next: [dtb:debug-plan]
  consumes: [BACKLOG.md]
  produces: [features/*/bug.md, BACKLOG.md]
---

# Bug erfassen

Du erfasst einen Bug-Report schnell und strukturiert. Ziel: Alles festhalten was zur Reproduktion und Einordnung noetig ist, ohne den Flow zu unterbrechen.

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
  ⛔ dtb:bug-report schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Wurde bereits Text uebergeben/erfasst, haengt die Meldung ihn als fertigen Befehl an —
  „Dein Text geht nicht verloren — dort absetzen: `/dtb:bug-report "{erfasster Text}"`".
  Greift der Abbruch VOR dem Erfassungs-Dialog, gibt es nichts zu echoen — nur den
  Befehl ohne Text-Anteil nennen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Bug-Informationen sammeln

**Input:** Der Freitext nach dem Command-Aufruf ist die Bug-Beschreibung.

Falls kein Freitext angegeben wurde oder die Beschreibung zu knapp ist, frage gezielt:

```
Was ist der Bug? Beschreibe kurz:
1. Was passiert? (Symptom)
2. Was sollte stattdessen passieren? (Erwartung)
3. Wie kann man den Fehler ausloesen? (Schritte)
```

Aus dem Freitext oder den Antworten extrahiere:
- **Symptom** — Was passiert falsch?
- **Erwartetes Verhalten** — Was sollte passieren?
- **Reproduktionsschritte** — Wie loest man den Bug aus?
- **Kontext** — Betroffene Datei/Komponente/Seite (falls erkennbar)

---

## Schritt 2: Severity einschaetzen

Schlage eine Severity vor basierend auf der Beschreibung:

| Severity | Bedeutung |
|----------|-----------|
| **Kritisch** | App stuerzt ab, Datenverlust, Security-Luecke |
| **Hoch** | Feature unbenutzbar, kein Workaround |
| **Mittel** | Feature eingeschraenkt, Workaround vorhanden |
| **Niedrig** | Kosmetisch, Edge-Case, minimaler Impact |

Frage den Benutzer nur bei Unklarheit — sonst schlage die Severity vor und verwende sie direkt.

---

## Schritt 3: Bug-Name / Slug ermitteln

Leite einen kurzen, beschreibenden Namen aus der Bug-Beschreibung ab.
- Max. 3-4 Woerter
- Leite den **kebab-case-Slug** ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "Login geht nicht" → `features/login-broken/`). Ein eigenstaendiger Bug ist ein eigener Change-Ordner
- Bei Slug-Kollision → melden und anderen Namen erfragen (§4)

---

## Schritt 4: bug.md speichern

### Datei

- Pfad: `{config.paths.workflows}/features/{slug}/bug.md` (Ordner bei Bedarf anlegen)
- Falls Datei bereits existiert: Frage "Bug-Report existiert bereits. Aktualisieren oder neuen Namen waehlen?"

### Template

```markdown
# Bug: [Bug-Name]

**Erstellt:** [YYYY-MM-DD]
**Severity:** Kritisch / Hoch / Mittel / Niedrig
**Status:** Offen
**Betroffene Komponente:** [Datei/Modul/Seite falls bekannt, sonst "Unbekannt"]

---

## Symptom

[Was passiert falsch?]

## Erwartetes Verhalten

[Was sollte stattdessen passieren?]

## Reproduktion

1. [Schritt 1]
2. [Schritt 2]
3. [Schritt 3]

## Kontext

- **Umgebung:** [Browser/OS/Version falls relevant]
- **Erstmals bemerkt:** [Wann/Wobei?]
- **Frequenz:** Immer / Manchmal / Einmalig

---

**Erfasst mit:** `/dtb:bug-report`
```

---

## Schritt 5: Backlog-Eintrag anbieten

Frage den Benutzer:
```
Bug gespeichert: {config.paths.workflows}/features/{slug}/bug.md

Soll der Bug in BACKLOG.md eingetragen werden? (Ja/Nein)
```

**Bei Ja:**
- Lies `{config.paths.workflows}/BACKLOG.md`
- Fuege eine neue Zeile in die Tabelle "Aktive Features" ein:
  `| Bug: {Bug-Name} | Offen | {Severity} | features/{slug}/bug.md | {Symptom-Einzeiler} |`
  (`Offen` = initialer abgeleiteter Status, kein Analyse-Abschnitt vorhanden. Die
  Status-Spalte ist abgeleitete Anzeige und wird danach von `dtb:workflow-checkpoint`
  gepflegt — Regeln: `project-rules/DERIVED_STATE_RULES.md` §1.5)
- Aktualisiere das Datum in "Letzte Aktualisierung"

**Bei Nein:**
```
OK, Bug nicht ins Backlog eingetragen.
Du kannst ihn spaeter mit /dtb:backlog-status sehen (features/*/bug.md werden automatisch erkannt).
```

---

## Schritt 6: Bestaetigung

```
Bug erfasst: {config.paths.workflows}/features/{slug}/bug.md
Severity: {Severity}

Naechste Schritte:
  1. Root-Cause analysieren: /dtb:debug-plan [Bug-Name]
  2. Direkt fixen (bei einfachen Bugs)
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.

---

## Richtlinien

- **Schnell:** Bug erfassen soll den Flow nicht unterbrechen — max. 1-2 Rueckfragen
- **Konkret:** Lieber zu viel Kontext als zu wenig
- **Keine Analyse:** Keine Root-Cause-Suche hier — das macht `/dtb:debug-plan`
- **Deutsch:** Alle Texte auf Deutsch
