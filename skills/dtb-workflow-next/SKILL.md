---
name: dtb:workflow-next
description: >-
  Use when: "was steht an", "naechster Schritt", "wo war ich",
  "workflow next", "was mache ich als naechstes". Read-only skill
  showing the concrete next action per active feature based on
  artifact existence and pipeline position.
disable-model-invocation: false
argument-hint: "[Feature-Name]"
allowed-tools: Read, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [INBOX.md, features/*/discovery.md, features/*/spec.md, features/*/plan.md, features/*/bug.md, features/*/task.md, features/*/worker-report.md, BACKLOG.md, WORKFLOW_STATUS.md, project-rules/DERIVED_STATE_RULES.md, workflow.config.yaml]
  produces: []
---

# DTB Workflow-Next

Leichtgewichtiger "Workflow-GPS": Zeigt den konkreten naechsten Schritt pro aktivem Feature.

## Schritt 1: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 2: Alle aktiven Features scannen

**Ableitungsregel:** Der Status wird aus Artefakten ABGELEITET, nie aus Statusfeldern
uebernommen — verbindliche Regeln in `{config.paths.rules}/DERIVED_STATE_RULES.md`
(Fallback: `dtb-project/project-rules/DERIVED_STATE_RULES.md`). Lies diese Datei zuerst.
Statusfelder in BACKLOG.md dienen nur der Konflikterkennung (siehe Schritt 3).

**Quellen:**
- `{config.paths.workflows}/INBOX.md` — Eintraege mit Status `In Arbeit`, dazu Eintraege mit Status
  `Ausgearbeitet` OHNE gueltigen Change-Link (operative Kopie von Regel-Datei §8).
  Kernsatz: `Ausgearbeitet` ohne gueltigen Change-Link (8.1) ist „Ausgearbeitet, Change fehlt" und zaehlt als offen.
  Gueltig ist `→ features/{slug}/{spec|task|bug}.md` mit existierender Datei oder `→ archive/{slug}/…`
  mit existierendem Ordner; ein Link nur auf `discovery.md` belegt nicht.
  Links stehen in der Spalte „Idee", Pfade relativ zu `{config.paths.workflows}`; mindestens ein gueltiger Link genuegt (ein zusaetzlicher toter Link macht die Zeile nicht ungueltig); ein toter `features/{slug}/`-Link gilt als belegt, wenn `archive/{slug}/` existiert (Change inzwischen archiviert).
  Naechster Schritt bei „Change fehlt" (erster zutreffender Zweig gilt): Vermerk „als Aufgabe geroutet" → `/dtb:task {N}`; Link auf `features/{slug}/` mit vorhandener `discovery.md` → `/dtb:feature-plan {slug}`; sonst → `/dtb:feature-discover {N}`.
  Existiert zum verlinkten Slug ein Change-Ordner (z.B. nur `discovery.md`), erscheint die Idee
  NICHT als eigene Zeile — der Ordner-Eintrag traegt den Zusatz `(INBOX #{N} Ausgearbeitet, Change fehlt)`.
  **Wartungs-Hinweis (Format-Kopplung):** spiegelt §8 (Kopie ist Absicht — Seed erreicht
  Bestandsprojekte nicht automatisch, INBOX #22, §8); Aenderung dort → hier mitziehen.
- `{config.paths.workflows}/features/*/discovery.md` — Discovery-Dokumente
- `{config.paths.workflows}/features/*/spec.md` — Feature-Specs
- `{config.paths.workflows}/features/*/plan.md` — Implementierungsplaene: `## Progress`-Checkboxen zaehlen (X von Y abgehakt); Kopf-Statusfeld (`Entwurf`/`Reviewed`) = die `**Status:**`-Zeile in den **ersten 10 Zeilen** (Definitionsfenster, Regel-Datei §7.1 — Zeilen ausserhalb zaehlen nicht). Lese-Toleranz nach §7.3:
  | Gelesener Zustand | Behandlung |
  |---|---|
  | Feld fehlt / liegt ausserhalb des Fensters | wie `Entwurf`, **still** (fehlende Info ist kein Konflikt) |
  | Altwerte `In Umsetzung`/`Abgeschlossen` | wie `Reviewed`, **still** |
  | unbekannter Wert | wie fehlend + 1 Hinweiszeile „unbekannter Statuswert {X}" |

  Gelesen wird nur das **erste Wort** nach `**Status:**` (§7.1 Parse-Regel) — Klammer-Vermerk
  und HTML-Kommentar dahinter sind Annotation. In der Detail-Ausgabe erscheint der Wert hinter
  `Impl-Plan`; ein toleriert gelesener Altwert wird dort als `✓ Reviewed` angezeigt.
  **Wartungs-Hinweis (Format-Kopplung):** Diese Matrix spiegelt `DERIVED_STATE_RULES.md` §7.3
  (Kopie ist Absicht — Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22);
  Aenderung dort → hier mitziehen.
- `{config.paths.workflows}/features/*/bug.md`, `task.md` — Checkliste in der Datei zaehlen (`## Fix-Schritte` bzw. `## Schritte`)
- `{config.paths.workflows}/BACKLOG.md` — NUR fuer Konflikterkennung und Prio
- Verlinkte Git-Worktrees — Schritt 2b (Bash ausschliesslich fuer die dort gelisteten lesenden Git-Kommandos)

**Pipeline-Position pro Feature ermitteln (abgeleitet):**

**Feature-Pipeline:**

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| INBOX `In Arbeit`, kein Change-Ordner | Discovery ausstehend | `/dtb:feature-discover` |
| INBOX `Ausgearbeitet`, Change fehlt (§8), kein Change-Ordner zum Slug | Change fehlt | naechster Schritt nach der Regel in den Quellen (oben) |
| `discovery.md` vorhanden, kein `spec.md` | Spec ausstehend | `/dtb:feature-plan [NAME]` |
| `spec.md` vorhanden, kein `plan.md` | Plan ausstehend | `/dtb:impl-plan [NAME]` |
| `plan.md` Status `Entwurf`, **0/Y Checkboxen** | Review ausstehend | `/dtb:plan-review [NAME]` |
| `plan.md` Status `Reviewed`, 0/Y Checkboxen | Start ausstehend | `/dtb:feature-start` |
| `plan.md` teilweise abgehakt (X/Y) | In Entwicklung | `/dtb:implement [NAME]` — Schritt {erster nicht abgehakter N.M} |
| `spec.md`/`task.md` `**Status:** Abgenommen`, alle Checkboxen abgehakt | Abgenommen | `/dtb:archive` — Abnahme liegt vor, KEIN erneuter Abnahme-Vorschlag |
| `plan.md` alle Checkboxen abgehakt | Fertig zum Testen | Manuell testen, Abnahme via `/dtb:workflow-checkpoint` (Beleg-Rueckfrage), dann `/dtb:archive` |
| Ordner in `archive/<slug>/` | Abgeschlossen | — |

> **Checkbox-Guard (Regel-Datei §7.3):** Die `Entwurf`-Zeile greift NUR bei 0/Y Checkboxen.
> Bei teilweise oder vollstaendig abgehaktem Progress gewinnt die Progress-Zeile (`In Entwicklung`
> bzw. `Fertig zum Testen`) — ein plan-review-Vorschlag waere dort falsch, weil laengst
> implementiert wird. Zusaetzlich greift dann die Feld-Konfliktmeldung aus Schritt 3.

> **Abgenommen-Zeile (Regel-Datei §1.2, gespiegelte Lese-Regel — Grep-Anker, eine Zeile):**
> Ein gesetztes `Abgenommen` ueberschreibt die Ableitung „Fertig zum Testen" und ist KEIN Konflikt nach §1.3 (analog `Pausiert`).
> Die Zeile steht bewusst VOR der Y/Y-Zeile (Erst-Treffer-Auswertung) — sie greift nur bei
> vollstaendigem Progress; `Abgenommen` bei unvollstaendigem Progress ist ein Feld-Konflikt
> (Schritt 3), kein Pipeline-Zustand.

**Bug-Pipeline** (Checkliste = `## Fix-Schritte` im Bug-Report):

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| kein Analyse-Abschnitt (nur Symptom) | Analyse ausstehend | `/dtb:debug-plan [NAME]` |
| Analyse vorhanden, 0 Fix-Schritte abgehakt | Fix ausstehend | `/dtb:feature-start` oder direkt fixen |
| Fix-Schritte teilweise abgehakt | Fix in Arbeit | naechsten Fix-Schritt umsetzen |
| alle Fix-Schritte abgehakt | Test/Abschluss | Testplan ausfuehren, `/dtb:workflow-checkpoint` |

**Aufgaben-Pipeline** (Checkliste = `## Schritte` in `task.md`):

| Abgeleiteter Zustand | Pipeline-Position | Naechster Skill |
|---|---|---|
| 0 Schritte abgehakt | Start ausstehend | `/dtb:feature-start` |
| teilweise abgehakt | In Arbeit | naechsten Schritt umsetzen |
| alle abgehakt | Abschluss | `/dtb:workflow-checkpoint` |

**Fallbacks (kein Abbruch, siehe Regel-Datei §1.4):**
- `plan.md` ohne `## Progress` oder mit 0 Checkbox-Zeilen → "Plan vorhanden, Fortschritt unbekannt"; Nachruestung anbieten
- Flache Alt-Dateien (`PLAN_*.md` etc.) oder `IMPL_STATUS_*.md` direkt in `features/` (Altbestand) → fuer Ableitung ignorieren, Migrations-Hinweis (`/dtb:migrate-change-folders`)
- Ordner mit `plan.md` ohne `spec.md` → als "Change ohne Spec" melden
- Explizit `Pausiert` markierte Items → nicht anzeigen (ueberschreibt Ableitung)

## Schritt 2b: Worktree-Stand (Arbeit ausserhalb des Haupt-Checkouts)

Naechste Schritte beruecksichtigen auch Arbeit, die bis zum Merge nicht im Arbeitsbaum liegt.

**Worktree-Stand (operative Kopie von Regel-Datei §10 — rein lesend).**
Kernsatz: Die Sichten zeigen unter `In Worktrees` je verlinktem Worktree genau eine Zeile — gelesen, nie beschrieben.
- **Quelle:** `git worktree list --porcelain`; der **erste** Eintrag ist der Haupt-Checkout und wird nicht
  gelistet; die Zeilen folgen der Reihenfolge der Liste. Kein Git-Repo (`git rev-parse --git-dir` scheitert) oder
  kein weiterer Worktree → Block entfaellt still (kein „keine"); scheitert `worktree list` IM Git-Repo → genau eine
  Zeile `In Worktrees: nicht lesbar ({Fehler})` — nie still schlucken
- **Slug / Art:** Verzeichnisname ohne Praefix `pane-`/`worker-`. `pane-` → `interaktiv (pane)`; `worker-` mit
  Branch → `autonom (pane)`; `worker-` detached → `autonom (subagent)`; alles andere → `manuell`
- **Hauptbranch:** `parallel.default_branch` aus `workflow.config.yaml`, sonst Branch des ersten Eintrags — nie
  zwischen master/main raten
- **Stand** — erster zutreffender Zustand gilt; n = `git rev-list --count {haupt}..{branch}`, Reflog =
  `git reflog show refs/heads/{branch}`:
  1. Eintrag traegt `prunable` oder Pfad fehlt → `verwaist → git worktree prune` (Rest der Zeile entfaellt)
  2. n > 0 → `+{n} Commits, zuletzt YYYY-MM-DD` (`git log -1 --format=%cs {branch}`) — `laufend`
  3. n = 0 UND Reflog hat mehr als den Anlage-Eintrag → `gemergt → aufraeumen (git worktree remove "{pfad}")`;
     bei uncommitted > 0 stattdessen `gemergt, {N} uncommitted → erst sichern` (nie zum Entfernen raten, solange
     Arbeit ungesichert ist); in beiden Faellen entfaellt der Rest der Zeile
  4. sonst (n = 0, Reflog nur mit Anlage-Eintrag oder fehlend) → `frisch` — nie „aufraeumen"
- **uncommitted:** Zeilen von `git -C {pfad} status --porcelain`. **Fortschritt** aus dem Worktree-Pfad (inkl.
  uncommitteter Flips): `{pfad}/{config.paths.workflows}/features/{slug}/plan.md` `## Progress` → `Progress X/Y` ·
  sonst `task.md` `## Schritte` → `Schritte X/Y` · sonst Stage-Name (Regel-Datei §1.1, z.B. `Discovery`) · sonst `—`
- **Detached** (Subagent-Worker): Branch-Feld `detached @{sha7}`, Feld „Stand" entfaellt, statt Fortschritt
  `worker-report {vorhanden | fehlt}` (Datei im Change-Ordner unter `{pfad}`)
- **⏳** am Zeilenende bei `laufend` und `frisch`, wenn der letzte Commit (bei `frisch`: der Anlage-Eintrag im
  Reflog) ≥ `status.alter_schwelle_tage` Tage alt ist (Default 7)
- **Nur lesend:** erlaubt sind ausschliesslich die Kommandos oben (`worktree list`, `rev-list --count`,
  `log -1`, `reflog show`, `rev-parse --git-dir`, `-C {pfad} status --porcelain`) und das Lesen von Dateien unter `{pfad}`. Nie
  `checkout`, `add`, `commit`, `stash`, `worktree remove`/`prune` — „aufraeumen"/„prune" sind Hinweise an den Menschen

```
In Worktrees:
  {slug}  {Art}  {branch | detached @sha7}  {Stand}  {N} uncommitted  {Fortschritt}[  ⏳]
```

> **Wartungs-Hinweis (Format-Kopplung):** spiegelt §10 (Kopie ist Absicht, §10 — Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22);
> Aenderung dort → hier UND in den beiden anderen Sichten mitziehen (`dtb:workflow-resume`, `dtb:workflow-next`,
> `dtb:backlog-status` — der Block ist in allen dreien wortgleich; Grep-Anker: `In Worktrees`).

## Schritt 3: Konflikte erkennen, sortieren & priorisieren

**Konfliktregel (Regel-Datei §1.3):** Weicht ein BACKLOG-Statusfeld vom abgeleiteten
Zustand ab, gewinnt das Artefakt. Den Widerspruch mit 1 Hinweiszeile melden
(`⚠ BACKLOG sagt "{Feld}", Artefakte zeigen "{abgeleitet}"`), NICHT selbst korrigieren (read-only).

**Ausnahme `Abgenommen` (Regel-Datei §1.2):** kein §1.3-Konflikt — Kernsatz steht als Grep-Anker
in der Abgenommen-Zeile von Schritt 2 (bewusst nur EINE Kopie pro Datei).
**Konflikt ist genau eine Kombination:** `**Status:** Abgenommen` gesetzt UND `## Progress`
unvollstaendig (< Y/Y) — dann gewinnt das Artefakt, 1 Hinweiszeile:
`⚠ {Item}: Feld sagt "Abgenommen", ## Progress zeigt "{X/Y}"`.
Still-Regel: Feld fehlt oder traegt den (mit der Ableitung uebereinstimmenden) Wert → still; jeder andere Nicht-`Abgenommen`-Wert faellt unter die normale Konfliktregel §1.3.

**Feld-Konflikt `plan.md`-Kopf (Regel-Datei §7.3, gleiche Logik):** **Konflikt ist genau eine
Kombination:** ein physisch vorhandenes Feld, das als `Entwurf` gilt, UND ≥1 abgehakte
`## Progress`-Checkbox. Dann gewinnt ebenfalls das Artefakt, eine Hinweiszeile:
`⚠ plan.md-Kopf sagt "{Wert}", ## Progress zeigt "{X/Y}"`. Auch hier NICHT selbst korrigieren:
Pfleger des Felds ist `dtb:plan-review` (§7.2).
**Vorrang der Still-Regel:** Als `Entwurf` behandelte Leerstellen (Feld fehlt oder liegt
ausserhalb des Fensters) bleiben **still** — auch bei teilweise abgehaktem Progress; ebenso
`Reviewed`/tolerierte Altwerte bei beliebigem Progress (das Feld sagt nichts ueber den
Umsetzungsstand). Sonst erzeugte der haeufigste Altbestand dauerhaft eine ⚠-Zeile.

- Abgeleitet "In Entwicklung" zuerst — die sind am weitesten
- Dann nach Pipeline-Position absteigend (weiter fortgeschritten = hoehere Prio)
- INBOX-Zeilen „Change fehlt" ganz ans Ende (sie stehen vor Beginn der Pipeline), untereinander nach
  INBOX-Nummer aufsteigend; Name: `#{N} {Kurztitel}` — Kurztitel = eigene Verdichtung des Idee-Texts,
  hoechstens ~6 Woerter (wie `dtb:idea-rank`). Passen sie nicht mehr ins Zeilenlimit, ersetzt EINE Sammelzeile
  `{K} Ideen Ausgearbeitet, Change fehlt → /dtb:project-health` die abgeschnittenen — nie still weglassen
- Falls ein Argument uebergeben wurde: Nur dieses Feature zeigen

## Schritt 4: Kompakt ausgeben

### Ohne Argument (alle aktiven Features):

```
Naechste Schritte:

1. {Feature-Name}  → /dtb:{skill} [NAME]
   ({Status-Detail})
2. {Feature-Name}  → /dtb:{skill} [NAME]
   ({Status-Detail})
...

{N} weitere Feature-Specs ohne Plan → /dtb:impl-plan
{falls abgeschnitten: {K} Ideen Ausgearbeitet, Change fehlt → /dtb:project-health}

In Worktrees:
  {Zeilen aus Schritt 2b}
```

Der Worktree-Block steht am Ende und entfaellt still (Schritt 2b). Zeilen mit `gemergt → aufraeumen`,
`verwaist → git worktree prune` oder ⏳ sind die naechsten Schritte dieses Blocks — nur anzeigen, nie ausfuehren.

### Mit Argument (ein Feature im Detail):

```
{Feature-Name}:
  Inbox          ✓
  Discovery      ✓ (YYYY-MM-DD)
  Feature-Spec   ✓ (YYYY-MM-DD)
  Impl-Plan      {✓ Reviewed | ✓ Entwurf (Review ausstehend)}
  Progress       X/Y Schritte (abgeleitet)
  Verifikation   ○ (SHA-Belege je Phase, `dtb:implement`)
  Abnahme        ○

→ Naechster Schritt: /dtb:implement [NAME] — Schritt {erster nicht abgehakter Schritt N.M aus ## Progress}
{falls Konflikt: ⚠ BACKLOG sagt "...", Artefakte zeigen "..."}
{falls Feld-Konflikt: ⚠ plan.md-Kopf sagt "...", ## Progress zeigt "X/Y"}
```

## Richtlinien

- **Read-Only**: Dieser Skill aendert keine Dateien; Bash nur fuer die lesenden Git-Kommandos aus Schritt 2b
- **Kompakt**: Max 15 Zeilen Output (ohne Argument, zuzueglich Worktree-Block und „Change fehlt"-Sammelzeile), max 12 Zeilen (mit Argument)
- **Keine Rueckfragen**: Sofort Output liefern
- **Deutsch**: Alle Texte auf Deutsch
- **Leer-Zustand**: Bei 0 aktiven Features/Bugs/Aufgaben: "Keine aktiven Features, Bugs oder Aufgaben. Starte mit `/dtb:idea`, `/dtb:feature-plan`, `/dtb:bug-report` oder `/dtb:task`."

## Verwandte Skills

- `/dtb:workflow-status` — Globale Pipeline-Visualisierung mit Queue-Details
- `/dtb:backlog-status` — Backlog-Details
- `/dtb:workflow-resume` — Session fortsetzen

---

Scanne jetzt die Workflow-Artefakte und zeige die naechsten Schritte.
