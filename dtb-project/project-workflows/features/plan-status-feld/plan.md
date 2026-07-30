# Implementierungsplan: plan-status-feld

**Erstellt:** 2026-07-30
**Feature-Spec:** `features/plan-status-feld/spec.md`
**Geschaetzte Dauer:** ~3,5 h (1 Session)
**Status:** Reviewed (plan-review 2026-07-30: REVISE → 3 WARNs behoben)

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Kanon & Doku-Fundament (Regel-§, Template, CLAUDE.md) | ~45 min | Geplant |
| Phase 2 | Pfleger: plan-review schreibt das Feld | ~60 min | Geplant |
| Phase 3 | Leser haerten (workflow-next, workflow-status) + Trockenlauf + Smoke-Test | ~65 min | Geplant |
| Phase 4 | Register & Distribution | ~30 min | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (uebernommen, Pfade verifiziert 2026-07-30).
> **Leitplanke (Wiedereinstieg):** Zeilennummern sind Stand 2026-07-30 und dienen nur der
> Orientierung — sie verschieben sich durch die eigenen Edits dieses Plans (Phase 1 aendert
> `impl-plan`, Phase 2 fuegt in `plan-review` einen ganzen Schritt ein). Beim Editieren
> **inhaltlich ankern** (Sektion, Tabellenzeilen-Kontext, Wortlaut), nie numerisch.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-impl-plan/SKILL.md` | Z. 102: Template-Kopf `**Status:** Entwurf / Reviewed / In Umsetzung / Abgeschlossen` — Entstehungsort des Felds; 2 der 4 Werte werden nie gesetzt |
| `skills/dtb-workflow-next/SKILL.md` | Z. 40 liest Feld aus ersten 10 Zeilen; Z. 53 `Entwurf → Review ausstehend` OHNE Checkbox-Guard (Z. 54 hat ihn); Z. 115 Beispiel-Output |
| `skills/dtb-workflow-status/SKILL.md` | Z. 49–50 Ableitung wartend/bereit; Z. 85 Gate `Reviewed ODER In Umsetzung` (letzterer Wert existiert nie); Z. 138/174 Visualisierung |
| `skills/dtb-backlog-status/SKILL.md` | Z. 43 nennt beide Werte nicht unterscheidend → kein Aenderungsbedarf (Nicht-Scope) |
| `skills/dtb-plan-review/SKILL.md` | Schreibt das Feld nirgends; Schritt 4 vergibt Verdikt (SOUND/REVISE/RETHINK), Schritt 5 bietet Anpassungen an → Traeger des Pflegers |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 2 zaehlt Sync-Ziele abschliessend — bleibt UNANGETASTET (expliziter Nicht-Integrationspunkt) |
| `skills/CLAUDE.md` | Z. 54: dokumentiert Feld-Konvention „Entwurf, Reviewed (first 10 lines)" |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | 0 Treffer fuer das Feld — steht komplett ausserhalb des Kanons; §6 war letzte Erweiterung (additiv) |
| `dtb-project/project-workflows/features/*/plan.md` | 4 Bestandskoepfe, alle `Reviewed` (2 mit Datum/Verdikt-Zusatz = gelebtes Vermerkformat) — konsistent, keine Migration noetig |

---

## Phase 1: Kanon & Doku-Fundament

### Ziel
Die Regeln existieren, BEVOR Schreiber und Leser sie umsetzen: Feld-Semantik kanonisiert,
Template gestrafft, Doku konsistent.

### Schritte

#### Schritt 1.1: Kanonisierung in DERIVED_STATE_RULES.md
- **Zweck:** Das Feld vom undefinierten Parallel-Status zum kanonisierten Anzeige-Feld machen
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** discovery.md (Randfall-Matrix, Wertematrix, Entscheidungen 3a–3e); Struktur der Regel-Datei sichten → §-Verortung entscheiden (offener Punkt aus der Spec)
- **Output:** Neuer §/Unterabschnitt: Feld = reiner Review-Nachweis; Definitionsfenster (die `**Status:**`-Zeile innerhalb der ersten 10 Zeilen, ausserhalb existiert kein Kopf-Statusfeld); Wertemenge `Entwurf`/`Reviewed`; Pfleger = plan-review (Wertematrix); Toleranz-Matrix der Leser (fehlend → wie Entwurf still, Altwerte `In Umsetzung`/`Abgeschlossen` → wie Reviewed still, unbekannt → wie fehlend + Hinweiszeile); manueller Flip nur als Ausnahme mit Vermerk-Pflicht `(manuell {Datum}: {Grund})`; Statusableitung (§1/§2) bleibt unberuehrt

#### Schritt 1.2: impl-plan-Template straffen
- **Zweck:** Nie gesetzte Werte aus der Welt schaffen — Umsetzungsstand ist Sache von `## Progress`
- **Dateien:** `skills/dtb-impl-plan/SKILL.md`
- **Input:** Z. 102 (Template-Kopf)
- **Output:** Wertemenge nur noch `Entwurf / Reviewed`; kurzer Hinweis im Template auf Pfleger plan-review + Kanon-§

#### Schritt 1.3: skills/CLAUDE.md nachziehen
- **Zweck:** Contributor-Doku konsistent zur neuen Regel
- **Dateien:** `skills/CLAUDE.md`
- **Input:** Z. 54 (plan.md-Zeile der Artefakt-Tabelle)
- **Output:** Zeile nennt Wertemenge (2 Werte), Pfleger plan-review und Kanon-Verweis

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Kanon-§ in DERIVED_STATE_RULES.md
- [ ] Gestrafftes Template + konsistente Doku

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "Kopf-Statusfeld" dtb-project/project-rules/DERIVED_STATE_RULES.md` ≥ 1 Treffer (neuer Kanon-Abschnitt)
- [ ] `grep -c "In Umsetzung" skills/dtb-impl-plan/SKILL.md` = 0
- [ ] `grep -n "plan-review" skills/CLAUDE.md` trifft in der plan.md-Tabellenzeile (Z. ~54, Pfleger benannt)

#### Manual
- [ ] §-Verortung passt zur Struktur der Regel-Datei (additiv, keine §-Kollision mit Bestand)

---

## Phase 2: Pfleger — plan-review schreibt das Feld

### Ziel
plan-review pflegt das Feld bei jedem Verdikt selbst; die Luecke „gelesen, nie geschrieben"
ist geschlossen.

### Schritte

#### Schritt 2.1: Schreibschritt mit Wertematrix
- **Zweck:** Kern des Features — der eine Pfleger
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Verdikt aus Schritt 4, Ausgang von Schritt 5 (Anpassungen angenommen/abgelehnt)
- **Output:** Neuer Schritt nach dem Anpassungs-Angebot: Feld gemaess Wertematrix setzen —
  SOUND → `Reviewed (plan-review {Datum}: SOUND)`;
  REVISE+behoben → `Reviewed (plan-review {Datum}: REVISE → {N} WARNs behoben)`;
  REVISE+offen → `Entwurf (plan-review {Datum}: REVISE — Findings offen)`;
  RETHINK → `Entwurf (plan-review {Datum}: RETHINK)`; still, ohne Bestaetigungsfrage.
  **Format verbindlich mit `plan-review`-Praefix** (Spec-Quelle; erstes Wort in der Klammer nennt
  den Urheber — traegt die manuelle Ausnahme `Reviewed (manuell {Datum}: {Grund})` semantisch mit)
- **Harte „behoben"-Bedingung (binaer, kein Ermessen):** `Reviewed` NUR, wenn ALLE WARN-getriebenen
  Anpassungen aus Schritt 5 tatsaechlich in `plan.md` geschrieben wurden. Teilannahme, Vertagung
  oder Ablehnung → `Entwurf (plan-review {Datum}: REVISE — Findings offen)`. Begruendung
  (asymmetrisches Risiko): `Reviewed` schaltet in workflow-next „Start ausstehend" frei — ein zu
  frueh gesetztes `Reviewed` schickt jemanden mit bekannten, unbehobenen Schwaechen in die
  Umsetzung; der umgekehrte Fehler kostet nur einen weiteren, billigen Review-Lauf

#### Schritt 2.2: Randfall-Verhalten des Schreibers
- **Zweck:** Fenster-Disziplin + Selbstheilung
- **Dateien:** `skills/dtb-plan-review/SKILL.md` (derselbe neue Schritt)
- **Input:** Randfall-Matrix aus discovery.md
- **Output:** Feld-Suche NUR in den ersten 10 Zeilen; fehlt die Zeile → an Kopfposition einfuegen; Altwerte werden beim Schreiben auf die neue Wertemenge normalisiert; `**Status:**`-Zeilen ausserhalb des Fensters bleiben unangetastet

#### Schritt 2.3: Report-Ausweis + Konsistenz-Sweep
- **Zweck:** Sichtbarkeit der Aenderung + keine vergessenen Querbezuege (Lektion L3)
- **Dateien:** `skills/dtb-plan-review/SKILL.md`; Sweep repo-weit read-only
- **Input:** Abschluss-Report-Format von plan-review
- **Output:** Eine Report-Zeile „Kopf-Statusfeld → {Wert}"; repo-weiter Grep nach `Entwurf`/`Reviewed`/`In Umsetzung`/`plan-review` bestaetigt: keine weitere Stelle referenziert die alte 4-Werte-Menge oder widerspricht der Pfleger-Regel (Befunde → im Plan nachtragen)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] plan-review als funktionierender Pfleger inkl. Randfaelle und Report-Ausweis

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "Reviewed (plan-review" skills/dtb-plan-review/SKILL.md` ≥ 1 UND `grep -n "Entwurf (plan-review" skills/dtb-plan-review/SKILL.md` ≥ 1 (positive UND negative Ausgaenge)
- [ ] `grep -n "ersten 10 Zeilen" skills/dtb-plan-review/SKILL.md` ≥ 1 (Definitionsfenster im Schreiber)

#### Manual
- [ ] Ablauf-Logik konsistent mit Verdikt-Disziplin (Schritt 4/5 unangetastet, Schreibschritt haengt am Schritt-5-Ausgang)

---

## Phase 3: Leser haerten + Trockenlauf

### Ziel
Kein Fehlvorschlag mehr aus veraltetem Feld; Konflikte werden sichtbar; Alt-/Fehlwerte
werden tolerant behandelt.

### Schritte

#### Schritt 3.1: workflow-next haerten
- **Zweck:** Teilbefund 2 der Idee beheben + Konfliktmeldung
- **Dateien:** `skills/dtb-workflow-next/SKILL.md`
- **Input:** Z. 40 (Lese-Anweisung), Z. 53 (Guard-Luecke), Z. 115 (Beispiel)
- **Output:** Guard-Zeile (`Entwurf → Review ausstehend`) greift nur bei 0/Y Checkboxen;
  ⚠-Konfliktzeile bei Feld-vs.-Progress-Widerspruch; Toleranz-Matrix in der Lese-Anweisung;
  Beispiel-Output konsistent
- **Konfliktzeilen-Format (Bestandsmuster, KEIN zweites erfinden):**
  `⚠ plan.md-Kopf sagt "{Wert}", ## Progress zeigt "{X/Y}"` — gleiche Grammatik wie die
  vorhandene BACKLOG-Konfliktzeile (`⚠ {Quelle} sagt "{Feld}", Artefakte zeigen "{abgeleitet}"`),
  gleiche „Artefakt gewinnt, melden statt korrigieren"-Logik (read-only bleibt gewahrt)

#### Schritt 3.2: workflow-status haerten
- **Zweck:** Gate vom nie gesetzten Wert loesen + gleiche Toleranz/Konfliktmeldung
- **Dateien:** `skills/dtb-workflow-status/SKILL.md`
- **Input:** Z. 49–50, Z. 85, Z. 138/174
- **Output:** Gate „Plan-Review" ohne `In Umsetzung` (Reviewed ODER Altwert-Toleranz gemaess Kanon); Ableitungszeilen an Toleranz-Matrix angepasst; ⚠-Konfliktzeile im selben Bestandsformat wie 3.1 (`⚠ plan.md-Kopf sagt …`); Visualisierungszeilen konsistent

#### Schritt 3.3: Trockenlauf an konstruierten Testkoepfen
- **Zweck:** Toleranz-Matrix und Guard verifizieren, bevor verteilt wird
- **Dateien:** keine (read-only Verifikation; Testkoepfe als Wegwerf-Dateien im Scratchpad, nicht im Repo)
- **Input:** 5 konstruierte plan.md-Koepfe: (a) Feld fehlt, (b) `In Umsetzung`, (c) unbekannter Wert, (d) `Entwurf` + 3/9 Checkboxen (Konflikt), (e) Feld ausserhalb der ersten 10 Zeilen
- **Output:** Fuer jeden Fall dokumentiert (Chat + spaeter Session-Log): erwartetes vs. tatsaechliches Leser-Verhalten nach neuem Skill-Text; Abweichungen vor Phase 4 behoben

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: End-to-End-Smoke-Test am echten Bestand
- **Zweck:** Ausfuehrung statt Interpretation — 3.3 bewertet Skill-Text mit demselben Kopf, der
  ihn geschrieben hat; dieser Schritt laesst den gehaerteten Skill real laufen
- **Dateien:** keine (read-only Lauf)
- **Input:** realer `/dtb:workflow-next`-Lauf im Kit-Repo; Material kostenlos vorhanden —
  5 echte Plaene (4 auf `Reviewed` mit 100 % Progress, dieser auf `Entwurf` mit 0/12)
- **Output:** Erwartungsabgleich, alle drei Punkte muessen zutreffen: (1) `plan-status-feld` →
  „Start ausstehend" (Guard darf hier gerade NICHT greifen, 0/Y ist der legitime Fall);
  (2) die vier fertigen Features → „Fertig zum Testen", KEIN plan-review-Vorschlag;
  (3) **null** ⚠-Konfliktzeilen (alle Koepfe stimmen mit ihrem Progress ueberein).
  Abweichung → vor Phase 4 beheben. Bewusste Grenze: reiner Positiv-Test — die pathologischen
  Faelle (Altwerte, unbekannt, echter Konflikt) kommen im Bestand nicht vor und bleiben bei 3.3

### Deliverables
- [ ] Beide Leser gehaertet, Trockenlauf-Protokoll (5 Faelle) ohne offene Abweichung
- [ ] Smoke-Test-Protokoll (3 Erwartungen) ohne Abweichung

### Checkpoint-Kriterien

#### Automated
- [ ] Die Guard-Zeile (`Entwurf` → „Review ausstehend") in `skills/dtb-workflow-next/SKILL.md` enthaelt `0/Y` in derselben Tabellenzeile (Anker: Tabellenkontext, nicht Zeilennummer — Lektion L2)
- [ ] `grep -c "In Umsetzung" skills/dtb-workflow-status/SKILL.md` = 0
- [ ] `grep -n "plan.md-Kopf" skills/dtb-workflow-next/SKILL.md skills/dtb-workflow-status/SKILL.md` ≥ je 1 Treffer (Anker auf den neuen Konfliktzeilen-Wortlaut — ein Grep auf bloss `⚠` waere ein False Positive: das Zeichen steht bereits fuer BACKLOG-Konflikte in beiden Skills, verifiziert 2026-07-30)
- [ ] Smoke-Test 3.4: realer `/dtb:workflow-next`-Lauf erfuellt alle drei Erwartungen (insb. 0 ⚠-Zeilen)

#### Manual
- [ ] Trockenlauf 3.3: alle 5 Faelle verhalten sich gemaess Toleranz-Matrix/Guard (menschliches Urteil ueber Skill-Text-Wirkung)

---

## Phase 4: Register & Distribution

### Ziel
Querbezuege eingeloest, Aenderungen auf beiden Maschinen verteilt.

### Schritte

#### Schritt 4.1: INBOX #22 Seed-Skew-Beleg
- **Zweck:** Entscheidung 3d einloesen — der hingenommene Skew zahlt in die Seed-Skew-Idee ein
- **Dateien:** `dtb-project/project-workflows/INBOX.md`
- **Input:** Einschraenkungen-Abschnitt der discovery.md
- **Output:** 1 Satz-Ergaenzung an Idee #22, die die Wendung **„zweiter Skew-Fall" woertlich**
  enthaelt (z. B. „plan-status-feld ist der zweite Skew-Fall nach dem Verifikations-Gate: …") —
  der Wortlaut ist der Anker des Checkpoint-Kriteriums; ein Grep auf `plan-status-feld` waere
  nicht entscheidbar, weil der String bereits in der #30-Zeile steht (Links auf discovery/spec)

#### Schritt 4.2: kit-sync Distribution + Verifikation
- **Zweck:** Geaenderte Klasse-A-Skills auf dieser Maschine installieren; Lock aktuell
- **Dateien:** `~/.claude/skills/dtb-{plan-review,workflow-next,workflow-status,impl-plan}/SKILL.md`, `~/.claude/dtb-lock.json` (ausserhalb des Repos)
- **Input:** Committeter Stand nach Phase 1–3; verbindliche kitcheck-Sequenz (Lektion L7: hartes Gate VOR jedem Vergleich, keine Improvisation)
- **Output:** `/dtb:kit-sync sync`-Lauf, Verifikations-check synchron (41/41); Hinweis fuer die andere Maschine im Session-Log (deren Lock steht auf `07d5107`)

### Deliverables
- [ ] INBOX #22 ergaenzt; Distribution verifiziert synchron

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "zweiter Skew-Fall" dtb-project/project-workflows/INBOX.md` = 1 (eindeutiger Anker im #22-Nachtrag)
- [ ] kit-sync Verifikations-check meldet synchron (kitcheck-Sequenz mit `GATE OK`, L7)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| §-Verortung Kanon | Neuer § (analog §6) / Unterabschnitt bestehender § | Offen | Bei Schritt 1.1 nach Sichtung der Regel-Datei-Struktur entscheiden (offener Punkt aus Spec) |
| Position des Schreibschritts in plan-review | Eigener Schritt nach dem Anpassungs-Angebot / in Schritt 5 einfalten | Eigener Schritt | Wertematrix haengt am Schritt-5-Ausgang; eigener Schritt haelt Verdikt-Disziplin (Schritt 4) und Anpassungs-Logik (Schritt 5) unangetastet |
| Reihenfolge der Phasen | Kanon zuerst / Skills zuerst | Kanon zuerst | Schreiber und Leser verweisen auf den Kanon-§ — der muss existieren, bevor die Verweise entstehen |
| workflow-next Z. 115 Beispiel | Mitziehen / belassen | Mitziehen | Beispiel-Output, der der neuen Regel widerspricht, ist eine Doku-Falle (Konsistenz, Schritt 3.1) |
| Testkoepfe-Ablage | Repo / Scratchpad | Scratchpad | Wegwerf-Material; im Repo waeren es Pseudo-Artefakte, die project-health/Derived-State-Scans stoeren koennten |
| Vermerkformat | `Reviewed ({Datum}: …)` / mit `plan-review`-Praefix | Mit Praefix | Spec ist die Quelle; Bestand lebt es bereits; erstes Klammerwort nennt den Urheber und traegt die manuelle Ausnahme mit (plan-review 2026-07-30) |
| „behoben"-Erkennung | Ermessen / binaer alle WARNs geschrieben | Binaer | Asymmetrisches Risiko: zu frueh `Reviewed` schickt jemanden mit unbehobenen Schwaechen in die Umsetzung (plan-review 2026-07-30) |
| Verifikation Phase 3 | Nur Trockenlauf / + realer Lauf | Beides (3.3 + 3.4) | 3.3 deckt die pathologischen Faelle, 3.4 ersetzt Interpretation durch Ausfuehrung am echten Bestand (plan-review 2026-07-30) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Kanonisierung DERIVED_STATE_RULES.md
- [x] 1.2 impl-plan-Template straffen
- [x] 1.3 skills/CLAUDE.md nachziehen
- [ ] 2.1 Schreibschritt mit Wertematrix
- [ ] 2.2 Randfall-Verhalten des Schreibers
- [ ] 2.3 Report-Ausweis + Konsistenz-Sweep
- [ ] 3.1 workflow-next haerten
- [ ] 3.2 workflow-status haerten
- [ ] 3.3 Trockenlauf Testkoepfe
- [ ] 3.4 Smoke-Test am echten Bestand
- [ ] 4.1 INBOX #22 Seed-Skew-Beleg
- [ ] 4.2 kit-sync Distribution + Verifikation

---

## Umsetzung

Umsetzung mit `/dtb:implement plan-status-feld` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/plan-status-feld/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
