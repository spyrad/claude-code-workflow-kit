---
name: dtb:session-summary
description: >-
  Use when the user wants a recap or summary of work already done —
  e.g. "fass die session zusammen", "was haben wir (heute / diese
  session) gemacht/erreicht/geschafft", "gib mir einen recap / kurzen
  ueberblick", "zusammenfassung vom 2026-06-12", "was hab ich am
  <Datum> gemacht", "wochenrueckblick", "was lief diese woche",
  "uebersicht der arbeit der letzten 7 tage", "session summary".
  Read-only skill: produces a compact, structured summary (Erledigt /
  Entscheidungen / Offen). Without an argument it summarizes the ACTIVE
  conversation; with a YYYY-MM-DD argument it reads and summarizes that
  day's changelog under dtb-project/project-changelog/; with
  "woche"/"week" it summarizes the last 7 days. Trigger this
  proactively for any retrospective recap of accomplished work, even if
  no mode is named. Do NOT use for: writing or saving a changelog entry
  (that is /dtb:workflow-checkpoint), planning what comes next or
  resuming work (/dtb:workflow-next, /dtb:workflow-resume), or
  summarizing arbitrary content like a PDF, a git diff, git log, or an
  application log file — this skill only recaps development sessions,
  not documents.
disable-model-invocation: false
argument-hint: "[YYYY-MM-DD | woche]"
allowed-tools: Read, Glob, Grep
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [session-log]
  produces: []
---

# DTB Session-Summary

Liefert eine **kompakte, strukturierte Zusammenfassung** der geleisteten Arbeit.
Read-Only — schreibt keine Dateien, gibt nur in den Chat aus.

Der Skill hat drei Modi, gesteuert ueber das (optionale) Argument:

| Argument | Modus | Quelle |
|----------|-------|--------|
| _(leer)_ | **Aktive Session** | Der aktuelle Gespraechsverlauf |
| `YYYY-MM-DD` (z.B. `2026-06-12`) | **Bestimmter Tag** | Changelog-Datei dieses Tages |
| `woche` / `week` | **Vergangene Woche** | Changelog-Dateien der letzten 7 Tage |

> **Abgrenzung zu `dtb:no-loss-check`:** Beide lesen den Gespraechsverlauf, beantworten aber
> verschiedene Fragen. Dieser Skill fasst zusammen, **was war** (rueckblickend, vollstaendig,
> unabhaengig davon ob es erfasst wurde). `dtb:no-loss-check` meldet, **was droht verloren zu
> gehen** — also nur den Teil, der in keinem Artefakt gelandet ist, jeweils mit fertigem
> Erfassungs-Befehl. Wer wissen will, was die Sitzung gebracht hat: hier. Wer vor dem Checkpoint
> sicherstellen will, dass nichts liegen bleibt: dort. Bewusst **keine** Pipeline-Kante zwischen
> beiden — sie stehen nebeneinander, nicht hintereinander.

## Schritt 1: Modus bestimmen

Wirf einen Blick auf das uebergebene Argument und entscheide:

- **Kein Argument** → Modus A (Aktive Session).
- **Argument passt auf `^\d{4}-\d{2}-\d{2}$`** (z.B. `2026-06-12`) → Modus B (Bestimmter Tag).
- **Argument ist `woche`, `week`, `letzte woche`, `wochenrueckblick` o.ae.** → Modus C (Vergangene Woche).

Bei einem unklaren Argument (z.B. ein unvollstaendiges Datum) kurz nachfragen statt zu raten.

## Schritt 2 (nur Modus B & C): Config laden

Lies `workflow.config.yaml` im Projekt-Root und verwende `{config.paths.changelog}`
als Changelog-Wurzel.

Falls die Config fehlt: Fallback-Pfad `dtb-project/project-changelog/`.

> Modus A braucht keine Config — es wird der Gespraechsverlauf analysiert, keine Datei.

---

## Modus A — Aktive Session

Analysiere **diesen Gespraechsverlauf** (vom Session-Start bis jetzt) und destilliere,
was tatsaechlich passiert ist. Es geht um die geleistete Arbeit, nicht um eine
Wiedergabe jeder Nachricht.

Achte beim Durchgehen auf:
- **Was wurde umgesetzt/geaendert** — welche Dateien, welche konkreten Aenderungen
- **Welche Entscheidungen wurden getroffen** — und kurz das Warum, falls relevant
- **Was wurde committet/ausgefuehrt** — Commits, Pushes, Builds, Tests
- **Was ist noch offen** — angesprochene, aber nicht erledigte Punkte

Wenn die Session bisher kaum Substanz hat (reines Lesen, keine Aenderung/Entscheidung),
sag das ehrlich in einem Satz, statt eine Zusammenfassung zu erfinden.

Gib dann das **Output-Format** (siehe unten) aus, mit der Kopfzeile
`# Session-Zusammenfassung — Aktive Session`.

---

## Modus B — Bestimmter Tag

1. Leite aus dem Datum `YYYY-MM-DD` den Monats-Ordner `YYYY-MM` ab.
2. Lies die Datei `{config.paths.changelog}/{YYYY-MM}/{YYYY-MM-DD}.md`.

**Falls die Datei nicht existiert:**
```
Kein Changelog fuer {YYYY-MM-DD} gefunden ({config.paths.changelog}/{YYYY-MM}/{YYYY-MM-DD}.md).
Pruefe das Datum oder dokumentiere Sessions kuenftig mit /dtb:workflow-checkpoint.
```

**Falls die Datei existiert:** Eine Tages-Datei kann **mehrere Sessions** enthalten
(getrennt durch `---` und `## Session N - HH:MM`). Fasse alle Sessions des Tages
zusammen — nicht jede einzeln nacherzaehlen, sondern das Gesamtergebnis des Tages.

Gib das **Output-Format** mit der Kopfzeile
`# Session-Zusammenfassung — {YYYY-MM-DD}` aus.

---

## Modus C — Vergangene Woche (letzte 7 Tage)

"Vergangene Woche" = **rollierende letzten 7 Tage**, von heute rueckwaerts
(inklusive heute). Beispiel: ist heute `2026-06-16`, ist das Fenster
`2026-06-10` bis `2026-06-16`.

1. Bestimme das heutige Datum (aus dem Environment) und berechne das Fenster
   `[heute−6 Tage, heute]`.
2. Das Fenster kann **zwei Monats-Ordner** umspannen (z.B. Ende Mai + Anfang Juni).
   Glob die relevanten Ordner: `{config.paths.changelog}/{YYYY-MM}/*.md`.
3. Behalte nur Dateien, deren Datum (aus dem Dateinamen `YYYY-MM-DD.md`) **im
   Fenster** liegt. Lies diese Dateien.

**Falls keine Datei im Fenster liegt:**
```
Keine Changelog-Eintraege in den letzten 7 Tagen ({Startdatum} bis {heute}).
```

**Falls Dateien vorhanden:** Aggregiere ueber alle Tage hinweg zu **einem**
Gesamtbild der Woche — nicht Tag fuer Tag nacherzaehlen. Wenn ein roter Faden
oder Schwerpunkt erkennbar ist (z.B. "Hauptarbeit lag auf X"), benenne ihn.

Gib das **Output-Format** mit der Kopfzeile
`# Wochenrueckblick — {Startdatum} bis {heute}` aus und ergaenze direkt darunter
eine Zeile mit den abgedeckten Tagen, z.B.:
`**Abgedeckte Tage:** 2026-06-12, 2026-06-14, 2026-06-16`

---

## Output-Format (alle Modi)

Halte dich an diese Struktur. Lass einen Abschnitt **weg**, wenn er leer waere —
ein "## Entscheidungen"-Block mit dem Inhalt "keine" ist Laerm, kein Signal.

```markdown
# {Kopfzeile je nach Modus}

## Erledigt
- [Konkrete Aenderung/Umsetzung — Datei- oder Komponentennamen nennen, nicht "Code verbessert"]
- ...

## Entscheidungen
- [Getroffene Entscheidung + kurz das Warum, falls nicht offensichtlich]

## Offen / Naechste Schritte
- [Angesprochener, aber nicht erledigter Punkt]
```

### Richtwerte fuer Laenge

- **Aktive Session / Tag:** ca. 5–10 Bullets gesamt.
- **Woche:** ca. 8–15 Bullets gesamt — verdichtet, nicht eine Liste pro Tag.

Lieber wenige praezise Punkte als eine vollstaendige Aufzaehlung. Wenn etwas
unwichtig war, gehoert es nicht rein.

## Richtlinien

- **Read-Only:** Dieser Skill aendert keine Dateien.
- **Kompakt & konkret:** Datei-/Funktions-/Feature-Namen statt vager Floskeln.
- **Ehrlich:** Nichts erfinden. Wenig Substanz → das so benennen.
- **Keine unnoetigen Rueckfragen:** Bei klarem Argument sofort liefern; nur bei
  echter Mehrdeutigkeit nachfragen.
- **Deutsch:** Alle Texte auf Deutsch.

## Verwandte Skills

- `/dtb:workflow-checkpoint` — Session **dokumentieren** (schreibt den Changelog, den dieser Skill liest)
- `/dtb:workflow-resume` — Session **fortsetzen** mit vollem Kontext
- `/dtb:backlog-status` — Ueberblick offener Features

---

Bestimme jetzt den Modus und erstelle die Zusammenfassung.
