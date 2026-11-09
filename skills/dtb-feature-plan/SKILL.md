---
name: dtb:feature-plan
description: >-
  Use when: "Feature planen", "feature plan", "Feature-Spec erstellen",
  "neues Feature dokumentieren". Creates a structured feature specification
  from the current chat discussion and saves it as features/<slug>/spec.md, then
  runs dtb:impl-plan by reference to create features/<slug>/plan.md in the same
  run (stop after the spec with the argument "nur-spec").
disable-model-invocation: true
argument-hint: "[Feature-Name] [nur-spec]"
allowed-tools: Read, Write, Glob, Grep
pipeline:
  stage: planning
  after: [dtb:feature-discover]
  next: [dtb:plan-review, dtb:impl-plan]
  consumes: [INBOX.md, features/*/discovery.md, workflow.config.yaml, project-rules/lessons.md, project-rules/DERIVED_STATE_RULES.md]
  produces: [features/*/spec.md, features/*/plan.md, INBOX.md, BACKLOG.md]
---

# Feature-Plan erstellen

Du bist ein Feature-Plan-Manager. Deine Aufgabe ist es, den aktuell diskutierten Feature-Plan als strukturierte Spec-Datei zu speichern — und danach im selben Lauf den Implementierungsplan zu erstellen, indem du `dtb:impl-plan` per Referenz ausfuehrst (Ausfuehrungs-Punkt 8a).

**Stopp-Weiche „nur spec.md":** Ist `nur-spec` das **letzte Argument-Token** des Aufrufs, oder
bittet der Mensch ausserhalb des Feature-Namens ausdruecklich nur um die Spec („nur spec",
„ohne Plan"), ueberspringst du den Plan-Teil (Punkt 8a); Punkt 9–11 laufen normal, naechster
Schritt `/dtb:impl-plan`. Das Token `nur-spec` entfernst du **vor** der Ableitung von
Feature-Name und Slug (Punkt 3) — es ist nie Teil des Namens. Ohne diese Angabe laeuft der Plan-Teil **immer** mit; es gibt dafuer
**keine Rueckfrage** (eine Frage wuerde die Kette nicht verkuerzen — Grund des Features
`plan-in-einem-befehl`).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Aufgabe

1. **Analysiere den Chat-Verlauf** und identifiziere den diskutierten Feature-Plan
2. **Strukturiere den Plan** nach dem unten stehenden Template
3. **Speichere** in `{config.paths.workflows}/features/{slug}/spec.md`
4. **Erstelle den Implementierungsplan** `{config.paths.workflows}/features/{slug}/plan.md` per
   Referenz auf `dtb:impl-plan` (Ausfuehrung Punkt 8a) — entfaellt bei der Stopp-Weiche „nur spec.md"
5. **Trage das Feature in BACKLOG.md ein** — ohne Rueckfrage, mit Anzeige-Zeile (Ausfuehrung Punkt 10)

## Template fuer spec.md

> **Wartungs-Hinweis (Struktur-Anker):** Diese Sektion samt Template (und der
> Technical-Leak-Lint unten) werden von `dtb:feature-fast` referenziert (Grep auf
> `## Template fuer spec.md`). Bei Umbenennung oder Umbau den Struktur-Check dort mitziehen.

Verwende folgende Struktur:

```markdown
# Feature: [Feature-Name]

**Erstellt:** [Datum]
**Ziel:** [Hauptziel in einem Satz]
**Prioritaet:** Hoch / Mittel / Niedrig
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

[2-3 Saetze: Was wird gemacht und warum?]

---

## Scope / Abgrenzung

### Enthalten
- [Was gehoert zu diesem Feature?]

### Nicht enthalten
- [Was gehoert explizit NICHT dazu?]

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| [Risiko 1] | Hoch/Mittel/Niedrig | Hoch/Mittel/Niedrig | [Loesung] |

---

## Dependencies

### Erforderlich vor Start
- [ ] [Dependency 1]
- [ ] [Dependency 2]

### Referenz-Dokumente
- `[Datei 1]` - [Beschreibung]
- `[Datei 2]` - [Beschreibung]

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

## Offene Punkte

- [Beim Schreiben ungeklaerte Fragen — als konkrete Frage formulieren, NICHT plausibel erraten. "— keine —", wenn nichts offen ist]
- [Gehoert eine Frage ins Fach-Meeting (nicht sofort/allein beantwortbar)? → als Checkbox mit Tag: `- [ ] [Fach] {Frage}`. Ein normaler „selbst-zu-klaeren"-Punkt bleibt untagged (reiner Bullet ohne Checkbox). Kanon/Details: `DERIVED_STATE_RULES.md` §6]

---

**Erstellt mit:** `/dtb:feature-plan`
```

---

## Wichtig - Anweisungen fuer die Ausfuehrung

### Beim Ausfuehren des Commands:

1. **Discovery pruefen (optional):**
   - Suche `{config.paths.workflows}/features/{slug}/discovery.md` (Slug aus dem Feature-Namen, §4)
   - Falls vorhanden: Lies die Discovery-Datei und uebernimm Scope, betroffene Module, Anforderungen und Abhaengigkeiten als Ausgangsbasis fuer die Feature-Spec
   - Falls nicht vorhanden: Ueberspringe diesen Schritt ohne Hinweis

2. **Inbox pruefen:**
   - Lies `{config.paths.workflows}/INBOX.md`
   - Filtere alle Eintraege mit Status `Offen`
   - Falls offene Ideen vorhanden, zeige:
     ```
     Offene Ideen in der Inbox:
       1. #{N} — {Idee-Text} ({Datum})
       2. #{N} — {Idee-Text} ({Datum})
       ...

     Idee auswaehlen (Nummer) oder neues Feature beschreiben:
     ```
   - Falls Inbox nicht existiert oder keine offenen Ideen: Ueberspringe diesen Schritt ohne Hinweis
   - **Bei Auswahl einer Idee:**
     - Verwende den Idee-Text als Ausgangsbasis fuer die Feature-Diskussion
     - Setze den Inbox-Status auf `In Arbeit` (Teil-Guard: im verlinkten Worktree diesen
       Flip NICHT ausfuehren — Hinweiszeile gemaess dem Teil-Guard-Block in Schritt 9,
       in den Hand-off aufnehmen)

3. **Feature-Name / Slug ermitteln:**
   - Frage den Benutzer nach dem Feature-Namen falls nicht klar
   - Leite den **kebab-case-Slug** ab (Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4; z.B. "Chat History" → `features/chat-history/`)
   - Bei Slug-Kollision mit einem bestehenden Ordner (anderer Name, gleicher Slug) → melden und anderen Namen erfragen (§4, kein Auto-Suffix)

4. **Prüfe ob `features/{slug}/spec.md` existiert:**
   - Falls JA: Frage "Soll ich die existierende Spec ueberschreiben oder aktualisieren?"
   - Falls NEIN: Lege den Ordner `features/{slug}/` bei Bedarf an und erstelle `spec.md`

5. **Analysiere den Chat-Verlauf:**
   - Identifiziere Ziel, Scope und Abgrenzung
   - Finde Risiken und Dependencies
   - Sammle Success Criteria

6. **Fuelle das Template:**
   - Nutze konkrete Informationen aus dem Chat
   - **Nie erfinden:** Fehlt eine Information, fuelle sie NICHT mit einer plausiblen Annahme.
     Trage sie stattdessen als konkrete Frage unter `## Offene Punkte` ein. Eine ehrliche
     Luecke ist besser als ein verstecktes Rateergebnis. Kein `[TODO]`-Platzhalter mehr.
     **Zwei Renderings, drei Intents:** untagged Bullet fuer (a) normaler offener Punkt und
     (b) diese „nie erfinden"-Luecke (fehlende Info, oft in der Spec selbst klaerbar); getaggt
     `- [ ] [Fach] {Frage}` nur fuer (c) Frage fuers Fach-Meeting (nicht sofort/allein
     beantwortbar). Nur (c) traegt Tag und Checkbox (Kanon: `DERIVED_STATE_RULES.md` §6).
   - Fokus auf Was/Warum, nicht auf Wie (Implementierungsdetails gehoeren in `plan.md`)
   - **Max. 500 Zeilen** — laengere Specs verschlechtern die AI-Verarbeitung. Bei komplexen Features: Details in `plan.md` auslagern

7. **Technical-Leak-Lint (Pflicht vor dem Speichern):**
   - Wende den Lint aus Abschnitt „## Technical-Leak-Lint" (unten) auf den fertigen Spec-Text an
   - **Treffer → Hard-Block:** Datei NICHT speichern; melde die Funde im Meldeformat und korrigiere, dann erneut pruefen
   - Override nur mit Begruendung + Markierung an der Stelle (siehe Abschnitt)

8. **Speichere die Datei**

8a. **Implementierungsplan mitlaufen lassen (`dtb:impl-plan` per Referenz):**

   Die Nummer `8a` ist Absicht: Punkt 9–11 behalten ihre Nummern, weil andere Skills und
   `skills/CLAUDE.md` sie zitieren (z.B. „analog feature-plan Schritt 10").

   **(a) Stopp-Weiche:** Gilt „nur spec.md" (Abschnitt oben unter dem Titel) → diesen Punkt
   ueberspringen, weiter mit Punkt 9. Ausgang fuer Punkt 10/11: **nur Spec**.

   **(b) Struktur-Check vor der ersten Nutzung:** Du fuehrst die Regeln von `dtb:impl-plan` aus,
   ohne sie zu kopieren — deshalb pruefst du zuerst, ob die genutzten Abschnitte dort noch stehen.
   Quelle aufloesen: zuerst die installierte Kopie `~/.claude/skills/dtb-impl-plan/SKILL.md`,
   sonst `skills/dtb-impl-plan/SKILL.md` im Projekt-Root (Kit-Repo-Fall). Dann je Anker ein
   Grep (Regex fuer das Grep-Werkzeug/ripgrep, zeilenverankert — nicht als Festtext und nicht als
   BRE uebernehmen, dort waere `\(` ein Gruppen-Start):

   | Anker (Grep) | Genutzt fuer |
   |--------------|--------------|
   | `^## Lektionen als Prior lesen` | Lektionen-Prior des Plans |
   | `^## Codebase-Research \(Ist-Analyse\)` | Ist-Analyse (Uebernahme aus `discovery.md` oder Scan) |
   | `^## Template fuer plan\.md` | Zielstruktur von `plan.md` |
   | `^## Wichtig - Anweisungen fuer die Ausfuehrung` | Regeln der Planerstellung |
   | `^## Lektion-Kandidat erkennen \(Vorschlager\)` | Vormerkung von Lektion-Kandidaten |

   Alle fuenf gefunden → genau eine Zeile `🧩 Struktur-Check impl-plan: 5/5 Anker gefunden`, weiter
   mit (c). **Zwei getrennte Fehlerpfade** (nie vermischen — eine fehlende Installation ist keine
   Drift):
   1. **Datei in beiden Quellen nicht gefunden:**
      ```
      ⚠ impl-plan weder global (~/.claude/skills/) noch im Projekt gefunden — Plan-Teil entfaellt.
         → /dtb:kit-sync sync ausfuehren (bzw. install), dann /dtb:impl-plan {Feature-Name}
      ```
   2. **Datei vorhanden, Anker fehlt:**
      ```
      ⚠ Struktur-Check impl-plan fehlgeschlagen: Anker "{Anker}" nicht gefunden — Plan-Teil entfaellt.
         impl-plan hat sich strukturell geaendert; ich plane NICHT auf veralteter Basis.
         → dtb:feature-plan Punkt 8a an die neue Struktur anpassen; bis dahin: /dtb:impl-plan {Feature-Name}
      ```
   In beiden Faellen bleibt die gespeicherte `spec.md` gueltig; weiter mit Punkt 9, Ausgang
   fuer Punkt 10/11: **nur Spec**.

   **(c) Ausfuehren:** Lies die aufgeloeste `dtb-impl-plan/SKILL.md` und wende ihre Abschnitte
   **per Name** (nie per Punktnummer) mit demselben Slug an:
   - `## Lektionen als Prior lesen` — inklusive der einen `📚`-Zeile
   - `## Codebase-Research (Ist-Analyse)` — verwertbare Modul-Liste aus `discovery.md`
     uebernehmen (`📂`-Zeile) oder Scan mit Bestaetigung, wie dort beschrieben
   - `## Wichtig - Anweisungen fuer die Ausfuehrung` **der impl-plan-Datei** (nicht der
     gleichnamige Abschnitt dieses Skills, in dem du gerade stehst) — alle Punkte **ausser** deren
     Punkten **Feature-Name / Slug ermitteln** (der Slug steht seit Punkt 3 fest),
     **Codebase-Research (Ist-Analyse) durchfuehren/uebernehmen** (durch den Listenpunkt oben
     bereits erledigt — kein zweiter Scan) und **Bestaetige** (es gibt eine gemeinsame in
     Punkt 11). Es gelten also auch die Ueberschreib-Frage bei vorhandenem `plan.md` und die
     Planerstellung nach `## Template fuer plan.md`
   - `## Lektion-Kandidat erkennen (Vorschlager)`

   Das Eligibility-Gate von `dtb:impl-plan` entfaellt still: `spec.md` ist in Punkt 8 im selben
   Lauf entstanden. `plan.md` wird inhaltlich genau so wie bei einem Einzel-Lauf von
   `dtb:impl-plan` — inklusive dessen Fusszeile `**Erstellt mit:** \`/dtb:impl-plan\``.

   **Ausgang fuer Punkt 9–11 — am Artefakt, nicht am Weg:** **Durchlauf** gilt genau dann, wenn
   `plan.md` in diesem Lauf geschrieben wurde (neu oder per „ueberschreiben/aktualisieren").
   Lehnt der Mensch die Ueberschreib-Frage ab, gilt **nur Spec** — der vorhandene Plan bleibt
   unangetastet und wird nicht als „gespeichert" gemeldet.

   > **Wartungs-Hinweis (Kopplung):** Dieser Punkt fuehrt `dtb:impl-plan` per Referenz aus. Die
   > fuenf Anker oben tragen dort je einen Gegen-Hinweis. Wird ein Abschnitt in `dtb:impl-plan`
   > umbenannt oder umgebaut, Tabelle und Liste hier mitziehen.

9. **Inbox-Status aktualisieren:**

   **Teil-Guard (Worktree):** Laeuft dieser Skill in einem verlinkten Worktree
   (die Guard-Pruefung aus `skills/CLAUDE.md` → „Worktree-Guard (kanonische Vorlage)"
   meldet `WORKTREE`), Schritt 9 UND 10 NICHT ausfuehren — stattdessen genau eine
   Hinweiszeile `↷ INBOX.md-/BACKLOG.md-Update uebersprungen (Worktree) — in den Hand-off
   aufnehmen` und normal weiterarbeiten (Schreibgrenzen-Regel: `skills/CLAUDE.md` →
   „Parallele Sessions"). Gilt auch fuer den Status-Flip in Schritt 2 (Inbox-Auswahl).

   - Falls das Feature aus einer Inbox-Idee erstellt wurde:
     - Setze den Status in `INBOX.md` auf `Ausgearbeitet`
     - Ergaenze die Idee-Zeile um den Link: `→ features/{slug}/spec.md`; bei Ausgang
       **Durchlauf** (Punkt 8a) zusaetzlich `→ features/{slug}/plan.md`

10. **Backlog-Eintrag (ohne Rueckfrage):**

   Keine Frage — der Eintrag ist der Default (0 belegte „Nein" in realen Laeufen; eine
   BACKLOG-Zeile ist eine abgeleitete Anzeige und per Zeilen-Loeschung billig umkehrbar).
   Ergebnis ist genau eine Anzeige-Zeile, die als `{Backlog-Zeile}` in der Bestaetigung
   (Punkt 11) erscheint: `→ in BACKLOG.md eingetragen (Status: {Status})`. Im Worktree
   entfaellt sie — dort steht die ↷-Hinweiszeile des Teil-Guards (Punkt 9).

   **`{Status}` wird aus den Dateien abgeleitet** (Regeln: `DERIVED_STATE_RULES.md` — vorhandene
   Artefakte in `features/{slug}/` + `## Progress` in `plan.md`), nie aus dem Weg durch Punkt 8a
   gesetzt. Normalfaelle: Ausgang **Durchlauf** mit frischem Plan (0 Progress-Haken) → `Geplant`;
   Ausgang **nur Spec** ohne vorhandenen Plan → `Spezifiziert`. Ein bereits vorhandener oder
   aktualisierter Plan mit Haken ergibt den dort abgeleiteten Status (z.B. `In Arbeit`).

   **Testordner-Ausnahme:** Beginnt der Slug mit `zz-test-` oder `abnahmeprobe-` → KEIN
   Eintrag, stattdessen die Anzeige-Zeile `→ kein BACKLOG-Eintrag (Testordner)`.

   **BACKLOG.md fehlt oder ist unlesbar** → kein Eintrag, kein Abbruch, genau die Zeile
   `⚠ BACKLOG.md fehlt oder ist unlesbar — kein Eintrag, weiter` (`/dtb:backlog-status`
   erkennt `features/*/spec.md` ohnehin).

   **Eintrag schreiben:**
   - Lies `{config.paths.workflows}/BACKLOG.md`
   - Die Status-Spalte ist eine **abgeleitete Anzeige** (Regeln: `project-rules/DERIVED_STATE_RULES.md`):
     trage den abgeleiteten Status `{Status}` ein (siehe oben; Normalfall `Geplant` bzw. `Spezifiziert`).
     Danach pflegt `dtb:workflow-checkpoint` das Feld; manuell gepflegt werden nur Prio und Ziel
   - Bestimme Ziel-Abschnitt anhand des Status:
     - Status "Idee" → "Ideen / Backlog"
     - Alle anderen (Geplant, In Arbeit, etc.) → "Aktive Features"
   - Fuege eine neue Zeile in die entsprechende Tabelle ein:
     `| {INBOX-Nr oder —} | {Feature-Name} | {Status} | {Prio} | features/{slug}/spec.md | {Ziel aus Executive Summary} |`
   - **Spalte `#` (INBOX-Nummer):** die Nummer der in Schritt 2 gewaehlten Idee; sonst die
     Nummer aus `**Idee-Referenz:** Inbox #{N}` der `discovery.md` (Schritt 1); sonst `—`.
     Nackte Zahl (`107`, nicht `#107`)
   - **Kopf ohne `#`** (Bestandsprojekt, Tabelle noch im alten Format) → Zeile im alten Format
     ohne erste Spalte schreiben, nicht selbst umbauen — `dtb:workflow-checkpoint` ergaenzt die
     Spalte und fuellt die Nummer nach
   - Aktualisiere das Datum in "Letzte Aktualisierung"

   (Form-Kanon fuer Autoren: `skills/CLAUDE.md` → „Rueckfragen-Defaults (Veto-Form)", Zeile Z3.)

11. **Bestaetige** — genau eine gemeinsame Abschlussmeldung, Variante nach dem Ausgang von
   Punkt 8a (die eigene Bestaetigung von `dtb:impl-plan` entfaellt):

   Ausgang **Durchlauf**:
   ```
   Feature gespeichert: {config.paths.workflows}/features/{slug}/spec.md
   Implementierungsplan gespeichert: {config.paths.workflows}/features/{slug}/plan.md
   {Backlog-Zeile}

   Naechster Schritt: /dtb:plan-review [Feature-Name]
   ```

   Ausgang **nur Spec** (Stopp-Weiche oder ausgefallener Plan-Teil — dessen ⚠-Meldung steht
   dann schon darueber):
   ```
   Feature gespeichert: {config.paths.workflows}/features/{slug}/spec.md
   {Backlog-Zeile}

   Naechster Schritt: /dtb:impl-plan [Feature-Name]
   ```

---

## Technical-Leak-Lint

Prueft den fertigen Spec-Text unmittelbar vor dem Speichern (Ausfuehrungs-Schritt 7). Ziel: die
Spec beschreibt das **Was/Warum**, nicht das **Wie**. Ein Treffer bricht den Write ab (Hard-Block).

> **Kopie-Hinweis (Format-Kopplung):** Diese 7 Kategorien sind bewusst auch in
> `dtb:greenfield-prd` (Selbst-Review Schritt 4b) dupliziert — kein Import-Mechanismus,
> je eine eigenstaendige SKILL.md. Aenderst du die Kategorien hier, den Lint in
> `greenfield-prd` mitdenken (dort steht der Gegen-Hinweis). Unterschied dort: der
> Redirect zeigt auf `TECH-STACK.md` statt auf loesungsneutrale Formulierung.

**7 Leck-Kategorien** (je 1 Beispiel → loesungsneutrale Alternative):

| # | Kategorie | Leck (verboten) | Stattdessen |
|---|-----------|-----------------|-------------|
| 1 | Vendor-/Produktname | „in PostgreSQL/Redis/S3 speichern" | „persistent speichern" |
| 2 | ORM-/Query-Notation | „`User.objects.filter()`", „`SELECT …`" | „Nutzer nach Kriterium finden" |
| 3 | Transport/Protokoll | „per REST `POST /users`", „WebSocket" | „Nutzer legt Datensatz an" |
| 4 | Implementierungs-Verb | „instanziiere", „iteriere", „caste" | „das System verarbeitet …" |
| 5 | Konkrete Datenstruktur | „`Dict[str, List]`", „Array von Objekten" | „Zuordnung von X zu Y" |
| 6 | Framework-/Library-Name | „mit React/FastAPI/Pydantic" | „Oberflaeche/Schnittstelle …" |
| 7 | Datei-/Pfad-/Klassenname | „`services/auth.py`", Klasse `AuthManager` | „im Authentifizierungs-Teil" |

**Meldeformat bei Treffern** (Hard-Block, Datei NICHT speichern):
```
❌ Technical-Leak-Lint: {N} Leck(s) gefunden, Write abgebrochen
  {## Sektion} [{Kategorie}]: „{Fund}" → {loesungsneutraler Hinweis}
```
Zaehlung: ein Fund = eine leckende Phrase (nicht pro Wort). Trifft eine Phrase mehrere
Kategorien, melde nur die zutreffendste (keine Doppelzaehlung). Anker ist die Spec-Sektion
(`## …`) + Zitat, KEINE Zeilennummer (der Text ist beim Pruefen noch nicht gespeichert).
Danach korrigieren und erneut pruefen.

**Meta-Spec-Ausnahme (eng gefasst):** Beschreibt die Spec selbst ein Code-/Config-/Skill-Artefakt
als Gegenstand (Heuristik: Spec-Gegenstand bzw. betroffene Module sind Skill-/Code-Dateien — eine
`## Betroffene Module`-Sektion ist Indiz, nicht Pflicht), sind Referenzen *auf dieses Artefakt*
legitim — inkl. aus `discovery.md` geerbter technischer Angaben. **Ebenfalls nie ein Leck:**
Namen des Skill-/Workflow-Systems selbst (Skill-Namen wie `feature-discover`, Konventionen wie
`## Offene Punkte`), unabhaengig vom Gegenstand. Technische Details ueber *andere*,
nicht-gegenstaendliche Fach-Loesungen bleiben Lecks.

**Override:** Ein bewusst gehaltener Fachbegriff (echte fachliche Anforderung, z.B. „Export nach
SAP") ist zulaessig — **nur mit kurzer Begruendung** und **Markierung an der Stelle** in der
erzeugten Spec: `<!-- Lint-Override: {Begruendung} -->`. Kein Override ohne Begruendung. Beim
erneuten Pruefen zaehlt eine mit gueltigem Marker versehene Stelle nicht mehr als Leck.
