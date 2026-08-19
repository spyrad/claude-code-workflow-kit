# Discovery: pane-start
<!-- resume: done -->

**Erstellt:** 2026-08-19
**Idee-Referenz:** Inbox #68 — "Interaktive Voll-Schiene-Sessions in Pane+Worktree per Skill starten (Arbeitstitel `dtb:pane-start`)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-pane-start/SKILL.md` | Neu — der Start-Skill: Argument-Aufloesung, Herdr-Gate, Worktree, Pane, Begruessungstext |
| `skills/dtb-worker/SKILL.md` | Kopplungs-Hinweis an `### Pane-Ausfuehrung` (Start-Sequenz) und an der Pane-Auftrag-Vorlage: der neue Skill liest diese Sequenz, sie bleibt die eine Quelle |
| `skills/CLAUDE.md` | Skill-Kategorien-Tabelle (`### Skill-Kategorien`) um den neuen Voll-Guard-Skill; Abgrenzungssatz in `## Autonomie-Regel (dtb:worker)`, damit der interaktive Start nicht darunter gelesen wird |
| `CLAUDE.md` | Skill-Katalog: Eintrag in der Kategorie-Liste |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Nur gelesen (Hand-off-Block-Format als Referenz im Begruessungstext) — dieses Feature aendert die Datei NICHT |

---

## Anforderungen

### Scope
**Enthalten:**
- Der HINWEG einer interaktiven Voll-Schiene-Session: Worktree anlegen, Pane oeffnen,
  Claude-Session starten und erkennen, EINEN Begruessungstext zustellen
- Aufloesung eines Arguments zu einem Change-Slug (INBOX-Nummer oder bestehender Slug)
- Hartes Eligibility-Gate auf Herdr, ohne stille Degradierung
- Verweis-Kopplung auf die bestehende Herdr-Start-Sequenz in beide Richtungen

**Nicht enthalten:**
- Die Start-Sequenz selbst neu formulieren oder kopieren (sie bleibt in `dtb:worker`)
- Der RUECKWEG: der WORKTREE-HANDOFF-Block und seine Empfangsseite bleiben unveraendert
- Merge, Diff-Abnahme, Worktree-Abbau (bleibt beim Menschen; Muster wird referenziert)
- Autonomie-Governance: Versuchslimit, Zeitdeckel, Tauglichkeitsraster, `worker-report.md`
- Aenderungen an `dtb:workflow-checkpoint` (auch nicht die bekannte Branch-Prosa —
  das ist ein eigener, bereits offener Nachlauf)

### Gewuenschtes Verhalten
- Ein Aufruf mit Argument fuehrt zu einer laufenden, ansprechbaren Session in einer eigenen
  Pane, die ihren Arbeitsplatz, ihren Startbefehl, die Orchestrator-Adresse und ihre
  Rueckweg-Pflicht kennt — ohne dass der Mensch etwas hineinkopiert
- Bei einer INBOX-Nummer schlaegt der Skill die passende Startschiene vor
  (`feature-discover` vs. `feature-fast`), entscheidet aber nie selbst
- Der Orchestrator kehrt nach der Zustellung zur eigenen Arbeit zurueck, ohne zu blockieren

### Randfaelle
- Kein Herdr (`HERDR_ENV` ungleich 1 oder `herdr` nicht im PATH) → Abbruch mit Alternativen,
  keine Degradierung auf einen anderen Traeger
- Aufruf aus einem verlinkten Worktree → harter Abbruch (Worktrees entstehen vom Haupt-Checkout)
- Argument trifft weder eine INBOX-Nummer noch einen bestehenden Change-Ordner → melden, nicht raten
- Change-Ordner existiert schon mit Artefakten → Fortsetzung, der Begruessungstext nennt den
  abgeleiteten naechsten Schritt statt eines Startbefehls
- Erkennung der Session bleibt aus → ein Wiederholungsversuch, dann Abbruch mit Pane-Inhalt
- Branch existiert bereits → melden statt ueberschreiben
- Zielarbeit ist uncommittet → Hinweis, weil der Worktree aus einem Commit entsteht

### Einschraenkungen
- Windows: die Session muss ueber die Pane-Shell gestartet werden, nicht ueber den
  Agent-Start-Weg (dort zweifach belegt gescheitert)
- Herdr-CLI-Drift ist ein bekanntes, dokumentiertes Risiko; genau deshalb darf die
  Kommando-Sequenz nicht dupliziert werden
- Der Skill schreibt keine Artefakte und keine zentralen Dateien

### Integrationspunkte
- `dtb:worker` — Quelle der Herdr-Mechanik (Start-Sequenz, Gate, Warteschlangen-Erfahrung)
- `dtb:workflow-checkpoint` — Rueckweg: erzeugt im Worktree den Hand-off-Block, dessen
  Format der Begruessungstext referenziert; die Empfangsseite bleibt unangetastet
- `dtb:feature-discover` / `dtb:feature-fast` — die Skills, die in der Pane gestartet werden
  (Teil-Guards: sie ueberspringen dort die globalen Schreibschritte planmaessig)
- `dtb:kit-sync` — verteilt den neuen Skill automatisch als Klasse-A-Artefakt

---

## Abhaengigkeiten

- Fundament `herdr-worker-automation` (#67) ist umgesetzt und abgenommen (archiviert):
  Start-Sequenz, Gate und Zustellung als eine Nachricht sind real belegt
- Keine Konflikte mit den vier laufenden Bestands-Features (kein gemeinsamer Pfad)
- Beruehrung #62 (Ort der Minimal-Notiz bei hartem Stopp) bleibt offen und wird von diesem
  Feature nicht geloest — bei einem Menschen in der Pane stellt sich die Frage anders

---

## Offene Punkte

- Der offene F4-Nachlauf an der Branch-Prosa in `dtb:workflow-checkpoint` beschreibt
  Worktrees pauschal als branchlos; sobald er korrigiert ist, sollte die Formulierung auch
  den hier gewaehlten `feature/{slug}`-Fall abdecken (nur Beobachtung, keine Aufgabe dieses Features)
- Ob der Skill spaeter mehrere Panes zugleich starten soll (Warteschlangen-Analogie zum
  Worker), ist bewusst offen gelassen — v1 startet genau eine Session pro Aufruf

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-19)
