# Feature: Skill-Lint

**Erstellt:** 2026-11-26
**Ziel:** Die mechanisch prüfbaren Frontmatter-Regeln der Kit-Skills werden bei jedem Push und Pull Request maschinell geprüft statt nur durch das Modell.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Frontmatter-Regeln aus `skills/CLAUDE.md` prüft heute nur das Modell in
`dtb:project-health` Check 8, und der lief laut Inbox #181 auf keinem Rechner je. Echte Funde
(#195, #46, #88) zeigen, dass Verstöße so lange unbemerkt bleiben. Ein Prüfskript im Kit-Repo
mit eigenem Selbsttest und ein CI-Lauf bei Push und Pull Request machen die eindeutigen Regeln
zu einer Verteidigungsebene, die nicht von Aufmerksamkeit abhängt.

---

## Scope / Abgrenzung

### Enthalten
- Prüfskript für die eindeutigen Regeln: Pflichtfelder, Name passt zum Verzeichnis,
  `Use when:`-Präfix, Vorgänger/Nachfolger als Liste oder leer, Kanten-Ziel existiert, Kante
  hat ihr Gegenstück (mit begründeter Ausnahmeliste), Stage im erlaubten Wertebereich,
  Beschreibungslänge bei modellaufrufbaren Skills, Werkzeug-Pflicht für Skills mit
  Shell-Schritten oder Worktree-Guard
- Selbsttest des Skripts mit Beispiel-Skills je Fehlerklasse
- CI-Lauf bei Push und Pull Request (Selbsttest, dann Lint); Fehler machen den Lauf rot
- `dtb:project-health` Check 8 nutzt das Skript, wenn es im Projekt liegt
- Bestand bereinigen, sodass der erste CI-Lauf grün ist (#195, 7 einseitige Kanten)
- Doku-Nachzug (Root-`CLAUDE.md`, `skills/CLAUDE.md` samt Stage-Tabelle)

### Nicht enthalten
- Verteilung des Skripts an Zielprojekte — dort bleibt Check 8 die Modell-Sicht
  (per Kernfrage entschieden 2026-11-26)
- Verwaiste `consumes`/`produces` und zirkuläre Nachfolger-Ketten (bleiben Modell-Sicht)
- Tote Verweise in Prosa (Inbox #100), Umbau der Skills (Inbox #219)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Die Werkzeug-Regel trifft Skills falsch (Skill erwähnt einen Guard nur, führt ihn nicht aus) | Mittel | Niedrig | Regel auf die festen Anker-Zeilen beschränken, nicht auf Stichwörter (Lektion L2); Probelauf über den Bestand vor dem Scharfschalten |
| Ausnahmeliste wird zur Abkürzung für jede neue einseitige Kante | Niedrig | Mittel | Jede Ausnahme braucht einen Grund im Eintrag; die Liste steht sichtbar im Skript |
| Das Skript läuft lokal anders als in der CI (Abhängigkeit, Zeilenenden) | Mittel | Mittel | Zeilenenden normalisieren; fehlende Abhängigkeit mit klarer Meldung; Selbsttest in beiden Umgebungen |
| Doku und Skript driften auseinander (neue Regel nur in einer der beiden) | Mittel | Mittel | `skills/CLAUDE.md` nennt das Skript als Prüfinstanz; Regel-Änderungen ziehen das Skript im selben Zug mit |
| Geänderte verteilte Skills bleiben in den installierten Kopien alt | Hoch | Niedrig | Nach dem Merge `dtb:kit-sync` (im Hand-off vermerken) |

---

## Dependencies

### Erforderlich vor Start
- [x] Laufzeitumgebung des Skripts samt Abhängigkeit lokal verfügbar (geprüft 2026-11-26, Details in `discovery.md`)
- [x] Zielort entschieden: nur Kit-Repo + CI (2026-11-26)

### Referenz-Dokumente
- `skills/CLAUDE.md` — Frontmatter-Regeln (die Quelle, die das Skript prüft)
- `skills/dtb-project-health/SKILL.md` — Check 8, heutige Einstufung FEHLER/WARNUNG
- `dtb-project/project-workflows/INBOX-BEFUNDE.md` — Befunde #46, #88, #195

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Das Skript meldet jede der abgedeckten Fehlerklassen an einem Beispiel-Skill und endet dann mit Fehler-Exit
- [ ] Das Skript läuft über den heutigen Skill-Bestand ohne FEHLER
- [ ] Der CI-Lauf startet bei Push und Pull Request und wird rot, sobald ein FEHLER auftritt
- [ ] Die bekannten Funde #195 (fehlendes Werkzeug in drei Skills — der dritte, `dtb-open-question`, per plan-review 2026-11-26 gefunden) und die 7 einseitigen Kanten sind behoben oder begründet ausgenommen
- [ ] Check 8 nutzt das Skript, wenn es vorhanden ist, und bleibt sonst unverändert
- [ ] Die Doku beschreibt Skript und CI; keine Aussage „keine Tests/Build-Schritte" mehr

---

## Offene Punkte

- Je einseitiger Kante: Gegenkante ergänzen oder begründete Ausnahme? Wird in der Umsetzung
  Kante für Kante entschieden (Tendenz siehe `discovery.md`)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
