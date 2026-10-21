# Feature: Triage-Vorsortierung

**Erstellt:** 2026-10-16
**Ziel:** `dtb:idea-triage` sortiert das Befund-Becken vor der eigentlichen Triage per lesender Voranalyse vor, sodass der Mensch nur noch eine vorbelegte Sammelliste bestätigt und nur unsichere Fälle einzeln entscheidet.
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Befund-Becken wächst schneller, als die Einzeltriage es abarbeitet — der Probelauf vom 2026-10-16 fand 73 Funde, von denen 16 erledigt, überholt oder doppelt waren und 3 eigentlich Lektionen. `dtb:idea-triage` bekommt deshalb einen Vor-Schritt: Hintergrund-Agenten prüfen jeden Fund lesend gegen den Kit-Stand und schlagen mit Beleg vor, ob er befördert, gebündelt, verworfen oder als Lektion bzw. Fachfrage abgelegt wird. Der Mensch bestätigt das Ergebnis als Sammelliste mit Veto; nur unsichere Fälle kommen einzeln, danach läuft die normale Triage für die verbleibenden Feature-Kandidaten.

Beleg: [becken-vorsortierung.md](becken-vorsortierung.md) (73 Funde → 51 befördern / 16 verwerfen / 6 unklar, 10 Bündel). Herleitung: [discovery.md](discovery.md).

---

## Scope / Abgrenzung

### Enthalten
- **Stufe 1 — Vorverarbeitung** (neuer Vor-Schritt in `dtb:idea-triage`):
  - Voranalyse aller ungesichteten Becken-Funde gegen den Kit-Stand, je Fund ein Vorschlag mit Grund, Beleg und Sicherheit
  - Verwandte Funde zu Bündeln zusammenfassen, wo es Sinn ergibt — nur gegenseitig verwandte Funde, Träger plus direkte Nachbarn, keine transitive Hülle (Review 2026-10-16, F1)
  - Erledigte, überholte und doppelte Funde zum Verwerfen vorschlagen (Beleg = Begründung)
  - Lektionen über die Schritte von `dtb:lesson`, Fachfragen über die Schritte von `dtb:open-question` ablegen, statt sie als Feature zu befördern
  - Nachtrag an eine bereits bestehende INBOX-Idee (bewusste Ausnahme von „nur neue Einträge")
- **Vorlage an den Menschen:** Sammelliste mit Veto (`alle uebernehmen` / `Nummern streichen` / `einzeln durchgehen`), Bündel als eigener Block oben; einzeln vorgelegt werden Vorschläge `Unklar`, Verwerfen-Vorschläge mit Sicherheit unter `hoch` oder ohne prüfbaren Ort, Dubletten- und Nachtrag-Vorschläge, die auf einen Fund im selben Lauf zeigen, Funde ohne Vorschlag und Vorschläge eines Typs mit gefallener Quelle (Review 2026-10-16/18)
- **Stufe 2 — normale Triage** für die verbleibenden Feature-Kandidaten: befördern, liegenlassen oder verwerfen wie bisher, dazu Option 0 „Vorschlag übernehmen“ (Nachtrag, Lektion, Fachfrage) bzw. „Lektion trotzdem erfassen“ nach einem Lektions-Dubletten-Treffer
- Nachziehen der Kit-Doku: Zwei-Becken-Regel (neue Schreibwege der Triage) und Skill-Beschreibung im Root-`CLAUDE.md`

### Nicht enthalten
- Agenten entscheiden oder schreiben nichts — die Voranalyse ist rein lesend; jedes Schreiben folgt der Bestätigung durch den Menschen
- Kein Umsetzen von Funden — auch ein offensichtlicher Einzeiler-Fix wird befördert oder verworfen, nicht nebenbei erledigt
- Keine Neu-Priorisierung oder Umsortierung der Haupt-INBOX — `dtb:idea-review` bleibt getrennt
- Keine Änderung an der Schreibseite: wie `dtb:workflow-checkpoint` ins Becken schreibt, bleibt unverändert
- Kein neuer Skill
- Kein echter Aufruf von `dtb:lesson`/`dtb:open-question` (jeder Aufruf fragte erneut nach) — die Triage führt deren Schritte per Referenz aus

---

## Verhalten (aus der Discovery)

| Situation | Verhalten |
|-----------|-----------|
| Becken leer | eine Zeile „Nichts zu sichten", keine Agenten |
| Weniger als 5 Funde | keine Hintergrund-Agenten, Voranalyse direkt in der Session |
| Umfang | die Voranalyse liest das ganze Becken (Bündel und Dubletten erkennt man nur im Gesamtbild); die Portions-Kappung gilt nur noch für die Einzelfälle |
| Schreiben | erst nach Bestätigung der Sammelliste, dann Eintrag für Eintrag, jeder sofort (Regel INBOX #71) — Abbruch mittendrin lässt das Geschriebene stehen; die Vorschläge selbst werden nicht gespeichert |
| Bündel | ein Fund trägt das Bündel (der jüngste freie Kandidat mit gegenseitigem Nachbarn — deterministisch, Review F1), seine Nummer bleibt, der Text nennt die übrigen; die übrigen gehen mit „gebündelt in #N" ins Verwerfen-Archiv; nie eine neue Nummer |
| Nachtrag | Fund wird als Satz an die bestehende INBOX-Idee angehängt, archiviert mit „nachgetragen in #N" |
| Fachfrage ohne aktives Feature | Vorschlag eines passenden (auch nicht aktiven) Features; passt keins → als Idee in die Haupt-INBOX mit Vorsatz „Fachfrage:" |
| Lektion schon vorhanden | Duplikat-Prüfung von `dtb:lesson` meldet; der Vorschlag wird „Verwerfen: Lektion L{N} deckt ab" (Sicherheit mittel) und immer einzeln vorgelegt — der Mensch kann den unscharfen Treffer mit „Lektion trotzdem erfassen" überstimmen |
| Agent fällt aus | seine Funde gehen ohne Vorschlag als Einzelfälle in die normale Triage — nie als „nichts gefunden" werten |
| Becken ändert sich während des Laufs | bestehende Lesestand-Prüfung greift; neue Funde erst im nächsten Lauf |
| Falscher Beleg | Mensch streicht die Nummer in der Sammelliste; der Fund geht einzeln in die normale Triage |

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Agenten-Vorschlag „erledigt/überholt" ist falsch, ein echter Fund wird verworfen | Mittel | Hoch | Verwerfen unter Sicherheit `hoch` wird einzeln vorgelegt; jeder Vorschlag trägt einen prüfbaren Beleg; das Verwerfen-Archiv bleibt Suchraum |
| Sammelliste wird zu lang, um sie ernsthaft zu prüfen (Probelauf: 73 Zeilen) | Mittel | Mittel | Bündel-Block oben verdichtet; Vorschlag + Beleg je Zeile in einer Zeile; `einzeln durchgehen` bleibt als Ausweg |
| Bündel über Agenten-Grenzen werden nicht erkannt, wenn das Becken auf mehrere Agenten aufgeteilt ist | Mittel | Niedrig | offener Punkt — Aufteilung im Plan festlegen |
| Die per Referenz genutzten Schritte von `dtb:lesson`/`dtb:open-question` werden umgebaut, die Triage arbeitet auf veralteter Basis | Niedrig | Mittel | Struktur-Check auf die Anker-Sektionen vor dem ersten Schreiben (Muster `dtb:workflow-checkpoint` Schritt 0) |
| Umbau der Triage bricht die Kopplung zu `dtb:workflow-checkpoint` | Niedrig | Mittel | `## Schreibmechanik INBOX-BEFUNDE.md` bleibt unverändert benannt; Struktur-Check-Grep als Erfolgskriterium |
| Die Regeln „nie das ganze Becken" und „sofort schreiben" aus dem Ursprungs-Feature werden stillschweigend aufgeweicht | Mittel | Mittel | Die Anpassung wird im Skill begründet (Sammelliste statt Einzelentscheidung), nicht nur geändert |

---

## Dependencies

### Erforderlich vor Start
- [x] `dtb:lesson` und `dtb:open-question` für das Modell freigegeben (`3fc03ee`) — für Variante A nicht zwingend, aber Teil des Ausgangsstands
- [ ] Discovery abgeschlossen und offene Punkte im Plan geklärt

### Referenz-Dokumente
- `features/triage-vorsortierung/discovery.md` — Entscheidungen (1)–(5) und Variante A
- `features/triage-vorsortierung/becken-vorsortierung.md` — Probelauf 2026-10-16 als Beleg und Testmaterial
- `skills/dtb-idea-triage/SKILL.md` — Hauptträger
- `skills/dtb-workflow-checkpoint/SKILL.md` Schritt 0 — Vorbild für Ausführung per Referenz mit Struktur-Check
- `skills/dtb-impl-review/SKILL.md` Schritt 9 — Vorbild Sammelliste mit schweren Fällen einzeln
- `skills/CLAUDE.md` — Zwei-Becken-Regel, Rückfragen-Defaults (Sammelliste), Duplikat-Schutz
- `archive/ideen-becken/` — Ursprung der Triage-Regeln

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Triage-Lauf über ein Becken mit ≥ 5 Funden legt eine Sammelliste vor, in der jede Zeile Vorschlag, Grund und Beleg trägt
- [ ] Verwerfen-Vorschläge unter Sicherheit `hoch` und Vorschläge `Unklar` erscheinen einzeln, nicht in der Sammelliste
- [ ] Bündel erscheinen als eigener Block; nach der Bestätigung trägt genau ein Fund das Bündel, die übrigen Nummern stehen mit „gebündelt in #N" im Verwerfen-Archiv, keine Nummer wird neu vergeben
- [ ] Ein als Lektion vorgeschlagener Fund landet nach Bestätigung in der Lektionen-Sammlung (ohne zweite Rückfrage) und verlässt das Becken
- [ ] Eine Fachfrage landet im vorgeschlagenen Feature oder — ohne passendes Feature — als „Fachfrage:"-Idee in der Haupt-INBOX
- [ ] Ein Nachtrag hängt den Fund an die bestehende INBOX-Idee an und archiviert ihn mit „nachgetragen in #N"
- [ ] Ein Abbruch nach Bestätigung lässt alle bis dahin geschriebenen Entscheidungen stehen
- [ ] Kein Agent schreibt eine Datei (nachprüfbar: Agenten-Typ ohne Schreib-Werkzeuge, wo verfügbar; der Auftrag verbietet Schreiben in jedem Fall)
- [ ] Becken leer → eine Zeile, keine Agenten; < 5 Funde → keine Hintergrund-Agenten
- [ ] Der Struktur-Check von `dtb:workflow-checkpoint` auf `## Schreibmechanik INBOX-BEFUNDE.md` greift weiter
- [ ] Ein Nachlauf auf dem Probelauf-Becken reproduziert die Größenordnung des Probelaufs (Befördern / Verwerfen / Unklar / Bündel)

---

## Offene Punkte

- Priorität ist nicht festgelegt — Hoch, Mittel oder Niedrig? → Mittel (2026-10-19)
- Aufteilung der Hintergrund-Agenten (Probelauf: 3 Agenten nach Nummernbereich) — wie entstehen Bündel über Agenten-Grenzen hinweg? → Vorschlag in `plan.md` T2
- Ergebnis-Format der Agenten (Probelauf-Tabelle: #, Vorschlag, Grund, Beleg, Sicherheit) und wie es in Sammelliste und Einzelfälle zerfällt → Vorschlag in `plan.md` T3
- Bekommt das Verwerfen-Archiv eine eigene Beleg-Spalte, oder wandert der Beleg in die Begründung? → Vorschlag in `plan.md` T5
- Was wird aus `altbestand_pro_lauf`, wenn die Kappung nur noch für Einzelfälle gilt — Bedeutung anpassen oder Schlüssel ersetzen? → Vorschlag in `plan.md` T1

---

**Erstellt mit:** `/dtb:feature-plan`
