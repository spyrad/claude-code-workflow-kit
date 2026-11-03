# Feature: Checkpoint ohne Rueckfragen

**Erstellt:** 2026-11-03
**Ziel:** Der Checkpoint laeuft im Normalfall ohne jede Rueckfrage durch — er fragt nur noch, wenn eine offene Aufgabe nicht sicher zugeordnet werden kann.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Seit #177 (checkpoint-schneller) stellt `dtb:workflow-checkpoint` alle Fragen vor dem Schreiben in
EINER Runde, dem Kontrollpunkt mit den Teilen Verlustfunde, Aufgaben-Zuordnung und alte Aufgaben.
Zwei dieser Teile sind reine Bestaetigungen, deren Antwort in der Praxis fast immer „passt" lautet:
Verlustfunde werden kuenftig nach ihrer Gruppe automatisch erfasst, alte Aufgaben behalten ihr ⏳
ohne Frage. Uebrig bleiben die Fragen, bei denen echte Information auf dem Spiel steht: unsichere
Aufgaben-Zuordnung und moegliche Duplikate unter den Verlustfunden (unscharfer Vergleich — Kopplungsregel
„Meldeform folgt Vergleichsschaerfe", Entscheid bei der Umsetzung 2026-11-03).
Dafuer wird die Regel „keine automatische Entscheidung" in `DERIVED_STATE_RULES.md` §9.4 bewusst
geaendert (Becken-Nachtrag #185).

---

## Scope / Abgrenzung

### Enthalten
- **Verlustfunde ohne Rueckfrage:** Funde der Gruppe „Vor dem Checkpoint erledigen" (Lektionen und
  Ideen) werden direkt erfasst; Ideen aus „Kann warten" gehen still ins Befund-Becken
  `INBOX-BEFUNDE.md` (Entscheidung #75 bleibt bestehen)
- **Meldung statt Frage:** alle Erfassungen erscheinen gesammelt in der Abschlussbestaetigung — je
  Lektion mit gekuerztem Regelsatz (nicht nur der Nummer), weil niemand mehr vorab bestaetigt, was
  kuenftig als Vorwissen fuer die Planungs-Skills gilt; bei erfassten Lektionen ein Korrektur-Hinweis
  auf `dtb:lesson-curate`
- **Duplikate werden gefragt:** ein moeglicher Duplikat-Treffer wird nicht still geschrieben und nicht
  still uebersprungen, sondern als ja/nein-Zeile im Kontrollpunkt gefragt (`ja` = nicht erfassen,
  Meldezeile „uebersprungen — aehnlich {Fundstelle}"; `nein`/unklar = erfassen) — geaendert bei der
  Umsetzung 2026-11-03 (Mismatch Schritt 1.2), weil der Vergleich unscharf ist und irren kann
- **Mengengrenze bleibt:** mehr als 10 Funde → nichts automatisch schreiben, die Funde bleiben
  Befehle im Report (Schutz gegen eine Fehlerkennung, die die Lektionen auf einen Schlag fuellt)
- **Alte offene Aufgaben ohne Frage:** faellige Aufgaben behalten die ⏳-Markierung, keine
  Sammelvorlage, kein automatischer „behalten"-Stempel — sonst verschwaende ⏳ alle
  `alter_schwelle_tage` still und das Warnzeichen waere wirkungslos. Erledigen/Verwerfen bleibt
  jederzeit ueber ein Session-Signal moeglich (Abgangsvermerk)
- **Regel-Aenderung §9.4** in `DERIVED_STATE_RULES.md` samt der bewussten Kurzkopie im Checkpoint
- **Verlustpruefung ohne Schlussfrage im Checkpoint:** `dtb:no-loss-check` stellt beim Aufruf aus
  dem Checkpoint nie mehr seine Abschlussfrage (heute entfaellt sie nur, solange der Kontrollpunkt
  Verlustfunde traegt); eigenstaendig aufgerufen unveraendert
- **Nachziehen der Kopplungen:** Kopplungs-Hinweise in `dtb:lesson`, `dtb:idea`, `dtb:idea-triage`,
  `dtb:no-loss-check`, Zeile I der Rueckfragen-Defaults in `skills/CLAUDE.md`, Kit-Beschreibung in
  `CLAUDE.md`
- **Der Checkpoint-Skill wird kuerzer, nicht laenger** — die Antwortregeln fuer Verlustfunde und
  alte Aufgaben entfallen

### Nicht enthalten
- **Unsichere Aufgaben-Zuordnung bleibt eine Frage** („ist X = Y?", „X erledigt? — Hinweis ohne
  Beleg"): ein falscher Rateversuch erzeugt eine stille Dublette, die kein spaeterer Vergleich mehr
  findet, oder streicht eine offene Aufgabe still
- Abnahme-Frage und fehlende Pflichtfelder eines Hand-off-Blocks bleiben eigene Fragen
- Keine Bereinigung bestehender „behalten"-Stempel in alten Aufgabenlisten (bleiben gueltig)
- Keine Aenderung an Dashboard und Status-Sichten (Dashboard zaehlt ⏳ wie bisher; das Worktree-⏳
  ist ein anderer Mechanismus); der Config-Schluessel `status.alter_schwelle_tage` bleibt
- Keine Aenderung der Erfassungsregeln selbst (Felder, Duplikat-Bewertung, Schreibmechanik bleiben
  per Referenz in `dtb:lesson` / `dtb:idea` / `dtb:idea-triage`)
- Bestandsprojekte: ihre `DERIVED_STATE_RULES.md`-Kopie (Seed, nicht drift-geprueft) bleibt alt bis
  zum Neu-Ausrollen — akzeptiert; das Verhalten kommt mit dem Skill per `kit-sync`

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Eine falsch erkannte Lektion landet ohne Veto im Vorwissen der Planungs-Skills | Mittel | Mittel | Regelsatz sichtbar in der Meldung, Korrektur-Hinweis auf `dtb:lesson-curate`, Mengengrenze > 10 |
| Die Verlustpruefung fragt wieder selbst, weil ihre Unterdrueckungs-Bedingung an Teil A haengt | Hoch (ohne Gegenmassnahme) | Mittel | Bedingung auf beiden Seiten wortgleich auf „Aufruf aus dem Checkpoint" umstellen |
| ⏳ wird ohne Frage zum Dauerrauschen und niemand handelt | Mittel | Niedrig | Bewusst hingenommen — ⏳ bleibt sichtbar; Erledigen/Verwerfen per Session-Signal |
| Kurzkopie im Checkpoint und §9 laufen auseinander | Niedrig | Mittel | Beide im selben Change aendern, Grep-Anker `Aufgaben-Abgaenge` |
| Gemeinsame Nachmessung mit #177 vermischt die Wirkung beider Changes | Hoch | Niedrig | Bewusst entschieden (2026-11-03); Kriterien siehe Offene Punkte |

---

## Dependencies

### Erforderlich vor Start
- [x] #177 checkpoint-schneller gemergt (Kontrollpunkt A/B/C ist die Ausgangsbasis)

### Referenz-Dokumente
- `features/checkpoint-ohne-rueckfragen/discovery.md` - Anforderungen und Entscheide 2026-11-03
- `features/checkpoint-schneller/spec.md` - Vorgaenger, Kontrollpunkt-Design und Nachmessung
- `project-rules/DERIVED_STATE_RULES.md` §9 - Lebenslauf offener Aufgaben (wird geaendert)
- INBOX #173, Becken #185 - Idee und Nachtrag zur Regelaenderung

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Checkpoint ohne unsichere Aufgaben-Zuordnung und ohne moegliches Duplikat stellt keine einzige Rueckfrage (ausser Abnahme-Frage bzw. fehlenden Hand-off-Pflichtfeldern)
- [ ] Dringende Verlustfunde werden erfasst und gemeldet, „Kann warten"-Ideen landen im Becken, moegliche Duplikate werden gefragt
- [ ] Faellige alte Aufgaben tragen ⏳, ohne Frage und ohne neuen „behalten"-Stempel
- [ ] Die Verlustpruefung stellt aus dem Checkpoint heraus keine Schlussfrage mehr
- [ ] `DERIVED_STATE_RULES.md` §9.4 und die Kurzkopie im Checkpoint sagen dasselbe; alle Kopplungs-Hinweise sind nachgezogen
- [ ] Der Checkpoint-Skill hat weniger Zeilen als vorher
- [ ] **Nachmessung (gemeinsam mit #177, bis 2026-12-02):** In der gemeinsamen Nachmessung stellt der
  Checkpoint keine Rueckfrage zu Verlustfunden oder alten Aufgaben mehr — nur noch Zuordnungs- und
  Duplikatfragen (Kategorien von `checkpoint-schneller/checkpoint-phasen.py --rueckfragen`:
  „Alters-Vorlage" = 0 Antworten; „Sammelvorlage/Kontrollpunkt" nur in Laeufen mit Zuordnungs- oder
  Duplikatfrage); Median ≤ 4 aktive min gilt gemeinsam mit #177.
  Ausgangswert 2026-11-03 (89 auswertbare Laeufe, 2026-10-05..2026-11-03): „Sammelvorlage/Kontrollpunkt"
  61 Antworten / 94,0 min Wartezeit (26 %), „Alters-Vorlage" 16 / 30,3 min (8 %), eigene Kategorie
  „Aufgaben-Zuordnung" 0 Antworten; Kern-Median 5,0 min

---

## Offene Punkte

- ~~Wie oft kommen unsichere Zuordnungen bzw. Abgaenge ohne Beleg tatsaechlich vor?~~ — geklaert 2026-11-03: `checkpoint-phasen.py --rueckfragen` zaehlt in 89 Laeufen 0 Antworten in der eigenen Kategorie „Aufgaben-Zuordnung" (Grenze: Textmuster-Heuristik; Zuordnungsfragen innerhalb des Kontrollpunkts seit 2026-11-02 fallen unter „Sammelvorlage/Kontrollpunkt")
- ~~Wie werden die Erfolgskriterien von #177 fuer die gemeinsame Messung angepasst — und braucht #173 ein eigenes Messkriterium?~~ — geklaert 2026-11-03 (plan-review): eigenes Kriterium „Nachmessung" in den Success Criteria, Median ≤ 4 aktive min gemeinsam mit #177
- Hand-off-Vormerkung: offene Aufgabe „Nachmessung #177" in `WORKFLOW_STATUS.md` zur gemeinsamen Messung #177 + #173 umbenennen (Orchestrator)

---

**Erstellt mit:** `/dtb:feature-plan`
