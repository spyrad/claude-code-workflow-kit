# Feature: Output-Style „gezielt"

**Erstellt:** 2026-08-07
**Ziel:** Eine global geltende, schaltbare Stil-Anweisung als versioniertes Kit-Artefakt ausliefern, die Claudes Fliesstext auf Orientierung statt Vollstaendigkeit ausrichtet.
**Prioritaet:** Mittel <!-- nicht ausdruecklich festgelegt, s. Offene Punkte -->
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

<!-- Lint-Override: Der Spec-Gegenstand ist selbst ein Kit-/Konfigurations-Artefakt (eine Stil-Datei
     und ihre Verteilung durch das Kit). Nach der Meta-Spec-Ausnahme des Technical-Leak-Lints sind
     Referenzen auf dieses Artefakt und auf das Skill-/Workflow-System legitim: Dateiorte,
     Frontmatter-Felder, Skill-Namen und Klassen-Bezeichnungen sind hier der Gegenstand, nicht ein
     durchgesickertes Loesungsdetail. -->

---

## Executive Summary

Claudes Antworten sind heute ausfuehrlicher als noetig: Begruendungen, Vergleiche und
Vorwegnahmen moeglicher Rueckfragen erscheinen unaufgefordert, wodurch der eigentliche Kern
— worum es geht, was der Stand ist, was zu entscheiden ist — untergeht. Dieses Feature liefert
eine Stil-Vorgabe aus, die genau diese Redundanz adressiert, ohne Erklaerungen zu verbieten.

Sie wird als **Kit-Artefakt** gepflegt und verteilt statt als lokale Einstellung. Grund: eine
maschinenlokale Datei existiert auf der zweiten Maschine nicht und driftet unbemerkt — das
Muster, das im Ideen-Bestand als Zwei-Maschinen-Divergenz belegt ist. Als Kit-Artefakt ist die
Vorgabe versioniert, reviewbar und auf beiden Maschinen identisch.

---

## Scope / Abgrenzung

### Enthalten

- **Eine Stil-Vorgabe fuer den Fliesstext ausserhalb der Skill-Report-Vorlagen** — Erklaerungen,
  Begruendungen, Zwischenkommentare, Einschaetzungen. Leitsatz (Nutzer-Formulierung 2026-08-07,
  ausdruecklich „gezielt" statt „sparsam"):

  > Jeder Ausgabe muss auf einen Blick zu entnehmen sein: **worum es geht**, **was der Stand
  > bzw. das Problem ist**, und **welche Entscheidung verlangt wird**. Erklaerungen dazu kurz,
  > knapp, einfach — reduziert auf das Wichtigste, nicht weggelassen.

  Der Gegner ist **Vorwegnahme und Redundanz**, nicht Erklaerung. Gliedernde Mittel bleiben
  ausdruecklich erlaubt, weil sie der Uebersicht dienen.

- **Geltung: global und workflow-uebergreifend** — nicht auf Aufrufe des Workflow-Systems
  beschraenkt, sondern in allen Projekten der jeweiligen Maschine wirksam.

- **Schaltbarkeit** — die Vorgabe laesst sich ein- und ausschalten, ohne sie zu entfernen.

- **Auslieferung als Kit-Artefakt der versionierten Klasse:** Quelle im Kit-Repo, Verteilung
  ueber `dtb:kit-sync` in den nutzerweiten Ablageort. Erfassung als **Muster**, nicht als
  Einzeleintrag — eine spaeter hinzukommende zweite Stil-Datei ist damit ohne Aenderung an
  `dtb:kit-sync` abgedeckt (analog zur bestehenden Regel fuer neue Skills).

- **Eine Ausnahme-Klausel in der Vorgabe selbst:** Wird ausdruecklich um Analyse, Begruendung
  oder Vergleich gebeten, gilt die Beschraenkung nicht. Bewusst in der Datei verankert statt
  ueber Umschalten geloest, weil ein Wechsel einen Sessionneustart erfordert und mitten in der
  Arbeit trifft.

- **Eine Vorrang-Regel:** Gibt ein Skill ein Ausgabeformat vor, gilt das Format; die Stil-Vorgabe
  wirkt nur auf den Text drumherum.

- **Eine Pruefung in `dtb:project-health`,** die meldet, wenn die Vorgabe zwar installiert, aber
  nicht aktiviert ist.

### Nicht enthalten

- **Die Vereinheitlichung der Report-Laengen der Skills.** 25 von 39 Skills tragen heute eine
  Laengenvorgabe, mit sechs verschiedenen Werten; 14 tragen keine. Das ist ein eigener Zuschnitt
  und trifft das Anliegen dieses Features nicht.
- **Wirkung in Sub-Agenten.** Stil-Vorgaben dieser Art greifen nur in der Hauptkonversation;
  Sub-Agenten arbeiten mit eigener Grundanweisung. Die Sub-Agenten von `dtb:impl-review` und
  `dtb:plan-review` bleiben also unberuehrt. Bewusst akzeptiert.
- **Aenderung der Sprache.** Deutsch bleibt; die Sprachwahl wird an anderer Stelle gesteuert.
- **Kuerzung von Substanz** — Belege, Zahlen und Zitate bleiben vollstaendig. Knappheit trifft
  Redundanz, nicht Inhalt.
- **Jeder Schreibzugriff auf Zielprojekte.** Weder im Projekt-Workflow-Baum noch in einer
  projektlokalen Konfiguration entsteht etwas. Das Feature wirkt auf Nutzer-Ebene und im Kit-Repo.
- **Praejudiz fuer andere Bausteine.** Die Antwort „Kit-Artefakt statt lokale Einstellung" gilt
  ausdruecklich **nur** fuer Stil-Vorgaben. Idee #41 (Sprachausgabe) und #45 (ereignisgebundene
  Automatisierung) bleiben eigenstaendig zu entscheiden — Nutzer-Entscheid 2026-08-07.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Die Vorgabe beschneidet bewusst gesetzte Report-Strukturen der Skills | Mittel | Hoch | Vorrang-Regel in der Datei; Gegenprobe in der Abnahme mit mindestens einem Skill-Lauf, dessen Report ein festes Format hat |
| Das Feld, das die eingebauten Entwicklungs-Anweisungen erhaelt, wird vergessen — sie entfallen dann vollstaendig | Mittel | **Sehr hoch** | Als Pflichtangabe in den Erfolgskriterien verankert und beim Abnahmelauf ausdruecklich geprueft |
| Zweite Maschine: Datei verteilt, Schalter nicht gesetzt — die Vorgabe liegt inaktiv herum | **Hoch** | Mittel | Pruefung in `dtb:project-health`; ohne sie waere es genau das Divergenz-Muster aus #34 |
| Wirkung ist subjektiv und schwer abnehmbar — „wirkt der Stil?" ist ein Urteil, kein Messwert | Hoch | Mittel | Abnahme an nachvollziehbaren Faellen statt am Gesamteindruck; Vorgehen ist offen (s. Offene Punkte) |
| Die Vorgabe wirkt zu stark und unterdrueckt noetige Begruendungen | Mittel | Mittel | Ausnahme-Klausel; Nachschaerfen nach Erprobung ist billig, weil die Datei versioniert ist |
| Erste Erweiterung der Artefakt-Klassen des Kits ueberhaupt — kein Praezedenzfall im Bestand | Mittel | Hoch | Spiegel-Kopplung geschlossen ziehen (Verteil-Skill, Contributor-Guide, Wurzel-Dokumentation); `dtb:plan-review` ist hier nicht optional |
| Dauerhafte Zusatzkosten, weil die Vorgabe in jeder Sitzung mitgetragen wird | Hoch | Niedrig | Laengenobergrenze von rund 40 Zeilen; eine ausufernde Stil-Anweisung waere zudem inhaltlich unglaubwuerdig |
| Eine projektlokale Einstellung ueberschreibt die globale ohne Vorwarnung | Niedrig | Niedrig | Als bekannte Einschraenkung dokumentieren, nicht bekaempfen — es ist die gewollte Vorrangordnung der Umgebung |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine. Idee #45 war als Vorbedingung im Gespraech, ist mit der Entscheidung fuer
      workflow-uebergreifende Geltung aber **entfallen** — die ereignisgebundene Variante wurde
      nur gebraucht, um die Wirkung auf Workflow-Aufrufe zu begrenzen.

### Referenz-Dokumente

- `dtb-project/project-workflows/features/output-style-gezielt/discovery.md` — Discovery mit der
  vollstaendigen Mechanik-Pruefung und dem Zustand beider Ablageorte
- `dtb-project/project-workflows/INBOX.md` #40 — Ursprungsidee samt Hebel-Sichtung
- `skills/CLAUDE.md` — Contributor-Guide; fuehrt die Artefakt-Klassen und traegt bis heute keinen
  Abschnitt zu Ausgabe und Stil
- `skills/dtb-kit-sync/SKILL.md` — Klassen-Tabelle und Verteilungslogik
- `skills/dtb-project-health/SKILL.md` — Ort der neuen Pruefung
- `CLAUDE.md` (Wurzel) — beschreibt das Verteilungsmodell
- Offizielle Dokumentation zu Ausgabe-Stilen, abgerufen 2026-08-07 —
  https://code.claude.com/docs/en/output-styles

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] Die Stil-Datei liegt versioniert im Kit-Repo, umfasst hoechstens rund 40 Zeilen und traegt
      die Angabe, die die eingebauten Entwicklungs-Anweisungen erhaelt
- [ ] Sie enthaelt Leitsatz, Ausnahme-Klausel und Vorrang-Regel in ausformulierter Form
- [ ] `dtb:kit-sync` erfasst sie ueber ein **Muster** — belegt dadurch, dass eine testweise
      zweite Datei ohne Aenderung am Verteil-Skill mitgenommen wuerde
- [ ] Ein Verteilungslauf legt sie am nutzerweiten Ablageort ab; die anschliessende Pruefung
      meldet null Abweichungen ueber alle drei Vergleichspunkte
- [ ] `dtb:project-health` meldet den Zustand „installiert, aber nicht aktiviert" korrekt —
      geprueft in **beiden** Richtungen (Meldung erscheint bei inaktivem Schalter, verschwindet
      nach Aktivierung)
- [ ] Nach Aktivierung ist in einer echten Sitzung nachvollziehbar, dass Antworten den Leitsatz
      erfuellen (Vorgehen der Abnahme s. Offene Punkte)
- [ ] **Gegenprobe:** Mindestens ein Skill mit festem Ausgabeformat laeuft unveraendert durch —
      die Vorrang-Regel greift
- [ ] Contributor-Guide und Wurzel-Dokumentation fuehren die neue Klasse; die Spiegel-Kopplung
      ist geschlossen und verifiziert

---

## Offene Punkte

- Sprache der Stil-Datei: Deutsch wurde angenommen (Kit-Konvention fuer Inhalte), vom Nutzer aber
  nicht ausdruecklich bestaetigt.
- Prioritaet wurde nicht festgelegt; „Mittel" ist ein Platzhalter und keine Entscheidung.
- Wie wird die Wirkung abgenommen? Der Leitsatz ist ein Urteil, kein Messwert. Denkbar waere ein
  kleiner Satz von Faellen mit erwarteter Antwortform (Vorbild: die Kalibrierung, mit der zuletzt
  ein anderer Skill abgenommen wurde) — die Form dieses Vorgehens ist offen und gehoert in den
  Implementierungsplan.
- Verhalten bestehender Sperrdateien, die den neuen Ablageort noch nicht kennen: erwartet wird,
  dass der Eintrag beim naechsten Abgleich als neu erkannt und angelegt wird. Im
  Implementierungsplan zu verifizieren, nicht anzunehmen.

---

**Erstellt mit:** `/dtb:feature-plan`
