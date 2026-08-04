# Review-Snapshot: plan-status-feld

Scope: 9 inhaltliche Dateien (DERIVED_STATE_RULES.md, skills/CLAUDE.md, dtb-{impl-plan,
plan-review,workflow-next,workflow-status,backlog-status,project-health}/SKILL.md, INBOX.md)
aus 5 Commits (`bdb412e`, `4dd8671`, `789495f`, `bf87fd2` aus `## Progress` + Triage-Commit
`8f3c3da`) · Geprueft bis: `8f3c3da` · Datum: 2026-07-31
Gesamt-Verdikt: REJECTED (1 blocking) — **Stand des Reviews**, nicht des Artefakts
Triage abgeschlossen 2026-07-31: **10 Fixed · 0 Lesson · 0 Skipped · 0 PENDING** — der Blocker
ist behoben. Die Fixes liegen im Working Tree (noch nicht committet); ein frisches Review nach
dem Commit wuerde das Verdikt neu vergeben.

> **Vorlauf:** Dieser Snapshot ersetzt den Lauf vom 2026-07-30 (Verdikt REJECTED, 2 Blocker,
> Triage 8 Fixed · 2 Skipped). Jener Stand ist in Commit `8f3c3da` und im Session-Log
> `2026-07/2026-07-30.md` (Session 2) dokumentiert. **Beide Alt-Blocker sind verifiziert
> behoben:** Parse-Regel steht in `DERIVED_STATE_RULES.md:292`; die Klausel „ohne je gelaufenes
> Review" kommt in `workflow-next` 0-mal vor (auch an der installierten Kopie gegengeprueft).
> Die Findings unten sind neu.

## Verdikt-Achsen

| Achse | Verdikt | Findings |
|-------|---------|----------|
| Plan Adherence | WARNING | 2 |
| Scope Discipline | WARNING | 1 |
| Safety & Quality | WARNING | 2 |
| Architecture | FAIL | 1 |
| Pattern Consistency | WARNING | 2 |
| Rules | WARNING | 2 |

Drift-Bilanz: 10/12 Schritte MATCH, 2 DRIFT (2.3, 3.4), 0 MISSING.
Rules-Basis: `STYLE.md` ist ein HTML/CSS-Diagramm-Guide und auf Markdown-Skills nicht
anwendbar — massgeblich war `skills/CLAUDE.md`.

## Findings

### F1 — Architecture — [S:Hoch × I:Hoch] — Craft/torvalds — blocking
`skills/dtb-plan-review/SKILL.md:332-334` — Der Output-Block (Z. 247-335) enthaelt in derselben
Fence zuerst die Schritt-5-Frage „Moechtest du Anpassungen … (Ja/Nein)" und direkt darunter
`📝 Kopf-Statusfeld → [neuer Wert aus Schritt 6.1]`. Der Wert haengt laut Z. 337 aber genau an
der Antwort auf diese Frage. Wer das Template ausfuehrt, gibt beides gleichzeitig aus — muss den
Feldwert also bestimmen (und nach 6.2 schreiben), bevor feststeht, ob die WARNs eingearbeitet
werden. Damit ist im REVISE-Pfad die harte binaere „behoben"-Bedingung ausgehebelt, die der Plan
(Z. 106-111) mit dem asymmetrischen Risiko begruendet: ein zu frueh gesetztes `Reviewed`
schaltet `feature-start` frei. Schritt 5 ist nur ein Einzeiler; keine andere Stelle rettet die
Reihenfolge.
Fix: `📝`-Zeile aus dem Output-Fence herausnehmen und in 6.3 als nachgelagerte, separate Ausgabe
deklarieren („nach abgeschlossener Anpassungs-Runde ausgeben, nicht Teil des Report-Blocks").
Decision: FIXED (2026-07-31 — 📝-Zeile aus dem Output-Fence entfernt, Begruendung dort umgedreht;
6.3 macht die Reihenfolge verbindlich)

### F2 — Pattern Consistency — [S:Hoch × I:Mittel] — Craft/principled + Drift (konvergent)
`skills/dtb-workflow-status/SKILL.md:131-134`, `skills/dtb-workflow-next/SKILL.md:105-109` —
Der Triage-Fix F4 hat den „Vorrang der Still-Regel" nur in den Kanon geschrieben
(`DERIVED_STATE_RULES.md:356-360`), nicht in die beiden Spiegel — obwohl der Wartungs-Hinweis
direkt darueber („Aenderung hier → beide Skills mitziehen") genau das fordert. Der Fix hat seine
eigene Kopplungsregel verletzt. Folge in Bestandsprojekten ohne aktuellen Kanon-Seed: der
haeufigste Altbestand (Plan ohne Kopffeld, Umsetzung laeuft) wird als `Entwurf` toleriert und
feuert eine ⚠-Zeile mit leerem `{Wert}`.
Fix: §7.3-Still-Vorrang-Satz woertlich in `workflow-status` Schritt 6 und `workflow-next`
Schritt 3 spiegeln (gleiche Kopie-mit-Wartungshinweis-Mechanik wie bei der Toleranz-Matrix).
Decision: FIXED (2026-07-31 — Still-Vorrang + Praedikat aus F3 in beide Spiegel uebernommen)

### F3 — Safety & Quality — [S:Mittel × I:Mittel] — Craft/principled
`dtb-project/project-rules/DERIVED_STATE_RULES.md:353` — Der Kanon schreibt die ⚠-Zeile vor,
definiert aber ihr Praedikat nicht („Widerspricht das Feld dem `## Progress`-Stand"). Nur
`workflow-next:106` benennt es („`Entwurf` trotz abgehakter Schritte"); `workflow-status` nennt
nichts. Woertlich gelesen waeren `Reviewed` + 7/12 oder der tolerierte Altwert `Abgeschlossen`
+ 3/12 ein Widerspruch — nach §7.4 (status-neutral) sind sie keiner.
Fix: In §7.3 explizit: „Konflikt = physisch vorhandenes Feld, das als `Entwurf` gilt, UND ≥1
abgehakte `## Progress`-Checkbox. Jede andere Kombination ist kein Konflikt."
Decision: FIXED (2026-07-31 — Praedikat in §7.3 ergaenzt, inkl. `Reviewed`/Altwert-Ausschluss)

### F4 — Plan Adherence — [S:Mittel × I:Mittel] — Drift (im Hauptkontext verifiziert)
`features/plan-status-feld/plan.md:196` gegen `skills/dtb-workflow-status/SKILL.md:55` — Das
Automated-Checkpoint-Kriterium `grep -c "In Umsetzung" skills/dtb-workflow-status/SKILL.md` = 0
ist rot: nachgezaehlt 1 Treffer (Z. 55, Altwert-Nennung in der Toleranz-Matrix, die derselbe
Schritt 3.2 fordert). Checkbox 3.2 wurde gegen ein rotes Kriterium geflippt (§2 Regel 3). Die
Umsetzung ist richtig, das Kriterium ist falsch — Muster von Lektion L8, die in derselben
Session erfasst wurde.
Fix: Kriterium auf die Wirkstelle ankern (Treffer nur in der Toleranz-Matrix-Zeile, nicht in der
Gate-Definition), mit Kurzvermerk, warum die Nennung dort noetig ist.
Decision: FIXED (2026-07-31 — Kriterium in plan.md:196 auf die Wirkstelle geankert, L8-Vermerk)

### F5 — Plan Adherence — [S:Mittel × I:Mittel] — Drift
`skills/dtb-plan-review/SKILL.md` (Schritt 2.3) — Der Report-Ausweis ist umgesetzt, der geplante
repo-weite Konsistenz-Sweep aber nirgends belegt und war nachweislich unvollstaendig: die beiden
echten Querbezuege (`project-health`, `backlog-status`) fielen erst dem nachgelagerten
impl-review auf. Genau das war die Aufgabe des Sweeps (2.3 verweist auf Lektion L3).
Fix: Sweep nachholen und Ergebnis im Plan unter 2.3 nachtragen (auch „0 weitere Befunde" ist ein
Nachweis).
Decision: FIXED (2026-07-31 — Sweep nachgeholt: 4 legitime Nennungen, 7 referenzierende Dateien,
0 neue Befunde; Nachweis-Block unter 2.3 im plan.md)

### F6 — Rules — [S:Mittel × I:Mittel] — Rules-Agent (vorbestehend, Datei in 1.3 offen)
`skills/CLAUDE.md:16-17,36-37` — Die Autoring-Konvention dokumentiert `after`/`next` als
`string/null`, real verwenden alle Kit-Skills Listen — und `skills/dtb-project-health/SKILL.md:201`
lintet ausdruecklich auf Listen. Ein streng nach dem Guide geschriebener neuer Skill faellt im
eigenen Health-Check durch.
Fix: Z. 16-17 und 36-37 auf Listen umstellen (`after: [dtb:<predecessor>]`, Typ `list/null`).
Decision: FIXED (2026-07-31 — Beispiel und Feldtabelle auf Listen, Lint-Hinweis ergaenzt)

### F7 — Pattern Consistency — [S:Mittel × I:Niedrig] — Craft/principled
`skills/dtb-workflow-status/SKILL.md:33` — Die Praeambel sagt pauschal „Statusfelder (BACKLOG.md,
`**Status:**`-Zeilen) dienen nur der Konflikterkennung". Nach der Haertung leiten Z. 49-51 daraus
die Stufe ab und Z. 93 macht das Feld zum Gate-Kriterium „Plan-Review" — zwei widersprechende
Anweisungen im selben Skill. `workflow-next:34` ist sauber auf BACKLOG eingegrenzt.
Fix: Z. 33 auf „Statusfelder in BACKLOG.md und `spec.md`/`task.md`" eingrenzen und den
Kopffeld-Sonderfall (§7.4) in einem Halbsatz ausnehmen.
Decision: FIXED (2026-07-31 — Z. 33 eingegrenzt, Kopffeld als Gate-Quelle ausgenommen)

### F8 — Rules — [S:Mittel × I:Niedrig] — Rules-Agent (vorbestehend, Nachbarzeile geaendert)
`skills/dtb-workflow-status/SKILL.md:172` — Die Gate-Definition (Z. 94) nennt das fuenfte Gate
„Verifikation", die Output-Tabelle nennt die Spalte „Build". Der Skill produziert einen Report
mit einer Spalte, die in keiner Gate-Definition existiert.
Fix: Spaltenueberschrift auf „Verifikation" ziehen.
Decision: FIXED (2026-07-31)

### F9 — Safety & Quality — [S:Niedrig × I:Mittel] — Craft/torvalds
`skills/dtb-plan-review/SKILL.md:227-229` — Die Einfuegeregel kennt ihr eigenes Definitionsfenster
nicht. Bei einem Kopfblock mit >9 Zeilen landet die eingefuegte Zeile ausserhalb der ersten 10,
ist damit kein Kopf-Statusfeld, und der naechste Lauf fuegt eine zweite ein — aus Selbstheilung
wird ein Akkumulator.
Fix: Punkt 2 ergaenzen: „Die eingefuegte Zeile muss innerhalb der ersten 10 Zeilen liegen; laege
die Kopfposition darunter, direkt nach der Titelzeile einfuegen."
Decision: FIXED (2026-07-31 — Fenster-Grenze als verbindlicher Zusatz in 6.2 Punkt 2)

### F10 — Scope Discipline — [S:Niedrig × I:Mittel] — Drift
`features/plan-status-feld/spec.md` — Die Spec fuehrt „Aenderungen an `dtb:backlog-status`" unter
*Nicht enthalten*, die Plan-Ist-Analyse (Z. 34) nennt die Datei „Nicht-Scope". Die Triage hat sie
trotzdem geaendert (F6) — inhaltlich richtig, aber die Spec widerspricht dem ausgelieferten
Stand. Schwaecher gilt dasselbe fuer `project-health` (ungeplant, notwendige Folge von §7.4).
Fix: Spec-Abschnitt *Nicht enthalten* nachziehen; beide Dateien mit Begruendung als nachtraeglich
in Scope genommen vermerken.
Decision: FIXED (2026-07-31 — spec.md „Nicht enthalten" nachgezogen, beide Dateien mit
Begruendung als nachtraeglich in Scope vermerkt)

## Unterhalb des Caps (8, nicht einzeln triagiert)

- Smoke-Test 3.4: Erwartung (1) wurde umgedeutet statt erfuellt, Checkbox trotzdem geflippt
- `skills/dtb-backlog-status/SKILL.md:64` — `{DD.MM.YYYY}` verletzt die `YYYY-MM-DD`-Regel
  (gleiche Abweichung in `dtb-build-check:62` und `dtb-repo-sync:60`, dort nicht im Scope)
- `skills/dtb-project-health/SKILL.md:206` — Lint prueft `Write`/`Bash` gegen `allowed-tools`,
  aber nicht `Edit`, obwohl dieser Change `plan-review` zum Edit-Schreiber macht
- Kanon §7.1 sagt „die `**Status:**`-Zeile" (Singular, kein Tiebreak), `plan-review:223`
  praezisiert eigenmaechtig auf „die erste"
- `skills/dtb-workflow-status/SKILL.md:56` nennt den Hinweis-Wortlaut „unbekannter Statuswert {X}"
  nicht woertlich (Kanon und `workflow-next:45` tun es)
- `plan-review` 6.2 Punkt 4 laesst offen, was beim Normalfall `Entwurf`→`Reviewed` mit
  bestehenden Annotationen (Klammer-Vermerk, HTML-Kommentar) passiert
- `skills/dtb-workflow-next/SKILL.md:138` nutzt `✓` in beiden Zweigen, wo der Block sonst `○`
  fuer „offen" fuehrt
- Plan-Entscheidungstabelle traegt „§-Verortung Kanon → Offen", obwohl §7 entschieden ist

## Info

7 Workflow-Artefakte im Diff, bekannt — nicht bewertet.
Kontrakt-Gegenprobe (20 Bestands-`plan.md`-Koepfe, alle `**Status:**`-Schreiber im Repo):
kein Bruch — alle Bestandswerte von §7.1/§7.3 abgedeckt, `workflow-checkpoint` ist kein
zweiter Schreiber.
