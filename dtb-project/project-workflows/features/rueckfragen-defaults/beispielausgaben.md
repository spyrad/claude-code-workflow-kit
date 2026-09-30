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
Finding-Runde") — zur Bestaetigung beim Menschen vorgelegt.
