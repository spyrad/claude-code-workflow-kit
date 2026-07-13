# Discovery: Greenfield-Autoren-Skills
<!-- resume: done -->

**Erstellt:** 2026-07-13
**Idee-Referenz:** Inbox #11 — "Greenfield-Strang (`greenfield-prd` + `greenfield-roadmap`) nach 10x-3.0 neu konzipieren: aktuell reine Lese-/Übersichts-Werkzeuge (read-only, `produces: []`) — Vorbild 10x-prd/10x-roadmap sind echte Autoren-Skills, die PRD/Roadmap generieren. Umfasst ggf. Write-Fähigkeit, Technical-Leak-Lint + „nie erfinden → Open Questions" (aus Idee #5, dort bewusst ausgeklammert)."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-greenfield-prd/SKILL.md` (198 Z.) | Kernobjekt: read-only-Zusammenfasser → Autoren-Skill (Interview + Generator für PRD-MVP.md). Funde: verschachtelte Code-Fences im Template, `disable-model-invocation: false`, `produces: []` |
| `skills/dtb-greenfield-roadmap/SKILL.md` (235 Z.) | Kernobjekt: read-only-Übersicht → Autoren-Skill (ROADMAP.md generieren) + geführte Stack-Besprechung → TECH-STACK.md. Fund: kein Fallback bei fehlender ROADMAP.md. Slices/Foundations/Selbst-Review aus skill-10x Block 3 werden Autoren-Template |
| `skills/dtb-pipeline-graph/SKILL.md` | Artefakt-Legende (PRD-MVP.md/ROADMAP.md, neu: TECH-STACK.md); liest `produces` aus Frontmatter — ändert sich von `[]` auf echte Artefakte |
| `skills/dtb-workflow-status/SKILL.md` | Liest Pipeline-Frontmatter für Flow-Visualisierung (stage `greenfield`, `after`/`next`-Kette) |
| `skills/dtb-project-health/SKILL.md` | UPPER_SNAKE_CASE-Check auf `project-strategy/` (greift nur direkt, nicht in `archive/`-Unterordner) — neue Artefakte TECH-STACK.md konform |
| `skills/dtb-docs-extract/SKILL.md` | Schreibt ebenfalls nach `project-strategy/` (aus `input/`-Dropzone) — Abgrenzung: Dropzone-Dokumente als Quellmaterial für PRD-Interview? |
| `skills/CLAUDE.md` | Konventionen: Frontmatter-Pflichtfelder, Eligibility-Gate-Zuordnung (Roadmap-Gate auf PRD-MVP.md?), Sprach-/Format-Regeln |
| `README.md` + `CLAUDE.md` (Root) | Skill-Beschreibungen aktualisieren (README verspricht heute Autoren-Verhalten, das die Skills nicht haben) |
| Extern: `10x-devs-3.0/.claude/skills/10x-{shape,prd,tech-stack-selector,roadmap}/SKILL.md` | Vorbilder (Shape-Interview, Generator-Disziplin „nie erfinden", Lean-Interview max. 3 Ankerfragen, vertikale Slices, Technical-Leak-Lint 7 Kategorien) |

---

## Anforderungen

### Scope

**Enthalten (3a, entschieden 2026-07-13):**
- **10x-Kettenglieder 1+2+5 übernehmen, 0+3+4 bewusst nicht** (Grobprüfung aller 6 Glieder):
  - Glied 0 `10x-init`: abgedeckt durch `dtb:project-init` — nicht übernehmen
  - Glied 1 `10x-shape` (Discovery-Interview): **integriert** als Interview-Phase in `greenfield-prd` (kein eigener Skill, kein Zwischenartefakt shape-notes.md — Nutzen erst bei Team-Arbeitsteilung)
  - Glied 2 `10x-prd`: `greenfield-prd` wird Autor von `project-strategy/PRD-MVP.md`
  - Glied 3 `10x-tech-stack-selector`: **nicht übernehmen** (Starter-Registry + Bootstrapper-Hand-off zu schwergewichtig) — stattdessen schlanke geführte Stack-Besprechung (Team-Skills, Sprach-/Framework-Präferenzen, Avoid-List, Deployment-Ziel) als Schritt in `greenfield-roadmap`, Ergebnis als Living Doc `project-strategy/TECH-STACK.md` (vorhanden → konsumieren, fehlt → Besprechung) — **Zuschnitt 1, Nutzer-Entscheidung**
  - Glied 4 `10x-bootstrapper`: **nicht übernehmen** (Projekt-Scaffolding passiert außerhalb des Kits)
  - Glied 5 `10x-roadmap`: `greenfield-roadmap` wird Autor von `project-strategy/ROADMAP.md`
- **Zwei-Modus-Design:** heutiger Lese-/Report-Modus bleibt als Zweitmodus (Artefakt existiert → zusammenfassen; fehlt → Autoren-Interview)
- **Foundation-Doc-Archivkonvention** in den Kollisions-Schritten beider Autoren-Skills (kein project-init-Umbau): Artefakt existiert bei Neuerzeugung → Dialog „Archivieren + ersetzen (Recommended) / Überschreiben / Abbrechen"; Archiv-Pfad `project-strategy/archive/YYYY-MM-DD-<DOC>.md` (Zweitlauf am selben Tag → `-2`-Suffix); `archive/`-Ordner lazy anlegen
- **Technical-Leak-Lint + „nie erfinden → Open Questions"** (aus Idee #5 hierher verschoben): PRD bleibt technikfrei, konstruktiver Redirect „gehört in TECH-STACK.md"
- **Die 3 SKILL_10X-Funde:** Code-Fences + ROADMAP.md-Fallback erledigen sich beim Neuschreiben; beide Skills auf `disable-model-invocation: true` (schreibende Skills dürfen nicht auto-getriggert werden)

**Nicht enthalten:**
- Stack-Auswahl per Starter-Registry / Projekt-Bootstrapping (10x-Glieder 3+4) — bei Bedarf neue INBOX-Idee
- Brownfield-Ast (`10x-stack-assess`, `10x-health-check`)
- Umbau `dtb:project-init` (project-strategy/ existiert; höchstens kosmetisch Baum-Diagramm um `archive/` ergänzen)
- [weitere Abgrenzungen aus 3b-3e folgen]

### Gewuenschtes Verhalten
- **PRD-Interview gründlich** (mehrphasig wie 10x-shape/feature-discover: Vision/Problem, Persona, User Stories, Business-Logik, Scope-Abgrenzung); **Roadmap-Interview lean** (max. 3 Ankerfragen mit starkem Recommend aus Artefakten, Investment-Areas abgeleitet statt erfragt; Stack-Besprechung ebenfalls kompakt geführt)
- **Alle UX-Muster übernehmen:**
  - Resume-Marker als HTML-Kommentar (Interview unterbrechbar, Wiedereinstieg ohne Doppelfragen — beim mehrphasigen PRD-Interview Pflicht)
  - „(Recommended)"-Muster an echten Auswahlpunkten
  - Sichtbare Skip-Zeilen bei übersprungenen Modi (z.B. „📂 TECH-STACK.md vorhanden → Besprechung übersprungen")
  - Thin-Input-Warnung: bei dünnem Input konkret benennen, welches Signal fehlt und mit welcher Konsequenz (nie generisch)
  - Selbst-Review mit Abbruch VOR dem Schreiben (Struktur-Check + Technical-Leak-Lint; bei Verstoß nicht schreiben, Befund melden)
  - Kein Auto-Chaining: Hand-off als Empfehlung („Nächster Schritt: …"), nie automatische Skill-Invokation

### Randfaelle
- **Fehler:**
  - Selbst-Review-Fail (Struktur oder Leak-Lint) → Abbruch OHNE Schreiben, Befund konkret melden (kein stilles Umschreiben)
  - Nicht-Git-Projekt (Referenz-Testbett dtb-assistant): Archivkonvention nutzt einfachen Filesystem-Move — das Archiv IST die Sicherung, kein zusätzliches Backup-Muster
  - Abbruch mitten im PRD-Interview: Entwurf mit Resume-Marker (HTML-Kommentar) direkt in die Zieldatei `PRD-MVP.md` schreiben (wie feature-discover); Wiedereinstieg ohne Doppelfragen
- **Leere Daten / Grenzwerte:**
  - `greenfield-roadmap` ohne `PRD-MVP.md` → Eligibility-Gate mit Redirect auf `greenfield-prd` (Standard-Gate-Muster, ersetzt den fehlenden Fallback aus dem SKILL_10X-Fund)
  - PRD existiert, aber hohl (viele `# TODO`/Open Questions) → Readiness-Check mit Score-Heuristik, Warnung benennt fehlende Signale + Konsequenz, „Trotzdem fortfahren"-Escape
  - PRD-Interview liefert wenig (User weiß noch nicht viel) → gültiges dünnes PRD mit großem `## Open Questions`, KEIN Abbruch (Lücken sichtbar machen statt verweigern)
- **Bekannte Edge Cases:**
  - Regeneration am selben Tag → Archiv-Suffix `-2`, `-3`, …
  - Greenfield-Skills in Brownfield-Projekt aufgerufen → kurzer Hinweis („für die Aufbauphase gedacht"), keine Verweigerung, kein Auto-Detect (10x-Brownfield-Ast bewusst nicht übernommen)

### Einschraenkungen
- **Ein-Datei-Zwang + Zeilenbudget (Weg A):** kit-sync erfasst nur `skills/dtb-*/SKILL.md` — keine `references/`-Zusatzdateien (würden nicht verteilt/drift-geprüft). Alles in je einer SKILL.md, Budget ~350 Zeilen pro Skill (Kompression: kein Brownfield-Zweig, keine Host-Agnostik, keine Registry, Template inline). **Risiko für die Spec:** Passt das gründliche Interview + Template + Lint + Selbst-Review nicht in ~350 Z., beim impl-plan nachverhandeln (Budget erhöhen oder kit-sync-`references/`-Support als Folge-Idee)
- **Format-Kopplung PRD ↔ Roadmap:** greenfield-roadmap parst Sektionen aus PRD-MVP.md (Readiness-Check, Slice-Ableitung) → beidseitige Gegen-Hinweise (Muster codebase-research-step, L5): PRD-Template nennt den Parser, Roadmap-Skill nennt das Template
- **Sprache:** Generierte Artefakte auf Deutsch; technische Bezeichner englisch (Statuswerte `proposed`/`ready`/`blocked`/`done`, IDs `S-NN`/`F-NN`, Frontmatter-Keys)
- **Keine Zeitschätzungen (10x-Prinzip), mit Ausnahme:** keine Kalenderdaten/Wochen/Story Points/Größenklassen auf Slice-Ebene — Reihenfolge steckt im Dependency-Graph (Prerequisites), Tempo in Blockern/Unknowns. Ressourcen-/Kapazitätstabelle entfällt. **Ausnahme:** extern gesetzte Termine als Constraints erlaubt (z.B. „Pilot-Demo Fachbereich 2026-09-01") — Fakten, keine Schätzungen
- **Roadmap-Status Derived-State-konform (revidiert nach Drift-Einwand des Nutzers):** Jedes Roadmap-Item trägt eine Change-ID in kebab-case = Feature-Slug. Status-Spalte in ROADMAP.md ist abgeleitete Anzeige („nicht manuell pflegen"): weder `features/<slug>/` noch `archive/<slug>/` → Doc-Status gilt (`proposed`/`ready`/`blocked`); `features/<slug>/` mit Progress → in Arbeit; `archive/<slug>/` → done. Lesende Läufe (Report-Modus) leiten ab + melden Konflikte (Artefakt gewinnt); Sync durch `dtb:workflow-checkpoint` (wie BACKLOG-Spalte, KEINE dtb:archive-Kopplung); neuer Absatz in DERIVED_STATE_RULES.md (§ Roadmap-Ableitung)

### Integrationspunkte

Gegen Code verifiziert (2026-07-13):

- **`workflow-checkpoint` Schritt 2** („Status ableiten & Anzeige-Felder synchronisieren") ist die Sync-Stelle für die ROADMAP.md-Statusspalte (nur wenn Datei existiert); Frontmatter `consumes`/`produces` um ROADMAP.md erweitern
- **DERIVED_STATE_RULES.md:** neuer §5 „Roadmap-Ableitung" nach dem Muster von §3 (Statusspalte = abgeleitete Anzeige): Change-ID→Slug-Mapping + Ableitungstabelle (kein Ordner → Doc-Status gilt; `features/<slug>/` → in Arbeit; `archive/<slug>/` → done)
- **Slug-Regeln §4:** Roadmap-Change-IDs werden §4-konform vergeben (deterministisch, kebab-case, Kollision → Abbruch) — Change-ID = künftiger Feature-Slug ist die Brücke für Statusableitung UND Hand-off
- **Brücke Roadmap → Change-Pipeline:** Hand-off = genau EIN empfohlener Befehl `/dtb:feature-discover <change-id>` (10x-Muster „Your next move"). **Kein BACKLOG-Doppeleintrag** (zweiter Speicherort = Drift, Argument wie Idee #13); Lese-Skills scannen nur `features/*/` + BACKLOG/INBOX → von der Roadmap unberührt, keine Änderung nötig
- **`docs-extract` als Zulieferer:** PRD-Interview liest vorhandene extrahierte Strategie-MDs (`project-strategy/*.md` außer PRD/ROADMAP/TECH-STACK) + INBOX-Ideen ein und bietet sie als Quellmaterial an
- **`pipeline-graph`:** Artefakt-Legende um TECH-STACK.md ergänzen; `produces` beider Skills von `[]` auf echte Artefakte; Roadmap-Frontmatter `next: [dtb:feature-discover]` → Graph zeigt die Brücke Greenfield → Change-Pipeline
- **Externe Abhängigkeiten:** keine — 10x-Repo ist reine Konzeptions-Referenz, zur Laufzeit nichts gebraucht

---

## Abhaengigkeiten

- **Bestehende Changes:** 1 — `codebase-research-step` (Fertig zum Testen, wartet auf Abnahme). Kein Konflikt: änderte `dtb-impl-plan` + `dtb-feature-discover`, #11 fasst andere Dateien an (nur `next:`-Verweis auf feature-discover in Roadmap-Frontmatter, kein Edit dort)
- **Überschneidungen (ideell, kollisionsfrei):** Archiv `spec-haertung` (Technical-Leak-Lint wurde dort bewusst zu #11 verschoben — hier eingelöst); Archiv `skill-10x-optimierungen` Block 3 (Slices/Foundations/Selbst-Review in greenfield-roadmap werden zum Autoren-Template weiterentwickelt)

---

## Offene Punkte

- **Zeilenbudget-Risiko (Weg A):** Passt gründliches Interview + Template + Leak-Lint + Selbst-Review nicht in ~350 Z. pro SKILL.md → beim impl-plan nachverhandeln (Budget erhöhen oder kit-sync-`references/`-Support als Folge-Idee)
- **Praxiserprobung:** Kein aktives Greenfield-Zielprojekt benannt — Abnahme vermutlich über Fixture-Projekt + ggf. ein reales neues Mini-Projekt; bei Spec/Testplan klären
- **PRD-Interview-Kategorien final festlegen** (gründlich, Orientierung an 10x-shape: Vision/Problem, Persona, User Stories, Business-Logik, Scope-Abgrenzung, Success Criteria) — Detail-Zuschnitt in der Spec

---

**Erstellt mit:** `/dtb:feature-discover`
