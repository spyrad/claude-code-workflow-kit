# Workflow fortsetzen (Resume)

Du stellst den Workflow-Kontext nach einem Session-Break wieder her.

## Aufgabe

1. **Lies die Status-Datei:** `dtb-project/project-workflows/WORKFLOW_STATUS.md`
2. **Lies den neuesten Session-Log:** `dtb-project/project-changelog/` (neueste Datei im neuesten Monats-Ordner)
3. **Pruefe Git-Status** beider Repos (assistant-backend, assistant-frontend)
4. **Praesentiere einen kompakten Resume-Report**
5. **Gib konkrete Handlungsempfehlung** fuer sofortiges Fortfahren

---

## Dateien lesen

```python
# Pflicht
read("dtb-project/project-workflows/WORKFLOW_STATUS.md")

# Neuesten Session-Log finden und lesen
# → Gibt Detail-Kontext zur letzten Session (was genau gemacht wurde, naechste Schritte)
find_newest("dtb-project/project-changelog/YYYY-MM/YYYY-MM-DD.md")
```

Falls WORKFLOW_STATUS.md nicht existiert:
```
WORKFLOW_STATUS.md nicht gefunden.
Empfehlung: Am Ende dieser Session /dtb:workflow-checkpoint ausfuehren.
```

## Git-Status pruefen

```bash
cd assistant-backend && git branch --show-current && git log --oneline -3 && git status --short && cd ..
cd assistant-frontend && git branch --show-current && git log --oneline -3 && git status --short && cd ..
```

---

## Resume-Report Format

Halte den Report **kompakt** (max 80 Zeilen Output). Fokus auf Actionable Info.

```markdown
# Workflow-Resume: DTB-Assistant

**Letzte Aktivitaet:** [Datum aus WORKFLOW_STATUS]
**Letzter Session-Log:** [Pfad]

---

## Status

| Kennzahl | Wert |
|----------|------|
| **Laufende Arbeit** | [aus WORKFLOW_STATUS] |
| **Naechster Schritt** | [aus WORKFLOW_STATUS] |
| **Blocker** | [aus WORKFLOW_STATUS] |
| **Uncommitted Changes** | [aus Git-Status] |

---

## Letzte Session (Zusammenfassung)

[2-4 Bullet Points aus dem neuesten Session-Log: Was wurde gemacht, welche naechsten Schritte wurden dort notiert]

---

## Offene Aufgaben

[Aus WORKFLOW_STATUS uebernehmen]

---

## Git-Status

**Backend:** Branch `[name]`, letzter Commit: `[hash]` — [message]
[Falls uncommitted: ⚠️ X uncommitted changes]

**Frontend:** Branch `[name]`, letzter Commit: `[hash]` — [message]
[Falls uncommitted: ⚠️ X uncommitted changes]

---

## Empfehlung

[Konkreter naechster Schritt — was genau tun, welche Dateien anfassen]

Bereit? Sage "Los" oder stelle Fragen.
```

---

## Wichtig

- **Actionable:** Benutzer muss sofort wissen was zu tun ist
- **Kompakt:** Keine 500-Zeilen-Reports, max 80 Zeilen
- **Zwei Quellen:** WORKFLOW_STATUS fuer Ueberblick + Session-Log fuer Detail-Kontext
- **Deutsch:** Alle Texte auf Deutsch
- Am Ende immer fragen ob Benutzer starten oder Fragen hat
