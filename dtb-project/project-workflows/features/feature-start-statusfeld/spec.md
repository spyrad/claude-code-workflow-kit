# Feature: feature-start schreibt keine Anzeigefelder mehr

**Erstellt:** 2026-08-07
**Ziel:** Ein Feature-, Bug- oder Aufgaben-Start behauptet keinen Status mehr, den die Ableitung nicht traegt — damit eine Konfliktmeldung wieder ein Befund ist und kein Dauerrauschen.
**Prioritaet:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

`dtb:feature-start` setzt beim Start eines Items den Anzeigewert „In Arbeit", waehrend der
Statuskanon bei null abgehakten Schritten „Geplant" (bzw. „Offen"/„Analysiert") ableitet. Jeder
Start erzeugt dadurch einen Widerspruch, den der naechste Wiedereinstieg pflichtgemaess als
Warnung meldet — eine Warnung, die immer erscheint und deshalb nichts mehr unterscheidet.

Statt den Wert zu korrigieren, verliert der Skill die Zustaendigkeit: Er liest, zeigt Kontext und
uebergibt. Gepflegt werden Anzeigefelder nur noch an der einen Stelle, die der Kanon dafuer
vorsieht. Damit verschwindet die Fehlerquelle, statt richtig gestellt zu werden.

---

## Scope / Abgrenzung

### Enthalten
- Alle Anweisungen zum Setzen von Anzeigewerten entfallen — in allen drei Startarten (Feature, Fehler, Aufgabe), sowohl im Backlog als auch in der Statusuebersicht
- Die Selbstbeschreibung des Skills (Ausloeser-Text, erklaerte Wirkung, deklarierte Schreibziele, erlaubte Werkzeuge) wird an die neue Wirkung angeglichen
- Die Kontext-Ausgaben nennen keinen Statuswechsel mehr
- Die Beschreibung des Skills im Contributor-Guide („nur Status-Updater") wird korrigiert

### Nicht enthalten
- Die Leseseite der Uebersichts-Sektion „Laufende Arbeit", auf die vier Skills zugreifen, obwohl sie niemand mehr erzeugt — bewusst ausgeklammert, separat als Inbox #52 erfasst
- Das Nachruesten einer fehlenden Fortschritts-Sektion: das repariert eine Struktur und pflegt kein Anzeigefeld — bleibt unveraendert
- Eingangspruefung, Auswahlliste und Kontextanzeige des Skills
- Ein Reparaturlauf fuer Projekte mit bereits falsch gesetztem Wert (der naechste Sitzungsabschluss gleicht sie ohnehin ab)
- Die kuenftige Pflege des Anzeigewerts in der Fehler-Beschreibung: dieses Feature entzieht dem Start die Zustaendigkeit, und der Sitzungsabschluss uebernimmt sie fuer Fehler bislang nicht. Die Luecke ist erhoben und als Inbox #53 ausgelagert (Nutzer-Entscheid 2026-08-07)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Begonnene Arbeit ist bis zum ersten abgehakten Schritt in keiner Uebersicht als laufend erkennbar | Hoch | Niedrig | Bewusst akzeptiert — genau diese Sichtbarkeit war die unbelegte Behauptung. Der Wiedereinstieg zeigt den Stand ohnehin aus den Artefakten; die allgemeine Luecke fuehrt Inbox #44 |
| Beim Entfernen der Schreibanweisungen wird versehentlich auch das Nachruesten der Fortschritts-Sektion entfernt | Mittel | Mittel | Eigenes Abnahmekriterium: das Nachruest-Angebot muss nach dem Umbau nachweisbar erhalten sein |
| Die drei Startarten werden ungleich behandelt (nur die Feature-Lane bereinigt) | Mittel | Hoch | Der urspruengliche Eintrag nannte nur die Feature-Lane; die Erhebung hat Fehler- und Aufgaben-Lane belegt. Je Lane ein eigenes Pruefkriterium |
| Die Aenderung wirkt nur in der Quelle, nicht in den ausgelieferten Kopien | Mittel | Hoch | Verteilungs-Nachlauf ist Teil der Abnahme (belegtes Muster, Inbox #51) |
| Ein Doku-Spiegel bleibt zurueck und beschreibt weiter die alte Wirkung | Mittel | Mittel | Der bekannte Spiegel ist erhoben und eigener Planschritt; zusaetzlich eine abschliessende Gegenprobe ueber den Bestand |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — der Zuschnitt ist eigenstaendig

### Referenz-Dokumente
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — Statusableitung §1.1 (Zeile 40), Feldkonflikt §1.3, Fehler/Aufgaben §1.5
- `dtb-project/project-workflows/features/feature-start-statusfeld/discovery.md` — Erhebung mit allen Fundstellen
- `skills/CLAUDE.md` — Konventionen und der zu korrigierende Spiegel

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Der Skill enthaelt in keiner der drei Startarten noch eine Anweisung, einen Anzeigewert zu setzen
- [ ] Die Selbstbeschreibung des Skills nennt das Setzen von Werten nicht mehr als seine Wirkung
- [ ] Das Nachruesten einer fehlenden Fortschritts-Sektion ist unveraendert vorhanden und weiterhin ausfuehrbar
- [ ] Der Contributor-Guide beschreibt den Skill nicht mehr als reinen Status-Aktualisierer
- [ ] Ein Start gefolgt von einem Wiedereinstieg meldet keinen Feldkonflikt mehr (an einem realen Item beobachtet)
- [ ] Die geaenderte Fassung liegt nicht nur in der Quelle, sondern auch in den ausgelieferten Kopien vor

---

## Offene Punkte

- [ ] Soll der Skill fuer Modell-Initiative freigegeben werden, sobald er nichts mehr schreibt? Die Konvention „nur lesend = frei aufrufbar" spraeche dafuer, seine Rolle als bewusst gesetzter Arbeitsschritt dagegen. Vorlaeufig bleibt die Sperre bestehen (per Veto-Vorlage bestaetigt 2026-08-07)
- [ ] Gehoert die Sichtbarkeitsluecke zwischen Start und erstem abgehakten Schritt gemeinsam mit Inbox #44 entschieden, oder bleibt sie dauerhaft akzeptiert?

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-07)
