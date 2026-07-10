# Discovery: Eligibility-Gates
<!-- resume: done -->

**Erstellt:** 2026-07-10
**Idee-Referenz:** Inbox #12 — "Eligibility-Gates mit Redirect (abgetrennt aus #5, Baustein C): Skills prüfen am Eingang, ob die Situation zu ihrem Zweck passt (Existenz des `consumes`-Artefakts, Git-Zustand, Argument) — bei Nichteignung konstruktive Weigerung + Verweis auf den passenden Skill (Redirect aus Pipeline-`after`/`next`). Vorbild: 10x-tdd"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-*/SKILL.md` (Hard-Gate-Kandidaten, ~9) | Erhalten je einen Eingangs-Gate-Schritt (Fit-Check + Redirect); Kern-Änderungsumfang |
| `pipeline.consumes` je Skill | Fit-Check-Quelle: existiert das **primäre** (erste) `consumes`-Artefakt? (Glob-Auflösung nötig, z.B. `features/*/spec.md`) |
| `pipeline.produces` / `pipeline.after` je Skill | Redirect-Ziel-Ableitung: Rückwärtssuche über `produces`, `after` (jetzt **Liste**) als Fallback |
| `skills/CLAUDE.md` | Contributor-Guide — Gate-Konvention + Einteilungsregel dokumentieren (Pflicht) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Konsistenz-Prüfpunkt: Gate-Artefakt-Existenz vs. Statusableitung (kein Umbau) |
| `workflow.config.yaml` (`repos[].path`) | Repo-Pfad für den gezielten Git-Zustand-Check |
| `dtb-project-health` | Optionaler Folge-Check (Drift-Wächter) — **bewusst aus dem Kern-Scope** |
| `dtb-pipeline-graph` | Liest dasselbe Frontmatter; Gate-Visualisierung optional/später |

---

## Anforderungen

### Scope
**Enthalten:**
- Eingangs-Fit-Check je gategeeignetem Skill: prüft, ob die Situation zum Skill-Zweck passt
- Fit-Check-Quellen: **Artefakt-Existenz generisch** (primäres `consumes` per Glob) + **Git-Zustand gezielt** (nur `code-review`/`build-check`, still übersprungen ohne Git)
- Bei Nichteignung: konstruktive Weigerung **mit Redirect** auf den passenden Skill
- Redirect-Ableitung: `produces`-Rückwärtssuche → `after` (Liste) als Fallback → sonst ehrliche Meldung ohne erfundenes Ziel
- Differenziertes Verhalten nach Skill-Art (Hard-Gate / Soft-Gate / kein Gate)
- Einteilungsregel als Fixpunkt + Drei-Eimer-Startliste; verbindliche Zuordnung pro Skill in `impl-plan`
- Konvention "erstes `consumes` = kritisch" in `skills/CLAUDE.md` dokumentiert

**Nicht enthalten:**
- Keine automatische Ausführung/Weiterleitung des Ziel-Skills (nur Verweis)
- Kein Gate für read-only-Skills und Entry-Points (`consumes: []`)
- **Argument-Check** raus (untergräbt bestehende Ableitungs-Fallbacks)
- Keine explizite required/optional-Markierung im `consumes`-Schema (Option C) — ggf. Folge-Feature
- Kein `project-health`-Drift-Wächter im Kern-Scope (optionaler Nachzügler)
- Keine Änderung der Pipeline-Struktur/-Semantik, keine neuen Skills

### Gewünschtes Verhalten
- Weigerung = kurzer Meldeblock (Muster wie `feature-discover` Schritt 1) mit konkretem Redirect-Befehl, kein stiller Abbruch, kein Weiterarbeiten auf falscher Basis
- Kein neues UX-Muster; bestehende Fehlermeldungs-/Fallback-Blöcke als Vorlage

### Randfälle
- **Hard vs. Soft:** schreibende Skills mit sinnlosem Output ohne Input → **Hard-Block**; nur empfohlene Voraussetzung → **Warnung + Fortfahren**; read-only → **kein Gate**
- **Kein Redirect-Ziel ableitbar** (Entry-Point ohne `after`, oder Git-Zustand als Ursache) → ehrliche Meldung ohne erfundenes Ziel
- **Mehrere `consumes`-Einträge, nur eines fehlt** → nur das **primäre (erste)** Artefakt gated; Weiteres (z.B. `lessons.md`) ist unkritischer Kontext und darf fehlen
- **Nicht-Git-Projekt** (z.B. Testbett `dtb-assistant`) → Git-Zustand-Check still überspringen

### Einschränkungen
- Fit-Check primär deklarativ aus vorhandenem Frontmatter (kein neues Schema, kein Zusatz-Tooling)
- Git-Zustand-Check nur für Skills mit `Bash` in `allowed-tools`; defensiv gegen fehlendes Git
- `consumes` enthält Glob-Muster → Fit-Check muss Globs auflösen

### Integrationspunkte
- **Pflicht:** `skills/CLAUDE.md` (Konvention dokumentieren); die ~9 Hard-Gate-Skills (Eingangs-Schritt)
- **Konsistenz:** `DERIVED_STATE_RULES.md` (Artefakt-Existenz-Logik)
- **Extern:** nur Git via `Bash` (gezielt, defensiv); sonst keine externen Abhängigkeiten
- **Distribution:** geänderte Skills = Klasse-A → nach Umsetzung per `dtb:kit-sync` global verteilen

---

## Abhängigkeiten

- **Herkunft:** abgetrennt aus Idee #5 / Feature `spec-haertung` (Baustein C), das Eligibility-Gates explizit ausschließt und auf #12 verweist — saubere Fortsetzung, kein Konflikt.
- **Überschneidung (wichtig):** `frontmatter-pfad-hygiene` hat `after`/`next` zu **Listen** (1:n) umgebaut → Redirect-`after`-Fallback muss Listen verarbeiten.
- Alle 5 Bestands-Features sind „Fertig zum Testen" — keine aktiven Konflikte.

---

## Offene Punkte

- Verbindliche Drei-Eimer-Zuordnung pro Skill (Hard/Soft/kein Gate) wird in `impl-plan` Zeile für Zeile festgelegt — die Startliste hier ist ein Vorschlag.
- `project-health`-Drift-Wächter und `pipeline-graph`-Gate-Visualisierung als mögliche Folge-Features prüfen.
- Explizite required/optional-Markierung im `consumes`-Schema (Option C) als potenzielles Folge-Feature, falls „erstes = kritisch" in der Praxis nicht reicht.

---

**Erstellt mit:** `/dtb:feature-discover`
