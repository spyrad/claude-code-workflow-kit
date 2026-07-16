---
name: dtb:implement
description: >-
  Use when: "implementieren", "Plan umsetzen", "implement", "weiter umsetzen",
  "naechste Phase umsetzen", "Schritte umsetzen". Drives an implementation plan
  (features/<slug>/plan.md) phase by phase in the 3x3 rhythm and enforces the
  verification gate at each phase end: checkpoint criteria, manual confirmation,
  commit, SHA write-back into the flipped progress rows.
disable-model-invocation: true
argument-hint: "[Feature-Name oder Slug] [phase N]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
pipeline:
  stage: implementation
  after: [dtb:feature-start]
  next: [dtb:impl-review]
  consumes: [features/*/plan.md, features/*/spec.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md, workflow.config.yaml]
  produces: [features/*/plan.md]
---

# Plan umsetzen (Implementierungs-Treiber)

Du setzt einen Implementierungsplan phasenweise um und erzwingst das **Verifikations-Gate**
am Phasen-Ende. Die Commit-SHA in `## Progress` ist ein Verifikations-Beleg, kein blosser
Commit-Beleg (Regeln: `project-rules/DERIVED_STATE_RULES.md` §2).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `implement` oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen bei der Umsetzung still an
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei behaltene Lektionen mit gegensaetzlicher `Rule`): beide zeigen und den
  Widerspruch melden — nicht selbst aufloesen

## Schritt 1: Plan aufloesen

1. Ermittle den Slug aus dem Argument oder Chat-Kontext (Regeln:
   `{config.paths.rules}/DERIVED_STATE_RULES.md` §4). Unklar → Feature-Namen erfragen,
   DANN pruefen (nicht raten). Optionales zweites Argument `phase N` merken.
2. **Archiv-Weigerung:** Existiert `{config.paths.workflows}/archive/{slug}/` (und kein
   aktiver Ordner `features/{slug}/`) → harte Weigerung, KEINE Escape-Hatch:
   ```
   ⛔ Dieser Change ist archiviert (archive/{slug}/).
      Archivierte Plaene werden nicht wieder angefasst — starte einen neuen Change
      (/dtb:idea oder /dtb:feature-discover).
   ```

## Eligibility-Gate (Fit-Check am Eingang)

Hard-Gate — Konvention: `skills/CLAUDE.md` → „Eligibility-Gates".

Pruefe, ob das **kritische Artefakt** `{config.paths.workflows}/features/{slug}/plan.md`
existiert (Glob, slug-spezifisch — nicht der `*`-Wildcard). Fehlt es → Meldeblock ausgeben
und NICHT weiterarbeiten, bis der Nutzer die Escape-Hatch bestaetigt:

```
⛔ implement braucht einen Implementierungsplan, der fehlt.
   Geprueft: features/{slug}/plan.md — nicht gefunden.
   → Erstelle ihn zuerst: /dtb:impl-plan {Feature-Name}   (erzeugt von impl-plan)

   Fehlalarm (plan.md existiert doch) oder bewusst ohne fortfahren? „trotzdem fortfahren" bestaetigen.
```

Bei Bestaetigung: normal fortfahren. Sonst: hier stoppen (keine Umsetzung ohne Plan).

## Schritt 2: Plan laden & Einstieg bestimmen

1. **Lies den Plan vollstaendig** (`features/{slug}/plan.md`) und die Spec
   (`features/{slug}/spec.md`, falls vorhanden) als Kontext. Lies referenzierte Dateien
   der anstehenden Phase, bevor du sie aenderst.
2. **`## Progress` fehlt oder hat 0 Checkbox-Zeilen** (Altbestand) → Nachruestung anbieten
   (§1.4: eine Zeile pro Schritt N.M aus dem Plan ableiten, Nutzer bestaetigt) — kein Abbruch.
3. **Einstieg (abgeleitet, kein Sidecar):** Der erste nicht abgehakte Eintrag in `## Progress`
   ist der naechste Schritt; die aktuelle Phase ist die zugehoerige Phase N. Wurde `phase N`
   uebergeben → erster offener Schritt innerhalb dieser Phase.
   Alle Checkboxen abgehakt → melden („Fertig zum Testen — nichts umzusetzen") und auf
   `/dtb:workflow-checkpoint` verweisen.
4. **Kriterien-Check der anstehenden Phase (Alt-Plan-Fallback, §2 Regel 3):**
   - `### Checkpoint-Kriterien` vorhanden und in `#### Automated`/`#### Manual` geteilt → normal
   - Kriterien fehlen oder sind ungeteilt → **alle als Manual behandeln** (das Gate entfaellt
     nie, es wandert zum Menschen) + einmalig Nachruestung anbieten:
     `⚠ Phase {N} ohne (geteilte) Checkpoint-Kriterien — behandle alle als Manual. Nachruesten? (/dtb:impl-plan aktualisieren)`
5. **Status zeigen (kompakt):** Feature, Fortschritt X/Y, aktuelle Phase + Ziel, naechste
   Schritte. Dann in den Umsetzungs-Loop.

## Schritt 3: Umsetzungs-Loop (3x3-Rhythmus)

> Kanonische Beschreibung des Rhythmus — andere Skills (`dtb:feature-start`,
> `dtb:impl-plan`-Template) verweisen hierher statt ihn zu duplizieren.

1. **Implementiere max. 3 Schritte** aus dem Plan (in Plan-Reihenfolge; Phasengrenzen
   respektieren — der Block endet spaetestens am Phasen-Ende)
2. **Nach jedem umgesetzten Schritt — Flip-Bedingung pruefen (§2 Regel 3):**
   Kein Automated-Kriterium der Phase darf durch den Stand **verletzt** sein. Verletzt =
   pruefbar und rot bezogen auf die bereits umgesetzten Schritte; Kriterien, die erst
   spaetere Schritte der Phase liefern, gelten als **ausstehend**, nicht verletzt.
   Rot → erst fixen, dann abhaken.
3. **Checkbox flippen — OHNE SHA:** genau eine Zeile `- [ ] N.M …` → `- [x] N.M …`
   (Edit). Die SHA kommt erst beim Phasen-Ende-Ritual (Schritt 4). Eine geflippte Zeile
   ohne SHA ist mid-phase ein gueltiger Zwischenzustand (§2 Regel 4)
4. **Nur `## Progress` mutieren:** Phasen-Bloecke des Plans (Ziel, Schritte, Deliverables,
   Kriterien) sind waehrend der Umsetzung read-only — Abweichungen gehoeren in den
   Mismatch-Block (unten), nicht still in den Plan editiert
5. **Beruehrte Dateien merken (Touched-Set):** Jede per Edit/Write geaenderte Datei zur
   Merkliste der Phase hinzufuegen (`plan.md` gehoert immer dazu). Das Set ist die Basis
   des expliziten Stagings im Ritual — nie aus `git status` heuristisch stagen
6. **Nach dem Block:** kurz zusammenfassen, die naechsten max. 3 Schritte beschreiben,
   **stoppen und auf Feedback warten**. Sind alle Schritte der Phase geflippt → direkt
   ins Phasen-Ende-Ritual (Schritt 4)

**Mismatch-Handling (Plan ≠ Realitaet):** Wenn ein Schritt nicht wie geplant umsetzbar ist —
STOPPEN, nicht improvisieren:

```
Abweichung in Schritt {N.M}:
  Erwartet: {was der Plan sagt}
  Gefunden: {tatsaechliche Lage}
  Warum es zaehlt: {Konsequenz}

Optionen: (1) anpassen und fortfahren  (2) Schritt ueberspringen  (3) stoppen und neu planen (/dtb:impl-plan)
```

Nutzer entscheidet. Bei (1): Anpassung im Block-Fazit dokumentieren (Session-Log via
`/dtb:workflow-checkpoint`). Bei (3): Umsetzung hier beenden.

**Wiedereinstieg (Kontextverlust, neue Session):** `## Progress` ist der Wiedereinstiegspunkt —
Plan laden, der erste nicht abgehakte Schritt ist der naechste. Bereits geflippte Schritte
gelten als erledigt (nur bei konkretem Verdacht nachpruefen).

## Schritt 4: Phasen-Ende-Ritual (Verifikations-Gate)

Sobald alle Schritte einer Phase geflippt sind, laeuft dieses Ritual — **immer vollstaendig,
nie still uebersprungen**. Es macht die SHA zum Verifikations-Beleg.

1. **Automated-Kriterien pruefen:** Jedes `#### Automated`-Kriterium der Phase tatsaechlich
   ausfuehren (Kommando, Grep, Datei-Check) und das Ergebnis zeigen. Rot → fixen, dann erneut
   pruefen — NICHT weiter zu 2. (Alt-Plan-Fallback aus Schritt 2: alle Kriterien sind Manual →
   dieser Punkt entfaellt, alles wandert in Punkt 2)
2. **Manuelles Bestaetigungs-Gate:** Die `#### Manual`-Kriterien der Phase auflisten und auf
   explizite Bestaetigung des Nutzers warten. Genau EINE Bestaetigung pro Phase (schlank —
   nicht pro Schritt). Ohne Bestaetigung kein Commit:
   ```
   Phase {N} umgesetzt — Automated-Kriterien gruen:
   - {Kriterium: Ergebnis}

   Manuelle Pruefungen laut Plan:
   - [ ] {Manual-Kriterium}

   Bestaetige („passt") oder nenne Korrekturen — dann folgt der Phasen-Commit.
   ```
3. **Staging-Set berechnen:** Touched-Set der Phase (Schritt 3, Punkt 5) ∪ `{plan.md}`.
   Dann `git status --short`: dirty paths AUSSERHALB des Sets → melden und fragen —
   (1) nur geplantes Set stagen (Empfehlung), (2) alles stagen (Nutzer verantwortet den
   breiteren Scope), (3) abbrechen. Nie still mitbuendeln
4. **Explizit stagen:** `git add` mit den Pfaden des gewaehlten Sets — NIE `git add -A`
   oder `git add .`
5. **Leerer Diff?** `git diff --cached --quiet` → Exit 0 heisst: nichts zu committen
   (reine Doku-/Verifikations-Phase). Melden: `Phase {N} ohne Commit-Diff — Zeilen bleiben
   SHA-los (§2 Regel 4)`, Ritual bei Punkt 9 fortsetzen
6. **Commit-Message vorschlagen:** Repo-Stil aus `git log --oneline -5` ableiten; Default
   Conventional Commits: `<type>({slug}): <Phasen-Titel> (p{N})` mit kurzem Body
   (beruehrte Dateien, Kernaenderung). Nutzer kann Subject/Body ueberschreiben
7. **Committen — Sicherheitsregeln hart:** NIE `--force`, `--no-verify`, `--amend` oder
   Signing-Bypass. Schlaegt ein Hook fehl → Ursache fixen und NEUEN Commit erstellen.
   Shell-agnostisch: mehrzeilige Message per Bash-heredoc (`git commit -m "$(cat <<'EOF' …"`);
   in reinen PowerShell-Kontexten stattdessen Here-String (`git commit -m @'…'@`,
   schliessendes `'@` auf Spalte 0)
8. **Kurz-SHA lesen:** `git rev-parse --short HEAD`
9. **SHA-Rueckschreibung:** In JEDE waehrend der Phase geflippte Progress-Zeile die SHA
   nachtragen: `- [x] N.M Kurzname` → `` - [x] N.M Kurzname — `SHA` ``.
   Zeilen, die schon eine SHA tragen, ueberspringen (Resume-Sicherheit, kein Doppel-Suffix).
   Multi-Repo: Praefix-Format nach §2 Regel 5 (`` `repo-name@SHA` ``).
   Bei leerem Diff (Punkt 5): Rueckschreibung entfaellt, Zeilen bleiben SHA-los.
   Die Rueckschreibung selbst liegt danach im Working Tree und landet regulaer im
   naechsten Phasen-Commit; nach der LETZTEN Phase im Session-/Checkpoint-Commit
   (Hinweis an den Nutzer ausgeben)
10. **Touched-Set zuruecksetzen** — das Ritual ist pro Phase in sich geschlossen
11. **Naechste-Phase-Entscheidung:** Falls eine weitere Phase folgt, fragen:
    (1) direkt weiter mit Phase {N+1}, (2) Kontext klaeren — Wiedereinstiegs-Kommando
    `/dtb:implement {slug} phase {N+1}` ausgeben, in neuer Session fortsetzen,
    (3) erst Review (`/dtb:impl-review`)

## Schritt 5: Multi-Repo & Abschluss

**Multi-Repo (`config.repos` mit mehr als einem Eintrag):**
- Automated-Kriterien und Commits laufen im Repo des jeweiligen Schritts
  (`git -C {repo.path} …`); das Ritual laeuft pro beteiligtem Repo (je ein Commit),
  die SHA-Zuordnung folgt §2 Regel 5 (Repo-Praefix)
- Bei genau einem Repo: alles still im Projekt-Repo, kein Praefix

**Nach der letzten Phase (alle Checkboxen geflippt):**
1. **Rest-Scan:** `## Progress` final auf offene `- [ ]`-Zeilen pruefen — Treffer einzeln
   listen und fragen (pausieren vs. bewusst offen lassen), nie still verlieren
2. Zusammenfassung ausgeben (Phasen, Kern-Dateien). **Feature-End-Review empfehlen:**
   `/dtb:impl-review {slug}` (Plan-Drift + Craft + Rules) VOR dem Checkpoint. Danach auf
   `/dtb:workflow-checkpoint` verweisen (Session-Log + Status-Sync; dort landet auch die
   letzte SHA-Rueckschreibung)
3. Der abgeleitete Status ist jetzt „Fertig zum Testen" — **„Abgenommen" vergibt NICHT
   dieser Skill**, sondern der Nutzer im Checkpoint (mit Beleg-Rueckfrage)

---

## Wichtig

- **Kein autonomer Durchlauf:** Das manuelle Gate (Ritual Punkt 2) wird IMMER gestellt —
  auch wenn der Nutzer „mach alle Phasen" sagt, stoppt jede Phase am Gate
- **Gate nie leer:** Fehlen (geteilte) Kriterien → alle als Manual (Alt-Plan-Fallback);
  das Ritual laeuft trotzdem
- **Nur `## Progress` mutieren** — Plan-Bloecke sind read-only (Abweichungen → Mismatch-Block)
- **Abgrenzung:** Routine-Commits ausserhalb des Phasen-Rituals sind nicht Aufgabe dieses
  Skills (INBOX #21 `dtb:commit-and-push`); der Feature-End-Review ist `/dtb:impl-review`
  (loest das alte code-review ab, INBOX #20 umgesetzt)
- **Kompakt & Deutsch:** Status-Ausgaben knapp halten; alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:impl-plan` — erzeugt den Plan mit Automated/Manual-Kriterien (Vorgaenger)
- `/dtb:feature-start` — aktiviert das Feature (Backlog → In Arbeit) und uebergibt hierher
- `/dtb:impl-review` — Feature-End-Review: Plan-Drift + Craft + Rules (Nachfolger)
- `/dtb:workflow-checkpoint` — Session-Ende, Status-Sync, Abnahme mit Beleg-Rueckfrage
- `/dtb:lesson` — Lektion festhalten (Prior-Quelle)
