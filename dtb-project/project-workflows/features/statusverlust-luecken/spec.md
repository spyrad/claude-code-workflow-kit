# Feature: Statusverlust-Luecken schliessen

**Erstellt:** 2026-09-23
**Ziel:** Der Status jeder Aufgabe wird ueber ihre gesamte Lebensdauer eindeutig festgehalten — nichts verschwindet mehr unbemerkt aus allen Sichten.
**Prioritaet:** Hoch <!-- Quelle: dtb:idea-rank 2026-09-17, #95 🟠 mittel-hoch, Rang 1 der offenen Ideen -->
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit leitet Status aus Artefakten ab — an vier Stellen fehlt dieses Artefakt, ist unsichtbar
oder traegt keinen Verlauf, sodass Arbeit still verloren gehen kann (INBOX #95, Befund 2026-09-17).
Der Change schliesst alle vier Luecken plus die Aufraeum-Luecke nach einer Leitlinie: **jeder Abgang
braucht einen Vermerk, jede offene Aufgabe ein Datum, jede Sicht sieht auch Worktrees** — ohne neuen
Status-Speicher, ohne Automatik-Entscheidungen, rein lesend ueber Worktree-Grenzen.

„Aufgabe" meint jede Arbeitseinheit, die in einer Sicht auftaucht: INBOX-Idee, Punkt unter
Offene Aufgaben / Naechste Schritte, Change im Worktree.

---

## Scope / Abgrenzung

### Enthalten
- **(1) Task-Lane-Luecke:** `Ausgearbeitet` gilt nur mit gueltigem Change-Link. Eine Idee ohne
  Link (oder mit Link auf einen nicht existierenden Ordner) gilt als „Ausgearbeitet, Change fehlt"
  und zaehlt als offen:
  - `dtb:archive` archiviert sie nicht, sondern meldet sie mit Hinweis auf `/dtb:task {N}`
  - `dtb:project-health` prueft den Link fuer `spec.md` UND `task.md`
  - `dtb:workflow-next`, `dtb:idea-rank`, `dtb:workflow-status` fuehren sie als offen
  - Link auf `archive/<slug>/` = erledigt, in Ordnung
- **(2) Abgangs-Luecke:** Kein Punkt verschwindet aus den Offenen Aufgaben ohne Abschlussvermerk.
  Der Checkpoint vergleicht die bisherige mit der neuen Liste und haelt fuer jeden wegfallenden
  Punkt im append-only Session-Log fest: `erledigt`, `verworfen: {Grund}` (Grund Pflicht) oder
  `aufgegangen in …`
- **(3) Alters-Luecke:** Jeder offene Punkt traegt `(seit YYYY-MM-DD)`; das Datum wird beim
  Uebertrag unveraendert mitgenommen. Ab einer konfigurierbaren Schwelle markiert der Checkpoint
  den Punkt mit ⏳ und fordert genau EINE Entscheidung (behalten / erledigen / verwerfen);
  „behalten" → erneute Frage erst nach der naechsten Schwelle. (2) und (3) sind ein Mechanismus
  (derselbe Vergleich)
- **(4) Worktree-Luecke:** `dtb:workflow-next`, `dtb:workflow-resume` und `dtb:backlog-status`
  zeigen einen Block „In Worktrees" — eine Zeile je Worktree ausser dem Haupt-Checkout mit Art
  (interaktiv / autonom / manuell), Branch, Commit-Stand, Anzahl uncommitteter Aenderungen und
  Fortschritt (Progress, Schritte oder Stage). Die Regel steht einmal in
  `DERIVED_STATE_RULES.md`; die drei Sichten referenzieren sie
- **Aufraeum-Luecke:** Ein bereits in den Hauptbranch gemergter Worktree erscheint als
  „gemergt → aufraeumen" statt mit Fortschritt; veralteter letzter Commit (Schwelle aus (3)) → ⏳
- **Uebergang Altbestand:** laufende Dauerlaeufer bekommen beim ersten Checkpoint nach Einfuehrung
  ein rekonstruiertes Datum aus ihrem ersten Log-Auftreten, gekennzeichnet `(seit ≤YYYY-MM-DD)`
- **Verteilungs-Robustheit (Kopie-Muster INBOX #22, entschieden 2026-09-23):** Die Regeln stehen
  kanonisch in `DERIVED_STATE_RULES.md`; jeder konsumierende Skill traegt eine kompakte operative
  Kopie mit Wartungs-Hinweis „Kopie ist Absicht — Seed erreicht Bestandsprojekte nicht automatisch".
  So wirken die Luecken-Schliessungen in allen Zielprojekten sofort nach `kit-sync`, ohne erneutes
  `project-init`

### Nicht enthalten
- Keine zentrale Statusdatei / -datenbank — Derived State bleibt; nur Artefakte werden ergaenzt
- Keine aktive Ueberwachung, kein getakteter Lauf — das ist #97; hier nur Anzeige beim Aufruf
- Keine Schreibzugriffe ueber Worktree-Grenzen — Sichten lesen Worktree-Branches und
  -Arbeitsbaeume, beschreiben sie nie; Schreibgrenzen-Regel und Worktree-Guard bleiben unveraendert
- Keine automatische Entscheidung — ⏳ und „aufraeumen" sind Hinweise; erledigen, verwerfen,
  abbauen entscheidet der Mensch bzw. der zustaendige Skill
- Keine rueckwirkende Aufarbeitung alter `WORKFLOW_STATUS`-Versionen und Logs; bereits archivierte
  Alt-Eintraege werden nicht nachgeprueft
- Kein Umbau des Statusmodells — BACKLOG-Legende und INBOX-Statuswerte bleiben; die Task-Lane-
  Entscheidung 2026-08-02 (impl-review F2: kein `In Arbeit` fuer geroutete Tasks) wird NICHT revidiert
- Keine Aenderung an der Worker-Governance (Autonomie-Regel, Kappen) und an `dtb:pane-start`/
  `dtb:worker` selbst — sie sind nur Leseziel

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| `DERIVED_STATE_RULES.md` ist ein Seed, `kit-sync` verteilt ihn nicht → Bestandsprojekte kennen die neuen Abschnitte nicht | Hoch | Mittel | Kopie-Muster #22: operative Kopie im Skill + Wartungs-Hinweis |
| Kopie und Kanon driften auseinander | Mittel | Mittel | Wartungs-Hinweis an jeder Kopie; Automated-Grep je Phase, dass Kopie und DSR-Abschnitt dieselben Kernbegriffe tragen |
| `workflow-checkpoint` (bereits 470 Zeilen) wird durch den Vergleich weiter aufgeblaeht | Hoch | Mittel | Kopie kompakt halten (Kernregel, Details nur in der DSR); Wachstum ≤ +40 Zeilen als Automated-Kriterium |
| Semantische Zuordnung irrt (umformulierter Punkt als „erledigt" gewertet) | Mittel | Mittel | Rueckfrage bei Unsicherheit; jeder Vermerk steht sichtbar im Log und ist korrigierbar |
| ⏳-Fragen werden zur Tapete (zu viele, zu oft) | Mittel | Mittel | Schwelle konfigurierbar, EINE vetobare Sammelvorlage statt Einzelfragen, „behalten" setzt neue Frist |
| Worktree-Sicht zeigt Harness- oder Fremd-Worktrees als Rauschen | Niedrig | Niedrig | Art `manuell`, genau 1 Zeile je Worktree; Block entfaellt ohne zusaetzliche Worktrees |
| Versehentliche Revision der F2-Entscheidung beim Umbau der Task-Lane | Niedrig | Hoch | Explizit im Nicht-enthalten; Absicherung nur auf der Leseseite |

---

## Dependencies

### Erforderlich vor Start
- [x] Offene Punkte in `/dtb:impl-plan` geklaert (2026-09-23, `plan.md` → Technische Entscheidungen)

### Referenz-Dokumente
- `features/statusverlust-luecken/discovery.md` - Discovery mit Modulen, Belegen, Randfaellen, Einschraenkungen
- `features/rueckfragen-erhebung/erhebung.md` - Schritt 3: 0 Pane-Stand-Nachfragen, belegte Anzeige- und Aufraeum-Luecke
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - Ableitungsregeln (§1.5 task/bug, §6.2/§6.4 Status-Neutralitaet)
- `skills/CLAUDE.md` - Schreibgrenzen-Regel „Parallele Sessions", Worktree-Guard-Vorlage
- `dtb-project/project-changelog/2026-09/2026-09-17.md` - Ursprungsbefund #95

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Eine Idee `Ausgearbeitet` ohne gueltigen Change-Link wird von `dtb:archive` nicht archiviert, sondern gemeldet; `dtb:project-health` meldet sie fuer `spec.md` und `task.md`; `dtb:workflow-next` fuehrt sie als offen
- [ ] Jeder Punkt, der aus den Offenen Aufgaben wegfaellt, hat im Session-Log genau einen Vermerk (`erledigt` / `verworfen: {Grund}` / `aufgegangen in …`) — kein Punkt verschwindet ohne Spur
- [ ] Jeder offene Punkt traegt ein `seit`-Datum, das ueber Checkpoints hinweg unveraendert bleibt; ab Schwelle erscheint ⏳ mit genau einer Entscheidung je Schwelle
- [ ] `dtb:workflow-next`, `-resume` und `dtb:backlog-status` zeigen jeden zusaetzlichen Worktree (pane, worker Pane-/Subagent-Traeger, manuell) mit Art, Stand, uncommitteten Aenderungen und Fortschritt; gemergte als „aufraeumen" — ohne einen Worktree zu beschreiben
- [ ] Abnahme-Lauf: ein vom Abnahme-Lauf selbst angelegter Wegwerf-Worktree erscheint in der Worktree-Sicht aus dem Haupt-Checkout heraus korrekt (auch nach Merge als „aufraeumen")
- [ ] Die Luecken-Schliessungen wirken auch mit einer alten `DERIVED_STATE_RULES.md`-Kopie (operative Kopie im Skill); ein Nicht-Git-Projekt zeigt keinen Worktree-Block und keinen Fehler
- [ ] Nutzer-Test: ein Checkpoint mit umformuliertem, zusammengelegtem und verworfenem Punkt erzeugt die richtigen Vermerke und uebernimmt das aelteste Datum

---

## Offene Punkte

- — keine — (die fuenf Punkte aus der Spec-Erstellung sind in `/dtb:impl-plan` am 2026-09-23 entschieden; siehe `plan.md` → `## Technische Entscheidungen`)

---

**Erstellt mit:** `/dtb:feature-plan`
