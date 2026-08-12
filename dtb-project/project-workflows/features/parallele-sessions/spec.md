# Feature: Parallele Sessions

**Erstellt:** 2026-08-12
**Ziel:** Parallele Sessions in einem Projekt laufen ohne Verlustrisiko an den globalen Dateien — genau ein globaler Schreiber (Orchestrator im Haupt-Checkout), Worker-Sessions in eigenen Worktrees, Hand-off statt Direktschreiben.
**Prioritaet:** Hoch
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit geht heute stillschweigend von einer Session pro Projekt aus: die globalen Dateien
(INBOX, BACKLOG, WORKFLOW_STATUS, Changelog, lessons.md) haben ein Single-Writer-Modell, das
nirgends erzwungen wird. Zwei belegte Vorfaelle (Nummernvergabe-Kollision #44/#39; fremder
INBOX-Nachtrag waehrend eines laufenden idea-review am 2026-08-11) zeigen beide Seiten des
Problems: unkoordinierte Schreiber und veraltete Lesestaende. Dieses Feature macht das
implizite Modell explizit und maschinell: global schreibende Skills brechen in Worktrees ab
(Schreib-Guard), lesend-entscheidende Skills pruefen ihren Lesestand vor Entscheidungen
(Lese-Seite), und Worktree-Sessions uebergeben ihre Session-Inhalte als standardisierten
Hand-off-Block an die Orchestrator-Session, die den Checkpoint ausfuehrt.

---

## Scope / Abgrenzung

### Enthalten

- **(A) Schreib-Guard** fuer die 8 global schreibenden Skills (`workflow-checkpoint`,
  `idea`, `idea-review`, `archive`, `lesson`, `meeting-dump`, `task`, `bug-report`):
  einheitlicher harter Abbruch, wenn der Skill in einem verlinkten Worktree laeuft
  (Erkennung: `git rev-parse --git-dir` ≠ `--git-common-dir` — mechanisch, nie ueber
  Pfad-Konventionen oder Config-Flags). Die Abbruchmeldung nennt den Haupt-Checkout-Pfad
  und gibt bei Capture-Skills den erfassten Text als fertigen Befehl zurueck (kein
  Erfassungs-Verlust durch den Abbruch)
- **(B) Lese-Seite** fuer lesend-entscheidende Skills (`idea-review`, `workflow-resume`):
  Pruefung des Lesestands (mtime als billiger Trigger) unmittelbar vor jeder
  Statusentscheidung bzw. vor der Report-Ausgabe; bei Abweichung Re-Read + eine ⚠-Zeile,
  Meldung stuetzt sich auf den Inhaltsvergleich. Kein Abbruch, keine Nachfrage —
  melden statt blockieren (§1.3-Ton)
- **(C) Konvention + Doku** in `skills/CLAUDE.md` (ggf. `DERIVED_STATE_RULES.md`):
  Orchestrator-Muster (genau EINE Session im Haupt-Checkout als einziger globaler
  Schreiber, N Worker-Sessions in eigenen Worktrees), EINE Schreibgrenzen-Regel, auf die
  `dtb:worker` und der Guard gemeinsam verweisen (keine zwei gepflegten Formulierungen),
  Liste der worktree-faehigen Skills (`open-question` explizit worktree-faehig — schreibt
  nur Feature-Artefakte), Empfehlung der nativen CC-Worktree-Tools (`EnterWorktree`/
  `ExitWorktree`, Subagents mit `isolation: worktree`) als dokumentierter Weg
- **(D) Hand-off Worker → Orchestrator:** standardisierter, status-neutraler
  Hand-off-Block, den eine Worktree-Session am Ende produziert (Session-Inhalte
  checkpoint-fertig), plus Empfangsseite in `workflow-checkpoint` (fremden Session-Block
  als Eingabe annehmen). Primaerer Transport: Herdr-Session-zu-Session-Kommunikation
  <!-- Lint-Override: Herdr ist die reale Arbeitsumgebung des Nutzers (Terminal-Multiplexer
  mit Session-Kommunikation) und als Transport eine echte fachliche Anforderung, kein
  Implementierungsdetail -->; Fallback ohne Herdr: Text-Echo der Guard-Abbruchmeldung,
  manuell getragen. Das Kit bleibt transportneutral definiert (Format + Empfangsseite),
  Herdr ist der gedachte Traeger
- Neuer **Config-Key** in `workflow.config.yaml` (Guard-/Parallelitaets-Konfiguration,
  z.B. Default-Branch) — optional mit Default, verteilt ueber das `project-init`-Template

### Nicht enthalten

- Keine aktive Worktree-Orchestrierung (kein Skill legt Worktrees an oder verwaltet sie —
  das leisten die CC-nativen Tools bzw. `dtb:worker` fuer seinen Fall selbst)
- Keine Locking-/Merge-Mechanik fuer die globalen Dateien (kein File-Lock, keine
  automatische Changelog-Zusammenfuehrung — nur Erkennen und Melden; Zusammenfuehrung
  zweier Sessions am selben Tag bleibt bei #56)
- Kein Schutz gegen externe Schreiber auf Dateisystem-Ebene (der Fremdprojekt-Fall wird
  ueber die Lese-Seite (B) adressiert, nicht verhindert)
- Keine Hook-Haertung (PreToolUse-Block) — mechanisch zuverlaessiger, aber exakt Idee #45
  (Hooks im Kit inkl. Verteilweg-Frage); hier nur als Notiz „Haertung per Hook =
  #45-Kandidat" festgehalten

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Spiegel-Kopplung: Guard-Text in 8 SKILL.md + Konvention laufen auseinander (zweimal belegte Fehlerklasse) | Hoch | Mittel | EINE Regel in `skills/CLAUDE.md`, Skills tragen nur kurzen einheitlichen Guard-Block mit Verweis; plan-review-Gate prueft die Kopplung |
| Guard wird ueberlesen (Skill-Anweisung, keine Mechanik — Modell fuehrt aus) | Mittel | Mittel | Guard als erster Schritt vor jedem Schreiben, identische Formulierung in allen 8; Haertung per Hook als #45-Kandidat notiert |
| Seed-Skew: Bestandsprojekte haben den Config-Key nicht (#22, sechs belegte Faelle) | Hoch | Niedrig | Key optional mit Default — Verhalten ohne Key identisch zu heute; kein Pflicht-Feld |
| Empfangsseite kollidiert mit #35 (beide fassen `workflow-checkpoint` an) | Mittel | Mittel | Reihenfolge vor Implementierungsstart klaeren; Hand-off-Block status-neutral nach §1.1 halten, damit keine neue Zustandsaussage ohne Pfleger entsteht |
| Lese-Seite: Race zwischen Pruefung und eigenem Schreiben bleibt | Mittel | Niedrig | Bewusst akzeptierte Restluecke (Locking ist Nicht-Ziel); dokumentiert in Konvention |
| Guard-Fehlschlag der Erkennung (kein Git, exotische Setups) | Niedrig | Niedrig | Fehlschlag = Durchlass, kein Abbruch — Nicht-Git-Projekte bleiben unbeeintraechtigt |

---

## Dependencies

### Erforderlich vor Start

- [ ] Reihenfolge-Entscheid zu #35 (parallel geplant? dann zuerst klaeren, wer
      `workflow-checkpoint` wann anfasst)

### Referenz-Dokumente

- `features/parallele-sessions/discovery.md` — vollstaendige Discovery (Scope-Herleitung, Randfaelle, Guard-Listen-Zuschnitt)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — §1.1 (status-neutrale Artefakte), §1.3 (Konfliktmeldungs-Ton), §4 (Slugs)
- `skills/dtb-worker/SKILL.md` — Prior Art: Schreibgrenze (F1), Kollisionsregel, Worktree-Lebenszyklus
- `INBOX.md` #42 (inkl. Nachtraege 2026-08-11) — Herleitung und Belegfaelle

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] Jeder der 8 Guard-Skills bricht in einem verlinkten Worktree vor dem ersten
      Schreiben ab; die Meldung nennt den Haupt-Checkout-Pfad, bei Capture-Skills
      enthaelt sie den erfassten Text als fertigen Befehl
- [ ] In Nicht-Git-Projekten und im Haupt-Checkout aendert sich NICHTS am Verhalten der
      8 Skills (Guard ist dort unsichtbar — kein Rauschen, keine Rueckfrage)
- [ ] `idea-review` und `workflow-resume` erkennen eine zwischenzeitliche Aenderung der
      gelesenen Datei, lesen neu und melden genau dann eine ⚠-Zeile, wenn der Inhalt
      tatsaechlich abweicht (mtime-only-Aenderung erzeugt keine bzw. eine abgeschwaechte
      Meldung)
- [ ] Eine Worktree-Session kann einen Hand-off-Block produzieren, und
      `workflow-checkpoint` nimmt ihn als Eingabe an und schreibt daraus den
      Session-Log-Eintrag — belegt durch einen realen Worker→Orchestrator-Durchlauf
- [ ] `skills/CLAUDE.md` traegt die Orchestrator-Konvention und EINE
      Schreibgrenzen-Regel, auf die `dtb:worker` und die Guard-Bloecke verweisen (kein
      zweiter gepflegter Wortlaut)
- [ ] Der neue Config-Key ist optional: ein Projekt ohne den Key verhaelt sich exakt wie
      heute (Seed-Skew-sicher, #22)

---

## Offene Punkte

- Konkretes Format des Hand-off-Blocks: welche Felder braucht die Empfangsseite von
  `workflow-checkpoint` mindestens (Erledigt / Entscheidungen / Dateien / Naechste
  Schritte?), status-neutral nach §1.1 — Detailfestlegung im Implementierungsplan
- Name und Default des neuen Config-Keys (Default-Branch/Guard-Konfiguration) — im
  Implementierungsplan festlegen, Constraint: optional mit Default (#22)
- Guard-Zugehoerigkeit von `dtb:feature-start` haengt an #52 (tote Schreib-Anweisung auf
  die nicht mehr existierende Sektion „Laufende Arbeit"; wird sie dort wiederbelebt, ist
  `feature-start` der neunte Guard-Skill)
- Wird #35 vor, nach oder mit diesem Feature umgesetzt? (beide aendern
  `workflow-checkpoint` — Dependency oben)

---

**Erstellt mit:** `/dtb:feature-plan`
