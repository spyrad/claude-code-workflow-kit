# Beispielausgaben: Statusverlust-Luecken schliessen

**Erstellt:** 2026-09-23 (Schritt 1.5, Abnahme-Gate nach L64)
**Zweck:** Zielform der neuen Ausgaben an echten Daten abnehmen, BEVOR die Skills umgebaut werden.
**Quellen:** `git worktree list --porcelain` (2026-09-23), `WORKFLOW_STATUS.md` @ `4f1ea74` (2026-09-22)
und @ `5666554` (2026-09-23), Session-Logs `dtb-project/project-changelog/`.
Zeilen mit **[Attrappe]** sind erfundene Faelle zur Formdemonstration (L57), alles andere ist echt.

---

## (a) Worktree-Block — `workflow-next` / `workflow-resume` / `backlog-status` (§10)

Echter Stand, gelesen aus dem Haupt-Checkout:

```
In Worktrees:
  statusverlust-luecken  interaktiv (pane)  feature/statusverlust-luecken  frisch  4 uncommitted  Progress 5/21
```

- `frisch`: Branch-Reflog hat nur `branch: Created from HEAD` — noch kein eigener Commit
- `Progress 5/21` stammt aus dem Worktree-Pfad (uncommittete Flips); `git show` haette `0/21` gezeigt

Weitere Zustaende zur Form **[Attrappe]**:

```
In Worktrees:
  statusverlust-luecken  interaktiv (pane)   feature/statusverlust-luecken  +4 Commits, zuletzt 2026-09-23  0 uncommitted  Progress 12/21
  idea-rank              interaktiv (pane)   feature/idea-rank              gemergt → aufraeumen (git worktree remove ../.dtb-worktrees/pane-idea-rank)
  lessons-sweep          autonom (subagent)  detached @5666554              3 uncommitted  worker-report vorhanden
  artikel-sdd            verwaist → git worktree prune
  xyz                    interaktiv (pane)   feature/xyz                    frisch  0 uncommitted  Discovery  ⏳
```

---

## (b) `## Offene Aufgaben` mit `seit` und ⏳ — `WORKFLOW_STATUS.md` (§9.1, §9.4, §9.5)

Echte Liste vom 2026-09-23, erster Checkpoint nach Einfuehrung → Daten rekonstruiert aus dem
ersten Log-Auftreten (`≤`), Schwelle 7 Tage:

```markdown
## Offene Aufgaben

- [ ] **`/dtb:idea-review` fortsetzen** — Kontext: 10 offene Ideen, Start bei #97 (seit ≤2026-07-11) ⏳
- [ ] **TypeSafe-Key rotieren (optional)** — Kontext: Key ueber „file changed"-Meldung in den Verlauf geraten (L71) (seit 2026-09-23)
- [ ] **INBOX #57/#97 um den Ergebnis-Stand ergaenzen** — Kontext: nur Hin-Verweis auf `task.md` (seit ≤2026-09-22)
- [ ] **Station 2 starten** — Kontext: 11 Policy-Zeilen in ~8 Skill-Dateien; Voll-Schiene (L70) (seit ≤2026-09-21)
- [ ] **`/dtb:archive rueckfragen-erhebung`** — Kontext: erst NACH Station 2 (seit ≤2026-09-22)
- [ ] **`/dtb:idea-triage`** — Kontext: 47 ungesichtet; #70/#54 vorher von bare Pipes befreien (seit ≤2026-09-09) ⏳
- [ ] **Veraltete TTS-Dateien loeschen + Sprachausgabe einrichten** — Kontext: 3 Dateien (L58) (seit ≤2026-09-11) ⏳
```

Die zugehoerige Sammelvorlage im Checkpoint:

```
⏳ 3 offene Aufgabe(n) liegen ≥ 7 Tage:
  1. /dtb:idea-review fortsetzen (seit ≤2026-07-11, 74 Tage)
  2. /dtb:idea-triage (seit ≤2026-09-09, 14 Tage)
  3. Veraltete TTS-Dateien loeschen + Sprachausgabe einrichten (seit ≤2026-09-11, 12 Tage)
„passt" = alle behalten · je Zeile: „{Nr} erledigt" | „{Nr} verwerfen: {Grund}" · „Abbruch"
```

Nach „passt" → `(seit ≤2026-07-11 · behalten 2026-09-23)`; naechste Frage fruehestens 2026-09-30.

**Beobachtung fuer die Abnahme:** `/dtb:idea-review` taucht zuerst 2026-07-11 auf — das kann eine
fruehere, laengst abgeschlossene Serie derselben Formulierung sein. Das `≤` kennzeichnet genau
diese Unsicherheit; die Regel rekonstruiert nur einmal (erster Checkpoint), danach laeuft `seit` exakt.

---

## (c) `### Aufgaben-Abgaenge` — Session-Log (§9.2, §9.3)

Echter Vergleich `WORKFLOW_STATUS.md` 2026-09-22 (`4f1ea74`) → 2026-09-23 (`5666554`). Heute sind
dabei **7 alte Punkte → 6 weitergetragen, 1 ohne Spur verschwunden**, 1 neu:

- weitergetragen (umformuliert, `seit` wandert mit): idea-review, #57/#97, Station 2, archive,
  idea-triage, TTS
- neu: TypeSafe-Key rotieren
- **verschwunden ohne Vermerk:** „Fremder Ordner `..\.dtb-worktrees\pane-artikel-sdd-was-ist-das`"
  — der Ordner existiert nicht mehr, der Log 2026-09-23 erwaehnt ihn nicht (0 Treffer). Genau Luecke (2).

Die Session belegt die Erledigung nicht → der neue Checkpoint haette nachgefragt („Fremder Ordner
— erledigt oder verwerfen?"). Ergibt die Rueckfrage „erledigt", steht im Log:

```markdown
### Aufgaben-Abgaenge
- erledigt: Fremder Ordner `..\.dtb-worktrees\pane-artikel-sdd-was-ist-das` klaeren (seit ≤2026-09-21)
```

Weitere Formen **[Attrappe]**:

```markdown
### Aufgaben-Abgaenge
- verworfen: Sprachausgabe auf dem Arbeitsrechner einrichten (seit ≤2026-09-11) — Grund: Arbeitsrechner nutzt kein TTS
- aufgegangen in „Veraltete TTS-Dateien loeschen + Sprachausgabe einrichten": Veraltete TTS-Dateien loeschen (seit ≤2026-09-12)
```

---

## (d) „Ausgearbeitet, Change fehlt" — `archive` / `workflow-next` (§8)

**[Attrappe]** INBOX-Zeile: `| 999 | 2026-09-23 | Probe-Idee … → als Aufgabe geroutet (2026-09-23); task.md ausstehend — /dtb:task 999 | Ausgearbeitet |`

`dtb:archive`, Schritt 3:

```
Archiv-Kandidaten gefunden:

Inbox:
  - #88 "…" (Verworfen)

Nicht archiviert — Change fehlt:
  - #999 "Probe-Idee …" (Ausgearbeitet, kein gueltiger Change-Link) → /dtb:task 999
```

`dtb:workflow-next`, Uebersicht:

```
| #999 Probe-Idee | Ausgearbeitet, Change fehlt | /dtb:task 999 |
```

`dtb:idea-rank`, unter der Tabelle:

```
offen, Change fehlt: #999 → /dtb:task 999
```

---

**Erstellt mit:** `/dtb:implement` (Schritt 1.5)
