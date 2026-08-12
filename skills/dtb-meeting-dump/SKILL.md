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
  after: [dtb:meeting-agenda]
  next: [dtb:workflow-next]
  consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md, project-meetings/*.md]
  produces: [features/*/spec.md, features/*/discovery.md, project-meetings/*.md]
---

# Meeting-Nachbereitung (meeting-dump)

Du nimmst die Notizen aus einer Projekt-/Fach-Besprechung als **Freitext-Dump** entgegen,
legst sie als Beleg ab und gleichst sie gegen die offenen **Fach-Fragen** aller Features ab
(`- [ ] [Fach] …` in `## Offene Punkte`, Konvention `{config.paths.rules}/DERIVED_STATE_RULES.md` §6).
Beantwortete Fragen werden — **erst nach deiner Freigabe** — §6-konform abgehakt bzw. mit einem
Zwischenstand ergaenzt. Der Rueckfluss-Schritt der Fachfragen-Kette: Format (#13) → Erfassung
(`/dtb:open-question`, #26) → Lese-Agenda (`/dtb:meeting-agenda`, #25) → **Rueckfluss (dieser
Skill, #24)**.

> **Wartungs-Hinweis (Format-Kopplung):** meeting-dump ist der **Mutator** der
> `## Offene Punkte`-Sektion — neben den drei **Erzeugern** `dtb:feature-discover`
> (`discovery.md`), `dtb:feature-plan` (`spec.md`) und `dtb:open-question` (beide). Er legt
> **keine** neuen `[Fach]`-Fragen an, sondern kippt die Checkbox und haengt
> `→ Antwort:`/`→ Zwischenstand:` an bestehende. Alle vier Akteure teilen dieselbe §6-Kanonform;
> Single Source der Grammatik ist `{config.paths.rules}/DERIVED_STATE_RULES.md` §6 (Nachtrag-Formen: §6.1,
> Status-Neutralitaet: §6.2) — aenderst du sie dort, ziehe alle vier Akteure mit. Der reziproke
> Hinweis steht in `dtb:open-question` (Kopplungs-Knoten).

> **Kein formales Eligibility-Gate (bewusst):** meeting-dump ist ein Capture-Werkzeug wie
> `/dtb:idea`/`/dtb:open-question` (`disable-model-invocation: true`) und hat **keine zwingende
> Eingabe** — 0 offene Fach-Fragen ist ein definierter Pfad (Schritt 3: Beleg wird trotzdem
> gespeichert, alles → „Nicht zugeordnet"), und der Skill laeuft config-los. Daher **kein
> Hard-Gate** nach `skills/CLAUDE.md` und **kein** Eintrag in dessen Hard-Gate-Tabelle.

## Worktree-Guard (Schritt 0)

Dieser Skill schreibt globale Dateien und laeuft nur in der Orchestrator-Session —
Schreibgrenzen-Regel: `skills/CLAUDE.md` → „Parallele Sessions".

Pruefe VOR dem ersten Schreiben in EINEM selbstaendigen Bash-Block (cd/pwd-Normalisierung
ist Pflicht — ohne sie False Positives in Unterverzeichnissen):

```bash
G=$(git rev-parse --git-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
C=$(git rev-parse --git-common-dir 2>/dev/null) || { echo DURCHLASS-NOGIT; exit 0; }
G=$(cd "$G" && pwd); C=$(cd "$C" && pwd)
if [ "$G" = "$C" ]; then echo HAUPT-CHECKOUT; else echo "WORKTREE (Haupt-Checkout: $(dirname "$C"))"; fi
```

- `DURCHLASS-NOGIT` (kein Git-Repo/Fehlschlag) oder `HAUPT-CHECKOUT` → Durchlass, KEIN
  Output — der Guard bleibt unsichtbar. Zusatz nur bei gesetztem `parallel.default_branch`
  (nicht `null`) in `workflow.config.yaml`: aktueller Branch ungleich dem Wert → Abbruch
  mit Hinweis „globale Dateien gehoeren auf `{default_branch}`"
- `WORKTREE` (verlinkter Worktree) → harter Abbruch, nichts schreiben:

  ```
  ⛔ dtb:meeting-dump schreibt globale Dateien und laeuft nur in der Orchestrator-Session
     (Schreibgrenzen-Regel: skills/CLAUDE.md → „Parallele Sessions").
     Haupt-Checkout: {Pfad aus der WORKTREE-Ausgabezeile}
  ```

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

## Schritt 3: Offene Fach-Fragen scannen

Finde die Abgleich-Basis **deterministisch** — die exakte §6-Kanonform, nicht per Fuzzy-Suche:

1. **Wo:** die Dateien, in die die §6-Schreiber schreiben — `{config.paths.workflows}/features/*/spec.md`
   **und** `.../features/*/discovery.md`. **`archive/` wird NICHT gescannt** (archivierte Changes
   haben keine aktiven Fragen mehr).
2. **Was:** in der Sektion `## Offene Punkte` jede Zeile der exakten Form `- [ ] [Fach] <Frage>`
   (offen). Nur diese Kanonform matcht — untagged Bullets (normale offene Punkte, „nie erfinden"-
   Luecken) und bereits beantwortete `- [x] [Fach] …` werden **nicht** als offene Frage gezaehlt
   (letztere nur fuer den Konflikt-Check in Schritt 4 herangezogen).
3. **Merke pro Treffer:** Feature-Slug, Datei, Zeilentext, ob unter der Zeile schon
   `→ Zwischenstand:`-Fortsetzungszeilen stehen (fuer Platzierung + Akkumulation in Schritt 5).
4. **0 offene Fragen** → kein Abbruch: der Beleg (Schritt 2) ist bereits gespeichert; melde
   „0 offene Fach-Fragen — nichts abzugleichen" und behandle den **gesamten** Dump als
   „Nicht zugeordnet" (Schritt 6).

---

## Schritt 4: Abgleich-Vorschlag + Freigabe (Variante B)

Der Abgleich Dump↔Frage ist **Interpretation** — deshalb wird **nichts** ohne deine Freigabe
geschrieben (eine Fehlzuordnung schriebe eine falsche Antwort als Beleg fest).

1. **Vorschlag als Tabelle** (keine Konfidenz-Spalte — die Freigabe IST das Urteil):
   ```
   Abgleich-Vorschlag ({T} Treffer, {O} offen geblieben):

   | # | Frage (Feature/Datei) | Antwort aus dem Dump | Art |
   |---|-----------------------|----------------------|-----|
   | 1 | [Fach] … (slug/spec.md) | „…" | Vollantwort |
   | 2 | [Fach] … (slug/discovery.md) | „…" | Zwischenstand |
   ```
   **Art** = Vollantwort (Frage ist beantwortet → `[x]`) oder Zwischenstand (nur Teilinfo →
   bleibt `[ ]`).
2. **Konflikte ausweisen statt still handeln** — als markierte Zeilen im selben Vorschlag,
   nie automatisch geschrieben:
   - **Mehrfach-Match:** eine Dump-Aussage passt auf mehrere offene Fragen → alle betroffenen
     Zeilen zeigen, als Konflikt markiert; du entscheidest je Zeile.
   - **Dump-Widerspruch:** zwei Stellen im Dump beantworten dieselbe Frage unterschiedlich →
     beide zeigen, markiert.
   - **Bereits `[x]` beantwortet:** der Dump liefert eine abweichende Antwort auf eine schon
     abgehakte Frage → **nicht ueberschreiben** (Beleg bleibt); als Konflikt melden
     („beantwortet am …, Meeting sagt jetzt X"), Behandlung manuell.
3. **Freigabe abwarten:** `alle` / einzelne `Nummern` / `abbrechen`. Erst nach Freigabe zu
   Schritt 5. Konflikt-markierte Zeilen nur schreiben, wenn du sie ausdruecklich freigibst.

---

## Schritt 5: Rueckschreiben (§6-konform, status-neutral)

Nur die **freigegebenen** Zuordnungen, ausschliesslich in `## Offene Punkte`.

1. **Platzierungs-Mechanik (eigene Logik — NICHT das open-question-Endanhaenge-Muster):**
   `dtb:open-question` haengt neue Bullets ans **Sektionsende** — das ist hier **falsch**. Eine
   Fortsetzungszeile gehoert **in den Block ihrer Frage**:
   - Einfuegepunkt = unmittelbar **nach der gematchten `- [ ] [Fach] …`-Zeile** UND nach allen
     bereits vorhandenen eingerueckten `→`-Fortsetzungszeilen, die schon zu **dieser** Frage
     gehoeren (der Frage-Block endet an der naechsten Bullet-Zeile, Ueberschrift oder Leerzeile).
   - Einrueckung konsistent zum §6.1-Beispiel (die Fortsetzungszeile unter dem Bullet eingerueckt).
2. **Vollantwort:** die Checkbox **derselben** Zeile `- [ ]` → `- [x]` kippen und
   `→ Antwort: <Antwort> (Meeting {Datum})` als Fortsetzungszeile einfuegen (Platzierung wie 1).
3. **Zwischenstand (Teilantwort):** Checkbox bleibt `- [ ]`; `→ Zwischenstand: <Info> (Meeting {Datum})`
   als Fortsetzungszeile **akkumulierend** anhaengen (bestehende `→ Zwischenstand:`-Zeilen bleiben
   stehen — Verlauf, §6.1). Eine spaetere Vollantwort tritt als letzte Zeile hinzu.
   **Duplikat-Schutz (§6.1 „je Meeting einer"):** Steht im Block **dieser** Frage bereits eine
   `→ Zwischenstand:`-Zeile mit demselben `(Meeting {Datum})`-Marker → **nicht erneut anhaengen**
   (warnen, uebergehen). Zwischenstand-Fragen bleiben `- [ ]` und wuerden sonst bei einem
   Doppel-Lauf am selben Tag eine zweite identische Zeile erzeugen — der Beleg-Doppel-Lauf-Schutz
   (Schritt 2) deckt den Schreib-Pfad nicht ab (analog `dtb:open-question` Schritt 4.2).
4. **Status-Neutralitaet (Invariante, §6.2):** **NIE** `## Progress`, dortige Checkboxen oder
   Statusfelder beruehren; bestehende Eintraege/Reihenfolge unangetastet lassen — **nur** die
   gematchte Checkbox kippen und Fortsetzungszeilen anhaengen. Das Erfassen aendert den
   abgeleiteten Feature-Status nicht.
5. **Beleg unberuehrt:** die Datei aus Schritt 2 wird nicht nachtraeglich mit Ergebnissen
   angereichert (Antworten leben in den Features, nicht im Beleg).

---

## Schritt 6: Rest-Input ausweisen + Abschluss-Summary

Was im Dump zu **keiner** offenen Frage passt, geht nicht verloren — es wird ausgewiesen, aber
**nicht** aktiv weitergereicht (keine Duplikation der Erfassungs-Logik anderer Skills; der Beleg
aus Schritt 2 haelt ohnehin alles fest).

1. **„Nicht zugeordnet"-Block** — die uebrigen Dump-Anteile auflisten, je mit Werkzeug-Hinweis,
   wohin sie gehoeren koennten (du entscheidest, ob/wann):
   ```
   Nicht zugeordnet (im Beleg erhalten):
     - „{neue offene Frage}"      → Kandidat fuer /dtb:open-question <slug> "…"
     - „{neue Idee/Aufgabe}"      → Kandidat fuer /dtb:idea
     - „{Kontext/Rauschen}"       → bleibt nur im Beleg
   ```
   Rein technische Notizen ohne Handlungsbedarf werden nicht einzeln aufgefuehrt (nur im Beleg).
2. **Abschluss-Summary (kompakt):**
   ```
   Meeting-Nachbereitung {Datum} abgeschlossen:
     Beleg:          project-meetings/{Datum}.md
     Vollantworten:  {N}  (Fragen abgehakt + → Antwort:)
     Zwischenstaende: {M} (Fragen offen + → Zwischenstand:)
     Konflikte:      {K}  (ausgewiesen, nicht automatisch geschrieben)
     Nicht zugeordnet: {R}

   Offene Fach-Fragen spaeter via /dtb:meeting-agenda (Lese-Ansicht der Kette).
   ```

---

**Erstellt mit:** `/dtb:meeting-dump`
