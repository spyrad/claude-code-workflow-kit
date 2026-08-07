# Implementierungsplan: feature-start schreibt keine Anzeigefelder mehr

**Erstellt:** 2026-08-07
**Feature-Spec:** `features/feature-start-statusfeld/spec.md`
**Geschaetzte Dauer:** 0.5 Session
**Status:** Reviewed (plan-review 2026-08-07: REVISE → 4 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill umbauen (Schreibanweisungen, Frontmatter, Ausgabe-Texte) | 0.3 Session | Geplant |
| Phase 2 | Spiegel korrigieren, Gegenprobe + Verteilung | 0.2 Session | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (Fundstellen verifiziert 2026-08-07 per Grep).

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-feature-start/SKILL.md` | Schritt 4 schreibt in allen drei Lanes: Feature Z. 96 (BACKLOG → „In Arbeit") + Z. 97 (WORKFLOW_STATUS „Laufende Arbeit"); Bug Z. 102 + Z. 103; Aufgabe Z. 108 + Z. 109. Zusaetzlich Bug Z. 101 (`bug.md`: `Analysiert` → `In Arbeit`) und Aufgabe Z. 107 (`task.md`: `Offen` → `In Arbeit`) — Schreibziel ist dort die Artefaktdatei selbst. Frontmatter: `description` Z. 8 („by updating status to «In Arbeit»"), `produces` Z. 16 (`BACKLOG.md, WORKFLOW_STATUS.md, features/*/plan.md, features/*/task.md`), `allowed-tools` Z. 10 (`Read, Write, Edit`). Ausgabe-Templates Z. 117/142/168 („Status: X → In Arbeit"), „Wichtig"-Block Z. 187. **Erhalten bleiben muss:** Progress-Nachruestung Z. 94 (schreibt `plan.md`) und Z. 186 („keine «In Arbeit» oder «Abgeschlossen»" — Auswahlregel, nennt den Begriff legitim) |
| `skills/CLAUDE.md` | Z. 107 beschreibt `feature-start` in der Hard-Gate-Tabelle als „nur Status-Updater"; Z. 105/106 betreffen das Eligibility-Gate und bleiben unveraendert |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | Nennt `feature-start` **nicht** (Grep = 0 Treffer) → kein Seed-Skew, keine Kanon-Aenderung |

---

## Phase 1: Skill umbauen

### Ziel
`dtb:feature-start` enthaelt keine Anweisung mehr, ein Anzeigefeld zu setzen — in keiner der drei
Lanes; Frontmatter und Ausgabe-Texte beschreiben die neue Wirkung korrekt.

### Schritte

#### Schritt 1.1: Schreibanweisungen aus Schritt 4 entfernen (alle drei Lanes)
- **Zweck:** Die Ursache beseitigen statt den Wert zu korrigieren
- **Dateien:** `skills/dtb-feature-start/SKILL.md` (Abschnitt „### Schritt 4: Aktivieren")
- **Input:** Fundstellen aus der Ist-Analyse — Feature Z. 96/97, Bug Z. 101/102/103, Aufgabe Z. 107/108/109
- **Output:** Alle sechs Schreibanweisungen auf Anzeigefelder (BACKLOG, WORKFLOW_STATUS) sowie die zwei Artefaktdatei-Statuswechsel (`bug.md`, `task.md`) entfernt; die Lese-Schritte (Spec, Plan, Bug-Report, Task lesen), das Eligibility-Gate und die Progress-Nachruestung bleiben unveraendert. Der Abschnitt heisst sinngemaess nicht mehr „Aktivieren", sondern beschreibt das Laden des Kontexts
- **Bewusste Nebenwirkung (plan-review 2026-08-07):** Mit Z. 101 entfaellt der letzte Schreiber des `bug.md`-Statusfelds — `workflow-checkpoint` pflegt es nachweislich nicht. Die Luecke wird NICHT hier geschlossen, sondern ist als **Inbox #53** erfasst (Entscheid siehe Technische Entscheidungen)

#### Schritt 1.2: Frontmatter angleichen
- **Zweck:** Die deklarierte Wirkung darf der tatsaechlichen nicht widersprechen (dieselbe Fehlerklasse wie der Befund selbst)
- **Dateien:** `skills/dtb-feature-start/SKILL.md` (Z. 3-17)
- **Input:** `description` nennt „by updating status to «In Arbeit»"; `produces` fuehrt `BACKLOG.md` + `WORKFLOW_STATUS.md`; `allowed-tools` enthaelt `Write`
- **Output:** `description` beschreibt Laden und Anzeigen des Kontexts; `produces: [features/*/plan.md]` (nur noch die Progress-Nachruestung); `allowed-tools: Read, Edit` (`Write` entfaellt — es wird keine Datei mehr neu angelegt); `disable-model-invocation` bleibt `true` (Entscheid siehe Technische Entscheidungen)

#### Schritt 1.3: Ausgabe-Templates und „Wichtig"-Block nachziehen
- **Zweck:** Der Skill darf dem Nutzer keinen Statuswechsel melden, den er nicht vollzieht
- **Dateien:** `skills/dtb-feature-start/SKILL.md` (Z. 117/142/168, Z. 187)
- **Input:** Drei Ausgabe-Templates mit „**Status:** X → In Arbeit"; „Wichtig"-Zeile „Status-Update: BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden"
- **Output:** Statuszeilen zeigen den unveraenderten abgeleiteten Stand (z.B. „**Status:** Geplant — wechselt mit dem ersten abgehakten Schritt"); die „Wichtig"-Zeile wird ersetzt durch den Hinweis, dass Anzeigefelder allein `dtb:workflow-checkpoint` pflegt (§1.3). Z. 186 („keine «In Arbeit» oder «Abgeschlossen»") bleibt — sie ist die Auswahlregel, nicht eine Schreibanweisung

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `dtb:feature-start` ohne Anzeigefeld-Schreibung; Frontmatter und Ausgabe-Texte konsistent

### Checkpoint-Kriterien

#### Automated
> **Kriterien-Doktrin (plan-review 2026-08-07, WARN behoben):** Geprueft wird die **Handlung**
> („wird noch etwas geschrieben?"), nicht der **Wert** („steht dort noch «In Arbeit»?"). Ein
> Wert-Grep bliebe gruen, wenn der Umbau versehentlich einen anderen Wert setzt — die Spec sagt
> aber Schreibfreiheit zu, nicht Wertkorrektheit. Der Wert-Grep bleibt als Zusatzprobe erhalten.
> Alle Anker liegen auf der Wirkstelle, nie dateiweit (Lektion 8).

- [ ] **Handlungspruefung Schritt 4** (Kern-Kriterium): `awk '/^### Schritt 4/{p=1} /^### Schritt 5/{p=0} p' skills/dtb-feature-start/SKILL.md | grep -ciE 'setze status|aktualisiere'` = **0**
- [ ] Zusatzprobe Wert: derselbe Abschnitt, `grep -c 'In Arbeit'` = **0**
- [ ] Selber Abschnitt ohne Statusdatei-Schreibung: `awk '/^### Schritt 4/{p=1} /^### Schritt 5/{p=0} p' skills/dtb-feature-start/SKILL.md | grep -c 'WORKFLOW_STATUS'` = **0**
- [ ] **Handlungspruefung Frontmatter** (Z. 1-17): `sed -n '1,17p' skills/dtb-feature-start/SKILL.md | grep -ciE 'updating|updates|setz|schreib'` = **0** — die Selbstbeschreibung deklariert keine Schreib-Wirkung mehr (faengt auch Umformulierungen, Einspruch Senior Dev)
- [ ] Frontmatter-Deklarationen: `produces` enthaelt weder `BACKLOG.md` noch `WORKFLOW_STATUS.md`; `allowed-tools` ohne `Write`
- [ ] Progress-Nachruestung erhalten: `grep -c 'Nachruestung' skills/dtb-feature-start/SKILL.md` ≥ **1**
- [ ] Auswahlregel unangetastet: `grep -c 'keine "In Arbeit"' skills/dtb-feature-start/SKILL.md` ≥ **1** (Z. 186 nennt den Begriff legitim — deshalb kein dateiweiter Negativ-Grep)

#### Manual
- [ ] Der umgebaute Schritt 4 liest sich als geschlossene Anweisung (kein Rest-Satz, der auf einen entfernten Schritt verweist) — Nachbarschaft gegengelesen (Lektion 12)

---

## Phase 2: Spiegel korrigieren, Gegenprobe + Verteilung

### Ziel
Kein Dokument beschreibt mehr die alte Wirkung; die Aenderung liegt auch in den installierten
Kopien vor und ist an einem realen Start belegt.

### Schritte

#### Schritt 2.1: Doku-Spiegel korrigieren
- **Zweck:** Kopplungs-Regel aus `skills/CLAUDE.md` einhalten — Spiegel im selben Zug mitziehen und mechanisch verifizieren
- **Dateien:** `skills/CLAUDE.md` (Z. 107)
- **Input:** „`impl-plan` (`after`-Match ueber `feature-start` hinweg: feature-start nur Status-Updater; …)"
- **Output:** Die Begruendung nennt die neue Rolle (`feature-start` zeigt nur Kontext, schreibt keinen Status); die Gate-Aussage der Zeile bleibt inhaltlich unveraendert

#### Schritt 2.2: Repo-weite Gegenprobe + Verteilung
- **Zweck:** Zurueckgebliebene Beschreibungen finden (Lektion 3: nicht nur Frontmatter-Referenzen betrachten) und die Aenderung wirksam machen
- **Dateien:** keine Repo-Aenderung ausser gefundenen Nachzuegler; danach Verteilung (Lock + `~/.claude/` liegen ausserhalb)
- **Input:** **Feste Reihenfolge (Nachlauf):** Gegenprobe `grep -rn "feature-start" --include=*.md skills/ CLAUDE.md` auswerten → gefundene Nachzuegler korrigieren → Phase committen → pushen → `/dtb:kit-sync sync` → Nachlauf-Kriterien pruefen → SHA-Nachtrag. Die Verteilungsquelle ist der gepushte Stand; vor dem Push koennen die Nachlauf-Kriterien nicht gruen sein (ausstehend ≠ verletzt, Lektion 1)
- **Output:** Gegenprobe dokumentiert; `/dtb:kit-sync check` meldet 0 Abweichungen; die installierte Kopie traegt den neuen Text

> **3x3-Block:** Nach Schritt 2.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Spiegel korrigiert, Gegenprobe dokumentiert, Aenderung verteilt

### Checkpoint-Kriterien

#### Automated
- [ ] **Wirkstellen-Anker** (plan-review 2026-08-07, WARN behoben — Lektion 8): `grep -c 'feature-start nur Status-Updater' skills/CLAUDE.md` = **0**. **NICHT** dateiweit auf `nur Status-Updater` pruefen: der Begriff steht zweimal, und Z. 104 (`workflow-checkpoint nur Status-Updater`) ist **korrekt** und betrifft einen anderen Skill — ein dateiweites Kriterium wuerde die Loeschung einer richtigen Aussage erzwingen
- [ ] Fremde Aussage unangetastet: `grep -c 'workflow-checkpoint.* nur Status-Updater' skills/CLAUDE.md` ≥ **1** (Z. 104 bleibt). **Muster bewusst mit `.*`:** Z. 104 setzt den Skillnamen in Backticks (`` `workflow-checkpoint` nur Status-Updater ``), Z. 107 nicht — ein wortwoertliches Muster ohne Backticks trifft die Zeile nicht (beim Kriterien-Test 2026-08-07 real aufgefallen)
- [ ] Gate-Zeile erhalten: `grep -c 'feature-start' skills/CLAUDE.md` ≥ **2** (Z. 105 + Z. 106 unveraendert)
- [ ] Gegenprobe ausgefuehrt und Ergebnis im Chat gezeigt: `grep -rn "feature-start" --include=*.md skills/ CLAUDE.md` — jede Trefferzeile bewertet (Verweis vs. Wirkungsbeschreibung)
- [ ] **(Nachlauf — gruen erst nach Commit→Push→Sync)** `kithash(~/.claude/skills/dtb-feature-start/SKILL.md)` = Lock-Hash = Repo-Hash (Drei-Punkte; Gate: alle drei Seiten gefuellt, Lektion 7)
- [ ] **(Nachlauf)** Abschluss-`check`: 0 Abweichungen ueber alle Artefakte

#### Manual
- [ ] **Realer Start** der Aufgabe `gitattributes-eol` (0/6, einziger startbarer Kandidat im Bestand) gefolgt von `/dtb:workflow-resume`: **kein** Feldkonflikt gemeldet, Status bleibt `Offen` (das eigentliche Erfolgskriterium — die Automated-Kriterien pruefen nur den Text). Bewusst ein echtes Item statt einer Attrappe: der Start ist ohnehin faellig und veraendert nur einen Anzeigewert, der nach diesem Feature gar nicht mehr geschrieben wird
- [ ] **Progress-Nachruestung per Wegwerf-Test** (Muster aus `output-style-gezielt` 2.4, plan-review 2026-08-07): temporaeren Plan ohne `## Progress` anlegen → `feature-start` darauf ausfuehren → Nachruest-Angebot erscheint und schreibt korrekt → Wegwerf-Datei wieder loeschen. Ohne diese Datei ist das Kriterium nicht ausfuehrbar, weil jeder Bestandsplan eine `## Progress`-Sektion hat (Senior Dev, Runde 3)
- [ ] Rueckweg einmal gedanklich durchgespielt: die Zeilen unter `## Rueckweg` reichen aus, um den alten Zustand ohne Rueckgriff auf diesen Chat wiederherzustellen

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Grundzuschnitt | Feld korrekt setzen vs. gar nicht mehr schreiben | **Gar nicht mehr schreiben** | Ein Write, der den vorhandenen Wert wiederholt, hat keinen Zweck; zwei Schreiber pro Feld sind die Konstellation aus Inbox #35. Nutzer-Entscheid 2026-08-07 |
| Lese-Seite „Laufende Arbeit" | mitnehmen vs. separat | **Separat (Inbox #52)** | Vier Leser + Status-Template haetten den Fast-Track auf 3 Phasen gehoben; anderer Defekt (Leser ohne Schreiber). Nutzer-Entscheid 2026-08-07 |
| Schreibrecht | ganz entziehen vs. `Edit` behalten | **`Edit` behalten** | Die Progress-Nachruestung repariert eine fehlende Struktur und bleibt erhalten; nur `Write` (Neuanlage) entfaellt |
| Modell-Initiative | `disable-model-invocation` auf `false` vs. `true` belassen | **`true` belassen** | Die Konvention „read-only = modellaufrufbar" zielt auf Lese-Reports; ein Start ist ein bewusst gesetzter Arbeitsschritt. Als offener Punkt in der Spec vermerkt |
| Bestands-Migration | Reparaturlauf vs. keiner | **Keiner** | `workflow-checkpoint` synchronisiert Anzeigefelder bei jedem Lauf (§1.3) — **Einschraenkung:** gilt fuer `spec.md`/`task.md`, NICHT fuer `bug.md` (siehe naechste Zeile) |
| Pflege des `bug.md`-Statusfelds nach dem Umbau | checkpoint erweitern vs. auslagern vs. Bug-Lane ausnehmen | **Auslagern (Inbox #53)** | Verifiziert im plan-review 2026-08-07: `workflow-checkpoint` fuehrt `bug.md` weder in `produces` noch in seinem Sync-Schritt; `feature-start` Z. 101 ist der einzige Schreiber. Nach diesem Feature hat das Feld keinen Pfleger — die Luecke ist real, aber wegen 0 Bugs im Bestand heute folgenlos. Checkpoint zu erweitern haette eine dritte Phase erzwungen; die Bug-Lane auszunehmen haette die drei Lanes ungleich behandelt (Spec-Risiko). Nutzer-Entscheid 2026-08-07 |

---

## Rueckweg

> Ergaenzt nach plan-review 2026-08-07 (Betriebs-Waechter, WARN behoben). Der Weg zurueck ist
> trivial — aber nur dokumentiert ist er auch in drei Wochen auf der zweiten Maschine trivial.

Erweist sich der Wegfall der Sichtbarkeit im Alltag als Fehler:

1. `git revert {SHA der Phase 1}` bzw. `git revert {SHA der Phase 2}` im Kit-Repo — die
   Aenderung liegt vollstaendig in zwei Commits an zwei Dateien, es gibt keinen Datenanteil
2. Pushen, dann `/dtb:kit-sync sync` — die installierten Kopien fallen auf die alte Fassung
   zurueck; der `check` danach muss 0 Abweichungen melden
3. Bereits gestartete Items bleiben unberuehrt: ihr abgeleiteter Status haengt an `## Progress`
   bzw. den Checklisten, nicht am Anzeigefeld

**Fehlermodus benennen (Betriebs-Waechter, Runde 3):** Faellt spaeter auf, dass ein Pfad doch
`Write` braucht, bricht der Lauf mitten in der Arbeit ab statt vorab zu warnen. Erkennungszeichen:
Der Skill meldet einen Werkzeug-Fehler bei der Progress-Nachruestung. Sofortmassnahme: `Write` in
`allowed-tools` zurueckgeben (eine Zeile), Rest des Features bleibt gueltig.

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Schreibanweisungen aus Schritt 4 entfernen
- [x] 1.2 Frontmatter angleichen
- [x] 1.3 Ausgabe-Templates + Wichtig-Block nachziehen
- [ ] 2.1 Doku-Spiegel korrigieren
- [ ] 2.2 Gegenprobe + Verteilung

---

## Umsetzung

Umsetzung mit `/dtb:implement feature-start-statusfeld` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/feature-start-statusfeld/plan.md` laden; der erste
nicht abgehakte Schritt in `## Progress` ist der naechste.

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-07)
