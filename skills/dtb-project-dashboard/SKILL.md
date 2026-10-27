---
name: dtb:project-dashboard
description: >-
  Use when: "Projekt-Dashboard", "Dashboard zeigen", "Projektstand als Seite",
  "zeig mir das Dashboard", "project dashboard". Read-only: renders the project
  state (key figures, active change, open tasks, worktrees, backlog by derived
  status, recent sessions, INBOX and finding basin, lessons) as one local,
  self-contained HTML page and opens it in the browser.
disable-model-invocation: false
argument-hint: "[ohne-browser]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
pipeline:
  stage: monitoring
  after: [dtb:workflow-checkpoint]
  next: null
  consumes: [WORKFLOW_STATUS.md, BACKLOG.md, INBOX.md, INBOX-BEFUNDE.md, features/*/discovery.md, features/*/spec.md, features/*/plan.md, features/*/task.md, features/*/bug.md, project-rules/lessons.md, project-changelog/*/*.md, workflow.config.yaml, project-rules/DERIVED_STATE_RULES.md]
  produces: [project-dashboard.html]
---

# DTB Projekt-Dashboard

Rein lesende Sicht: buendelt den Projektstand in EINER lokalen HTML-Seite
`dtb-project/project-dashboard.html` (unversioniert). Die Seite aendert keine Projektdatei. Zwei Wege, ein
Ergebnis: auf Abruf (`/dtb:project-dashboard`, oeffnet den Browser) und automatisch am
Session-Ende durch `dtb:workflow-checkpoint` Schritt 4b (Modus „ohne Browser").

## Ablauf

> **Wartungs-Hinweis (Struktur-Anker):** `## Ablauf` und `## Seitengeruest` sind die Anker, auf
> die `dtb:workflow-checkpoint` Schritt 4b seinen Struktur-Check fuehrt (Leser: workflow-checkpoint
> Schritt 4b). Umbenennen oder Umbauen → den Check dort mitziehen.

### Schritt 0: Config und Modus

Lies `workflow.config.yaml` im Projekt-Root. Fallbacks: `paths.workflows` →
`dtb-project/project-workflows`, `paths.changelog` → `dtb-project/project-changelog`,
`paths.rules` → `dtb-project/project-rules`, `status.alter_schwelle_tage` → 7. Fehlt die Config
ganz, gelten alle Fallbacks (kein Abbruch).

- **Modus „auf Abruf"** (Standard, `/dtb:project-dashboard`): Seite schreiben und im Browser oeffnen
- **Modus „ohne Browser"** (Argument `ohne-browser`, so ruft `dtb:workflow-checkpoint` Schritt 4b
  auf): Seite schreiben, nicht oeffnen, nur die Pfad-Zeile ausgeben

**Rein lesend:** Der Skill schreibt ausschliesslich `dtb-project/project-dashboard.html`. Keine
Projektdatei wird geaendert, kein Statusfeld korrigiert (DSR §1.3 Punkt 3).

### Schritt 1: Worktree-Erkennung (nur Banner)

Dieselbe Pruefung wie `skills/CLAUDE.md` → „Worktree-Guard (kanonische Vorlage)", in EINEM
selbstaendigen Bash-Block — aber **ohne Abbruch**:

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(cd "$C" 2>/dev/null && pwd) || { echo DURCHLASS-NOGIT; exit 0; }
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `WORKTREE` → Slot `{{BANNER}}` = Baustein „Worktree-Banner" mit `git branch --show-current`
- `HAUPT-CHECKOUT` oder `DURCHLASS-NOGIT` → Slot `{{BANNER}}` leer

### Schritt 2: Quellen lesen

| Quelle | Bereich | Fehlt → |
|--------|---------|---------|
| `{workflows}/WORKFLOW_STATUS.md` | Offene Aufgaben, Meilensteine, Naechster Befehl, Pausierte Themen | „nicht vorhanden" in Wo wir stehen + Meilensteine |
| `{workflows}/BACKLOG.md` | Anzeige-Status je Change (nur fuer den Konflikt-Vergleich) | kein Vergleich, still |
| `{workflows}/INBOX.md` | Kennzahl + Liste INBOX | „nicht vorhanden" |
| `{workflows}/INBOX-BEFUNDE.md` | Kennzahl + Liste Becken | „nicht vorhanden" |
| `{workflows}/features/*/` | Changes, Backlog nach Status, Aktiver Change | Leerzustand |
| `{rules}/lessons.md` | Kennzahl + Lektionen-Block | „nicht vorhanden" |
| `{changelog}/*/*.md` | Letzte 5 Sessions | „nicht vorhanden" |
| `git worktree list --porcelain` | Worktrees | Block entfaellt still (kein Git) |

**Tabellen lesen:** gezaehlt werden nur Datenzeilen — nie Kopfzeile, nie `|---|`-Trennzeile.
Escapte Pipes (`\|`) trennen keine Zellen. Zeile mit falscher Spaltenzahl → Eintrag trotzdem
zeigen (soweit lesbar), Warnchip „Zeile defekt", weiterzaehlen.

### Schritt 3: Zaehl- und Ableitungsregeln

**Kennzahlen** (genau sechs, diese Reihenfolge — Slot `{{KENNZAHLEN}}`):

| Kennzahl | Regel | Zusatzzeile |
|----------|-------|-------------|
| Ideen offen | INBOX-Datenzeilen mit Status `Offen` oder `In Arbeit` | — |
| Befunde ungesichtet | Becken-Datenzeilen, die nach der Definition **„Ungesichtet"** im Kopf von `INBOX-BEFUNDE.md` ungesichtet sind — die Definition steht dort und nur dort | — |
| Lektionen | Datenzeilen in `lessons.md` | `{Zeilen der Datei}/150 Zeilen` |
| Aktive Changes | Change-Ordner direkt unter `features/` (nicht `archive/`) | — |
| Offene Aufgaben | Zeilen `- [ ]` unter `## Offene Aufgaben` in `WORKFLOW_STATUS.md` | `{N} ⏳` = Zeilen, die ⏳ tragen |
| Worktrees | Zeilen des Worktree-Blocks (unten) | — |

**Offene Aufgaben** werden so gezeigt, wie der Checkpoint sie geschrieben hat: Titel, Kontext,
`(seit …[ · behalten …])` woertlich, ⏳ nur wenn die Zeile es traegt — **keine eigene
Alters-Ableitung** (Kanon: Regel-Datei §9.4, Schreiber: `dtb:workflow-checkpoint`). Altformat
ohne `— Kontext:` (Bestandsprojekte) → die ganze Zeile als Titel (Markdown entfernt), ohne Meta.

**Statusableitung je Change (operative Kopie von Regel-Datei §1/§3 — rein lesend).**
Kernsatz: Der Status eines Change-Ordners folgt aus seinen Dateien und `## Progress`; ein Feld, das etwas anderes sagt, verliert und bekommt einen Warnchip.
- **Ableitung** (hoechste zutreffende Zeile): nur `discovery.md` → In Discovery · `spec.md` ohne
  `plan.md` → Spezifiziert · `plan.md` mit 0 abgehakten `## Progress`-Zeilen → Geplant · teilweise →
  In Arbeit (`X/Y`) · alle → Fertig zum Testen
- **Explizit** (ueberschreibt die Ableitung): `**Status:** Abgenommen` im Kopf von `spec.md`
  (bzw. `task.md`/`bug.md`) → Abgenommen — Konflikt NUR, wenn `## Progress` dabei < Y/Y ist;
  Change unter `## Pausierte Themen` in `WORKFLOW_STATUS.md` → Pausiert
- **`task.md`/`bug.md` ohne `plan.md`:** Checkboxen unter `## Schritte` bzw. `## Fix-Schritte`;
  0 → Spalte Geplant (Chip `Offen`), teilweise → In Arbeit, alle → Fertig zum Testen (Chip
  `Erledigt`/`Behoben`)
- **Defekt:** `plan.md` ohne `## Progress` oder mit 0 Checkbox-Zeilen → Spalte Geplant, Warnchip
  „Fortschritt unbekannt"; `plan.md` ohne `spec.md` → Warnchip „Change ohne Spec"; leerer Ordner
  → nicht zeigen; flache Alt-Dateien direkt in `features/` (`FEATURE_*.md`, `PLAN_*.md`,
  `IMPL_STATUS_*.md` …) → fuer die Ableitung ignoriert, im Backlog-Block EIN Warnchip
  `{N} Alt-Dateien ohne Change-Ordner — Migration: /dtb:migrate-change-folders` ueber den Spalten
- **Konflikt → Warnchip:** Sagt die `**Status:**`-Zeile in `spec.md` oder die Status-Spalte der
  BACKLOG-Zeile etwas anderes als die Ableitung → Warnchip
  `Anzeige in {Datei}: {Wert} — abgeleitet: {Status}`. Kein Konflikt: Feld fehlt, Feld = Ableitung,
  BACKLOG-Legende nach §3 (`Idee` fuer In Discovery/Spezifiziert)

> **Wartungs-Hinweis (Format-Kopplung):** spiegelt Regel-Datei §1.1, §1.2, §1.4, §1.5 und §3
> kompakt (Kopie ist Absicht — der Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22).
> Aenderung dort → hier mitziehen (Grep-Anker: `Statusableitung je Change (operative Kopie`).

**Backlog nach Status** (Slot `{{BACKLOG}}`): sieben Spalten in fester Reihenfolge — In Discovery,
Spezifiziert, Geplant, In Arbeit, Fertig zum Testen, Abgenommen, Pausiert. Leere Spalte bleibt
stehen (`col empty`, Zahl 0). Eintrag = Titel aus der ersten `# `-Zeile von `spec.md` (sonst
Ordnername), Link auf `plan.md` (sonst `spec.md`), bei In Arbeit `X/Y`, Warnchips darunter.

**Wo wir stehen** (Slot `{{STAND}}`):
- **Aktiver Change:** alle Changes mit Status In Arbeit; gibt es keinen, die mit Geplant; gibt es
  auch keinen → Baustein „Leerzustand". Je Karte: Titel, Status-Chip (`gold`), Warnchips,
  Fortschrittsbalken, `Progress X/Y · naechster Schritt {erste offene Progress-Zeile}`
- **Naechster Befehl:** `**Naechster Befehl:**` aus `## Handoff` in `WORKFLOW_STATUS.md`
- **Offene Aufgaben:** Karte daneben (Regel oben)
- **Worktrees:** Karte darunter (Regel unten); ohne verlinkten Worktree entfaellt die Karte

**Worktrees — Verweis, keine Kopie.** Die Zeilen folgen der operativen Kopie von Regel-Datei §10
in `dtb:workflow-next` (Abschnitt mit der Fettzeile `**Worktree-Stand (operative Kopie von
Regel-Datei §10 — rein lesend).**`): Quelle, Slug/Art, Hauptbranch, Stand
(verwaist/laufend/gemergt/frisch), uncommitted, Fortschritt, ⏳ und die Nur-lesend-Liste der
erlaubten Kommandos gelten dort und nur dort. Das Dashboard zeigt dieselben Felder als
Tabellenzeile (`<table class="wt">`, eine `<tr>` je Worktree, Stand als Chip).

**Struktur-Check vor der Worktree-Zeile** (Muster `dtb:pane-start` → „Struktur-Check"):
Quelle zuerst `~/.claude/skills/dtb-workflow-next/SKILL.md`, sonst
`skills/dtb-workflow-next/SKILL.md` im Projekt-Root. Anker zeilenende-normalisiert
(`tr -d '\r'` vorschalten) und am Zeilenanfang verankert: `^\*\*Worktree-Stand (operative Kopie`.
Zwei getrennte Fehlerpfade — nie Abbruch, die Seite entsteht trotzdem:
1. **Datei in beiden Quellen nicht gefunden** → Karte „nicht vorhanden: dtb:workflow-next
   (Installation — /dtb:kit-sync sync)"
2. **Datei vorhanden, Anker fehlt** → Karte mit Warnchip „Worktree-Regel in dtb:workflow-next
   nicht gefunden — Dashboard anpassen" (Drift), keine Zeilen

**Zuletzt gemacht** (Slot `{{ZULETZT}}`): links die letzten 5 Sessions ueber alle Logs (neueste
zuerst): Datum (Link auf den Log), Session-Kopf = Text der `## Session …`-Zeile ohne `## `
(heute `Session N - HH:MM`, in Bestandsprojekten auch mit Titel), darunter als Kurztext die erste
nicht-leere Zeile unter der Session, die keine Ueberschrift ist — Listenzeichen und Markdown
entfernt, ≤ 150 Zeichen, gekappt mit `…`. Rechts die Zeilen von
`## Abgeschlossene Meilensteine` aus `WORKFLOW_STATUS.md`: Meilenstein, darunter Datum · Ergebnis.

**INBOX & Befund-Becken** (Slot `{{INBOX}}`): zwei Karten, je die neuesten 10 (Datum absteigend,
bei Gleichstand hoehere Nummer zuerst), Rest im Baustein „Einklappbare Liste". INBOX zeigt nur
offene Ideen (Kennzahl-Regel); das Becken zeigt alle ungesichteten Befunde, Zusatz
„status-neutral, erst nach Triage bearbeitbar" (Regel-Datei §6.4). **Kurztitel:** beginnt die
Zelle mit Fettdruck, dessen Text — sonst der erste Satz (bis `. `, `? `, `! ` oder `: `);
Markdown-Zeichen (`**`, Backticks, Link-Syntax) entfernt; ≤ 96 Zeichen, gekappt mit `…`.

**Lektionen** (Slot `{{LEKTIONEN}}`): Anzahl, letzte Nummer, Fuellstand `{Zeilen}/150` als
Balken. Mehr als 150 Zeilen → „Kuratierung faellig → INBOX #141"; sonst „Kuratierung noch nicht
faellig (Signal ab > 150 Zeilen)" — dieselbe Schwelle wie `dtb:lesson`.

### Schritt 4: Randfaelle

- **Quelle fehlt** → Baustein „nicht vorhanden" an der Stelle des Blocks; Seitenstruktur bleibt
  gleich; die zugehoerige Kennzahl zeigt `—` mit Zusatzzeile `nicht vorhanden` (nie `0` — „keine
  Datei" ist nicht „leer")
- **Defekte Zeile / Konflikt** → Artefakt gewinnt, mit dem abgeleiteten Wert weiterrechnen, Warnchip
- **Kein aktiver Change** → Baustein „Leerzustand" mit dem Naechsten Befehl (fehlt er: `/dtb:workflow-next`)
- **Escaping:** JEDER Text aus einer Quelldatei wird vor dem Einsetzen HTML-escaped (Baustein-Regel)
- **Link-Regel:** Quelltext wird nie zu Links — auch keine Markdown-Links aus INBOX oder Logs
  (sie werden zu reinem Text). Links entstehen nur aus Pfaden, die der Skill selbst bildet,
  relativ zu `dtb-project/` (z.B. `project-workflows/features/{slug}/plan.md`)

### Schritt 5: Seite erzeugen (zwei Takte)

1. **Geruest kopieren** — Bash, woertlich, nie abgetippt:
   ```bash
   SRC=~/.claude/skills/dtb-project-dashboard/SKILL.md
   [ -f "$SRC" ] || SRC=skills/dtb-project-dashboard/SKILL.md
   mkdir -p dtb-project
   tr -d '\r' < "$SRC" | awk '/^## Seitengeruest/{s=1} s&&/^```html/{c=1;next} c&&/^```/{exit} c' > dtb-project/project-dashboard.html
   grep -c '{{[A-Z_]*}}' dtb-project/project-dashboard.html
   ```
   Erwartet: `8`. Sonst Abbruch mit `⚠ Seitengeruest nicht lesbar ({SRC}) — /dtb:kit-sync sync`.
2. **Slots fuellen** — die kopierte Datei zuerst einmal lesen, nur den Teil ab `<body>` (Edit
   setzt einen Read der Datei voraus; das Stylesheet davor bleibt ungelesen). Dann je Slot genau
   ein Edit (`{{NAME}}` → Inhalt aus Schritt 3). Danach
   `grep -c '{{[A-Z_]*}}' dtb-project/project-dashboard.html` = `0`.

### Schritt 6: Versionierung pruefen (einmal je Lauf, nur Hinweis)

- `git check-ignore -q dtb-project/project-dashboard.html` → ignoriert: still
- nicht ignoriert → genau eine Zeile `💡 dtb-project/project-dashboard.html wird nicht ignoriert —
  Vorschlag fuer .gitignore: dtb-project/project-dashboard.html` (nie selbst schreiben)
- kein Git-Repo → genau eine Zeile `ℹ Kein Git-Repo — Versionierung nicht geprueft`

### Schritt 7: Oeffnen und Bestaetigung

- **Auf Abruf:** oeffnen je Plattform — Windows `start "" "dtb-project\project-dashboard.html"`,
  macOS `open dtb-project/project-dashboard.html`, Linux `xdg-open dtb-project/project-dashboard.html`
- **Ohne Browser:** nicht oeffnen
- Bestaetigung (genau eine Zeile, beide Modi): `Dashboard: dtb-project/project-dashboard.html`
  plus Hinweiszeilen aus Schritt 6 und je fehlender Quelle `⚠ nicht vorhanden: {Datei}`

## Seitengeruest

> **Wartungs-Hinweis (Struktur-Anker):** Diese Sektion ist die eine Quelle des Seitengeruests.
> Pro Lauf wird der Codeblock unten **woertlich** in die Ausgabedatei kopiert (Bash, Extraktion
> zwischen den Codeblock-Zaeunen dieser Sektion) und danach jeder Slot per Edit durch seinen
> Inhalt ersetzt — CSS und Skript laufen nie durch die Ausgabe. Jeder Slot steht genau einmal im
> Geruest. Bei Umbenennung der Ueberschrift die Struktur-Checks der Leser mitziehen.

**Slots:** `{{BANNER}}` (Worktree-Banner oder leer) · `{{STAND_DATUM}}` (YYYY-MM-DD) ·
`{{KENNZAHLEN}}` (sechs Kennzahl-Bausteine) · `{{STAND}}` (Wo wir stehen) · `{{BACKLOG}}`
(Spalten nach abgeleitetem Status) · `{{ZULETZT}}` (Sessions + Meilensteine) · `{{INBOX}}`
(INBOX + Befund-Becken) · `{{LEKTIONEN}}` (Anzahl + Fuellstand).

```html
<!DOCTYPE html>
<html lang="de" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projekt-Dashboard</title>
<script>
  try { var t = localStorage.getItem('dtb-dashboard-theme'); if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t); } catch (e) {}
</script>
<style>
  :root {
    --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --mono: ui-monospace, "Cascadia Code", "SF Mono", Consolas, "Liberation Mono", monospace;
    --gold: #f5c451; --gold-hover: #eab534; --on-gold: #191510;
  }
  [data-theme="dark"] {
    --page: #0b0b0b; --card: #100f0e; --raised: #161514;
    --ink: #f4f3f1; --body: #f4f3f1cc; --muted: #f4f3f1b3; --label: #f4f3f199; --faint: #f4f3f159;
    --line: #ffffff14; --line-soft: #ffffff0f; --line-strong: #ffffff1f;
    --ok: #58da98; --bad: #fd736d;
  }
  [data-theme="light"] {
    --page: #f1f2f5; --card: #ffffff; --raised: #fbfbfc;
    --ink: #14161a; --body: #14161acc; --muted: #14161ab3; --label: #14161a99; --faint: #14161a59;
    --line: #14161a1a; --line-soft: #14161a12; --line-strong: #14161a24;
    --ok: #007e46; --bad: #c9302d;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; background: var(--page); color: var(--body); font-family: var(--sans); font-size: 15px; line-height: 1.5; }
  a { color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line-strong); }
  a:hover { border-bottom-color: var(--gold); }
  code, .mono { font-family: var(--mono); }
  .wrap { max-width: 1180px; margin: 0 auto; padding: 32px 24px 64px; }
  header { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 28px; }
  h1 { margin: 0; color: var(--ink); font-size: 34px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1; }
  .kicker { font-family: var(--mono); font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--label); margin-bottom: 8px; }
  .kicker b { color: var(--gold); font-weight: 600; }
  .toggle { font: 600 13px var(--sans); color: var(--ink); background: transparent; border: 1px solid var(--line-strong); border-radius: 6px; padding: 7px 12px; cursor: pointer; }
  .toggle:hover { border-color: var(--gold); }
  .banner { border: 1px solid var(--gold); color: var(--ink); background: color-mix(in srgb, var(--gold) 10%, transparent); border-radius: 9px; padding: 10px 14px; margin-bottom: 20px; font-size: 14px; }
  .stats { display: grid; grid-template-columns: repeat(6, 1fr); border: 1px solid var(--line); border-radius: 9px; background: var(--card); margin-bottom: 36px; }
  .stat { padding: 20px 18px; border-left: 1px solid var(--line); }
  .stat:first-child { border-left: 0; }
  .num { font-family: var(--mono); font-size: 40px; font-weight: 600; color: var(--ink); letter-spacing: -0.04em; line-height: 1; }
  .lbl { font-family: var(--mono); font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--label); margin-top: 10px; }
  .sub { font-family: var(--mono); font-size: 12px; color: var(--faint); margin-top: 4px; }
  section { margin-bottom: 36px; }
  h2 { color: var(--ink); font-size: 20px; font-weight: 700; letter-spacing: -0.02em; margin: 0 0 14px; }
  h3 { color: var(--ink); font-size: 18px; font-weight: 700; letter-spacing: -0.02em; margin: 4px 0 10px; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 9px; padding: 18px 20px; min-width: 0; }
  .card.missing { opacity: 0.55; border-style: dashed; }
  .eyebrow { font-family: var(--mono); font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--label); margin-bottom: 8px; }
  .eyebrow a { color: var(--label); }
  .eyebrow.gap { margin-top: 18px; }
  .muted { color: var(--faint); text-transform: none; letter-spacing: 0; font-family: var(--sans); font-size: 12px; font-weight: 400; }
  .meta { font-size: 13px; color: var(--label); }
  .row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
  .chip { display: inline-block; font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; border: 1px solid var(--line-strong); border-radius: 4px; padding: 2px 7px; color: var(--muted); white-space: nowrap; }
  .chip.gold { background: var(--gold); border-color: var(--gold); color: var(--on-gold); font-weight: 600; }
  .chip.warn { border-color: var(--bad); color: var(--bad); white-space: normal; }
  .chip.ok { border-color: var(--ok); color: var(--ok); }
  .progress { height: 6px; background: var(--line); border-radius: 4px; overflow: hidden; margin: 6px 0 8px; }
  .progress span { display: block; height: 100%; background: var(--gold); min-width: 2px; }
  .cmd { display: inline-block; font-size: 13px; color: var(--ink); background: var(--raised); border: 1px solid var(--line); border-radius: 6px; padding: 5px 10px; }
  .list { list-style: none; margin: 0; padding: 0; }
  .list li { display: flex; gap: 10px; padding: 9px 0; border-top: 1px solid var(--line-soft); }
  .list li:first-child { border-top: 0; }
  .list li > div { min-width: 0; }
  .list.tasks li, .card > .list li { flex-direction: column; gap: 2px; }
  .list li:has(> .num-s) { flex-direction: row; }
  .t { color: var(--ink); font-size: 14px; }
  .num-s { font-size: 12px; color: var(--faint); min-width: 38px; padding-top: 2px; }
  .hourglass { font-size: 12px; }
  details { margin-top: 8px; }
  summary { cursor: pointer; font-family: var(--mono); font-size: 12px; color: var(--label); padding: 6px 0; }
  summary:hover { color: var(--gold); }
  .wt { width: 100%; border-collapse: collapse; font-size: 13px; }
  .wt td { padding: 4px 12px 4px 0; color: var(--muted); }
  .kanban { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
  .col { background: var(--card); border: 1px solid var(--line); border-radius: 9px; padding: 12px; min-height: 92px; min-width: 0; }
  .col.empty { opacity: 0.5; }
  .colhead { display: flex; justify-content: space-between; font-family: var(--mono); font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--label); margin-bottom: 8px; }
  .col .list li { flex-direction: column; font-size: 14px; gap: 0; }
  .split { display: flex; gap: 32px; align-items: center; }
  .grow { flex: 1; }
  .big { font-size: 40px; font-weight: 600; color: var(--ink); letter-spacing: -0.04em; line-height: 1; }
  .emptystate { color: var(--muted); font-size: 14px; line-height: 2; }
  footer { margin-top: 40px; font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--faint); }
  @media (max-width: 980px) { .stats { grid-template-columns: repeat(3, 1fr); } .stat:nth-child(4) { border-left: 0; } .stat:nth-child(n+4) { border-top: 1px solid var(--line); } .kanban { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 680px) { .grid2 { grid-template-columns: 1fr; } .stats { grid-template-columns: repeat(2, 1fr); } .stat { border-left: 0; border-top: 1px solid var(--line); } .split { flex-direction: column; align-items: flex-start; } .wrap { padding: 20px 16px 48px; } }
</style>
</head>
<body>
<div class="wrap">
  {{BANNER}}
  <header>
    <div>
      <div class="kicker"><b>●</b> Projektstand · {{STAND_DATUM}}</div>
      <h1>Projekt-Dashboard</h1>
    </div>
    <button class="toggle" id="theme-toggle" type="button" aria-label="Hell/Dunkel umschalten">☀ Hell</button>
  </header>

  <div class="stats">{{KENNZAHLEN}}</div>

  <section><h2>Wo wir stehen</h2>{{STAND}}</section>
  <section><h2>Backlog nach Status</h2>{{BACKLOG}}</section>
  <section><h2>Zuletzt gemacht</h2>{{ZULETZT}}</section>
  <section><h2>INBOX &amp; Befund-Becken</h2>{{INBOX}}</section>
  <section><h2>Lektionen</h2>{{LEKTIONEN}}</section>

  <footer>Rein lesend · erzeugt von /dtb:project-dashboard · Quelle: Artefakte (Artefakt gewinnt)</footer>
</div>
<script>
  (function () {
    var root = document.documentElement, btn = document.getElementById('theme-toggle');
    function label() { btn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀ Hell' : '☾ Dunkel'; }
    label();
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next); label();
      try { localStorage.setItem('dtb-dashboard-theme', next); } catch (e) {}
    });
  })();
</script>
</body>
</html>
```

### Bausteine

Alle Texte aus Quelldateien werden HTML-escaped (`&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`,
`"` → `&quot;`). `[TEXT]` sind Platzhalter fuer den Inhalt.

| Baustein | Vorlage |
|----------|---------|
| Kennzahl | `<div class="stat"><div class="num">[ZAHL]</div><div class="lbl">[LABEL]</div><div class="sub">[ZUSATZ]</div></div>` (`sub` entfaellt ohne Zusatz) |
| Karte | `<article class="card"><div class="eyebrow">[TITEL]</div>[INHALT]</article>` |
| Zwei Karten nebeneinander | `<div class="grid2">[KARTE][KARTE]</div>` |
| Chip | `<span class="chip">[TEXT]</span>` · Status hervorgehoben: `chip gold` |
| Warnchip | `<span class="chip warn" title="[KONFLIKT]">⚠ [KONFLIKT]</span>` |
| Fortschritt | `<div class="progress"><span style="width:[PROZENT]%"></span></div>` |
| Befehl | `<code class="cmd">[BEFEHL]</code>` |
| Listeneintrag | `<li><div class="t">[TITEL]</div><div class="meta">[META]</div></li>` · mit Nummer: `<li><span class="num-s mono">#[N]</span><div><div class="t">[TITEL]</div><div class="meta mono">[META]</div></div></li>` |
| Einklappbare Liste | `<ul class="list">[NEUESTE 10]</ul><details><summary>alle [N] anzeigen</summary><ul class="list">[REST]</ul></details>` (`details` entfaellt bei ≤ 10) |
| Leerzustand | `<div class="emptystate">Kein aktives Feature.<br>Weiter mit <code class="cmd">[BEFEHL]</code></div>` |
| „nicht vorhanden" | `<article class="card missing"><div class="eyebrow">[BEREICH]</div><div class="meta">nicht vorhanden: [DATEI]</div></article>` |
| Backlog-Spalte | `<div class="col">` (leer: `col empty`) `<div class="colhead"><span>[STATUS]</span><span class="mono">[N]</span></div><ul class="list">[EINTRAEGE]</ul></div>` |
| Worktree-Banner | `<div class="banner">Worktree-Ansicht <code>[BRANCH]</code> — globaler Stand vom Abzweig, massgeblich ist der Haupt-Checkout</div>` |
