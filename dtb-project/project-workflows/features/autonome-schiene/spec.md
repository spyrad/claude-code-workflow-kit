# Feature: Autonome Schiene

**Erstellt:** 2026-08-08
**Ziel:** Eine leichtgewichtige Lane, die worker-taugliche INBOX-Eintraege erkennt und nach menschlicher Freigabe autonom bis zur Abnahmereife abarbeitet — ohne die volle Kette Discovery → Spec → Plan.
**Prioritaet:** Hoch
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit kennt drei Lanes (Task, Fast-Track, Voll-Schiene) — alle drei fuehren durch den
Menschen. Dabei gibt es Eintraege, deren Erledigung keinen Menschen im Ablauf braucht:
Zielzustand mechanisch verifizierbar, Scope geschlossen, keine Fremdwirkung, umkehrbar
(Bestandsprobe 2026-08-06: `gitattributes-eol` ist so ein Fall, Schritt 1 ausgenommen).
Die autonome Schiene liefert beide fehlenden Seiten in einem Skill: eine **Erkennungs-Sicht**,
die die INBOX scannt und je Eintrag Tauglichkeit, Abhaengigkeiten, Reihenfolge und offene
Vorab-Fragen zeigt — und eine **Ausfuehrung**, die freigegebene Eintraege im Hintergrund
abarbeitet und mit gruenen Kriterien zur Abnahme meldet. Der Mensch behaelt die Klammer:
Freigabe vor dem Start, Abnahme nach dem Lauf.

---

## Scope / Abgrenzung

### Enthalten

- **Erkennungs-Sicht:** scannt die INBOX (Ideen UND Tasks) und zeigt je Eintrag:
  - Urteil „autonom ausfuehrbar: ja / teilweise / nein" mit 1-Satz-Begruendung
    (Kriterien: Zielzustand mechanisch verifizierbar; Scope geschlossen; keine
    Fremdwirkung/Spiegel-Kopplung; umkehrbar)
  - Abhaengigkeiten zwischen Eintraegen und eine empfohlene Bearbeitungs-Reihenfolge
  - **Nebenspalte „Vorab-Fragen":** fehlen einem Eintrag Kleinigkeiten zur vollen
    Autonomie (z.B. eine offene Scope-Entscheidung), stellt die Sicht pro Eintrag eine
    kurze Frage, die der Nutzer VOR der Ausfuehrung beantwortet
  - bei leerem Ergebnis: melden UND je Eintrag begruenden, was zur Tauglichkeit fehlt
- **Freigabe-Wahl:** einzelner Eintrag ODER die gesamte vorgeschlagene Liste in der
  vorgeschlagenen Reihenfolge; parallele Ausfuehrung, wo Eintraege laut Analyse
  unabhaengig sind und disjunkte Dateien anfassen
- **Ausfuehrung im Hintergrund:** Worker arbeiten die definierten Schritte des Eintrags
  ab (`task.md ## Schritte` bzw. definierte Schritte), der Nutzer arbeitet weiter,
  Meldung bei Abschluss
- **Bericht:** voller Bericht pro Task (was getan, was verifiziert, was aufgefallen) als
  `worker-report.md` im jeweiligen Change-Ordner — dritter Eintrag der status-neutralen
  Ordner-Datei-Familie (nach `review.md`, `fast-draft.md`); im Chat nur kompakte
  Sammel-Zeilen mit Links
- **Deckelung:** Limits (max. Versuche, max. Zeit pro Task) konfigurierbar in
  `workflow.config.yaml`; bei Erreichen Abbruch mit Befund im Bericht
- **Governance-Regel** in `skills/CLAUDE.md`: Autonomie nur zwischen Freigabe und
  Abnahme; der Skill ist schreibend und damit `disable-model-invocation: true`

### Nicht enthalten

- Selbst committen oder pushen — bleibt beim Menschen
- Status-/Anzeigefelder pflegen (Single-Writer-Annahme bleibt unangetastet)
- Start ohne menschliche Freigabe
- Discovery-/Spec-wuerdige Features — strikt nur Material mit definierten Schritten;
  eine INBOX-Idee ohne Change-Ordner muss vorher durch `/dtb:task` (die Nebenspalte
  weist darauf hin)
- Aenderungen an `idea-review` (keine vierte Weiche-Stufe), `workflow-next`,
  `workflow-checkpoint` — beleg-getriebener Folge-Zuschnitt
- Miterledigung von INBOX #33 (Triage-Sicht) — aber der Scanner wird so gebaut, dass
  #33 spaeter als zweites Bewertungsraster andocken kann (ein Scanner, mehrere Sichten)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Schreibkollision paralleler Worker auf zentralen Dateien (WORKFLOW_STATUS, INBOX, BACKLOG) | Mittel | Hoch | Design-Entscheidung im impl-plan (s. Offene Punkte); Scope-Ausschluss „Worker pflegen keine Statusfelder" deckt Status bereits ab; Kollisionsregel: zweiter Worker stoppt |
| Erkennungs-Fehlurteil: Eintrag als tauglich eingestuft, braucht aber doch Entscheidungen | Mittel | Mittel | Vorab-Fragen-Nebenspalte faengt Bekanntes ab; trifft der Worker trotzdem auf Ungeklaertes → Abbruch und Rueckmeldung als „teilweise", kein Raten |
| Task wird nie gruen → Endlos-Lauf | Mittel | Mittel | Deckelung (Versuche/Zeit) aus `workflow.config.yaml`; Abbruch mit Befund |
| Governance-Verwaesserung: schreibender Skill laeuft autonom | Niedrig | Hoch | `disable-model-invocation: true`; Autonomie nur zwischen expliziter Freigabe und Abnahme; Regel in `skills/CLAUDE.md` festgeschrieben |
| Seed-Skew: `DERIVED_STATE_RULES.md`-Aenderung (worker-report.md) erreicht Bestandsprojekte nicht | Hoch | Niedrig | Bekannter Preis (siebter Fall, Beleg fuer #22); Leser tolerant bauen wie bei den Vorgaengern |
| Abnahme-Aufwand waechst: Mensch muss fremde Diffs beurteilen | Mittel | Mittel | Voller Bericht pro Task (was getan/verifiziert/aufgefallen); abgelehnte Ergebnisse bleiben fuer Korrektur-Lauf liegen |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine harten Vorbedingungen — `workflow.config.yaml`-Platzhalter werden im Zuge
      der Limit-Konfiguration ohnehin befuellt (steht als offene Aufgabe im Status)

### Referenz-Dokumente

- `features/autonome-schiene/discovery.md` — vollstaendige Discovery (Scope, Verhalten, Randfaelle, Einschraenkungen, Integrationen)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — status-neutrale Ordner-Dateien (§1.1), Slug-Regeln (§4)
- `skills/dtb-implement/SKILL.md` — Checkpoint-Kriterien/Verifikations-Gate als Vorbild fuer das Abbruch-/Erfolgskriterium
- `skills/dtb-task/SKILL.md` — Task-Lane, deren Erfassungs-Ende die Schiene fortsetzt
- `skills/CLAUDE.md` — Governance-Konvention, dort landet die Autonomie-Regel
- Extern (Vorbild, kein Aenderungsziel): Pocock-Skills-Repo; Harness-Traeger Subagents/Worktrees/Background-Tasks/`/loop`

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] Die Erkennungs-Sicht listet alle offenen INBOX-Eintraege mit Urteil
      (ja/teilweise/nein) + 1-Satz-Begruendung, Abhaengigkeiten, empfohlener Reihenfolge
      und Vorab-Fragen-Nebenspalte
- [ ] Nach Freigabe fuehrt ein Worker einen einzelnen Eintrag im Hintergrund aus und
      erzeugt `worker-report.md` im Change-Ordner mit vollem Bericht
- [ ] Listen-Freigabe arbeitet die vorgeschlagene Reihenfolge ab; unabhaengige Eintraege
      mit disjunkten Dateien laufen parallel; ohne Worktree-Isolation degradiert die
      Lane auf sequenziell statt zu verweigern
- [ ] „teilweise"-Eintraege werden im Listen-Lauf uebersprungen und am Ende gesammelt
      gemeldet; ein Worker, der auf eine ungeklaerte Entscheidung stoesst, bricht ab und
      meldet „teilweise"
- [ ] Die Deckelung greift: ein nicht gruen werdender Task endet nach den konfigurierten
      Limits mit Befund statt endlos zu laufen
- [ ] `worker-report.md` ist in `DERIVED_STATE_RULES.md` als status-neutral deklariert;
      die Statusableitung eines Ordners aendert sich durch die Datei nachweislich nicht
- [ ] Kein Worker committet, pusht oder schreibt Status-/Anzeigefelder bzw. zentrale
      Dateien (WORKFLOW_STATUS, INBOX, BACKLOG)
- [ ] Erstlauf gegen `gitattributes-eol` durchgefuehrt: Vorab-Frage (Scope-Entscheidung
      Schritt 1) wird gestellt, danach laeuft der Rest autonom bis zur Abnahmemeldung

---

## Offene Punkte

- Die vier urspruenglichen Punkte (Schreibkoordination, Deckelungs-Defaults, Skill-Name,
  Worker-Form) sind entschieden — Ergebnisse in `plan.md` → `## Technische
  Entscheidungen` (E1: strukturelle Trennung; E2: 3 Versuche / 30 Min via Config;
  E3: `dtb:worker`; E4: Background-Subagent, Worktree immer)
- **Listen-/Parallel-Kalibrierung bewusst nachgelagert (plan-review 2026-08-08, F4a):**
  die Erstwurf-Abnahme deckt den Einzel-Pfad (`gitattributes-eol`); der Listen-/
  Parallel-Pfad ist textlich geliefert, aber unkalibriert. Nachgelagerte Kalibrierung
  beim ersten realen Listen-Lauf — benannter Kandidat: INBOX #46 (als Task erfasst)
  plus ein weiterer tauglicher Eintrag

---

**Erstellt mit:** `/dtb:feature-plan`
