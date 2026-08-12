# Discovery: Parallele Sessions
<!-- resume: done -->

**Erstellt:** 2026-08-11 (abgeschlossen 2026-08-12)
**Idee-Referenz:** Inbox #42 — "Parallele Sessions in einem Projekt mit dem Workflow-Kit ermoeglichen: native CC-Worktree-Tools, Guard fuer global schreibende Skills, Lese-Seiten-Problem bei Parallelitaet (inkl. projektuebergreifender Schreiber)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-workflow-checkpoint/SKILL.md | Global schreibend (Status, Backlog, Changelog) → Guard-Kandidat |
| skills/dtb-idea/SKILL.md | Global schreibend (INBOX inkl. Nummernvergabe) → Guard-Kandidat |
| skills/dtb-idea-review/SKILL.md | Global schreibend (INBOX-Status) → Guard-Kandidat; zugleich Lese-Seite (liest, dann entscheidet — belegter Vorfall 2026-08-11) |
| skills/dtb-archive/SKILL.md | Global schreibend (git mv, ARCHIVE_LOG, Backlog/Status) → Guard-Kandidat |
| skills/dtb-lesson/SKILL.md | Global schreibend (lessons.md append + Nummernvergabe) → Guard-Kandidat |
| skills/dtb-meeting-dump/SKILL.md | Global schreibend (Zwischenstaende in discovery/spec) → Guard-Kandidat |
| skills/dtb-open-question/SKILL.md | KEIN Guard (schreibt nur features/* — worktree-sicher); wird in der Konvention explizit als worktree-faehig gefuehrt |
| skills/dtb-workflow-resume/SKILL.md | Lese-Seite: liest Status/INBOX/Artefakte und gibt Handlungsempfehlung — Lesestand-Frage |
| skills/dtb-worker/SKILL.md | Prior Art: einziger Skill mit Worktree-Mechanik (Isolation, Kollisionsregel, Schreibgrenze F1) |
| skills/dtb-task/SKILL.md | Guard-Skill (produces: BACKLOG.md — schreibt global, per Frontmatter belegt) |
| skills/dtb-bug-report/SKILL.md | Guard-Skill (produces: BACKLOG.md — schreibt global, per Frontmatter belegt) |
| workflow.config.yaml | Neuer Key (Default-Branch / Guard-Konfiguration), Kandidat lt. Nachtrag |
| skills/dtb-project-init/SKILL.md | Verteilt die Config als Seed — neuer Key muss im Template mitkommen |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §1.3 entschaerft die Anzeige-Seite; ggf. neuer § fuer Parallelitaets-Regeln (Seed-Skew #22!) |
| skills/CLAUDE.md | Traeger der kitweiten Konvention (welche Skills worktree-faehig, welche nicht) |

Bewusst NICHT aufgenommen: `dtb-feature-discover`/`dtb-impl-plan`/`dtb-implement` (laut
Nachtrag ausdruecklich worktree-faehig, keine Aenderung); `EnterWorktree`/`ExitWorktree`
(CC-native Tools, kein Kit-Artefakt — Referenzquelle, siehe Einschraenkungen).

---

## Anforderungen

### Scope
**Enthalten:**
- **(A) Schreib-Guard:** Die 7 global schreibenden Skills (workflow-checkpoint, idea,
  idea-review, archive, lesson, meeting-dump, open-question) brechen ab oder warnen, wenn
  sie in einem verlinkten Worktree laufen (Erkennung: `git rev-parse --git-dir` ≠
  `--git-common-dir`)
- **(B) Lese-Seite:** Antwort auf veraltete Lesestaende bei Parallelitaet (Re-Read/
  mtime-Pruefung vor Statusentscheidungen, Lesestand im Report) — mindestens fuer
  `idea-review` und `workflow-resume`
- **(C) Konvention + Doku:** Welche Skills sind worktree-faehig, welche nicht — festgehalten
  in `skills/CLAUDE.md`, ggf. `DERIVED_STATE_RULES.md`; Empfehlung der nativen
  CC-Worktree-Tools als dokumentierter Weg. Erweitert um das **Orchestrator-Muster**
  (siehe Gewuenschtes Verhalten): genau eine Orchestrator-Session pro Projekt-Checkout
  als Regel
- **(D) Hand-off Worker → Orchestrator (nachgezogen in 3c):** Standardisierter,
  status-neutraler Hand-off-Block, den eine Worktree-Session am Ende produziert
  (Session-Inhalte checkpoint-fertig), plus **Empfangsseite** in `workflow-checkpoint`
  (fremden Session-Block als Eingabe annehmen — heute schoepft der Checkpoint nur aus der
  eigenen Konversation). Primaerer Transport: **Herdr** (Session-zu-Session-Kommunikation,
  Worker-Pane → Orchestrator-Pane — erklaertes Zielbild des Nutzers); Fallback ohne Herdr:
  Text-Echo in der Guard-Abbruchmeldung, manuell getragen

**Nicht enthalten:**
- Keine aktive Worktree-Orchestrierung (kein Skill, der Worktrees anlegt/verwaltet — das
  machen die CC-nativen Tools bzw. `dtb:worker` fuer seinen Fall selbst)
- Keine Locking-/Merge-Mechanik fuer die globalen Dateien (kein File-Lock, keine
  automatische Changelog-Zusammenfuehrung — nur Erkennen und Melden)
- Kein Schutz gegen externe Schreiber auf Dateisystem-Ebene (der pkp-Fall wird ueber die
  Lese-Seite adressiert, nicht verhindert)

### Gewuenschtes Verhalten
- **Guard-Verhalten (A): einheitlicher harter Abbruch fuer alle Guard-Skills — keine
  Nachfrage, keine Differenzierung nach Skill-Typ.** Begruendung: (1) gerade die
  Capture-Skills tragen die belegten Kollisionen (Nummernvergabe #44/#34; `lessons.md`
  ungetrackt → Worktree-Schreiben geht beim Aufraeumen ersatzlos verloren); (2) eine Regel
  statt zwei — der Guard wird in 7 SKILL.md gespiegelt, jede Differenzierung vergroessert
  die Spiegel-Kopplungs-Flaeche; (3) das Verlust-Argument loest die Abbruchmeldung selbst:
  sie gibt den erfassten Text als fertigen Befehl fuers Haupt-Checkout zurueck
  (`/dtb:idea "…"`, Pfad aus `git rev-parse --git-common-dir`)
- **Lese-Seiten-Verhalten (B): still bei Uebereinstimmung, ⚠-Zeile + Re-Read bei
  Abweichung.** Pruefzeitpunkt: unmittelbar vor jeder Statusentscheidung (idea-review: vor
  jedem Status-Schreiben; workflow-resume: vor der Report-Ausgabe). Mechanik: mtime der
  gelesenen Datei gegen den Lesezeitpunkt (ein `stat`, kein Inhalt). Bei Treffer: neu
  lesen, ⚠-Zeile („{Datei} wurde seit dem Einlesen geaendert ({mtime}) — Stand neu
  geladen"), mit frischem Stand weiterarbeiten. Kein Abbruch, keine Nachfrage — Lesen ist
  ungefaehrlich, nur der veraltete Stand ist das Problem; der Nutzer erfaehrt aber, DASS
  parallel geschrieben wurde (§1.3-Ton: nicht blockieren, melden). Bewusste Restluecke:
  Race zwischen Pruefung und eigenem Schreiben bleibt (vollstaendig schliessen = Locking =
  Nicht-Ziel) → Randfall 3c
- **Uebernommene Muster (alle drei):** (1) `dtb:commit-and-push` — mechanisch pruefen
  statt Namen/Config vertrauen: Guard-Erkennung ausschliesslich ueber `git rev-parse
  --git-dir` vs. `--git-common-dir`, nie ueber Pfad-Konventionen oder Config-Flags.
  (2) §1.3-Konfliktmeldungs-Ton fuer die Lese-Seite — melden statt blockieren, eine
  ⚠-Zeile, frischer Stand gewinnt. (3) `dtb:worker`-Schreibgrenze (F1) verallgemeinern —
  `skills/CLAUDE.md` formuliert EINE Schreibgrenzen-Regel („im Worktree entstehen nur
  Feature-Artefakte, globale Dateien erreicht nichts vor der Abnahme/dem Haupt-Checkout"),
  auf die `dtb:worker` UND der neue Guard verweisen; keine zwei getrennt gepflegten
  Formulierungen (Spiegel-Kopplungs-Risiko)
- **Orchestrator-Muster (Zielbild, aus 3c):** Genau EINE Session im Haupt-Checkout
  (Orchestrator, einziger Schreiber der globalen Dateien), N Worker-Sessions in eigenen
  Worktrees. Worker uebergeben ihre Session-Inhalte als Hand-off-Block an den
  Orchestrator, der Orchestrator fuehrt den Checkpoint aus. Der Guard erzwingt maschinell,
  was das Muster verabredet — konsequente Form des „eine Anlaufstelle"-Vorschlags.
  Umgebung des Nutzers: Herdr (Terminal-Multiplexer, Sessions koennen kommunizieren)

### Randfaelle
- **Kein Git-Repo:** `git rev-parse` schlaegt fehl → kein Worktree moeglich → Guard
  schweigt, Skill laeuft normal (Fehlschlag der Erkennung = Durchlass, kein Abbruch;
  Kit unterstuetzt Nicht-Git-Projekte, vgl. `dtb:archive`-Fallback)
- **Race-Restluecke:** mtime-Pruefung faengt den Schreiber zwischen Lesen und Entscheiden,
  nicht den waehrend des eigenen Schreibens — bewusst offen, Locking ist Nicht-Ziel
- **mtime geaendert, Inhalt gleich** (touch/Checkout): mtime ist nur der billige Trigger;
  Re-Read + Inhaltsvergleich entscheidet ueber die Meldung (keine bzw. abgeschwaechte
  ⚠-Zeile bei identischem Inhalt)
- **Geprueffte Datei existiert nicht mehr** (parallel archiviert/verschoben): wie
  Abweichung behandeln — ⚠-Zeile, mit dem neuen Zustand weiterarbeiten („Eintrag
  inzwischen archiviert, Entscheidung hinfaellig")
- **`dtb:worker`-Worktrees:** Worker fassen laut eigener Regel nie globale Dateien an —
  der Guard ist dort ein zweites Netz, kein Sonderfall
- **Checkpoint aus der Worktree-Session:** gewollter Abbruch; geloest ueber (D) — die
  Session produziert den Hand-off-Block, der Orchestrator checkpointet. Ohne Herdr:
  Text-Echo in der Abbruchmeldung + Hinweis „erst mergen/abnehmen, dann im
  Haupt-Checkout checkpointen"
- **Parallelitaet ohne Worktree** (zwei Terminals im selben Checkout; Fremdprojekt
  schreibt in globale Dateien, pkp-Fall 2026-08-11): der Guard erkennt nur Worktrees und
  feuert hier NICHT. Antwort: Orchestrator-Konvention als Leitplanke (macht den Fall zur
  Regelverletzung statt zur stillen Luecke), Lese-Seite (B) als Auffangnetz, Rest
  dokumentierte Grenze

### Einschraenkungen
- **Verteil-Realitaet (Klasse A):** Der Guard reist via `kit-sync` in ALLE Projekte — in
  Projekten ohne Parallelitaet muss er unsichtbar sein (no-op, keine Rueckfrage, kein
  Rauschen). Der neue Config-Key ist **optional mit Default**: Bestandsprojekte tragen den
  alten Seed und bekommen ihn nie automatisch (Seed-Skew #22 — sonst entsteht hier der
  siebte Fall)
- **Zwei Plattformen:** mtime-Pruefung und `rev-parse` muessen unter Windows und POSIX
  laufen — keine einseitigen Shell-Konstrukte
- **Herdr-Verfuegbarkeit:** Herdr nur bei `HERDR_ENV=1` ansprechbar — das Hand-off-Design
  degradiert ohne Herdr auf das Text-Echo (definierter Fallback, kein Sonderpfad-Wildwuchs)
- **Fachlich:** Derived-State-Prinzip unangetastet — der Guard schuetzt die NICHT
  ableitbaren Inhalte; fuer ableitbare gilt weiter §1.3 (naechster Checkpoint
  regeneriert). Kein zweiter Speicherort, kein Lock-File als Zustand
- **Umsetzungsebene: Skill-Anweisung, KEIN Hook.** Der Guard wird vom Modell ausgefuehrt
  und haengt an der Anweisungsbefolgung (bekannte Grenze). Die Haertung per
  PreToolUse-Hook ist mechanisch zuverlaessiger, aber exakt Idee #45 (Hooks im Kit,
  inkl. Verteilweg-Frage) — bewusst NICHT hier mitentschieden; Spec-Notiz
  „Haertung per Hook = #45-Kandidat" genuegt

### Integrationspunkte
- **Finale Guard-Liste: 8 Skills** (Praezisierung der INBOX-Annahme „7") —
  `workflow-checkpoint`, `idea`, `idea-review`, `archive`, `lesson`, `meeting-dump`,
  `task`, `bug-report`. Aenderungen gegenueber dem Nachtrag: `open-question` RAUS
  (produces nur `features/*` — worktree-sicher, in Konvention (C) explizit als
  worktree-faehig fuehren), `task` + `bug-report` REIN (produces `BACKLOG.md`, per
  Frontmatter belegt). `meeting-dump` bleibt: verteilt quer ueber mehrere Feature-Ordner,
  im Worktree stuenden fremde Ordner im falschen Branch-Stand — Meeting-Nachbereitung ist
  Orchestrator-Arbeit
- **Arbeitsteilung (bestaetigt):** Guard-Skills laufen nur in der Orchestrator-Session
  (Haupt-Checkout, einziger globaler Schreiber); Worker-Sessions fahren alles, was nur
  den eigenen Feature-Ordner anfasst (implement, impl-plan, feature-discover, debug-plan,
  impl-review, open-question); Read-only-Sichten laufen ueberall (Guard betrifft nur
  Schreiben)
- **Beruehrungen mit offenen Ideen (dokumentieren, nicht mitloesen):** #35 (Empfangsseite
  (D) fasst `workflow-checkpoint` an — dasselbe File wie die Handoff-Gueltigkeits-Idee,
  Reihenfolge bei paralleler Bearbeitung klaeren) · #48 (Duplikat-Schutz Capture-Skills —
  der Guard entschaerft dessen INBOX-Fall teilweise) · #56 (Changelog-Zusammenfuehrung
  zweier Sessions am selben Tag — bleibt Nicht-Ziel, Nachbar der Empfangsseite) · #45
  (Hook-Haertung, notiert in 3d) · #62 (Worker-Notiz-Ort) · #63/#64
  (Maschinen-Parallelitaet — dieselbe Familie, andere Achse)
- **Externe Abhaengigkeiten:** Herdr (`HERDR_ENV=1`, primaerer Hand-off-Transport);
  CC-native Worktree-Tools (`EnterWorktree`/`ExitWorktree`, Subagents mit
  `isolation: worktree` — Referenz, keine Kit-Artefakte); Git mit Worktree-Support.
  Keine APIs/Services

---

## Abhaengigkeiten

- **Keine Datei-Konflikte** mit den vier bestehenden Features (`feature-fast`,
  `output-style-gezielt`, `feature-start-statusfeld`, `meeting-agenda` — alle „Fertig zum
  Testen", Restarbeit sind Abnahmen, keine Edits an unseren Modulen)
- **Thematische Ueberschneidung `feature-start-statusfeld`:** dieselbe Familie — dort
  wurde der Start-Seite das Status-Behaupten abgewoehnt, hier bekommen die globalen
  Dateien einen einzigen Schreiber. In der Spec als Verwandtschaft nennen
- **Ideen-Beruehrungen:** siehe Integrationspunkte (#35, #48, #56, #45, #62, #63/#64)

---

## Offene Punkte

- Guard-Zugehoerigkeit von `dtb:feature-start` haengt an #52: es enthaelt noch
  Schreib-Anweisungen auf die WORKFLOW_STATUS-Sektion „Laufende Arbeit", die ins Leere
  gehen (Sektion existiert nicht mehr) — tote Anweisung, Bereinigung gehoert zu #52;
  wird dort die Sektion wieder eingefuehrt, ist `feature-start` der neunte Guard-Kandidat
- Konkretes Format des Hand-off-Blocks (D) — Spec-Arbeit: welche Felder braucht die
  Empfangsseite von `workflow-checkpoint` mindestens (Erledigt/Entscheidungen/Dateien/
  Naechste Schritte?), status-neutral nach §1.1
- Name und Default des neuen Config-Keys (Default-Branch/Guard-Konfiguration) — Spec-Arbeit,
  Constraint aus 3d beachten (optional mit Default, Seed-Skew #22)
- Reihenfolge mit #35 klaeren, falls #35 parallel angegangen wird (beide fassen
  `workflow-checkpoint` an)

---

**Erstellt mit:** `/dtb:feature-discover`
