# Feature Backlog

**Letzte Aktualisierung:** 2026-08-09 (`/dtb:workflow-checkpoint` Session 1: die autonome Lane erstmals komplett durchlaufen — Worker-Lauf `pipeline-kanten-reziprok` gruen nach 1 Versuch (7 Min), Diff abgenommen, `a79c218` gepusht, Kit auf `a79c218` gesynct; Aufgabe damit 4/4 = Erledigt. Zwei Befunde ueber die Lane: die Auftragsdatei muss vor dem Start committet sein (L18), und die #46-Fehlerklasse reproduziert sich weiter (#58). Davor 2026-08-08 `/dtb:task`: `pipeline-kanten-reziprok` aus INBOX #46 erfasst — Teil-Routing, nur die Bestandsbereinigung. Davor `/dtb:feature-plan`: `autonome-schiene` (#43, zusammengelegt mit ex-#49) spezifiziert — Discovery + Spec in einer Session; Erkennungs-Sicht + autonome Ausfuehrung zwischen Freigabe und Abnahme. Davor 2026-08-07 (`/dtb:workflow-checkpoint` Session 3: `feature-start-statusfeld` (#50) **an einem Nachmittag von der Triage bis 5/5** — Fast-Track, plan-review REVISE (4 WARNs behoben), zwei Phasen (`43e9c9a`, `4047ea3`), impl-review **REJECTED** wegen eines blocking Findings (der Skill setzte dieselbe Fehlerklasse neu ein, die er abschafft) → alle 9 Findings gefixt. Ausgelagert: #52, #53, #54; neu erfasst L15/L16. Kit-Verteilung der Triage-Fixes steht noch aus. Davor Session 2: `output-style-gezielt` (#40) **11/11 fertig zum Testen** — Kalibrier-Abnahme 5/5 in frischer Session (Fall-Set a-e, inkl. Gegenprobe `workflow-next` und Ausnahme-Klausel), Abschluss-Verteilung, danach `impl-review`: Plan Adherence 7/7 MATCH, 0 EXTRA, 9 Findings (0 blocking) allesamt gefixt, Kit gesynct auf `1758671` mit 45/45 synchron. Neu erfasst: L13/L14 und INBOX #51. Davor Session 1: von der Idee bis 9/11 — Discovery, Spec, Plan (reviewt REVISE → 4 WARNs behoben), Phasen 1+2 komplett inkl. Wegwerf-Test der neuen kit-sync-Klasse, Check 12 + Aktivierung; es fehlt die Kalibrier-Abnahme (3.3, braucht frische Session) + Abschluss-Verteilung (3.4). Davor 2026-08-06 (`/dtb:workflow-checkpoint` Session 3): `no-loss-check` (#29) **abgenommen** — an einem Tag von der Spec bis zur Abnahme, 11/11, fuenf Commits bis `3d15d0a`, drei Review-Laeufe mit 27 behobenen Findings, Kalibrierung 5/5, zwei produktive Laeufe ohne Falsch-Positive. Damit Archiv-Kandidat. Davor am selben Tag spezifiziert und von `no-loss-gate` umbenannt, weil „Gate" eine Blockade versprach, die der Skill bewusst nicht leistet. Davor 2026-08-05: `/dtb:task` erfasste `gitattributes-eol` aus INBOX #28; 2026-08-04: `/dtb:archive` — 6 abgenommene Features nach `archive/`, Details `archive/ARCHIVE_LOG.md`. Aktiv bleiben `feature-fast` + `meeting-agenda`, beide Fertig zum Testen, Restabnahmen offen)

> Die **Status-Spalte ist eine abgeleitete Anzeige** (Quelle: Artefakte + `## Progress`-Checkboxen,
> Regeln: `project-rules/DERIVED_STATE_RULES.md`). Sie wird von `dtb:workflow-checkpoint`
> synchronisiert — nicht manuell pflegen. Manuell gepflegt werden nur **Prio** und **Ziel**.

---

## Aktive Features

| Feature | Status | Prio | Datei | Ziel |
|---------|--------|------|-------|------|
| meeting-agenda | Fertig zum Testen | Mittel | features/meeting-agenda/spec.md | Rein lesende Agenda-Sicht: sammelt offene `[Fach]`-Fragen aus features/*/{discovery,spec}.md, gruppiert nach Feature — die fehlende Lese-Ansicht der Fachfragen-Kette (#13→#26→#25→#24); via Fast-Track geplant |
| feature-fast | Fertig zum Testen | Hoch | features/feature-fast/spec.md | Kleine Features durchlaufen die Erhebungsphase in einem Durchgang mit Default-Annahmen statt drei Interviews — ohne Abstriche an Artefakten, Derived State oder Reviews |
| output-style-gezielt | Fertig zum Testen | Mittel | features/output-style-gezielt/spec.md | Eine global geltende, schaltbare Stil-Vorgabe als versioniertes Kit-Artefakt ausliefern, die Claudes Fliesstext auf Orientierung statt Vollstaendigkeit ausrichtet — worum es geht, was der Stand ist, was zu entscheiden ist; Gegner sind Vorwegnahme und Redundanz, nicht Erklaerung |
| feature-start-statusfeld | Fertig zum Testen | Hoch | features/feature-start-statusfeld/spec.md | `dtb:feature-start` schreibt keine Anzeigefelder mehr — der Start behauptet keinen Status, den die Ableitung nicht traegt, damit die Feld-Konfliktmeldung wieder ein Befund ist statt Dauerrauschen (INBOX #50, via Fast-Track) |
| autonome-schiene | Fertig zum Testen | Hoch | features/autonome-schiene/spec.md | Leichtgewichtige Lane: erkennt worker-taugliche INBOX-Eintraege (Urteil + Abhaengigkeiten + Reihenfolge + Vorab-Fragen) und arbeitet freigegebene Eintraege im Hintergrund autonom bis zur Abnahmereife ab — Freigabe und Abnahme bleiben beim Menschen (INBOX #43, zusammengelegt mit ex-#49) |

---

## Aufgaben

| Aufgabe | Status | Prio | Datei | Beschreibung |
|---------|--------|------|-------|--------------|
| .gitattributes fuer deterministische Zeilenenden | In Arbeit | Mittel | features/gitattributes-eol/task.md | `.gitattributes` ergaenzen + Bestand einmalig renormalisieren, damit LF-Dateien unter `core.autocrlf=true` nicht mehr faelschlich als „modified" erscheinen (10 Belege seit 2026-07-18) |
| Pipeline-Kanten reziprok nachtragen | Erledigt | Mittel | features/pipeline-kanten-reziprok/task.md | Die zwei echten halbseitigen Kanten aus INBOX #46 gegenrichtig eintragen (`plan-review.after` += `feature-fast`, `feature-discover.after` += `greenfield-roadmap`); die vier read-only-Faelle und die Konventionsfrage bleiben bewusst draussen |

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
