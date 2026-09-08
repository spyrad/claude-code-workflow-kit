# Feature: Checkpoint erfasst Verlustfunde

**Erstellt:** 2026-09-08
**Ziel:** Der Checkpoint erfasst die dringenden Verlustfunde nach einer einmal bestaetigten, zeilenweise streichbaren Sammelvorlage selbst, statt sie als Befehle zurueckzugeben, die liegen bleiben.
**Prioritaet:** Mittel
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Heute liefert die Verlustpruefung (Schritt 0 von `dtb:workflow-checkpoint`, ausgefuehrt von
`dtb:no-loss-check`) kopierfertige Befehle, die der Mensch einzeln tippen muss. Belegt
2026-09-07: neun Funde blieben offen, weil der Aufruf-Aufwand ueber die Erfassung entschied,
nicht die Wichtigkeit (Muster #69). Kuenftig zeigt der Checkpoint die Funde der Gruppe
**„Vor dem Checkpoint erledigen"** als EINE Sammelvorlage; der Mensch bestaetigt einmal oder
streicht Zeilen, und der Checkpoint schreibt die bestaetigten Eintraege selbst nach
`lessons.md` bzw. `INBOX.md` — nach den Regeln von `dtb:lesson` und `dtb:idea`, per Referenz
auf deren Schritte, nicht per Kopie. Die Gruppe „Kann warten" bleibt wie heute.

---

## Scope / Abgrenzung

### Enthalten
- **Sammelvorlage** fuer alle Funde der Gruppe „Vor dem Checkpoint erledigen" — beide Typen, Lektionen und Ideen. Schnittachse ist das Verlustrisiko (Gruppierung von `dtb:no-loss-check`), nicht der Typ
- **Eine Bestaetigung fuer alle**, einzelne Zeilen streichbar (Muster `dtb:feature-fast`). Nie still: die Vorlage IST die Bestaetigung, die Regel „Nie stiller Auto-Write" aus `dtb:lesson` bleibt gewahrt
- **Der Checkpoint schreibt selbst** nach `lessons.md` und `INBOX.md` und folgt dabei den Schritten von `dtb:lesson` (Feld-Ableitung, Duplikat-Check, Append-only) und `dtb:idea` (Duplikat-Check, Nummernvergabe, Format) — **per Referenz** auf deren Skill-Dateien, aufgeloest **Repo zuerst** (`skills/dtb-*/SKILL.md` relativ zum Projekt-Root), sonst installierte Kopie — bewusst umgekehrt zu `dtb:pane-start` (plan-review 2026-09-08). Die Regeln leben weiter an genau einer Stelle
- **Herkunfts-Marker** an jedem so erfassten Eintrag, innerhalb eines bestehenden Textfelds (keine neue Spalte)
- **Struktur-Check** vor dem Schreiben (Muster `dtb:pane-start` → `## Struktur-Check`): zwei getrennte Fehlerpfade — Quelle fehlt (Installationsproblem) vs. Anker fehlt (Drift). In beiden Faellen kein Schreiben, Rueckfall auf die heutigen Befehle im Report
- **Deklaration:** `produces` des Checkpoints wird um `project-rules/lessons.md` und `INBOX.md` erweitert (Pipeline-Kante, beidseitig gedacht — #46)
- **Wartungs-Hinweis (Format-Kopplung)** in `dtb:no-loss-check`, der den Checkpoint als Leser des Report-Formats (Gruppen-Ueberschriften, Befehlszeilen) benennt
- **Feste Log-Zeile** im Session-Log: Funde je Gruppe, davon erfasst mit Kennung (z.B. „2 dringend → L38, #73 · 5 kann warten, Befehle im Report")
- **Meldung nach dem Schreiben:** je Eintrag Zielartefakt und Kennung
- **Randfaelle:** leere dringende Gruppe → keine Vorlage; Duplikat-Treffer → Zeile markiert und vorgestrichen, nicht geblockt; alle gestrichen → nichts geschrieben, eine Meldezeile; Schreibfehler mitten drin → melden, was geschrieben wurde, Rest als Befehle; mehr als 10 dringende Funde → Rueckfall auf Befehle
- **Verteilung:** `kit-sync`-Nachlauf ist Teil der Abnahme — die installierte Kopie ist die, die laeuft
- **Korrektur der Zuordnungstabelle in `dtb:no-loss-check`** (`lessons.md` versioniert seit `f75979d`) — Nachtrag plan-review 2026-09-08: die Zeile steht im Block, den der Checkpoint in die Vorlage uebernimmt
- **Doku-Nachzug in `CLAUDE.md`/`skills/CLAUDE.md`/`README.md` (L3)** — Nachtrag Phase 3, 2026-09-08: Beschreibungen von Checkpoint („writes a session log AND …") und `no-loss-check` („writes nothing") tragen den neuen Schreibpfad; Duplikat-Schutz-Konvention nennt den Checkpoint als vierten Anwender per Referenz

### Nicht enthalten
- Die Gruppe **„Kann warten"** — bleibt kopierfertige Befehle im Report
- Aenderung der **Gruppierungslogik** von `dtb:no-loss-check` (ob „im Zweifel erste Gruppe" tatsaechlich greift — eigener offener Punkt)
- Das Flag `disable-model-invocation` an `dtb:lesson`/`dtb:idea` — bleibt `true`, das Flag steuert das Starten eines Skills, nicht das Lesen einer Datei (→ #69)
- **Pipe-Escaping** im Fund-Text (→ #70/#54)
- Nutzung des Herkunfts-Markers fuer die Triage in `dtb:idea-review` (→ #33)
- Eine Skill-Kante Checkpoint → `dtb:lesson`/`dtb:idea` im Frontmatter — es findet kein Aufruf statt
- Aufruf-Modell (Skill-Tool) statt Referenz-Modell — verworfen, weil es #69 vorwegnaehme

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Inhaltsdrift der referenzierten Schritte — der Struktur-Check prueft Anker-Existenz, nicht Inhalt (F1-Klasse vom 2026-09-07) | Mittel | Mittel | Restrisiko benennen wie `dtb:pane-start`; beidseitige Wartungs-Hinweise an den Anker-Sektionen in `lesson`/`idea`; `impl-review` prueft die Kopplung |
| Dringende Gruppe praktisch immer leer — Feature greift selten | Hoch | Niedrig | Bewusst enger Schnitt, Datenlage in der Discovery dokumentiert; die neue Log-Zeile macht die Gruppierung kuenftig sichtbar und liefert die Grundlage fuer eine Nachjustierung |
| Ein zweiter Schreiber entsteht doch (Regeln werden kopiert statt referenziert) | Mittel | Hoch | Success-Kriterium mit Grep-Nachweis: Regeltexte existieren nur an einer Stelle; Referenz-Mechanik im Plan festschreiben |
| Vorlage wird unhandlich | Niedrig | Mittel | Ab mehr als 10 dringenden Funden Rueckfall auf Befehle |
| Doppelter Eintrag trotz Duplikat-Check | Niedrig | Niedrig | Treffer in der Vorlage markiert und vorgestrichen, Mensch entscheidet |
| Merge-Konflikt mit #56/#52/#35 an derselben Skill-Datei | Niedrig | Niedrig | Nicht parallel bearbeiten |
| Checkpoint-Skill waechst (heute 373 Zeilen) | Mittel | Niedrig | Neue Logik als ein Unterabschnitt in Schritt 0; Referenz statt Kopie haelt ihn schlank |

---

## Dependencies

### Erforderlich vor Start
- [x] `lessons.md` versioniert (`f75979d`, 2026-09-07) — sonst waere der Schreibpfad maschinenlokal
- [x] Duplikat-Check in `dtb:idea` gebaut und abgenommen (`capture-duplikat-schutz`, 2026-09-07)
- [x] Discovery abgeschlossen (`features/checkpoint-verlustfunde/discovery.md`, 2026-09-08)

### Referenz-Dokumente
- `features/checkpoint-verlustfunde/discovery.md` - Scope, Randfaelle, Einschraenkungen, Datenlage zur Gruppierung
- `skills/dtb-workflow-checkpoint/SKILL.md` - Wirkstelle, Schritt 0
- `skills/dtb-lesson/SKILL.md` - Referenzquelle Schritte 2-4
- `skills/dtb-idea/SKILL.md` - Referenzquelle Duplikat-Check, Nummernvergabe, Format
- `skills/dtb-no-loss-check/SKILL.md` - Report-Format, zwei Gruppen nach Verlustrisiko
- `skills/dtb-pane-start/SKILL.md` - Muster Referenz-statt-Kopie und Struktur-Check
- `skills/dtb-feature-fast/SKILL.md` - Muster Sammelvorlage und Selbst-Eskalation
- `INBOX.md` #72 (Idee), #69 (Gegenseite), #46 (Kanten-Reziprozitaet)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Checkpoint mit mindestens einem dringenden Fund zeigt genau EINE Vorlage; nach der Bestaetigung stehen die Eintraege in `lessons.md` bzw. `INBOX.md` — mit Marker, korrekt nummeriert, im selben Format wie von Hand erfasst
- [ ] Eine gestrichene Zeile wird nicht geschrieben; sind alle gestrichen, wird nichts geschrieben und genau eine Meldezeile ausgegeben
- [ ] Leere dringende Gruppe → keine Vorlage, kein leerer Block; „Kann warten" erscheint unveraendert als Befehle
- [ ] Ein Duplikat-Treffer wird in der Vorlage markiert und vorgestrichen gezeigt, nicht geblockt
- [ ] Struktur-Check: fehlende Quelle und fehlender Anker fuehren zu zwei verschiedenen Meldungen und in beiden Faellen zum Rueckfall auf Befehle, ohne Schreiben
- [ ] Das Session-Log traegt die feste Zeile mit Funden je Gruppe und den erfassten Kennungen
- [ ] `produces` des Checkpoints enthaelt `project-rules/lessons.md` und `INBOX.md`; `dtb:no-loss-check` traegt den Wartungs-Hinweis mit dem Checkpoint als Leser
- [ ] Kein Regeltext aus `dtb:lesson`/`dtb:idea` ist kopiert — Grep-Nachweis, dass Feld-Ableitung, Duplikat-Check und Nummernvergabe nur an je einer Stelle beschrieben sind
- [ ] `kit-sync`-Nachlauf durchgefuehrt; Wirklauf im Haupt-Checkout gegen die installierte Kopie (L29), nicht im Worktree

---

## Offene Punkte

- Wendet `dtb:no-loss-check` die Regel „im Zweifel erste Gruppe" tatsaechlich an? Belegt sind 6/6 „Kann warten" in drei Sessions. Ausserhalb von #72, bestimmt aber, wie oft das Feature greift
- Marker-Form ist Arbeitsannahme: Suffix `(via Checkpoint YYYY-MM-DD)` im Textfeld `Context` (lessons) bzw. im Idee-Text (INBOX) — im Implementierungsplan bestaetigen
- Antwortformat fuer „Zeile streichen" in der Vorlage (Nummern nennen? Zeile loeschen?) — im Implementierungsplan festlegen, Muster `dtb:feature-fast` pruefen

---

**Erstellt mit:** `/dtb:feature-plan`
