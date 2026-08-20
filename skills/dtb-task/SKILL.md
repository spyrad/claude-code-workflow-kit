---
name: dtb:task
description: >-
  Use when: "Aufgabe erfassen", "task anlegen", "Housekeeping",
  "Wartungsaufgabe", "operativ", "Aufgabe erstellen", "task".
  Captures a lightweight operational/infrastructure task as
  features/<slug>/task.md in the features directory.
disable-model-invocation: true
argument-hint: "[Aufgaben-Beschreibung als Freitext]"
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: idea
  after: [dtb:idea-review]
  next: [dtb:worker]
  consumes: [BACKLOG.md]
  produces: [features/*/task.md, BACKLOG.md]
---

# Aufgabe erfassen

Du erfasst eine operative oder infrastrukturelle Aufgabe schnell und strukturiert. Aufgaben sind leichtgewichtiger als Features — kein Spec/Plan-Zyklus, sondern direkte Checkliste.

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
  ⛔ dtb:task schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Wurde bereits Text uebergeben/erfasst, haengt die Meldung ihn als fertigen Befehl an —
  „Dein Text geht nicht verloren — dort absetzen: `/dtb:task "{erfasster Text}"`".
  Greift der Abbruch VOR dem Erfassungs-Dialog, gibt es nichts zu echoen — nur den
  Befehl ohne Text-Anteil nennen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Aufgaben-Informationen sammeln

**Input:** Der Freitext nach dem Command-Aufruf ist die Aufgaben-Beschreibung.

Falls kein Freitext angegeben wurde oder die Beschreibung zu knapp ist, frage gezielt:

```
Was soll gemacht werden? Beschreibe kurz:
1. Was genau ist die Aufgabe?
2. Warum ist das noetig?
3. Welcher Bereich ist betroffen? (System/Komponente/Infrastruktur)
```

Aus dem Freitext oder den Antworten extrahiere:
- **Beschreibung** — Was genau soll gemacht werden?
- **Begruendung** — Warum ist das noetig? Was passiert wenn es nicht gemacht wird?
- **Bereich** — Betroffenes System, Komponente oder Infrastruktur-Bereich
- **Schritte** — Konkrete Teilschritte als Checkliste (3-7 Punkte)

---

## Duplikat-Check

Vor Prioritaet und Slug-Vergabe (ein erkanntes Duplikat braucht keinen Namen mehr): pruefe die
erfasste Aufgabe **unscharf** gegen die Abschnitte `## Beschreibung` und `## Begruendung` aller
`{config.paths.workflows}/features/*/task.md` (nur aktive Changes; `archive/` wird NIE
durchsucht). Vergleich per Grep nach dem Kern der Aufgabe (Stichworte), Bewertung je Kandidat:

> Gleicher Gegenstand **und** gleiche Aussage — die bestehende Aufgabe koennte die neue Erfassung
> vollstaendig ersetzen → Treffer. Gleicher Gegenstand, andere Aussage → kein Duplikat.
> Im Zweifel: kein Duplikat, still durchlassen.

- **Treffer** (max. 3 zeigen, Rest als `+N weitere`; Bestandstext auf ~120 Zeichen + `…` kuerzen):
  ```
  Aehnliche Aufgabe steht schon in features/{slug}/task.md: "{Bestandstext, gekuerzt}"
  Trotzdem als neue Aufgabe erfassen? (Ja / Abbrechen)
  ```
  Die Entscheidung liegt beim Menschen — **nie hart blocken** (wiederkehrende
  Housekeeping-Aufgaben sind legitim).
- **Kein Treffer → keine Ausgabe**, direkt weiter zu Schritt 2 — der Check ist im Normalfall
  unsichtbar; im Trefferfall kommt genau eine Rueckfrage hinzu (die Richtlinie unten nennt
  diese Ausnahme).
- **Fail-open:** kein `features/`-Ordner oder keine `task.md` vorhanden → Check still
  ueberspringen, kein Hinweis.

(Autoren-Doku: Konvention in `skills/CLAUDE.md` → „Duplikat-Schutz (Capture-Skills)" — dieser
Abschnitt ist zur Laufzeit autark.)

---

## Schritt 2: Prioritaet einschaetzen

Schlage eine Prioritaet vor basierend auf der Beschreibung:

| Prioritaet | Bedeutung |
|------------|-----------|
| **Hoch** | Blockiert andere Arbeit, muss zeitnah erledigt werden |
| **Mittel** | Sollte bald erledigt werden, nicht dringend |
| **Niedrig** | Irgendwann erledigen, Nice-to-have |

Frage den Benutzer nur bei Unklarheit — sonst schlage die Prioritaet vor und verwende sie direkt.

---

## Schritt 3: Task-Name / Slug ermitteln

Leite einen kurzen, beschreibenden Namen aus der Aufgaben-Beschreibung ab.
- Max. 3-4 Woerter
- Leite den **kebab-case-Slug** ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "HANA Schema Audit" → `features/hana-schema-audit/`). Eine eigenstaendige Aufgabe ist ein eigener Change-Ordner
- Bei Slug-Kollision → melden und anderen Namen erfragen (§4)

---

## Schritt 4: task.md speichern

### Datei

- Pfad: `{config.paths.workflows}/features/{slug}/task.md` (Ordner bei Bedarf anlegen)
- Falls Datei bereits existiert: Frage "Aufgabe existiert bereits. Aktualisieren oder neuen Namen waehlen?"
  (Das ist die **Namens**-Kollision — `DERIVED_STATE_RULES.md` §4; die **Inhalts**-Dublette prueft
  der Duplikat-Check oben, beide Pruefungen bleiben getrennt.)

### Template

```markdown
# Aufgabe: [Aufgaben-Name]

**Erstellt:** [YYYY-MM-DD]
**Prioritaet:** Hoch / Mittel / Niedrig
**Status:** Offen
**Bereich:** [System/Komponente/Infrastruktur-Bereich]

---

## Beschreibung

[Was genau soll gemacht werden?]

## Begruendung

[Warum ist das noetig? Was passiert wenn es nicht gemacht wird?]

## Schritte

- [ ] [Schritt 1]
- [ ] [Schritt 2]
- [ ] [Schritt 3]

## Ergebnis

[Was ist das erwartete Ergebnis / Definition of Done?]

---

**Erfasst mit:** `/dtb:task`
```

---

## Schritt 4b: INBOX-Rueckverlinkung (falls aus Idee geroutet)

Stammt die Aufgabe aus einer INBOX-Idee (Dreier-Weiche von `dtb:idea-review`, Argument
nennt eine Nummer, oder der Chat-Kontext zeigt es):

- Haenge an die Idee-Zeile in `{config.paths.workflows}/INBOX.md` den Link
  `→ features/{slug}/task.md` an
- Steht die Idee noch nicht auf `Ausgearbeitet`, setze sie darauf (die Weiche hat das
  im Regelfall schon getan — hier nur nachziehen, nie zurueckstufen)

Ohne INBOX-Herkunft: Schritt still ueberspringen.

---

## Schritt 5: Backlog-Eintrag anbieten

Frage den Benutzer:
```
Aufgabe gespeichert: {config.paths.workflows}/features/{slug}/task.md

Soll die Aufgabe in BACKLOG.md eingetragen werden? (Ja/Nein)
```

**Bei Ja:**
- Lies `{config.paths.workflows}/BACKLOG.md`
- Fuege eine neue Zeile in die Tabelle "Aufgaben" ein:
  `| {Aufgaben-Name} | Offen | {Prioritaet} | features/{slug}/task.md | {Beschreibung-Einzeiler} |`
  (`Offen` = initialer abgeleiteter Status, 0 Schritte abgehakt. Die Status-Spalte ist
  abgeleitete Anzeige und wird danach von `dtb:workflow-checkpoint` gepflegt —
  Regeln: `project-rules/DERIVED_STATE_RULES.md` §1.5)
- Falls die Sektion "Aufgaben" noch nicht existiert, fuege sie zwischen "Aktive Features" und "Ideen / Backlog" ein:
  ```markdown
  ## Aufgaben

  | Aufgabe | Status | Prio | Datei | Beschreibung |
  |---------|--------|------|-------|--------------|
  | {Aufgaben-Name} | Offen | {Prioritaet} | features/{slug}/task.md | {Beschreibung-Einzeiler} |
  ```
- Aktualisiere das Datum in "Letzte Aktualisierung"

**Bei Nein:**
```
OK, Aufgabe nicht ins Backlog eingetragen.
Du kannst sie spaeter mit /dtb:backlog-status sehen (features/*/task.md werden automatisch erkannt).
```

---

## Schritt 6: Bestaetigung

```
Aufgabe erfasst: {config.paths.workflows}/features/{slug}/task.md
Prioritaet: {Prioritaet}

Naechste Schritte:
  1. Direkt starten: /dtb:feature-start
  2. Spaeter im Backlog finden: /dtb:backlog-status
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.

---

## Richtlinien

- **Schnell:** Aufgabe erfassen soll den Flow nicht unterbrechen — max. 1-2 Rueckfragen
  (ein Duplikat-Treffer kann eine weitere hinzufuegen; ohne Treffer bleibt der Check still)
- **Konkret:** Checkliste mit konkreten Schritten, keine vagen Beschreibungen
- **Leichtgewichtig:** Kein Plan oder Spec noetig — Aufgaben sind direkte Action-Items
- **Deutsch:** Alle Texte auf Deutsch
