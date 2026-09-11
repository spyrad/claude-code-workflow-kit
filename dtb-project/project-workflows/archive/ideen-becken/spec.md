# Feature: Ideen-Becken (Zwei-Becken-Modell fuer die INBOX)

**Erstellt:** 2026-09-08
**Ziel:** Maschinell erfasste Verlustfunde von den Fach-Wuenschen trennen, damit die Haupt-INBOX handhabbar bleibt und nur Befoerdertes je gearbeitet wird.
**Prioritaet:** Hoch
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Ideen-Inbox waechst schneller, als sie abgearbeitet wird: von 37 offenen Eintraegen tragen 24
ein Beleg-Muster, stammen also aus der maschinellen Verlustpruefung und nicht vom Menschen. Beide
Sorten haben voellig verschiedene Haltbarkeit — ein Fach-Wunsch altert nicht, ein Befund ueber den
Kit-Zustand von vor acht Wochen oft schon.

Dieses Feature trennt sie in zwei Becken: `INBOX.md` behaelt die Fach-Wuensche und alles
Befoerderte, ein neues `INBOX-BEFUNDE.md` nimmt die maschinellen Funde auf. Ein neuer Skill
`dtb:idea-triage` sichtet das Becken portionsweise und entscheidet je Eintrag dreifach:
befoerdern, verwerfen oder genau einmal liegenlassen. Ein Becken-Eintrag wird nie gearbeitet,
bevor er befoerdert wurde — das ist die eigentliche Zulauf-Bremse.

---

## Scope / Abgrenzung

### Enthalten
- `INBOX-BEFUNDE.md` als maschinelles Becken, gleicher Ordner wie `INBOX.md`
- Neuer Skill `dtb:idea-triage` (schreibend: befoerdern / verwerfen / liegenlassen)
- `dtb:workflow-checkpoint`: Ideen-Funde aus Schritt 0 gehen ins Becken statt in die Haupt-INBOX;
  Handoff-Zeile ab Schwelle ungesichteter Eintraege
- `dtb:no-loss-check`: Abgleich ueber beide Dateien statt nur ueber `INBOX.md`
- Nummernvergabe ueber beide Dateien (gemeinsamer Nummernkreis) in `dtb:idea` und im Checkpoint
- Alterungshinweis in der Triage: das Aenderungsdatum der im Befund genannten Datei wird dem
  Befund-Datum gegenuebergestellt; ist die Datei juenger, kann der Fund ueberholt sein. Reiner
  Hinweis ohne Anspruch auf Richtigkeit, er entfaellt ersatzlos, wenn keine Datei erkennbar ist
- `dtb:project-init` (Seed), `dtb:project-health` (Integritaets-Pruefung), Config-Block
  `idea_triage`, eine Regel-Zeile in `DERIVED_STATE_RULES.md`, Doku in beiden `CLAUDE.md`

### Nicht enthalten
- Jede Aenderung an Name, Pfad oder Format von `INBOX.md`
- Aenderungen an `dtb:idea-review`, `dtb:worker`, `dtb:workflow-next`, `dtb:archive` —
  ausgenommen die Pipeline-Kante `after:` in `dtb:idea-review`, die beidseitig gesetzt wird,
  damit keine halbseitige Kante entsteht (INBOX #46/#58)
- Automatischer Zeitverfall — bewusst gegen die Zwangsentscheidung nach einmaligem
  Liegenlassen getauscht
- Becken-Eintraege in Arbeits-Ansichten sichtbar machen
- **Migration der 24 Altbestands-Befunde** — eigener Lauf NACH diesem Feature. Das Becken startet
  leer und fuellt sich nur mit Neuem; sonst haengt die Abnahme an 24 Urteilsfragen, die den
  Mechanismus selbst nicht betreffen
- Aufteilung des Checkpoint-Skills (steht als eigene Notiz offen — hier wird nur kompensiert)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Die Triage wird nicht gelaufen — das Becken wird ein aufgeraeumterer Friedhof | Mittel | Hoch | Handoff-Zeile ab Schwelle als einzige Erinnerung; bewusst akzeptiertes Restrisiko, kein Zwang |
| `dtb:no-loss-check` liest das Becken nicht mit und meldet verschobene Funde erneut → Doppelschreibung | Hoch (wenn uebersehen) | Hoch | Abgleich ueber beide Dateien ist eigenes Erfolgskriterium mit Wirklauf |
| Nummernkollision: `dtb:idea` vergibt eine Nummer, die im Becken schon steht | Hoch | Mittel | Maximum ueber beide Dateien in beiden Schreibern; Wirklauf mit Becken-Schreibung gefolgt von Haupt-INBOX-Schreibung |
| Zeilenbudget des Checkpoints (470/470) wird gesprengt | Hoch | Niedrig | Jede neue Zeile mit Kuerzung an anderer Stelle kompensieren; Zeilenzahl als Pruefkriterium der Phase |
| Die geliehene Schreibmechanik des Checkpoints zeigt nach dem Zielwechsel ins Leere | Mittel | Mittel | Offener Punkt, im Implementierungsplan zu entscheiden — siehe unten |
| Das Becken fehlt in Bestandsprojekten (Seed-Skew, sechster dokumentierter Fall) | Hoch | Mittel | Der Triage-Skill legt das Becken beim ersten Lauf selbst an |

---

## Dependencies

### Erforderlich vor Start
- [x] `checkpoint-verlustfunde` archiviert — erledigt 2026-09-08 (`c36db8a`); dessen Wirkstelle
      wird hier umgeleitet, der Ordner darf nicht parallel wegwandern

### Referenz-Dokumente
- `features/ideen-becken/discovery.md` - Anforderungen, Randfaelle, sieben Funde
- `project-rules/DERIVED_STATE_RULES.md` - Statusableitung; bekommt die Zeile zur Status-Neutralitaet
- `archive/checkpoint-verlustfunde/spec.md` - die Wirkstelle, die hier umgeleitet wird
- `skills/dtb-idea-review/SKILL.md` - Muster fuer Worktree-Guard, Lesestand-Pruefung, Einzeldurchgang
- `skills/dtb-idea/SKILL.md` - Muster fuer Duplikat-Check und Nummernvergabe

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Verlustfund aus einem echten Checkpoint-Lauf landet im Becken, nicht in der Haupt-INBOX
- [ ] `/dtb:idea-review` zeigt danach unveraendert nur die Haupt-INBOX
- [ ] Ein zweiter Verlustpruefungs-Lauf meldet einen bereits ins Becken geschriebenen Fund NICHT erneut
- [ ] Eine vom Menschen getippte Idee nach einer Becken-Schreibung erhaelt keine bereits vergebene Nummer
- [ ] Je ein Wirklauf fuer befoerdern, verwerfen und liegenlassen ist protokolliert
- [ ] Ein Abbruch nach der zweiten Entscheidung laesst genau zwei Entscheidungen fest geschrieben
- [ ] Ein zweiter Lauf erzwingt bei einem liegengelassenen Eintrag die Entscheidung
- [ ] Der Checkpoint haengt ab Schwelle genau eine Handoff-Zeile an, darunter keine
- [ ] `skills/dtb-workflow-checkpoint/SKILL.md` bleibt bei hoechstens 470 Zeilen
- [ ] Die drei Pipeline-Kanten stehen beidseitig; die Pipeline-Ansicht zeigt keine halbseitige Kante
- [ ] Fehlt das Becken, legt der erste Triage-Lauf es an, statt abzubrechen

---

## Offene Punkte

- Referenz-Kopplung: Der Checkpoint fuehrt heute die Schreibmechanik von `dtb:idea` per Referenz
  aus und prueft dabei auf deren Sektions-Titel. Schreibt er kuenftig ins Becken, stimmt die
  geliehene Mechanik nicht mehr. Zu entscheiden: bekommt `dtb:idea` einen zieloffenen Abschnitt,
  oder bekommt die Triage eine eigene Schreibmechanik als Referenzquelle?
- Welchen Wert soll die Schwelle `idea_triage.becken_schwelle` als Standard haben? Im Entwurf
  stand 8, belegt ist der Wert nicht — er soll die Erinnerung selten genug halten, um nicht
  ignoriert zu werden.

---

**Erstellt mit:** `/dtb:feature-plan`
