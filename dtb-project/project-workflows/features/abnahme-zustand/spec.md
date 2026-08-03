# Feature: Abnahme-Zustand

**Erstellt:** 2026-08-03
**Ziel:** Der explizite Zustand `Abgenommen` erhaelt eine widerspruchsfreie Definition im Kanon und eine durchgaengige Behandlung in allen lesenden Skills, damit freigegebene Changes nicht weiter als "Fertig zum Testen" gefuehrt oder als Widerspruch gemeldet werden.
**Prioritaet:** Hoch
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Statusableitung kennt zwei Zustaende, die nicht abgeleitet werden koennen, sondern gesetzt
werden muessen: die Freigabe nach bestandener Pruefung und den Abschluss durch Archivierung.
Der Kanon behandelt beide in einem Satz und schreibt beiden denselben Schreiber zu — die
Archivierung. Das ist falsch: Die Freigabe wird an anderer Stelle gesetzt, naemlich beim
Session-Abschluss nach einer Beleg-Rueckfrage, und die Archivierung setzt sie sogar **voraus**.
Waere der Satz woertlich richtig, waere die Archiv-Vorbedingung toter Text — ein Zustand, den
niemand setzen darf, kann keine Bedingung erfuellen.

Die Folge ist keine theoretische: Drei der vier lesenden Skills kennen den Freigabe-Zustand
ueberhaupt nicht. Einer schlaegt fuer jeden vollstaendig umgesetzten Change die Abnahme vor —
auch fuer laengst freigegebene; einer muesste die Abweichung zwischen Anzeige-Feld und Ableitung
als Widerspruch melden; einer zeigt freigegebene Changes gar nicht. Seit dem 2026-08-03 tragen
fuenf Changes den Zustand, jeder davon wird derzeit falsch dargestellt.

Das Vorhaben trennt die beiden Zustaende im Kanon, gibt der Freigabe eine Lese-Regel (sie
ueberschreibt die Ableitung, wie es die Pausierung bereits tut) und zieht die drei Leser nach.
Es ist strukturell dieselbe Aufgabe wie beim Kopf-Statusfeld des Plans: ein Zustand wird gelesen,
ohne dass seine Behandlung ueberall definiert ist. Dort war die Loesung Pfleger benennen, Leser
haerten, Kanon ergaenzen — dieselbe Dreiteilung greift hier.

---

## Scope / Abgrenzung

### Enthalten

- **Trennung im Kanon:** Freigabe und Abschluss werden zu zwei eigenen Eintraegen mit je ihrem
  Schreiber und ihrer Bedeutung. Die Freigabe laesst den Change im aktiven Bereich; der
  Abschluss ist der Verschiebe-Akt.
- **Lese-Regel fuer die Freigabe:** Ein gesetzter Freigabe-Zustand ueberschreibt die Ableitung
  und ist ausdruecklich **kein** Widerspruch. Der eine echte Widerspruch wird definiert: Freigabe
  gesetzt, obwohl der Fortschritt unvollstaendig ist — dort gewinnt das Artefakt und die
  Abweichung wird mit einer Zeile gemeldet.
- **Toleranz fuer Leerstellen:** Fehlt der Zustand, verhaelt sich alles wie bisher (still).
- **Spiegelung in den drei Lesern**, die den Zustand nicht kennen: der Naechster-Schritt-Skill
  (keine Abnahme-Empfehlung mehr fuer Freigegebene), die Backlog-Uebersicht (kein
  Widerspruchs-Hinweis) und der Wiederaufnahme-Skill (Freigegebene werden sichtbar).
- **Korrektur des internen Widerspruchs im Archiv-Skill:** Seine Richtlinie zaehlt die
  archivierbaren Zustaende auf und laesst die Freigabe aus, obwohl seine Kandidaten-Regel sie
  ausdruecklich nennt.
- **Pruefung des Schreiber-Verweises:** Die schreibende Seite (der Session-Abschluss-Skill)
  verweist fuer die Freigabe auf den Kanon-Abschnitt, der aufgespalten wird — der Verweis wird
  im selben Zug geprueft und, falls noetig, praezisiert.
- **Kopplungs-Hinweis am Kanon**, der die Spiegel benennt, damit eine kuenftige Aenderung sie
  mitzieht.

### Nicht enthalten

- **Bestandsmigration:** Bereits archivierte Changes bleiben unberuehrt. Aeltere Artefakte ohne
  Zustandsangabe verhalten sich weiter wie abgeleitet und heilen beim naechsten Abgleich.
- **Automatisches Zuruecknehmen der Freigabe**, wenn ein Change nachtraeglich veraendert wird.
- **Allgemeine Sichtbarkeit fertiger Changes** in der Wiederaufnahme — die Ergaenzung bleibt auf
  den Freigabe-Zustand begrenzt und baut keine neue Uebersicht.
- **Der bereits korrekte Leser** (die Pipeline-Visualisierung) wird nicht angefasst.
- **Vermerkform der Freigabe** (Datum, Beleg, Vorbehalte im Text) — als offener Punkt notiert,
  nicht Teil dieses Schnitts.
- **Roadmap-Ableitung:** Die Regel, die Roadmap-Zeilen aus dem Ordner-Zustand ableitet, kennt
  nur aktiv und archiviert — ein freigegebener, noch nicht archivierter Change bleibt dort
  vorerst „in Arbeit". Bewusst ausgeschlossen (plan-review 2026-08-03): die Roadmap-Datei ist
  im Kit-Repo ein reiner Platzhalter, es gibt keine reale Verifikationsbasis. Der offene Punkt
  unten bleibt als Wiedervorlage bestehen.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|--------------------|-----------|------------|
| Die Spiegelung wird nur an einer Stelle nachgezogen und die uebrigen bleiben zurueck — genau der Fehler, der dieses Vorhaben ausgeloest hat | Mittel | Hoch: der Zustand bliebe teilweise unbekannt, der Befund kaeme zurueck | Kopplungs-Hinweis am Kanon; Verifikation zaehlt die Spiegel mechanisch (Zielzahl = Anzahl der Leser), nicht nach Augenmass |
| Die neue Lese-Regel unterdrueckt auch den **echten** Widerspruch und verdeckt damit einen falsch gesetzten Zustand | Mittel | Mittel: eine vorschnelle Freigabe fiele nicht mehr auf | Der Konfliktfall wird positiv definiert (Freigabe bei unvollstaendigem Fortschritt) und im Trockenlauf eigens geprueft |
| Formulierung im Kanon kollidiert mit der Nachbarregel zur Pausierung oder mit der Statusmatrix | Niedrig | Mittel: neuer Widerspruch statt behobener | Aufspaltung bleibt additiv; die Matrix ist bereits korrekt und dient als Zielbild, gegen das formuliert wird |
| Der Schreiber-Skill verweist nach der Aenderung auf einen Wortlaut, den es nicht mehr gibt | Niedrig | Niedrig | Verweis wird im selben Zug geprueft; die Pruefung ist ein eigener Schritt |

---

## Dependencies

### Erforderlich vor Start

- Keine. Die betroffenen Stellen sind identifiziert und die Diagnose ist vollstaendig.

### Referenz-Dokumente

- `dtb-project/project-workflows/INBOX.md` #38 — Befund mit allen Fundstellen
- `dtb-project/project-changelog/2026-08/2026-08-03.md` (Session 2) — Entstehungskontext
- `dtb-project/project-workflows/features/plan-status-feld/` — gleiche Fehlerklasse,
  Loesungsmuster als Vorlage (Abgenommen 2026-08-03, noch nicht archiviert)

---

## Success Criteria

- [ ] Der Kanon nennt Freigabe und Abschluss als zwei getrennte Eintraege, jeder mit dem
      zustaendigen Schreiber; kein Satz schreibt beiden denselben zu
- [ ] Der Kanon definiert, dass eine gesetzte Freigabe die Ableitung ueberschreibt und kein
      Widerspruch ist — und benennt den einen Fall, der einer ist
- [ ] Alle vier lesenden Skills behandeln den Freigabe-Zustand; die Spiegelung ist mechanisch
      gezaehlt, nicht geschaetzt
- [ ] Kein Leser empfiehlt fuer einen freigegebenen Change erneut die Abnahme
- [ ] Kein Leser meldet fuer einen freigegebenen Change mit vollstaendigem Fortschritt einen
      Widerspruch
- [ ] Ein freigegebener Change mit unvollstaendigem Fortschritt wird als Widerspruch gemeldet
- [ ] Die Archiv-Vorbedingungen und die Archiv-Richtlinie nennen denselben Zustand
- [ ] Die fuenf real freigegebenen Changes erscheinen korrekt; die beiden fertigen, aber nicht
      freigegebenen erscheinen weiterhin als "Fertig zum Testen" (Negativ-Test)
- [ ] Der Kanon traegt einen Kopplungs-Hinweis, der die Spiegel benennt

---

## Offene Punkte

- Soll der Kanon eine Vermerkform fuer die Freigabe vorschreiben (Datum, kurzer Beleg), oder
  bleibt die Form frei? Die fuenf Bestandsfaelle nennen jeweils ein Datum, ohne dass eine Form
  festgelegt ist.
- Wie ist ein freigegebener, aber noch nicht archivierter Change in der Roadmap-Ableitung zu
  fuehren? Dort wird nach aktiv und archiviert unterschieden; dieser Zwischenzustand ist in der
  Zweiteilung nicht eigens vorgesehen.

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-03)
