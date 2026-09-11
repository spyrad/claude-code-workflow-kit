# Discovery: Ideen-Becken (Zwei-Becken-Modell fuer die INBOX)
<!-- resume: done -->

**Erstellt:** 2026-09-08
**Idee-Referenz:** Inbox #76 — "Zwei-Becken-Modell fuer die INBOX"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-idea-triage/SKILL.md` | NEU — der schreibende Triage-Lauf ueber das Becken |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Zielwechsel Schritt 0 (Z. 346/364-368), Handoff-Zeile ab Schwelle, Struktur-Check-Tabelle (Z. 313) |
| `skills/dtb-no-loss-check/SKILL.md` | Abgleich-Quelle (Z. 128) muss beide Dateien lesen, sonst Doppelmeldung |
| `skills/dtb-project-init/SKILL.md` | Seed `INBOX-BEFUNDE.md` + Ordnerbaum (Z. 129) |
| `skills/dtb-project-health/SKILL.md` | INBOX-Integritaet (Z. 89) um Becken erweitern |
| `CLAUDE.md`, `skills/CLAUDE.md` | Doku: Output-Locations, Skill-Kategorien, Konventionen |

**Unveraendert** (lesen weiter nur `INBOX.md`): `dtb:idea`, `dtb:idea-review`, `dtb:worker` (Z. 62),
`dtb:workflow-next`, `dtb:archive`, `dtb:feature-*`. `kit-sync` und `pipeline-graph` ziehen automatisch nach.

---

## Anforderungen

### Scope

**Enthalten:**
- `INBOX-BEFUNDE.md` (neue Datei, gleicher Ordner) als maschinelles Becken
- Neuer Skill `dtb:idea-triage` (schreibend: befoerdern / verwerfen / liegenlassen)
- `dtb:workflow-checkpoint`: Ideen-Funde aus Schritt 0 gehen ins Becken; Handoff-Zeile ab Schwelle
- `dtb:no-loss-check`: Abgleich ueber beide Dateien
- `dtb:project-init` (Seed), `dtb:project-health` (Integritaet), Config-Block `idea_triage`, Doku

**Nicht enthalten:**
- Jede Aenderung an Name, Pfad oder Format von `INBOX.md`
- Aenderungen an `dtb:idea-review`, `dtb:worker`, `dtb:workflow-next`, `dtb:archive`
- Automatischer Zeitverfall (bewusst gegen die Zwangsentscheidung getauscht)
- Becken-Eintraege in Arbeits-Ansichten sichtbar machen
- **Migration der 24 Altbestands-Befunde** — eigener Lauf NACH diesem Feature; das Becken startet leer
  und fuellt sich nur mit Neuem (Entscheidung 2026-09-08: sonst haengt die Abnahme an 24 Urteilsfragen,
  die den Mechanismus nicht betreffen)

**Im MVP enthalten, aber bewusst anspruchslos:**
- Alterungspruefung (`git log`-Datum der im Befund genannten Datei vs. Befund-Datum) als reine
  Hinweiszeile ohne Anspruch auf Richtigkeit — sie muss raten, welche Datei ein Befund meint

### Gewuenschtes Verhalten
- Einzeldurchgang mit nummerierten Aktionen wie `dtb:idea-review` (1./2./3.) — bewusst KEINE
  vetobare Sammelvorlage (Muster `feature-fast`): jede Entscheidung wird einzeln getroffen
- **Jede Entscheidung wird sofort geschrieben, nicht gesammelt am Ende.** Bricht der Lauf nach
  Eintrag 4 von 8 ab, sind 4 Entscheidungen fest und 4 stehen beim naechsten Lauf wieder an —
  loest nebenbei **#71** (idea-review verliert bei Abbruch die getroffenen Entscheidungen) und
  ist damit Vorbild fuer dessen spaetere Umsetzung
- Worktree-Guard + Lesestand-Pruefung (mtime) wie `dtb:idea-review` — der Skill schreibt globale
  Dateien und ist lesend-entscheidend
- **Reihenfolge: aelteste zuerst** — der Kontext baut aufeinander auf und der Altbestand schrumpft sichtbar
- Abschluss-Bilanz wie `impl-review`: `Befoerdert: N · Verworfen: N · Liegengelassen: N`
- **Nach dem Lauf: genau eine Hinweiszeile** auf `/dtb:idea-review`, wenn befoerdert wurde —
  kein Automatismus, kein Kettenaufruf

### Randfaelle
- **Nummernkollision (gemeinsamer Nummernkreis):** `dtb:idea` Schritt 2 vergibt heute die naechste
  Nummer aus `max(INBOX.md)`. Schreibt der Checkpoint #77 ins Becken, vergibt ein danach getipptes
  `/dtb:idea` die #77 erneut. Die Nummernvergabe muss das Maximum ueber BEIDE Dateien nehmen —
  in `dtb:idea` und im Checkpoint
- Becken fehlt / leer / alles gesichtet → eine Zeile "nichts zu sichten", Skill endet (fail-open wie `dtb:idea`)
- Alterungspruefung findet keine Datei im Befundtext, Datei umbenannt oder kein Git-Repo →
  Hinweiszeile weglassen, nie raten
- `archive/INBOX-BEFUNDE-verworfen.md` fehlt → mit Header anlegen
- Becken waehrend des Laufs fremdgeaendert → mtime-Pruefung vor JEDER Statusentscheidung,
  Stand neu laden, genau eine Warnzeile (Muster `dtb:idea-review`)
- **Duplikat-Check bei Befoerderung:** ja, unscharf gegen `INBOX.md` mit genau einer Rueckfrage
  (Muster `dtb:idea` Duplikat-Check); NICHT gegen das Becken
- **Begruendung beim Verwerfen ist Pflicht** (ein Satz genuegt) — sie landet in der Archivdatei und
  ist in sechs Monaten das Einzige, was den Vorgang noch erklaert

### Einschraenkungen
**Technisch:**
- **Zeilenbudget `dtb-workflow-checkpoint/SKILL.md`: 470 Zeilen, ausgeschoepft.** Laut Session-Log
  S11 wurde dort zuletzt jeder Fix mit Kompensation gemacht, damit die Datei bei 470/470 bleibt;
  `WORKFLOW_STATUS.md` fuehrt "Aufteilung faellig" als offene Notiz. **Entscheidung: kompensieren,
  nicht aufteilen** — die Aufteilung ist ein eigenes Thema und wuerde dieses Feature verdoppeln
- **Seed-Skew (INBOX #22, sechster dokumentierter Fall):** `INBOX-BEFUNDE.md` wird von
  `dtb:project-init` angelegt; Seeds sind "copied once, never drift-checked" und erreichen
  Bestandsprojekte NICHT automatisch. Der Triage-Skill muss das Becken beim ersten Lauf selbst
  anlegen koennen
- Kein Buildsystem, keine Tests — Verifikation laeuft ueber Wirklaeufe (Muster #72: 9 Stueck)
- Verteilung automatisch via `dtb:kit-sync` (Klasse-A-Muster `skills/dtb-*/SKILL.md` greift);
  Lock waechst von 47 auf 48 Eintraege
- `git` CLI noetig fuer die Alterungspruefung — fehlt es, entfaellt die Hinweiszeile ersatzlos

**Fachlich:**
- Deutsch, Markdown, Pipeline-Frontmatter (`stage`, `after`, `next`, `consumes`, `produces`)
- **`disable-model-invocation: true` fuer `dtb:idea-triage`** (Muster `dtb:idea-review`) — das
  Modell startet die Triage nie von selbst

### Integrationspunkte
**Pipeline-Kanten — beidseitig notieren** (INBOX #46/#58: Kanten im Kit sind zur Haelfte einseitig
notiert, kein Skill prueft das; dieses Feature darf den Bestand nicht vergroessern):

| Skill | heute | kuenftig |
|-------|-------|----------|
| `dtb:idea-triage` (neu) | — | `stage: idea` · `after: [dtb:workflow-checkpoint]` · `next: [dtb:idea-review]` |
| `dtb:workflow-checkpoint` | `next: [dtb:workflow-resume]` | `next: [dtb:workflow-resume, dtb:idea-triage]` |
| `dtb:idea-review` | `after: [dtb:idea]` | `after: [dtb:idea, dtb:idea-triage]` |

- **`DERIVED_STATE_RULES.md` bekommt eine Zeile:** ein Becken-Eintrag ist **status-neutral** — er ist
  keine Idee im Sinne der Ableitung (§-Tabelle Z. 38/166 "kein Ordner, nur INBOX-Eintrag → Idee"),
  sondern noch gar kein Vorgang. Behandlung analog zu den `[Fach]`-Fragen in §6
- **Externe Abhaengigkeiten:** keine. Einzig `git` fuer die Alterungspruefung, das faellt bei
  Abwesenheit ersatzlos weg

---

## Abhaengigkeiten

- **Ueberschneidung mit `checkpoint-verlustfunde` (#72, abgenommen 2026-09-08):** Das Feature hat die
  Wirkstelle gebaut, die dieses hier umleitet — Checkpoint Schritt 0 schreibt Verlustfunde selbst nach
  `lessons.md`/`INBOX.md`. Kein Konflikt, aber eine **Reihenfolge-Empfehlung**: erst `/dtb:archive`
  fuer #72, dann hier implementieren — sonst wird an einer Wirkstelle gebaut, deren Feature-Ordner
  parallel nach `archive/` wandert
- Keine Konflikte mit `feature-fast`, `feature-start-statusfeld`, `meeting-agenda`, `output-style-gezielt`

---

## Offene Punkte

- Referenz-Kopplung: `dtb:workflow-checkpoint` fuehrt heute `dtb:idea` Schritt 2 per Referenz aus
  (Grep auf `## Schritt 2: In INBOX.md speichern`, Z. 313). Schreibt der Checkpoint kuenftig ins Becken,
  stimmt die geliehene Schreibmechanik nicht mehr — entweder `dtb:idea` bekommt einen zieloffenen
  Abschnitt, oder die Triage-Datei bekommt eine eigene Schreibmechanik als Referenzquelle

---

**Erstellt mit:** `/dtb:feature-discover`
