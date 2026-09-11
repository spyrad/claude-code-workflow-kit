# Review-Snapshot: feature-fast
Scope: skills/dtb-feature-fast + 4 Weichen-/Quell-Skills + CLAUDE.md + meeting-agenda/{discovery,spec,plan}.md · Geprueft bis: `8c095a0` · Datum: 2026-08-02
Gesamt-Verdikt: REJECTED (2 blocking; Plan Adherence + Scope Discipline PASS, Rules uebersprungen) — Stand des Review-Laufs vom 2026-08-02
Triage 2026-08-02: 10 Fixed · 0 Skipped · 0 Lesson (alle Decisions unten; Commit der Fixes folgt regulaer via commit-and-push/Checkpoint)

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] (principled/blocking)
skills/dtb-feature-fast/SKILL.md:12 vs. :200 — allowed-tools (Read, Write, Glob, Grep) kann keine Datei loeschen; Schritt 5.5 und Wiederaufnahme-Option 2 verlangen Loeschen von fast-draft.md.
Fix: Bash in allowed-tools aufnehmen, Loesch-Schritte als explizites rm-Kommando fassen.
Decision: FIXED

### F2 — Safety & Quality — [S:Hoch × I:Hoch] (principled/blocking)
skills/dtb-idea-review/SKILL.md:88, 98-105 — Task-Lane der Dreier-Weiche setzt Idee auf "In Arbeit", dtb:task hat aber keine INBOX-Integration → Eintrag bleibt dauerhaft "In Arbeit" und wird von argumentlosen feature-fast-/feature-discover-Laeufen automatisch geladen (Beleg: #28 steht aktuell genau so).
Fix: Task-Lane setzt bei Bestaetigung direkt "Ausgearbeitet" + Link → features/{slug}/task.md (Task-Erfassung ist einschrittig).
Decision: FIXED (idea-review Task-Lane auf Ausgearbeitet+Vermerk; dtb:task Schritt 4b INBOX-Rueckverlinkung neu; #28 korrigiert)

### F3 — Pattern Consistency — [S:Mittel × I:Mittel] (principled)
skills/dtb-feature-fast/SKILL.md:18 — produces verschweigt INBOX.md und BACKLOG.md, die der Skill schreibt (Geschwister feature-plan/feature-discover deklarieren sie).
Fix: produces um INBOX.md, BACKLOG.md ergaenzen.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Mittel] (principled)
Kanten-Asymmetrie im Changeset: feature-discover.next ohne dtb:feature-fast (trotz Kleinfall-Weiche), feature-fast.after ohne dtb:feature-discover, dtb-task.after null (trotz Weiche aus idea-review).
Fix: die drei Frontmatter-Listen symmetrisch nachziehen.
Decision: FIXED

### F5 — Pattern Consistency — [S:Mittel × I:Mittel] (principled)
skills/dtb-feature-fast/SKILL.md:47-57 vs. skills/CLAUDE.md Hard-Gate-Tabelle — INBOX-Gate ist nicht registriert; Abweichung (keine Escape-Hatch) unbegruendet in der Konvention.
Fix: Zeile in die Hard-Gate-Zuordnung aufnehmen, Escape-Hatch-Abweichung dort begruenden.
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Mittel] (principled)
skills/dtb-feature-fast/SKILL.md Schritt 3 — Lessons-Prior fehlt: die Voll-Schiene (impl-plan) liest lessons.md verbindlich vor der Planerstellung, feature-fast ersetzt die Planerstellung ohne diesen Pflicht-Input.
Fix: Lessons-Block analog impl-plan als Schritt 3.0 + project-rules/lessons.md in consumes.
Decision: FIXED (Block nach Schritt 0, Filter feature-fast/impl-plan/alle)

### F7 — Architecture — [S:Mittel × I:Mittel] (torvalds)
skills/dtb-feature-fast/SKILL.md:78-94 — Struktur-Check meldet bei FEHLENDER Datei faelschlich "Template-Quelle strukturell geaendert"; kein Repo-/Projekt-Fallback (plan-review Schritt 2 hat das Muster: global zuerst, Fallback, kit-sync-Hinweis).
Fix: zwei Fehlerpfade trennen (Datei fehlt → /dtb:kit-sync-Hinweis | Anker fehlt → Drift-Warnung) + Fallback ergaenzen.
Decision: FIXED

### F8 — Architecture — [S:Mittel × I:Mittel] (torvalds)
fast-draft.md ist dem Derived-State-Kanon unbekannt — Change-Ordner NUR mit fast-draft.md (Abbruch-Fall) trifft keine Ableitungszeile; review.md wurde fuer denselben Fall explizit als status-neutral registriert.
Fix: status-neutrale Tabellenzeile in DERIVED_STATE_RULES.md analog review.md + Dateiliste im Root-CLAUDE.md-Change-Folder-Absatz mitziehen (Achtung: Seed-Skew #22).
Decision: FIXED (inkl. Skew-Vermerk in der Fusszeile — fuenfter #22-Fall)

### F9 — Architecture — [S:Niedrig × I:Niedrig] (torvalds/nit)
dtb-project/project-workflows/features/meeting-agenda/plan.md:94-97 — technische Entscheidungen referenzieren A-IDs (A3/A4/A5/A7) aus der geloeschten fast-draft.md — Belege zeigen ins Leere.
Fix: Skill-Regel in Schritt 5: Begruendung ausschreiben ("per Veto bestaetigt {Datum}") statt A-ID; meeting-agenda/plan.md entsprechend anpassen.
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig × I:Niedrig] (principled/nit)
Provenienz-Fusszeile "Erstellt mit: /dtb:feature-fast (…)" in den E2E-Artefakten ist vom Skill nicht angewiesen und widerspricht formal der Ununterscheidbarkeits-Klausel (Z. 220-221).
Fix: Fusszeilen-Format in Schritt 5 definieren; Klausel praezisieren ("fuer nachgelagerte Kette und Statusableitung").
Decision: FIXED
