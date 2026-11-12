---
name: dtb:pane-start
description: >-
  Use when: "pane start", "Session in eigener Pane starten", "Voll-Schiene
  im Worktree starten", "interaktive Session aufsetzen", "Arbeitsplatz fuer
  Change einrichten". Sets up an interactive full-lane session for one change:
  own worktree, own named tab in the Herdr app, a started Claude session, and ONE
  greeting message carrying workplace, start command, orchestrator address and
  the return-path duty. Writes no artifacts and no central files; no autonomy
  governance — a human works in the pane.
disable-model-invocation: true
argument-hint: "[INBOX-Nummer | Change-Slug]"
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: execution
  after: [dtb:idea-review]
  next: [dtb:feature-discover, dtb:feature-fast]
  consumes: [INBOX.md, workflow.config.yaml, features/*/discovery.md, features/*/plan.md, features/*/spec.md]
  produces: []
---

# Interaktive Session in Pane + Worktree starten

Du richtest fuer EINEN Change einen eigenen Arbeitsplatz ein — Worktree, eigener Tab in der
Herdr-App, laufende Session — und stellst dieser Session EINEN Begruessungstext zu. Danach
kehrst du zur eigenen Arbeit zurueck; im Tab arbeitet ein **Mensch**.

**Abgrenzung zu `dtb:worker` (Traeger `pane`):** Dieselbe Herdr-Mechanik, anderer Zweck.
`dtb:worker` stellt einen **autonomen Auftrag** auf Basis einer `task.md` zu und unterliegt
der Autonomie-Regel (Versuchslimit, Zeitdeckel, Tauglichkeitsraster, Bericht). Dieser Skill
stellt einen **Begruessungstext** zu und hat davon nichts — es sitzt jemand drin. Was beide
teilen, ist die Start-Sequenz; sie lebt ausschliesslich in `dtb:worker` und wird
hier NUR referenziert, niemals kopiert (Drift-Schutz — Details: `## Herdr-Mechanik`; einzige
deklarierte Ausnahme ist die Rueckweg-Zeile des Begruessungstexts, ein benannter Spiegel —
siehe „Regeln zur Vorlage").

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
  ⛔ dtb:pane-start schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

  Wurde ein Argument uebergeben, haengt die Meldung es als fertigen Befehl an —
  „Dein Ziel geht nicht verloren — dort absetzen: `/dtb:pane-start {Argument}`".
  Greift der Abbruch ohne Argument, gibt es nichts zu echoen — nur den Befehl ohne
  Argument-Anteil nennen.

> **Warum Voll-Guard, obwohl `produces` leer ist:** Dieser Skill schreibt keine Artefakte —
> die Kategorie folgt hier nicht dem `produces`-Kriterium, sondern dem Betrieb: einen
> verlinkten Worktree legt man vom Haupt-Checkout aus an, nie aus einem anderen Worktree.
> Bewusste Abweichung vom Einteilungs-Kriterium in `skills/CLAUDE.md` → `### Skill-Kategorien`.
> Der Satz „schreibt globale Dateien" in Rahmenprosa und ⛔-Fence ist **Vorlagen-Wortlaut**
> (byte-identische Uebernahme der kanonischen Guard-Vorlage, nur der Skill-Name variiert) —
> real schuetzt der Guard hier die Worktree-Anlage, nicht Datei-Schreibzugriffe.

## Herdr-Gate (hart)

**Eligibility-Gate:** Die Session laeuft in einem Terminal der Herdr-App — `$HC_TERMINAL_ID`
nicht leer (die eigene Adresse: ohne sie gibt es keinen Rueckkanal, der Begruessungstext
braucht die Orchestrator-Adresse) UND `hc` im PATH UND `herdr-app` im PATH (ohne `herdr-app`
bekommt der Tab keinen Namen). In EINEM selbstaendigen Bash-Block (dasselbe Gate wie
`dtb:worker` → `### Traeger-Weiche`; Aenderung dort → hier mitziehen):

```bash
[ -n "$HC_TERMINAL_ID" ] && command -v hc >/dev/null 2>&1 && command -v herdr-app >/dev/null 2>&1 && echo "APP-OK $HC_TERMINAL_ID" || echo APP-FEHLT
```

`APP-FEHLT` → Abbruch — KEINE stille Degradierung auf einen anderen Weg:

```
⛔ dtb:pane-start braucht die Herdr-App (eigene Terminal-Adresse $HC_TERMINAL_ID + hc +
   herdr-app), hier nicht verfuegbar.
   Weg: die Herdr-App oeffnen, dort einen Tab im Projektordner anlegen, darin `claude`
   starten. Dein Ziel geht nicht verloren — dort absetzen:
   /dtb:pane-start {Argument}
   Alternativen: die Voll-Schiene direkt in dieser Session fahren (Befehl je nach
   Stand — Tabelle Schritt 1b) oder den Arbeitsplatz manuell einrichten
   (git worktree add + Session von Hand starten).
```

Wurde kein Argument uebergeben, entfallen die `{Argument}`-Anteile der Meldung ersatzlos.

Die alte `herdr`-CLI (Terminal-Multiplexer) ist ein anderes System und sieht die Terminals
der App nicht — sie genuegt diesem Gate nicht (Umstellung 2026-11-12).

Der Skill hat bewusst **keinen** Ersatzpfad: sein ganzer Zweck ist der Hinweg in einen
eigenen Tab. Ohne Tab gibt es nichts zu verkuerzen, und ein halb eingerichteter Arbeitsplatz
waere schlechter als keiner.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

Relevante Werte: `paths.workflows`, `paths.rules`, `parallel.default_branch` (fuer die
Branch-Pruefung des Guards und als Basis des Worktree-Stands).

**Fehlende Keys** (nicht nur fehlende Datei): `paths.rules` fehlt in aelteren Configs →
Fallback `dtb-project/project-rules/`. Fehlt `parallel.default_branch` → wie `null`
behandeln (Branch-Pruefung entfaellt).

## Schritt 1: Argument aufloesen und Vorbedingungen pruefen

### 1a: Argument aufloesen (zwei Einstiegspunkte, ein Argument)

Das Argument ist entweder eine **INBOX-Nummer** oder ein **Change-Slug**. Pruefe in dieser
Reihenfolge:

1. **Rein numerisch** → als INBOX-Nummer behandeln: Eintrag in
   `{config.paths.workflows}/INBOX.md` suchen.
   - Treffer → Slug nach `{config.paths.rules}/DERIVED_STATE_RULES.md` §4 ableiten
     (Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`) und dem
     Nutzer zur Bestaetigung zeigen (kein Auto-Suffix bei Kollision, §4)
   - Kein Treffer → Abbruch (unten)
2. **Nicht numerisch** → als Change-Slug behandeln: existiert
   `{config.paths.workflows}/features/{slug}/`?
   - Ja → Fortsetzung eines angefangenen Change
   - Nein → VOR dem Abbruch einmal die INBOX per Stichwort greppen (das Argument als
     Suchbegriff); genau ein Treffer → als Fund behandeln und zur Bestaetigung zeigen,
     sonst Abbruch (unten)
3. **Kein Argument** → Abbruch (unten). Dieser Skill raet kein Ziel: welcher Change einen
   eigenen Arbeitsplatz bekommt, ist eine Entscheidung, keine Ableitung.

**Abbruch bei unaufloesbarem Argument** — die `Geprueft:`-Zeilen nennen NUR die
tatsaechlich gelaufenen Pruefungen des jeweiligen Zweigs (keine Behauptungen):

```
⛔ Kein Ziel aufloesbar: "{Argument}"
   Geprueft: {je nach Zweig: INBOX.md als Nummer | features/{Argument}/ als Slug
             + INBOX.md als Stichwort}
   → Idee zuerst erfassen: /dtb:idea {Beschreibung}
   → oder vorhandene Ziele sehen: /dtb:backlog-status
```

### 1b: Startbefehl bestimmen (Vorschlag, nie automatisch)

| Lage im Change-Ordner | Vorgeschlagener Startbefehl |
|-----------------------|-----------------------------|
| Ordner existiert nicht (INBOX-Einstieg) | `/dtb:feature-discover {N}` — bei erkennbar kleinem Zuschnitt alternativ `/dtb:feature-fast {N}` |
| `discovery.md` vorhanden, kein `spec.md` | `/dtb:feature-plan {slug}` |
| `spec.md` vorhanden, kein `plan.md` | `/dtb:impl-plan {slug}` |
| `plan.md` mit Kopf-Status `Entwurf` (§7) | `/dtb:plan-review {slug}` |
| `plan.md` `Reviewed`, `## Progress` teilweise/leer | `/dtb:implement {slug}` |
| `plan.md` vollstaendig abgehakt | `/dtb:impl-review {slug}` |

Zeige den Vorschlag mit einem Satz Begruendung und lass ihn bestaetigen oder ersetzen. Der
Skill entscheidet die Schiene nie selbst — er richtet den Arbeitsplatz ein, die Schiene
waehlt der Mensch.

### 1c: Vorbedingungen (in dieser Reihenfolge)

1. **Zielarbeit committet?** (L18) Der Worktree entsteht aus einem Commit und sieht
   Uncommittetes nicht. `git status --short -- {config.paths.workflows}/features/{slug}/`
   muss leer sein; beim INBOX-Einstieg zusaetzlich IMMER
   `git status --short -- {config.paths.workflows}/INBOX.md` (mechanisch statt Ermessen).
   Sonst Abbruch mit Hinweis: erst committen, z.B. via `/dtb:commit-and-push`
2. **Branch frei?** `git branch --list feature/{slug}` muss leer sein. Existiert der Branch,
   melden und Entscheidung einholen (fortsetzen mit bestehendem Branch / anderen Namen /
   abbrechen) — **nie** ueberschreiben
3. **Worktree-Pfad frei?** Der Zielpfad darf nicht existieren und in `git worktree list`
   nicht auftauchen. Sonst melden (ggf. Rest eines frueheren Laufs → `git worktree prune`
   vorschlagen, nicht selbst ausfuehren)
4. **Fremde Session im Haupt-Checkout?** Die Pruefung steht in der Quelle (`dtb:worker` →
   `### Pane-Ausfuehrung`, Unterabschnitt „Hinweg: Vorbedingungen", Punkt 2 — ein
   Bash-Block ueber die Terminal-Liste der App) und wird per Referenz ausgefuehrt, nie
   kopiert. Deshalb laeuft sie als EINZIGE Vorbedingung erst NACH dem `## Struktur-Check`
   (er loest die Quelle auf); sie warnt nur und blockiert nie, die spaetere Stelle kostet
   nichts. Je ausgegebener Adresse genau EINE Warnzeile, dann weiterarbeiten (melden statt
   blockieren; der Startordner ist der Stand beim Start des Terminals und stale-anfaellig):
   ```
   ⚠ Weitere Session im Haupt-Checkout gefunden ({adresse}) — der Worktree-Guard
     deckt diesen Fall nicht (bekannte Grenze: er erkennt nur verlinkte Worktrees).
   ```

   (Wortlaut gespiegelt aus `skills/dtb-worker/SKILL.md` → „Hinweg: Vorbedingungen" —
   Aenderung dort mitziehen.)

## Struktur-Check (Kopplungs-Waechter)

Dieser Skill traegt die Start-Sequenz nicht selbst — er MUSS deshalb **vor jeder
Einrichtung** (nach der Argument-Aufloesung und den Vorbedingungen 1–3 aus Schritt 1, vor
Vorbedingung 4 und dem ersten Kommando der Herdr-Mechanik) pruefen, dass seine Quelle existiert und ihre
Anker-Sektionen noch traegt. Endet ein Lauf schon in Guard, Gate oder Schritt 1, laeuft der
Check planmaessig nie. Ohne ihn gaebe es weder Fallback noch Diagnose: die Quelle koennte
fehlen oder umgebaut sein, und der Ausfall bliebe stumm bis mitten in die Einrichtung.

**Aufloesung der Quelle** (Muster: `dtb:feature-fast` Schritt 2): zuerst die installierte
Kopie `~/.claude/skills/dtb-worker/SKILL.md`, sonst Fallback auf `skills/dtb-worker/SKILL.md`
im Projekt-Root (Kit-Repo-Fall).

**Anker-Grep** (zeilenende-normalisiert — `tr -d '\r'` vorschalten, nie `$`-Anker gegen den
Rohtext) auf alle drei Anker, jeweils **am Zeilenanfang** verankert (`^### …` / `^#### …`) —
sonst zaehlen Erwaehnungen in Prosa und Vorlagen mit, und eine umbenannte Ueberschrift
bliebe unbemerkt:

| Anker (Grep, woertlich, Zeilenanfang) | Traegt |
|---------------------------------------|--------|
| `^### Pane-Ausfuehrung` | Vorbedingungen, Start-Sequenz, Rueckweg, Abschluss |
| `^### Pane-Auftrag` | Vorlagen-Muster fuer den zugestellten Text |
| `^#### Rueckweg: Stand-Pruefung` | Pruefliste und Meldungsform der Stand-Pruefung auf Zuruf („Stand?") |

**Alle drei Anker gefunden** → eine Statuszeile und weiter:
`🧩 Struktur-Check: 3/3 Anker in {aufgeloeste Quelle} gefunden`

**Zwei getrennte Fehlerpfade** (nie vermischen — eine fehlende Installation ist KEINE Drift):

1. **Datei in beiden Quellen nicht gefunden** → Installations-Problem:

   ```
   ⚠ Mechanik-Quelle dtb:worker weder global (~/.claude/skills/) noch im Projekt gefunden.
      → /dtb:kit-sync sync ausfuehren (bzw. install), dann dtb:pane-start erneut starten.
   ```

2. **Datei vorhanden, Anker fehlt** → Struktur-Drift, harter STOPP (keine Einrichtung auf
   veralteter Basis):

   ```
   ⚠ Struktur-Check fehlgeschlagen: {Quelle} — Anker "{Anker}" nicht gefunden.
      Die Pane-Sektionen von dtb:worker wurden umbenannt oder umgebaut; ich richte KEINEN
      Arbeitsplatz auf veralteter Basis ein. → dtb:pane-start an die neue Struktur anpassen
      (die Kopplungs-Hinweise an den Sektionen in dtb:worker nennen diesen Leser).
   ```

> **Benanntes Restrisiko:** Der Check prueft Anker-EXISTENZ, nicht Sequenz-INHALT. Gegen
> inhaltliche Drift verteidigen die Kopplungs-Hinweise in den drei Sektionen von
> `dtb:worker` — bei Aenderungen dort muss dieser Skill mitgezogen werden.

## Herdr-Mechanik (referenziert, nicht dupliziert)

> **Die Start-Sequenz steht NICHT hier.** Quelle ist `dtb:worker` →
> `### Pane-Ausfuehrung`, Unterabschnitt „Hinweg: Start-Sequenz" (drei Schritte:
> `worktree add`, den zugestellten Text als Datei in den Git-Verwaltungsordner des
> Worktrees schreiben, Tab starten — benennen — Zustellung pruefen). Aufloesung und
> Existenz-Pruefung der Quelle: `## Struktur-Check`.
>
> **Warum:** `hc` und `herdr-app` sind junge Werkzeuge, ihre Syntax driftet. `dtb:worker`
> deklariert seine zwei Pane-Sektionen ausdruecklich als die einzigen Orte dieser
> Kommandos; ein dritter Ort waere ein Spiegel, der bei der naechsten Aenderung
> zurueckbleibt. Korrigiert wird dort, nie hier.

**Vier bewusste Abweichungen** von der referenzierten Sequenz — alle gelten fuer diesen
Skill und sind beim Ausfuehren einzusetzen:

| Punkt | `dtb:worker` (Quelle) | Hier |
|-------|----------------------|------|
| Branch | `task/{slug}` | **`feature/{slug}`** — die Voll-Schiene arbeitet an einem Feature-Change, und der Branchname ist der Merge-Anker |
| Text in der Datei `dtb-auftrag.md` | Pane-Auftrag (autonome Arbeitsanweisung) | **Begruessungstext** (unten) — derselbe Dateiname, die Bloecke der Quelle pruefen ihn |
| Worktree-Pfad | `.dtb-worktrees/worker-{slug}` | **`.dtb-worktrees/pane-{slug}`** — interaktive Arbeitsplaetze bleiben in `git worktree list` von autonomen unterscheidbar |
| Startzeile (das eine Argument an `claude`) | `Lies die Datei … vollstaendig und fuehre den Auftrag darin aus.` | **`Lies die Datei $G/dtb-auftrag.md vollstaendig und befolge sie. Sie ist eine Begruessung, kein Arbeitsauftrag.`** — einzeilig und ohne Anfuehrungszeichen wie in der Quelle; „fuehre den Auftrag aus" widerspraeche der Wartepflicht |

Alles andere — Start aus dem eigenen Terminal mit dem Label des eigenen Fenster-Bereichs
(macht den Tab sichtbar und zum Kind des Orchestrators), Terminal-Name = Slug, Tab
umbenennen, Warte-Schleife, Auswertung von `START-OK`/`TAB-NAME-FEHLT`/`ZUSTAND`/`START-FEHLT`,
nie blind erneut senden — gilt unveraendert wie in der Quelle beschrieben. Nach der
Begruessung steht die Session auf `done` oder `idle`: das ist hier der erwartete Zustand
(sie wartet auf den Menschen), kein Befund.

**Nach dem Start** gibst du im eigenen Chat die Kopfzeile der Quelle aus (`🔭 gestartet: …`)
— mit dem tatsaechlich angelegten Branch (Regel `feature/{slug}`, abweichend, falls in 1c.2
anders entschieden) und der Adresse aus `START-OK`. Sie nennt den Weg zum Stand: der Mensch
fragt „Stand?", die Pruefung steht in `dtb:worker` → `#### Rueckweg: Stand-Pruefung`. Einen
wiederkehrenden Lauf gibt es nicht mehr (entfallen 2026-11-12 — Rueckfrage und Ende meldet
die App von selbst). Danach kehrst du zur eigenen Arbeit zurueck: KEIN
blockierendes Warten. Der Rueckweg laeuft wie beim Worker-Traeger (der Hand-off-Block
erreicht diese Session von selbst als Eingabe) — siehe `## Rueckweg und Abschluss`.

## Begruessungstext (Vorlage — die eine Quelle dieses Skills)

Der Text traegt ALLES, was die neue Session wissen muss, und reist als EINE Datei
(`dtb-auftrag.md` im Git-Verwaltungsordner des Worktrees — Start-Sequenz der Quelle); die
Session liest sie auf die eine Startzeile hin. Die Orchestrator-Adresse `{orchestrator}`
kommt zur Laufzeit aus `$HC_TERMINAL_ID` (Terminal-ID wie `t13`), `{handoff-datei}` ist
`{G}/dtb-handoff.md` im selben Git-Verwaltungsordner (Pfad `{G}` aus der Start-Sequenz). Es
gibt bewusst keine persistierte Adress-Registry (fluechtige Adressen — eine Datei waere eine
Zustandsaussage ohne Pfleger). Einzige benannte Abweichung: die Uebergabe-Notiz von
`dtb:workflow-checkpoint` haelt die Adresse je „Wechsel" als Momentaufnahme fest — kurzlebig
(lebt bis zum Abbau) und von `dtb:workflow-resume` vor jeder Anzeige geprueft, also
keine Registry.

```
Willkommen — du bist eine interaktive Arbeits-Session fuer den Change `{slug}`.
Hier arbeitet ein MENSCH mit dir; du bist kein autonomer Worker.

Arbeitsplatz: {worktree-pfad} (Branch feature/{slug})
Arbeite nur hier. Zentrale Workflow-Dateien gehoeren dir nicht: WORKFLOW_STATUS.md,
INBOX.md, BACKLOG.md, Changelog — die Teil-Guard-Skills ueberspringen ihre globalen
Schreibschritte hier planmaessig und melden das im Hand-off.
Orchestrator: Terminal {orchestrator} der Herdr-App.

Stand des Change: {1-2 Zeilen — welche Artefakte liegen vor, was ist der abgeleitete
naechste Schritt}
Vorgeschlagener Startbefehl: {Startbefehl aus Schritt 1b}

WARTEPFLICHT: Fuehre diesen Befehl NICHT selbst aus. Er ist ein Vorschlag an den
Menschen, der diesen Tab oeffnet — er entscheidet, ob und womit begonnen wird. Bis
dahin arbeitest du nicht, aenderst keine Dateien und stellst keine Rueckfragen an den
Orchestrator. Begruesse kurz und warte auf Eingabe.

Session-Wechsel (Kontext voll, Arbeit geht weiter): `/dtb:workflow-checkpoint` → „Wechsel"
waehlen → `/clear` → `/dtb:workflow-resume`. Die Uebergabe-Notiz traegt Rolle,
Orchestrator, Rueckweg und offene Punkte in die neue Session. Bevorzugt `/clear` statt
`/exit` + `claude` (ein `/exit` meldet die App dem Orchestrator als beendete Session).

Rueckweg (am Ende der Arbeit, nicht vorher): `/dtb:workflow-checkpoint` aufrufen und
„Ende" waehlen. Der Worktree-Guard dieses Skills bricht ab und erzeugt stattdessen den
WORKTREE-HANDOFF-Block. Diesen Block WOERTLICH und VOLLSTAENDIG (inklusive Kopfzeile
„WORKTREE-HANDOFF (dtb) — …") zuerst in die Datei {handoff-datei} schreiben und dann aus
dieser Datei an den Orchestrator schicken:
hc send {orchestrator} "$(cat '{handoff-datei}')"
Nichts paraphrasieren — die Kopfzeile ist der einzige Erkennungsanker der Empfangsseite.
Endet der Befehl mit Exit 9 (beim Orchestrator steht ein Dialog offen), 30 Sekunden warten
und wiederholen — hoechstens drei Wiederholungen, also vier Versuche insgesamt; NIE
--force. Kommt er dann nicht an, dem Menschen
sagen — die Datei bleibt liegen, der Orchestrator liest sie auf „Stand?".
Jeder andere Fehler (nicht Exit 9): NICHT wiederholen — aufhoeren und dem Menschen sagen;
die Datei bleibt liegen.
```

**Regeln zur Vorlage:**

- **Wartepflicht ist Pflichtbestandteil.** Sie ist der operative Unterschied zwischen
  Begruessung und Auftrag: ohne sie kann die Session den vorgeschlagenen Startbefehl selbst
  ausfuehren und der Mensch findet einen bereits laufenden Vorgang vor, den er nicht
  angestossen hat
- **Kein Governance-Teil.** Kein Versuchslimit, kein Zeitdeckel, keine Berichtspflicht,
  kein Tauglichkeitsurteil — es sitzt ein Mensch drin. Wer die Worker-Vorlage als Muster
  nimmt, laesst diese Zeilen ersatzlos weg
- **Rueckweg-Anweisung woertlich uebernehmen.** Das Blockformat selbst wird NICHT hier
  gepflegt: es steht in `dtb:workflow-checkpoint` → `### Hand-off-Block (Format — die eine
  Quelle)`. Die Session erhaelt den Block ueber den `/dtb:workflow-checkpoint`-Aufruf bei
  der Wahl „Ende" — die Sende-Seite seines Worktree-Guards erzeugt ihn; das Format liest sie
  nie separat, gepflegt wird es nur dort
- **Die Rueckweg-Kommandozeile der Vorlage ist ein DEKLARIERTER SPIEGEL** der
  Rueckweg-Zeile im Pane-Auftrag von `dtb:worker` (die einzige erlaubte Kommando-Zeile in
  diesem Skill — sie ist zugestellter Text, nicht Start-Sequenz). Drift an der
  Zustell-Syntax wird in `dtb:worker` korrigiert und HIER mitgezogen
- **Fortsetzungsfall:** Liegen im Change-Ordner schon Artefakte, nennt „Stand des Change"
  den abgeleiteten naechsten Schritt (Tabelle in Schritt 1b) statt eines Neustarts

## Rueckweg und Abschluss

- **Rueckweg:** Es laeuft kein blockierender Warteprozess und kein Takt. Rueckfrage,
  Session-Ende und geschlossenen Tab meldet die App dem Orchestrator von selbst (der Tab ist
  sein Kind-Terminal); den Stand liest der Orchestrator sonst auf Zuruf (der Mensch fragt
  „Stand?") — Pruefliste und Meldungsform: `dtb:worker` → `#### Rueckweg: Stand-Pruefung`
  (sie liest auch die Hand-off-Datei, falls das Senden abgewiesen wurde). Ein eingetroffener
  WORKTREE-HANDOFF-Block (Kopfzeile als Anker) wandert per `/dtb:workflow-checkpoint` in den
  Session-Log — die Empfangsseite dort bleibt unveraendert und traegerneutral.
- **Session-Wechsel im Tab:** Wird der Kontext voll, wechselt der Mensch die Session
  ueber `/dtb:workflow-checkpoint` → „Wechsel" → `/clear` → `/dtb:workflow-resume` (im
  Begruessungstext angekuendigt); die Uebergabe-Notiz im Git-Verwaltungsordner traegt den
  Startkontext, und erst „Ende" schickt EINEN kumulierten Block an den Orchestrator.
- **Abschluss (Merge, Diff-Abnahme, Abbau des Arbeitsplatzes):** gehoert NICHT in diesen
  Skill. Der Merge-Zeitpunkt einer Voll-Schienen-Arbeit ist beim Start unbekannt. Muster und
  Reihenfolge (Notiz-Pruefung → Merge → Klasse-A-Check → Checkpoint → Worktree/Branch entfernen): `dtb:worker`
  → `#### Abschluss (nach menschlicher Diff-Abnahme)`. Der Mensch fuehrt ihn aus, wenn die
  Arbeit abgenommen ist.
