# Feature: Seed-Skew aktiv melden

**Erstellt:** 2026-11-09
**Ziel:** Ein Projekt, dessen Statusregel-Datei hinter der Kit-Fassung zurückliegt, fällt beim normalen Kit-Check auf statt nur zufällig.
**Prioritaet:** Hoch
**Status:** Spezifiziert <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Statusregel-Datei `DERIVED_STATE_RULES.md` wird pro Projekt einmal verteilt und danach von
keinem Check mehr beobachtet. Die global verteilten Skills setzen aber laufend neuere Abschnitte
dieser Datei voraus — im PKP-Projekt lag sie knapp vier Monate zurück, während `dtb:kit-sync check`
„alles synchron" meldete. Künftig vergleicht `dtb:kit-sync check` die Regel-Datei des Projekts im
Arbeitsverzeichnis mit der Kit-Fassung und meldet eine Abweichung als eigenen, informativen
Hinweis — ohne sie selbst zu ändern.

---

## Scope / Abgrenzung

### Enthalten
- Inhaltlicher Vergleich der Regel-Datei des Projekts im Arbeitsverzeichnis mit der Kit-Fassung
  im Modus `check` von `dtb:kit-sync`
- Eigener Hinweis-Block im Check-Bericht mit drei Ausgängen: aktuell / weicht ab / nicht geprüft
- Eine Abweichung verhindert die Schlussaussage „Alles synchron — keine Aktion noetig"
- Abhilfe-Hinweis: Übernahme von Hand mit fertigem Vergleichs- und Kopierbefehl (`dtb:project-init` hat keinen Weg „nur Seeds erneuern" — entschieden 2026-11-09, Plan Schritt 1.1)
- Nachziehen der Kit-Doku, die Seeds heute als „nie geprüft" beschreibt

### Nicht enthalten
- Automatisches Aktualisieren des Seeds — er bleibt projektgehörig
- Vergleich der Projekt-Einstellungsdatei (`settings.json`): sie ist projekteigen, eine Abweichung
  ist dort der Normalfall
- Änderungen an den Modi `sync` und `install` und an der Lock-Datei
- Ein zweiter Melde-Ort in `dtb:project-health`

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Projekt hat die Regel-Datei bewusst angepasst und erhält einen Dauerhinweis | Niedrig | Niedrig | `dtb:project-init` überschreibt die Datei ohnehin — Anpassung ist nicht vorgesehen; die Meldung formuliert neutral „weicht ab" und nennt einen Vergleichsbefehl |
| Werkzeugfehler liest sich als Abweichung (leere Vergleichsseite) | Mittel | Mittel | Beide Seiten vor dem Vergleich auf Inhalt prüfen; sonst „Werkzeug-Fehlschlag, kein Datenbefund" |
| Hinweis geht unter, weil die Schlusszeile weiter „Alles synchron" sagt | Mittel | Hoch | Schlusszeile ist an den Seed-Ausgang gekoppelt |
| Kit-Doku widerspricht danach dem Verhalten („never drift-checked") | Hoch | Niedrig | Spiegelstellen im selben Zug nachziehen und per Suche verifizieren |

---

## Dependencies

### Erforderlich vor Start
- [x] Kit-Quelle wird im Modus `check` bereits beschafft (keine neue Abhängigkeit)

### Referenz-Dokumente
- `skills/dtb-kit-sync/SKILL.md` - Träger der Änderung
- `skills/dtb-project-init/SKILL.md` - Seed-Politik (Regel-Datei überschreiben, Einstellungsdatei nie)
- `dtb-project/project-workflows/INBOX.md` #22 - Herleitung, sieben dokumentierte Skew-Fälle, PKP-Feldbeleg 2026-11-03

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `dtb:kit-sync check` in einem Projekt mit älterer Regel-Datei meldet die Abweichung im eigenen Block, und die Schlusszeile sagt nicht „Alles synchron"
- [ ] In einem Projekt mit aktueller Regel-Datei erscheint genau eine Zeile „aktuell", die übrige Ausgabe bleibt wie bisher
- [ ] Ohne DTB-Projekt im Arbeitsverzeichnis erscheint genau eine Zeile „nicht geprüft", kein Fehler
- [ ] Der Check schreibt nichts ins Projekt; Drift-Zahlen und Lock bleiben unberührt
- [ ] Die Kit-Doku beschreibt Seeds nicht mehr als „nie geprüft"

---

## Offene Punkte

- Kann `dtb:project-init` in einem eingerichteten Projekt nur die Seeds erneuern, ohne das Interview zu wiederholen? → Beantwortet 2026-11-09 (Plan Schritt 1.1): nein — der Abhilfe-Hinweis nennt deshalb die Übernahme von Hand mit fertigem Vergleichs- und Kopierbefehl.

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)
