# Feature: Codebase-Research-Step

**Erstellt:** 2026-07-13
**Ziel:** `dtb:impl-plan` stellt vor der Schrittplanung eine verifizierte Ist-Analyse der betroffenen Module sicher — Pläne fußen auf realem Code statt auf Annahmen.
**Prioritaet:** Hoch
**Status:** Abgeschlossen <!-- explizit abgenommen 2026-07-14 (pkp-praxiserprobt); archiviert via dtb:archive -->

---

## Executive Summary

Wer `feature-discover` überspringt und direkt zu `impl-plan` geht, plant heute ohne erzwungenen
Codebase-Scan: Der einzige angeleitete Ist-Analyse-Schritt sitzt in `feature-discover` Schritt 2,
und `plan-review` (Grounding 2d) verifiziert nur nachgelagert einen fertigen Plan. `impl-plan`
erhält einen angeleiteten Codebase-Research-Schritt (Spec→Ist-Abgleich), der genau dann läuft,
wenn keine verwertbare Modul-Liste aus einer Discovery existiert — die Lücke zwischen Erst-Quelle
(feature-discover) und Nachprüfung (plan-review) wird geschlossen, ohne Doppelarbeit einzuführen.

---

## Scope / Abgrenzung

### Enthalten
- Angeleiteter Codebase-Research-Schritt in `dtb:impl-plan`: Ist-Code der betroffenen Module
  analysieren (read-only) und mit der Feature-Spec abgleichen, bevor Plan-Schritte formuliert werden
- **Auslöse-Kriterium (ein mechanisches Kriterium):** Der Schritt läuft, wenn KEINE verwertbare
  Modul-Liste existiert. Verwertbar = `discovery.md` vorhanden UND `## Betroffene Module` vorhanden
  UND ≥1 Pfad-Zeile UND Stichproben-Verifikation bestanden (gelistete Pfade existieren; ≥1 fehlt →
  „veraltet" → Schritt läuft). „Fehlt", „leer", „kaputt", „veraltet" kollabieren in diese eine Regel
- **Zwischenausgabe + Bestätigung:** Scan-Ergebnis als kompakte Tabelle im Muster von
  `feature-discover` Schritt 2 (`| # | Pfad | Relevanz |` + „Stimmt das so?"); die Relevanz-Spalte
  trägt den Ist-Befund (was wurde im Code vorgefunden), User bestätigt/korrigiert vor der Planung
- **0-Treffer-Dialog:** nie stumm mit leerer Liste weiterplanen — User nennt Pfade (mit
  Kurz-Verifikation) oder erklärt das Feature explizit zum Neubau („keine betroffenen Bestandsmodule")
- **Treffer-Kappung:** bei ~15 Zeilen, priorisiert; Kappung immer explizit ausgewiesen
  („+ N weitere"), Nachfordern im Bestätigungsdialog möglich
- **Ergebnis-Verankerung:** bestätigte Liste als kompakter Abschnitt `## Ist-Analyse` in `plan.md`
  (Tabelle, keine Prosa) — prüfbares Material für das plan-review-Grounding
- Frontmatter-Erweiterung: `consumes:` von `impl-plan` um `features/*/discovery.md`
- Verteilung der Änderung über `dtb:kit-sync` (Klasse-A-Artefakt)

### Nicht enthalten
- Keine Änderung an `dtb:feature-plan` (bewusste Discovery-Entscheidung: nur impl-plan)
- Kein zweites Grounding — die nachgelagerte Verifikation bleibt bei `plan-review` Schritt 2d
- Kein Ersatz für `feature-discover` Schritt 2 (bleibt die Erst-Quelle der Modul-Liste)
- Keine Änderungen am analysierten Code (reine Lese-Analyse)
- Keine Status-Semantik: `## Ist-Analyse` ist Zusatz-Info, KEINE Quelle für Derived State
  (`DERIVED_STATE_RULES.md` bleibt unberührt)
- Kein Zeitvergleich (mtime/git log) als Veraltet-Kriterium — bewusst verworfen
  (Non-Git-unzuverlässig, False-Positive-Lawine)

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Doppelarbeit mit feature-discover (Scan läuft trotz guter Discovery) | Mittel | Mittel | Mechanisches Auslöse-Kriterium: verwertbare Modul-Liste → Schritt wird übersprungen |
| Format-Kopplung: Auslöse-Kriterium parst `## Betroffene Module` aus discovery.md — spätere Formatänderung an feature-discover bricht das Kriterium still | Niedrig | Hoch | Kopplung im impl-plan-Skilltext explizit benennen (Wartungs-Hinweis in beide Richtungen) |
| Generische Spec-Schlüsselwörter liefern Treffer-Lawine oder Streu-Treffer | Mittel | Niedrig | Kappung ~15 + explizite „+N weitere"-Zeile + Bestätigungsdialog + Hinweis: schärfer nachscannen statt abkippen |
| Skill-Aufblähung von impl-plan (Prosa statt Determinismus) | Niedrig | Mittel | Budget ca. +30–40 Zeilen (aktuell 219, Grenze 500); kompakt-deterministische Formulierung nach Vorbild Eligibility-Gate |
| Falsches Vertrauen: bestätigte Ist-Analyse veraltet während langer Implementierung | Niedrig | Niedrig | Außerhalb des Scopes — plan-review-Grounding prüft beim Review erneut; keine eigene Mechanik |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — alle betroffenen Skills sind synchron verteilt (Lock-Stand geprüft 2026-07-13)

### Referenz-Dokumente
- `features/codebase-research-step/discovery.md` - Discovery mit allen Entscheidungen (3a–3e)
- `skills/dtb-impl-plan/SKILL.md` - Zielartefakt (Eingangs-Reihenfolge: Lektionen-Prior → Eligibility-Gate → Research-Schritt → Spec-Analyse)
- `skills/dtb-feature-discover/SKILL.md` - Schritt 2 „Codebase-Scan": UX-Muster-Quelle + Format-Kopplung (`## Betroffene Module`)
- `skills/dtb-plan-review/SKILL.md` - Schritt 2d „Grounding": Abgrenzung (nachgelagerte Verifikation, unverändert)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` - bleibt unberührt (Ist-Analyse ≠ Status-Quelle)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [x] SC1: `impl-plan` ohne `discovery.md` → Research-Schritt läuft; Tabelle (`| # | Pfad | Relevanz |`) wird gezeigt und die Bestätigungsfrage kommt VOR der Schrittplanung — blinder Lauf Fixture A (3 Treffer, Tabelle + „Stimmt das so?", Wartestellung vor Planung)
- [x] SC2: `impl-plan` mit verwertbarer `discovery.md` (Modul-Liste vorhanden, Pfade verifizierbar) → Schritt wird übersprungen, kein Doppel-Scan — blinder Lauf Fixture B (2 Pfade verifiziert, Skip-Zeile `📂 … (2 Module, Pfade verifiziert)`, kein Scan; Negativ-Kontrolle: kein Fehlalarm)
- [x] SC3: `discovery.md` vorhanden, aber ≥1 gelisteter Pfad existiert nicht mehr → Schritt läuft (Veraltet-Regel greift) — blinder Lauf Fixture CE (toter Pfad `src/old/legacy_handler.py` erkannt → Scan statt Übernahme)
- [x] SC4: Scan mit 0 Treffern → aktiver Dialog; beide Ausgänge funktionieren (User-Pfade werden verifiziert übernommen / Neubau wird explizit in `## Ist-Analyse` dokumentiert); kein stummes Weiterplanen — blinder Lauf Fixture D (0 Treffer → Dialog mit beiden Optionen, „lege keine Ist-Analyse auf gut Glück an")
- [x] SC5: Erzeugtes `plan.md` enthält kompakten `## Ist-Analyse`-Abschnitt; plan-review-Grounding kann die dortigen Pfade als prüfbare Referenzen verifizieren — blinder plan-review-2d-Lauf: `🔎 Grounding: 4 Referenzen geprueft, alle gefunden` (3 Ist-Analyse-Pfade + spec.md)
- [x] SC6: >15 Treffer → genau ~15 gezeigt + explizite „+ N weitere"-Zeile (keine stille Kappung) — blinder Lauf Fixture CE (20 Treffer → 15 gelistet + „+ 5 weitere Treffer nicht gelistet"; Streu-Treffer per Priorisierung ausgeschlossen)
- [x] SC7: `consumes:` von impl-plan enthält `features/*/discovery.md`; Reader ohne Fehler — statisch (2.1): pipeline-graph liest Frontmatter, project-health Check 8 kein Verwaisen (feature-discover `produces` discovery.md); workflow-status liest fremde Frontmatter nicht → nicht im Umfang (L2)
- [x] SC8: impl-plan bleibt schlank (≤ 260 Zeilen) und Repo == globale Kopie nach `kit-sync` (Lock aktualisiert) — 258 Z.; Repo==Lock==Global `28dce15`, Lock `sourceCommit 4e46d32`; Praxistest pkp bestanden (Fund gehärtet + gegenverifiziert)

---

## Offene Punkte

- — keine —

---

**Erstellt mit:** `/dtb:feature-plan`
