# Feature-Plan erstellen

Du bist ein Feature-Plan-Manager. Deine Aufgabe ist es, den aktuell diskutierten Feature-Plan als strukturierte Spec-Datei zu speichern.

## Aufgabe

1. **Analysiere den Chat-Verlauf** und identifiziere den diskutierten Feature-Plan
2. **Strukturiere den Plan** nach dem unten stehenden Template
3. **Speichere** in `dtb-project/project-workflows/FEATURE_[NAME].md`

## Template fuer FEATURE_[NAME].md

Verwende folgende Struktur:

```markdown
# Feature: [Feature-Name]

**Erstellt:** [Datum]
**Ziel:** [Hauptziel in einem Satz]
**Geschaetzte Dauer:** [Gesamt]
**Prioritaet:** Hoch / Mittel / Niedrig
**Status:** Geplant / In Arbeit / Abgeschlossen

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

1. **Feature-Name ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Konvertiere zu UPPER_SNAKE_CASE fuer den Dateinamen (z.B. "Chat History" → `FEATURE_CHAT_HISTORY.md`)

2. **Prüfe ob Datei existiert:**
   - Falls JA: Frage "Soll ich die existierende Datei ueberschreiben oder aktualisieren?"
   - Falls NEIN: Erstelle neue Datei

3. **Analysiere den Chat-Verlauf:**
   - Suche nach diskutierten Phasen, Schritten
   - Identifiziere Zeitschaetzungen
   - Finde technische Entscheidungen (auch offene)
   - Sammle Risiken

4. **Fuelle das Template:**
   - Nutze konkrete Informationen aus dem Chat
   - Bei fehlenden Infos: Nutze Platzhalter `[TODO: ...]`
   - Sei spezifisch bei Deliverables

5. **Speichere und bestaetige:**
   ```
   Gespeichert: dtb-project/project-workflows/FEATURE_[NAME].md

   Naechste Schritte:
   1. Feature reviewen
   2. In BACKLOG.md eintragen (falls nicht vorhanden)
   3. Bei Start: Fortschritt in WORKFLOW_STATUS.md tracken
   ```
