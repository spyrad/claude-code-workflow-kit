# Feature: idea-rank

**Erstellt:** 2026-09-17
**Ziel:** Die wiederholt von Hand gebaute Priorisierungs-Sicht ueber offene Ideen (Aufwand, Wichtigkeit, Blocker) als eigenen, rein lesenden Skill `dtb:idea-rank` bereitstellen.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Am 2026-07-30 wurde ein angesetztes `dtb:idea-review` dreimal in eine Priorisierungs-Sicht umgelenkt, am
2026-08-08 entstand dieselbe Sicht erneut von Hand (vier Toepfe, Abhaengigkeiten, Reihenfolge). `dtb:idea-rank`
formalisiert dieses Muster: Der Skill zeigt alle offenen Ideen der Inbox als eine nach Wichtigkeit sortierte Tabelle
mit Aufwand und Bemerkung — ohne irgendetwas zu veraendern. (Urspruenglich vier Toepfe; nach nicht bestandener
Abnahme am 2026-09-17 auf die Tabellen-Form umgestellt, Phase 3 in `plan.md`.) Die Entscheidung je Idee bleibt bei `dtb:idea-review`.

---

## Scope / Abgrenzung

### Enthalten
- Rangliste aller offenen Inbox-Ideen (oder einer per Nummern benannten Teilmenge) als **eine Tabelle**
  `# | Idee (kurz) | Aufwand | Wichtigkeit | Bemerkung`, sortiert nach Wichtigkeit
- Je Idee Aufwand als Zeitspanne und Wichtigkeit in 6 Stufen / 4 Farben
- Blocker und Abhaengigkeiten als Teil der Bemerkung (eine Zelle je Idee, Teile mit `; ` getrennt)
- Zeilen-Reihenfolge als Empfehlung plus Uebergabe-Hinweis auf `dtb:idea-review`
- Einbindung in die Kit-Uebersichten (Skill-Kategorien, Worktree-Kategorien, Skills-Tabelle) und Pipeline-Kante zu `dtb:idea-review`

### Nicht enthalten
- Statusaenderungen an Ideen oder sonstige Schreibwirkung; das Ergebnis wird nicht als Datei abgelegt
- Das Befund-Becken — Becken-Eintraege sind bis zur Befoerderung fuer keine Arbeitssicht sichtbar
- Aenderungen an `dtb:idea-triage` (bleibt Becken-Skill)
- Fortschreiben frueherer Ranglisten; jeder Lauf bewertet neu
- Automatische Uebernahme der Reihenfolge durch `dtb:idea-review`

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Verwechslung mit `dtb:idea-triage` (aehnlicher Zweckbegriff, 2026-09-09 schon einmal passiert) | Mittel | Mittel | Abgrenzung in Beschreibung und Skill-Einleitung ausdruecklich benennen; Ausloese-Phrasen ohne „Triage"/„Becken" |
| Schein-Genauigkeit der Bewertung | Mittel | Niedrig | Aufwand immer als Spanne, nie Einzelzahl; Wichtigkeit an Belege gebunden, Grenzfall → niedrigere Stufe (seit Phase 3 statt grober Stufen) |
| Rangliste veraltet, wird aber spaeter als gueltig zitiert | Niedrig | Mittel | Keine Ablage; Report traegt Datum und Anzahl bewerteter Ideen |
| Skill schreibt versehentlich doch (z.B. Status-Flip aus Gewohnheit von idea-review) | Niedrig | Hoch | Werkzeugfreigabe ohne Schreibwerkzeuge; Success Criterion „Inbox unveraendert" im Probelauf geprueft |
| Uebersichts-Skills kennen den neuen Skill nicht | Mittel | Niedrig | Repo-weiter Namens-Grep vor Abschluss (Lektion #3) |

---

## Dependencies

### Erforderlich vor Start
- [x] Skill-Name entschieden (`dtb:idea-rank`, 2026-09-17)

### Referenz-Dokumente
- `dtb-project/project-workflows/INBOX.md` — Eintrag #33 (Ursprung, offene Punkte 1-5)
- `dtb-project/project-changelog/2026-07/2026-07-30.md` — erste manuelle Triage (Quick Wins #30/#32/#28)
- `dtb-project/project-changelog/2026-08/2026-08-08.md` — zweite manuelle Triage mit vier Toepfen
- `skills/dtb-meeting-agenda/SKILL.md` — Vorbild fuer eine rein lesende Sicht
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` §6.4 — Becken nicht in Arbeitssichten

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Lauf ueber die aktuelle Inbox zeigt jede offene Idee als genau eine Tabellenzeile, je mit Aufwand-Spanne, Wichtigkeit und Bemerkung
- [ ] Die Inbox ist nach dem Lauf unveraendert (kein Statuswechsel, keine Aenderung)
- [ ] Blockierte Ideen nennen ihre Vorbedingung konkret in der Bemerkung, Abhaengigkeiten mit Richtung (`Vorbedingung fuer #B` / `Erst nach #A`)
- [ ] Die Tabelle ist nach Wichtigkeit sortiert und der Report endet mit dem Hinweis auf `dtb:idea-review`
- [ ] Becken-Eintraege tauchen im Report nicht auf
- [ ] Der Skill ist in allen Kit-Uebersichten eingetragen und die Pipeline-Kante zu `dtb:idea-review` ist beidseitig deklariert

---

## Offene Punkte

- ~~Zuordnungsregel fuer Grenzfaelle (z.B. kleiner Aufwand bei niedrigem Nutzen — Quick Win oder nicht?) beim Bau festlegen und im Probelauf pruefen~~ → erledigt durch Phase 3 (2026-09-17): keine Toepfe mehr; Grenzfall-Regeln in SKILL.md 4.3, Sortierung 4.4

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-17)
