# Implementierungsplan: Parallele Sessions

**Erstellt:** 2026-08-12
**Feature-Spec:** `features/parallele-sessions/spec.md`
**Geschaetzte Dauer:** 3-4 Sessions
**Status:** Reviewed (plan-review 2026-08-12: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Fundament: Konvention, Guard-Wortlaut, Config-Key | 0.5 Session | Geplant |
| Phase 2 | Schreib-Guard in 8 Skills ausrollen | 1 Session | Geplant |
| Phase 3 | Lese-Seite (idea-review, workflow-resume) | 0.5-1 Session | Geplant |
| Phase 4 | Hand-off: Format, Sende-Seite, Empfangsseite | 1 Session | Geplant |
| Phase 5 | Verteilung + End-to-End-Beleg | 0.5-1 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (15 Module, Pfade am 2026-08-12 per Datei-Existenz verifiziert).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-workflow-checkpoint/SKILL.md | Guard-Skill; bekommt zusaetzlich Sende- (4.2) und Empfangsseite (4.3) |
| skills/dtb-idea/SKILL.md | Guard-Skill, Capture (Text-Echo); vergibt INBOX-Nummern |
| skills/dtb-idea-review/SKILL.md | Guard-Skill; zusaetzlich Lese-Seite (3.1) — liest, dann entscheidet |
| skills/dtb-archive/SKILL.md | Guard-Skill; git mv + ARCHIVE_LOG/BACKLOG/Status |
| skills/dtb-lesson/SKILL.md | Guard-Skill, Capture (Text-Echo); lessons.md ungetrackt → Worktree-Write ginge verloren |
| skills/dtb-meeting-dump/SKILL.md | Guard-Skill; schreibt quer ueber mehrere Feature-Ordner |
| skills/dtb-task/SKILL.md | Guard-Skill, Capture (Text-Echo); produces BACKLOG.md |
| skills/dtb-bug-report/SKILL.md | Guard-Skill, Capture (Text-Echo); produces BACKLOG.md |
| skills/dtb-open-question/SKILL.md | KEIN Guard (produces nur features/*); in Konvention als worktree-faehig fuehren |
| skills/dtb-workflow-resume/SKILL.md | Lese-Seite (3.2): Pruefung vor Report-Ausgabe |
| skills/dtb-worker/SKILL.md | Traegt F1-Schreibgrenze als eigenen Wortlaut → auf zentrale Regel umstellen (1.1) |
| workflow.config.yaml | Template mit Platzhaltern; `worker:`-Block als Muster fuer neuen `parallel:`-Block |
| skills/dtb-project-init/SKILL.md | Seedet die Config → neuer Key muss ins Seed-Template (1.3) |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §1.1 (status-neutral), §1.3 (Konflikt-Ton) — nur referenziert, KEINE Aenderung (Seed-Skew #22 vermeiden) |
| skills/CLAUDE.md | Ziel der Konvention (1.1) und des kanonischen Guard-Blocks (1.2) |

---

## Phase 1: Fundament — Konvention, Guard-Wortlaut, Config-Key

### Ziel
Die EINE Quelle steht, bevor irgendein Skill angefasst wird: Schreibgrenzen-Regel,
Orchestrator-Muster und kanonischer Guard-Block in `skills/CLAUDE.md`; Config-Key im
Template. Verhindert von Anfang an zwei gepflegte Wortlaute (L14, Spiegel-Kopplungs-Risiko).

### Schritte

#### Schritt 1.1: Konvention in skills/CLAUDE.md + dtb-worker umstellen
- **Zweck:** EINE Schreibgrenzen-Regel („global schreibend ⇒ nur im Haupt-Checkout") + Orchestrator-Muster (genau eine Orchestrator-Session, N Worker in Worktrees) + Liste worktree-faehiger Skills (inkl. `open-question` explizit)
- **Dateien:** `skills/CLAUDE.md`, `skills/dtb-worker/SKILL.md`
- **Input:** discovery.md (Verhalten, Arbeitsteilung), dtb-worker F1-Passage
- **Output:** Neue Konventions-Sektion; dtb-worker verweist auf die Regel statt eigenen Wortlaut zu tragen (bestehende Worker-Mechanik unveraendert — Positiv-Gegenprobe #54: die Worker-eigenen Ablaeufe muessen stehen bleiben)

#### Schritt 1.2: Kanonischen Guard-Block festlegen
- **Zweck:** Einheitlicher, kurzer Block, den alle 8 Skills woertlich uebernehmen: Erkennung (`git rev-parse --absolute-git-dir` ≠ `--git-common-dir` — normalisierte absolute Pfade, kein relativ/absolut-Mix; Fehlschlag/kein Git = Durchlass), Abbruchmeldung (nennt Haupt-Checkout-Pfad via `--git-common-dir`), Text-Echo-Muster fuer Capture-Skills, optionale Branch-Pruefung (nur wenn Config-Key gesetzt)
- **Dateien:** `skills/CLAUDE.md` (Block steht dort als zitierbare Vorlage mit eindeutigem Grep-Anker, z. B. Ueberschrift `### Worktree-Guard`)
- **Input:** Schritt 1.1, Randfaelle aus discovery.md
- **Output:** Vorlage-Block mit Grep-Anker; definierter Wortlaut der Abbruchmeldung. Anforderungen (plan-review 2026-08-12): (a) Erkennungs- und Meldungs-Kommandos als EIN selbstaendiger Shell-Block — jeder Bash-Aufruf ist eine eigene Shell (L11); (b) Echo-Verhalten bei Dialog-Erfassung benannt: greift der Abbruch VOR dem Dialog, gibt es nichts zu echoen — die Meldung nennt dann nur den Befehl ohne Text-Anteil

#### Schritt 1.3: Config-Key + project-init-Seed
- **Zweck:** `parallel:`-Block in `workflow.config.yaml` (Muster: bestehender `worker:`-Block) — optional, Default-Verhalten ohne Key identisch zu heute (#22)
- **Dateien:** `workflow.config.yaml` (Template im Kit-Root), `skills/dtb-project-init/SKILL.md` (Seed-Template)
- **Input:** Technische Entscheidung „Config-Key" (unten)
- **Output:** `parallel.default_branch: null` in beiden Templates, kommentiert (null = nur Worktree-Check, gesetzt = zusaetzlich Branch-Pruefung im Haupt-Checkout)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Konventions-Sektion in `skills/CLAUDE.md` (Regel + Muster + Liste + Guard-Vorlage)
- [ ] `dtb-worker` verweist auf die zentrale Regel
- [ ] `parallel:`-Block in Config-Template und project-init-Seed

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "### Worktree-Guard" skills/CLAUDE.md` = 1 (Vorlage existiert genau einmal)
- [ ] Grep auf den Regel-Verweis in `skills/dtb-worker/SKILL.md` ≥ 1 UND die Worker-Kernregel („Never commits/pushes"-Passage bzw. Kollisionsregel) weiterhin vorhanden (Positiv-Gegenprobe)
- [ ] `grep -c "parallel:" workflow.config.yaml` = 1 und Grep im project-init-Seed-Template ≥ 1
- [ ] `open-question` steht in der worktree-faehig-Liste (Grep in skills/CLAUDE.md)

---

## Phase 2: Schreib-Guard in 8 Skills ausrollen

### Ziel
Alle 8 global schreibenden Skills tragen den Guard-Block aus 1.2 — vor ihrem ersten
schreibenden Schritt, mit identischem Wortlaut (L14: Spiegelung mechanisch verifizieren).

### Schritte

#### Schritt 2.1: Capture-Vierergruppe
- **Zweck:** Guard + Text-Echo in die vier Capture-Skills (der erfasste Freitext geht als fertiger Befehl in die Abbruchmeldung — kein Erfassungs-Verlust)
- **Dateien:** `skills/dtb-idea/SKILL.md`, `skills/dtb-lesson/SKILL.md`, `skills/dtb-task/SKILL.md`, `skills/dtb-bug-report/SKILL.md`
- **Input:** Guard-Vorlage aus 1.2
- **Output:** Guard-Block als frueher Schritt (vor Nummernvergabe/Write) in allen vier

#### Schritt 2.2: Prozess-Vierergruppe
- **Zweck:** Guard in die vier Prozess-Skills; bei `workflow-checkpoint` mit Vorgriff-Hinweis auf die Sende-Seite (Phase 4 ersetzt dort das blosse Echo durch den Hand-off-Block)
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`, `skills/dtb-idea-review/SKILL.md`, `skills/dtb-archive/SKILL.md`, `skills/dtb-meeting-dump/SKILL.md`
- **Input:** Guard-Vorlage aus 1.2
- **Output:** Guard-Block als Schritt 0/1 in allen vier

#### Schritt 2.3: Spiegel-Verifikation + No-op-Beleg + blinder Lauf
- **Zweck:** L14 mechanisch: identischer Wortlaut ueberall; #54-Gegenprobe: kein Guard, wo keiner hingehoert; Verhalten im Haupt-Checkout unveraendert; L7: ein blinder Agenten-Lauf (frische Session, nur Skill + Worktree-Fixture, kein Autor-Kontext) prueft die Guard-Mechanik ohne Autor-Brille
- **Dateien:** keine (read-only Pruefung; Fixture-Worktree wird nach dem Lauf entfernt)
- **Input:** Grep-Anker aus 1.2
- **Output:** Verifikations-Protokoll im Chat (Zaehlungen + Probelauf + Blind-Lauf-Ergebnis)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] 8 Skills mit identischem Guard-Block
- [ ] Verifikations-Protokoll (Grep-Zaehlung + No-op-Probelauf)

### Checkpoint-Kriterien

#### Automated
- [ ] Grep auf den Guard-Anker ueber `skills/dtb-*/SKILL.md` = genau 8 Dateien (Zielzahl, L14)
- [ ] Grep auf den Guard-Anker in `skills/dtb-open-question/SKILL.md` = 0 (Gegenprobe)
- [ ] Text-Echo-Muster in genau den 4 Capture-Skills vorhanden (Grep = 4)
- [ ] Probelauf eines Guard-Skills im Haupt-Checkout: kein Guard-Output (No-op-Beleg; `git rev-parse --absolute-git-dir` = `--git-common-dir` als Vorbedingung protokolliert)
- [ ] Blinder Agenten-Lauf (L7): frische Session, ein Guard-Skill in einem Fixture-Worktree → Abbruch mit korrekter Meldung; im Haupt-Checkout → No-op (beide Ausgaenge protokolliert)

---

## Phase 3: Lese-Seite

### Ziel
`idea-review` und `workflow-resume` erkennen veraltete Lesestaende vor Entscheidungen —
der belegte 2026-08-11-Fall (Fremdschreib waehrend des Laufs) wird gefangen statt zufaellig entdeckt.

### Schritte

#### Schritt 3.1: idea-review — Lesestand-Pruefung
- **Zweck:** Beim Einlesen mtime der INBOX merken; unmittelbar vor JEDER Statusentscheidung (Schreiben) mtime erneut pruefen; bei Abweichung Re-Read + Inhaltsvergleich; ⚠-Zeile nur bei tatsaechlicher Inhaltsabweichung
- **Dateien:** `skills/dtb-idea-review/SKILL.md`
- **Input:** Verhalten (B) aus discovery.md, mtime-Mechanik (Technische Entscheidung unten)
- **Output:** Pruef-Baustein im Ablauf vor Schritt-3-Aktionen und dem Statusschreiben

#### Schritt 3.2: workflow-resume — Pruefung vor Report-Ausgabe
- **Zweck:** Gleicher Baustein, gespiegelt: gelesene Dateien (Status, INBOX, plan.md) vor der Report-Ausgabe gegen den Lesezeitpunkt pruefen; ⚠-Zeile im Report bei Abweichung
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md`
- **Input:** Baustein aus 3.1 (identischer Wortlaut, L14)
- **Output:** Pruef-Schritt vor Schritt 5 (Resume-Report)

#### Schritt 3.3: Verifikation per simuliertem Fremdschreib
- **Zweck:** Beide Faelle belegen: (a) Datei zwischen Lesen und Entscheiden inhaltlich geaendert → ⚠ + Re-Read; (b) nur mtime beruehrt (touch) → keine bzw. abgeschwaechte Meldung
- **Dateien:** keine (Testlauf, Aenderungen werden zurueckgenommen)
- **Input:** 3.1 + 3.2
- **Output:** Testprotokoll im Chat (beide Faelle)

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Lesestand-Pruefung in beiden Skills (identischer Baustein)
- [ ] Testprotokoll Fall (a) und (b)

> **Zwischenabnahme-Marker (plan-review 2026-08-12):** Mit Phase 3 ist ein eigenstaendig
> verteilbarer Zwischenstand erreicht (Guard + Lese-Seite, unabhaengig vom Hand-off) —
> verschiebt sich der Herdr-Ausbau, kann hier abgenommen und verteilt werden; Phase 4/5
> folgen dann separat.

### Checkpoint-Kriterien

#### Automated
- [ ] Grep auf den Pruef-Baustein-Anker ueber `skills/dtb-*/SKILL.md` = genau 2 Dateien (idea-review, workflow-resume)
- [ ] Testlauf (a): simulierter Fremdschreib erzeugt ⚠-Zeile + Re-Read (protokolliert)
- [ ] Testlauf (b): touch-only erzeugt KEINE Voll-Warnung (protokolliert)

---

## Phase 4: Hand-off — Format, Sende-Seite, Empfangsseite

### Ziel
Eine Worktree-Session uebergibt ihre Session-Inhalte checkpoint-fertig an die
Orchestrator-Session; `workflow-checkpoint` kann fremde Bloecke konsumieren.

### Schritte

#### Schritt 4.1: Hand-off-Block-Format definieren
- **Zweck:** Standardisierter, status-neutraler Block (§1.1; L9: explizit als status-neutral abgrenzen — KEINE Checkboxen, die §1/§2-Ableitung mitzaehlen koennte). Felder: Quelle (Feature-Slug, Branch, Zeitpunkt), Erledigt, Entscheidungen, Dateien, Offene Punkte/Naechste Schritte
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (Format lebt dort als die eine Quelle), `skills/CLAUDE.md` (nur Verweis)
- **Input:** Session-Log-Template des Checkpoints (Felder muessen aufs Log abbildbar sein)
- **Output:** Format-Definition mit Grep-Anker (z. B. `### Hand-off-Block`)

#### Schritt 4.2: Sende-Seite — checkpoint-Guard produziert den Block
- **Zweck:** Laeuft `workflow-checkpoint` im Worktree, bricht der Guard nicht nur ab, sondern erzeugt den Hand-off-Block aus dem Sitzungskontext als Text-Echo (Transport: Herdr an die Orchestrator-Pane; ohne Herdr manuell kopieren)
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` (ersetzt den Vorgriff-Hinweis aus 2.2)
- **Input:** Format aus 4.1, Guard aus Phase 2
- **Output:** Sende-Pfad im Guard-Zweig des Checkpoints

#### Schritt 4.3: Empfangsseite — checkpoint nimmt fremden Block an
- **Zweck:** `workflow-checkpoint` erkennt einen uebergebenen Hand-off-Block (Argument oder eingefuegter Text), validiert die Pflichtfelder und schreibt daraus den Session-Log-Eintrag mit Quell-Kennzeichnung („Worker-Session, Worktree {branch}"); fehlende Pflichtfelder → nachfragen, nicht raten
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Format aus 4.1
- **Output:** Empfangs-Pfad im Checkpoint-Ablauf

> **3x3-Block:** Nach Schritt 4.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Format-Definition (status-neutral, §1.1-konform)
- [ ] Sende-Pfad (Guard-Zweig) + Empfangs-Pfad im Checkpoint

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c "### Hand-off-Block" skills/dtb-workflow-checkpoint/SKILL.md` = 1; Verweis in `skills/CLAUDE.md` ≥ 1
- [ ] Format enthaelt keine `- [ ]`-Checkbox-Zeilen (L9-Gegenprobe: Grep im Format-Beispiel = 0)
- [ ] Fixture-Lauf Empfangsseite: Beispiel-Block → Session-Log-Eintrag mit Quell-Kennzeichnung (protokolliert)

#### Manual
- [ ] Der erzeugte Log-Eintrag ist inhaltlich gleichwertig zu einem selbst geschriebenen (Stichprobe, menschliches Urteil)

---

## Phase 5: Verteilung + End-to-End-Beleg

### Ziel
Die Aenderungen erreichen die installierten Kopien, und das Gesamtbild ist einmal real
durchlaufen: Worker-Session im Worktree → Hand-off → Orchestrator-Checkpoint.

### Schritte

#### Schritt 5.1: Commit, Push, kit-sync
- **Zweck:** Klasse-A-Nachlauf (bewusst manuell, #51 ist offen): alle geaenderten SKILL.md verteilen; `dtb-kit-sync` selbst ist nicht betroffen → ein Lauf genuegt (L22-Bedingung greift nicht)
- **Dateien:** keine neuen (git + sync)
- **Input:** Phasen 1-4 committet
- **Output:** Lock aktuell, Report „0 Abweichungen"

#### Schritt 5.2: End-to-End-Durchlauf
- **Zweck:** Realer Beleg der Success Criteria im Zusammenspiel: Worktree-Session (nativ via EnterWorktree oder Herdr-Worker) versucht einen Guard-Skill (Abbruch + Echo belegt), erzeugt den Hand-off-Block, Orchestrator-Session konsumiert ihn per Checkpoint (der Lese-Seiten-Beleg ist bereits deterministisch in 3.3 erbracht und hier kein Kriterium)
- **Dateien:** keine (Abnahme-Lauf; entstehende Artefakte sind echte Session-Artefakte)
- **Input:** 5.1 (installierte Kopien aktuell)
- **Output:** Abnahme-Protokoll im Session-Log

### Deliverables
- [ ] Sync-Report 0 Abweichungen
- [ ] End-to-End-Protokoll (Guard-Abbruch, Hand-off, Empfangs-Checkpoint)

### Checkpoint-Kriterien

#### Automated
- [ ] `kit-sync check` nach dem Sync: 0 Abweichungen ueber alle Klasse-A-Artefakte
- [ ] Guard-Beleg aus dem Durchlauf: Abbruchmeldung enthaelt den Haupt-Checkout-Pfad (Protokoll)

#### Manual
- [ ] End-to-End-Durchlauf abgenommen (Hand-off-Inhalt kam vollstaendig im Session-Log an)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Guard-Verhalten | Abbruch / Warnung+Nachfrage / differenziert | Abbruch, einheitlich | Discovery 3b: Capture-Skills tragen die belegten Kollisionen; eine Regel statt zwei; Text-Echo loest den Verlust-Fall |
| Guard-Erkennung | rev-parse-Vergleich / Pfad-Konvention / Config-Flag | `git rev-parse --absolute-git-dir` ≠ `--git-common-dir`; Fehlschlag = Durchlass | Mechanisch, config-unabhaengig (commit-and-push-Muster); absolute Pfade vermeiden den relativ/absolut-Mix der Ausgaben (plan-review 2026-08-12); Nicht-Git-Projekte unbeeintraechtigt |
| Reihenfolge zu #35 | #35 zuerst / dieses Feature zuerst / parallel | Dieses Feature zuerst — #35 wartet | Beide aendern `workflow-checkpoint`; #35 baut danach auf der neuen Struktur (Guard-Zweig, Empfangsseite) auf statt umgekehrt; loest die Spec-Dependency „Erforderlich vor Start" |
| DERIVED_STATE_RULES.md | Neuer § fuer Parallelitaet / unveraendert lassen | Unveraendert (Spec sagt „ggf.") | Klasse-B-Seed: jeder neue § erzeugt Seed-Skew in Bestandsprojekten (#22, sechs belegte Faelle); die Konvention traegt `skills/CLAUDE.md` (Klasse A, reist mit kit-sync) |
| Config-Key | `parallel.default_branch` / eigener Guard-Block / kein Key | `parallel.default_branch: null` (Default null) | Optional mit Default (#22): null = nur Worktree-Check (heutiges Verhalten), gesetzt = zusaetzliche Branch-Pruefung im Haupt-Checkout |
| Hand-off-Traeger | Chat-Text (Herdr) / Datei im Feature-Ordner | Chat-Text, KEINE Datei | Transient, veraltet schnell (Drift-Risiko, #33-Muster „Chat-only"); `worker-report.md` bleibt der Worker-Lane vorbehalten |
| Sende-Seite | Eigener Skill / checkpoint-Guard-Zweig | checkpoint-Guard-Zweig | Kein neuer Einstiegspunkt; der Abbruch-Moment IST der Sende-Moment |
| mtime-Mechanik | `ls --time-style=full-iso` / `stat` / Datei-Hash | `ls --time-style=full-iso` (Git-Bash, beide Plattformen) als Trigger; Inhaltsvergleich entscheidet die Meldung | In dieser Umgebung belegt funktionsfaehig; Hash allein waere teurer, mtime allein zu falsch-positiv-anfaellig |
| Format-Quelle Hand-off | CLAUDE.md / workflow-checkpoint | workflow-checkpoint (CLAUDE.md verweist nur) | Konsument definiert das Format (eine Quelle, L14); Checkpoint ist Empfaenger |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Konvention CLAUDE.md + worker-Umstellung — `7009da6`
- [x] 1.2 Kanonischer Guard-Block — `7009da6`
- [x] 1.3 Config-Key + project-init-Seed — `7009da6`
- [x] 2.1 Guard Capture-Vierergruppe — `bd35683`
- [x] 2.2 Guard Prozess-Vierergruppe — `bd35683`
- [x] 2.3 Spiegel-Verifikation + No-op-Beleg — `bd35683`
- [x] 3.1 Lese-Seite idea-review — `d97ad6b`
- [x] 3.2 Lese-Seite workflow-resume — `d97ad6b`
- [x] 3.3 Fremdschreib-Verifikation — `d97ad6b`
- [x] 4.1 Hand-off-Format — `42774fe`
- [x] 4.2 Sende-Seite (Guard-Zweig checkpoint) — `42774fe`
- [x] 4.3 Empfangsseite checkpoint — `42774fe`
- [x] 5.1 Commit, Push, kit-sync — `f91b8d5`
- [x] 5.2 End-to-End-Durchlauf — `f91b8d5`

---

## Umsetzung

Umsetzung mit `/dtb:implement parallele-sessions` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/parallele-sessions/plan.md` laden; der erste
nicht abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
