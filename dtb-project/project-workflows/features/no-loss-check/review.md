# Review-Snapshot: no-loss-check

Scope: `skills/dtb-no-loss-check/SKILL.md`, `skills/dtb-workflow-checkpoint/SKILL.md`,
`skills/dtb-session-summary/SKILL.md`, `skills/dtb-workflow-status/SKILL.md`, `CLAUDE.md`
Geprueft bis: Arbeitsbaum (SHA-Scope `926ec71` + uncommittete Triage-Fixes) · Datum: 2026-08-06

**Gesamt-Verdikt: NEEDS ATTENTION** — kein offener Blocker; die Fixes des 2. Laufs sind
mechanisch gegengeprueft, aber **nicht unabhaengig verifiziert**. Fuer ein APPROVED braucht es
einen dritten Lauf gegen den jetzigen Stand.

## Verlauf

| Lauf | Modus | Verdikt | Ergebnis |
|------|-------|---------|----------|
| 1 (Erstreview) | 2 Sub-Agents (Drift mechanisch, Craft principled/torvalds) | REJECTED | 10 Findings, davon 2 blocking |
| Triage 1 | — | — | 10 Fixed · 0 Lesson · 0 Skipped |
| 2 (Verifikation) | 1 Sub-Agent, fokussiert auf die Fixes | REJECTED | 8/10 sauber, 2 teilweise, **6 neue Probleme durch die Fixes** |
| Triage 2 | — | — | 5 Fixed (G1-G5) + 2 Nits · 0 Skipped |

## Lauf 1 — Findings (alle FIXED)

| # | Achse | Kern | Decision |
|---|-------|------|----------|
| F1 | Safety & Quality | Versioniert-Kennzeichnung per `.gitignore`-Lookup — `.gitignore` traegt Glob-Muster mit Last-Match-wins, kein Pfad-Vergleich beantwortet die Frage; zugleich Drift gegen die feste Zuordnung in Spec/Plan | FIXED — feste Tabelle + Vorbehalt + Begruendung |
| F2 | Safety & Quality | Leer-Fall („nichts weiter") widerspricht Randfall 1 („Kompressions-Zeile nie weglassen") | FIXED — Ausnahme-Absatz |
| F3 | Plan Adherence | Begruendung der Slug-Pflicht sachlich falsch („erstes Fragewort wird verschluckt") — von beiden Agents unabhaengig gefunden | FIXED — Skill + Plan |
| F4 | Plan Adherence | Zwei technische Entscheidungen im Plan auf „Offen", faktisch getroffen | FIXED |
| F5 | Architecture | „Lief die Pruefung bereits, genuegt ihr Ergebnis" widerspricht Randfall 3 | FIXED |
| F6 | Plan Adherence | Stufe-2-Nachschaerfung (untagged Bullets) nicht im Plan nachgezogen | FIXED |
| F7 | Pattern Consistency | Sektionsgrenze `## Offene Punkte` undefiniert | FIXED — Klausel von `meeting-agenda` |
| F8 | Safety & Quality | Unklar, ob gespraechsseitig Verworfenes in die Sammelzeile zaehlt | FIXED (Nachbesserung in Lauf 2, siehe G1) |
| F9 | Safety & Quality | Zweitlauf-Kopfzeile behauptet eine Klassifikation, die Stufe 1 nicht leisten kann | FIXED |
| F10 | Pattern Consistency | Degradierte Form der Versioniert-Angabe undefiniert | FIXED (durch F1 hinfaellig) |

## Lauf 2 — Findings (alle FIXED)

### G1 — Safety & Quality — [S:Mittel x I:Hoch]
`SKILL.md:268` ↔ `336-338` — **Selbst erzeugt:** Der F8-Fix schob die Rechenschaft ueber
gespraechsseitig verworfene Funde an die Zweitlauf-Kopfzeile ab, der F9-Fix machte genau diese
Kopfzeile zustandsfrei. Eine Fund-Klasse fiel damit aus jeder Ausweisung heraus — dasselbe still
wirkende Muster, gegen das die Sammelzeile existiert.
Decision: FIXED (2026-08-06 — ehrlich benannt: zaehlt nirgends, weil die Entscheidung in dieser
Sitzung fiel und im Verlauf steht; ueber Sitzungsgrenzen hinweg wieder legitimer Fund)

### G2 — Safety & Quality — [S:Mittel x I:Mittel]
`SKILL.md:142` ↔ `259`/`265` — Platzhalter `{N}` statt `{M}` im Verworfen-Zusatz, und
„bewusst verworfen" bezeichnete zwei disjunkte Mengen (INBOX-Status vs. Gespraech).
Decision: FIXED (2026-08-06 — Platzhalter korrigiert, beide Bedeutungen explizit getrennt)

### G3 — Plan Adherence — [S:Niedrig x I:Mittel]
`plan.md:143` — Schritt-Text sagte konditional „Slug ist Pflicht, sobald mehr als ein Feature in
Frage kommt", waehrend Skill und eigenes Kriterium ihn unbedingt verlangen.
Decision: FIXED (2026-08-06 — auf unbedingt gesetzt, mit dem echten Grund)

### G4 — Pattern Consistency — [S:Niedrig x I:Niedrig]
`SKILL.md:327` — F9 ersetzte „Zweiter Lauf" nur im Codeblock, nicht in der Abschnitts-Ueberschrift.
Decision: FIXED (2026-08-06)

### G5 — Safety & Quality — [S:Niedrig x I:Niedrig]
`SKILL.md:220-221` — Der F1-Vorbehalt las sich als Handlungsanweisung an den Skill, ist aber eine
an den Menschen; der Check kann den Abweichungsfall per Konstruktion nicht erkennen.
Decision: FIXED (2026-08-06 — als Hinweis an den Menschen gekennzeichnet)

### Nits (beide FIXED)
- Leer-Fall-Codeblock zeigt die Kompressions-Zeile jetzt mit, statt sie nur in Prosa darunter zu
  fuehren (der Block ist als woertliche Vorlage gedacht)
- `plan.md:87-88` Input-Bullet verweist jetzt auf die Nachschaerfung zwei Absaetze tiefer

## Offen fuer die Abnahme

- Ein dritter, unabhaengiger Lauf gegen den jetzigen Stand — noetig fuer APPROVED
- Die drei wartenden Manual-Kriterien der Phase 3 (echter Lauf am Sitzungsende, Fund-Rate,
  Aufruf aus dem Checkpoint nicht stoerend) — sie werden ueber die Beleg-Rueckfrage in
  `dtb:workflow-checkpoint` eingeloest, nicht hier

## Methodik-Notiz

Der wertvollste Befund beider Laeufe war jeweils einer, den der Autor selbst nicht gesehen haette:
F1 (sachlich falsche Regel, fuer plausibel gehalten) und G1 (zwei eigene Fixes, die sich
gegenseitig die Grundlage entziehen). Der zweite ist die Nachbarschafts-Regel aus
`skills/CLAUDE.md`, angewandt auf Review-Fixes statt auf Code: **wird eine Stelle geaendert, alle
benachbarten Anweisungen im selben Abschnitt mitpruefen** — auch dann, wenn die Aenderung aus
einem Review-Finding stammt.
