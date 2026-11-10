# Feature: implement ohne feature-start

**Erstellt:** 2026-11-10
**Ziel:** Nach dem Plan-Review fuehrt genau ein Befehl in die Umsetzung — `dtb:implement`, ohne vorgeschalteten `dtb:feature-start`.
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Zwischen geprueftem Plan und Umsetzung steht heute ein zweiter Befehl, `dtb:feature-start`, der fuer
Features nur Kontext zeigt und an `dtb:implement` weiterreicht. Gemessen ging es auf dem
Arbeitsrechner 11-mal direkt in `implement` und nur 6-mal ueber `feature-start` (Quelle: Inbox #179).
`implement` uebernimmt die beiden Leistungen, die `feature-start` fuer Features zusaetzlich
erbringt; `feature-start` bleibt der Einstieg fuer Bugs und Aufgaben, die keinen Plan haben.

---

## Scope / Abgrenzung

### Enthalten
- `implement` bietet ohne Argument eine Auswahl der startbaren und laufenden Features an
- `implement` zeigt in seiner Statusanzeige Ziel und Scope aus der Spec (2-3 Zeilen)
- `feature-start` bietet keine Features mehr an; wird eines genannt, verweist es mit einer Zeile auf `implement`
- Alle Skills und Doku-Stellen, die fuer Features auf `feature-start` als naechsten Schritt zeigen, nennen `implement`
- Die Pipeline-Kanten (Vorgaenger/Nachfolger) folgen dem neuen Weg: `plan-review` → `implement`

### Nicht enthalten
- Der Weg fuer Bugs und Aufgaben (analysierte Bugs, offene Aufgaben) bleibt unveraendert
- Die zentralen Ableitungsregeln (Kit-Seed) bleiben unberuehrt
- Weitere Straffungen der Kette (Schwester-Ideen #177, #180) und die autonome Kette (#182)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Ein Verweis auf `feature-start` als Feature-Start bleibt irgendwo stehen | Mittel | Mittel | Repo-weite Gegenprobe nach dem Skill-Namen als eigener Planschritt, nicht nur Frontmatter |
| Bug-/Aufgaben-Verweise werden versehentlich mit umgestellt | Niedrig | Mittel | Gegenprobe trennt Feature- von Bug-/Aufgaben-Stellen; Bug-/Aufgaben-Zeilen bleiben ausdruecklich stehen |
| Die neue Auswahl in `implement` wirkt wie eine neue Leerlauf-Rueckfrage | Niedrig | Niedrig | Auswahl nur ohne Argument und ohne erkennbaren Kontext; mit Argument laeuft `implement` wie heute |
| Inkonsistente Pipeline-Kanten (Vorgaenger/Nachfolger) | Niedrig | Mittel | Kanten in einem Schritt umstellen und per Grep beidseitig pruefen |

---

## Dependencies

### Erforderlich vor Start
- [x] Schwester-Idee #178 (feature-plan ruft impl-plan mit auf) gemergt — beruehrt dieselben Abschluss-Bloecke nicht

### Referenz-Dokumente
- `features/implement-ohne-feature-start/discovery.md` - betroffene Module und Randfaelle
- Inbox #179 - Befund und Messung

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Nach `plan-review` nennt die Kette fuer Features genau einen Befehl in die Umsetzung: `implement`
- [ ] `plan-review` und `impl-plan` nennen als Folgeschritt nur noch `implement`
- [ ] `implement` ohne Argument zeigt eine Auswahl der Features mit offenen Plan-Schritten
- [ ] Die Statusanzeige von `implement` enthaelt Ziel und Scope aus der Spec
- [ ] `feature-start` listet nur noch Bugs und Aufgaben und verweist bei einem Feature auf `implement`
- [ ] Die Uebersichts-Skills (`workflow-next`, `workflow-status`, `workflow-resume`, `workflow-checkpoint`) empfehlen fuer ein geplantes Feature `implement`

---

## Offene Punkte

- — keine —

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-10)
