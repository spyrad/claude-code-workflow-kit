# DTB Projekt-Architektur

Du liest die Architektur-Dokumentation und erklaerst die technischen Zusammenhaenge.

## Aufgabe

Lade die Architektur-Dokumente aus `dtb-project/project-strategy/architecture/` und erstelle eine verstaendliche Uebersicht der System-Architektur.

## Schritt 1: Architektur-Dokumente laden

Lies die folgenden Dateien:

1. **dtb-project/project-strategy/architecture/llm-production-architecture.md** - LLM-Produktionsarchitektur
2. **dtb-project/project-strategy/architecture/multi-agent-architecture.md** - Multi-Agenten-Konzept
3. **dtb-project/project-strategy/tech-landscape.md** - Technologie-Landschaft (fuer Kontext)

## Schritt 2: Architektur analysieren

Fuer jedes Architektur-Dokument:
- Identifiziere Kernkomponenten
- Verstehe Datenfluss und Interaktionen
- Notiere Design-Entscheidungen und deren Gruende
- Erkenne Schnittstellen zu anderen Systemen

## Schritt 3: Architektur-Report erstellen

Erstelle einen strukturierten Report in diesem Format:

```markdown
# Architektur-Uebersicht: DtB-Assistant
**Stand:** {DD.MM.YYYY}

---

## System-Uebersicht

### Architektur-Stil
[Beschreibe den uebergeordneten Architektur-Stil: Microservices, Monolith, Hybrid, etc.]

### Komponenten-Diagramm (ASCII)
```
+------------------+     +------------------+
|    Frontend      |<--->|    Backend       |
|   (React/TS)     |     |   (FastAPI)      |
+------------------+     +--------+---------+
                                  |
                         +--------v---------+
                         |   LLM-Engine     |
                         |  (Multi-Provider)|
                         +--------+---------+
                                  |
              +-------------------+-------------------+
              |                   |                   |
     +--------v--------+ +--------v--------+ +--------v--------+
     |   MCP Server    | |   Vector DB     | |   SAP HANA      |
     |   (KPI-Daten)   | |   (Qdrant)      | |   (Stammdaten)  |
     +-----------------+ +-----------------+ +-----------------+
```

---

## LLM-Architektur

### Provider-Strategie
[Erklaere Multi-Provider-Ansatz: Ollama, Claude, Groq, etc.]

### Kernkomponenten
| Komponente | Zweck | Datei |
|------------|-------|-------|
| AssistantAgent | [Zweck] | `src/classes/class_assistant_agent.py` |
| LLM-Engine | [Zweck] | `src/classes/class_llm.py` |
| MCP-Client | [Zweck] | `src/classes/class_mcp.py` |

### Datenfluss
```
1. User-Anfrage
   |
   v
2. AssistantAgent empfaengt
   |
   v
3. Tool-Auswahl (lokal + MCP)
   |
   +---> Lokale Tools (Calculator, etc.)
   |
   +---> MCP Server (KPI-Abfragen)
   |
   v
4. LLM-Verarbeitung
   |
   v
5. Streaming-Response an Frontend
```

### Design-Entscheidungen
| Entscheidung | Grund | Alternative |
|--------------|-------|-------------|
| [Entscheidung 1] | [Warum?] | [Was waere alternativ?] |
| [Entscheidung 2] | [Warum?] | [Was waere alternativ?] |

---

## Multi-Agent-Architektur

### Agent-Typen
| Agent | Verantwortung | Tools |
|-------|---------------|-------|
| [Agent 1] | [Was macht er?] | [Welche Tools?] |
| [Agent 2] | [Was macht er?] | [Welche Tools?] |

### Orchestrierung
[Wie werden Agents koordiniert? Sequentiell, parallel, hierarchisch?]

### Kommunikation
[Wie kommunizieren Agents untereinander?]

---

## Integration Points

### Externe Systeme
| System | Protokoll | Zweck |
|--------|-----------|-------|
| MCP Server | stdio/JSON | KPI-Daten |
| Qdrant | REST | Vector Search |
| SAP HANA | ODBC | Stammdaten |
| Keycloak | OIDC | Auth |

### API-Schnittstellen
- **WebSocket**: Real-time Kommunikation Frontend <-> Backend
- **REST**: Fallback und spezifische Endpoints
- **MCP**: Tool-Aufrufe zu externen Datenquellen

---

## Skalierung & Performance

### Aktuelle Grenzen
- [Grenze 1]: [Beschreibung]
- [Grenze 2]: [Beschreibung]

### Skalierungs-Optionen
- [Option 1]: [Beschreibung]
- [Option 2]: [Beschreibung]

---

## Architektur-Prinzipien

1. **[Prinzip 1]**: [Erklaerung]
2. **[Prinzip 2]**: [Erklaerung]
3. **[Prinzip 3]**: [Erklaerung]

---

## Offene Architektur-Fragen

- [ ] [Frage 1]
- [ ] [Frage 2]

---

*Quelle: dtb-project/project-strategy/architecture/ Dokumentation*
```

## Richtlinien

- **Technisch praezise**: Korrekte Begriffe und Zusammenhaenge
- **Visuell**: ASCII-Diagramme wo moeglich
- **Begruendet**: Design-Entscheidungen mit Gruenden
- **Deutsch**: Alle Texte auf Deutsch
- **Aktuell**: Nur implementierte Architektur, keine Zukunftsplaene

## Verwendung

Nutze diesen Command:
- Vor Implementierung neuer Features
- Bei Architektur-Diskussionen
- Beim Onboarding neuer Entwickler
- Bei Performance-Analysen

## Verwandte Commands

- `/dtb:project-context` - Business-Kontext
- `/dtb:project-prd` - Anforderungen
- `/dtb:project-roadmap` - Roadmap

---

Lies jetzt die Architektur-Dokumentation und erstelle den Report.
