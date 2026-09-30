# Discovery: Rueckfragen-Defaults (Station 2 der Autonomie-Achse)
<!-- resume: done -->

**Erstellt:** 2026-09-30
**Idee-Referenz:** Inbox #57 — "Die Voll-Schiene nach Rueckfragen durchsuchen, die faktisch immer gleich beantwortet werden — und diese automatisieren."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-feature-discover/SKILL.md | Z1 Slug mit Veto (Schritt 5) · Z14 Scan-Bestaetigung mit Veto (Schritt 2) |
| skills/dtb-feature-fast/SKILL.md | Z1 Slug ableiten (Schritt 3) · Z3 BACKLOG ohne Frage (Schritt 5.7) |
| skills/dtb-task/SKILL.md | Z2 Backlog-Frage (Schritt 5) → Default Ja, Testordner-Ausnahme |
| skills/dtb-feature-plan/SKILL.md | Z3 Backlog-Frage (Aufgabe 4, Schritt 10) → Default Ja, Testordner-Ausnahme |
| skills/dtb-bug-report/SKILL.md | Z2/Z3 analog (Zusatz 2026-09-30): Backlog-Frage (Schritt 5) → Default Ja, Testordner-Ausnahme |
| skills/dtb-plan-review/SKILL.md | Z7 „Anpassungen? (Ja/Nein)" (Schritt 5) → bei REVISE/REJECTED direkt in die Finding-Runde |
| skills/dtb-implement/SKILL.md | Z9 Staging (4.3) · Z10 Commit-Message (4.6) · Z11 Naechste Phase (4.11) · Z8 Form des Manual-Gates (Freitext → Auswahl) |
| skills/dtb-impl-review/SKILL.md | Z13 Triage (Schritt 9) → Sammelvorlage fuer non-blocking, blocking einzeln |
| skills/dtb-impl-plan/SKILL.md | Z14 Scan-Bestaetigung 2b · Z16 Lektion-Kandidat (Rueckfrage entfaellt, Vormerk-Zeile) |
| skills/dtb-debug-plan/SKILL.md | Z16 Lektion-Kandidat (Rueckfrage entfaellt, Vormerk-Zeile) |
| skills/dtb-feature-start/SKILL.md | Z15 „Bereit? Sage ‚Los'" entfaellt → direkt `/dtb:implement` |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §4 Slug-Ableitung — moeglicher Ort der allgemeinen Namensregel (Kandidat) |
| skills/CLAUDE.md | moeglicher Ort einer kanonischen Veto-Default-Form (Kandidat) |
| CLAUDE.md | Skill-Kurzbeschreibungen bei spuerbarer Verhaltensaenderung (Kandidat) |

Quelle (nur lesend): `dtb-project/project-workflows/features/rueckfragen-erhebung/erhebung.md` → „## Festlegung 2026-09-22 (verbindlich)".

---

## Anforderungen

### Scope
**Enthalten:**
- Umsetzung der 11 skill-wirksamen Zeilen der Festlegung 2026-09-22 (Z1, 2, 3, 7, 9, 10, 11, 13, 14, 15, 16) plus Form-Auflage (Veto-Default sichtbar, eindeutiges „weiter")
- **Backlog (Z2/Z3 + Zusatz):** Feature (`feature-plan`/`feature-fast`), Aufgabe (`task`) und Bug (`bug-report`) werden ohne Frage eingetragen; Ausnahme Ordner-Praefix `zz-test-*`/`abnahmeprobe-*`. Eine Anzeige-Zeile meldet, was eingetragen wurde (`→ in BACKLOG.md eingetragen (Status: …)` bzw. `→ kein BACKLOG-Eintrag (Testordner)`). Worktree-Teil-Guard bleibt unveraendert (Eintrag in den Hand-off). Ideen kommen nie ins Backlog (bleiben in INBOX.md)
- **impl-review-Triage (Z13):** non-blocking Findings in EINER Sammelvorlage, jedes auf Fix vorbelegt; ein „weiter" uebernimmt alle, Skip per Zeile; blocking Findings weiterhin einzeln. Kein stiller Hintergrund-Fix (Code-Aenderung bleibt sichtbar; Datenlage: 10 von 158 Findings nicht uebernommen)
- **Namensregel (Z1), allgemein gefasst:** „Liefert das Feature etwas mit festem Namen, uebernimmt der Slug diesen Namen" (statt kit-spezifisch „Kit-Skill → englischer Skill-Name")
- **Manual-Gate (Z8):** bleibt beim Menschen, je Phase; Form wird von Freitext auf blockierende Auswahl (passt / Korrekturen) umgestellt (Lehre 2026-07-30)
- **Lektion-Kandidat (Z16):** Rueckfrage in impl-plan/debug-plan entfaellt; der Skill merkt den Kandidaten mit einer Zeile vor, der Checkpoint erfasst ihn (seit 2026-09-08)

**Nicht enthalten:**
- Arbeiten ganz ohne Menschen, Antwortgeber, Frontmatter-Entsperrung, Autopilot (#98)
- Konfidenz-Mechanik / Anbieterwahl (#99)
- Pane-/Worktree-Stand-Nachfrage (Z4, wird nicht gebaut); Entscheidung ueber #97 (gehoert in `/dtb:idea-review`)
- Aenderungen an den 5 Zeilen „nie automatisch" (Z5, Z6, Z8-Inhalt, Z12, Ueberschreib-Fragen) und an der feature-fast-Sammelvorlage (Z17)

### Gewuenschtes Verhalten
- **Eine einheitliche Veto-Form, einmal zentral beschrieben**, zwei Varianten:
  - **Einzel-Vorschlag** (Slug, Commit-Message, Staging, Scan-Liste): Vorschlag anzeigen, „weiter" uebernimmt, Freitext korrigiert
  - **Sammelliste** (impl-review non-blocking): alle Eintraege vorbelegt, „weiter" uebernimmt alle, Nummern nennen streicht einzelne
- **Bedienform nach Folge:** Knopf (blockierende Auswahl, AskUserQuestion) bei allem, was zu einem Commit fuehrt — Commit-Message, Staging, impl-review-Korrekturen; Textzeile bei Kleinem ohne Commit-Folge — Slug, Scan-Liste
- **Vorbild:** feature-fast-Sammelvorlage (Ok / Korrekturen), 5 Laeufe ohne Befund
- Stiller Default ohne Rueckfrage (nur Anzeige-Zeile): Backlog-Eintrag, Lektion-Vormerkung, Wegfall „Bereit? Los", Direkteinstieg in die Finding-Runde bei REVISE/REJECTED

### Randfaelle
- **BACKLOG.md fehlt/unlesbar:** eine Warnzeile, Lauf geht weiter (Fehlen meldet `backlog-status` ohnehin)
- **Slug-Kollision:** kein Veto-Default — echte Rueckfrage nach anderem Namen wie heute (§4: kein Auto-Suffix)
- **impl-review-Sammelliste:** nur blocking Findings → Liste entfaellt; viele non-blocking (≥20) → trotzdem EINE Liste, nach Datei gruppiert
- **Naechste Phase (Z11):** Default „direkt weiter"; die Schwelle „Kontext knapp" ist Einschaetzung des Skills, nicht Messung → der Skill meldet es von sich aus und bietet den Wiedereinstieg (2) an, oder der Nutzer sagt „Stopp"
- **feature-start bei Bugs/Aufgaben** (keine `plan.md`): „Bereit? Los" entfaellt ebenfalls; der Skill bietet direkt den Einstiegsbefehl an (Erweiterung von Z15 ueber den plan.md-Fall hinaus)
- Kein bekannter Fall, in dem ein Default sicher falsch waere (Nutzer 2026-09-30)

### Einschraenkungen
- **Wirkung erst nach `/dtb:kit-sync`:** laufende Sessions nutzen die installierten Kopien unter `~/.claude/`; bis zum Sync fragen die Skills wie bisher
- **Querverweise mitziehen:** `impl-plan` 2b uebernimmt die Scan-Form aus `feature-discover` Schritt 2 („Stimmt das so?"); `feature-fast` Schritt 5.7 verweist auf „feature-plan Schritt 10"; `feature-fast` prueft den Anker `## Schritt 6` in `feature-discover`. Schritt-Ueberschriften bleiben stabil, nur Inhalte aendern sich
- **Worktree-Teil-Guards unveraendert** — zentrale Dateien (BACKLOG, INBOX) werden im Worktree weiterhin nicht beschrieben
- **`disable-model-invocation` bleibt** — Frontmatter-Entsperrung ist #98
- **Arbeitsweise:** Entscheidungspunkte werden nur noch dort einzeln durchgegangen, wo die Festlegung „nie automatisch" sagt, plus bei blocking Findings
- **Festlegung 2026-09-22 ist verbindliche Vorgabe:** Ergaenzungen dieser Discovery (Bug-Backlog, allgemeine Namensregel, Auswahl-Form des Manual-Gates, Lektion-Frage entfaellt, feature-start bei Bugs/Aufgaben) werden in der Spec ausdruecklich als Zusatz markiert

### Integrationspunkte
- **`no-loss-check` / `workflow-checkpoint`:** uebernehmen die Lektion-Kandidaten, deren Rueckfrage in impl-plan/debug-plan entfaellt. Die Vormerk-Zeile braucht eine feste, erkennbare Form, z.B. `💡 Lektion-Kandidat vorgemerkt: „…" → wird beim Checkpoint erfasst`
- **`backlog-status`:** Sicherheitsnetz — meldet fehlende BACKLOG-Zeilen, falls ein automatischer Eintrag ausfaellt
- **`worker` / `pane-start`:** nicht betroffen (schreiben selbst nicht ins BACKLOG, Startbefehle bleiben gueltig)
- **#98 (Station 3):** baut auf den Veto-Defaults auf — die Form bleibt so gewaehlt, dass ein spaeterer Antwortgeber sie bestaetigen koennte
- **Externe Abhaengigkeiten:** keine (reine Markdown-Aenderungen)

---

## Abhaengigkeiten

- **Quelle:** `features/rueckfragen-erhebung/` (Aufgabe, Abgenommen) — `erhebung.md` bleibt bis nach Station 2 unter diesem Pfad, danach `/dtb:archive rueckfragen-erhebung`
- **Ueberschneidung INBOX #107** (BACKLOG-Spalte „#"): aendert dieselben vier BACKLOG-Schreibstellen (`task`, `bug-report`, `feature-plan`, `feature-fast`). Bewusst NICHT eingebaut (Scope); Koordination als offener Punkt
- **#98 / #99:** spaetere Stationen der Autonomie-Achse, bewusst ausgegrenzt; #98 baut auf den Veto-Defaults auf
- Keine Konflikte mit anderen Change-Ordnern

---

## Offene Punkte

- **#107-Koordination:** Wer zuerst fertig ist, dessen BACKLOG-Zeilenvorlage uebernimmt der andere — beim Merge pruefen
- **Ort der kanonischen Veto-Form:** zentral in `skills/CLAUDE.md` mit Verweis aus den Skills (Muster Worktree-Guard) oder je Skill ausformuliert — in `impl-plan` entscheiden
- **Ort der Namensregel:** `DERIVED_STATE_RULES.md` §4 wird an alle Projekte verteilt — passt die allgemein gefasste Regel dort hinein, oder gehoert sie nur in `feature-discover`/`feature-fast` Schritt 5/3?
- **Z11-Formulierung:** wie der Skill „Kontext wird knapp" einschaetzt und meldet, ohne es messen zu koennen — konkrete Formel in `impl-plan` festlegen
- **Zusaetze gegenueber der Festlegung 2026-09-22** in der Spec als solche markieren: Bug-Backlog, allgemeine Namensregel, Auswahl-Form des Manual-Gates, Lektion-Frage entfaellt, feature-start bei Bugs/Aufgaben

---

**Erstellt mit:** `/dtb:feature-discover`
