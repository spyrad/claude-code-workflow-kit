---
name: dtb:pane-start
description: >-
  Use when: "pane start", "Session in eigener Pane starten", "Voll-Schiene
  im Worktree starten", "interaktive Session aufsetzen", "Arbeitsplatz fuer
  Change einrichten". Sets up an interactive full-lane session for one change:
  own worktree, own Herdr pane, a started and detected Claude session, and ONE
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
  consumes: [INBOX.md, workflow.config.yaml, features/*/plan.md, features/*/spec.md]
  produces: []
---

# Interaktive Session in Pane + Worktree starten

Du richtest fuer EINEN Change einen eigenen Arbeitsplatz ein — Worktree, Pane, laufende
Session — und stellst dieser Session EINEN Begruessungstext zu. Danach kehrst du zur
eigenen Arbeit zurueck; in der Pane arbeitet ein **Mensch**.

**Abgrenzung zu `dtb:worker` (Traeger `pane`):** Dieselbe Herdr-Mechanik, anderer Zweck.
`dtb:worker` stellt einen **autonomen Auftrag** auf Basis einer `task.md` zu und unterliegt
der Autonomie-Regel (Versuchslimit, Zeitdeckel, Tauglichkeitsraster, Bericht). Dieser Skill
stellt einen **Begruessungstext** zu und hat davon nichts — es sitzt jemand drin. Was beide
teilen, sind die vier Start-Kommandos; sie leben ausschliesslich in `dtb:worker` und werden
hier NUR referenziert, niemals kopiert (Drift-Schutz — Details: `## Herdr-Mechanik`).

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

**Eligibility-Gate:** `HERDR_ENV` = `1` UND `herdr` im PATH (`command -v herdr`) UND
`$HERDR_PANE_ID` nicht leer (ohne eigene Pane-Adresse gibt es keinen Rueckkanal — der
Begruessungstext braucht die Orchestrator-Adresse; eine Herdr-CLI ausserhalb einer Pane
genuegt nicht). Sonst Abbruch — KEINE stille Degradierung auf einen anderen Weg:

```
⛔ dtb:pane-start braucht Herdr (HERDR_ENV=1 + herdr-CLI + eigene Pane-Adresse
   $HERDR_PANE_ID), hier nicht verfuegbar.
   Alternativen: die Voll-Schiene direkt in dieser Session fahren
   (/dtb:feature-discover {Argument} bzw. /dtb:feature-fast {Argument}) oder den
   Arbeitsplatz manuell einrichten (git worktree add + Session von Hand starten).
   Dein Ziel geht nicht verloren — in einer Herdr-Session absetzen:
   /dtb:pane-start {Argument}
```

Wurde kein Argument uebergeben, entfallen die `{Argument}`-Anteile der Meldung ersatzlos.

Der Skill hat bewusst **keinen** Ersatzpfad: sein ganzer Zweck ist der Pane-Hinweg. Ohne
Pane gibt es nichts zu verkuerzen, und ein halb eingerichteter Arbeitsplatz waere schlechter
als keiner.

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

**Abbruch bei unauflösbarem Argument** — die `Geprueft:`-Zeilen nennen NUR die
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
| `plan.md` vorhanden, `## Progress` teilweise/leer | `/dtb:implement {slug}` |
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
4. **Fremde Session im Haupt-Checkout?** `herdr agent list` lesen und Eintraege mit
   Arbeitsverzeichnis = Haupt-Checkout (ausser der eigenen Pane `$HERDR_PANE_ID`) suchen.
   Fund → genau EINE Warnzeile, dann weiterarbeiten (melden statt blockieren; die
   Verzeichnis-Angabe ist der Pane-Start-Stand und stale-anfaellig):
   ```
   ⚠ Weitere Session im Haupt-Checkout gefunden ({pane-id}) — der Worktree-Guard
     deckt diesen Fall nicht (bekannte Grenze: er erkennt nur verlinkte Worktrees).
   ```

## Struktur-Check (Kopplungs-Waechter)

Dieser Skill traegt die Start-Sequenz nicht selbst — er MUSS deshalb **vor jeder
Einrichtung** (nach der Argument-Aufloesung und den Vorbedingungen aus Schritt 1, vor dem
ersten Kommando der Herdr-Mechanik) pruefen, dass seine Quelle existiert und ihre
Anker-Sektionen noch traegt. Endet ein Lauf schon in Guard, Gate oder Schritt 1, laeuft der
Check planmaessig nie. Ohne ihn gaebe es weder Fallback noch Diagnose: die Quelle koennte
fehlen oder umgebaut sein, und der Ausfall bliebe stumm bis mitten in die Einrichtung.

**Aufloesung der Quelle** (Muster: `dtb:feature-fast` Schritt 2): zuerst die installierte
Kopie `~/.claude/skills/dtb-worker/SKILL.md`, sonst Fallback auf `skills/dtb-worker/SKILL.md`
im Projekt-Root (Kit-Repo-Fall).

**Anker-Grep** (zeilenende-normalisiert — `tr -d '\r'` vorschalten, nie `$`-Anker gegen den
Rohtext) auf beide Sektionen:

| Anker (Grep, woertlich) | Traegt |
|-------------------------|--------|
| `### Pane-Ausfuehrung` | Vorbedingungen, Start-Sequenz, Rueckweg, Abschluss |
| `### Pane-Auftrag` | Vorlagen-Muster fuer den zugestellten Text |

**Beide Anker gefunden** → eine Statuszeile und weiter:
`🧩 Struktur-Check: 2/2 Anker in {aufgeloeste Quelle} gefunden`

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
> inhaltliche Drift verteidigen die Kopplungs-Hinweise in den beiden Sektionen von
> `dtb:worker` — bei Aenderungen dort muss dieser Skill mitgezogen werden.

## Herdr-Mechanik (referenziert, nicht dupliziert)

> **Die Start-Sequenz steht NICHT hier.** Quelle ist `dtb:worker` →
> `### Pane-Ausfuehrung`, Unterabschnitt „Hinweg: Start-Sequenz" (vier
> Kommandos: `worktree add`, Pane teilen, Session ueber die Pane-Shell starten inkl.
> Erkennungs-Warten, Auftrag als EINE Nachricht zustellen). Aufloesung und
> Existenz-Pruefung der Quelle: `## Struktur-Check`.
>
> **Warum:** Herdr-CLI-Drift ist ein bekanntes, dokumentiertes Risiko. `dtb:worker`
> deklariert seine zwei Pane-Sektionen ausdruecklich als die einzigen Orte dieser
> Kommandos; ein dritter Ort waere ein Spiegel, der bei der naechsten CLI-Aenderung
> zurueckbleibt. Korrigiert wird dort, nie hier.

**Zwei bewusste Abweichungen** von der referenzierten Sequenz — beide gelten fuer diesen
Skill und sind beim Ausfuehren einzusetzen:

| Punkt | `dtb:worker` (Quelle) | Hier |
|-------|----------------------|------|
| Branch | `task/{slug}` | **`feature/{slug}`** — die Voll-Schiene arbeitet an einem Feature-Change, und der Branchname ist der Merge-Anker |
| Zugestellter Text | Pane-Auftrag (autonome Arbeitsanweisung) | **Begruessungstext** (unten) |

Alles andere — Pfad-Schema des Worktrees, Pane-Teilung ohne Fokuswechsel, Startweg ueber die
Pane-Shell statt ueber den Agent-Start, Erkennungs-Warten mit einem Wiederholungsversuch,
Zustellung als EINE Nachricht — gilt unveraendert wie in der Quelle beschrieben.

**Nach der Zustellung** kehrst du zur eigenen Arbeit zurueck: KEIN blockierendes Warten. Der
Rueckweg laeuft wie beim Worker-Traeger (der Hand-off-Block erreicht diese Session von
selbst als Eingabe) — siehe `## Rueckweg und Abschluss`.

## Begruessungstext (Vorlage — die eine Quelle dieses Skills)

Der Text traegt ALLES, was die neue Session wissen muss, und wird als EINE Nachricht
zugestellt. Die Orchestrator-Adresse kommt zur Laufzeit aus `$HERDR_PANE_ID`; es gibt
bewusst keine persistierte Pane-Registry (fluechtige Adressen — eine Datei waere eine
Zustandsaussage ohne Pfleger).

```
Willkommen — du bist eine interaktive Arbeits-Session fuer den Change `{slug}`.
Hier arbeitet ein MENSCH mit dir; du bist kein autonomer Worker.

Arbeitsplatz: {worktree-pfad} (Branch feature/{slug})
Arbeite nur hier. Zentrale Workflow-Dateien gehoeren dir nicht: WORKFLOW_STATUS.md,
INBOX.md, BACKLOG.md, Changelog — die Teil-Guard-Skills ueberspringen ihre globalen
Schreibschritte hier planmaessig und melden das im Hand-off.
Orchestrator: Herdr-Pane {orchestrator-pane}.

Stand des Change: {1-2 Zeilen — welche Artefakte liegen vor, was ist der abgeleitete
naechste Schritt}
Vorgeschlagener Startbefehl: {Startbefehl aus Schritt 1b}

WARTEPFLICHT: Fuehre diesen Befehl NICHT selbst aus. Er ist ein Vorschlag an den
Menschen, der diese Pane oeffnet — er entscheidet, ob und womit begonnen wird. Bis
dahin arbeitest du nicht, aenderst keine Dateien und stellst keine Rueckfragen an den
Orchestrator. Begruesse kurz und warte auf Eingabe.

Rueckweg (am Ende der Session, nicht vorher): `/dtb:workflow-checkpoint` aufrufen. Der
Worktree-Guard dieses Skills bricht ab und erzeugt stattdessen den WORKTREE-HANDOFF-Block.
Diesen Block WOERTLICH und VOLLSTAENDIG (inklusive Kopfzeile „WORKTREE-HANDOFF (dtb) — …")
an den Orchestrator zurueckschicken:
herdr agent prompt {orchestrator-pane} "<der komplette Block>"
Nichts paraphrasieren — die Kopfzeile ist der einzige Erkennungsanker der Empfangsseite.
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
  Quelle)`. Die Session liest es dort, wenn sie den Block baut — sie ruft den Skill nicht auf,
  um das Format zu lesen
- **Fortsetzungsfall:** Liegen im Change-Ordner schon Artefakte, nennt „Stand des Change"
  den abgeleiteten naechsten Schritt (Tabelle in Schritt 1b) statt eines Neustarts

## Rueckweg und Abschluss

- **Rueckweg:** Es laeuft kein blockierender Warteprozess. Anlassbezogen (der Mensch fragt
  nach dem Stand) kann der Orchestrator den Pane-Zustand lesen; ein eingetroffener
  WORKTREE-HANDOFF-Block (Kopfzeile als Anker) wandert per `/dtb:workflow-checkpoint` in den
  Session-Log — die Empfangsseite dort bleibt unveraendert und traegerneutral.
- **Abschluss (Merge, Diff-Abnahme, Abbau des Arbeitsplatzes):** gehoert NICHT in diesen
  Skill. Der Merge-Zeitpunkt einer Voll-Schienen-Arbeit ist beim Start unbekannt. Muster und
  Reihenfolge (Merge → Klasse-A-Check → Checkpoint → Worktree/Branch entfernen): `dtb:worker`
  → `#### Abschluss (nach menschlicher Diff-Abnahme)`. Der Mensch fuehrt ihn aus, wenn die
  Arbeit abgenommen ist.
