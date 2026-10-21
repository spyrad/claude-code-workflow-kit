# Feature: Pane-Session-Neustart

**Erstellt:** 2026-10-21
**Ziel:** In einem `dtb:pane-start`-Arbeitsplatz eine frische Session starten koennen, ohne Pane-Startkontext, offene Hand-off-Punkte oder Session-Wissen zu verlieren.
**Prioritaet:** offen (siehe Offene Punkte)
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Wird in einer Pane aus `dtb:pane-start` das Kontextfenster zu gross (z. B. `dtb:implement` meldet „Schwelle erreicht — weiter in neuer Session"), verliert eine frische Session heute alles, was nur im Gespraech steht: Rolle, Orchestrator-Adresse, Rueckweg-Pflicht, gesammelte uebersprungene globale Updates und Entscheide (Praxisfall PKP `simulationsmaske-organisationseinheit`, 2026-10-21). Das Feature schafft einen definierten Uebergabe-Weg Session → Session in derselben Pane: `dtb:workflow-checkpoint` sichert beim Wechsel eine lokale Uebergabe-Notiz im Worktree, `dtb:workflow-resume` findet sie in der neuen Session, und am Ende erhaelt der Orchestrator genau einen kumulierten WORKTREE-HANDOFF-Block. Vorbild ist der Session-Wechsel im Haupt-Checkout (`## Handoff` in `WORKFLOW_STATUS.md` → `/clear` → `/dtb:workflow-resume`).

---

## Scope / Abgrenzung

### Enthalten
- **Uebergabe traegt vier Verlust-Klassen:**
  1. Pane-Startkontext — Rolle (interaktiv, kein autonomer Worker), Orchestrator-Adresse, Schreibgrenzen, Rueckweg-Pflicht (Block woertlich inkl. Kopfzeile)
  2. aufgelaufene `↷`-Zeilen der Teil-Guards und Hand-off-Punkte aus der Umsetzung, die nicht in `plan.md` stehen
  3. Session-Verlauf — Entscheide, Plan-Abweichungen, Lektions-Kandidaten ausserhalb von `## Lektion-Kandidaten`
  4. Hinweis auf Uncommittetes, das die neue Session mitnehmen muss (z. B. SHA-Rueckschreibung in `plan.md`)
- **Geltungsbereich:** jeder verlinkte Worktree, nicht nur `pane-start`-Arbeitsplaetze — Worker-Traeger rufen den Checkpoint nie auf, eine Abgrenzung ist daher unnoetig
- **Sichern ueber `dtb:workflow-checkpoint`:** im verlinkten Worktree fragt der Skill „Session-Wechsel oder Ende der Arbeit?"
  - Wechsel → Uebergabe-Notiz anlegen bzw. um einen Abschnitt ergaenzen; kein Block an den Orchestrator
  - Ende → genau EIN kumulierter WORKTREE-HANDOFF-Block (alle Notiz-Abschnitte + aktuelle Session), Format unveraendert
- **Wiederfinden ueber `dtb:workflow-resume`:** nach `/clear` (bzw. `/exit` + `claude`) findet der Skill die Notiz und stellt Startkontext, offene Hand-off-Punkte und naechsten Befehl her
- **Notiz lebt im Git-Verwaltungsordner des Worktrees:** nie committet, keine Ignorier-Regel noetig, verschwindet mit dem Abbau des Arbeitsplatzes
- **Mehrere Wechsel:** die Notiz waechst append-only, ein Abschnitt je Session
- **Adress-Pruefung:** `workflow-resume` prueft die Orchestrator-Adresse aus der Notiz ueber Herdr; ist sie weg → Warnung + Rueckfrage nach der neuen Adresse. Diese Pruefung ist eine zweite benannte Ausnahme vom Kanon „Herdr-Kommandos nur in `dtb:worker`" (Spiegel-Hinweis in beiden Richtungen)
- **Warnung vor dem Abbau:** die Abbau-Anleitung in `dtb:worker` (`#### Abschluss`, von `pane-start` per Referenz genutzt) prueft vor dem Entfernen des Worktrees, ob eine ungesendete Notiz existiert
- **Wechsel-Weg angekuendigt an zwei Stellen:** Begruessungstext von `dtb:pane-start`; Schwellen-Zeile von `dtb:implement` (im Worktree: „erst `/dtb:workflow-checkpoint` (Wechsel), dann `/clear`, dann `/dtb:workflow-resume`")
- **Ohne Herdr** funktionieren Sichern und Wiederfinden; nur die Adress-Pruefung entfaellt
- Kopplungen nachziehen: Struktur-Check von `pane-start`, Herdr-Ausnahmen-Liste in `dtb:worker`, Skill-Kategorien in `skills/CLAUDE.md`, Beschreibungen in `CLAUDE.md`

### Nicht enthalten
- Der autonome Pane-Traeger von `dtb:worker` (eigene Governance; ruft den Checkpoint nie auf)
- Sessions im Haupt-Checkout (dort traegt `WORKFLOW_STATUS.md` → `## Handoff`)
- Neustart per Herdr-Fernsteuerung durch Pane-Session oder Orchestrator — der Mensch loest den Neustart selbst aus
- Zwischen-Bloecke an den Orchestrator je Session-Wechsel
- Persistierte Pane-Registry
- Ein neuer Skill oder ein SessionStart-Hook
- Lesen der Notiz in jedem Arbeits-Skill (z. B. `dtb:implement`)
- Anzeige ungesendeter Notizen in den Worktree-Zeilen von `workflow-next`/`workflow-resume`/`backlog-status` (DSR §10)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Abbau loescht eine ungesendete Notiz still (sie liegt im Git-Verwaltungsordner) | Mittel | Hoch | Pflicht-Warnung in der Abbau-Anleitung; Ende-Checkpoint als regulaerer Weg |
| Orchestrator-Adresse in der Notiz ist veraltet → End-Block geht ins Leere | Mittel | Mittel | Adress-Pruefung im Resume mit Rueckfrage |
| Mensch tippt nach `/clear` direkt den Arbeitsbefehl statt Resume → Startkontext fehlt in dieser Session | Hoch | Niedrig | Ankuendigung im Begruessungstext und in der Schwellen-Zeile; Ende-Checkpoint liest die Notiz trotzdem — kein Verlust am Ende |
| Startkontext fehlt bereits in der ersten Session (Verlauf verdichtet, Begruessungstext weg) | Niedrig | Mittel | Rueckfall definieren (Offene Punkte) |
| Neue Herdr-Ausnahme im Resume driftet gegen `dtb:worker` | Niedrig | Mittel | deklarierter Spiegel mit Kopplungs-Hinweis in beiden Richtungen + Grep-Verifikation |
| Checkpoint-Guard wird komplexer (Voll-Guard mit lokalem Schreibweg) — Kategorie-Kanon in `skills/CLAUDE.md` passt nicht mehr woertlich | Mittel | Niedrig | Kategorie-Text praezisieren: Schreibweg nur in den Git-Verwaltungsordner, nie in globale Dateien |

---

## Dependencies

### Erforderlich vor Start
- [ ] Discovery abgeschlossen (`features/pane-session-neustart/discovery.md`)

### Referenz-Dokumente
- `dtb-project/project-workflows/features/pane-session-neustart/discovery.md` - Anforderungen, Entscheide, Randfaelle
- `skills/dtb-workflow-checkpoint/SKILL.md` - Worktree-Guard, `### Hand-off-Block`, `## Handoff`-Muster im Haupt-Checkout
- `skills/dtb-workflow-resume/SKILL.md` - Empfangsseite des Handoffs, Worktree-Stand
- `skills/dtb-pane-start/SKILL.md` - Begruessungstext, Struktur-Check
- `skills/dtb-worker/SKILL.md` - `### Pane-Auftrag` (Herdr-Ausnahmen), `#### Abschluss`
- `skills/dtb-implement/SKILL.md` - Ritual Punkt 11 (Schwelle)
- `skills/CLAUDE.md` - Parallele Sessions, Skill-Kategorien, Rueckfragen-Defaults
- `dtb-project/project-rules/lessons.md` - L67 (`/clear` behaelt Prozess), L86/L87 (Herdr-Tasten, Pane-Status)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] In einem verlinkten Worktree (z. B. einer `pane-start`-Pane) fragt `/dtb:workflow-checkpoint` „Wechsel oder Ende?"; „Wechsel" legt die Notiz an bzw. ergaenzt sie um einen Abschnitt und schickt nichts an den Orchestrator
- [ ] Nach `/clear` stellt `/dtb:workflow-resume` Rolle, Orchestrator-Adresse, Rueckweg-Pflicht, offene Hand-off-Punkte und den naechsten Befehl her, ohne dass der Mensch etwas kopiert
- [ ] Nach zwei Wechseln enthaelt der Ende-Block die Inhalte aller drei Sessions; der Orchestrator empfaengt genau einen Block mit unveraenderter Kopfzeile
- [ ] Die Notiz erscheint nie in `git status` und nie in einem Commit
- [ ] Veraltete Orchestrator-Adresse → Resume warnt und fragt nach der neuen Adresse
- [ ] Worktree ohne Notiz → Resume-Ausgabe unveraendert gegenueber heute
- [ ] Abbau-Anleitung warnt vor dem Entfernen eines Worktrees mit ungesendeter Notiz
- [ ] Begruessungstext von `pane-start` und Schwellen-Zeile von `implement` (im Worktree) nennen den Wechsel-Weg
- [ ] Haupt-Checkout-Verhalten von `workflow-checkpoint` und `workflow-resume` unveraendert
- [ ] Spiegel und Kopplungen per Grep verifiziert (Herdr-Ausnahme, Struktur-Check-Anker, Skill-Kategorien)
- [ ] Abnahme am Praxisfall: ein Session-Wechsel in einer echten `pane-start`-Pane ohne Verlust der vier Klassen

---

## Offene Punkte

- Prioritaet des Features festlegen (in der Discovery nicht besprochen)
- Notiz-Format: Dateiname im Git-Verwaltungsordner; Kopf (Pane-Startkontext, einmalig) + append-only Abschnitt je Session — sollen die Abschnitts-Felder 1:1 auf den Hand-off-Block abbilden, damit der Ende-Checkpoint mechanisch kumulieren kann?
- Was passiert nach dem Ende-Checkpoint mit der Notiz: als „gesendet" markieren oder loeschen? (Herdr bestaetigt die Zustellung nicht — bestimmt, wie die Abbau-Warnung „ungesendet" erkennt)
- Geklaert im Plan (T4, plan-review 2026-10-21): Die Weiche „Wechsel oder Ende?" gilt in jedem verlinkten Worktree
- Form der Weiche nach den Rueckfragen-Defaults: Knopf oder Textzeile, und welche Option ist der Vorschlag?
- Rueckfall, wenn der Begruessungstext beim ersten Wechsel nicht mehr im Verlauf steht (Verlauf verdichtet): Orchestrator-Adresse und Rolle erfragen oder aus dem Worktree-Pfad ableiten?
- Die Notiz haelt die fluechtige Orchestrator-Adresse fest — bewusste Abweichung vom Persistenz-Verzicht in `pane-start`; Begruendung im Plan an der Stelle festhalten

---

**Erstellt mit:** `/dtb:feature-plan`
