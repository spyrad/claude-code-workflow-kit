# Feature Backlog

**Letzte Aktualisierung:** 2026-08-13 (`/dtb:workflow-checkpoint` Session 1, Sitzung ueber drei Tage 08-11 bis 08-13: **`parallele-sessions` (#42) von der Idee bis 14/14 „Fertig zum Testen"** — Voll-Schiene komplett (Discovery → Spec → Plan → plan-review REVISE/4 WARNs behoben → 5 Phasen `7009da6`…`f91b8d5` → impl-review REJECTED mit 10 Findings, alle behoben `746b810`). Kernstueck: Schreibgrenzen-Regel + Orchestrator-Muster in `skills/CLAUDE.md`, Worktree-Guard in 8 Voll-Guard- und 3 Teil-Guard-Skills, Lesestand-Pruefung in `idea-review`/`workflow-resume`, Worktree-Hand-off mit Empfangsseite im Checkpoint, Config-Key `parallel.default_branch`. Guard-Liste zweimal per `produces`-Frontmatter korrigiert (7 → 8 + 3 Teil-Guards, L1 in Reinform); Guard-Erkennung auf cd/pwd-Normalisierung umgestellt, weil `--path-format` erst ab Git 2.31 existiert (hier 2.28) → L24; Spiegel-Zaehlung scheiterte an gemischten Zeilenenden → L25. Kit verteilt, Lock @ `746b810`, 46 Artefakte synchron. Status bewusst NICHT „Abgenommen": die Herdr-Uebergabe ist noch nicht real belegt. Davor 2026-08-11 (`/dtb:workflow-checkpoint` Session 1: Lese- und Sicherungs-Sitzung, nichts implementiert — Status-Spalte unveraendert, alle vier Features weiter `Fertig zum Testen`. `/dtb:workflow-resume` belegte den **Handoff-Verfall zum zweiten Mal** (Bedingung „solange `git status` nicht leer" war verfallen, der mitgeschriebene Nachfolge-Schritt griff ohne Nacharbeit → #35/L23). `/dtb:idea-review` nach der Uebersicht abgebrochen, **keine** Statusentscheidung, 34 Eintraege weiter `Offen`. Kernbefund: eine **parallele Session im pkp-Projekt** schrieb 08:56:44 einen Nachtrag an INBOX **#42** (native CC-Worktree-Tools, Derived-State-Analyse, Guard ueber `git-dir` ≠ `git-common-dir`) — mitten in dieser Sitzung, der Lesestand war zwei Minuten nach der Ausgabe veraltet; #42 belegt sich damit selbst, und zwar auf der **Lese**-Seite, die der Guard nicht deckt. Nachtrag als `6d3f619` committet, `/dtb:commit-and-push` uebersprang korrekt den Commit-Schritt (clean, `ahead 1`) und pushte nur. Verlustpruefung 3 Funde, **alle noch offen**. Davor 2026-08-10 (`/dtb:workflow-checkpoint` Session 1: Maschinen-Nachlauf auf dem zweiten Rechner. `gitattributes-eol` Schritt 6 belegt → **6/6, erledigt und archiviert** (`git status` leer bei 196x `i/lf` trotz `core.autocrlf=true`); `kit-sync` war dabei faellig und lief von 44 @ `3d15d0a` auf **46 @ `f0c204a`** — zwei Laeufe noetig, weil die installierte kit-sync-Fassung die neue Klasse `output-styles/` noch nicht kannte (→ L22); Sicherungs-Branch `backup/2026-08-03-pre-merge` geloescht. `/dtb:archive` verschob `autonome-schiene` (11/11, abgenommen) und `gitattributes-eol` (6/6) als ganze Ordner — INBOX hatte keine Kandidaten. Verlustpruefung 5 Funde, **alle abgesetzt**: #64 (`lessons.md` endet auf dieser Maschine bei L14, L15-L21 nie angekommen — erster Schadensbeleg zu #34), #65 (`dtb:archive` 4d/4e tragen den heutigen Archivierungsweg nicht), #66 (Kit-Stand-Kennzahl misst maschinenlokal), L22, L23. Davor 2026-08-09 (`/dtb:workflow-checkpoint` Session 2: `autonome-schiene` **abgenommen** — Restabnahme aller vier `#### Manual`-Kriterien, dabei aufgefallen, dass das 3.3-Pruefprotokoll nie abgelegt worden war (Schritt seit `a59662b` abgehakt, Output nirgends) → gegen `4d16740` nachgeholt, 8 Treffer bewertet, keine neue Zustandsaussage ohne Pfleger. `/dtb:archive` verschob INBOX #49/#43 und die Aufgabe `pipeline-kanten-reziprok` (4/4). `gitattributes-eol` bleibt 5/6, aber entschaerft: drei Clones mit `core.autocrlf=true|false|input` zeigen je 0 modified — das Konfigurations-Risiko ist ausgeschlossen, offen bleibt nur die Beobachtung auf dem anderen Rechner. Commits `edca1e0`, `c56abff`. Davor Session 1: die autonome Lane erstmals komplett durchlaufen — Worker-Lauf `pipeline-kanten-reziprok` gruen nach 1 Versuch (7 Min), Diff abgenommen, `a79c218` gepusht, Kit auf `a79c218` gesynct; Aufgabe damit 4/4 = Erledigt. Zwei Befunde ueber die Lane: die Auftragsdatei muss vor dem Start committet sein (L18), und die #46-Fehlerklasse reproduziert sich weiter (#58). Davor 2026-08-08 `/dtb:task`: `pipeline-kanten-reziprok` aus INBOX #46 erfasst — Teil-Routing, nur die Bestandsbereinigung. Davor `/dtb:feature-plan`: `autonome-schiene` (#43, zusammengelegt mit ex-#49) spezifiziert — Discovery + Spec in einer Session; Erkennungs-Sicht + autonome Ausfuehrung zwischen Freigabe und Abnahme. Davor 2026-08-07 (`/dtb:workflow-checkpoint` Session 3: `feature-start-statusfeld` (#50) **an einem Nachmittag von der Triage bis 5/5** — Fast-Track, plan-review REVISE (4 WARNs behoben), zwei Phasen (`43e9c9a`, `4047ea3`), impl-review **REJECTED** wegen eines blocking Findings (der Skill setzte dieselbe Fehlerklasse neu ein, die er abschafft) → alle 9 Findings gefixt. Ausgelagert: #52, #53, #54; neu erfasst L15/L16. Kit-Verteilung der Triage-Fixes steht noch aus. Davor Session 2: `output-style-gezielt` (#40) **11/11 fertig zum Testen** — Kalibrier-Abnahme 5/5 in frischer Session (Fall-Set a-e, inkl. Gegenprobe `workflow-next` und Ausnahme-Klausel), Abschluss-Verteilung, danach `impl-review`: Plan Adherence 7/7 MATCH, 0 EXTRA, 9 Findings (0 blocking) allesamt gefixt, Kit gesynct auf `1758671` mit 45/45 synchron. Neu erfasst: L13/L14 und INBOX #51. Davor Session 1: von der Idee bis 9/11 — Discovery, Spec, Plan (reviewt REVISE → 4 WARNs behoben), Phasen 1+2 komplett inkl. Wegwerf-Test der neuen kit-sync-Klasse, Check 12 + Aktivierung; es fehlt die Kalibrier-Abnahme (3.3, braucht frische Session) + Abschluss-Verteilung (3.4). Davor 2026-08-06 (`/dtb:workflow-checkpoint` Session 3): `no-loss-check` (#29) **abgenommen** — an einem Tag von der Spec bis zur Abnahme, 11/11, fuenf Commits bis `3d15d0a`, drei Review-Laeufe mit 27 behobenen Findings, Kalibrierung 5/5, zwei produktive Laeufe ohne Falsch-Positive. Damit Archiv-Kandidat. Davor am selben Tag spezifiziert und von `no-loss-gate` umbenannt, weil „Gate" eine Blockade versprach, die der Skill bewusst nicht leistet. Davor 2026-08-05: `/dtb:task` erfasste `gitattributes-eol` aus INBOX #28; 2026-08-04: `/dtb:archive` — 6 abgenommene Features nach `archive/`, Details `archive/ARCHIVE_LOG.md`. Aktiv bleiben `feature-fast` + `meeting-agenda`, beide Fertig zum Testen, Restabnahmen offen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |
| output-style-gezielt | Fertig zum Testen | Mittel | features/output-style-gezielt/spec.md | Eine global geltende, schaltbare Stil-Vorgabe als versioniertes Kit-Artefakt ausliefern, die Claudes Fliesstext auf Orientierung statt Vollstaendigkeit ausrichtet — worum es geht, was der Stand ist, was zu entscheiden ist; Gegner sind Vorwegnahme und Redundanz, nicht Erklaerung |
| feature-start-statusfeld | Fertig zum Testen | Hoch | features/feature-start-statusfeld/spec.md | `dtb:feature-start` schreibt keine Anzeigefelder mehr — der Start behauptet keinen Status, den die Ableitung nicht traegt, damit die Feld-Konfliktmeldung wieder ein Befund ist statt Dauerrauschen (INBOX #50, via Fast-Track) |
| parallele-sessions | Fertig zum Testen | Hoch | features/parallele-sessions/spec.md | Parallele Sessions ohne Verlustrisiko an den globalen Dateien: Schreib-Guard fuer 8 global schreibende Skills (Abbruch im Worktree), Lesestand-Pruefung vor Statusentscheidungen, Orchestrator-Konvention + Hand-off Worker→Orchestrator mit Empfangsseite in workflow-checkpoint (INBOX #42) |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|

---

## Status-Legende (abgeleitet aus Artefakten)

| Status | Abgeleitet aus |
|--------|----------------|
| Idee | Nur INBOX-/BACKLOG-Eintrag, keine Artefakte |
| In Discovery | discovery.md existiert, kein spec.md |
| Spezifiziert | spec.md existiert, kein plan.md |
| Geplant | plan.md existiert, 0 Progress-Checkboxen |
| In Arbeit | `## Progress` teilweise abgehakt (X/Y) |
| Fertig zum Testen | Alle Schritte abgehakt |
| Abgenommen | Explizit gesetzt (getestet und freigegeben) |
| Abgeschlossen | Explizit via `/dtb:archive` |
| Pausiert | Explizit gesetzt, ueberschreibt Ableitung |

## Prio-Legende

| Prio | Bedeutung |
|------|-----------|
| Kritisch | Blocker, sofort umsetzen |
| Hoch | Naechster Sprint |
| Mittel | Backlog, bei Kapazitaet |
| Niedrig | Nice-to-have |
