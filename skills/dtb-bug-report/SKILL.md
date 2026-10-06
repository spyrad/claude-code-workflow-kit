---
name: dtb:bug-report
description: >-
  Use when: "Bug melden", "bug report", "Fehler gefunden", "Bug erfassen",
  "das geht nicht", "Fehler notieren". Captures a bug report with reproduction
  steps and saves it as features/<slug>/bug.md in the features directory.
disable-model-invocation: true
argument-hint: "[Bug-Beschreibung als Freitext]"
allowed-tools: Read, Write, Glob, Grep, Bash
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

## Duplikat-Check

Vor Severity und Slug-Vergabe (ein erkanntes Duplikat braucht keinen Namen mehr): pruefe das
erfasste Symptom **unscharf** gegen den Abschnitt `## Symptom` aller
`{config.paths.workflows}/features/*/bug.md` (nur aktive Changes; `archive/` wird NIE durchsucht —
ein Treffer auf einen dort abgeschlossenen Bug waere ein Regressions-Signal, keine Dublette, und
Regressions-Erkennung ist bewusst nicht Teil dieses Checks). Kandidaten per Grep nach dem Kern des
Symptoms (Stichworte) finden, dann `## Symptom` lesen und je Kandidat bewerten:

> Gleicher Gegenstand **und** gleiche Aussage — der bestehende Bug-Report koennte die neue
> Erfassung vollstaendig ersetzen → Treffer. Gleicher Gegenstand, andere Aussage (z.B. gleiches
> Modul, anderes Symptom) → kein Duplikat. Im Zweifel: kein Duplikat, still durchlassen.

- **Treffer** (max. 3 zeigen — je Treffer eine Fundstellen-Zeile, Rest als `+N weitere`, die
  Entscheidungsfrage genau einmal am Ende; Bestandstext auf ~120 Zeichen + `…` kuerzen):
  ```
  Aehnlicher Bug steht schon in features/{slug}/bug.md: "{Bestandstext, gekuerzt}"
  Trotzdem als neuen Bug erfassen? (Ja / Abbrechen)
  ```
  Die Entscheidung liegt beim Menschen — **nie hart blocken** (ein wiederkehrender Fehler darf
  legitim erneut erfasst werden).
  **Abbrechen** → eine Zeile `Nicht gespeichert — Bestand: features/{slug}/bug.md`, Skill endet.
- **Kein Treffer → keine Ausgabe**, direkt weiter zu Schritt 2 — der Check ist im Normalfall
  unsichtbar; im Trefferfall kommt genau eine Rueckfrage hinzu (die Richtlinie unten nennt
  diese Ausnahme).
- **Fail-open:** kein `features/`-Ordner oder keine `bug.md` vorhanden → Check still
  ueberspringen, kein Hinweis.

(Autoren-Doku: Konvention in `skills/CLAUDE.md` → „Duplikat-Schutz (Capture-Skills)" — dieser
Abschnitt ist zur Laufzeit autark.)

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
  (Das ist die **Namens**-Kollision — `DERIVED_STATE_RULES.md` §4; die **Inhalts**-Dublette prueft
  der Duplikat-Check oben, beide Pruefungen bleiben getrennt.)

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

## Schritt 5: Backlog-Eintrag (ohne Rueckfrage)

Keine Frage — der Eintrag ist der Default (gleiche Datenlage wie bei `dtb:task`: „Nein" kam nur
in Testlaeufen vor; eine BACKLOG-Zeile ist eine abgeleitete Anzeige und per Zeilen-Loeschung
billig umkehrbar). Ergebnis ist genau eine Anzeige-Zeile, die als `{Backlog-Zeile}` in der
Bestaetigung (Schritt 6) erscheint: `→ in BACKLOG.md eingetragen (Status: Offen)`

**Testordner-Ausnahme:** Beginnt der Slug mit `zz-test-` oder `abnahmeprobe-` → KEIN Eintrag,
stattdessen die Anzeige-Zeile `→ kein BACKLOG-Eintrag (Testordner)`.

**BACKLOG.md fehlt oder ist unlesbar** → kein Eintrag, kein Abbruch, genau die Zeile
`⚠ BACKLOG.md fehlt oder ist unlesbar — kein Eintrag, weiter` (`/dtb:backlog-status` erkennt
`features/*/bug.md` ohnehin).

**Eintrag schreiben:**
- Lies `{config.paths.workflows}/BACKLOG.md`
- Fuege eine neue Zeile in die Tabelle "Aktive Features" ein:
  `| — | Bug: {Bug-Name} | Offen | {Severity} | features/{slug}/bug.md | {Symptom-Einzeiler} |`
  (`Offen` = initialer abgeleiteter Status, kein Analyse-Abschnitt vorhanden. Die
  Status-Spalte ist abgeleitete Anzeige und wird danach von `dtb:workflow-checkpoint`
  gepflegt — Regeln: `project-rules/DERIVED_STATE_RULES.md` §1.5)
- **Spalte `#` (INBOX-Nummer):** Startwert `—` — dieser Skill kennt keine Idee;
  `dtb:workflow-checkpoint` fuellt die Nummer nach, falls spaeter eine Idee auf diese
  `bug.md` verlinkt
- **Kopf ohne `#`** (Bestandsprojekt, Tabelle noch im alten Format) → Zeile im alten Format
  ohne erste Spalte schreiben, nicht selbst umbauen — `dtb:workflow-checkpoint` ergaenzt die
  Spalte und fuellt die Nummer nach
- Aktualisiere das Datum in "Letzte Aktualisierung"

(Form-Kanon fuer Autoren: `skills/CLAUDE.md` → „Rueckfragen-Defaults (Veto-Form)", Zeile A.)

---

## Schritt 6: Bestaetigung

```
Bug erfasst: {config.paths.workflows}/features/{slug}/bug.md
Severity: {Severity}
{Backlog-Zeile}

Naechste Schritte:
  1. Root-Cause analysieren: /dtb:debug-plan [Bug-Name]
  2. Direkt fixen (bei einfachen Bugs)
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.

---

## Richtlinien

- **Schnell:** Bug erfassen soll den Flow nicht unterbrechen — max. 1-2 Rueckfragen
  (ein Duplikat-Treffer kann eine weitere hinzufuegen; ohne Treffer bleibt der Check still)
- **Konkret:** Lieber zu viel Kontext als zu wenig
- **Keine Analyse:** Keine Root-Cause-Suche hier — das macht `/dtb:debug-plan`
- **Deutsch:** Alle Texte auf Deutsch
