---
name: dtb:feature-discover
description: >-
  Use when: "Feature Discovery", "Idee vertiefen", "Anforderungen klaeren",
  "Discovery machen". Analyzes an idea from the inbox, scans the codebase for
  affected modules, gathers requirements through structured questions, and
  produces a features/<slug>/discovery.md before spec writing.
disable-model-invocation: true
argument-hint: "[Idee-Nummer oder Suchbegriff]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: [dtb:idea-review]
  next: [dtb:feature-plan]
  consumes: [INBOX.md, workflow.config.yaml]
  produces: [features/*/discovery.md, INBOX.md]
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

> **Wartungs-Hinweis (Format-Kopplung):** Diese Liste wird in Schritt 6 als `## Betroffene Module`
> in `discovery.md` geschrieben und von `dtb:impl-plan` als Ausloese-Kriterium seines
> Codebase-Research-Schritts geparst (jede Zeile mit fuehrendem Pfad-Token). Aenderst du hier das
> Format der `## Betroffene Module`-Zeilen, die Pfad-Zeilen-Erkennung in `impl-plan` mitdenken.

---

## Schritt 3: Klaerungsfragen

Gehe Kategorie fuer Kategorie durch. Stelle pro Kategorie die Fragen und warte auf Antwort, bevor die naechste Kategorie kommt.

**Wiederaufnahme (leichtgewichtig):** Nach jeder beantworteten Kategorie speichere den
DISCOVERY-Entwurf (Schritt-6-Template, so weit befuellt) mit einem Resume-Marker als
**HTML-Kommentar** direkt unter dem Header: `<!-- resume: {zuletzt beantwortete Kategorie, z.B. 3c} -->`.
Bewusst ein Kommentar statt YAML-Frontmatter — so ignorieren project-health und pipeline-graph
den DISCOVERY-Konsum unveraendert. Wird der Skill fuer eine Idee erneut gestartet und existiert
bereits `{config.paths.workflows}/features/<slug>/discovery.md` mit einem Marker ungleich `done`,
biete an, ab der naechsten Kategorie fortzusetzen (bereits beantwortete Kategorien nicht erneut fragen).

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

Scanne `{config.paths.workflows}/features/*/` nach bestehenden Change-Ordnern (`spec.md`/`plan.md`):

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

## Schritt 5: Feature-Name / Slug festlegen

```
Feature-Name festlegen:
  1. {Name basierend auf Idee-Text} (Recommended)  →  Ordner: features/{slug}/
  2. Alternativer Name (angeben)
```

Aus dem Namen wird der **kebab-case-Slug** abgeleitet (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4).
Der Change-Ordner `features/{slug}/` traegt die fixen Dateien `discovery.md`, `spec.md`, `plan.md`.
Bei einer Slug-Kollision mit einem bestehenden Ordner (anderer Name, gleicher Slug) → melden und
einen anderen Namen erfragen (kein Auto-Suffix, §4).

**„(Recommended)"-Muster:** An echten Auswahlpunkten dieses Skills — dem Namensvorschlag hier und
einem etwaigen Scope-Schnitt (wenn eine Sammelidee in mehrere Features zerlegt wird) — die
empfohlene Option als erste listen und mit `(Recommended)` markieren. Gilt NUR fuer solche
Auswahlpunkte; die offenen Klaerungsfragen (3a-3e) bleiben Freitext ohne Optionsliste.

---

## Schritt 6: discovery.md speichern

Lege bei Bedarf den Ordner `{config.paths.workflows}/features/{slug}/` an und speichere in
`{config.paths.workflows}/features/{slug}/discovery.md` (setzt den Resume-Marker aus
Schritt 3 final auf `<!-- resume: done -->`):

```markdown
# Discovery: [Feature-Name]
<!-- resume: done -->

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

- [Falls waehrend der Discovery ungeklaerte Fragen aufkamen — als konkrete Frage formulieren]
- [Gehoert eine Frage ins Fach-Meeting (nicht sofort/allein beantwortbar)? → als Checkbox mit Tag erfassen: `- [ ] [Fach] {Frage}`. Ein normaler „selbst-zu-klaeren"-Punkt bleibt untagged. Kanon/Details: `DERIVED_STATE_RULES.md` §6 — diese Zeile ist selbsterklaerend, der Verweis nur der Kanon-Ort]

---

**Erstellt mit:** `/dtb:feature-discover`
```

---

## Schritt 7: Inbox aktualisieren

- Der Status der Idee bleibt auf `In Arbeit`
- Haenge den Link `→ features/{slug}/discovery.md` an die Inbox-Zeile an

---

## Schritt 8: Naechste Schritte

```
Discovery abgeschlossen: {config.paths.workflows}/features/{slug}/discovery.md

Naechster Schritt: /dtb:feature-plan {Feature-Name}
  (Die Discovery-Ergebnisse werden automatisch uebernommen)
```
