# Implementierungsplan: Checkpoint schneller

**Erstellt:** 2026-11-02
**Feature-Spec:** `features/checkpoint-schneller/spec.md`
**Geschaetzte Dauer:** 2,5–3 h (Nachmessung nach dem Merge nicht eingerechnet)
**Status:** Reviewed (plan-review 2026-11-02: REVISE → 5 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Checkpoint-Text verschlanken (Weiter-Zeile, ein Kontrollpunkt, Dashboard bedingt) | 1,5–2 h | Geplant |
| Phase 2 | Messgrundlage sichern, Doku und Spiegel, Probelauf | 1 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Betroffene Module + Messung), Stichproben per Grep am 2026-11-02 verifiziert.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | 757 Zeilen. Schritt 0 (Z. 459–569): Verlustpruefung + eigene Sammelvorlage mit Antwortregeln. Schritt 1 (Z. 571–628): Hand-off-Empfang, Git, Aufgaben-Vergleich mit Zuordnungsfragen (Z. 599–610) und eigener ⏳-Vorlage (Z. 612–624) — also bis zu drei Rueckfrage-Runden nacheinander. Schritt 4b (Z. 703–733): Dashboard, Schalter `dashboard.bei_checkpoint` (Z. 712), keine Existenzpruefung der Seite. Schritt 6 (Z. 742–757): Bestaetigung ohne Commit-Hinweis; eine Commit-Frage steht nirgends (Grep `committen\|commit-and-push` → nur Z. 276) |
| `skills/CLAUDE.md` | „Rueckfragen-Defaults (Veto-Form)": vier Formen, Zuordnungstabelle mit Zeilen 1–16 und A–H |
| `CLAUDE.md` | Z. „Session lifecycle": Kurzbeschreibung `workflow-checkpoint` ohne Hinweis auf Commit-Uebergang oder Kontrollpunkt |
| `README.md` | Z. 100: „refreshed by `workflow-checkpoint` unless `dashboard.bei_checkpoint: false`" |
| `skills/dtb-project-dashboard/SKILL.md` | Z. 25, 53: Aufruf aus Checkpoint-Schritt 4b, Modus „ohne Browser" |
| `skills/dtb-project-init/SKILL.md` | Z. 113 (Config-Vorlage), Z. 129 (Erklaerung des Schalters) |
| `features/checkpoint-schneller/checkpoint-phasen.py`, `checkpoint-rueckfragen.py` | Mess-Skripte aus der Erhebung (Scratchpad-Stand, gesichert); das zweite laedt das erste per `exec` ueber den alten Dateinamen `cp_phases.py` — so nicht lauffaehig |

---

## Phase 1: Checkpoint-Text verschlanken

### Ziel
Der Checkpoint fragt vor dem Schreiben hoechstens einmal, stellt keine Commit-Frage mehr und frischt
das Dashboard nur auf, wo es eine Seite gibt — die Verlustpruefung bleibt unveraendert.

### Schritte

#### Schritt 1.1: Weiter-Zeile statt Commit-Frage
- **Zweck:** Groesster Einzelposten der Wartezeit (35 %, 55×) entfaellt; der Slash-Befehl beendet zugleich das Mess-Segment
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 6)
- **Input:** Bestaetigungs-Template Z. 744–757; Form „Stille Anzeige" aus `skills/CLAUDE.md`
- **Output:** Im Template eine Zeile `→ Weiter mit: /dtb:commit-and-push` (nach „Naechster Schritt"); darunter die Regel: nach der Bestaetigung keine Rueckfrage, ob committet oder gepusht werden soll — der Mensch setzt den Befehl ab. Im verlinkten Worktree unveraendert (Voll-Guard bricht vorher ab)

#### Schritt 1.2: Ein Kontrollpunkt vor dem Schreiben
- **Zweck:** Bis zu drei Rueckfrage-Runden (Verlust-Sammelvorlage, Zuordnungsfragen, ⏳-Vorlage) werden eine
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 0 „Funde erfassen", Schritt 1 „Aufgaben-Vergleich" und „⏳ Alter")
- **Input:** Antwortregeln beider Vorlagen; Kopplungs-Hinweise (Format von `no-loss-check`, §9-Kopie mit Anker `Aufgaben-Abgaenge`)
- **Output:** Neue Unter-Sektion `#### Kontrollpunkt (eine Rueckfrage-Runde)` am Ende von Schritt 1. Ablauf: Schritt 0 ermittelt die Verlustfunde und bereitet sie vor (Struktur-Check, Duplikat-Vorbereitung) — zeigt aber keine eigene Vorlage mehr; Schritt 1 fuehrt den Aufgaben-Vergleich aus und sammelt unsichere Zuordnungen und faellige ⏳-Aufgaben; der Kontrollpunkt zeigt alle drei Teile in EINER Nachricht (Teile ohne Inhalt entfallen, ohne Inhalt in allen Teilen keine Runde). Antwortregeln je Teil bleiben gueltig und sind kombinierbar („Ok, passt", „streiche 2 · 1 erledigt"); unklar → eine Rueckfrage, dann Abbruch nur des unklaren Teils. Geschrieben wird erst danach (Verlustfunde wie bisher per Referenz). Rueckfall „> 10 Funde" und Mengenprobe (L90) bleiben. Die Abnahme-Frage (Schritt 2) bleibt eigene Runde. Kopplungs-Hinweise an den neuen Ort mitziehen, ebenso die Verweise innerhalb des Skills auf die alte Vorlage in Schritt 0 („Sammelvorlage (Unterabschnitt unten)", „die Vorlage ist der eine Kontrollpunkt", Quelle der Verlustpruefungs-Zeile in den Log-Richtlinien, Wartungs-Hinweis zum Ausgabe-Muster von `no-loss-check`)

#### Schritt 1.3: Dashboard nur bei vorhandener Seite
- **Zweck:** Keine Erzeugung in Projekten, in denen niemand die Seite angelegt hat
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Schritt 4b, Punkt 1)
- **Input:** Schalter-Regel Z. 712–713
- **Output:** Punkt 1 ergaenzt: zusaetzlich zum Schalter muss `dtb-project/project-dashboard.html` existieren; fehlt die Seite → Schritt still ueberspringen, keine Zeile in Schritt 6 (die Seite entsteht nur per `/dtb:project-dashboard`)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Geaenderte `skills/dtb-workflow-checkpoint/SKILL.md` (Schritte 0, 1, 4b, 6)

### Checkpoint-Kriterien

#### Automated
- [ ] `sed -n '/^### Schritt 6: Bestaetigung/,$p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'Weiter mit: /dtb:commit-and-push'` ≥ 1
- [ ] `grep -c '^#### Kontrollpunkt (eine Rueckfrage-Runde)$' skills/dtb-workflow-checkpoint/SKILL.md` = 1
- [ ] `sed -n '/^#### Funde erfassen/,/^### Schritt 1/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c '^Ok fuer alle nicht gestrichenen'` = 0 (die eigene Vorlage in Schritt 0 ist weg; Wirkstellen-Anker statt Datei-Grep)
- [ ] `sed -n '/^#### Kontrollpunkt/,/^### Schritt 2/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'nicht gestrichenen\|alle behalten'` ≥ 2 (beide Antwortformen am neuen Ort)
- [ ] `grep -c 'Aufgaben-Abgaenge' skills/dtb-workflow-checkpoint/SKILL.md` ≥ 3 (Log-Format, Richtlinie, §9-Kopplungsanker bleiben)
- [ ] `sed -n '/^### Schritt 4b/,/^### Schritt 5/p' skills/dtb-workflow-checkpoint/SKILL.md | grep -c 'project-dashboard.html'` ≥ 2 (Seitenpfad + neue Existenzbedingung)
- [ ] `git diff --stat $(git merge-base master HEAD) -- skills/dtb-no-loss-check/ skills/dtb-project-dashboard/SKILL.md` zeigt in Phase 1 keine Aenderung an `no-loss-check`

#### Manual
- [ ] Beispiel-Ausgabe des Kontrollpunkts im Chat gezeigt und vom Menschen als lesbar abgenommen — in zwei Varianten: (a) alle drei Teile (Verlustfunde, unsichere Zuordnung, faellige ⏳-Aufgabe), (b) nur ein Teil. Grundlage ist der echte Stand im Haupt-Checkout (offene Aufgaben aus dessen `WORKFLOW_STATUS.md`, Verlustfunde dieser Session); fehlt dort ein Teil, wird er durch eine sichtbar als Attrappe gekennzeichnete Zeile ersetzt (per Review-Finding bestaetigt 2026-11-02)

---

## Phase 2: Messgrundlage, Doku, Probelauf

### Ziel
Die Messung ist wiederholbar, alle Spiegel und die Kit-Doku stimmen, und ein echter Lauf belegt das neue Verhalten.

### Schritte

#### Schritt 2.1: Mess-Skript fertigstellen
- **Zweck:** Nachmessung nach dem Merge mit demselben Werkzeug (Protokolle reichen nur 30 Tage, L106)
- **Dateien:** `features/checkpoint-schneller/checkpoint-phasen.py` (aendern), `features/checkpoint-schneller/checkpoint-rueckfragen.py` (loeschen)
- **Input:** beide Erhebungs-Skripte
- **Output:** EIN Skript mit Schalter `--rueckfragen` (Wartezeit nach Rueckfrage-Art, nur Zahlen und Kategorien), `--auszuege` (zusaetzlich Klartext-Auszuege von Frage und Antwort) und `-v` (Tabelle je Lauf); Kopf-Docstring mit Aufruf, Segment-/Kern-Definition, benannten Grenzen (Phasen-Zuordnung per Werkzeug-Heuristik; Projekte mit abweichendem Changelog-Pfad) und der Warnung: Auszuege stammen aus fremden Sitzungen, enthalten Personennamen und gehoeren nie in versionierte Dateien (L109); Ausgabe-Encoding im Skript gesetzt (L92); ohne `exec`

#### Schritt 2.2: Doku und Spiegel nachziehen
- **Zweck:** Kit-Doku und alle Stellen, die das alte Verhalten beschreiben, stimmen ueberein (L3, Kopplungs-Regel)
- **Dateien:** `skills/CLAUDE.md` (Zuordnungstabelle „Rueckfragen-Defaults": neue Zeile `I` fuer Weiter-Zeile = Stille Anzeige und Kontrollpunkt = eine Runde; Zwei-Becken-Tabelle Z. 374 „(Schritt 0)"), `CLAUDE.md` (Session lifecycle: ein Satz zu Kontrollpunkt und Weiter-Zeile; Z. 91 „written by `dtb:workflow-checkpoint` step 0"), `README.md` Z. 100, `skills/dtb-project-dashboard/SKILL.md` Z. 25, `skills/dtb-project-init/SKILL.md` Z. 129, die Kopplungs-Hinweise „(Schritt 0, Sammelvorlage)" — nur Hinweistext, kein Verhalten — in `skills/dtb-no-loss-check/SKILL.md` Z. 311, `skills/dtb-lesson/SKILL.md` Z. 113/156/177, `skills/dtb-idea/SKILL.md` Z. 79/118, `skills/dtb-idea-triage/SKILL.md` Z. 778 (7 Stellen, Grep 2026-11-02), dazu `skills/dtb-idea-triage/SKILL.md` Z. 99 (Herkunft der Becken-Eintraege)
- **Input:** repo-weiter Grep nach `workflow-checkpoint` + `Sammelvorlage`, `workflow-checkpoint` + `Schritt 0`/`step 0`, `bei_checkpoint`, `Schritt 4b`, `⏳` (Fundstellen ausserhalb `dtb-project/project-changelog/` und `archive/`); `Schritt 0` bleibt richtig, wo nur der Struktur-Check oder die Quellen-Aufloesung gemeint ist (z. B. `idea-triage` Z. 305, `project-dashboard` Z. 162)
- **Output:** jede Fundstelle, die das alte Verhalten beschreibt, angepasst; Fundliste mit Entscheidung „angepasst / passt schon" im Session-Log dieser Session

#### Schritt 2.3: Probelauf im Haupt-Checkout
- **Zweck:** Das neue Verhalten an einem echten Stand belegen — im Worktree bricht der Voll-Guard ab
- **Dateien:** `features/checkpoint-schneller/probelauf.md` (neu, status-neutral: Datum, Projekt, Zahl der Rueckfrage-Runden, welche der drei Teile des Kontrollpunkts vorkamen, Commit-Frage ja/nein, Dashboard-Verhalten, Verlustfunde)
- **Input:** Die Orchestrator-Session im Haupt-Checkout fuehrt ihren naechsten regulaeren Checkpoint nach der Worktree-Fassung `skills/dtb-workflow-checkpoint/SKILL.md` aus (L74: Repo-Fassung, nicht installierte Kopie). Rollen: Der Orchestrator fuehrt aus und schreibt nichts in diesen Worktree; der Mensch meldet das Ergebnis in dieser Pane; die Worktree-Session schreibt `probelauf.md`
- **Output:** `probelauf.md` mit dem Beleg; Abweichungen als Nacharbeit in Phase 2 vor der Abnahme (L97). Fuer den Hand-off vorgemerkt (Feld „Offene Punkte / Naechste Schritte"): `Nachmessung #177: Median ≤ 4 aktive min nach ≥ 10 Laeufen (chain-metrics + checkpoint-phasen.py) und 3 Vergleichslaeufe — bis 2026-12-02` — der Orchestrator fuehrt das als offene Aufgabe in `WORKFLOW_STATUS.md`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `features/checkpoint-schneller/checkpoint-phasen.py` (ein Skript, dokumentiert)
- [ ] Angepasste Doku: `skills/CLAUDE.md`, `CLAUDE.md`, `README.md`, `skills/dtb-project-dashboard/SKILL.md`, `skills/dtb-project-init/SKILL.md`
- [ ] `features/checkpoint-schneller/probelauf.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `python -I dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py` endet mit Exit 0 und gibt eine Zeile mit `Checkpoint-Segmente` aus; mit `--rueckfragen` ebenso eine Zeile mit `Commit/Push`
- [ ] `test ! -f dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-rueckfragen.py`
- [ ] `grep -c 'exec(' dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py` = 0
- [ ] `python -I dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py --rueckfragen | grep -c ' Q: \| A: '` = 0 (ohne `--auszuege` kein Klartext aus fremden Sitzungen)
- [ ] `grep -r 'Schritt 0, Sammelvorlage' skills/ | wc -l` = 0 und `grep -c 'checkpoint. step 0' CLAUDE.md` = 0 (Verweise auf den alten Ort nachgezogen)
- [ ] `grep -c '^| I |' skills/CLAUDE.md` = 1
- [ ] `grep -n 'workflow-checkpoint' README.md | grep -c 'exist'` ≥ 1 (Dashboard-Bedingung in der README genannt)
- [ ] `test -f dtb-project/project-workflows/features/checkpoint-schneller/probelauf.md`

#### Manual
- [ ] Probelauf belegt in `probelauf.md`: hoechstens eine Rueckfrage-Runde vor dem Schreiben (Abnahme ausgenommen), keine Commit-Frage, Weiter-Zeile sichtbar, Verlustpruefung gelaufen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Commit nach dem Checkpoint | A: Weiter-Zeile auf `commit-and-push` · B: Commit-Knopf im Checkpoint | A | Keine zweite Commit-Logik neben `commit-and-push`; Form „Stille Anzeige" wie bei `feature-start` (per Veto-Vorlage bestaetigt 2026-11-02) |
| Rueckfrage-Runden | A: eine gebuendelte Nachricht · B: Vorlagen einzeln wie bisher | A | Wartezeit ist der groesste Block (39 % der Kern-Zeit); Antwortregeln je Teil bleiben, nur die Runde wird gemeinsam |
| Abnahme-Frage | A: in den Kontrollpunkt · B: eigene Runde | B | Explizite Entscheidung mit Beleg-Rueckfrage, bewusst beim Menschen |
| Dashboard | A: nur bei vorhandener Seite · B: Default `bei_checkpoint: false` | A | Feature erst seit 2026-10-27 aktiv; B ist der benannte naechste Hebel, falls die Nachmessung ≤ 4 min verfehlt |
| Verlustpruefung | A: unveraendert immer · B: bedingt | A | Findet oft etwas (Sammelvorlage 38× in 74 Laeufen); „dieselben Funde" ist damit vom Aufbau her gesichert |
| Ablage der Messung | A: Change-Ordner · B: Nachbar-Repo mega.dev | A | Reist mit dem Change und wird mit ihm archiviert; Uebernahme nach mega.dev bleibt moeglich |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Weiter-Zeile statt Commit-Frage — `083b8d4`
- [x] 1.2 Ein Kontrollpunkt vor dem Schreiben — `083b8d4`
- [x] 1.3 Dashboard nur bei vorhandener Seite — `083b8d4`
- [x] 2.1 Mess-Skript fertigstellen
- [x] 2.2 Doku und Spiegel nachziehen
- [x] 2.3 Probelauf im Haupt-Checkout

---

## Umsetzung

Umsetzung mit `/dtb:implement Checkpoint schneller` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/checkpoint-schneller/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).
Nach dem Merge: Nachmessung (Median ≤ 4 min nach ≥ 10 Laeufen) und 3 Vergleichslaeufe, spaetestens
2026-12-02 — keine Progress-Schritte. Traeger ist der Hand-off (Schritt 2.3): der Auftrag steht unter
„Offene Punkte / Naechste Schritte", der Orchestrator uebernimmt ihn als offene Aufgabe in
`WORKFLOW_STATUS.md`; `spec.md`/`discovery.md` nennen ihn zusaetzlich als offenen Punkt.

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-02)
