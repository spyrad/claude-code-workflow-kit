# Implementierungsplan: idea-rank-schiene

**Erstellt:** 2026-10-29
**Feature-Spec:** `features/idea-rank-schiene/spec.md`
**Geschaetzte Dauer:** 4–6 h
**Status:** Reviewed (plan-review 2026-10-29: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Einstufung im Skill (Beispiel zuerst) | 3–4 h | Geplant |
| Phase 2 | Kopplung, Kit-Doku, Probelauf | 1–2 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Modul-Liste per Grep verifiziert 2026-10-29).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-idea-rank/SKILL.md` | 345 Zeilen; Tabelle `# / Idee (kurz) / Aufwand / Wichtigkeit / Bemerkung` (Schritt 5, Zeile 270); Bewertung in 4.3, Sortierung 4.4; Bemerkung in vier Teilen (Zeile 288 ff.); `allowed-tools: Read, Glob, Grep`; kein Struktur-Check vorhanden |
| `skills/dtb-idea-review/SKILL.md` | Dreier-Weiche unter `**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**` (Zeile 144), Tabelle Einstufung/Heuristik/Schiene (Zeilen 149–153); kein Wartungs-Hinweis fuer Fremdleser |
| `skills/dtb-worker/SKILL.md` | Raster unter `### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)` (Zeile 69), vier Kriterien + Urteil ja/teilweise/nein (Zeilen 73–86); Zeile 71: „Schwester-Raster … docken hier als eigene Unterueberschrift an"; Zeile 66: Features mit Spec/Plan sind kein Worker-Material |
| `skills/dtb-feature-fast/SKILL.md` | Vorbild fuer den Struktur-Check: Aufloesung installierte Kopie → Projekt-Fallback, zwei getrennte Fehlerpfade (Schritt 2) |
| `CLAUDE.md` | Zeile 51: Beschreibung `idea-rank` ohne Schiene |
| `README.md` | Zeile 72: Skill-Tabelle `/dtb:idea-rank` ohne Schiene |

---

## Phase 1: Einstufung im Skill (Beispiel zuerst)

### Ziel
Die Rangliste stuft jede Idee nach Schiene und Worker-Tauglichkeit ein — die Ausgabeform ist an echten Daten abgenommen, bevor die Regeln im Skill stehen (Lektion L64).

### Schritte

#### Schritt 1.1: Beispiel-Ausgabe mit echten Daten
- **Zweck:** Ausgabeform (sieben Spalten, Bemerkungs-Teil `Worker: …`) am echten Inbox-Stand pruefen, bevor Regeln ausgearbeitet werden (L64)
- **Dateien:** `features/idea-rank-schiene/beispiel-ausgabe.md` (neu)
- **Input:** `INBOX.md` (alle `Offen`-Ideen), Dreier-Weiche (`skills/dtb-idea-review/SKILL.md`), Worker-Raster (`skills/dtb-worker/SKILL.md`), heutige Regeln in `skills/dtb-idea-rank/SKILL.md`
- **Output:** vollstaendige Rangliste in Zielform unter `## Beispiel {Datum}`; dem Nutzer im Chat zeigen und die Form bestaetigen lassen, BEVOR Schritt 1.2 beginnt (Zwischen-Gate; Ergebnis — beibehalten oder eine Spalte — als Zeile `Form-Entscheidung:` in der Datei festhalten); dazu die Zeilen-Reihenfolge nach dem heutigen Regeltext als Zeile `Reihenfolge-Basis: #a, #b, …` (Vergleichsbasis fuer 2.3b — der Skill ist dann schon umgebaut) und eine Zeile `Worker-Abdeckung: {n} Task-Ideen, davon {m} teilweise` (macht sichtbar, ob die Worker-Spalte und der Bemerkungs-Teil `Worker: …` (Teil 3) an echten Daten ueberhaupt geprobt werden)

#### Schritt 1.2: Struktur-Check auf die Regelquellen
- **Zweck:** beide Regelquellen vor ihrer ersten Nutzung pruefen (L89), ohne die Rangliste bei Ausfall zu opfern
- **Dateien:** `skills/dtb-idea-rank/SKILL.md`
- **Input:** Muster `skills/dtb-feature-fast/SKILL.md` Schritt 2; Anker `**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**` und `### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)`
- **Output:** neuer Abschnitt nach Schritt 3 (Querbelege): Aufloesung installierte Kopie `~/.claude/skills/dtb-*/SKILL.md` → Fallback `skills/dtb-*/SKILL.md`; Grep woertlich auf beide Anker; zwei getrennte Fehlerpfade (Datei fehlt → `/dtb:kit-sync`; Anker fehlt → Drift) mit je genau einer ⚠-Zeile; „Datei fehlt" nur, wenn beide Aufloesungen leer sind — ein Werkzeugfehler ist kein Befund (L7); betroffene Spalte zeigt dann `?`; benanntes Restrisiko (Anker-Existenz, nicht Inhalt)

#### Schritt 1.3: Einstufungsregeln und Ausgabeform
- **Zweck:** Regeln fuer Schiene und Worker festschreiben, Ausgabe auf die in 1.1 abgenommene Form ziehen
- **Dateien:** `skills/dtb-idea-rank/SKILL.md`
- **Input:** Form-Entscheidung aus 1.1, Struktur-Check aus 1.2
- **Output:** neuer Abschnitt `### 4.5 Schiene und Worker` (Regeln per Referenz auf die gelesenen Quellen; Worker nur bei `Task`, sonst `—`; Grundsatzfrage → Entscheidungsarbeit, Default `Voll-Schiene`; Aufwand `3+ Tage` nie `Fast-Track`; Grenzfall groessere Schiene / schwaecheres Worker-Urteil; `(Rest)` bewertet nur den Rest; keine Wirkung auf 4.4); Schritt 5: Template-Kopf und Spaltenbeschreibung, neuer Bemerkungs-Teil `Worker: {fehlendes Kriterium}` als Teil 3 (nach dem Grund der Wichtigkeit, vor der Reihenfolge; die bisherigen Teile 3 und 4 ruecken auf 4 und 5); Abschnitt `## Wichtig` um „Einstufung ist Vorschlag, der Review entscheidet"; description und Einleitungsabsatz nachziehen

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `features/idea-rank-schiene/beispiel-ausgabe.md` mit abgenommener Form
- [ ] `skills/dtb-idea-rank/SKILL.md` mit Struktur-Check, 4.5 und neuer Ausgabeform

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^## Beispiel ' dtb-project/project-workflows/features/idea-rank-schiene/beispiel-ausgabe.md` ≥ 1 und `grep -c '^Form-Entscheidung:' …/beispiel-ausgabe.md` = 1 und `grep -c '^Reihenfolge-Basis:' …/beispiel-ausgabe.md` = 1
- [ ] `grep -cF '**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**' skills/dtb-idea-rank/SKILL.md` ≥ 1 und `grep -cF '### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)' skills/dtb-idea-rank/SKILL.md` ≥ 1 (Anker im Struktur-Check genannt)
- [ ] `grep -c '^### 4.5 Schiene und Worker' skills/dtb-idea-rank/SKILL.md` = 1
- [ ] Template-Kopf in Schritt 5 traegt die abgenommene Form: bei sieben Spalten `grep -cF '| # | Idee (kurz) | Aufwand | Schiene | Worker | Wichtigkeit | Bemerkung |' skills/dtb-idea-rank/SKILL.md` = 1 (bei Form-Entscheidung „eine Spalte" den Kopf laut `Form-Entscheidung:` greppen)
- [ ] `grep -c '^allowed-tools: Read, Glob, Grep$' skills/dtb-idea-rank/SKILL.md` = 1 (unveraendert, L75)

#### Manual
- [ ] Beispiel-Ausgabe aus 1.1 vom Nutzer als lesbar abgenommen (vor 1.2)
- [ ] Regeltext 4.5 widerspruchsfrei zu Dreier-Weiche und Worker-Raster (Text-Review, L14)

---

## Phase 2: Kopplung, Kit-Doku, Probelauf

### Ziel
Die Quellen kennen ihren neuen Leser, die Kit-Doku beschreibt die erweiterte Sicht, und ein Probelauf gegen die Repo-Fassung belegt die Einstufung an echten Daten.

### Schritte

#### Schritt 2.1: Wartungs-Hinweise an den Quellen
- **Zweck:** Wer Dreier-Weiche oder Worker-Raster umbaut, sieht die Kopplung (Kopplungs-Hinweise-Regel `skills/CLAUDE.md`)
- **Dateien:** `skills/dtb-idea-review/SKILL.md`, `skills/dtb-worker/SKILL.md`
- **Input:** Wortlaut der Wartungs-Hinweise in `skills/dtb-feature-discover/SKILL.md` Schritt 6 (Vorbild)
- **Output:** je ein Blockzitat `> **Wartungs-Hinweis (Struktur-Anker):** … von `dtb:idea-rank` als Struktur-Anker referenziert …` direkt unter dem jeweiligen Anker

#### Schritt 2.2: Kit-Doku nachziehen
- **Zweck:** Die Kit-Doku beschreibt die Schienen- und Worker-Spalten (L3: alle Fundstellen per Grep erhoben)
- **Dateien:** `CLAUDE.md` (Zeile 51), `README.md` (Zeile 72)
- **Input:** Fundstellen-Liste aus der Discovery; vor dem Schreiben erneut `grep -rn 'idea-rank' CLAUDE.md README.md skills/*/SKILL.md` gegen Neuzugaenge
- **Output:** beide Beschreibungen nennen Schiene (Task / Fast-Track / Voll-Schiene) und Worker-Tauglichkeit

#### Schritt 2.3: Probelauf gegen die Repo-Fassung
- **Zweck:** Einstufung und Fehlerpfade an der Repo-Fassung belegen, nie an der installierten Kopie (L74)
- **Dateien:** `features/idea-rank-schiene/beispiel-ausgabe.md` (Ablage, L20)
- **Input:** `skills/dtb-idea-rank/SKILL.md` (Repo-Fassung), echter `INBOX.md`-Stand
- **Output:** Abschnitt `## Probelauf {Datum}` mit (a) Rangliste nach dem neuen Regeltext, (b) Vergleich der Zeilen-Reihenfolge mit der Zeile `Reihenfolge-Basis:` aus 1.1 (muss gleich sein; der Inbox-Stand im Worktree ist zwischen 1.1 und 2.3 unveraendert), (c) Schreibtisch-Probe beider Fehlerpfade — die Aufloesung bevorzugt die installierte Kopie, deshalb lenkt der Probelauf die Quellpfade ausdruecklich auf selbst erzeugte Scratchpad-Objekte um (L57); installierte Kopien unter `~/.claude/` bleiben unberuehrt (L54): (i) nicht existenter Pfad → Installations-Hinweis, (ii) Kopie einer Quelle ohne Anker → Drift-Hinweis; je Pfad erwartet `?` in der betroffenen Spalte + genau eine ⚠-Zeile, Ergebnis je Pfad dokumentiert

### Deliverables
- [ ] Wartungs-Hinweise in beiden Quellen
- [ ] Kit-Doku nachgezogen
- [ ] Probelauf dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'von `dtb:idea-rank` als Struktur-Anker' skills/dtb-idea-review/SKILL.md` = 1 und dasselbe fuer `skills/dtb-worker/SKILL.md` = 1
- [ ] `grep -n '`idea-rank` (read-only' CLAUDE.md | grep -c 'Schiene'` = 1
- [ ] `grep -n '^| `/dtb:idea-rank`' README.md | grep -c 'Schiene'` = 1
- [ ] `grep -c '^## Probelauf ' dtb-project/project-workflows/features/idea-rank-schiene/beispiel-ausgabe.md` = 1

#### Manual
- [ ] Probelauf vom Nutzer abgenommen: Schiene und Worker je Zeile plausibel, Reihenfolge unveraendert, beide Fehlerpfade der Schreibtisch-Probe (Installation, Drift) zeigen den jeweils erwarteten Hinweis

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Kopplung an die Regelquellen | A: Kopie mit Wartungs-Hinweis · B: Referenz + Struktur-Check | B | Keine dritte Fassung der Dreier-Weiche; beide Quellen sind Klasse-A-Skills und in Zielprojekten global installiert (L82 greift nicht); Muster aus feature-fast/pane-start; per Veto-Vorlage bestaetigt 2026-10-29 |
| Ausgabeform | A: zwei Spalten · B: eine kombinierte Spalte | A (vorlaeufig) | Getrennt besser scanbar; endgueltig am Manual-Gate 1.1 |
| Worker-Urteil | A: alle Ideen · B: nur Schiene `Task` | B | `dtb:worker` selbst: Features mit Spec/Plan sind kein Worker-Material, taugliche Ideen gehen zuerst ueber `/dtb:task`; per Veto-Vorlage bestaetigt 2026-10-29 |
| Ausfall einer Regelquelle | A: Abbruch · B: Rangliste mit `?` + ⚠-Zeile | B | Read-only-Sicht; Rangliste haengt nicht an den Quellen, nur die zwei Spalten; Fehlschlag wird nie als Befund ausgegeben (L7) |
| Quell-Skills in `consumes` | A: aufnehmen · B: nicht aufnehmen | B | Bestandsmuster: feature-fast und pane-start fuehren referenzierte Skills nicht in `consumes` (nur Artefakte) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Beispiel-Ausgabe mit echten Daten — `7e51cac`
- [x] 1.2 Struktur-Check auf die Regelquellen — `7e51cac`
- [x] 1.3 Einstufungsregeln und Ausgabeform — `7e51cac`
- [x] 2.1 Wartungs-Hinweise an den Quellen
- [x] 2.2 Kit-Doku nachziehen
- [x] 2.3 Probelauf gegen die Repo-Fassung

---

## Umsetzung

Umsetzung mit `/dtb:implement idea-rank-schiene` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/idea-rank-schiene/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-29)
