# DTB Projekt-Kontext

Du liest die Projektdokumentation und fasst den relevanten Kontext zusammen.

## Aufgabe

Lade Business-Kontext, Tech-Landscape und Constraints aus `dtb-project/project-strategy/` und erstelle eine kompakte Zusammenfassung fuer den aktuellen Entwicklungskontext.

## Schritt 1: Dokumentation laden

Lies die folgenden Dateien aus `dtb-project/project-strategy/`:

1. **business-context.md** - Geschaeftsziele und Problemstellung
2. **tech-landscape.md** - Technologie-Landschaft
3. **constraints.md** - Einschraenkungen und Rahmenbedingungen
4. **stakeholders.md** - Stakeholder und Rollen
5. **team.md** - Projektteam

## Schritt 2: Kontext extrahieren

Fuer jedes Dokument:
- Identifiziere die 3-5 wichtigsten Punkte
- Extrahiere aktuelle Prioritaeten
- Notiere relevante Einschraenkungen

## Schritt 3: Kontext-Report erstellen

Erstelle einen praegnanten Report in diesem Format:

```markdown
# Projekt-Kontext: DtB-Assistant
**Stand:** {DD.MM.YYYY}

---

## Business-Kontext

### Kernziel
[1-2 Saetze: Was ist das Hauptziel des Projekts?]

### Primaere Nutzer
- [Nutzergruppe 1]: [Beduerfnis]
- [Nutzergruppe 2]: [Beduerfnis]

### Business Value
- [Wert 1]
- [Wert 2]

---

## Technologie-Kontext

### Stack-Uebersicht
| Komponente | Technologie |
|------------|-------------|
| Backend | [Tech] |
| Frontend | [Tech] |
| Datenbank | [Tech] |
| LLM | [Tech] |

### Externe Abhaengigkeiten
- **[System 1]**: [Zweck]
- **[System 2]**: [Zweck]

### Integrations-Punkte
- [Integration 1]
- [Integration 2]

---

## Einschraenkungen & Rahmenbedingungen

### Technische Constraints
- [Constraint 1]
- [Constraint 2]

### Organisatorische Constraints
- [Constraint 1]
- [Constraint 2]

### Sicherheit & Compliance
- [Anforderung 1]
- [Anforderung 2]

---

## Team & Stakeholder

### Kernteam
- [Rolle]: [Verantwortung]

### Wichtige Stakeholder
- [Stakeholder 1]: [Interesse/Einfluss]
- [Stakeholder 2]: [Interesse/Einfluss]

---

## Aktuelle Prioritaeten

1. **[Prioritaet 1]**: [Warum wichtig?]
2. **[Prioritaet 2]**: [Warum wichtig?]
3. **[Prioritaet 3]**: [Warum wichtig?]

---

## Relevanter Kontext fuer Entwicklung

**Bei Architektur-Entscheidungen beachten:**
- [Punkt 1]
- [Punkt 2]

**Bei Feature-Entwicklung beachten:**
- [Punkt 1]
- [Punkt 2]

---

*Quelle: dtb-project/project-strategy/ Dokumentation*
```

## Richtlinien

- **Kompakt**: Maximal 1-2 Seiten
- **Relevant**: Nur aktuell wichtige Informationen
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Kontext soll bei Entscheidungen helfen
- **Aktuell**: Fokus auf aktuelle Prioritaeten, nicht Historie

## Verwendung

Nutze diesen Command:
- Vor groesseren Architektur-Entscheidungen
- Beim Onboarding neuer Entwickler
- Bei Unklarheiten ueber Projektausrichtung
- Als Kontext fuer strategische Diskussionen

## Verwandte Commands

- `/dtb:project-architecture` - Technische Architektur im Detail
- `/dtb:project-prd` - MVP-Anforderungen
- `/dtb:project-roadmap` - Roadmap und Meilensteine
- `/dtb:project-glossary` - Begriffsdefinitionen

---

Lies jetzt die Projektdokumentation und erstelle den Kontext-Report.
