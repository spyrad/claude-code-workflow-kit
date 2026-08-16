# Aufgabe: Pipeline-Kante worker→checkpoint reziprok

**Erstellt:** 2026-08-16
**Prioritaet:** Mittel
**Status:** Offen
**Bereich:** Skill-Pipeline-Metadaten (Frontmatter)

---

## Beschreibung

`dtb:worker` traegt `next: [dtb:workflow-checkpoint]`, aber
`skills/dtb-workflow-checkpoint/SKILL.md` hat `after: [dtb:impl-review, dtb:no-loss-check]`
— der Worker-Rueckweg fehlt in der Gegenrichtung. `dtb:worker` in die `after`-Liste von
`dtb:workflow-checkpoint` aufnehmen und die Reziprozitaet per Grep belegen.

Nur INBOX #58 **Fall (2)**. Fall (1) (`greenfield-prd.after: null`) bleibt bewusst offen,
weil dort ungeklaert ist, ob `null` als Einstiegspunkt des Greenfield-Astes gesetzt wurde.

## Begruendung

Das Kit notiert Pipeline-Kanten reziprok; `pipeline-graph` und `workflow-status` zeichnen
sonst einen Fluss, der in einer Richtung Kanten hat, die in der anderen fehlen (INBOX #58,
Beleg: `worker-report.md` des Laufs `pipeline-kanten-reziprok` vom 2026-08-09). Der Fall
ist im Eintrag selbst als unstrittig eingestuft — dieselbe Fehlerklasse wurde dort auf der
`dtb:task`-Seite bereits behoben, die Checkpoint-Seite blieb offen.

## Schritte

- [x] `after`-Liste in `skills/dtb-workflow-checkpoint/SKILL.md` um `dtb:worker` ergaenzen
- [x] Reziprozitaet belegen: Grep auf `next:` in `dtb-worker/SKILL.md` und `after:` in `dtb-workflow-checkpoint/SKILL.md` — beide Richtungen vorhanden
- [x] Gegenprobe: keine weiteren Frontmatter-Zeilen veraendert (Diff zeigt genau 1 geaenderte Zeile)

## Ergebnis

Die Kante `dtb:worker` ↔ `dtb:workflow-checkpoint` ist beidseitig notiert;
`grep "after:" skills/dtb-workflow-checkpoint/SKILL.md` enthaelt `dtb:worker`.
Fall (1) aus #58 bleibt unveraendert offen.

---

**Erfasst mit:** `/dtb:task`
