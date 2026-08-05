# Feature Backlog

**Letzte Aktualisierung:** 2026-08-05 (`/dtb:task`: Aufgabe `gitattributes-eol` aus INBOX #28 erfasst und in die Aufgaben-Tabelle eingetragen. Davor 2026-08-04: `/dtb:archive` — 6 abgenommene Features nach `archive/` verschoben, Details `archive/ARCHIVE_LOG.md`. Aktiv bleiben `feature-fast` + `meeting-agenda`, beide Fertig zum Testen, Restabnahmen offen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|
| .gitattributes fuer deterministische Zeilenenden | Offen | Mittel | features/gitattributes-eol/task.md | `.gitattributes` ergaenzen + Bestand einmalig renormalisieren, damit LF-Dateien unter `core.autocrlf=true` nicht mehr faelschlich als „modified" erscheinen (10 Belege seit 2026-07-18) |

---

## Ideen / Backlog

| Feature | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|

---

## Abgeschlossen

| Feature | Abgeschlossen | Datei |
|---------|---------------|-------|
| abnahme-zustand | 2026-08-04 | `archive/abnahme-zustand/` |
| plan-status-feld | 2026-08-04 | `archive/plan-status-feld/` |
| commit-and-push | 2026-08-04 | `archive/commit-and-push/` (Vorbehalt Multi-Root offen) |
| meeting-dump | 2026-08-04 | `archive/meeting-dump/` (Beleg Projekt/Datum offen) |
| open-question | 2026-08-04 | `archive/open-question/` |
| Fachfragen-Erfassung | 2026-08-04 | `archive/fachfragen-erfassung/` |

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
