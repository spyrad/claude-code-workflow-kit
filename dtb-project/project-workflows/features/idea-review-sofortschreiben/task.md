# Aufgabe: idea-review Sofort-Schreiben

**Erstellt:** 2026-09-09
**Prioritaet:** Mittel
**Status:** Offen
**Bereich:** Kit-Skills — `skills/dtb-idea-review/SKILL.md`

---

## Beschreibung

`dtb:idea-review` schreibt jede Statusentscheidung sofort in `INBOX.md` — aber der Skill sagt es
nirgends. Schritt 3 beschreibt die vier Aktionen (Behalten / Ausarbeiten / Verwerfen /
Zusammenlegen) ohne eine Aussage darueber, WANN geschrieben wird. Ein Lauf, der die
Entscheidungen sammelt und am Ende schreibt, waere nach dem Text genauso zulaessig — und
verloere bei jedem Abbruch alles.

Die Loesungsformulierung liegt bereits vor und muss nur uebertragen werden:
`skills/dtb-idea-triage/SKILL.md` Schritt 4 traegt sie woertlich („entscheiden → schreiben →
naechster Eintrag", inklusive Begruendung mit Abbruch-Beispiel), und `lessons.md` L43 haelt die
verallgemeinerte Regel fest.

## Begruendung

INBOX #71 (2026-09-07): „idea-review verliert bei Abbruch mitten in der Triage die getroffenen
Entscheidungen." Der Fall ist eintrittsnah — ein `idea-review` ueber 34 offene Ideen wird
praktisch immer abgebrochen, nicht zu Ende gefuehrt.

Belegt am 2026-09-09: In einem Lauf ueber 5 Ideen wurden #74, #73, #33 und #71 einzeln sofort
geschrieben und ueberlebten damit den Wechsel. Das lag am Vorgehen, nicht am Skill — dieselbe
Sitzung hatte kurz zuvor die Becken-Triage bei Eintrag 1 abgebrochen. Waere dort gesammelt
worden, waeren alle Entscheidungen weg gewesen.

Wird die Aufgabe nicht gemacht, bleibt der Schutz Zufall: er haengt daran, wie der jeweilige
Lauf die Anweisung auslegt.

## Schritte

- [x] `skills/dtb-idea-triage/SKILL.md` Schritt 4 als Vorlage lesen (Absatz „Jede Entscheidung
      wird SOFORT geschrieben…", inkl. Abbruch-Begruendung und der verbindlichen Reihenfolge)
- [x] Den Absatz nach `skills/dtb-idea-review/SKILL.md` Schritt 3 uebertragen, an den dortigen
      Kontext angepasst (Status-Aenderung in `INBOX.md` statt Becken-Zeile); Bezug auf L43 setzen
- [x] Pruefen, ob eine Abbruch-Meldezeile noetig ist (Muster `dtb:idea-triage` Schritt 6:
      „Abgebrochen nach Eintrag {K} von {N} — die {K} getroffenen Entscheidungen sind geschrieben")
- [x] Kein Spiegel-Text: `dtb:idea-triage` bleibt die ausfuehrliche Fassung, `idea-review` bekommt
      die eigene knappe — beide muessen dieselbe Entscheidung erzwingen (L43)
- [ ] `/dtb:kit-sync sync` — sonst laeuft im Alltag weiter die alte Fassung
- [x] INBOX #71 nach der Umsetzung schliessen (Umsetzungsvermerk wie bei #73/#74)

## Ergebnis

`skills/dtb-idea-review/SKILL.md` enthaelt eine explizite Anweisung, dass jede Statusentscheidung
unmittelbar geschrieben wird, mit derselben Wirkung wie in `dtb:idea-triage` Schritt 4. Ein
Abbruch mitten im Review laesst alle bis dahin getroffenen Entscheidungen fest geschrieben
zurueck — nachweisbar an einem Lauf, der nach der zweiten Entscheidung abgebrochen wird.

---

**Erfasst mit:** `/dtb:task`
