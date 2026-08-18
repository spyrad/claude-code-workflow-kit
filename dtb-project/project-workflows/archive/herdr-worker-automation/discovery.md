# Discovery: Herdr-Worker-Automation
<!-- resume: done -->

**Erstellt:** 2026-08-16
**Idee-Referenz:** Inbox #67 — "Orchestrator/Worker-Uebergaben ueber Herdr automatisieren (1:n)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-worker/SKILL.md | Kern-Kandidat als Traeger: Erkennungs-Sicht, Worktree-Anlage, Kollisionsregel, worker:-Config — Pane-Modus kaeme neben den Subagenten-Modus |
| skills/dtb-workflow-checkpoint/SKILL.md | Hand-off-Format + Empfangsseite (die eine Quelle) — Rueckweg muss dazu passen, vermutlich KEINE Aenderung |
| skills/CLAUDE.md | Orchestrator-Konvention + Schreibgrenzen-Regel — Pane-Worker als Variante des Musters dokumentieren |
| workflow.config.yaml | worker:-Block als Muster; ggf. neue Keys (Seed-Skew-Constraint #22) |
| skills/dtb-project-init/SKILL.md | Seedet die Config — nur betroffen, falls neue Keys kommen |
| (extern) ~/.claude/skills/herdr/ | Herdr-CLI-Skill — nicht Kit-Bestandteil, Befehls-Referenz fuer den Auftragstext |

---

## Anforderungen

### Scope
**Enthalten:**
- (a) Hinweg: Orchestrator legt pro freigegebener Aufgabe Worktree an, oeffnet Pane
  (`herdr pane split`), startet Worker (`herdr agent start`), uebergibt Auftragstext
  (Worktree-Pfad, Change-Slug, Orchestrator-Pane-Adresse, Rueckkanal-Anweisung)
- (b) Rueckweg: Worker ruft am Ende `/dtb:workflow-checkpoint`, Guard erzeugt den
  WORKTREE-HANDOFF-Block, Worker schickt ihn woertlich per `herdr agent prompt` an die
  Orchestrator-Pane (Anweisung steht im Auftragstext)
- (c) Abschluss: Orchestrator meldet "Worker N fertig", Mensch nimmt den Diff ab,
  Orchestrator merged, checkpointet, entfernt Worktree + Pane
- (d) Warteschlange: mehr Aufgaben als Worker → freier Worker bekommt die naechste;
  Reihenfolge aus der Abhaengigkeitsanalyse der Erkennungs-Sicht, Aufgaben mit
  gemeinsamen Dateien nie parallel

**Nicht enthalten:**
- Autonome Aufgaben-AUSWAHL — welche Eintraege worker-tauglich sind, bleibt die
  bestehende Erkennungs-Sicht von dtb:worker + menschliche Freigabe
- Auto-Merge — kein Merge ohne menschliche Diff-Abnahme
- Voll-Schiene im Pane-Worker — nur autonome Tasks (Features mit Interview-Anteil
  bleiben ausserhalb dieses Scopes)

### Gewuenschtes Verhalten
- Zwei Beruehrungspunkte fuer den Menschen: Freigabe der Zuteilung am Anfang, Diff-Abnahme
  am Ende — dazwischen laeuft alles automatisch, die Worker-Panes bleiben sichtbar
  (beobachtbar und unterbrechbar, im Unterschied zum blinden Subagenten-Modus)
- Einstieg uebernimmt die bestehende Erkennungs-Sicht von dtb:worker (Tabelle mit Urteil
  je Eintrag + Freigabe-Frage)
- Freigabe und Abnahme als blockierende Auswahlfrage (Muster dtb:commit-and-push,
  Abnahme-Befund 2026-07-30: Freitext-Bestaetigungen versanden)

### Randfaelle
(je einzeln entschieden, 2026-08-16)
- **Start-Fehler:** `herdr agent start` immer mit Dummy-Argument aufrufen (umgeht den
  belegten PowerShell-Bug `Start-Process -ArgumentList ''` von vornherein); bei Timeout
  genau 1 Retry mit laengerem Timeout, danach Abbruch mit Meldung + Pane-Inhalt
- **Worker meldet sich nie zurueck:** Timeout aus `worker.max_minutes` (eine Quelle, kein
  neuer Key). Bei Ablauf ODER `blocked` (billig fangbar via `herdr agent wait --until
  blocked` parallel zum Warten): Pane lesen, Zustand melden, Mensch entscheidet
  (weiterwarten / eingreifen / stoppen) — KEIN Auto-Stopp (vermeidet zugleich das
  ungeloeste #62-Problem des Notiz-Orts)
- **Beschaedigter/falscher Hand-off-Block:** bestehende Pflichtfeld-Pruefung der
  Empfangsseite + zusaetzlich Verifikation gegen den Branch (genannter Commit existiert,
  Diff-Dateiliste stimmt mit `Dateien:` ueberein — zwei git-Befehle); Abweichung melden,
  nicht raten. Der Block ist eine Behauptung, git ist die Wahrheit; faengt auch
  "vergessen zu committen"
- **Kein Herdr:** Eligibility-Gate auf `HERDR_ENV=1` — ohne Herdr ehrlicher Abbruch mit
  Verweis auf Subagenten-Modus bzw. manuellen Hand-off; KEINE stille Degradierung.
  #42 bleibt traegerneutral, nur der neue Pane-Modus ist Herdr-gebunden
- **Zweite Session im Haupt-Checkout** (Guard-Grenze, heute real vorgefunden): beim Start
  pruefen (`herdr agent list` + cwd); Fund → genau eine ⚠-Warnung mit Pane-ID, dann
  weiterarbeiten (§1.3: melden statt blockieren). Kein hartes Verbot — Herdrs cwd-Angabe
  ist der Pane-Start-Stand und nachweislich stale-anfaellig (heute belegt)

### Einschraenkungen
- **Alternate Screen (technisch, belegt 2026-08-16):** Der Rueckweg MUSS Push durch den
  Worker sein — `herdr agent read` verliert aus dem Sichtfenster gescrollten Text
  (Claude Code rendert auf dem Alternate Screen); Pull ist fuer den Hand-off unbrauchbar
- **Seed-Skew (#22):** Neue Config-Keys (falls noetig, z.B. Pane-Anzahl) optional mit
  Default — Verhalten ohne Key identisch zu heute; kein Pflicht-Feld
- **#42 bleibt unangetastet:** Pane-Modus baut auf Guard, Hand-off-Format und
  Empfangsseite auf — kein Umbau an diesen Bestandteilen
- **`disable-model-invocation` bleibt bestehen (fachlich):** Der Worker darf
  `/dtb:workflow-checkpoint` nicht aufrufen — der Auftragstext instruiert ihn, den
  WORKTREE-HANDOFF-Block nach dem Format aus der installierten Skill-Kopie zu BAUEN
  (lesen erlaubt, aufrufen nicht). Formalisiert den heute real gegangenen Weg,
  kein Eingriff in die Kit-Konvention

### Integrationspunkte
- **dtb:worker** — Traeger-Kandidat: Erkennungs-Sicht als Einstieg (3b), Kollisionsregel
  und `worker.max_minutes` (3c) werden wiederverwendet
- **dtb:workflow-checkpoint** — bleibt UNVERAENDERT: die Branch-Verifikation (3c) laeuft
  im Orchestrator VOR dem Checkpoint-Aufruf, ausserhalb des Skills; die Empfangsseite
  konsumiert wie bisher nur den Block
- **skills/CLAUDE.md** — Pane-Worker als Variante des Orchestrator-Musters dokumentieren
- **Extern: Herdr-CLI** — Eligibility-Gate `HERDR_ENV=1`; die Befehlssyntax entspricht
  dem Stand 2026-08-16. **Bekanntes Risiko (dokumentiert, kein Laufzeit-Check):** aendert
  Herdr seine CLI, bricht der Auftragstext — bewusst kein `--help`-Versionscheck beim Start

---

## Abhaengigkeiten

- Keine Konflikte mit den 4 aktiven Features (feature-fast, feature-start-statusfeld,
  meeting-agenda, output-style-gezielt — alle Fertig zum Testen, keines beruehrt
  dtb:worker, Hand-off oder Config)
- INBOX-Beruehrungen (in #67 vermerkt): #59 (Erkennungs-Sicht-Spalte „fehlender
  Entscheid" — gleiche Selektionsfrage), #62 (Notiz-Ort bei hartem Stopp — durch
  Randfall-Entscheid „kein Auto-Stopp" bewusst umgangen), #45 (Hook-Haertung, unabhaengig)

---

## Offene Punkte

- Traeger endgueltig festlegen: Pane-Modus IN `dtb:worker` (Wiederverwendung von
  Erkennungs-Sicht, Kollisionsregel, Config-Block spricht dafuer) vs. eigener Skill —
  Entscheidung gehoert in die Spec/den Implementierungsplan
- Aufraeum-Reihenfolge im Abschluss (c): Worktree entfernen nach Merge sofort oder erst
  nach dem Orchestrator-Checkpoint? (Heute real: nach Checkpoint + Worker-Session-Ende —
  als Default-Kandidat)
- Kollisionsregel von dtb:worker bei n parallelen Panes: gilt sie woertlich oder braucht
  die Warteschlange (d) eine eigene Formulierung? — Detail fuer den Implementierungsplan
- Auftragstext-Vorlage: genauer Wortlaut (heutiger Test-Auftrag als Ausgangspunkt) —
  Detailfestlegung im Implementierungsplan

---

**Erstellt mit:** `/dtb:feature-discover`
