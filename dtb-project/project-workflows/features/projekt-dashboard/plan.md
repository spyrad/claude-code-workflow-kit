# Implementierungsplan: Projekt-Dashboard

**Erstellt:** 2026-10-26
**Feature-Spec:** `features/projekt-dashboard/spec.md`
**Geschaetzte Dauer:** ~5–6 h (3 Phasen)
**Status:** Reviewed (plan-review 2026-10-26: REVISE → 6 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Zielform abnehmen: Prototyp mit echten Daten + festes Seitengeruest | ~1.5 h | Geplant |
| Phase 2 | Skill `dtb:project-dashboard`: Quellen, Zaehlregeln, Ableitung, Randfaelle | ~2.5 h | Geplant |
| Phase 3 | Checkpoint-Anbindung, Config, Kit-Doku, Abnahme | ~1.5 h | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` → `## Betroffene Module` (Pfade verifiziert 2026-10-26) + Scan-Nachtrag `README.md`.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-project-dashboard/SKILL.md` | Neubau — existiert noch nicht |
| `skills/dtb-workflow-checkpoint/SKILL.md` | 724 Zeilen; `disable-model-invocation: true`, `allowed-tools: Read, Write, Edit, Grep, Bash`; Voll-Guard bricht im Worktree VOR jedem Schritt ab; Schritt 4 (WORKFLOW_STATUS) → Schritt 5 (Archiv-Hinweis) → Schritt 6 (Bestaetigung, Codeblock-Vorlage); `pipeline.next: [dtb:workflow-resume, dtb:idea-triage]` |
| `skills/dtb-pane-start/SKILL.md` | Vorbild `## Struktur-Check (Kopplungs-Waechter)`: Quelle `~/.claude/skills/…` → Fallback `skills/…`, Anker-Grep zeilenanfangs-verankert nach `tr -d '\r'`, zwei getrennte Fehlerpfade (fehlt = Installation, Anker fehlt = Drift) |
| `skills/dtb-pipeline-graph/SKILL.md` | Vorbild: Claude schreibt eine eigenstaendige HTML-Datei nach `dtb-project/claude-code-workflow-kit.html`; Meldung mit `start …` — nutzt aber CDN + Google Fonts (hier bewusst NICHT uebernommen) |
| `skills/dtb-workflow-next/SKILL.md` | Operative Kopie von DSR §10 (Fettzeile `**Worktree-Stand (operative Kopie von Regel-Datei §10 — rein lesend).**`), wortgleich gespiegelt in `workflow-resume`/`backlog-status` (nicht `workflow-status` — Grounding-Korrektur plan-review); Wartungs-Hinweis direkt nach dem Block nennt die drei Spiegel, Grep-Anker `In Worktrees` |
| `skills/dtb-workflow-status/SKILL.md`, `skills/dtb-backlog-status/SKILL.md` | Read-only-Sichten, nur Referenz/Abgleich — bleiben unveraendert |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Seed (Klasse B); §1–§3 Ableitung + Statusmodell, §6.4 Becken status-neutral, §9 offene Aufgaben (`seit`/⏳), §10 Worktrees |
| `dtb-project/project-workflows/WORKFLOW_STATUS.md` | `## Offene Aufgaben` mit `(seit …)`/⏳ fertig vom Checkpoint geschrieben; `## Abgeschlossene Meilensteine` (5 Zeilen); `## Handoff` mit `**Naechster Befehl:**` |
| `dtb-project/project-workflows/INBOX.md` | Tabelle `# / Datum / Idee / Status`, 17 Datenzeilen; Idee-Zellen sehr lang (Kurztitel noetig) |
| `dtb-project/project-workflows/INBOX-BEFUNDE.md` | Kopf definiert „ungesichtet" (leer / `L1 …` / `Altbestand`) — Zaehlbegriff steht an der Quelle (L45); 76 Datenzeilen |
| `dtb-project/project-workflows/BACKLOG.md` | 4 Standardtabellen mit `#`-Spalte; Status = abgeleitete Anzeige |
| `dtb-project/project-rules/lessons.md` | Tabelle `# / Datum / Context / Problem / Rule / Applies-to`; 93 Zeilen, Eintraege bis #97; `dtb:lesson` warnt ab „> ~150 Zeilen" |
| `dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md` | Session-Logs, `## Session {N} - {HH:MM}` |
| `.gitignore` | `dtb-project/*` mit Negationen fuer workflows/changelog/strategy/rules — `dtb-project/project-dashboard.html` ist damit bereits ignoriert |
| `skills/dtb-project-init/SKILL.md` | Config-Seed Schritt 3 (Bloecke bis `status:`, Erklaerzeilen darunter); Bestaetigung Schritt 5 listet `/dtb:pipeline-graph` |
| `workflow.config.yaml` | Bloecke `paths/repos/idea_triage/worker/parallel/status` — kein `dashboard:` |
| `CLAUDE.md`, `skills/CLAUDE.md`, `README.md` | Skill-Katalog, Output Locations, Tabelle „Skill-Kategorien (Worktree-Verhalten)" (Read-only-Sichten inkl. `pipeline-graph`) |

---

## Phase 1: Zielform abnehmen (Prototyp + Geruest)

### Ziel
Die Seite einmal von Hand mit den ECHTEN Daten dieses Repos bauen und vom Menschen abnehmen
lassen, BEVOR Regeln ausgearbeitet werden (L64). Ergebnis ist das feste Seitengeruest mit
benannten Slots, das ab Phase 2 jeder Lauf nur noch befuellt. Klaert dabei die drei offenen
Spec-Punkte (Kennzahlen-Auswahl, Abgrenzung Sessions/Meilensteine, Kuratierungs-Schwelle).

### Schritte

#### Schritt 1.1: Prototyp mit echten Daten
- **Zweck:** Zielform sichtbar machen (L64) — Gestaltung aus `discovery.md` → „Gewuenschtes Verhalten" (aihero-Stil, nur Systemschriften, dunkel als Standard + Umschalter)
- **Dateien:** `dtb-project/project-dashboard.html` (lokal, ignoriert)
- **Input:** Ist-Stand dieses Repos (WORKFLOW_STATUS, BACKLOG, INBOX, Becken, lessons.md, letzte 5 Session-Logs, `git worktree list`)
- **Output:** vollstaendige Seite mit allen sechs Bereichen; mindestens ein „nicht vorhanden"-Block und ein Warnchip als Muster (Attrappe im Prototyp, L57)

#### Schritt 1.2: Offene Spec-Punkte am Prototyp entscheiden
- **Zweck:** die drei offenen Punkte der Spec am sichtbaren Objekt klaeren statt abstrakt; zwei Spec-Stellen an den Plan angleichen (plan-review Empf. 5)
- **Dateien:** `features/projekt-dashboard/spec.md` (`## Offene Punkte` → in `## Scope` ueberfuehren; Worktree-Zeile unter „Robustheit" und Success Criteria 4 + 6 angleichen), dieser Plan (`## Technische Entscheidungen`)
- **Input:** Prototyp 1.1 + Vorschlaege: Kennzahlen = Ideen offen · Befunde ungesichtet · Lektionen · aktive Changes · offene Aufgaben · Worktrees; Sessions und Meilensteine als zwei Spalten eines Blocks „Zuletzt gemacht"; Kuratierungs-Signal ab derselben Schwelle wie `dtb:lesson` (> ~150 Zeilen, eine Definition — L45)
- **Output:** Spec ohne offene Punkte; Entscheidungen im Plan; **Spec-Angleichung:** (a) Worktree — Checkpoint-Hinweiszeile entfaellt (T7: Voll-Guard bricht vorher ab), es bleibt nur das Banner auf Abruf — in „Robustheit" und Kriterium 6; (b) Kriterium 4 „keine externe Anfrage" → „die Seite laedt keine Ressource von einer externen Adresse (kein `src`/`href` auf `http(s)://`, kein `@import`, kein `url(http…)`)" — per Grep pruefbar statt Netzwerk-Mitschnitt

#### Schritt 1.3: Seitengeruest mit Slots extrahieren
- **Zweck:** Stabiles Aussehen ueber Laeufe — Claude fuellt nur Slots, Struktur/CSS/Umschalter sind fix
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md` (neu — nur Frontmatter-Rumpf + Sektion `## Seitengeruest`)
- **Input:** abgenommener Prototyp
- **Output:** Geruest als EIN Codeblock (wird pro Lauf per Bash woertlich in die Ausgabedatei kopiert — T1) mit benannten Slots, jeder Slot genau einmal im Geruest, (`{{KENNZAHLEN}}`, `{{STAND}}`, `{{BACKLOG}}`, `{{ZULETZT}}`, `{{INBOX}}`, `{{LEKTIONEN}}`, `{{BANNER}}`, `{{STAND_DATUM}}`), Baustein-Vorlagen (Karte, Chip, Warnchip, Leerzustand, „nicht vorhanden", einklappbare Liste)

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Abgenommener Prototyp `dtb-project/project-dashboard.html`
- [ ] Spec-Offene-Punkte entschieden
- [ ] `## Seitengeruest` in `skills/dtb-project-dashboard/SKILL.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `test -f dtb-project/project-dashboard.html && git check-ignore -q dtb-project/project-dashboard.html` (existiert UND ignoriert — L11)
- [ ] Keine externe Ressource im Prototyp und im Geruest (nur was geladen wird, nicht jedes `http` im Text — L8): `grep -cE "(src|href)=[\"']https?://|@import|url\([\"']?https?://" dtb-project/project-dashboard.html` = 0 und dieselbe Pruefung auf den Codeblock unter `^## Seitengeruest` = 0
- [ ] Dunkel als Standard: Geruest-Codeblock enthaelt `data-theme="dark"` am Wurzelelement; Umschalter-Skript enthaelt `try` (Speicher-Zugriff abgesichert)
- [ ] Alle acht Slots im Geruest: `grep -c '{{[A-Z_]*}}'` ueber den Codeblock ≥ 8
- [ ] `spec.md` → `## Offene Punkte` traegt nur noch „— keine —"
- [ ] Spec angeglichen: `grep -c 'Dashboard-Update übersprungen' spec.md` = 0 (Checkpoint-Hinweiszeile weg) UND `grep -c 'externen Adresse' spec.md` ≥ 1 (Kriterium 4 neu gefasst)

#### Manual
- [ ] Mensch nimmt den Prototyp ab: dunkel und hell (Umschalter, Wahl nach Neuladen erhalten), Kennzahlen-Leiste, Lesbarkeit, Gesamteindruck „aihero-Stil"

---

## Phase 2: Skill `dtb:project-dashboard` (Ablauf)

### Ziel
Der Skill erzeugt die Seite aus jedem Projektstand reproduzierbar: Quellen lesen, nach
festen Regeln zaehlen und ableiten, Randfaelle sichtbar machen, Datei schreiben, auf
Abruf im Browser oeffnen.

### Schritte

#### Schritt 2.1: Frontmatter, Config und Quellen
- **Zweck:** Rahmen des Skills
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md`
- **Input:** `skills/CLAUDE.md` → Frontmatter-Pflichtfelder; Entscheidungen unten
- **Output:** Frontmatter (`stage: monitoring`, `after: [dtb:workflow-checkpoint]`, `next: null`, `consumes:` alle sieben Quellen + `workflow.config.yaml` + `project-rules/DERIVED_STATE_RULES.md`, `produces: [project-dashboard.html]`, `allowed-tools: Read, Glob, Grep, Bash, Write, Edit` — L44/L75); Schritt „Config laden" (Pfade + `dashboard:`-Block, Fallbacks); Worktree-Erkennung (Guard-Pruefung aus `skills/CLAUDE.md`) → nur Banner-Slot, kein Abbruch; Quell-Tabelle (Datei → Bereich)

#### Schritt 2.2: Zaehl- und Ableitungsregeln
- **Zweck:** dieselben Zahlen wie die Terminal-Sichten (Spec-Kriterium 2)
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md`
- **Input:** DSR §1–§3, §6.4, §9; Becken-Kopf (Definition „ungesichtet"); `dtb:workflow-next` Worktree-Block
- **Output:** je Kennzahl genau eine Zaehlregel (Datenzeilen, nie Kopf/Trennzeile — L17): Ideen = INBOX-Status `Offen`/`In Arbeit`; Befunde = „ungesichtet" laut Becken-Kopf (Verweis, keine eigene Definition — L45); Lektionen = Datenzeilen + Zeilenzahl gegen 150; Changes = `features/*/` mit abgeleitetem Status (kompakte operative Kopie DSR §1/§3 mit Wartungs-Hinweis + Grep-Anker — L82); offene Aufgaben = Zeilen unter `## Offene Aufgaben` inkl. ⏳ (keine eigene Ableitung, Checkpoint liefert sie fertig); Worktrees = Verweis auf `dtb:workflow-next` Worktree-Stand (Entscheidung T3) mit Struktur-Check nach Muster `pane-start` → `worker`: Quelle zuerst `~/.claude/skills/dtb-workflow-next/SKILL.md`, sonst `skills/dtb-workflow-next/SKILL.md`; Anker nach `tr -d '\r'` zeilenanfangs-verankert `^\*\*Worktree-Stand (operative Kopie`; zwei Fehlerpfade (Datei fehlt = Installationsproblem, Anker fehlt = Drift) → Worktree-Block zeigt „nicht vorhanden"/Warnchip, kein Abbruch; Konfliktregel: Artefakt gewinnt, Anzeige ≠ Ableitung → Warnchip

#### Schritt 2.3: Randfaelle, Ausgabe, Oeffnen
- **Zweck:** Robustheit + Ablage laut Spec
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md`
- **Input:** Spec → „Robustheit"
- **Output:** Regeln fuer fehlende Quelle („nicht vorhanden"), defekte Zeile (Warnchip, weiterrechnen), kein aktives Feature (Leerzustand + `**Naechster Befehl:**` aus Handoff), lange Listen (neueste 10 + einklappbar), Kurztitel (erster Satz bzw. Fettdruck der Idee-Zelle, gekappt), HTML-Escaping aller Quelltexte; **Link-Regel:** Quelltext wird nie zu Links (auch keine Markdown-Links aus INBOX/Logs) — Links entstehen nur aus Pfaden, die der Skill selbst bildet; Erzeugen in zwei Takten (T1): (1) Codeblock `## Seitengeruest` per Bash woertlich nach `dtb-project/project-dashboard.html` kopieren (`mkdir -p`, Extraktion zwischen den Codeblock-Zaeunen der Sektion, `tr -d '\r'`), (2) jeden Slot per Edit durch seinen Inhalt ersetzen — CSS/Skript laufen nie durch die Ausgabe; `git check-ignore` → nicht ignoriert ⇒ einmalig Ausschluss-Zeile vorschlagen, nie selbst schreiben; Kein-Git ⇒ Hinweis statt Pruefung (L11); Oeffnen per Plattform (`start ""` / `open` / `xdg-open`) nur im Abruf-Modus; Modus-Schalter „ohne Browser" fuer den Checkpoint-Aufruf; Bestaetigungszeile

#### Schritt 2.4: Probelauf + Abgleich
- **Zweck:** Spec-Kriterien 2 und 3 belegen, gegen die Repo-Fassung (L74)
- **Dateien:** `dtb-project/project-dashboard.html` (Ausgabe); Belege in diesem Plan unter `## Probelauf-Belege` (status-neutral, L20)
- **Input:** Skill aus 2.1–2.3, `skills/dtb-project-dashboard/SKILL.md` direkt (nicht `~/.claude/`)
- **Output:** Probelauf in diesem Worktree (Banner sichtbar); Zahlen-Abgleich gegen `/dtb:workflow-next` + `/dtb:backlog-status`; Attrappe `features/zz-test-dashboard/` (nur im eigenen Ordner, keine zentrale Datei — Schreibgrenzen-Regel): `plan.md` mit 100 % Progress, `spec.md` mit abweichender `**Status:**`-Anzeige (z. B. `In Arbeit`) und Titel `<script>alert(1)</script> & <b>fett</b>` → erwartet: „Fertig zum Testen" + Warnchip, Titel als reiner Text; danach Attrappe entfernen (L57); **Testbett-Lauf** (vorgezogen aus 3.4, plan-review Empf. 3): Ablauf aus der Repo-Fassung (L74) gegen `C:/Users/SpyraD/Desktop/Projekte/dtb-assistant` (kein Git, kein Becken, keine `lessons.md`) → Seite vollstaendig, „nicht vorhanden"-Bloecke, Kein-Git-Hinweis; einzige Schreibstelle dort ist `dtb-project/project-dashboard.html`

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Vollstaendiger Skill `skills/dtb-project-dashboard/SKILL.md`
- [ ] `## Probelauf-Belege` mit Abgleich und Attrappen-Ergebnis

### Checkpoint-Kriterien

#### Automated
- [ ] Frontmatter vollstaendig: `name: dtb:project-dashboard`, `stage: monitoring`, `produces:` enthaelt `project-dashboard.html`, `allowed-tools` enthaelt `Bash`, `Write` und `Edit` (Grep je Feld im Frontmatter-Block)
- [ ] Probelauf-Ausgabe vollstaendig befuellt: `grep -c '{{[A-Z_]*}}' dtb-project/project-dashboard.html` = 0
- [ ] Geruest woertlich uebernommen: der `<style>`-Block der Ausgabe ist identisch mit dem des Geruests (Extraktion beider Bloecke + `diff` ohne Ausgabe)
- [ ] Struktur-Anker vorhanden (zeilenanfangs-verankert nach `tr -d '\r'`): `^## Seitengeruest`, `^## Ablauf` in `skills/dtb-project-dashboard/SKILL.md`
- [ ] Wartungs-Hinweis an der operativen DSR-Kopie: Grep auf `Wartungs-Hinweis (Format-Kopplung)` in der Ableitungs-Sektion ≥ 1
- [ ] Worktree-Verweis traegt: Anker-String `Worktree-Stand (operative Kopie` steht im Dashboard-Skill (Struktur-Check) UND `tr -d '\r' < skills/dtb-workflow-next/SKILL.md | grep -c '^\*\*Worktree-Stand (operative Kopie'` = 1
- [ ] Escaping-Probe: Probelauf-Ausgabe mit Attrappe enthaelt `&lt;script&gt;alert(1)&lt;/script&gt;` und KEIN `<script>alert(1)` (Grep auf die Ausgabedatei, vor dem Entfernen der Attrappe festgehalten in `## Probelauf-Belege`)
- [ ] Zentrale Dateien unberuehrt: `git diff --name-only $(git merge-base master HEAD) -- dtb-project/project-workflows/BACKLOG.md dtb-project/project-workflows/INBOX.md dtb-project/project-workflows/WORKFLOW_STATUS.md` leer (L85)
- [ ] Attrappe entfernt: `test ! -e dtb-project/project-workflows/features/zz-test-dashboard`
- [ ] `## Probelauf-Belege` in `plan.md` vorhanden und nicht leer
- [ ] Datei ≤ 500 Zeilen: `wc -l skills/dtb-project-dashboard/SKILL.md`

#### Manual
- [ ] Mensch bestaetigt: Zahlen der Seite = Zahlen aus `workflow-next`/`backlog-status`; Worktree-Banner, Warnchip und reiner-Text-Titel der Attrappe sichtbar
- [ ] Mensch bestaetigt die Testbett-Seite (`dtb-assistant`): vollstaendig, Luecken als „nicht vorhanden", kein Abbruch

---

## Phase 3: Checkpoint-Anbindung, Config, Kit-Doku

### Ziel
Der Checkpoint aktualisiert die Seite am Session-Ende ueber einen Verweis (keine Kopie),
die Config steuert das, und die Kit-Doku kennt den neuen Skill.

### Schritte

#### Schritt 3.1: Checkpoint-Schritt „Dashboard aktualisieren"
- **Zweck:** Automatische Aktualisierung (Spec), abschaltbar
- **Dateien:** `skills/dtb-workflow-checkpoint/SKILL.md`
- **Input:** Muster `dtb:pane-start` → `## Struktur-Check`; Anker aus 2.x
- **Output:** neuer `### Schritt 4b: Dashboard aktualisieren` zwischen Schritt 4 und 5: `dashboard.bei_checkpoint` lesen (fehlt = `true`); `false` → still ueberspringen; sonst Struktur-Check auf `dtb:project-dashboard` (Quelle `~/.claude/skills/…` → Fallback `skills/…`, Anker `^## Seitengeruest` + `^## Ablauf`, zwei Fehlerpfade — Fehler hier blockiert den Checkpoint NIE, nur Warnzeile — L89: Check vor der ersten Nutzung) → Ablauf im Modus „ohne Browser" ausfuehren; Schritt-6-Vorlage um `Dashboard: dtb-project/project-dashboard.html` erweitern; Frontmatter `produces` += `project-dashboard.html`, `next` += `dtb:project-dashboard` (Gegenkante zu `after`, reziprok); Kopplungs-Hinweis im Dashboard-Skill an beiden Ankern („Leser: workflow-checkpoint Schritt 4b")

#### Schritt 3.2: Config-Block + project-init
- **Zweck:** Schalter verfuegbar, Bestandsprojekte ohne Key gueltig
- **Dateien:** `workflow.config.yaml`, `skills/dtb-project-init/SKILL.md`
- **Input:** Muster `status:`-Block samt Erklaerzeile
- **Output:** `dashboard:` + `bei_checkpoint: true  # dtb:workflow-checkpoint Schritt 4b — Dashboard am Session-Ende aktualisieren` in Config und Seed; Erklaerzeile „Optional (Default true bei fehlendem Key)"; Bestaetigung Schritt 5 += `/dtb:project-dashboard — Projektstand als HTML-Seite`

#### Schritt 3.3: Kit-Doku + Repo-weiter Namens-Sweep
- **Zweck:** Katalog vollstaendig (Spec-Kriterium 9); L3
- **Dateien:** `CLAUDE.md` (Skill Categories + Output Locations), `skills/CLAUDE.md` (Skill-Kategorien: Read-only-Sichten += `project-dashboard`), `README.md` (Skill-Liste), `skills/dtb-workflow-next/SKILL.md` (Leser-Eintrag: eine eigene Blockquote-Zeile direkt nach dem bestehenden Wartungs-Hinweis zum Worktree-Stand — „Leser per Verweis: `dtb:project-dashboard` (Struktur-Check auf die Fettzeile) — Anker hier nicht umbenennen, ohne den Check dort mitzuziehen"; der wortgleiche Block der drei Sichten bleibt unangetastet)
- **Input:** Grep `pipeline-graph` als Nachbar-Fundstellen
- **Output:** neuer Skill an jeder Stelle, an der `pipeline-graph` als Sicht/HTML-Ausgabe gefuehrt wird; Output Location `dtb-project/project-dashboard.html` (lokal, unversioniert)

#### Schritt 3.4: Orchestrator-Abnahme (nach Merge, Push, kit-sync)
- **Zweck:** Spec-Kriterien 1 und 5 im echten Lauf mit der installierten Kopie
- **Wer/Wo:** Orchestrator-Session im Haupt-Checkout — NICHT in der Pane; die Pane endet vorher mit dem Hand-off (Progress-Flip 3.4 und SHA dort)
- **Dateien:** Belege unter `## Probelauf-Belege` (L20)
- **Input:** gemergter + gepushter Stand, danach `/dtb:kit-sync sync` (L39: erst pushen, dann syncen)
- **Output:** (a) `/dtb:workflow-checkpoint` aktualisiert die Seite ohne Browser + Pfad-Zeile; (b) mit `bei_checkpoint: false` entfaellt der Schritt still; (c) `/dtb:project-dashboard` aus der installierten Kopie oeffnet die Seite im Browser

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Checkpoint Schritt 4b + Bestaetigungszeile + Frontmatter
- [ ] Config + Seed + Kit-Doku
- [ ] Abnahme-Belege

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^### Schritt 4b: Dashboard aktualisieren' skills/dtb-workflow-checkpoint/SKILL.md` = 1, und er steht zwischen `^### Schritt 4:` und `^### Schritt 5:` (Zeilennummern-Vergleich)
- [ ] Keine Geruest-Kopie im Checkpoint: Grep auf `{{KENNZAHLEN}}` in `skills/dtb-workflow-checkpoint/SKILL.md` = 0 (Wirkstelle = Datei, Slot-Name kommt dort nur bei einer Kopie vor — L8)
- [ ] Kante reziprok: Checkpoint-Frontmatter `next:` enthaelt `dtb:project-dashboard` UND Dashboard-Frontmatter `after:` enthaelt `dtb:workflow-checkpoint`
- [ ] `produces:` im Checkpoint-Frontmatter enthaelt `project-dashboard.html`
- [ ] `grep -c '^dashboard:' workflow.config.yaml` = 1 und Seed in `skills/dtb-project-init/SKILL.md` traegt `bei_checkpoint:` (Grep im Schritt-3-Codeblock)
- [ ] Doku: `grep -l 'project-dashboard' CLAUDE.md skills/CLAUDE.md README.md` liefert alle drei
- [ ] Leser-Eintrag: `grep -c 'Leser per Verweis: .dtb:project-dashboard.' skills/dtb-workflow-next/SKILL.md` = 1; Worktree-Block der drei Sichten weiter wortgleich (Extraktion ab Fettzeile bis Wartungs-Hinweis in resume/next/backlog-status + `diff` ohne Ausgabe)

#### Manual
- [ ] Orchestrator-Abnahme 3.4 (a)–(c) im Haupt-Checkout bestanden (nach kit-sync)

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| T1 Erzeugung | A Claude fuellt Geruest · B Skript · C Daten-JS + festes Geruest | **A, zweitaktig:** Geruest per Bash woertlich kopieren, Slots per Edit fuellen | Discovery 2026-10-26: Kit bleibt reines Markdown, kit-sync unveraendert. plan-review 2026-10-26 (Empf. 1): CSS/Skript nie durch die Ausgabe — Kosten skalieren mit den Daten, nicht mit dem Design; Aussehen per Konstruktion stabil. C bleibt Ausbaustufe |
| T2 Statusableitung | Verweis auf DSR-Seed · kompakte operative Kopie inline | **Operative Kopie** (§1/§3, wenige Zeilen) mit Wartungs-Hinweis | L82: Seed erreicht Bestandsprojekte nicht; Muster wie Checkpoint Schritt 2 |
| T3 Worktree-Block | vierter wortgleicher Spiegel · Verweis auf `dtb:workflow-next` mit Struktur-Check | **Verweis** | Drei Spiegel existieren schon; ein vierter erhoeht Mitzieh-Last; Dashboard braucht nur die Daten, nicht das Terminal-Format; gleiche Zustaende (laeuft/gemergt/verwaist) wie die Terminal-Sichten. Restrisiko Fettzeilen-Anker abgefedert (plan-review 2026-10-26): Anker woertlich in 2.2, Leser-Eintrag in `workflow-next` (3.3), Automated-Grep in Phase 2 und 3 |
| T4 Checkpoint → Skill | Geruest kopieren · Verweis + Struktur-Check | **Verweis + Struktur-Check** | Eine Quelle; Muster `pane-start`; L9: gesperrter Skill darf ungesperrten im Ablauf anstossen |
| T5 Fehler im Dashboard-Schritt | Checkpoint abbrechen · Warnzeile, weiter | **Warnzeile** | Dashboard ist Komfort; Log + Status duerfen nie daran scheitern |
| T6 `disable-model-invocation` | true · weglassen | **weglassen** (modell-aufrufbar) | Rein lesende Sicht wie `workflow-status`; „zeig mir das Dashboard" soll greifen |
| T7 Worktree-Hinweiszeile im Checkpoint | eigene Zeile · entfaellt | **entfaellt** | Voll-Guard bricht im Worktree VOR Schritt 1 ab — Schritt 4b ist dort strukturell unerreichbar; Spec-Kriterium 6 wird in 1.2 entsprechend angepasst (Worktree-Teil nur noch: Banner auf Abruf) |
| T8 Kuratierungs-Schwelle | eigene Quote · Schwelle von `dtb:lesson` | **dieselbe** (> ~150 Zeilen) — entschieden 2026-10-27 am Prototyp (1.2) | Eine Definition statt zwei (L45) |
| T9 Kennzahlen-Leiste | Minimum (5) · sechs inkl. Worktrees | **sechs**, feste Reihenfolge: Ideen offen · Befunde ungesichtet · Lektionen (+ Zeilen/150) · aktive Changes · offene Aufgaben (+ Anzahl ⏳) · Worktrees — entschieden 2026-10-27 (1.2) | Prototyp: sechs Spalten passen in eine Zeile, Worktrees sind ab der Pane-Schiene Alltag |
| T10 „Zuletzt gemacht" | nur Sessions · nur Meilensteine · beide nebeneinander | **beide nebeneinander** (zwei Spalten) — entschieden 2026-10-27 (1.2) | Sessions = was lief, Meilensteine = was fertig wurde; Session-Kopf traegt nur die Uhrzeit (`## Session N - HH:MM`) → Kurztext = erster Punkt unter der Session, gekappt |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Prototyp mit echten Daten — `94b9fd9`
- [x] 1.2 Offene Spec-Punkte entscheiden — `94b9fd9`
- [x] 1.3 Seitengeruest mit Slots — `94b9fd9`
- [x] 2.1 Frontmatter, Config, Quellen — `a5cdaf3`
- [x] 2.2 Zaehl- und Ableitungsregeln — `a5cdaf3`
- [x] 2.3 Randfaelle, Ausgabe, Oeffnen — `a5cdaf3`
- [x] 2.4 Probelauf + Abgleich — `a5cdaf3`
- [x] 3.1 Checkpoint Schritt 4b
- [x] 3.2 Config + project-init
- [x] 3.3 Kit-Doku + Namens-Sweep
- [ ] 3.4 Abnahme

---

## Umsetzung

Umsetzung mit `/dtb:implement Projekt-Dashboard` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/projekt-dashboard/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

**Worktree-Hinweis:** Phasen 1–3.3 laufen in diesem Worktree (`feature/projekt-dashboard`);
3.4 ist die Orchestrator-Abnahme im Haupt-Checkout nach Merge, Push und kit-sync — der Hand-off nennt sie als offenen Punkt. Das Testbett `dtb-assistant` laeuft schon in 2.4.

---

## Probelauf-Belege

> Status-neutral (L20). Probelauf 2.4 am 2026-10-27, Ablauf aus der Repo-Fassung `skills/dtb-project-dashboard/SKILL.md` (L74).

**Worktree-Lauf** (`feature/projekt-dashboard`, mit Attrappe `features/zz-test-dashboard/`):
- Geruest per Bash kopiert: 8 Slots; nach 8 Edits 0 Slots; `<style>`-Block identisch zum Geruest (`diff` leer); externe Ressourcen 0
- Escaping-Probe (vor dem Entfernen der Attrappe): `&lt;script&gt;alert(1)&lt;/script&gt;` 1 Treffer, `<script>alert(1)` 0 Treffer
- Attrappe: Spalte „Fertig zum Testen" 2/2 + Warnchip „Anzeige in spec.md: In Arbeit"; projekt-dashboard: „In Arbeit" 6/11 + Warnchip „Anzeige in spec.md: Spezifiziert"; Worktree-Banner gesetzt
- Abgleich (unabhaengiger Helfer, Regeln aus `workflow-next`/`backlog-status`, ohne Blick auf die Seite): Status + X/Y beider Changes gleich; Worktree-Zeile `projekt-dashboard  interaktiv (pane)  feature/projekt-dashboard  +1 Commits, zuletzt 2026-10-27  4 uncommitted  Progress 6/11` gleich; Ideen 17, Befunde 76, offene Aufgaben 6 (0 ⏳ in der Datei), Naechster Befehl `/dtb:workflow-next` gleich
- Abweichung ohne Handlungsbedarf: `workflow-next` meldet zusaetzlich den Plan-Kopf der Attrappe (`Entwurf` bei 2/2, Regel-Datei §7.3) — Plan-Kopf ist nicht Gegenstand des Dashboards
- Kosten: Seite 35 KB, davon ~25 KB Listen (17 Ideen + 76 Befunde); die Slot-Edits sind der Hauptaufwand

**Testbett-Lauf** (`dtb-assistant`, kein Git, Altbestand):
- Einzige Schreibstelle `dtb-project/project-dashboard.html`; Geruest aus der Repo-Fassung (keine installierte Kopie, kein `skills/` im Projekt)
- 0 Slots offen, externe Ressourcen 0, kein Banner (`DURCHLASS-NOGIT`)
- „nicht vorhanden": Befund-Becken, Lektionen (Kennzahlen zeigen `—`); Worktree-Karte entfaellt (kein Git)
- 41 flache Alt-Dateien, 0 Change-Ordner → Leerzustand + Warnchip „41 Alt-Dateien ohne Change-Ordner — Migration: /dtb:migrate-change-folders"
- Session-Koepfe mit Titel/Gedankenstrich und Aufgaben im Altformat korrekt dargestellt
- Quelle `WORKFLOW_STATUS.md` traegt ein Passwort im Klartext; im Probelauf ausgelassen — Schutz gehoert an die Quelle (INBOX #110)

**Nachschaerfungen aus dem Probelauf** (in `SKILL.md` eingearbeitet): Read vor den Slot-Edits; Kurztitel-Fettdruck nur am Zellanfang; Session-Kopf = ganze Kopfzeile, Kurztext = erste Nicht-Ueberschrift-Zeile; Altformat offener Aufgaben; fehlende Quelle → Kennzahl `—`; flache Alt-Dateien → Migrations-Warnchip

---

## Lektion-Kandidaten

- „Ein Schritt hinter dem Voll-Guard eines Skills ist im Worktree strukturell unerreichbar — fuer solche Schritte kein eigenes Worktree-Verhalten spezifizieren, sondern den Guard als Antwort nennen" (vorgemerkt 2026-10-26)
- „Ein Skill, der eine Datei per Bash erzeugt und danach per Edit fuellt, muss den Read-Schritt dazwischen ausdruecklich nennen — Edit verweigert ungelesene Dateien; im Probelauf faellt das nur auf, wenn die Datei vorher noch nicht gelesen war" (vorgemerkt 2026-10-27)

---

**Erstellt mit:** `/dtb:impl-plan`
