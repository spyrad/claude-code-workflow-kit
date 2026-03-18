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
  after: dtb:idea
  next: dtb:feature-discover
  consumes: [INBOX.md]
  produces: [INBOX.md]
---

# Ideen-Inbox reviewen

Du fuehrst den Benutzer durch alle offenen Ideen in der Inbox. Fuer jede Idee wird eine Entscheidung getroffen.

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
  2. Ausarbeiten → startet /dtb:feature-discover mit dieser Idee
  3. Verwerfen
  4. Zusammenlegen mit anderer Idee (Nummer angeben)
```

### Aktionen ausfuehren:

**Behalten (1):** Keine Aenderung, weiter zur naechsten Idee.

**Ausarbeiten (2):**
- Setze Status auf `In Arbeit`
- Beende den Review
- Weise darauf hin: `/dtb:feature-discover` als naechsten Schritt ausfuehren
```
Idee #{N} auf "In Arbeit" gesetzt.
Naechster Schritt: /dtb:feature-discover
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
