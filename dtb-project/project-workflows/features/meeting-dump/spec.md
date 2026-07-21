# Feature: meeting-dump

**Erstellt:** 2026-07-21
**Ziel:** Ein aktiver Skill `/dtb:meeting-dump`, der Meeting-Notizen als Beleg persistiert und gegen die offenen `[Fach]`-Fragen aller Features abgleicht — beantwortete Fragen §6-konform abhakt/nachträgt, Teilantworten und Rest-Input sichtbar macht.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die Fachfragen-Kette hat ein Format (`[Fach]`-Konvention §6, #13) und eine Erfassungs-Stufe
(`/dtb:open-question`, #26), aber keinen **Rückfluss**: Antworten aus dem wöchentlichen
Fach-Meeting landen heute nur manuell in den Artefakten — der unbegleitetste Moment der Kette.
`meeting-dump` schließt das: Du kippst deine Meeting-Notizen als Freitext in den Chat, der Skill
persistiert sie als Beleg unter `project-meetings/`, gleicht sie gegen alle offenen
`- [ ] [Fach]`-Fragen ab und trägt — nach deiner Freigabe — Antworten Derived-State-konform in
`## Offene Punkte` zurück. Er ist der dritte Verb-Schritt der Kette:
Format (#13) → Erfassung (#26) → **Rückfluss (#24)** → Lese-Agenda (#25, offen).

---

## Scope / Abgrenzung

### Enthalten

- **Skill `/dtb:meeting-dump`** — Capture-/Rückfluss-Werkzeug nach Vorbild `/dtb:open-question`
  (`disable-model-invocation: true`), aber mit Abgleich-Schritt und Belegablage.
- **Eingabe (schneller Pfad):** Meeting-Notizen als **Freitext-Dump direkt im Chat**. Leerer
  Aufruf → nachfragen statt abbrechen. Markdown/Sonderzeichen 1:1 übernehmen, nichts escapen.
- **Beleg persistieren:** Roh-Dump unverändert nach `project-meetings/YYYY-MM-DD.md` schreiben
  (neuer, flacher Ordner). Bleibt als Quelle/Beleg liegen. Meeting-Datum wird erfragt
  (Default: heute). Zwei Meetings am selben Tag → an Tagesdatei anhängen
  (`## Besprechung 2 – HH:MM`). Doppel-Lauf mit identischem Dump → warnen, nicht doppelt anhängen.
- **Scan offener Fach-Fragen:** exakte §6-Kanonform `- [ ] [Fach] …` in `## Offene Punkte` der
  Dateien, in die die §6-Schreiber schreiben (aktuell `features/*/{discovery,spec}.md`).
  `archive/` wird nicht gescannt. Kein Fuzzy-Matching auf der Lese-Seite.
- **Abgleich-Vorschlag + Freigabe (Variante B als Liste):** Zuordnung Meeting-Aussage ↔ offene
  Frage als Tabelle zeigen (Frage, Feature/Datei, Antwort-Kandidat, Konfidenz), auf Freigabe
  warten (alle / Nummern / abbrechen) — **erst dann** schreiben.
- **Rückschreiben §6-konform** (nur nach Freigabe):
  - **Vollantwort:** Checkbox `[ ]`→`[x]`, Antwort als eingerückte Fortsetzungszeile
    `→ Antwort: … (Meeting YYYY-MM-DD)`.
  - **Teilantwort:** Frage bleibt **offen** (`[ ]`), Zwischeninfo als
    `→ Zwischenstand: … (Meeting YYYY-MM-DD)` (neue §6.1-Form).
- **Konflikte immer ausweisen statt still handeln:** eine Aussage passt auf mehrere Fragen;
  Widerspruch im Dump selbst; Frage schon `[x]` beantwortet, Meeting liefert Abweichung
  (nicht überschreiben — Beleg bleibt, als Konflikt melden).
- **Rest-Input ausweisen:** was zu keiner offenen Frage passt, am Ende als „Nicht zugeordnet"
  auflisten mit Werkzeug-Hinweis (`/dtb:idea`, `/dtb:open-question <slug>`). Bleibt im Beleg.
- **Kanon-Update (Pflichtteil, gleicher Umsetzungs-Zug):** `DERIVED_STATE_RULES.md` §6.1
  (`→ Zwischenstand:`-Form + Seed-Vermerk) und §6.3 (Satz „kein schreibender Konsument" ersetzen).
- **Wartungs-Hinweis-Kette:** `open-question`-Hinweis „drei Schreiber" → „vier Akteure"
  (drei Erzeuger + ein Mutator meeting-dump); reziproker Gegen-Hinweis im neuen Skill.

### Nicht enthalten

- **Meeting-Agenda-Ansicht vorab** (Einsammeln offener `[Fach]`-Fragen als Agenda) → bleibt #25
  (`fach-agenda`), noch nicht gebaut.
- **Neue Fach-Fragen anlegen** → das ist `/dtb:open-question`; meeting-dump mutiert nur bestehende.
- **Aktives Weiterreichen von Rest-Input** in INBOX / `## Offene Punkte` → nur ausweisen, keine
  Duplikation der Erfassungs-Logik anderer Skills (mögliche Folge-Idee).
- **Antwort-Versionierung** bei bereits beantworteten Fragen → nur Konflikt-Hinweis, manuelle
  Behandlung (MVP-Schnitt).
- **Scan von `plan.md`/`bug.md`/`task.md`** → `## Offene Punkte` lebt dort nicht (#13-MVP-Schnitt).
- **Berühren von `## Progress`, Statusfeldern oder Eintrags-Reihenfolge** → Status-Neutralität §6.2.
- **Anlegen von `project-meetings/` durch `project-init`** → der Skill erstellt den Ordner
  bei Bedarf selbst.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Fehlzuordnung Antwort ↔ Frage schreibt falsche Antwort als Beleg | Mittel | Hoch | Abgleich-Vorschlag + Freigabe VOR jedem Schreiben (Variante B); nichts wird still gehakt |
| §6.1-Erweiterung (`→ Zwischenstand:`) erreicht Bestandsprojekte nicht (Seed-Skew, #22) | Hoch | Niedrig | Rein additiv, kein Lese-Skill bricht; Standard-Seed-Vermerk in Regel-Datei; #22 bleibt eigenständig |
| Grammatik-Drift zwischen den vier §6-Akteuren | Mittel | Mittel | Single Source §6; reziproke Wartungs-Hinweise (open-question ↔ meeting-dump); Lese-Grammatik = Schreib-Grammatik |
| Beleg-Datei wird zum zweiten Status-Speicher (Derived-State-Verletzung) | Niedrig | Hoch | Beleg enthält nur Roh-Dump, NIE Abgleich-Ergebnisse; kanonischer Ort bleibt die Frage selbst |
| Roh-Dump enthält versehentlich Sensibles, landet im Repo | Niedrig | Mittel | Beleg bleibt lokal im Projekt; kein Auto-Commit durch den Skill (Commit über commit-and-push/checkpoint mit Red-Flag-Scan) |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine harten Vorbedingungen — Skill läuft config-los (Fallback-Pfade) und ohne offene
      Fragen (0 Fragen = definierter Pfad, Beleg wird trotzdem gespeichert)

### Referenz-Dokumente
- `features/meeting-dump/discovery.md` - vollständige Discovery (alle Entscheidungen 3a–3e)
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` §6 - Fach-Frage-Konvention (zu erweitern)
- `skills/dtb-open-question/SKILL.md` - Vorbild: Platzierungs-/Duplikat-/Normalisierungs-Logik
  für `## Offene Punkte`; Kopplungs-Knoten der Wartungs-Hinweise
- `skills/dtb-feature-discover/SKILL.md`, `skills/dtb-feature-plan/SKILL.md` - die zwei anderen
  §6-Schreiber (Format-Kopplung)
- `skills/CLAUDE.md` - Frontmatter-/Pipeline-Konventionen, Eligibility-Gate-Einteilung

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] `/dtb:meeting-dump "<notizen>"` persistiert den Roh-Dump nach `project-meetings/YYYY-MM-DD.md`
      (Ordner bei Bedarf angelegt) und zeigt einen Abgleich-Vorschlag als Tabelle
- [ ] Nach Freigabe wird eine passende offene `- [ ] [Fach]`-Frage zu `- [x]` + `→ Antwort: … (Meeting <Datum>)`,
      ohne `## Progress`/Statusfelder/Reihenfolge zu verändern
- [ ] Eine Teilantwort lässt die Frage offen (`[ ]`) und ergänzt `→ Zwischenstand: … (Meeting <Datum>)`
- [ ] Konflikte (Mehrfach-Match, Dump-Widerspruch, bereits `[x]`-beantwortet) werden ausgewiesen
      statt still verarbeitet
- [ ] Rest-Input erscheint als „Nicht zugeordnet"-Block mit Werkzeug-Hinweis; nichts geht verloren
- [ ] `DERIVED_STATE_RULES.md` §6.1 (+ `→ Zwischenstand:`) und §6.3 (Konsumenten) sind aktualisiert;
      `open-question`-Wartungs-Hinweis nennt vier Akteure; reziproker Hinweis im neuen Skill steht
- [ ] 0 offene Fragen und leerer Aufruf führen zu definiertem Verhalten (Beleg speichern bzw.
      nachfragen), nicht zu Absturz/Rateergebnis

---

## Offene Punkte

- Konfidenz-Einstufung im Abgleich-Vorschlag: reicht eine zweistufige Markierung
  (sicher / unsicher), oder braucht es eine dreistufige (hoch/mittel/niedrig)? — im impl-plan
  entscheidbar (normaler offener Punkt, keine Fach-Meeting-Frage → untagged)
- Reihenfolge-Abhängigkeit zu #25 (fach-agenda): meeting-dump ist ohne die Lese-Agenda nutzbar
  (eigener Scan), der spätere `after: dtb:fach-agenda`-Anschluss wird erst mit #25 eingetragen

---

**Erstellt mit:** `/dtb:feature-plan`
