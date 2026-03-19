---
name: dtb:plan-review
description: >-
  Use when: "Plan Review", "Implementierungsplan reviewen", "Plan bewerten",
  "Plan pruefen". Conducts a structured review of an implementation plan
  with three agent perspectives (Architekt, Pragmatiker, Senior Dev).
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[Feature-Name]"
pipeline:
  stage: planning
  after: dtb:impl-plan
  next: dtb:feature-start
  consumes: [PLAN_*.md, FEATURE_*.md, agents/*.md]
  produces: []
---

# Plan Review Discussion

Du fuehrst ein strukturiertes Review eines Implementierungsplans durch. Drei Agenten (Architekt, Pragmatiker und Senior Dev) diskutieren den Plan und stellen Damian als Product Owner gezielte Fragen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Plan und Feature-Spec laden

1. **Feature ermitteln:** Frage den Benutzer nach dem Feature-Namen, falls nicht aus dem Chat-Kontext erkennbar
2. **Plan lesen:** Lies `{config.paths.workflows}/features/PLAN_[NAME].md`
3. **Feature-Spec lesen:** Lies `{config.paths.workflows}/features/FEATURE_[NAME].md` als zusaetzlichen Kontext

Falls Plan nicht gefunden:
```
Implementierungsplan nicht gefunden: PLAN_[NAME].md
Erstelle zuerst einen Implementierungsplan mit /dtb:impl-plan.
```

## Schritt 2: Agent-Definitionen laden

Lies die Agenten-Definitionen aus dem Projekt-Root:
- `agents/architekt.md`
- `agents/pragmatiker.md`
- `agents/senior-dev.md`

Nimm diese Rollen fuer die Diskussion ein.

## Schritt 3: Diskussion fuehren

Fuehre die Diskussion in **3 Runden** basierend auf dem geladenen Implementierungsplan (mit Feature-Spec als Kontext):

### Runde 1 — Staerken des Implementierungsplans
Alle drei Agenten bewerten, was am Plan gut ist — jeweils aus ihrer Perspektive: Systemdesign (Architekt), Scope (Pragmatiker), Umsetzbarkeit (Senior Dev).

### Runde 2 — Bedenken & Risiken
Alle drei Agenten identifizieren Probleme aus ihrer Perspektive: technische Risiken und Abhaengigkeiten (Architekt), Scope-Creep und Aufwand-Nutzen (Pragmatiker), unrealistische Zeitschaetzungen und fehlende Implementierungsschritte (Senior Dev).

### Runde 3 — Challenge-Runde (Anti-Bias)
Alle drei Agenten wenden gezielt kritische Analysetechniken an:
- **Architekt:** Pre-Mortem — "Angenommen das Feature ist gescheitert. Was war die wahrscheinlichste Ursache?"
- **Pragmatiker:** Devil's Advocate — "Was spricht GEGEN diesen Plan? Welche einfachere Alternative wurde uebersehen?"
- **Senior Dev:** Unknown Unknowns — "Was wissen wir NICHT, das uns spaeter ueberraschen koennte?"

### Runde 4 — Fragen an Damian
Alle drei Agenten stellen gezielte Entscheidungsfragen an Damian. Die Fragen sollen konkret und entscheidungsrelevant sein — keine rhetorischen Fragen. Fragen koennen sich auf Erkenntnisse aus der Challenge-Runde beziehen.

## Schritt 4: Zusammenfassung

Erstelle eine kompakte Bewertungstabelle und konkrete Empfehlungen.

## Schritt 5: Anpassungen anbieten

Frage Damian ob Anpassungen am Implementierungsplan vorgenommen werden sollen.

---

## Output-Format

Gib die Diskussion in folgendem Format aus:

```markdown
# Plan Review: [Feature-Name]
**Datum:** [YYYY-MM-DD]
**Implementierungsplan:** `features/PLAN_[NAME].md`
**Feature-Spec:** `features/FEATURE_[NAME].md`

---

## Runde 1: Staerken des Implementierungsplans

**🏗️ Architekt:** "[Einschaetzung zu Systemdesign, technischen Entscheidungen, Abhaengigkeiten]"

**⚡ Pragmatiker:** "[Einschaetzung zu Scope, Ergebnisorientierung, Priorisierung]"

**💻 Senior Dev:** "[Einschaetzung zu Umsetzbarkeit, Schrittfolge, Zeitschaetzungen]"

---

## Runde 2: Bedenken & Risiken

**🏗️ Architekt:** "[Technische Risiken, Systemgrenzen, Abhaengigkeiten]"

**⚡ Pragmatiker:** "[Aufwand-Nutzen-Probleme, Scope-Creep, Priorisierung]"

**💻 Senior Dev:** "[Unrealistische Zeitschaetzungen, fehlende Schritte, Teststrategie]"

---

## Runde 3: Challenge (Anti-Bias)

**🏗️ Architekt (Pre-Mortem):** "Angenommen dieses Feature ist gescheitert — [wahrscheinlichstes Szenario und Ursache]."

**⚡ Pragmatiker (Devil's Advocate):** "Gegen diesen Plan spricht: [staerkstes Gegenargument]. Alternative: [einfachere Loesung]."

**💻 Senior Dev (Unknown Unknowns):** "Was wir nicht wissen: [versteckte Risiken, fehlende Informationen, ungetestete Annahmen]."

---

## Runde 4: Fragen an Damian

**🏗️ Architekt:** "Damian, [konkrete technische Entscheidungsfrage]?"

**⚡ Pragmatiker:** "Damian, [konkrete Priorisierungs-/Scope-Frage]?"

**💻 Senior Dev:** "Damian, [konkrete Frage zu Umsetzung/Zeitrahmen/Teststrategie]?"

---

## Review-Zusammenfassung

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Technische Machbarkeit | ✅/⚠️/❌ | [kurz] |
| Scope / MVP-Schnitt | ✅/⚠️/❌ | [kurz] |
| Abhaengigkeiten | ✅/⚠️/❌ | [kurz] |
| Reihenfolge der Phasen | ✅/⚠️/❌ | [kurz] |
| Zeitschaetzungen | ✅/⚠️/❌ | [kurz] |
| Teststrategie | ✅/⚠️/❌ | [kurz] |

## Empfehlungen

1. [Konkrete Empfehlung]
2. [Konkrete Empfehlung]

---

Moechtest du Anpassungen am Implementierungsplan vornehmen? (Ja/Nein)
```

---

## Wichtig — Anweisungen fuer die Ausfuehrung

- **Rollen einhalten:** Jeder Agent argumentiert konsequent aus seiner Perspektive
- **Konkret bleiben:** Keine generischen Aussagen — immer Bezug auf den spezifischen Implementierungsplan
- **Feature-Spec als Kontext:** Die Feature-Spec definiert das "Was/Warum" — der Plan das "Wie". Pruefe ob der Plan die Feature-Anforderungen vollstaendig abdeckt
- **Fragen muessen entscheidungsrelevant sein:** Nur Fragen stellen, deren Antwort den Plan tatsaechlich aendert
- **Max 3 Fragen pro Agent** in Runde 3 — Qualitaet vor Quantitaet
- **Deutsch:** Alle Texte auf Deutsch
- **Keine Datei-Erstellung:** Die Diskussion wird nur in der Konsole ausgegeben
- **Bei "Ja" zu Anpassungen:** Konkrete Aenderungen am Implementierungsplan vorschlagen und nach Bestaetigung umsetzen
