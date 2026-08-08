# Aufgabe: Pipeline-Kanten reziprok nachtragen

**Erstellt:** 2026-08-08
**Prioritaet:** Mittel
**Status:** Offen
**Bereich:** Kit-Skills — Pipeline-Metadaten im Frontmatter (`skills/dtb-*/SKILL.md`)

---

## Beschreibung

Die **zwei echten** halbseitigen Pipeline-Kanten aus INBOX #46 reziprok nachtragen:

| Vorhandene Kante | Fehlende Gegenrichtung |
|------------------|------------------------|
| `dtb-feature-fast` → `next: [dtb:plan-review]` | `dtb-plan-review` → `after:` enthaelt nur `dtb:impl-plan` |
| `dtb-greenfield-roadmap` → `next: [dtb:feature-discover]` | `dtb-feature-discover` → `after:` enthaelt nur `dtb:idea-review` |

**Zuschnitt (Nutzer-Entscheidung 2026-08-08):** Nur diese zwei. Die **vier** read-only-Faelle
aus #46 (`workflow-next`, `meeting-agenda` — jeweils `after: null`) bleiben **unangetastet**;
ob eine jederzeit aufrufbare Sicht ueberhaupt eine Pipeline-Station ist, ist die offene
Konventionsfrage #46 (a)/(b) und NICHT Teil dieser Aufgabe.

## Begruendung

`dtb:pipeline-graph` und `dtb:workflow-status` zeichnen den Fluss aus genau diesen
Frontmatter-Kanten. Solange die Gegenrichtung fehlt, hat der dargestellte Graph Kanten,
die in der einen Richtung existieren und in der anderen nicht — der Fast-Track sieht
aus, als fuehre er ins Leere, und der Greenfield-Ast bricht vor der Discovery ab.
Beide Faelle entstanden, weil beim Bau eines Skills die Gegenseite nicht mitgezogen
wurde (`dtb:feature-fast` vom 2026-08-02, `dtb:plan-review` nie nachgefuehrt) —
dasselbe Spiegel-Kopplungs-Muster wie die Faelle vom 30./31.07.

## Schritte

- [ ] `dtb:feature-fast` in `skills/dtb-plan-review/SKILL.md` → `pipeline.after` ergaenzen — Pruefung: `grep -A6 '^pipeline:' skills/dtb-plan-review/SKILL.md` zeigt `after: [dtb:impl-plan, dtb:feature-fast]`
- [ ] `dtb:greenfield-roadmap` in `skills/dtb-feature-discover/SKILL.md` → `pipeline.after` ergaenzen — Pruefung: `grep -A6 '^pipeline:' skills/dtb-feature-discover/SKILL.md` zeigt `after: [dtb:idea-review, dtb:greenfield-roadmap]`
- [ ] Gegenprobe Vollscan: kein weiterer Skill verliert eine Kante, und die vier read-only-Faelle stehen unveraendert auf `after: null` — Pruefung: `grep -c 'after: null' skills/dtb-workflow-next/SKILL.md skills/dtb-meeting-agenda/SKILL.md` unveraendert
- [ ] **(beim Menschen — bei der Worker-Freigabe ausgeklammert)** Commit/Push + `/dtb:kit-sync sync`: beide geaenderten Dateien sind Klasse-A-Artefakte, ohne sync laufen die installierten Kopien weiter mit den halbseitigen Kanten

## Ergebnis

Beide `after:`-Listen tragen ihre Gegenkante; ein Vollscan ueber alle `skills/dtb-*/SKILL.md`
findet keine echte halbseitige Kante mehr. Die vier read-only-Faelle sind unveraendert.
Die offene Konventionsfrage #46 (a)/(b) bleibt bewusst offen und wandert nicht mit.

---

**Erfasst mit:** `/dtb:task`
