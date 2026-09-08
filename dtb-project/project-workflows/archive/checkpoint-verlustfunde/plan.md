# Implementierungsplan: Checkpoint erfasst Verlustfunde

**Erstellt:** 2026-09-08
**Feature-Spec:** `features/checkpoint-verlustfunde/spec.md`
**Geschaetzte Dauer:** ~6 h (3 Phasen, 9 Schritte; Phase 3 traegt 5 echte Checkpoint-Laeufe)
**Status:** Reviewed (plan-review 2026-09-08: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Quellen koppeln — Anker und Kopplungs-Hinweise in `lesson`, `idea`, `no-loss-check` | ~1 h | Geplant |
| Phase 2 | Wirkstelle — Checkpoint Schritt 0 erweitern (Struktur-Check, Sammelvorlage, Schreibpfad, Log-Zeile) | ~2 h | Geplant |
| Phase 3 | Doku-Nachzug, Verteilung, Wirklauf im Haupt-Checkout (5 Laeufe) | ~3 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (9 Module, Pfade am 2026-09-08 verifiziert). Kompakt, keine Prosa.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | 373 Zeilen. Schritt 0 (Z. 253-275) ruft `dtb:no-loss-check` und begruendet das mit dessen `disable-model-invocation: false`; Funde werden nur als Befehle weitergereicht. `allowed-tools: Read, Write, Bash`. `produces` ohne `lessons.md`/`INBOX.md`. Teil 1 Log-Format (Z. 115-155): `### Implementiert` als Bullet-Liste, keine feste Verlustpruefungs-Zeile |
| `skills/dtb-lesson/SKILL.md` | 213 Zeilen, `disable-model-invocation: true`, `allowed-tools: Read, Write, Edit, Grep`. Anker-Sektionen: `## Schritt 2: In 4 Felder strukturieren` (Feld-Hygiene: Pipes escapen), `## Schritt 3: Duplikat-Check` (weich, Ja/Abbrechen), `## Schritt 4: Append-only speichern` (Append **mit `Edit`**, nie `Write`-Neuschrieb; naechste Nummer; Datum). Kein Kopplungs-Hinweis auf einen externen Leser |
| `skills/dtb-idea/SKILL.md` | `disable-model-invocation: true`, `allowed-tools: Read, Write, Grep, Bash`. Anker: `## Duplikat-Check` (unscharf gegen alle Zeilen, `archive/` nie; Treffer → eine Fundstellen-Zeile + eine Frage; Abbrechen-Pfad), `## Schritt 2: In INBOX.md speichern` (Zeile anfuegen, naechste Nummer, Status `Offen`). Kein Pipe-Escaping (#70). Kein Kopplungs-Hinweis |
| `skills/dtb-no-loss-check/SKILL.md` | 414 Zeilen, `disable-model-invocation: false`, `produces: []`. Report: feste Ueberschriften `## Vor dem Checkpoint erledigen` / `## Kann warten`, je Fund `- {Satz}` + `→ /dtb:{skill} {Argument}` + `Ziel: {pfad} ({versioniert\|nicht versioniert})`. Gruppe steht **nur** in der Ueberschrift. Zuordnungstabelle „Versioniert oder nicht" fuehrt `lessons.md` als **nicht versioniert (#34)** — seit `f75979d` (2026-09-07) falsch. Kein Wartungs-Hinweis mit benanntem Leser des Report-Formats |
| `skills/dtb-pane-start/SKILL.md` | `## Struktur-Check (Kopplungs-Waechter)` (Z. 189-247): Quelle aufloesen (`~/.claude/skills/…` vor Repo), Anker-Grep zeilenende-normalisiert (`tr -d '\r'`), Statuszeile `🧩 Struktur-Check: 2/2 Anker in {Quelle} gefunden`, zwei getrennte Fehlerpfade (Datei fehlt ≠ Anker fehlt), benanntes Restrisiko (Existenz, nicht Inhalt). Gegenseite: `dtb:worker` traegt `> **Kopplungs-Hinweis:**`-Bloecke an den Anker-Sektionen |
| `skills/dtb-feature-fast/SKILL.md` | Schritt 4 Sammelvorlage: nummerierte Eintraege, „Korrekturen als Freitext, Unkommentiertes gilt als angenommen", Abschlussfrage `Ok / Korrekturen / … / Abbruch`; Veto-Verarbeitung: nur Geaendertes rueckbestaetigen; Selbst-Eskalation bei >10 Eintraegen |
| `skills/CLAUDE.md` | Konventionen: Parallele Sessions/Schreibgrenzen, Eligibility-Gates, Duplikat-Schutz-Konvention der Capture-Familie, `disable-model-invocation`-Regel („`true` unless auto-triggered") |
| `dtb-project/project-rules/lessons.md` | 24 Datenzeilen (hoechste Nummer 37 — Luecken in der Nummerierung, #64), 6 Spalten (`# \| Datum \| Context \| Problem \| Rule \| Applies-to`), versioniert seit `f75979d` |
| `skills/dtb-pipeline-graph/SKILL.md`, `skills/dtb-project-health/SKILL.md` | Lesen `produces`/`consumes`/`after`/`next`; neue Datei-Kanten erscheinen automatisch, keine Aenderung dort |
| `CLAUDE.md` (Repo-Root) | Beschreibt `workflow-checkpoint` als „writes a session log AND overwrites WORKFLOW_STATUS.md" und `no-loss-check` als „writes nothing" — beides wird um den neuen Schreibpfad ergaenzt (Doku-Nachzug, L3) |

---

## Phase 1: Quellen koppeln

### Ziel
`dtb:lesson`, `dtb:idea` und `dtb:no-loss-check` sind als Referenzquellen abgesichert: ihre Anker-Sektionen tragen Kopplungs-Hinweise, die den Checkpoint als Leser nennen, und das Report-Format von `no-loss-check` ist als Kopplung deklariert. Kein Verhalten der drei Skills aendert sich.

### Schritte

#### Schritt 1.1: Anker und Kopplungs-Hinweise in `dtb:lesson`
- **Zweck:** Die drei Sektionen, die der Checkpoint per Referenz ausfuehrt, als Anker deklarieren — Umbau dort soll den Checkpoint benennen (Muster `dtb:worker` → `dtb:pane-start`)
- **Dateien:** `skills/dtb-lesson/SKILL.md`
- **Input:** Sektions-Titel `## Schritt 2: In 4 Felder strukturieren`, `## Schritt 3: Duplikat-Check`, `## Schritt 4: Append-only speichern` (Ist-Analyse)
- **Output:** Je Sektion ein `> **Kopplungs-Hinweis:**`-Block (Wortlaut-Muster `dtb:worker` Z. 173-175): „`dtb:workflow-checkpoint` fuehrt diese Schritte fuer dringende Verlustfunde per Referenz aus und greppt auf den Sektions-Titel (Struktur-Check). Umbenennung/Umbau → `skills/dtb-workflow-checkpoint/SKILL.md` mitziehen." Kein Regeltext veraendert, keine Zeile kopiert

#### Schritt 1.2: Anker und Kopplungs-Hinweise in `dtb:idea`
- **Zweck:** Dasselbe fuer die zwei Sektionen, die der Checkpoint fuer Ideen-Funde ausfuehrt
- **Dateien:** `skills/dtb-idea/SKILL.md`
- **Input:** Sektions-Titel `## Duplikat-Check`, `## Schritt 2: In INBOX.md speichern`
- **Output:** Je Sektion ein Kopplungs-Hinweis (Wortlaut wie 1.1). Pipe-Escaping bleibt bewusst unangetastet (#70, Spec „Nicht enthalten")

#### Schritt 1.3: Report-Format von `dtb:no-loss-check` als Kopplung deklarieren + Zuordnungstabelle korrigieren
- **Zweck:** (a) Der Checkpoint liest kuenftig die Gruppen-Ueberschriften und die `→ /dtb:{skill} {Argument}`-Zeilen — das muss am Ausgabe-Muster als Format-Kopplung stehen (Muster `feature-discover` Z. 84-87). (b) Die feste Zuordnungstabelle nennt `lessons.md` „nicht versioniert (#34)" — seit `f75979d` falsch; der Checkpoint wuerde die falsche Angabe sonst in die Vorlage uebernehmen
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md`
- **Input:** Sektion `### Ausgabe-Muster (feste Ueberschriften, woertlich uebernehmen)`, Sektion `### Versioniert oder nicht (Pflichtangabe je Fund)`
- **Output:** (a) `> **Wartungs-Hinweis (Format-Kopplung):**`-Block direkt unter dem Ausgabe-Muster: Leser `dtb:workflow-checkpoint` Schritt 0, geparst werden die beiden `## `-Ueberschriften und je Fund die `→ /dtb:…`-Zeile; Format-Aenderung → Checkpoint mitziehen. (b) Tabellenzeile `project-rules/lessons.md` → „versioniert — seit 2026-09-07 (`f75979d`, #34 revidiert)"; die Beispiel-Zeile `Ziel: dtb-project/project-rules/lessons.md (nicht versioniert)` im Ausgabe-Muster entsprechend. **Spec-Nachtrag (plan-review 2026-09-08):** beim Phasen-1-Commit in `spec.md` → `### Enthalten` einen Bullet „Korrektur der Zuordnungstabelle in `no-loss-check` (`lessons.md` versioniert)" ergaenzen — sonst Drift-Finding im impl-review

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 5 Kopplungs-Hinweise (3 in `lesson`, 2 in `idea`), die `dtb:workflow-checkpoint` als Leser nennen
- [ ] 1 Wartungs-Hinweis (Format-Kopplung) in `no-loss-check` mit Leser `dtb:workflow-checkpoint`
- [ ] Zuordnungstabelle in `no-loss-check` korrekt (`lessons.md` versioniert)

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^## Schritt 2: In 4 Felder strukturieren$\|^## Schritt 3: Duplikat-Check$\|^## Schritt 4: Append-only speichern$' skills/dtb-lesson/SKILL.md` → `3` (Anker unveraendert vorhanden; zeilenende-normalisiert per `tr -d '\r'`)
- [ ] `grep -c '^## Duplikat-Check$\|^## Schritt 2: In INBOX.md speichern$' skills/dtb-idea/SKILL.md` → `2`
- [ ] `grep -c 'Kopplungs-Hinweis.*dtb:workflow-checkpoint' skills/dtb-lesson/SKILL.md` → `3`; dasselbe fuer `skills/dtb-idea/SKILL.md` → `2`
- [ ] `grep -c 'Wartungs-Hinweis (Format-Kopplung).*' skills/dtb-no-loss-check/SKILL.md` → `≥1` UND die Fundstelle nennt `dtb:workflow-checkpoint` innerhalb der naechsten 4 Zeilen
- [ ] `grep -c 'lessons.md.*nicht versioniert' skills/dtb-no-loss-check/SKILL.md` → `0` (L8: auf die Zuordnungstabelle und das Ausgabe-Muster geankert, nicht auf die ganze Datei — beide Fundstellen sind in 1.3 benannt)
- [ ] `git diff --stat` der Phase zeigt genau 3 Dateien; kein Regeltext geloescht: `git diff skills/dtb-lesson/SKILL.md skills/dtb-idea/SKILL.md | grep -c '^-[^-]'` → `0` (nur Zugaenge; in `no-loss-check` genau die 2 korrigierten Zeilen als Abgang)

---

## Phase 2: Wirkstelle — Checkpoint Schritt 0

### Ziel
`dtb:workflow-checkpoint` erfasst die dringenden Funde nach einer Sammelvorlage selbst, folgt dabei den referenzierten Schritten aus Phase 1, schreibt nichts auf veralteter Basis (Struktur-Check) und haelt das Ergebnis im Session-Log fest.

### Schritte

#### Schritt 2.1: Frontmatter — Deklaration und Werkzeuge
- **Zweck:** Ehrliche Deklaration der neuen Schreibziele (Pipeline-Kante, #46) und die Werkzeuge, die die referenzierten Schritte benennen (`Edit` fuer Append-only, `Grep` fuer Duplikat-Check) — eine Uebersetzung „nimm stattdessen Bash" waere eine Mini-Kopie der Quelle
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Z. 1-15)
- **Input:** `produces: [WORKFLOW_STATUS.md, BACKLOG.md, features/*/spec.md, features/*/task.md, session-log, ROADMAP.md]`; `allowed-tools: Read, Write, Bash`; `consumes` ohne `lessons.md`
- **Output:** `produces` + `project-rules/lessons.md`, `INBOX.md`; `consumes` + `project-rules/lessons.md` (Duplikat-Check liest sie); `allowed-tools: Read, Write, Edit, Grep, Bash`. **Abweichung von der Discovery** (dort 3d: „kein Frontmatter-Eingriff, Bash deckt es ab") — beim Phasen-2-Checkpoint im Session-Log mit Grund festhalten (die referenzierten Schritte benennen `Edit`/`Grep` woertlich)

#### Schritt 2.2: Unterabschnitt „Dringende Funde erfassen" in Schritt 0
- **Zweck:** Die Wirkstelle. Ein neuer Unterabschnitt zwischen dem `no-loss-check`-Aufruf und Schritt 1, der den Ablauf vollstaendig traegt — ohne Regeltext aus `lesson`/`idea` zu wiederholen
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (nach Z. 275, vor `### Schritt 1`)
- **Input:** Report von `no-loss-check` (Gruppen-Ueberschriften, `→`-Zeilen); Anker-Titel aus 1.1/1.2; Muster Struktur-Check (`pane-start` Z. 196-231) und Sammelvorlage (`feature-fast` Schritt 4)
- **Output:** Sektion `#### Dringende Funde erfassen (Sammelvorlage)` mit genau diesen Bloecken, in dieser Reihenfolge:
  1. **Eingang:** nur Funde unter `## Vor dem Checkpoint erledigen`; Gruppe leer → Block entfaellt still, weiter mit Schritt 1. „Kann warten" bleibt unveraendert Befehle im Report. `> Wartungs-Hinweis (Format-Kopplung)`: liest das Ausgabe-Muster von `no-loss-check` (Gegenseite zu 1.3)
  2. **Struktur-Check (Kopplungs-Waechter):** Quellen aufloesen — **Regel (plan-review 2026-09-08): zuerst `skills/dtb-lesson/SKILL.md` bzw. `skills/dtb-idea/SKILL.md` relativ zum Projekt-Root (Kit-Repo-Fall: das Repo ist die Quelle, aus der `kit-sync` verteilt), sonst `~/.claude/skills/dtb-{lesson,idea}/SKILL.md` (Zielprojekt).** Bewusst umgekehrt zu `dtb:pane-start` (dort installiert zuerst); der Grund steht als ein Satz im Block. Nur die Quellen aufloesen, deren Typ in der Gruppe vorkommt; Anker-Grep zeilenende-normalisiert auf die 3+2 Titel aus 1.1/1.2; Statuszeile `🧩 Struktur-Check: {n}/{n} Anker in {Quelle} gefunden`; **zwei Fehlerpfade** wortgleich zum `pane-start`-Muster (Datei fehlt → Installationsproblem, `/dtb:kit-sync`; Anker fehlt → Drift, „ich schreibe NICHT auf veralteter Basis") — beide → Rueckfall: Funde bleiben Befehle im Report, weiter mit Schritt 1. Benanntes Restrisiko: Existenz, nicht Inhalt
  3. **Vorbereitung je Fund (per Referenz):** Lektion → Schritt 2 (vier Felder inkl. Feld-Hygiene) und Schritt 3 (Duplikat-Check) aus `dtb:lesson`; Idee → `## Duplikat-Check` aus `dtb:idea`. Duplikat-Treffer werden **nicht** gefragt, sondern in der Vorlage als vorgestrichene Zeile mit Fundstelle gezeigt (`~~3~~ … — aehnlich L23 / #33 (Offen)`)
  4. **Sammelvorlage** (Kurzfassung je Fund, nie Vollwortlaut der vier Felder):
     ```
     # Verlustfunde erfassen — {D} dringend
     1  Lektion  {Rule-Satz gekuerzt}                     → lessons.md L{naechste}
     2  Idee     {Idee-Satz gekuerzt}                     → INBOX.md #{naechste}
     ~~3~~ Lektion {…} — aehnlich L23 (vorgestrichen, "3 behalten" nimmt sie auf)
     Ok fuer alle nicht gestrichenen? (Ok / streiche {Nr,…} / behalte {Nr} / Abbruch)
     ```
     Antwortregeln: `Ok` = alle nicht gestrichenen schreiben; `streiche 2` / `behalte 3` als Freitext, nur Geaendertes rueckbestaetigen (Muster `feature-fast`); `Abbruch` = nichts schreiben, eine Zeile, weiter mit Schritt 1. **Fallback:** jede andere Antwort gilt als nicht bestaetigt — genau eine Rueckfrage (`Ok / streiche {Nr} / behalte {Nr} / Abbruch?`), bei erneut unklarer Antwort `Abbruch`. Mehr als 10 dringende Funde → Vorlage entfaellt, Rueckfall auf Befehle mit einer Hinweiszeile
  5. **Schreiben (per Referenz):** je bestaetigtem Fund Schritt 4 aus `dtb:lesson` (Append mit `Edit`, naechste Nummer, Datum) bzw. Schritt 2 aus `dtb:idea` (Zeile anfuegen, naechste Nummer, `Offen`). **Herkunfts-Marker** als Suffix im Textfeld: lessons → Ende von `Context`, INBOX → Ende des Idee-Texts, Wortlaut `(via Checkpoint {YYYY-MM-DD})`. Schreibfehler mitten drin → melden, was geschrieben ist, Rest als Befehle ausgeben, nie zurueckrollen (append-only)
  6. **Meldung:** eine Zeile je Eintrag `✔ L{N} → lessons.md` / `✔ #{N} → INBOX.md`; alle gestrichen → `Nichts erfasst — {D} Fund(e) bleiben als Befehle im Report`
  7. **Selbstpruefung gegen die Fehlerklasse (L15):** der Unterabschnitt traegt keinen Satz, der Feld-Ableitung, Duplikat-Bewertung oder Append-Mechanik **beschreibt** — er benennt nur den Anker, aus dem sie zu lesen ist

#### Schritt 2.3: Feste Log-Zeile im Session-Log
- **Zweck:** Gruppierung und Erfassung ins Log bringen — 5 von 8 Logs tragen die Gruppierung heute nicht (Discovery-Datenlage); „kommen zum Checkpoint" aus der Discovery
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Teil 1 → `### Format` und `### Richtlinien`)
- **Input:** Log-Format Z. 127-146
- **Output:** Pflicht-Bullet als **letzter** Eintrag unter `### Implementiert`, festes Format: `- Verlustpruefung: {D} dringend → {L…, #…} erfasst · {W} kann warten (Befehle im Report) · {S} gefiltert` (bei `D = 0`: `0 dringend`; bei uebersprungener Pruefung: `Verlustpruefung uebersprungen — {Grund}`). Richtlinie: die Zeile ist Pflicht, auch bei 0/0/0

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Frontmatter mit erweitertem `produces`/`consumes`/`allowed-tools`
- [ ] Unterabschnitt `#### Dringende Funde erfassen (Sammelvorlage)` mit den 7 Bloecken
- [ ] Pflicht-Log-Zeile im Teil-1-Format

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'project-rules/lessons.md' skills/dtb-workflow-checkpoint/SKILL.md` → `≥2` (produces + consumes) und `grep -c '^  produces:.*INBOX.md' …` → `1`
- [ ] `grep -c '^allowed-tools: Read, Write, Edit, Grep, Bash$' skills/dtb-workflow-checkpoint/SKILL.md` → `1`
- [ ] `grep -c '^#### Dringende Funde erfassen (Sammelvorlage)$' skills/dtb-workflow-checkpoint/SKILL.md` → `1`, und die Sektion steht **vor** `### Schritt 1: Informationen sammeln` (Zeilennummern vergleichen)
- [ ] **Anker-Deckung (L2):** jeder der 5 Anker-Titel aus 1.1/1.2 kommt im neuen Unterabschnitt woertlich vor: `for a in 'Schritt 2: In 4 Felder strukturieren' 'Schritt 3: Duplikat-Check' 'Schritt 4: Append-only speichern' 'Duplikat-Check' 'Schritt 2: In INBOX.md speichern'; do grep -c "$a" …; done` → alle `≥1`
- [ ] **Keine Kopie (L15, Spec-Kriterium 8):** drei markante Regel-Phrasen der Quellen fehlen im Checkpoint: `grep -c 'Feld-Hygiene\|Gleicher Gegenstand \*\*und\*\* gleiche Aussage\|letzte Datenzeile als Anker' skills/dtb-workflow-checkpoint/SKILL.md` → `0`
- [ ] `grep -c '^- Verlustpruefung: {D} dringend' skills/dtb-workflow-checkpoint/SKILL.md` → `1` (Format-Zeile im Teil-1-Template)
- [ ] `grep -c 'Struktur-Check' skills/dtb-workflow-checkpoint/SKILL.md` → `≥2` (Block-Titel + Statuszeile) und `grep -c 'Restrisiko' …` → `≥1`
- [ ] Aufloesungs-Regel und Fallback vorhanden: `grep -c 'relativ zum Projekt-Root' skills/dtb-workflow-checkpoint/SKILL.md` → `≥1` und `grep -c 'Ok / streiche' …` → `≥2` (Vorlage + Fallback-Rueckfrage)
- [ ] Dateilaenge: `wc -l skills/dtb-workflow-checkpoint/SKILL.md` → `≤ 470` (373 + max. ~95 Zeilen; Referenz statt Kopie haelt ihn schlank)

#### Manual
- [ ] Die Vorlage liest sich als EIN Kontrollpunkt: eine Antwort genuegt fuer den Normalfall (1-3 Funde), Streichen ist ohne Nachdenken moeglich
- [ ] Der Unterabschnitt erklaert **nicht**, wie Felder abgeleitet oder Duplikate bewertet werden — wer das wissen will, muss in `lesson`/`idea` lesen (Referenz gehalten)

---

## Phase 3: Doku-Nachzug, Verteilung, Wirklauf

### Ziel
Alle Beschreibungen des Checkpoints und der Verlustpruefung im Repo sind nachgezogen, die Klasse-A-Artefakte sind verteilt und bezeugt, und ein Wirklauf im Haupt-Checkout belegt die Success-Kriterien der Spec an einem Fall-Set.

### Schritte

#### Schritt 3.1: Doku-Nachzug (L3 — repo-weit greppen, nicht nur Frontmatter)
- **Zweck:** Jede Stelle, die den Checkpoint als „schreibt Log + Status" oder `no-loss-check` als „writes nothing" beschreibt, traegt den neuen Schreibpfad
- **Dateien:** `CLAUDE.md` (Root, Sektionen „Skill Workflow Lifecycle" Punkt 3 und „Session lifecycle"), `skills/CLAUDE.md` (Duplikat-Schutz-Konvention: der Checkpoint ist jetzt vierter Anwender per Referenz; Schreibgrenzen: lessons.md/INBOX.md als Checkpoint-Ziel), ggf. `README.md`
- **Input:** `grep -rn 'no-loss-check\|workflow-checkpoint' --include='*.md' . | grep -v '^./dtb-project/project-changelog\|^./dtb-project/project-workflows'` (Treffer-Liste als Ablageort im Session-Log, L20)
- **Output:** Nachgezogene Saetze (je 1 Satz, kein Absatz); Treffer, die bewusst unveraendert bleiben, mit Grund im Session-Log. **Vorher-Wert festhalten:** `grep -c 'lessons.md' CLAUDE.md` VOR der Aenderung im Session-Log notieren (Sollwert des Automated-Kriteriums). **Spec-Nachtrag:** beim Phasen-3-Commit in `spec.md` → `### Enthalten` einen Bullet „Doku-Nachzug in `CLAUDE.md`/`skills/CLAUDE.md` (L3)" ergaenzen

#### Schritt 3.2: Verteilen und bezeugen (`/dtb:kit-sync sync`)
- **Zweck:** Die installierte Kopie ist die, die laeuft (Spec, Klasse A). Erfolg an einen unabhaengigen Zeugen binden (L35), nicht an den Hash-Vergleich
- **Dateien:** `~/.claude/skills/dtb-{workflow-checkpoint,lesson,idea,no-loss-check}/SKILL.md`, `~/.claude/dtb-lock.json` (ausserhalb des Repos)
- **Input:** Commit-SHA des Phase-2/3.1-Standes
- **Output:** Lock @ SHA, 4 Updates; Zeuge: `ls -l --time-style=full-iso` der 4 Zielkopien **nach** dem Sync zeigt mtime ≥ Sync-Zeitpunkt, plus Hash-Vergleich. Protokoll (Zeilen des Zeugen) in `## Beleg-Protokolle (Phase 3)` dieses Plans (Ablageort, L20)

#### Schritt 3.3: Wirklauf im Haupt-Checkout (Fall-Set, L14/L29)
- **Zweck:** Verhaltens-Kalibrierung an Faellen — der Text-Review (impl-review) findet eine andere Fehlerklasse. Gegen die Wirkstelle im Haupt-Checkout, nie im Worktree (Voll-Guard des Checkpoints). Nach 3.2 laufen (der Checkpoint selbst laeuft aus `~/.claude`; die Quellen-Aufloesung „Repo zuerst" macht die installierte `dtb-lesson` fuer den Struktur-Check hier zweitrangig)
- **Dateien:** `dtb-project/project-rules/lessons.md`, `dtb-project/project-workflows/INBOX.md` (echte Eintraege — Blind-Faelle von Capture-Skills schreiben echte Artefakte, Verlustfund 2026-09-07 S3), `skills/dtb-lesson/SKILL.md` (Laeufe 4/5, per git rueckholbar), `~/.claude/skills/dtb-lesson/SKILL.md` (Lauf 5, ~10 s per `mv` weg, Hash-Zeuge), `features/checkpoint-verlustfunde/plan.md` → `## Beleg-Protokolle (Phase 3)`
- **Input:** **Fuenf echte `/dtb:workflow-checkpoint`-Laeufe** (plan-review 2026-09-08: jede Antwort auf die Vorlage ist ein eigener Lauf). **Nebenwirkung, bewusst akzeptiert:** jeder Lauf schreibt einen echten `## Session N`-Block und ueberschreibt `WORKFLOW_STATUS.md` — die Bloecke dokumentieren ihren eigenen Wirklauf, kein Nachloeschen

  | Lauf | Faelle | Vorbereitung | Antwort | Belegt |
  |------|--------|--------------|---------|--------|
  | 1 | (a) Treffer + (d) Duplikat | 2 dringende Funde: eine echte Lektion aus diesem Bau (kein Wegwerf-Inhalt) + ein Fund, der L37 aehnelt | `Ok` → nur der nicht vorgestrichene wird geschrieben: `L{N}` mit Marker, Format wie von Hand; Duplikat vorgestrichen mit Fundstelle, nicht geblockt | Spec-Kriterium 1, 4 |
  | 2 | (b) Streichen | 3 dringende Funde | `streiche 2, 3` → genau 1 geschrieben | Kriterium 2, Teil 1 |
  | 3 | (b) Abbruch | ≥1 dringender Fund | `Abbruch` → nichts geschrieben, genau eine Meldezeile | Kriterium 2, Teil 2 |
  | 4 | (e) Anker-Drift | Titel `## Schritt 3: Duplikat-Check` in `skills/dtb-lesson/SKILL.md` (Arbeitskopie) umbenennen | kein Dialog → Fehlerpfad 2 (Drift), Rueckfall auf Befehle, nichts geschrieben; danach `git checkout -- skills/dtb-lesson/SKILL.md` | Kriterium 5, Pfad 2 |
  | 5 | (e) Datei fehlt | `git mv skills/dtb-lesson/SKILL.md skills/dtb-lesson/SKILL.md.off` UND `mv ~/.claude/skills/dtb-lesson/SKILL.md{,.off}` | kein Dialog → Fehlerpfad 1 (Installation), Rueckfall, nichts geschrieben; danach beide zurueck, `git hash-object ~/.claude/skills/dtb-lesson/SKILL.md` = `artifacts['skills/dtb-lesson/SKILL.md'].hash` im Lock (Zeuge) | Kriterium 5, Pfad 1 |

  **(c) Leer** kostet keinen eigenen Lauf: der erste Checkpoint des Tages vor Lauf 1 (keine dringende Gruppe) belegt „keine Vorlage, kein leerer Block, Kann-warten unveraendert" (Kriterium 3) — als Protokoll-Block mitschreiben
- **Output:** Je Lauf (und fuer c) ein `**Wirklauf {Datum}**`-Block (Eingabe, Vorlage-Auszug, Antwort, Ergebnis-Zeilen, `git diff --stat`, bei Lauf 5 die Zeugen-Zeilen) in `## Beleg-Protokolle (Phase 3)`; Log-Zeile aus 2.3 im Session-Log jedes Laufs (Kriterium 6)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Doku-Nachzug mit Treffer-Liste im Session-Log
- [ ] Lock @ SHA mit mtime-Zeuge fuer 4 Kopien
- [ ] 5 Wirklauf-Protokolle in `## Beleg-Protokolle (Phase 3)`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -rln 'writes nothing' CLAUDE.md` → leer, oder die Fundstelle nennt den Checkpoint-Schreibpfad in derselben Zeile (L8: auf den `no-loss-check`-Satz geankert)
- [ ] `grep -c 'lessons.md' CLAUDE.md` → um `≥1` hoeher als der in 3.1 notierte Vorher-Wert (Zeile zum Checkpoint)
- [ ] Lock: `python -c "import json,os;d=json.load(open(os.path.expanduser('~/.claude/dtb-lock.json'),encoding='utf-8'));print(d['sourceCommit'])"` → SHA von 3.1; fuer die 4 Pfade `d['artifacts'][pfad]['hash']` = `git hash-object` der Repo-Datei = `git hash-object` der Zielkopie; mtime-Zeuge fuer alle 4 Kopien ≥ Sync-Zeit (L35)
- [ ] `grep -c '^\*\*Wirklauf 2026-' dtb-project/project-workflows/features/checkpoint-verlustfunde/plan.md` → `6` (5 Laeufe + Fall c)
- [ ] Nach (a): letzte Datenzeile von `lessons.md` enthaelt `(via Checkpoint 2026-` und hat genau 6 Spalten (`awk -F'|' 'END{print NF-2}'` → `6`); nach (a)/(b): `wc -l lessons.md` und INBOX-Zeilenzahl um genau die erwartete Zahl gewachsen
- [ ] Nach Lauf 4: `git status --short skills/dtb-lesson/SKILL.md` → leer (Arbeitskopie zurueckgeholt). Nach Lauf 5: `git hash-object ~/.claude/skills/dtb-lesson/SKILL.md` = `artifacts[…].hash` im Lock UND `git status --short skills/dtb-lesson/` → leer (beide Dateien zurueck)

#### Manual
- [ ] Abnahme der 5 Laeufe + Fall (c) gegen die Spec-Kriterien 1-6 — keine Abweichung zur Vorlage
- [ ] Die Vorlage war im Alltag ein Kontrollpunkt, kein Interview (Urteil nach Fall a und b)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Wiederverwendung von `lesson`/`idea` | A) Referenz auf Schritte (Read + Struktur-Check), B) Aufruf per Skill-Tool (Flag auf `false`) | **A** | Spec: Flag steuert Initiative, nicht Anweisungskette (L9); B naehme #69 vorweg. Praezedenz `pane-start`→`worker` |
| `allowed-tools` des Checkpoints | A) `Edit, Grep` ergaenzen, B) Bash-Uebersetzung im Text („statt Edit nimm >>") | **A** | Die referenzierten Schritte benennen `Edit`/`Grep`; eine Uebersetzung waere eine Mini-Kopie der Quelle |
| Antwortformat der Vorlage | A) `Ok / streiche {Nr,…} / behalte {Nr} / Abbruch`, B) Freitext ohne Schema | **A** | Muster `feature-fast` („Unkommentiertes gilt als angenommen"), plus `behalte` fuer vorgestrichene Duplikate; Spec offener Punkt 3 |
| Herkunfts-Marker | A) Suffix im Textfeld `(via Checkpoint YYYY-MM-DD)`, B) eigene Spalte, C) Praefix | **A** | Keine Spalte (5 Leser), Suffix stoert Grep auf den Kern nicht; Spec offener Punkt 2 |
| Duplikat-Treffer in der Vorlage | A) vorgestrichen + Fundstelle, `behalte` hebt auf; B) Rueckfrage je Treffer wie in `lesson`/`idea` | **A** | B waere eine zweite Rueckfrage-Runde — genau der Zustand, den die Vorlage abloest. Die Bewertung selbst bleibt per Referenz |
| Ort der Log-Zeile | A) letzter Bullet unter `### Implementiert`, B) eigener Abschnitt | **A** | Bisherige Praxis der Logs, kein neuer Abschnitt; Pflicht auch bei 0/0/0 |
| Stale „nicht versioniert" in `no-loss-check` | A) in 1.3 mitkorrigieren, B) eigener Fund | **A** | Gleiche Datei, gleicher Block, den der Checkpoint parst; ohne Korrektur zeigt die Vorlage eine falsche Angabe |
| Quellen-Aufloesung im Struktur-Check | A) Repo zuerst, wenn `skills/dtb-*/SKILL.md` relativ zum Projekt-Root existiert, sonst installiert; B) installiert zuerst wie `pane-start`; C) `pane-start` mit harmonisieren | **A** (plan-review 2026-09-08) | Im Kit-Repo ist das Repo die Quelle, aus der `kit-sync` verteilt — installiert zuerst prueft waehrend des Baus gegen den Stand von gestern. Zielprojekte unberuehrt (kein `skills/`). C waere Scope ueber #72 |
| Antwort-Fallback der Vorlage | A) unklare Antwort = eine Rueckfrage, dann Abbruch; B) unklare Antwort = `Ok` | **A** (plan-review 2026-09-08) | B waere stiller Auto-Write durch Missverstaendnis |
| Wirklauf-Umfang | A) 5 echte Checkpoint-Laeufe (+ c frei), B) 4 Laeufe, Abbruch per Text-Review | **A** (plan-review 2026-09-08) | Konsistent zur Entscheidung, Kriterium 5 mit beiden Pfaden zu belegen; Session-Bloecke als Nebenwirkung akzeptiert |
| Struktur-Anker | 5 Sektions-Titel (3 `lesson`, 2 `idea`) | **fest** | Titel sind die eine Quelle; Restrisiko Existenz≠Inhalt benannt (F1-Klasse) |
| Wirklauf-Inhalt | A) echte Lektion/Idee aus dem Bau, B) Wegwerf-Eintraege mit Nachloeschen | **A** | Blind-Faelle von Capture-Skills schreiben echte Artefakte (Verlustfund S3 2026-09-07); `lessons.md` ist append-only |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Anker + Kopplungs-Hinweise `dtb:lesson` — `e6cbb3a`
- [x] 1.2 Anker + Kopplungs-Hinweise `dtb:idea` — `e6cbb3a`
- [x] 1.3 Format-Kopplung + Zuordnungstabelle `dtb:no-loss-check` — `e6cbb3a`
- [x] 2.1 Frontmatter Checkpoint (produces/consumes/allowed-tools) — `4988263`
- [x] 2.2 Unterabschnitt „Dringende Funde erfassen" — `4988263`
- [x] 2.3 Pflicht-Log-Zeile Teil 1 — `4988263`
- [x] 3.1 Doku-Nachzug (CLAUDE.md, skills/CLAUDE.md) — `96a7b3f`
- [x] 3.2 kit-sync + mtime-Zeuge — `96a7b3f`
- [x] 3.3 Wirklauf Fall-Set a-e — `96a7b3f`

---

## Umsetzung

Umsetzung mit `/dtb:implement checkpoint-verlustfunde` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/checkpoint-verlustfunde/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

## Beleg-Protokolle (Phase 3)

**kit-sync 2026-09-08 13:02 (Schritt 3.2)** — Push `fec3371..4988263` vorab (GitHub ist die Quelle;
ohne Push haette der Sync die Checkpoint-Fassung OHNE Phase 2 installiert). Check: 43 synchron,
4 Update verfuegbar (`idea`, `lesson`, `no-loss-check`, `workflow-checkpoint`), sonst 0. Sync: 4 uebernommen,
Lock `b9e0b57` → **`4988263`**, 47 Artefakte, Nachpruefung 47/47 synchron (Repo = Lock = Kopie).
mtime-Zeuge (L35), Sync-Zeit `2026-09-08T13:02:02`:

```
6493  2026-09-08 13:02:02.384894800 +0200 ~/.claude/skills/dtb-idea/SKILL.md                (2464fa7)
10041 2026-09-08 13:02:02.399986400 +0200 ~/.claude/skills/dtb-lesson/SKILL.md              (d920b32)
22343 2026-09-08 13:02:02.415036600 +0200 ~/.claude/skills/dtb-no-loss-check/SKILL.md       (51c533a)
22005 2026-09-08 13:02:02.431020400 +0200 ~/.claude/skills/dtb-workflow-checkpoint/SKILL.md (9ddfb48)
```

**Wirklauf 2026-09-08 13:16 — Lauf 1, Faelle (a) Treffer + (d) Duplikat** (Checkpoint S2, installierte Kopie @ `4988263`)
- Eingabe: 2 im Chat als dringend gesetzte Lektionen (kit-sync erst pushen; `~` nicht an Python) + 1 L37-Nachbau.
  `no-loss-check`-Report: 2 „Vor dem Checkpoint erledigen", 2 „Kann warten" (Ideen), **1 gefiltert = der L37-Nachbau**
- Struktur-Check: `🧩 Struktur-Check: 3/3 Anker in skills/dtb-lesson/SKILL.md gefunden` (Repo zuerst; `idea` nicht aufgeloest, kein Ideen-Fund dringend)
- Vorlage (Auszug): `1  Lektion  Vor kit-sync sync … erst pushen → lessons.md L39` / `2  Lektion  ~ nie an python -c … → lessons.md L40` / `Ok fuer alle nicht gestrichenen? (Ok / streiche {Nr,…} / behalte {Nr} / Abbruch)`
- Duplikat-Check (Schritt 3 `dtb:lesson`, Stichwort-Grep Rule-Spalte): L6/L35/L38 lexikalisch getroffen, andere Aussage → kein Treffer, nichts vorgestrichen
- Antwort: `Ok` → `✔ L39 → lessons.md`, `✔ L40 → lessons.md`; je 6 Spalten, Marker `(via Checkpoint 2026-09-08)` am Ende von `Context`, Datum, laufende Nummern 39/40; Hebe-Hinweis (`alle`) ausgegeben
- `git diff --stat dtb-project/project-rules/lessons.md` → `1 file changed, 2 insertions(+)`; Log-Zeile S2: `Verlustpruefung: 2 dringend → L39, L40 erfasst · 2 kann warten (Befehle im Report) · 1 gefiltert`
- **Ergebnis:** (a) belegt — Spec-Kriterium 1 (eine Vorlage, Eintraege mit Marker, korrekt nummeriert, Format wie von Hand), Kriterium 6 (Log-Zeile). **(d) NICHT belegt:** ein echtes Duplikat faellt bereits in Stufe 2 der Verlustpruefung (Ersetzungsprobe) und erreicht die Vorlage nie; die Vorstreichung greift nur bei semantisch neuen, lexikalisch aehnlichen Funden → fuer Kriterium 4 ist ein solcher Fund in Lauf 2/3 nachzustellen
- Nebenbefund: Pflicht-Abschlussfrage von `no-loss-check` steht direkt ueber der Vorlage — zwei Fragen, eine Antwort (Restabnahme bewerten)

**Wirklauf 2026-09-08 13:43 — Lauf 2, Fall (b) Streichen + Fall (d) Duplikat nachgeholt** (Checkpoint S3)
- Eingabe: 3 im Chat als dringend gesetzte Funde — 1 Idee (Abschlussfrage redundant), 2 Lektionen (Testfund-Design hinter semantischem Filter; kithash-Nachbildung kennzeichnen). Report: 3 dringend, 2 kann warten, 0 gefiltert, Randfall-3-Kopfzeile
- Struktur-Check: `🧩 Struktur-Check: 5/5 Anker in skills/dtb-lesson/SKILL.md, skills/dtb-idea/SKILL.md gefunden` (beide Quellen, weil beide Typen dringend)
- Duplikat-Check per Referenz: Idee gegen INBOX (#72/#69 anderer Gegenstand) kein Treffer; Lektion 2 (L8/L10 lexikalisch, andere Aussage) kein Treffer; **Lektion 3 trifft L7** („verbindliche Kommando-Sequenzen nie improvisieren") → in der Vorlage `~~3~~ … — aehnlich L7 (vorgestrichen; "behalte 3" nimmt sie auf)`
- Vorlage: `1  Idee … → INBOX.md #73` / `2  Lektion … → lessons.md L41` / `~~3~~ Lektion … aehnlich L7` / Abschlussfrage `Ok / streiche {Nr,…} / behalte {Nr} / Abbruch`
- Antwort: `streiche 2, 3` → Rueckbestaetigung nur des Geaenderten („2 gestrichen · 3 war bereits vorgestrichen · geschrieben wird nur 1"), dann `✔ #73 → INBOX.md` — neue Zeile oben (absteigende Sortierung des Bestands), Datum, `Offen`, Marker `(via Checkpoint 2026-09-08)` am Ende des Idee-Texts
- `git diff --stat INBOX.md` → `1 file changed, 1 insertion(+)`; `lessons.md` unveraendert gegenueber Lauf 1 (kein L41). Log-Zeile S3: `Verlustpruefung: 3 dringend → #73 erfasst · 2 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Spec-Kriterium 2 Teil 1 belegt (gestrichene Zeilen nicht geschrieben, genau 1 Eintrag), **Kriterium 4 belegt** (Duplikat-Treffer markiert + vorgestrichen, nicht geblockt), Kriterium 1 fuer den Ideen-Pfad belegt (Nummer 73, Format wie von Hand). Beobachtung: `dtb:idea` Schritt 2 legt die Einfuegeposition nicht fest — Bestand ist absteigend sortiert, oben eingefuegt

**Wirklauf 2026-09-08 13:49 — Lauf 3, geplant Fall (b) Abbruch, real Fall (a) Ideen-Pfad** (Checkpoint S4)
- Eingabe: 1 im Chat als dringend gesetzte Idee (`dtb:idea` Schritt 2 ohne Einfuegeposition). Report: 1 dringend, 2 kann warten, 0 gefiltert; die zwei in Lauf 2 gestrichenen Lektionen wurden NICHT wiederholt (Randfall 3 „bewusst verworfen" greift)
- Struktur-Check: `🧩 Struktur-Check: 2/2 Anker in skills/dtb-idea/SKILL.md gefunden` — nur `idea` aufgeloest, weil nur dieser Typ dringend (Regel „nur die Quellen, deren Typ vorkommt" belegt)
- Duplikat-Check per Referenz gegen INBOX: #61 (lessons.md unsortiert) anderer Gegenstand → kein Treffer
- Vorlage: `1  Idee … → INBOX.md #74` / Abschlussfrage. Antwort **`Ok`** (Testplan sah `Abbruch` vor) → `✔ #74 → INBOX.md`, oben, `Offen`, Marker `(via Checkpoint 2026-09-08)`
- `git diff --stat INBOX.md` → `2 insertions(+)` kumuliert (#73 + #74). Log-Zeile S4: `Verlustpruefung: 1 dringend → #74 erfasst · 2 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Kriterium 1 erneut fuer den Ideen-Pfad belegt; die Vorlage folgt der Antwort, nicht dem Testplan (korrekt). **Fall (b) Teil 2 (Abbruch) weiterhin offen** → Lauf 4. Nebenbefund: Randfall 3 von `no-loss-check` wirkt auf gestrichene Vorlage-Zeilen wie auf verworfene Report-Funde

**Wirklauf 2026-09-08 14:02 — Lauf 4, geplant Fall (b) Abbruch, real Fall (a) Lektionen-Pfad** (Checkpoint S5)
- Eingabe: 1 im Chat als dringend gesetzte Lektion (gestrichene Vorlage-Zeile = verworfen). Report: 1 dringend, 2 kann warten, 0 gefiltert, Randfall-3-Kopfzeile
- Struktur-Check: `🧩 Struktur-Check: 3/3 Anker in skills/dtb-lesson/SKILL.md gefunden`; Duplikat-Grep (verworfen/gestrichen/vertagen/Randfall) ohne Treffer
- Vorlage: `1  Lektion … → lessons.md L41`. Antwort **`Ok`** (Testplan: `Abbruch`) → `✔ L41 → lessons.md`, 6 Spalten, Marker, Datei 37 Zeilen
- Log-Zeile S5: `Verlustpruefung: 1 dringend → L41 erfasst · 2 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Kriterium 1 zum dritten Mal belegt (Lektionen-Pfad); **Fall (b) Abbruch weiterhin offen** → Lauf 5

**Wirklauf 2026-09-08 14:18 — Lauf 5, geplant Fall (b) Abbruch, real Fall (a) Ideen-Pfad** (Checkpoint S6)
- Eingabe: 1 im Chat als dringend gesetzte Idee (Kann-warten-Funde als Sammelzeile). Report: 1 dringend, 2 kann warten, 0 gefiltert, Randfall-3-Kopfzeile
- Struktur-Check: `🧩 Struktur-Check: 2/2 Anker in skills/dtb-idea/SKILL.md gefunden`; Duplikat-Grep gegen INBOX (#32 lexikalisch, anderer Gegenstand) kein Treffer
- Vorlage: `1  Idee … → INBOX.md #75`. Antwort **`Ok`** (Testplan: `Abbruch`) → `✔ #75 → INBOX.md`, oben, `Offen`, Marker
- Log-Zeile S6: `Verlustpruefung: 1 dringend → #75 erfasst · 2 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Kriterium 1 zum dritten Mal auf dem Ideen-Pfad belegt; **Fall (b) Abbruch nach drei Anlaeufen unbelegt** — Entscheidung des Nutzers: weiterer Lauf oder Text-Review der Abbruch-Zeile (Antwortregel `Abbruch → nichts schreiben, eine Meldezeile, weiter mit Schritt 1`)

**Wirklauf 2026-09-08 14:21 — Lauf 6, Fall (b) Abbruch** (Checkpoint S7)
- Eingabe: 1 im Chat als dringend gesetzte Lektion (tatsaechliche Antwort zaehlt als Fall). Report: 1 dringend, 2 kann warten, 0 gefiltert
- Struktur-Check: `🧩 Struktur-Check: 3/3 Anker in skills/dtb-lesson/SKILL.md gefunden`; Duplikat-Grep trifft **L14** (Kalibrierung an Faellen vs. Text-Review) → Zeile vorgestrichen `~~1~~ … — aehnlich L14` (zweiter Beleg Fall d)
- Vorlage: 1 Zeile, vorgestrichen. Antwort **`Abbruch`** → genau eine Meldezeile `Nichts erfasst — 1 Fund(e) bleiben als Befehle im Report`, weiter mit Schritt 1
- `git diff --stat lessons.md INBOX.md` unveraendert gegenueber Lauf 5 (3 + 3 insertions kumuliert, nichts Neues). Log-Zeile S7: `Verlustpruefung: 1 dringend → nichts erfasst (Abbruch) · 2 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Spec-Kriterium 2 Teil 2 belegt (Abbruch: nichts geschrieben, genau eine Meldezeile); Checkpoint brach nicht ab

**Wirklauf 2026-09-08 14:32 — Lauf 7, Fall (e) Anker-Drift, Fehlerpfad 2** (Checkpoint S8)
- Vorbereitung: `sed` in der Arbeitskopie `skills/dtb-lesson/SKILL.md`: `## Schritt 3: Duplikat-Check` → `## Schritt 3: Dublettenpruefung (DRIFT-TEST)`; Anker Repo 0, installiert 1; `git status` M
- Eingabe: 2 dringende Funde — 1 Idee (Vorlage-Frage bei nur vorgestrichenen Zeilen) + 1 **Lektion** (Fehlerpfad-Test im Typ der gedrifteten Quelle setzen; waehrend der Vorbereitung erkannt: ein Ideen-Fund allein haette `lesson` nie aufgeloest). Report 2 dringend, 2 kann warten, 0 gefiltert
- Struktur-Check: Repo-zuerst; `idea` 2/2, `lesson` **2/3** → `⚠ Struktur-Check fehlgeschlagen: skills/dtb-lesson/SKILL.md — Anker "## Schritt 3: Duplikat-Check" nicht gefunden. dtb:lesson wurde umgebaut; ich schreibe NICHT auf veralteter Basis …` — Rueckfall, **keine Vorlage, kein Dialog**, beide Funde als Befehle im Report; Checkpoint lief weiter
- `git diff --stat lessons.md INBOX.md` unveraendert (6 insertions kumuliert, nichts Neues). Log-Zeile S8: `Verlustpruefung: 2 dringend → nichts erfasst (Struktur-Check Fehlerpfad 2, Rueckfall) · 2 kann warten (Befehle im Report) · 0 gefiltert`
- Rueckholung: `git checkout -- skills/dtb-lesson/SKILL.md` → `git status --short skills/dtb-lesson/SKILL.md` leer (Automated-Kriterium „Nach Lauf 4")
- **Ergebnis:** Spec-Kriterium 5 Pfad 2 (Drift) belegt: eigene Meldung, kein Schreiben, Rueckfall. Nebenbefund: Fehlerpfad 2 zieht auch den unbetroffenen Ideen-Fund in den Rueckfall (Block-Regel „beide enden im Rueckfall") — bewusst so gebaut, im Review bewerten

**Wirklauf 2026-09-08 14:40 — Lauf 8, Fall (e) Datei fehlt, Fehlerpfad 1** (Checkpoint S9)
- Vorbereitung: `git mv skills/dtb-lesson/SKILL.md skills/dtb-lesson/SKILL.md.off` (Index R) + `mv ~/.claude/skills/dtb-lesson/SKILL.md{,.off}`; Hash der Kopie vorher `d920b323a5d49172b105eb8e30952722fc8481f7`
- Eingabe: 1 dringende **Lektion** (Rueckfall global vs. typweise). Report 1 dringend, 2 kann warten, 0 gefiltert
- Struktur-Check: Quelle `dtb:lesson` — Repo FEHLT, installiert FEHLT → `⚠ Erfassungs-Quelle dtb:lesson weder im Projekt (skills/) noch global (~/.claude/skills/) gefunden. → /dtb:kit-sync sync, Funde bleiben Befehle im Report.` — Rueckfall, keine Vorlage, kein Dialog; Checkpoint lief weiter (Session 9)
- Log-Zeile S9: `Verlustpruefung: 1 dringend → nichts erfasst (Struktur-Check Fehlerpfad 1, Rueckfall) · 2 kann warten (Befehle im Report) · 0 gefiltert`
- Rueckholung: `git mv …SKILL.md.off …SKILL.md` + `mv` der Kopie → `git status --short skills/dtb-lesson/` leer. **Zeuge:** `git hash-object` Kopie = Repo = `artifacts['skills/dtb-lesson/SKILL.md'].hash` im Lock = `d920b323…` (alle drei gleich); mtime der Kopie unveraendert `2026-09-08 13:02:02` (Sync-Zeit)
- **Ergebnis:** Spec-Kriterium 5 Pfad 1 (Installation) belegt — eigene Meldung, verschieden von Pfad 2, kein Schreiben, Rueckfall. Beide Fehlerpfade damit getrennt belegt (Lauf 7 + 8)

**Wirklauf 2026-09-08 14:47 — Lauf 9, Fall (c) leer** (Checkpoint S10)
- Eingabe: kein dringender Fund im Chat; die Rueckfall-Funde aus Lauf 7/8 stehen als Befehle in den Logs S8/S9 (rekonstruierbar → „Kann warten"). Report: **keine** Ueberschrift `## Vor dem Checkpoint erledigen`, 5 kann warten, 0 gefiltert
- Sammelvorlage entfiel still: kein leerer Block, kein Struktur-Check, keine Frage; „Kann warten" unveraendert als Befehle im Report
- Log-Zeile S10: `Verlustpruefung: 0 dringend · 5 kann warten (Befehle im Report) · 0 gefiltert`
- **Ergebnis:** Spec-Kriterium 3 belegt. Fall-Set komplett: a (Laeufe 1/3/4/5), b (2 streichen, 6 Abbruch), c (9), d (2 L7, 6 L14), e (7 Drift, 8 Datei fehlt); Kriterium 6 Log-Zeile in allen 9 Sessions

---

**Erstellt mit:** `/dtb:impl-plan`
