---
name: dtb:idea
description: >-
  Use when: "Idee notieren", "idea", "Gedanke festhalten", "Einfall",
  "kurz notieren", "Idee speichern". Captures a quick idea or thought
  into the project inbox without interrupting the current workflow.
disable-model-invocation: true
argument-hint: "[Idee als Freitext]"
---

# Idee schnell erfassen

Du erfasst eine Idee oder einen Gedanken in der Projekt-Inbox. Keine Rueckfragen, keine Ausarbeitung — nur speichern.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Idee erfassen

**Input:** Der Freitext nach dem Command-Aufruf ist die Idee.

Falls kein Freitext angegeben wurde:
```
Welche Idee moechtest du festhalten? (Freitext)
```

---

## Schritt 2: In INBOX.md speichern

### Datei
- Pfad: `{config.paths.workflows}/INBOX.md`
- Falls Datei nicht existiert: Erstelle sie mit Header

### Format bei neuer Datei

```markdown
# Ideen-Inbox

> Schnell erfasste Ideen und Gedanken. Ausarbeitung mit `/dtb:feature-plan`.

---

| # | Datum | Idee | Status |
|---|-------|------|--------|
| 1 | YYYY-MM-DD | [Idee-Text] | Offen |
```

### Format bei bestehender Datei

- Fuege eine neue Zeile in die Tabelle ein
- Naechste laufende Nummer vergeben
- Status: `Offen`
- Datum: Aktuelles Datum

### Status-Werte
- **Offen** — Noch nicht bearbeitet
- **In Arbeit** — Wird gerade mit `/dtb:feature-plan` ausgearbeitet
- **Ausgearbeitet** — Feature-Plan erstellt → `FEATURE_*.md`
- **Verworfen** — Bewusst nicht weiterverfolgt

---

## Schritt 3: Bestaetigung

```
Idee #{N} gespeichert: {config.paths.workflows}/INBOX.md

  "{Idee-Text}"

Ausarbeiten: /dtb:feature-plan
```

**Keine weiteren Rueckfragen.** Zurueck zur aktuellen Arbeit.
