---
name: dtb:debug-plan
description: >-
  Use when: "Bug analysieren", "debug plan", "Root Cause", "Fehler untersuchen",
  "warum passiert das", "Bug fixen planen". Creates a structured debug plan
  with root-cause hypotheses and fix strategy based on an existing features/<slug>/bug.md.
disable-model-invocation: true
argument-hint: "[Bug-Name]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: [dtb:bug-report]
  next: [dtb:feature-start]
  consumes: [features/*/bug.md, project-rules/lessons.md]
  produces: [features/*/bug.md]
---

# Debug-Plan erstellen

Du bist ein Debug-Analyst. Deine Aufgabe ist es, basierend auf einem bestehenden Bug-Report eine strukturierte Root-Cause-Analyse und Fix-Strategie zu erstellen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `debug-plan` oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen bei Hypothesen und Fix-Strategie still an
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei nach dem Filter behaltene Lektionen mit gegensaetzlicher `Rule` — z.B. „immer X" vs. „nie X" zum selben Gegenstand):
  beide zeigen und den Widerspruch melden — nicht selbst aufloesen

---

## Schritt 1: Bug-Report laden

### Bug-Name / Slug ermitteln
- Aus dem Argument oder Frage den Benutzer
- Leite den kebab-case-Slug ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "Login broken" → `features/login-broken/`)

### Bug-Report lesen
- Lies `{config.paths.workflows}/features/{slug}/bug.md`
- Falls Datei nicht gefunden:
  ```
  Bug-Report nicht gefunden: features/{slug}/bug.md
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

Formuliere 2-3 Hypothesen und fuehre sie in einer **Hypothesen-Tabelle mit Evidenzstaerke**:

| # | Hypothese (Was) | Wo (Datei:Zeile) | Evidenz | Staerke |
|---|-----------------|------------------|---------|---------|
| 1 | … | `pfad:zeile` | konkreter Codebefund/Beobachtung | STRONG/WEAK/NONE |

**Evidenzstaerke** (auf Basis des in Schritt 2 gelesenen Codes, nie Vermutung):
- **STRONG:** direkter Codebefund erklaert das Symptom vollstaendig
- **WEAK:** plausibel, aber Beleg indirekt/unvollstaendig — Pruefung noetig
- **NONE:** noch kein Beleg, reine Vermutung → Pruefschritt definieren, bevor sie Fix-Grundlage wird

Sortiere nach Staerke (STRONG zuerst). Zu jeder Hypothese zusaetzlich: **Warum** (fuehrt zum
Symptom) und **Pruefung** (wie verifizieren).

**Ergebnis „Framing war korrekt" (valider Ausgang):** Erreicht KEINE Hypothese mindestens WEAK
mit klarer Pruefung — oder zeigt die Untersuchung, dass das Symptom bereits behoben ist, gar nicht
reproduziert oder falsch geframt war —, ist das ein legitimes Endergebnis. Dann KEINE Fix-Strategie
erfinden: dokumentiere den Befund („Framing war korrekt / kein Root-Cause im vermuteten Bereich")
und den naechsten sinnvollen Schritt (Bug neu framen, Repro schaerfen, schliessen).

---

## Schritt 4: Fix-Strategie entwickeln

Basierend auf der wahrscheinlichsten Hypothese:

1. **Fix-Schritte:** Konkrete Aenderungen mit Dateibezug
2. **Testplan:** Wie verifizieren wir dass der Fix funktioniert?
3. **Regressionsrisiko:** Was koennte durch den Fix kaputt gehen?

---

## Schritt 5: Bug-Report aktualisieren

Ergaenze die bestehende `features/{slug}/bug.md` um einen Analyse-Abschnitt:

```markdown

---

## Analyse

**Analysiert:** [YYYY-MM-DD]
**Status:** Offen → Analysiert

### Root-Cause-Hypothesen

| # | Hypothese | Wo (Datei:Zeile) | Evidenz | Staerke |
|---|-----------|------------------|---------|---------|
| 1 | [wahrscheinlichste Ursache] | `[Pfad:Zeile]` | [Codebefund] | STRONG/WEAK/NONE |
| 2 | [Alternative] | `[Pfad:Zeile]` | [Codebefund] | STRONG/WEAK/NONE |

Je Hypothese ergaenzend — **Begruendung:** [warum fuehrt das zum Symptom?] · **Pruefung:** [wie verifizieren?]

### Ergebnis (nur wenn keine tragfaehige Hypothese)

- **Befund:** Framing war korrekt / kein Root-Cause im vermuteten Bereich / nicht reproduzierbar / bereits behoben
- **Naechster Schritt:** [Bug neu framen | Repro schaerfen | schliessen]

---

## Fix-Schritte

> Nur ausfuellen, wenn mindestens eine Hypothese STRONG/WEAK mit Pruefung ist; sonst „## Analyse → Ergebnis" nutzen.
> **Diese Checkliste ist die Status-Quelle** (DERIVED_STATE_RULES §1.5): 0 abgehakt = Analysiert, teilweise = In Arbeit, alle = Behoben.

- [ ] [Konkrete Aenderung in Datei X]
- [ ] [Konkrete Aenderung in Datei Y]

**Regressionsrisiko:** [Was koennte durch den Fix betroffen sein?]

## Testplan

- [ ] [Test 1: Reproduktionsschritte nochmal durchfuehren]
- [ ] [Test 2: Regression pruefen fuer ...]

---

**Analysiert mit:** `/dtb:debug-plan`
```

Aktualisiere ausserdem den **Status** im Header von `Offen` auf `Analysiert`. Beim
Framing-Ergebnis (keine Fix-Strategie) bleibt der Bug faktisch analysiert, aber ohne Fix-Schritte —
den Naechsten-Schritt-Befund im Header vermerken.

---

## Schritt 6: Bestaetigung

```
Debug-Analyse gespeichert: {config.paths.workflows}/features/{slug}/bug.md

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
