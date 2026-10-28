# Implementierungsplan: Lektionen kuratieren

**Erstellt:** 2026-10-27
**Feature-Spec:** `features/lektionen-kuratieren/spec.md`
**Geschaetzte Dauer:** ~6–7 h
**Status:** Reviewed (plan-review 2026-10-27: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Geruest, Voranalyse und Probe in Zielform | ~2 h | Geplant |
| Phase 2 | Entscheiden und Schreiben (Sammelliste, Einzelfaelle, Archiv, Entnahme) | ~2 h | Geplant |
| Phase 3 | Integration (`dtb:lesson`, Dashboard, Config, Doku) | ~1,5 h | Geplant |
| Phase 4 | Simulationen und Text-Selbstpruefung | ~1 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` `## Betroffene Module` (Pfade verifiziert 2026-10-27; zwei Neubau-Ziele, L5) plus Research in impl-plan.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-lesson-curate/SKILL.md` | Neubau |
| `archive/lessons-ausgemustert.md` | Neubau (unter `{config.paths.workflows}/archive/`); nicht ignoriert → versioniert |
| `skills/dtb-lesson/SKILL.md` | Frontmatter `allowed-tools: Read, Write, Edit, Grep` — **kein Bash** (fuer KB-Messung noetig, L75). Schritt 4: Kopftext-Template Z. 185–189 („~150 Zeilen"), Nummernvergabe Z. 200 („Naechste laufende Nummer"), Groessen-Warnung Z. 203–208 (Zeilen), Hebe-Hinweis Z. 210ff. Kopplungs-Hinweis Z. 172: Checkpoint und idea-triage greppen auf `## Schritt 4: Append-only speichern` |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 0 schreibt Lektionen per Referenz auf die **ganze** Sektion `## Schritt 4: Append-only speichern` (Z. 509, 561) → Groessen-Warnung und Nummernvergabe werden mit vererbt; kein Eingriff noetig |
| `skills/dtb-idea-triage/SKILL.md` | Vorbild. 7f schreibt per Referenz auf `dtb:lesson` Schritt 4 (Z. 703) → erbt ebenfalls. Bausteine: Worktree-Guard (Z. 36ff), Weiche inline/Agenten + Explore-Rueckfall (3a), Auftrag mit Ergebniszeile (3b), Nummern-/Spalten-Gate (3c), Sammelliste mit Knopf (5), Archiv-Kopf ohne eigene Beleg-Spalte (7b) |
| `dtb-project/project-rules/lessons.md` | 96 Zeilen, 56 290 Bytes, 87 Lektionen; L22–L34 fehlen; Reihenfolge nicht monoton (8 vor 7, 17→12). Kopf Z. 3–6: Leser-Liste veraltet („code-review", `implement` fehlt), „~150 Zeilen" |
| `skills/dtb-project-dashboard/SKILL.md` | Z. 88 Kennzahl-Zusatz `{Zeilen der Datei}/150 Zeilen`; Z. 170–172 Lektionen-Block mit 150-Zeilen-Schwelle und Verweis auf `/dtb:lesson`. Paralleler Branch `dashboard-projektname-hintergrund` aendert dieselbe Datei an anderer Stelle |
| `skills/dtb-project-init/SKILL.md` | Config-Template Z. ~95–115 traegt `worker:`, `parallel:`, `status:`, `dashboard:` — nicht `idea_triage:` |
| `workflow.config.yaml` | Bloecke `idea_triage:`, `worker:`, `parallel:`, `status:`, `dashboard:`; kein `lessons:` |
| `skills/CLAUDE.md` | Voll-Guard-Tabelle Z. 469; Orchestrator-Liste Z. 443; Rueckfragen-Defaults-Zuordnung (letzte Zeile G); Worktree-Guard-Vorlage (byte-identisch zu uebernehmen, Referenz-Instanz `dtb:idea`) |
| `CLAUDE.md`, `README.md` | Skill-Liste „Knowledge management", Output Locations |
| Prior-Leser (impl-plan, debug-plan, plan-review, impl-review, implement, feature-fast), Duplikat-Pruefer (no-loss-check, idea-triage 4c) | Keine Aenderung (Spec „Nicht enthalten") |

**Alle Fundstellen der alten Schwelle** (L47, Grep `150 Zeilen\|~150\|/150` ohne Changelog/Archiv): `lessons.md:6`, `dtb-lesson:189`, `:204`, `:206`, `dtb-project-dashboard:88`, `:170`, `:171`, `:172`. Nicht betroffen: `dtb-project-init:235` und `WORKLOG.md:84` (betreffen die CLAUDE.md-Groesse).

---

## Phase 1: Skill-Geruest, Voranalyse und Probe in Zielform

### Ziel
Der Skill existiert bis einschliesslich der Voranalyse; eine read-only Probe am echten Bestand zeigt Uebersicht und Sammelliste in Zielform, bevor die Schreib-Regeln ausgearbeitet werden (L64).

### Schritte

#### Schritt 1.1: Geruest, Guard, Config, Laden
- **Zweck:** Rahmen, der nur im Haupt-Checkout schreibt und den Bestand robust laedt
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md` (neu)
- **Input:** Spec; Frontmatter-Konvention `skills/CLAUDE.md`; Guard-Referenz-Instanz `dtb:idea`
- **Output:**
  - Frontmatter: `name: dtb:lesson-curate`, `disable-model-invocation: true`, `allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion`, Pipeline `stage: development`, `after: [dtb:lesson]`, `next: null`, `consumes`/`produces` vollstaendig (L44: `project-rules/lessons.md`, `archive/lessons-ausgemustert.md`, `workflow.config.yaml`, `skills/CLAUDE.md`, `project-rules/*.md`, `features/*/{spec,plan}.md` nur consumes)
  - `## Worktree-Guard` byte-identisch (Bash-Block + ⛔-Fence), ohne Echo-Anteil
  - Schritt 0 Config: Block `lessons:` mit `schwelle_kb` (Default 40) und `einzeln_pro_lauf` (Default 5), still auf Default bei Fehlen
  - Schritt 1 Laden: Datenzeilen = Zeilen `^\| [0-9]+ \|` unter der Trennzeile, nach Nummer gefuehrt (nie Position); fehlt/leer → Meldung + Ende; Zeilen ohne dieses Muster nie anfassen; Bestand in Lektionen, Zeilen, KB (KB = Bytes/1024, abgerundet) — Messung per `wc -c`, Ausfall → Hinweiszeile, kein Befund (L7); unter Schwelle → eine Stand-Zeile, Lauf geht weiter
  - **Selbstheilungs-Erkennung:** Nummern, die in `lessons.md` UND im Archiv stehen, vor jeder Analyse melden; die Entnahme-Mechanik folgt in 2.3

#### Schritt 1.2: Voranalyse (Weiche, Auftrag, Ergebnis-Gate)
- **Zweck:** Je Lektion ein belegtes Urteil, read-only, ausfallsicher
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md`
- **Input:** idea-triage 3a–3c als Vorbild (nicht per Referenz — becken-spezifisch, Spec)
- **Output:**
  - Weiche: unter 5 Lektionen inline, sonst Portionen zu hoechstens 15 (Lektionen sind lang), je Portion ein `Explore`-Agent, parallel; Rueckfall `general-purpose` mit ⚠-Zeile
  - Auftrag je Portion: Portion im vollen Wortlaut + **alle** Lektionen als `L{N} {Rule, ~100 Zeichen}` (macht `doppelt` ueber Portionsgrenzen sichtbar); Pruefraeume: Skill-/Code-Bestand, Hebe-Ziele (`skills/CLAUDE.md` falls vorhanden; `{rules}/*.md` ohne `lessons.md`, `DERIVED_STATE_RULES.md`)
  - Urteile genau eines je Lektion: `behalten` / `ueberholt` / `doppelt zu L{M}` / `gehoben`; Ersetzungsprobe als Laufzeit-Kurzform fuer `doppelt` UND `gehoben` (gleicher Gegenstand + gleiche Aussage, Richtung: die bleibende Lektion bzw. die Fundstelle traegt die Aussage vollstaendig — nur derselbe Gegenstand reicht nicht); Abwesenheits-Beleg nur mit Nachfolge-Stelle → `hoch`, sonst hoechstens `mittel`
  - Die KB-Definition aus 1.1 (genau eine Stelle im Skill) traegt einen Kopplungs-Hinweis auf die beiden Spiegel (`dtb:lesson` Schritt 4, `dtb:project-dashboard`)
  - Ergebniszeile: `L{N} | {Urteil} | {Grund, 1 Satz} | {Beleg datei:zeile} | {Sicherheit}`; Pipes escapen
  - Ergebnis-Gate: Nummern-Mengenprobe je Portion (genau die Portions-Nummern, je einmal), Spaltenzahl, bekanntes Urteil; Ausfall → Lektionen der Portion `nicht geprueft → behalten`, ⚠-Zeile; alle Portionen ausgefallen → Abbruch ohne Schreiben

#### Schritt 1.3: Probe in Zielform
- **Zweck:** Zielform am echten Bestand abnehmen lassen, bevor Phase 2 die Regeln ausarbeitet (L64)
- **Dateien:** `features/lektionen-kuratieren/probe.md` (neu, status-neutral — Ablageort L20)
- **Input:** Repo-Fassung des Skills (L74), Kit-Bestand `lessons.md`
- **Output:** Voranalyse read-only am **vollen Bestand** ausgefuehrt (Entscheidung 2026-10-27 — zugleich Vorschau auf den ersten echten Lauf); Uebersicht (Bestand, Vorschlaege je Grund, erwartete KB-Einsparung) und eine Muster-Sammelliste plus Einzelfall-Liste in Zielform, ohne zu schreiben; Rohzeilen der Agenten als Anhang

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `skills/dtb-lesson-curate/SKILL.md` mit Guard, Config, Laden, Voranalyse
- [ ] `features/lektionen-kuratieren/probe.md` mit Uebersicht und Muster-Liste

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f skills/dtb-lesson-curate/SKILL.md` und Frontmatter-Zeile `name: dtb:lesson-curate` vorhanden
- [ ] Guard byte-identisch: Bash-Block aus `skills/dtb-lesson-curate/SKILL.md` und `skills/dtb-idea/SKILL.md` per `diff` (zwischen ```` ```bash ```` und ```` ``` ```` unter `## Worktree-Guard`) ohne Unterschied
- [ ] `grep -c "disable-model-invocation: true" skills/dtb-lesson-curate/SKILL.md` = 1
- [ ] `probe.md` enthaelt je Urteilsart eine Zaehlzeile und die Summe der Zaehlzeilen = Anzahl Lektionen (Mengenprobe, L90)

#### Manual
- [ ] Mensch nimmt Uebersicht und Muster-Sammelliste in `probe.md` als Zielform ab (Spalten, Kuerzung, Lesbarkeit, Belegqualitaet)

---

## Phase 2: Entscheiden und Schreiben

### Ziel
Aus den Urteilen entstehen mechanisch Sammelliste und Einzelfaelle; jede bestaetigte Entscheidung wird sofort geschrieben — Ziel vor Quelle.

### Schritte

#### Schritt 2.1: Konsolidieren
- **Zweck:** Mechanische Einordnung ohne neue Bewertung
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md`
- **Input:** Ergebniszeilen aus 1.2, Feedback aus 1.3
- **Output:**
  - `niedrig` und `behalten` → behalten (nur Zahl)
  - **Ketten-Sperre:** die bleibende Lektion eines `doppelt`-Paares ist im Lauf fuer Ausmusterung gesperrt; ist sie selbst Kandidat → beide Einzelfall; Kreise (A↔B) → Einzelfall
  - Sammelliste = `hoch` + Beleg mit `datei:zeile`, `doppelt` nur ohne Sperre; sonst Einzelfall (`mittel`, Ketten/Kreise, ohne Beleg-Ort, `nicht geprueft` zaehlt nicht als Einzelfall — bleibt behalten)
  - Kappung der Einzelfaelle auf `einzeln_pro_lauf`, Rest als Zahl „naechster Lauf"
  - Hinweis je Zeile, wenn `L{N}` in offenen `features/*/{spec,plan}.md` referenziert ist (nicht blockierend)
  - Uebersicht vor der Vorlage + Mengenprobe: gezeigte Nummern = Eingangsmenge, Summe der Gruppen = Bestand — bei Abweichung keine Vorlage (L90)

#### Schritt 2.2: Sammelliste und Einzelfaelle
- **Zweck:** Der Mensch entscheidet jede Ausmusterung
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md`
- **Input:** Vorlage-Form aus 1.3; idea-triage Schritt 5/6 als Vorbild
- **Output:**
  - Sammelliste: je Zeile `L{N}`, Grund, Beleg (gekuerzt), Wirkung `→ Archiv`; Knopf `Alle uebernehmen (Vorschlag)` / `Nummern streichen` / `Einzeln durchgehen`; gestrichen = Einzelfall (zaehlt nicht gegen die Kappung), nie ausgemustert; jede andere Antwort → eine Rueckfrage, sonst Abbruch ohne Schreiben
  - Einzelfall: Lektion im Wortlaut, Urteil, Beleg; Knopf `Ausmustern ({Grund})` / `Behalten`; bei `doppelt` mit offener Richtung zusaetzlich `Die andere ausmustern`
  - Kein Liegenlassen-Zustand (Lektionen tragen keinen Sichtungsvermerk — behalten heisst: naechster Lauf prueft neu)

#### Schritt 2.3: Schreiben, Selbstheilung, Bilanz
- **Zweck:** Nichts geht verloren, nie eine Zeile doppelt
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md`
- **Input:** bestaetigte Entscheidungen
- **Output:**
  - Archiv `{config.paths.workflows}/archive/lessons-ausgemustert.md`: Selbstanlage mit Kopf (append-only, „Suchraum, wenn ein Thema wiederkommt"); Spalten `| Ausgemustert am | # | Datum | Context | Problem | Rule | Applies-to | Grund |` — Lektions-Spalten unveraendert (Wiederherstellung = Zeile zurueckkopieren), `Grund` = `{Urteil}: {Grund} — Beleg: {Beleg}`
  - Je Entscheidung sofort: (1) Archivzeile anhaengen (Edit am Tabellenende), (2) zuruecklesen, (3) Entnahme aus `lessons.md` per `Edit` mit der exakten Zeile als Anker — Read vor Edit ausdruecklich (L99), nie `Write`. Ziel vor Quelle (L43)
  - Selbstheilung aus 1.1: Nummer in beiden → nur Entnahme nachholen, kein zweiter Archiveintrag, Meldezeile
  - Schreibfehler mitten drin → melden was geschrieben ist, Rest offen lassen, nie zurueckrollen
  - Bilanz: ausgemustert je Grund, behalten, nicht geprueft, gekappt; neuer Umfang Zeilen/KB vs. Schwelle; Hebe-Hinweis fuer Lektionen mit `Applies-to: alle` (nur Hinweis)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Skill vollstaendig von Laden bis Bilanz

### Checkpoint-Kriterien

#### Automated
- [ ] Sektion „Konsolidieren" enthaelt die Ketten-Sperre (Grep `gesperrt` innerhalb der Sektion ≥ 1)
- [ ] Archiv-Kopf mit 8 Spalten im Skill (Grep `| Ausgemustert am | # | Datum | Context | Problem | Rule | Applies-to | Grund |` = 1)
- [ ] Schreibreihenfolge im Schreib-Abschnitt: Zeile mit „Archiv" steht vor der Zeile mit „Entnahme" (Zeilennummern-Vergleich per `grep -n`, auf den Abschnitt geankert, L2)
- [ ] Entnahme-Anweisung im Schreib-Abschnitt nennt `per \`Edit\`` UND `exakte Zeile als Anker` (positiver Anker statt Negativ-Grep — der Abschnitt muss „nie `Write`" selbst nennen, L8)

---

## Phase 3: Integration

### Ziel
`dtb:lesson`, Dashboard, Config und Doku ziehen mit; die alte Zeilen-Schwelle ist an allen Fundstellen ersetzt (L47).

### Schritte

#### Schritt 3.1: `dtb:lesson` — Nummer, Warnung, Kopftext
- **Zweck:** Keine Nummer doppelt vergeben, Warnung misst das Richtige und an genau einer Stelle
- **Dateien:** `skills/dtb-lesson/SKILL.md`
- **Input:** Ist-Analyse Z. 185–212
- **Output:**
  - Nummernvergabe: Maximum ueber `lessons.md` UND `archive/lessons-ausgemustert.md` (fehlt das Archiv → nur `lessons.md`) plus eins
  - Groessen-Warnung: KB (Bytes/1024, abgerundet) gegen `lessons.schwelle_kb` (Default 40), Verweis `/dtb:lesson-curate`; Messung per `wc -c`, Ausfall → keine Warnung, eine Hinweiszeile; Kopplungs-Hinweis auf die Spiegel (`dtb:lesson-curate`, `dtb:project-dashboard`)
  - Kopftext-Template: append-only gilt fuers Schreiben, Entnahme nur ueber `/dtb:lesson-curate`; Soft-Limit in KB; Leser-Liste aktuell (impl-plan, debug-plan, plan-review, impl-review, implement)
  - `allowed-tools` um `Bash` erweitern (L75); `consumes` um `archive/lessons-ausgemustert.md`, Config (L44)
  - Kopplungs-Hinweis Z. 172 bleibt gueltig (Anker unveraendert); Checkpoint und idea-triage erben per Referenz

#### Schritt 3.2: Live-Datei, Dashboard, Config
- **Zweck:** Anzeige und Daten folgen der neuen Schwelle
- **Dateien:** `dtb-project/project-rules/lessons.md` (nur Kopf Z. 3–6), `skills/dtb-project-dashboard/SKILL.md` (Z. 88, 170–172), `workflow.config.yaml`, `skills/dtb-project-init/SKILL.md` (Config-Template)
- **Input:** 3.1
- **Output:**
  - `lessons.md`-Kopf wortgleich zum neuen Template-Kopf (ausser Datei-Existenz); keine Datenzeile beruehrt
  - Dashboard: Kennzahl-Zusatz `{KB}/{schwelle_kb} KB`; Lektionen-Block: Fuellstand in KB, „Kuratierung faellig … siehe /dtb:lesson-curate" ab Schwelle; Config-Default 40 in der Fallback-Liste Z. 37; KB-Definition mit Kopplungs-Hinweis auf die Spiegel (`dtb:lesson`, `dtb:lesson-curate`)
  - Config-Block `lessons:` mit beiden Schluesseln und Kommentaren — im Kit-`workflow.config.yaml` und im `project-init`-Template

#### Schritt 3.3: Doku und Gegenprobe
- **Zweck:** Konventionen und Uebersichten kennen den Skill; keine Altstelle bleibt
- **Dateien:** `skills/CLAUDE.md`, `CLAUDE.md`, `README.md`
- **Input:** 3.1, 3.2
- **Output:**
  - `skills/CLAUDE.md`: `lesson-curate` in die Voll-Guard-Zeile (Z. 469); Orchestrator-Liste „Lektionen" um Kuratierung ergaenzen (Z. 443); Rueckfragen-Defaults Zeile **H** (`lesson-curate` Sammelliste + Einzelfaelle, Form wie F)
  - `CLAUDE.md`: Knowledge management um `lesson-curate`; Output Location `archive/lessons-ausgemustert.md`; `lessons.md`-Eintrag „append-only" um die Entnahme-Regel ergaenzen
  - `README.md`: Skill-Liste
  - Gegenprobe (L3, L16): repo-weiter Grep auf `150 Zeilen\|~150\|/150`, `append-only` im Lektionen-Kontext, `lesson-curate` und auf Leser von `archive/` (Grep `archive/` ueber `skills/`); Prueffrage ausformuliert: „Traegt die Aussage nach der Aenderung noch?"; Ergebnis in `probe.md` (Abschnitt Gegenprobe)
  - **Leser von `archive/` — Entscheidung 2026-10-27:** `dtb:migrate-change-folders` wertet jede lose `.md` ausser `ARCHIVE_LOG.md` als Altlayout (trifft heute schon `INBOX-BEFUNDE-verworfen.md`). NICHT in diesem Change reparieren — die Gegenprobe haelt fest, was migrate bei beiden Dateien meldet; die Korrektur geht als eigene Idee in den Hand-off

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `dtb:lesson`, Dashboard, Config, `lessons.md`-Kopf, Doku nachgezogen

### Checkpoint-Kriterien

#### Automated
- [ ] Alte Schwelle an den 8 Fundstellen weg: `grep -n "150 Zeilen\|~150\|/150" dtb-project/project-rules/lessons.md skills/dtb-lesson/SKILL.md skills/dtb-project-dashboard/SKILL.md` = 0 Treffer (Wirkstellen-Dateien, L8)
- [ ] `grep -c "lesson-curate" skills/dtb-lesson/SKILL.md` ≥ 2 (Warnung + Kopftext-Template)
- [ ] `grep -c "lessons-ausgemustert" skills/dtb-lesson/SKILL.md` ≥ 1 (Nummernvergabe)
- [ ] `allowed-tools` von `dtb:lesson` enthaelt `Bash`
- [ ] `grep -c "schwelle_kb" workflow.config.yaml skills/dtb-project-init/SKILL.md skills/dtb-project-dashboard/SKILL.md skills/dtb-lesson/SKILL.md` je ≥ 1
- [ ] `lesson-curate` in `skills/CLAUDE.md` (Voll-Guard-Zeile), `CLAUDE.md`, `README.md` je ≥ 1
- [ ] Datenzeilen von `lessons.md` unveraendert: `git diff -U0 -- dtb-project/project-rules/lessons.md | grep -c "^[-+]| [0-9]"` = 0

---

## Phase 4: Simulationen und Text-Selbstpruefung

### Ziel
Die Fehlerpfade der Spec sind an einer Wegwerf-Kopie belegt, der Regeltext ist in sich widerspruchsfrei (L14).

### Schritte

#### Schritt 4.1: Simulationen in Wegwerf-Kopie
- **Zweck:** Success Criteria zu Selbstheilung, Agent-Ausfall und Nummernvergabe belegen, ohne den echten Bestand zu beruehren
- **Dateien:** keine im Repo; Ablage `features/lektionen-kuratieren/probe.md` (Abschnitt Simulationen, L20)
- **Input:** Repo-Fassung der Skills (L74); Scratchpad-Ordner ohne Git (Guard → `DURCHLASS-NOGIT`) mit Kopie von `lessons.md`, Config, `skills/CLAUDE.md`
- **Output:** drei Faelle mit Ergebnis:
  1. Abbruch zwischen Archiv und Entnahme (Lektion vorab in beide Dateien gelegt) → naechster Lauf meldet und heilt ohne Doppel-Archiv
  2. Agent-Ausfall: ein **praeparierter Ergebnisblock** (je eine Variante: fremde Nummer, fehlende Zeile, falsche Spaltenzahl) wird durch das Gate aus 1.2 geschickt — Block und Gate-Ausgabe woertlich in `probe.md` → `nicht geprueft → behalten` in der Bilanz, kein Vorschlag (belegt statt erzaehlt)
  3. Hoechste Nummer ausgemustert → `dtb:lesson`-Nummernvergabe liefert eine nie benutzte Nummer
  Plus ein Durchlauf Sammelliste → bestaetigt → Archiv + Entnahme an der Kopie (Spaltenzahl der Archivzeile = 8)

#### Schritt 4.2: Text-Selbstpruefung und Spiegel
- **Zweck:** Regeln untereinander widerspruchsfrei; Kopplungen verifiziert
- **Dateien:** `skills/dtb-lesson-curate/SKILL.md` (nur Korrekturen); Ablage `probe.md` (Abschnitt Selbstpruefung)
- **Input:** fertiger Skill, Spec
- **Output:** Gegenlesen auf Praezedenz-Konflikte (Sicherheit vs. Ketten-Sperre vs. Kappung vs. Streichen); Abgleich jeder Spec-Zeile „Enthalten" gegen eine Skill-Stelle; KB-Definition an allen drei Nutzern wortgleich (Grep, Zielzahl 3: `dtb:lesson`, `dtb:lesson-curate`, `dtb:project-dashboard`)

### Deliverables
- [ ] `probe.md` mit Simulationen und Selbstpruefung

### Checkpoint-Kriterien

#### Automated
- [ ] `probe.md` enthaelt die Abschnitte `## Simulationen` und `## Selbstpruefung`, je Simulation eine Ergebniszeile `✅`/`❌` (3 + 1 Zeilen), keine `❌`
- [ ] KB-Definition: Grep auf `Bytes/1024` ueber die drei Skills = 3

#### Manual
- [ ] Mensch liest die Simulations-Ergebnisse gegen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Erbt die KB-Warnung in Checkpoint/idea-triage? | A eigene Hinweise · B Referenz | B | Beide referenzieren die ganze Sektion `## Schritt 4: Append-only speichern`, die Warnung ist eine Unter-Sektion davon — kein Spiegel noetig (Spec-Offener-Punkt 1 geklaert) |
| Archiv-Spalten | A wie Verworfen-Archiv (Text + Begruendung) · B Lektions-Spalten + Grund | B | Wiederherstellung = Zeile zurueckkopieren; Beleg in `Grund` (Verworfen-Muster: keine eigene Beleg-Spalte) |
| `lessons:` ins `project-init`-Template | A ja · B nur Default | A | Template traegt bereits `worker:`/`status:`/`dashboard:`; `dtb:lesson` laeuft in jedem Projekt. Bestandsprojekte fallen still auf Default |
| KB-Messung in `dtb:lesson` | A `wc -c` (Bash nachruesten) · B Zeichen per Read schaetzen | A | Messbar, gleich in allen drei Nutzern; `allowed-tools` nachziehen (L75) |
| Portionsgroesse | 25 (idea-triage) · 15 | 15 | Lektionen ~650 Bytes je Zeile, Agent prueft je Lektion gegen Skills/Regeldateien |
| Lauf-Wirkort echter Lauf | A im Worktree · B im Haupt-Checkout nach Merge | B | Voll-Guard; der erste echte Lauf (Spec-Kriterium) ist Abnahme-Schritt des Orchestrators und steht im Hand-off, nicht in `## Progress` (L21: ortsunabhaengiger Teil = Probe 1.3 + Simulationen 4.1) |
| Probe-/Pruef-Ablage | Session-Log · `probe.md` im Change-Ordner | `probe.md` | Worktree schreibt keine Changelog-Dateien; status-neutral, ueberlebt Session-Wechsel (L20) |
| Default `schwelle_kb` | 30 · 40 · 50 | 40 | ~60 Lektionen heutiger Laenge; nach erstem echten Lauf gegenpruefen (Spec-Offener-Punkt 4) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Geruest, Guard, Config, Laden — `0ae8cf3`
- [x] 1.2 Voranalyse — `0ae8cf3`
- [x] 1.3 Probe in Zielform — `0ae8cf3`
- [x] 2.1 Konsolidieren — `84aafcc`
- [x] 2.2 Sammelliste und Einzelfaelle — `84aafcc`
- [x] 2.3 Schreiben, Selbstheilung, Bilanz — `84aafcc`
- [x] 3.1 dtb:lesson nachziehen
- [x] 3.2 Live-Datei, Dashboard, Config
- [x] 3.3 Doku und Gegenprobe
- [ ] 4.1 Simulationen
- [ ] 4.2 Text-Selbstpruefung

---

## Nach dem Merge (Orchestrator)

> Ausserhalb von `## Progress` — der Skill hat einen Voll-Guard und schreibt nur im Haupt-Checkout.
> Diese Punkte gehoeren in den WORKTREE-HANDOFF-Block und sind Teil der Abnahme (Spec-Kriterium „Erster echter Lauf").

- [ ] `kit-sync` nach dem Merge (Klasse-A: neuer Skill + geaenderte Skills)
- [ ] Erster echter Lauf `/dtb:lesson-curate` im Haupt-Checkout am Kit-Bestand (Repo-Fassung, L74)
- [ ] Bilanz des Laufs im Session-Log festhalten (ausgemustert je Grund, neuer Umfang KB)
- [ ] Default `schwelle_kb: 40` am Ergebnis gegenpruefen (Spec-Offener-Punkt 4)

---

## Umsetzung

Umsetzung mit `/dtb:implement Lektionen kuratieren` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/lektionen-kuratieren/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

## Lektion-Kandidaten

- „Eine Groessen-Schwelle an der Kostenart messen, die sie begrenzen soll (Bytes fuer geladene Priors), nie an einer Ersatzgroesse wie Zeilen — bei Tabellen mit einer Zeile je Eintrag schlaegt eine Zeilen-Schwelle nie an" (vorgemerkt 2026-10-27)

---

**Erstellt mit:** `/dtb:impl-plan`
