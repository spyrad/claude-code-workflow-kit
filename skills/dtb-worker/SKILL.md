---
name: dtb:worker
description: >-
  Use when: "worker", "autonome Schiene", "was kann autonom laufen",
  "Task automatisch erledigen", "Worker starten", "worker liste".
  View mode (no argument) scans INBOX and open tasks and judges per entry
  whether an autonomous background worker could complete it without the
  full discovery-spec-plan chain. Run mode (slug or "liste", only after
  explicit approval) executes entries as background workers in isolated
  worktrees, checking off `## Schritte` in the task's own change folder
  and writing a full worker-report.md per task. Never commits or pushes,
  never touches status displays or central files.
disable-model-invocation: true
argument-hint: "[slug | liste]"
allowed-tools: Read, Glob, Grep, Bash, Agent
pipeline:
  stage: execution
  after: [dtb:task]
  next: [dtb:workflow-checkpoint]
  consumes: [INBOX.md, features/*/task.md, workflow.config.yaml]
  produces: [features/*/worker-report.md, features/*/task.md]
---

# Autonomer Worker (Erkennung + Ausfuehrung)

Du bist die autonome Schiene des Kits. **Modus 1** (ohne Argument) zeigt, welche offenen
Eintraege ein Hintergrund-Worker ohne die volle Kette (Discovery → Spec → Plan) erledigen
koennte. **Modus 2** (mit Argument, nur nach expliziter Freigabe) fuehrt sie aus.
Autonomie gilt ausschliesslich **zwischen Freigabe und Abnahme** — das Modell entscheidet
nie selbst, DASS gearbeitet wird (Kanon: `skills/CLAUDE.md` → Autonomie-Regel).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

Deckelung aus dem `worker:`-Block lesen:

```yaml
worker:
  max_attempts: 3   # Versuche pro Task
  max_minutes: 30   # Minuten pro Task (Anweisungs-Ebene, siehe Modus 2)
```

Fehlt der Block oder einzelne Schluessel → Defaults `3` / `30` still verwenden (kein Abbruch).

## Modus-Weiche

- **Kein Argument** → Modus 1: Erkennungs-Sicht (read-only, schreibt nichts)
- **Argument `{slug}` oder `liste`** → Modus 2: Ausfuehrung. Voraussetzung ist eine
  Freigabe aus der Sicht dieser Session (Schritt 5) — fehlt sie, zuerst Modus 1 zeigen

---

## Modus 1: Erkennungs-Sicht (read-only)

### Schritt 1: Quellen scannen

1. `{config.paths.workflows}/INBOX.md` — Eintraege mit Status `Offen` oder `Ausgearbeitet`
2. `{config.paths.workflows}/features/*/task.md` mit Status `Offen` und einer
   `## Schritte`-Sektion (`archive/` ausgenommen)

Bugs (`bug.md`) und Features mit Spec/Plan sind KEIN Worker-Material — sie gehoeren in
die bestehenden Lanes.

### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)

> Schwester-Raster ueber dieselbe Quellenliste (z.B. Aufwand×Nutzen, INBOX #33) docken hier als eigene Unterueberschrift an.

Vier Kriterien, jedes je Eintrag mit ja/nein bewertet:

1. **Zielzustand mechanisch verifizierbar** — Test, Grep, Build oder Datei-Existenz
   entscheidet ueber Erfolg, kein menschliches Urteil
2. **Scope geschlossen** — keine offenen Design- oder Zuschnitts-Entscheidungen
3. **Keine Fremdwirkung** — keine Spiegel-Kopplung, keine Aenderungen an Dateien
   ausserhalb des Eintrags-Gegenstands
4. **Umkehrbar** — Aenderungen ohne Datenverlust rueckholbar

**Urteil:** alle vier erfuellt → `ja`. Genau eine Luecke, die sich mit EINER kurzen
Nutzer-Antwort schliessen laesst (typisch: eine offene Scope-Entscheidung) → `teilweise`
+ **Vorab-Frage** formulieren. Sonst → `nein`. Je Eintrag eine 1-Satz-Begruendung.

### Schritt 3: Abhaengigkeiten & Reihenfolge

- Abhaengigkeiten zwischen tauglichen Eintraegen benennen (`X vor Y` + Grund)
- Empfohlene Bearbeitungs-Reihenfolge ableiten
- **Parallel-Kandidaten** markieren: nur Eintraege, die unabhaengig sind UND disjunkte
  Dateien anfassen

### Schritt 4: Sicht ausgeben

```
# Worker-Sicht: {N} Eintraege geprueft — {J} ja / {T} teilweise / {X} nein

| Eintrag | Urteil | Begruendung | Vorab-Frage |
|---------|--------|-------------|-------------|
| {INBOX-# bzw. slug} | ja/teilweise/nein | {1 Satz} | {Frage oder —} |

Reihenfolge-Empfehlung: {geordnete Liste, Parallel-Kandidaten mit ∥ markiert}
{Je tauglicher Idee ohne Change-Ordner: "→ zuerst /dtb:task {N} — Worker brauchen definierte Schritte"}

Freigabe? ({slug} | liste | nein)
```

**Leerfall (kein Eintrag `ja` oder `teilweise`):** melden UND je Eintrag in einer Zeile
begruenden, was zur Tauglichkeit fehlt — die Nebenspalte fuer alle. Keine Freigabe-Frage.

### Schritt 5: Freigabe-Dialog

Die Freigabe ist die Governance-Klammer vorn — ohne sie startet nichts.

1. **Vorab-Fragen zuerst:** Alle offenen Vorab-Fragen der gewaehlten Eintraege stellen
   und beantworten lassen, BEVOR irgendetwas startet. Ein `teilweise`-Eintrag mit
   unbeantworteter Frage bleibt draussen (beim Listen-Lauf: ueberspringen, am Ende
   gesammelt melden)
2. **Umfang bestaetigen:** einzelner Eintrag ODER Liste in der vorgeschlagenen
   Reihenfolge. Bei Liste anzeigen, welche Teile parallel laufen (∥-Markierung aus
   Schritt 3)
2b. **Unerreichbare Schritte ausklammern:** Schritte, die Commits/Pushes verlangen
   oder ausserhalb der Worker-Reichweite liegen (z.B. andere Maschine), werden bei
   der Freigabe sichtbar als „beim Menschen" markiert — sie zaehlen nicht gegen den
   Worker-Ausgang
3. **Stoppweg nennen (Pflichtzeile im Dialog):**
   ```
   Laufende Worker sind Background-Tasks dieser Session — Auflistung und Abbruch
   ueber die Task-Verwaltung, jederzeit. Abgebrochene/halbfertige Ergebnisse bleiben
   als Diff im jeweiligen Worktree liegen.
   ```
4. **Explizite Bestaetigung** („Start") ist die Startbedingung. Danach → Modus 2.

---

## Modus 2: Ausfuehrung (nur nach Freigabe aus Schritt 5)

### Traeger-Weiche (Subagent | Pane)

Die Ausfuehrung hat zwei Traeger; die Wahl faellt im Freigabe-Dialog (Schritt 5), Default
ist der Subagent:

- **`subagent` (Default):** Background-Subagent im Worktree — blind, Ergebnis als
  `worker-report.md` (Schritte 6-9, unveraendertes Verhalten)
- **`pane` (nur auf explizite Wahl):** Echte Claude-Code-Session in einer Herdr-Pane —
  beobachtbar und unterbrechbar; Ergebnis als WORKTREE-HANDOFF-Block statt
  `worker-report.md` (Ablauf: `### Pane-Ausfuehrung`, wird von Phase 2/3 dieses Features
  gefuellt)

**Eligibility-Gate des Pane-Traegers (hart):** `HERDR_ENV` = `1` UND `herdr` im PATH
(`command -v herdr`). Sonst Abbruch — KEINE stille Degradierung auf den Subagenten:

```
⛔ Pane-Modus braucht Herdr (HERDR_ENV=1 + herdr-CLI), hier nicht verfuegbar.
   Alternativen: Subagenten-Modus (dtb:worker, Default) oder manueller
   Worker-Hand-off (skills/CLAUDE.md → „Parallele Sessions").
```

### Pane-Auftrag (Vorlage — die eine Quelle)

Der Auftragstext traegt ALLES, was die Worker-Session wissen muss — Rolle, Ort, Adressen,
Rueckkanal. Es gibt bewusst KEINE Team-Registry und keine persistierten Pane-IDs
(fluechtige Adressen; eine Datei waere eine Zustandsaussage ohne Pfleger). Die
Orchestrator-Adresse kommt zur Laufzeit aus `$HERDR_PANE_ID`. Alle Herdr-Kommandos des
Pane-Modus stehen NUR in dieser Vorlage und in `### Pane-Ausfuehrung` — Herdr-CLI-Drift
(bekanntes, dokumentiertes Risiko; Syntax-Stand 2026-08-16) wird an einem Ort korrigiert:

```
Du bist Worker-Session fuer den Change `{slug}`.
Dein Arbeitsplatz ist dieser Worktree ({worktree-pfad}) — arbeite nur hier, fasse keine
zentralen Workflow-Dateien an (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele
Sessions").
Orchestrator: Herdr-Pane {orchestrator-pane}.

Auftrag: Lies {config.paths.workflows}/features/{slug}/task.md und arbeite die
## Schritte ab. Hake erledigte Schritte in der task.md ab.
{Vorab-Antworten aus der Freigabe, falls vorhanden}
Committe deine Aenderungen auf dem aktuellen Branch (task/{slug}) mit aussagekraeftiger
Message — NIEMALS pushen, keine anderen Branches.
Deckelung: max. {worker.max_attempts} Versuche, max. {worker.max_minutes} Minuten.
Triffst du auf eine ungeklaerte Entscheidung, die deine Vorab-Antworten nicht abdecken:
stoppe die Arbeit und fuehre sie unter „Offene Punkte" im Hand-off-Block auf — niemals
raten.

Wenn fertig: Baue den WORKTREE-HANDOFF-Block nach dem Format aus deiner installierten
Skill-Kopie `~/.claude/skills/dtb-workflow-checkpoint/SKILL.md` (Sektion
„### Hand-off-Block") — den Skill NICHT aufrufen, nur das Format lesen. Schicke den
Block WOERTLICH und VOLLSTAENDIG (inklusive Kopfzeile „WORKTREE-HANDOFF (dtb) — …") an
den Orchestrator zurueck:
herdr agent prompt {orchestrator-pane} "<der komplette Block>"
Nichts paraphrasieren — die Kopfzeile ist der einzige Erkennungsanker der Empfangsseite.
```

Der Block ersetzt im Pane-Modus den `worker-report.md` vollstaendig (er landet via
Empfangsseite im Session-Log — dauerhafter als der Report; Entscheidung 2026-08-16).
Die Schreibgrenze und die VERBOTE-Substanz gelten unveraendert — einziger Unterschied
zum Subagenten: der Pane-Worker COMMITTET auf seinem eigenen Task-Branch (Merge und
Diff-Abnahme brauchen eine Branch-Referenz), pusht aber nie.

### Pane-Ausfuehrung (Traeger `pane`)

#### Hinweg: Vorbedingungen

Vor jedem Pane-Start, in dieser Reihenfolge:

1. **Auftragsdatei committet?** (L18) Die `task.md` des Eintrags muss committet sein —
   der Worktree entsteht aus einem Commit und sieht Uncommittetes nicht:
   `git status --short -- {config.paths.workflows}/features/{slug}/task.md` muss leer
   sein. Sonst Abbruch mit Hinweis (erst committen, z.B. via `/dtb:commit-and-push`)
2. **Fremde Session im Haupt-Checkout?** `herdr agent list` lesen und Eintraege mit
   Arbeitsverzeichnis = Haupt-Checkout (ausser der eigenen Pane `$HERDR_PANE_ID`)
   suchen. Fund → genau EINE Warnzeile, dann weiterarbeiten (melden statt blockieren;
   die Verzeichnis-Angabe ist der Pane-Start-Stand und stale-anfaellig — belegt
   2026-08-16, deshalb kein hartes Verbot):
   ```
   ⚠ Weitere Session im Haupt-Checkout gefunden ({pane-id}) — der Worktree-Guard
     deckt diesen Fall nicht (skills/CLAUDE.md → „Bekannte Grenze").
   ```

#### Hinweg: Start-Sequenz

Vier Kommandos je Aufgabe — Antworten lesen, IDs nie raten (Syntax-Stand 2026-08-16,
Drift-Risiko dokumentiert; Kommandos nur hier und in der Vorlage oben):

1. `git worktree add {repo-parent}/.dtb-worktrees/worker-{slug} -b task/{slug}` —
   Task-Branch statt detached HEAD (bewusste Differenz zum Subagenten-Traeger:
   Merge und Diff-Abnahme brauchen eine Branch-Referenz; Entscheidung 2026-08-16)
2. `herdr pane split --current --direction right --cwd {worktree-pfad} --no-focus` —
   Pane-ID aus `.result.pane.pane_id` der Antwort lesen
3. `herdr pane run {pane-id} "claude"` — startet die Session ueber die Pane-Shell.
   BEWUSST NICHT `herdr agent start`: der scheitert auf Windows zweifach (ohne
   Agent-Argumente am `Start-Process -ArgumentList ''`-Bug, mit Argumenten an
   „%1 ist keine zulaessige Win32-Anwendung" — `claude` ist ein npm-Shim, kein
   Win32-Exe; beide belegt 2026-08-16). Danach **Erkennungs-Warten**: `herdr pane
   list` wiederholt lesen, bis die Pane `"agent": "claude"` mit `agent_status`
   `idle` traegt (Budget ~90 s, genau EIN weiterer Anlauf), sonst Abbruch:
   Meldung + Pane-Inhalt (`herdr pane read {pane-id}`) zeigen
4. `herdr agent prompt {pane-id} "{Pane-Auftrag aus der Vorlage}"` — Ziel ist die
   Pane-ID (kein Agent-Name — `pane run` vergibt keinen). Der Auftrag ist
   mehrzeilig; als EIN Argument uebergeben (die Zustellung als eine Nachricht ist
   belegt — Zustellungs-Probe 2026-08-16)

Danach kehrt der Orchestrator zur eigenen Arbeit zurueck — KEIN blockierendes Warten
(Rueckweg: naechste Sektion, gefuellt von Phase 3 dieses Features).

### Schritt 6: Worker starten (Einzel-Task)

**Vorbedingung (hart):** Zielbereich clean — `git status --short` fuer die vom Task
beruehrten Pfade zeigt nichts Uncommittetes. Sonst kein Start (melden, Nutzer raeumt auf).

**Isolation (immer):** Je Worker ein eigener Git-Worktree — auch fuer den Einzel-Worker:
`git worktree add {repo-parent}/.dtb-worktrees/worker-{slug} HEAD` — ein stabiler Ort
NEBEN dem Repo, kein Session-Temp-Verzeichnis (die Abnahme kann in einer Folgesession
passieren, der Diff muss sie ueberleben). Das Ergebnis bleibt als Diff im Worktree
liegen, bis der Mensch abnimmt; der Arbeitsbaum des Nutzers wird nie beruehrt.

**Start:** Background-Subagent mit dem Auftrags-Template (der Nutzer arbeitet weiter,
Meldung bei Abschluss):

```
Auftrag Worker {slug}:
- Arbeitsverzeichnis: {Worktree-Pfad} — dein gesamter Aktionsradius
- Schritte: {## Schritte aus features/{slug}/task.md}
- Vorab-Antworten: {beantwortete Vorab-Fragen aus der Freigabe}
- Erfolgskriterium: {mechanische Pruefung je Schritt — Grep/Test/Build/Datei}
- Deckelung: max. {max_attempts} Versuche, max. {max_minutes} Minuten
  (Anweisungs-Ebene — protokolliere Start/Ende/Dauer je Versuch im Report)
- Versuchsschleife: umsetzen → Kriterien pruefen → bei Rot nachbessern und erneut
  pruefen — bis gruen, Versuche verbraucht oder Zeit um
- Rechenschaft: erledigte `## Schritte` in features/{slug}/task.md abhaken und
  features/{slug}/worker-report.md schreiben (Template in Schritt 8) — beides IN
  DEINEM WORKTREE (die Pfade sind Worktree-relativ); das Haupt-Repo erreichen die
  Aenderungen erst mit der Abnahme

VERBOTE (hart, keine Ausnahme):
- niemals committen oder pushen
- keine Schreibzugriffe ausserhalb des eigenen Worktrees
- keine zentralen Dateien (WORKFLOW_STATUS.md, INBOX.md, BACKLOG.md) und keine
  Status-/Anzeigefelder anfassen
- triffst du auf eine ungeklaerte Entscheidung, die deine Vorab-Antworten nicht
  abdecken: Abbruch + Ausgang „teilweise" im Report — niemals raten, niemals fragen
```

Die VERBOTE sind die Worker-Instanz der kitweiten **Schreibgrenzen-Regel**
(`skills/CLAUDE.md` → „Parallele Sessions") — Aenderungen an der Grenze dort nachziehen,
nicht hier eigenstaendig formulieren.

### Schritt 7: Listen-Lauf

Ein einheitlicher Ausfuehrungspfad — sequenziell und parallel unterscheiden sich nur in
der Anzahl gleichzeitig laufender Worker (je Worker immer ein eigener Worktree):

1. **Reihenfolge:** Die freigegebene Reihenfolge aus der Sicht wird abgearbeitet.
   Abhaengige Eintraege warten auf ihren Vorgaenger; unabhaengige Eintraege mit
   disjunkten Dateien (∥-Kandidaten) starten gleichzeitig
2. **Kollisionsregel (gilt fuer BEIDE Traeger — Subagent wie Pane):** Stellt sich
   waehrend des Laufs heraus, dass zwei Worker doch dieselbe Datei anfassen (die Analyse
   ist eine Schaetzung) → der SPAETER gestartete Worker stoppt mit Ausgang „gestoppt";
   sein Eintrag wandert ans Listen-Ende. Im Pane-Modus verhindert die Zuteilung die
   Kollision zusaetzlich vorab: Aufgaben mit gemeinsamen Dateien werden nie gleichzeitig
   zugeteilt — der freie Worker bekommt die naechste konfliktfreie Aufgabe, die
   kollidierende wartet (Warteschlange). Diese Stopp-Regel bleibt das Auffangnetz
3. **`teilweise`-Eintraege** (unbeantwortete Vorab-Frage): ueberspringen und am Ende
   gesammelt melden — kein stiller Verlust
4. **Degradation:** Kein Git-Repo bzw. keine Worktree-Faehigkeit → sequenziell direkt im
   Arbeitsbaum, mit Pflicht-Warnhinweis im Freigabe-Dialog („waehrend des Laufs nicht im
   Repo arbeiten"). Die Lane verweigert nie wegen fehlender Traeger

### Schritt 8: Bericht (`worker-report.md`)

Jeder SELBST-beendete Worker schreibt VOR seinem Ende den vollen Bericht nach
`features/{slug}/worker-report.md` (status-neutral, zaehlt NICHT fuer die
Statusableitung — Kanon: `DERIVED_STATE_RULES.md` §1.1). Bei harten Stopps
(Task-Verwaltung, Kollisionsregel) bleibt der Diff ohne Report — der koordinierende
Haupt-Agent legt eine Minimal-Notiz an (Ausgang „gestoppt", Zeitpunkt):

```markdown
# Worker-Report: {slug}

**Gestartet:** {YYYY-MM-DD HH:MM} · **Beendet:** {HH:MM} · **Gesamtdauer:** {Min}
**Ausgang:** gruen | Deckel erreicht | teilweise | gestoppt
  (gruen = alle WORKER-ERREICHBAREN Schritte gruen; bei der Freigabe ausgeklammerte
  Schritte weist der Report unter „Was aufgefallen ist" als Abnahme-Aufgaben aus)
**Worktree:** {Pfad} (Diff liegt dort bis zur Abnahme)

## Versuche

| # | Start | Ende | Dauer | Ergebnis |
|---|-------|------|-------|----------|
| 1 | {HH:MM} | {HH:MM} | {Min} | {gruen / rot: woran} |

## Was getan wurde
- {konkrete Aenderungen, je Datei}

## Was verifiziert wurde
- {ausgefuehrte Pruefungen mit Ergebnis — Kommando + Ausgabe-Kern}

## Was aufgefallen ist
- {Nebenbefunde, Ueberraschungen, offene Reste — oder „nichts"}
```

### Schritt 9: Abschluss-Meldung

Im Chat je Task genau **eine** Sammel-Zeile (Details gehoeren in den Bericht, nicht in
den Chat — Status-Konvention):

```
{slug}: {Ausgang} nach {N} Versuch(en) ({Min} Min) → features/{slug}/worker-report.md
(bis zur Abnahme im Worktree, danach im Haupt-Repo)
{Bei Liste: uebersprungene "teilweise"-Eintraege + gestoppte Worker gesammelt}

Naechster Schritt: Abnahme durch dich — Diff im Worktree pruefen, dann uebernehmen
(Merge/Apply + Commit via /dtb:commit-and-push) oder mit Korrekturhinweis liegen lassen
(zweiter Lauf nutzt den Hinweis als zusaetzliche Vorab-Antwort).
```

Nach Uebernahme ODER endgueltigem Verwerfen: `git worktree remove {Pfad}` (`--force` bei
verworfenem Stand) — keine verwaisten Worktree-Registrierungen zuruecklassen.
