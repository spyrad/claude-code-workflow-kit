# Discovery: Ueberwachungs-Tick
<!-- resume: done -->

**Erstellt:** 2026-09-24
**Idee-Referenz:** Inbox #97 — "Pruefen, ob und wie Harness-Befehle wie `/loop` im DTB-Workflow Vorgaenge automatisieren koennen — Leitfall Herdr-Ueberwachung" (Zuschnitt 2026-09-24: eigenstaendiger Rest ohne Autopilot-Governance)
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-worker/SKILL.md` | `### Pane-Ausfuehrung` (Z. 221 ff.): neue Untersektion `#### Rueckweg: Ueberwachungs-Tick` traegt Pruefliste, Meldungsregel, Selbstende, Angebots-Vorlage; `#### Rueckweg: Warten ohne Warten` (Z. 279-294) wird "anlassbezogen oder getaktet"; Angebot nach der Start-Sequenz (Z. 276-277); Kopplungs-Hinweis der Sektion (Z. 223-227); Frontmatter `consumes` (Z. 22) |
| `skills/dtb-pane-start/SKILL.md` | Struktur-Check-Ankertabelle (Z. 205-211) + Statuszeile 2/2 → 3/3; "Nach der Zustellung" (Z. 262-264) bietet den Tick per Verweis an; `## Rueckweg und Abschluss` (Z. 323-326) |
| `CLAUDE.md` | Katalogzeile "Autonomous execution" (Z. 58) nennt worker und pane-start — um den Tick ergaenzen |

---

## Anforderungen

### Scope
**Enthalten:**
- Ein getakteter, rein lesender Ueberwachungs-Tick fuer Pane-Arbeitsplaetze beider Traeger
  (`dtb:pane-start` interaktiv, `dtb:worker` Pane-Traeger) — die nicht-blockierende Form des
  heutigen "anlassbezogen nachfragen"
- EINE Quelle: Pruefliste und Herdr-Kommandos in `dtb:worker` → `### Pane-Ausfuehrung` (die
  Herdr-Kommando-Regel erlaubt Kommandos nur dort und in `### Pane-Auftrag`,
  `skills/dtb-worker/SKILL.md:180-186`); pane-start verweist und prueft die Existenz per Struktur-Check
- Angebot nach der Zustellung (beide Traeger): fertiger Loop-Befehl mit Pane-ID und Branch,
  Kostenhinweis, Rueckfall-Zeile fuer Harnesses ohne wiederkehrenden Lauf

**Nicht enthalten:**
- Autopilot, Schreibrechte eines Ticks, Autonomie-Governance, Antwortgeber-Muster → bleiben bei #98
- Ueberwachung ausserhalb von Pane-Arbeitsplaetzen (CI/`build-check`, `repo-sync`)
- Eine Shell-Schleife ohne Modell (Nebenbefund des Zuschnitts, Bezug #45)
- Aenderungen an den Lese-Sichten (`workflow-next`/`resume`/`backlog-status`) — deren
  `In Worktrees`-Block (DSR §10) bleibt "rein lesend, ohne Ueberwachung"

### Gewuenschtes Verhalten
- **Pruefliste je Tick (nur lesen):** (1) Pane-Status per `herdr agent get {pane-id}`
  (`idle`/`working`/`blocked`/`done`/`unknown`); (2) Worktree-Stand dieses einen Worktrees nach
  DSR §10.2 — Commits vor dem Hauptbranch, uncommitted, Fortschritt X/Y (Verweis auf §10, keine
  Kopie); (3) ob seit dem letzten Tick ein WORKTREE-HANDOFF-Block (Kopfzeile) im eigenen Verlauf
  eingetroffen ist
- **Meldung nur bei Aenderung:** Vergleich gegen die letzte Tick-Meldung im Gespraechsverlauf —
  keine Zustandsdatei (waere eine Zustandsaussage ohne Pfleger). Ohne Aenderung keine Meldung
- **Selbstende:** Hand-off eingetroffen ODER Pane nicht mehr vorhanden → Endgrund genau einmal
  melden, den wiederkehrenden Lauf selbst beenden
- **Nur melden, nicht beenden:** Status `blocked` und (Worker) Ueberschreiten von
  `worker.max_minutes` — wie die heutigen Ausgaenge (b)/(c), der Mensch entscheidet
- **Harness-neutral:** Kern ist die Pruefliste; `/loop 15m` ist nur der Vorschlag fuer Claude
  Code. Ohne wiederkehrenden Lauf gilt der heutige Weg: auf Zuruf "Stand?" die Pruefliste einmal
  ausfuehren. Der Skill fragt die Existenz von `/loop` NICHT ab
- **Nie selbst starten:** der Loop-Befehl ist ein Angebot; der Mensch tippt ihn

### Randfaelle
- Pane geschlossen oder Session beendet, ohne Hand-off → Selbstende mit Grund "Pane weg"
- Hand-off trifft zwischen zwei Ticks ein → naechster Tick meldet Ende, keine weitere Pruefung
- Pane dauerhaft `blocked` → einmal melden, bei unveraendertem Zustand still bleiben
- Worker ueber `max_minutes` → einmal melden, KEIN Auto-Stopp (wie Ausgang (c) heute)
- Status `unknown` → wie eine Aenderung melden, nie als Abschluss werten (Herdr: "does not prove completion")
- Harness ohne wiederkehrenden Lauf (z. B. Codex CLI) → Rueckfall "Stand?" einmal

### Einschraenkungen
- Herdr-Kommandos nur in den zwei benannten worker-Sektionen (Drift-Schutz); pane-start
  behaelt genau seine heutigen zwei Herdr-Zeilen (Z. 177 gespiegelte Vorbedingung, Z. 296 Rueckweg)
- Schreibgrenzen-Regel und Worktree-Guard unveraendert; der Tick schreibt nichts
- Kosten: jeder Tick ist ein Modellaufruf im vollen Orchestrator-Kontext — steht im Angebot

### Integrationspunkte
- DSR §10.2/§10.4 (Worktree-Stand, erlaubte Lese-Kommandos) — per Verweis *(ueberholt 2026-09-24: autark gespiegelt in `dtb:worker`, kein Laufzeit-Verweis auf den Klasse-B-Seed — #22)*
- `dtb:workflow-checkpoint` → `### Hand-off-Block` (Kopfzeile als Erkennungsanker) — unveraendert
- worker `#### Rueckweg: Branch-Verifikation` folgt beim Hand-off wie bisher

---

## Abhaengigkeiten

- Keine blockierenden. Beruehrungen: #98 (Autopilot, Governance), #95 (4) (Anzeige-Seite, als
  DSR §10 umgesetzt), #45 (Hooks/Shell-Schleife), Beleg #102 (Becken: `/loop 15m`, 7 Ticks,
  3 echte Eingriffe am 2026-09-23)

---

## Offene Punkte

- Kann ein Loop mit festem Intervall sich in Claude Code selbst beenden (nicht nur der
  selbstgetaktete)? Wird im Wirklauf (Plan 2.3) belegt; faellt der Beleg negativ aus, meldet der
  Tick den Endgrund und nennt den Stopp-Weg fuer den Menschen

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-24)
