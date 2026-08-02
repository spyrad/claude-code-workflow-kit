# Implementierungsplan: Fast-Track-Schiene (dtb:feature-fast)

**Erstellt:** 2026-08-01
**Feature-Spec:** `features/feature-fast/spec.md`
**Geschaetzte Dauer:** 4.5-5.5h (3 Phasen)
**Status:** Reviewed (plan-review 2026-08-01: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Orchestrator-Skill `dtb:feature-fast` bauen | 2-3h | Geplant |
| Phase 2 | Weichen (idea-review, feature-discover) + Kopplungs-Hinweise | 1h | Geplant |
| Phase 3 | Doku + Distribution + E2E-Probelauf | 1.5h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Pfade verifiziert 2026-08-01; Neubau-Ziel nach L5 ausgenommen).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-feature-fast/SKILL.md | Existiert nicht — Neubau-Ziel, keine Slug-/Namenskollision |
| skills/dtb-idea-review/SKILL.md | Aktion "Ausarbeiten" in Schritt 3 (Z. 72-87): setzt In Arbeit, beendet Review, verweist auf feature-discover; Frontmatter `next: [dtb:feature-discover]` (Z. 12) |
| skills/dtb-feature-discover/SKILL.md | Schritt 1 laedt Idee (Argument oder In-Arbeit-Filter); Schritt-6-Template ist der Discovery-Anker; traegt bereits einen Format-Kopplungs-Hinweis Richtung impl-plan (Muster fuer 2.3) |
| skills/dtb-feature-plan/SKILL.md | Sektion `## Template fuer spec.md` = Spec-Anker; enthaelt Technical-Leak-Lint (7 Kategorien) + Meta-Spec-Ausnahme |
| skills/dtb-impl-plan/SKILL.md | Sektion `## Template fuer plan.md` = Plan-Anker (inkl. `## Progress`-Block, §7-Kopf); Wartungs-Hinweis-Muster vorhanden |
| CLAUDE.md | Skill-Kategorien unter "### Skill Categories", Zeile "Feature workflow" listet die Kette |

---

## Phase 1: Orchestrator-Skill bauen

### Ziel
`skills/dtb-feature-fast/SKILL.md` existiert vollstaendig: Gate, Struktur-Check, Erhebung mit
Defaults, Sammelvorlage mit Veto-Mechanik, Schreibphase, Eskalation, Wiederaufnahme.

### Schritte

#### Schritt 1.1: Skill-Geruest + Eingangs-Gate
- **Zweck:** Konventionskonformer Rahmen; Einstieg nur ueber INBOX (Spec: Pflicht-Vorstufe)
- **Dateien:** skills/dtb-feature-fast/SKILL.md (neu)
- **Input:** skills/CLAUDE.md (Frontmatter-Pflichtfelder, Eligibility-Gate-Konvention)
- **Output:** Frontmatter (`name: dtb:feature-fast`, `disable-model-invocation: true`,
  `allowed-tools: Read, Write, Glob, Grep`, pipeline `stage: planning`,
  `after: [dtb:idea-review]`, `next: [dtb:plan-review]`, `consumes: [INBOX.md,
  workflow.config.yaml, features/*/discovery.md, features/*/spec.md, features/*/plan.md]`
  (Bestandsaufnahme liest vorhandene Artefakte — plan-review Befund 3), `produces:
  [features/*/discovery.md, features/*/spec.md, features/*/plan.md,
  features/*/fast-draft.md]`); Schritt 0 Config; Gate: INBOX-Eintrag laden (Argument oder
  In-Arbeit-Filter), fehlt er → Weigerung + Redirect `/dtb:idea`; Slug nach §4 inkl.
  Kollisionsregel; Bestandsaufnahme des Change-Ordners (vorhandene Artefakte uebernehmen,
  nur fehlende vorbefuellen)

#### Schritt 1.2: Struktur-Check der drei Template-Quellen
- **Zweck:** Kopplungs-Drift erkennen statt still falsch buendeln (Spec-Risiko 2)
- **Dateien:** skills/dtb-feature-fast/SKILL.md
- **Input:** Anker-Entscheidung (siehe Technische Entscheidungen)
- **Output:** Check-Sektion: prueft in den installierten Kopien unter `~/.claude/skills/`
  die drei Anker — feature-discover `## Schritt 6` (Discovery-Template), feature-plan
  `## Template fuer spec.md`, impl-plan `## Template fuer plan.md` (inkl. `## Progress`-Block);
  fehlt ein Anker → benannte Warnmeldung + Stopp (kein Weiterarbeiten). **Benanntes
  Restrisiko** (plan-review Pre-Mortem): der Check prueft Anker-EXISTENZ, nicht
  Template-INHALT — die inhaltliche Verteidigung sind die Wartungs-Hinweise aus 2.3

#### Schritt 1.3: Erhebungs-Kern (Defaults + Kernfragen)
- **Zweck:** Die eigentliche Buendelung — Interviews durch begruendete Annahmen ersetzen
- **Dateien:** skills/dtb-feature-fast/SKILL.md
- **Input:** INBOX-Idee-Text, Repo-Kontext (Glob/Grep read-only)
- **Output:** Erhebungs-Sektion: Default-Annahmen je Template-Abschnitt ableiten;
  Kernfragen-Budget max. 3 (nur echte Informationsluecken, sonst Annahme); jede Annahme
  nummeriert (A1..An) und gekennzeichnet als **verifiziert** (gegrepter Befund) oder
  **Vermutung** (Lektion Inbox #36b); laufender Annahmen-Zaehler fuer die Selbst-Eskalation

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Sammelvorlage + Veto-Mechanik + Zwischenspeicher
- **Zweck:** Der eine Kontrollpunkt vor dem Schreiben (Spec-Risiko 1: Durchwinken)
- **Dateien:** skills/dtb-feature-fast/SKILL.md
- **Input:** Erhebungs-Ergebnis aus 1.3
- **Output:** Vorlagen-Format: Kurzfassung je Artefakt (nicht voller Wortlaut) +
  Annahmen-Block (max. ~10, nummeriert); Veto-Verarbeitung: Freitext-Korrekturen
  ("A2: stattdessen ..."), Unkommentiertes gilt als angenommen; Zwischenspeicher
  `features/{slug}/fast-draft.md` (geschrieben vor dem Ok bzw. bei Abbruch; wird
  committet/gepusht — Wiederaufnahme auf beiden Maschinen, Entscheid plan-review
  2026-08-01; geloescht nach erfolgreichem Artefakt-Schreiben); Wiederaufnahme:
  existiert fast-draft.md beim Start → anbieten statt neu zu erheben

#### Schritt 1.5: Schreibphase + Eskalation
- **Zweck:** Konventionskonforme Artefakte; geordneter Ausstieg nach oben (Spec-Risiken 4/5)
- **Dateien:** skills/dtb-feature-fast/SKILL.md
- **Input:** bestaetigte Vorlage aus 1.4
- **Output:** Schreibreihenfolge discovery → spec → plan; spec nach feature-plan-Template
  inkl. Technical-Leak-Lint (per Referenz auf die Lint-Sektion in feature-plan, keine Kopie);
  plan nach impl-plan-Template inkl. `## Progress` (§2) und Kopf `Status: Entwurf` (§7,
  Definitionsfenster erste 10 Zeilen); INBOX-Zeile auf Ausgearbeitet + Links; Selbst-Eskalation:
  mehr als 10 Annahmen ODER mehr als 2 Plan-Phasen → Empfehlung Voll-Schiene mit benannter
  Begruendung; Eskalationspfad: entstandene Artefakte bleiben, Verweis auf den naechsten
  regulaeren Skill (feature-discover-Wiederaufnahme bzw. feature-plan/impl-plan)

### Deliverables
- [ ] skills/dtb-feature-fast/SKILL.md vollstaendig (Gate, Struktur-Check, Erhebung, Vorlage, Schreibphase, Eskalation, Wiederaufnahme)

### Checkpoint-Kriterien

#### Automated
- [ ] Baseline: `/dtb:project-health` VOR Schritt 1.1 einmal ausgefuehrt, Stand im Session-Log festgehalten (Vergleichswert fuer das Phase-3-Kriterium)
- [ ] Datei existiert: `skills/dtb-feature-fast/SKILL.md`
- [ ] Grep Frontmatter (Zeilen 1-20): `name: dtb:feature-fast`, `disable-model-invocation: true`, `next: [dtb:plan-review]`
- [ ] Grep Struktur-Check-Sektion: alle drei Anker-Strings woertlich benannt (`## Schritt 6`, `## Template fuer spec.md`, `## Template fuer plan.md`)
- [ ] Grep Selbst-Eskalations-Regel: Schwellwerte `10` (Annahmen) und `2` (Phasen) an der Eskalations-Zeile
- [ ] Grep Wiederaufnahme-Sektion: `fast-draft.md` als Zwischenspeicher benannt

#### Manual
- [ ] Sammelvorlagen-Format am Beispiel gelesen: kompakt genug, dass ein echtes Veto realistisch ist

---

## Phase 2: Weichen + Kopplungs-Hinweise

### Ziel
Der Fast-Track ist von der Voll-Schiene aus erreichbar (Dreier-Weiche, Umleitung); die
Kopplung an die drei Quell-Skills ist an Ort und Stelle dokumentiert.

### Schritte

#### Schritt 2.1: idea-review Dreier-Weiche
- **Zweck:** Eingangsweiche Task / Fast-Track / Voll-Schiene (Discovery-Entscheid)
- **Dateien:** skills/dtb-idea-review/SKILL.md
- **Input:** Weichen-Textentwurf (Muster aus Discovery: 1 Satz Einschaetzung + Begruendung + 3 Antworten)
- **Output:** Aktion "Ausarbeiten" (Z. 72-87) erweitert: Groesseneinschaetzung mit Vorschlag
  (operative Aufgabe → dtb:task; klein → dtb:feature-fast; sonst → dtb:feature-discover),
  immer Nutzer-Bestaetigung; Frontmatter `next` → `[dtb:feature-discover, dtb:feature-fast, dtb:task]`;
  vorab repo-weiter Grep nach `idea-review`-Referenzen ausserhalb der Frontmatter (L3)

#### Schritt 2.2: feature-discover Umleitungs-Angebot
- **Zweck:** Zweite Weiche fuer Faelle, die direkt in der Discovery landen
- **Dateien:** skills/dtb-feature-discover/SKILL.md
- **Input:** Kleinfall-Heuristik (analog Weiche 1)
- **Output:** Schritt 1 ergaenzt: wirkt die geladene Idee klein → Umleitung auf
  `/dtb:feature-fast` anbieten (Vorschlag + Bestaetigung, kein Automatismus); Ablehnung →
  Discovery laeuft normal weiter

#### Schritt 2.3: Wartungs-Hinweise in den drei Quell-Skills
- **Zweck:** Kopplung sichtbar machen (Spec: einzige Aenderung an den Quellen)
- **Dateien:** skills/dtb-feature-discover/SKILL.md, skills/dtb-feature-plan/SKILL.md, skills/dtb-impl-plan/SKILL.md
- **Input:** bestehendes Hinweis-Muster (Format-Kopplung feature-discover ↔ impl-plan)
- **Output:** je ein Blockquote-Hinweis an der Template-Sektion: "Dieses Template wird von
  `dtb:feature-fast` als Struktur-Anker referenziert — bei Umbenennung/Umbau der Sektion den
  Struktur-Check dort mitziehen"; Templates selbst unveraendert

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Dreier-Weiche in idea-review, Umleitung in feature-discover, 3 Wartungs-Hinweise

### Checkpoint-Kriterien

#### Automated
- [ ] Grep skills/dtb-idea-review/SKILL.md Frontmatter: `next:` enthaelt `dtb:feature-fast` und `dtb:task`
- [ ] Grep skills/dtb-idea-review/SKILL.md Aktion "Ausarbeiten": Dreier-Weiche-Block vorhanden (Task/Fast-Track/Voll-Schiene)
- [ ] Grep skills/dtb-feature-discover/SKILL.md Schritt 1: Umleitungs-Angebot auf `dtb:feature-fast` vorhanden
- [ ] Grep `dtb:feature-fast` je einmal an der Template-Sektion von feature-discover, feature-plan, impl-plan (Wartungs-Hinweis; Anker: Blockquote, nicht Datei-weit — L8)

#### Manual
- [ ] Weichen-Texte sprachlich rund und im Ton der bestehenden Skill-Dialoge

---

## Phase 3: Doku + Distribution + E2E-Probelauf

### Ziel
Der Skill ist dokumentiert, verteilt und einmal komplett real durchlaufen — inklusive
der Sonderpfade (Weichen-Routing, Wiederaufnahme, Eskalation).

### Schritte

#### Schritt 3.1: CLAUDE.md ergaenzen
- **Zweck:** Kit-Doku aktuell halten
- **Dateien:** CLAUDE.md (Repo-Root)
- **Input:** Skill-Kategorien-Sektion
- **Output:** feature-fast in der "Feature workflow"-Zeile + 1-Satz-Beschreibung im
  Lifecycle-Absatz (Fast-Track als Alternative ab reviewtem Kleinfall)

#### Schritt 3.2: Distribution (vorgezogen)
- **Zweck:** Der Probelauf ruft die INSTALLIERTE Kopie auf — Distribution muss davor
  liegen (plan-review Befund 2); Skill auf beide Maschinen bringen
- **Dateien:** ~/.claude/skills/dtb-feature-fast/SKILL.md, ~/.claude/dtb-lock.json
- **Input:** dtb:kit-sync (Klasse-A-Muster erfasst den Skill automatisch)
- **Output:** `/dtb:kit-sync sync` gelaufen (Lock-Eintrag vorhanden, kein Drift);
  Hinweis: fuer die Aufrufbarkeit der frisch installierten Kopie ggf. frische Session
  starten (Verfuegbarkeits-Verhalten ist unbekannt — Senior-Dev Unknown Unknown 3)

#### Schritt 3.3: E2E-Probelauf (zweiteilig + Provokationen) + Gesundheitscheck
- **Zweck:** Beide neuen Mechaniken an echten Backlog-Items beweisen; Sonderpfade nicht
  dem Erstgebrauch ueberlassen (Entscheid plan-review 2026-08-01)
- **Dateien:** dtb-project/project-workflows/features/fach-agenda/ (entsteht im Lauf), INBOX.md
- **Input:** Inbox #28 (Weichen-Test), #25 (Fast-Track-Pilot), #35 (Eskalations-Kandidat)
- **Output:** (a) **Weichen-Test:** #28 durch die Dreier-Weiche — erwartet: Task-Routing-
  Vorschlag (`dtb:task`), Weiche trifft die ehrliche Einstufung; (b) **Fast-Track-Pilot:**
  #25 (fach-agenda) komplett: Weiche → max. 3 Kernfragen → Sammelvorlage → Ok → drei
  Artefakte; dabei einmal absichtlich VOR dem Ok abbrechen → Wiederaufnahme ueber
  fast-draft.md pruefen, dann fortsetzen; Verifikation: impl-plan-Gate-Bedingung erfuellt,
  plan.md-Kopf `Status: Entwurf` in Zeile ≤10, `## Progress` §2-konform; (c) **Eskalations-
  Provokation:** Lauf mit #35 — erwartet: Empfehlung Voll-Schiene an den benannten
  Schwellen, Abbruch ohne Artefakte; (d) `/dtb:project-health` gegen die Phase-1-Baseline;
  Befunde fliessen als Skill-Korrekturen zurueck (danach erneut kit-sync)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] CLAUDE.md aktuell, Skill verteilt, Weichen-Test + kompletter Fast-Track-Lauf + beide Sonderpfade dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] Grep CLAUDE.md: `feature-fast` in der Feature-workflow-Zeile
- [ ] `/dtb:kit-sync check`: dtb-feature-fast im Lock, Status synced (kein Drift)
- [ ] `features/fach-agenda/` enthaelt discovery.md + spec.md + plan.md und KEIN fast-draft.md mehr; Grep plan.md: `**Status:** Entwurf` innerhalb der ersten 10 Zeilen; `## Progress` vorhanden
- [ ] `/dtb:project-health`: keine neuen Befunde gegenueber der Phase-1-Baseline

#### Manual
- [ ] Weichen-Test #28: Task-Routing wurde vorgeschlagen und war nachvollziehbar begruendet
- [ ] Sonderpfade: Wiederaufnahme nach Abbruch wurde angeboten; Eskalations-Empfehlung bei #35 kam an den benannten Schwellen
- [ ] Sammelvorlage-UX im #25-Lauf: als Nutzer akzeptiert (Vetos praktikabel, nichts Wichtiges verdeckt)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Zwischenspeicher-Ablage | a) `features/{slug}/fast-draft.md`, b) Scratchpad ausserhalb, c) Marker in discovery.md | a, committet | Reist mit dem Change-Ordner — wird committet/gepusht fuer maschinenuebergreifende Wiederaufnahme (Entscheid plan-review 2026-08-01), nach Ok geloescht; kein bekannter Artefakt-Typ der Statusableitung → beeinflusst Derived State nicht |
| Struktur-Check-Anker | Ueberschriften-Grep vs. Zeilennummern | Ueberschriften-Grep (3 benannte Anker) | Zeilennummern driften bei jeder Aenderung; Sektions-Ueberschriften sind die stabilste Referenz (L2: Anker auf Wirkstelle) |
| Template-Quelle zur Laufzeit | installierte Kopien `~/.claude/skills/` vs. Kit-Repo | installierte Kopien | Zielprojekt-Realitaet (Kit-Repo dort nicht vorhanden); kit-sync haelt Klasse A synchron (Discovery-Entscheid) |
| idea-review `next`-Liste | nur feature-fast ergaenzen vs. auch dtb:task | beide | Die Dreier-Weiche routet real in beide Ziele; pipeline-graph soll die echten Kanten zeigen |
| Probelauf-Gegenstand | Wegwerf-Testidee vs. #28 allein vs. Aufteilung | #28 Weichen-Test + #25 Fast-Track-Pilot (+#35 Eskalations-Provokation) | #28 ist ehrlich eingestuft ein Task — die eigene Weiche wuerde ihn dorthin routen (plan-review Befund); #25 (fach-agenda) ist ein echtes kleines Feature und testet den Kernpfad komplett; #35 ist erkennbar KEIN Kleinfall und provoziert die Eskalation |
| Spec-Lint im Fast-Track | Lint-Kopie vs. Referenz auf feature-plan-Sektion | Referenz | Keine dritte Lint-Kopie (feature-plan ↔ greenfield-prd sind schon bewusst gedoppelt); Fast-Track verweist auf die Sektion in der installierten feature-plan-Kopie |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [ ] 1.1 Skill-Geruest + Eingangs-Gate
- [ ] 1.2 Struktur-Check Template-Quellen
- [ ] 1.3 Erhebungs-Kern (Defaults + Kernfragen)
- [ ] 1.4 Sammelvorlage + Veto + Zwischenspeicher
- [ ] 1.5 Schreibphase + Eskalation
- [ ] 2.1 idea-review Dreier-Weiche
- [ ] 2.2 feature-discover Umleitung
- [ ] 2.3 Wartungs-Hinweise Quell-Skills
- [ ] 3.1 CLAUDE.md ergaenzen
- [ ] 3.2 Distribution (kit-sync)
- [ ] 3.3 E2E-Probelauf (#28/#25/#35) + Gesundheitscheck

---

## Umsetzung

Umsetzung mit `/dtb:implement feature-fast` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/feature-fast/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
