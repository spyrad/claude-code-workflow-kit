# Discovery: KIT_SYNC

**Erstellt:** 2026-07-08
**Idee-Referenz:** Inbox #4 — "Distributionsmodell light: skills-lock.json mit SHA-256 pro Skill (Drift-Erkennung installierte Kopie ↔ Repo), Sentinel-Marker fuer idempotente CLAUDE.md-Bloecke, Install-Manifest fuer sauberes Entfernen — ohne npm/Registry-Overhead"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `README.md` (## Installation) | Manuelle cp-Anleitung wird auf `/dtb:kit-sync install` umgestellt (cp bleibt als Fallback) |
| `skills/dtb-project-init/SKILL.md` | Nutzt kuenftig Sentinel-Marker fuer CLAUDE.md-Bloecke; prueft Kit-Installation statt selbst zu kopieren |
| `skills/dtb-project-health/SKILL.md` | Neuer Check 5: Drift-Meldung (read-only, verweist auf `/dtb:kit-sync sync`) |
| `skills/dtb-repo-sync/SKILL.md` | Keine Code-Beruehrung — nur Abgrenzung dokumentieren (repo-sync = Git-Status der Projekt-Repos, kit-sync = Kit-Distribution) |
| `skills/CLAUDE.md` | Konventionen fuer Lock-Format und `mode: synced/seed` dokumentieren |
| *(neu)* `skills/dtb-kit-sync/SKILL.md` | Kern des Features: ein Skill, drei Modi (check/sync/install) |
| *(neu)* `~/.claude/dtb-lock.json` | Lock + Manifest kombiniert, liegt beim Installationsziel |

---

## Anforderungen

### Scope

**Enthalten:**
- **Lock-Datei** `~/.claude/dtb-lock.json`: Lock und Install-Manifest in EINER JSON-Datei — `source` (GitHub-URL), `sourceType`, `ref`, optional `localPath`; pro Artefakt `mode` (synced/seed), `target`, `hash` (nur synced), `installedAt`
- **Drei-Punkte-Drift-Check**: GitHub-Stand ↔ Lock ↔ installierte Kopie; unterscheidet "Update verfuegbar" / "lokal geaendert" / "echter Konflikt"
- **Quelle:** `https://github.com/spyrad/claude-code-workflow-kit.git`, `ref: master` — es zaehlt immer der neueste Push; lokaler Klon (`localPath`) als optionaler Offline-/Schnellweg
- **Ein Skill** `/dtb:kit-sync` mit drei Modi: `check` (read-only Report), `sync` (Abgleich mit Bestaetigung pro Datei), `install` (Erstinstallation inkl. Adoption vorhandener Kopien)
- **Zwei Artefakt-Klassen:**
  - Klasse A (`mode: synced`, Hash + Drift-Check): `skills/`, `agents/`, `personas/`, `commands/`
  - Klasse B (`mode: seed`, einmal kopiert, nie als Drift gemeldet): `frameworks/`-Templates, `settings.json`
- **Sentinel-Marker** `<!-- BEGIN dtb -->…<!-- END dtb -->` fuer idempotente CLAUDE.md-Bloecke (genutzt von project-init)
- **project-health-Integration:** Drift-Check als Check 5, nur melden

**Nicht enthalten:**
- Kein npm, keine Registry, kein semver ("Distributionsmodell light")
- Kein Hintergrund-Sync, keine Hooks — Pruefung nur bei explizitem Aufruf
- Kein Key-Merging fuer settings.json (v1: Seed; JSON kennt keine Kommentare → keine Sentinel-Marker moeglich)
- Keine projektlokalen Installationsziele (`.claude/skills/` im Projekt) — v1 unterstuetzt nur das globale Ziel `~/.claude/`
- Keine Updates von Zielprojekt-Artefakten (BACKLOG, WORKFLOW_STATUS etc.)

### Gewuenschtes Verhalten
- `check`: read-only, kompakter Report (pro Artefakt: synchron / Update verfuegbar / lokal geaendert / Konflikt / verwaist / fehlt)
- Bei erkanntem Drift: direkt Abgleich anbieten — Bestaetigung pro Datei, lokal geaenderte Kopien werden NIE stillschweigend ueberschrieben
- `install` auf bestehendem Setup: vorhandene Kopien werden adoptiert (Hashes erfasst), nicht blind ueberschrieben
- project-init prueft kuenftig zu Beginn "Kit installiert & aktuell?" und verweist ggf. auf kit-sync — kopiert selbst nichts Globales mehr

### Randfaelle

| # | Randfall | Verhalten |
|---|----------|-----------|
| 1 | Kein Lock vorhanden (Erstnutzung/geloescht) | check/sync verweisen auf install; kein Abbruch |
| 2 | Skills installiert, aber ohne Lock (Bestand 2026-07-08) | install adoptiert vorhandene Kopien (Hashes erfassen) |
| 3 | GitHub nicht erreichbar (offline/Ausfall) | Fallback auf localPath falls hinterlegt und vorhanden; sonst klare Meldung, kein Abbruch |
| 4 | Artefakt im Repo geloescht/umbenannt (pipeline-docs-Fall) | check meldet verwaiste Kopie, sync bietet Entfernen an (mit Bestaetigung) |
| 5 | Neues Artefakt im Repo, nicht installiert | check meldet, sync bietet Installation an |
| 6 | Installierte Kopie lokal geloescht (Ziel fehlt) | check meldet, sync bietet Neuinstallation an |
| 7 | Echter Konflikt (Repo UND Kopie geaendert) | beide Diffs zeigen, Nutzer entscheidet pro Datei — nie automatisch |
| 8 | Zeilenenden Windows (Repo LF, Kopie evtl. CRLF) | Hashing normalisiert Zeilenenden (z.B. via `git hash-object`) |
| 9 | Seed-Artefakte (Klasse B) veraendert | niemals als Drift melden — das ist ihr Bestimmungszweck |

### Einschraenkungen
- Bewusst "light": nur git, SHA-256-Hashes, JSON — keine neuen Tools/Abhaengigkeiten
- Plattform: Windows (Git Bash) UND macOS/Linux; Hashing via `git hash-object` (normalisiert Zeilenenden, ueberall verfuegbar wo git ist)
- Netzwerk + git-Credentials noetig fuer GitHub-Check (funktioniert bei privatem wie oeffentlichem Repo ueber vorhandene Credentials)
- Kein Hintergrund-Mechanismus — konsistent zur Kit-Philosophie (keine Hooks, Ableitung/Pruefung nur bei Skill-Aufruf)
- EINE Lock-Datei (Lock + Manifest kombiniert) — zwei sich referenzierende Dateien waeren Fehlerquelle

### Integrationspunkte
- `project-health` → Check 5 (Drift, nur melden)
- `project-init` → Sentinel-Marker fuer CLAUDE.md-Bloecke; Kit-Pruefung statt Kopieren; klare Ebenen-Trennung: kit-sync = Maschinen-Ebene (einmal pro Rechner + bei Kit-Updates), project-init = Projekt-Ebene (einmal pro Projekt, Scaffolding/Seeds)
- `README.md` → Installationsabschnitt auf kit-sync umstellen
- `skills/CLAUDE.md` → Lock-/Manifest-Konventionen dokumentieren
- `dtb-repo-sync` → nur Doku-Abgrenzung, keine Code-Beruehrung
- `pipeline-graph` → neuer Skill erscheint automatisch ueber Frontmatter
- Extern: nur git + GitHub, keine neuen Abhaengigkeiten

---

## Abhaengigkeiten

- Bestehende Features: 1 — DERIVED_STATE (Abgenommen, wartet auf Archivierung): kein Konflikt
- Synergie: project-health wurde durch DERIVED_STATE bereits um 4 Checks erweitert, Drift-Check folgt demselben Muster als Check 5
- Vorausschau Idee #7 (Change-Folder-Modell): aendert spaeter Projekt-Artefakt-Pfade, kit-sync verteilt Kit-Dateien — keine Blockade in beide Richtungen

---

## Offene Punkte

- `DERIVED_STATE_RULES.md` im Zielprojekt: inhaltlich Kit-gepflegt (Klasse A), liegt aber projektlokal — deckt der Drift-Check sie in v1 mit ab oder bleibt sie Seed? → Entscheidung in der Spec
- Genaues Lock-Schema (Feldnamen, Versionsfeld) → Implementierungsplan
- Projektlokale Installationsziele als spaetere Ausbaustufe (v2)

---

**Erstellt mit:** `/dtb:feature-discover`
