# Feature Backlog

**Letzte Aktualisierung:** 2026-08-07 (`/dtb:workflow-checkpoint` Session 1: `output-style-gezielt` (#40) an einem Vormittag von der Idee bis 9/11 — Discovery, Spec, Plan (reviewt REVISE → 4 WARNs behoben), Phasen 1+2 komplett inkl. Wegwerf-Test der neuen kit-sync-Klasse, Check 12 + Aktivierung; es fehlt die Kalibrier-Abnahme (3.3, braucht frische Session) + Abschluss-Verteilung (3.4). Davor 2026-08-06 (`/dtb:workflow-checkpoint` Session 3): `no-loss-check` (#29) **abgenommen** — an einem Tag von der Spec bis zur Abnahme, 11/11, fuenf Commits bis `3d15d0a`, drei Review-Laeufe mit 27 behobenen Findings, Kalibrierung 5/5, zwei produktive Laeufe ohne Falsch-Positive. Damit Archiv-Kandidat. Davor am selben Tag spezifiziert und von `no-loss-gate` umbenannt, weil „Gate" eine Blockade versprach, die der Skill bewusst nicht leistet. Davor 2026-08-05: `/dtb:task` erfasste `gitattributes-eol` aus INBOX #28; 2026-08-04: `/dtb:archive` — 6 abgenommene Features nach `archive/`, Details `archive/ARCHIVE_LOG.md`. Aktiv bleiben `feature-fast` + `meeting-agenda`, beide Fertig zum Testen, Restabnahmen offen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |
| output-style-gezielt | In Arbeit | Mittel | features/output-style-gezielt/spec.md | Eine global geltende, schaltbare Stil-Vorgabe als versioniertes Kit-Artefakt ausliefern, die Claudes Fliesstext auf Orientierung statt Vollstaendigkeit ausrichtet — worum es geht, was der Stand ist, was zu entscheiden ist; Gegner sind Vorwegnahme und Redundanz, nicht Erklaerung |
| no-loss-check | Abgenommen | Hoch | features/no-loss-check/spec.md | Vergleicht den Gespraechsverlauf gegen den Artefakt-Stand und meldet nicht persistierte Lektionen, Fach-Fragen und Entscheidungen mit fertig formulierten Erfassungs-Befehlen — empfehlende Vorstufe des Checkpoints, schreibt nichts selbst |

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
