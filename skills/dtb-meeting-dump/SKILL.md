---
name: dtb:meeting-dump
description: >-
  Use when: "Meeting nachbereiten", "Besprechungs-Notizen erfassen", "meeting dump",
  "Antworten aus dem Fach-Meeting einpflegen", "offene Fach-Fragen abgleichen". Persists
  raw meeting notes as evidence under project-meetings/ and reconciles them against the
  open `[Fach]` questions across all features — matched answers get checked off and
  annotated §6-conform after an explicit approval step.
disable-model-invocation: true
argument-hint: "[<Meeting-Notizen als Freitext-Dump>]"
allowed-tools: Read, Glob, Grep, Edit, Write
pipeline:
  stage: capture
  after: null
  next: [dtb:workflow-next]
  consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]
  produces: [features/*/spec.md, features/*/discovery.md, project-meetings/*.md]
---

# Meeting-Nachbereitung (meeting-dump)

Du nimmst die Notizen aus einer Projekt-/Fach-Besprechung als **Freitext-Dump** entgegen,
legst sie als Beleg ab und gleichst sie gegen die offenen **Fach-Fragen** aller Features ab
(`- [ ] [Fach] …` in `## Offene Punkte`, Konvention `{config.paths.rules}/DERIVED_STATE_RULES.md` §6).
Beantwortete Fragen werden — **erst nach deiner Freigabe** — §6-konform abgehakt bzw. mit einem
Zwischenstand ergaenzt. Der Rueckfluss-Schritt der Fachfragen-Kette: Format (#13) → Erfassung
(`/dtb:open-question`, #26) → **Rueckfluss (dieser Skill, #24)** → Lese-Agenda (#25).

> **Wartungs-Hinweis (Format-Kopplung):** meeting-dump ist der **Mutator** der
> `## Offene Punkte`-Sektion — neben den drei **Erzeugern** `dtb:feature-discover`
> (`discovery.md`), `dtb:feature-plan` (`spec.md`) und `dtb:open-question` (beide). Er legt
> **keine** neuen `[Fach]`-Fragen an, sondern kippt die Checkbox und haengt
> `→ Antwort:`/`→ Zwischenstand:` an bestehende. Alle vier Akteure teilen dieselbe §6-Kanonform;
> Single Source der Grammatik ist `{config.paths.rules}/DERIVED_STATE_RULES.md` §6 (Nachtrag-Formen: §6.1,
> Status-Neutralitaet: §6.2) — aenderst du sie dort, ziehe alle vier Akteure mit. Der reziproke
> Hinweis steht in `dtb:open-question` (Kopplungs-Knoten).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfade `dtb-project/project-workflows/` (Features) und
`dtb-project/project-meetings/` (Beleg). Der Skill laeuft auch config-los.

---

## Schritt 1: Meeting-Dump entgegennehmen

**Input:** Das gesamte Argument nach dem Command-Aufruf ist der Roh-Dump (freie Meeting-Notizen).

- **Leerer/fehlender Dump** → nachfragen (nicht abbrechen):
  ```
  Was kam aus der Besprechung? Notizen hier als Freitext einfuegen
  (Antworten, Entscheidungen, neue Punkte — Rohform genuegt).
  ```
- **Markdown/Sonderzeichen** im Dump (Listen, Backticks, `[...]`) → 1:1 als Inline-Text
  uebernehmen; **nichts escapen**, nichts umformatieren.
- **Meeting-Datum bestimmen:** kurz erfragen, mit dem **heutigen Datum als Default** anbieten
  (Nachbereitung erfolgt oft am Folgetag — stilles „heute" waere falsch). Format `YYYY-MM-DD`.
  Dieses Datum ist zugleich der Beleg-Dateiname (Schritt 2) und der `(Meeting YYYY-MM-DD)`-Marker
  in den spaeteren Nachtraegen.

---

## Schritt 2: Beleg persistieren (project-meetings/)

Der Roh-Dump wird als **Quelle/Beleg** abgelegt — unveraendert, ohne Abgleich-Ergebnisse
(die leben in den Features, §6; kein zweiter Status-Speicher).

1. **Ordner sicherstellen:** `dtb-project/project-meetings/` (Geschwister-Ordner zu
   `{config.paths.workflows}`; die Config hat bewusst keinen eigenen `meetings`-Pfad).
   Fehlt der Ordner → anlegen (kein `project-init` noetig).
2. **Eine Datei pro Kalendertag:** `project-meetings/{Meeting-Datum}.md` (z.B. `2026-07-21.md`).
3. **Neuer Tag → neue Datei** mit Kopf + Roh-Dump:
   ```markdown
   # Besprechung {YYYY-MM-DD}

   ## Besprechung 1 – {HH:MM}

   {Roh-Dump 1:1}
   ```
4. **Zweite Besprechung am selben Tag → anhaengen** an dieselbe Tagesdatei als weitere Sektion
   `## Besprechung 2 – {HH:MM}` (Muster wie die Session-Logs im Changelog); Kopf nicht doppeln.
5. **Doppel-Lauf-Schutz:** Steht der identische Dump-Text bereits in der Tagesdatei →
   **warnen und nicht doppelt anhaengen**:
   ```
   Dieser Dump steht bereits in project-meetings/{datum}.md — nichts angehaengt.
   ```
6. **Sensibilitaets-Hinweis (immer, schlank):** Nach dem Schreiben einen sichtbaren Einzeiler
   ausgeben — der Beleg ist git-getrackt und wandert mit dem naechsten `commit-and-push` ins
   Repo/Remote:
   ```
   ⚠ Meeting-Klartext liegt jetzt in project-meetings/{datum}.md und ist versionierbar
     (naechster commit-and-push → Repo/Remote). Sensibles vorher entfernen?
   ```
   Kein Gate, kein Extra-Schritt an `commit-and-push` — der Inhalt ist i.d.R. technische
   Fach-Klaerung (Risikoklasse wie `discovery.md`/`spec.md`), der Hinweis deckt den seltenen
   Ausrutscher ab.

---

<!-- Ab hier folgt die Kern-Logik (Scan, Abgleich+Freigabe, Rueckschreiben, Rest-Input) —
     Umsetzung in Phase 3 des Implementierungsplans (features/meeting-dump/plan.md). -->

**Erstellt mit:** `/dtb:meeting-dump`
