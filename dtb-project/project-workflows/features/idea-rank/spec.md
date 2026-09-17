# Feature: idea-rank

**Erstellt:** 2026-09-17
**Ziel:** Die wiederholt von Hand gebaute Aufwand×Nutzen-Sicht ueber offene Ideen als eigenen, rein lesenden Skill `dtb:idea-rank` bereitstellen.
**Prioritaet:** Mittel
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Am 2026-07-30 wurde ein angesetztes `dtb:idea-review` dreimal in eine Priorisierungs-Sicht umgelenkt, am
2026-08-08 entstand dieselbe Sicht erneut von Hand (vier Toepfe, Abhaengigkeiten, Reihenfolge). `dtb:idea-rank`
formalisiert dieses Muster: Der Skill ordnet alle offenen Ideen der Inbox nach Aufwand und Nutzen in vier Toepfe
und empfiehlt eine Reihenfolge — ohne irgendetwas zu veraendern. Die Entscheidung je Idee bleibt bei `dtb:idea-review`.

---

## Scope / Abgrenzung

### Enthalten
- Rangliste aller offenen Inbox-Ideen (oder einer per Nummern benannten Teilmenge) in vier Toepfen:
  Quick Wins, strategisch wertvoll, wartend/blockiert, braucht eigenen Fokus
- Je Idee grobe Aufwand- und Nutzen-Stufe mit 1-Satz-Begruendung
- Ausgewiesene Abhaengigkeiten zwischen Ideen und benannte Blocker
- Empfohlene Reihenfolge als Fazit plus Uebergabe-Hinweis auf `dtb:idea-review`
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
| Schein-Genauigkeit der Bewertung | Mittel | Niedrig | Grobe Stufen mit Begruendung statt Zahlen (Lektion #10) |
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
- [ ] Ein Lauf ueber die aktuelle Inbox ordnet jede offene Idee genau einem der vier Toepfe zu, je mit Aufwand, Nutzen und Begruendung
- [ ] Die Inbox ist nach dem Lauf unveraendert (kein Statuswechsel, keine Aenderung)
- [ ] Blockierte Ideen nennen ihre Vorbedingung konkret, Abhaengigkeiten stehen als gerichtete Paare
- [ ] Der Report endet mit einer Reihenfolge-Empfehlung und dem Hinweis auf `dtb:idea-review`
- [ ] Becken-Eintraege tauchen im Report nicht auf
- [ ] Der Skill ist in allen Kit-Uebersichten eingetragen und die Pipeline-Kante zu `dtb:idea-review` ist beidseitig deklariert

---

## Offene Punkte

- Zuordnungsregel fuer Grenzfaelle (z.B. kleiner Aufwand bei niedrigem Nutzen — Quick Win oder nicht?) beim Bau festlegen und im Probelauf pruefen

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-17)
