---
name: dtb:workflow-checkpoint
description: >-
  Use when: "Session speichern", "checkpoint", "workflow checkpoint",
  "Session dokumentieren". Documents the current development session with
  a session log entry and updates WORKFLOW_STATUS.md.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Bash
pipeline:
  stage: session
  after: [dtb:impl-review, dtb:no-loss-check, dtb:worker]
  next: [dtb:workflow-resume]
  consumes: [BACKLOG.md, INBOX.md, features/*/spec.md, features/*/plan.md, features/*/task.md, features/*/review.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md, ROADMAP.md]
  produces: [WORKFLOW_STATUS.md, BACKLOG.md, features/*/spec.md, features/*/task.md, session-log, ROADMAP.md, project-rules/lessons.md, INBOX.md]
---

# DTB Workflow-Checkpoint (Log + Status)

Du dokumentierst den aktuellen Stand einer Development-Session. Zwei Aufgaben:
1. **Session-Log schreiben** (Tages-Changelog)
2. **WORKFLOW_STATUS.md aktualisieren** (kompaktes Status-Dashboard)

---

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
  ⛔ dtb:workflow-checkpoint schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  **Sende-Seite:** Nach der ⛔-Meldung erzeugt dieser Skill aus dem Sitzungskontext den
  Hand-off-Block (Format: naechste Sektion) und gibt ihn vollstaendig aus — die
  Worktree-Session uebergibt ihn an die Orchestrator-Session (Transport: z.B.
  Herdr-Session-Kommunikation an die Orchestrator-Pane; ohne Herdr manuell kopieren).
  Der Orchestrator checkpointet damit (Empfangsseite: Schritt 1). Es wird weiterhin
  NICHTS geschrieben — der Block ist Chat-Output, keine Datei.

---

## Worktree-Hand-off (Worktree → Orchestrator)

> Nicht zu verwechseln mit dem `## Handoff`-Block in WORKFLOW_STATUS.md (Uebergang
> Session→Folgesession, Teil 2/Schritt 4) — dieses Konzept hier ist die Uebergabe
> Worktree→Orchestrator. Grep-eindeutiges Token: `WORKTREE-HANDOFF`.

### Hand-off-Block (Format — die eine Quelle)

Der Block ist **status-neutral** (`DERIVED_STATE_RULES.md` §1.1): er enthaelt bewusst
KEINE `- [ ]`-Checkboxen (nichts, das eine Status-Ableitung mitzaehlen koennte) — nur
einfache Aufzaehlungen. Pflichtfelder sind die `HANDOFF`-Kopfzeile und `Erledigt:`;
alle uebrigen Felder duerfen mit `- keine` gefuellt sein.

```text
WORKTREE-HANDOFF (dtb) — Quelle: {feature-slug} @ {branch | detached HEAD ({short-sha})}, {YYYY-MM-DD HH:MM}

Erledigt:
- {was wurde umgesetzt, mit Datei-/Schritt-Bezug}

Entscheidungen:
- {getroffene Entscheidung + 1-Satz-Begruendung, oder "- keine"}

Dateien:
- {pfad} - {Kurzbeschreibung, oder "- keine"}

Offene Punkte / Naechste Schritte:
- {offener Punkt, oder "- keine"}

Uebersprungene globale Updates (Teil-Guards):
- {z.B. "INBOX #NN: Link/Status nachziehen", oder "- keine"}
```

**Branch-Angabe:** Steht der Worktree auf einem detached HEAD, ist das der Normalfall,
kein Sonderfall — `dtb:worker` legt seine Worktrees mit `git worktree add {pfad} HEAD`
an (`skills/dtb-worker/SKILL.md`), also ohne Branch. Dann
`detached HEAD ({short-sha})` eintragen, nie raten oder leer lassen.

Die Felder bilden 1:1 auf das Session-Log-Format ab (Teil 1): Erledigt → Implementiert,
Dateien → Dateien, Entscheidungen → Kontext, Offene Punkte → Naechste Schritte.
`skills/CLAUDE.md` (Orchestrator-Muster) verweist hierher — Format nur hier pflegen.

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
- Verlustpruefung: {D} dringend → {L…, #…} erfasst · {W} kann warten (Befehle im Report) · {S} gefiltert

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
- **Verlustpruefung (Pflicht, auch bei 0/0/0)**: letzter Bullet unter `### Implementiert` im festen
  Format oben (Quelle: Schritt 0). Pfeil-Slot: `→ {L…, #…} erfasst` oder `→ nichts erfasst ({Abbruch|alle
  gestrichen|Rueckfall Pfad 1|Rueckfall Pfad 2|>10 Funde})`; bei `D = 0` entfaellt der Pfeil-Teil; wurde die
  Pruefung uebersprungen → `Verlustpruefung uebersprungen — {Grund}` statt der Zaehl-Zeile

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
- Funde gemeldet → die Gruppe „Vor dem Checkpoint erledigen" laeuft durch die Sammelvorlage
  (Unterabschnitt unten), „Kann warten" bleibt kopierfertige Befehle im Report; der Mensch
  entscheidet. **Der Checkpoint bricht nie ab** — `no-loss-check` ist empfehlend, nicht
  blockierend; die Vorlage ist der eine Kontrollpunkt und ersetzt dessen Abschlussfrage
- Lief die Pruefung in dieser Sitzung bereits, laeuft sie hier **trotzdem erneut** — dieser Lauf
  sieht alles, was seither dazugekommen ist. Den Zweitlauf regelt `dtb:no-loss-check` (Randfall 3:
  der frueherer Report ist keine Kandidatenquelle, bereits Verworfenes wird nicht unveraendert
  wiederholt)

#### Dringende Funde erfassen (Sammelvorlage)

**Eingang:** In die Vorlage kommen nur die Funde unter `## Vor dem Checkpoint erledigen`; je
Fund liefert die `→ /dtb:{skill} {Argument}`-Zeile den Typ (`lesson` → Lektion, `idea` → Idee)
und den Freitext; andere Skills (`open-question`) kommen nicht in die Vorlage, bleiben Befehle im
Report und zaehlen in `{D}` mit, nie unter „erfasst". Fehlt die Ueberschrift (Gruppe leer), entfaellt
dieser Block **still** — weiter mit Schritt 1. `## Kann warten` bleibt unveraendert: Befehle im Report.

> **Wartungs-Hinweis (Format-Kopplung):** Dieser Block liest das Ausgabe-Muster von
> `dtb:no-loss-check` (die beiden `## `-Gruppen-Ueberschriften, je Fund die `→`-Zeile).
> Aendert sich das Format dort, diesen Parser mitziehen — der Gegen-Hinweis steht am
> Ausgabe-Muster in `skills/dtb-no-loss-check/SKILL.md`.

**Struktur-Check (Kopplungs-Waechter):** Die Erfassungsregeln stehen NICHT hier, sondern in
`dtb:lesson`/`dtb:idea` — vor dem ersten Schreiben muss die Quelle existieren und ihre Anker tragen:

- **Quelle aufloesen — Repo zuerst, dann Installation:** `skills/dtb-{lesson,idea}/SKILL.md`
  relativ zum Projekt-Root, sonst `~/.claude/skills/dtb-{lesson,idea}/SKILL.md`. Bewusst umgekehrt
  zu `dtb:pane-start`: im Kit-Repo ist das Repo die Quelle, aus der `kit-sync` verteilt — die
  installierte Kopie waere waehrend eines Umbaus der Stand von gestern; Zielprojekte haben kein
  `skills/`. Nur die Quellen aufloesen, deren Typ in der dringenden Gruppe vorkommt
- **Anker-Grep** zeilenverankert auf den ganzen Titel (`tr -d '\r' | grep -x -F`), nie als
  Substring — die Kopplungs-Hinweise darunter zitieren den Titel selbst und wuerden ein
  falsches Gruen liefern:

  | Quelle | Anker (woertlich) | Traegt |
  |--------|-------------------|--------|
  | `dtb:lesson` | `## Schritt 2: In 4 Felder strukturieren` | Feld-Ableitung |
  | `dtb:lesson` | `## Schritt 3: Duplikat-Check` | Duplikat-Bewertung Lektion |
  | `dtb:lesson` | `## Schritt 4: Append-only speichern` | Schreibmechanik `lessons.md` |
  | `dtb:idea` | `## Duplikat-Check` | Duplikat-Bewertung Idee |
  | `dtb:idea` | `## Schritt 2: In INBOX.md speichern` | Schreibmechanik `INBOX.md` |

- Alle Anker gefunden → eine Statuszeile, weiter: `🧩 Struktur-Check: {n}/{n} Anker in {aufgeloeste Quelle(n)} gefunden`
- **Zwei getrennte Fehlerpfade** (nie vermischen — eine fehlende Installation ist KEINE Drift);
  beide enden im **Rueckfall je Quelle**: die Funde des gefallenen Typs bleiben Befehle im Report,
  die Vorlage traegt nur Typen mit gruener Quelle; faellt jede Quelle, weiter mit Schritt 1:

  1. Datei in beiden Quellen nicht gefunden → Installations-Problem:
     ```
     ⚠ Erfassungs-Quelle dtb:{lesson|idea} weder im Projekt (skills/) noch global
        (~/.claude/skills/) gefunden. → /dtb:kit-sync sync, Funde bleiben Befehle im Report.
     ```
  2. Datei vorhanden, Anker fehlt → Struktur-Drift:
     ```
     ⚠ Struktur-Check fehlgeschlagen: {Quelle} — Anker "{Anker}" nicht gefunden.
        dtb:{lesson|idea} wurde umgebaut; ich schreibe NICHT auf veralteter Basis. → diesen
        Block anpassen (die Kopplungs-Hinweise dort nennen diesen Leser). Funde bleiben Befehle.
     ```

> **Benanntes Restrisiko:** Der Check prueft Anker-EXISTENZ, nicht Regel-INHALT. Gegen
> inhaltliche Drift verteidigen die Kopplungs-Hinweise an den fuenf Sektionen — bei
> Aenderungen dort muss dieser Block mitgezogen werden.

**Vorbereitung je Fund (per Referenz — die Regeln dort lesen, nicht hier):**
- Lektion → `## Schritt 2: In 4 Felder strukturieren` und `## Schritt 3: Duplikat-Check` aus
  `dtb:lesson`; Idee → `## Duplikat-Check` aus `dtb:idea` (Read auf die aufgeloeste Quelle)
- Duplikat-Treffer werden **nicht** einzeln gefragt (zweite Rueckfrage-Runde): der Fund erscheint **vorgestrichen** mit Fundstelle

**Sammelvorlage** (Kurzfassung je Fund — nie der volle Wortlaut der vier Felder):

```
# Verlustfunde erfassen — {D} dringend
1  Lektion  {Rule-Satz gekuerzt}                    → lessons.md
2  Idee     {Idee-Satz gekuerzt}                    → INBOX.md
~~3~~ Lektion {…} — aehnlich L23 (vorgestrichen; "behalte 3" nimmt sie auf)
Ok fuer alle nicht gestrichenen? (Ok / streiche {Nr,…} / behalte {Nr} / Abbruch)
```

Antwortregeln:
- `Ok` → alle nicht gestrichenen Zeilen werden geschrieben
- `streiche 2` / `behalte 3` als Freitext, kombinierbar; nur das Geaenderte kurz
  rueckbestaetigen, nicht die ganze Vorlage erneut zeigen (Muster `dtb:feature-fast`)
- `streiche` heisst verwerfen, nicht vertagen (Randfall 3 von `no-loss-check`) — wer nur vertagen
  will, setzt den Befehl aus dem Report ab
- `Abbruch` → nichts schreiben, eine Meldezeile, weiter mit Schritt 1
- **Fallback:** jede andere Antwort gilt als NICHT bestaetigt — genau eine Rueckfrage
  (`Ok / streiche {Nr} / behalte {Nr} / Abbruch?`); bleibt sie unklar → `Abbruch`, nie stiller Auto-Write
- Mehr als 10 dringende Funde → keine Vorlage, Rueckfall auf Befehle mit einer Hinweiszeile

**Schreiben (per Referenz):** je bestaetigtem Fund
- Lektion → `## Schritt 4: Append-only speichern` aus `dtb:lesson`
- Idee → `## Schritt 2: In INBOX.md speichern` aus `dtb:idea`
- **Herkunfts-Marker** als Suffix im Textfeld, Wortlaut `(via Checkpoint {YYYY-MM-DD})`: lessons → Ende von `Context`, INBOX → Ende des Idee-Texts; keine neue Spalte
- Schreibfehler mitten drin → melden, was geschrieben ist, Rest als Befehle ausgeben — **nie zurueckrollen** (append-only)

**Meldung:** eine Zeile je Eintrag — `✔ L{N} → lessons.md` / `✔ #{N} → INBOX.md`;
alle gestrichen → `Nichts erfasst — {D} Fund(e) bleiben als Befehle im Report`.

**Selbstpruefung (L15):** Dieser Block **beschreibt** nirgends, wie Felder abgeleitet, Duplikate bewertet oder Zeilen angehaengt werden — nur Anker; ein solcher Satz waere ein Spiegel.

### Schritt 1: Informationen sammeln

**Empfangsseite (Worktree-Hand-off):** Enthaelt der Aufruf einen Hand-off-Block (Argument
oder eingefuegter Text, erkennbar an der Kopfzeile `WORKTREE-HANDOFF (dtb) — Quelle: …`):
1. Pflichtfelder pruefen (Kopfzeile mit Slug/Branch + `Erledigt:`) — fehlt eines →
   nachfragen, NICHT raten
2. Die Session-Inhalte aus dem BLOCK schoepfen statt aus dem Chat-Verlauf (Zuordnung:
   Erledigt → Implementiert, Dateien → Dateien, Entscheidungen → Kontext,
   Offene Punkte → Naechste Schritte)
3. Den Log-Eintrag mit Quell-Kennzeichnung schreiben: Kontext beginnt mit
   `Worker-Session (Worktree {branch}, Hand-off {YYYY-MM-DD HH:MM})`
4. `Uebersprungene globale Updates` aus dem Block als offene Punkte in
   `### Naechste Schritte` uebernehmen (dort ALS Checkboxen — der Block selbst traegt
   keine) bzw. direkt in diesem Lauf nachziehen, wenn trivial (z.B. INBOX-Link)
Ohne Hand-off-Block: normal aus dem Chat-Verlauf (unten).

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
