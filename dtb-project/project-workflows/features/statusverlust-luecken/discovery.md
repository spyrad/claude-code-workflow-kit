# Discovery: Statusverlust-Luecken schliessen
<!-- resume: done -->

**Erstellt:** 2026-09-23
**Idee-Referenz:** Inbox #95 — "Statusverlust-Luecken schliessen: (1) idea-review Task-Lane setzt "Ausgearbeitet" vor /dtb:task; (2) "Offene Aufgaben" in WORKFLOW_STATUS werden nie abgehakt, nur geloescht; (3) Dauerlaeufer ohne Alter; (4) Worktree-Fortschritt fuer workflow-next/resume/backlog-status unsichtbar bis Merge"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-idea-review/SKILL.md | (1) Task-Lane setzt `Ausgearbeitet` vor `/dtb:task` (Aktion Ausarbeiten, Dreier-Weiche) |
| skills/dtb-task/SKILL.md | (1) Schritt 4b INBOX-Rueckverlinkung — Gegenstueck der Luecke |
| skills/dtb-archive/SKILL.md | (1) Schritt 2 nimmt `Ausgearbeitet` pauschal als Archiv-Kandidat, ohne Change-Link-Pruefung |
| skills/dtb-project-health/SKILL.md | (1) Konsistenzpruefung „Ausgearbeitet → spec.md existiert" deckt `task.md` und fehlenden Link nicht ab |
| skills/dtb-idea-rank/SKILL.md | (1) kennt „Ausgearbeitet ohne Change-Link" bereits als „nicht pruefbar" — lesendes Vorbild |
| skills/dtb-workflow-checkpoint/SKILL.md | (2) Teil 2 Template `## Offene Aufgaben` (nur Ueberschreiben, kein Abhaken); (3) `### Naechste Schritte`-Uebertrag ohne Alter |
| skills/dtb-workflow-next/SKILL.md | (4) liest nur den Haupt-Checkout, keine Worktree-Sicht |
| skills/dtb-workflow-resume/SKILL.md | (4) liest nur den Haupt-Checkout, keine Worktree-Sicht |
| skills/dtb-backlog-status/SKILL.md | (4) liest nur den Haupt-Checkout; Tabelle `## Offene Aufgaben` |
| skills/dtb-pane-start/SKILL.md | (4) legt Worktree `.dtb-worktrees/pane-{slug}` / Branch `feature/{slug}` an — Quelle fuer eine Worktree-Sicht |
| skills/dtb-worker/SKILL.md | (4) Pane-Traeger legt `.dtb-worktrees/worker-{slug}` / Branch `task/{slug}` an — Quelle fuer eine Worktree-Sicht |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | (1)(4) §1.5 Sonderregel task/bug; Regel fuer INBOX-Status mit Link-Pflicht und fuer Worktree-Stand fehlt |
| skills/CLAUDE.md | (4) Schreibgrenzen-Regel „Parallele Sessions" und Worktree-Guard-Vorlage |
| dtb-project/project-workflows/WORKFLOW_STATUS.md | (2) Betroffenes Objekt (Daten, kein Skill) |

**Belege (Scan 2026-09-23):**
- (1) latent: kein Eintrag „als Aufgabe geroutet" ohne `task.md`-Link in `INBOX.md` oder `archive/` — Luecke belegbar, bisher nie eingetreten
- (2) 173 Commits an `WORKFLOW_STATUS.md`, in keiner Version ein `- [x]`
- (3) „Sprachausgabe auf dem Arbeitsrechner installieren" 6× offen in den Logs 2026-09-11..16, ohne Erstdatum
- (4) keine Lese-Sicht fragt `git worktree list` oder Task-Branches ab

---

## Anforderungen

### Scope
**Enthalten:**
- Leitziel: Der Status einer Aufgabe wird ueber ihre gesamte Lebensdauer eindeutig festgehalten
- „Aufgabe" in der breiten Lesart: jede Arbeitseinheit, die in einer Sicht auftaucht — INBOX-Idee, Punkt unter Offene Aufgaben / Naechste Schritte, Change im Worktree
- **Eindeutig:** jeder Endzustand ist unterscheidbar (erledigt / verworfen / noch offen); „verschwunden" ist kein Zustand mehr — schliesst (2)
- **Ganze Lebensdauer:** kein Uebergang zwischen Erfassung und Abschluss, an dem die Aufgabe aus allen Sichten faellt — schliesst (1) (Weiche → `task.md`) und (4) (Worktree-Arbeit → Merge)
- **Festhalten:** eine Aufgabe weiss, seit wann sie offen ist — schliesst (3)
- **Aufraeum-Luecke (Zusatz aus Schritt 4):** „erledigt, aber nicht abgebaut" ist ebenfalls ein
  uneindeutiger Status — gemergte Worktrees werden in der Worktree-Sicht (4) als solche angezeigt
  (Beleg: `features/rueckfragen-erhebung/erhebung.md` Schritt 3)

**Nicht enthalten:**
- Keine zentrale Statusdatei / -datenbank — Derived State bleibt; die Loesung ergaenzt Artefakte (Erstdatum, `[x]` mit Vermerk), keinen neuen Status-Speicher
- Keine aktive Ueberwachung / kein getakteter Lauf — das ist #97; hier nur Anzeige in den bestehenden Sichten beim Aufruf
- Keine Schreibzugriffe ueber Worktree-Grenzen — Sichten duerfen Worktree-Branches und -Arbeitsbaeume lesen (praezisiert in 3c), nie dort oder von dort in zentrale Dateien schreiben; Schreibgrenzen-Regel und Worktree-Guard bleiben unveraendert
- Keine automatische Entscheidung bei Dauerlaeufern — Alter wird angezeigt/ab Schwelle hervorgehoben, Verwerfen/Erledigen entscheidet der Mensch
- Keine rueckwirkende Aufarbeitung der alten `WORKFLOW_STATUS`-Versionen und Logs — Regel gilt ab Einfuehrung; laufende Dauerlaeufer bekommen beim ersten Checkpoint ihr Erstdatum, rekonstruiert aus dem ersten Log-Auftreten
- Kein Umbau des Statusmodells — BACKLOG-Legende und INBOX-Statuswerte (§3) bleiben; bei (1) wird nur der Setz-Zeitpunkt von `Ausgearbeitet` korrigiert und/oder die Link-Pflicht geprueft, kein neuer Status

### Gewuenschtes Verhalten
Leitlinie: **Jeder Abgang braucht einen Vermerk, jede offene Aufgabe ein Datum, jede Sicht sieht auch Worktrees.**

- **(1) Task-Lane — `Ausgearbeitet` bleibt, die Leseseite wird abgesichert.** Die Entscheidung
  2026-08-02 (impl-review F2: kein `In Arbeit`, sonst laden argumentlose feature-fast/-discover-Laeufe
  die Idee) wird NICHT revidiert. Neue Regel in `DERIVED_STATE_RULES.md`: `Ausgearbeitet` gilt nur mit
  Change-Link; ohne Link = „Ausgearbeitet, Change fehlt" → zaehlt als offen.
  - `dtb:archive` archiviert sie nicht, sondern meldet sie mit Hinweis `/dtb:task {N}`
  - `dtb:project-health` prueft den Link fuer `spec.md` UND `task.md`
  - `dtb:workflow-next` und `dtb:idea-rank` zeigen sie als offen, nicht als erledigt
  - Muster: „nicht pruefbar"-Regel aus `dtb:idea-rank`; kein neuer Status
- **(2) Offene Aufgaben — kein Punkt verschwindet ohne Abschlussvermerk.** Ein `[x]` in
  `WORKFLOW_STATUS.md` waere nutzlos (Datei wird ueberschrieben). Die dauerhafte Spur gehoert in den
  append-only Session-Log: der Checkpoint vergleicht die alte mit der neuen „Offene Aufgaben"-Liste und
  schreibt fuer jeden wegfallenden Punkt einen Vermerk `erledigt` oder `verworfen: {Grund}` (Grund
  Pflicht). Muster: `archive/INBOX-BEFUNDE-verworfen.md` mit Pflicht-Grund.
- **(3) Alter — `(seit YYYY-MM-DD)` an jedem offenen Punkt, einmal zur Entscheidung zwingen.**
  - Datum wird beim Uebertragen woertlich mitgenommen, nie neu gesetzt
  - ab Schwelle in `workflow.config.yaml` (Vorschlag 7 Tage) markiert der Checkpoint den Punkt mit ⏳
    und fragt EINMAL: behalten / erledigen / verwerfen; „behalten" → erst nach der naechsten Schwelle
    wieder. Muster: „genau einmal liegen lassen" aus `dtb:idea-triage`
  - (2) und (3) laufen ueber DENSELBEN Vergleich im Checkpoint — ein Mechanismus, nicht zwei
- **(4) Worktree-Sicht — eine Regel, dreimal referenziert.** Neuer Abschnitt „Worktree-Stand" in
  `DERIVED_STATE_RULES.md`; `workflow-next`, `workflow-resume`, `backlog-status` referenzieren ihn
  (Verweis, keine Kopie). Je `git worktree list`-Eintrag ausser dem Haupt-Checkout eine Zeile:
  ```
  In Worktrees:
    statusverlust-luecken  interaktiv (pane)  feature/statusverlust-luecken  +2 Commits, zuletzt 2026-09-23  Progress 3/12
  ```
  - Art aus dem Pfad-Praefix: `pane-` = interaktiv, `worker-` = autonom
  - Progress per `git show {branch}:…/plan.md` aus dem Haupt-Checkout — Worktree wird nicht betreten,
    nichts geschrieben (Ausschluss 3a)
  - letzter Commit aelter als die Schwelle aus (3) → Zeile ebenfalls ⏳; liegengebliebene
    Worktree-Arbeit faellt auf, ohne #97
  - Branch bereits in den Hauptbranch gemergt (`git branch --merged`) → statt Progress
    `gemergt → aufraeumen (git worktree remove …)`; nur Hinweis — abbauen tut der Mensch bzw. der
    zustaendige Skill (Ausschluss „keine automatische Entscheidung")

### Randfaelle
**(1) Task-Lane**
- Link vorhanden, Zielordner fehlt (umbenannt/geloescht) → wie „kein Link": „Ausgearbeitet, Change fehlt"
- Link zeigt auf `archive/<slug>/` → erledigt, in Ordnung
- bereits archivierte Alt-Eintraege → nicht rueckwirkend geprueft (Ausschluss 3a)

**(2)+(3) Offene Aufgaben / Alter (derselbe Vergleich)**
- Punkt umformuliert → semantische Zuordnung statt Textvergleich; bei Unsicherheit Rueckfrage
  („ist X = Y?"); `seit`-Datum wandert mit
- zusammengelegt/aufgeteilt → Vermerk `aufgegangen in …`, das aelteste Datum wird geerbt
- erster Checkpoint nach Einfuehrung → Datum aus dem ersten Log-Auftreten rekonstruiert, gekennzeichnet
  `(seit ≤YYYY-MM-DD)`; nichts gefunden → heutiges Datum mit `≤`
- viele ⏳ auf einmal (v.a. erster Lauf) → EINE Sammelvorlage mit Default „behalten", vetobar
  (Muster Sammelvorlage feature-fast/Checkpoint) statt N Einzelfragen
- Abbruch der Entscheidung → alles bleibt offen, Daten unveraendert, Frage kommt naechstes Mal wieder
- leere Liste → kein Vergleich, kein Vermerk
- Checkpoint im Worktree → Teil-Guard ueberspringt WORKFLOW_STATUS, kein Vergleich; holt der naechste
  Orchestrator-Checkpoint nach

**(4) Worktree-Sicht**
- uncommittete Arbeit → `git show` sieht sie nicht; zusaetzlich rein lesend
  `git -C {pfad} status --porcelain` → `N uncommitted`. Praezisiert den Ausschluss 3a: Worktree wird
  nicht **beschrieben** (Lesen ist erlaubt)
- Subagent-Worker (detached HEAD, keine Commits, `git show` greift ins Leere) → Zeile
  `autonom (subagent) · detached · N uncommitted · worker-report vorhanden ja/nein`;
  `worker-report.md` wird direkt aus dem Worktree-Pfad gelesen (lesend, erlaubt)
- Branch ohne `plan.md` (Discovery-Phase, Worker-Task) → Progress aus `task.md` `## Schritte`; beides
  fehlt → „—" + Stage-Name (z.B. `Discovery`)
- verwaister Eintrag (Pfad weg, `prunable`) → Zeile „verwaist → `git worktree prune`", kein Abbruch
- Worktree ausserhalb `.dtb-worktrees/` (von Hand angelegt) → wird gezeigt, Art `manuell`
- Nicht-Git-Projekt (z.B. dtb-assistant) → Block entfaellt still
- kein zusaetzlicher Worktree → Block entfaellt still (kein „keine"-Rauschen)

### Einschraenkungen
**Technisch**
- Nur Prompt-Anweisungen — alles muss als Anweisung in `SKILL.md` / `DERIVED_STATE_RULES.md`
  umsetzbar sein; keine Skripte, keine Hooks (Klasse A kennt keine Hooks, Vorbefund #35(d)/#45)
- **`DERIVED_STATE_RULES.md` ist ein Seed, wird von `kit-sync` NICHT verteilt** (nur `project-init`).
  Skills kommen per kit-sync sofort an, die neuen DSR-Abschnitte (1)/(4) erst nach erneutem
  project-init → ein aktualisierter Skill verweist auf einen Abschnitt, den die Zielprojekt-Kopie
  nicht hat. Loesung: Regel kanonisch in DSR; jeder referenzierende Skill traegt eine
  Einzeiler-Rueckfallregel „Abschnitt fehlt → Hinweis `DERIVED_STATE_RULES.md veraltet —
  /dtb:project-init aktualisieren`, Alt-Verhalten beibehalten" (Vorbild `dtb:plan-review` Z. 34)
- Checkpoint-Groesse knapp: `workflow-checkpoint` hat bereits 470 Zeilen, der Vergleich (2)+(3) kommt
  hinzu (Idee „Checkpoint-Zeilenlimit" laeuft in den Logs) → Logik moeglichst in die DSR-Regel,
  der Checkpoint referenziert nur
- `WORKFLOW_STATUS.md` bleibt 60-80 Zeilen, Offene Aufgaben bleiben 1-Zeiler — `(seit …)`/⏳
  verlaengern die Zeile, fuegen keine Zeilen hinzu
- Git in Lese-Sichten nur lesend: `git worktree list --porcelain`, `git show`, `git log`,
  `git -C … status --porcelain`; Pfade mit Forward-Slash, Git-Bash-tauglich (Windows); 2-3 Aufrufe je
  Worktree — Performance unkritisch
- Neuer Config-Key (Schwelle) mit Default im Skill bei fehlendem Key (Muster
  `parallel.default_branch`) — alte Configs laufen weiter

**Fachlich**
- Derived State bleibt oberstes Prinzip — Artefakt gewinnt, Konflikt wird gemeldet
- Status-Neutralitaet: Abschlussvermerke und `(seit …)` im Session-Log sind einfache Aufzaehlungen,
  KEINE Checkboxen — duerfen nie in eine Status-Ableitung eingehen (Muster WORKTREE-HANDOFF-Block)
- Schreibgrenzen-Regel und Autonomie-Regel bleiben unberuehrt — zentrale Dateien schreibt nur der
  Orchestrator; Worker-Governance unveraendert
- Kit-Konventionen: Deutsch in ae/oe/ue-Umschreibung der Skill-Dateien, Datum `YYYY-MM-DD`,
  bestehende Struktur-Anker und Grep-Tokens bleiben stabil

### Integrationspunkte
**Schreibende Seite (Verhalten aendert sich)**
- `dtb:workflow-checkpoint` — Offene-Aufgaben-Vergleich, Abschlussvermerke im Log, `(seit …)`,
  ⏳-Sammelvorlage; Teil-Guard im Worktree bleibt
- `dtb:idea-review` — Task-Lane-Vermerk bleibt, macht nur „Link ausstehend" explizit
- `dtb:task` Schritt 4b — unveraendert; ist der Uebergang „Change fehlt" → „Ausgearbeitet mit Link"
- `DERIVED_STATE_RULES.md` — zwei neue Abschnitte ((1) Link-Pflicht, (4) Worktree-Stand) + die
  Vergleichsregel (2)+(3)
- `workflow.config.yaml` — Schwellen-Key mit Default

**Lesende Seite (Anzeige kommt dazu)**
- `workflow-next`, `workflow-resume`, `backlog-status` — Block „In Worktrees" + „Ausgearbeitet, Change
  fehlt" als offen
- `archive` (Sperre + Meldung), `project-health` (Link-Pruefung spec/task), `idea-rank` (als offen)
- mitbetroffen, nur Vertraeglichkeit pruefen: `workflow-status` (zaehlt INBOX-Status → „Change
  fehlt"), `session-summary` (liest `Offen / Naechste Schritte` aus Logs — muss `(seit …)` vertragen),
  `feature-start` (zeigt Offene Aufgaben), `workflow-resume` (liest WORKFLOW_STATUS als Kontext)

**Quellen der Worktree-Sicht (unveraendert, nur Leseziel)**
- `dtb:pane-start` — `.dtb-worktrees/pane-{slug}`, Branch `feature/{slug}`, committet
- `dtb:worker` Pane-Traeger — `worker-{slug}`, Branch `task/{slug}`, committet
- `dtb:worker` Subagent-Traeger (SKILL.md Schritt 6) — `git worktree add … HEAD` = detached HEAD
  ohne Commits, Ergebnis als uncommitteter Diff + `worker-report.md` (siehe Randfaelle (4))
- Harness-Worktrees (`isolation: worktree`, ausserhalb `.dtb-worktrees/`) → Art `manuell` (3c)

**Externe Abhaengigkeiten**
- nur `git` (bereits vorausgesetzt); **kein Herdr** — die Sicht funktioniert ohne `HERDR_ENV`, sie
  liest Git-Stand, nicht Pane-Stand (zugleich die Grenze zu #97)
- Verteilung: Skills via `kit-sync`, `DERIVED_STATE_RULES.md` via `project-init` (Rueckfallregel 3d)

**Beruehrte Ideen**
- #97 (Rueckkanal) bleibt eigenstaendig — #95 (4) liefert die Anzeige, auf die ein #97-Loop spaeter
  nur noch aufsetzen muesste
- #57/#98 (Autonomie-Achse) nicht beruehrt

---

## Abhaengigkeiten

- Bestehende Changes: 1 — `rueckfragen-erhebung` (Task, `Abgenommen`); keine Konflikte (aendert keine
  der betroffenen Dateien)
- Ueberschneidung (Beleg, kein Konflikt): `rueckfragen-erhebung/erhebung.md` Schritt 3 (Z. 86-88) —
  0 belegte Nachfragen nach Pane-/Worktree-Stand in 5 Laeufen → #97-Nutzen nicht belegt, Anzeige-Luecke
  #95 (4) und Aufraeum-Luecke belegt; stuetzt den Zuschnitt dieses Change
- #97 (Rueckkanal) bleibt eigenstaendige Idee; kann spaeter auf der Worktree-Sicht (4) aufsetzen

---

## Offene Punkte

- Schwelle fuer ⏳: finaler Wert (Vorschlag 7 Tage) und Key-Name in `workflow.config.yaml` — in der Spec festlegen
- Traeger des `seit`-Datums: sind `## Offene Aufgaben` (WORKFLOW_STATUS) und `### Naechste Schritte` (Session-Log) derselbe Uebertrag oder zwei Listen? Welche ist die Quelle fuer den Vergleich (2)+(3)?
- Vergleichsbasis fuer (2): alte Liste aus der committeten `WORKFLOW_STATUS.md` (`git show HEAD:…`) oder aus dem letzten Session-Log — in der Spec festlegen (Nicht-Git-Projekt beachten)
- Hauptbranch fuer `git branch --merged`: `parallel.default_branch` aus der Config oder Auto-Erkennung (master/main)?
- Checkpoint-Groesse (470 Zeilen): reicht „Logik in die DSR-Regel, Checkpoint referenziert", oder braucht es vorher die separate Idee „Checkpoint-Zeilenlimit"?

---

**Erstellt mit:** `/dtb:feature-discover`
