# Aufgabe: zz-test-hc-worker

**Erstellt:** 2026-11-12
**Status:** Offen
**Zweck:** Wegwerf-Aufgabe fuer die Abnahme 4.1 der Herdr-App-Umstellung (#200). Wird nach dem Lauf entfernt.

## Beschreibung

Ein Pane-Worker schreibt eine kleine Datei in diesen Ordner, wartet zwei Minuten (in dieser
Zeit wird das App-Fenster testweise geschlossen) und committet. Kein fachlicher Inhalt.

## Schritte

- [ ] 1. Lege im selben Ordner wie diese Datei die Datei `ergebnis.md` an, Inhalt genau eine Zeile: `Start` und die aktuelle Uhrzeit (aus `date '+%H:%M:%S'`)
- [ ] 2. Fuehre `sleep 120` aus (ein einziger Aufruf im Vordergrund) und haenge danach eine zweite Zeile an `ergebnis.md` an: `Nach Wartezeit` und die aktuelle Uhrzeit
- [ ] 3. Committe `ergebnis.md` und diese `task.md` (mit abgehakten Schritten) auf dem aktuellen Branch
