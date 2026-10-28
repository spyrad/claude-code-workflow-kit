# Discovery: Dashboard mit Projektname und Raster-Hintergrund
<!-- resume: done -->

**Erstellt:** 2026-10-27
**Idee-Referenz:** Inbox #158 — "Kleiner Change an `project-dashboard.html` (`dtb:project-dashboard`): Die Seite soll den Namen des Projekts enthalten, und der Hintergrund soll gleich sein wie auf https://pi.dev/docs/latest."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-project-dashboard/SKILL.md` | `## Seitengeruest` (Kopf `<h1>`/Kicker, Stylesheet, Inline-Skript), Slot-Liste, Schritt 0 (Config-Werte), Schritt 3 (Slot-Regeln), Schritt 5.1 (Slot-Zahl `8`, Zeile 196) |

---

## Anforderungen

### Scope
**Enthalten:**
- Projektname als Seitentitel: im Kopf der Seite (`<h1>`) und im Browser-Tab
- Ableitungsregel fuer den Namen: `project_name` aus `workflow.config.yaml`; fehlt der Wert, ist er leer oder ein Platzhalter (beginnt mit `[`) → Ordnername des Haupt-Checkouts (`dirname` von `git rev-parse --git-common-dir`), ohne Git der aktuelle Ordner
- Seitenhintergrund wie pi.dev/docs: Grundfarbe, Millimeterraster und Vignette — in beiden Themes (Hell/Dunkel)
- Slot-Zahl im Erzeugungs-Check von 8 auf 9

**Nicht enthalten:**
- Karten, Schrift, Gold-Akzent und uebrige Theme-Farben (bleiben unveraendert)
- Laden von Ressourcen von pi.dev (alle Werte inline kopiert)
- Aenderungen an README.md, CLAUDE.md oder anderen Skills

### Gewuenschtes Verhalten
- Die grosse Ueberschrift zeigt den Projektnamen; die Kicker-Zeile darueber lautet „Projekt-Dashboard · Projektstand · {Datum}"
- Der Browser-Tab zeigt „{Projektname} · Projekt-Dashboard" — gesetzt vom vorhandenen Inline-Skript aus dem `<h1>`-Text (kein zweiter Slot im `<head>`; die Regel „jeder Slot genau einmal" und „Read ab `<body>`" bleiben gueltig). Ohne Skript bleibt der statische Titel „Projekt-Dashboard"
- Hintergrund als fixe Ebene hinter dem Inhalt (pi.dev: `body::before` Raster — 4 px fein, 20 px grob, Kreuzmarken an den Schnittpunkten; `body::after` Vignette nach unten); der Inhalt liegt darueber
- Grundfarben aus pi.dev: dunkel `#161d27`, hell `#ebe7e4`; Rasterfarben je Theme (dunkel `hsl(218 60% 80%)` mit Deckung 0.009375/0.02625/0.075, hell `#252f3d08`/`#252f3d12`/`#252f3d1d`), Vignette dunkel `#0d11161f`, hell `#ebe7e426` (Quelle: pi.dev/style.css, Abruf 2026-10-27)

### Randfaelle
- `project_name` fehlt, ist leer oder steht auf dem Platzhalter `[Projektname]` (heute im Kit-Repo der Fall) → Ordnername-Fallback
- Lauf in einem verlinkten Worktree: der Toplevel-Ordner hiesse `pane-…` — deshalb Haupt-Checkout-Name ueber `--git-common-dir`
- Sonderzeichen im Projektnamen (`&`, `<`, `"`, `{`) → HTML-Escaping nach der bestehenden Baustein-Regel
- Theme-Umschaltung zur Laufzeit: Raster und Grundfarbe folgen dem Theme ohne Neuladen

### Einschraenkungen
- Seite bleibt self-contained (keine externen Ressourcen) und offline lesbar
- Das Geruest wird pro Lauf woertlich kopiert — jeder Slot steht genau einmal darin

### Integrationspunkte
- `dtb:workflow-checkpoint` Schritt 4b erzeugt die Seite per Referenz und prueft nur die Anker `## Ablauf`/`## Seitengeruest` (skills/dtb-workflow-checkpoint/SKILL.md:718) — keine Slot-Zahl, daher nicht betroffen
- `project_name` wird von `dtb:project-init` gesetzt (skills/dtb-project-init/SKILL.md:87/117)

---

## Abhaengigkeiten

- Keine — Basis ist der abgenommene Change `projekt-dashboard` (INBOX #135, archiviert 2026-10-27)

---

## Offene Punkte

- Wirken die unveraendert fast schwarzen Karten auf dem blaugrauen Grund gut? Urteil in der Sichtabnahme (Plan Schritt 2.2); bei Nein Karten-Toene als Folge-Idee oder Nacharbeit vor der Abnahme

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-27)
