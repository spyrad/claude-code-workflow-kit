# Implementierungsplan: pane-start

**Erstellt:** 2026-08-19
**Feature-Spec:** `features/pane-start/spec.md`
**Geschaetzte Dauer:** ~5 h
**Status:** Reviewed (plan-review 2026-08-19: REVISE → 5 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill anlegen + Kopplung setzen | ~2.5 h | Geplant |
| Phase 2 | Absicherung + Verteilung | ~2.5 h | Geplant |

---

## Ist-Analyse

> Anker sind **Sektions-Titel und Absatz-Marker**, nie Zeilennummern (plan-review 2026-08-19:
> zwei von vier Zeilenangaben stimmten schon am Erstellungstag nicht — L2). Zeilenzahlen stehen
> nur als Groessenangabe der Datei.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-worker/SKILL.md` | 452 Zeilen. `### Traeger-Weiche (Subagent \| Pane)` mit dem Absatz `**Eligibility-Gate des Pane-Traegers (hart):**` (HERDR_ENV + `command -v herdr`, ⛔-Fence ohne stille Degradierung); `### Pane-Auftrag (Vorlage — die eine Quelle)`; `### Pane-Ausfuehrung (Traeger `pane`)` mit Vorbedingungen, 4-Kommando-Start-Sequenz, Rueckweg und `#### Abschluss (nach menschlicher Diff-Abnahme)`. Beide Pane-Sektionen deklarieren sich ausdruecklich als die einzigen Orte der Herdr-Kommandos |
| `skills/CLAUDE.md` | 366 Zeilen. `## Autonomie-Regel (dtb:worker)`; `### Skill-Kategorien (Worktree-Verhalten)` mit Voll-Guard/Teil-Guard/worktree-faehig/read-only und dem Satz „Ein NEUER Skill mit globalen `produces`-Eintraegen uebernimmt die Guard-Vorlage ab dem ersten Tag"; `### Worktree-Guard (kanonische Vorlage)`, Referenz-Instanz ist `skills/dtb-idea/SKILL.md` |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 373 Zeilen. `### Hand-off-Block (Format — die eine Quelle)`; der Absatz `**Branch-Angabe:**` direkt darunter beschreibt Worktrees pauschal als branchlos — bekannter, separat offener Nachlauf, hier nur gelesen |
| `skills/dtb-feature-fast/SKILL.md` | `## Schritt 2: Struktur-Check (Kopplungs-Waechter)` — Vorbild fuer die Quellen-Aufloesung (global mit Projekt-Fallback), den Anker-Grep und die zwei getrennten Fehlerpfade |
| `CLAUDE.md` (Projekt-Root) | Skill-Katalog nach Kategorien; `dtb:worker` steht unter „Autonomous execution" |
| `skills/dtb-pane-start/` | Existiert nicht — Neubau |

---

## Phase 1: Skill anlegen + Kopplung setzen

### Ziel
Der Skill existiert vollstaendig, traegt Guard, Gate und einen Struktur-Check auf seine
Mechanik-Quelle, und die Herdr-Sequenz bleibt an ihren zwei Orten — mit beidseitigem
Kopplungs-Hinweis.

### Schritte

#### Schritt 1.1: Skill-Grundgeruest, Guard und Gate
- **Zweck:** Rahmen, Eingangsbedingungen und Argument-Aufloesung stehen, bevor irgendetwas gestartet wird
- **Dateien:** `skills/dtb-pane-start/SKILL.md` (neu)
- **Input:** Guard-Vorlage aus `skills/CLAUDE.md` → `### Worktree-Guard (kanonische Vorlage)`, Referenz-Instanz `skills/dtb-idea/SKILL.md`; Gate-Wortlaut-Vorbild aus `skills/dtb-worker/SKILL.md` → Absatz `**Eligibility-Gate des Pane-Traegers (hart):**`
- **Output:** Frontmatter (`name: dtb:pane-start`, `disable-model-invocation: true`, `argument-hint`, `allowed-tools: Read, Glob, Grep, Bash`, `pipeline` mit leerem `produces`), `## Worktree-Guard` byte-identisch zur Vorlage, Herdr-Gate mit eigenem ⛔-Text, Argument-Aufloesung (INBOX-Nummer ODER Change-Slug, kein Ad-hoc-Einstieg ohne Treffer), Vorbedingungs-Pruefung auf uncommittete Zielarbeit

#### Schritt 1.2: Begruessungstext-Vorlage und Start-Ablauf
- **Zweck:** Die Session erfaehrt in EINER Nachricht alles Notwendige und weiss, dass sie auf den Menschen wartet; der Ablauf verweist auf die bestehende Sequenz statt sie zu wiederholen
- **Dateien:** `skills/dtb-pane-start/SKILL.md`
- **Input:** `### Pane-Auftrag (Vorlage — die eine Quelle)` und `### Pane-Ausfuehrung` aus `skills/dtb-worker/SKILL.md` (Vorbild fuer Aufbau und Reihenfolge, NICHT zum Kopieren der Kommandos); `### Hand-off-Block (Format — die eine Quelle)` aus `skills/dtb-workflow-checkpoint/SKILL.md`
- **Output:** Sektion `## Herdr-Mechanik` mit Verweis auf `dtb:worker` → `### Pane-Ausfuehrung` als die eine Quelle (Branch abweichend: `feature/{slug}` statt `task/{slug}`, begruendet); Begruessungstext-Vorlage mit Change-Slug, Worktree-Pfad, vorgeschlagenem Startbefehl, Orchestrator-Adresse aus `$HERDR_PANE_ID`, Rueckweg-Pflicht; **ausdrueckliche Wartepflicht am Ende des Texts** — der genannte Startbefehl wird VOM MENSCHEN ausgeloest, die Session fuehrt ihn nicht selbst aus und arbeitet bis dahin nicht (das ist der operative Unterschied zwischen Begruessung und autonomem Auftrag); Fall „Change-Ordner hat schon Artefakte" nennt den abgeleiteten naechsten Schritt statt eines Startbefehls; Abschluss-Hinweis verweist auf `dtb:worker` → `#### Abschluss`

#### Schritt 1.3: Struktur-Check der Mechanik-Quelle
- **Zweck:** Der Skill traegt die Kommandos nicht selbst und darf deshalb nie auf einer fehlenden oder umgebauten Quelle arbeiten — ohne diesen Check hat er weder Fallback noch Diagnose
- **Dateien:** `skills/dtb-pane-start/SKILL.md`
- **Input:** Muster aus `skills/dtb-feature-fast/SKILL.md` → `## Schritt 2: Struktur-Check (Kopplungs-Waechter)`
- **Output:** Sektion `## Struktur-Check` mit Quellen-Aufloesung (zuerst `~/.claude/skills/dtb-worker/SKILL.md`, sonst Fallback `skills/dtb-worker/SKILL.md` im Projekt-Root), Anker-Grep auf `### Pane-Ausfuehrung` UND `### Pane-Auftrag` (zeilenende-normalisiert, L25), sowie zwei **getrennte** Fehlerpfade: Datei in beiden Quellen nicht gefunden → Installations-Hinweis (`/dtb:kit-sync sync`), kein Drift-Befund; Datei vorhanden aber Anker fehlt → harter Stopp (keine Arbeit auf veralteter Basis)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Kopplung und Einordnung in die Konventionen
- **Zweck:** Spaetere Herdr-Drift wird an einer Stelle korrigiert, und der neue Skill wird nicht unter die Autonomie-Regel gelesen
- **Dateien:** `skills/dtb-worker/SKILL.md`, `skills/CLAUDE.md`
- **Input:** Kopplungs-Regel L14 (Spiegel mitziehen und mechanisch verifizieren)
- **Output:** In `dtb:worker` je ein Kopplungs-Hinweis **innerhalb** von `### Pane-Auftrag` und `### Pane-Ausfuehrung` — nicht in einer Fussnote („`dtb:pane-start` liest diese Sequenz und greppt auf diesen Sektions-Titel — Umbenennung oder Umbau dort mitziehen"); in `skills/CLAUDE.md` eine Zeile in `### Skill-Kategorien` (Voll-Guard, Begruendung: legt Worktrees vom Haupt-Checkout an, obwohl `produces` leer ist — bewusste Abweichung vom `produces`-Kriterium) und ein Abgrenzungssatz in `## Autonomie-Regel (dtb:worker)` (der interaktive Start faellt nicht darunter: ein Mensch arbeitet in der Pane, es gibt keine Deckelung und keinen Bericht)

### Deliverables
- [ ] `skills/dtb-pane-start/SKILL.md` vollstaendig (Guard, Gate, Struktur-Check, Begruessungstext)
- [ ] Beidseitige Kopplungs-Hinweise gesetzt
- [ ] Guard-Kategorie und Autonomie-Abgrenzung in `skills/CLAUDE.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `skills/dtb-pane-start/SKILL.md` existiert und traegt `## Worktree-Guard` (Grep, zeilenende-normalisiert per `tr -d` mit CR-Argument — L25)
- [ ] Guard-Bash-Block und ⛔-Fence sind byte-identisch zur Referenz-Instanz `skills/dtb-idea/SKILL.md` (Vergleich der extrahierten Bloecke, nur der Skill-Name darf abweichen)
- [ ] Keine Start-Sequenz-Kommandos im neuen Skill: zeilenende-normalisierter Grep auf `herdr pane split` und `herdr pane run` ergibt je 0 Treffer. `herdr agent prompt` hoechstens 1 Treffer, und dieser MUSS `{orchestrator-pane}` als Ziel tragen (Rueckweg-Anweisung im zugestellten Begruessungstext — im Vorbild `dtb:worker` identisch im Pane-Auftrag vorhanden); ein Treffer mit `{pane-id}` waere die duplizierte Zustellung und ist verboten. Korrektur waehrend der Umsetzung 2026-08-19, Anlass: das vorige Wort-Kriterium traf die Rueckweg-Zeile des zugestellten Texts — zweiter #54-Fall dieser Phase (Wirkstelle statt Sprach-Muster)
- [ ] Der neue Skill traegt `## Struktur-Check` mit beiden Ankern (`### Pane-Ausfuehrung`, `### Pane-Auftrag`) und beiden getrennten Fehlerpfaden (Grep auf Sektion + je einen Pfad-Marker)
- [ ] Keine Governance-**Mechanik** im neuen Skill: zeilenende-normalisierter Grep auf `{worker.max_attempts}`, `{worker.max_minutes}`, `worker-report.md` und `Deckelung: max.` ergibt je 0 Treffer. Begriffsnennungen in der Abgrenzungs-Prosa („hat kein Tauglichkeitsraster") sind KEIN Treffer — Negativ-Kriterien werden auf die Wirkstelle geankert, nicht auf Sprach-Muster (`skills/CLAUDE.md` → `### Negativ-Kriterien auf die Wirkstelle ankern`; INBOX #54). Korrektur waehrend der Umsetzung 2026-08-19, Anlass: das vorige Wort-Kriterium schlug an der Abgrenzung an, die es schuetzen soll
- [ ] Zeilenende-normalisierter Grep auf `dtb:pane-start` in `skills/dtb-worker/SKILL.md` ergibt mindestens 2 Treffer (beide Kopplungs-Hinweise)
- [ ] Zeilenende-normalisierter Grep auf `pane-start` in `skills/CLAUDE.md` ergibt mindestens 2 Treffer (Kategorien-Zeile + Autonomie-Abgrenzung)
- [ ] Frontmatter traegt `disable-model-invocation: true` und ein leeres `produces`

#### Manual
- [ ] Der Begruessungstext liest sich als vollstaendiger Arbeitsauftrag an einen Menschen: Ort, Startbefehl, Rueckkanal, Rueckweg-Pflicht, Wartepflicht — ohne Governance-Sprache des autonomen Workers

---

## Phase 2: Absicherung + Verteilung

### Ziel
Die Abbruchpfade sind blind gegengetestet, ein echter Start ist belegt — inklusive der
Wartepflicht — und der Skill ist verteilt und katalogisiert.

### Schritte

#### Schritt 2.1: Fixture-Setup und -Abbau
- **Zweck:** Der Worktree-Abbruchpfad braucht einen verlinkten Worktree; ohne benanntes Setup hat der Test keine Vorbedingung und der Abbau bleibt liegen
- **Dateien:** keine Aenderung (Testumgebung)
- **Input:** Haupt-Checkout, sauberer Arbeitsbaum
- **Output:** Ein verlinkter Test-Worktree existiert (`git worktree add`, Pfad unter `.dtb-worktrees/`); nach Schritt 2.2 wieder entfernt (`git worktree remove` + `git worktree prune`, unter Windows ggf. mit kurzer Wartezeit wegen Datei-Locks)

#### Schritt 2.2: Drei blinde Abbruch-Laeufe
- **Zweck:** Implizite Kontext-Annahmen im Skill-Text sichtbar machen (L7) und belegen, dass ohne Pane-Umgebung nichts halb Eingerichtetes zurueckbleibt
- **Dateien:** keine Aenderung (Pruefung); Befunde fliessen als Korrekturen in `skills/dtb-pane-start/SKILL.md`
- **Input:** Skill-Datei aus Phase 1; drei Fixtures: Aufruf ohne `HERDR_ENV`, Aufruf mit unbekanntem Argument, Aufruf aus dem Test-Worktree aus 2.1
- **Output:** Drei Laeufe mit korrektem Abbruch (kein Worktree, keine Pane, keine Degradierung); gefundene Unklarheiten korrigiert. **Ablage der Lauf-Protokolle: Session-Log ueber `/dtb:workflow-checkpoint`** — dieser Skill schreibt selbst keine Dateien

#### Schritt 2.3: Echter Pane-Start (Ende-zu-Ende)
- **Zweck:** Der Hinweg ist real belegt, nicht nur beschrieben — und die Wartepflicht haelt
- **Dateien:** keine Aenderung (Pruefung)
- **Input:** der eigene Change `pane-start` (Dogfooding: die gestartete Session ist die, die Schritt 2.4 abschliesst), laufende Herdr-Umgebung
- **Output:** Worktree + Branch entstanden, Pane traegt eine erkannte Session, Begruessungstext als EINE Nachricht angekommen, Wartepflicht beobachtet, Arbeitsplatz danach wieder abgebaut

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

#### Schritt 2.4: Katalog und Verteilung
- **Zweck:** Der Skill ist auffindbar und auf der Maschine installiert
- **Dateien:** `CLAUDE.md`, `~/.claude/skills/dtb-pane-start/SKILL.md` (via Verteilung), `~/.claude/dtb-lock.json`
- **Input:** fertige Skill-Datei, `/dtb:kit-sync`
- **Output:** Katalog-Eintrag in `CLAUDE.md` (bei „Autonomous execution" abgegrenzt oder als eigener Punkt), Commit, dann `/dtb:kit-sync sync` — Lock traegt 47 Artefakte

### Deliverables
- [ ] Test-Worktree angelegt und rueckstandsfrei abgebaut
- [ ] Drei blinde Abbruch-Laeufe im Session-Log protokolliert
- [ ] Ein echter Start belegt, inklusive Wartepflicht
- [ ] Katalog-Eintrag + Verteilung

### Checkpoint-Kriterien

#### Automated
- [ ] Zeilenende-normalisierter Grep auf `pane-start` in `CLAUDE.md` ergibt mindestens 1 Treffer
- [ ] `/dtb:kit-sync check` meldet 47 Artefakte, 0 Abweichungen
- [ ] Keine verwaisten Registrierungen: `git worktree list` zeigt nur den Haupt-Checkout, `git branch --list` mit Muster `feature/*` enthaelt weder Test-Branch noch Dogfooding-Branch

#### Manual
- [ ] Die drei blinden Laeufe brachen aus dem richtigen Grund ab (Gate, unbekanntes Argument, Worktree) und hinterliessen nichts
- [ ] Die gestartete Session hat den vorgeschlagenen Startbefehl NICHT selbst ausgefuehrt und auf Eingabe gewartet
- [ ] Im echten Lauf war die gestartete Session ohne Rueckfrage arbeitsfaehig — der Begruessungstext genuegte

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traegerschaft | eigener Skill mit Verweis / dritter Modus in `dtb:worker` / eigener Skill mit Kopie | eigener Skill, Mechanik referenziert | Governance-Trennung sauber (keine Autonomie-Deckelung fuer einen Menschen), ohne einen dritten Drift-Ort fuer die Herdr-Kommandos zu schaffen (Nutzer-Entscheid 2026-08-19) |
| Absicherung des Verweises | Prosa-Verweis / Laufzeit-Struktur-Check | Struktur-Check nach `feature-fast`-Muster (Schritt 1.3) | Ein Skill ohne eigene Kopie hat keinen Fallback: fehlt oder wandert die Quelle, waere der Ausfall ohne Check stumm (plan-review 2026-08-19, Pre-Mortem) |
| Anker-Form der Verweise | Zeilennummern / Sektions-Titel | Sektions-Titel und Absatz-Marker | Zeilennummern verschieben sich bei jeder Aenderung der Fremd-Datei; zwei von vier Angaben waren am Erstellungstag bereits falsch (L2) |
| Branch-Konvention | `task/{slug}` / `feature/{slug}` | `feature/{slug}` | `task/` ist Worker-Konvention fuer aufgabenbasierte Auftraege; die Voll-Schiene arbeitet an einem Feature-Change, und der Branchname ist der Merge-Anker |
| Einstiegspunkt | nur INBOX-Nummer / nur Slug / beides | beides, ein Argument | Der Skill soll auch die Fortsetzung eines angefangenen Change tragen; ein INBOX-Pflicht-Gate wie bei `feature-fast` waere dafuer zu eng |
| Abschluss (Merge/Abbau) | im Skill / beim Menschen | beim Menschen, Muster referenziert | Der Merge-Zeitpunkt ist beim Start unbekannt (Voll-Schiene laeuft ueber mehrere Sessions) |
| Guard-Kategorie | Voll-Guard / worktree-faehig | Voll-Guard | Betriebliche Begruendung statt `produces`: Worktrees entstehen vom Haupt-Checkout; die Kategorien-Zeile nennt diese Abweichung vom Einteilungs-Kriterium ausdruecklich |
| Statusflip in der Inbox | im Start-Skill / im gestarteten Skill | im gestarteten Skill | Der Start-Skill schreibt nichts Zentrales; `feature-discover`/`feature-fast` flippen als Teil-Guards selbst und melden es im Hand-off |
| Nachweis der fehlenden Governance | Absicht in der Prosa / Negativ-Grep | Negativ-Grep als Automated-Kriterium | Die Spec-Aussage „entfaellt ersatzlos" wird nur so pruefbar; die Verwechslungsgefahr entsteht beim Kopieren der Nachbar-Sektion (plan-review 2026-08-19) |
| Testobjekt des echten Laufs | fremder Bestands-Slug / eigener Change | eigener Change (Dogfooding) | Ein fremder Slug erzeugt Worktree und Branch fuer Arbeit, die niemand macht; der eigene Change testet die Mechanik am richtigen Objekt |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Skill-Grundgeruest, Guard und Gate — `cad078f`
- [x] 1.2 Begruessungstext-Vorlage und Start-Ablauf — `cad078f`
- [x] 1.3 Struktur-Check der Mechanik-Quelle — `cad078f`
- [x] 1.4 Kopplung und Einordnung in die Konventionen — `cad078f`
- [x] 2.1 Fixture-Setup und -Abbau — `7b9d773`
- [x] 2.2 Drei blinde Abbruch-Laeufe — `7b9d773`
- [x] 2.3 Echter Pane-Start (Ende-zu-Ende) — `5ed27c8`
- [x] 2.4 Katalog und Verteilung — `585574a`

---

## Umsetzung

Umsetzung mit `/dtb:implement pane-start` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/pane-start/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-19)
