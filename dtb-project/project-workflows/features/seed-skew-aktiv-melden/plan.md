# Implementierungsplan: Seed-Skew aktiv melden

**Erstellt:** 2026-11-09
**Feature-Spec:** `features/seed-skew-aktiv-melden/spec.md`
**Geschaetzte Dauer:** 0,5–1 Tag
**Status:** Reviewed (plan-review 2026-11-09: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Probeausgabe in Zielform + Abhilfe-Weg klären | 2–3 h | Geplant |
| Phase 2 | kit-sync ausformulieren, Spiegel nachziehen, Probelauf | 2–4 h | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-kit-sync/SKILL.md` | check-Sequenz Schritte 1-6 (Lock lesen, Quelle beschaffen, Repo-Bestand, Klassifikation, Verwaiste, Report); Report-Format fix mit Schlusszeile „Alles synchron — keine Aktion noetig"; Klassen-Tabelle fuehrt nur `settings.json` als Klasse B, `DERIVED_STATE_RULES.md` „nicht in v1"; Randfall 9 „Seed-Artefakte veraendert → nie als Drift melden"; Frontmatter `consumes: [dtb-lock.json]` |
| `CLAUDE.md` | Distributionsmodell: Seeds „copied per project by `dtb:project-init` and never drift-checked" |
| `skills/CLAUDE.md` | Abschnitt „Distribution (kit-sync)": „Class B (`mode: seed`, copied once, never drift-checked)" |
| `skills/dtb-project-init/SKILL.md` | Seed-Tabelle: Regel-Datei wird ueberschrieben, `settings.json` nie; Schritt 0 fragt bei vorhandener Config nach einem Update |
| `skills/dtb-project-health/SKILL.md` | Check 11 „Seeds (`mode: seed`) NIE pruefen" — bleibt unveraendert |

---

## Phase 1: Probeausgabe in Zielform + Abhilfe-Weg klären

### Ziel
Die drei Ausgaenge des Seed-Hinweises (aktuell / weicht ab / nicht geprueft) liegen als echte
Probeausgabe vor und sind vom Menschen abgenommen, bevor die Regeln im Skill ausformuliert werden
(Lektion: Report-Skills zuerst Beispiel-Ausgabe mit echten Daten abnehmen lassen).

### Schritte

#### Schritt 1.1: Abhilfe-Weg ueber project-init klaeren
- **Zweck:** Offenen Punkt der Spec beantworten — kann `dtb:project-init` in einem eingerichteten
  Projekt nur die Seeds erneuern, ohne das Interview zu wiederholen?
- **Dateien:** `skills/dtb-project-init/SKILL.md` (nur lesen)
- **Input:** Schritt 0 und Abschnitt „Seeds verteilen"
- **Output:** Entscheidung zum Wortlaut der Abhilfe-Zeile — Ablageort: Zeile „Abhilfe-Zeile" in
  `## Technische Entscheidungen` dieses Plans; offener Punkt in `spec.md` auf beantwortet setzen

#### Schritt 1.2: Probe-Sequenz bauen und an vier Faellen fahren
- **Zweck:** Zielform mit echten Daten zeigen
- **Dateien:** Probeskript im Scratchpad (nicht im Repo); zwei Wegwerf-Projekte im Scratchpad,
  je mit `workflow.config.yaml`: **alt** mit einer aelteren Regel-Datei aus der Git-Historie
  (`git show {alter Commit}:dtb-project/project-rules/DERIVED_STATE_RULES.md`), **aktuell** mit
  einer Kopie der Regel-Datei aus der beschafften Quelle `$SRC`
- **Input:** Kit-Quelle wie im check (Referenz 3), Hashing nach Referenz 2 — keine eigene Methode
- **Output:** vier Probeausgaben (Wegwerf alt → „weicht ab"; Wegwerf aktuell → „aktuell";
  Kit-Worktree → „Kit-Repo — Regel-Datei ist die Quelle, nicht geprueft" (Erkennung:
  `skills/dtb-kit-sync/SKILL.md` existiert im Arbeitsverzeichnis); leerer Ordner → „nicht
  geprueft") — Ablageort: Abschnitt `## Probeausgabe` am Ende dieses Plans, woertlich. Vor und
  nach der Probe Hash und mtime der beiden Wegwerf-Regel-Dateien und von `~/.claude/dtb-lock.json`
  festhalten (Ablageort: derselbe Abschnitt)

#### Schritt 1.3: Zielform abnehmen
- **Zweck:** Mensch bestaetigt Block-Form, Wortlaut der drei Ausgaenge und die geaenderte Schlusszeile
- **Dateien:** keine
- **Input:** `## Probeausgabe`
- **Output:** Abnahme oder Korrekturen, eingearbeitet in `## Probeausgabe`

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Entscheidung Abhilfe-Zeile in `## Technische Entscheidungen`
- [ ] `## Probeausgabe` mit vier Ausgaengen

### Checkpoint-Kriterien

#### Automated
- [ ] `awk '/^## Probeausgabe/{p=1} /^## Probelauf Phase 2/{p=0} p' dtb-project/project-workflows/features/seed-skew-aktiv-melden/plan.md | grep -cE "weicht ab|aktuell|Kit-Repo|nicht gepr"` ≥ 4
- [ ] `grep -n "^| Abhilfe-Zeile" dtb-project/project-workflows/features/seed-skew-aktiv-melden/plan.md` liefert genau eine Zeile, deren Entscheidungs-Spalte nicht `Offen` ist
- [ ] Hash und mtime der beiden Wegwerf-Regel-Dateien und von `~/.claude/dtb-lock.json` vor/nach der Probe identisch (Werte in `## Probeausgabe`; Probe schreibt nichts)

#### Manual
- [ ] Mensch nimmt die Zielform der drei Ausgaenge und der Schlusszeile ab

---

## Phase 2: kit-sync ausformulieren, Spiegel nachziehen, Probelauf

### Ziel
Der abgenommene Seed-Hinweis steht als feste Sequenz im Skill, die Kit-Doku widerspricht ihm
nicht mehr, und der Probelauf gegen die Repo-Fassung zeigt die drei Ausgaenge.

### Schritte

#### Schritt 2.1: Seed-Hinweis in kit-sync check einbauen
- **Zweck:** Verhalten verankern
- **Dateien:** `skills/dtb-kit-sync/SKILL.md`
- **Input:** `## Probeausgabe`, Entscheidung Abhilfe-Zeile
- **Output:** neuer check-Schritt „Seed-Hinweis" vor dem Report (eigener, selbststaendiger
  Bash-Block: Regelpfad aus `workflow.config.yaml` → `paths.rules`, Fallback
  `dtb-project/project-rules/`; Kit-Repo-Erkennung vor dem Vergleich — existiert
  `skills/dtb-kit-sync/SKILL.md` im Arbeitsverzeichnis, Ausgang „Kit-Repo — Regel-Datei ist die
  Quelle, nicht geprueft" ohne Vergleich und ohne Abhilfe-Zeile; beide Vergleichsseiten vor dem
  Vergleich auf Inhalt pruefen);
  Report-Format um den Seed-Block und die gekoppelte Schlusszeile erweitert; Klassen-Tabelle um
  `DERIVED_STATE_RULES.md` (Klasse B, Drift-Check nein, Seed-Hinweis im check ja) ergaenzt und den
  Satz „Nicht in v1 … `DERIVED_STATE_RULES.md`" angepasst; Randfall 9 umformuliert („nie als Drift
  — eigener Seed-Hinweis im check"), Randfall „kein DTB-Projekt im Arbeitsverzeichnis" ergaenzt;
  Frontmatter `consumes` um `workflow.config.yaml` und `project-rules/DERIVED_STATE_RULES.md`
  ergaenzt; `allowed-tools` pruefen (Read/Grep/Bash genuegen)

#### Schritt 2.2: Spiegel nachziehen
- **Zweck:** Doku konsistent zum Verhalten
- **Dateien:** `CLAUDE.md` (Distributionsmodell), `skills/CLAUDE.md` (Abschnitt „Distribution (kit-sync)")
- **Input:** Wortlaut aus 2.1
- **Output:** beide Stellen nennen „nie Drift-geprueft, aber `kit-sync check` meldet eine
  abweichende Regel-Datei im Arbeitsprojekt als Hinweis"; vorher repo-weite Suche nach weiteren
  Fundstellen der Seed-Aussage (Lektion: vor Skill-Umbau repo-weit greppen)

#### Schritt 2.3: Probelauf gegen die Repo-Fassung
- **Zweck:** Wirkung belegen
- **Dateien:** keine Repo-Aenderung; Wegwerf-Projekt aus 1.2 wiederverwenden
- **Input:** `skills/dtb-kit-sync/SKILL.md` aus diesem Worktree (nicht die installierte Kopie)
- **Output:** die vier Ausgaenge erneut, jeder Bash-Block einzeln in frischer Shell gefahren,
  dazu Hash und mtime der Wegwerf-Regel-Dateien und von `~/.claude/dtb-lock.json` vor/nach —
  Ablageort: Abschnitt `## Probelauf Phase 2` am Ende dieses Plans

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Erweiterter check-Modus in `skills/dtb-kit-sync/SKILL.md`
- [ ] Zwei nachgezogene Spiegelstellen
- [ ] `## Probelauf Phase 2` mit vier Ausgaengen

### Checkpoint-Kriterien

#### Automated
- [ ] `awk '/^## Modus: check/{p=1} /^## Modus: install/{p=0} p' skills/dtb-kit-sync/SKILL.md | grep -c "Seed"` ≥ 3 (Schritt, Report-Block, Schlusszeile)
- [ ] `awk '/^## Modus: check/{p=1} /^## Modus: install/{p=0} p' skills/dtb-kit-sync/SKILL.md | grep -c "skills/dtb-kit-sync/SKILL.md"` ≥ 1 (Kit-Repo-Erkennung im check)
- [ ] `grep -n "^| 9 |" skills/dtb-kit-sync/SKILL.md | grep -c "Seed-Hinweis"` = 1
- [ ] `grep -n "^  consumes:" skills/dtb-kit-sync/SKILL.md | grep -c "DERIVED_STATE_RULES.md"` = 1
- [ ] `awk '/^- \*\*Class B/{p=1;print;next} p&&/^- /{p=0} p' skills/CLAUDE.md | grep -c "kit-sync check"` ≥ 1 (ganzer Listenpunkt, nicht nur seine erste Zeile)
- [ ] `awk '/^\*\*Distribution model:\*\*/{p=1} p&&/^$/{p=0} p' CLAUDE.md | grep -c "never drift-checked"` = 0 und `… | grep -c "kit-sync check"` ≥ 1 (Negativ-Kriterium auf den Absatz verankert)
- [ ] `awk '/^## Probelauf Phase 2/{p=1} p' dtb-project/project-workflows/features/seed-skew-aktiv-melden/plan.md | grep -cE "weicht ab|aktuell|Kit-Repo|nicht gepr"` ≥ 4
- [ ] Hash und mtime der Wegwerf-Regel-Dateien und von `~/.claude/dtb-lock.json` vor/nach dem Probelauf identisch (Werte in `## Probelauf Phase 2`)

#### Manual
- [ ] Mensch bestaetigt, dass der Probelauf der abgenommenen Zielform aus Phase 1 entspricht

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger | kit-sync check, project-health | kit-sync check | Feldbeleg 2026-11-03: der Fehlschluss „kit-sync haelt alles aktuell" entstand genau dort (per Veto-Vorlage bestaetigt 2026-11-09) |
| Erkennung | Seed-Hash im Lock, Versions-Marker in der Datei, Zwei-Punkt-Vergleich gegen die Quelle | Zwei-Punkt-Vergleich gegen die Quelle | check beschafft die Quelle ohnehin; Bestandsprojekte haben keinen Lock-Eintrag, ein Marker muesste in jedem Feature gepflegt werden |
| Verglichene Seeds | Regel-Datei + settings.json, nur Regel-Datei | nur Regel-Datei | project-init ueberschreibt die Regel-Datei immer, settings.json nie — Abweichung ist nur bei der Regel-Datei Skew |
| Projekt-Anpassung | eigener Zustand „angepasst", neutrale Meldung | neutrale Meldung „weicht ab" + Vergleichsbefehl | Anpassung ist nach Seed-Politik nicht vorgesehen; neutraler Wortlaut behauptet nichts Unbelegtes |
| Abhilfe-Zeile | project-init, Hand-Kopie, beides | Hand-Kopie: fertiger Vergleichs- und Kopierbefehl aus `localPath`; ohne `localPath` Verweis auf die Datei in der Quelle | Schritt 1.1 (2026-11-09): `dtb:project-init` hat keinen Weg „nur Seeds erneuern" — Schritt 0 fragt bei vorhandener Config nach einem Update der Config, die Richtlinie sagt „pro Projekt nur einmal ausgefuehrt", die Seed-Verteilung haengt in Schritt 4 hinter Interview und Config-Schreiben; der Hinweis auf project-init schickte den Menschen durch das ganze Setup. Hand-Kopie ist der belegte Weg (PKP 2026-11-03) |
| Kit-Repo als Arbeitsverzeichnis | vergleichen, eigener Ausgang ohne Vergleich | eigener Ausgang „Kit-Repo — Regel-Datei ist die Quelle, nicht geprueft" | dort ist die Regel-Datei die Quelle; ein Vergleich gegen den gepushten Stand empfaehle bei ungepushten Aenderungen faelschlich `/dtb:project-init` (plan-review 2026-11-09) |
| project-health Check 11 | mitziehen, unveraendert | unveraendert | ein Traeger; Check 11 verweist bereits auf kit-sync check |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Abhilfe-Weg klaeren
- [x] 1.2 Probe an drei Faellen
- [x] 1.3 Zielform abnehmen
- [ ] 2.1 Seed-Hinweis in kit-sync
- [ ] 2.2 Spiegel nachziehen
- [ ] 2.3 Probelauf Repo-Fassung

---

## Umsetzung

Umsetzung mit `/dtb:implement Seed-Skew aktiv melden` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/seed-skew-aktiv-melden/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)

---

## Probeausgabe

Probelauf 2026-11-09 (Schritt 1.2), Quelle frisch geklont: `master @ 7b754e2`. Probeskript im
Scratchpad (`seed-probe.sh`, Prototyp des spaeteren Skill-Blocks); Wegwerf-Projekte im Scratchpad:
**alt** = Regel-Datei aus Commit `e127284` (116 Zeilen), **aktuell** = Kopie aus der Quelle (668 Zeilen).

### Rohbefund je Fall

| Fall | Arbeitsverzeichnis | Probe-Ergebnis |
|------|--------------------|----------------|
| 1 | Wegwerf alt | `ZUSTAND=WEICHT-AB` (Projekt 116 Zeilen, Kit 668 Zeilen) |
| 2 | Wegwerf aktuell | `ZUSTAND=AKTUELL` |
| 3 | Kit-Worktree | `ZUSTAND=KIT-REPO` |
| 4 | leerer Ordner | `ZUSTAND=NICHT-GEPRUEFT` (keine workflow.config.yaml) |

### Zielform im Report (Seed-Block nach der Zusammenfassung, Drift-Teil unveraendert)

Fall 1 — weicht ab:
```
Kit-Sync Check
Quelle: https://github.com/spyrad/claude-code-workflow-kit.git @ master (7b754e2)
Lock:   2026-11-06, 53 Artefakte

Zusammenfassung: {Drift-Zahlen wie bisher}

Seed im Arbeitsprojekt:
| Seed | Zustand |
|------|---------|
| DERIVED_STATE_RULES.md | weicht von der Kit-Fassung ab (Projekt 116 Zeilen, Kit 668 Zeilen) |

→ Vergleichen: git diff --no-index "dtb-project/project-rules/DERIVED_STATE_RULES.md" "C:/Users/SpyraD/Desktop/Projekte/claude-code-workflow-kit/dtb-project/project-rules/DERIVED_STATE_RULES.md"
→ Uebernehmen (der Seed gehoert dem Projekt — kit-sync schreibt ihn nie): cp "C:/Users/SpyraD/Desktop/Projekte/claude-code-workflow-kit/dtb-project/project-rules/DERIVED_STATE_RULES.md" "dtb-project/project-rules/DERIVED_STATE_RULES.md"
  (localPath vorher auf den gepushten Stand bringen: git -C "C:/Users/SpyraD/Desktop/Projekte/claude-code-workflow-kit" pull)

Kit-Kopien synchron — Seed weicht ab (siehe oben).
```

Fall 2 — aktuell (Schlusszeile wie bisher):
```
Seed im Arbeitsprojekt:
| Seed | Zustand |
|------|---------|
| DERIVED_STATE_RULES.md | aktuell |

Alles synchron — keine Aktion noetig.
```

Fall 3 — Kit-Repo:
```
Seed im Arbeitsprojekt: Kit-Repo — die Regel-Datei ist hier die Quelle, nicht geprueft
```

Fall 4 — kein DTB-Projekt:
```
Seed im Arbeitsprojekt: nicht geprueft — keine workflow.config.yaml im Arbeitsverzeichnis
```

Ohne `localPath` im Lock entfallen die beiden `→`-Befehle; an ihrer Stelle steht
`→ Kit-Fassung: dtb-project/project-rules/DERIVED_STATE_RULES.md in {source} — von Hand vergleichen und uebernehmen`.
Gibt es zusaetzlich Drift, bleibt `→ Abgleich: /dtb:kit-sync sync` stehen; die Seed-Zeilen kommen dazu.

### Schreibschutz-Beleg (Hash · mtime, vorher = nachher)

| Datei | vorher | nachher |
|-------|--------|---------|
| `~/.claude/dtb-lock.json` | `d9b5944c3ef3` · 1793980814 | `d9b5944c3ef3` · 1793980814 |
| Wegwerf alt, Regel-Datei | `597f542f72ed` · 1794206495 | `597f542f72ed` · 1794206495 |
| Wegwerf aktuell, Regel-Datei | `dd96ad195c74` · 1794206495 | `dd96ad195c74` · 1794206495 |
