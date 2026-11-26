# Implementierungsplan: Skill-Beschreibungen kürzen und abgrenzen

**Erstellt:** 2026-11-26
**Feature-Spec:** `features/skill-beschreibungen/spec.md`
**Geschaetzte Dauer:** 1–1,5 h
**Status:** Reviewed (plan-review 2026-11-26: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Regel festlegen, Beschreibungen kürzen und abgrenzen | 1–1,5 h | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/CLAUDE.md` | :11 Template-Zeile `Use when: "<trigger phrases>". <English summary …>.`; :26 Feldbeschreibung „starts with `Use when:` trigger phrases (German), ends with English summary" — Form, keine Länge |
| `skills/dtb-session-summary/SKILL.md` | 1128 Zeichen; beginnt mit „Use when the user wants…" (kein `Use when:`); Modus-Tabelle schon im Body :38-44; hat einen „Do NOT use for"-Satz |
| `skills/dtb-idea-rank/SKILL.md` | 655 Zeichen; Spalten-/Stufen-Aufzählung, im Body ab :135 und :227 ausgeführt; hat „Not for"-Satz |
| `skills/dtb-no-loss-check/SKILL.md` | 543 Zeichen; Proaktiv-Satz „Trigger this proactively …" am Ende |
| `skills/dtb-project-dashboard/SKILL.md` | 358 Zeichen; Inhaltsliste in Klammern; kein „Not for" |
| `skills/dtb-workflow-next/SKILL.md` | 227 Zeichen; Auslöser „was steht an", „naechster Schritt", „wo war ich"; kein „Not for" |
| `skills/dtb-workflow-status/SKILL.md` | 261 Zeichen; Auslöser „Pipeline", „wo steckt was", „Queue Status"; kein „Not for" |
| `skills/dtb-backlog-status/SKILL.md` | 210 Zeichen; Auslöser „offene Features", „Backlog zeigen"; kein „Not for" |

Messbasis: gefalteter Text (Zeilenumbrüche + Einrückung = ein Leerzeichen), gemessen 2026-11-26.

---

## Phase 1: Regel festlegen, Beschreibungen kürzen und abgrenzen

### Ziel
Alle zehn vom Modell aufrufbaren Skills haben eine Beschreibung ≤ 350 Zeichen in der Form
`Use when:`-Phrasen + ein Satz Zweck + ggf. `Not for`-Satz; die vier Status-Skills schließen
sich gegenseitig aus; die Regel steht in `skills/CLAUDE.md`.

### Schritte

#### Schritt 1.1: Regel in skills/CLAUDE.md + Prüfskript
- **Zweck:** Die Länge und die Abgrenzungsform festschreiben, bevor Texte geändert werden — und das Werkzeug bereitstellen, das sie misst.
- **Dateien:** `skills/CLAUDE.md` (Template-Zeile :11 um den optionalen `Not for … (that is dtb:X).`-Satz ergänzen; Feldbeschreibung :26 um: Grenze höchstens 350 Zeichen gefalteter Text (Kit-Maß, kein Plattformlimit), verbindlich für `disable-model-invocation: false`, Form Phrasen + ein Satz Zweck + „Not for"-Satz bei Überschneidung, Modus-/Ausgabe-Details in den Body, Begründung: diese Beschreibungen laden in jede Session; Freigabe-Moment: wer `disable-model-invocation` auf `false` setzt, prüft die Länge im selben Zug — Bezug Inbox #181 a). Prüfskript `desc-check.py` im Scratchpad der Session (per Write-Tool, nie inline — Lektion 91; `python -I`, Ausgabe-Encoding im Skript setzen — Lektion 92)
- **Input:** Ist-Analyse oben
- **Output:** Regeltext; Prüfskript, das je aufrufbarem Skill meldet: Länge (gefaltet), `Use when:`-Präfix, bei den vier Status-Skills `Not for` vorhanden, jedes `dtb:X` im `Not for`-Satz als `skills/dtb-X/` vorhanden; dazu die Liste der Auslöser-Phrasen (Text in Anführungszeichen im `description`-Feld), die gegenüber `git show $(git merge-base master HEAD):{pfad}` fehlen (Lektion 85). Exit 0 nur, wenn Länge, Präfix und Verweise grün sind; die Phrasenliste ist Information für das Manual-Kriterium. **Formprüfung:** das Skript verlangt `description: >-` mit eingerückten Folgezeilen und meldet jede andere Form als Fehler (PyYAML fehlt, das Skript zerlegt den Block selbst). **Positivprobe (Lektion 130):** vor der ersten Textänderung das Skript einmal gegen den merge-base-Stand laufen lassen (Dateien per `git show $(git merge-base master HEAD):{pfad}` lesen) — es muss mindestens session-summary mit 1128 Zeichen und fehlendem `Use when:`-Präfix als Fehler melden; Ausgabe in `### Abnahme-Beleg` eintragen. Erst danach zählt „Exit 0" als Befund

#### Schritt 1.2: session-summary, idea-rank, no-loss-check kürzen
- **Zweck:** Die drei größten Beschreibungen unter die Grenze bringen, ohne einen Auslöse-Anlass zu verlieren.
- **Dateien:** `skills/dtb-session-summary/SKILL.md`, `skills/dtb-idea-rank/SKILL.md`, `skills/dtb-no-loss-check/SKILL.md` (nur das `description`-Feld)
- **Input:** Regel aus 1.1; Body-Fundstellen der wegfallenden Details (Ist-Analyse)
- **Output:** session-summary mit `Use when:`-Präfix, Phrasen zusammengelegt (je ein Vertreter für Session / Tag / Woche), kurzer `Not for`-Satz (Checkpoint, workflow-next); idea-rank ohne Spalten-/Stufen-Aufzählung, `Not for`-Satz bleibt; no-loss-check mit gekürztem Proaktiv-Satz. Nur streichen, was nachweislich im Body steht; fehlt ein Detail dort → anhalten und nachfragen, nicht in den Body schreiben (Kriterium 4 erlaubt nur Änderungen im `description`-Feld)

#### Schritt 1.3: vier Status-Skills abgrenzen
- **Zweck:** Die überschneidenden Auslöser („was steht an" / „wo steckt was" / „offene Features" / „Projektstand als Seite") eindeutig einem Skill zuordnen.
- **Dateien:** `skills/dtb-workflow-next/SKILL.md`, `skills/dtb-workflow-status/SKILL.md`, `skills/dtb-backlog-status/SKILL.md`, `skills/dtb-project-dashboard/SKILL.md` (nur das `description`-Feld)
- **Input:** Abgrenzung: workflow-next = nächste Aktion je Feature; workflow-status = Pipeline und Warteschlangen; backlog-status = Backlog-Liste mit Prioritäten; project-dashboard = Projektstand als HTML-Seite
- **Output:** je ein `Not for … (that is dtb:X)`-Satz mit Verweis auf die Nachbarn; project-dashboard zugleich gekürzt (Inhaltsliste streichen — sie steht im Body; fehlt etwas → anhalten und nachfragen). Danach den eigenen neuen Text gegen die Fehlerklasse lesen (Lektion 15): Überschneidet sich eine neue Formulierung mit einem Nachbarn? Zum Abschluss Skriptausgabe und Liste der gestrichenen bzw. zusammengelegten Phrasen in `### Abnahme-Beleg` (unten in Phase 1) eintragen

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Regel in `skills/CLAUDE.md` (:11 und :26)
- [ ] Sieben geänderte `description`-Felder
- [ ] Ausgabe des Prüfskripts inkl. Phrasenliste (Ablageort: `### Abnahme-Beleg` in diesem Plan)

### Checkpoint-Kriterien

#### Automated
- [ ] Positivprobe gegen den merge-base-Stand hat rot gemeldet (mindestens session-summary: Länge 1128 und fehlendes `Use when:`-Präfix) — Ausgabe in `### Abnahme-Beleg`
- [ ] Prüfskript `desc-check.py` endet mit Exit 0: alle zehn Skills mit `disable-model-invocation: false` haben ≤ 350 Zeichen (gefaltet) und beginnen mit `Use when:`; die vier Status-Skills enthalten `Not for`; jedes `dtb:X` im `Not for`-Satz existiert als `skills/dtb-X/`
- [ ] Grep auf `skills/CLAUDE.md`, verankert auf die Feldbeschreibung (`^- \*\*description\*\*:`): die Zeile nennt `350`, `Not for` und `disable-model-invocation`
- [ ] `git diff $(git merge-base master HEAD) --stat -- skills/` zeigt genau die acht erwarteten Dateien (`skills/CLAUDE.md` + sieben SKILL.md), sonst nichts
- [ ] In den sieben SKILL.md hat sich nur das `description`-Feld geändert: `git diff $(git merge-base master HEAD) -- skills/dtb-*/SKILL.md` zeigt keine Hunks hinter der schließenden Frontmatter-Grenze `---` der jeweiligen Datei (Grenze je Datei per `awk 'NR>1&&/^---/{print NR;exit}'` ermitteln — sie liegt zwischen Zeile 15 und 31)

#### Manual
- [ ] Der Mensch liest die sieben neuen Beschreibungen gegen und bestätigt die Liste der weggefallenen bzw. zusammengelegten Auslöser-Phrasen in `### Abnahme-Beleg` als abgedeckt

### Abnahme-Beleg

> Schritt 1.1 trägt die Ausgabe der Positivprobe ein; Schritt 1.3 ergänzt die Ausgabe von `desc-check.py` und Liste der gestrichenen bzw. zusammengelegten Auslöser-Phrasen je Skill.

**Positivprobe 2026-11-26** — `python -I desc-check.py --ref fa083f5` (merge-base), vor der ersten Textänderung, Exit 1:

```
Quelle: git fa083f5  (Grenze 350)
  ROT dtb-backlog-status             210  'Not for' fehlt
  ROT dtb-idea-rank                  655  Laenge 655 > 350
  OK  dtb-lesson                     305
  OK  dtb-meeting-agenda             299
  ROT dtb-no-loss-check              543  Laenge 543 > 350
  OK  dtb-open-question              296
  ROT dtb-project-dashboard          358  Laenge 358 > 350; 'Not for' fehlt
  ROT dtb-session-summary           1128  Laenge 1128 > 350; Praefix 'Use when:' fehlt
  ROT dtb-workflow-next              227  'Not for' fehlt
  ROT dtb-workflow-status            261  'Not for' fehlt
Geprueft: 10 Skills mit disable-model-invocation: false — Fehler: 9
```

**Endlauf 2026-11-26** — `python -I desc-check.py` (Arbeitsbaum, Phrasen gegen merge-base `fa083f5`), nach Schritt 1.3, Exit 0:

```
Quelle: Arbeitsbaum  (Grenze 350)
  OK  dtb-backlog-status             312
  OK  dtb-idea-rank                  316
  OK  dtb-lesson                     305
  OK  dtb-meeting-agenda             299
  OK  dtb-no-loss-check              335
  OK  dtb-open-question              296
  OK  dtb-project-dashboard          330
  OK  dtb-session-summary            344
        - Phrase entfallen/geaendert: "was haben wir (heute / diese session) gemacht/erreicht/geschafft"
        - Phrase entfallen/geaendert: "gib mir einen recap / kurzen ueberblick"
        - Phrase entfallen/geaendert: "was hab ich am <Datum> gemacht"
        - Phrase entfallen/geaendert: "was lief diese woche"
        - Phrase entfallen/geaendert: "uebersicht der arbeit der letzten 7 tage"
        - Phrase entfallen/geaendert: "woche"
        - Phrase entfallen/geaendert: "week"
  OK  dtb-workflow-next              315
  OK  dtb-workflow-status            307
Geprueft: 10 Skills mit disable-model-invocation: false — Fehler: 0
```

**Phrasenliste zur Abnahme (session-summary)** — wie der Anlass abgedeckt bleibt:

| Entfallen | Abgedeckt durch |
|-----------|-----------------|
| „was haben wir (heute / diese session) gemacht/erreicht/geschafft" | „was haben wir heute gemacht" + „fass die session zusammen" |
| „gib mir einen recap / kurzen ueberblick" | „recap" |
| „was hab ich am <Datum> gemacht" | „zusammenfassung vom 2026-06-12" + Zweck-Satz „one day" |
| „was lief diese woche" | „wochenrueckblick" + Zweck-Satz „the last 7 days" |
| „uebersicht der arbeit der letzten 7 tage" | „wochenrueckblick" + Zweck-Satz „the last 7 days" |
| „woche" / „week" | kein Auslöser, sondern Argumentname — steht in `argument-hint` und in der Modus-Tabelle des Body |

Weitere Streichungen ohne Phrasenbezug: session-summary verliert „Trigger this proactively for any retrospective recap" (Auslöse-Hinweis; der Zweck-Satz „recap of work done" trägt den Anlass) und die Aufzählung „PDF, git diff, git log, application log" — in der ersten Fassung als „verdichtet zu summarizing documents" bezeichnet; das war ungenau (git diff/git log sind keine Dokumente, Ausschluss war entfallen). Nach impl-review F1 (2026-11-26) steht er wieder: „summarizing documents, diffs or git logs"; „application log" bleibt entfallen (von „logs" mitgetragen). no-loss-check verliert die Begründung „the loss … happens precisely in sessions that end without a checkpoint"; die erste Fassung hatte daraus die nicht wissbare Bedingung „ends without a checkpoint" gemacht — nach impl-review F2 wieder „seems to be ending or the topic shifts". Die übrigen gestrichenen Details stehen im Body (Ist-Analyse; workflow-status `:20`).

**Abgrenzung des Dashboards (impl-review F3):** workflow-status und backlog-status nennen project-dashboard nicht; der Ausschluss läuft über den eigenen Satz des Dashboards („Not for a chat answer (that is dtb:workflow-next, dtb:workflow-status or dtb:backlog-status)"), weil ein weiterer Satz backlog-status über 350 Zeichen brächte.

**Endlauf nach Triage 2026-11-26** — `desc-check.py` Exit 0: backlog-status 312, idea-rank 316, lesson 305, meeting-agenda 299, no-loss-check 329, open-question 296, project-dashboard 318, session-summary 338, workflow-next 322, workflow-status 307; Phrasenliste unverändert gegenüber dem Endlauf oben.

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Geltungsbereich der Grenze | alle Skills / nur aufrufbare | nur `disable-model-invocation: false` | Nur diese zehn laden ihre Beschreibung in jede Session; per Veto-Vorlage bestätigt 2026-11-26 |
| Messbasis | Rohtext / gefalteter Text | gefalteter Text | Das Modell sieht den gefalteten YAML-Wert, nicht die Einrückung |
| Ort der Regel | neuer Abschnitt / Feldbeschreibung erweitern | Feldbeschreibung :26 + Template :11 | Die Form-Regel steht schon dort; kein zweiter Ort |
| Phrasen-Erhalt | wörtlich / Anlass abgedeckt | Anlass abgedeckt, vom Menschen bestätigt | Wörtlicher Erhalt passt bei session-summary nicht unter 350 Zeichen |
| Prüfskript | ins Repo / Scratchpad | Scratchpad | Repo-Skript ist Inbox #214; hier nur Abnahme-Werkzeug |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Regel + Prüfskript — `0bc7190`
- [x] 1.2 drei Beschreibungen kürzen — `0bc7190`
- [x] 1.3 vier Status-Skills abgrenzen — `0bc7190`

---

## Umsetzung

Umsetzung mit `/dtb:implement skill-beschreibungen` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/skill-beschreibungen/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
