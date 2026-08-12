---
name: dtb:workflow-checkpoint
description: >-
  Use when: "Session speichern", "checkpoint", "workflow checkpoint",
  "Session dokumentieren". Documents the current development session with
  a session log entry and updates WORKFLOW_STATUS.md.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
pipeline:
  stage: session
  after: [dtb:impl-review, dtb:no-loss-check]
  next: [dtb:workflow-resume]
  consumes: [BACKLOG.md, INBOX.md, features/*/spec.md, features/*/plan.md, features/*/task.md, features/*/review.md, project-rules/DERIVED_STATE_RULES.md, ROADMAP.md]
  produces: [WORKFLOW_STATUS.md, BACKLOG.md, features/*/spec.md, features/*/task.md, session-log, ROADMAP.md]
---

# DTB Workflow-Checkpoint (Log + Status)

Du dokumentierst den aktuellen Stand einer Development-Session. Zwei Aufgaben:
1. **Session-Log schreiben** (Tages-Changelog)
2. **WORKFLOW_STATUS.md aktualisieren** (kompaktes Status-Dashboard)

---

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
  ⛔ dtb:workflow-checkpoint schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele Sessions").
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Die Worktree-Session uebergibt ihre Session-Inhalte stattdessen als Hand-off an die
  Orchestrator-Session, die dort checkpointet (Sende-Seite: die Meldung erzeugt kuenftig
  den Hand-off-Block — bis dahin Inhalte manuell in die Orchestrator-Session tragen).

---

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfade `dtb-project/project-workflows/` und `dtb-project/project-changelog/`.

---

## Teil 1: Session-Log

### Datei
- Pfad: `{config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md`
- Falls Datei existiert: Neue Session anhaengen (mit `---` Trenner)
- Falls neu: Neue Datei erstellen

### Session-Nummer
- Zaehle vorhandene Sessions in der Datei
- Neue Session bekommt naechste Nummer
- Zeitstempel: Aktuelle Zeit (HH:MM Format)

### Format

```markdown
## Session {N} - {HH:MM}

### Implementiert
- Feature/Fix/Aenderung 1
- Feature/Fix/Aenderung 2

### Dateien
- `pfad/zur/datei.py` - Kurzbeschreibung der Aenderung

### Kontext
1-2 Saetze: Warum diese Aenderungen? Welches Problem wurde geloest?

### Naechste Schritte
- [ ] Offener Punkt 1
- [ ] Offener Punkt 2
```

### Richtlinien
- **Technisch**: Dateinamen, Funktionsnamen, konkrete Werte
- **Praezise**: Was genau wurde geaendert, nicht nur "Code optimiert"
- **Kontext**: Kurz erklaeren warum, nicht nur was
- **Deutsch**: Alle Texte auf Deutsch

---

## Teil 2: WORKFLOW_STATUS.md aktualisieren

### Datei
- Pfad: `{config.paths.workflows}/WORKFLOW_STATUS.md`
- **IMMER UEBERSCHREIBEN** (nicht anhaengen)
- **Max 60-80 Zeilen** — keine Detail-Tabellen, nur 1-Zeilen-Zusammenfassungen mit Links

### Aufbau: generierter Statusblock + manueller Kontextblock

Der Statusblock wird aus Artefakten GENERIERT (Regeln:
`{config.paths.rules}/DERIVED_STATE_RULES.md`, Fallback
`dtb-project/project-rules/DERIVED_STATE_RULES.md`). **Befuelle ausschliesslich die
`{Platzhalter}` — Struktur, Spaltennamen und feste Texte duerfen NICHT umformuliert
werden.** Keine freien Statusaussagen im generierten Block; Prosa gehoert in den
Session-Log oder den Kontextblock.

### Template

```markdown
# Workflow-Status: {config.project_name}

**Letztes Update:** YYYY-MM-DD
**Letzter Session-Log:** `{config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| {Feature/Bug/Task-Name} | {abgeleiteter Status} | {X/Y oder —} | {erster nicht abgehakter Schritt N.M oder /dtb:skill} |

{Pro Konflikt genau 1 Zeile: ⚠ {Item}: {Quelle} sagt "{Feld}", Artefakte zeigen "{abgeleitet}"}
{Falls keine aktiven Items: "Kein aktives Feature."}

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine / [Beschreibung] |
| **Notizen** | [optional, 1 Zeile] |

---

## Offene Aufgaben

- [ ] [Aufgabe 1] — Kontext: [kurz]
- [ ] [Aufgabe 2] — Kontext: [kurz]

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| YYYY-MM-DD | [Meilenstein] | [Ergebnis] | `[Link zu Quelle]` |

---

## Pausierte Themen

### [Ticket-ID]: [Titel]
**Status:** [Warum pausiert]
**Details:** `[Link zu Planfile oder Testbericht]`

---

## Handoff

**Naechster Befehl:** `{konkret abgeleiteter Befehl, z.B. /dtb:feature-start oder /dtb:impl-plan NAME}`
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume` (stellt Kontext her), danach obigen Befehl.
```

### Handoff generieren (Schritt 4)

Der Handoff-Block ist die **Sende-Seite** des Uebergangs (Gegenstueck: `dtb:workflow-resume` liest ihn).
- **Naechster Befehl** wird aus dem abgeleiteten Stand bestimmt: Feature „Geplant" (0/Y) →
  `/dtb:feature-start`; Feature „In Arbeit" (erster nicht abgehakter `## Progress`-Schritt) →
  `/dtb:implement {NAME}`; Feature „Fertig zum Testen" (Y/Y) ∧ **keine** `features/{slug}/review.md` →
  `/dtb:impl-review {NAME}` (Feature-End-Review vor der Abnahme); existiert `features/{slug}/review.md`
  mit Gesamt-Verdikt **REJECTED** → `/dtb:implement {NAME}` (Rueckweg zur Nacharbeit, danach frisches
  Review); PLAN fehlt → `/dtb:impl-plan {NAME}`; kein aktives Item → `/dtb:workflow-next`
- **Fallback:** Ist kein naechster Befehl eindeutig ableitbar, KEINEN erfinden — schreibe
  `Naechster Befehl: — offen — (mit /dtb:workflow-next bestimmen)`
- Format stabil halten (Zeilen `**Naechster Befehl:**` / `**Empfehlung:**`), damit die Empfangs-Seite es zuverlaessig liest

### Kernprinzip
- **Statusblock = generiert**, Kontextblock = manuell — niemals mischen
- **Keine Detail-Tabellen** in WORKFLOW_STATUS
- Nur **1-Zeilen-Zusammenfassungen** mit Link zur Quelle
- Details leben in Session-Logs, Testberichten, Planfiles

---

## Ausfuehrung

### Schritt 0: Verlustpruefung (vorgeschaltet)

Bevor du Informationen sammelst, laeuft `/dtb:no-loss-check` — er vergleicht den
Gespraechsverlauf gegen den Artefakt-Stand und meldet, was nur im Chat lebt (Lektionen,
Fach-Fragen, Ideen ohne Ablage). Der Grund fuer die Position: **nur hier** kann ein Fund den
Inhalt dieses Checkpoints noch beeinflussen; nach Schritt 3 ist der Log geschrieben.

Der Aufruf ist moeglich, obwohl dieser Skill selbst gegen Modell-Aufrufe gesperrt ist —
`dtb:no-loss-check` traegt `disable-model-invocation: false` und darf aus einem laufenden
Skill angestossen werden.

**Weich, nie blockierend:**
- Skill nicht installiert (kein `dtb:no-loss-check` verfuegbar) → **eine** Hinweiszeile
  (`Verlustpruefung uebersprungen — dtb:no-loss-check nicht installiert (/dtb:kit-sync)`),
  danach unveraendert weiter mit Schritt 1
- Funde gemeldet → die kopierfertigen Befehle stehen im Report; der Mensch entscheidet, ob er
  sie absetzt. **Der Checkpoint wartet nicht darauf und bricht nie ab** — `no-loss-check` ist
  empfehlend, nicht blockierend
- Lief die Pruefung in dieser Sitzung bereits, laeuft sie hier **trotzdem erneut** — dieser Lauf
  sieht alles, was seither dazugekommen ist. Den Zweitlauf regelt `dtb:no-loss-check` (Randfall 3:
  der frueherer Report ist keine Kandidatenquelle, bereits Verworfenes wird nicht unveraendert
  wiederholt)

### Schritt 1: Informationen sammeln

**Aus Chat-Verlauf:**
- Was wurde implementiert/geaendert?
- Welche Entscheidungen wurden getroffen?
- Was sind naechste Schritte?
- Gibt es Blocker?

**Aus Git (alle config.repos pruefen):**
```bash
git -C {repo.path} status --short && git -C {repo.path} log --oneline -3
```

### Schritt 2: Status ableiten & Anzeige-Felder synchronisieren

Der Status wird NICHT abgefragt, sondern ABGELEITET (Regel-Datei lesen, siehe Teil 2):

1. **Leite den Status aller aktiven Items ab:** `features/*/plan.md` `## Progress`-Checkboxen zaehlen
   (0/Y = Geplant, X/Y = In Arbeit, Y/Y = Fertig zum Testen); Bugs/Tasks ueber die
   Checkliste in `bug.md`/`task.md` (Regel-Datei §1.5). Pruefe dabei, ob Checkboxen dieser Session
   abgehakt wurden — falls nicht, erinnere daran (Flip-Bedingung §2, Loop in `dtb:implement`)
2. **Synchronisiere die Anzeige-Felder** mit dem abgeleiteten Status (dieser Skill ist der
   schreibende Skill aus Regel-Datei §1.3):
   - Status-Spalte in BACKLOG.md (Abschnitte "Aktive Features"/"Aufgaben")
   - `**Status:**`-Zeile in `features/<slug>/spec.md` bzw. `task.md`
   - Datum in "Letzte Aktualisierung"
   - **Falls `dtb-project/project-strategy/ROADMAP.md` existiert**: Statusspalte nach Regel-Datei §5
     synchronisieren (Change-ID = Slug → Ordner-Zustand: `archive/<slug>/` = `done`,
     `features/<slug>/` = `in-progress`, sonst gesetzter Doc-Status). Existiert die Datei
     nicht → still ueberspringen (kein Hinweis)
3. **Nur explizite Zustaende erfragen** (Regel-Datei §1.2 — nicht ableitbar). Frage NUR,
   wenn ein Item vollstaendig abgehakt ist oder der Chat-Verlauf es nahelegt:

```
{Item-Name} ist fertig umgesetzt (alle Schritte abgehakt).
  1. Fertig zum Testen (Standard — keine Aktion noetig)
  2. Abgenommen (getestet & freigegeben — Beleg-Rueckfrage folgt)
  3. Abgeschlossen → /dtb:archive
  4. Pausiert (mit Grund)
```

   **Beleg-Rueckfrage bei „Abgenommen" (Verifikations-Gate der Abnahme):** „Abgenommen"
   wird NICHT auf blossen Zuruf gesetzt. Bei Wahl 2:
   1. Lies die `#### Manual`-Checkpoint-Kriterien aus `features/{slug}/plan.md` und liste
      die offenen (Alt-Plan ohne geteilte Kriterien → alle Kriterien listen):
      ```
      Abnahme {Item-Name} — diese manuellen Pruefungen belegen die Abnahme:
        - [ ] {Manual-Kriterium}
      Bestaetigt? Kurzer Beleg (1 Zeile, z.B. "im Zielprojekt X durchgespielt"):
      ```
   2. Antwort des Nutzers als 1-Zeilen-Beleg in den Session-Log uebernehmen
      (Abschnitt „Implementiert" oder „Kontext": `Abnahme {Item}: {Beleg}`)
   3. **Keine/ausweichende Antwort → Status bleibt „Fertig zum Testen"** (kein stilles
      Durchwinken); hat der Plan gar keine Kriterien, genuegt der Freitext-Beleg

4. **Falls kein aktives Item betroffen ist**, ueberspringe diesen Schritt ohne Nachfrage.

### Schritt 3: Session-Log schreiben

### Schritt 4: WORKFLOW_STATUS.md aktualisieren
- Halte die 60-80 Zeilen-Grenze ein

### Schritt 5: Archiv-Hinweis pruefen

Zaehle in INBOX.md (Status `Verworfen` + `Ausgearbeitet`) und BACKLOG.md (Abschnitt "Abgeschlossen") die archivierbaren Eintraege.

- Falls >5 archivierbare Eintraege: Hinweis in die Bestaetigung aufnehmen
- Falls <=5: Keinen Hinweis zeigen

### Schritt 6: Bestaetigung

```
Workflow-Checkpoint dokumentiert:

Session-Log: {config.paths.changelog}/YYYY-MM/YYYY-MM-DD.md (Session N)
Status: {config.paths.workflows}/WORKFLOW_STATUS.md
{Falls Feature-Update: "Feature-Update: {Feature-Name} → {neuer Status}"}

Naechster Schritt: [Konkret]
Blocker: [Keine / Beschreibung]
{Falls >5 archivierbare Eintraege: "Aufraumen: {N} Eintraege koennten archiviert werden → /dtb:archive"}

Fuer naechste Session: /dtb:workflow-resume
```
