# Feature: Projekt-Dashboard

**Erstellt:** 2026-10-26
**Ziel:** Eine lokale, grafisch ansprechende HTML-Seite zeigt den Projektstand auf einen Blick — ohne Nachfragen, ohne Checkpoint-Zwang.
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Der Projektstand ist heute über sieben Dateien verteilt (Status, Backlog, INBOX, Befund-Becken,
Lektionen, Session-Logs, Change-Ordner) und nur per Skill-Aufruf im Terminal sichtbar. Ein neuer
Skill `dtb:project-dashboard` bündelt diesen Stand in einer einzigen, rein lesenden HTML-Seite
(Stil angelehnt an aihero.dev, dunkel als Standard). Sie entsteht auf Abruf und automatisch beim
Checkpoint — so ist sie nach jeder Session aktuell und zwischendurch jederzeit auffrischbar.

Grundlage: `discovery.md` (gleicher Ordner) — dort stehen die extrahierten Design-Werte und alle
Einzelentscheidungen.

---

## Scope / Abgrenzung

### Enthalten

**Inhalt der Seite** (Reihenfolge von oben nach unten):
- **Kennzahlen-Leiste:** grosse Zahl + kleines Label je Kennzahl — genau sechs, in dieser
  Reihenfolge: offene Ideen, ungesichtete Befunde, Lektionen (mit Füllstand), aktive Changes,
  offene Aufgaben (mit Anzahl ⏳), Worktrees
- **Wo wir stehen:** aktives Feature mit Fortschritt (X/Y Schritte), offene Aufgaben (mit Alter/⏳
  nach DSR §9), laufende Worktrees (DSR §10), nächster empfohlener Befehl
- **Backlog nach Status:** Features/Aufgaben gruppiert nach dem *abgeleiteten* Status (DSR §3 —
  In Discovery, Spezifiziert, Geplant, In Arbeit, Fertig zum Testen, Abgenommen, Pausiert);
  Quelle sind die Artefakte, nicht die Anzeigespalte in BACKLOG.md
- **Zuletzt gemacht:** zwei Spalten nebeneinander — links die letzten 5 Sessions (Datum,
  Session-Kopf und der erste erledigte Punkt als Kurztext, denn der Session-Kopf trägt nur die
  Uhrzeit), rechts die abgeschlossenen Meilensteine aus dem Status
- **INBOX + Befund-Becken:** je Anzahl + die neuesten 10 mit Kurztitel, Rest einklappbar
  („alle N anzeigen"); Becken-Einträge status-neutral (DSR §6.4)
- **Lektionen:** Anzahl + Füllstand gegen das Soft-Limit (~150 Zeilen); ab mehr als ~150 Zeilen
  das Signal „Kuratierung fällig → INBOX #141" — dieselbe Schwelle wie beim Erfassen einer
  Lektion (eine Definition, nicht zwei)
- Einträge verlinken relativ auf ihre Quelldatei

**Gestaltung:**
- Design-Sprache angelehnt an https://www.aihero.dev/ — nur Stil (Farben, Typo-Hierarchie,
  Kennzahlen-Muster, Formen), kein Logo, kein Bildmaterial, kein Markenname. Werte: `discovery.md`
  → „Gewuenschtes Verhalten"
- **Dunkel ist Standard**; ein Umschalter oben rechts wechselt auf Hell, die Wahl merkt sich der Browser
- Nur Systemschriften; die Seite ist vollständig lokal und lädt keine Ressource von einer externen Adresse

**Erzeugung & Aktualisierung — zwei Wege, ein Ergebnis:**
- **Auf Abruf:** `/dtb:project-dashboard` erzeugt die Seite und öffnet sie im Browser
- **Automatisch:** `/dtb:workflow-checkpoint` erzeugt sie am Session-Ende ohne Browser-Popup, nur
  mit einer Pfad-Zeile in der Bestätigung; per Config `dashboard.bei_checkpoint` abschaltbar
  (Standard: an)
- Beide Wege nutzen dasselbe Seitengerüst; es liegt genau einmal im neuen Skill, der Checkpoint
  verweist darauf (keine Kopie)
- Ablage `dtb-project/project-dashboard.html`, unversioniert; in Zielprojekten prüft der Skill
  einmal, ob die Datei vom Versionieren ausgeschlossen ist, und schlägt sonst die Ausschluss-Zeile vor
- Verteilter Kit-Skill: läuft in jedem Zielprojekt; Distribution über `dtb:kit-sync` wie jeder Skill

**Robustheit:**
- Fehlende Quelldatei → der Block bleibt stehen, gedämpft, mit „nicht vorhanden: {Datei}"
- Widersprüchliche oder defekte Daten → Artefakt gewinnt (DSR §1.3), der Konflikt erscheint als
  **Warnchip** am Eintrag
- Kein aktives Feature → Leerzustand mit dem empfohlenen nächsten Befehl
- Inhalte aus Quelldateien werden so dargestellt, dass Sonderzeichen die Seite nicht zerbrechen
- **Worktree:** auf Abruf erzeugt, mit Banner „Worktree-Ansicht — massgeblich ist der
  Haupt-Checkout"; der Checkpoint läuft im Worktree gar nicht (er bricht dort vor dem ersten
  Schritt ab) — die Seite wird nach dem Merge im Haupt-Checkout aktualisiert

### Nicht enthalten
- Aktionen auf der Seite — sie ist rein lesend und ändert keine Projektdatei
- Live-Server / automatisches Nachladen (spätere Option)
- Trends oder Historie über Zeit
- Ablösung von WORKFLOW_STATUS.md oder der Terminal-Sichten (`workflow-status`, `workflow-next`,
  `backlog-status` bleiben unverändert)
- Inhalt oder Bewertung einzelner Lektionen — das ist Kuratierung (INBOX #141)
- `[Fach]`-Fragen (später ergänzbar; Sicht dafür heute `dtb:meeting-agenda`)
- Eigener Datenschutz-Filter (Schutz gehört an die Quelle → INBOX #110)
- Projekt-eigene Design-Tokens als Override des Kit-Stils
- Ausbaustufe „nur Daten schreiben, festes Gerüst liest sie ein" (nur falls Kosten spürbar werden)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Aussehen schwankt zwischen Läufen, weil Claude die Seite jedes Mal neu schreibt | Mittel | Mittel | Festes Gerüst mit klar benannten Daten-Slots; nur die Slots werden gefüllt, Struktur und Stil sind vorgegeben |
| Checkpoint wird spürbar langsamer bzw. teurer | Mittel | Niedrig | Schalter `dashboard.bei_checkpoint`; Ausbaustufe „nur Daten schreiben" als vorbereiteter zweiter Schritt |
| Statusableitung im Dashboard driftet von den Terminal-Sichten ab | Mittel | Mittel | Ableitung per Verweis auf DERIVED_STATE_RULES, nie nachgebaut; dieselben Paragraphen wie `workflow-status`/`workflow-next` |
| Verweis Checkpoint → Skill bricht bei späterem Umbau des Skills | Niedrig | Hoch | Struktur-Check im Checkpoint auf einen festen Anker im Skill (Muster `pane-start` → `worker`) mit eigener Fehlermeldung |
| Quellen in Bestandsprojekten weichen im Format ab (alte Tabellen, fehlende Dateien) | Hoch | Niedrig | „nicht vorhanden"-Blöcke und Warnchips statt Abbruch; Abnahme im Referenz-Testbett |
| Generierte Seite landet in Zielprojekten versehentlich in der Versionierung | Mittel | Niedrig | Einmalige Prüfung durch den Skill + vorgeschlagene Ausschluss-Zeile |
| Seite bündelt personenbezogene Klartexte aus den Quellen gut lesbar | Niedrig | Mittel | Rein lokal, unversioniert, keine Übertragung; Schutz an der Quelle (INBOX #110) |

---

## Dependencies

### Erforderlich vor Start
- [x] Discovery abgeschlossen (`discovery.md`, 2026-10-26)
- [ ] Einfügestelle im aktuellen `workflow-checkpoint` (zwischen Schritt 4 und 5) beim Planen gegen den Ist-Stand prüfen — meistgeänderter Skill des Kits

### Referenz-Dokumente
- `dtb-project/project-workflows/features/projekt-dashboard/discovery.md` - Anforderungen, Design-Werte, Einzelentscheidungen
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - §1–§3 Status, §6.4 Becken, §9 offene Aufgaben, §10 Worktrees
- `skills/dtb-pipeline-graph/SKILL.md` - Vorbild: eigenständige HTML-Seite, von Claude geschrieben, unversioniert abgelegt
- `skills/dtb-workflow-checkpoint/SKILL.md` - Einfügestelle, Teil-Guard-Muster im Worktree
- `skills/dtb-pane-start/SKILL.md` - Vorbild für Verweis + Struktur-Check statt Kopie
- `skills/CLAUDE.md` - Worktree-Guard, Parallele Sessions, Rueckfragen-Defaults

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `/dtb:project-dashboard` erzeugt `dtb-project/project-dashboard.html` und öffnet sie im Browser; die Seite öffnet dunkel, der Umschalter wechselt auf Hell und die Wahl bleibt nach Neuladen erhalten
- [ ] Die Seite zeigt alle sechs Bereiche (Kennzahlen-Leiste, Wo wir stehen, Backlog nach Status, Zuletzt gemacht, INBOX + Becken, Lektionen) mit Werten, die mit `workflow-status`/`workflow-next` für denselben Stand übereinstimmen
- [ ] Ein Feature mit 100 % Progress-Checkboxen erscheint unter „Fertig zum Testen", auch wenn die BACKLOG-Anzeigespalte etwas anderes sagt — mit Warnchip
- [ ] Die Seite lädt keine Ressource von einer externen Adresse — kein Verweis auf eine http(s)-Adresse als Quelle, kein Import von aussen (per Suche in der Datei prüfbar)
- [ ] `/dtb:workflow-checkpoint` im Haupt-Checkout aktualisiert die Seite ohne Browser-Popup und meldet den Pfad; mit `dashboard.bei_checkpoint: false` entfällt der Schritt
- [ ] Im Worktree erzeugt `/dtb:project-dashboard` die Seite mit dem Worktree-Banner
- [ ] In einem Bestandsprojekt ohne Befund-Becken und ohne `lessons.md` entsteht die Seite vollständig, die fehlenden Blöcke tragen „nicht vorhanden"
- [ ] Der Checkpoint enthält kein kopiertes Seitengerüst, nur den Verweis samt Struktur-Check
- [ ] Kit-Doku nachgezogen: Skill-Katalog und Output Locations in `CLAUDE.md`, Skill-Liste und Config-Seed in `project-init`

---

## Offene Punkte

— keine —

---

**Erstellt mit:** `/dtb:feature-plan`
