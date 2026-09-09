# Feature Backlog

**Letzte Aktualisierung:** 2026-09-09 (`/dtb:task`: Aufgabe `idea-review-sofortschreiben` aus INBOX #71; zuvor `/dtb:workflow-checkpoint` Session 1 und `/dtb:idea-review`)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| ideen-becken | Fertig zum Testen | Hoch | features/ideen-becken/spec.md | Maschinelle Verlustfunde in ein eigenes Becken trennen; nur Befoerdertes wird gearbeitet |
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |
| output-style-gezielt | Fertig zum Testen | Mittel | features/output-style-gezielt/spec.md | Eine global geltende, schaltbare Stil-Vorgabe als versioniertes Kit-Artefakt ausliefern, die Claudes Fliesstext auf Orientierung statt Vollstaendigkeit ausrichtet — worum es geht, was der Stand ist, was zu entscheiden ist; Gegner sind Vorwegnahme und Redundanz, nicht Erklaerung |
| feature-start-statusfeld | Fertig zum Testen | Hoch | features/feature-start-statusfeld/spec.md | `dtb:feature-start` schreibt keine Anzeigefelder mehr — der Start behauptet keinen Status, den die Ableitung nicht traegt, damit die Feld-Konfliktmeldung wieder ein Befund ist statt Dauerrauschen (INBOX #50, via Fast-Track) |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|
| idea-review Sofort-Schreiben | Offen | Mittel | features/idea-review-sofortschreiben/task.md | Sofort-Schreiben-Absatz aus `dtb:idea-triage` Schritt 4 nach `dtb:idea-review` uebertragen (INBOX #71) |

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
