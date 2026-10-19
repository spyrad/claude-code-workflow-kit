# Discovery: Triage-Vorsortierung
<!-- resume: done -->

**Erstellt:** 2026-10-16
**Idee-Referenz:** Inbox #137 — "dtb:idea-triage um einen Vor-Schritt erweitern: Funde per Hintergrund-Agenten voranalysieren und gegen den Kit-Stand prüfen, verwandte Funde zu Bündeln zusammenfassen, erledigte/überholte/doppelte mit Beleg zum Verwerfen vorschlagen, Lektionen per dtb:lesson und Fachfragen per dtb:open-question anlegen statt sie als Feature zu befördern."
**Beleg:** [becken-vorsortierung.md](becken-vorsortierung.md) — Probelauf 2026-10-16 (73 Funde → 51 befördern / 16 verwerfen / 6 unklar, 10 Bündel)
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-idea-triage/SKILL.md | Hauptträger: neuer Vor-Schritt vor Schritt 2–5, Bündel, Verwerfen mit Beleg, neue Ausgänge; Sofort-Schreiben (Schritt 4, INBOX #71) und Portionierung (Schritt 2) |
| skills/dtb-lesson/SKILL.md | Ausgang Lektionen; seit `3fc03ee` modell-aufrufbar, „Zwei Eingangskanaele" (Schritt 1), Duplikat-Check (Schritt 3) |
| skills/dtb-open-question/SKILL.md | Ausgang Fachfragen; bricht bei 0 aktiven Features ohne Slug ab (Schritt 2b) |
| skills/dtb-idea/SKILL.md | `## Duplikat-Check` — von der Triage per Referenz genutzt |
| skills/dtb-workflow-checkpoint/SKILL.md | Struktur-Check auf `## Schreibmechanik INBOX-BEFUNDE.md`, Becken-Erinnerung |
| skills/dtb-worker/SKILL.md | Vorbild Hintergrund-Agenten (Subagenten-Träger, lesend) — nur Referenz |
| skills/CLAUDE.md | Zwei-Becken-Regel, Rückfragen-Defaults (Sammelliste), Duplikat-Schutz |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §6.4 Becken-Einträge status-neutral |
| skills/dtb-project-health/SKILL.md | Becken-Integrität und Nummernkreis — betroffen, falls Bündel Nummern zusammenlegen |
| workflow.config.yaml | Block `idea_triage` — ggf. neue Schlüssel |
| CLAUDE.md | Skill-Beschreibung `idea-triage` |

Format-Ziele: `archive/INBOX-BEFUNDE-verworfen.md` (Beleg-Spalte?), `INBOX.md` (Bündel-Einträge).

---

## Anforderungen

### Scope
**Enthalten:**
- Zwei Stufen im selben Skill `dtb:idea-triage`:
  1. **Vorverarbeitung:** Funde vorsortieren und voranalysieren (gegen den Kit-Stand prüfen), verwandte Funde wo sinnvoll zu Bündeln zusammenfassen, erledigte/überholte verwerfen, Lektionen per `dtb:lesson` und Fachfragen per `dtb:open-question` anlegen, wenn es keine echten Features sind
  2. **Normale Triage:** die verbleibenden, vorverarbeiteten und gebündelten Feature-Kandidaten in die Haupt-INBOX befördern, zurückstellen (liegenlassen) oder verwerfen

**Nicht enthalten:**
- Agenten entscheiden oder schreiben nichts — Voranalyse ist lesend, liefert Vorschläge mit Beleg; jedes Schreiben folgt einer Bestätigung durch den Menschen
- Kein Umsetzen von Funden — auch ein offensichtlicher Einzeiler-Fix wird befördert oder verworfen, nicht nebenbei erledigt
- `dtb:idea-review` bleibt getrennt — keine Neu-Priorisierung oder Umsortierung der Haupt-INBOX, nur neue Einträge
- Schreibseite unverändert — wie `dtb:workflow-checkpoint` ins Becken schreibt, ändert sich nicht
- Kein neuer Skill — Vor-Schritt in `dtb:idea-triage`

### Gewuenschtes Verhalten
- **Sammelliste mit Veto, schwere Fälle einzeln** — Muster wie `dtb:impl-review` Schritt 9 (Entscheidung (1): Sammelliste statt automatischem Verwerfen)
- **Einzeln vorgelegt** (Kriterium: Unsicherheit des Vorschlags):
  - Vorschlag **Unklar** — die Agenten können nicht einordnen, eine Frage an den Menschen ist Teil des Vorschlags (Probelauf: 6, z.B. #69, #103)
  - **Verwerfen mit Sicherheit < `hoch`** — ein falsch verworfener Fund ist nur über das Archiv wiederzufinden, der teurere Fehler
- **Sammelliste**, vorbelegt mit Vorschlag + Beleg: alles andere — Befördern, Verwerfen mit Sicherheit `hoch`, Lektion, Fachfrage
- **Bündel** als eigener Block oben in der Sammelliste, je Bündel eine Zeile mit den Nummern
- Steuerung in Veto-Form: `alle uebernehmen` / `Nummern streichen` / `einzeln durchgehen`

### Randfaelle
- **Abbruch / Sofort-Schreiben (Entscheidung (5), INBOX #71):** geschrieben wird erst nach Bestätigung der Sammelliste, dann Eintrag für Eintrag, jeder sofort — Abbruch mittendrin lässt das Geschriebene stehen. Die Agenten-Vorschläge selbst werden nicht persistiert; geht der Lauf vor der Bestätigung verloren, wird neu gestartet (kostet Rechenzeit, keine Entscheidung)
- **Umfang der Voranalyse (Entscheidung (4)):** die Voranalyse liest das ganze Becken (alles Ungesichtete) — Bündel und Dubletten erkennt man nur im Gesamtbild (Probelauf: 73 Funde in einem Durchgang). Die Portions-Kappung (`altbestand_pro_lauf`) entfällt für die Sammelliste und bleibt für die Einzelfälle
- **Leeres Becken** → wie heute eine Zeile „Nichts zu sichten", keine Agenten
- **Wenige Funde (< 5)** → keine Hintergrund-Agenten, Voranalyse inline in der Session
- **Bündel (Entscheidung (2)):**
  - Ein Fund trägt das Bündel (Agenten schlagen den konkretesten vor); seine Nummer bleibt, der Text nennt die übrigen: „(enthält #86, #118, …)"
  - Die übrigen Nummern → `archive/INBOX-BEFUNDE-verworfen.md` mit Begründung „gebündelt in #N"
  - Keine neue Nummer für ein Bündel — Nummern werden nie neu vergeben (Vorbild: #105 → #100)
- **Nachtrag an bestehende INBOX-Idee (Variante A, bewusste Ausnahme vom Scope „nur neue Einträge"):** gehört ein Fund zu einer Idee, die schon in `INBOX.md` steht (Probelauf: #103/#106 → #99, #46/#58 → #100), wird er dort als Satz angehängt und archiviert mit „nachgetragen in #N"
- **Fachfrage ohne aktives Feature (Entscheidung (3), Variante A):** die Agenten schlagen ein passendes Feature vor, auch ein nicht aktives (Slug-Override von `dtb:open-question`); passt keins → als Idee nach `INBOX.md` befördert mit Vorsatz „Fachfrage:". Selten — Probelauf: 0 von 73
- **Agent fällt aus / liefert nichts** → seine Funde gehen ohne Vorschlag als Einzelfälle in die normale Triage (Werkzeug-Fehlschlag ist kein Datenbefund — nie als „nichts gefunden" werten)
- **Becken ändert sich zwischen Analyse und Schreiben** → bestehende Lesestand-Prüfung greift; neue Funde erst im nächsten Lauf
- **Lektion steht schon in `lessons.md`** → Duplikat-Check von `dtb:lesson` meldet; Fund wird verworfen mit „Lektion L{N} deckt ab"
- **Falscher Beleg** → Nummer in der Sammelliste streichen; der Fund geht einzeln in die normale Triage

### Einschraenkungen
**Technisch:**
- **Einzeldatei:** `dtb:kit-sync` verteilt je Skill nur `SKILL.md` (Klasse-A-Muster `skills/dtb-*/SKILL.md`) — der Agenten-Auftrag muss inline im Skill stehen, keine Nebendatei (Laufzeit-Autarkie)
- **Agenten nur lesend:** nur Lese-Werkzeuge im Agenten-Auftrag; der Skill selbst braucht zusätzlich `Agent` in `allowed-tools`
- **`disable-model-invocation: true` bleibt** — das Modell startet die Triage nie selbst
- **Voll-Guard unverändert** — läuft nur in der Orchestrator-Session (Schreibgrenzen-Regel)
- **Kopplung zum Checkpoint bleibt:** `## Schreibmechanik INBOX-BEFUNDE.md` wird nicht umbenannt (Struktur-Check in `dtb:workflow-checkpoint`)

**Fachlich:**
- **Verwerfen braucht Begründung** — der Agenten-Beleg ist diese Begründung
- **Dublette = Ersetzungsprobe** (kitweiter Kanon, `skills/CLAUDE.md` → Duplikat-Schutz)
- **Becken-Einträge werden nie gearbeitet**, bevor sie befördert sind (Zwei-Becken-Regel, DSR §6.4) — die Agenten lesen nur

### Integrationspunkte
- **Ausgänge Lektion/Fachfrage per Referenz (Variante A):** die Triage führt die Schritte von `dtb:lesson` und `dtb:open-question` selbst aus — Muster `dtb:workflow-checkpoint` Schritt 0 (Struktur-Check auf die Anker-Sektionen der Quell-Skills vor dem ersten Schreiben, nie Kopie). Die Bestätigung der Sammelliste genügt, keine zweite Rückfrage je Eintrag. Verworfen: echter Skill-Aufruf (B) — jeder Aufruf fragt erneut
- **`skills/CLAUDE.md` → Zwei-Becken-Regel:** neue Schreibwege der Triage aufnehmen (Lektionen nach `lessons.md`, Fachfragen nach `features/*/`, Nachträge an bestehende `INBOX.md`-Einträge)
- **`CLAUDE.md` (Root):** Beschreibung von `idea-triage` unter „Idea management" anpassen
- **Externe Abhängigkeiten:** keine, außer dem `Agent`-Werkzeug

---

## Abhaengigkeiten

- Keine Konflikte — kein weiteres aktives Feature (48 archiviert)
- Überschneidung INBOX #99 (Jev: typisierte Urteile mit Konfidenzwert): die Agenten-Vorschläge tragen eine Sicherheit; der Probelauf war als Messsatz für #99 gedacht
- Überschneidung `archive/ideen-becken` (Ursprung von `dtb:idea-triage`): dessen Regeln (Portionierung, Sofort-Schreiben, Liegenlassen) werden hier bewusst angepasst

---

## Offene Punkte

- Die fünf offenen Entscheidungen aus dem Orchestrator-Gespräch sind geklärt: (1) → Gewünschtes Verhalten, (2)–(5) → Randfälle
- Aufteilung der Hintergrund-Agenten festlegen (Probelauf: 3 Agenten nach Nummernbereich) — wie entstehen Bündel über Agenten-Grenzen hinweg?
- Ergebnis-Format der Agenten festlegen (Probelauf-Tabelle: #, Vorschlag, Grund, Beleg, Sicherheit) und wie es in Sammelliste/Einzelfälle zerfällt
- Ob `archive/INBOX-BEFUNDE-verworfen.md` eine eigene Beleg-Spalte bekommt oder der Beleg in die Begründung wandert

---

**Erstellt mit:** `/dtb:feature-discover`
