# Implementierungsplan: Dashboard mit Projektname und Raster-Hintergrund

**Erstellt:** 2026-10-27
**Feature-Spec:** `features/dashboard-projektname-hintergrund/spec.md`
**Geschaetzte Dauer:** ~1 h
**Status:** Reviewed (plan-review 2026-10-27: REVISE → 2 WARNs behoben) <!-- Review-Nachweis (nicht Umsetzungsstand); einziger Pfleger ist dtb:plan-review — Kanon: project-rules/DERIVED_STATE_RULES.md §7 -->

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Skill-Text: Projektname-Slot, Ableitungsregel, Hintergrund-CSS | ~35 min | Geplant |
| Phase 2 | Probelauf und Sichtabnahme | ~25 min | Geplant |

---

## Ist-Analyse

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `skills/dtb-project-dashboard/SKILL.md` | Schritt 0 liest `workflow.config.yaml` mit Fallbacks (Z. 35–38), kein `project_name`; Schritt 5.1 erwartet `8` Slots (Z. 196); Geruest: `<title>Projekt-Dashboard</title>` (Z. 243), `html, body { background: var(--page) }` (Z. 266), Seitenfarben `--page` dunkel `#0b0b0b` / hell `#f1f2f5` (Z. 254/260), `<h1>Projekt-Dashboard</h1>` (Z. 337), Kicker `Projektstand · {{STAND_DATUM}}` (Z. 336), Inline-Skript nur Theme-Schalter (Z. 352–363); Slot-Liste (Z. 232–235) |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 4b prueft nur die Anker `^## Ablauf`/`^## Seitengeruest` (Z. 718) — keine Slot-Zahl, nicht anzupassen |
| `workflow.config.yaml` (Kit-Repo) | `project_name: "[Projektname]"` — Platzhalter, loest im Probelauf den Fallback aus |

---

## Phase 1: Skill-Text anpassen

### Ziel
`skills/dtb-project-dashboard/SKILL.md` erzeugt eine Seite mit Projektname als Titel und pi.dev-Hintergrund; Erzeugungs-Check passt zur neuen Slot-Zahl.

### Schritte

#### Schritt 1.1: Projektname-Slot im Geruest
- **Zweck:** Name sichtbar in Kopf und Tab
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md` (`## Seitengeruest`)
- **Input:** Discovery „Gewuenschtes Verhalten"
- **Output:** `<h1>{{PROJEKT}}</h1>`; Kicker `<b>●</b> Projekt-Dashboard · Projektstand · {{STAND_DATUM}}`; statisches `<title>Projekt-Dashboard</title>` bleibt als Rueckfall; Inline-Skript setzt `document.title = h1.textContent + ' · Projekt-Dashboard'`; Slot-Liste um `{{PROJEKT}}` (Projektname, escaped) ergaenzt

#### Schritt 1.2: Ableitungsregel Projektname + Slot-Zahl
- **Zweck:** Name in jedem Projekt und jedem Checkout korrekt
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md` (Schritt 0, Schritt 3, Schritt 5.1)
- **Input:** Randfaelle aus der Discovery
- **Output:** Schritt 0: `project_name` lesen — Wert ohne umschliessende Anfuehrungszeichen und Leerraum; fehlt/leer/beginnt mit `[` → Ordnername des Haupt-Checkouts per eigenstaendigem Bash-Block (eigene Shell, Normalisierung wie Schritt 1 — im Haupt-Checkout liefert Git relativ `.git`):
  ```bash
  C=$(git rev-parse --git-common-dir 2>/dev/null) && C=$(cd "$C" 2>/dev/null && pwd) && basename "$(dirname "$C")" || basename "$PWD"
  ```
  Schritt 3: Regel fuer Slot `{{PROJEKT}}` (HTML-escaped nach Baustein-Regel). Schritt 5.1: ``Erwartet: `9` ``

#### Schritt 1.3: Hintergrund-CSS beider Themes
- **Zweck:** Hintergrund wie pi.dev/docs
- **Dateien:** `skills/dtb-project-dashboard/SKILL.md` (`<style>` im Geruest)
- **Input:** Werte aus der Discovery (pi.dev/style.css, Abruf 2026-10-27)
- **Output:** `--page` dunkel `#161d27` / hell `#ebe7e4`; neue Tokens `--grid-minor`/`--grid-major`/`--grid-cross`/`--vignette` je Theme; `html { background: var(--page) }`, `body` transparent; `body::before` (Raster, 4 px/20 px + Kreuzmarken) und `body::after` (Vignette nach unten) als `position: fixed`, `inset: -8rem`, `z-index: 0`, `pointer-events: none`; `.wrap { position: relative; z-index: 1 }`

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Angepasster Skill `skills/dtb-project-dashboard/SKILL.md`

### Checkpoint-Kriterien

Geruest-Extraktion fuer alle Kriterien (woertlich aus Schritt 5.1 des Skills):
`tr -d '\r' < skills/dtb-project-dashboard/SKILL.md | awk '/^## Seitengeruest/{s=1} s&&/^```html/{c=1;next} c&&/^```/{exit} c'` → im Folgenden `GERUEST`

#### Automated
- [ ] `GERUEST | grep -c '{{[A-Z_]*}}'` = `9`
- [ ] `GERUEST | grep -c '<h1>{{PROJEKT}}</h1>'` = `1`
- [ ] `GERUEST | grep -c 'document.title'` = `1`
- [ ] ``grep -cF 'Erwartet: `9`' skills/dtb-project-dashboard/SKILL.md`` = `1` und ``grep -cF 'Erwartet: `8`' skills/dtb-project-dashboard/SKILL.md`` = `0` (Wirkstelle Schritt 5.1; `-F` ohne Rueckstrich — `\`` waere in GNU grep ein Puffer-Anker)
- [ ] `awk '/^\*\*Slots:\*\*/{s=1} s&&/^$/{exit} s' skills/dtb-project-dashboard/SKILL.md | grep -c '{{PROJEKT}}'` = `1` (Slot-Liste)
- [ ] `GERUEST | grep -c 'body::before'` ≥ `1` und `GERUEST | grep -c 'body::after'` ≥ `1`
- [ ] `GERUEST | grep -ci '#161d27'` ≥ `1` und `GERUEST | grep -ci '#ebe7e4'` ≥ `1`
- [ ] `GERUEST | grep -cE 'https?://'` = `0` (self-contained)
- [ ] `awk '/^### Schritt 0/{s=1} /^### Schritt 1/{s=0} s' skills/dtb-project-dashboard/SKILL.md | grep -c 'project_name'` ≥ `1`
- [ ] `awk '/^### Schritt 0/{s=1} /^### Schritt 1/{s=0} s' skills/dtb-project-dashboard/SKILL.md | grep -c 'git rev-parse --git-common-dir'` = `1` und dieselbe Sektion `| grep -c 'pwd'` ≥ `1` (normalisierter Fallback)

---

## Phase 2: Probelauf und Sichtabnahme

### Ziel
Nachweis an echten Seiten: Fallback-Name, konfigurierter Name mit Sonderzeichen, Hintergrund in beiden Themes.

### Schritte

#### Schritt 2.1: Probelaeufe gegen die Repo-Fassung
- **Zweck:** Verhalten belegen, nicht nur Text (Lektion L74: Repo-Fassung, nie die installierte Kopie)
- **Dateien:** erzeugt `dtb-project/project-dashboard.html` (unversioniert, `git check-ignore` = 0) in diesem Worktree; Wegwerf-Ordner `zz-test-dashboard-name/` im Scratchpad (`git init`, `workflow.config.yaml` mit `project_name: "A & <B> {x}"`, dazu die Repo-Fassung kopiert nach `zz-test-dashboard-name/skills/dtb-project-dashboard/SKILL.md` — sonst faellt Schritt 5.1 dort auf die installierte Kopie zurueck) — vom Lauf selbst erzeugt (Lektion L57)
- **Input:** Skill aus Phase 1, Ablauf `dtb:project-dashboard` Modus „ohne Browser"
- **Output:** zwei Seiten; Ergebnis je Lauf als Zeile unter `## Abnahme-Belege` am Ende dieser Datei (Lektion L20)
- **Browser-Pruefung:** Playwright oeffnet die Seite per `file://`; ist das gesperrt → `python -m http.server` im Hintergrund im Seitenordner starten (PID beim Start merken), Seite per `http://localhost:…` oeffnen, danach `taskkill //PID {PID}` (Lektion L52, nie per Image-Name)

#### Schritt 2.2: Sichtabnahme neben pi.dev
- **Zweck:** Menschliches Urteil „gleicher Hintergrund", Lesbarkeit der Karten
- **Dateien:** Screenshots Hell/Dunkel (Dashboard + pi.dev/docs) im Scratchpad; Urteil als Zeile unter `## Abnahme-Belege`
- **Input:** Seite aus 2.1, Browser
- **Output:** Entscheidung des Menschen; Karten-Nacharbeit vor Abnahme oder als Folge-Idee (Lektion L97)

### Deliverables
- [ ] Zwei Probeseiten, Belege unter `## Abnahme-Belege`

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -c '{{' dtb-project/project-dashboard.html` = `0`
- [ ] `grep -c '<h1>claude-code-workflow-kit</h1>' dtb-project/project-dashboard.html` = `1` (Fallback im Worktree greift auf den Haupt-Checkout, nicht `pane-…`)
- [ ] `grep -cE '(src|href)="https?://|url\(["'"'"']?https?://' dtb-project/project-dashboard.html` = `0` (angepasst 2026-10-27 per Mismatch-Entscheid: der fruehere Grep auf jede Adresse traf escapten INBOX-Text, keine geladene Ressource)
- [ ] Wegwerf-Ordner: `cmp skills/dtb-project-dashboard/SKILL.md {scratchpad}/zz-test-dashboard-name/skills/dtb-project-dashboard/SKILL.md` → Exit `0` (Probelauf prueft die Repo-Fassung)
- [ ] Wegwerf-Seite: `grep -c '<h1>A &amp; &lt;B&gt; &#123;x}</h1>'` = `1`
- [ ] Im Browser (Playwright): `document.title` = `claude-code-workflow-kit · Projekt-Dashboard`; nach Klick auf den Theme-Schalter aendert sich die berechnete Hintergrundfarbe von `html` ohne Neuladen

#### Manual
- [ ] Hintergrund wirkt in Hell und Dunkel wie pi.dev/docs (Grundfarbe, Raster, Vignette)
- [ ] Karten, Links und Theme-Schalter bleiben lesbar und bedienbar — Karten-Toene ok oder Nacharbeit entschieden

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Tab-Titel | A: zweiter Slot im `<head>` · B: Inline-Skript aus `<h1>` | B | „jeder Slot genau einmal" und „Read ab `<body>`" bleiben gueltig; statischer Titel als Rueckfall ohne Skript (per Veto-Vorlage bestaetigt 2026-10-27) |
| Fallback-Name | A: Toplevel-Ordner · B: Haupt-Checkout ueber `--git-common-dir` | B | im Worktree waere A der `pane-…`-Ordner |
| Hintergrund-Werte | A: von pi.dev laden · B: inline kopiert | B | Seite bleibt self-contained und offline lesbar |
| Umfang Optik | A: ganzes pi.dev-Theme · B: nur Seitenhintergrund | B | Idee nennt nur den Hintergrund; Karten-Urteil in 2.2 |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 Projektname-Slot im Geruest — `f2fb8d9`
- [x] 1.2 Ableitungsregel + Slot-Zahl — `f2fb8d9`
- [x] 1.3 Hintergrund-CSS — `f2fb8d9`
- [x] 2.1 Probelaeufe
- [x] 2.2 Sichtabnahme

---

## Umsetzung

Umsetzung mit `/dtb:implement Dashboard mit Projektname und Raster-Hintergrund` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/dashboard-projektname-hintergrund/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

## Abnahme-Belege

- **2.1 Lauf Worktree (2026-10-27):** Repo-Fassung (`SRC=skills/…`), Geruest 9 Slots, Rest 0; `project_name` = Platzhalter → Fallback `claude-code-workflow-kit` (nicht `pane-…`); `<h1>claude-code-workflow-kit</h1>` = 1, `{{` = 0, externe Ressourcen = 0 (Kriterium per Mismatch-Entscheid auf `src`/`href`/`url(` verengt — der breite Grep traf escapten INBOX-Text #39/#27); Seite ignoriert (`git check-ignore` Exit 0). Kopf-Slots per Edit, die sechs unveraenderten Daten-Slots per Hilfsskript aus berechneten Bausteinen (Abweichung vom Ein-Edit-je-Slot, Probelauf-Hilfe)
- **2.1 Lauf Wegwerf-Ordner (2026-10-27):** `cmp` Kopie = Repo-Fassung (Exit 0), `HAUPT-CHECKOUT`, `project_name: "A & <B> {x}"` → `<h1>A &amp; &lt;B&gt; &#123;x}</h1>` = 1, Tab-Titel `A & <B> {x} · Projekt-Dashboard`; fehlende Quellen als „nicht vorhanden"
- **2.1 Browser (2026-10-27):** `file://` in Playwright gesperrt → Ausweichweg `python -m http.server` (127.0.0.1:8765/8766), danach per PID beendet. Worktree-Seite: `document.title` = `claude-code-workflow-kit · Projekt-Dashboard`; `html`-Hintergrund dunkel `rgb(22, 29, 39)` → nach Klick hell `rgb(235, 231, 228)` ohne Neuladen; `body::before` fixed mit 7 Verlaufsebenen; erster Link per `elementFromPoint` erreichbar (Raster faengt keine Klicks); einziger Konsolenfehler `favicon.ico` 404 (Testserver)
- **2.2 Sichtabnahme:** Screenshots Hell/Dunkel von Dashboard, pi.dev/docs und Testseite im Scratchpad der Session — Urteil Gate Phase 2 (2026-10-27): „passt" — Hintergrund wie pi.dev in Hell und Dunkel, dunkle Karten auf blaugrauem Grund bewusst akzeptiert, keine Nacharbeit

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-27)
