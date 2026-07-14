# Discovery: Codebase-Research-Step
<!-- resume: done -->

**Erstellt:** 2026-07-13
**Idee-Referenz:** Inbox #14 — "Codebase-Research-Step in `impl-plan`/`feature-plan` verankern (Vorbild 10x): angeleiteter Ist-Analyse-Schritt (Spec→Ist-Code-Abgleich) vor der Schrittplanung"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-impl-plan/SKILL.md` | Hauptziel: neuer angeleiteter Research-Schritt zwischen "Spec lesen" (2) und "Spec analysieren" (4); Eligibility-Gate + Lektionen-Prior als Vorbild für Eingangs-Schritte; ggf. `consumes:` um `features/*/discovery.md` erweitern |
| `skills/dtb-feature-plan/SKILL.md` | NICHT Ziel (3a-Entscheidung: nur impl-plan); bleibt unverändert |
| `skills/dtb-feature-discover/SKILL.md` | Redundanz-Quelle: Schritt 2 "Codebase-Scan" erzeugt `## Betroffene Module` in discovery.md — neuer Schritt läuft nur, wenn discovery.md fehlt oder veraltet ist |
| `skills/dtb-plan-review/SKILL.md` | Abgrenzung, unverändert: Schritt 2d "Grounding" verifiziert nachgelagert; neuer Schritt liefert vorgelagert das Material |

**Randnotiz:** impl-plan ist Klasse-A-Artefakt → Änderung erfordert `kit-sync` (globale Kopie `8bd3ee2c` im Lock).

---

## Anforderungen

### Scope
**Enthalten:**
- Angeleiteter Codebase-Research-Schritt in `dtb:impl-plan` (NUR impl-plan, nicht feature-plan)
- Vor der Schrittplanung: Ist-Code der betroffenen Module per Glob/Grep analysieren und mit der Spec abgleichen (Spec→Ist-Abgleich), damit Plan-Schritte auf realen Dateien/Strukturen fußen statt auf Annahmen
- Bedingt: Schritt läuft nur, wenn `discovery.md` fehlt ODER veraltet ist (Redundanz zu feature-discover Schritt 2 vermeiden)

**Nicht enthalten:**
- Kein zweites Grounding — nachgelagerte Verifikation bleibt bei plan-review Schritt 2d
- Kein Ersatz für feature-discover Schritt 2 (Codebase-Scan bleibt dort)
- Keine Änderungen am Code selbst (read-only Analyse)
- Keine Änderung an `feature-plan` (3a-Entscheidung)

### Gewuenschtes Verhalten
- **Zwischenausgabe + Bestätigung** (nicht still): Scan-Ergebnis wird als kompakte Tabelle gezeigt,
  User bestätigt/korrigiert, BEVOR es Planungsgrundlage wird. Begründung: Der Schritt läuft nur,
  wenn discovery.md fehlt/veraltet ist — also genau dann, wenn keine menschlich bestätigte
  Modul-Liste existiert; die Bestätigung holt das nach
- **UX-Muster = feature-discover Schritt 2 wiederverwendet:** `Codebase-Scan: {N} potenziell
  betroffene Dateien/Module` + Tabelle `| # | Pfad | Relevanz |` + „Stimmt das so? Fehlt etwas
  oder ist etwas irrelevant?" — gleiche Situation, gleiches Muster
- **Relevanz-Spalte trägt den Spec→Ist-Abgleich:** nicht nur welche Datei, sondern was dort im
  Ist-Code vorgefunden wurde
- **Ergebnis-Verankerung im Plan:** bestätigte Liste wird als kompakter Abschnitt (z.B.
  `## Ist-Analyse`) in plan.md dokumentiert → prüfbares Material für plan-review-Grounding,
  Leser sieht worauf der Plan fußt

### Randfaelle
- **Ein mechanisches Auslöse-Kriterium statt vier Sonderfälle:** Der Research-Schritt läuft,
  wenn KEINE verwertbare Modul-Liste existiert. Verwertbar = `discovery.md` vorhanden UND
  `## Betroffene Module` vorhanden UND ≥1 Pfad-Zeile UND Stichproben-Verifikation bestanden.
  Damit kollabieren „fehlt", „leer", „kaputt", „veraltet" in eine Regel
- **„Veraltet"-Kriterium = Stichproben-Verifikation (A):** Existenz der gelisteten Pfade per
  Glob prüfen; Zusatzregel: ≥1 gelisteter Pfad fehlt → veraltet → Scan läuft. Bewusst KEIN
  Zeitvergleich (mtime/git log): Non-Git-unzuverlässig + False-Positive-Lawine
- **0 Treffer → Dialog, nie stumm weiterplanen:** „Codebase-Scan: 0 Treffer" + aktive Frage
  nach den Modulen. Zwei legitime Ausgänge: (1) User nennt Pfade → Kurz-Verifikation per Glob →
  bestätigte Liste; (2) „komplett neu (Greenfield-Anteil)" → `## Ist-Analyse` sagt explizit
  „keine betroffenen Bestandsmodule (Neubau)"
- **Abgebrochene Discovery (Resume-Marker ≠ done) mit Modul-Tabelle:** Tabelle zählt, wenn
  verifizierbar (wurde in feature-discover Schritt 2 vom User bestätigt, bevor die Fragen begannen)
- **Treffer-Kappung bei ~15 Zeilen**, priorisiert (direkte Modul-Treffer vor Streu-Treffern in
  Doku/Tests); Kappung IMMER explizit ausweisen („+ N weitere Treffer nicht gelistet"), nie still.
  Nachfordern im Bestätigungsdialog möglich. Hinweis-Satz im Skill: viele Treffer = Schlüsselwörter
  zu generisch → schärfer nachscannen statt abkippen (keine harte Mechanik)

### Einschraenkungen
**Technisch:**
- Kein neues Tool: `impl-plan` hat bereits `Read, Glob, Grep, Write` — Schritt nutzt nur
  Vorhandenes (read-only Analyse, Write nur für plan.md wie bisher)
- Skill bleibt schlank: impl-plan aktuell 219 Zeilen, neuer Schritt ca. +30–40 Zeilen,
  deutlich unter 500; kompakt-deterministisch formulieren (Vorbild Eligibility-Gate)
- Eingangs-Reihenfolge: Lektionen-Prior → Eligibility-Gate → Research-Schritt → Spec-Analyse
  (Gate muss vorher greifen: ohne Spec kein Spec→Ist-Abgleich)
- Frontmatter-Konsistenz: `consumes:` um `features/*/discovery.md` erweitern
  (pipeline-graph + workflow-status lesen das)
- plan.md-Budget: `## Ist-Analyse` zählt gegen die 500-Zeilen-Grenze → kompakt (Tabelle,
  keine Prosa); DERIVED_STATE_RULES unberührt — Ist-Analyse ist Zusatz-Info, keine Status-Quelle
- Klasse-A-Verteilung: Änderung erfordert `kit-sync` (Lock `8bd3ee2c`)
- Projekt-agnostisch: funktioniert in jedem Zielprojekt (Pfade aus `workflow.config.yaml`,
  kein Git vorausgesetzt — deckt sich mit Verzicht auf Zeitvergleich)

**Fachlich:**
- Deutsch, wie alle DTB-Skills; Skill-Text im etablierten Stil

### Integrationspunkte
- `dtb:impl-plan` — Träger des neuen Schritts (einzige geänderte Datei im Kern)
- `dtb:feature-discover` — Format-Kopplung, ungeändert: Auslöse-Kriterium parst dessen Output
  (`## Betroffene Module` in discovery.md); Kopplung im impl-plan-Text explizit benennen, damit
  eine spätere Formatänderung das Kriterium nicht still bricht
- `dtb:plan-review` — Konsument ohne Änderung: Grounding (2d) extrahiert Datei-Pfade aus dem
  Plan; Pfade im neuen `## Ist-Analyse`-Abschnitt fallen automatisch in diese Mechanik
- `dtb:pipeline-graph` / `dtb:workflow-status` — lesen das erweiterte `consumes:`-Frontmatter
  (reine Anzeige-Folge)
- `dtb:kit-sync` — Verteilungsweg nach der Änderung (Standard-Prozess)
- **Extern:** keine (keine APIs/Services/neue Tools; bordeigene Glob/Grep-Mechanik)

---

## Abhaengigkeiten

- Keine Konflikte: `features/` enthält nur diesen Change-Ordner (alle 9 anderen archiviert)
- Berührung ohne Konflikt: INBOX #11 (Greenfield-Autoren-Skills) will später feature-plan/greenfield-*
  umbauen — keine Datei-Überschneidung (3a: nur impl-plan); Auslöse-Kriterium bewusst generisch
  formuliert, als Vorbild für #11 wiederverwendbar

---

## Offene Punkte

— keine — (das in 3a offene „Veraltet"-Kriterium wurde in 3c entschieden: Stichproben-Verifikation + Zusatzregel)

---

**Erstellt mit:** `/dtb:feature-discover`
