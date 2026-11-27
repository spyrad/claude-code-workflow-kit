# Discovery: Skill-Lint
<!-- resume: done -->

**Erstellt:** 2026-11-26
**Idee-Referenz:** Inbox #214 — "Skill-Regeln als Skript plus CI statt Prosa-Prüfung (Ergänzung zu Kit-INBOX #100)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `scripts/lint-skills.py` | Neubau: das Prüfskript über `skills/dtb-*/SKILL.md` |
| `scripts/tests/` | Neubau: Selbsttest samt Fixture-Skills (je Fehlerklasse rot, dazu eine grüne) |
| `.github/workflows/lint-skills.yml` | Neubau: CI-Lauf bei Push und PR (neben dem bestehenden `notify-site.yml`, das unberührt bleibt) |
| `skills/dtb-project-health/SKILL.md` | Check 8 (Skill-Frontmatter-Konsistenz): ruft das Skript auf, wenn es im Projekt liegt |
| `skills/CLAUDE.md` | Abschnitt „Frontmatter (Pflichtfelder)": Verweis aufs Skript; die Stage-Tabelle nennt 8 statt 10 Werte (Teil von Befund #88) |
| `CLAUDE.md` (Root) | Die Aussage „There are no build steps, tests, or runtime dependencies" wird falsch und muss nachgezogen werden |
| `skills/dtb-feature-plan/SKILL.md`, `skills/dtb-feature-discover/SKILL.md`, `skills/dtb-open-question/SKILL.md` | Bestand bereinigen: Teil-Guard ohne `Bash` in `allowed-tools` (Befund #195; open-question per plan-review 2026-11-26 ergänzt) |
| `skills/dtb-plan-review/SKILL.md`, `skills/dtb-lesson/SKILL.md`, `skills/dtb-greenfield-prd/SKILL.md`, `skills/dtb-workflow-next/SKILL.md`, `skills/dtb-meeting-agenda/SKILL.md`, `skills/dtb-meeting-dump/SKILL.md`, `skills/dtb-open-question/SKILL.md`, `skills/dtb-opportunity-map/SKILL.md`, `skills/dtb-lesson-curate/SKILL.md`, `skills/dtb-feature-plan/SKILL.md` | Bestand bereinigen: 7 einseitige Pipeline-Kanten (Gegenkante ergänzen oder Ausnahme) |
| `.gitignore` | Zeile gegen `__pycache__/` |

---

## Anforderungen

### Scope
**Enthalten:**
- Ein Prüfskript, das die eindeutigen Frontmatter-Regeln aus `skills/CLAUDE.md` mechanisch prüft:
  Pflichtfelder, `name` = Verzeichnis, `Use when:`-Präfix, `after`/`next` als Liste oder null,
  Kanten-Ziel existiert, Kante hat ihr Gegenstück (mit Ausnahmeliste), `stage` im Enum,
  Beschreibungslänge ≤ 350 Zeichen bei `disable-model-invocation: false`, Werkzeug-Pflicht `Bash`
- Ein Selbsttest des Skripts mit Fixture-Skills
- Ein CI-Lauf bei Push (alle Branches) und Pull Request, der Selbsttest und Lint ausführt
- Einbindung in `dtb:project-health` Check 8, wenn das Skript im Projekt liegt
- Bereinigung des Bestands, damit der erste CI-Lauf grün ist
- Doku-Nachzug in Root-`CLAUDE.md` und `skills/CLAUDE.md`

**Nicht enthalten:**
- Verteilung des Skripts an Zielprojekte (`dtb:kit-sync` verteilt kein `scripts/`; in
  Zielprojekten bleibt Check 8 die Modell-Sicht) — per Kernfrage entschieden 2026-11-26
- `consumes`/`produces`-Waisen und zirkuläre `next`-Ketten (unscharf bzw. im Kit als
  Session-Schleife gewollt — bleiben Modell-Sicht in Check 8)
- Tote Verweise in Prosa (Inbox #100)
- Umbau der Skills selbst (Inbox #219)

### Gewuenschtes Verhalten
- Das Skript meldet je Befund eine Zeile mit Stufe, Skill und Regel; Exit 1 bei mindestens
  einem FEHLER, sonst Exit 0
- Stufen folgen der bestehenden Einstufung von Check 8: FEHLER bei fehlendem
  `name`/`description`, `name` ≠ Verzeichnis, fehlendem Präfix, falscher Listenform,
  Kanten-Ziel ohne Skill, `stage` außerhalb des Enums, Werkzeug-Verstoß, zu langer
  Beschreibung und einseitiger Kante ohne Ausnahme; WARNUNG bei fehlendem
  `disable-model-invocation`/`allowed-tools`/`pipeline`
- Werkzeug-Regel: Ein Skill mit ```` ```bash ````-Block oder mit dem Anker `## Worktree-Guard`
  bzw. `**Teil-Guard (Worktree):**` muss `Bash` in `allowed-tools` tragen — der Teil-Guard
  verweist auf die Guard-Prüfung, statt sie zu enthalten, deshalb reicht die Suche nach dem
  Wort „Bash" nicht (belegt an `dtb-feature-plan` und `dtb-feature-discover`)
- Bewusst einseitige Kanten stehen mit Grund in einer Ausnahmeliste im Skript

### Randfaelle
- Mehrzeilige, gefaltete Beschreibungen (`>-`): die Länge zählt auf dem gefalteten Text
  (Zeilenumbruch und Einrückung = ein Leerzeichen), wie in `skills/CLAUDE.md` definiert
- CRLF-Zeilenenden in Skill-Dateien dürfen das Ergebnis nicht ändern
- Frontmatter fehlt oder ist kein gültiges YAML → FEHLER für diesen Skill, kein Abbruch des Laufs
- Ein Verzeichnis ohne `SKILL.md` → FEHLER
- PyYAML fehlt → klare Meldung mit Installationshinweis statt Stacktrace
- Aufruf ohne `python -I`: `-I` blendet die User-site-packages aus, PyYAML wäre dann nicht
  auffindbar (im Probelauf am 2026-11-26 belegt)
- Der Selbsttest darf kein `__pycache__` im versionierten Baum hinterlassen (Lektion L138)

### Einschraenkungen
- Einzige Fremdabhängigkeit ist PyYAML (lokal 6.0.1 vorhanden); die CI installiert es selbst
- Die CI braucht keine Secrets und nur Leserechte; `notify-site.yml` bleibt unberührt
- Der Stage-Enum hat 10 Werte (`idea`, `capture`, `planning`, `implementation`, `execution`,
  `development`, `session`, `monitoring`, `setup`, `greenfield`) — Quelle ist der
  Frontmatter-Block in `skills/CLAUDE.md`; die Tabelle darunter nennt nur 8 und wird angeglichen

### Integrationspunkte
- `dtb:project-health` Check 8: liegt `scripts/lint-skills.py` im Projekt, ruft er es auf
  und übernimmt dessen Befunde für die abgedeckten Regeln; sonst unverändert Modell-Sicht
- Geänderte verteilte Skills (`project-health`, `feature-plan`, `feature-discover` und die
  Kanten-Skills) erreichen die installierten Kopien erst per `dtb:kit-sync` nach dem Merge

---

## Abhaengigkeiten

- Inbox #100 (tote Teile scannen) — Ergänzung, keine Überschneidung: #214 prüft Frontmatter-Regeln
- Inbox #219 (Skills aufteilen) — abgegrenzt, baut die Skills selbst um
- Befunde #46 (einseitige Kanten), #88 (Stage-Tabelle), #195 (`Bash` fehlt) im Becken — werden
  durch die Bestandsbereinigung miterledigt; die Becken-Einträge selbst räumt der Orchestrator ab

---

## Offene Punkte

- Je einseitiger Kante entscheiden: Gegenkante ergänzen oder Ausnahme mit Grund (Schritt 1.3).
  Tendenz: Gegenkante bei feature-plan↔plan-review, lesson↔lesson-curate,
  opportunity-map↔greenfield-prd; Ausnahme bei Kanten zu den Lese-Sichten workflow-next und
  meeting-agenda

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
