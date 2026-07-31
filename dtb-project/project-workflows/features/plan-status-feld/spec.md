# Feature: plan-status-feld

**Erstellt:** 2026-07-30
**Ziel:** Das plan.md-Kopf-Statusfeld bekommt genau einen definierten Pfleger (plan-review), die lesenden Skills werden gegen Feld-Drift gehaertet, und Feld-Semantik samt Randfaellen wird in DERIVED_STATE_RULES.md kanonisiert.
**Prioritaet:** Hoch
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Das Kopf-Statusfeld (`Entwurf`/`Reviewed`) in `plan.md` wird von `workflow-next` und
`workflow-status` gelesen, aber von keinem Skill je geschrieben — es veraltet stillschweigend
und produziert belegte Fehlvorschlaege (Review-Empfehlung trotz 100 % Progress). Das Feature
schliesst die Luecke dreifach: `plan-review` wird der eine Pfleger des Felds (schreibt bei jedem
Verdikt den letzten Review-Stand), die Leser werden gehaertet (Checkbox-Guard, ⚠-Konfliktmeldung,
Toleranz-Matrix fuer Alt-/Fehlwerte), und Feld, Definitionsfenster und Ausnahmen werden in
`DERIVED_STATE_RULES.md` kanonisiert — das Feld steht heute komplett ausserhalb des
Ableitungs-Kanons.

---

## Scope / Abgrenzung

### Enthalten
- **Pfleger:** `dtb:plan-review` schreibt das Kopf-Statusfeld am Review-Ende selbst — still,
  ohne Bestaetigungsfrage, im Abschluss-Report als eine Zeile ausgewiesen. Geschrieben wird bei
  JEDEM Verdikt (Wertematrix):
  | Ausgang | Feld danach |
  |---------|-------------|
  | SOUND | `Reviewed (plan-review {Datum}: SOUND)` |
  | REVISE, Findings im selben Zug behoben (Schritt 5 angenommen) | `Reviewed (plan-review {Datum}: REVISE → {N} WARNs behoben)` |
  | REVISE, Findings offen (Schritt 5 abgelehnt/vertagt) | `Entwurf (plan-review {Datum}: REVISE — Findings offen)` |
  | RETHINK | `Entwurf (plan-review {Datum}: RETHINK)` |
  Fehlt die Feld-Zeile, fuegt plan-review sie an der Kopfposition ein
- **Guard:** `dtb:workflow-next` Z. 53 (`Entwurf` → „Review ausstehend") greift nur noch bei
  0/Y Progress-Checkboxen — analog Z. 54, bisher die einzige Pipeline-Zeile ohne Guard
- **Haertung `dtb:workflow-status`:** Gate „Plan-Review" (Z. 85) haengt nicht mehr am nie
  gesetzten Wert `In Umsetzung`; Ableitungszeilen Z. 49–50 konsistent nachgezogen
- **Konfliktmeldung:** Widerspricht das Feld dem `## Progress`-Stand, melden workflow-next und
  workflow-status eine ⚠-Zeile nach dem Derived-State-Muster (Artefakt gewinnt, melden statt
  korrigieren)
- **Toleranz-Matrix der Leser:** Feld fehlt → wie `Entwurf`, still; Altwerte
  `In Umsetzung`/`Abgeschlossen` → wie `Reviewed`, still; unbekannter Wert → wie fehlend +
  1 Hinweiszeile. Selbstheilung ueber den naechsten plan-review-Lauf, keine Bestandsmigration
- **Wertemenge gestrafft:** impl-plan-Template (Z. 102) fuehrt nur noch `Entwurf` / `Reviewed` —
  Umsetzungsstand ist Sache von `## Progress`
- **Kanonisierung in `DERIVED_STATE_RULES.md`:** Feld-Semantik (reiner Review-Nachweis),
  Definitionsfenster (die `**Status:**`-Zeile innerhalb der ersten 10 Zeilen — ausserhalb
  existiert kein Kopf-Statusfeld), Pfleger-Regel, manueller Flip nur als dokumentierte Ausnahme
  mit Vermerk-Pflicht `({manuell {Datum}: {Grund}})`
- **Doku nachgezogen:** `skills/CLAUDE.md` Z. 54 (Feld-Konvention) an Wertemenge und
  Pfleger-Regel angepasst
- **INBOX #22** um den Seed-Skew-Beleg aus dieser Discovery ergaenzt (1 Satz)

### Nicht enthalten
- Bestandsmigration archivierter Plaene (`archive/*/plan.md`) — Selbstheilung genuegt
- Automatische Rueck-Stufung `Reviewed` → `Entwurf` bei Plan-Aenderungen nach dem Review
- ~~Aenderungen an `dtb:backlog-status` (liest das Feld nicht unterscheidend)~~ —
  **nachtraeglich in Scope genommen** (impl-review-Triage 2026-07-30, `8f3c3da`): Der Skill las
  das Feld doch, was §7.4 (Status-Neutralitaet) widerspricht; er ist jetzt davon entkoppelt.
  Aus demselben Grund ebenfalls nachtraeglich in Scope: `dtb:project-health` — dessen
  Anzeige-Drift-Check pruefte den `plan.md`-Kopf gegen den abgeleiteten Status und haette nach
  §7.4 Dauerwarnungen erzeugt; er ist jetzt auf `spec.md`/`task.md` eingeschraenkt
- Aufnahme des Felds in die Sync-Ziele von `dtb:workflow-checkpoint` — **expliziter
  Nicht-Integrationspunkt:** ein Feld, ein Pfleger; ein zweiter Schreiber mit anderer Logik
  waere die naechste Drift-Quelle
- Loesung des generellen Seed-Skew-Problems (Klasse-B-Seeds in Bestandsprojekten) — bewusst
  hingenommen, gehoert zu INBOX #22

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Spaeterer zweiter Schreiber (z. B. checkpoint-Sync „gut gemeint" nachgeruestet) | Mittel | Mittel | Nicht-Integrationspunkt explizit in Spec + Plan-Leitplanke; Pfleger-Regel kanonisiert |
| Seed-Skew: Bestandsprojekte mit altem Seed, aber neuen globalen Skills | Hoch | Niedrig | Leser-Toleranz-Matrix ist rueckwaertskompatibel; Beleg fliesst in #22 |
| Feld wird wieder als Umsetzungs-Status gelesen | Niedrig | Mittel | Wertemenge auf 2 Werte gestrafft; Kanon stellt klar: reiner Review-Nachweis |
| Manuelle Flips unterlaufen die Review-Semantik | Niedrig | Niedrig | Ausnahme-Regel mit Vermerk-Pflicht — manueller Flip gibt sich nicht als Review-Ergebnis aus |

---

## Dependencies

### Erforderlich vor Start
- [ ] — keine —

### Referenz-Dokumente
- `features/plan-status-feld/discovery.md` — vollstaendige Discovery (Scan-Belege, Randfall-Matrix, Entscheidungen 3a–3e)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` — Ziel der Kanonisierung; §-Verortung offen
- `skills/dtb-plan-review/SKILL.md` — Traeger des Pflegers (Schritt 4 Verdikt, Schritt 5 Anpassungen)
- `skills/dtb-workflow-next/SKILL.md`, `skills/dtb-workflow-status/SKILL.md` — zu haertende Leser
- `skills/dtb-impl-plan/SKILL.md` — Template-Wertemenge (Z. 102)
- `skills/CLAUDE.md` — Feld-Konvention (Z. 54)
- INBOX #30 (Ursprungs-Idee), INBOX #22 (Seed-Skew-Kontext)

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `plan-review` schreibt das Feld bei jedem der vier Verdikt-Ausgaenge gemaess Wertematrix und weist die Aenderung im Abschluss-Report aus; fehlende Feld-Zeile wird an der Kopfposition eingefuegt
- [ ] `workflow-next` schlaegt bei teilweise abgehaktem `## Progress` kein plan-review mehr vor (Guard Z. 53) und meldet Feld-Konflikte als ⚠-Zeile
- [ ] `workflow-status` liest den Wert `In Umsetzung` nicht mehr und meldet Feld-Konflikte analog
- [ ] Beide Leser folgen der Toleranz-Matrix (fehlend / Altwerte / unbekannt) — verifizierbar an konstruierten Testkoepfen
- [ ] impl-plan-Template fuehrt nur noch `Entwurf` / `Reviewed`
- [ ] `DERIVED_STATE_RULES.md` kanonisiert Feld-Semantik, Definitionsfenster, Pfleger und manuelle Ausnahme; `skills/CLAUDE.md` Z. 54 ist konsistent dazu
- [ ] INBOX #22 traegt den Seed-Skew-Beleg
- [ ] Distribution: geaenderte Klasse-A-Skills via kit-sync verteilt, Verifikation synchron

---

## Offene Punkte

- §-Verortung der Kanonisierung in `DERIVED_STATE_RULES.md`: eigener neuer § (analog §6) oder Unterabschnitt eines bestehenden §? — beim impl-plan anhand der Struktur der Regel-Datei entscheiden

---

**Erstellt mit:** `/dtb:feature-plan`
