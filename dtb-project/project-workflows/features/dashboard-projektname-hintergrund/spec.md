# Feature: Dashboard mit Projektname und Raster-Hintergrund

**Erstellt:** 2026-10-27
**Ziel:** Das Projekt-Dashboard zeigt auf den ersten Blick, zu welchem Projekt es gehoert, und traegt den Seitenhintergrund der pi.dev-Dokumentation. <!-- Lint-Override: pi.dev ist die vom Menschen genannte visuelle Referenz (INBOX #158), keine Loesungswahl -->
**Prioritaet:** Niedrig
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Wer mehrere Projekte betreut, hat mehrere Dashboard-Seiten offen — heute tragen alle denselben
Titel „Projekt-Dashboard". Der Skill `dtb:project-dashboard` setzt kuenftig den Projektnamen als
Seitentitel (Kopf und Browser-Tab) und uebernimmt den Hintergrund der pi.dev-Dokumentation
(Grundfarbe, feines Raster, Vignette) in beiden Themes. Der uebrige Seitenaufbau bleibt unveraendert.

---

## Scope / Abgrenzung

### Enthalten
- Projektname als grosse Ueberschrift der Seite und im Browser-Tab („{Projektname} · Projekt-Dashboard")
- Herkunft des Namens: Projekt-Konfiguration; fehlt der Wert, ist er leer oder noch ein Platzhalter → Name des Projektordners (Haupt-Checkout, auch beim Lauf in einem Worktree)
- Seitenhintergrund wie pi.dev/docs: Grundfarbe, Millimeterraster, Vignette — Hell und Dunkel <!-- Lint-Override: visuelle Referenz aus INBOX #158 -->
- Anpassung des Erzeugungs-Checks an den zusaetzlichen Platzhalter

### Nicht enthalten
- Karten, Schrift, Akzentfarbe und uebrige Theme-Farben
- Nachladen von Inhalten fremder Seiten — die Seite bleibt eigenstaendig und offline lesbar
- Aenderungen an anderen Skills oder an der Kit-Dokumentation

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Dunkle Karten wirken auf dem blaugrauen Grund dunkler als die Seite und stoeren die Lesbarkeit | Mittel | Niedrig | Sichtabnahme in beiden Themes; bei Nein Nacharbeit vor der Abnahme oder Folge-Idee |
| Im Worktree erscheint der Worktree-Ordner statt des Projektnamens | Mittel | Mittel | Fallback auf den Haupt-Checkout; Probelauf im Worktree belegt es |
| Sonderzeichen im Projektnamen brechen die Seite | Niedrig | Mittel | bestehende Escaping-Regel gilt auch fuer den Namen |
| Raster ueberdeckt Inhalt oder faengt Klicks ab | Niedrig | Mittel | Hintergrund liegt hinter dem Inhalt und ist nicht anklickbar; Probelauf prueft Theme-Schalter und Links |

---

## Dependencies

### Erforderlich vor Start
- [x] Abgenommener Change `projekt-dashboard` (INBOX #135, archiviert 2026-10-27)

### Referenz-Dokumente
- `skills/dtb-project-dashboard/SKILL.md` - Gegenstand des Change (Seitengeruest, Slot-Regeln)
- `features/dashboard-projektname-hintergrund/discovery.md` - Werte des Referenz-Hintergrunds und Randfaelle

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Ein Probelauf im Kit-Repo zeigt „claude-code-workflow-kit" als Ueberschrift und im Tab-Titel (Platzhalter-Fallback, Lauf im Worktree)
- [ ] Ist ein Projektname konfiguriert, erscheint genau dieser — Sonderzeichen korrekt dargestellt
- [ ] Der Hintergrund zeigt in Hell und Dunkel das Raster mit Vignette und folgt dem Theme-Schalter ohne Neuladen
- [ ] Karten, Links und Theme-Schalter bleiben lesbar und bedienbar
- [ ] Die erzeugte Seite laedt keine externen Ressourcen
- [ ] Der Mensch bestaetigt im Sichtvergleich neben pi.dev/docs, dass der Hintergrund „gleich" wirkt <!-- Lint-Override: visuelle Referenz aus INBOX #158 -->

---

## Offene Punkte

- Wirken die unveraendert dunklen Karten auf dem neuen Grund gut? Entscheidung in der Sichtabnahme (Plan Schritt 2.2)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-27)
