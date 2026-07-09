---
name: dtb:feature-plan
description: >-
  Use when: "Feature planen", "feature plan", "Feature-Spec erstellen",
  "neues Feature dokumentieren". Creates a structured feature specification
  from the current chat discussion and saves it as features/<slug>/spec.md.
disable-model-invocation: true
argument-hint: "[Feature-Name]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: [dtb:feature-discover]
  next: [dtb:impl-plan]
  consumes: [INBOX.md, features/*/discovery.md, workflow.config.yaml]
  produces: [features/*/spec.md, INBOX.md, BACKLOG.md]
---

# Feature-Plan erstellen

Du bist ein Feature-Plan-Manager. Deine Aufgabe ist es, den aktuell diskutierten Feature-Plan als strukturierte Spec-Datei zu speichern.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Aufgabe

1. **Analysiere den Chat-Verlauf** und identifiziere den diskutierten Feature-Plan
2. **Strukturiere den Plan** nach dem unten stehenden Template
3. **Speichere** in `{config.paths.workflows}/features/{slug}/spec.md`
4. **Frage den Benutzer** ob das Feature in BACKLOG.md eingetragen werden soll

## Template fuer spec.md

Verwende folgende Struktur:

```markdown
# Feature: [Feature-Name]

**Erstellt:** [Datum]
**Ziel:** [Hauptziel in einem Satz]
**Prioritaet:** Hoch / Mittel / Niedrig
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

[2-3 Saetze: Was wird gemacht und warum?]

---

## Scope / Abgrenzung

### Enthalten
- [Was gehoert zu diesem Feature?]

### Nicht enthalten
- [Was gehoert explizit NICHT dazu?]

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| [Risiko 1] | Hoch/Mittel/Niedrig | Hoch/Mittel/Niedrig | [Loesung] |

---

## Dependencies

### Erforderlich vor Start
- [ ] [Dependency 1]
- [ ] [Dependency 2]

### Referenz-Dokumente
- `[Datei 1]` - [Beschreibung]
- `[Datei 2]` - [Beschreibung]

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

## Offene Punkte

- [Beim Schreiben ungeklaerte Fragen — als konkrete Frage formulieren, NICHT plausibel erraten. "— keine —", wenn nichts offen ist]

---

**Erstellt mit:** `/dtb:feature-plan`
```

---

## Wichtig - Anweisungen fuer die Ausfuehrung

### Beim Ausfuehren des Commands:

1. **Discovery pruefen (optional):**
   - Suche `{config.paths.workflows}/features/{slug}/discovery.md` (Slug aus dem Feature-Namen, §4)
   - Falls vorhanden: Lies die Discovery-Datei und uebernimm Scope, betroffene Module, Anforderungen und Abhaengigkeiten als Ausgangsbasis fuer die Feature-Spec
   - Falls nicht vorhanden: Ueberspringe diesen Schritt ohne Hinweis

2. **Inbox pruefen:**
   - Lies `{config.paths.workflows}/INBOX.md`
   - Filtere alle Eintraege mit Status `Offen`
   - Falls offene Ideen vorhanden, zeige:
     ```
     Offene Ideen in der Inbox:
       1. #{N} — {Idee-Text} ({Datum})
       2. #{N} — {Idee-Text} ({Datum})
       ...

     Idee auswaehlen (Nummer) oder neues Feature beschreiben:
     ```
   - Falls Inbox nicht existiert oder keine offenen Ideen: Ueberspringe diesen Schritt ohne Hinweis
   - **Bei Auswahl einer Idee:**
     - Verwende den Idee-Text als Ausgangsbasis fuer die Feature-Diskussion
     - Setze den Inbox-Status auf `In Arbeit`

3. **Feature-Name / Slug ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Leite den **kebab-case-Slug** ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "Chat History" → `features/chat-history/`)
   - Bei Slug-Kollision mit einem bestehenden Ordner (anderer Name, gleicher Slug) → melden und anderen Namen erfragen (§4, kein Auto-Suffix)

4. **Prüfe ob `features/{slug}/spec.md` existiert:**
   - Falls JA: Frage "Soll ich die existierende Spec ueberschreiben oder aktualisieren?"
   - Falls NEIN: Lege den Ordner `features/{slug}/` bei Bedarf an und erstelle `spec.md`

5. **Analysiere den Chat-Verlauf:**
   - Identifiziere Ziel, Scope und Abgrenzung
   - Finde Risiken und Dependencies
   - Sammle Success Criteria

6. **Fuelle das Template:**
   - Nutze konkrete Informationen aus dem Chat
   - **Nie erfinden:** Fehlt eine Information, fuelle sie NICHT mit einer plausiblen Annahme.
     Trage sie stattdessen als konkrete Frage unter `## Offene Punkte` ein. Eine ehrliche
     Luecke ist besser als ein verstecktes Rateergebnis. Kein `[TODO]`-Platzhalter mehr.
   - Fokus auf Was/Warum, nicht auf Wie (Implementierungsdetails gehoeren in `plan.md`)
   - **Max. 500 Zeilen** — laengere Specs verschlechtern die AI-Verarbeitung. Bei komplexen Features: Details in `plan.md` auslagern

7. **Technical-Leak-Lint (Pflicht vor dem Speichern):**
   - Wende den Lint aus Abschnitt „## Technical-Leak-Lint" (unten) auf den fertigen Spec-Text an
   - **Treffer → Hard-Block:** Datei NICHT speichern; melde die Funde im Meldeformat und korrigiere, dann erneut pruefen
   - Override nur mit Begruendung + Markierung an der Stelle (siehe Abschnitt)

8. **Speichere die Datei**

9. **Inbox-Status aktualisieren:**
   - Falls das Feature aus einer Inbox-Idee erstellt wurde:
     - Setze den Status in `INBOX.md` auf `Ausgearbeitet`
     - Ergaenze die Idee-Zeile um den Link: `→ features/{slug}/spec.md`

10. **Backlog-Eintrag anbieten:**

   Frage den Benutzer:
   ```
   Feature gespeichert: {config.paths.workflows}/features/{slug}/spec.md

   Soll das Feature in BACKLOG.md eingetragen werden? (Ja/Nein)
   ```

   **Bei Ja:**
   - Lies `{config.paths.workflows}/BACKLOG.md`
   - Die Status-Spalte ist eine **abgeleitete Anzeige** (Regeln: `project-rules/DERIVED_STATE_RULES.md`):
     trage den initialen abgeleiteten Status ein — frisch erstellte Spec ohne Plan = `Spezifiziert`.
     Danach pflegt `dtb:workflow-checkpoint` das Feld; manuell gepflegt werden nur Prio und Ziel
   - Bestimme Ziel-Abschnitt anhand des Status:
     - Status "Idee" → "Ideen / Backlog"
     - Alle anderen (Geplant, In Arbeit, etc.) → "Aktive Features"
   - Fuege eine neue Zeile in die entsprechende Tabelle ein:
     `| {Feature-Name} | Spezifiziert | {Prio} | features/{slug}/spec.md | {Ziel aus Executive Summary} |`
   - Aktualisiere das Datum in "Letzte Aktualisierung"

   **Bei Nein:**
   ```
   OK, Feature nicht ins Backlog eingetragen.
   Du kannst es spaeter mit /dtb:backlog-status sehen (features/*/spec.md werden automatisch erkannt).
   ```

11. **Bestaetige:**
   ```
   Naechste Schritte:
   1. Implementierungsplan erstellen: /dtb:impl-plan [Feature-Name]
   2. Plan reviewen: /dtb:plan-review [Feature-Name]
   3. Feature starten: /dtb:feature-start
   ```

---

## Technical-Leak-Lint

Prueft den fertigen Spec-Text unmittelbar vor dem Speichern (Ausfuehrungs-Schritt 7). Ziel: die
Spec beschreibt das **Was/Warum**, nicht das **Wie**. Ein Treffer bricht den Write ab (Hard-Block).

**7 Leck-Kategorien** (je 1 Beispiel → loesungsneutrale Alternative):

| # | Kategorie | Leck (verboten) | Stattdessen |
|---|-----------|-----------------|-------------|
| 1 | Vendor-/Produktname | „in PostgreSQL/Redis/S3 speichern" | „persistent speichern" |
| 2 | ORM-/Query-Notation | „`User.objects.filter()`", „`SELECT …`" | „Nutzer nach Kriterium finden" |
| 3 | Transport/Protokoll | „per REST `POST /users`", „WebSocket" | „Nutzer legt Datensatz an" |
| 4 | Implementierungs-Verb | „instanziiere", „iteriere", „caste" | „das System verarbeitet …" |
| 5 | Konkrete Datenstruktur | „`Dict[str, List]`", „Array von Objekten" | „Zuordnung von X zu Y" |
| 6 | Framework-/Library-Name | „mit React/FastAPI/Pydantic" | „Oberflaeche/Schnittstelle …" |
| 7 | Datei-/Pfad-/Klassenname | „`services/auth.py`", Klasse `AuthManager` | „im Authentifizierungs-Teil" |

**Meldeformat bei Treffern** (Hard-Block, Datei NICHT speichern):
```
❌ Technical-Leak-Lint: {N} Leck(s) gefunden, Write abgebrochen
  {## Sektion} [{Kategorie}]: „{Fund}" → {loesungsneutraler Hinweis}
```
Zaehlung: ein Fund = eine leckende Phrase (nicht pro Wort). Trifft eine Phrase mehrere
Kategorien, melde nur die zutreffendste (keine Doppelzaehlung). Anker ist die Spec-Sektion
(`## …`) + Zitat, KEINE Zeilennummer (der Text ist beim Pruefen noch nicht gespeichert).
Danach korrigieren und erneut pruefen.

**Meta-Spec-Ausnahme (eng gefasst):** Beschreibt die Spec selbst ein Code-/Config-/Skill-Artefakt
als Gegenstand (Heuristik: Spec-Gegenstand bzw. betroffene Module sind Skill-/Code-Dateien — eine
`## Betroffene Module`-Sektion ist Indiz, nicht Pflicht), sind Referenzen *auf dieses Artefakt*
legitim — inkl. aus `discovery.md` geerbter technischer Angaben. **Ebenfalls nie ein Leck:**
Namen des Skill-/Workflow-Systems selbst (Skill-Namen wie `feature-discover`, Konventionen wie
`## Offene Punkte`), unabhaengig vom Gegenstand. Technische Details ueber *andere*,
nicht-gegenstaendliche Fach-Loesungen bleiben Lecks.

**Override:** Ein bewusst gehaltener Fachbegriff (echte fachliche Anforderung, z.B. „Export nach
SAP") ist zulaessig — **nur mit kurzer Begruendung** und **Markierung an der Stelle** in der
erzeugten Spec: `<!-- Lint-Override: {Begruendung} -->`. Kein Override ohne Begruendung. Beim
erneuten Pruefen zaehlt eine mit gueltigem Marker versehene Stelle nicht mehr als Leck.
