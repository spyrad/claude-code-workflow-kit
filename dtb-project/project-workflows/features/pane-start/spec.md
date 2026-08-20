# Feature: pane-start

**Erstellt:** 2026-08-19
**Ziel:** Eine interaktive Voll-Schiene-Session laesst sich mit einem Befehl in einer eigenen Pane und einem eigenen Worktree starten, fertig eingerichtet und ueber ihren Rueckweg informiert.
**Prioritaet:** Hoch
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Der autonome Worker automatisiert seinen Hinweg vollstaendig, aber nur fuer autonome,
aufgabenbasierte Auftraege. Wer eine Idee interaktiv auf der Voll-Schiene bearbeiten will,
richtet den Arbeitsplatz heute von Hand ein: Worktree anlegen, Pane oeffnen, Session
starten, Kontext hineintragen — und der Rueckweg laeuft per Copy-Paste. Dieses Feature
schliesst genau diese Luecke mit einem duennen Start-Skill: er richtet den Arbeitsplatz ein
und stellt der neuen Session EINEN Begruessungstext zu, der Arbeitsplatz, Startbefehl,
Orchestrator-Adresse und Rueckweg-Pflicht enthaelt. Die Mechanik dafuer existiert und ist
real belegt; neu ist ausschliesslich, dass ein Mensch statt eines autonomen Auftrags
empfangen wird — mit der Folge, dass die gesamte Autonomie-Governance ersatzlos entfaellt.

---

## Scope / Abgrenzung

### Enthalten
- Aufloesung eines Arguments (Ideen-Nummer aus der Inbox oder bestehender Change-Slug) zu
  genau einem Change; bei einer Ideen-Nummer ein Vorschlag fuer die Startschiene
- Hartes Eignungs-Gate auf die Pane-Umgebung: fehlt sie, bricht der Skill ab und nennt
  Alternativen, statt still auf einen anderen Traeger auszuweichen
- Einrichtung des Arbeitsplatzes: eigener Worktree mit eigenem Branch pro Change
- Start und Erkennung der interaktiven Session in einer neuen, nicht fokussierten Pane
- Zustellung des Begruessungstexts als EINE Nachricht
- Verweis-Kopplung: der Skill nennt die bestehende Kommando-Sequenz als seine Quelle, die
  Quelle nennt ihren neuen Leser (beidseitig, damit spaetere Drift an einer Stelle
  korrigiert wird)
- Einordnung in die bestehenden Konventionen: Guard-Kategorie, Skill-Katalog, Abgrenzung
  gegen die Autonomie-Regel

### Nicht enthalten
- Die Kommando-Sequenz selbst: sie wird referenziert, nicht kopiert — ein dritter Ort
  waere genau der Drift-Fall, den die bestehende Ein-Quelle-Regel verhindert
- Der Rueckweg: das Uebergabe-Format und seine Empfangsseite bleiben unveraendert
- Zusammenfuehren, Abnahme und Abbau des Arbeitsplatzes — das bleibt beim Menschen; das
  bestehende Abschluss-Muster wird nur referenziert
- Jede Form von Deckelung oder Tauglichkeitsurteil: es sitzt ein Mensch in der Session
- Mehrere Sessions pro Aufruf (v1 startet genau eine)
- Korrektur der bekannten, pauschalen Branch-Aussage im Checkpoint-Skill (eigener,
  bereits offener Nachlauf)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Drift der Kommando-Sequenz, weil der neue Skill sie faktisch doch mitfuehrt | Mittel | Hoch | Sequenz nie zitieren, nur verweisen; beidseitiger Kopplungs-Hinweis; Spiegel-Pruefung mechanisch per Grep als Abnahmekriterium |
| Der neue Skill wird faelschlich unter die Autonomie-Regel gelesen (Deckelung, Report-Pflicht) | Mittel | Mittel | Abgrenzungssatz an der Regel selbst; die Spec nennt das Fehlen der Governance als gewollte Eigenschaft, nicht als Luecke |
| Session-Erkennung schlaegt fehl, der Arbeitsplatz bleibt halb eingerichtet zurueck | Mittel | Mittel | Ein Wiederholungsversuch, dann Abbruch mit sichtbarem Pane-Inhalt; Aufraeum-Hinweis nennt Worktree und Branch namentlich |
| Verwaiste Arbeitsplaetze haeufen sich, weil der Abschluss ausserhalb des Skills liegt | Mittel | Niedrig | Der Begruessungstext nennt die Rueckweg-Pflicht; der Abschluss-Hinweis verweist auf das bestehende Abbau-Muster |
| Der Start laeuft auf uncommitteter Arbeit und die Session sieht sie nicht | Niedrig | Mittel | Vorbedingung pruefen und melden, bevor der Arbeitsplatz entsteht |

---

## Dependencies

### Erforderlich vor Start
- [x] Fundament aus #67 vorhanden: Start-Sequenz, Eignungs-Gate und Ein-Nachricht-Zustellung sind umgesetzt und real belegt
- [x] Uebergabe-Format mit traegerneutraler Empfangsseite vorhanden
- [ ] Keine (weitere) Vorbedingung

### Referenz-Dokumente
- `skills/dtb-worker/SKILL.md` - Quelle der Pane-Mechanik (Start-Sequenz, Eignungs-Gate, Abschluss-Muster)
- `skills/dtb-workflow-checkpoint/SKILL.md` - Quelle des Uebergabe-Formats (nur gelesen)
- `skills/CLAUDE.md` - Guard-Vorlage, Skill-Kategorien, Autonomie-Regel, Schreibgrenzen-Regel
- `dtb-project/project-workflows/features/pane-start/discovery.md` - Erhebung zu diesem Feature
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - Slug-Regeln, Statusableitung

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Aufruf mit gueltigem Argument fuehrt zu einer laufenden Session in einer eigenen Pane, die ihren Arbeitsplatz kennt und ihren Startbefehl vorgeschlagen bekommt — ohne manuelles Hineinkopieren
- [ ] Fehlt die Pane-Umgebung, bricht der Skill mit Alternativen ab und weicht auf keinen anderen Traeger aus
- [ ] Aus einem verlinkten Worktree aufgerufen, bricht der Skill hart ab
- [ ] Der Begruessungstext kommt vollstaendig als EINE Nachricht an und nennt Arbeitsplatz, Startbefehl, Orchestrator-Adresse und Rueckweg-Pflicht
- [ ] Die Kommando-Sequenz existiert nach der Umsetzung an unveraendert zwei Orten; der neue Skill verweist darauf und wird dort als Leser genannt (beidseitig per Grep belegbar)
- [ ] Keine Deckelung, kein Tauglichkeitsurteil und kein Bericht sind im neuen Skill vorhanden; die Autonomie-Regel grenzt ihn ausdruecklich aus
- [ ] Der Skill erscheint in der Guard-Kategorien-Tabelle und im Skill-Katalog und wird von der Verteilung erfasst

---

## Offene Punkte

- Ob spaeter mehrere Sessions pro Aufruf sinnvoll sind (Analogie zur bestehenden
  Warteschlange), bleibt bewusst offen — v1 startet genau eine
- Die pauschale Branch-Aussage im Checkpoint-Skill bleibt bis zu ihrem eigenen Nachlauf
  ungenau; dieses Feature aendert sie nicht

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-19)
