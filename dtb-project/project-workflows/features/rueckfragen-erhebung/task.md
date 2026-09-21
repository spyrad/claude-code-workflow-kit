# Aufgabe: Rueckfragen-Erhebung (Autonomie-Achse, Station 1)

**Erstellt:** 2026-09-21
**Prioritaet:** Mittel
**Status:** Fertig zum Testen
**Bereich:** DTB-Workflow — Voll-Schiene und Pane-/Worktree-Ueberwachung (Kit-Skills als Untersuchungsgegenstand, keine Aenderung an ihnen)

---

## Beschreibung

Gemeinsame Vorarbeit fuer die vier verwandten INBOX-Ideen #57 (Kriterium), #98 (Rahmen),
#97 (Rueckkanal) und #99 (Mechanik) — Station 1 von 3 des am 2026-09-21 festgehaltenen
Zuschnitts. Die Behauptung „diese Rueckfragen werden faktisch immer gleich beantwortet" wird
durch Zahlen aus den Session-Logs ersetzt; daraus werden das Abgrenzungskriterium und eine
Delegations-Policy je Fragetyp abgeleitet. Dieselbe Auszaehlung wird als Eval-Set fuer #99
aufbereitet.

**Quellen (ausschliesslich lesend):** `dtb-project/project-changelog/` (alle Monatsordner),
`dtb-project/project-workflows/features/` und `dtb-project/project-workflows/archive/`.

**Nicht im Zuschnitt:** irgendeine Umsetzung, eine Anbieterwahl (TypeSafe vs. Claude-Urteil)
oder eine Aenderung an Skills. Ergebnis ist eine Entscheidungs-Notiz mit Zahlen, kein Code.

## Begruendung

Ohne das Abgrenzungskriterium sind #98 und #99 nicht entscheidbar — es entstuenden zwei
widerspruechliche Definitionen von „braucht keine Entscheidung" (#57, Beruehrung #43).
#57 (3) und #97 (8) verlangen denselben Lesedurchgang durch die Logs; getrennt gemacht ist
das doppelte Arbeit. Eine behauptete Kalibrierung (#99) ist ohne eigenes Eval-Set nicht
pruefbar — die Auszaehlung liefert es ohne Mehraufwand. Unterbleibt die Erhebung, bleibt die
ganze Achse Vermutung.

## Schritte

- [x] 1. Auszaehlen, wie oft ein von `dtb:feature-discover` bzw. `dtb:feature-fast` vorgeschlagener Slug abgelehnt oder geaendert wurde — je Fundstelle Datum und Logzeile notieren
- [x] 2. Auszaehlen, wie oft die Backlog-Frage aus `dtb:task` mit Nein beantwortet wurde — je Fundstelle Datum und Logzeile
- [x] 3. Auszaehlen, wie oft real nach dem Pane-/Worktree-Stand gefragt wurde (Beleg fuer #97 Punkt 8) — je Fundstelle Datum und Logzeile
- [x] 4. Die Voll-Schiene (`feature-discover`, `feature-plan`, `impl-plan`, `plan-review`, `feature-start`, `implement`, `impl-review`) nach weiteren Rueckfragen durchsuchen, deren Antwort keine Festlegung traegt, und je Fundstelle dieselbe Auszaehlung machen
- [x] 5. Aus den Zahlen das Abgrenzungskriterium formulieren (Kandidat aus #57: traegt die Antwort eine Festlegung, die spaeter teuer zu revidieren ist?) und je Fragetyp eine Delegations-Policy festlegen: nie automatisch / automatisch mit Veto / automatisch ab Schwellwert
- [x] 6. Die Auszaehlung als Eval-Set fuer #99 aufbereiten: je Fragetyp die Faelle mit der tatsaechlich gegebenen Antwort, damit eine behauptete Kalibrierung spaeter messbar ist

## Ergebnis

Eine Entscheidungs-Notiz `features/rueckfragen-erhebung/erhebung.md` mit:
- je Fragetyp: Anzahl Vorkommen, Anzahl abweichender Antworten, Fundstellen (Datum + Logzeile)
- dem formulierten Abgrenzungskriterium (ein Satz) und der Policy-Tabelle je Fragetyp
- dem Eval-Set (Fragetyp, Fall, tatsaechliche Antwort) als Tabelle
- keinerlei Aenderung an Skills, INBOX-Status oder anderen zentralen Dateien

Definition of Done: alle sechs Schritte abgehakt, die Notiz existiert, und jede Zahl darin
ist auf eine konkrete Logzeile rueckfuehrbar.

---

**Erfasst mit:** `/dtb:task`
