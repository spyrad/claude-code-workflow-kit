---
name: dtb:idea-review
description: >-
  Use when: "Ideen reviewen", "idea review", "Inbox aufraumen",
  "Ideen sichten", "Inbox pruefen". Reviews all open ideas in the
  inbox and lets the user decide on each: keep, elaborate, or discard.
disable-model-invocation: true
allowed-tools: Read, Write
pipeline:
  stage: idea
  after: [dtb:idea]
  next: [dtb:feature-discover, dtb:feature-fast, dtb:task]
  consumes: [INBOX.md]
  produces: [INBOX.md]
---

# Ideen-Inbox reviewen

Du fuehrst den Benutzer durch alle offenen Ideen in der Inbox. Fuer jede Idee wird eine Entscheidung getroffen.

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
  ⛔ dtb:idea-review schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: globale Dateien haben genau einen Schreiber —
     die Session im Haupt-Checkout).
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Inbox laden

Lies `{config.paths.workflows}/INBOX.md`.

Falls nicht vorhanden oder leer:
```
Keine Inbox vorhanden. Ideen erfassen mit /dtb:idea
```

Filtere alle Eintraege mit Status `Offen`.

Falls keine offenen Eintraege:
```
Keine offenen Ideen in der Inbox. Alles aufgeraeumt.
```

---

## Lesestand-Pruefung (Lese-Seite)

Parallele Sessions koennen gelesene Dateien zwischen Einlesen und Entscheidung
veraendern (Orchestrator-Muster: `skills/CLAUDE.md` → „Parallele Sessions" — dieser
Skill ist lesend-entscheidend; Beleg: fremder INBOX-Nachtrag waehrend eines laufenden
Reviews, 2026-08-11).

1. **Beim Einlesen merken:** mtime der gelesenen `INBOX.md` festhalten — in EINEM
   selbstaendigen Bash-Block:
   ```bash
   ls -la --time-style=full-iso {pfad}/INBOX.md
   ```
2. **Unmittelbar vor JEDER Statusentscheidung** (jedem Schreiben einer Status-Aenderung
   in Schritt 3) dieselbe Abfrage erneut ausfuehren und vergleichen:
   - mtime unveraendert → still weiterarbeiten (kein Output)
   - mtime veraendert → Datei NEU lesen und den Inhalt vergleichen:
     - Inhalt tatsaechlich abweichend → genau eine Zeile
       `⚠ INBOX.md wurde seit dem Einlesen geaendert ({neue mtime}) — Stand neu geladen`
       und mit dem FRISCHEN Stand weiterarbeiten (kein Abbruch, keine Nachfrage)
     - Inhalt identisch (nur mtime, z.B. touch/Checkout) → keine Warnung
   - Datei existiert nicht mehr → wie Abweichung behandeln:
     `⚠ INBOX.md seit dem Einlesen entfernt/verschoben — Entscheidung ggf. hinfaellig`
3. **Bewusste Restluecke:** Das Fenster zwischen Pruefung und eigenem Schreiben bleibt
   (kein Locking) — Konvention: `skills/CLAUDE.md` → „Parallele Sessions".

## Schritt 2: Uebersicht zeigen

```
Ideen-Review: {Anzahl} offene Ideen

| # | Datum | Idee |
|---|-------|------|
| {N} | {Datum} | {Text} |
| ... | ... | ... |

Gehe ich einzeln durch? (Ja / Nummern zum Ueberspringen / Alle verwerfen)
```

---

## Schritt 3: Einzeln durchgehen

Fuer jede offene Idee zeige:

```
Idee #{N} ({Datum}):
  "{Idee-Text}"

Aktion?
  1. Behalten (bleibt Offen)
  2. Ausarbeiten → Groesseneinschaetzung, dann Task / Fast-Track / Voll-Schiene
  3. Verwerfen
  4. Zusammenlegen mit anderer Idee (Nummer angeben)
```

### Aktionen ausfuehren:

**Behalten (1):** Keine Aenderung, weiter zur naechsten Idee.

**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**

Schaetze die Idee in einem Satz mit Begruendung ein und schlage die passende Schiene vor —
immer Vorschlag + Bestaetigung, nie automatisch:

| Einstufung | Heuristik | Schiene |
|------------|-----------|---------|
| Operative Aufgabe | kein Spec-wuerdiges Feature: Wartung, Config, einmalige Handgriffe | `/dtb:task` |
| Kleines Feature | wenige Module, absehbar max. 2 Plan-Phasen, keine neuen Konzepte | `/dtb:feature-fast` |
| Sonst | alles andere — bei Unsicherheit ist die Voll-Schiene der sichere Default | `/dtb:feature-discover` |

```
Einschaetzung: {1 Satz mit Begruendung}
Vorschlag: {Task | Fast-Track | Voll-Schiene} ({Skill-Befehl})
Uebernehmen? (Ja / lieber {Alternative 1} / lieber {Alternative 2})
```

Nach der Bestaetigung:
- **Task-Lane:** Setze Status direkt auf `Ausgearbeitet` mit Vermerk
  `→ als Aufgabe geroutet ({Datum}); task.md-Link ergaenzt /dtb:task` — KEIN `In Arbeit`.
  Grund: dtb:task schliesst die Erfassung einschrittig ab; ein dauerhaftes "In Arbeit"
  wuerde von argumentlosen feature-fast-/feature-discover-Laeufen automatisch geladen
  (impl-review F2, 2026-08-02)
- **Fast-Track- oder Voll-Schiene:** Setze Status auf `In Arbeit`
- Beende den Review
- Weise auf den gewaehlten Skill als naechsten Schritt hin
```
Idee #{N} auf "{Ausgearbeitet | In Arbeit}" gesetzt.
Naechster Schritt: {/dtb:task | /dtb:feature-fast | /dtb:feature-discover}
```

**Verwerfen (3):**
- Setze Status auf `Verworfen`
- Weiter zur naechsten Idee

**Zusammenlegen (4):**
- Frage nach der Zielnummer
- Ergaenze den Text der Ziel-Idee um den Text der aktuellen Idee
- Setze die aktuelle Idee auf `Verworfen` mit Hinweis `→ zusammengelegt mit #{Ziel}`
- Weiter zur naechsten Idee

---

## Schritt 4: Zusammenfassung

```
Ideen-Review abgeschlossen:

  Behalten:       {N}
  In Arbeit:      {N}
  Verworfen:      {N}
  Zusammengelegt: {N}

Offene Ideen gesamt: {N}
```
