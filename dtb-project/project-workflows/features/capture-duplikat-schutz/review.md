# Review-Snapshot: capture-duplikat-schutz

Scope: `skills/CLAUDE.md`, `skills/dtb-{idea,task,bug-report,no-loss-check}/SKILL.md`, Change-Artefakte (plan/spec/discovery) · Geprueft bis: `ca38d97` · Datum: 2026-08-19
Gesamt-Verdikt (Erstlauf): **REJECTED** (zwei blocking-Findings)
Nach Triage 2026-08-19: **alle 13 Findings FIXED** - ein neues Verdikt erfordert einen erneuten
Lauf `/dtb:impl-review capture-duplikat-schutz` gegen den dann committeten Stand.

Achsen: Plan Adherence FAIL (3) · Scope Discipline PASS (0) · Safety & Quality WARNING (3) ·
Architecture FAIL (2) · Pattern Consistency WARNING (2) · Rules uebersprungen
Drift-Bilanz: 8x MATCH, 1x DRIFT (2.4), 3x MISSING (3.1-3.3), 0 SHA-Luecken.

## Findings

### F1 — Plan Adherence — [S:Hoch × I:Hoch] — principled
`skills/dtb-idea/SKILL.md:9` + `plan.md:206` — Frontmatter-Nachzug ergaenzte `Grep`, liess `Bash`
fehlen, obwohl alle drei Zielskills einen ```bash-Block im Worktree-Guard tragen. `project-health`
warnt darauf. Das Automated-Kriterium „meldet fuer keinen der drei Skills eine Werkzeug-Warnung"
kann woertlich nicht gruen sein — Schritt 2.4 ist trotzdem mit SHA geflippt (Verletzung des
Flip-Kontrakts §2). Verifiziert: 6 von 9 Guard-Skills ohne `Bash` (Alt-Bestand; der Befund ist das
gruen gemeldete Kriterium, nicht die Luecke).
Fix: `Bash` in `allowed-tools` der drei Zielskills ergaenzen (Empfehlung) — Alternative: Kriterium
auf „keine NEUE Warnung" umschreiben + Alt-Befund in die Uebergabe-Notiz.
Decision: FIXED — `Bash` in `dtb-idea`, `dtb-task`, `dtb-bug-report` ergaenzt; die verbleibende
Alt-Luecke (`idea-review`, `lesson`, `meeting-dump`) als **Punkt 7** in die Uebergabe-Notiz
aufgenommen (bewusst nicht angefasst, Spec schliesst Umbau der geschuetzten Skills aus).

### F2 — Architecture — [S:Hoch × I:Hoch] — torvalds
`skills/CLAUDE.md:159-163` gegen `:208-214` — Kopplungs-Hinweis sagt „Zielzahl 2 … keine dritte
Stelle"; die Laufzeit-Autarkie verlangt sechs Zeilen spaeter eine Kurzform inline in JEDEM
Capture-Skill. Drei existieren (absichtlich anderer Wortlaut) und sind in Zielprojekten die einzig
wirksamen Fassungen (`skills/CLAUDE.md` ist nicht Klasse A). Wer den Kanon aendert, greppt, findet 2,
zieht 2 nach — und verteilt drei veraltete Laufzeit-Regeln global. Fehlerklasse des im selben File
dokumentierten Praxisfalls 2026-07-30/31.
Fix: Hinweis zweistufig — „Vollwortlaut Zielzahl 2 (Kanon + `no-loss-check`); Laufzeit-Kurzformen
Zielzahl 6, Grep-Anker `gleiche Aussage`, bei Kanon-Aenderung inhaltlich mitziehen".
Decision: FIXED — Kopplungs-Hinweis auf zwei Stufen umgebaut (Vollwortlaut woertlich mitziehen,
Laufzeit-Kurzformen inhaltlich), beide mit literalem Grep-Anker und Zielzahl. Nachgemessen: Stufe 1
= 3, Stufe 2 = 7. **Selbstreferenz-Korrektur:** die zuerst notierten Zielzahlen 2/6 waren falsch,
weil der Hinweis die Anker woertlich nennt und sich damit selbst trifft — die Zaehlung ist jetzt
explizit aufgeschluesselt, inklusive „diese Hinweiszeile zaehlt mit".

### F3 — Plan Adherence — [S:Hoch × I:Mittel] — Drift
`plan.md` Phase 3 — Die sechs Protokolle aus 3.1-3.3 existieren nur im Gespraechsverlauf;
`project-changelog/` hat 0 Eintraege zu diesem Feature. 5 von 6 Automated-Kriterien der Phase sind
am Artefakt-Stand nicht verifizierbar, obwohl alle vier Checkboxen mit `ca38d97` geflippt sind. Die
Arbeit fand statt (echte Kommandos, echte Daten) — sie ist nicht persistiert, und das Kriterium
wurde gegen Konsolenausgabe abgehakt statt gegen ein Artefakt.
Fix: Protokolle im Checkpoint in den Session-Log schreiben (der Plan nennt ihn als Ablage) — bis
dahin ist der Beleg an diese Session gebunden.
Decision: FIXED — statt auf den Checkpoint zu warten in `plan.md` → `## Beleg-Protokolle (Phase 3)`
persistiert (8 Bloecke: 6 Treffer-/Blind-Faelle, Kuerzungs-Nachweis, Ausschluss-Block mit 4 Punkten). Begruendung fuer den abweichenden Ablageort: der Changelog gehoert diesem
Worktree nicht (zentrale Datei), der Change-Ordner schon — der Beleg ist damit versioniert und
unabhaengig davon, ob der Hand-off ankommt. Ausdruecklich als Mechanik-Beleg markiert, nicht als E2E.

### F4 — Safety & Quality — [S:Mittel × I:Hoch] — principled
`skills/CLAUDE.md:141` vs. `dtb-idea/SKILL.md:82` (+ `task`, `bug-report`, `no-loss-check`) — Kanon
ist symmetrisch formuliert („wenn der eine den anderen ersetzen koennte"), alle vier operativen
Fassungen sind gerichtet („der bestehende Eintrag koennte die neue Erfassung ersetzen"). Nicht
dieselbe Regel: ein neuer, reicherer Eintrag mit Bestands-Teilmenge ist symmetrisch eine Dublette,
gerichtet nicht. Kanon und Spiegel muessen dieselbe Entscheidung produzieren.
Fix: Zeile 141 auf die gerichtete Form ziehen.
Decision: FIXED — Kanon auf die gerichtete Form gezogen („wenn der VORHANDENE Eintrag sie ersetzen
koennte") und die Richtung ausdruecklich als Teil der Regel benannt, samt Hinweis, dass eine
symmetrische Lesart abweichend entscheiden wuerde. Beide Grep-Zielzahlen unveraendert gueltig (3 / 7).

### F5 — Plan Adherence — [S:Mittel × I:Mittel] — Drift
`skills/CLAUDE.md:159-163` — Die eigene Verifikations-Anweisung ist nicht ausfuehrbar: Grep auf den
fettgedruckten Regelsatz trifft 0 (Zeilenumbruch mit `> `-Zitatzeichen) und koennte selbst multiline
nie 2 treffen, weil die beiden Saetze unterschiedlich beginnen. Der Anker wird nicht literal
genannt — die Zuordnungstabelle 60 Zeilen spaeter macht es richtig.
Fix: literalen Anker nennen — „Grep `Informationsverlust ersetzen koennte` → Zielzahl 2".
Decision: FIXED — gemeinsam mit F2 behoben (dieselben fuenf Zeilen); der Anker steht jetzt literal,
die Zielzahl ist aufgeschluesselt statt behauptet.

### F6 — Pattern Consistency — [S:Mittel × I:Mittel] — principled
`skills/CLAUDE.md:123-137` — Die Einteilungsregel verspricht „mechanisch pruefen, nie schaetzen",
trifft mechanisch angewandt aber auch `feature-discover`/`feature-plan`/`feature-fast`: menschlicher
Freitext, Datei-Familie `features/*/discovery.md` (formgleich mit dem eigenen Beispiel
`features/*/task.md`), selbst abgeleiteter Slug. Merkmal 2 trennt `task.md` nicht von `discovery.md`.
Die Spec fordert Schaerfe „ohne Ermessen".
Fix: Gegenprobe um einen Satz erweitern, der die drei namentlich ausschliesst und das scheiternde
Merkmal benennt (Interview-Synthese → Merkmal 1).
Decision: FIXED - Gegenprobe erweitert: `feature-discover`/`feature-plan`/`feature-fast` namentlich
ausgeschlossen, mit dem scheiternden Merkmal (Interview-Synthese -> Merkmal 1) und dem
ausdruecklichen Hinweis, dass Merkmal 2 sie NICHT ausschliesst (`discovery.md` ist formgleich
mit `task.md`).

### F7 — Safety & Quality — [S:Mittel × I:Niedrig] — principled
`skills/CLAUDE.md:193` (+ alle drei Skills) — „max. 3 Treffer zeigen, Rest als `+N weitere`", aber
das Schema zeigt genau eine Fundstellen- plus eine Rueckfrage-Zeile. Fuer 2-3 Treffer ist das
Rendering unspezifiziert: drei Rueckfragen oder eine? Wohin gehoert `+N weitere`?
Fix: Renderregel ergaenzen — „je Treffer eine Fundstellen-Zeile, danach `+N weitere`, danach genau
EINE Rueckfrage"; die drei Skills erben es ueber die Slot-Fassung.
Decision: FIXED - Schema-Punkt „Kappung + Rendering“: je Treffer eine Fundstellen-Zeile, danach
`+N weitere`, danach GENAU EINE Entscheidungsfrage (nie eine Frage pro Treffer).

### F8 — Architecture — [S:Niedrig × I:Mittel] — torvalds
`dtb-idea/SKILL.md:20` (+ `task:249`, `bug-report:231`), `plan.md:218` — Der Check fuegt im
Trefferfall eine Rueckfrage hinzu; statt die unbedingte Zusage („Keine Rueckfragen, keine
Ausarbeitung") zu qualifizieren, behauptet der neue Text, sie bleibe „unangetastet" — und das
Manual-Kriterium „nirgends relativiert" hat den Widerspruch fixiert. Gegenkontext: der Guard bricht
`idea:20` heute schon ohne Qualifizierung, ist aber Fehlerpfad, waehrend der Check Normalpfad ist.
Fix: Zusage einmal je Skill qualifizieren — „Keine Rueckfragen (Ausnahme: ein Duplikat-Treffer fragt
einmal)".
Decision: FIXED - alle drei Zusagen qualifiziert (`idea`-Kopf: „Keine Rueckfragen (einzige Ausnahme: ein
Duplikat-Treffer fragt genau einmal)“; `task`/`bug-report`-Richtlinie analog) und die falsche
Behauptung „Versprechen bleibt unangetastet“ in allen drei Checks ersetzt. Zusaetzlich das
Manual-Kriterium in `plan.md` umgeschrieben: es forderte Nicht-Relativierung und war damit selbst
der Widerspruch - jetzt fordert es korrekte Qualifizierung. Die Phase-2-Bestaetigung dieses
Kriteriums war sachlich falsch.

### F9 — Pattern Consistency — [S:Niedrig × I:Mittel] — torvalds
`skills/CLAUDE.md:179-183` gegen `:223` — „Jeder Skill fuellt dieses Schema", drei Zeilen weiter
drei Skills ausgenommen, deren Form Kuerzung, Kappung und Fail-open nicht kennt. Nichts sagt,
welcher Form ein NEUER Skill oder die naechste Beruehrung von `lesson` folgt. Das Guard-Vorbild
loest das mit Referenz-Instanz + Vorrangregel; hier fehlt das Aequivalent.
Fix: ein Satz an Zeile 223 — „Bestands-Form ist Alt-Bestand, nicht Alternative: bei der naechsten
Beruehrung aufs Schema ziehen."
Decision: FIXED - Satz an der Bestands-Ausnahme: „Diese Form ist Alt-Bestand, nicht Alternative“ - ein
NEUER Capture-Skill folgt immer dem Schema, bei der naechsten inhaltlichen Beruehrung werden
`lesson`/`open-question`/`meeting-dump` aufs Schema gezogen (`lesson` fehlen Kuerzung, Kappung,
Fail-open).

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled
`dtb-idea/SKILL.md:78,86` — Suchraum ist bewusst „alle Status", die Meldung nennt aber nur
`INBOX (#{N})`. Ob #N offen, ausgearbeitet oder bewusst verworfen ist, ist der
entscheidungsrelevante Teil; `no-loss-check` weist genau das explizit aus.
Fix: Fundstelle auf `INBOX (#{N}, {Status})` erweitern.
Decision: FIXED - Fundstelle auf `INBOX (#{N}, {Status})` erweitert, samt Begruendung im Skill (ob ein
Treffer offen, ausgearbeitet oder bewusst verworfen ist, entscheidet der Mensch anders); die
Konvention nennt den Status-Slot jetzt ebenfalls.

## Findings unterhalb des Report-Caps (vollstaendig gehalten, damit nichts verloren geht)

### F11 — Architecture — [S:Niedrig × I:Niedrig] — torvalds
`skills/CLAUDE.md:187` — Der `{exakt: Nichts geschrieben.}`-Zweig des Meldeform-Schemas hat null
Konsumenten: die drei neuen Skills sind unscharf, die zwei exakten sind in Zeile 223 ausgenommen und
formulieren anders. Neue Abstraktion ohne zwei echte Konsumenten.
Fix: Alternativzweig aus dem Code-Block streichen; die Aussage steht bereits in der
Kopplungsregel-Prosa.
Decision: FIXED - `{exakt: Nichts geschrieben.}`-Alternativzweig aus dem Schema-Codeblock entfernt; die
Aussage steht als eigener Aufzaehlungspunkt in der Prosa („Entscheidungsfrage-Zeile entfaellt bei
exaktem Vergleich“).

### F12 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled (nit)
`skills/CLAUDE.md:228-229`, `dtb-bug-report/SKILL.md:88-89` — `task` vergleicht zwei Abschnitte
(`## Beschreibung`/`## Begruendung`), `bug-report` nur `## Symptom`, obwohl `## Erwartetes Verhalten`
das strukturelle Gegenstueck traegt. Zwei strukturgleiche Schwester-Skills, unterschiedlich weiter
Suchraum, ohne genannten Grund (vermutlich Absicht: das Symptom ist die Identitaet eines Bugs).
Fix: halber Satz Begruendung in der Tabellenzelle, oder `## Erwartetes Verhalten` mit aufnehmen.
Decision: FIXED - Begruendung in die Tabellenzelle: das Symptom ist die Identitaet eines Bugs,
`## Erwartetes Verhalten` folgt daraus und wuerde nur Rauschen beitragen.

### F13 — Plan Adherence — [S:Niedrig × I:Niedrig] — torvalds
`plan.md:326` — Die technische Entscheidung „Beruehrung `CLAUDE.md` (Repo-Root)" steht auf **Offen**
mit dem Vermerk „entscheidbar am Ende von Phase 1"; alle 11 Progress-Zeilen sind geflippt, die
Entscheidung wurde nie eingetragen, und die sechs Punkte der Uebergabe-Notiz fuehren sie nicht.
Haengengelassener Kontrakt mit ausdruecklichem Faelligkeitsdatum.
Fix: Zelle aufloesen (Empfehlung im Review-Gespraech: Katalogtext bleibt unberuehrt) oder als
Punkt 7 in die Uebergabe-Notiz.
Decision: FIXED - Entscheidung auf **B** aufgeloest: Repo-Root-`CLAUDE.md` bleibt unberuehrt (der
Katalogtext beschreibt Skills, nicht Autoren-Konventionen - die Eligibility-Gates stehen dort
ebenfalls nicht). Keine offene technische Entscheidung mehr im Plan.

---

**Erstellt mit:** `/dtb:impl-review`
