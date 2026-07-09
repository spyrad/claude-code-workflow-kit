# Feature: KIT_SYNC

**Erstellt:** 2026-07-08
**Ziel:** Drift zwischen Kit-Repo und installierten Kopien wird automatisch erkannt und kontrolliert abgeglichen — manueller, fehleranfaelliger Sync entfaellt.
**Prioritaet:** Hoch
**Status:** Abgeschlossen (2026-07-08 — archiviert; Abnahme nach Praxiserprobung check → sync gegen GitHub-Quelle) <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Zwischen dem Kit-Repo (Quelle) und den installierten Kopien unter `~/.claude/` gibt es heute keinerlei Tooling — Installation ist ein manuelles `cp -r`, Drift bleibt unbemerkt (belegt: 14 veraltete Skills am 2026-07-08, alter Resume-Skill lief unbemerkt; pipeline-docs-Leiche am 2026-07-03). Kuenftig haelt eine Lock-Datei (`~/.claude/dtb-lock.json`) pro Artefakt Herkunft und SHA-256-Hash fest; ein neuer Skill `/dtb:kit-sync` (Modi check/sync/install) prueft drei Punkte — GitHub-Stand ↔ Lock ↔ installierte Kopie — und gleicht kontrolliert ab. Sentinel-Marker machen die CLAUDE.md-Bloecke von project-init idempotent. (Vorbild: 10x-devs-3.0 skills-lock/pack-init, ohne npm/Registry-Overhead.)

---

## Scope / Abgrenzung

### Enthalten
- **Lock + Manifest in EINER Datei** `~/.claude/dtb-lock.json`: `source` (GitHub-URL `https://github.com/spyrad/claude-code-workflow-kit.git`), `sourceType`, `ref: master` (es zaehlt der neueste Push), optional `localPath` als Offline-/Schnellweg; pro Artefakt `mode`, `target`, `hash` (nur synced), `installedAt`
- **Zwei Artefakt-Klassen:** Klasse A `mode: synced` mit Hash + Drift-Check (`skills/`, `agents/`, `commands/` — alle mit realem globalem Ziel unter `~/.claude/`, verifiziert 2026-07-08); Klasse B `mode: seed` — einmal kopiert, nie als Drift gemeldet (`frameworks/`-Templates, `settings.json`)
- **Neuer Skill `/dtb:kit-sync`** mit drei Modi:
  - `check` — read-only Drei-Punkte-Report: synchron / Update verfuegbar / lokal geaendert / Konflikt / verwaist / fehlt
  - `sync` — Abgleich mit Bestaetigung pro Datei; lokal geaenderte Kopien werden NIE stillschweigend ueberschrieben
  - `install` — Erstinstallation; adoptiert vorhandene Kopien (Hashes erfassen statt ueberschreiben)
- **Sentinel-Marker** `<!-- BEGIN dtb -->…<!-- END dtb -->`: project-init schreibt seine CLAUDE.md-Bloecke idempotent (Kit-Updates aktualisieren Kit-Bloecke, Nutzertext bleibt unberuehrt)
- **project-health:** Drift-Check als Check 5 (nur melden, verweist auf `/dtb:kit-sync sync`)
- **Ebenen-Trennung:** kit-sync = Maschinen-Ebene (einmal pro Rechner + bei Kit-Updates); project-init = Projekt-Ebene (Scaffolding/Seeds, prueft kuenftig nur noch "Kit installiert & aktuell?" statt selbst global zu kopieren)
- **Doku:** README-Installation auf kit-sync umstellen (cp als Fallback), Lock-Konventionen in `skills/CLAUDE.md`, Abgrenzung zu `dtb:repo-sync`

### Nicht enthalten
- Kein npm, keine Registry, kein semver ("Distributionsmodell light")
- Kein Hintergrund-Sync, keine Hooks — Pruefung nur bei explizitem Skill-Aufruf (Kit-Philosophie)
- Kein Key-Merging fuer `settings.json` (v1: Seed; JSON kennt keine Kommentare → keine Sentinel-Marker moeglich)
- Keine projektlokalen Installationsziele (`.claude/skills/` im Projekt) — v1 nur globales Ziel `~/.claude/` (v2-Kandidat)
- Keine `personas/` in v1: der installierte Command referenziert ein externes Repo (`oma-personas`) statt der Kit-Kopie — Quellen-Klaerung ist eine eigene Aufraeum-Entscheidung (Plan-Review 2026-07-08)
- `DERIVED_STATE_RULES.md` bleibt Seed via project-init (projektlokales Ziel passt nicht ins globale v1-Lock)
- Keine Updates von Zielprojekt-Artefakten (BACKLOG, WORKFLOW_STATUS etc.)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Zeilenenden-Falsch-Drift: Repo LF, Windows-Kopie CRLF → Hash weicht ab trotz identischem Inhalt | Hoch | Mittel | Hashing via `git hash-object` (normalisiert, ueberall verfuegbar wo git ist); Success Criterion mit CRLF-Fixture |
| Lock veraltet durch manuelles cp am Skill vorbei | Mittel | Mittel | check erkennt das als "lokal geaendert"; sync bietet Re-Adoption an; README verweist primaer auf kit-sync |
| Nutzer aendert installierte Kopie bewusst lokal | Mittel | Hoch | Drei-Punkte-Diagnose unterscheidet lokale Aenderung von Update; nie stillschweigend ueberschreiben, Diff zeigen |
| GitHub nicht erreichbar (offline/Ausfall) | Niedrig | Niedrig | Fallback localPath; sonst klare Meldung, kein Abbruch (Fallback-Philosophie wie Derived State) |
| Skill-Komplexitaet: 3 Modi + 9 Randfaelle in einem SKILL.md | Mittel | Mittel | Modi klar getrennt strukturieren; Randfall-Tabelle statt Prosa; ggf. Referenzteil analog DERIVED_STATE_RULES |
| Bestehende Ziel-CLAUDE.md ohne Sentinel-Marker | Mittel | Niedrig | project-init erkennt marker-lose Alt-Bloecke und bietet einmalige Migration an |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — DERIVED_STATE ist abgenommen, kein konkurrierendes Feature aktiv

### Referenz-Dokumente
- `features/DISCOVERY_KIT_SYNC.md` - Discovery mit Scan, 9 Randfaellen, Constraints, Integrationspunkten
- `dtb-project/project-workflows/INBOX.md` - Idee #4 (Ursprung), Schmerz belegt 2026-07-03 und 2026-07-08
- `dtb-project/project-changelog/2026-07/2026-07-08.md` - 14-Skill-Sync-Fall (alter Resume-Skill lief unbemerkt)
- `C:/Users/SpyraD/Desktop/Projekte/10x-devs-3.0/skills-lock.json` - Vorbild-Referenz (Lock-Format)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [x] `/dtb:kit-sync install` auf dem Bestand vom 2026-07-08 erzeugt `~/.claude/dtb-lock.json` mit allen Klasse-A-Artefakten (Hash, Ziel, Datum) und adoptiert die vorhandenen Kopien ohne Ueberschreiben — Realtest 2026-07-08: 34 Artefakte, 1 kopiert / 30 adoptiert / 3 mit Abweichung, nichts ueberschrieben
- [x] `/dtb:kit-sync check` erkennt den Drift-Fall des 2026-07-08 (Repo-Datei neuer als Kopie) als "Update verfuegbar" — nicht als lokale Aenderung — Fixture ALPHA + real (project-health/project-init), 2026-07-08
- [x] Drei-Punkte-Diagnose unterscheidet die drei Drift-Arten korrekt — Fixtures ALPHA (Update) / BETA (lokal geaendert) / GAMMA (Konflikt), unabhaengiger Agent, 2026-07-08
- [x] `sync` ueberschreibt eine lokal geaenderte Kopie nie ohne explizite Bestaetigung — Buendel-2-Regel; real: dtb-pitch-coach bewusst uebersprungen (Anm.: Diff-Dialog per Plan-Review-Entscheidung zu einfacher Wahl verschlankt)
- [x] Verwaiste Kopie wird erkannt, Entfernen wird angeboten — Fixture ORPHAN, 2026-07-08
- [x] Identischer Inhalt mit LF vs. CRLF erzeugt KEINEN Drift — Hash-Spike + Fixture DELTA (Methode: tr + git hash-object mit autocrlf=false erzwungen), 2026-07-08
- [x] Offline-Verhalten: ohne Netz klare Meldung bzw. localPath-Fallback, kein Abbruch — Fixture-Szenario C, 2026-07-08
- [x] `project-health` meldet Drift read-only und verweist auf kit-sync — implementiert als Check 11 (Plan sprach von "Check 5"; real hat der Skill 10 Bestands-Checks), `aa87aa9`
- [x] Zweiter `project-init`-Lauf auf einem Projekt mit Sentinel-Markern aendert Nutzertext in CLAUDE.md nicht — Fixture-Szenario D: Nutzertext byte-identisch, nur Block zwischen Markern ersetzt, 2026-07-08
- [x] README-Installation verweist primaer auf `/dtb:kit-sync install` (inkl. Bootstrap-Schritt); `pipeline-graph` zeigt den neuen Skill ohne Nacharbeit — 2026-07-08

---

**Erstellt mit:** `/dtb:feature-plan`
