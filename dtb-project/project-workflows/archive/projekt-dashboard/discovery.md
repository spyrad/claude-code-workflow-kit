# Discovery: Projekt-Dashboard
<!-- resume: done -->

**Erstellt:** 2026-10-26
**Idee-Referenz:** Inbox #135 — "Projekt-Dashboard als lokale HTML-Seite: zeigt auf einen Blick, was zuletzt gemacht wurde, wo wir stehen (aktives Feature, Fortschritt, offene Aufgaben) und was in INBOX/Befund-Becken liegt (Anzahl + Liste). Grafisch ansprechend. Aktualisierung: automatisch bei /dtb:workflow-checkpoint + auf Abruf; Live-Server als spätere Option."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-project-dashboard/SKILL.md | Neuer Skill `dtb:project-dashboard`: hält Gerüst + Abschnittsregeln (eine Quelle), erzeugt das Dashboard auf Abruf und öffnet es im Browser |
| skills/dtb-workflow-checkpoint/SKILL.md | Neuer Schritt zwischen Schritt 4 (WORKFLOW_STATUS) und 5 (Archiv-Hinweis): Dashboard erzeugen per Verweis auf den Skill (Struktur-Check, keine Kopie), Pfad-Zeile in Schritt 6, Überspringen im Worktree |
| skills/dtb-pipeline-graph/SKILL.md | Vorbild: eigenständiges HTML nach `dtb-project/*.html`, unversioniert; STYLE.md-Logik |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | Ableitungsgrundlage: §1/§2/§3 Status, §6.4 Becken, §9 offene Aufgaben, §10 Worktrees |
| skills/dtb-workflow-status/SKILL.md | Bestehende Status-Ableitung (Referenz, nicht kopieren) |
| skills/dtb-workflow-next/SKILL.md | Bestehende Status-Ableitung + Worktree-Block (Referenz) |
| skills/dtb-backlog-status/SKILL.md | Bestehende Backlog-Sicht nach Status (Referenz) |
| dtb-project/project-workflows/WORKFLOW_STATUS.md | Datenquelle: offene Aufgaben, Meilensteine, Handoff |
| dtb-project/project-changelog/ | Datenquelle „zuletzt gemacht" (Session-Logs YYYY-MM/YYYY-MM-DD.md) |
| dtb-project/project-workflows/INBOX.md | Datenquelle: offene Ideen (Anzahl + Liste) |
| dtb-project/project-workflows/INBOX-BEFUNDE.md | Datenquelle: Befund-Becken (status-neutral, §6.4) |
| dtb-project/project-workflows/BACKLOG.md | Datenquelle: Backlog-Stand nach Status |
| .gitignore | `dtb-project/*` hält generiertes HTML lokal — Ablageort prüfen |
| skills/dtb-project-init/SKILL.md | Skill-Liste + `dashboard:`-Block im Config-Seed |
| workflow.config.yaml | Neuer Block `dashboard:` mit `bei_checkpoint: true` |
| CLAUDE.md | Skill-Katalog + Output Locations nachziehen |
| skills/CLAUDE.md | Kanon-Abschnitte ggf. nachziehen |

---

## Anforderungen

### Scope
**Enthalten:**
- Block „Zuletzt gemacht" (letzte Session-Logs)
- Block „Wo wir stehen": aktives Feature, Fortschritt, offene Aufgaben
- Block INBOX + Befund-Becken: Anzahl + Liste
- Backlog-Stand: Aufgaben/Features gruppiert nach abgeleitetem Status (DSR §3, z. B. „Fertig zum Testen") — Status aus Artefakten, nicht aus der BACKLOG-Anzeigespalte (Artefakt gewinnt)
- Lektionen: Anzahl in `project-rules/lessons.md` + Füllstand gegen das Soft-Limit ~150 Zeilen (Signal „Kuratierung fällig" → #141)
- Worktrees (laufende Panes, DSR §10), abgeschlossene Meilensteine, nächster empfohlener Befehl
- Verteilter Kit-Skill — läuft in jedem Zielprojekt, nicht nur im Kit

**Nicht enthalten:**
- Lektionen-Inhalte oder deren Bewertung (veraltet/doppelt) — das ist Kuratierung, INBOX #141
- `[Fach]`-Fragen (später ergänzbar)
- Aktionen/Buttons — rein lesend, ändert keine Datei ausser dem eigenen HTML
- Live-Server (laut Idee spätere Option), Trends/Historie über Zeit
- Ablösung von WORKFLOW_STATUS.md

### Gewuenschtes Verhalten
- **Design-Sprache angelehnt an https://www.aihero.dev/** (extrahiert 2026-10-26, nur Stil — kein Logo, kein Bildmaterial, kein Markenname):
  - Typografie: Vorlage nutzt DM Sans (Fliesstext + Headlines, 700, enges negatives Letter-Spacing −0.02…−0.04em) und JetBrains Mono für Labels/Kennzahlen (uppercase, 11px, Sperrung ~0.16em, gedämpft). **Umsetzung nur mit Systemschriften** (`system-ui`/Segoe UI bzw. `ui-monospace`/Cascadia/Consolas) — Charakter über Gewichte, Laufweite, Mono-Labels und Farben (siehe Einschränkungen)
  - Farben hell: Seite `#f1f2f5`, Flächen `#fbfbfc`/Karte `#fff`, Text `#14161a` mit Alpha-Abstufungen (body cc, muted b3, label 99, faint 59), Linien `#14161a` 1a/12/24
  - Farben dunkel: Seite `#0b0b0b`, Karte `#100f0e`, Text `#f4f3f1` mit denselben Alpha-Stufen, Linien weiss 14/0f/1f
  - Einziger Akzent Gold `#f5c451` (Hover `#eab534`), Text darauf `#191510`; Ja/Nein-Marken grün `#007e46`/`#58da98`, rot `#c9302d`/`#fd736d`
  - Radius 9px (Karten), 6px (Buttons), 4px (Chips mit 1px-Rahmen); viel Weissraum, keine Schatten
  - Muster „Kennzahlen-Leiste": grosse Mono-Zahl + kleines Mono-Label darunter (wie „134,500+ / DEVELOPERS LEARNING")
- **Dark Mode ist Standard:** Seite öffnet immer dunkel; kleiner Umschalter ☾/☀ oben rechts, Wahl im Browser gemerkt (`localStorage`, ~10 Zeilen JS, in try/catch). Rein lesend bleibt gewahrt — der Schalter ändert keine Projektdatei
- **Öffnen:** auf Abruf öffnet der Skill die Seite im Browser; beim Checkpoint nur schreiben + eine Pfad-Zeile (kein Browser-Popup je Checkpoint)
- **Aufbau:** oben Kennzahlen-Leiste, darunter Sektionen: Wo wir stehen → Backlog nach Status → Zuletzt gemacht → INBOX/Becken; lange Listen einklappbar (`<details>`, kein JavaScript nötig)
- **Verlinkung:** Einträge verlinken relativ auf ihre Quelldatei (plan.md, Session-Log, INBOX)

### Randfaelle
- **Fehlende Quelle** (z. B. kein `INBOX-BEFUNDE.md`, keine `lessons.md`, kein Changelog): Block bleibt stehen, gedämpft, mit Vermerk „nicht vorhanden: {Datei}" — Seitenstruktur ist immer gleich, Lücke sichtbar
- **Defekte Daten** (falsche Spaltenzahl, `plan.md` ohne `## Progress`, Anzeige ≠ Ableitung): DSR-Regel „Artefakt gewinnt" — mit dem abgeleiteten Wert weiterrechnen, Konflikt als **Warnchip** am Eintrag
- **Kein aktives Feature:** Leerzustand „Kein aktives Feature" + empfohlener nächster Befehl aus dem Handoff
- **Lange Listen:** Anzahl in der Kennzahlen-Leiste; im Block die neuesten 10 mit Kurztitel, Rest in `<details>` („alle N anzeigen")
- **Zuletzt gemacht:** letzte 5 Sessions (Datum + Überschrift); Fenster später per Config steuerbar
- **Worktree, Checkpoint:** Dashboard-Schritt übersprungen mit Hinweiszeile `↷ Dashboard-Update übersprungen (Worktree)` (Teil-Guard-Muster); Haupt-Checkout erzeugt nach Merge neu
- **Worktree, auf Abruf:** wird erzeugt, mit Banner „Worktree-Ansicht `feature/x` — globaler Stand vom Abzweig, massgeblich ist der Haupt-Checkout" (Datei ist lokal + unversioniert, harmlos)
- **Inhalte escapen:** Text aus INBOX/Logs kann `<`, `>`, `&`, Pipes enthalten — HTML-escapen

### Einschraenkungen
**Technisch:**
- **Claude schreibt das HTML** (Muster `pipeline-graph`): festes HTML/CSS-Gerüst mit Platzhaltern in der SKILL.md, Claude liest die Quellen und füllt es. Kein Skript, keine Laufzeit-Abhängigkeit — das Kit bleibt reines Markdown, `kit-sync` verteilt weiterhin nur `SKILL.md`. Ableitung referenziert DSR (eine Quelle), wird nicht in Code nachgebaut
- **Ablageort:** `dtb-project/project-dashboard.html` — neben `dtb-project/claude-code-workflow-kit.html`, durch `dtb-project/*` in `.gitignore` bereits unversioniert; in Zielprojekten prüft der Skill einmal, ob die Datei ignoriert wird, und schlägt sonst die Zeile vor
- **Vollständig lokal:** einzelne, eigenständige HTML-Datei, keine externen Anfragen (keine Google Fonts, kein CDN) — nur Systemschriften
- Einziges JavaScript: der Hell/Dunkel-Umschalter
- **Abschaltbar beim Checkpoint:** Config-Schalter `dashboard.bei_checkpoint` (Standard `true`) — der automatische Schritt kostet je Checkpoint einige Sekunden + einige tausend Tokens; Projekte ohne Dashboard-Nutzung schalten ihn ab. Auf Abruf funktioniert immer

**Fachlich:**
- **Datenschutz:** keine eigene Regel im Dashboard. Es zeigt nur, was ohnehin in den Artefakten steht, erzeugt keine neuen Daten, die Datei ist lokal + unversioniert und wird nirgends übertragen. Schutz gehört an die Quelle (schreibende Skills) → INBOX #110. Kein `nur_kennzahlen`-Schalter im MVP

### Integrationspunkte
- **Zwei Wege, ein Ergebnis:** `/dtb:project-dashboard` (auf Abruf, öffnet Browser) und `/dtb:workflow-checkpoint` (automatisch, ohne Browser, Pfad-Zeile). Beide nutzen dasselbe Gerüst aus dem Skill
- **Neuer Skill `dtb:project-dashboard`:** Pipeline-Stage `monitoring` (wie `pipeline-graph`), `after: workflow-checkpoint`; rein lesend bis auf das eigene HTML
- **`workflow-checkpoint`:** neuer Schritt zwischen 4 und 5 — liest den frisch geschriebenen Stand, erzeugt das HTML wenn `dashboard.bei_checkpoint` an ist; Verweis auf den Skill mit Struktur-Check (Muster `pane-start` → `worker`), keine Kopie des Gerüsts; Schritt 6 bekommt die Pfad-Zeile; Worktree → überspringen mit Hinweiszeile
- **`workflow.config.yaml`:** Block `dashboard:` mit `bei_checkpoint: true`; Fenster (5 Sessions, 10 Einträge) im MVP fest im Skill
- **`project-init`:** Skill-Liste + Config-Seed; **`CLAUDE.md`/`skills/CLAUDE.md`:** Skill-Katalog + Output Locations
- **Unverändert (nur Referenz):** `workflow-status`, `workflow-next`, `backlog-status`, `pipeline-graph`
- **Externe Abhängigkeiten:** keine — nur Browser + plattformabhängiger Öffnen-Befehl (`start` / `open` / `xdg-open`)

---

## Abhaengigkeiten

- Keine aktiven Features, keine Konflikte (Haupt-Checkout + alle Worktrees geprüft, 2026-10-26)
- `workflow-checkpoint` ist der meistgeänderte Skill (zuletzt #142, archiviert) — Einfügestelle beim Planen gegen den aktuellen Stand prüfen
- INBOX #141 (Lektionen kuratieren): erhält vom Dashboard den Auslöser „Kuratierung fällig"
- INBOX #110 (Datenschutz-Schutz): Schutz bewusst dorthin ausgelagert
- INBOX #113 (Offene Aufgaben ausdünnen): wirkt auf eine Datenquelle, nicht auf das Dashboard
- INBOX #138 / #45 (Mods / Hooks): mögliche spätere Anzeigeorte bzw. Auslöser

---

## Offene Punkte

- Ausbaustufe C (Claude schreibt nur `dashboard-data.js`, festes Gerüst liest sie ein) — falls Token-Kosten/Laufzeit beim Checkpoint spürbar werden; zugleich Vorstufe für einen Live-Server
- Projekt-eigene Design-Tokens aus `project-design/` als Override des Kit-Stils? (MVP: nein, fester Kit-Stil)
- Schwelle für „Kuratierung fällig" bei den Lektionen festlegen (z. B. ab 80 % des Soft-Limits) — in der Spec
- Abgrenzung „Zuletzt gemacht" (Session-Logs) vs. „Abgeschlossene Meilensteine" (WORKFLOW_STATUS) — Doppelung vermeiden, in der Spec klären
- Struktur-Anker im neuen Skill festlegen, den der Checkpoint-Struktur-Check greppt

---

**Erstellt mit:** `/dtb:feature-discover`
