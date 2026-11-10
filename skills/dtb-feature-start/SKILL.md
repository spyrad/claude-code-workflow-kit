---
name: dtb:feature-start
description: >-
  Use when: "Bug fixen", "Bug-Fix starten", "Aufgabe starten", "Task starten".
  Loads an analyzed bug or an open task and shows its context and entry point.
  Features are not started here: after plan-review, dtb:implement is the one
  entry into implementation. Status displays remain untouched.
disable-model-invocation: true
allowed-tools: Read, Glob
pipeline:
  stage: implementation
  after: [dtb:debug-plan]
  next: [dtb:implement]
  consumes: [features/*/bug.md, features/*/task.md, project-rules/DERIVED_STATE_RULES.md]
  produces: []
---

# Bug-Fix oder Aufgabe starten

Du startest einen analysierten Bug-Fix oder eine offene Aufgabe — beides ohne `plan.md`.

> **Features starten nicht hier** (seit 2026-11-10): Nach `dtb:plan-review` fuehrt
> `/dtb:implement {Feature-Name}` direkt in die Umsetzung — es zeigt ohne Argument selbst die
> Auswahl, laedt den Kontext aus `spec.md` und ruestet eine fehlende `## Progress`-Sektion nach.

## Aufgabe

### Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden:
```
workflow.config.yaml nicht gefunden.
Erstelle eine Config-Datei mit /dtb:project-init.
```

### Schritt 2: Bugs und Aufgaben lesen

1. **Scanne Bug-Reports:** `{config.paths.workflows}/features/*/bug.md`
2. **Filtere Bugs mit Status "Analysiert"** (haben einen Debug-Plan, sind bereit zum Fixen)
3. **Scanne Aufgaben:** `{config.paths.workflows}/features/*/task.md`
4. **Filtere Tasks mit Status "Offen"**

**Feature genannt** (Argument oder Kontext zeigt auf einen Change-Ordner mit `spec.md`/`plan.md`
statt `bug.md`/`task.md`) → keine Auswahl, genau eine Zeile und Ende:
```
→ Features startet /dtb:implement {Feature-Name} direkt
```

Falls weder analysierte Bugs noch offene Aufgaben vorhanden:
```
Nichts zu starten — keine analysierten Bugs oder offenen Aufgaben.
  Features: /dtb:implement
```

### Schritt 3: Auswahl

Zeige Bugs und Aufgaben als gemeinsame Auswahlliste:

```
# Bug-Fix / Aufgabe starten

Analysierte Bugs:
  1. Bug: {Bug-Name} ({Severity})
  2. Bug: {Bug-Name} ({Severity})

Offene Aufgaben:
  3. Aufgabe: {Aufgaben-Name} ({Prio})
  4. Aufgabe: {Aufgaben-Name} ({Prio})

Was moechtest du starten?
```

Falls nur eine Kategorie vorhanden: Zeige nur die relevante Sektion.

### Schritt 4: Artefakte lesen

Nach Auswahl durch den Benutzer werden die Artefakte des Items gelesen — **mehr nicht**.

> **Keine Anzeigefelder anfassen (Kanon §1.3):** Dieser Skill pflegt keine Statusanzeigen —
> weder im Backlog noch in der Uebersichtsdatei noch in `bug.md`/`task.md`. Der abgeleitete
> Status folgt der Ableitung aus vorhandenen Artefakten und der Checkliste (§1.1/§1.5) und
> wechselt mit dem ersten abgehakten Schritt.
> Ein Start, der eine Anzeige veraendert, behauptet einen Fortschritt, den es noch nicht gibt —
> und erzeugt genau den Feldkonflikt, den `dtb:workflow-resume` dann pflichtgemaess meldet.
>
> **Wer pflegt was:** Backlog, Uebersichtsdatei und die `**Status:**`-Zeile in
> `spec.md`/`task.md` pflegt `dtb:workflow-checkpoint` (§1.3 — dort „beim naechsten
> schreibenden Skill oder manuell"). Das Statusfeld in `bug.md` hat **derzeit keinen
> Pfleger**: der Checkpoint fuehrt es weder in `produces` noch in seinem Sync-Schritt. Es
> bleibt auf seinem Anlagewert stehen, bis INBOX #53 entschieden ist — nicht stillschweigend
> hier wieder aufnehmen.

**Bei Bug:**
1. **Lies den Bug-Report:** `{config.paths.workflows}/features/{slug}/bug.md` — Symptom,
   Analyse-Abschnitt und `## Fix-Schritte` als Kontext fuer Schritt 5

**Bei Aufgabe:**
1. **Lies die Aufgabe:** `{config.paths.workflows}/features/{slug}/task.md` — Beschreibung
   und `## Schritte` als Kontext fuer Schritt 5

### Schritt 5: Kontext zeigen

**Bei Bug:**
```
# Bug-Fix geladen: {Bug-Name}

**Status:** Analysiert (wechselt mit dem ersten abgehakten Fix-Schritt)
**Severity:** {Severity}

## Symptom

[Symptom aus `bug.md`]

## Root-Cause

[Wahrscheinlichste Hypothese aus Analyse-Abschnitt]

## Fix-Schritte

[Fix-Schritte aus Analyse-Abschnitt]

## Testplan

[Testplan aus Analyse-Abschnitt]

→ Weiter mit: Fix-Schritt {N} — {Kurzname des ersten offenen Fix-Schritts}
```

**Bei Aufgabe:**
```
# Aufgabe geladen: {Aufgaben-Name}

**Status:** Offen (wechselt mit dem ersten abgehakten Schritt)
**Prioritaet:** {Prio}

## Beschreibung

[Beschreibung aus `task.md`]

## Schritte

[Schritte-Checkliste aus `task.md`]

→ Weiter mit: Schritt {N} — {Kurzname des ersten offenen Schritts}
```

**Abschlusszeile statt Start-Rueckfrage:** Jeder Block endet mit genau EINER Zeile `→ Weiter mit: …`
— keine Rueckfrage (sie trug keine Festlegung, nur den Uebergang). Der Skill **startet nichts
selbst**: keine Code-Aenderung vor der naechsten Nutzer-Eingabe. Gestartet wird nur durch einen
Befehl oder „weiter"; eine **Frage** wird beantwortet, ohne zu starten (danach gilt die
`→ Weiter mit: …`-Zeile unveraendert).
(Form-Kanon fuer Autoren: `skills/CLAUDE.md` → „Rueckfragen-Defaults (Veto-Form)", Zeile E.)

---

## Wichtig

- **Nur startbare Items:** Bugs mit Status "Analysiert" und Aufgaben mit Status "Offen" — keine "In Arbeit" oder "Abgeschlossen". Features gehen direkt in `/dtb:implement`
- **Kein Status-Update, kein Schreiben:** Dieser Skill schreibt nichts — keine Anzeigefelder in BACKLOG.md, WORKFLOW_STATUS.md oder `bug.md`/`task.md`. Wer sie stattdessen pflegt (und wo derzeit niemand zustaendig ist): siehe den Kasten in Schritt 4. Der abgeleitete Status folgt dem Fortschritt, nicht dem Start
- **Checkbox-Pflicht:** `## Fix-Schritte` bzw. `## Schritte` werden waehrend der Arbeit einzeln abgehakt, nicht gesammelt am Session-Ende — die Checkliste ist die Single Source of Truth (`project-rules/DERIVED_STATE_RULES.md` §1.5)
- **Kompakt:** Max 40 Zeilen Output
- **Deutsch:** Alle Texte auf Deutsch
