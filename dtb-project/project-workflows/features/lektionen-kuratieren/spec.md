# Feature: Lektionen kuratieren

**Erstellt:** 2026-10-27
**Ziel:** Ein vom Menschen gestarteter Lauf haelt die Lektionen-Sammlung kompakt, indem er ueberholte, doppelte und schon gehobene Lektionen mit Beleg zum Ausmustern vorschlaegt und Bestaetigtes mit Grund ins Archiv verschiebt statt es zu loeschen.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

`lessons.md` ist auf 56 KB gewachsen und wird von sechs Skills bei jedem Lauf als Prior geladen; die bestehende 150-Zeilen-Warnung schlaegt nie an, weil eine Lektion eine einzige lange Zeile ist. Der neue Skill `dtb:lesson-curate` prueft den vollen Bestand nach dem Vorbild der Vorsortierung (`dtb:idea-triage`) und verschiebt nur, was der Mensch bestaetigt, nach `archive/lessons-ausgemustert.md`. Damit loest er zugleich den Widerspruch zwischen „append-only" und „aussortieren": append-only gilt fuers Schreiben, die Entnahme laeuft ausschliesslich ueber diesen Skill.

---

## Scope / Abgrenzung

### Enthalten
- **Pruefung des vollen Bestands je Lauf** (kein Lesestand) — Lektionen veralten durch spaetere Skill-Aenderungen, nicht durch ihr Alter
- **Drei Ausmusterungs-Gruende**, je mit pruefbarem Beleg (`datei:zeile`):
  - **ueberholt** — die beschriebene Mechanik gibt es nicht mehr oder ein Skill erzwingt die Regel inzwischen selbst; ein Abwesenheits-Beleg (Begriff + Suchraum ohne Treffer) traegt nur zusammen mit der Stelle der Nachfolge-Mechanik Sicherheit `hoch`
  - **doppelt** — eine andere Lektion ersetzt sie ohne Informationsverlust (Ersetzungsprobe)
  - **schon gehoben** — die Regel steht bereits versioniert in `skills/CLAUDE.md` (Kit) bzw. einer Projekt-Regeldatei unter `{rules}/` (ohne `lessons.md`, `DERIVED_STATE_RULES.md`)
- **Pruefung in Portionen** durch read-only Hintergrund-Agenten, inline bei kleinem Bestand; je Lektion ein Urteil mit Sicherheit (hoch/mittel/niedrig)
- **Uebersicht vor der Vorlage:** Bestand, Vorschlaege je Grund, erwartete Einsparung in KB
- **EINE vorbefuellte Sammelliste mit Veto** — nur Sicherheit `hoch` mit Beleg; `doppelt` nur bei einseitiger Ersetzung (bleibende Lektion benannt und deckt die andere vollstaendig ab)
- **Einzelfaelle** fuer Sicherheit `mittel`, `hoch` ohne pruefbaren Ort, offene „wer bleibt"-Fragen, Ketten und Kreise bei `doppelt` — gekappt per `lessons.einzeln_pro_lauf` (Default 5). Nicht vorgelegt, sondern behalten: Teilueberlappung (Ersetzungsprobe nicht erfuellt → `behalten`) und Agent-Ausfaelle (`nicht geprueft`, nur als Zahl in der Bilanz) — angeglichen 2026-10-28 nach Selbstpruefung 4.2 und impl-review
- **Im Zweifel behalten:** Sicherheit `niedrig` gilt als `behalten` und erscheint nur als Zahl; `behalten` wird nie vorgelegt
- **Sofortiges Schreiben je bestaetigter Entscheidung:** erst ins Archiv, dann Entnahme aus `lessons.md` — die Nummer bleibt erhalten und wird nie neu vergeben
- **Archiv `archive/lessons-ausgemustert.md`**, append-only, Selbstanlage beim ersten Schreiben, versioniert wie `lessons.md`
- **Selbstheilung zu Laufbeginn:** Nummern, die in `lessons.md` UND im Archiv stehen (Abbruch zwischen beiden Schreibschritten), werden gemeldet und die Entnahme nachgeholt — ohne doppeltes Archivieren
- **Abschluss-Bilanz:** Ausgemustertes mit Grund, nicht geprueft (Ausfall), neuer Umfang (Zeilen/KB), Hebe-Hinweis fuer Lektionen mit `Applies-to: alle` (nur Hinweis)
- **Groessen-Mass in KB statt Zeilen:** neue Schwelle `lessons.schwelle_kb` (Default 40) in `dtb:lesson`; die Warnung verweist auf `dtb:lesson-curate` und steht an genau einer Stelle
- **Nummernvergabe in `dtb:lesson`:** naechste Nummer = Maximum ueber `lessons.md` UND Archiv (sonst entstuende nach Ausmusterung der hoechsten Nummer ein Duplikat)
- **Kopftext** von `lessons.md` und des Anlage-Templates in `dtb:lesson`: append-only fuers Schreiben, Entnahme nur ueber `dtb:lesson-curate`; dabei veraltete Leser-Liste korrigieren
- **Begleitende Anzeigen und Doku:** Dashboard-Kennzahl Lektionen in KB; Voll-Guard-Tabelle, Liste schreibender Skills und Rueckfragen-Defaults in `skills/CLAUDE.md`; Skill-Liste und Output Location in `CLAUDE.md`/`README.md`; Pipeline-Frontmatter des neuen Skills
- **Voll-Guard:** der Skill laeuft nur im Haupt-Checkout (`lessons.md` und `archive/` sind global geteilt)
- **Nur vom Menschen gestartet** (`disable-model-invocation: true`)

### Nicht enthalten
- Lektionen umformulieren, zusammenfuehren oder kuerzen — nur ganz ausmustern oder behalten
- Regeln selbst nach `skills/CLAUDE.md` oder `{rules}/` heben — der Skill erkennt „schon gehoben", das Heben bleibt beim Menschen bzw. `dtb:lesson`
- Aenderungen an den Prior-Lesern (impl-plan, debug-plan, plan-review, impl-review, implement, feature-fast) — sie lesen weiter nur `lessons.md`, nie das Archiv
- Aenderungen an den Duplikat-Pruefern (`dtb:lesson` Duplikat-Check, `dtb:no-loss-check`, `dtb:idea-triage` Lektions-Abgleich) — das Archiv ist Ablage, kein Vergleichsbestand
- Ein eigener Schwellen-Hinweis im Checkpoint (waere ein zweiter Spiegel der Warnung)
- Wiederherstellung der fehlenden Lektionen 22–34 (beim Versionieren 2026-09-07 nie eingecheckt)
- Automatisches Anspringen

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Eine noch tragende Lektion wird zu Unrecht ausgemustert — ein schon gemachter Fehler kann sich wiederholen | Mittel | Hoch | Asymmetrie „im Zweifel behalten": nur `hoch` + Beleg in die Sammelliste, `mittel` einzeln, `niedrig` behalten; jede Ausmusterung bestaetigt der Mensch; Archiv + Git-Historie als zwei Rueckwege |
| Agent-Ausfall sieht aus wie ein Befund („nichts gefunden") | Mittel | Mittel | Werkzeug-Fehlschlag ist kein Datenbefund: betroffene Portion gilt als `nicht geprueft → behalten`, Bilanz meldet sie; Totalausfall → Abbruch ohne Schreiben |
| Abbruch zwischen Archiv-Schreiben und Entnahme hinterlaesst eine Lektion an beiden Orten | Niedrig | Niedrig | Reihenfolge Archiv vor Entnahme (nichts geht verloren) + Selbstheilung zu Laufbeginn |
| Nach Ausmusterung der hoechsten Nummer vergibt `dtb:lesson` dieselbe Nummer erneut | Hoch (ohne Gegenmassnahme) | Mittel | Nummernvergabe ueber `lessons.md` UND Archiv |
| Die KB-Warnung erreicht Checkpoint und idea-triage nicht, weil deren Referenz auf `dtb:lesson` die Warn-Unter-Sektion nicht mit ausfuehrt | Mittel | Niedrig | impl-plan prueft die Referenz-Reichweite; Warnung bleibt an einer Stelle |
| Parallele Session schreibt waehrend des Laufs eine neue Lektion | Niedrig | Mittel | Entnahme nur zeilenweise mit exaktem Zeilen-Anker, nie Neuschreiben der Datei; Voll-Guard haelt Worktree-Sessions ganz fern |
| `doppelt`-Ketten (bleibende Lektion ist selbst Kandidat) lassen beide verschwinden | Niedrig | Hoch | Bleibende Lektion eines Paares im selben Lauf gesperrt; Ketten und Kreise → Einzelfall |
| Textkonflikt mit dem parallelen Worktree `dashboard-projektname-hintergrund` (gleiche Dashboard-Skill-Datei, andere Stelle) | Mittel | Niedrig | Beim Merge auf Textkonflikt achten; Reihenfolge egal |

---

## Dependencies

### Erforderlich vor Start
- [x] Discovery abgeschlossen (`features/lektionen-kuratieren/discovery.md`)
- [ ] `dtb:idea-triage` als Vorbild gelesen (Portionen, Belegpflicht, Sammelliste, Einzelfaelle, Kappung, Werkzeug-Fehlschlag)

### Referenz-Dokumente
- `features/lektionen-kuratieren/discovery.md` — Anforderungen, Randfaelle, Einschraenkungen, Integrationspunkte
- `skills/dtb-idea-triage/SKILL.md` — Vorbild fuer Ablauf und Entscheidungsformen
- `skills/dtb-lesson/SKILL.md` — Zeilenform, Schreibmechanik, Groessen-Warnung, Nummernvergabe
- `skills/CLAUDE.md` — Rueckfragen-Defaults (Veto-Form), Worktree-Guard, Schreibgrenzen-Regel
- `archive/INBOX-BEFUNDE-verworfen.md` (Format in `dtb:idea-triage`) — Vorbild fuer das Archiv
- `dtb-project/project-rules/lessons.md` — Bestand (Lektion 10: Ersetzungsprobe statt Quote; Lektion 7: Werkzeug-Fehlschlag ≠ Datenbefund)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `dtb:lesson-curate` existiert, ist nur vom Menschen startbar und bricht im verlinkten Worktree vor dem ersten Schreiben ab
- [ ] Ein Lauf im Haupt-Checkout prueft den vollen Bestand und legt EINE Sammelliste vor, in der jede Zeile Grund, Beleg (`datei:zeile`) und Sicherheit `hoch` traegt
- [ ] Bestaetigte Lektionen stehen danach mit Grund, Datum und unveraenderter Nummer im Archiv und nicht mehr in `lessons.md`; nicht bestaetigte sind unveraendert
- [ ] Ein simulierter Abbruch zwischen Archiv und Entnahme wird beim naechsten Lauf erkannt und ohne Doppel-Archivierung geheilt
- [ ] Ein simulierter Agent-Ausfall fuehrt zu `nicht geprueft → behalten` in der Bilanz, nicht zu einem Ausmusterungs-Vorschlag
- [ ] `dtb:lesson` vergibt nach Ausmusterung der hoechsten Nummer eine neue, noch nie benutzte Nummer
- [ ] `dtb:lesson` warnt nach KB gegen `lessons.schwelle_kb` (Default 40) und verweist auf `dtb:lesson-curate`; die 150-Zeilen-Warnung ist weg
- [ ] Kopftext von `lessons.md` und Anlage-Template sagen dasselbe: append-only fuers Schreiben, Entnahme nur ueber `dtb:lesson-curate`
- [ ] Dashboard zeigt die Lektionen-Kennzahl in KB gegen die Schwelle
- [ ] `skills/CLAUDE.md`, `CLAUDE.md` und `README.md` fuehren den Skill, seinen Voll-Guard und die neue Output Location
- [ ] Erster echter Lauf am Kit-Bestand (heute 56 KB) ist durchgefuehrt und die Bilanz im Session-Log festgehalten

---

## Offene Punkte

- Fuehren `dtb:workflow-checkpoint` (Verlustfunde) und `dtb:idea-triage` (Lektion erfassen) bei ihrer Referenz auf `dtb:lesson` Schritt 4 die Unter-Sektion „Groessen-Warnung" mit aus? Sonst erbt die KB-Warnung nicht — in impl-plan klaeren
- Archiv-Spalten: Lektionen-Spalten plus `Ausgemustert am` / `Grund` / `Beleg` — in impl-plan festlegen
- Soll der `lessons:`-Block ins Config-Template von `dtb:project-init`, oder reicht der Default-Rueckfall im Skill (das Template traegt heute nur `status:`)? — in impl-plan entscheiden
- Traegt der Default `schwelle_kb: 40` nach dem ersten echten Lauf? Gegenpruefen am Ergebnis (heute 56 KB) — **beantwortet 2026-10-29:** nein; nach dem Lauf 92 von 96 gueltig, 56 KB — Default auf 80 KB angehoben (L111)

---

**Erstellt mit:** `/dtb:feature-plan`
