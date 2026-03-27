---
name: dtb:docs-extract
description: >-
  Use when: "Dokumente extrahieren", "docs extract", "PDFs einlesen",
  "Infos aus Dokumenten ziehen", "Input-Ordner scannen", "Dokumente verarbeiten".
  Scans an input/ folder, reads all files (PDF, TXT, MD, images),
  clusters facts by topic, and creates/updates thematic MD files in the parent directory.
disable-model-invocation: true
argument-hint: "[Pfad zum input-Ordner, z.B. project-infrastructure/input]"
allowed-tools: Read, Write, Glob
pipeline:
  stage: setup
  after: null
  next: null
  consumes: []
  produces: [project-infrastructure/*.md]
---

# DTB Docs Extract

Du liest alle Dokumente aus einem `input/`-Ordner und destillierst daraus thematisch getrennte `.md`-Dateien im Elternverzeichnis. Diese MDs sind fuer Claude/LLM optimiert — strukturierte Fakten mit Quellenreferenzen, keine Rohdaten.

---

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Weiter im Fallback-Modus (kein Abbruch, kein Config-Pfad noetig).

---

## Schritt 1: Input-Pfad ermitteln

**Aus Argument:** Der Pfad nach dem Skill-Aufruf ist der Input-Ordner.
Beispiel: `/dtb:docs-extract project-infrastructure/input` → Input: `project-infrastructure/input/`

**Falls kein Argument angegeben:**
```
Welcher Ordner soll gescannt werden?
Beispiel: project-infrastructure/input
```

**Elternverzeichnis ableiten** (= Output-Ziel):
- Input: `project-infrastructure/input` → Output: `project-infrastructure/`
- Input: `project-strategy/input` → Output: `project-strategy/`
- Input: `beliebig/tief/input` → Output: `beliebig/tief/`

---

## Schritt 2: Input-Ordner scannen

Nutze Glob um alle Dateien im Input-Ordner zu finden:
- `{input-pfad}/**/*.pdf`
- `{input-pfad}/**/*.txt`
- `{input-pfad}/**/*.md`
- `{input-pfad}/**/*.png`
- `{input-pfad}/**/*.jpg`
- `{input-pfad}/**/*.jpeg`
- `{input-pfad}/**/*.yaml`
- `{input-pfad}/**/*.yml`
- `{input-pfad}/**/*.json`

Falls der Ordner nicht existiert:
```
Ordner nicht gefunden: {input-pfad}/

Standardordner werden von /dtb:project-init angelegt:
  - dtb-project/project-infrastructure/input/
  - dtb-project/project-requirements/input/
  - dtb-project/project-strategy/input/
  - integrations/vendor-x/input/  (vendor-x umbenennen)

Fuer eigene Pfade: Ordner manuell anlegen, dann erneut aufrufen.
```
→ Abbruch.

Falls Ordner existiert aber keine Dateien gefunden:
```
Keine Dokumente gefunden in: {input-pfad}/

Lege Dokumente dort ab und rufe /dtb:docs-extract erneut auf.
```
→ Abbruch.

**Fuer jede gefundene Datei:**
- Lies den Inhalt mit dem Read-Tool (unterstuetzt PDF, Bilder, TXT, MD nativ)
- Notiere: relativer Dateiname + extrahierter Inhalt
- Bei PDFs: falls > 10 Seiten, lese seitenweise (pages: "1-10", "11-20" etc.)

---

## Schritt 3: Thematisch clustern

Analysiere alle extrahierten Inhalte gemeinsam und bilde Themengruppen.

**Prinzip:**
- So wenige MDs wie sinnvoll (kein 1-Fakt-MD)
- So viele wie noetig (kein 500-Zeilen-Monolith)
- Themen ergeben sich aus dem Inhalt — kein Hardcoding

**Beispiel-Mapping fuer Infrastruktur-Dokumente:**

| Thema | Dateiname |
|-------|-----------|
| Server-Hardware, Specs, IPs | `GPU_SERVERS.md` |
| Deployed Modelle, Parameter | `VLLM_MODELS.md` |
| Netzwerk, Routing, Firewall | `NETWORKING.md` |
| Auth, Keycloak, SSO | `AUTH.md` |
| Monitoring, Metriken, Alerts | `MONITORING.md` |

**Andere Kontexte erzeugen andere Themen** — lass den Inhalt entscheiden.

---

## Schritt 4: Bestehende MDs pruefen

Nutze Glob: `{elternverzeichnis}/*.md`

Fuer jede bereits existierende MD die auch in den neuen Themen vorkommt:
- Lies den bestehenden Inhalt
- Merke welche Fakten bereits enthalten sind (Duplikate vermeiden)
- Neue Fakten werden ergaenzt, bestehende nicht geloescht

---

## Schritt 5: MDs erstellen / aktualisieren

Fuer jedes Thema eine MD-Datei anlegen oder aktualisieren.

### Template (neue MD):

```markdown
# [Thema]

**Extrahiert:** [YYYY-MM-DD]
**Aktualisiert:** [YYYY-MM-DD]

---

## [Sektion]

- [Fakt] — (Quelle: input/[dateiname], S.[n])
- [Fakt] — (Quelle: input/[dateiname])

## [Weitere Sektion]

- [Fakt] — (Quelle: input/[dateiname])

---

## Quellen

- `input/[dateiname.pdf]` — [Einzeiler: was ist in dieser Datei]
- `input/[dateiname.txt]` — [Einzeiler: was ist in dieser Datei]
```

### Regeln:

- **Nur Fakten, keine Rohdaten** — Kein Copy-Paste von Tabellen/Logs, nur extrahierte Aussagen
- **Quellenreferenz pro Fakt** — Format: `(Quelle: input/datei.pdf, S.3)` oder `(Quelle: input/config.yaml)`
- **Sektionen nach Unterthemen** — z.B. Hardware-Specs, Netzwerk-Konfiguration, Known Issues
- **Kein Duplikat** — Fakt existiert bereits → nicht noch einmal einfuegen
- **Datum aktualisieren** — Bei Update: `Aktualisiert:` auf heute setzen
- **Deutsch** — Alle Inhalte auf Deutsch
- **UPPER_SNAKE_CASE** — Dateinamen: `GPU_SERVERS.md`, `VLLM_MODELS.md` etc.

---

## Schritt 6: Bestaetigung

```
Extraktion abgeschlossen:

Input:   {input-pfad}/ ({n} Dateien gelesen)
Output:  {elternverzeichnis}/
  → [DATEI_1.md]   (neu | {n} Fakten)
  → [DATEI_2.md]   (aktualisiert | {n} neue Fakten ergaenzt)
  → ...

Naechste Schritte:
  - MDs pruefen und manuell ergaenzen
  - /dtb:docs-extract erneut aufrufen wenn neue Dokumente in input/ liegen
```

---

## Richtlinien

- **Generisch:** Kein Hardcoding fuer bestimmte Themen — Inhalt bestimmt die Struktur
- **Idempotent:** Mehrfach aufrufbar ohne Datenverlust oder Duplikate
- **LLM-optimiert:** MDs sind fuer Claude/AI lesbar, nicht fuer Menschen als Hauptzielgruppe
- **Rueckfragen minimal:** Nur am Anfang wenn Pfad fehlt — danach kein Interrupt

## Verwandte Skills

- `/dtb:project-init` — Erstinitialisierung legt `project-infrastructure/` an (falls gewuenscht)
- `/dtb:workflow-checkpoint` — Session-Log nach Extraktion + Analyse
