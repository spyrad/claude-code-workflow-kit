# DTB Projekt-Analyse

Analysiere ein Brownfield-Projekt und erstelle eine umfassende Onboarding-Dokumentation.

## Aufgabe

Verstehe ein bestehendes Projekt durch Analyse von Git-History, Dateistruktur und Code-Patterns.

## Schritt 1: Projekt-Kontext erfassen

Verwende das AskUserQuestion Tool um zu fragen:
1. **Projekt-Verzeichnis?** (z.B. `assistant-backend/`, `assistant-frontend/`)
2. **Fokus?** (Backend / Frontend / Full-Stack / Spezifisches Modul)

## Schritt 2: Git-History analysieren

Falls Git-Repo vorhanden:
```bash
# Letzte 50 Commits
git log --oneline -50

# Häufigste Autoren
git shortlog -sn --all

# Meistgeänderte Dateien
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -20
```

## Schritt 3: Projekt-Struktur erfassen

1. **Verzeichnis-Übersicht**:
   - Haupt-Verzeichnisse identifizieren
   - Erkenne Architektur-Pattern (MVC, Layered, etc.)

2. **Wichtigste Dateien**:
   - Entry Points (main.py, main.tsx, index.ts)
   - Konfigurationsdateien (package.json, requirements.txt, .env.example)
   - Dokumentation (README.md, CLAUDE.md, docs/)

3. **Technologie-Stack**:
   - Programmiersprache & Version
   - Framework & Hauptbibliotheken
   - Build-Tools & Dependencies

## Schritt 4: Code-Analyse

1. **Architektur-Patterns**:
   - Wie ist der Code organisiert?
   - Welche Layer gibt es? (Routes, Services, Models, etc.)
   - Wie kommunizieren Komponenten?

2. **Wichtigste Module**:
   - Identifiziere 5-10 Kern-Module
   - Was macht jedes Modul?
   - Wie hängen sie zusammen?

3. **Konventionen & Standards**:
   - Code-Style (TypeScript, Python, etc.)
   - Namenskonventionen
   - Dokumentations-Standard

## Schritt 5: Dokumentation erstellen

Erstelle eine strukturierte Analyse in diesem Format:

```markdown
# Projekt-Analyse: {PROJEKT-NAME}
**Datum:** {DD.MM.YYYY} | **Analysiert:** {Komponente}

---

## 📋 Projekt-Übersicht

### Typ
- **Kategorie**: [Web-App / API / CLI / Library]
- **Status**: [Development / Production / Legacy]
- **Team**: [Solo / Small Team / Enterprise]

### Technologie-Stack
- **Sprache**: [Python 3.x / TypeScript / etc.]
- **Framework**: [FastAPI / React / etc.]
- **Datenbank**: [PostgreSQL / HANA / etc.]
- **Tools**: [Vite / Docker / etc.]

---

## 🏗️ Architektur

### Verzeichnis-Struktur
```
projekt/
├── src/           # [Beschreibung]
├── tests/         # [Beschreibung]
├── docs/          # [Beschreibung]
└── config/        # [Beschreibung]
```

### Architektur-Pattern
[Beschreibe das verwendete Pattern: Layered Architecture, Clean Architecture, etc.]

### Haupt-Komponenten
1. **{Komponente 1}**: [Was macht sie?]
2. **{Komponente 2}**: [Was macht sie?]
3. **{Komponente 3}**: [Was macht sie?]

---

## 🔑 Wichtigste Dateien

### Entry Points
- `{datei}`: [Beschreibung]

### Konfiguration
- `{datei}`: [Beschreibung]

### Kern-Module (Top 10)
| Datei | Zweck | Änderungshäufigkeit |
|-------|-------|---------------------|
| `{datei}` | {Zweck} | [Hoch/Mittel/Niedrig] |

---

## 📊 Git-History Insights

### Letzte Entwicklungen
[Zusammenfassung der letzten 20-30 Commits]

### Haupt-Contributoren
1. {Name}: {Commit-Anzahl} Commits
2. {Name}: {Commit-Anzahl} Commits

### Entwicklungs-Hotspots
[Welche Bereiche werden am häufigsten geändert?]

---

## 🧩 Kern-Module Deep Dive

### Modul 1: {Name}
- **Location**: `{pfad/}`
- **Zweck**: [Was macht dieses Modul?]
- **Wichtigste Dateien**:
  - `{datei}`: {Beschreibung}
- **Dependencies**: [Welche anderen Module nutzt es?]
- **Patterns**: [Verwendete Design Patterns]

### Modul 2: {Name}
...

---

## 🔗 Datenfluss & Integration

### Typischer Request-Flow
```
1. {Schritt 1}
   ↓
2. {Schritt 2}
   ↓
3. {Schritt 3}
```

### Externe Integrationen
- **{Integration}**: [Zweck]

---

## 📝 Code-Konventionen

### Namenskonventionen
- Dateien: [snake_case / kebab-case / PascalCase]
- Funktionen: [camelCase / snake_case]
- Klassen: [PascalCase]

### Dokumentation
- [Docstrings / JSDoc / Kommentare]

### Testing
- Framework: [pytest / jest / etc.]
- Coverage: [Gut / Mittel / Niedrig / Nicht vorhanden]

---

## ⚠️ Technische Schulden & Probleme

### Identifizierte Probleme
1. {Problem}: [Beschreibung]
2. {Problem}: [Beschreibung]

### Verbesserungs-Potenzial
- {Bereich}: [Konkrete Empfehlung]

---

## 🚀 Schnellstart für Entwickler

### Setup
```bash
# {Setup-Schritt 1}
# {Setup-Schritt 2}
```

### Entwicklung starten
```bash
# {Command zum Starten}
```

### Wichtigste Commands
| Command | Zweck |
|---------|-------|
| `{command}` | {Beschreibung} |

---

## 📚 Weiterführende Dokumentation

### Vorhandene Docs
- `{datei}`: [Beschreibung]

### Empfohlene nächste Schritte
1. [ ] {Action 1}
2. [ ] {Action 2}
3. [ ] {Action 3}

---

## 💡 Zusammenfassung

### Stärken
- {Stärke 1}
- {Stärke 2}

### Herausforderungen
- {Herausforderung 1}
- {Herausforderung 2}

### Empfehlung
[Gesamteinschätzung: Wie gut ist das Projekt strukturiert? Was sollte priorisiert werden?]
```

## Schritt 6: Dokumentation speichern

Speichere die Analyse mit dem Write Tool:
- Pfad: `docs/project-analysis/YYYY-MM-DD-{komponente}-analysis.md`
- Falls `docs/project-analysis/` nicht existiert, erstelle es

## Richtlinien

- **Objektiv**: Beschreibe was ist, nicht was sein sollte
- **Konkret**: Dateinamen, Funktionsnamen, konkrete Beispiele
- **Deutsch**: Alle Texte auf Deutsch
- **Actionable**: Gib konkrete nächste Schritte
- **Kontext-bewusst**: Verstehe das Business-Problem, nicht nur den Code

## Integration mit Workflow

Nach der Analyse:
1. Erwähne die Analyse-Datei in deinem nächsten `/dtb:workflow-checkpoint`
2. Nutze die Erkenntnisse fuer `/dtb:backlog`
3. Update `CLAUDE.md` falls nötig mit wichtigen Patterns

---

Analysiere jetzt das Projekt und erstelle die Projekt-Analyse.
