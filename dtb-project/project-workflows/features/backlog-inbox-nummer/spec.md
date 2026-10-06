# Feature: BACKLOG-Spalte #

**Erstellt:** 2026-10-06
**Ziel:** Der Stand eines Changes ist in BACKLOG.md ueber die INBOX-Nummer seiner Idee nachschlagbar.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Ideen werden in der INBOX nummeriert, im BACKLOG aber nur per Name gefuehrt — wer eine Nummer
kennt („#107"), muss den Change erst ueber den INBOX-Link suchen. BACKLOG.md bekommt deshalb eine
erste Spalte `#` mit der INBOX-Nummer; Changes ohne Idee tragen `—`. Die Nummer ist wie die
Status-Spalte eine abgeleitete Anzeige und wird in Bestandsprojekten beim Checkpoint nachgezogen.

---

## Scope / Abgrenzung

### Enthalten
- Spalte `#` als erste Spalte in allen vier BACKLOG-Tabellen — gleiche Kopfform wie in der INBOX
- Neue Projekte erhalten die Spalte ab Anlage (`dtb:project-init`)
- Jeder Skill, der BACKLOG-Zeilen anlegt (`dtb:feature-plan`, `dtb:feature-fast`, `dtb:task`, `dtb:bug-report`), fuellt die Spalte mit der Nummer oder `—`
- `dtb:workflow-checkpoint` ergaenzt die Spalte in Bestandsprojekten und fuellt fehlende Nummern nach — eine vorhandene Nummer wird nie ueberschrieben
- `dtb:backlog-status` zeigt die Nummer als erste Spalte
- Regel-Absatz in `DERIVED_STATE_RULES.md`: die Nummer ist abgeleitete Anzeige

### Nicht enthalten
- Umstellung der kit-eigenen BACKLOG.md in diesem Worktree (zentrale Datei; Hand-off, der naechste Checkpoint auf master stellt sie um)
- Aenderungen an `dtb:archive` und `dtb:project-health` (sie finden Zeilen ueber den Dateipfad, nicht ueber die Spaltenposition)
- Rueckwirkende Zuordnung von Changes, deren Idee keinen Change-Link in der INBOX hat — diese tragen `—`

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Ein Skill liest BACKLOG-Spalten nach Position und verrutscht durch die neue erste Spalte | Niedrig | Mittel | Repo-weiter Grep nach BACKLOG-Lesern vor Phase-1-Ende (Lektion 3); bisher nur Pfad- bzw. Spaltennamen-Zugriffe gefunden |
| Bestandsprojekte bekommen die Spalte nie, weil nur die Vorlage geaendert wurde | Mittel | Mittel | Nachzug im Checkpoint (Laufzeittext inline, nicht im Seed — Lektion 82) |
| Schreiber und Checkpoint leiten die Nummer unterschiedlich her | Niedrig | Niedrig | Quellen fuer den Nachzug: INBOX-Change-Link (DSR §8), dann Archiv-Log; die Schreiber setzen den Startwert, der Checkpoint fuellt nur Luecken und ueberschreibt nie (die INBOX-Zeile kann vor dem Change archiviert werden) |
| Kopfzeilen-Form driftet zwischen Vorlage und Schreibern | Mittel | Niedrig | Automated-Kriterium: alle Tabellenkoepfe beginnen mit `| # |` |

---

## Dependencies

### Erforderlich vor Start
- [x] INBOX-Nummern sind stabile IDs (Nummern werden nie neu vergeben — `dtb:archive`)
- [x] Change-Link-Pflicht fuer `Ausgearbeitet` (DSR §8) als Ableitungsquelle

### Referenz-Dokumente
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — §1.3 schreibender Sync-Skill, §3 BACKLOG-Anzeige, §8 Change-Link
- `features/backlog-inbox-nummer/discovery.md` — betroffene Module und Randfaelle

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein neu angelegtes Projekt hat in allen vier BACKLOG-Tabellen die erste Spalte `#`
- [ ] Ein aus einer Idee entstandener Change erscheint im BACKLOG mit seiner INBOX-Nummer, ein Bug mit `—`
- [ ] Ein Bestandsprojekt ohne Spalte hat sie nach dem naechsten Checkpoint, mit abgeleiteten Nummern
- [ ] `dtb:backlog-status` zeigt die Nummer, sodass ein Change per Nummer auffindbar ist
- [ ] Kein bestehender Skill liest BACKLOG.md nach der Umstellung falsch

---

## Offene Punkte

- — keine — (geklaert 2026-10-06 im plan-review: verlinken zwei INBOX-Zeilen denselben Change-Ordner (Teil-Routing per `dtb:task`), gilt die kleinste Nummer)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-06)
