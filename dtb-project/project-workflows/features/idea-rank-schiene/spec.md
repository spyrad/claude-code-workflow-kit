# Feature: idea-rank-schiene

**Erstellt:** 2026-10-29
**Ziel:** Die Ideen-Rangliste zeigt je Idee zusaetzlich, welche Art von Arbeit sie ist — Schiene (Task / Fast-Track / Voll-Schiene) und Worker-Tauglichkeit.
**Prioritaet:** Mittel
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

`dtb:idea-rank` sagt heute, wie wichtig und wie aufwendig eine Idee ist, aber nicht, auf welcher Schiene sie
laufen wuerde. Diese Einschaetzung entsteht erst im `dtb:idea-review` (Dreier-Weiche) bzw. in der Sicht von
`dtb:worker`. Das Feature holt beide Einstufungen in die Rangliste — nach den Regeln der beiden Skills selbst,
per Referenz statt als Kopie — damit man schon vor dem Review sieht, ob eine Idee eine schnelle Aufgabe, ein
kleines Feature oder ein Fall fuer die Voll-Schiene ist, und ob ein Worker sie erledigen koennte.

---

## Scope / Abgrenzung

### Enthalten
- Je Idee genau ein Schienen-Wert nach der Dreier-Weiche von `dtb:idea-review`: `Task`, `Fast-Track` oder `Voll-Schiene`
- Je Idee genau ein Worker-Wert nach den vier Kriterien von `dtb:worker`: `ja`, `teilweise` oder `nein` — nur bei Schiene `Task`, als Zusatz in derselben Spalte (`Task · Worker {Urteil}`; Gate-Entscheidung 2026-10-29, siehe `beispiel-ausgabe.md`)
- Bei `teilweise` die eine fehlende Voraussetzung in der Bemerkung
- Regeln fuer Grenzfaelle (groessere Schiene, schwaecheres Worker-Urteil), fuer Grundsatzfragen (Entscheidungsarbeit → `Task`; Gate-Entscheidung 2026-10-29, siehe `beispiel-ausgabe.md`) und eine Konsistenzregel zum Aufwand (mehr als zwei Phasen sind nie Fast-Track)
- Pruefung, dass die beiden Regelquellen vorhanden und strukturell unveraendert sind; bei Ausfall bleibt die Rangliste vollstaendig, nur die betroffene Einstufung zeigt `?` mit einem Hinweis
- Kopplungs-Hinweise an beiden Regelquellen und Nachzug der Kit-Doku

### Nicht enthalten
- Aenderungen an der Dreier-Weiche oder am Worker-Raster selbst
- Aenderungen an Sortierung, Wichtigkeits- oder Aufwand-Stufen — Schiene und Worker verschieben keine Zeile
- Uebernahme der Einstufung durch `dtb:idea-review` (der Review schaetzt weiterhin selbst ein)
- Freigabe oder Start von Workern aus der Rangliste
- Deckungsgleichheit mit der Worker-Sicht bei Ideen, die nicht auf der Task-Schiene liegen: dort zeigt die Rangliste nur die Schiene, ohne Worker-Zusatz, weil solche Ideen vor jedem Worker-Lauf erst Spec und Plan braeuchten (per Veto-Vorlage bestaetigt 2026-10-29)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Tabelle mit sieben Spalten wird im Chat unlesbar | Mittel | Mittel | Beispiel-Ausgabe mit echten Daten als Manual-Gate vor dem Regeltext; Rueckfall: beide Werte in einer Spalte |
| Regelquelle aendert ihre Struktur, die Rangliste stuft auf veralteter Basis ein | Niedrig | Mittel | Struktur-Check auf beide Anker vor der ersten Nutzung; Kopplungs-Hinweise an den Quellen |
| Inhaltliche Drift der Quellen bei unveraendertem Anker | Niedrig | Niedrig | Benanntes Restrisiko (Anker-Existenz, nicht Inhalt); die Kopplungs-Hinweise an den Quellen nennen idea-rank |
| Einstufung wirkt verbindlicher als sie ist | Mittel | Niedrig | Fusszeile bleibt „Momentaufnahme"; der Review entscheidet; Grenzfaelle vorsichtig |

---

## Dependencies

### Erforderlich vor Start
- [x] Tabellen-Form von `dtb:idea-rank` (abgeschlossener Change `idea-rank`, 2026-09-17)
- [x] Dreier-Weiche in `dtb:idea-review` und Worker-Raster in `dtb:worker` vorhanden

### Referenz-Dokumente
- `features/idea-rank-schiene/discovery.md` - Erhebung mit betroffenen Modulen und Randfaellen
- `archive/idea-rank/spec.md` - Vorgaenger-Spec der Rangliste

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Jede Zeile der Rangliste genau einen Schienen-Wert und genau einen Worker-Wert traegt
- [ ] Die Einstufung den Regeln von Dreier-Weiche und Worker-Raster folgt, ohne deren Text zu kopieren
- [ ] Die Zeilen-Reihenfolge bei gleichem Inbox-Stand unveraendert gegenueber heute ist
- [ ] Bei fehlender oder gedrifteter Regelquelle die Rangliste trotzdem erscheint — mit `?` in der betroffenen Spalte und genau einem Hinweis, getrennt nach Installations- und Drift-Fall
- [ ] Ein Probelauf auf den echten offenen Ideen vom Menschen als plausibel abgenommen ist
- [ ] Die Sicht weiterhin keine Datei aendert und ohne Rueckfrage ausgibt

---

## Offene Punkte

- Sind sieben Spalten im Chat noch lesbar? Entscheidung an der Beispiel-Ausgabe (Phase 1); Rueckfall: beide Werte in einer Spalte → entschieden 2026-10-29: eine Spalte (`beispiel-ausgabe.md`)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-29)
