# Implementierungsplan: implement ohne feature-start

**Erstellt:** 2026-11-10
**Feature-Spec:** `features/implement-ohne-feature-start/spec.md`
**Geschaetzte Dauer:** ca. 1,5 h
**Status:** Reviewed (plan-review 2026-11-10: REVISE → 2 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | `implement` uebernimmt Auswahl und Kontext | 30 min | Geplant |
| Phase 2 | `feature-start` einschraenken, Verweise nachziehen, Gegenprobe | 60 min | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Modul-Liste per Grep `feature-start` ueber das Repo verifiziert 2026-11-10).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-implement/SKILL.md` | `after: [dtb:feature-start]`; Schritt 1 Punkt 1 „Unklar → Feature-Namen erfragen"; Schritt 2 laedt Plan + Spec, ruestet `## Progress` nach, Punkt 5 Statusanzeige ohne Spec-Ziel; Rhythmus-Hinweis in Schritt 3 und „Verwandte Skills" nennen feature-start |
| `skills/dtb-feature-start/SKILL.md` | Feature-, Bug- und Aufgaben-Zweig in Schritt 2-5; Feature-Zweig mit plan.md-Gate und `## Progress`-Nachruestung (einziger Grund fuer `Edit` in `allowed-tools` und `produces: [features/*/plan.md]`); `after: [dtb:plan-review, dtb:debug-plan]` |
| `skills/dtb-plan-review/SKILL.md` | `next: [dtb:feature-start]` (sonst keine Erwaehnung) |
| `skills/dtb-impl-plan/SKILL.md` | Bestaetigung Punkt 8: „2. Feature starten: /dtb:feature-start"; „Verwandte Skills": `/dtb:feature-start` |
| `skills/dtb-workflow-next/SKILL.md` | Feature-Zeile „`plan.md` Status `Reviewed`, 0/Y" → `/dtb:feature-start`; Bug- und Aufgaben-Zeilen ebenfalls feature-start (bleiben) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Handoff-Template-Beispiel und Regel „„Geplant" (0/Y) → `/dtb:feature-start`" |
| `skills/dtb-workflow-status/SKILL.md` | Queue „Backlog (Geplant)" und Uebergang „Feature starten" → feature-start; Bug-/Aufgaben-Zeilen bleiben |
| `skills/dtb-workflow-resume/SKILL.md` | Fall C (2 Stellen): „Starte eines mit `/dtb:feature-start`" |
| `skills/dtb-pipeline-graph/SKILL.md` | Kanten-Beispiel „`feature-start` ← 2 Vorgaenger"; Beispiel-Kette Feature-Pipeline mit feature-start |
| `skills/CLAUDE.md` | Hard-Gate-Tabelle (plan-review, feature-start, implement); Rueckfragen-Tabelle Zeile 15; Worktree-Kategorien-Tabelle fuehrt feature-start als worktree-faehig |
| `README.md` | Skill-Tabelle: „Start a planned feature from the backlog" |
| `CLAUDE.md` | Skill-Kategorien „Feature workflow": feature-start-Beschreibung |

---

## Phase 1: `implement` uebernimmt Auswahl und Kontext

### Ziel
`implement` leistet alles, was `feature-start` fuer Features zusaetzlich bot — danach ist der Vorschritt fachlich ueberfluessig.

### Schritte

#### Schritt 1.1: Auswahl ohne Argument
- **Zweck:** Ersetzt die Auswahlliste aus feature-start Schritt 3 fuer Features.
- **Dateien:** `skills/dtb-implement/SKILL.md` (Schritt 1 Punkt 1)
- **Input:** feature-start Schritt 2/3 (Filter und Listenform), `DERIVED_STATE_RULES.md` (Ableitung Geplant/In Arbeit)
- **Output:** Kein Argument und kein erkennbarer Chat-Kontext → Liste der Change-Ordner mit `plan.md` und mindestens einer offenen Progress-Zeile, gruppiert „Geplant" / „In Arbeit", je Zeile der Review-Stand aus dem Kopf-Statusfeld (`Entwurf`/`Reviewed`, §7 — reine Anzeige, keine Sperre), Wahl per Nummer. Leere Liste → ehrliche Meldung mit Verweis `/dtb:feature-start` (Bug, Aufgabe) bzw. `/dtb:impl-plan`. Mit Argument unveraendert.

#### Schritt 1.2: Ziel und Scope in der Statusanzeige
- **Zweck:** Ersetzt den Kontextblock aus feature-start Schritt 5.
- **Dateien:** `skills/dtb-implement/SKILL.md` (Schritt 2 Punkt 5)
- **Input:** `spec.md` (Kopfzeile `**Ziel:**`, Executive Summary)
- **Output:** Statusanzeige enthaelt 2-3 Zeilen Ziel/Scope; fehlt `spec.md`, entfallen sie still (kein Abbruch).

#### Schritt 1.3: Kanten und Verweise in implement
- **Zweck:** Pipeline-Vorgaenger und Selbstbeschreibung folgen dem neuen Weg.
- **Dateien:** `skills/dtb-implement/SKILL.md` (Frontmatter `description` und `after`, Rhythmus-Hinweis in Schritt 3, „Verwandte Skills")
- **Input:** Trigger-Phrasen aus der `description` von feature-start
- **Output:** `description` uebernimmt die Feature-Trigger „Feature starten", „naechstes Feature" (feature-start gibt sie in 2.1 ab); `after: [dtb:plan-review]`; Rhythmus-Hinweis nennt nur noch das impl-plan-Template; „Verwandte Skills" fuehrt `/dtb:plan-review` als Vorgaenger und `/dtb:feature-start` nur noch fuer Bugs/Aufgaben.

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-implement/SKILL.md` mit Auswahl, Spec-Kontext und neuer Vorgaenger-Kante

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "^  after:" skills/dtb-implement/SKILL.md` → genau `  after: [dtb:plan-review]`
- [ ] `awk '/^description:/,/^disable-model-invocation:/' skills/dtb-implement/SKILL.md | grep -c "Feature starten"` = 1
- [ ] `awk '/^## Schritt 1: Plan aufloesen/,/^## Eligibility-Gate/' skills/dtb-implement/SKILL.md | grep -c "Geplant"` ≥ 1 und dieselbe Sektion enthaelt `In Arbeit` (Auswahl-Gruppen) und `Reviewed` (Review-Stand je Zeile)
- [ ] `awk '/^## Schritt 2: Plan laden/,/^## Schritt 3/' skills/dtb-implement/SKILL.md | grep -c "Ziel"` ≥ 1 (Spec-Kontext in der Statusanzeige)
- [ ] `awk '/^## Schritt 3: Umsetzungs-Loop/,/^1\. \*\*Implementiere/' skills/dtb-implement/SKILL.md | grep -c "feature-start"` = 0 (Rhythmus-Hinweis)

#### Manual
- [ ] Beispiel-Ausgabe von Auswahl und Statusanzeige nach der Repo-Fassung von `implement` mit den echten Ordnern unter `dtb-project/project-workflows/features/` im Chat gezeigt und vom Nutzer abgenommen: die Auswahl erscheint nur ohne Argument und Kontext, wirkt nicht als Leerlauf-Rueckfrage, Review-Stand und Ziel-Zeilen stimmen mit den Dateien; Ergebnis im Session-Log (ueber den Hand-off)

---

## Phase 2: `feature-start` einschraenken, Verweise nachziehen, Gegenprobe

### Ziel
Kein Skill und keine Doku-Stelle nennt `feature-start` mehr als Start eines Features; der Bug- und Aufgaben-Weg bleibt unveraendert.

### Schritte

#### Schritt 2.1: feature-start auf Bug und Aufgabe beschraenken
- **Zweck:** Der Feature-Zweig wandert vollstaendig nach implement.
- **Dateien:** `skills/dtb-feature-start/SKILL.md` (Frontmatter `description`, `allowed-tools`, `after`, `consumes`, `produces`; Schritte 2-5; „Wichtig")
- **Input:** Phase 1
- **Output:** Nur noch Bugs „Analysiert" und Aufgaben „Offen"; Feature genannt → genau eine Zeile `→ Features startet /dtb:implement {Name} direkt`; Leer-Meldung „Nichts zu starten — keine analysierten Bugs oder offenen Aufgaben." plus Verweis `Features: /dtb:implement`; plan.md-Gate und `## Progress`-Nachruestung entfallen; `after: [dtb:debug-plan]`, `next` bleibt `[dtb:implement]`; `consumes` ohne spec/plan, `produces: []`, `Edit` aus `allowed-tools` (Frontmatter im selben Zug wie der Datei-Umgang).

#### Schritt 2.2: Planungs-Skills nennen implement
- **Zweck:** „plan-review/impl-plan nennen nur noch diesen" (Fertig-Kriterium der Idee).
- **Dateien:** `skills/dtb-plan-review/SKILL.md` (`next`), `skills/dtb-impl-plan/SKILL.md` (Bestaetigung Punkt 8, „Verwandte Skills")
- **Input:** —
- **Output:** `next: [dtb:implement]`; Bestaetigung „2. Umsetzen: /dtb:implement [Feature-Name]"; Verwandte-Skills-Zeile auf `/dtb:implement`.

#### Schritt 2.3: Uebersichts-Skills empfehlen implement
- **Zweck:** Next-/Status-/Resume-/Checkpoint-Sichten zeigen fuer ein geplantes Feature den neuen Befehl.
- **Dateien:** `skills/dtb-workflow-next/SKILL.md`, `skills/dtb-workflow-checkpoint/SKILL.md`, `skills/dtb-workflow-status/SKILL.md`, `skills/dtb-workflow-resume/SKILL.md`
- **Input:** Ist-Analyse (Feature- vs. Bug-/Aufgaben-Zeilen)
- **Output:** Nur die Feature-Stellen umgestellt: workflow-next „Reviewed, 0/Y" → `/dtb:implement [NAME]`; workflow-checkpoint Beispiel + Regel „Geplant (0/Y)" → `/dtb:implement {NAME}`; workflow-status „Backlog (Geplant)" → `/dtb:implement`, Uebergangszeile „Feature starten" wird „Bug-Fix/Aufgabe starten" (`/dtb:feature-start`) — der Feature-Weg steht schon in der vorhandenen Zeile „Umsetzung + Verifikation" (`/dtb:implement`), keine zusaetzliche Zeile; workflow-resume Fall C nennt `/dtb:implement` (Feature) und `/dtb:feature-start` (Bug, Aufgabe).

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Konventionen und Doku
- **Zweck:** Autoren-Doku und Uebersichten passen zum neuen Weg.
- **Dateien:** `skills/dtb-pipeline-graph/SKILL.md`, `skills/CLAUDE.md`, `README.md`, `CLAUDE.md`
- **Input:** Schritte 2.1-2.3
- **Output:** pipeline-graph: Feature-Kette ohne feature-start, Kanten-Beispiel stimmt mit den neuen `after`-Listen; `skills/CLAUDE.md`: Hard-Gate-Tabelle (feature-start-Zeile entfaellt oder „kein Gate mehr", plan-review- und implement-Zeile ohne feature-start-Bezug), Rueckfragen-Tabelle Zeile 15 mit Vermerk „seit 2026-11-10 entfallen — Feature-Weg fuehrt direkt in implement" (Zeile E bleibt), Worktree-Kategorien-Tabelle: feature-start zu den Read-only-Sichten (schreibt nichts mehr); README: Zeile `/dtb:feature-start` auf Bug/Aufgabe umschreiben und eine NEUE Zeile `/dtb:implement` direkt nach `/dtb:plan-review` einfuegen (die README hat heute keine — weitere README-Luecken wie impl-review/pane-start bleiben ausserhalb dieses Changes); CLAUDE.md-Beschreibung von feature-start (Bug/Aufgabe) und implement (Auswahl ohne Argument).

#### Schritt 2.5: Repo-weite Gegenprobe
- **Zweck:** Kein uebersehener Feature-Verweis (Pipeline-Umbau-Lektion: Uebersichts-Skills nennen Schritte ausserhalb der Frontmatter).
- **Dateien:** keine (reine Pruefung) — **Ablageort:** Session-Log ueber den WORKTREE-HANDOFF-Block (Trefferliste mit Einstufung)
- **Input:** `grep -rn "feature-start" skills/ README.md CLAUDE.md agents/`
- **Output:** Jeder Treffer eingestuft als Bug/Aufgabe, Selbstbeschreibung von feature-start, Geschichte (Vermerk) oder Defekt; Defekte sofort behoben.

### Deliverables
- [ ] feature-start nur noch fuer Bug und Aufgabe
- [ ] Alle Feature-Verweise zeigen auf implement
- [ ] Gegenprobe-Liste im Hand-off

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "^  next:" skills/dtb-plan-review/SKILL.md` → genau `  next: [dtb:implement]`
- [ ] `grep -n "^  after:" skills/dtb-feature-start/SKILL.md` → genau `  after: [dtb:debug-plan]`
- [ ] `grep -rln "^  next: \[dtb:feature-start\]" skills/*/SKILL.md` → nur `skills/dtb-debug-plan/SKILL.md`
- [ ] `grep -c "feature-start" skills/dtb-impl-plan/SKILL.md` = 0
- [ ] `grep -n "Reviewed\`, 0/Y" skills/dtb-workflow-next/SKILL.md` → Zeile enthaelt `/dtb:implement`
- [ ] `grep -n "Geplant\" (0/Y)" skills/dtb-workflow-checkpoint/SKILL.md` → Zeile enthaelt `/dtb:implement`
- [ ] `grep -n "Backlog (Geplant)" skills/dtb-workflow-status/SKILL.md` → Zeile enthaelt `/dtb:implement`
- [ ] `grep -c "^| Feature starten |" skills/dtb-workflow-status/SKILL.md` = 0 und `grep -n "^| Bug-Fix/Aufgabe starten |" skills/dtb-workflow-status/SKILL.md` → Zeile enthaelt `/dtb:feature-start`
- [ ] `grep -n "Kein aktives Feature" skills/dtb-workflow-resume/SKILL.md` → jede Zeile enthaelt `/dtb:implement`
- [ ] `grep -c "Geplante Features" skills/dtb-feature-start/SKILL.md` = 0 (Feature-Liste aus der Auswahl entfernt)
- [ ] `grep -c "geplanten Features" skills/dtb-feature-start/SKILL.md` = 0 (Leer-Meldung ohne Features)
- [ ] `grep -A1 "^| \`/dtb:plan-review\` |" README.md` → Folgezeile beginnt mit `` | `/dtb:implement` | ``
- [ ] `grep -n "^| \`feature-start\` |" skills/CLAUDE.md` → keine Zeile mehr in der Hard-Gate-Tabelle mit `features/*/plan.md`

#### Manual
- [ ] Gegenprobe-Liste aus Schritt 2.5 gelesen: jeder verbliebene Treffer ist Bug/Aufgabe, Selbstbeschreibung oder Geschichte

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Umfang des Kontexts in implement | A: 2-3 Zeilen Ziel/Scope · B: voller feature-start-Block | A | Per Veto-Vorlage bestaetigt 2026-11-10 — implement bleibt kompakt; der volle Block war Leerlauf vor dem eigentlichen Status |
| Auswahl ohne Argument | A: Liste Geplant + In Arbeit · B: weiter nur Namen erfragen | A | Per Veto-Vorlage bestaetigt 2026-11-10 — ersetzt die Auswahl von feature-start; mit Argument keine Aenderung |
| Feature-Zweig in feature-start | A: entfernen, Verweis-Zeile · B: als Alias behalten | A | Per Veto-Vorlage bestaetigt 2026-11-10 — ein Alias hielte den zweiten Weg am Leben, den die Idee abschaffen will |
| Bug-/Aufgaben-Verweise | A: unveraendert · B: mitumbauen | A | Per Veto-Vorlage bestaetigt 2026-11-10 — ausserhalb des Scopes; Bugs/Aufgaben haben keinen plan.md |
| Rueckfragen-Tabelle Zeile 15 | A: Vermerk „entfallen" · B: Zeile loeschen | A | Per Veto-Vorlage bestaetigt 2026-11-10 — Festlegungsgeschichte bleibt nachvollziehbar |
| Kanten von feature-start | `after: [dtb:debug-plan]`, `next` unveraendert `[dtb:implement]` | gesetzt | Per Veto-Vorlage bestaetigt 2026-11-10 — kleinster Eingriff; DERIVED_STATE_RULES.md nennt feature-start nicht und bleibt unberuehrt |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Auswahl ohne Argument
- [x] 1.2 Ziel und Scope in der Statusanzeige
- [x] 1.3 Kanten und Verweise in implement
- [ ] 2.1 feature-start auf Bug und Aufgabe beschraenken
- [ ] 2.2 Planungs-Skills nennen implement
- [ ] 2.3 Uebersichts-Skills empfehlen implement
- [ ] 2.4 Konventionen und Doku
- [ ] 2.5 Repo-weite Gegenprobe

---

## Umsetzung

Umsetzung mit `/dtb:implement implement-ohne-feature-start` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/implement-ohne-feature-start/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-10)
