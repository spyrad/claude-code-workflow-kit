# Derived State — Ableitungsregeln

> **Single Source fuer die Statusableitung.** Alle Lese-Skills (`dtb:workflow-next`,
> `dtb:workflow-status`, `dtb:workflow-resume`, `dtb:backlog-status`) leiten den
> Feature-Status nach DIESEN Regeln aus Artefakten ab. Keine eigene Logik in Skills —
> Aenderungen nur hier.

**Grundprinzip:** Status wird nicht gespeichert, sondern abgeleitet. Quelle der Wahrheit
sind die Artefakte im `features/`-Ordner und deren `## Progress`-Checkboxen — nicht
Statusfelder in BACKLOG.md oder WORKFLOW_STATUS.md.

---

## 1. Ableitungsregel

### 1.1 Artefakt-Existenz → Pipeline-Stage

Pro Feature (Pairing ueber `{NAME}` in Dateinamen) gilt die **hoechste** zutreffende Zeile:

| Vorhandene Artefakte | Abgeleiteter Status |
|----------------------|---------------------|
| keine | Idee (nur INBOX-Eintrag) |
| `DISCOVERY_{NAME}.md` | In Discovery |
| `FEATURE_{NAME}.md` (ohne PLAN) | Spezifiziert |
| `PLAN_{NAME}.md`, 0 Checkboxen abgehakt | Geplant |
| `PLAN_{NAME}.md`, teilweise abgehakt | In Arbeit |
| `PLAN_{NAME}.md`, alle Checkboxen abgehakt | Fertig zum Testen |
| Datei in `archive/` | Abgeschlossen |

### 1.2 Explizite Zustaende (nicht ableitbar)

Diese Zustaende sind bewusste Nutzer-Entscheidungen und ueberschreiben die Ableitung:

- **Pausiert** — manuelle Markierung (WORKFLOW_STATUS "Pausierte Themen" oder BACKLOG-Anmerkung)
- **Abgenommen / Abgeschlossen** — nur via `/dtb:archive`; 100% Checkboxen ≠ automatisch abgeschlossen

### 1.3 Konfliktregel

Widerspricht ein manuelles Statusfeld (z.B. in BACKLOG.md) dem abgeleiteten Zustand:

1. **Das Artefakt gewinnt.** Reports zeigen den abgeleiteten Status.
2. **Der Widerspruch wird gemeldet** (1 Hinweiszeile im Report), nie stillschweigend uebergangen.
3. Lese-Skills korrigieren das Feld NICHT selbst (read-only) — Korrektur erfolgt beim
   naechsten schreibenden Skill (`workflow-checkpoint`) oder manuell.

### 1.4 Fallbacks (Altbestand, defekte Daten)

Kein Fallback fuehrt zum Abbruch — immer definiertes Verhalten:

| Situation | Verhalten |
|-----------|-----------|
| PLAN ohne `## Progress`-Sektion | Status "Plan vorhanden, Fortschritt unbekannt"; Nachruestung anbieten |
| `## Progress` mit 0 Checkbox-Zeilen | wie "keine Sektion" |
| `IMPL_STATUS_*.md` vorhanden (Altbestand) | ignorieren fuer Ableitung; Hinweis auf Migration (Progress-Sektion) |
| PLAN ohne zugehoerige FEATURE-Spec | Meldung "verwaister Plan" (Pairing pruefen) |
| FEATURE/PLAN-Namen passen nicht zusammen | `dtb:project-health` meldet verwaiste Paare |
| gar keine Artefakte im features/-Ordner | "Kein aktives Feature" (wie bisher) |

### 1.5 Sonderregel TASK_* / BUG_*

Aufgaben und Bugs haben keinen PLAN — ihre Checkliste steht **direkt in der Datei**
(`## Schritte` bzw. `## Fix-Schritte`). Ableitung analog: 0 abgehakt = Offen/Analysiert,
teilweise = In Arbeit, alle = Fertig zum Testen. Explizite Statusfelder im Frontmatter/Kopf
dieser Dateien gelten als manuelle Zustaende nach 1.2 nur fuer: Pausiert.

---

## 2. Progress-Sektion — Format

Jedes `PLAN_*.md` enthaelt eine `## Progress`-Sektion (erzeugt von `dtb:impl-plan`):

```markdown
## Progress

- [ ] 1.1 Kurzname des Schritts
- [x] 1.2 Kurzname des Schritts — `a1b2c3d`
- [x] 1.3 Doku-Schritt ohne Commit
```

**Regeln:**

1. **Eine Zeile pro Plan-Schritt**, Nummerierung identisch zu den Schritten im Plan (N.M)
2. **Checkbox-Syntax:** `- [ ]` offen, `- [x]` erledigt — keine anderen Marker
3. **Commit-SHA als Beleg:** nach ` — ` als Inline-Code (`` `a1b2c3d` ``, Kurzform 7 Zeichen).
   Optional — Schritte ohne Commit (reine Doku/Verifikation) haben keine SHA
4. **Gebuendelte Commits:** ein Commit darf mehrere Checkboxen belegen (gleiche SHA an
   mehreren Zeilen zulaessig)
5. **Kompakt:** max ~30 Zeilen, keine Prosa — Details gehoeren in die Plan-Schritte
6. **Manuelles Abhaken erlaubt:** auch der Mensch darf Checkboxen setzen (Artefakt = Wahrheit)
7. **Abhaken ist Teil des Implementierungs-Loops:** nach jedem umgesetzten Schritt sofort,
   nicht gesammelt am Session-Ende

---

## 3. Statusmodell — Mapping auf die BACKLOG-Legende

Abgeleitete Zustaende und ihre Anzeige in Reports/BACKLOG:

| Abgeleiteter Status | BACKLOG-Legende | Anzeige-Hinweis |
|---------------------|-----------------|-----------------|
| Idee | Idee | nur INBOX/BACKLOG-Zeile, keine Artefakte |
| In Discovery | Idee | Zusatz "(in Discovery)" |
| Spezifiziert | Idee | Zusatz "(Spec erstellt)" — noch kein Plan |
| Geplant | Geplant | Plan existiert, 0% umgesetzt |
| In Arbeit | In Arbeit | Zusatz "X/Y Schritte" aus Checkbox-Zaehlung |
| Fertig zum Testen | Fertig zum Testen | 100% Checkboxen; wartet auf Abnahme |
| Abgenommen | Abgenommen | explizit (1.2) |
| Abgeschlossen | Abgeschlossen | explizit via `/dtb:archive` |
| Pausiert | Pausiert | explizit (1.2), ueberschreibt Ableitung |

**Statusfeld in BACKLOG.md** ist abgeleitete **Anzeige**: schreibende Skills befuellen es
beim naechsten Lauf nach diesen Regeln; manuell gepflegt werden nur Prio und Ziel.

---

**Eingefuehrt mit:** Feature DERIVED_STATE (`features/FEATURE_DERIVED_STATE.md`), 2026-07-06
