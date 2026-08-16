# Aufgabe: Lesestand-Pruefung ls portabel

**Erstellt:** 2026-08-16
**Prioritaet:** Niedrig
**Status:** Abgenommen <!-- explizit gesetzt 2026-08-16 (dtb:workflow-checkpoint) — Beleg: Diff-Abnahme vor ff-Merge cdd2c63/c659150 -->
**Bereich:** Skill-Lesestand-Pruefung (dtb-idea-review, dtb-workflow-resume)

---

## Beschreibung

`ls -la --time-style=full-iso` in den zwei Lesestand-Pruefungs-Bloecken durch
`ls -l --time-style=full-iso` ersetzen: `skills/dtb-idea-review/SKILL.md` (Z. 87) und
`skills/dtb-workflow-resume/SKILL.md` (Z. 130). Das `-a` ist unnoetig (versteckte
Dateien sind nie Ziel der mtime-Pruefung) und ein Portabilitaets-Risiko.

**ACHTUNG Spiegel:** Die beiden Bloecke sind woertlich gespiegelt (Anker
`Lesestand-Pruefung (Lese-Seite)` in `skills/CLAUDE.md`) — beide identisch aendern.

## Begruendung

impl-review-Finding unterhalb des Caps (seit 2026-08-14 in den Offenen Aufgaben):
unnoetige GNU-Spezifika in verbindlichen Kommando-Sequenzen erschweren die
Portabilitaet; `ls -l` genuegt fuer die mtime-Anzeige.

## Schritte

- [x] `skills/dtb-idea-review/SKILL.md`: `ls -la --time-style=full-iso` → `ls -l --time-style=full-iso`
- [x] `skills/dtb-workflow-resume/SKILL.md`: dito (identischer Wortlaut, Spiegel)
- [x] Verifikation: `grep -r "ls -la" skills/dtb-*/SKILL.md` = 0 Treffer UND `grep -rc "ls -l --time-style" skills/dtb-*/SKILL.md` = genau 2 Dateien mit je 1 Treffer

## Ergebnis

Beide Lesestand-Pruefungs-Bloecke verwenden `ls -l --time-style=full-iso`; kein
`ls -la` mehr in Klasse-A-Skills; Spiegelung weiterhin woertlich identisch.

---

**Erfasst mit:** `/dtb:task`
