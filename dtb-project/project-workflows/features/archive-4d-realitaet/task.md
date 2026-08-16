# Aufgabe: archive 4d/4e Archiv-Realitaet

**Erstellt:** 2026-08-16
**Prioritaet:** Mittel
**Status:** Offen
**Bereich:** skills/dtb-archive/SKILL.md (Schritte 4d + 4e)

---

## Beschreibung

`dtb:archive` Schritte 4d und 4e an die Archiv-Realitaet anpassen (INBOX #65):

- **4d** sagt „Abschnitt *Aktive Features* bleibt unberuehrt" — archivierte Features
  stehen aber genau dort, weil der „Abgeschlossen"-Abschnitt in BACKLOG.md seit
  2026-08-07 bewusst leer ist (Karteileichen-Entscheidung). Umformulieren auf:
  **archivierte Items werden aus JEDEM Abschnitt entfernt** (Aktive Features,
  Aufgaben, Abgeschlossen).
- **4e** sagt fuer WORKFLOW_STATUS.md „nicht entfernen, sondern warnen" — bei einem
  GENERIERTEN Statusblock greift das ins Leere. Anpassen: Zeilen archivierter Items
  werden aus der Status-Tabelle entfernt; die Warnung bleibt NUR fuer den Fall, dass
  ein archiviertes Item dort faelschlich als „In Arbeit" (teilabgehakter Progress)
  gefuehrt wird.

**Vorab-Antwort (Freigabe 2026-08-16):** Option 1 aus #65 — aus jedem Abschnitt
entfernen; der „Abgeschlossen"-Abschnitt bleibt Karteileichen-frei (die Entscheidung
vom 2026-08-07 bleibt bestehen).

Nur `skills/dtb-archive/SKILL.md` — keine anderen Dateien.

## Begruendung

Zwei reale Belege (2026-08-10 `autonome-schiene`, 2026-08-16 `parallele-sessions`):
die Anweisung musste beide Male bewusst gebrochen werden, sonst waeren genau die
Karteileichen entstanden, die 2026-08-07 in sechs Faellen geraeumt wurden. Eine
Anweisung, die bei jeder Ausfuehrung gebrochen werden muss, ist ein Defekt.

## Schritte

- [x] 4d umformulieren: archivierte Items aus JEDEM BACKLOG-Abschnitt entfernen (Aktive Features, Aufgaben, Abgeschlossen)
- [x] 4e umformulieren: Zeilen archivierter Items aus der Status-Tabelle entfernen; Warnung nur noch bei faelschlich „In Arbeit" gefuehrten Items
- [x] Verifikation: `grep -c "bleibt unberuehrt" skills/dtb-archive/SKILL.md` = 0 UND Schritt-4d-/4e-Ueberschriften weiterhin vorhanden (Grep je = 1)

## Ergebnis

4d/4e beschreiben das real gelebte (und zweimal belegte) Verhalten; kuenftige
Archiv-Laeufe brauchen keine dokumentierte Abweichung mehr. INBOX #65 ist damit
bestandsbereinigt (die Grundsatzfrage 4e-Warnung-Design bleibt dort nicht zurueck —
der Eintrag kann nach Abnahme geschlossen werden).

---

**Erfasst mit:** `/dtb:task`
