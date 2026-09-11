# Feature Backlog

**Letzte Aktualisierung:** 2026-09-11 (`/dtb:workflow-checkpoint` Session 2: `idea-review-sofortschreiben` erledigt 6/6; drei Features archiviert)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| feature-start-statusfeld | Fertig zum Testen | Hoch | features/feature-start-statusfeld/spec.md | `dtb:feature-start` schreibt keine Anzeigefelder mehr — der Start behauptet keinen Status, den die Ableitung nicht traegt, damit die Feld-Konfliktmeldung wieder ein Befund ist statt Dauerrauschen (INBOX #50, via Fast-Track) |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|
| idea-review Sofort-Schreiben | Erledigt | Mittel | features/idea-review-sofortschreiben/task.md | Sofort-Schreiben-Absatz aus `dtb:idea-triage` Schritt 4 nach `dtb:idea-review` uebertragen (INBOX #71) |

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|

---

## Status-Legende (abgeleitet aus Artefakten)

| Status | Abgeleitet aus |
|--------|----------------|
| Idee | Nur INBOX-/BACKLOG-Eintrag, keine Artefakte |
| In Discovery | discovery.md existiert, kein spec.md |
| Spezifiziert | spec.md existiert, kein plan.md |
| Geplant | plan.md existiert, 0 Progress-Checkboxen |
| In Arbeit | `## Progress` teilweise abgehakt (X/Y) |
| Fertig zum Testen | Alle Schritte abgehakt |
| Abgenommen | Explizit gesetzt (getestet und freigegeben) |
| Abgeschlossen | Explizit via `/dtb:archive` |
| Pausiert | Explizit gesetzt, ueberschreibt Ableitung |

## Prio-Legende

| Prio | Bedeutung |
|------|-----------|
| Kritisch | Blocker, sofort umsetzen |
| Hoch | Naechster Sprint |
| Mittel | Backlog, bei Kapazitaet |
| Niedrig | Nice-to-have |
