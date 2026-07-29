# Bug: project-init verteilt settings.json nicht

**Erstellt:** 2026-07-28
**Severity:** Mittel
**Status:** Behoben (8/8 Fix-Schritte). Blinde Abnahme am 2026-07-29 **durchgefuehrt** — sie fand eine
vom Fix selbst eingeschleppte Regression (B1, s.u.), die in Fix-Schritt 8 behoben und verifiziert wurde.
`41ebf97` ist auf dieser Maschine installiert; der Nachtrag aus Schritt 8 braucht einen erneuten `/dtb:kit-sync sync`.
**Betroffene Komponente:** `skills/dtb-project-init/SKILL.md` (Body + `produces:` `:14`)

---

## Symptom

`/dtb:project-init` legt im Zielprojekt **keine** `.claude/settings.json` an. Der Seed
`settings.json` aus dem Kit-Repo-Root wird nicht kopiert — die Anweisung fehlt im Skill
vollstaendig.

Beleg: `grep -ni "settings"` ueber die komplette `skills/dtb-project-init/SKILL.md` liefert
**null Treffer**. Weder im Body noch im Frontmatter. `produces:` (`:14`) nennt nur
`workflow.config.yaml`, `CLAUDE.md`, `WORKFLOW_STATUS.md`, `BACKLOG.md` und
`project-rules/DERIVED_STATE_RULES.md`.

Gegenbeleg — das Kit-`CLAUDE.md` behauptet zweimal das Gegenteil:
- Verteilungsliste: `settings.json` → target project's `.claude/settings.json`
- Distributionsmodell: „Seeds (`settings.json`, `DERIVED_STATE_RULES.md`) are copied per project
  by `dtb:project-init` and never drift-checked"

Ebenso `skills/CLAUDE.md`, Abschnitt Distribution: `settings.json` steht dort als Klasse B
(`mode: seed`, per Projekt von `dtb:project-init` verteilt).

## Erwartetes Verhalten

`project-init` kopiert `settings.json` nach `.claude/settings.json` im Zielprojekt (falls dort
noch keine existiert) und fuehrt sie in `produces:` — analog zum Seed-Absatz fuer
`DERIVED_STATE_RULES.md`, der bei `:257` unmittelbar darunter steht und es korrekt macht
(Zielpfad genannt, Kopier-Anweisung explizit).

## Reproduktion

1. Leeres Verzeichnis anlegen, `/dtb:project-init` darin ausfuehren
2. Nach Abschluss `.claude/` im Zielprojekt pruefen
3. → `settings.json` fehlt; nichts im Skill-Ablauf hat sie je erzeugt

Bereits belegt: der blinde Abnahme-Lauf zum Bug `project-init-status-pfad` (2026-07-28, S3,
Subagent ohne Chat-Kontext, nur die SKILL.md als Quelle) protokollierte woertlich —
„wird im Body der Anleitung nirgends erwaehnt und steht nicht in `produces:` — daher nicht
erzeugt."

## Auswirkung

Der Seed traegt mehr als Komfort. Ohne ihn startet jedes neue Projekt ohne:

- **Deny-Liste fuer Secrets** — `Read(./.env)`, `Read(./.env.*)`, `Read(./secrets/**)`
  (der Grund fuer Severity Mittel statt Niedrig)
- **Allow-Liste** fuer gaengige Lesepfade (`*.md`, `*.ts`, `*.py`, …) → unnoetige
  Permission-Prompts
- **Plugin-Aktivierung** `context7@claude-plugins-official`
- `effortLevel: medium`

Workaround: Datei manuell aus dem Kit-Repo kopieren — deshalb „Feature eingeschraenkt,
Workaround vorhanden".

## Kontext

- **Umgebung:** Kit-Repo `claude-code-workflow-kit`, Skill `dtb:project-init`
- **Erstmals bemerkt:** 2026-07-28 (Session 3), als Nebenbefund der blinden Abnahme des Bugs
  `project-init-status-pfad`
- **Frequenz:** Immer — betrifft jede Initialisierung
- **Verwandt:** `features/project-init-status-pfad/bug.md` (behoben, `9e2e9e3`). Gleicher
  Defekt-Typ und gleicher Skill-Abschnitt: eine Erzeugungs-/Kopier-Anweisung fehlt oder ist
  unvollstaendig, waehrend die Nachbaranweisung es richtig macht — das Muster von Lektion **L10**
  („beim Haerten einer Datei-Erzeugung alle benachbarten Erzeugungs-Anweisungen im selben
  Abschnitt mitpruefen")
- **Nicht Teil dieses Bugs, gleicher Abschnitt:** (a) `CLAUDE.md` hat an ihrer eigenen
  Erzeugungs-Anweisung (`:175-245`) keinen Zielort — seit dem Fix `9e2e9e3` steht der Root nur
  indirekt in der Negativregel `:250-251`; (b) `.gitkeep` wird nur in `input/`-Ordnern angelegt
  (`:135`), waehrend `project-changelog/`, `project-testing/` und `project-workflows/features/`
  leer und unversioniert bleiben — obwohl `project-design/` zwei Zeilen spaeter genau dafuer eine
  README bekommt. Beim Fix dieses Bugs mitnehmen

---

**Erfasst mit:** `/dtb:bug-report`

---

## Analyse

**Analysiert:** 2026-07-29
**Status:** Offen → Analysiert

### Root-Cause-Hypothesen

| # | Hypothese | Wo (Datei:Zeile) | Evidenz | Staerke |
|---|-----------|------------------|---------|---------|
| 1 | Die Kopier-Anweisung fehlt vollstaendig, und **kein anderer Skill springt ein** — die Datei wird von niemandem verteilt | `skills/dtb-project-init/SKILL.md` (ganze Datei) + `skills/dtb-kit-sync/SKILL.md:192-193` | `grep -ni "settings"` ueber project-init → 0 Treffer. kit-sync Schritt 4 woertlich: „Klasse B (Seeds): wird von install NICHT kopiert — Seeds sind projektlokal und Sache von `dtb:project-init`" | STRONG |
| 2 | **Entstehungsursache:** Die Seed-Mechanik wurde fuer *eine Datei* gebaut statt fuer die *Klasse* | `SKILL.md:261-296` vs. `kit-sync:75-77` | Der Seed-Block heisst „Regel-Datei verteilen" und hat `SRC`/`DST` auf `DERIVED_STATE_RULES.md` hartkodiert. Die Klassen-Tabelle in kit-sync fuehrt aber **zwei** Klasse-B-Seeds (`:77`: `settings.json` → „projektlokal (via project-init)"). Ein klassen-generischer Block haette `settings.json` automatisch mitgenommen | STRONG |
| 3 | **Fix-Blockade, nicht symptom-ursaechlich:** Die vorhandene Quellenaufloesung funktioniert auf dieser Maschine gar nicht — `localPath` fehlt im Lock | `~/.claude/dtb-lock.json` vs. `SKILL.md:269/275` | Grep ueber den realen Lock findet nur `sourceCommit` und `seeds` — **kein `localPath`**. Damit ist `KIT=""`, der Bash-Block faellt in den `else`-Zweig: „FEHLER: Kit-Quelle nicht aufloesbar". Der DERIVED_STATE_RULES-Seed ist hier also heute schon funktionsuntuechtig | STRONG |

**H1 — Begruendung:** Ohne Anweisung im einzigen verteilenden Skill wird die Datei nie kopiert.
**Pruefung:** erledigt (Grep beidseitig: project-init nennt sie nicht, kit-sync delegiert sie an project-init).

**H2 — Begruendung:** Erklaert, warum der Defekt unbemerkt blieb: der Autor loeste die konkrete
Aufgabe („Regel-Datei verteilen"), nicht die generische („Klasse-B-Seeds verteilen"). Exakt das
Muster von Lektion **L10** — nur eine Ebene hoeher: nicht die Nachbarzeile wurde uebersehen,
sondern das zweite Element derselben Klasse.
**Pruefung:** erledigt (Tabellenvergleich `kit-sync:75-77` ↔ Skill-Body).

**H3 — Begruendung:** Betrifft nicht das Symptom (die Anweisung fehlt ohnehin), bestimmt aber die
Fix-Strategie: ein blindes Nachbauen des bestehenden Blocks erzeugt einen Seed, der auf dieser
Maschine sofort in die Fehlermeldung laeuft.
**Pruefung:** auf der Zweitmaschine (Lock-Stand `9e2e9e3`, S3) gegenpruefen, ob dort `localPath`
gesetzt ist — hier ist der Lock von `7c3272a` / 2026-07-23.

---

## Fix-Schritte

> **Diese Checkliste ist die Status-Quelle** (DERIVED_STATE_RULES §1.5): 0 abgehakt = Analysiert,
> teilweise = In Arbeit, alle = Behoben.

- [x] `.claude/` in den Verzeichnisbaum von Schritt 4 aufnehmen — als eigener Abschnitt „Zusaetzlich auf Projektwurzel-Ebene (NICHT unter `dtb-project/`)" mit `mkdir -p .claude`, statt den `dtb-project/`-Baum zu verbiegen
- [x] Zweiten Seed-Absatz fuer `settings.json` eingefuegt (Schritt C), **mit Existenz-Gate**: `elif [ -f "$DST" ]` → `UEBERSPRUNGEN` + `diff` zur Anzeige, ausdruecklich „NICHT automatisch mergen". Verifiziert durch Test 2 (Datei byte-identisch)
- [x] Quellenaufloesung gehaertet und **vor** beide Seeds gezogen (Schritt A): drei unterscheidbare Faelle statt einer Sammelmeldung — kein Lock / Lock ohne `localPath` / `localPath` zeigt ins Leere (letzteres mit Rechnerwechsel-Hinweis). Verifiziert durch Test 3
- [x] `produces:` (`:14`) um `.claude/settings.json` ergaenzt — Unbedenklichkeit doppelt belegt: `project-health:199` prueft nur `consumes` → Producer, und Test 5 zeigt, dass **kein** Skill `settings.json` in `consumes` fuehrt
- [x] Gegenprobe: Kit-`CLAUDE.md` und `skills/CLAUDE.md` decken sich jetzt mit dem Skill. **Befund dabei:** die kit-sync-Klassen-Tabelle ist NICHT unvollstaendig — `DERIVED_STATE_RULES.md` ist dort bewusst als „nicht in v1" ausgeklammert (`kit-sync:80-81`). Der Verweis im Fix wurde entsprechend praezisiert statt kit-sync zu aendern
- [x] **Mitnahme 1:** `CLAUDE.md` hat jetzt an ihrer eigenen Anweisung einen Zielort („**Zielort:** `CLAUDE.md` im **Projekt-Root** (neben `workflow.config.yaml`)")
- [x] **Mitnahme 2:** `.gitkeep` jetzt auch fuer `project-changelog/`, `project-testing/` und `project-workflows/features/`, mit Begruendung („bleiben leer und waeren in Git sonst unversioniert") und Abgrenzung zu `project-design/` (README) und `.claude/` (hat sofort Inhalt)
- [x] **Schritt 8 (aus der blinden Abnahme, 2026-07-29):** Bloecke B und C **selbstaendig** gemacht — die `LOCK`/`KIT`-Aufloesung steht jetzt in jedem der drei Bloecke, plus `[ ! -d "$KIT" ]`-Guard mit ehrlicher Meldung („Kit-Quelle nicht aufloesbar — Diagnose siehe Schritt A") statt der irrefuehrenden „Datei nicht gefunden: /settings.json". Warnblock nach Schritt A ergaenzt, der die Wiederholung als Absicht kennzeichnet. **Mitnahme B3:** aeusseren Code-Fence der Integrations-README auf 4 Backticks (der innere ```` ``` ````-Fence beendete formal den aeusseren). **Mitnahme B11:** `|| true` an den `ls`-Block `:52` (Exit 2 im leeren Projekt — genau dem Normalfall fuer project-init)

**Regressionsrisiko:**
- **Hoechstes Risiko: Datenverlust durch Ueberschreiben.** Viele Projekte haben eine eigene `.claude/settings.json` (permissions, hooks, env). Der Vorlage-Block `:281` macht `cp` **ohne Existenzpruefung** — 1:1 uebernommen zerstoert das die Projekt-Config. Das Existenz-Gate ist deshalb nicht optional
- Der Kit-Seed aktiviert `context7@claude-plugins-official` und setzt `effortLevel: medium` — im Zielprojekt evtl. unerwuenscht. Der Seed ist Startpunkt, kein Zwang; im Meldetext erwaehnen
- Umbau der Quellenaufloesung (Fix-Schritt 3) darf den bestehenden DERIVED_STATE_RULES-Seed nicht brechen
- `pipeline-graph` (`:40/:103`) behandelt `produces`-Eintraege als Artefakt-Patterns → `.claude/settings.json` erscheint als neuer Knoten in der Visualisierung (kosmetisch, kein Fehlalarm)

## Testplan

Ausgefuehrt 2026-07-29. Die Bash-Bloecke wurden **aus der SKILL.md extrahiert** (`awk`) und
unveraendert ausgefuehrt — getestet ist also der Text, der im Skill steht, keine Nachbildung.

- [x] Repro nachstellen: leeres Verzeichnis + Block C → `.claude/settings.json` angelegt, Hash `67a06f4c…` **identisch** zur Kit-Quelle
- [x] Regression Ueberschreib-Schutz: Zielverzeichnis mit eigener `.claude/settings.json` (permissions + hooks) → `UEBERSPRUNGEN`, Hash `13d7df48…` vorher = nachher, Diff nur angezeigt
- [x] Regression Quellenaufloesung: Block A gegen den **echten** Lock dieser Maschine → „FEHLER: Lock vorhanden, aber ohne 'localPath'" mit konkretem Handlungshinweis; nichts wurde erfunden
- [x] Regression Regel-Seed: Block B unveraendert lauffaehig, `DERIVED_STATE_RULES.md` hashgleich kopiert (Syntax-Check + Lauf)
- [x] `produces`-Fehlalarm ausgeschlossen: `grep -rn "consumes:.*settings" skills/` → 0 Treffer
- [x] **Blinde Abnahme** (Subagent, leeres git-Verzeichnis, nur die SKILL.md als Quelle, kein Chat-Kontext) — **2026-07-29 durchgefuehrt, NICHT bestanden.** Befund B1 s.u.; nach Fix-Schritt 8 nachverifiziert
- [x] Nachverifikation B1: Bloecke B und C per `awk` aus der SKILL.md extrahiert und **jeder in einer eigenen, frischen Shell** ausgefuehrt (`$KIT` beweisbar leer beim Start) → beide `Seed OK: … hashgleich`, `.claude/settings.json` wieder `67a06f4c…`
- [x] Nachverifikation Ueberschreib-Schutz nach Schritt 8: eigene `.claude/settings.json` → `UEBERSPRUNGEN`, Hash `8ecec192…` vorher = nachher
- [x] Nachverifikation neuer Guard: Block C mit `HOME` auf ein lock-freies Verzeichnis → „FEHLER: Kit-Quelle nicht aufloesbar", **nichts angelegt** (Zielverzeichnis leer)
- [x] Nachverifikation B11: `ls`-Block im leeren Projekt → `exit=0` (vorher 2)
- [x] Vorab-Sonde: `git hash-object` funktioniert **ausserhalb** eines Git-Repos (exit 0) — die Hash-Verifikation beider Seeds traegt auch in Nicht-Git-Projekten (relevant fuer `dtb-assistant`)

## Blinde Abnahme 2026-07-29 — nicht bestanden

Aufbau: Subagent, leeres `git init`-Verzeichnis, **einzige** Wissensquelle die SKILL.md (Lesen von
`features/**`, Changelogs und anderen Skills ausdruecklich untersagt), Interview-Antworten vorgegeben,
harte Schreibgrenze auf das Testverzeichnis. Der Lauf **gelang** — aber nur, weil der Subagent
improvisierte und die Abweichung selbst berichtete.

### B1 — `$KIT` ueberlebt den Blockwechsel nicht (Regression aus diesem Fix)

Schritt A loest `$KIT` auf, B und C benutzen es — aber jeder Bash-Aufruf ist eine eigene Shell.
Selbst nachgestellt, zwei getrennte Aufrufe:

```
Block A hat aufgeloest: KIT=C:/Users/SpyraD/Desktop/Projekte/claude-code-workflow-kit
Block B sieht:          KIT=[]
SRC=[/dtb-project/project-rules/DERIVED_STATE_RULES.md]
-> FEHLER-Zweig: Regel-Datei nicht gefunden
```

**Auswirkung:** woertlich ausgefuehrt melden **beide** Seeds „nicht gefunden" und werden
uebersprungen — bei vorhandenem, korrektem Kit. Das Zielprojekt bekommt weder
`DERIVED_STATE_RULES.md` noch `.claude/settings.json`, und die Fehlermeldung ist sachlich falsch.

**Es ist eine Regression, keine Alt-Last** — belegt per `git show 4ab0069:skills/dtb-project-init/SKILL.md`:
vor dem Fix stand die `LOCK`/`KIT`-Aufloesung **im selben Block** wie `SRC`/`cp`, der Block war
selbstaendig. Fix-Schritt 3 („Quellenaufloesung vor beide Seeds gezogen") hat ihn aufgeteilt und
damit den vorher **funktionierenden** Regel-Seed mit gebrochen — genau das Risiko, das der
Regressionsrisiko-Abschnitt oben als Punkt 3 benannt hatte, ohne dass ein Test es abdeckte.

**Warum 5/6 gruene Tests das nicht sahen — die eigentliche Lehre:** der Testplan extrahierte die
Bloecke per `awk` und fuehrte sie **gebuendelt** aus. In einer Shell funktioniert es; der Defekt
existiert nur an der **Naht zwischen** den Bloecken. Die Methode „getestet ist der Text, der im
Skill steht" war richtig, aber unvollstaendig: sie testete den Text, nicht seine
**Ausfuehrungsgrenzen**. Konsequenz fuer kuenftige Skill-Tests: Bash-Bloecke, die Variablen teilen,
immer **einzeln in frischer Shell** pruefen.

### Zurueckgestellte Nebenbefunde des Laufs (eigene Vorgaenge, nicht Teil dieses Bugs)

- **B2 — Integrations-README am falschen Ort (`:150`):** Inhalt heisst `# Integrations`, beschreibt
  die Struktur *von* `integrations/` und endet mit „Verzeichnis `vendor-x/` umbenennen" — landete
  aber in `vendor-x/input/`, der Drop-Zone, die `dtb:docs-extract` nach Rohdokumenten scannt.
  **Nachtraeglich direkt gefixt** (2026-07-29, noch in S3): Zielort auf `integrations/` korrigiert,
  mit Begruendung im Text und Hinweis, dass `vendor-x/input/` durch die `.gitkeep` in Git bleibt.
  **Kein eigener Vorgang** — Ursache, Auswirkung und Fix stehen vollstaendig hier; ein `bug.md`
  haette sie nur umkopiert (dieselbe Schwelle wie bei B4/B8/B9)
- **B4 — Repo-`name` wird nie erfragt:** Interview (`:74`) fragt Pfad/Typ/Test/Build, das
  Config-Format (`:97`) verlangt `name`, Schritt 5 gibt ihn aus. Der Subagent nahm den Namespace — geraten
- **B8/B9 — Platzhalter-Regeln offen:** `{paths.*}` aufloesen ist nur fuer **Fall 3** gefordert
  (`:261`), fuer die Neuanlage nicht; ebenso ungeregelt, ob die `[…]`-Bloecke des CLAUDE.md-Templates
  und `[YYYY-MM-DD]` gefuellt werden. Der Subagent handelte inkonsistent (fuellte
  `## Development Commands`, liess den Rest)
- **B5/B6/B7 — kosmetisch:** „Status-Dateien anlegen" (`:264`) ist durch den kompletten
  Seeds-Abschnitt von seinen Vorlagen (`:378`) getrennt; `mkdir -p .claude` steht zweimal;
  `mkdir -p "{workflows}"` ist ein No-Op; `vendor-x/input/` bekommt `.gitkeep` **und** README
- **B12** — keine `.gitignore`-Behandlung (reine Beobachtung, war nie im Auftrag)

**Nicht gemacht:** ein **zweiter** blinder Lauf gegen die Fassung nach Schritt 8. B1 selbst ist
staerker belegt als ein blinder Lauf es koennte (die Bloecke wurden einzeln in frischer Shell
ausgefuehrt), aber ein erneuter Lauf koennte weitere Befunde derselben Klasse finden. Bewusst
offengelassen, nicht vergessen.

---

### Nebenbefunde (nicht Teil dieses Bugs)

- **`seeds`-Sektion im Lock wird nie befuellt.** `kit-sync:68` beschreibt sie als „Projektlokale Seed-Ereignisse (befuellt von `dtb:project-init`, nicht von kit-sync)"; project-init schreibt aber nirgends in den Lock (Grep: nur `ls` in Schritt 0). Realer Lock: `"seeds": {}`. **Drittes Vorkommen desselben Musters** — ein Skill erwartet etwas von project-init, das project-init nicht tut
- **Rechner-Divergenz belegt:** Der Lock dieser Maschine steht auf `sourceCommit 7c3272a` / 2026-07-23; der kit-sync-Lauf aus S3 (2026-07-28, Lock → `9e2e9e3`, 41 Artefakte) lief auf der Zweitmaschine. Der Fix aus `9e2e9e3` ist hier also **nicht installiert**
- **Lektionen-Prior lief auf 0 Treffer:** `lessons.md` enthaelt hier nur L1-L6 (letzte 2026-07-19). L7-L10 — darunter das einschlaegige L10 mit `Applies-to: alle` — fehlen, weil die Datei per `.gitignore:15` unversioniert ist und damit nicht zwischen den Rechnern synchronisiert wird. Die in `WORKFLOW_STATUS.md` notierte „Applies-to-Luecke" hat damit eine zweite, mechanische Ursache

---

**Analysiert mit:** `/dtb:debug-plan`
