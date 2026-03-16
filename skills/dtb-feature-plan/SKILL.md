---
name: dtb:feature-plan
description: >-
  Use when: "Feature planen", "feature plan", "Feature-Spec erstellen",
  "neues Feature dokumentieren". Creates a structured feature specification
  from the current chat discussion and saves it as FEATURE_[NAME].md.
disable-model-invocation: true
argument-hint: "[Feature-Name]"
---

# Feature-Plan erstellen

Du bist ein Feature-Plan-Manager. Deine Aufgabe ist es, den aktuell diskutierten Feature-Plan als strukturierte Spec-Datei zu speichern.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Aufgabe

1. **Analysiere den Chat-Verlauf** und identifiziere den diskutierten Feature-Plan
2. **Strukturiere den Plan** nach dem unten stehenden Template
3. **Speichere** in `{config.paths.workflows}/features/FEATURE_[NAME].md`
4. **Frage den Benutzer** ob das Feature in BACKLOG.md eingetragen werden soll

## Template fuer FEATURE_[NAME].md

Verwende folgende Struktur:

```markdown
# Feature: [Feature-Name]

**Erstellt:** [Datum]
**Ziel:** [Hauptziel in einem Satz]
**Geschaetzte Dauer:** [Gesamt]
**Prioritaet:** Hoch / Mittel / Niedrig
**Status:** Geplant / In Arbeit / Fertig zum Testen / Abgenommen / Abgeschlossen / Pausiert

---

## Executive Summary

[2-3 Saetze: Was wird gemacht und warum?]

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | [Name] | [Zeit] | Geplant |
| Phase 2 | [Name] | [Zeit] | Geplant |

---

## Phase 1: [Name]

### Ziel
[Was soll erreicht werden?]

### Schritte

#### Schritt 1: [Name]
- **Zweck:** [Warum wird dieser Schritt gemacht?]
- **Input:** [Was wird benoetigt?]
- **Output:** [Was wird erzeugt?]
- **Geschaetzte Dauer:** [Zeit]

#### Schritt 2: [Name]
[Gleiche Struktur]

### Deliverables
- [ ] [Output 1]
- [ ] [Output 2]

### Checkpoint-Kriterien
**Phase gilt als abgeschlossen wenn:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

## Phase 2: [Name]

[Gleiche Struktur wie Phase 1]

---

## Technische Entscheidungen (zu treffen)

| Thema | Optionen | Zu klaeren in | Relevanz |
|-------|----------|-------------|----------|
| [Thema 1] | [Option A, Option B] | [Phase X] | [Warum wichtig?] |

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

**Erstellt mit:** `/dtb:feature-plan`
```

---

## Wichtig - Anweisungen fuer die Ausfuehrung

### Beim Ausfuehren des Commands:

1. **Inbox pruefen:**
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

2. **Feature-Name ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Konvertiere zu UPPER_SNAKE_CASE fuer den Dateinamen (z.B. "Chat History" → `FEATURE_CHAT_HISTORY.md`)

3. **Prüfe ob Datei existiert:**
   - Falls JA: Frage "Soll ich die existierende Datei ueberschreiben oder aktualisieren?"
   - Falls NEIN: Erstelle neue Datei

4. **Analysiere den Chat-Verlauf:**
   - Suche nach diskutierten Phasen, Schritten
   - Identifiziere Zeitschaetzungen
   - Finde technische Entscheidungen (auch offene)
   - Sammle Risiken

5. **Fuelle das Template:**
   - Nutze konkrete Informationen aus dem Chat
   - Bei fehlenden Infos: Nutze Platzhalter `[TODO: ...]`
   - Sei spezifisch bei Deliverables

6. **Speichere die Datei**

7. **Inbox-Status aktualisieren:**
   - Falls das Feature aus einer Inbox-Idee erstellt wurde:
     - Setze den Status in `INBOX.md` auf `Ausgearbeitet`
     - Ergaenze die Idee-Zeile um den Link: `→ FEATURE_{NAME}.md`

8. **Backlog-Eintrag anbieten:**

   Frage den Benutzer:
   ```
   Feature gespeichert: {config.paths.workflows}/features/FEATURE_[NAME].md

   Soll das Feature in BACKLOG.md eingetragen werden? (Ja/Nein)
   ```

   **Bei Ja:**
   - Lies `{config.paths.workflows}/BACKLOG.md`
   - Bestimme Ziel-Abschnitt anhand des Status:
     - Status "Idee" → "Ideen / Backlog"
     - Alle anderen (Geplant, In Arbeit, etc.) → "Aktive Features"
   - Fuege eine neue Zeile in die entsprechende Tabelle ein:
     `| {Feature-Name} | Geplant | {Prio} | FEATURE_{NAME}.md | {Ziel aus Executive Summary} |`
   - Aktualisiere das Datum in "Letzte Aktualisierung"

   **Bei Nein:**
   ```
   OK, Feature nicht ins Backlog eingetragen.
   Du kannst es spaeter mit /dtb:backlog-status sehen (FEATURE_*.md werden automatisch erkannt).
   ```

9. **Bestaetige:**
   ```
   Naechste Schritte:
   1. Feature reviewen
   2. Bei Start: Fortschritt wird ueber /dtb:workflow-checkpoint getrackt
   ```
