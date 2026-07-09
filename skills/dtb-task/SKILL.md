---
name: dtb:task
description: >-
  Use when: "Aufgabe erfassen", "task anlegen", "Housekeeping",
  "Wartungsaufgabe", "operativ", "Aufgabe erstellen", "task".
  Captures a lightweight operational/infrastructure task as
  features/<slug>/task.md in the features directory.
disable-model-invocation: true
argument-hint: "[Aufgaben-Beschreibung als Freitext]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: idea
  after: null
  next: null
  consumes: [BACKLOG.md]
  produces: [features/*/task.md, BACKLOG.md]
---

# Aufgabe erfassen

Du erfasst eine operative oder infrastrukturelle Aufgabe schnell und strukturiert. Aufgaben sind leichtgewichtiger als Features — kein Spec/Plan-Zyklus, sondern direkte Checkliste.

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
- **Konkret:** Checkliste mit konkreten Schritten, keine vagen Beschreibungen
- **Leichtgewichtig:** Kein Plan oder Spec noetig — Aufgaben sind direkte Action-Items
- **Deutsch:** Alle Texte auf Deutsch
