# Implementierungsplan: Ideen-Becken

**Erstellt:** 2026-09-08
**Feature-Spec:** `features/ideen-becken/spec.md`
**Geschaetzte Dauer:** 3 Phasen, ca. 5-7 Stunden
**Status:** Reviewed (plan-review 2026-09-08: REVISE → 6 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Becken-Format und Triage-Skill (Neubau, nichts wird umgehaengt) | ~3 h | Geplant |
| Phase 2 | Schreiber umstellen: Checkpoint, Nummernvergabe, Verlustpruefung | ~2 h | Geplant |
| Phase 3 | Verteilung, Doku, Wirklaeufe | ~1.5 h | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-idea-triage/SKILL.md` | Existiert nicht — Neubau-Ziel dieses Plans (L5: kein Scan-Ausloeser) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 470 Zeilen, Budget ausgeschoepft. Schritt 0 schreibt Ideen-Funde nach `INBOX.md` (Z. 346, 364-368); Struktur-Check-Tabelle Z. 313 greppt auf `## Schritt 2: In INBOX.md speichern` in `dtb:idea`; Archiv-Zaehler Z. 451; `next: [dtb:workflow-resume]` |
| `skills/dtb-no-loss-check/SKILL.md` | 421 Zeilen. Abgleich-Quelle Z. 128 = Idee-Spalte JEDER Zeile in `INBOX.md`, Status egal (Z. 146); Zielangaben Z. 30, 235, 243, 284, 388 |
| `skills/dtb-project-init/SKILL.md` | 501 Zeilen. Ordnerbaum Z. 129 listet `project-workflows/`; Pfad-Defaults Z. 91/113 |
| `skills/dtb-project-health/SKILL.md` | 392 Zeilen. Sektion „INBOX Integritaet" Z. 89, „INBOX → Features" Z. 84, Report-Zeile Z. 282 |
| `skills/dtb-idea/SKILL.md` | 163 Zeilen. Nummernvergabe Schritt 2 („Naechste laufende Nummer") liest nur `INBOX.md`; Duplikat-Check als Referenzquelle nutzbar |
| `CLAUDE.md` (116 Z.), `skills/CLAUDE.md` (541 Z.) | Doku: Output-Locations, Skill-Kategorien, Konventionen |

---

## Phase 1: Becken-Format und Triage-Skill

### Ziel

Das Becken existiert als Datei mit festgelegtem Format, und `dtb:idea-triage` kann es sichten,
befoerdern, verwerfen und liegenlassen — ohne dass ein bestehender Schreiber schon umgestellt ist.
Nach dieser Phase ist der Neubau fuer sich lauffaehig und aendert am Bestand nichts.

### Schritte

#### Schritt 1.1: Becken-Format festlegen und Datei anlegen
- **Zweck:** Ein festes Tabellenformat, bevor irgendein Skill hineinschreibt — sonst entstehen zwei Formate
- **Dateien:** `dtb-project/project-workflows/INBOX-BEFUNDE.md` (neu)
- **Input:** Format von `INBOX.md` (4 Spalten) + die Sichtung-Spalte aus dem Design
- **Output:** Datei mit Header und Tabellenkopf `| # | Datum | Befund | Sichtung |`, keine Datenzeile.
  Sichtung-Werte: leer (neu), `L1 YYYY-MM-DD` (einmal liegengelassen), `Altbestand` (Migration).
  Feld-Hygiene wie `INBOX.md`: literale Pipes im Textfeld escapen (Fehlerbild INBOX #70)

#### Schritt 1.2: Skill-Geruest `dtb:idea-triage` mit Guards
- **Zweck:** Der Skill schreibt globale Dateien und ist lesend-entscheidend — Guards gehoeren vor die erste Zeile Fachlogik, nicht danach
- **Dateien:** `skills/dtb-idea-triage/SKILL.md` (neu)
- **Input:** Guard-Bloecke aus `skills/dtb-idea-review/SKILL.md` (Worktree-Guard, Lesestand-Pruefung), Frontmatter-Konvention
- **Output:** Datei mit Frontmatter (`disable-model-invocation: true`, `allowed-tools`, Pipeline-Metadaten),
  Worktree-Guard, Config-Laden, Lesestand-Pruefung (mtime vor JEDER Statusentscheidung),
  Selbstanlage des Beckens bei Fehlen (Seed-Skew, INBOX #22)

#### Schritt 1.3: Sichtungs-Regel und Dreifach-Entscheidung
- **Zweck:** Der Kern des Ventils — welche Eintraege ein Lauf sichtet und was er mit ihnen tut
- **Dateien:** `skills/dtb-idea-triage/SKILL.md`
- **Input:** Design-Entscheidungen: nur Neue + faellige `L1` + max. `altbestand_pro_lauf` Altbestand, aelteste zuerst
- **Output:** Sichtungs-Regel als Auswahl-Abschnitt; je Eintrag Einzelentscheidung
  (befoerdern / verwerfen / liegenlassen), Liegenlassen nur bei leerer Sichtung;
  **jede Entscheidung wird sofort geschrieben**, nicht am Lauf-Ende gesammelt (loest #71 mit);
  Verwerfen verlangt eine Begruendung (Pflicht, ein Satz)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Beförderung, Archiv-Ausgang und Alterungshinweis
- **Zweck:** Die beiden Ausgaenge des Beckens vollstaendig machen
- **Dateien:** `skills/dtb-idea-triage/SKILL.md`, `dtb-project/project-workflows/archive/INBOX-BEFUNDE-verworfen.md` (bei Bedarf)
- **Input:** Duplikat-Check-Mechanik aus `dtb:idea` (per Referenz, nicht kopieren — Spiegel-Kopplung vermeiden)
- **Output:** Beförderung schreibt die Zeile unter die Trennzeile von `INBOX.md` (setzt #74 um), Status `Offen`,
  Vermerk `(befoerdert YYYY-MM-DD)`, Nummer bleibt; Duplikat-Check unscharf NUR gegen `INBOX.md`;
  Verwerfen haengt Zeile + Begruendung an die Archivdatei (bei Fehlen mit Header anlegen);
  Alterungshinweis vergleicht das Aenderungsdatum der im Befund genannten Datei mit dem Befund-Datum
  und entfaellt ersatzlos, wenn keine Datei erkennbar ist oder die Historie nicht abfragbar ist

#### Schritt 1.5: Abschluss-Bilanz und Pipeline-Kanten beidseitig
- **Zweck:** Lauf-Ende sichtbar machen und die drei Kanten sofort beidseitig setzen (INBOX #46/#58: halbseitige Kanten sind der Bestandsfehler, den dieses Feature nicht vergroessern darf)
- **Dateien:** `skills/dtb-idea-triage/SKILL.md`, `skills/dtb-workflow-checkpoint/SKILL.md`, `skills/dtb-idea-review/SKILL.md`
- **Input:** Kanten-Tabelle aus `discovery.md` → Integrationspunkte
- **Output:** Bilanz `Befoerdert: N · Verworfen: N · Liegengelassen: N` plus genau eine Hinweiszeile auf
  `/dtb:idea-review`, wenn befoerdert wurde; Frontmatter: `dtb:idea-triage` mit `stage: idea`,
  `after: [dtb:workflow-checkpoint]`, `next: [dtb:idea-review]`; `dtb:workflow-checkpoint`
  `next: [dtb:workflow-resume, dtb:idea-triage]`; `dtb:idea-review` `after: [dtb:idea, dtb:idea-triage]`

### Deliverables
- [ ] `INBOX-BEFUNDE.md` mit festgelegtem Format
- [ ] `skills/dtb-idea-triage/SKILL.md` vollstaendig
- [ ] Drei Pipeline-Kanten beidseitig notiert

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f dtb-project/project-workflows/INBOX-BEFUNDE.md` und die Datei enthaelt genau eine Zeile, die auf `| Sichtung |` endet
- [ ] `test -f skills/dtb-idea-triage/SKILL.md`
- [ ] `grep -c 'disable-model-invocation: true' skills/dtb-idea-triage/SKILL.md` = 1
- [ ] Frontmatter des neuen Skills enthaelt `after: [dtb:workflow-checkpoint]` und `next: [dtb:idea-review]` (Grep im `pipeline:`-Block, nicht im Fliesstext — L2)
- [ ] `grep -F 'dtb:idea-triage' skills/dtb-workflow-checkpoint/SKILL.md` trifft in der `next:`-Zeile
- [ ] `grep -F 'dtb:idea-triage' skills/dtb-idea-review/SKILL.md` trifft in der `after:`-Zeile
- [ ] Der Skill enthaelt einen Worktree-Guard-Block und eine Lesestand-Pruefung (Grep auf beide Sektions-Titel)
- [ ] `wc -l skills/dtb-workflow-checkpoint/SKILL.md` ≤ 470 — Schritt 1.5 fasst die Datei an, das Budget gilt schon hier

#### Manual
- [ ] Die Sichtungs-Regel ist beim Lesen eindeutig: ein fremder Leser kann sagen, welche Eintraege ein Lauf anfasst und welche nicht

---

## Phase 2: Schreiber umstellen

### Ziel

Die maschinellen Funde landen im Becken statt in der Haupt-INBOX, ohne dass dabei Nummern
kollidieren oder die Verlustpruefung dieselben Funde erneut meldet. Nach dieser Phase ist die
Trennung wirksam.

### Schritte

#### Schritt 2.1: Referenz-Kopplung entscheiden und umbauen
- **Zweck:** Der Checkpoint leiht sich heute die Schreibmechanik von `dtb:idea` und prueft auf deren Sektions-Titel. Nach dem Zielwechsel zeigt die Leihe ins Leere — das muss ENTSCHIEDEN werden, bevor der Zielwechsel erfolgt
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Z. 313, 364), `skills/dtb-idea/SKILL.md` (Schritt 2) oder `skills/dtb-idea-triage/SKILL.md`
- **Input:** Offener Punkt aus `spec.md`; Vorbedingung: repo-weiter Grep nach beiden Sektions-Titeln (L3 — nicht nur Frontmatter-Referenzen betrachten)
- **Output:** Entscheidung in der Tabelle „Technische Entscheidungen" eingetragen und umgesetzt; der
  Struktur-Check des Checkpoints greppt auf einen Titel, der existiert. **Ablageort des Ergebnisses:**
  Zeile in „Technische Entscheidungen" dieses Plans (L20)

#### Schritt 2.2: Zielwechsel Schritt 0 im Checkpoint
- **Zweck:** Die eigentliche Wirkstelle — Ideen-Funde gehen ins Becken
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Z. 346, 364-368)
- **Input:** Becken-Format aus 1.1
- **Output:** Sammelvorlage-Zeile und Meldezeile nennen das Becken statt `INBOX.md`; der
  Herkunfts-Marker `(via Checkpoint {YYYY-MM-DD})` entfaellt fuer Ideen-Funde, weil die Herkunft
  jetzt strukturell durch die Datei feststeht; Lektionen-Pfad bleibt unveraendert.
  Die Zweiteilung dringend/kann-warten entfaellt fuer Ideen — alle Ideen-Funde gehen ins Becken (loest #75 mit).
  **Fehlt `INBOX-BEFUNDE.md`, legt der Checkpoint sie mit Header an** — dieselbe Zusage wie in 1.2,
  weil `dtb:project-init` Bestandsprojekte nicht erreicht (Seed-Skew, INBOX #22) und der Checkpoint
  nach der Verteilung sofort in allen Projekten laeuft

#### Schritt 2.3: Nummernvergabe ueber beide Dateien
- **Zweck:** Der gemeinsame Nummernkreis darf keine Nummer zweimal vergeben
- **Dateien:** `skills/dtb-idea/SKILL.md` (Schritt 2), `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Randfall aus `spec.md`
- **Output:** Beide Schreiber bestimmen die naechste Nummer als Maximum ueber `INBOX.md` UND
  `INBOX-BEFUNDE.md`; fehlt eine der Dateien, zaehlt nur die vorhandene (fail-open).
  Der Zaehl-Ausdruck wird gegen eine Stichprobe der getroffenen Zeilen geprueft, nicht nur gegen die Zahl (L17)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Verlustpruefung liest beide Dateien
- **Zweck:** Ohne diesen Schritt meldet die Verlustpruefung jeden ins Becken verschobenen Fund erneut als „nicht erfasst" — und der Checkpoint schreibt ihn ein zweites Mal
- **Dateien:** `skills/dtb-no-loss-check/SKILL.md` (Z. 30, 128, 146, 235, 243, 284, 388)
- **Input:** Abgleich-Regel Z. 128 („Idee-Spalte jeder Zeile, unabhaengig vom Status")
- **Output:** Die Abgleich-Quelle umfasst beide Dateien; die Zielangabe in den Befehls-Vorschlaegen
  bleibt `dtb:idea` (der Mensch erfasst weiter in die Haupt-INBOX), nur der Abgleich waechst

#### Schritt 2.5: Handoff-Zeile, Config-Block und Zeilenbudget
- **Zweck:** Die Erinnerung, ohne die das Becken ein Friedhof wird — und die Kompensation, ohne die der Checkpoint sein Budget reisst
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`, `workflow.config.yaml`
- **Input:** Schwellwert-Entscheidung aus „Technische Entscheidungen"
- **Output:** Der Checkpoint zaehlt die ungesichteten Becken-Eintraege und haengt ab Schwelle GENAU
  EINE Zeile an den Handoff-Block; Config-Block `idea_triage` mit `becken_schwelle` und
  `altbestand_pro_lauf`; jede neue Zeile im Checkpoint durch Kuerzung an anderer Stelle kompensiert

### Deliverables
- [ ] Checkpoint schreibt Ideen-Funde ins Becken
- [ ] Nummernvergabe kollisionsfrei
- [ ] Verlustpruefung meldet Becken-Eintraege nicht erneut
- [ ] Config-Block dokumentiert

### Checkpoint-Kriterien

#### Automated
- [ ] `wc -l skills/dtb-workflow-checkpoint/SKILL.md` ≤ 470
- [ ] Die Schreib-Zielzeile in Schritt 0 des Checkpoints nennt `INBOX-BEFUNDE.md` (Grep auf die Zielzeile, nicht auf die Datei — L8: die Wirkstelle ist die Zeile, `INBOX.md` kommt anderswo legitim weiter vor)
- [ ] Der Struktur-Check-Grep des Checkpoints zeigt auf einen Sektions-Titel, der in der referenzierten Datei zeilenverankert existiert (`grep -x -F`)
- [ ] `dtb:idea` Schritt 2 und der Checkpoint nennen beide Dateien bei der Nummernvergabe (Grep je Skill in der Nummern-Zeile)
- [ ] `skills/dtb-no-loss-check/SKILL.md` nennt `INBOX-BEFUNDE.md` in der Abgleich-Quellen-Zeile
- [ ] `workflow.config.yaml` enthaelt den Block `idea_triage` mit beiden Schluesseln
- [ ] Der Checkpoint enthaelt genau eine Stelle, die die Handoff-Zeile erzeugt (Grep-Trefferzahl = 1)
- [ ] Nach einem Checkpoint-Lauf in einem Verzeichnis ohne Becken existiert die Datei und enthaelt die geschriebene Zeile — der Schreibvorgang wird bezeugt, nicht der Vergleich (L35)

#### Manual
- [ ] Der Zielwechsel liest sich als eine Regel, nicht als zwei nebeneinanderstehende Wahrheiten — `INBOX.md` und Becken sind im Text klar auseinandergehalten

---

## Phase 3: Verteilung, Doku, Wirklaeufe

### Ziel

Der Mechanismus ist in Bestands- und Neuprojekten verfuegbar, dokumentiert und an echten Laeufen
belegt statt behauptet.

### Schritte

#### Schritt 3.1: Seed, Integritaets-Pruefung und Regel-Zeile
- **Zweck:** Neuprojekte bekommen das Becken; die Gesundheitspruefung kennt es; die Statusableitung sagt, dass es status-neutral ist
- **Dateien:** `skills/dtb-project-init/SKILL.md` (Z. 129), `skills/dtb-project-health/SKILL.md` (Z. 89), `dtb-project/project-rules/DERIVED_STATE_RULES.md`
- **Input:** Ordnerbaum, Integritaets-Sektion, §6-Muster der Fach-Fragen
- **Output:** `project-init` legt `INBOX-BEFUNDE.md` an und nennt sie im Ordnerbaum; `project-health`
  prueft Spaltenzahl und Sichtung-Werte des Beckens; `DERIVED_STATE_RULES.md` bekommt die Zeile, dass
  ein Becken-Eintrag status-neutral ist und NICHT als Idee zaehlt

#### Schritt 3.2: Doku nachziehen
- **Zweck:** Ein Kit-Feature, das in keiner der beiden CLAUDE.md steht, existiert fuer den naechsten Leser nicht
- **Dateien:** `CLAUDE.md`, `skills/CLAUDE.md`
- **Input:** Skill-Kategorien-Liste, Output-Locations-Liste
- **Output:** `dtb:idea-triage` unter „Idea management" eingetragen; `INBOX-BEFUNDE.md` und
  `archive/INBOX-BEFUNDE-verworfen.md` unter Output-Locations; die Zwei-Becken-Regel als Konvention
  in `skills/CLAUDE.md` (wer schreibt wohin)

#### Schritt 3.3: Wirklaeufe gegen die Erfolgskriterien
- **Zweck:** Die elf Kriterien der Spec sind Behauptungen, bis sie gelaufen sind. L15: der eigene neue Text muss ausdruecklich gegen die Fehlerklasse geprueft werden, die er beseitigt
- **Dateien:** `dtb-project/project-workflows/features/ideen-becken/plan.md` (Protokoll-Abschnitt), Session-Log
- **Input:** Success Criteria aus `spec.md`
- **Output:** Je Kriterium ein protokollierter Lauf mit Ergebnis. **Ablageort:** Abschnitt
  `## Wirklauf-Protokoll` in diesem Plan (L20 — ein Schritt ohne Datei-Deliverable braucht einen
  benannten Ablageort). Mindestens abzudecken: Fund landet im Becken · `idea-review` unveraendert ·
  zweiter Verlustpruefungs-Lauf meldet nicht erneut · Nummer nicht doppelt · befoerdern/verwerfen/
  liegenlassen je einmal · Abbruch nach Entscheidung 2 · Zwangsentscheidung im Folgelauf ·
  Handoff-Zeile ab Schwelle · fehlendes Becken wird angelegt

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Verteilung
- **Zweck:** Die installierte Kopie unter `~/.claude/` ist das, was tatsaechlich laeuft
- **Dateien:** `~/.claude/dtb-lock.json`, installierte Skill-Kopien
- **Input:** Klasse-A-Muster von `dtb:kit-sync`
- **Output:** Vor dem Sync `git status -sb` geprueft — steht der Branch auf `ahead`, erst pushen (L39);
  danach Lock mit 48 Eintraegen, Sync-Meldung an einen unabhaengigen Zeugen gebunden (L35: mtime der
  Zielkopie nach dem Kopieren, nicht der Vergleich allein)

### Deliverables
- [ ] Seed, Integritaets-Pruefung, Regel-Zeile
- [ ] Beide CLAUDE.md aktualisiert
- [ ] `## Wirklauf-Protokoll` mit einem Eintrag je Erfolgskriterium
- [ ] Lock @ 48, Sync belegt

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -F 'INBOX-BEFUNDE.md' skills/dtb-project-init/SKILL.md` trifft im Ordnerbaum-Block
- [ ] `grep -F 'INBOX-BEFUNDE' skills/dtb-project-health/SKILL.md` trifft in der Integritaets-Sektion
- [ ] `grep -F 'INBOX-BEFUNDE' dtb-project/project-rules/DERIVED_STATE_RULES.md` trifft
- [ ] `grep -F 'dtb:idea-triage' CLAUDE.md` und `grep -F 'INBOX-BEFUNDE' CLAUDE.md` treffen beide
- [ ] Der Abschnitt `## Wirklauf-Protokoll` in `plan.md` existiert und hat mindestens so viele Ergebniszeilen wie die Spec Erfolgskriterien hat
- [ ] `dtb-lock.json` enthaelt 48 Eintraege und einen Eintrag fuer `skills/dtb-idea-triage/SKILL.md`

#### Manual
- [ ] Ein Lauf im Alltag fuehlt sich richtig portioniert an: die Sichtungsmenge ist erledigbar, die Bilanz sagt etwas Nuetzliches

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Referenz-Kopplung Checkpoint → Schreibmechanik | A: `dtb:idea` bekommt einen zieloffenen Schreib-Abschnitt · B: `dtb:idea-triage` bekommt eine eigene Schreibmechanik als Referenzquelle | **B** (2026-09-08) | `dtb:idea` schreibt tatsaechlich immer nach `INBOX.md` — sein Sektions-Titel ist dort korrekt und bleibt unangetastet. B kostet 2 Dateien statt 4 Fundstellen und macht die Zustaendigkeit sauber: wer die Datei besitzt, beschreibt das Schreiben. Umgesetzt: neuer Abschnitt `## Schreibmechanik INBOX-BEFUNDE.md` in `dtb:idea-triage`, Anker-Tabelle und Schreib-Referenz im Checkpoint umgehaengt, Quellen-Aufloesung um `idea-triage` erweitert |
| Standardwert `becken_schwelle` | 5 · 8 · 10 · hoch starten und messen | **10, gesetzt 2026-09-08; nach 4 Sessions nachjustieren** | Der Wert ist nicht belegt — die Zahl der Funde pro Session wurde nie gemessen. Ein zu kleiner Wert macht die Handoff-Zeile zur Tapete. Also bewusst hoch anfangen und die tatsaechliche Rate abwarten, statt jetzt zu raten |
| Dateiname des Beckens | `INBOX-BEFUNDE.md` · `BEFUNDE.md` | `INBOX-BEFUNDE.md` | Das Praefix bindet die Datei sichtbar an die INBOX und sortiert daneben |
| Werte der Sichtung-Spalte | leer · `L1 YYYY-MM-DD` · `Altbestand` | uebernommen | Einfachste greppbare Form; `L1` traegt das Datum, damit der Folgelauf die Zwangsentscheidung begruenden kann |
| Zweiteilung dringend/kann-warten fuer Ideen | beibehalten · aufloesen | aufloesen | Das Becken IST der Ort fuer „kann warten" — die Zweiteilung erzeugte die Wiederholung aus #75 |

---

## Wirklauf-Protokoll

> Ablageort fuer Schritt 3.3 (L20). Eine Zeile je Erfolgskriterium aus `spec.md`.
> Leer bis Phase 3.

| Datum | Kriterium | Lauf | Ergebnis |
|-------|-----------|------|----------|

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Becken-Format festlegen und Datei anlegen — `03b1e6d`
- [x] 1.2 Skill-Geruest mit Guards — `03b1e6d`
- [x] 1.3 Sichtungs-Regel und Dreifach-Entscheidung — `03b1e6d`
- [x] 1.4 Befoerderung, Archiv-Ausgang, Alterungshinweis — `03b1e6d`
- [x] 1.5 Abschluss-Bilanz und Pipeline-Kanten beidseitig — `03b1e6d`
- [x] 2.1 Referenz-Kopplung entscheiden und umbauen
- [x] 2.2 Zielwechsel Schritt 0 im Checkpoint
- [x] 2.3 Nummernvergabe ueber beide Dateien
- [x] 2.4 Verlustpruefung liest beide Dateien
- [x] 2.5 Handoff-Zeile, Config-Block und Zeilenbudget
- [ ] 3.1 Seed, Integritaets-Pruefung und Regel-Zeile
- [ ] 3.2 Doku nachziehen
- [ ] 3.3 Wirklaeufe gegen die Erfolgskriterien
- [ ] 3.4 Verteilung

---

## Umsetzung

Umsetzung mit `/dtb:implement Ideen-Becken` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/ideen-becken/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
