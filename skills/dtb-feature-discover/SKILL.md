---
name: dtb:feature-discover
description: >-
  Use when: "Feature Discovery", "Idee vertiefen", "Anforderungen klaeren",
  "Discovery machen". Analyzes an idea from the inbox, scans the codebase for
  affected modules, gathers requirements through structured questions, and
  produces a DISCOVERY_*.md before spec writing.
disable-model-invocation: true
argument-hint: "[Idee-Nummer oder Suchbegriff]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: dtb:idea-review
  next: dtb:feature-plan
  consumes: [INBOX.md, workflow.config.yaml]
  produces: [DISCOVERY_*.md, INBOX.md]
---

# Feature Discovery

Du fuehrst eine strukturierte Discovery-Phase durch, bevor ein Feature spezifiziert wird. Ziel: Anforderungen klaeren, betroffene Codebase-Bereiche identifizieren und offene Fragen abarbeiten.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

---

## Schritt 1: Idee laden

Lies `{config.paths.workflows}/INBOX.md`.

- Falls ein Argument uebergeben wurde: Suche nach Nummer oder Stichwort in der Inbox
- Falls kein Argument: Filtere alle Eintraege mit Status `In Arbeit`

Falls keine passende Idee gefunden:
```
Keine passende Idee gefunden.
- Ideen mit Status "In Arbeit" werden automatisch geladen
- Alternativ: /dtb:feature-discover [Nummer oder Suchbegriff]
```

Zeige die gefundene Idee:
```
Discovery fuer Idee #{N}: "{Idee-Text}"
```

---

## Schritt 2: Codebase-Scan

Fuehre einen automatischen Scan durch:

1. Extrahiere Schluesselwoerter aus dem Idee-Text
2. Nutze Glob und Grep um betroffene Module/Dateien zu finden
3. Zeige die Ergebnisse:

```
Codebase-Scan: {Anzahl} potenziell betroffene Dateien/Module

| # | Pfad | Relevanz |
|---|------|----------|
| 1 | {Pfad} | {Kurzbeschreibung} |
| ... | ... | ... |

Stimmt das so? Fehlt etwas oder ist etwas irrelevant?
```

Warte auf Benutzer-Feedback. Bereinige die Liste entsprechend.

---

## Schritt 3: Klaerungsfragen

Gehe Kategorie fuer Kategorie durch. Stelle pro Kategorie die Fragen und warte auf Antwort, bevor die naechste Kategorie kommt.

### 3a: Scope

```
Scope-Klaerung:
1. Was genau soll das Feature koennen?
2. Was soll es explizit NICHT koennen?
```

### 3b: Gewuenschtes Verhalten

```
Gewuenschtes Verhalten:
1. Wie soll es sich fuer den Benutzer anfuehlen/verhalten?
2. Gibt es bestehende UX-Muster die uebernommen werden sollen?
```

### 3c: Randfaelle

```
Randfaelle:
1. Was passiert bei Fehlern?
2. Wie wird mit leeren Daten oder Grenzwerten umgegangen?
3. Gibt es bekannte Edge Cases?
```

### 3d: Einschraenkungen

```
Einschraenkungen:
1. Gibt es technische Constraints (Performance, Kompatibilitaet, etc.)?
2. Gibt es fachliche Constraints (Regulatorik, Business Rules, etc.)?
```

### 3e: Integrationspunkte

```
Integrationspunkte:
1. Welche bestehenden Features/Module sind betroffen?
2. Gibt es externe Abhaengigkeiten (APIs, Services, etc.)?
```

---

## Schritt 4: Abhaengigkeiten pruefen

Scanne `{config.paths.workflows}/features/` nach bestehenden FEATURE_*.md und PLAN_*.md:

- Lies jeweils Titel und Scope
- Identifiziere potenzielle Konflikte oder Ueberschneidungen
- Melde Ergebnisse:

```
Abhaengigkeits-Check:
  Bestehende Features: {N}
  Potenzielle Konflikte: {Liste oder "keine"}
  Ueberschneidungen: {Liste oder "keine"}
```

---

## Schritt 5: Feature-Name festlegen

```
Feature-Name festlegen:
  Vorschlag: {UPPER_SNAKE_CASE basierend auf Idee-Text}

  Passt das? (Ja / Alternativer Name)
```

Der Name wird fuer DISCOVERY_{NAME}.md, FEATURE_{NAME}.md und PLAN_{NAME}.md verwendet.

---

## Schritt 6: DISCOVERY_[NAME].md speichern

Speichere in `{config.paths.workflows}/features/DISCOVERY_{NAME}.md`:

```markdown
# Discovery: [Feature-Name]

**Erstellt:** [YYYY-MM-DD]
**Idee-Referenz:** Inbox #{N} — "{Idee-Text}"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| {Pfad} | {Was wird dort beruehrt} |

---

## Anforderungen

### Scope
**Enthalten:**
- [Zusammenfassung aus 3a]

**Nicht enthalten:**
- [Zusammenfassung aus 3a]

### Gewuenschtes Verhalten
- [Zusammenfassung aus 3b]

### Randfaelle
- [Zusammenfassung aus 3c]

### Einschraenkungen
- [Zusammenfassung aus 3d]

### Integrationspunkte
- [Zusammenfassung aus 3e]

---

## Abhaengigkeiten

- [Konflikte/Ueberschneidungen aus Schritt 4 oder "Keine"]

---

## Offene Punkte

- [Falls waehrend der Discovery ungeklaerte Fragen aufkamen]

---

**Erstellt mit:** `/dtb:feature-discover`
```

---

## Schritt 7: Inbox aktualisieren

- Der Status der Idee bleibt auf `In Arbeit`
- Haenge den Link `→ DISCOVERY_{NAME}.md` an die Inbox-Zeile an

---

## Schritt 8: Naechste Schritte

```
Discovery abgeschlossen: {config.paths.workflows}/features/DISCOVERY_{NAME}.md

Naechster Schritt: /dtb:feature-plan {Feature-Name}
  (Die Discovery-Ergebnisse werden automatisch uebernommen)
```
