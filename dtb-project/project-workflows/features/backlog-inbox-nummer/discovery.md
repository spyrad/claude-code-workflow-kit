# Discovery: BACKLOG-Spalte #
<!-- resume: done -->

**Erstellt:** 2026-10-06
**Idee-Referenz:** Inbox #107 — "BACKLOG.md um Spalte # (INBOX-Nummer) ergänzen, damit Status per Nummer nachschlagbar ist; Changes ohne Idee → „—""
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-project-init/SKILL.md` | BACKLOG.md-Vorlage fuer neue Projekte (vier Tabellenkoepfe) |
| `skills/dtb-feature-plan/SKILL.md` | Schritt 10: Zeilenformat "Aktive Features" / "Ideen / Backlog" |
| `skills/dtb-feature-fast/SKILL.md` | Schritt 7: Backlog-Eintrag "analog feature-plan Schritt 10" — Nummer aus Schritt 1 |
| `skills/dtb-task/SKILL.md` | Schritt 4/4b: Zeilenformat "Aufgaben" + Abschnitts-Vorlage |
| `skills/dtb-bug-report/SKILL.md` | Backlog-Eintrag: Zeilenformat `Bug: …` in "Aktive Features" |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Sync der Anzeige-Felder in BACKLOG.md — wird um die `#`-Spalte erweitert (Migration + Nachzug) |
| `skills/dtb-backlog-status/SKILL.md` | Report-Tabellen — zeigen `#` als erste Spalte |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §3 "Statusfeld in BACKLOG.md ist abgeleitete Anzeige" — Absatz zur `#`-Spalte |

---

## Anforderungen

### Scope
**Enthalten:**
- Neue erste Spalte `#` in allen vier BACKLOG-Tabellen (Aktive Features, Aufgaben, Ideen / Backlog, Abgeschlossen) — gleiche Kopfform wie INBOX.md
- Alle vier Zeilen-Schreiber (feature-plan, feature-fast, task, bug-report) fuellen die Spalte: INBOX-Nummer oder `—`
- `dtb:workflow-checkpoint` ergaenzt die Spalte in Bestandsprojekten und fuellt fehlende Werte nach — eine vorhandene Nummer wird nie ueberschrieben
- `dtb:backlog-status` zeigt die Nummer als erste Spalte
- Kurzer Regel-Absatz in DERIVED_STATE_RULES.md §3

**Nicht enthalten:**
- Migration der kit-eigenen BACKLOG.md in diesem Worktree (zentrale Datei — Hand-off; der naechste Checkpoint auf master erledigt sie)
- Aenderungen an `dtb:archive` und `dtb:project-health` (lesen Zeilen ueber den Dateipfad, nicht ueber die Spaltenposition)
- Rueckwirkende Nummernvergabe fuer Changes, deren Idee keinen Change-Link in der INBOX traegt

### Gewuenschtes Verhalten
- Zellwert ist die nackte Nummer (`107`), nicht `#107` — wie die `#`-Spalte der INBOX
- feature-fast nimmt die Nummer aus seinem Eingangs-Gate; feature-plan aus der Inbox-Auswahl oder aus `**Idee-Referenz:** Inbox #{N}` der discovery.md; task aus dem Zahl-Argument bzw. der INBOX-Herkunft (Schritt 4b); bug-report schreibt immer `—`
- Findet ein Schreiber eine Kopfzeile ohne `#`, schreibt er die Zeile im alten Format (keine Eigen-Migration) — der Checkpoint zieht nach
- Der Checkpoint leitet fehlende Nummern aus dem INBOX-Change-Link ab (`→ features/{slug}/…` ↔ Datei-Spalte, DSR §8), danach aus dem Archiv-Log; ohne Treffer `—`; vorhandene Nummern bleiben unangetastet. Die Nummer ist abgeleitete Anzeige wie die Status-Spalte

### Randfaelle
- Bestandsprojekt mit altem Tabellenkopf → Checkpoint ergaenzt Kopf + Trennzeile + jede Datenzeile
- Bug ohne Idee → `—`
- Voll-Schiene: feature-plan kennt die Nummer nur ueber discovery.md, wenn die Idee schon `In Arbeit` ist (feature-plan filtert die Inbox-Auswahl auf `Offen`)
- Mehrere INBOX-Zeilen verlinken denselben Ordner (Teil-Routing) → offener Punkt, siehe unten
- Leere Tabellen (wie aktuell in der kit-eigenen BACKLOG.md) → nur Kopf und Trennzeile aendern sich

### Einschraenkungen
- Laufzeittext bleibt inline je Skill — `DERIVED_STATE_RULES.md` ist ein Seed und erreicht Bestandsprojekte nicht (Lektion 82)
- Zentrale Dateien (BACKLOG.md, INBOX.md) werden im Worktree nicht geschrieben (Teil-Guard)

### Integrationspunkte
- DSR §8 Change-Link-Pflicht liefert die Ableitungsquelle (INBOX-Link → Ordner)
- `dtb:workflow-checkpoint` ist bereits der schreibende Sync-Skill fuer BACKLOG-Anzeigefelder (DSR §1.3)

---

## Abhaengigkeiten

- Keine — keine aktive Feature-Arbeit an BACKLOG-Formaten (features/ war leer bei Anlage)

---

## Offene Punkte

- — keine — (geklaert 2026-10-06 im plan-review: verlinken zwei INBOX-Zeilen denselben Ordner (Teil-Routing per `dtb:task`), gilt die kleinste Nummer)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-06)
