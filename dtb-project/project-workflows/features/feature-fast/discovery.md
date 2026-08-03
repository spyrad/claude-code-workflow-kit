# Discovery: Fast-Track-Schiene (dtb:feature-fast)
<!-- resume: done -->

**Erstellt:** 2026-08-01
**Idee-Referenz:** Inbox #37 — "Fast-Track-Schiene fuer kleine Features: neuer Kit-Skill `/dtb:feature-fast` (Name offen) als Orchestrator OHNE eigene Templates — buendelt discover/spec/impl-plan zu einem Durchgang mit Default-Annahmen und vetobarer Sammelvorlage; Artefakte, Derived State und beide Reviews bleiben unveraendert; Eingangsweiche 'Vorschlag + Bestaetigung' an idea-review und feature-discover."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-feature-fast/SKILL.md | NEU — der Orchestrator-Skill selbst (Name noch offen, Schritt 5) |
| skills/dtb-idea-review/SKILL.md | Weiche 1: Aktion "Ausarbeiten" (Z. 72-87) bekommt Groesseneinschaetzung + Fast-Track-Vorschlag; Frontmatter `next` (Z. 12) ergaenzen |
| skills/dtb-feature-discover/SKILL.md | Weiche 2: Schritt 1 erkennt Kleinfaelle und bietet die Umleitung an |
| skills/dtb-feature-plan/SKILL.md | Template-Quelle, vom Orchestrator nur referenziert — KEINE Aenderung (Kern des Designs) |
| skills/dtb-impl-plan/SKILL.md | Template-Quelle, nur referenziert — KEINE Aenderung; dessen Hard-Gate auf spec.md wird im selben Lauf erfuellt |
| CLAUDE.md | Skill-Kategorien-Liste ("Feature workflow") um den neuen Skill ergaenzen |

Bewusst nicht betroffen: `DERIVED_STATE_RULES.md` (Derived State unveraendert — Designentscheidung), `dtb:kit-sync` (Klasse-A-Muster erfasst den neuen Skill automatisch), `dtb:pipeline-graph`/`dtb:workflow-status` (generieren aus Frontmatter), `dtb:plan-review`/`dtb:impl-review` (laufen unveraendert nach).

---

## Anforderungen

### Scope
**Enthalten:**
- Neuer Orchestrator-Skill: buendelt die Interviews von feature-discover/feature-plan/impl-plan zu EINEM Durchgang mit begruendeten Default-Annahmen
- EINE Sammelvorlage vor dem Schreiben: Annahmen als eigener, prominenter Block, jede einzeln vetobar; erst nach Nutzer-Ok entstehen die Artefakte
- Alle drei Artefakte werden erzeugt (discovery.md, spec.md, plan.md inkl. `## Progress`) — volle Kompatibilitaet mit Derived State, Hard-Gates, plan-review/impl-review
- Eingangsweiche "Vorschlag + Bestaetigung" an zwei Stellen: idea-review (bei "Ausarbeiten") und feature-discover (Schritt 1)
- Keine eigenen Templates — die drei bestehenden SKILL.md bleiben Single Source
- Eskalationspfad in v1: geordneter Wechsel auf die Voll-Schiene mitten im Lauf (entstandene Artefakte bleiben gueltig, ab Wechselpunkt normal weiterfragen)

**Nicht enthalten:**
- Keine Aenderung an DERIVED_STATE_RULES.md, Hard-Gates oder den beiden Reviews
- Kein automatisches Routing ueber harte Kriterien (immer Mensch bestaetigt)
- Keine Artefakt-Verschmelzung, keine Review-Verschlankung (im Brainstorming 2026-08-01 verworfen)
- Kein Ad-hoc-Einstieg: INBOX-Eintrag ist Pflicht-Vorstufe (Idee muss erfasst sein, bevor der Fast-Track startet)

### Gewuenschtes Verhalten
- Erlebnis: EIN Aufruf → Skill arbeitet die drei Stationen selbst durch → EINE kompakte Sammelvorlage → ein Ok (oder gezielte Vetos) → Artefakte werden geschrieben. Gefuehlt eine Entscheidung statt ~15 Interviewfragen
- Fragen-Budget: der Skill darf VOR der Sammelvorlage maximal 3 gezielte Kernfragen stellen (nur bei echten Informationsluecken — eine falsche Kern-Annahme macht die ganze Vorlage wertlos); alle uebrigen Luecken werden zu markierten Annahmen
- Veto-Mechanik: Annahmen nummeriert (A1, A2, ...), Korrektur per Freitext ("A2: stattdessen ..."), alles Unkommentierte gilt als angenommen — kein Einzel-Abhaken
- Bestehende UX-Muster uebernehmen: "(Recommended)"-Muster an Auswahlpunkten (wie feature-discover Schritt 5), Bestaetigung vor dem Schreiben (wie open-question Variante B), Annahmen-Kennzeichnung verifiziert vs. Vermutung (Lektion aus Inbox #36 Pilot-Erkenntnis b)

### Randfaelle
- Slug-Kollision beim Anlegen des Change-Ordners → wie Voll-Schiene: melden, anderen Namen erfragen (DERIVED_STATE_RULES §4, kein Auto-Suffix)
- Zu duenne INBOX-Idee: reichen selbst 3 Kernfragen nicht fuer tragfaehige Defaults, empfiehlt der Skill die Voll-Schiene statt eine Vorlage voller Spekulation zu bauen
- Selbst-Eskalation: der Skill empfiehlt den Wechsel auf die Voll-Schiene, wenn sein eigener Entwurf Schwellen reisst (z.B. Plan braeuchte mehr als 2 Phasen oder mehr als ~5 Annahmen noetig) — Schwellwerte in der Spec festzulegen; zusaetzlich kann der Nutzer jederzeit eskalieren (v1-Scope)
- Abbruch vor dem Ok (z.B. Session-Ende vor Bestaetigung der Sammelvorlage): Skill speichert die Vorlage als Entwurfs-Datei zwischen (Wiederaufnahme-Muster analog Resume-Marker in feature-discover); Ablageort in der Spec festzulegen
- Idee mit bereits existierendem Change-Ordner (Voll-Schiene wurde frueher angefangen): vorhandene Artefakte werden uebernommen, nur die fehlenden vorbefuellt — kein Verweigern
- Hard-Gate-Reihenfolge: Schreibreihenfolge discovery → spec → plan (impl-plan-Gate auf spec.md wird im selben Lauf erfuellt)
- Groessen-Limits gelten weiter: spec.md/plan.md max. 500 Zeilen auch im Fast-Track

### Einschraenkungen
- Skill-Konventionen aus skills/CLAUDE.md gelten: Frontmatter-Pflichtfelder, `disable-model-invocation: true`, deutscher Skill-Body, Bash-Bloecke eigenstaendig, Pipeline-Block korrekt
- Distribution: in Zielprojekten liest der Orchestrator die drei Template-Quellen aus den INSTALLIERTEN Kopien unter `~/.claude/skills/` (nicht aus dem Kit-Repo); kit-sync haelt sie als Klasse A synchron
- Kopplungspunkt zweifach abgesichert (entschieden 2026-08-01): (1) Struktur-Check zur Laufzeit — vor dem Buendeln prueft der Orchestrator, ob die erwarteten Template-Anker in den drei SKILL.md existieren; fehlt ein Anker → Warnung und Stopp statt stilles Falsch-Buendeln; (2) Wartungs-Hinweis in den drei Quell-Skills ("dieses Template wird von dtb:feature-fast referenziert") — bewusste kleine Ausnahme von "keine Aenderung an Quell-Skills": Templates unangetastet, nur je ein Hinweis-Kommentar (Muster: Format-Kopplungs-Hinweis feature-discover Schritt 2 → impl-plan)
- Laengen-Budget der Sammelvorlage (entschieden 2026-08-01): Annahmen-Block max. ~10 nummerierte Annahmen — darueber zieht der Skill die Selbst-Eskalation (Annahmen-Zahl als Groessenindikator zusaetzlich zur Phasen-Schwelle >2); Vorlage insgesamt kompakt (Kurzfassung je Artefakt, nicht voller Wortlaut). Konkrete Schwellwerte (10 Annahmen, 2 Phasen) in der Spec als benannte Werte festhalten, damit plan-review sie pruefen kann
- Fachlich: Review-Disziplin (Stepwise-Einzelentscheidungen in plan-review/impl-review) bleibt unangetastet — der Fast-Track endet, wo die Reviews beginnen

### Integrationspunkte
- Schreibend betroffen: skills/dtb-idea-review/SKILL.md (Weiche 1) und skills/dtb-feature-discover/SKILL.md (Weiche 2); nur Hinweis-Kommentar: skills/dtb-feature-plan/SKILL.md + skills/dtb-impl-plan/SKILL.md (Template-Quellen); Doku: CLAUDE.md (Repo-Root)
- Pipeline-Anschluss: Frontmatter des neuen Skills `after: [dtb:idea-review]`, `next: [dtb:plan-review]` — nach dem Fast-Track laeuft die normale Review-Kette
- Lese-Skills (workflow-next, workflow-status, pipeline-graph) integrieren den Skill automatisch ueber Frontmatter + Artefakt-Ableitung (alle drei Artefakte entstehen normal)
- Dreier-Weiche in idea-review (entschieden 2026-08-01): Groesseneinschaetzung unterscheidet Task / Fast-Track / Voll-Schiene — erkennt auch "das ist gar kein Feature, sondern eine operative Aufgabe" und schlaegt dann dtb:task vor; immer Vorschlag + Bestaetigung. Loest die dtb:task-Abgrenzung (Offener Punkt 4 aus Inbox #37) direkt an der Weiche
- Externe Abhaengigkeiten: keine (reines Markdown-Kit)

---

## Abhaengigkeiten

- Keine Konflikte: kein aktives Feature arbeitet an idea-review oder feature-discover (den beiden schreibend betroffenen Dateien)
- Ueberschneidung mit plan-status-feld (abgeschlossen, 12/12): §7 DERIVED_STATE_RULES gilt — der Fast-Track legt den plan.md-Kopf mit `Status: Entwurf` an und fasst das Feld danach NIE an (einziger Pfleger bleibt dtb:plan-review)

---

## Offene Punkte

- Schwellwerte der Selbst-Eskalation final in der Spec benennen (Arbeitsstand: max. ~10 Annahmen, max. 2 Plan-Phasen) — als benannte Werte, damit plan-review sie pruefen kann
- Ablageort + Format der zwischengespeicherten Sammelvorlage bei Abbruch vor dem Ok (Wiederaufnahme-Mechanik) — Spec-Detail
- Struktur-Check konkretisieren: welche Anker-Abschnitte in den drei referenzierten SKILL.md werden geprueft (z.B. Schritt-6-Template in feature-discover) — Spec-/Plan-Detail
- Formulierung der beiden Weichen-Texte (idea-review Dreier-Weiche, feature-discover Schritt-1-Umleitung) — Spec-Detail

---

**Erstellt mit:** `/dtb:feature-discover`
