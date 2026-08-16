# Feature: Herdr-Worker-Automation

**Erstellt:** 2026-08-16
**Ziel:** Die Orchestrator/Worker-Uebergaben (1:n) laufen automatisch — der Mensch trifft nur noch zwei Entscheidungen: Freigabe der Aufgaben-Zuteilung am Anfang, Abnahme des Diffs am Ende.
**Prioritaet:** Hoch
**Status:** Abgenommen <!-- explizit gesetzt 2026-08-16 (dtb:workflow-checkpoint) — Beleg: E2E-Queue-Durchlauf 2 Aufgaben/1 Worker, Bloecke automatisch, Negativ-Test gefangen -->

---

## Executive Summary

Feature #42 (parallele-sessions, abgenommen 2026-08-16) hat Schreibgrenze, Worktree-Guard
und den WORKTREE-HANDOFF-Block etabliert — aber jede Uebergabe ist Handarbeit: Pane
wechseln, Verzeichnis wechseln, Session starten, Auftrag kopieren, Block zuruecktragen.
Der reale Abnahme-Lauf vom 2026-08-16 hat belegt, dass beide Kommunikationsrichtungen
zwischen Orchestrator- und Worker-Pane automatisierbar sind (Herdr-Session-Kommunikation
<!-- Lint-Override: Herdr ist die reale Arbeitsumgebung des Nutzers (Terminal-Multiplexer
mit Session-Kommunikation) und als Traeger eine bewusste Scope-Entscheidung (Randfall
„Kein Herdr" → Gate), kein Implementierungsdetail -->). Dieses Feature automatisiert den
kompletten Lebenszyklus autonomer Worker-Aufgaben: Hinweg (Worktree + Pane + Worker +
Auftrag), Rueckweg (Hand-off-Block kommt automatisch zurueck) und Abschluss (Merge nach
Abnahme, Aufraeumen) — auf dem Fundament von #42, ohne es umzubauen.

---

## Scope / Abgrenzung

### Enthalten

- **(a) Hinweg:** Der Orchestrator legt pro freigegebener Aufgabe einen Worktree an,
  oeffnet eine Pane (`herdr pane split`), startet den Worker (`herdr agent start`) und
  uebergibt den Auftragstext per `herdr agent prompt`. Der Auftragstext traegt alles,
  was der Worker wissen muss: Worktree-Pfad, Change-Slug, Orchestrator-Pane-Adresse,
  Rueckkanal-Anweisung — KEINE Team-Registry, keine persistierten Pane-IDs
  (Zustandsaussage ohne Pfleger, #35-Familie); Rolle und Adressen leben im Auftrag
- **(b) Rueckweg:** Der Worker baut am Ende den WORKTREE-HANDOFF-Block nach dem Format
  aus seiner installierten Skill-Kopie und schickt ihn woertlich (inkl. Kopfzeile) per
  `herdr agent prompt` an die Orchestrator-Pane — Push, nie Pull (Einschraenkung
  „Alternate Screen")
- **(c) Abschluss:** Der Orchestrator verifiziert den Block gegen den Branch, meldet
  „Worker N fertig", der Mensch nimmt den Diff ab, der Orchestrator merged, checkpointet
  und entfernt Worktree + Pane
- **(d) Warteschlange:** Mehr Aufgaben als Worker → freier Worker bekommt die naechste;
  Reihenfolge aus der Abhaengigkeitsanalyse der bestehenden Erkennungs-Sicht, Aufgaben
  mit gemeinsamen Dateien laufen nie parallel

### Nicht enthalten

- **Keine autonome Aufgaben-Auswahl** — welche Eintraege worker-tauglich sind, bleibt
  die bestehende Erkennungs-Sicht von `dtb:worker` plus menschliche Freigabe
- **Kein Auto-Merge** — kein Merge ohne menschliche Diff-Abnahme
- **Keine Voll-Schiene im Pane-Worker** — nur autonome Tasks; Features mit
  Interview-Anteil bleiben ausserhalb dieses Scopes
- **Kein Umbau an #42** — Guard, Hand-off-Format und Empfangsseite von
  `dtb:workflow-checkpoint` bleiben unveraendert (die Block-Verifikation laeuft im
  Orchestrator VOR dem Checkpoint-Aufruf)
- **Keine stille Degradierung** — ohne Herdr bricht der Pane-Modus ab (Gate), er faellt
  nicht unbemerkt auf den Subagenten-Modus zurueck

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Herdr-CLI-Drift: Befehlssyntax (Stand 2026-08-16) aendert sich, Auftragstext bricht | Mittel | Mittel | Bewusst dokumentiertes Risiko (Discovery 3e), kein Laufzeit-Versionscheck; Befehle nur an EINER Stelle (Auftragstext-Vorlage) pflegen |
| Rueckkanal-Block beschaedigt/falsch (paraphrasiert, Kopfzeile fehlt, behaupteter Commit existiert nicht) | Mittel | Mittel | Branch-Verifikation im Orchestrator vor dem Checkpoint: Commit existiert, Diff-Dateiliste ↔ `Dateien:`-Feld; Abweichung melden, nicht raten |
| Worker haengt oder wartet in `blocked`, Rueckkanal kommt nie | Mittel | Mittel | Timeout aus `worker.max_minutes` (eine Quelle) + `herdr agent wait --until blocked` parallel; bei Ablauf/blocked: Pane lesen, melden, Mensch entscheidet — kein Auto-Stopp (umgeht zugleich #62) |
| `agent start` scheitert (belegter Argument-Bug, Timeout) | Mittel | Niedrig | Immer Dummy-Argument (umgeht den Bug deterministisch); 1 Retry mit laengerem Timeout, dann Abbruch mit Pane-Inhalt |
| Fremde Session im Haupt-Checkout (Guard-Grenze, real vorgefunden 2026-08-16) | Mittel | Mittel | Start-Pruefung via Agent-Liste + Verzeichnis-Vergleich → genau eine ⚠-Warnung mit Pane-ID, weiterarbeiten (§1.3: melden statt blockieren); kein hartes Verbot, da die Verzeichnis-Angabe stale-anfaellig ist (belegt) |
| Datei-Kollision bei parallelen Workern (zwei Aufgaben, gleiche Datei) | Niedrig | Hoch | Warteschlangen-Regel (d): gemeinsame Dateien nie parallel; Verhaeltnis zur bestehenden Kollisionsregel von `dtb:worker` ist offener Punkt fuer den Plan |

---

## Dependencies

### Erforderlich vor Start

- [x] #42 (parallele-sessions) abgenommen — Fundament steht (2026-08-16, archiviert)
- [ ] Traeger-Entscheid: Pane-Modus IN `dtb:worker` vs. eigener Skill (Offener Punkt,
      gehoert an den Anfang des Implementierungsplans)

### Referenz-Dokumente

- `features/herdr-worker-automation/discovery.md` — vollstaendige Discovery (5 einzeln entschiedene Randfaelle, Constraints, Integrationspunkte)
- `skills/dtb-worker/SKILL.md` — Traeger-Kandidat: Erkennungs-Sicht, Kollisionsregel, `worker:`-Config
- `skills/dtb-workflow-checkpoint/SKILL.md` — Hand-off-Format + Empfangsseite (bleibt unveraendert, ist aber der Konsument)
- `skills/CLAUDE.md` — Orchestrator-Muster + Schreibgrenzen-Regel (Pane-Worker als Variante dokumentieren)
- `dtb-project/project-workflows/archive/parallele-sessions/spec.md` — Fundament #42
- `dtb-project/project-changelog/2026-08/2026-08-16.md` — realer Abnahme-Lauf als Vorlage des Ablaufs; INBOX #67 — Herleitung + drei Test-Befunde

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] Eine freigegebene Aufgabe laeuft ohne Handarbeit an: ein Freigabe-Entscheid →
      Worktree angelegt, Pane geoeffnet, Worker gestartet (mit Dummy-Argument),
      Auftrag zugestellt
- [ ] Der Hand-off-Block kommt automatisch beim Orchestrator an (Push durch den Worker,
      Kopfzeile intakt) und die unveraenderte Empfangsseite konsumiert ihn
- [ ] Die Branch-Verifikation faengt einen abweichenden Block (fehlender Commit ODER
      Dateiliste ≠ Diff) mit einer Meldung — belegt durch einen Negativ-Test
- [ ] Ohne `HERDR_ENV=1` bricht der Pane-Modus mit Verweis auf Subagenten-Modus/manuellen
      Weg ab — keine stille Degradierung, kein Fehlerzustand
- [ ] Warteschlange belegt: mehr freigegebene Aufgaben als Worker → alle werden
      nacheinander abgearbeitet, Aufgaben mit gemeinsamen Dateien nie gleichzeitig
- [ ] Der Mensch beruehrt den Ablauf an genau zwei Punkten (Freigabe als blockierende
      Auswahlfrage, Diff-Abnahme vor dem Merge) — kein Auto-Merge
- [ ] `skills/dtb-workflow-checkpoint/SKILL.md` bleibt unveraendert (Diff = 0 gegen den
      Stand vor dem Feature)

---

## Offene Punkte

- Traeger endgueltig festlegen: Pane-Modus IN `dtb:worker` (Wiederverwendung von
  Erkennungs-Sicht, Kollisionsregel, Config-Block spricht dafuer) vs. eigener Skill —
  Entscheidung am Anfang des Implementierungsplans
- Aufraeum-Reihenfolge im Abschluss (c): Worktree entfernen nach Merge sofort oder erst
  nach dem Orchestrator-Checkpoint? (Real gegangener Weg 2026-08-16: nach Checkpoint +
  Worker-Session-Ende — Default-Kandidat)
- Kollisionsregel von `dtb:worker` bei n parallelen Panes: gilt sie woertlich oder
  braucht die Warteschlange (d) eine eigene Formulierung?
- Auftragstext-Vorlage: genauer Wortlaut (der Test-Auftrag vom 2026-08-16 als
  Ausgangspunkt) — Detailfestlegung im Implementierungsplan
- **Nachlauf NACH der Abnahme (impl-review F4, 2026-08-16):** In
  `skills/dtb-workflow-checkpoint/SKILL.md` (Hand-off-Block, Branch-Angabe) die Prosa
  „dtb:worker legt seine Worktrees mit `git worktree add {pfad} HEAD` an … also ohne
  Branch" um einen Satz ergaenzen: gilt fuer den Subagenten-Traeger; der Pane-Traeger
  nutzt `task/{slug}`-Branches. Bewusst ausserhalb des Diff-0-Fensters des Features

---

**Erstellt mit:** `/dtb:feature-plan`
