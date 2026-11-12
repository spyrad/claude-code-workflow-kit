# Feature: Herdr-App-Umstellung

**Erstellt:** 2026-11-12
**Ziel:** Alle Herdr-gestützten Abläufe des Kits (Pane-Worker, interaktiver Pane-Start, Pane-Übergabe) laufen in der Herdr-App über `hc` und `herdr-app` statt über die alte `herdr`-CLI.
**Prioritaet:** Hoch
**Status:** In Arbeit <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Der Mensch arbeitet künftig nur noch in der Herdr-Desktop-App. App und alte `herdr`-CLI sind
zwei getrennte Systeme (gemessen 2026-11-12): die App fährt den eigenen Motor herdr-core (`hc`),
den die CLI nicht sieht — die Herdr-Gates des Kits greifen dort nicht, Pane-Worker und
`dtb:pane-start` sind in der App unbenutzbar. Dieses Feature stellt alle Herdr-Stellen des Kits
auf `hc`/`herdr-app` um und ersetzt dabei Stop-Hook und Überwachungs-Tick durch die eingebaute
Rückmeldung von `hc`.

---

## Scope / Abgrenzung

### Enthalten
- **Pane-Träger von `dtb:worker`:** Gate, Start eines Workers, Auftragszustellung, Lesen des
  Worker-Stands und Rückweg laufen über `hc`/`herdr-app`
- **`dtb:pane-start`:** Gate, Arbeitsplatz-Anlage und Begrüßung über `hc`/`herdr-app`; die
  Start-Sequenz bleibt per Referenz beim Worker (keine Kopie)
- **`dtb:workflow-resume` Schritt 2a:** Prüfung der Orchestrator-Adresse über `hc`
- **`dtb:workflow-checkpoint`:** Transport des Hand-off-Blocks an den Orchestrator nachziehen
- **Sichtbare Tabs:** jeder Worker und jeder `pane-start`-Arbeitsplatz erscheint als eigener,
  nach dem Slug benannter Tab in der App — kein unsichtbares Terminal (Entscheidung 2026-11-12)
- **Stop-Hook und Überwachungs-Tick ersetzen:** Worker-Meldungen (fertig, hängt an Rückfrage,
  Fehler, beendet) erreichen die Orchestrator-Session von selbst; das Abfragen per `/loop`
  entfällt (Entscheidung 2026-11-12 — direkt in diesem Feature, kein Folge-Feature)
- **Probe vor dem Umbau:** ein kurzer Test in der App belegt die Annahmen, auf denen der Umbau
  steht (siehe Dependencies)
- **Doku nachziehen:** `skills/CLAUDE.md` (Orchestrator-Muster, Autonomie-Regel) und `CLAUDE.md`
- **Lektionen und Befunde sichten:** die Herdr-Lektionen in `lessons.md` und die Herdr-Befunde
  in `INBOX-BEFUNDE.md` auf Gültigkeit unter `hc` prüfen; Ergebnis ist eine Liste
  „gilt weiter / überholt" — die Ausmusterung selbst läuft über `dtb:lesson-curate` bzw.
  `dtb:idea-triage`

### Nicht enthalten
- Parallelbetrieb beider Systeme (alte `herdr`-CLI und App) — die alten Befehle fallen komplett weg
- Neue `hc`-Fähigkeiten, die das Kit heute nicht nutzt (andere Rechner, Rollen-Vorlagen)
- Subagenten-Träger von `dtb:worker` (nutzt kein Herdr, bleibt unverändert)
- Deinstallation der alten `herdr`-CLI (entscheidet der Mensch)
- Änderungen an Freigabe, Abnahme, Hand-off-Block-Format, Übergabe-Notiz-Format,
  Begrüßungstext-Inhalt und Wartepflicht — die Abläufe bleiben, nur der Unterbau wechselt

---

## Gewuenschtes Verhalten

- Läuft die Session nicht in der App, bricht der Skill hart ab und nennt den Weg, die Session
  in der App zu starten — wie das heutige Herdr-Gate
- Kommt der erste Auftrag bei einem Worker nicht an (z. B. Vertrauens-Dialog beim Start), wird
  zuerst der Bildschirm des Workers gelesen; nie blind erneut gesendet
- Wartet ein Worker auf eine Rückfrage, meldet der Orchestrator das dem Menschen und antwortet
  nie selbst — eine Berechtigungs-Entscheidung wird nie umgangen
- Tippt der Mensch gerade im Ziel-Tab, wird eine Nachricht zurückgehalten, bis er fertig ist
- Wird das App-Fenster geschlossen, arbeiten die Worker zu Ende
- Das Kit stoppt oder startet den herdr-core-Dienst nie neu (träfe alle Terminals des Menschen)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Eine Annahme aus der `hc`-Anleitung trägt in der Praxis nicht (Adresse nicht gesetzt, Nachricht kommt nicht an, Ende wird nicht gemeldet) | Mittel | Hoch | Probe vor dem Umbau ist Pflicht; ohne Belege kein Umbau |
| Die eingebaute Rückmeldung ersetzt den Stop-Hook nicht vollständig (z. B. Turn-Ende ohne Terminal-Ende wird nicht gemeldet) | Mittel | Mittel | Probe prüft genau diesen Fall; bleibt ein Rest, wird er im Plan benannt statt still verloren |
| `hc` 0.1.20 ist jung — Befehle ändern sich mit einem Update | Mittel | Mittel | Geprüfte Version im Skill nennen; Abweichung als Hinweis, nicht als stiller Fehlschlag |
| Struktur-Checks von `pane-start` auf Abschnitts-Anker im Worker brechen, wenn Abschnitte umbenannt werden oder entfallen (Tick-Anker) | Hoch | Mittel | Anker-Liste vor dem Umbau erheben; Checks im selben Zug mitziehen und per Grep verifizieren (Kopplungsregel `skills/CLAUDE.md`) |
| Erfahrungswissen aus 11 Herdr-Lektionen geht beim Umbau verloren oder gilt ungeprüft weiter | Mittel | Mittel | Sichtung ist Teil des Scopes; jede Lektion bekommt ein Urteil mit Beleg |
| Installierte Skill-Kopien unter `~/.claude/` bleiben auf dem alten Stand | Hoch | Niedrig | `dtb:kit-sync` nach der Abnahme als Abschluss-Schritt |

---

## Dependencies

### Erforderlich vor Start
- [ ] Probe in der App: Ist die eigene Terminal-Adresse (`HC_TERMINAL_ID`) in App-Terminals gesetzt?
- [ ] Probe in der App: Kommt eine per `hc` gesendete Nachricht in einer Claude-Session an?
- [ ] Probe in der App: Meldet `hc` das Ende bzw. das Hängen eines Workers von selbst an den Auftraggeber?
- [ ] Probe in der App: Sind `hc` und `herdr-app` in einem App-Terminal direkt aufrufbar?

### Referenz-Dokumente
- `features/herdr-app-umstellung/discovery.md` - Discovery mit betroffenen Modulen und Entscheidungen
- `hc --skill` / `herdr-app --skill` - aktuelle Anleitungen der beiden Werkzeuge (Quelle der Befehls-Zuordnung)
- `skills/CLAUDE.md` - Autonomie-Regel, Orchestrator-Muster, Kopplungsregel für Spiegel
- `dtb-project/project-rules/lessons.md` - Herdr-Lektionen (u. a. 69, 87, 95, 119–124, 127)
- INBOX #98 und #182 - Nachfolger, die auf der Pane-Mechanik aufbauen (erst nach diesem Feature planen)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Die Probe ist dokumentiert und belegt alle vier Punkte aus den Dependencies (oder benennt den Rest, der nicht trägt)
- [ ] In den vier betroffenen Skills steht an keiner Wirkstelle mehr ein Befehl der alten `herdr`-CLI und keine Prüfung auf `HERDR_ENV`/`HERDR_PANE_ID`
- [ ] Ein Worker-Lauf mit Pane-Träger aus einer App-Session: eigener Tab mit dem Slug als Namen, Auftrag kommt an, Worker committet auf seinem Branch, Hand-off-Block erreicht den Orchestrator
- [ ] Das Ende eines Workers erreicht die Orchestrator-Session ohne Stop-Hook und ohne `/loop`-Abfrage
- [ ] `dtb:pane-start` aus einer App-Session: eigener Tab, Claude-Session gestartet, Begrüßung zugestellt, die Session wartet auf den Menschen
- [ ] Session-Wechsel im Arbeitsplatz-Tab (Checkpoint „Wechsel" → `/clear` → `workflow-resume`) findet die Übergabe-Notiz und prüft die Orchestrator-Adresse
- [ ] Außerhalb der App brechen `dtb:pane-start` und der Pane-Träger hart ab, mit Hinweis auf den Start in der App
- [ ] Alle Struktur-Checks zwischen `pane-start` und Worker laufen grün (Anker-Zahl per Grep verifiziert)
- [ ] Jede Herdr-Lektion und jeder Herdr-Befund hat ein Urteil „gilt weiter / überholt" mit Beleg

---

## Offene Punkte

Alle vier Punkte der Planung sind seit dem 2026-11-12 entschieden (Belege: `probe.md`, Tabelle „Technische Entscheidungen" in `plan.md`):

- Claude-Integration: nicht nötig — frische Sessions melden ihren Status ohne Zutun; die Start-Sequenz bekommt eine Hinweiszeile für den Fall, dass die Erkennung fehlt.
- Stop-Hook: entfällt ganz. Zwei Reste sind ohne Hook gelöst: die Meldepflicht des Workers je Turn-Ende und die Hand-off-Datei für einen abgewiesenen Hand-off.
- Tab mit Kind-Beziehung: Start über `hc run --bg` mit Fenster-Label, danach den Tab umbenennen; der erste Auftrag ist einzeilig und nennt eine Auftragsdatei.
- Tab nach der Abnahme: Der Orchestrator bietet das Schließen an, der Mensch bestätigt.

Noch ungeprüft, in die Abnahme (Plan-Schritt 4.1) verlegt:

- Trifft eine Meldung ein, während der Mensch beim Orchestrator tippt — wird sie zurückgehalten?
- Arbeitet ein Worker bei geschlossenem App-Fenster zu Ende?

---

**Erstellt mit:** `/dtb:feature-plan`
