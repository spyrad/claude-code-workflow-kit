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

### Schritt 7: Listen-Lauf

Ein einheitlicher Ausfuehrungspfad — sequenziell und parallel unterscheiden sich nur in
der Anzahl gleichzeitig laufender Worker (je Worker immer ein eigener Worktree):

1. **Reihenfolge:** Die freigegebene Reihenfolge aus der Sicht wird abgearbeitet.
   Abhaengige Eintraege warten auf ihren Vorgaenger; unabhaengige Eintraege mit
   disjunkten Dateien (∥-Kandidaten) starten gleichzeitig
2. **Kollisionsregel:** Stellt sich waehrend des Laufs heraus, dass zwei Worker doch
   dieselbe Datei anfassen (die Analyse ist eine Schaetzung) → der SPAETER gestartete
   Worker stoppt mit Ausgang „gestoppt"; sein Eintrag wandert ans Listen-Ende
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
