# Beispielausgaben: Rueckfragen-Defaults

**Zweck:** Abnahme der Zielform VOR dem Ausrollen in die Skills (Plan Schritt 1.2, L64).
Eine Ausgabe je Form, mit echten Daten. Abgenommen wird die Form, nicht jede Stelle.
Kanon: `skills/CLAUDE.md` → „## Rueckfragen-Defaults (Veto-Form)".

---

## 1. Textzeile — Slug-Vorschlag (`feature-discover` Schritt 5)

Daten: dieser Change (INBOX #57). Kein fester Artefakt-Name → Slug aus dem Feature-Namen.

```
Feature-Name: Rueckfragen-Defaults  →  Ordner: features/rueckfragen-defaults/  (Vorschlag)
→ weiter = uebernehmen · oder anderen Namen nennen
```

Variante mit Namensregel (Zusatz B) — Daten: Change `idea-rank` (lieferte den Skill `dtb:idea-rank`):

```
Feature-Name: idea-rank  →  Ordner: features/idea-rank/  (Vorschlag — Feature liefert den Skill `dtb:idea-rank`)
→ weiter = uebernehmen · oder anderen Namen nennen
```

Kollision (bleibt echte Rueckfrage, kein Vorschlag):

```
⚠ Ordner features/rueckfragen-defaults/ existiert bereits mit anderem Inhalt.
Anderen Feature-Namen nennen:
```

---

## 2. Knopf — Commit-Message (`implement` Ritual Punkt 6)

Daten: Phase 1 dieses Changes, Repo-Stil aus `git log --oneline -5` (Conventional Commits, deutsch, Umlaute ausgeschrieben).

Vorschau im Chat:

```
Commit-Vorschlag:
  feat(rueckfragen-defaults): Kanon der Veto-Form + Beispielausgaben (p1)

  - skills/CLAUDE.md: neue Sektion „Rueckfragen-Defaults (Veto-Form)"
  - features/rueckfragen-defaults/: discovery, spec, plan, beispielausgaben
```

Blockierende Auswahl (eine Frage, drei Knoepfe):

```
Frage: Phase 1 committen?
  ● Commit mit dieser Message (Vorschlag)
  ○ Message aendern
  ○ Abbrechen
```

Staging und Manual-Gate folgen demselben Muster — Staging: `Nur geplantes Set (Vorschlag)` / `Alles stagen` / `Abbrechen`; Manual-Gate: `passt — Phasen-Commit` / `Korrekturen`.

---

## 3. Sammelliste — impl-review-Triage (`impl-review` Schritt 9)

Daten: echtes Review `archive/feature-fast/review.md` (2026-08-02, 10 Findings).
Regel: einzeln = `S:Hoch` ODER aus einer FAIL-Achse → F1, F2. Rest (8) → Sammelliste.

Durchgang 1 — einzeln wie bisher (je eine Auswahl mit 4 Optionen):

```
F1 · [S:Hoch × I:Hoch] · Safety & Quality
skills/dtb-feature-fast/SKILL.md:12 vs. :200 — allowed-tools kann keine Datei loeschen,
Schritt 5.5 verlangt aber das Loeschen von fast-draft.md.
→ Fix: Bash in allowed-tools, Loesch-Schritte als explizites rm-Kommando.
  ● Fix anwenden  ○ Anders fixen  ○ Skip  ○ Als Lektion erfassen
```
(F2 analog)

Durchgang 2 — eine Liste:

```
8 weitere Findings — alle werden wie vorgeschlagen gefixt:

 1. F3  [S:Mittel] produces verschweigt INBOX.md/BACKLOG.md
        → produces um INBOX.md, BACKLOG.md ergaenzen
 2. F4  [S:Mittel] Kanten-Asymmetrie discover.next / fast.after / task.after
        → drei Frontmatter-Listen symmetrisch nachziehen
 3. F5  [S:Mittel] INBOX-Gate nicht in der Hard-Gate-Tabelle registriert
        → Zeile aufnehmen, fehlende Escape-Hatch begruenden
 4. F6  [S:Mittel] Lessons-Prior fehlt vor der Planerstellung
        → Lessons-Block analog impl-plan + consumes
 5. F7  [S:Mittel] Struktur-Check meldet fehlende Datei als Drift
        → zwei Fehlerpfade trennen + Fallback
 6. F8  [S:Mittel] fast-draft.md dem Derived-State-Kanon unbekannt
        → status-neutrale Zeile in DERIVED_STATE_RULES.md + Root-CLAUDE.md
 7. F9  [S:Niedrig] Plan-Entscheidungen verweisen auf geloeschte A-IDs
        → Begruendung ausschreiben statt A-ID
 8. F10 [S:Niedrig] Provenienz-Fusszeile vom Skill nicht angewiesen
        → Fusszeilen-Format in Schritt 5 definieren

Frage: Wie weiter mit diesen 8?
  ● Alle uebernehmen (Vorschlag)
  ○ Nummern streichen        → danach Freitext: „3, 7" (gestrichene = Skip; „7 Lektion" = Lektion)
  ○ Einzeln durchgehen       → bisheriger Ablauf je Finding
```

Abschluss (unveraendert): `10 Fixed · 0 Lesson · 0 Skipped`

---

## 4. Stille Anzeige — Backlog + Lektion (`task`, `feature-plan`, `impl-plan`)

Daten: dieser Change (Spec ohne Plan = `Spezifiziert`) bzw. Wegwerf-Ordner.

Backlog, Normalfall — letzte Zeilen des Abschlusses:

```
Feature gespeichert: dtb-project/project-workflows/features/rueckfragen-defaults/spec.md
→ in BACKLOG.md eingetragen (Status: Spezifiziert)
```

Backlog, Testordner:

```
Aufgabe gespeichert: dtb-project/project-workflows/features/zz-test-rueckfragen/task.md
→ kein BACKLOG-Eintrag (Testordner)
```

Backlog, Datei fehlt:

```
⚠ BACKLOG.md fehlt oder ist unlesbar — kein Eintrag, weiter
```

Lektion-Vormerkung (statt „Nach lessons.md uebernehmen? ja/nein") — Daten: echte Erkenntnis aus diesem Plan:

```
💡 Lektion-Kandidat vorgemerkt: „Regeln, die Bestandsprojekte erreichen sollen, gehoeren inline in
Klasse-A-Skills, nicht in den Klasse-B-Seed DERIVED_STATE_RULES.md" → wird beim Checkpoint erfasst
```

---

## Abgleich Zuordnung ↔ Festlegung (Plan Schritt 1.3)

Festlegung 2026-09-22: 17 Zeilen.

| Gruppe | Zeilen | In der Kanon-Zuordnung |
|--------|--------|------------------------|
| umgesetzt | Z1, Z2, Z3, Z7, Z9, Z10, Z11, Z13, Z14, Z15, Z16 (11) | je eine Tabellenzeile ✅ |
| unveraendert beim Menschen | Z5, Z6, Z8-Entscheidung, Z12, Z17 (+ Ueberschreib-Fragen) | Absatz „Bewusst beim Menschen" ✅ |
| nicht gebaut | Z4 | Absatz „Nicht gebaut" ✅ |
| Zusaetze Discovery 2026-09-30 | A, B, C, D, E (5) | je eine Tabellenzeile ✅ |

Summe: 11 + 5 + 1 = 17 ✅ · Zusaetze 5/5 ✅ · Tabellenzeilen 11 + 5 = 16 ✅

**Namens-Korrektur bei Z7:** Die Festlegung sagt „REVISE/REJECTED". `plan-review` kennt aber die
Verdikte SOUND / REVISE / RETHINK — REJECTED ist ein `impl-review`-Verdikt. Die Kanon-Zeile
verwendet deshalb REVISE/RETHINK (Sinn der Festlegung: „negatives Verdikt → direkt in die
Finding-Runde") — zur Bestaetigung beim Menschen vorgelegt. **Bestaetigt 2026-09-30** (Phase-1-Gate).

---

## Eigen-Text-Pruefung

Plan Schritt 5.1 (L15/L14), Stand nach `0f1850c` (Phasen 1–4). Drei Fragen je geaenderter Stelle:
**sichtbar?** (Default/Vorschlag erscheint vor der Wirkung) · **„weiter" eindeutig?** · **stiller
Default mit Commit-Folge?** (darf nie vorkommen).

| Stelle | Form | sichtbar | „weiter" eindeutig | stiller Commit-Default |
|--------|------|----------|--------------------|------------------------|
| `feature-discover` Schritt 5 — Slug | Textzeile | ✅ | ✅ `→ weiter = uebernehmen` | ✅ nein |
| `feature-discover` Schritt 2 / `impl-plan` 2b — Scan | Textzeile | ✅ | ✅ `→ weiter = Liste uebernehmen` | ✅ nein |
| `feature-fast` Schritt 1.3 — Slug | Kopfzeile der Sammelvorlage | ✅ `Ordner: …` | ✅ ueber das „Ok" der Vorlage | ✅ nein |
| `task` / `bug-report` / `feature-plan` / `feature-fast` — Backlog | stille Anzeige | ✅ Anzeige-Zeile | n/a (keine Frage) | ✅ nein (schreibt BACKLOG, committet nicht; Worktree-Guard unveraendert) |
| `plan-review` Schritt 5 — REVISE/RETHINK | stille Anzeige | ✅ | n/a; Findings einzeln | ✅ nein (Plan-Edits nur nach Bestaetigung je Empfehlung) |
| `impl-plan` / `debug-plan` — Lektion | stille Anzeige (Vormerk-Zeile) | ✅ | n/a | ✅ nein (kein Write in `lessons.md`) |
| `impl-review` Schritt 9 — Sammel-Findings | Sammelliste + Knopf | ✅ je Zeile Befund + Fix | ✅ `Alle uebernehmen (Vorschlag)` | ✅ nein (kein Commit; kein Fix ohne sichtbare Zeile) |
| `feature-start` Abschluss | stille Anzeige | ✅ `→ Weiter mit: …` | n/a | ✅ nein (startet nichts selbst) |
| `implement` Punkt 2 — Manual-Gate | Knopf | ✅ Kriterien gelistet | ✅ `passt — Phasen-Commit` | ✅ nein (Entscheidung beim Menschen) |
| `implement` Punkt 3 — Staging | Knopf | ✅ fremde Pfade gelistet | ✅ `Nur geplantes Set (Vorschlag)` | ✅ nein |
| `implement` Punkt 6 — Commit-Message | Knopf | ✅ Message vollstaendig | ✅ `Commit mit dieser Message (Vorschlag)` | ✅ nein |
| `implement` Punkt 11 — Naechste Phase | stille Anzeige | ✅ `→ weiter mit Phase …` | n/a; „Stopp" jederzeit | ✅ nein (der naechste Commit braucht das naechste Gate) |

**Widerspruchsfreiheit Kanon ↔ Inline:** alle 16 Zuordnungszeilen gegen die Inline-Texte gelesen —
keine Abweichung im Verhalten. Zwei bewusste Formvarianten, kein Widerspruch: (a) die Scan-Textzeile
fuellt den Slot `{Alternative}` mit „Pfade nennen, die fehlen oder wegfallen"; (b) der
Manual-Gate-Knopf traegt KEIN `(Vorschlag)`, weil er kein Default ist, sondern eine Entscheidung
beim Menschen (Z8, nie automatisch).

**Siegel-Check** (Stellen „nie automatisch", Trefferzahl `master` = Arbeitsbaum):

| Datei | Ankerphrase | master / jetzt |
|-------|-------------|----------------|
| `feature-discover` | „Kleinfall-Weiche" | 1 / 1 ✅ |
| alle Skills | „Fehlalarm" (Escape-Hatch) | 7 / 7 ✅ |
| `implement` | „Mismatch-Handling (Plan ≠ Realitaet)" | 1 / 1 ✅ |
| `feature-plan` | „Soll ich die existierende Spec ueberschreiben oder aktualisieren?" | 1 / 1 ✅ |
| `impl-plan` | „Implementierungsplan existiert bereits. Soll ich ueberschreiben" | 1 / 1 ✅ |
| `impl-review` | „Ueberschreiben / Erst Triage fortsetzen / Abbrechen?" | 1 / 1 ✅ |
| `feature-fast` | „Kernfragen-Budget (max. 3)" | 1 / 1 ✅ |

0 Abweichungen. (Erster Zaehlversuch fuer „Fehlalarm" scheiterte am fehlenden `bc` — Werkzeug-,
kein Datenbefund, L7; mit `awk` neu gezaehlt.)

**Spiegel-Zaehlung** (feste Zeilen, Zielzahl = Anwender-Stellen):

| Feste Zeile | Soll | Ist | Anmerkung |
|-------------|------|-----|-----------|
| `→ weiter =` (Textzeile) | 2 | 2 ✅ | discover, impl-plan — Soll von 3 auf 2 gesenkt (Mismatch 2.3: feature-fast ohne eigene Frage) |
| Knopf-Stellen | 4 | 4 ✅ | implement 3 (Gate, Staging, Commit) + impl-review 1 (Sammelliste) |
| `Lektion-Kandidat vorgemerkt` | 3 | 4 ✅ | impl-plan, debug-plan, no-loss-check + `lesson` (Spiegel aus Schritt 3.2, im Plan-Soll nicht mitgezaehlt) |
| `→ in BACKLOG.md eingetragen (Status:` | 4 | 4 ✅ | task, bug-report, feature-plan, feature-fast |

---

## Abnahme-Probelauf

Plan Schritt 5.3, 2026-10-01. **Ort:** Wegwerf-Clone `Projekte/.dtb-worktrees/zz-probe-rueckfragen`
(Branch `feature/rueckfragen-defaults` @ `0f1850c`, Haupt-Checkout-Situation — Guards lassen durch;
der Scratchpad der Session stand nicht mehr zur Verfuegung, Ort vom Menschen gewaehlt). Skills nach
der **Repo-Fassung** im Clone gelesen und ausgefuehrt (L74), nicht nach der installierten Kopie.
Alle Probe-Objekte vom Lauf selbst erzeugt (L57). Clone danach geloescht.

| Stelle | Probe | Beobachtet | Befund |
|--------|-------|------------|--------|
| `task` Schritt 5 — Normalfall | Aufgabe `probe-rueckfragen` | keine Frage; BACKLOG-Zeile in „Aufgaben" (Status Offen), Datum aktualisiert; Anzeige `→ in BACKLOG.md eingetragen (Status: Offen)` | ✅ |
| `task` Schritt 5 — Testordner | Aufgabe `zz-test-rueckfragen` | keine Frage, kein Eintrag; Anzeige `→ kein BACKLOG-Eintrag (Testordner)` | ✅ |
| `feature-discover` Schritt 2 / 5 | Ausgabe nach Repo-Text, Daten INBOX #107 | Scan-Tabelle + `→ weiter = Liste uebernehmen …`; Slug-Vorschlag + `→ weiter = uebernehmen …` | ✅ (Form; kein Voll-Lauf) |
| `implement` Punkt 2 — Manual-Gate | Mini-Plan `zz-test-mini`, Phase 1 | Knopf `passt — Phasen-Commit` / `Korrekturen` → Mensch: passt | ✅ |
| `implement` Punkt 3 — Staging | fremde Datei `zz-fremd.txt` | Knopf mit fremdem Pfad gelistet, erste Option `Nur geplantes Set (Vorschlag)` → gewaehlt; `zz-fremd.txt` blieb liegen | ✅ |
| `implement` Punkt 6 — Commit-Message | Message vollstaendig gezeigt | Knopf `Commit mit dieser Message (Vorschlag)` → gewaehlt; Commit `5837eab` im Clone, SHA zurueckgeschrieben | ✅ |
| `implement` Punkt 11 — Naechste Phase | Mini-Plan hat Phase 2 | Schwelle erreicht (Session hatte bereits >2 Phasen) → `→ Schwelle erreicht (2 Phasen in dieser Session) — weiter in neuer Session: …`, Stopp | ✅ |

**Eindruck des Menschen (Manual-Kriterium):** die drei Knoepfe hintereinander (Gate → Staging →
Commit) sind **angenehmer** als die bisherigen Freitext-Antworten „passt / 1 / ok" (2026-10-01).

**Grenze des Probelaufs:** `plan-review` (Direkteinstieg), `impl-review` (Sammelliste) und die
Lektion-Vormerkung wurden nicht live gefahren — sie sind ueber die Beispielausgaben (Phase 1) und
das Phase-3-Gate abgenommen; ihr erster echter Lauf ist das `/dtb:impl-review` dieses Changes.
