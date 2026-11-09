# Feature Backlog

**Letzte Aktualisierung:** 2026-11-09 (#175 worker-job-ende-meldung archiviert)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| # | Feature | Status | Prio | Datei | Ziel |
|---|---------|--------|------|-------|------|
| 173 | checkpoint-ohne-rueckfragen | Fertig zum Testen | Mittel | features/checkpoint-ohne-rueckfragen/spec.md | Checkpoint laeuft im Normalfall ohne Rueckfrage |
| 177 | checkpoint-schneller | Fertig zum Testen | Hoch | features/checkpoint-schneller/spec.md | Checkpoint-Median ≤ 4 aktive min ohne Verlust an Funden |

---

## Aufgaben

| # | Aufgabe | Status | Prio | Datei | Beschreibung |
|---|---------|--------|------|-------|--------------|

---

## Ideen / Backlog

| # | Feature | Status | Prio | Datei | Beschreibung |
|---|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| # | Feature | Abgeschlossen | Datei |
|---|---------|---------------|-------|

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
