# Discovery: open-question
<!-- resume: done -->

**Erstellt:** 2026-07-18
**Idee-Referenz:** Inbox #26 — "Aktiver Erfassungs-Skill /dtb:open-question (Vorbild /dtb:idea, aber fuer Fach-Fragen): Frage per Text-Argument -> als [Fach]-Frage nach §6 ablegen (`- [ ] [Fach] {Frage}` in `## Offene Punkte`)."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-open-question/SKILL.md` | NEU — der zu bauende Erfassungs-Skill |
| `skills/dtb-idea/SKILL.md` | Struktur-Vorbild (Config->Input->Write->Confirm, `disable-model-invocation: true`, `allowed-tools`, `argument-hint`) |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §6 = Schreib-Format (`- [ ] [Fach] {Frage}` in `## Offene Punkte`); §1.1 = Ableitung des aktiven „In Arbeit"-Features |
| `skills/dtb-feature-discover/SKILL.md` + `skills/dtb-feature-plan/SKILL.md` | Bestehende Schreiber von `## Offene Punkte`; open-question wird dritter Schreiber -> Format-Kopplung |
| `skills/dtb-kit-sync/SKILL.md` | Neuer Skill = Klasse A -> global verteilen + Lock-Eintrag |
| `CLAUDE.md` (Repo-Root) | Skill-Katalog: neuer Skill muss gelistet werden |

---

## Anforderungen

### Scope
**Enthalten:**
- `/dtb:open-question "{Frage}"` schreibt die Frage §6-konform als `- [ ] [Fach] {Frage}` in `## Offene Punkte` eines Change-Artefakts.
- **Ziel-Feature (Variante c):** Default = aktives „In Arbeit"-Feature ableiten (§1.1: `plan.md` teilweise abgehakt); Override per optionalem Slug-Argument (`/dtb:open-question <slug> "{Frage}"`). Bei Mehrdeutigkeit fragen.
- **Ziel-Datei:** am weitesten fortgeschrittene vorhandene — `spec.md` falls vorhanden, sonst `discovery.md`; `## Offene Punkte` anlegen, falls die Sektion fehlt. (`plan.md` bleibt außen vor — MVP-Schnitt #13.)

**Nicht enthalten:**
- Beantworten/Abhaken von Fragen (-> #24).
- Lese-/Agenda-Ansicht (-> #25).
- `[Stakeholder]`-Tag (spaeter).
- Zweiter Speicherort (waere Derived-State-Drift).

### Gewuenschtes Verhalten
- **Reibungslos wie `/dtb:idea`, aber mit Ziel-Bestaetigung (Variante B, immer):** Skill zeigt das
  ermittelte Ziel (`features/<slug>/<datei>`) + die formatierte `- [ ] [Fach] {Frage}`-Zeile an und
  wartet auf kurze Freigabe (ok/ja), *dann* schreiben. Bewusster Unterschied zu `/dtb:idea` (das
  still schreibt) — verhindert Fehl-Ablage bei abgeleitetem Ziel.
- **Bestaetigung nach dem Schreiben:** kompakt, mit Verweis auf die spaetere Agenda-Ansicht (#25) /
  `/dtb:workflow-next`.
- **UX-Skelett = `/dtb:idea`-Muster:** Schritt 0 Config -> 1 Input -> 2 Ziel ermitteln+bestaetigen ->
  3 Write -> 4 Confirm. `disable-model-invocation: true`, `allowed-tools: Read, Edit, Write`.

### Randfaelle
- **0 aktive Features + kein Slug:** abbrechen mit Hinweis „Kein aktives Feature. Ziel angeben:
  `/dtb:open-question <slug> \"{Frage}\"`" + kurze Liste waehlbarer Feature-Slugs. Kein Schreiben ins Blaue.
- **>1 aktive Features + kein Slug:** Auswahlliste zeigen (analog `workflow-resume` Fall B), Nutzer waehlt.
  Kein stilles Raten.
- **Slug zeigt auf nicht existierenden/leeren Ordner:** abbrechen, „Feature `<slug>` nicht gefunden" +
  Liste vorhandener Feature-Ordner. Kein Auto-Anlegen (das ist `feature-discover`s Job).
- **Ziel-Feature ohne `discovery.md`/`spec.md` (nur `plan.md`/`bug.md`/`task.md`):** `## Offene Punkte`
  gehoert nicht in `plan.md` (#13). -> in `spec.md` schreiben falls vorhanden; sonst abbrechen mit Hinweis.
  `bug.md`/`task.md` sind KEIN Schreibziel.
- **Leeres/fehlendes Frage-Argument:** nachfragen „Welche Fach-Frage moechtest du festhalten?" (wie `/dtb:idea`),
  nicht abbrechen.
- **Sonderzeichen/Markdown in der Frage:** 1:1 als Inline-Text uebernehmen (nur `- [ ] [Fach] ` voranstellen);
  mehrzeilige Eingabe zu einer Bullet-Zeile normalisieren (§6-Grammatik verlangt eine Zeile). Kein Escaping.

### Einschraenkungen
- **Derived-State-Neutralitaet (Invariante):** schreibt ausschliesslich in `## Offene Punkte`
  (status-neutral, §6.2). Beruehrt `## Progress`/Statusfelder NIE — das Erfassen einer `[Fach]`-Frage
  aendert den abgeleiteten Feature-Status nicht (auch kein „Fertig zum Testen" -> „In Arbeit").
- **§6-Grammatik strikt:** Ausgabe exakt `- [ ] [Fach] {Frage}` (je ein Leerzeichen). Der Skill ist der
  erste maschinelle Schreiber des Formats -> muss die Grammatik selbst garantieren (nicht nur empfehlen).
- **Platzierung:** neue Zeile ans Ende der bestehenden `## Offene Punkte`-Sektion anhaengen (vor naechste
  `##`-Ueberschrift / `**Erstellt mit:**`-Footer); fehlt die Sektion, vor dem Footer neu einfuegen.
  Bestehende Eintraege nie umsortieren.
- **Duplikat-Schutz:** existiert die exakt gleiche Frage schon als offene `[Fach]`-Zeile -> warnen +
  ueberspringen (nur exakter Textvergleich, kein Fuzzy-Matching).
- **Verteilung:** neuer Skill = Klasse A -> `kit-sync`-Distribution + Lock-Eintrag nach dem Bau
  (Umsetzungs-Constraint, kein Discovery-Entscheid).
- Keine externen/fachlichen Constraints (rein kit-internes Werkzeug).

### Integrationspunkte
- **`## Offene Punkte`-Oekosystem:** open-question wird der DRITTE Schreiber dieser Sektion neben
  `feature-discover` (`discovery.md`) und `feature-plan` (`spec.md`) — alle drei muessen dasselbe
  §6-Format erzeugen (Format-Kopplung bei kuenftigen §6-Aenderungen mitziehen).
- **`DERIVED_STATE_RULES.md` §6 + §1.1** als gelesene Autoritaet (Grammatik + aktives-Feature-Ableitung).
- **`pipeline-graph`/`workflow-status`** zeichnen den Skill automatisch aus dem Frontmatter;
  **`project-health`** lintet es — kein manuelles Zutun.
- **Pipeline-Frontmatter:** `stage: capture`, `after: null` (jederzeit aufrufbar),
  `consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]`,
  `produces: [features/*/spec.md, features/*/discovery.md]`,
  `next: [dtb:workflow-next]` (spaeter `dtb:fach-agenda` #25, sobald dieser existiert).
- **Externe Abhaengigkeiten:** keine (nur Dateisystem im Zielprojekt).

---

## Abhaengigkeiten

- **Kein Konflikt** mit den 5 bestehenden Features.
- **Enge Verwandtschaft (kein Widerspruch) zu `fachfragen-erfassung` (#13):** #13 definiert das
  `[Fach]`-Format (§6, gebaut); open-question liefert die Erfassung/Eingabe, die #13 bewusst ausklammerte.
- **Nachgelagert (noch keine Ordner):** #25 (Lese-Ansicht/Agenda) liest kuenftig, was open-question schreibt;
  #24 (Antwort-Rueckfluss) ergaenzt spaeter. Beide reine INBOX-Ideen -> keine Ordner-Kollision.

---

## Offene Punkte

- Genauer Wortlaut der Ziel-Bestaetigung (Variante B) und der Duplikat-Warnung final in `impl-plan` festlegen.
- `next: [dtb:fach-agenda]` erst verdrahten, wenn #25 existiert (bis dahin `dtb:workflow-next`).

---

**Erstellt mit:** `/dtb:feature-discover`
