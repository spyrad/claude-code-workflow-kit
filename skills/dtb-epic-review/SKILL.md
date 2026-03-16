---
name: dtb:epic-review
description: >-
  Use when: "Epic Review", "Feature reviewen", "Plan bewerten",
  "Feature-Spec pruefen". Conducts a structured review of a feature plan
  with two agent perspectives (Architekt and Pragmatiker).
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[Feature-Name]"
---

# Epic Review Discussion

Du fuehrst ein strukturiertes Review eines Feature-Plans durch. Zwei Agenten (Architekt und Pragmatiker) diskutieren den Plan und stellen Damian als Product Owner gezielte Fragen.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Feature-Spec laden

1. **Feature ermitteln:** Frage den Benutzer nach dem Feature-Namen, falls nicht aus dem Chat-Kontext erkennbar
2. **Spec lesen:** Lies `{config.paths.workflows}/features/FEATURE_[NAME].md`

Falls Datei nicht gefunden:
```
Feature-Spec nicht gefunden: FEATURE_[NAME].md
Erstelle zuerst einen Feature-Plan mit /dtb:feature-plan.
```

## Schritt 2: Agent-Definitionen laden

Lies die Agenten-Definitionen aus dem Projekt-Root:
- `agents/architekt.md`
- `agents/pragmatiker.md`

Nimm diese Rollen fuer die Diskussion ein.

## Schritt 3: Diskussion fuehren

Fuehre die Diskussion in **3 Runden** basierend auf der geladenen Feature-Spec:

### Runde 1 — Staerken
Beide Agenten bewerten, was am Plan gut ist: Struktur, Phasenaufteilung, technische Entscheidungen.

### Runde 2 — Bedenken & Risiken
Beide Agenten identifizieren Luecken, Risiken und problematische Annahmen — jeweils aus ihrer Perspektive.

### Runde 3 — Fragen an Damian
Beide Agenten stellen gezielte Entscheidungsfragen an Damian. Die Fragen sollen konkret und entscheidungsrelevant sein — keine rhetorischen Fragen.

## Schritt 4: Zusammenfassung

Erstelle eine kompakte Bewertungstabelle und konkrete Empfehlungen.

## Schritt 5: Anpassungen anbieten

Frage Damian ob Anpassungen an der Feature-Spec vorgenommen werden sollen.

---

## Output-Format

Gib die Diskussion in folgendem Format aus:

```markdown
# Epic Review: [Feature-Name]
**Datum:** [YYYY-MM-DD]
**Feature-Spec:** `features/FEATURE_[NAME].md`

---

## Runde 1: Staerken

**🏗️ Architekt:** "[Einschaetzung zu Struktur, technischen Entscheidungen, Vollstaendigkeit]"

**⚡ Pragmatiker:** "[Einschaetzung zu Scope, Phasenaufteilung, Ergebnisorientierung]"

---

## Runde 2: Bedenken & Risiken

**🏗️ Architekt:** "[Technische Bedenken, fehlende Abhaengigkeiten, Risiken]"

**⚡ Pragmatiker:** "[Scope-Bedenken, Aufwand-Nutzen-Probleme, Priorisierung]"

---

## Runde 3: Fragen an Damian

**🏗️ Architekt:** "Damian, [konkrete technische Entscheidungsfrage]?"

**⚡ Pragmatiker:** "Damian, [konkrete Priorisierungs-/Scope-Frage]?"

---

## Review-Zusammenfassung

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Technische Machbarkeit | ✅/⚠️/❌ | [kurz] |
| Scope / MVP-Schnitt | ✅/⚠️/❌ | [kurz] |
| Abhaengigkeiten | ✅/⚠️/❌ | [kurz] |
| Reihenfolge der Phasen | ✅/⚠️/❌ | [kurz] |

## Empfehlungen

1. [Konkrete Empfehlung]
2. [Konkrete Empfehlung]

---

Moechtest du Anpassungen an der Feature-Spec vornehmen? (Ja/Nein)
```

---

## Wichtig — Anweisungen fuer die Ausfuehrung

- **Rollen einhalten:** Jeder Agent argumentiert konsequent aus seiner Perspektive
- **Konkret bleiben:** Keine generischen Aussagen — immer Bezug auf die spezifische Feature-Spec
- **Fragen muessen entscheidungsrelevant sein:** Nur Fragen stellen, deren Antwort den Plan tatsaechlich aendert
- **Max 3 Fragen pro Agent** in Runde 3 — Qualitaet vor Quantitaet
- **Deutsch:** Alle Texte auf Deutsch
- **Keine Datei-Erstellung:** Die Diskussion wird nur in der Konsole ausgegeben
- **Bei "Ja" zu Anpassungen:** Konkrete Aenderungen an der Feature-Spec vorschlagen und nach Bestaetigung umsetzen
