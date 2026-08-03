# Discovery: Abnahme-Zustand
<!-- resume: done -->

**Erstellt:** 2026-08-03
**Idee-Referenz:** Inbox #38 — "§1.2 der `DERIVED_STATE_RULES.md` wirft `Abgenommen` und `Abgeschlossen` falsch zusammen — der Zustand `Abgenommen` hat einen Schreiber, aber keine durchgaengige Leser-Behandlung."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §1.2 Z. 50 wirft beide Zustaende zusammen ("nur via `/dtb:archive`") — Aufspaltung + Lese-Regel + Kopplungs-Hinweis; §3-Matrix Z. 147/148 ist bereits korrekt und dient als Referenz |
| `skills/dtb-workflow-next/SKILL.md` | Z. 68 fuehrt jedes Y/Y-Feature als "Fertig zum Testen" und schlaegt die Abnahme vor; kennt "Abgenommen" nicht (0 Treffer) |
| `skills/dtb-backlog-status/SKILL.md` | Schritt 2 nennt nur `Pausiert` als ueberschreibenden Zustand; muesste `Abgenommen` derzeit als §1.3-Konflikt melden |
| `skills/dtb-workflow-resume/SKILL.md` | kennt weder "Abgenommen" (0 Treffer) noch eine Y/Y-Behandlung — abgenommene Changes verschwinden in "Kein aktives Feature" |
| `skills/dtb-archive/SKILL.md` | Z. 48 fuehrt `**Status:** Abgenommen` als Vorbedingung, Z. 159 vergisst ihn in der Richtlinie — interner Widerspruch |
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schreiber-Seite (Schritt 2.3 setzt den Zustand mit Beleg-Gate): Verweis auf den neuen §1.2-Wortlaut pruefen und ggf. praezisieren |

---

## Anforderungen

### Scope

**Enthalten:**
- Trennung der beiden expliziten Zustaende im Kanon: `Abgenommen` (Schreiber `dtb:workflow-checkpoint` Schritt 2.3, Beleg-Gate; Change bleibt unter `features/`) vs. `Abgeschlossen` (nur via `dtb:archive`, die Archivierung IST der Akt)
- Lese-Regel fuer `Abgenommen`: ueberschreibt die Ableitung, ist kein Konflikt — plus Definition des einen echten Konfliktfalls
- Spiegelung in den drei Lesern, die den Zustand nicht kennen
- Korrektur des internen Widerspruchs in der Archiv-Richtlinie
- Kopplungs-Hinweis am Kanon, der die Spiegel benennt (Wartbarkeit)

**Nicht enthalten:**
- Bestandsmigration: archivierte Ordner unter `archive/` bleiben unberuehrt; Specs ohne Feld verhalten sich weiter wie abgeleitet (Selbstheilung beim naechsten Checkpoint)
- Automatisches Zurueckstufen von `Abgenommen` bei nachtraeglichen Plan-Aenderungen
- Erweiterung der Y/Y-Sichtbarkeit ueber den Zustand `Abgenommen` hinaus (z. B. eine allgemeine "fertige Features"-Ansicht im Resume)
- Aenderungen an `dtb:workflow-status` — dieser Leser behandelt beide Zustaende bereits korrekt

### Gewuenschtes Verhalten
- Der Kanon nennt beide Zustaende getrennt, jeweils mit dem zustaendigen Schreiber
- Ein Change mit gesetztem `Abgenommen` und vollstaendigem Fortschritt erscheint in allen Lesern als abgenommen — kein erneuter Abnahme-Vorschlag, keine Konfliktmeldung
- Ein Change mit gesetztem `Abgenommen`, dessen Fortschritt unvollstaendig ist, gilt als echter Konflikt: das Artefakt gewinnt, der Widerspruch wird mit einer Zeile gemeldet
- Die Archiv-Vorbedingungen und die Archiv-Richtlinie nennen denselben Zustand

### Randfaelle
- Feld fehlt oder liegt nicht im Kopf: still wie abgeleitet (keine Meldung) — analog zur bestehenden Toleranz-Regel fuer das Plan-Kopffeld
- `Abgenommen` bei unvollstaendigem Fortschritt: einziger echter Konfliktfall
- Bereits archivierte Changes tragen `Abgeschlossen` — unberuehrt
- Unbekannter Wert im Statusfeld: wie bisher behandelt, dieses Vorhaben aendert daran nichts
- Ein Change kann `Abgenommen` tragen und dennoch offene Punkte oder Vorbehalte im Text haben — der Zustand ist eine Freigabe-Aussage, keine Vollstaendigkeitsaussage

### Einschraenkungen
- Der Kanon ist ein Seed und erreicht Bestandsprojekte nicht automatisch — die Leser muessen autark bleiben, die Spiegelung ist Absicht und kein vermeidbares Duplikat
- Anzeige-Felder bleiben abgeleitete Anzeigen; ein manuell gesetzter Zustand ist die Ausnahme mit Vermerkpflicht
- Groessen-Limits fuer die Artefakte gelten unveraendert

### Integrationspunkte
- Schreibende Seite: der Checkpoint setzt den Zustand nach dem Beleg-Gate
- Lesende Seite: die vier Lese-Skills werten ihn aus
- Archivierung: `Abgenommen` ist der Eingang, `Abgeschlossen` der Ausgang

---

## Abhaengigkeiten

- Keine offenen Vorbedingungen. Fuenf Changes tragen den Zustand seit 2026-08-03 bereits — sie sind das Testmaterial, nicht ein Hindernis.
- Strukturell verwandt mit dem abgeschlossenen Vorhaben zum Plan-Kopf-Statusfeld (gleiche Fehlerklasse: gelesener Zustand ohne durchgaengige Behandlung); dessen Loesungsmuster — Pfleger benennen, Leser haerten, Kanon ergaenzen — ist hier die Vorlage.

---

## Offene Punkte

- Soll der Kanon eine Vermerkform fuer `Abgenommen` vorschreiben (Datum und Beleg in der Statuszeile), oder genuegt der freie Text im Artefakt? Die fuenf Bestandsfaelle verwenden bereits eine Datums-Angabe, ohne dass eine Form festgelegt ist.
- Wie verhaelt sich `Abgenommen` in der Roadmap-Ableitung? Dort wird nach Ordner-Zustand unterschieden (aktiv vs. archiviert) — ein abgenommener, noch nicht archivierter Change ist in dieser Zweiteilung nicht eigens vorgesehen.

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-03)
