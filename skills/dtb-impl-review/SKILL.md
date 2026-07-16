---
name: dtb:impl-review
description: >-
  Use when: "Impl Review", "Implementierung reviewen", "Feature-End-Review",
  "Umsetzung pruefen", "Plan-Drift pruefen", "Code gegen Plan pruefen".
  Reviews an implemented feature across three dimensions (plan drift, craft, rules)
  after dtb:implement, produces features/<slug>/review.md with an interactive triage.
disable-model-invocation: true
argument-hint: "[Feature-Name oder Slug] [phase N]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
pipeline:
  stage: development
  after: [dtb:implement]
  next: [dtb:workflow-checkpoint]
  consumes: [features/*/plan.md, features/*/spec.md, project-rules/*.md, project-rules/lessons.md, workflow.config.yaml]
  produces: [features/*/review.md]
---

# DTB Impl-Review

Du reviewst ein **umgesetztes Feature** entlang drei Dimensionen — **Plan-Drift** (mechanischer
Plan↔Code-Abgleich), **Craft** (Handwerks-Urteil aus zwei destillierten Reviewer-Linsen) und
**Rules** (Abgleich gegen Projekt-Richtlinien). Ergebnis ist ein Report mit sechs Verdikt-Achsen,
persistiert als `features/{slug}/review.md`, mit interaktiver Triage pro Finding.

Anders als das abgeloeste `code-review` prueft dieser Skill nicht nur Rules, sondern auch ob der
Code dem **Plan** folgt und ob er **handwerklich** traegt. Er fuehrt **keine** Verifikations-Laeufe
aus — Success Criteria gehoeren dem Verifikations-Gate in `dtb:implement`. Er ist read-only, ausser
bei explizit gewaehlten Triage-Fixes.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/` und
`dtb-project/project-rules/` fuer die Rules.

## Schritt 1: Eingangs-Gates

### 1a. Slug aufloesen

Ermittle den Slug aus dem Argument oder Chat-Kontext (Regeln:
`{config.paths.rules}/DERIVED_STATE_RULES.md` §4). Unklar → Feature-Namen erfragen,
DANN pruefen (nicht raten). Optionales zweites Argument `phase N` merken (Notausgang fuer
lange Plaene — nie automatisch anwenden).

### 1b. Archiv-Weigerung (hart, keine Escape-Hatch)

Existiert `{config.paths.workflows}/archive/{slug}/` (und kein aktiver Ordner
`features/{slug}/`) → harte Weigerung, KEINE Escape-Hatch:

```
⛔ Dieser Change ist archiviert (archive/{slug}/).
   Archivierte Umsetzungen werden nicht nachtraeglich reviewt — falls Nacharbeit noetig,
   starte einen neuen Change (/dtb:idea oder /dtb:feature-discover).
```

### 1c. Eligibility-Hard-Gate (kritisches Artefakt: `plan.md`)

Pruefe, ob das **kritische Artefakt** `{config.paths.workflows}/features/{slug}/plan.md`
existiert (Glob, slug-spezifisch — **nicht** der `*`-Wildcard). Fehlt es → Meldeblock ausgeben
und NICHT weiterarbeiten, bis der Nutzer die Escape-Hatch bestaetigt:

```
⛔ impl-review braucht einen Implementierungsplan als Review-Grundlage, der fehlt.
   Geprueft: features/{slug}/plan.md — nicht gefunden.
   → Erstelle ihn zuerst: /dtb:impl-plan {Feature-Name}   (erzeugt von impl-plan)

   Fehlalarm (plan.md existiert doch) oder bewusst ohne fortfahren? „trotzdem fortfahren" bestaetigen.
```

Bei Bestaetigung: normal fortfahren. Sonst: hier stoppen (kein Review ohne Plan).

## Schritt 2: Scope-Aufloesung + Diff-Scope aus Progress-SHAs

Der Review-Gegenstand wird **exakt aus den Commit-SHAs** der `## Progress`-Sektion bestimmt —
keine Datums-Heuristik.

1. **Plan + Spec laden:** `features/{slug}/plan.md` vollstaendig, `features/{slug}/spec.md`
   (falls vorhanden) als Kontext. Wurde `phase N` uebergeben → nur die Schritte dieser Phase
   in den Scope nehmen.
2. **SHAs sammeln:** Alle Inline-Code-SHAs aus geflippten `## Progress`-Zeilen extrahieren
   (Format `` `a1b2c3d` `` bzw. Multi-Repo `` `repo-name@a1b2c3d` `` — §2 Regel 4+5).
   Deduplizieren (gebuendelte Commits belegen mehrere Zeilen). Repo-Praefixe aufloesen →
   Zuordnung SHA → Repo aus `config.repos`.
3. **Commit-Menge → Dateiliste:** Pro Repo die Commit-Menge in eine geaenderte Dateiliste
   uebersetzen — `git -C {repo.path} show --stat --name-only {SHA}` je Commit bzw.
   `git -C {repo.path} diff --name-only {erster}~1 {letzter}` bei zusammenhaengender Kette.
   Die Dateiliste (nicht die Dateiinhalte) ist der Kontext der Sub-Agents.
4. **Randfaelle — ehrlich melden, nie raten:**
   - `## Progress` fehlt oder hat 0 Checkbox-Zeilen → melden + Nachruestung anbieten
     (`/dtb:impl-plan` aktualisieren); kein Review-Scope ableitbar → stoppen und Scope erfragen.
   - Geflippte Zeile **ohne** SHA ausserhalb der Leer-Diff-Ausnahme (§2 Regel 4) →
     als **Scope-Luecke** vormerken (wird Dimension-1-Finding „Gate nicht durchlaufen?", Detail
     in Schritt 4). Den restlichen Scope trotzdem bilden.
   - Keine einzige SHA ermittelbar (Feature ganz ohne Commit-Beleg) → ehrlich melden, Scope
     erfragen — **nie** eine Datums-/Branch-Heuristik erfinden.
5. **Workflow-Artefakt-Ausnahme:** Aenderungen an Workflow-Artefakten sind erwartete
   Pipeline-Nebenprodukte und werden aus dem **Drift-Vergleich ausgenommen** — nie als
   DRIFT/EXTRA gewertet. Betroffen:
   `features/{slug}/plan.md` (die SHA-Rueckschreibung landet systematisch im Folge-/Checkpoint-Commit),
   `features/{slug}/review.md`, `WORKFLOW_STATUS.md`, `BACKLOG.md`, `INBOX.md`,
   `project-changelog/**`. Im Report erscheinen sie als **genau eine** Info-Zeile:
   `{N} Workflow-Artefakte im Diff, bekannt — nicht bewertet`.

## Schritt 3: Lektionen als Prior (mit Legacy-Alias)

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen
  Schritt **still ueberspringen** (kein Abbruch).
- Sonst: filtere Eintraege, deren `Applies-to` einen dieser Werte enthaelt:
  - `impl-review` (der neue, kanonische Wert)
  - `code-review` — **Legacy-Alias**: nur auf der **Lese-Seite** akzeptiert, damit bestehende
    Lektionen ohne Datenmigration sofort weiterwirken. `dtb:lesson` vergibt diesen Wert nicht neu.
  - `alle`
- Wende die passenden `Rule`-Aussagen beim Review still an.
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`.
- **Konflikt** (zwei nach dem Filter behaltene Lektionen mit gegensaetzlicher `Rule`):
  beide zeigen und den Widerspruch melden — **nicht** selbst aufloesen.

## Schritt 4: Sub-Agent 1 — Drift (mechanisch)

Der Drift-Agent gleicht **Plan gegen Code** ab — ohne Geschmacksurteil. Er bewertet den
Code-Stand, **nicht** Testergebnisse.

**SHA-Vollstaendigkeits-Check (laeuft im Hauptkontext, VOR dem Agent):** Jede geflippte
`## Progress`-Zeile ohne SHA ausserhalb der Leer-Diff-Ausnahme (§2 Regel 4) ist ein Verdacht
„Gate nicht durchlaufen?". Ergebnis wird ein **Dimension-1-Finding** (Achse Plan Adherence) —
nicht an den Agent delegiert.

Dispatch **einen** Sub-Agent (Typ `general-purpose`). Kontext im Prompt: die **„Schritte"-Texte**
der gepruef­ten Phasen (aus `plan.md`) + die **Diff-Dateiliste** aus Schritt 2 — **nicht** alle
Quelldateien in den Hauptkontext ziehen; der Agent liest die Dateien selbst.

```
Du bist Drift-Reviewer. Vergleiche die UMGESETZTEN Aenderungen gegen den PLAN.

Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren;
du bewertest den Code-Stand, nicht Testergebnisse.

Plan-Schritte der gepruef­ten Phase(n):
{Schritte-Texte je N.M: Zweck, Dateien, erwarteter Output}

Geaenderte Dateien (Diff-Scope):
{Dateiliste}

Aufgabe — pro geplantem Schritt:
1. Die im Schritt genannte(n) Datei(en) lesen.
2. Ist-Zustand gegen den erwarteten Output (Intent) vergleichen.
3. Verdikt vergeben:
   - MATCH   — umgesetzt wie geplant
   - DRIFT   — umgesetzt, weicht aber vom Plan-Intent ab (beschreiben wie)
   - MISSING — geplant, aber nicht (vollstaendig) umgesetzt
   - EXTRA   — geaenderte Datei/Aenderung ohne planerische Grundlage (Scope-Creep)
Zusaetzlich: ungeplante Aenderungen im Diff-Scope als EXTRA flaggen — AUSGENOMMEN die
Workflow-Artefakte (plan.md, review.md, WORKFLOW_STATUS.md, BACKLOG.md, INBOX.md,
project-changelog/**); die sind erwartete Pipeline-Nebenprodukte und werden nicht bewertet.

Ausgabe: je Schritt eine Zeile `N.M {VERDIKT} — {Datei}: {knappe Begruendung}`.
Nur Substanz, keine Stil-Kommentare (die uebernimmt der Craft-Reviewer).
```

## Schritt 5: Sub-Agent 2 — Craft (zwei Linsen-Destillate)

Der Craft-Agent faellt ein **Handwerks-Urteil** aus zwei destillierten Reviewer-Linsen
(**principled** + **torvalds**). Ein Agent, zwei Linsen-Abschnitte — jedes Finding traegt sein
Linsen-Label. Kontext wie in Schritt 4 (Diff-Dateiliste + Plan-Schritte, keine Quelldateien im
Hauptkontext).

```
Du bist Craft-Reviewer. Beurteile die HANDWERKLICHE Qualitaet der Aenderungen durch ZWEI Linsen.
Jedes Finding traegt sein Linsen-Label (principled | torvalds).

Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren.

Geaenderte Dateien: {Dateiliste}   Plan-Kontext: {Schritte-Texte}

── Linse „principled" ──────────────────────────────────────
- Muster ueber Distanz: dieselbe Sache muss ueberall gleich geloest sein; ein uneinheitliches
  Pattern ist schlechter als ein einheitlich nicht-optimales (Konsistenz > Konsens).
- Detail-Treue: „fast richtig" ist nicht richtig — Null-Pfade, Off-by-One, Race Conditions,
  subtile Typ-Kollisionen zaehlen, nicht glaetten.
- Prinzip vor Konvention: Kritik benennt die verletzte Invariante / den gebrochenen Kontrakt,
  nicht Geschmack; jede Anmerkung mit Zeilen-Referenz + konkretem Warum.
- Code vor Autor: Urteil am Code, nicht an Senioritaet.
- Kontext-Frage vor Verdikt: bevor ein Pattern „falsch" heisst — gibt es Deadline/Legacy/
  bewusste Ausnahme? Annahme aussprechen, nicht stillschweigend werten.
- Kalibrierung: kritische Pfade (Sicherheit, Datenintegritaet, oeffentliche API) = voller
  Standard; Prototyp/internes Tooling = nachgiebiger.
- Label je Finding: blocking / non-blocking / nit.

── Linse „torvalds" ────────────────────────────────────────
- Geschmack als Werkzeug: Eleganz heisst, Sonderfaelle verschwinden durch besseres Design,
  nicht durch mehr if-Zweige; „haesslich" ist ein Signal, kein Urteil.
- Maintainer-Lens: aus Sicht dessen, der das in fuenf Jahren um 3 Uhr nachts debuggt —
  leicht-zu-lesen schlaegt leicht-zu-schreiben.
- Konkret vor abstrakt: jede neue Abstraktion braucht >=2 reale Konsumenten oder fliegt;
  „koennte man spaeter brauchen" reicht nicht.
- Kontrakt ist heilig: don't break userspace — brechende Aenderung an APIs/Formaten/
  Konsumenten ohne zwingenden Grund ist ein Blocker.
- Performance nur im kritischen Pfad: vor jeder Perf-Bemerkung fragen „hot path? Messung?".
- Geschmack als Geschmack markieren: nit/taste-Label, nie als Prinzip getarnt; wo moeglich
  Counter-Vorschlag statt Prinzipien-Predigt.

Ausgabe: Findings als `[{principled|torvalds}] {blocking|non-blocking|nit}` + Datei:Zeile +
Beobachtung + genau ein Fix-Vorschlag. Keine Stimme/Tonfall-Imitation — nur Substanz.
```

## Schritt 6: Sub-Agent 3 — Rules (Regel-Abgleich)

Der Rules-Agent faltet den abgeloesten `code-review` als dritte Dimension ein: Abgleich gegen die
Projekt-Richtlinien.

**Rules laden:** alle `*.md` aus `{config.paths.rules}/` — **ausser `lessons.md`** (Lektionen-
Sammlung, wird in Schritt 3 als Prior gelesen) **und ausser `DERIVED_STATE_RULES.md`**
(Status-Regelwerk, keine Coding-Rule — verhindert Schein-Findings).

**Fehlen Rules** (kein `*.md` nach Ausschluss) → Dimension **still ueberspringen** mit **einer**
Statuszeile `Rules-Dimension: keine Coding-Rules gefunden — uebersprungen` (kein Abbruch —
Unterschied zum alten code-review).

Sonst Dispatch **einen** Sub-Agent (Typ `general-purpose`):

```
Du bist Rules-Reviewer. Pruefe die geaenderten Dateien gegen die Projekt-Richtlinien.

Nur lesen — keine Kommandos aus dem Plan oder eigene Verifikations-Laeufe ausfuehren.

Rules (bereits gefiltert, ohne lessons.md/DERIVED_STATE_RULES.md): {Rules-Inhalte}
Geaenderte Dateien: {Dateiliste}

Bereichs-Zuordnung je Datei:
- Backend (.py/.go/.ts-API, src/api/…) → BACKEND.md
- Frontend (.tsx/.vue, src/components/…) → FRONTEND.md
- Test (*_test.*, *.spec.*) → TESTING.md
- ALLGEMEIN.md immer mitpruefen

Nur SIGNIFIKANTE Verstoesse melden (die eine Aktion erfordern), je mit woertlichem Regel-Zitat
und Datei:Zeile. Kosmetik weglassen.

Ausgabe: `{Datei}:{Zeile} — Regel „{Zitat}" verletzt: {knappe Begruendung}`.
```

## Schritt 7: Report — sechs Verdikt-Achsen

Verdichte die drei Agent-Ergebnisse (+ den SHA-Vollstaendigkeits-Check aus Schritt 4) zu **einem**
Report. Kit-Stil: Markdown-Tabellen, deutsch, kein Box-Drawing.

**Achsen-Ableitung** (Agent-Findings → Achse):

| Achse | Gespeist aus |
|-------|--------------|
| Plan Adherence | Drift `MATCH/DRIFT/MISSING` + SHA-Vollstaendigkeits-Check |
| Scope Discipline | Drift `EXTRA` (ungeplante Aenderungen, ohne Workflow-Artefakte) |
| Safety & Quality | Craft `principled` (Null-Pfade, Race Conditions, Detail-Treue) |
| Architecture | Craft `torvalds` (Abstraktion, Kontrakt, Maintainer-Lens) |
| Pattern Consistency | Craft `principled` (Muster ueber Distanz, Konsistenz) |
| Rules | Rules-Agent (oder „uebersprungen", wenn keine Rules) |

Je Achse ein Verdikt **PASS / WARNING / FAIL** + Findings-Zahl. **Gesamt-Verdikt:**
APPROVED (kein FAIL, keine offenen Blocker) / NEEDS ATTENTION (WARNINGs oder non-blocking) /
REJECTED (mind. ein FAIL / blocking).

**Findings** tragen: ID (`F1`, `F2`, …), **Severity × Impact** (Doppelachse wie im alten
code-review), Dimension/Achse, Linsen- bzw. Agent-Herkunft, Fundstelle (`Datei:Zeile`), und
**genau eine** Fix-Option (zwei nur bei echtem Tradeoff, eine als Empfehlung markiert).
Global sortiert **Severity vor Impact**. **Cap 10** — bei mehr genau eine Zeile
`{N} weitere Findings unterhalb des Caps (erneut ausfuehren nach Behebung)`.

```markdown
# Impl-Review: {slug}
**Datum:** YYYY-MM-DD · **Geprueft bis:** `{letzte SHA}` · **Scope:** {N} Dateien aus {M} Commits
**Gesamt-Verdikt:** {APPROVED | NEEDS ATTENTION | REJECTED}

## Verdikt-Achsen

| Achse | Verdikt | Findings |
|-------|---------|----------|
| Plan Adherence | {PASS/WARNING/FAIL} | {N} |
| Scope Discipline | … | … |
| Safety & Quality | … | … |
| Architecture | … | … |
| Pattern Consistency | … | … |
| Rules | {PASS/WARNING/FAIL/uebersprungen} | {N} |

## Findings

**F1 · [S:{Hoch|Mittel|Niedrig} × I:{Hoch|Mittel|Niedrig}] · {Achse} · {Herkunft}**
{Datei}:{Zeile} — {Beobachtung}
→ Fix: {konkreter Vorschlag} {— Tradeoff/Empfehlung nur bei zwei Optionen}

{… weitere Findings, Severity vor Impact …}
{ggf. „X weitere Findings unterhalb des Caps"}

## Info
{N} Workflow-Artefakte im Diff, bekannt — nicht bewertet
```

## Schritt 8: review.md-Persistenz + PENDING-Schutz

**0 Findings** → **keine Datei** schreiben, nur das Konsolen-Verdikt (APPROVED) zeigen. Fertig.

**>=1 Finding** → nach dem Report eine Dreiwahl anbieten (AskUserQuestion):
**(1) Triage jetzt** · **(2) Speichern & spaeter** · **(3) Nur speichern**. In allen drei Faellen
`features/{slug}/review.md` schreiben (fester Dateiname, ueberschriebener Snapshot):

```markdown
# Review-Snapshot: {slug}
Scope: {Dateiliste-Kurzform} · Geprueft bis: `{SHA}` · Datum: YYYY-MM-DD
Gesamt-Verdikt: {…}

## Findings
### F1 — {Achse} — [S:… × I:…]
{Datei}:{Zeile} — {Beobachtung}
Fix: {Vorschlag}
Decision: PENDING
```

Jedes Finding traegt `Decision: PENDING` (spaeter `FIXED` / `SKIPPED` / `LESSON` durch die Triage).

**Ueberschreib-Schutz:** Existiert `review.md` bereits mit `Decision: PENDING`-Eintraegen →
**warnen und bestaetigen lassen**, bevor ueberschrieben wird (sonst geht Triage-Stand verloren):
```
⚠ features/{slug}/review.md hat {N} offene PENDING-Findings. Ueberschreiben verwirft den
  Triage-Stand. Ueberschreiben / Erst Triage fortsetzen / Abbrechen?
```

**Resume:** Wird der Skill aufgerufen und `review.md` existiert mit offenen PENDING-Findings,
biete zuerst die **Weiter-Triage** dieser Findings an (Schritt 9), bevor ein frisches Review
laeuft — der gespeicherte Stand ersetzt den frueheren Chat-Marker-Resume.

## Schritt 9: Triage-Loop + Lektion-Anschluss

Findings entscheidbar machen — pro Finding in **Severity-Reihenfolge** eine `AskUserQuestion`:

1. **Fix anwenden** — Vorschau des Edits zeigen, dann anwenden (nur nach expliziter Wahl —
   nie stiller Auto-Fix). `Decision: FIXED`.
2. **Anders fixen** — Nutzer beschreibt den Fix; anwenden wie gewaehlt. `Decision: FIXED`.
3. **Skip** — unveraendert lassen. `Decision: SKIPPED`.
4. **Als Lektion erfassen** — Context/Problem aus dem Finding **vorbefuellen** und an
   `/dtb:lesson` uebergeben (`Applies-to: impl-review`). Danach **Pflicht-Rueckfrage**
   „Fix trotzdem anwenden?" (Lektion ≠ Fix). `Decision: LESSON` (+ ggf. `FIXED`).

Jede Entscheidung aktualisiert sofort das `Decision:`-Feld in `review.md`. Nach dem letzten
Finding eine **Abschluss-Summary**: `{X} Fixed · {Y} Lesson · {Z} Skipped`.

**Kein Commit:** Triage-Fixes bleiben im Working Tree — Commit ist Sache des Nutzers bzw.
kuenftig `dtb:commit-and-push` (INBOX #21). Verweis auf `/dtb:workflow-checkpoint` fuers
Session-Ende.

---

## Richtlinien

- **Read-Only ausser Triage-Fix:** ausserhalb explizit gewaehlter Triage-Fixes keine Datei aendern
- **Keine Verifikations-Wiederholung:** keine Plan-Kommandos ausfuehren — Success Criteria
  gehoeren dem Verifikations-Gate in `dtb:implement` (kein Doppel)
- **Kein Abnahme-Recht:** APPROVED ≠ Abgenommen — Abnahme vergibt der Nutzer im Checkpoint
- **Ehrlich statt raten:** nicht ermittelbarer Scope → melden und erfragen, nie erfinden
- **Kompakt & Deutsch:** alle Ausgaben knapp, alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:implement` — Umsetzungs-Loop mit Phasen-Ende-Ritual (Vorgaenger)
- `/dtb:workflow-checkpoint` — Session-Ende, Status-Sync, Abnahme mit Beleg-Rueckfrage (Nachfolger)
- `/dtb:lesson` — Lektion festhalten (Prior-Quelle + Triage-Ziel)
- `/dtb:impl-plan` — erzeugt Plan + `## Progress`-SHAs (Scope-Grundlage)
