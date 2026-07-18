# Implementierungsplan: open-question

**Erstellt:** 2026-07-18
**Feature-Spec:** `features/open-question/spec.md`
**Geschaetzte Dauer:** ~2.5 h
**Status:** Entwurf

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Geruest + Eingabe + Ziel-Routing (Variante c) | ~45 min | Geplant |
| Phase 2 | Ziel-Datei, Bestaetigung (Variante B) + §6-Schreiben + Randfaelle | ~60 min | Geplant |
| Phase 3 | Katalog, Distribution + End-to-End-Verifikation | ~45 min | Geplant |

---

## Ist-Analyse

> Uebernommen aus `discovery.md` (`## Betroffene Module`), Bestandspfade per Glob verifiziert.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-open-question/SKILL.md` | **Existiert noch nicht** — Neubau-Ziel dieses Features |
| `skills/dtb-idea/SKILL.md` | Struktur-Vorbild: Frontmatter (`disable-model-invocation: true`, `allowed-tools`, `argument-hint`, `pipeline`) + Schritt 0 Config -> 1 Input -> 2 Write -> 3 Confirm |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §6 = `[Fach]`-Grammatik (Kanonform `- [ ] [Fach] <Frage>`, Status-Neutralitaet §6.2); §1.1 = Ableitung „In Arbeit" (plan.md teilweise abgehakt) |
| `skills/dtb-feature-discover/SKILL.md` | Schreibt `## Offene Punkte` in `discovery.md`; traegt §6-Anleitung + Format-Kopplungs-Hinweis (Vorbild fuer den reziproken Hinweis) |
| `skills/dtb-feature-plan/SKILL.md` | Schreibt `## Offene Punkte` in `spec.md`; ebenfalls §6-Anleitung |
| `skills/dtb-kit-sync/SKILL.md` | Klasse-A-Distribution (`skills/dtb-*/SKILL.md`) global + `~/.claude/dtb-lock.json` |
| `CLAUDE.md` (Repo-Root) | Skill-Katalog (Abschnitt „Skill Categories") — neuer Skill muss gelistet werden |

---

## Phase 1: Skill-Geruest + Eingabe + Ziel-Routing

### Ziel
Der Skill existiert mit korrektem Frontmatter, erfasst die Frage und ermittelt das Ziel-Feature nach Variante (c) inklusive aller Mehrdeutigkeits-Ausgaenge.

### Schritte

#### Schritt 1.1: Skill-Verzeichnis + Frontmatter
- **Zweck:** Skill auffindbar + Pipeline-korrekt anlegen
- **Dateien:** `skills/dtb-open-question/SKILL.md` (neu)
- **Input:** Frontmatter-Vorbild `dtb-idea`, Pipeline-Entscheidung aus Spec
- **Output:** Frontmatter mit `name: dtb:open-question`, `disable-model-invocation: true`, `argument-hint: "[<slug>] <Frage>"`, `allowed-tools: Read, Glob, Grep, Edit, Write`, `pipeline: {stage: capture, after: null, next: [dtb:workflow-next], consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md], produces: [features/*/spec.md, features/*/discovery.md]}`

#### Schritt 1.2: Config laden + Frage erfassen
- **Zweck:** Eingabe robust aufnehmen
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** Command-Argument (Freitext, optional fuehrender Slug)
- **Output:** Schritt „Config laden" (Fallback-Pfad) + Eingabe-Regeln: leeres Frage-Argument -> nachfragen (wie `/dtb:idea`); Sonderzeichen 1:1; mehrzeilige Eingabe zu einer Bullet-Zeile normalisieren

#### Schritt 1.3: Ziel-Feature ermitteln (Variante c)
- **Zweck:** korrektes Ablage-Feature bestimmen, kein stilles Raten
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** §1.1-Ableitung (Scan `features/*/plan.md`, teilweise abgehakt = „In Arbeit"), optionaler Slug-Override
- **Output:** Routing-Logik: Default = einziges aktives Feature; Slug-Argument = Override; **0 aktiv + kein Slug** -> abbrechen + waehlbare Slugs; **>1 aktiv** -> Auswahlliste; **Slug ungueltig/leerer Ordner** -> abbrechen + Liste vorhandener Ordner (kein Auto-Anlegen)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-open-question/SKILL.md` mit Frontmatter, Config/Eingabe, Ziel-Routing (c)

### Checkpoint-Kriterien

#### Automated
> Artefakt-Form-Checks (Existenz/Frontmatter) — kein Verhaltensbeweis; die Verhaltensverifikation liefern der P2-Smoke (Ende Phase 2) und 3.3.
- [ ] Datei existiert: Glob `skills/dtb-open-question/SKILL.md` liefert 1 Treffer
- [ ] Frontmatter korrekt: Grep in `skills/dtb-open-question/SKILL.md` findet `name: dtb:open-question`, `disable-model-invocation: true` und `stage: capture` (verankert auf die Datei — Lektion #2)

#### Manual
- [ ] Ziel-Routing (c) deckt alle vier Ausgaenge (Default / Override / 0 aktiv / >1 aktiv) eindeutig ab

---

## Phase 2: Ziel-Datei, Bestaetigung (B) + §6-Schreiben + Randfaelle

### Ziel
Der Skill waehlt die richtige Zieldatei, zeigt Ziel + formatierte Zeile zur Freigabe (Variante B) und schreibt §6-konform ans Sektionsende — status-neutral, mit Duplikat-Schutz.

### Schritte

#### Schritt 2.1: Ziel-Datei waehlen
- **Zweck:** deterministische Datei-Wahl im Feature-Ordner
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** Ordnerinhalt des Ziel-Features
- **Output:** Regel: am weitesten fortgeschritten = `spec.md` falls vorhanden, sonst `discovery.md`; nur `plan.md`/`bug.md`/`task.md` vorhanden -> in `spec.md` schreiben falls vorhanden, sonst abbrechen (kein Schreiben in `plan.md`/`bug.md`/`task.md`)

#### Schritt 2.2: Formatieren, Bestaetigen (B), Duplikat-Schutz
- **Zweck:** korrekte §6-Zeile, Fehl-Ablage verhindern, Doppelerfassung vermeiden
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** normalisierte Frage, ermitteltes Ziel
- **Output:** Kanonform `- [ ] [Fach] <Frage>` (je ein Leerzeichen); Variante-B-Anzeige (Ziel + Zeile) + Freigabe abwarten; Duplikat-Schutz: existiert die exakt gleiche offene `[Fach]`-Zeile -> warnen + ueberspringen (nur exakter Textvergleich)

#### Schritt 2.3: Schreiben + Bestaetigung + Status-Neutralitaet
- **Zweck:** Zeile korrekt platzieren, Invariante sichern
- **Dateien:** `skills/dtb-open-question/SKILL.md`
- **Input:** Zieldatei + freigegebene Zeile
- **Output:** Anhaengen **ans Ende des Textblocks der bestehenden `## Offene Punkte`-Sektion** — nach der letzten Inhaltszeile der Sektion, vor der naechsten `##`-Ueberschrift; der `**Erstellt mit:**`-Footer dient nur als Fallback-Anker, wenn die Sektion die letzte im Dokument ist. Fehlt die Sektion -> vor dem Footer neu anlegen. Bestehende Eintraege inkl. beantworteter `[x]`-Zeilen und eingerueckter `→ Antwort:`-Fortsetzungszeilen bleiben unveraendert (nur anhaengen, nie umsortieren/verschieben); **nie** `## Progress`/Status beruehren; Abschluss-Bestaetigung mit Verweis #25 / `/dtb:workflow-next`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Vollstaendige Schreib-/Bestaetigungs-/Randfall-Logik im Skill

### Checkpoint-Kriterien

#### Automated
> Artefakt-Form-Checks (SKILL.md-Inhalt) — kein Verhaltensbeweis; die Verhaltensverifikation liefert der P2-Smoke unten.
- [ ] Grep in `skills/dtb-open-question/SKILL.md` findet die Kanonform-Vorschrift `- [ ] [Fach]` und die Sektionsmarke `## Offene Punkte` (verankert auf die Datei)
- [ ] Grep findet Belege fuer Duplikat-Schutz und Variante-B-Bestaetigung (Stichworte „Duplikat"/„exakt", „bestaetig"/„Freigabe")

#### Manual
- [ ] Status-Neutralitaet ist als explizite Invariante formuliert (kein `## Progress`-Zugriff)
- [ ] Alle Randfaelle aus der Spec sind im Skill abgedeckt (leeres Arg, Sonderzeichen, nur plan/bug/task)
- [ ] Einfuegung laesst bestehende `## Offene Punkte`-Inhalte unversehrt — beantwortete `[x]`-Eintraege + eingerueckte `→ Antwort:`-Zeilen bleiben an Ort und Stelle
- [ ] **P2-Smoke gruen** (Verhaltensverifikation VOR jeder Distribution): Skill-Schritte manuell an einem Wegwerf-Fixture (Feature mit teilweise abgehaktem `plan.md`) durchgespielt -> `[Fach]`-Zeile korrekt am Sektionsende platziert, Feature-Status unveraendert

---

## Phase 3: Katalog, Distribution + Verifikation

### Ziel
Der Skill ist dokumentiert, global verteilt und end-to-end an einem echten Feature belegt.

### Schritte

#### Schritt 3.1: CLAUDE.md-Katalog + Kopplungs-Hinweis
- **Zweck:** Auffindbarkeit + Wartbarkeit der Format-Kopplung
- **Dateien:** `CLAUDE.md`, `skills/dtb-open-question/SKILL.md`
- **Input:** bestehende Katalog-Struktur, bestehende Kopplungs-Hinweise als Vorbild
- **Output:** Katalog-Eintrag fuer `open-question`; im Skill ein Wartungs-Hinweis „Format-Kopplung" (open-question ist der dritte Schreiber von `## Offene Punkte` neben feature-discover/-plan; §6 ist Single Source)

#### Schritt 3.2: Distribution via kit-sync
- **Zweck:** Skill global verfuegbar machen (Klasse A)
- **Dateien:** `~/.claude/skills/dtb-open-question/SKILL.md`, `~/.claude/dtb-lock.json` (via `/dtb:kit-sync sync`)
- **Input:** committeter Feature-Stand
- **Output:** globaler Skill-Ordner + Lock-Eintrag; Verifikation „synchron, 0 Abweichung" (laeuft nach dem Feature-Commit)

#### Schritt 3.3: End-to-End-Verifikation
- **Zweck:** Success Criteria real belegen
- **Dateien:** ein Test-Feature-Ordner (temporaer/vorhanden)
- **Input:** installierter Skill
- **Output:** Durchlauf belegt c-Routing (Default/Override/0/>1), Variante B, korrekte §6-Zeile, Status-Neutralitaet (Testfeature bleibt im Status), Duplikat-Schutz; Ergebnisse in den Session-Log

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Katalog aktualisiert, Skill verteilt, End-to-End verifiziert

### Checkpoint-Kriterien

#### Automated
- [ ] Grep in `CLAUDE.md` findet `open-question` im Skill-Katalog
- [ ] Nach kit-sync: Glob `~/.claude/skills/dtb-open-question/SKILL.md` liefert 1 Treffer und Grep in `~/.claude/dtb-lock.json` findet `dtb-open-question`

#### Manual
- [ ] Installierter Command-Smoke gruen: alle Success Criteria der Spec belegt (inkl. Status-Neutralitaet am echten Feature). Bei Fehler -> fix im Repo, `/dtb:kit-sync` erneut (idempotent); erst danach abhaken. Die inhaltliche Verifikation ist bereits im P2-Smoke gelaufen (vor der Distribution)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Pipeline-Stage | `idea` / `capture` | `capture` | open-question schreibt in ein laufendes Feature, nicht in die INBOX — eigener Quer-Erfassungs-Stage ehrlicher (Discovery 3e) |
| Ziel-Routing | (a) ableiten / (b) Slug / (c) beides | (c) | Deckt 1-aktives-Feature-Normalfall reibungslos, bleibt bei 0/>1 sauber (Discovery 3a) |
| Bestaetigung | (A) nur anzeigen / (B) Freigabe abwarten | (B), immer | Verhindert Fehl-Ablage bei abgeleitetem Ziel (Discovery 3b) |
| Duplikat-Matching | exakt / fuzzy | exakter Textvergleich | Billiger Schutz, kein Fuzzy-Aufwand (Discovery 3d) |
| Reziproker Kopplungs-Hinweis in feature-discover/-plan | ja / nein | Offen | In `plan-review`/Umsetzung entscheiden; Spec verlangt Hinweis nur im neuen Skill |
| Verifikations-Reihenfolge Phase 3 | verify→distribute / distribute→smoke | distribute→installierter Smoke; echte Verifikation vorgezogen in den P2-Smoke | Command laeuft nur aus `~/.claude/` (Installation noetig), reines Tauschen unmoeglich; kit-sync ist idempotent, Fehler -> fix+re-sync (plan-review 2026-07-18) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Skill-Verzeichnis + Frontmatter
- [x] 1.2 Config laden + Frage erfassen
- [x] 1.3 Ziel-Feature ermitteln (Variante c)
- [ ] 2.1 Ziel-Datei waehlen
- [ ] 2.2 Formatieren, Bestaetigen (B), Duplikat-Schutz
- [ ] 2.3 Schreiben + Bestaetigung + Status-Neutralitaet
- [ ] 3.1 CLAUDE.md-Katalog + Kopplungs-Hinweis
- [ ] 3.2 Distribution via kit-sync
- [ ] 3.3 End-to-End-Verifikation

---

## Umsetzung

Umsetzung mit `/dtb:implement open-question` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/open-question/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
