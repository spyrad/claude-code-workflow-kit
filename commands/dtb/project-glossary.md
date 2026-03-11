# DTB Projekt-Glossar

Du liest das Glossar und zeigst relevante Begriffsdefinitionen.

## Aufgabe

Lade das Glossar aus `dtb-project/project-strategy/glossary.md` und zeige relevante Begriffe basierend auf dem aktuellen Kontext oder einer Suchanfrage.

## Schritt 1: Kontext ermitteln

Verwende das AskUserQuestion Tool um zu fragen:

**Frage:** Welche Begriffe moechtest du nachschlagen?

**Optionen:**
1. **Alle anzeigen** - Komplettes Glossar
2. **LLM/AI-Begriffe** - KI-spezifische Terminologie
3. **Business-Begriffe** - Fachbegriffe aus dem Geschaeftskontext
4. **Technische Begriffe** - Architektur und Implementierung
5. **Spezifischer Begriff** - Nach einem bestimmten Begriff suchen

## Schritt 2: Glossar laden

Lies die Datei:
- **dtb-project/project-strategy/glossary.md**

## Schritt 3: Begriffe filtern und anzeigen

Je nach Auswahl:

### Option: Alle anzeigen
Zeige das komplette Glossar, gruppiert nach Kategorien.

### Option: Kategorie-Filter
Filtere nach relevanten Begriffen fuer die gewaehlte Kategorie.

### Option: Spezifischer Begriff
Suche nach dem Begriff und zeige:
- Definition
- Kontext im Projekt
- Verwandte Begriffe

## Schritt 4: Glossar-Report erstellen

```markdown
# Glossar: DtB-Assistant
**Stand:** {DD.MM.YYYY} | **Filter:** {Gewaehlte Option}

---

## Begriffe

### [Begriff 1]
**Definition:** [Erklaerung]
**Kontext:** [Wie wird der Begriff im Projekt verwendet?]
**Siehe auch:** [Verwandte Begriffe]

---

### [Begriff 2]
**Definition:** [Erklaerung]
**Kontext:** [Wie wird der Begriff im Projekt verwendet?]
**Siehe auch:** [Verwandte Begriffe]

---

## Abkuerzungen

| Abkuerzung | Bedeutung | Erklaerung |
|------------|-----------|------------|
| MCP | Model Context Protocol | Protokoll fuer LLM-Tool-Integration |
| RAG | Retrieval-Augmented Generation | Wissensbasierte LLM-Erweiterung |
| KPI | Key Performance Indicator | Geschaeftskennzahl |

---

## Haeufig verwechselte Begriffe

| Begriff A | Begriff B | Unterschied |
|-----------|-----------|-------------|
| [Begriff 1] | [Begriff 2] | [Was ist der Unterschied?] |

---

*Quelle: dtb-project/project-strategy/glossary.md*
```

## Schnellzugriff-Modus

Falls der User direkt einen Begriff angibt (z.B. `/dtb:project-glossary MCP`):
- Ueberspringe die Frage
- Suche direkt nach dem Begriff
- Zeige Definition und Kontext

## Richtlinien

- **Praezise**: Korrekte Definitionen
- **Kontextbezogen**: Erklaere Begriffe im Projekt-Kontext
- **Verstaendlich**: Auch fuer Nicht-Experten lesbar
- **Deutsch**: Alle Texte auf Deutsch
- **Vernetzt**: Zeige verwandte Begriffe

## Verwendung

Nutze diesen Command:
- Bei unbekannten Fachbegriffen
- Beim Onboarding neuer Teammitglieder
- Bei Kommunikation mit Stakeholdern
- Zur Klaerung von Missverstaendnissen

## Verwandte Commands

- `/dtb:project-context` - Gesamtkontext
- `/dtb:project-architecture` - Technische Details

---

Frage jetzt nach dem gewuenschten Filter und zeige das Glossar.
