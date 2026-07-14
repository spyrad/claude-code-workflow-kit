# Feature: Opportunity-Map (build/buy/complement/wait-Sichtung)

**Erstellt:** 2026-07-14
**Ziel:** Ein eigenständiger Vorfeld-Skill `dtb-opportunity-map`, der wiederkehrende Reibung in eine build/buy/complement/wait-Entscheidung überführt, bevor teure PRD-/Bau-Arbeit beginnt.
**Prioritaet:** Mittel
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kit hat heute keinen Schritt, der *vor* dem Bauen fragt, ob überhaupt gebaut werden soll.
`dtb-opportunity-map` schließt diese Lücke nach dem Vorbild von `10x-opportunity-map`: ein
manuell gestarteter Vorfeld-Skill, der Signale (wiederkehrende Reibung) normalisiert, jedes Signal
grob in **build / buy / complement / wait** einordnet und genau **einen** empfohlenen Kandidaten
für eine dünne, read-only Erstversion vorschlägt. Ergebnis ist ein Entscheidungs-Artefakt
(`project-strategy/OPPORTUNITY-MAP.md`), das die anschließende `greenfield-prd`-Interviewphase als
Quellmaterial aufgreift. Ein aktiver Eingangs-Nudge in `greenfield-prd` sorgt dafür, dass die
build/buy-Frage nicht vergessen wird — ohne die Greenfield-Kette umzubauen.

---

## Scope / Abgrenzung

### Enthalten

- **Eigenständiger Skill `dtb-opportunity-map`** als **grobe Vorfeld-Trade-off-Sichtung**
  (Kern-Schmerz + grobe Must-Haves + Marktkenntnis), rein manuell gestartet
- **Signal-Erhebung:** liest `project-strategy/*.md` + INBOX-Ideen und bietet sie als Signale an;
  zusätzlich Freitext; „baut mir ein Dashboard/Agent" wird als *vorgeschlagene Lösung* behandelt,
  nicht als Schmerzsignal (Rückfrage nach dem echten wiederkehrenden Schmerz)
- **4-Wege-Klassifikation je Signal:** build / buy / complement / wait — Signal-für-Signal als
  Block dargestellt (keine breite Tabelle mitten im Gespräch); Daten-Risiko früh per Auswahlfrage
  (mock/lokal/read-only vs. echte Firmen-/Kundendaten)
- **Genau 1 empfohlener Kandidat** mit dünner, read-only Erstversion (Reads / Returns /
  Does-not-do / Daten-Risiko / Richtung); qualifiziert sich keiner → „no build / bestehendes Tool
  nutzen" ist ein gültiges Ergebnis
- **Marktkenntnis:** Live-Websuche **primär** (maximale Aktualität) mit **Fallback auf
  Modellwissen**, wenn die Websuche-Fähigkeit nicht verfügbar ist; „nie erfinden" — recherchierte
  Funde als solche kennzeichnen, Unsicherheit benennen
- **Artefakt** `project-strategy/OPPORTUNITY-MAP.md`: Kontext, kompakte Vergleichstabelle
  (1 Zeile/Signal), empfohlener Kandidat, Begründung, Richtung; deutsch
- **Selbst-Review vor dem Schreiben**; leere Basis/Abbruch → kein Write; vorhandenes Artefakt →
  Kollisions-Dialog (Archivieren+ersetzen / Überschreiben / Abbrechen)
- **Hand-off (kein Auto-Chaining):** build → `/dtb:greenfield-prd`; buy/complement →
  Handlungshinweis (welche Produktkategorie gegen die Must-Haves prüfen); wait → Map speichern
- **Aktiver Eingangs-Nudge in `greenfield-prd`** (Autoren-Modus, wenn keine `OPPORTUNITY-MAP.md`
  existiert): einmaliger Hinweis „build/buy geklärt? → opportunity-map erwägen — Weiter/Abbrechen";
  **additiv, isolierter letzter Umsetzungsschritt**, verschwindet sobald eine Map vorliegt

### Nicht enthalten

- Kein Implementierungsplan, kein Code, kein SDK-/CI-/Deployment-/Packaging-Output (reine
  Entscheidungshilfe — die Umsetzung übernimmt weiter shape→PRD→roadmap)
- **Kein Detail-Fit** („erfüllt Produkt X *genau* meine N Anforderungen") — das setzt ein fertiges
  PRD voraus und ist bewusst ausgeklammert
- **Kein Umbau der Greenfield-Kette** — shape bleibt in `greenfield-prd` integriert (Variante A,
  nicht die shape-Rauslösung; die bleibt eine spätere, separate Option)
- **Keine `DERIVED_STATE_RULES.md`-Erweiterung / kein abgeleiteter Status** — die Map ist ein
  Vorfeld-Strategie-Artefakt (wie `PRD-MVP.md`), kein Change mit `## Progress`
- Kein Hard-Gate in `greenfield-prd` (nur Nudge, kein Zwang)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Live-Websuche ist nicht-deterministisch → blinde Fixture-Verifikation (wie beim Greenfield-Feature) nicht 1:1 anwendbar | Hoch | Mittel | Marktrecherche-Teil gemockt/separat prüfen; Mechanik (Klassifikation, Selbst-Review, Nudge, Hand-off) bleibt fixture-testbar. Verifikationsstrategie im `impl-plan` festlegen |
| Eingangs-Nudge berührt `greenfield-prd`, das auf reale Abnahme wartet | Mittel | Mittel | Rein additiver Eingangs-Zweig als **isolierter letzter Schritt**; berührt die verifizierten SC1–3 des Greenfield-Features nicht; im Session-Log vermerken, dass greenfield-prd mitangefasst wurde |
| Websuche/Modellwissen erfindet Produkte oder nennt veraltete Marktlage | Mittel | Hoch | „Nie erfinden"-Guardrail + recherchierte Funde kennzeichnen + buy/complement-Handlungshinweis enthält explizit „aktuelle Produktlage selbst verifizieren" |
| Signal-Erhebung überschneidet sich mit der Shape-Phase → Doppelfragen | Mittel | Niedrig | Map-als-Quellmaterial-Brücke: `OPPORTUNITY-MAP.md` in `project-strategy/` wird von greenfield-prds Quellmaterial-Glob aufgegriffen; die Shape-Phase baut darauf auf statt neu zu fragen |
| WebSearch im Host nicht verfügbar (headless/cron) | Mittel | Niedrig | Sauberer Fallback auf Modellwissen, ehrliche Kennzeichnung; kein harter Fehler |
| Zeilenbudget ~350 reicht nicht (Erhebung + Klassifikation + Kandidat + Selbst-Review + Artefakt) | Mittel | Mittel | Kompression ggü. Vorbild; bei Bruch im `impl-plan` nachverhandeln (Budget vs. Kürzung vs. references-Folge-Idee) |

---

## Dependencies

### Erforderlich vor Start

- [ ] Keine harten Blocker — der Eingangs-Nudge berührt `greenfield-prd` (Fertig zum Testen),
      ist aber als isolierter additiver Schritt geplant; kein Konflikt vor Start

### Referenz-Dokumente

- `features/opportunity-map/discovery.md` — vollständige Discovery mit allen Entscheidungen (2026-07-14)
- `C:/Users/SpyraD/Desktop/Projekte/10x-devs-3.0/.claude/skills/10x-opportunity-map/SKILL.md` — Konzeptions-Vorbild (nur Referenz, keine Laufzeit-Abhängigkeit)
- `skills/dtb-greenfield-prd/SKILL.md` — Quellmaterial-Mechanismus, Kollisions-/Selbst-Review-Muster, Frontmatter-Vorbild; Ort des Eingangs-Nudge
- `skills/CLAUDE.md` — Frontmatter-/Gate-/Sprach-Konventionen

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] SC1: Der Skill erhebt Signale aus `project-strategy/*.md` + INBOX + Freitext, normalisiert wiederkehrende Reibung und behandelt eine vorgeschlagene Lösung („baut mir X") nicht als Schmerzsignal, sondern fragt nach dem echten wiederkehrenden Schmerz
- [ ] SC2: Jedes Signal wird als eigener Block in build / buy / complement / wait eingeordnet (keine breite Tabelle mitten im Gespräch); das Daten-Risiko wird früh per Auswahlfrage erfasst
- [ ] SC3: Der Skill empfiehlt genau **einen** Kandidaten mit dünner read-only Erstversion (Reads/Returns/Does-not-do/Daten-Risiko/Richtung); qualifiziert sich keiner, ist „no build / bestehendes Tool nutzen" das ausgegebene Ergebnis (kein Fehler)
- [ ] SC4: Marktkenntnis stammt primär aus Live-Websuche; ist die Websuche-Fähigkeit nicht verfügbar, degradiert der Skill sauber auf Modellwissen und kennzeichnet das; keine Produkte/Preise werden erfunden, Unsicherheit wird benannt
- [ ] SC5: Der Skill schreibt `project-strategy/OPPORTUNITY-MAP.md` (Kontext + Vergleichstabelle + empfohlener Kandidat + Begründung + Richtung), das von greenfield-prds Quellmaterial-Glob (`project-strategy/*.md`) aufgegriffen wird
- [ ] SC6: Selbst-Review vor dem Schreiben bricht bei leerer Basis/Abbruch ohne Write ab; existiert bereits eine `OPPORTUNITY-MAP.md`, erscheint der Kollisions-Dialog (Archivieren+ersetzen / Überschreiben / Abbrechen), kein stilles Überschreiben
- [ ] SC7: Der Hand-off ist korrekt und ohne Auto-Chaining: build → genau ein empfohlener `/dtb:greenfield-prd`-Befehl; buy/complement → Handlungshinweis; wait → Map gespeichert
- [ ] SC8: `greenfield-prd` zeigt im Autoren-Modus (PRD fehlt) **und** wenn keine `OPPORTUNITY-MAP.md` existiert genau einen Eingangs-Nudge (Weiter/Abbrechen); liegt eine Map vor, erscheint er nicht; die verifizierten SC1–3 des Greenfield-Features bleiben unverändert (additiv)
- [ ] SC9: `dtb-opportunity-map/SKILL.md` ≤ ~350 Zeilen, `disable-model-invocation: true`, Frontmatter (`produces`, `allowed-tools` inkl. Websuche-Fähigkeit) korrekt, deutsch, Guardrails im Text; pipeline-graph-Legende kennt `OPPORTUNITY-MAP.md`, kit-sync nimmt den Skill auf, README/CLAUDE.md-Katalog aktualisiert

---

## Offene Punkte

- **Verifikationsstrategie bei Live-Websuche:** Wie wird der nicht-deterministische Marktrecherche-Teil verifiziert (Mock? separate manuelle Probe?), während die Mechanik (Klassifikation/Selbst-Review/Nudge/Hand-off) über deterministische Fixtures geprüft wird? → im `impl-plan` festlegen
- **Kollisions-Verhalten des Artefakts:** Kollisions-Dialog wie greenfield (Vorschlag) vs. edit-in-place Living-Doc — final in `impl-plan`/Umsetzung
- **Genaue Nudge-Formulierung und Platzierung** in `greenfield-prd`: an welchem Zweig der Modus-Weiche; Auswirkung auf kit-sync-Drift und die SC9-Zeilenzahl von greenfield-prd
- **Artefakt-Dateiname:** `OPPORTUNITY-MAP.md` (analog `PRD-MVP.md`/`TECH-STACK.md`) — gegen die `project-health`-Namenskonvention gegenprüfen
- **WebSearch-Fallback-Verhalten exakt:** Ab wann wird auf Modellwissen degradiert, und wie wird der Unterschied im Artefakt sichtbar gemacht?
- **Priorität** „Mittel" bestätigen oder anpassen (manuell gepflegt)

---

**Erstellt mit:** `/dtb:feature-plan`
