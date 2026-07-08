---
name: dtb:kit-sync
description: >-
  Use when: "kit sync", "kit check", "kit installieren", "skills aktualisieren",
  "drift pruefen", "installierte kopien pruefen", "kit updaten". Detects and
  reconciles drift between the kit repo (GitHub) and installed copies under
  ~/.claude using a lock file with content hashes (modes: check/sync/install).
disable-model-invocation: true
argument-hint: "[check|sync|install]"
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: monitoring
  after: null
  next: null
  consumes: [dtb-lock.json]
  produces: [dtb-lock.json]
---

# Kit-Sync (Distribution)

Du haeltst die installierten Kit-Kopien unter `~/.claude/` mit dem Kit-Repo synchron.
Drei Modi: `check` (read-only Drift-Report), `sync` (kontrollierter Abgleich),
`install` (Erstinstallation/Adoption).

> **Ebenen-Trennung:** kit-sync arbeitet auf der **Maschinen-Ebene** (einmal pro Rechner,
> plus bei Kit-Updates). Projekt-Scaffolding (Ordner, Vorlagen, Regel-Datei, CLAUDE.md)
> ist Sache von `dtb:project-init` — kit-sync fasst NIE Zielprojekt-Dateien an.

> **Determinismus-Regel:** Alle Vergleiche laufen ueber die festen Kommando-Sequenzen
> in diesem Dokument. Nicht improvisieren, keine alternativen Hash- oder Diff-Methoden.

---

## Referenz 1: Lock-Datei `~/.claude/dtb-lock.json`

Lock und Install-Manifest in EINER Datei. Sie ist die dritte Bezugsgroesse des
Drei-Punkte-Vergleichs: **Repo ↔ Lock ↔ installierte Kopie**.

```json
{
  "version": 1,
  "source": "https://github.com/spyrad/claude-code-workflow-kit.git",
  "sourceType": "github",
  "ref": "master",
  "sourceCommit": "ccc7f9e",
  "localPath": "C:/Users/SpyraD/Desktop/Projekte/claude-code-workflow-kit",
  "updatedAt": "2026-07-08",
  "artifacts": {
    "skills/dtb-workflow-next/SKILL.md": {
      "mode": "synced",
      "target": "~/.claude/skills/dtb-workflow-next/SKILL.md",
      "hash": "0fa49c58c95fc61ca988ed99d51598aa4aa4688b",
      "installedAt": "2026-07-08"
    }
  },
  "seeds": {}
}
```

| Feld | Bedeutung |
|------|-----------|
| `source` | Kanonische Quelle (GitHub-URL) — Wahrheit ist der gepushte Stand |
| `ref` | Default-Branch, beim install **dynamisch erfasst** (nie hartkodieren) |
| `sourceCommit` | Commit-SHA des Repo-Stands beim letzten install/sync |
| `localPath` | Optionaler lokaler Klon als Offline-/Schnellweg |
| `artifacts` | Ein Eintrag pro Klasse-A-Datei, Schluessel = Repo-Pfad |
| `hash` | Hash der installierten Kopie zum Zeitpunkt von install/sync (Referenz 3) |
| `seeds` | Projektlokale Seed-Ereignisse (befuellt von `dtb:project-init`, nicht von kit-sync) |

### Artefakt-Klassen

| Klasse | Repo-Quelle | Globales Ziel | mode | Drift-Check |
|--------|------------|---------------|------|-------------|
| A | `skills/dtb-*/SKILL.md` | `~/.claude/skills/dtb-*/SKILL.md` | synced | ja |
| A | `agents/*.md` | `~/.claude/agents/*.md` | synced | ja |
| A | `commands/dtb-*.md` | `~/.claude/commands/dtb-*.md` | synced | ja |
| B | `frameworks/`, `settings.json` | projektlokal (via project-init) | seed | nein — nie als Drift melden |

Nicht in v1: `personas/` (Quellen-Klaerung offen), projektlokale Ziele,
`DERIVED_STATE_RULES.md` (Seed via project-init).

---

## Referenz 2: Hashing (verbindlich)

```bash
kithash() { tr -d '\r' < "$1" | git -c core.autocrlf=false hash-object --stdin; }
```

Begruendung (Spike 2026-07-08): `git hash-object` allein ist **config-abhaengig** —
mit autocrlf=true normalisiert es, mit false nicht. `tr -d '\r'` + erzwungenes
`core.autocrlf=false` liefert auf jeder Maschine denselben Hash; LF- und CRLF-Kopien
mit gleichem Inhalt gelten damit korrekt als identisch.

---

## Referenz 3: Quelle beschaffen (feste Sequenz)

```bash
SRC="{scratchpad}/kit-src"
rm -rf "$SRC"
git clone --depth 1 "{source}" "$SRC"          # bei Erfolg: Online-Stand
REF=$(git -C "$SRC" symbolic-ref --short HEAD)  # Default-Branch dynamisch
COMMIT=$(git -C "$SRC" rev-parse --short HEAD)
```

- Clone schlaegt fehl (offline/Auth) UND `localPath` existiert → `SRC="{localPath}"`,
  im Report kennzeichnen: `Quelle: localPath (offline-Fallback — Stand kann vom
  GitHub-Stand abweichen)`
- Clone schlaegt fehl UND kein localPath → Meldung, kein Abbruch:
  `Quelle nicht erreichbar. Netzverbindung pruefen oder localPath im Lock hinterlegen.`
- Nach Abschluss des Laufs: `rm -rf "{scratchpad}/kit-src"` (Scratch aufraeumen)

---

## Modus: check (read-only)

### Sequenz

1. **Lock lesen:** `~/.claude/dtb-lock.json`. Fehlt es oder ist es kein gueltiges JSON
   → Randfall 1/10 (siehe Tabelle), Ende.
2. **Quelle beschaffen** (Referenz 3).
3. **Repo-Bestand erfassen:** alle Klasse-A-Dateien im `$SRC` gemaess Klassen-Tabelle
   auflisten, je `kithash` berechnen.
4. **Pro Repo-Datei klassifizieren** (R = Repo-Hash, L = Lock-Hash, K = Hash der
   installierten Kopie):

| Vergleich | Zustand |
|-----------|---------|
| R = L = K | synchron |
| R ≠ L, K = L | **Update verfuegbar** (Repo ist weitergezogen) |
| R = L, K ≠ L | **lokal geaendert** (Kopie weicht ab) |
| R ≠ L, K ≠ L, K = R | **Lock veraltet** (Kopie wurde manuell aktualisiert, z.B. cp am Skill vorbei) |
| R ≠ L, K ≠ L, K ≠ R | **Konflikt** (beide Seiten geaendert) |
| Kopie fehlt am `target` | **fehlt** |
| Datei im Repo, kein Lock-Eintrag | **neu** (noch nie installiert) |

5. **Verwaiste Kopien:** installierte `dtb-*`-Dateien in den drei Zielverzeichnissen,
   die keinem Repo-Pfad mehr entsprechen → **verwaist** (z.B. umbenannter Skill).
6. **Report ausgeben** (Format fix), Scratch aufraeumen.

### Report-Format (fix)

```
Kit-Sync Check
Quelle: {source} @ {REF} ({COMMIT})   [ggf. "localPath (offline-Fallback)"]
Lock:   {updatedAt}, {N} Artefakte

Abweichungen:
| Artefakt | Zustand |
|----------|---------|
| {repo-pfad} | {Zustand} |

Zusammenfassung: {N} synchron, {N} Update verfuegbar, {N} lokal geaendert,
{N} Lock veraltet, {N} Konflikt, {N} neu, {N} fehlt, {N} verwaist

{Falls Abweichungen} → Abgleich: /dtb:kit-sync sync
{Falls alles synchron} Alles synchron — keine Aktion noetig.
```

Synchrone Artefakte werden NUR gezaehlt, nie einzeln gelistet.

---

## Modus: install

Erstinstallation ODER Adoption eines bestehenden Setups (Lock fehlt/wird neu aufgebaut).

### Sequenz

1. **Quelle beschaffen** (Referenz 3). `REF` und `COMMIT` erfassen.
2. **Bestehendes Lock?** Falls gueltiges Lock existiert: Hinweis ausgeben, dass install
   das Lock neu aufbaut (Adoption), und Bestaetigung einholen.
3. **Pro Klasse-A-Datei im Repo** (Ziel gemaess Klassen-Tabelle):
   - **Ziel fehlt** → kopieren, `kithash` der neuen Kopie in den Lock-Eintrag
   - **Ziel existiert, Hash = Repo-Hash** → adoptieren: nur Lock-Eintrag schreiben
   - **Ziel existiert, Hash ≠ Repo-Hash** → **NICHT ueberschreiben**; Hash der
     VORHANDENEN Kopie in den Lock-Eintrag (der naechste check diagnostiziert dann
     korrekt "Update verfuegbar") und Datei in der Abschlussliste unter
     "adoptiert mit Abweichung" auffuehren
4. **Klasse B (Seeds):** wird von install NICHT kopiert — Seeds sind projektlokal und
   Sache von `dtb:project-init`; die `seeds`-Sektion bleibt unberuehrt.
5. **Lock schreiben:** `version`, `source`, `sourceType`, `ref: REF`,
   `sourceCommit: COMMIT`, `localPath` (falls bekannt, z.B. aus altem Lock oder wenn
   die Quelle ein lokaler Klon war), `updatedAt` (heutiges Datum), alle Artefakt-Eintraege.
6. **Abschlussreport:** Anzahl kopiert / adoptiert / adoptiert mit Abweichung;
   Empfehlung `/dtb:kit-sync check` als Verifikation. Scratch aufraeumen.

---

## Modus: sync

> Wird in Schritt 1.4 des Implementierungsplans spezifiziert (PLAN_KIT_SYNC.md).
> Bis dahin: auf `check` und manuelle Bestaetigung verweisen.

---

## Randfaelle (kein Abbruch — immer definiertes Verhalten)

| # | Situation | Verhalten |
|---|-----------|-----------|
| 1 | Kein Lock vorhanden | check/sync: Hinweis auf `/dtb:kit-sync install`; kein Abbruch |
| 2 | Kopien vorhanden, aber kein Lock (Bestand) | install adoptiert (Sequenz Schritt 3), ueberschreibt nichts |
| 3 | GitHub nicht erreichbar | localPath-Fallback, sonst Meldung (Referenz 3) |
| 4 | Artefakt im Repo geloescht/umbenannt | check: "verwaist"; sync bietet Entfernen an (mit Bestaetigung) |
| 5 | Neues Artefakt im Repo | check: "neu"; sync bietet Installation an |
| 6 | Installierte Kopie geloescht | check: "fehlt"; sync bietet Neuinstallation an |
| 7 | Konflikt (beide Seiten geaendert) | melden + einfache Wahl: Repo-Version uebernehmen / ueberspringen (kein Diff-Dialog) |
| 8 | Zeilenenden LF vs. CRLF | durch Hashing-Methode (Referenz 2) kein Drift |
| 9 | Seed-Artefakte veraendert | nie als Drift melden — Bestimmungszweck |
| 10 | Lock korrupt (ungueltiges JSON) | wie "kein Lock" behandeln: Meldung + install (Adoption) anbieten; korrupte Datei vorher nach `dtb-lock.json.bak` sichern |

---

## Verwandte Skills

- `/dtb:project-health` — prueft Drift als Check 5 (read-only, verweist hierher)
- `/dtb:project-init` — Projekt-Ebene: Scaffolding, Seeds, CLAUDE.md-Bloecke
- `/dtb:repo-sync` — NICHT verwandt: prueft Git-Status der Projekt-Repos, nicht die Kit-Distribution
