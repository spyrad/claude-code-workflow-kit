# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-08-20
**Letzter Session-Log:** `dtb-project/project-changelog/2026-08/2026-08-20.md` (Session 1)

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| pane-start (#68) | Abgenommen | 8/8 | `/dtb:archive` — Arbeitsplatz vorher abbauen (Pane `w3:p6`, Worktree, Branch) |
| capture-duplikat-schutz (#48) | Fertig zum Testen | 11/11 | `/dtb:impl-review capture-duplikat-schutz` (Zweitlauf), dann echter Skill-Lauf im Haupt-Checkout |
| feature-fast (#37) | Fertig zum Testen | 11/11 | Restabnahme: 2 UX-Urteile + Lauf mit gefixter Fassung (`1eec2ea`) |
| output-style-gezielt (#40) | Fertig zum Testen | 11/11 | Im Alltag beobachten, dann Abnahme im Checkpoint |
| feature-start-statusfeld (#50) | Fertig zum Testen | 5/5 | Verhaltenstests gegen die gefixte Fassung, dann Abnahme |
| meeting-agenda (#25) | Fertig zum Testen | 5/5 | Restabnahme dreigeteilt — Positiv-Lauf nur ausserhalb des Kits moeglich |

Anzeigefelder synchron zur Ableitung. Keine Feld-Konflikte.
⚠ Alle fuenf `review.md` mit negativem Verdikt (4x REJECTED, `pane-start` NEEDS ATTENTION) —
Triage-Bilanzen zeigen alle Findings behoben oder entschieden: eingefrorene Verdikt-Felder (#35).
⚠ `capture-duplikat-schutz`: die Handoff-Regel „review.md REJECTED → `/dtb:implement`" trifft hier
nicht — alle 13 Findings sind behoben, faellig ist der Review-Zweitlauf (dieselbe Familie #35).

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Erreicht (2026-08-20)** | **`pane-start` (#68) abgenommen — und zwar durch echte Arbeit:** die Pane-Session fuhr `capture-duplikat-schutz` (#48) von der Erhebung bis 11/11 inkl. impl-review-Triage (13/13 FIXED) und lieferte einen formatkonformen Hand-off. Damit ist das vierte Manual-Kriterium erstmals belegt statt behauptet. ff-Merge (9 Dateien, +1321/-4), 6 Commits gepusht (`96cea91`), **Lock 47 @ `96cea91`, 47/47 synchron** |
| **Notizen** | Nachbesserung `e126294`: nicht reproduzierbare Zielzahl im `no-loss-check`-Spiegel behoben, alle drei Zusagen nachgemessen (4/7/3). **L28-L33 erfasst** (nur lokal, #34/#64) — Rueckstand „nach `skills/CLAUDE.md` heben" jetzt L11-L14 + L22-L33. Ideen-Bestand 33 offen (#69, #70 neu). ROADMAP-§5-Sync zum **15.** Mal leer (reine Platzhalter-Vorlage) |

---

## Offene Aufgaben

- [ ] **Arbeitsplatz `capture-duplikat-schutz` abbauen** — `/exit` in Pane `w3:p6`, `git worktree remove ../.dtb-worktrees/pane-capture-duplikat-schutz`, `herdr pane close w3:p6`, `git branch -d feature/capture-duplikat-schutz`
- [ ] **Echter Skill-Lauf je Zielskill** (`/dtb:idea`, `/dtb:task`, `/dtb:bug-report`) im Haupt-Checkout — Treffer- und Blind-Fall; im Worktree strukturell unmoeglich (L29)
- [ ] **INBOX #54 reparieren** — bare Pipes brechen das Rendering (Teil von #70)
- [ ] **3 Verlustfunde vom 2026-08-19 absetzen** — Config-vor-Guard, `{Grund}`-Platzhalter (F8), `stage`-Enum; F7 (`impl-review`-Ausnahmeliste) bewusst nicht erfasst, inzwischen zweifach belegt
- [ ] **F4-Nachlauf** — Branch-Prosa in `dtb-workflow-checkpoint`; Quelle: `archive/herdr-worker-automation/spec.md`
- [ ] **Aeltere Verlustfunde absetzen** — L15-Raender-Lektion, Fall-C (2026-08-14), #60-Nachtrag, 9 Funde aus 2026-08-06/07/11
- [ ] **L11-L14 + L22-L33 nach `skills/CLAUDE.md` heben** — leben nur lokal (#34/#64), L15-L21 fehlen auf dieser Maschine ganz
- [ ] **`/dtb:idea-review` fortsetzen** — 33 offene Ideen
- [ ] #70 · #69 · #66 · #64 · #63 · #62 · #61 · #60 · #59 · #58 · #57 · #56 · #55 · #54 · #53 · #52 · #51 · #35 · #33 entscheiden
- [ ] Restabnahmen der vier Bestands-Features · Config-Platzhalter fuellen · ROADMAP.md befuellen oder entfernen

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-08-20 | `capture-duplikat-schutz` (#48) Idee→11/11 in der Pane; `pane-start` abgenommen | Duplikat-Schutz-Konvention + 3 gehaertete Capture-Skills, Lock 47 @ `96cea91` | `2026-08/2026-08-20.md` (S1) |
| 2026-08-19 | `pane-start` (#68) Idee→8/8 an einem Tag, verteilt | Interaktive Pane-Schiene, E2E real belegt | `2026-08/2026-08-19.md` (S1+S2) |
| 2026-08-18 | 5 abgenommene Items archiviert, Bestand bereinigt | 2 Ideen + 1 Feature + 2 Aufgaben nach `archive/` | `2026-08/2026-08-18.md` (S1) |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant
**Status:** Bewusst vertagt (2026-07-28) — Ast-Entscheidung (Brownfield-Zweig), braucht Fokus.
**Details:** `INBOX.md` #15; Analysen `2026-07/2026-07-27.md`, `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — dieser Checkpoint hinterlaesst Log, Status, BACKLOG, INBOX und zwei `spec.md` uncommittet.
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume`, danach obigen Befehl.
**Gueltigkeitsbedingung:** Der Commit-Befehl gilt, solange `git status --short` nicht leer ist; danach ist der naechste Schritt der **Abbau des Arbeitsplatzes** (Pane `w3:p6`, Worktree, Branch — pruefbar an `git worktree list`, `git branch --list "feature/*"`, `herdr agent list`), gefolgt von `/dtb:archive` fuer das abgenommene `pane-start`. Der Review-Zweitlauf `/dtb:impl-review capture-duplikat-schutz` gilt, solange `features/capture-duplikat-schutz/review.md` das Verdikt des Erstlaufs traegt.
