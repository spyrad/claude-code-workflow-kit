# Implementierungsplan: Pane-Session-Neustart

**Erstellt:** 2026-10-21
**Feature-Spec:** `features/pane-session-neustart/spec.md`
**Geschaetzte Dauer:** ca. 4-5 h
**Status:** Reviewed (plan-review 2026-10-21: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Sende-Seite: Notiz-Format + Weiche „Wechsel oder Ende?" im Checkpoint | 1,5-2 h | Geplant |
| Phase 2 | Empfangs-Seite: Resume liest die Notiz, prueft die Adresse; Ankuendigungen | 1,5 h | Geplant |
| Phase 3 | Abbau-Warnung, Kanon/Doku nachziehen, Verifikation am echten Wechsel | 1-1,5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` → `## Betroffene Module` (9 Pfade, per Glob verifiziert 2026-10-21).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-workflow-checkpoint/SKILL.md | `## Worktree-Guard`: im verlinkten Worktree ⛔ + „Sende-Seite" (baut WORKTREE-HANDOFF-Block aus dem Sitzungskontext, schreibt NICHTS). `### Hand-off-Block (Format — die eine Quelle)` mit Feldern Erledigt/Entscheidungen/Dateien/Offene Punkte/Uebersprungene globale Updates. Haupt-Checkout: `## Handoff` in WORKFLOW_STATUS (Vorbild). Schritt 0 `no-loss-check` laeuft im Worktree nie (Guard bricht vorher ab) |
| skills/dtb-workflow-resume/SKILL.md | read-only (`produces: []`, Tools Read/Bash). Schritt 2 liest `WORKFLOW_STATUS.md` → `## Handoff` (im Worktree: veraltete Branch-Kopie). Report-Vorlagen Fall A/B/C, max. 60 Zeilen. Kein Worktree-spezifischer Pfad ausser Schritt 3b (Worktree-Liste) |
| skills/dtb-pane-start/SKILL.md | `## Begruessungstext (Vorlage — die eine Quelle …)` mit Wartepflicht + Rueckweg-Zeile (deklarierter Herdr-Spiegel). Kein Hinweis auf Session-Wechsel |
| skills/dtb-worker/SKILL.md | `### Pane-Auftrag`: Kanon „Herdr-Kommandos nur hier und in `### Pane-Ausfuehrung`", einzige deklarierte Ausnahme = Rueckweg-Zeile von pane-start. `#### Abschluss` Punkt 4: `git worktree remove` + `branch -d` nach dem Checkpoint. `herdr agent get {pane}` → `agent_not_found` (Exit 1) = Pane weg (Tick, belegt 2026-09-24) |
| skills/dtb-implement/SKILL.md | Ritual Punkt 11: Zeile `→ Schwelle erreicht (…) — weiter in neuer Session: /dtb:implement {slug} phase {N+1}` — einziges Vorkommen im Kit |
| skills/CLAUDE.md | Skill-Kategorien (Checkpoint = Voll-Guard), Rueckfragen-Defaults-Tabelle (Zeilen Z/A-F), Abgrenzung pane-start in der Autonomie-Regel |
| CLAUDE.md | Skill-Liste: Beschreibungen `workflow-checkpoint`, `workflow-resume`, `pane-start` |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §10 Worktree-Sicht — bleibt unberuehrt (Spec: keine Anzeige in den Uebersichten) |
| dtb-project/project-rules/lessons.md | Prior: L2 Greps auf Zielort ankern, L15 eigenen neuen Text gegen die beseitigte Fehlerklasse pruefen, L67 `/clear` behaelt Prozess, L85 Vergleich gegen merge-base, L86/L87 Herdr |

Verifiziert: Git-Verwaltungsordner eines verlinkten Worktrees = `<haupt>/.git/worktrees/<name>/` (`git rev-parse --git-dir`, absolut), liegt ausserhalb des Arbeitsbaums → nie in `git status`, wird von `git worktree remove`/`prune` mitgeloescht.

---

## Phase 1: Sende-Seite im Checkpoint

### Ziel
`/dtb:workflow-checkpoint` sichert im verlinkten Worktree wahlweise einen Session-Wechsel (Notiz, kein Block) oder das Ende der Arbeit (ein kumulierter Block). Das Notiz-Format hat genau eine Quelle.

### Schritte

#### Schritt 1.1: Notiz-Format als eine Quelle
- **Zweck:** Schreib- und Leseseite brauchen ein festes Format; Felder 1:1 zum Hand-off-Block, damit das Kumulieren mechanisch bleibt
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` — neue Sektion `### Uebergabe-Notiz (Format — die eine Quelle)` unter `## Worktree-Hand-off`, direkt nach `### Hand-off-Block`
- **Input:** Hand-off-Block-Format, Entscheidungen T1-T4 unten
- **Output:**
  - Pfad: `$(git rev-parse --git-dir)/dtb-session-uebergabe.md` (Begruendung: nie committet, keine Ignorier-Regel, verschwindet mit dem Abbau)
  - Kopf (einmalig beim ersten Wechsel): Slug, Branch, Rolle „interaktive Arbeits-Session, kein autonomer Worker", Schreibgrenzen (zentrale Dateien gehoeren nicht der Pane), Rueckweg-Pflicht als Prosa (Block woertlich inkl. Kopfzeile an den Orchestrator — die Kommandozeile selbst steht nur in `workflow-resume`, T5)
  - je Wechsel ein Abschnitt `## Wechsel {YYYY-MM-DD HH:MM}` mit `Orchestrator: {pane-id | —}`, den fuenf Block-Feldern sowie `Uncommittet:` (was die Folge-Session mitcommitten muss) und `Lektion-Kandidaten:` (ausserhalb von `## Lektion-Kandidaten` in plan.md/bug.md)
  - Ende-Marker `## Ende-Block erzeugt {YYYY-MM-DD HH:MM}` (T3)
  - status-neutral: keine `- [ ]`-Checkboxen (wie der Block, DSR §1.1); append-only
  - Kopplungs-Hinweis: Leser ist `dtb:workflow-resume` (Schritt 2a) und die Abbau-Warnung in `dtb:worker` → `#### Abschluss`
  - Frontmatter: `pipeline.produces` des Checkpoints um `dtb-session-uebergabe.md` ergaenzen — gleiche Bezeichnung wie im `consumes` von `workflow-resume` (Schritt 2.1), sonst meldet der `project-health`-Lint den Resume-Eintrag als verwaist

#### Schritt 1.2: Weiche „Wechsel oder Ende?" in der Sende-Seite
- **Zweck:** Entscheid 3b.1 — kein neuer Skill, die Weiche sitzt im bestehenden Worktree-Pfad
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` — Absatz „Sende-Seite" unter `## Worktree-Guard` (⛔-Fence bleibt byte-identisch zur kanonischen Vorlage); `skills/CLAUDE.md` → `### Skill-Kategorien` (im selben Zug, Kopplungs-Regel)
- **Input:** Rueckfragen-Defaults (Textzeile = Vorschlag ohne Commit-Folge)
- **Output:**
  - direkt nach der ⛔-Meldung eine Klarstellungszeile: `↳ Global wird nichts geschrieben — lokal nur die Uebergabe-Notiz (Git-Verwaltungsordner, nie committet)`
  - Kanon `skills/CLAUDE.md` Skill-Kategorien: Zeile Voll-Guard um den benannten Sonderfall ergaenzen — `workflow-checkpoint` schreibt im verlinkten Worktree ausschliesslich die Uebergabe-Notiz im Git-Verwaltungsordner (ausserhalb des Arbeitsbaums, nie global); die Schreibgrenzen-Regel bleibt unberuehrt
  - danach eine Textzeile mit abgeleitetem Vorschlag (T2): `→ Vorschlag: {Wechsel | Ende} ({Grund}) · weiter = uebernehmen · oder „{Alternative}" nennen`
  - Ableitung: `## Progress` im eigenen Change vollstaendig UND kein `review.md` mit `**Gesamt-Verdikt:** REJECTED` → Ende; sonst Wechsel (REJECTED = Nacharbeit offen, plan-review 2026-10-21)
  - Orchestrator-Adresse fuer den Abschnitt: juengster `Orchestrator:`-Wert der Notiz → sonst aus dem Begruessungstext im Verlauf → sonst Textzeile `Orchestrator-Pane? · weiter = ohne (Block manuell tragen)` (T6)
  - **Wechsel:** Notiz anlegen (Kopf + Abschnitt) bzw. Abschnitt anhaengen; Ausgabe: Pfad + Folge-Zeile `→ jetzt: /clear, dann /dtb:workflow-resume`; KEIN Block, nichts an den Orchestrator
  - es wird weiterhin nichts ausserhalb des Git-Verwaltungsordners geschrieben (Schreibgrenze bleibt)

#### Schritt 1.3: Ende-Pfad kumuliert
- **Zweck:** Entscheid 2b — genau EIN Block mit dem Inhalt aller Sessions der Pane
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md` — Sende-Seite, Ende-Zweig
- **Input:** Notiz (alle Abschnitte seit dem letzten Ende-Marker) + aktuelle Session
- **Output:**
  - Block nach `### Hand-off-Block`, Format und Kopfzeile unveraendert; Felder je Feld chronologisch aneinandergereiht, Dubletten bleiben stehen (kein Ermessens-Zusammenlegen — eine doppelte Zeile ist sichtbar, eine faelschlich verschmolzene geht still verloren; plan-review 2026-10-21); `Uncommittet:`-Reste und `Lektion-Kandidaten:` gehen als `- Lektion-Kandidat: …` bzw. `- Uncommittet: …` in `Offene Punkte / Naechste Schritte` (Format bleibt unveraendert, Empfangsseite im Orchestrator unberuehrt)
  - danach Ende-Marker an die Notiz anhaengen (Notiz bleibt als Beleg bis zum Abbau)
  - ohne Notiz: Verhalten exakt wie heute (Block nur aus dem Sitzungskontext)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Format-Sektion `### Uebergabe-Notiz (Format — die eine Quelle)` im Checkpoint
- [ ] Weiche Wechsel/Ende mit abgeleitetem Vorschlag in der Sende-Seite
- [ ] Ende-Pfad kumuliert Notiz + aktuelle Session, setzt Ende-Marker

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^### Uebergabe-Notiz (Format — die eine Quelle)' skills/dtb-workflow-checkpoint/SKILL.md` = 1
- [ ] `grep -c 'dtb-session-uebergabe.md' skills/dtb-workflow-checkpoint/SKILL.md` ≥ 2 (Format + Sende-Seite)
- [ ] ⛔-Fence des Guards unveraendert: `git diff $(git merge-base master HEAD) -- skills/dtb-workflow-checkpoint/SKILL.md` zeigt keine geaenderte Zeile innerhalb des ⛔-Fence (L85: gegen merge-base)
- [ ] `grep -c 'herdr' skills/dtb-workflow-checkpoint/SKILL.md` unveraendert gegenueber merge-base (Checkpoint bleibt Herdr-frei, T5)
- [ ] `grep -c '^### Hand-off-Block (Format — die eine Quelle)' skills/dtb-workflow-checkpoint/SKILL.md` = 1 (Format-Anker unberuehrt)
- [ ] `grep -c '^  produces:.*dtb-session-uebergabe.md' skills/dtb-workflow-checkpoint/SKILL.md` = 1 (Frontmatter; Gegenstueck `consumes` in Resume prueft Phase 2)
- [ ] `grep -c 'Global wird nichts geschrieben' skills/dtb-workflow-checkpoint/SKILL.md` = 1 (Klarstellungszeile)
- [ ] Kanon im selben Zug: `grep -c 'Uebergabe-Notiz' skills/CLAUDE.md` ≥ 1, Treffer innerhalb `### Skill-Kategorien`

#### Manual
- [ ] Trockenlauf im Kopf an PKP-Fall: Notiz-Kopf + Abschnitt decken die vier Verlust-Klassen (L15: eigenen Text gegen die beseitigte Fehlerklasse pruefen — steht etwas nur im Chat, das die Notiz nicht traegt?)

---

## Phase 2: Empfangs-Seite und Ankuendigungen

### Ziel
`/dtb:workflow-resume` stellt nach `/clear` aus der Notiz Rolle, Orchestrator-Adresse, Rueckweg und offene Punkte her; der Wechsel-Weg ist dort angekuendigt, wo der Mensch ihn braucht.

### Schritte

#### Schritt 2.1: Resume Schritt 2a — Notiz lesen
- **Zweck:** Entscheid 3b.2 — Wiederfinden ohne Kopieren
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md` — neuer `### Schritt 2a: Pane-Uebergabe (nur im verlinkten Worktree)` + Report-Abschnitt `## Pane-Uebergabe` in den Vorlagen Fall A/B/C; Frontmatter `consumes` um die Notiz ergaenzen
- **Input:** Notiz-Format (1.1)
- **Output:**
  - Erkennung „verlinkter Worktree" per git-dir ≠ git-common-dir (cd/pwd-normalisiert, eigener Bash-Block — Mechanik-Regel „Bash-Bloecke sind eigene Shells")
  - Notiz vorhanden und juengster Abschnitt ist ein Wechsel → Report-Abschnitt: Rolle + Schreibgrenzen (1 Zeile), Orchestrator, Rueckweg-Zeile, offene Punkte/↷-Zeilen kumuliert seit dem letzten Ende-Marker, `Uncommittet:`-Hinweis
  - im Worktree hat der `**Naechster Befehl:**` aus der Notiz Vorrang vor `WORKFLOW_STATUS.md` → `## Handoff` (Branch-Kopie, veraltet); Artefakt-Ableitung gewinnt weiterhin bei Widerspruch
  - keine Notiz / Haupt-Checkout / juengster Abschnitt ist Ende-Marker → Abschnitt entfaellt still (Randfall 4)
  - Resume bleibt read-only (schreibt die Notiz nie)

#### Schritt 2.2: Adress-Pruefung + Rueckweg-Zeile (Herdr-Ausnahme)
- **Zweck:** Randfall 2 — veraltete Adresse erkennen, bevor der End-Block ins Leere geht
- **Dateien:** `skills/dtb-workflow-resume/SKILL.md` (Schritt 2a); `skills/dtb-worker/SKILL.md` → `### Pane-Auftrag` (Ausnahmen-Liste um `workflow-resume` erweitern)
- **Input:** Tick-Beleg `agent_not_found` (Exit 1)
- **Output:**
  - nur wenn `HERDR_ENV` = `1` und `herdr` im PATH: `herdr agent get {orchestrator-pane}`; Exit 1 → `⚠ Orchestrator-Pane {id} nicht erreichbar` + Textzeile `Neue Orchestrator-Adresse? · weiter = ohne (Block manuell tragen)`; die Antwort gilt fuer diese Session und landet beim naechsten Checkpoint im neuen Abschnitt
  - ohne Herdr: Pruefung still ueberspringen (Sichern/Wiederfinden laufen weiter)
  - Rueckweg-Zeile im Report: `herdr agent prompt {orchestrator-pane} "<der komplette Block>"` — deklarierter Spiegel der Rueckweg-Zeile aus `### Pane-Auftrag`
  - Kopplungs-Hinweis in beiden Richtungen (Resume ↔ Worker-Ausnahmen-Liste)

#### Schritt 2.3: Ankuendigungen (Begruessung + Schwellen-Zeile)
- **Zweck:** Entscheid 3e.2 — die erste Session und der Schwellen-Moment kennen den Weg
- **Dateien:** `skills/dtb-pane-start/SKILL.md` (`## Begruessungstext`, Absatz nach „Rueckweg"); `skills/dtb-implement/SKILL.md` (Ritual Punkt 11)
- **Input:** —
- **Output:**
  - Begruessungstext: Absatz „Session-Wechsel (Kontext voll): `/dtb:workflow-checkpoint` → „Wechsel" → `/clear` → `/dtb:workflow-resume`. Bevorzugt `/clear` statt `/exit` + `claude` (sonst meldet der Ueberwachungs-Tick die Pane kurz als weg)"
  - implement Punkt 11: unter der Schwellen-Zeile eine zweite Zeile `  Wechsel: /dtb:workflow-checkpoint → /clear → /dtb:workflow-resume` — gilt in Haupt-Checkout und Worktree gleich (dort schreibt der Checkpoint `## Handoff`, hier die Notiz), daher keine Worktree-Erkennung in implement noetig (T7)

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Resume Schritt 2a + Report-Abschnitt `## Pane-Uebergabe`
- [ ] Adress-Pruefung + Rueckweg-Zeile als deklarierte Herdr-Ausnahme, in `dtb:worker` registriert
- [ ] Wechsel-Weg im Begruessungstext und in der Schwellen-Zeile

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^### Schritt 2a: Pane-Uebergabe' skills/dtb-workflow-resume/SKILL.md` = 1
- [ ] `grep -c '^## Pane-Uebergabe' skills/dtb-workflow-resume/SKILL.md` = 3 (Vorlagen Fall A/B/C)
- [ ] `grep -c 'dtb-session-uebergabe.md' skills/dtb-workflow-resume/SKILL.md` ≥ 1
- [ ] `grep -c '^  consumes:.*dtb-session-uebergabe.md' skills/dtb-workflow-resume/SKILL.md` = 1 (gleiche Bezeichnung wie `produces` im Checkpoint)
- [ ] `grep -c 'herdr agent get' skills/dtb-workflow-resume/SKILL.md` = 1 und `grep -c 'herdr agent prompt' skills/dtb-workflow-resume/SKILL.md` = 1
- [ ] `grep -c 'workflow-resume' skills/dtb-worker/SKILL.md` ≥ 1, Treffer innerhalb `### Pane-Auftrag` (L2: auf Sektion ankern)
- [ ] `grep -c 'Wechsel: /dtb:workflow-checkpoint' skills/dtb-implement/SKILL.md` = 1
- [ ] `grep -c 'Session-Wechsel' skills/dtb-pane-start/SKILL.md` ≥ 1, Treffer innerhalb `## Begruessungstext`
- [ ] Struktur-Check von pane-start weiter gruen: die drei Anker `^### Pane-Ausfuehrung`, `^### Pane-Auftrag`, `^#### Rueckweg: Ueberwachungs-Tick` je genau 1× in `skills/dtb-worker/SKILL.md`
- [ ] Resume im Haupt-Checkout unveraendert: `git diff $(git merge-base master HEAD) -- skills/dtb-workflow-resume/SKILL.md` entfernt keine Zeile ausser der alten `consumes`-Zeile; alle Hinzufuegungen liegen in Frontmatter-`consumes`, `### Schritt 2a` oder den `## Pane-Uebergabe`-Abschnitten (L85: gegen den merge-base)

---

## Phase 3: Abbau-Warnung, Kanon, Verifikation

### Ziel
Der Abbau loescht keine ungesendete Notiz unbemerkt; Kanon-Texte stimmen mit dem neuen Verhalten ueberein; der Wechsel ist an einer echten pane-start-Pane abgenommen.

### Schritte

#### Schritt 3.1: Abbau-Warnung im Abschluss
- **Zweck:** Randfall 5 / Entscheid 3e.1 — eine Stelle
- **Dateien:** `skills/dtb-worker/SKILL.md` → `#### Abschluss (nach menschlicher Diff-Abnahme)`, Punkt 4 (vor `git worktree remove`)
- **Input:** Notiz-Format (Ende-Marker, T3)
- **Output:** Pruefung `"$(git -C {pfad} rev-parse --git-dir)/dtb-session-uebergabe.md"` existiert UND letzte `## `-Ueberschrift ist kein Ende-Marker → `⚠ Ungesendete Uebergabe-Notiz in {pfad} — erst in der Pane /dtb:workflow-checkpoint → „Ende", dann abbauen`; kein Abbruch, der Mensch entscheidet. Kopplungs-Hinweis auf das Format im Checkpoint
- **Restrisiko (bewusst akzeptiert, plan-review 2026-10-21):** Die Warnung sitzt nur an dieser einen Stelle. Ein Abbau daran vorbei (`git worktree remove`/`prune` von Hand, Ordner loeschen) entfernt eine ungesendete Notiz still mit dem Git-Verwaltungsordner — kein weiterer Schutz; der regulaere Weg bleibt der Ende-Checkpoint vor dem Abbau

#### Schritt 3.2: Kanon und Doku nachziehen
- **Zweck:** Konventionen und Beschreibungen spiegeln das neue Verhalten (Kopplungs-Regel: Spiegel im selben Zug + Grep)
- **Dateien:**
  - `skills/CLAUDE.md`: Rueckfragen-Defaults neue Zeile **G** (Weiche Wechsel/Ende = Textzeile mit abgeleitetem Vorschlag); Abgrenzung pane-start: Verweis auf den Wechsel-Weg
  - `CLAUDE.md`: Session lifecycle (`workflow-checkpoint` Weiche im Worktree, `workflow-resume` liest die Notiz), `pane-start` (Begruessung nennt den Wechsel-Weg)
  - `skills/dtb-pane-start/SKILL.md` `## Rueckweg und Abschluss`: ein Satz zum Wechsel innerhalb der Pane
- **Output:** konsistente Kanon-Texte

#### Schritt 3.3: Verifikation am echten Wechsel
- **Zweck:** Success Criterion „Abnahme am Praxisfall"
- **Dateien:** keine (nur Laufzeit); Befunde → Session-Log via Hand-off
- **Input (Abnahme-Setup, plan-review 2026-10-21):** erst nach Merge + Push + `/dtb:kit-sync` (L39: kit-sync zieht von GitHub, nicht vom lokalen Branch), dann in einem frischen `dtb:pane-start`-Arbeitsplatz mit einem `zz-test-`-Change — keine Handkopie nach `~/.claude/skills/` (vermeidet Lock-Drift). Fehlschlag → Fix-Runde auf neuem Branch
- **Output:** Protokoll: (a) Wechsel schreibt Notiz, `git status` sauber; (b) `/clear` + Resume zeigt Rolle/Adresse/Rueckweg/offene Punkte; (c) zweiter Wechsel haengt an; (d) Ende liefert EINEN Block mit allen Abschnitten + setzt Marker; (e) falsche Adresse → Warnung; (f) Abbau-Warnung greift bei ungesendeter Notiz

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Abbau-Warnung im Worker-Abschluss
- [ ] Kanon/Doku nachgezogen
- [ ] Abnahme-Protokoll des echten Wechsels

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c 'dtb-session-uebergabe.md' skills/dtb-worker/SKILL.md` ≥ 1, Treffer innerhalb `#### Abschluss`
- [ ] Spiegel-Zaehlung Dateiname: `grep -l 'dtb-session-uebergabe.md' skills/dtb-*/SKILL.md` = genau checkpoint, resume, worker (3 Dateien)
- [ ] `grep -c '^| G |' skills/CLAUDE.md` = 1 (neue Rueckfragen-Defaults-Zeile)
- [ ] `grep -c 'Uebergabe-Notiz' CLAUDE.md` ≥ 1
- [ ] `awk '/\r/{n++} END{print n+0}'` = 0 fuer alle geaenderten SKILL.md (L36, keine CRLF eingeschleppt)
- [ ] Haupt-Checkout-Pfad unveraendert: `git diff $(git merge-base master HEAD) -- skills/dtb-workflow-checkpoint/SKILL.md` beruehrt `## Teil 1`/`## Teil 2`/`## Ausfuehrung` nicht

#### Manual
- [ ] Abnahme-Protokoll (a)-(f) am echten Wechsel bestaetigt — nach Merge + Push + kit-sync, in einem frischen `zz-test-`-Arbeitsplatz von `dtb:pane-start`

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| T1 Notiz-Format | frei / 1:1 zu Block-Feldern + 2 Zusatzfelder | 1:1 + `Uncommittet:` + `Lektion-Kandidaten:` | Ende-Pfad kumuliert mechanisch; Zusatzfelder decken Verlust-Klassen 3/4, die der Block nicht kennt — landen im Block unter Offene Punkte (Format unveraendert) |
| T2 Weiche: Form + Vorschlag | Knopf / Textzeile; Default fest / abgeleitet | Textzeile, Vorschlag abgeleitet (Progress vollstaendig und kein REJECTED-`review.md` → Ende, sonst Wechsel) | Rueckfragen-Defaults: Vorschlag ohne Commit-Folge = Textzeile; Fehlwahl ist billig (Checkpoint erneut) |
| T3 Notiz nach dem Ende | loeschen / Ende-Marker | Ende-Marker anhaengen | Herdr bestaetigt die Zustellung nicht; Marker macht „ungesendet" pruefbar (letzte Ueberschrift ≠ Marker) und bleibt bis zum Abbau als Beleg; Weiterarbeit nach dem Ende macht die Notiz wieder „ungesendet" |
| T4 Geltungsbereich der Weiche | nur `pane-{slug}`-Pfade / jeder verlinkte Worktree | jeder verlinkte Worktree | Worker-Traeger rufen den Checkpoint nie auf (Pane-Worker liest nur das Format, Subagent schreibt Report) → keine Pfad-Heuristik noetig; manuelle Worktrees profitieren gleich. Spec im plan-review 2026-10-21 angeglichen — Scope-Ausschluss Worker bleibt faktisch erhalten |
| T5 Ort der Herdr-Kommandos | Checkpoint + Resume / nur Resume | nur Resume (`agent get` + Rueckweg-Zeile) | haelt den Checkpoint Herdr-frei (traeger-neutral wie seine Empfangsseite); die neue Session erhaelt die Rueckweg-Zeile ueber den Resume-Report — eine Ausnahme-Stelle statt zwei |
| T6 Adresse fehlt beim ersten Wechsel (Verlauf verdichtet) | erfragen / aus `herdr agent list` ableiten | erfragen (Textzeile, „weiter" = ohne) | Ableitung braeuchte Herdr im Checkpoint (gegen T5) und ist mehrdeutig bei mehreren Sessions im Haupt-Checkout |
| T7 Ankuendigung in implement | Worktree-Erkennung / universelle Zeile | universelle Zeile | Weg ist in Haupt-Checkout und Worktree derselbe (Checkpoint → `/clear` → Resume); spart einen Bash-Block |
| T8 Fluechtige Adresse in einer Datei | nicht speichern / Momentaufnahme | Momentaufnahme je Abschnitt + Pruefung im Resume | bewusste Abweichung vom Persistenz-Verzicht in pane-start: die Notiz ist kurzlebig (lebt nur bis zum Abbau) und wird beim Lesen validiert — keine Zustandsaussage ohne Pfleger |
| T9 no-loss-check im Worktree-Pfad | laufen lassen / nicht | nicht | bleibt beim Orchestrator-Checkpoint, der den Block empfaengt (dort sieht er den Block im Verlauf); haelt den Wechsel schnell |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [ ] 1.1 Notiz-Format als eine Quelle
- [ ] 1.2 Weiche Wechsel/Ende
- [ ] 1.3 Ende-Pfad kumuliert
- [ ] 2.1 Resume liest Notiz
- [ ] 2.2 Adress-Pruefung + Rueckweg-Zeile
- [ ] 2.3 Ankuendigungen
- [ ] 3.1 Abbau-Warnung
- [ ] 3.2 Kanon und Doku
- [ ] 3.3 Verifikation am echten Wechsel

---

## Umsetzung

Umsetzung mit `/dtb:implement Pane-Session-Neustart` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/pane-session-neustart/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
