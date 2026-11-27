# Implementierungsplan: plan-review mit Subagenten

**Erstellt:** 2026-11-27
**Feature-Spec:** `features/plan-review-subagenten/spec.md`
**Geschaetzte Dauer:** 3–4 h
**Status:** Reviewed (plan-review 2026-11-27: REVISE → 3 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Umbau `dtb:plan-review`, Config-Block + Probelauf | 2,5–3,5 h | Geplant |
| Phase 2 | Doku-Spiegel, Lint + Gegenprobe | ~45 min | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| skills/dtb-plan-review/SKILL.md | 373 Zeilen; `allowed-tools: Read, Glob, Grep, Write, Edit` (:8), kein `Agent`; Schritt 2 endet mit „Nimm diese Rollen fuer die Diskussion ein." (:68); Schritt 3 = 4 Runden im selben Kontext (:131-151); Schritt 4 Verdikte + Einspruchs-Regel (:153-181); Output-Format (:258-349); „Wichtig" (:360-373) |
| skills/dtb-impl-review/SKILL.md | Vorbild: Dispatch je eines general-purpose-Subagenten, Kontext im Prompt, Agent liest Dateien selbst (:133-135), festes Rueckgabeformat im Prompt (:137-162); `allowed-tools` mit `Agent` (:10) |
| agents/*.md | 4 Rollendateien (je 25–26 Zeilen), ohne Frontmatter; global installiert unter `~/.claude/agents/` (4 Dateien + CLAUDE.md belegt) |
| agents/CLAUDE.md | Zweck-Satz „reusable role perspectives for multi-agent skill discussions" (:5), Tabelle „Current agents" (:31-36) |
| CLAUDE.md | Abschnitt „### Agent Roles" (:73) |
| README.md | `/dtb:plan-review`-Zeile (:79) „Structured review with Architekt, Pragmatiker + Senior Dev agents" |
| workflow.config.yaml | Bloecke `worker:`, `parallel:`, `status:`, `dashboard:`, `lessons:` — kein `plan_review:` |
| skills/dtb-project-init/SKILL.md | Config-Vorlage mit denselben Bloecken (:102-117) |
| skills/dtb-feature-fast/SKILL.md | :105 zitiert „Muster wie `dtb:plan-review` Schritt 2" (Aufloesung global → Projekt) — Kopplung, muss gueltig bleiben |
| scripts/lint-skills.py | prueft Frontmatter inkl. `allowed-tools` (:199-210) |

---

## Phase 1: Skill-Umbau `dtb:plan-review` + Probelauf

### Ziel
Jede aktive Rolle laeuft als eigener paralleler Subagent ohne Sicht auf die anderen; der Haupt-Skill fuehrt im unveraenderten Report-Format zusammen; Ausfall faellt sichtbar auf den heutigen Ablauf zurueck. Ein Probelauf an einem echten Plan belegt die Brauchbarkeit.

### Schritte

#### Schritt 1.1: Frontmatter, Schritt 0 und Schritt 2
- **Zweck:** Werkzeug freischalten (L75) und Eingaben vorbereiten, bevor der Dispatch sie braucht
- **Dateien:** `skills/dtb-plan-review/SKILL.md`
- **Input:** Ist-Analyse; Kernfrage 2026-11-27 (general-purpose + Rollentext)
- **Output:**
  - `allowed-tools: Read, Glob, Grep, Write, Edit, Agent`
  - `consumes` um `workflow.config.yaml` ergaenzt (L44); `after`/`next` bewusst unveraendert — die Funktion des Skills (Plan reviewen, Kopf-Statusfeld pflegen) bleibt gleich (L128)
  - `description` nennt die isolierten Subagenten (Englisch, Skill bleibt `disable-model-invocation: true`)
  - Schritt 0: liest optional `plan_review.modelle` (Schluessel `architekt`, `pragmatiker`, `senior-dev`, `betriebs-waechter`; Werte = Modellname des Agent-Werkzeugs oder `null`); fehlt der Block → alle erben
  - Schritt 2: Aufloesung global → Projekt bleibt woertlich (Kopplung `feature-fast:105`); der Satz „Nimm diese Rollen fuer die Diskussion ein." wird ersetzt durch: Rollentexte werden als Prompt-Material fuer Schritt 3 gehalten

#### Schritt 1.2: Schritt 3 neu — Dispatch, Rueckgabe-Pruefung, Zusammenfuehrung
- **Zweck:** Kern des Features — unabhaengige Rollen-Urteile
- **Dateien:** `skills/dtb-plan-review/SKILL.md` (Schritt 3, Schritt 4)
- **Input:** Schritt 1.1; Vorbild `skills/dtb-impl-review/SKILL.md:133-162`
- **Output:**
  - **3a Dispatch:** je aktiver Rolle ein Subagent (Typ `general-purpose`), alle in EINER Nachricht parallel; `model` aus Schritt 0, sonst weglassen. Inline-Auftragsvorlage: Rollentext; Pfade von `plan.md`/`spec.md` (Agent liest selbst); Grounding- und Challenger-Ergebnisse (2d/2e); gefilterte Lektionen-Regeln (2b); „nur lesen — nichts schreiben, keine Kommandos"; die Runden-Definitionen 1–4 fuer DIESE Rolle (inkl. ihrer Challenge-Technik); festes Rueckgabeformat (Runde 1–4, danach `Verdikt {Dimension}: PASS|WARN|FAIL — {1 Satz}` nur fuer die eigenen Dimensionen, optional `Einspruch zu {Dimension}: {1 Satz}`); max. 3 Fragen in Runde 4
  - **3b Warte-Regel:** Subagenten laufen im Hintergrund und melden sich einzeln — der Haupt-Skill wartet, bis alle M Rueckgaben eingetroffen sind; eine noch laufende Rolle wird NIE aus dem Hauptkontext gefuellt oder vorweggenommen; die Zahl N in `🤖 Subagenten: {N}/{M}` zaehlt nur Rollen, deren Rueckgabe tatsaechlich vom Subagenten kam
  - **3b Rueckgabe-Pruefung + Fallback:** Agent-Werkzeug fehlt → alle Rollen im Hauptkontext wie bisher, eine ⚠-Zeile; einzelne Rueckgabe fehlt/unbrauchbar (Verdikt fehlt, fremde Dimension bewertet, Zwischenstufe) → diese Rolle im Hauptkontext nachholen, ⚠-Zeile `⚠ Rolle {Name} im Hauptkontext ({Grund})`; unbekannter Modellwert → erben + ⚠-Zeile; das Review bricht nie ab
  - **3c Zusammenfuehrung:** Rueckgaben unveraendert in die Runden-Abschnitte einsetzen; der Haupt-Skill fuegt den Runden keine eigenen Befunde hinzu; gleiche Befunde mehrerer Rollen erst in `## Empfehlungen` zusammenfassen
  - Schritt 4: Verdikte stammen aus den Rueckgaben (Regel „erst nach Runde 3" gilt je Subagent); Einspruchs-Regel: die Reaktion schreibt der Haupt-Skill in einem Satz, gekennzeichnet `Reaktion (Haupt-Skill, {zustaendige Rolle}):`; Gesamt-Verdikt-Regel unveraendert

#### Schritt 1.3: Output-Format und „Wichtig"
- **Zweck:** Isolation im Report sichtbar machen, Ausfuehrungsregeln an den neuen Ablauf anpassen
- **Dateien:** `skills/dtb-plan-review/SKILL.md` (Output-Format, „Wichtig")
- **Input:** Schritt 1.2
- **Output:**
  - Kopfblock des Output-Formats um `🤖 Subagenten: {N}/{M} Rollen isoliert` (+ ⚠-Zeilen aus 3b) ergaenzt
  - „Wichtig": „Rollen einhalten" → Isolation (keine Rolle sieht die Rueckgabe einer anderen; der Haupt-Skill ordnet nur an); „Keine Datei-Erstellung" um „Subagenten schreiben nie" ergaenzt; Rest unveraendert

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Config-Block `plan_review.modelle`
- **Zweck:** Optionales Modell je Rolle (Spec: Success Criterion Modellwahl) — vor dem Probelauf, damit 1.5 den Modellpfad ausfuehren kann (plan-review 2026-11-27)
- **Dateien:** `workflow.config.yaml`, `skills/dtb-project-init/SKILL.md` (Config-Vorlage)
- **Input:** Schluessel aus Schritt 1.1
- **Output:** in beiden Dateien derselbe Block nach `lessons:` — `plan_review:` / `modelle:` mit den vier Rollen-Schluesseln, je `null` und Kommentar `# dtb:plan-review — Modell je Rolle; null = Session-Modell erben`

#### Schritt 1.5: Probelauf an einer Kopie eines echten Plans
- **Zweck:** Brauchbarkeit des Reports am echten Material belegen, bevor die Doku nachgezogen wird (L64); Manual-Kriterium an ein Objekt gebunden, das der Lauf selbst erzeugt (L57); Modellpfad und ⚠-Pfad fuer unbekannte Werte ausfuehren
- **Dateien:** `features/zz-test-plan-review-probe/` (temporaer: Kopie von `archive/skill-lint/plan.md` + `spec.md`), `workflow.config.yaml` (temporaer), `features/plan-review-subagenten/plan.md` (Abschnitt `## Probelauf-Protokoll`)
- **Input:** Schritte 1.1–1.4
- **Output:**
  - Probeordner angelegt; in `workflow.config.yaml` vorlaeufig `pragmatiker: haiku` und `senior-dev: ungueltig-probe` gesetzt (erwartet: Pragmatiker laeuft mit `haiku`, Senior Dev erbt + ⚠-Zeile)
  - der Mensch setzt als EINEN Handgriff ab: „Lies {worktree}/skills/dtb-plan-review/SKILL.md vollstaendig und fuehre ihn aus fuer zz-test-plan-review-probe" (Repo-Fassung, nicht `~/.claude/` — L74/L133); Findings des Probelaufs werden abgelehnt (die Kopie wird nicht ueberarbeitet)
  - `## Probelauf-Protokoll` in diesem Plan: Datum, `🤖`-Zeile, ⚠-Zeilen, Gesamt-Verdikt, Abnahme-Urteil des Menschen, Beurteilung des offenen Punkts (Einspruch-Reaktion), Pflichtzeile `- ungeprueft: Werkzeug fehlt, Rueckgabe unbrauchbar` (nicht herbeifuehrbare Fallback-Pfade, L135)
  - beide Probewerte zurueck auf `null`; Probeordner entfernt (Bash `rm -r`; lehnt der Auto-Modus ab → Befehl an den Menschen, L58)

### Deliverables
- [ ] `skills/dtb-plan-review/SKILL.md` mit Subagenten-Dispatch, Warte-Regel, Fallback und Zusammenfuehrung
- [ ] `plan_review:`-Block in `workflow.config.yaml` und project-init-Vorlage
- [ ] `## Probelauf-Protokoll` in diesem Plan

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '^allowed-tools: .*Agent' skills/dtb-plan-review/SKILL.md` = 1
- [ ] `grep -c '^  consumes: .*workflow.config.yaml' skills/dtb-plan-review/SKILL.md` = 1
- [ ] `sed -n '/^## Schritt 2: /,/^## Schritt 2b/p' skills/dtb-plan-review/SKILL.md | grep -c 'Nimm diese Rollen'` = 0
- [ ] `sed -n '/^## Schritt 2: /,/^## Schritt 2b/p' skills/dtb-plan-review/SKILL.md | grep -c 'Aufloesung je Datei'` = 1 (Kopplung `feature-fast:105`)
- [ ] `sed -n '/^## Schritt 3/,/^## Schritt 4/p' skills/dtb-plan-review/SKILL.md | grep -c 'general-purpose'` ≥ 1
- [ ] `sed -n '/^## Schritt 3/,/^## Schritt 4/p' skills/dtb-plan-review/SKILL.md | grep -c 'nie aus dem Hauptkontext'` ≥ 1 (Warte-Regel)
- [ ] `grep -c '🤖 Subagenten:' skills/dtb-plan-review/SKILL.md` ≥ 2 (Ablauf + Output-Format)
- [ ] `grep -c '^## Probelauf-Protokoll' dtb-project/project-workflows/features/plan-review-subagenten/plan.md` = 1
- [ ] `grep -c '^- ungeprueft: ' dtb-project/project-workflows/features/plan-review-subagenten/plan.md` = 1
- [ ] `test ! -d dtb-project/project-workflows/features/zz-test-plan-review-probe` (Probeordner entfernt)
- [ ] `grep -c '^plan_review:' workflow.config.yaml` = 1
- [ ] `grep -c '^plan_review:' skills/dtb-project-init/SKILL.md` = 1
- [ ] `sed -n '/^plan_review:/,/^[a-z]/p' workflow.config.yaml | grep -cE 'haiku|ungueltig-probe'` = 0 (Probewerte zurueckgesetzt)
- [ ] `python scripts/lint-skills.py` Exit 0

#### Manual
- [ ] Probelauf-Report abgenommen: Rollen erkennbar unabhaengig, Format wie bisher, Verdikt nachvollziehbar; Pragmatiker lief mit `haiku`, fuer Senior Dev erschien die ⚠-Zeile
- [ ] Offener Punkt entschieden: Ein-Satz-Reaktion des Haupt-Skills auf Einsprueche reicht — oder Folge-Idee

---

## Phase 2: Doku-Spiegel, Lint + Gegenprobe

### Ziel
Alle Beschreibungen von plan-review und den Rollendateien stimmen mit dem neuen Ablauf ueberein.

### Schritte

#### Schritt 2.1: Doku-Spiegel
- **Zweck:** Beschreibungen ausserhalb des Skills nachziehen (L3)
- **Dateien:** `agents/CLAUDE.md`, `CLAUDE.md`, `README.md`
- **Input:** Phase 1
- **Output:**
  - `agents/CLAUDE.md`: Zweck-Satz → Rollendateien sind Prompt-Material fuer isolierte Subagenten; Hinweis „bewusst ohne Frontmatter — sonst registriert Claude Code sie als globale Agent-Typen in jeder Session" (Kernfrage 2026-11-27)
  - `CLAUDE.md` „### Agent Roles": plan-review startet je Rolle einen isolierten Subagenten
  - `README.md:79`: Zeile nennt die isolierten Subagenten je Rolle

#### Schritt 2.2: Lint, Selbsttest und repo-weite Gegenprobe
- **Zweck:** Frontmatter- und Kopplungsregeln belegen, keine veraltete Beschreibung zuruecklassen
- **Dateien:** keine (Pruefschritt) — Ergebnis in diesem Plan unter `## Probelauf-Protokoll` als Zeile `- Gegenprobe Phase 2: …` (L20)
- **Input:** Schritt 2.1
- **Output:** `python scripts/lint-skills.py` und `python -m unittest discover -s scripts/tests` gruen; `grep -rn "plan-review" --include=*.md skills/ agents/ CLAUDE.md README.md` gesichtet — jede Fundstelle, die das alte Rollenspiel in einem Kontext beschreibt, ist nachgezogen oder als gueltig begruendet; Ergebniszeile im Protokoll

> **3x3-Block:** Nach Schritt 2.2 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Nachgezogene Doku in `agents/CLAUDE.md`, `CLAUDE.md`, `README.md`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -ci 'subagent' agents/CLAUDE.md` ≥ 1
- [ ] `grep -n '/dtb:plan-review' README.md | grep -ci 'subagent'` = 1
- [ ] `python scripts/lint-skills.py` Exit 0
- [ ] `python -m unittest discover -s scripts/tests` Exit 0
- [ ] `grep -c '^- Gegenprobe Phase 2:' dtb-project/project-workflows/features/plan-review-subagenten/plan.md` = 1

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Traeger der Rollen | general-purpose + Rollentext im Prompt / native Agent-Typen per Frontmatter | general-purpose + Rollentext | Kernfrage 2026-11-27: Rollendateien bleiben unveraendert, Projekt-Fallback `agents/` funktioniert, keine globalen Agent-Typen in fremden Sessions |
| Einspruch-Reaktion | Haupt-Skill (1 Satz, gekennzeichnet) / zweite Subagenten-Runde | Haupt-Skill | per Veto-Vorlage bestaetigt 2026-11-27; Kosten/Laufzeit; Beurteilung am Manual-Gate Phase 1 |
| Zeitpunkt der Rollen-Verdikte | im Subagenten nach seiner Runde 3 / im Haupt-Skill | im Subagenten | per Veto-Vorlage bestaetigt 2026-11-27; die Rolle urteilt ueber ihre Dimensionen selbst, die feste Gesamt-Regel bleibt im Haupt-Skill |
| Ort der Modellwahl | Projekt-Config / Rollendatei / gar nicht | Projekt-Config `plan_review.modelle`, Default erben | per Veto-Vorlage bestaetigt 2026-11-27; Rollendateien bleiben ohne Frontmatter |
| Ausfall eines Subagenten | Abbruch / Rueckfall auf Hauptkontext | Rueckfall mit ⚠-Zeile | per Veto-Vorlage bestaetigt 2026-11-27; ein Review darf nie an der Werkzeug-Verfuegbarkeit scheitern |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Frontmatter, Schritt 0 und Schritt 2 — `3cdb61e`
- [x] 1.2 Schritt 3 neu (Dispatch, Rueckgabe-Pruefung, Zusammenfuehrung) — `3cdb61e`
- [x] 1.3 Output-Format und Wichtig — `3cdb61e`
- [x] 1.4 Config-Block plan_review.modelle — `3cdb61e`
- [x] 1.5 Probelauf an Plan-Kopie — `3cdb61e`
- [x] 2.1 Doku-Spiegel
- [x] 2.2 Lint, Selbsttest, Gegenprobe

---

## Probelauf-Protokoll

**Probelauf 2026-11-27** — Repo-Fassung `skills/dtb-plan-review/SKILL.md` gegen `features/zz-test-plan-review-probe/` (Kopie von `archive/skill-lint/plan.md` + `spec.md`), Probewerte `pragmatiker: haiku`, `senior-dev: ungueltig-probe`

- Kopfzeilen: `🤖 Subagenten: 4/4 Rollen isoliert` (Betriebs-Waechter aktiviert: neuer CI-Workflow); `⚠ plan_review.modelle.senior-dev: „ungueltig-probe" unbekannt — Rolle erbt das Session-Modell`
- Modellpfad: Pragmatiker mit `model: haiku` gestartet, die drei anderen ohne `model` (Beleg = Aufruf-Parameter; welches Modell tatsaechlich lief, zeigt die Rueckgabe nicht)
- Warte-Regel: Rueckgaben trafen einzeln ein (Pragmatiker, Betriebs-Waechter, Architekt, Senior Dev); zusammengefuehrt erst nach der vierten
- Gesamt-Verdikt: REVISE (7 WARN, 1 PASS), 5 Einsprueche, 12 Empfehlungen — darunter Befunde, die der Original-Review vom 2026-11-26 (3 WARNs) nicht hatte (u. a. Check 8 fuehrt fremden Code in Zielprojekten aus, `scripts/yaml.py`-Schatten ohne `-I`)
- Format-Treue: Architekt, Senior Dev, Betriebs-Waechter exakt; Pragmatiker (`haiku`) mit doppelten `VERDIKT`-Zeilen, `RUNDE 4` hinter den Verdikten und einem Einspruch gegen eine Nicht-Dimension („Grounding/Konsistenz") — nach 3c verwertbar, aber vom Skill nicht geregelt
- Abweichungen des Haupt-Skills: (1) statt aller 87 gefilterten Lektionen (18 KB) je Rolle eine vorausgewaehlte Teilmenge mitgegeben — Vorpraegung durch den Hauptkontext; (2) Finding-Runde als Sammel-Nein auf Wunsch des Menschen (Probe-Kopie)
- Kosten: 80–111 Tsd. Subagenten-Tokens je Rolle, 64–95 s je Rolle (parallel)
- ungeprueft: Werkzeug fehlt, Rueckgabe unbrauchbar (beide Rueckfall-Pfade aus 3c nicht herbeifuehrbar)
- Manual-Gate 2026-11-27 → Korrekturen (Mensch): (1) Lektionen als Pfad + Filterregel statt Volltext/Vorauswahl (Schritt 2b, Auftragsvorlage 3a); (2) identisch doppelte Zeilen und abweichende Reihenfolge gelten als verwertbar, widerspruechliche Verdikte derselben Dimension nicht (3c); (3) Einspruch ohne gueltige Dimension wird `Hinweis` ohne Verdikt-Wirkung (Schritt 4). Einspruch-Reaktion in einem Satz reichte in allen 5 Faellen — offener Punkt entschieden: keine zweite Runde
- Gegenprobe Phase 2: 2026-11-27 — Pruefrage: „Beschreibt die Fundstelle plan-review noch als Rollenspiel in einem Kontext oder widerspricht sie der Subagenten-Isolation?" `grep -rn "plan-review" --include=*.md skills/ agents/ CLAUDE.md README.md` ausserhalb von `skills/dtb-plan-review/`, auf Rollen-/Agent-/Kontext-Begriffe gefiltert: 19 Treffer. Nachgezogen in 2.1: `agents/CLAUDE.md`:5/:11, `CLAUDE.md`:61/:73, `README.md`:79. Gueltig ohne Aenderung: `agents/{architekt,pragmatiker,senior-dev,betriebs-waechter}.md` „Verdikt-Pflicht (plan-review)" (die Einspruchs-Form steht im Auftrag der Subagenten), `agents/CLAUDE.md`:34-41 (Tabelle, Ensemble-Groesse), `skills/dtb-project-init/SKILL.md`:120 (neuer Config-Kommentar), `skills/dtb-feature-fast/SKILL.md`:105 („Muster wie plan-review Schritt 2" — Aufloesung global → Projekt unveraendert), `skills/dtb-impl-plan/SKILL.md`:85 (Grounding 2d unveraendert), `skills/CLAUDE.md`:347 (Z7, Schritt 5 unveraendert), `skills/dtb-pipeline-graph/SKILL.md`:206 (kein plan-review-Bezug, Treffer ueber „Kontext"). Lint Exit 0 (45 Skills), Selbsttest 37 Tests OK

---

## Umsetzung

Umsetzung mit `/dtb:implement plan-review mit Subagenten` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/plan-review-subagenten/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-27)
