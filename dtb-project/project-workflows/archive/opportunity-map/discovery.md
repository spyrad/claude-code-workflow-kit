# Discovery: Opportunity-Map (build/buy/complement/wait-Sichtung)
<!-- resume: done -->

**Erstellt:** 2026-07-14
**Idee-Referenz:** Inbox #17 — "`10x-opportunity-map`-Pendant bauen: Skill, der wiederkehrende Reibung/unerfüllten Bedarf in ein Entscheidungs-Artefakt überführt — build vs. buy vs. complement vs. wait"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-opportunity-map/SKILL.md` | **NEU** — der eigenständige Vorfeld-Skill (Signal-Erhebung → 4-Wege-Klassifikation → 1 Kandidat → Artefakt) |
| `skills/dtb-greenfield-prd/SKILL.md` | Aktiver Eingangs-Nudge (Mini-Touch, **isolierter letzter Umsetzungsschritt**); berührt das noch nicht abgenommene Greenfield-Feature |
| `dtb-project/project-strategy/` | Zielort des Artefakts `OPPORTUNITY-MAP.md`; wird von greenfield-prds Quellmaterial-Glob (`project-strategy/*.md`) automatisch aufgegriffen |
| `skills/dtb-pipeline-graph/SKILL.md` | Artefakt-Legende um `OPPORTUNITY-MAP.md` + neuer Skill über `stage`/`next`-Frontmatter im Flow |
| `skills/dtb-kit-sync/SKILL.md` | Neuer class-A-Skill → in den globalen Sync-Umfang + Lock aufnehmen |
| `README.md` + `CLAUDE.md` (Root) | Skill-Katalog: neuer Skill + Kategorie-Einordnung (Greenfield-Vorfeld) |
| `skills/CLAUDE.md` | Frontmatter-Pflichtfelder/Konventionen für den neuen Skill; ggf. Nudge-Konvention |

> **Nicht betroffen (bewusst):** `DERIVED_STATE_RULES.md` — die Map ist ein Vorfeld-Strategie-Artefakt
> (wie `PRD-MVP.md`), kein Change mit `## Progress`. Keine Statusableitung nötig.

---

## Anforderungen

### Scope

**Enthalten:**
- Eigenständiger Skill `dtb-opportunity-map` als **grobe Vorfeld-Trade-off-Sichtung** (nicht Detail-Fit gegen ein fertiges PRD)
- Eigene schlanke Signal-Erhebung: wiederkehrende Reibung/unerfüllter Bedarf normalisieren (Kern-Schmerz + grobe Must-Haves)
- 4-Wege-Klassifikation je Signal: **build / buy / complement / wait**
- Genau **1 empfohlener Kandidat** + dünne, read-only Erstversion (Reads/Returns/Does-not-do)
- Artefakt `project-strategy/OPPORTUNITY-MAP.md` (Vergleichstabelle + Kandidat + Begründung + Richtung)
- Hand-off: bei „build" → `/dtb:greenfield-prd`; „buy/complement" → Handlungshinweis (welche Produkte gegen Must-Haves prüfen); „wait" → Map speichern & später. Kein Auto-Chaining
- Aktiver **Eingangs-Nudge** in `greenfield-prd` (Autoren-Modus, wenn keine Map existiert): einmaliger Hinweis „build/buy geklärt? → opportunity-map erwägen — Weiter/Abbrechen"

**Nicht enthalten:**
- Kein Implementierungsplan / kein Code / kein SDK-/CI-/Deployment-Output (reine Entscheidungshilfe)
- **Kein Detail-Fit** (erfüllt Produkt X genau meine N Anforderungen) — das setzt ein PRD voraus und ist bewusst ausgeklammert
- Kein Umbau der Greenfield-Kette (shape bleibt in `greenfield-prd` integriert — Variante A, nicht die shape-Rauslösung)
- Keine `DERIVED_STATE_RULES.md`-Erweiterung, kein abgeleiteter Status
- Kein Hard-Gate in greenfield-prd (nur Nudge)

### Gewünschtes Verhalten
- **Trigger:** rein manuell (`/dtb:opportunity-map`) + aktiver Eingangs-Nudge aus greenfield-prd; kein Auto-Invoke (`disable-model-invocation: true`)
- **Input-Quellen:** liest `project-strategy/*.md` + INBOX-Ideen und bietet sie als Signale an; zusätzlich Freitext für undokumentierte Reibung
- **Interaktionsstil (10x-Vorbild):** Signal-für-Signal als Block (keine breite Tabelle mitten im Gespräch); Daten-Risiko früh per Auswahlfrage (mock/lokal vs. echte Firmendaten); am Ende kompakte Vergleichstabelle ins Artefakt
- **Marktkenntnis:** Live-**Websuche primär** (maximale Aktualität), **Fallback Modellwissen** wenn WebSearch nicht verfügbar; „nie erfinden" — Funde kennzeichnen, Unsicherheit benennen
- Selbst-Review vor dem Schreiben; Verstoß/leere Basis → Abbruch ohne Write
- Deutsch (Kit-Konvention; Vorbild ist englisch)

### Randfälle
- Kein/leeres Signal oder Abbruch → kein Artefakt schreiben
- Kein Kandidat qualifiziert sich → „no build / bestehendes Tool nutzen" ist ein **gültiges** Ergebnis, kein Fehler
- `OPPORTUNITY-MAP.md` existiert bereits → Kollisions-Dialog analog greenfield (Archivieren+ersetzen / Überschreiben / Abbrechen) — Detail final in spec
- Skill in Brownfield/Nicht-Greenfield-Kontext → funktioniert trotzdem (build/buy nicht Greenfield-gebunden); greenfield-prd-Hand-off nur wenn Greenfield sinnvoll
- „Baut mir ein Dashboard/Agent" → als vorgeschlagene Lösung behandeln, nicht als Schmerzsignal; nach dem echten Schmerz fragen (Guardrail)

### Einschränkungen
- Technisch: reiner Dialog-/Schreib-Skill; `allowed-tools` inkl. `WebSearch` (+ ggf. `WebFetch`); Zeilenbudget ~350; WebSearch-Verfügbarkeit variiert (Fallback nötig)
- Fachlich: Guardrails aus dem Vorbild — keine Marktprodukte/Preise erfinden, keine Outcomes versprechen (Karriere/Umsatz), Daten-Risiko früh eskalieren, essenzielle vs. akzidentelle Komplexität prüfen

### Integrationspunkte
- **`greenfield-prd`** (Eingangs-Nudge, isolierter letzter Schritt) — betroffenes wartendes Feature
- **`project-strategy/OPPORTUNITY-MAP.md`** → Quellmaterial-Brücke zu greenfield-prd (SC3-Mechanismus des Greenfield-Features)
- `pipeline-graph`, `kit-sync`, `README`/`CLAUDE.md`, `skills/CLAUDE.md` (Umfeld)
- **#16 mom-test** — konzeptioneller Nachbar (map = *ob* bauen; mom-test = *ob Problem echt*); **keine harte Abhängigkeit** (noch nicht gebaut)
- Externe Abhängigkeit: Websuche-Fähigkeit des Hosts (mit Modellwissen-Fallback)

---

## Abhängigkeiten

- **`greenfield-autoren-skills`** (Status: Fertig zum Testen, wartet auf reale Abnahme): **Überschneidung** über den Eingangs-Nudge in `greenfield-prd`. Bewusst als **isolierter, additiver letzter Umsetzungsschritt** geplant (berührt SC1–3 nicht); im Session-Log zu vermerken, dass greenfield-prd mitangefasst wurde. Der reale Greenfield-Abnahme-Lauf würde dann die volle Kette Nudge → opportunity-map → greenfield-prd testen.
- Keine harten Blocker.

### Referenz-Dokumente
- `C:/Users/SpyraD/Desktop/Projekte/10x-devs-3.0/.claude/skills/10x-opportunity-map/SKILL.md` — Konzeptions-Vorbild (Signale normalisieren, 4-Wege-Klassifikation, 1 Kandidat, Artefakt-Shape); nur Referenz
- `skills/dtb-greenfield-prd/SKILL.md` — Quellmaterial-Mechanismus (SC3), Kollisions-/Selbst-Review-Muster, Frontmatter-Vorbild
- `skills/CLAUDE.md` — Frontmatter-/Gate-/Sprach-Konventionen

---

## Offene Punkte

- **Verifikationsstrategie bei Live-Websuche:** blinde deterministische Fixtures allein unzureichend (Nicht-Determinismus) → Marktrecherche-Teil gemockt/separat prüfen; Mechanik-Fixtures für Klassifikation/Selbst-Review/Nudge bleiben möglich. → in `impl-plan` klären
- **Kollisions-Verhalten** des Artefakts: Kollisions-Dialog (wie greenfield) vs. edit-in-place Living-Doc — Vorschlag Dialog; final in `spec.md`
- **Genaue Nudge-Formulierung + Platzierung** in greenfield-prd (welcher Zweig der Modus-Weiche); + kit-sync-Drift/SC9-Zeilenzahl beachten
- **Artefakt-Dateiname:** `OPPORTUNITY-MAP.md` (analog `PRD-MVP.md`/`TECH-STACK.md`, UPPERCASE-mit-Bindestrich) — vs. project-health-Erwartung prüfen
- **WebSearch-Fallback-Verhalten** exakt spezifizieren (wann degradieren, wie kennzeichnen)

---

**Erstellt mit:** `/dtb:feature-discover`
