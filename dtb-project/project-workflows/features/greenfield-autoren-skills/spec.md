# Feature: Greenfield-Autoren-Skills

**Erstellt:** 2026-07-13
**Ziel:** `greenfield-prd` und `greenfield-roadmap` werden von read-only-Reports zu Autoren-Skills, die `PRD-MVP.md`, `TECH-STACK.md` und `ROADMAP.md` im Dialog erzeugen — Greenfield-Projekte bekommen damit einen echten Einstiegspfad ins Kit.
**Prioritaet:** Hoch
**Status:** Abgenommen <!-- explizit abgenommen per Nutzer-Entscheidung 2026-07-22; Entscheidung G (echte Abnahme erst am ersten realen Greenfield-Lauf) dabei bewusst uebersprungen. Sync: dtb:workflow-checkpoint (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die beiden Greenfield-Skills sind heute tote Werkzeuge: Sie fassen Dokumente zusammen
(`PRD-MVP.md`, `ROADMAP.md`), die kein Skill je erzeugt — in keinem Zielprojekt existieren sie.
Nach dem Vorbild des 10x-3.0-Greenfield-Strangs (`10x-shape` → `10x-prd` → `10x-roadmap`) werden
beide zu Autoren: `greenfield-prd` führt ein gründliches, unterbrechbares Produkt-Interview und
generiert ein technikfreies PRD („nie erfinden → Open Questions"); `greenfield-roadmap` führt eine
schlanke Stack-Besprechung (→ `TECH-STACK.md`) plus ein Lean-Interview (max. 3 Ankerfragen) und
zerlegt das PRD in vertikale Slices mit Dependency-Reihenfolge. Die Roadmap-Slices tragen
Change-IDs, die direkt Feature-Slugs sind — die Brücke in die bestehende Change-Pipeline und
in die Derived-State-Statusableitung.

---

## Scope / Abgrenzung

### Enthalten

- **`greenfield-prd` als Autor (Zwei-Modus-Skill):**
  - `PRD-MVP.md` fehlt → gründliches, mehrphasiges Produkt-Interview (Shape-Phase integriert,
    kein eigener Skill, kein Zwischenartefakt); Ergebnis `project-strategy/PRD-MVP.md`
  - `PRD-MVP.md` existiert → bisheriger Report-Modus (zusammenfassen); Neuerzeugung nur auf
    expliziten Wunsch mit Kollisions-Dialog
  - Quellmaterial-Angebot: vorhandene `project-strategy/*.md` (docs-extract-Ergebnisse) und
    INBOX-Ideen werden eingelesen und als Interview-Input angeboten
  - „Nie erfinden"-Hard-Rule: fehlende Inhalte landen wörtlich in `## Open Questions`
  - Technical-Leak-Lint (7 Kategorien, aus Idee #5): PRD bleibt technikfrei, konstruktiver
    Redirect „gehört in TECH-STACK.md"
- **`greenfield-roadmap` als Autor:**
  - Eligibility-Gate auf `PRD-MVP.md` (Redirect `greenfield-prd`); Readiness-Check bei hohlem
    PRD (Score-Heuristik, Warnung benennt fehlende Signale, „Trotzdem fortfahren"-Escape)
  - Stack-Besprechung: `TECH-STACK.md` fehlt → kompakte geführte Besprechung (Team-Skills,
    Sprach-/Framework-Präferenzen, Avoid-List, Deployment-Ziel) → Living Doc
    `project-strategy/TECH-STACK.md`; vorhanden → sichtbare Skip-Zeile, konsumieren
  - Lean-Interview: max. 3 Ankerfragen (Hauptziel, North-Star-Slice, Top-Blocker), jede mit
    „(Recommended)"-Vorschlag aus den Artefakten; Investment-Schwerpunkte abgeleitet statt erfragt
  - Zerlegung in vertikale Slices (Foundations nur als benannte Enabler mit Unlocks) mit
    Dependency-Reihenfolge; Change-ID je Slice in kebab-case nach Slug-Regeln §4
  - Keine Zeitschätzungen (keine Kalenderwochen/Story Points/Größenklassen); Ausnahme: extern
    gesetzte Termine als Constraints (Fakten, keine Schätzungen); Ressourcen-Tabelle entfällt
  - Hand-off: genau EIN empfohlener Befehl `/dtb:feature-discover <change-id>` — kein
    Auto-Chaining, kein BACKLOG-Doppeleintrag der Slices
- **Gemeinsame Mechanik beider Skills:**
  - Selbst-Review VOR dem Schreiben (Strukturprüfung + Leak-Lint): Verstoß → Abbruch ohne
    Write, konkreter Befund (kein stilles Umschreiben)
  - Foundation-Doc-Archivkonvention im Kollisions-Schritt: Artefakt existiert → Dialog
    „Archivieren + ersetzen (Recommended) / Überschreiben / Abbrechen"; Archiv-Pfad
    `project-strategy/archive/YYYY-MM-DD-<DOC>.md` (Zweitlauf am Tag → `-2`); `archive/` lazy
    angelegt; Nicht-Git: einfacher Move genügt
  - Resume-Marker als HTML-Kommentar direkt in der Zieldatei (Interview unterbrechbar,
    Wiedereinstieg ohne Doppelfragen); Thin-Input-Warnung benennt fehlende Signale konkret
  - `disable-model-invocation: true` (schreibende Skills nicht auto-triggern)
- **Derived-State-Integration (Roadmap-Status ohne Drift):**
  - Statusspalte in `ROADMAP.md` = abgeleitete Anzeige („nicht manuell pflegen"); Ableitung
    über Change-ID = Slug: kein Ordner → Doc-Status (`proposed`/`ready`/`blocked`),
    `features/<slug>/` → in Arbeit, `archive/<slug>/` → done
  - Neuer §5 „Roadmap-Ableitung" in `DERIVED_STATE_RULES.md` (Muster §3)
  - `workflow-checkpoint` Schritt 2 synchronisiert die Spalte (nur wenn `ROADMAP.md` existiert);
    KEINE `dtb:archive`-Kopplung
- **Umfeld-Anpassungen:** Frontmatter beider Skills (`produces` echte Artefakte, Roadmap
  `next: [dtb:feature-discover]`), beidseitige Gegen-Hinweise zur Format-Kopplung
  PRD-Template ↔ Roadmap-Parser (L5-Muster), pipeline-graph-Artefaktlegende um `TECH-STACK.md`,
  README/CLAUDE.md-Skill-Beschreibungen

### Nicht enthalten

- **Stack-Auswahl per Starter-Registry + Projekt-Bootstrapping** (10x-Glieder 3+4:
  `tech-stack-selector`, `bootstrapper`) — zu schwergewichtig (Registry-Pflege), Zielprojekte
  entstehen nicht aus Starter-Templates; bei Bedarf neue INBOX-Idee (Anschlusspunkt:
  `TECH-STACK.md` existiert dann als definierter Input)
- **Eigener Shape-Skill mit Zwischenartefakt** (10x-Glied 1 als Skill) — integriert in
  `greenfield-prd`
- **`10x-init`-Pendant** — durch `dtb:project-init` abgedeckt; project-init wird NICHT umgebaut
  (höchstens kosmetische Baum-Ergänzung `project-strategy/archive/`)
- **Brownfield-Ast** (`10x-stack-assess`, `10x-health-check`) — Greenfield-Skills in
  Brownfield-Projekten: nur Hinweis, keine Verweigerung, kein Auto-Detect
- **BACKLOG-Eintrag der Roadmap-Slices** — die Roadmap ist das einzige Slice-Verzeichnis
  (zweiter Speicherort = Drift); BACKLOG füllt sich erst via feature-discover
- **kit-sync-Erweiterung um `references/`-Dateien** — Weg A (eine SKILL.md pro Skill);
  bei Budget-Bruch Folge-Idee

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Zeilenbudget ~350/Skill reicht nicht (Interview + Template + Lint + Selbst-Review) | Mittel | Mittel | Kompression ggü. Vorbild (kein Brownfield-Zweig, keine Host-Agnostik, keine Registry); beim impl-plan nachverhandeln: Budget erhöhen oder kit-sync-`references/`-Support als Folge-Idee |
| Format-Kopplung PRD-Template ↔ Roadmap-Parser bricht still bei Template-Änderung | Mittel | Hoch | Beidseitige Gegen-Hinweise (L5-Muster aus codebase-research-step); plan-review-Grounding prüft Referenzen |
| Interview-Skills erfinden plausible Inhalte statt Lücken zu zeigen | Mittel | Hoch | „Nie erfinden"-Hard-Rule + wörtliches Open-Questions-Routing + Selbst-Review-Abbruch vor Write |
| Keine reale Greenfield-Praxiserprobung verfügbar (kein aktives Greenfield-Zielprojekt) | Mittel | Mittel | Fixture-Projekt + ggf. reales Mini-Projekt; L5 beachten: Fixtures verstecken Ambiguitäten — Abnahme braucht mindestens einen echten Kontext |
| `workflow-checkpoint`-Erweiterung (ROADMAP-Sync) bläht den Checkpoint auf | Niedrig | Mittel | Minimal-invasiv: nur wenn `ROADMAP.md` existiert; gleiche Mechanik wie BACKLOG-Spalte |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine harten — `codebase-research-step` (wartet auf Abnahme) fasst andere Dateien an; kein Konflikt

### Referenz-Dokumente

- `features/greenfield-autoren-skills/discovery.md` - vollständige Discovery mit allen Entscheidungen (2026-07-13)
- `C:/Users/SpyraD/Desktop/Projekte/10x-devs-3.0/.claude/skills/10x-{shape,prd,tech-stack-selector,roadmap}/SKILL.md` - Konzeptions-Vorbilder (nur Referenz, keine Laufzeit-Abhängigkeit)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - §3 (Anzeige-Muster), §4 (Slug-Regeln); bekommt neuen §5
- `skills/CLAUDE.md` - Frontmatter-/Gate-/Sprach-Konventionen
- `dtb-project/project-rules/lessons.md` - L5 (Fixtures verstecken Trigger-Ambiguitäten)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [x] SC1: `greenfield-prd` ohne vorhandenes `PRD-MVP.md` führt das mehrphasige Interview (mit Resume-Marker, unterbrech- und wiederaufnehmbar ohne Doppelfragen) und erzeugt ein `PRD-MVP.md`, in dem fehlende Inhalte als `## Open Questions` stehen statt erfunden zu sein — **Beleg:** Blindlauf fx-a: Autoren-Modus, Resume-Marker `a…f…done`, NFRs/Abhängigkeiten/Risiken als nummerierte Open Questions (nichts erfunden)
- [x] SC2: `greenfield-prd` mit vorhandenem `PRD-MVP.md` liefert den Report-Modus; Neuerzeugung nur auf expliziten Wunsch und dann mit Kollisions-Dialog inkl. Archivierung nach `project-strategy/archive/YYYY-MM-DD-PRD-MVP.md` (Zweitlauf → `-2`) — **Beleg:** Blindlauf fx-b: Report-Modus wegen Marker `done`; bei Neuerzeugungs-Wunsch Kollisions-Dialog, Ziel `…/archive/2026-07-13-PRD-MVP.md`, kein stilles Überschreiben
- [x] SC3: Das PRD-Interview bietet vorhandene `project-strategy/*.md` und INBOX-Ideen als Quellmaterial an; das erzeugte PRD besteht den Technical-Leak-Lint (technikfreie Probe), technische Nennungen werden nach `TECH-STACK.md` umgeleitet — **Beleg:** Blindlauf fx-a: MARKTANALYSE.md + INBOX #1/#2 angeboten; React/PostgreSQL nicht im PRD (Leak-Lint sauber, Redirect)
- [x] SC4: `greenfield-roadmap` ohne `PRD-MVP.md` blockt mit Redirect auf `greenfield-prd` (Gate-Muster inkl. Escape-Hatch); mit hohlem PRD warnt der Readiness-Check unter Nennung der fehlenden Signale und erlaubt „Trotzdem fortfahren" — **Beleg:** Blindläufe fx-d (Hard-Gate + Redirect + Escape, kein Write) und fx-e (Readiness 0/4, fehlende Signale konkret benannt, kein Write)
- [x] SC5: Fehlt `TECH-STACK.md`, führt die Roadmap die kompakte Stack-Besprechung und schreibt das Living Doc; existiert es, erscheint eine sichtbare Skip-Zeile und es wird konsumiert — **Beleg:** Blindläufe fx-g (Besprechung → TECH-STACK.md geschrieben) und fx-f (Skip-Zeile, Datei byte-identisch unverändert)
- [x] SC6: Die erzeugte `ROADMAP.md` enthält vertikale Slices in Dependency-Reihenfolge mit §4-konformen Change-IDs, ohne Zeitschätzungen (externe Termine als Constraints erlaubt); das Lean-Interview stellt höchstens 3 Ankerfragen, jede mit „(Recommended)"-Option; Hand-off ist genau ein empfohlener `/dtb:feature-discover <change-id>`-Befehl — **Beleg:** Blindlauf fx-g: 3 Ankerfragen je (Recommended), 3 Slices + 2 Foundations mit kebab-case-Change-IDs, keine Zeitschätzung, genau ein Hand-off `/dtb:feature-discover angebot-erstellen`
- [x] SC7: Selbst-Review vor dem Schreiben bricht bei Struktur- oder Lint-Verstoß ab, ohne zu schreiben, und meldet den konkreten Befund (Negativ-Test mit präpariertem Verstoß) — **Beleg:** Blindlauf fx-h: 3 Leaks (PostgreSQL/REST/React) gemeldet, Write abgebrochen, keine Datei geschrieben
- [x] SC8: `DERIVED_STATE_RULES.md` §5 definiert die Roadmap-Ableitung (Change-ID = Slug); `workflow-checkpoint` synchronisiert die als abgeleitete Anzeige markierte Statusspalte, ein abgeschlossener Change (`archive/<slug>/`) erscheint nach dem nächsten Checkpoint als `done` — **Beleg:** Blindlauf fx-i: Spalte synchronisiert `features/`→in-progress, `archive/`→done, kein Ordner→Doc-Status `ready`
- [x] SC9: Beide SKILL.md ≤ ~350 Zeilen, `disable-model-invocation: true`, `produces` korrekt befüllt; pipeline-graph-Legende kennt `TECH-STACK.md`; beidseitige Gegen-Hinweise zur Format-Kopplung vorhanden; README/CLAUDE.md-Beschreibungen aktualisiert — **Beleg:** statische Prüfung 4.2: prd 208 Z. / roadmap 193 Z., Frontmatter korrekt, Gegen-Hinweise beidseitig (Grep), Legende + README/CLAUDE.md aktualisiert

---

## Offene Punkte

- ~~Womit praxiserproben?~~ Entschieden (plan-review 2026-07-13, Entscheidung G): **zweistufige Abnahme** — Fixtures bringen das Feature auf „Fertig zum Testen"; die echte Abnahme (L5) erfolgt erst beim ersten realen Greenfield-Vorhaben
- ~~PRD-Interview-Kategorien~~ Entschieden (impl-plan, Entscheidung B): 6 Kategorien ans Template gespiegelt
- ~~Readiness-Score-Heuristik~~ Entschieden (impl-plan, Entscheidung C): 4 Signale à 1 Punkt, Schwelle ≥3

---

**Erstellt mit:** `/dtb:feature-plan`
