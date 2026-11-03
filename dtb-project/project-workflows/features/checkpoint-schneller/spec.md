# Feature: Checkpoint schneller

**Erstellt:** 2026-11-02
**Ziel:** Der Checkpoint braucht im Median hoechstens 4 aktive Minuten, ohne dass ein Verlustfund verloren geht.
**Prioritaet:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

`dtb:workflow-checkpoint` ist der groesste Zeitblock der Kette (Median rund 7 aktive Minuten je Lauf).
Die Messung an 74 echten Laeufen zeigt: Die Zeit steckt vor allem im Warten auf den Menschen — und
der groesste Einzelposten ist eine Commit-Frage, die gar nicht im Skill steht. Das Feature kuerzt
Rueckfrage-Runden und Nachlauf, statt Pruefungen zu streichen: feste Weiter-Zeile statt Commit-Frage,
ein Kontrollpunkt statt mehrerer Vorlagen, Dashboard nur, wo es eine Seite gibt.

---

## Scope / Abgrenzung

### Enthalten
- Am Ende des Checkpoints eine feste Weiter-Zeile auf den Commit-Skill; keine Rueckfrage, ob committet werden soll
- Ein Kontrollpunkt vor dem Schreiben: Verlustfunde, unsichere Aufgaben-Zuordnungen und faellige
  ⏳-Aufgaben erscheinen in einer Nachricht, der Mensch antwortet einmal
- Dashboard-Auffrischung nur, wenn die Seite im Projekt schon existiert (Schalter bleibt, Default an)
- Mess-Skript und Vorher-Werte im Change-Ordner; Doku und alle Spiegel nachgezogen

### Nicht enthalten
- Aenderungen an der Verlustpruefung (`no-loss-check`) — sie bleibt immer an und unveraendert
- Aenderungen an der Erzeugung des Dashboards
- Die Abnahme-Frage mit Beleg — sie bleibt eine eigene Entscheidung des Menschen
- Die Sende-Seite im verlinkten Worktree (Weiche Wechsel/Ende, Hand-off, Uebergabe-Notiz)
- Ein Commit innerhalb des Checkpoints
- Die anderen Teile der Ketten-Straffung (#178–#181)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Die gebuendelte Vorlage wird so lang, dass der Mensch weniger genau hinsieht | Mittel | Mittel | Teile klar getrennt und nummeriert; Antwortregeln je Teil bleiben; Abnahme bleibt eigene Runde |
| Die Ersparnis reicht nicht fuer ≤ 4 min | Mittel | Mittel | Ehrliche Nachmessung; naechster Hebel (Dashboard-Default aus) ist benannt |
| Das Modell fragt trotz Weiter-Zeile nach dem Commit | Mittel | Niedrig | Ausdrueckliche Regel im Skill-Text; Pruefung im Probelauf und in den Vergleichslaeufen |
| Vorziehen des Aufgaben-Vergleichs bricht eine Abhaengigkeit (Hand-off-Empfang, Log braucht die Abgaenge) | Niedrig | Hoch | Reihenfolge im Plan pruefen; Probelauf mit echtem Stand im Haupt-Checkout |
| Projekte ohne Dashboard-Seite verlieren eine erwartete Auffrischung | Niedrig | Niedrig | Seite einmal per `/dtb:project-dashboard` erzeugen, danach frischt der Checkpoint sie wieder auf |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine

### Referenz-Dokumente
- `features/checkpoint-schneller/discovery.md` - Messung (Vorher-Werte) und Anforderungen
- `skills/dtb-workflow-checkpoint/SKILL.md` - der veraenderte Skill
- `skills/CLAUDE.md` → „Rueckfragen-Defaults (Veto-Form)" - Formen und Zuordnungstabelle

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Der Checkpoint endet mit der festen Weiter-Zeile und stellt keine Commit-Frage mehr
- [ ] Vor dem Schreiben gibt es hoechstens eine Rueckfrage-Runde (ausgenommen die Abnahme-Entscheidung)
- [ ] Ohne vorhandene Dashboard-Seite wird keine erzeugt; mit Seite wird sie wie bisher aufgefrischt
- [ ] Die Verlustpruefung ist unveraendert; 3 Vergleichslaeufe nach dem Merge finden dieselben Lektionen, Fach-Fragen und Entscheidungen
- [ ] Median der aktiven Minuten ≤ 4 nach mindestens 10 Laeufen (chain-metrics), gemessen spaetestens 2026-12-02

---

## Offene Punkte

- Nachmessung und Vergleichslaeufe sind erst nach dem Merge moeglich (Voll-Guard im Worktree, echte Laeufe noetig) — Termin spaetestens 2026-12-02 wegen des 30-Tage-Fensters der Protokolle; die Nachmessung laeuft gemeinsam mit #173 (`checkpoint-ohne-rueckfragen`, Entscheid 2026-11-03 — dessen Kriterium steht in seinen Success Criteria)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-02)
