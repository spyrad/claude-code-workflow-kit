# Implementierungsplan: KIT_SYNC

**Erstellt:** 2026-07-08
**Feature-Spec:** `features/FEATURE_KIT_SYNC.md`
**Geschaetzte Dauer:** 2-3 Sessions
**Status:** Reviewed (Plan-Review 2026-07-08: 3 Agenten, 3 Entscheidungen, 6 Empfehlungen eingearbeitet)

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Lock-Schema & Kern-Skill kit-sync (check/install/sync) | 1 Session | Geplant |
| Phase 2 | Sentinel-Marker & project-init-Umbau (abtrennbares Paket) | 0.5 Session | Geplant |
| Phase 3 | Integration, Fixture-Tests, Realtest, Doku | 1 Session | Geplant |

---

## Phase 1: Lock-Schema & Kern-Skill

### Ziel
`/dtb:kit-sync` existiert mit allen drei Modi; das Lock-Format ist definiert und dokumentiert.

### Schritte

#### Schritt 1.1: Lock-Schema definieren + Skill-Geruest anlegen
- **Zweck:** Datenmodell festzurren, bevor Verhalten implementiert wird
- **Dateien:** `skills/dtb-kit-sync/SKILL.md` (neu)
- **Input:** Discovery (Scope, Klassen A/B), 10x-Vorbild `skills-lock.json`, Review-Entscheidungen 2026-07-08
- **Output:** Frontmatter (pipeline: stage monitoring) + Referenzabschnitt "Lock-Format" im SKILL.md: `version`, `source`, `sourceType`, `ref` (wird beim install dynamisch vom Repo erfasst, nicht hartkodiert), `localPath?`, pro Artefakt `mode: synced|seed`, `target`, `hash?`, `installedAt`; Artefakt-Klassen-Tabelle (A: skills/agents/commands — alle global unter `~/.claude/`; B: frameworks, settings.json; Personas NICHT in v1)
- **Hash-Spike (Pflichtteil):** `git hash-object` mit/ohne `--path` gegen CRLF-Fixture testen — normalisiert es NICHT zuverlaessig, Fallback `tr -d '\r' | git hash-object --stdin`; das Spike-Ergebnis legt die Hashing-Methode fuer alle Modi fest

#### Schritt 1.2: Modus `check` implementieren
- **Zweck:** Kern-Nutzen — Drift sichtbar machen (read-only)
- **Dateien:** `skills/dtb-kit-sync/SKILL.md`
- **Input:** Lock-Schema aus 1.1
- **Output:** Anleitung fuer Drei-Punkte-Vergleich (GitHub via shallow clone ins Scratch-Verzeichnis ↔ Lock ↔ Kopie) als **feste Bash-Kommando-Sequenzen** + **fixes Report-Format** mit 6 Zustaenden (synchron / Update verfuegbar / lokal geaendert / Konflikt / verwaist / fehlt) — Determinismus ist Kernanforderung (Pre-Mortem-Befund: improvisierte Ablaeufe zerstoeren das Vertrauen); Fallbacks (kein Lock ODER korruptes Lock-JSON → wie fehlend behandeln, install anbieten; offline → localPath bzw. Meldung)

#### Schritt 1.3: Modus `install` implementieren
- **Zweck:** Erstinstallation + Adoption des Bestands (Randfall 2)
- **Dateien:** `skills/dtb-kit-sync/SKILL.md`
- **Input:** Lock-Schema, Klassen-Tabelle
- **Output:** Anleitung: Klasse A kopieren/adoptieren (vorhandene identische Kopien nur hashen, abweichende NICHT ueberschreiben → als Drift melden), Klasse B nur bei Fehlen seeden, `~/.claude/dtb-lock.json` schreiben

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

#### Schritt 1.4: Modus `sync` implementieren
- **Zweck:** Kontrollierter Abgleich nach Drift-Befund
- **Dateien:** `skills/dtb-kit-sync/SKILL.md`
- **Input:** check-Diagnose aus 1.2
- **Output:** Anleitung als feste Kommando-Sequenzen: Aktionen je Zustand (Update uebernehmen / verwaiste Kopie entfernen / fehlende neu installieren); **Konflikt-Ast schlank** (Nutzer-Entscheidung 2026-07-08: installierte Kopien werden nie lokal editiert): "lokal geaendert" wird gemeldet + einfache Wahl "Repo-Version uebernehmen / ueberspringen", kein Diff-Dialog; Lock nach jeder Aktion aktualisieren; NIE stillschweigend ueberschreiben

### Deliverables
- [ ] `skills/dtb-kit-sync/SKILL.md` vollstaendig (3 Modi + Lock-Referenz + Randfall-Tabelle)

### Checkpoint-Kriterien
- [ ] Alle 10 Randfaelle sind im Skill abgedeckt (9 aus der Discovery + Randfall 10: korruptes Lock-JSON), keiner fuehrt zu Abbruch
- [ ] Lock-Schema deckt beide Klassen ab (synced mit Hash, seed ohne)

---

## Phase 2: Sentinel-Marker & project-init

> **Abtrennbares Paket** (Review-Empfehlung): kein Muss fuer den Kern-Nutzen (Drift-Erkennung).
> Bei Session-Engpass kann Phase 2 als eigener Meilenstein nachgezogen werden — Phase 3 haengt
> nur mit Schritt 3.2 (Idempotenz-Fixture) und SC9 daran.

### Ziel
project-init schreibt idempotente CLAUDE.md-Bloecke und respektiert die Ebenen-Trennung.

### Schritte

#### Schritt 2.1: Sentinel-Marker in project-init
- **Zweck:** Kit-Bloecke in Ziel-CLAUDE.md idempotent aktualisierbar machen
- **Dateien:** `skills/dtb-project-init/SKILL.md`
- **Input:** Marker-Konvention `<!-- BEGIN dtb -->…<!-- END dtb -->`
- **Output:** CLAUDE.md-Template mit Markern; Update-Logik (Block ersetzen statt anhaengen); Migration: marker-lose Alt-Bloecke erkennen und einmalige Umstellung anbieten

#### Schritt 2.2: Ebenen-Trennung in project-init
- **Zweck:** project-init kopiert nichts Globales mehr (Maschinen- vs. Projekt-Ebene)
- **Dateien:** `skills/dtb-project-init/SKILL.md`
- **Input:** kit-sync aus Phase 1
- **Output:** Eingangspruefung "Kit installiert & aktuell?" (Lock vorhanden? check-Kurzlauf) mit Verweis auf `/dtb:kit-sync install`; projektlokale Seeds (Ordner, Vorlagen, Regel-Datei) bleiben bei project-init

### Deliverables
- [ ] project-init idempotent (Marker) + entlastet (keine globalen Kopien)

### Checkpoint-Kriterien
- [ ] Zweiter project-init-Lauf aendert Nutzertext nicht (Idempotenz)

---

## Phase 3: Integration, Tests, Doku

### Ziel
Drift-Check in project-health integriert, alle Success Criteria per Fixture/Realtest belegt, Doku konsistent.

### Schritte

#### Schritt 3.1: project-health Check 5
- **Zweck:** Drift faellt im Alltag auf, ohne dass man kit-sync kennen muss
- **Dateien:** `skills/dtb-project-health/SKILL.md`
- **Input:** check-Logik aus 1.2 (referenzieren, nicht duplizieren)
- **Output:** Check 5 "Kit-Drift" (read-only Kurzform, verweist auf `/dtb:kit-sync sync`); Fallback ohne Lock: Hinweis auf install, kein FAIL

> **3x3-Block:** Nach Schritt 3.1 → Zusammenfassung + Feedback einholen (2.1, 2.2, 3.1)

#### Schritt 3.2: Fixture-Tests
- **Zweck:** Success Criteria 2-7 und 9 belegen
- **Dateien:** Scratch-Fixtures (nicht versioniert), Testprotokoll im Session-Log
- **Input:** Fixtures: nur Repo geaendert / nur Kopie geaendert / beide (Konflikt) / verwaiste Kopie / CRLF-Kopie / korruptes Lock / offline / project-init-Zweitlauf
- **Output:** Testprotokoll (Szenario → erwartet → beobachtet), **verbindlich durch unabhaengigen Agenten ohne Session-Kenntnis** (Muster DERIVED_STATE Phase 3, Nutzer-Entscheidung 2026-07-08)

#### Schritt 3.3: Realtest — install auf dem Bestand
- **Zweck:** Success Criterion 1 am echten Setup (Adoption der 28 Skills vom 2026-07-08)
- **Dateien:** `~/.claude/dtb-lock.json` (entsteht real)
- **Input:** kit-sync install, GitHub-Repo als Quelle
- **Output:** Lock mit allen Klasse-A-Artefakten; anschliessender check meldet "alles synchron"

> **3x3-Block:** Nach Schritt 3.3 → Zusammenfassung + Feedback einholen

#### Schritt 3.4: Doku + Abnahme
- **Zweck:** Installationsweg und Konventionen konsistent machen
- **Dateien:** `README.md`, `skills/CLAUDE.md`, `CLAUDE.md`, `skills/dtb-repo-sync/SKILL.md` (nur Abgrenzungshinweis)
- **Input:** Alle vorherigen Schritte
- **Output:** README-Installation via kit-sync (cp als Fallback), Lock-Konventionen dokumentiert, repo-sync/kit-sync-Abgrenzung, pipeline-graph regeneriert, alle 10 Success Criteria in FEATURE_KIT_SYNC.md abgehakt

### Deliverables
- [ ] Testprotokoll mit allen Fixtures bestanden
- [ ] Reales Lock auf diesem Rechner, check = synchron
- [ ] Doku + pipeline-graph aktuell

### Checkpoint-Kriterien
- [ ] Alle 10 Success Criteria aus FEATURE_KIT_SYNC.md abgehakt

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Ablage Lock-Schema-Doku | eigener project-rules-Eintrag vs. Referenzabschnitt im kit-sync SKILL.md | SKILL.md | kit-sync ist Maschinen-Ebene; project-rules/ ist projektlokal — passt konzeptionell nicht; project-health referenziert den Skill |
| Hashing | `sha256sum` vs. `git hash-object` (mit/ohne `--path`) vs. `tr -d '\r'`-Normalisierung | Spike in 1.1 | Annahme "git hash-object normalisiert" ist ungetestet (Review-Befund Senior Dev) — Spike-Ergebnis entscheidet |
| Klasse-A-Umfang v1 | nur skills vs. skills+agents+commands vs. inkl. Personas | skills+agents+commands | alle drei haben reale globale Ziele unter `~/.claude/` (verifiziert 2026-07-08); Personas raus: installierter Command referenziert externes oma-personas-Repo — Quellen-Klaerung noetig (v2) |
| Konflikt-Behandlung | Diff-Dialog vs. schlank (melden + Wahl) | schlank | Nutzer editiert installierte Kopien nie lokal (Entscheidung 2026-07-08); Schutzregel bleibt |
| `ref` im Lock | hartkodiert `master` vs. dynamisch beim install erfassen | dynamisch | Repo-Default-Branch kann abweichen (main); Review-Empfehlung 5 |
| GitHub-Zugriff | Raw-URLs vs. shallow clone (`--depth 1`) ins Scratch-Verzeichnis | shallow clone | ein Befehl fuer alle Dateien, Auth ueber vorhandene git-Credentials (auch privat), keine API-Rate-Limits |
| settings.json v1 | Seed vs. Key-Merging | Seed | JSON ohne Kommentare → keine Sentinel-Marker; Merging ist v2-Kandidat (in Spec ausgeklammert) |
| DERIVED_STATE_RULES.md im Zielprojekt | Drift-Check in v1 vs. Seed | Seed | Plan-Review 2026-07-08: projektlokales Ziel passt nicht ins globale v1-Lock; Verteilung bleibt bei project-init |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Nach jedem umgesetzten Schritt sofort abhaken; Commit-SHA als Beleg (optional bei Schritten ohne Commit).

- [ ] 1.1 Lock-Schema + Skill-Geruest
- [ ] 1.2 Modus check
- [ ] 1.3 Modus install
- [ ] 1.4 Modus sync
- [ ] 2.1 Sentinel-Marker in project-init
- [ ] 2.2 Ebenen-Trennung project-init
- [ ] 3.1 project-health Check 5
- [ ] 3.2 Fixture-Tests
- [ ] 3.3 Realtest install auf Bestand
- [ ] 3.4 Doku + Abnahme

---

## 3x3 Umsetzungsrhythmus

Dieser Plan ist fuer die Umsetzung im **3x3-Rhythmus** ausgelegt:

1. Implementiere max. 3 Schritte aus dem Plan
2. Hake die erledigten Schritte in `## Progress` ab (Commit-SHA als Beleg)
3. Fasse kurz zusammen was erledigt wurde
4. Beschreibe die naechsten 3 Schritte
5. **Stoppe und warte auf Feedback** bevor du weiterarbeitest

Bei Kontextverlust oder nach >6 Schritten: Die `## Progress`-Sektion ist der Wiedereinstiegspunkt —
in neuer Konversation `PLAN_KIT_SYNC.md` laden; der erste nicht abgehakte Schritt ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
