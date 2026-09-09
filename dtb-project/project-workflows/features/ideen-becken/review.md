# Review-Snapshot: ideen-becken
Scope: 13 Dateien aus 4 Commits · Geprueft bis: `d5e8dad` · Datum: 2026-09-08
Gesamt-Verdikt: REJECTED (5 blocking)

Achsen: Plan Adherence WARNING (4) · Scope Discipline PASS (0) · Safety & Quality FAIL (5) ·
Architecture FAIL (2) · Pattern Consistency FAIL (4) · Rules uebersprungen (keine Coding-Rules)

Drift-Bilanz: 11 MATCH / 3 DRIFT / 0 MISSING / 0 EXTRA · SHA-Vollstaendigkeit 14/14

## Findings

### F1 — Safety & Quality — [S:Hoch x I:Hoch] — craft/principled, blocking
`skills/dtb-idea-triage/SKILL.md`:5a vs. 5b — Die beiden Ausgaenge des Beckens loesen dieselbe
Sache gegenlaeufig: Verwerfen schreibt erst ins Archiv und entfernt dann aus dem Becken;
Befoerdern entfernt erst die Becken-Zeile und schreibt dann nach `INBOX.md`. Bricht der Lauf
dazwischen ab, ist der Eintrag ersatzlos weg — und die Zusage "nie zurueckrollen" macht den
Verlust endgueltig. Kritischer Pfad (Datenverlust), voller Standard.
Fix: Reihenfolge in 5a auf die von 5b ziehen — erst nach `INBOX.md` schreiben inkl.
Spaltenzahl-Pruefung, dann die Becken-Zeile entfernen. Ein Zwischenabbruch hinterlaesst dann
eine Dublette, die der naechste Duplikat-Check sieht, statt eines Lochs.
Decision: FIXED

### F2 — Safety & Quality — [S:Hoch x I:Hoch] — craft/principled, blocking
`skills/dtb-workflow-checkpoint/SKILL.md`:302 — Der Struktur-Check loest "nur die Quellen auf,
deren Typ in der DRINGENDEN GRUPPE vorkommt". Der Eingang wurde aber auf Ideen aus
`## Kann warten` erweitert. Ein Lauf mit leerer dringender Gruppe und zwei Kann-warten-Ideen
loest keine Quelle auf, findet keinen Anker — und schreibt trotzdem. Der Kopplungs-Waechter, der
genau dieses Schreiben absichern soll, wird durch die Erweiterung umgangen.
Fix: Bedingung auf "deren Typ in der VORLAGE vorkommt" umstellen; zusaetzlich die Platzhalter
der beiden Fehlerpfade auf `dtb:{lesson|idea|idea-triage}` erweitern.
Decision: FIXED

### F3 — Architecture — [S:Mittel x I:Hoch] — craft/torvalds + drift, blocking
`skills/dtb-workflow-checkpoint/SKILL.md`:13-14, `skills/dtb-no-loss-check/SKILL.md`:15,
`skills/dtb-idea/SKILL.md`:14, `skills/dtb-project-health/SKILL.md`:11 — Vier `pipeline`-Bloecke
laufen dem Koerper hinterher: keiner nennt `INBOX-BEFUNDE.md`, obwohl der Checkpoint dorthin
schreibt und es liest, `no-loss-check` dagegen abgleicht, `dtb:idea` es fuer die Nummernvergabe
liest und `project-health` es prueft. Genau dieser Block ist die maschinelle Quelle fuer
`workflow-status`, `pipeline-graph` und den Health-Lint — der Kontrakt ist stumm zur wichtigsten
neuen Datei. (Vom Drift-Agent unabhaengig als DRIFT zu Schritt 2.2 gemeldet.)
Fix: `INBOX-BEFUNDE.md` in allen vier Bloecken nachziehen — Checkpoint in `consumes` UND
`produces`, die uebrigen drei in `consumes`.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel x I:Hoch] — craft/principled, blocking
`skills/CLAUDE.md`:296-298 — Die neue verbindliche Regel "Abgleiche lesen beide Dateien" ist im
Moment ihrer Niederschrift fuer zwei von drei Duplikat-Checks falsch: `dtb:idea` sucht nur
`INBOX.md`, und die Befoerderung in `dtb:idea-triage` sucht ABSICHTLICH nur `INBOX.md` (ein
Treffer gegen die eigene Herkunft waere immer positiv). Eine Konvention, die kategorisch etwas
verlangt, was der neue Skill mit Begruendung nicht tut, erzeugt beim naechsten Leser entweder
einen falschen "Fix" oder eine ignorierte Regel.
Fix: Bullet auf die tatsaechlichen Konsumenten einschraenken — "Verlustpruefung und der
Ideen-Duplikat-Check des Checkpoints lesen beide Dateien; die Befoerderung prueft nur
`INBOX.md` (Herkunfts-Selbsttreffer)".
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel x I:Mittel] — craft/principled, blocking
`skills/dtb-no-loss-check/SKILL.md`:312 gegen `skills/dtb-workflow-checkpoint/SKILL.md`:288 —
Die Unterdrueckung der Abschlussfrage haengt an "Aufruf aus dem Checkpoint MIT nicht-leerer
dringender Gruppe". Der Checkpoint hat seine Bedingung auf "ohne vorlage-faehigen Fund entfaellt
der Block still" umgestellt. Im neuen Fall — dringende Gruppe leer, Kann-warten-Ideen vorhanden —
stellt `no-loss-check` seine Frage UND der Checkpoint zeigt die Vorlage: zwei Fragen uebereinander.
Das ist wortgleich INBOX #73; die Aenderung vergroessert dessen Trefferflaeche.
Fix: Bedingung auf "mit nicht-leerer Vorlage (dringende Gruppe ODER Ideen-Funde)" umformulieren —
derselbe Satz auf beiden Seiten.
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel x I:Mittel] — craft/principled, non-blocking
`skills/dtb-workflow-checkpoint/SKILL.md`:281/344/360/369 — Nach der Eingangs-Erweiterung ist das
"dringend"-Vokabular nicht nachgezogen: Ueberschrift, Vorlagenkopf `{D} dringend`,
Abbruchmeldung und vor allem die Kappung "Mehr als 10 DRINGENDE Funde → keine Vorlage". Bei 2
dringenden und 25 Kann-warten-Ideen greift die Kappung nicht und die Vorlage wird 27 Zeilen lang —
genau die Unbenutzbarkeit, gegen die die Kappung gebaut wurde.
Fix: Zaehlwort fuer die Vorlagenmenge einfuehren (z.B. `{V}`) und Ueberschrift, Kopfzeile,
Kappung und Abbruchmeldung darauf ankern; `{D}` nur noch dort, wo Dringlichkeit gemeint ist.
Decision: FIXED

### F7 — Pattern Consistency — [S:Mittel x I:Mittel] — craft/principled, non-blocking
`skills/dtb-workflow-checkpoint/SKILL.md`:246-247 + `skills/dtb-project-health/SKILL.md`:98 gegen
`skills/dtb-idea-triage/SKILL.md`:312 — "Ungesichtet" ist zweimal verschieden definiert:
Erinnerungs-Zaehler und Health-Check zaehlen `leer` oder `L1`, die Abschluss-Bilanz nennt
`Altbestand` ausdruecklich "noch nicht gesichtet". Nach der geplanten Migration steht ein Becken
mit 24 Altbestands-Eintraegen bei 0 "ungesichtet" — die Handoff-Erinnerung schweigt genau dann,
wenn der Rueckstand am groessten ist.
Fix: In allen drei Stellen dieselbe Definition verwenden (`leer` ∪ `L1` ∪ `Altbestand`) und den
Begriff einmal im Becken-Kopf festschreiben.
Decision: FIXED

### F8 — Safety & Quality — [S:Mittel x I:Niedrig] — craft/principled, non-blocking
`skills/dtb-no-loss-check/SKILL.md`:242-249, 289, 393 — Die Zielangabe ist als Pflichtangabe je
Fund deklariert ("Vor dem Absetzen muss sichtbar sein, wohin der Inhalt wandert"), die
Zuordnungstabelle als fest bezeichnet. Fuer Ideen-Funde stimmt beides nicht mehr: gemeldet wird
`Ziel: …/INBOX.md`, geschrieben wird nach `INBOX-BEFUNDE.md`. Der eine Ort, an dem der Mensch das
Ziel kontrollieren soll, zeigt das falsche.
Fix: Zeile fuer `INBOX-BEFUNDE.md` (versioniert) in die Tabelle aufnehmen und in den
Muster-Beispielen das Ziel der Ideen-Funde auf das Becken setzen.
Decision: FIXED

### F9 — Safety & Quality — [S:Niedrig x I:Mittel] — craft/principled, non-blocking
`skills/dtb-idea-triage/SKILL.md`:258-261 — Der Ausweg "stattdessen verwerfen" aus der
Duplikat-Rueckfrage fuehrt nirgendwohin: 5b wird nicht referenziert, damit ist offen, ob die als
Pflicht gesetzte Begruendung auf diesem Pfad gilt. Nebenbei weicht die Antwortzeile vom
verbindlichen Meldeform-Schema in `skills/CLAUDE.md` ab, ohne die Abweichung zu benennen.
Fix: Option explizit nach 5b verzweigen ("weiter wie Aktion 2 in Schritt 4, Begruendung bleibt
Pflicht") und die Schema-Abweichung als begruendeten Sonderfall vermerken.
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig x I:Mittel] — craft/principled, non-blocking
`skills/dtb-idea/SKILL.md`:141 gegen `skills/dtb-idea-triage/SKILL.md`:264 — Die Befoerderung
begruendet ihre Einfuegeposition mit einer Invariante ueber `INBOX.md` ("absteigend sortiert,
setzt #74 um"). Der zweite und weit haeufigere Schreiber derselben Datei — `dtb:idea` Schritt 2 —
sagt weiterhin nur "Fuege eine neue Zeile in die Tabelle ein". #74 ist damit fuer den Hauptfall
unerledigt, obwohl der Plan ihn als miterledigt fuehrt.
Fix: In `dtb:idea` Schritt 2 denselben Satz ergaenzen ("direkt unter der Tabellen-Trennzeile,
nicht ans Tabellenende").
Decision: FIXED

5 weitere Findings unterhalb des Caps (erneut ausfuehren nach Behebung):
- Plan Adherence: Begruendungssatz in `dtb:idea-triage` Schritt 1 behauptet weiterhin,
  `project-init` lege das Becken in neuen Projekten an — nach Entscheidung 3.1 falsch
- Plan Adherence: die zwei Mismatch-Entscheidungen (Duplikat-Check beide Dateien;
  project-init nennt statt anlegt) stehen nur in den Commit-Bodies, nicht in
  "Technische Entscheidungen"
- Plan Adherence: Wirklauf-Protokoll deckt "Fund landet im Becken" nicht ab (offen deklariert,
  nicht behauptet) und hat keine Zeile fuer "Checkpoint ≤ 470"
- Pattern Consistency: `skills/CLAUDE.md` Register (Voll-Guard-Kategorie, Lesestand-Spiegelliste)
  nennen `dtb:idea-triage` nicht — die Verifikations-Greps dieser Konvention melden das kuenftig
- Architecture (nit): `DERIVED_STATE_RULES.md` §6.4 steht vor §6.3, Gliederung nicht monoton

## Info
3 Workflow-Artefakte im Diff, bekannt — nicht bewertet (plan.md, BACKLOG.md, INBOX.md)
