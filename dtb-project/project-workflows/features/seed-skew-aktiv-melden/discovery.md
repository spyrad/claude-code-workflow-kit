# Discovery: Seed-Skew aktiv melden
<!-- resume: done -->

**Erstellt:** 2026-11-09
**Idee-Referenz:** Inbox #22 — "Seed-Skew aktiv melden: Seeds (`DERIVED_STATE_RULES.md`, `settings.json`) sind bewusst „copied once, never drift-checked" (Klasse B) — … `kit-sync check` oder `project-health` meldet veraltete Seeds als eigenen Hinweis-Zustand (informativ, KEIN Auto-Update …)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-kit-sync/SKILL.md` | Träger: check-Sequenz (neuer Seed-Schritt nach den Verwaist-Kopien), Report-Format (eigener Seed-Block, geänderte Schlusszeile), Klassen-Tabelle (Zeile 78 und Absatz Zeile 80-82: `DERIVED_STATE_RULES.md` „nicht in v1"), Randfall 9 (Zeile 265 „nie als Drift melden") |
| `CLAUDE.md` | Spiegel: Distributionsmodell, Zeile 25 „copied per project by `dtb:project-init` and never drift-checked" |
| `skills/CLAUDE.md` | Spiegel: Abschnitt „Distribution (kit-sync)", Zeile 656 „Class B (`mode: seed`, copied once, never drift-checked)" |
| `skills/dtb-project-init/SKILL.md` | nur gelesen: Seed-Politik (Zeile 313-314: Regel-Datei wird überschrieben, `settings.json` nie) — Grundlage der Abgrenzung, keine Änderung |
| `skills/dtb-project-health/SKILL.md` | nur gelesen: Check 11 „Seeds (`mode: seed`) NIE pruefen" (Zeile 258) — bleibt unverändert |

---

## Anforderungen

### Scope
**Enthalten:**
- `kit-sync check` vergleicht die Regel-Datei `DERIVED_STATE_RULES.md` des Projekts im
  Arbeitsverzeichnis inhaltlich mit der Kit-Fassung aus der ohnehin beschafften Quelle
  (Hashing nach Referenz 2 des Skills, Zwei-Punkt-Vergleich ohne Lock-Eintrag)
- Eigener Seed-Block im Report, getrennt von den Drift-Zahlen; Schlusszeile ändert sich, wenn
  der Seed abweicht
- Spiegelstellen in `CLAUDE.md` und `skills/CLAUDE.md` nachziehen

**Nicht enthalten:**
- Kein Auto-Update, kein Schreibzugriff aufs Projekt — Seeds bleiben projektgehörig
- Kein Vergleich von `settings.json` (projekteigen, Abweichung ist dort der Normalfall)
- Keine Änderung an `sync`, `install` und am Lock-Schema (`seeds: {}` bleibt unbenutzt)
- Kein zweiter Träger in `dtb:project-health` (Check 11 bleibt Drift-only)

### Gewuenschtes Verhalten
- Seed gleich der Kit-Fassung → eine Zeile „aktuell", Schlusszeile unverändert
- Seed weicht ab → Zeile „weicht von der Kit-Fassung ab" (neutral, nicht „veraltet"), dazu ein
  Vergleichsbefehl und die Abhilfe `/dtb:project-init` (verteilt Seeds, überschreibt die
  Regel-Datei) bzw. Hand-Kopie nach Vergleich; die Schlusszeile lautet dann sinngemäß
  „Kit-Kopien synchron — Seed weicht ab (siehe oben)" statt „Alles synchron — keine Aktion noetig"
- Kein DTB-Projekt im Arbeitsverzeichnis (keine `workflow.config.yaml` bzw. keine Regel-Datei am
  aufgelösten Pfad) → genau eine Zeile „Seed nicht geprüft", kein Fehler

### Randfaelle
- Arbeitsverzeichnis ist das Kit-Repo selbst: die Regel-Datei ist dort die Quelle; der Vergleich
  läuft trotzdem gegen den gepushten Stand und zeigt ungepushte lokale Änderungen ehrlich an
- Quelle offline → localPath-Fallback der bestehenden Referenz 3 gilt auch für den Seed-Vergleich
- Eine Vergleichsseite leer oder nicht lesbar → Werkzeug-Fehlschlag, kein Datenbefund (harte
  Prüfung beider Seiten vor dem Vergleich)
- Zeilenenden LF/CRLF → durch die Hashing-Methode kein Unterschied
- Regelpfad aus `workflow.config.yaml` → `paths.rules`, Fallback `dtb-project/project-rules/`

### Einschraenkungen
- kit-sync bleibt Maschinen-Ebene und schreibt nie ins Projekt (Ebenen-Trennung des Skills)
- Feste Kommando-Sequenzen des Skills nicht durch eigene Hash-/Diff-Methoden ersetzen
- Probeläufe gegen die Repo-Fassung `skills/dtb-kit-sync/SKILL.md`, nicht gegen die installierte Kopie

### Integrationspunkte
- `dtb:project-init` als Abhilfe-Ziel (Seed-Verteilung, Abschnitt „Seeds verteilen")
- `dtb:project-health` Check 11 verweist auf `kit-sync check` — der neue Hinweis wird darüber
  mittelbar erreichbar, ohne dass Check 11 sich ändert

---

## Abhaengigkeiten

- Keine — die Quelle beschafft `check` bereits (Referenz 3), das Hashing existiert (Referenz 2)

---

## Offene Punkte

- Läuft `/dtb:project-init` in einem bereits eingerichteten Projekt bis zur Seed-Verteilung durch,
  ohne das Interview zu wiederholen? (Schritt 0 fragt bei vorhandener Config nach einem Update —
  ob danach nur die Seeds erneuert werden können, ist ungeprüft; bestimmt den Wortlaut der
  Abhilfe-Zeile)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)
