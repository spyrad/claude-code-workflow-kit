---
name: dtb:debug-plan
description: >-
  Use when: "Bug analysieren", "debug plan", "Root Cause", "Fehler untersuchen",
  "warum passiert das", "Bug fixen planen". Creates a structured debug plan
  with root-cause hypotheses and fix strategy based on an existing BUG_*.md.
disable-model-invocation: true
argument-hint: "[Bug-Name]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: dtb:bug-report
  next: dtb:feature-start
  consumes: [BUG_*.md, project-rules/lessons.md]
  produces: [BUG_*.md]
---

# Debug-Plan erstellen

Du bist ein Debug-Analyst. Deine Aufgabe ist es, basierend auf einem bestehenden Bug-Report eine strukturierte Root-Cause-Analyse und Fix-Strategie zu erstellen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (nur Header) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `debug-plan` oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen bei Hypothesen und Fix-Strategie still an
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei passende Lektionen mit ueberlappendem `Applies-to` und gegensaetzlicher `Rule`):
  beide zeigen und den Widerspruch melden — nicht selbst aufloesen

---

## Schritt 1: Bug-Report laden

### Bug-Name ermitteln
- Aus dem Argument oder Frage den Benutzer
- Konvertiere zu UPPER_SNAKE_CASE (z.B. "Login broken" → `BUG_LOGIN_BROKEN.md`)

### Bug-Report lesen
- Lies `{config.paths.workflows}/features/BUG_[NAME].md`
- Falls Datei nicht gefunden:
  ```
  Bug-Report nicht gefunden: BUG_[NAME].md
  Erstelle zuerst einen Bug-Report mit /dtb:bug-report.
  ```

---

## Schritt 2: Codebase untersuchen

Basierend auf dem Bug-Report:

1. **Betroffene Dateien finden:** Nutze Grep/Glob um die im Bug genannte Komponente zu lokalisieren
2. **Relevanten Code lesen:** Lies die betroffenen Dateien/Funktionen
3. **Zusammenhaenge erkennen:** Suche nach verwandten Modulen, Imports, Aufrufen

---

## Schritt 3: Root-Cause-Hypothesen aufstellen

Formuliere 2-3 Hypothesen, sortiert nach Wahrscheinlichkeit:

Fuer jede Hypothese:
- **Was:** Was genau koennte den Bug verursachen?
- **Wo:** Welche Datei(en) und Zeile(n)?
- **Warum:** Warum fuehrt das zum beobachteten Symptom?
- **Pruefung:** Wie kann man diese Hypothese verifizieren?

---

## Schritt 4: Fix-Strategie entwickeln

Basierend auf der wahrscheinlichsten Hypothese:

1. **Fix-Schritte:** Konkrete Aenderungen mit Dateibezug
2. **Testplan:** Wie verifizieren wir dass der Fix funktioniert?
3. **Regressionsrisiko:** Was koennte durch den Fix kaputt gehen?

---

## Schritt 5: Bug-Report aktualisieren

Ergaenze die bestehende `BUG_[NAME].md` um einen Analyse-Abschnitt:

```markdown

---

## Analyse

**Analysiert:** [YYYY-MM-DD]
**Status:** Offen → Analysiert

### Root-Cause-Hypothesen

#### Hypothese 1 (wahrscheinlichste)
- **Ursache:** [Was verursacht den Bug?]
- **Datei:** `[Pfad:Zeile]`
- **Begruendung:** [Warum fuehrt das zum Symptom?]
- **Pruefung:** [Wie verifizieren?]

#### Hypothese 2
- **Ursache:** [Alternative Erklaerung]
- **Datei:** `[Pfad:Zeile]`
- **Begruendung:** [Warum?]
- **Pruefung:** [Wie verifizieren?]

### Fix-Strategie

#### Schritte
1. [Konkrete Aenderung in Datei X]
2. [Konkrete Aenderung in Datei Y]

#### Testplan
- [ ] [Test 1: Reproduktionsschritte nochmal durchfuehren]
- [ ] [Test 2: Regression pruefen fuer ...]

#### Regressionsrisiko
- [Was koennte durch den Fix betroffen sein?]

---

**Analysiert mit:** `/dtb:debug-plan`
```

Aktualisiere ausserdem den **Status** im Header von `Offen` auf `Analysiert`.

---

## Schritt 6: Bestaetigung

```
Debug-Analyse gespeichert: {config.paths.workflows}/features/BUG_[NAME].md

Root-Cause (wahrscheinlichste): {Hypothese-1-Einzeiler}
Fix-Schritte: {N} Schritte identifiziert

Naechste Schritte:
  1. Fix umsetzen: /dtb:feature-start
  2. Oder direkt fixen, falls der Bug einfach ist
```

---

## Lektion-Kandidat erkennen (Vorschlager)

Wenn dir waehrend der Analyse eine nicht-offensichtliche, wiederverwendbare Erkenntnis auffaellt
(Trigger-Frage: „Wuerde ich denselben Fehler nochmal machen, wenn das nur im Session-Log stuende?"),
schlage sie zur Aufnahme vor — **nie stiller Auto-Write**:
```
💡 Lektion-Kandidat: "{knappe Regel}". Nach lessons.md uebernehmen? (/dtb:lesson oder ja/nein)
```
Bei „ja": den Text an `/dtb:lesson` uebergeben.

---

## Richtlinien

- **Evidenzbasiert:** Hypothesen muessen auf konkretem Code basieren, nicht auf Vermutungen
- **Priorisiert:** Wahrscheinlichste Hypothese zuerst
- **Pragmatisch:** Bei einfachen Bugs reicht eine Hypothese und 1-2 Fix-Schritte
- **Kein Over-Engineering:** Nicht das halbe System analysieren — Fokus auf den Bug
- **Deutsch:** Alle Texte auf Deutsch
