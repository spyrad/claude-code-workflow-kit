---
name: dtb:project-dashboard
description: >-
  Use when: "Projekt-Dashboard", "Dashboard zeigen", "Projektstand als Seite",
  "zeig mir das Dashboard", "project dashboard". Read-only: renders the project
  state (key figures, active change, open tasks, worktrees, backlog by derived
  status, recent sessions, INBOX and finding basin, lessons) as one local,
  self-contained HTML page and opens it in the browser.
disable-model-invocation: false
---

# DTB Projekt-Dashboard

Rein lesende Sicht: buendelt den Projektstand in EINER lokalen HTML-Seite
`dtb-project/project-dashboard.html` (unversioniert). Die Seite aendert keine Projektdatei.

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
