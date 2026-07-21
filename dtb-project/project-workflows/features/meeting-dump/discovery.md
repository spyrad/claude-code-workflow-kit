# Discovery: meeting-dump (Meeting-Nachbereitung / Antwort-Rückfluss)
<!-- resume: done -->

**Erstellt:** 2026-07-20
**Feature-Name:** meeting-dump (Skill `/dtb:meeting-dump`) — Ordner-Slug = Skill-Name (wie open-question)
**Idee-Referenz:** Inbox #24 — "Skill für Besprechungs-Nachbereitung: Punkte/Antworten/Input aus der letzten Projekt-Besprechung eingeben und gegen die offenen Fragen der Features prüfen. Abgleich Meeting-Ergebnisse ↔ offene Punkte in `features/*/{discovery,spec,plan}.md`; beantwortete Fragen zuordnen/nachtragen, unbeantwortete/neue Punkte sichtbar machen."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-meeting-dump/SKILL.md | Neuer Skill (Träger entschieden: eigener Skill `/dtb:meeting-dump`) |
| dtb-project/project-rules/DERIVED_STATE_RULES.md §6 | Kanon: Antwort-Nachtrag-Grammatik (§6.1) bereits definiert; #24 wird erster schreibender Konsument → §6.3-Satz („kein schreibender Konsument") anpassen |
| skills/dtb-open-question/SKILL.md | Nächster Verwandter: Platzierungs-/Duplikat-/Normalisierungs-Logik für `## Offene Punkte` wiederverwendbar; Wartungs-Hinweis „drei Schreiber" → „vier Schreiber" |
| skills/dtb-feature-discover/SKILL.md | Schreiber #1 der `## Offene Punkte` (discovery.md) — Format-Kopplung |
| skills/dtb-feature-plan/SKILL.md | Schreiber #2 (spec.md) — Format-Kopplung |
| features/*/{discovery,spec}.md (Zielprojekte) | Datenbasis: dort wird gescannt und zurückgeschrieben |
| skills/CLAUDE.md | Eligibility-Gate-Tabelle + Frontmatter-Konventionen — Einordnung des neuen Skills |

**Hinweis:** #25 (`fach-agenda`, Lese-Ansicht) ist NICHT gebaut — #24 muss den Scan nach
offenen `- [ ] [Fach]`-Fragen selbst mitbringen.

---

## Anforderungen

### Scope

**Enthalten:**
- Kern: Meeting-Input abgleichen gegen alle offenen `- [ ] [Fach]`-Fragen in
  `features/*/{discovery,spec}.md` — Treffer abhaken (`[x]`) + Antwort §6.1-konform nachtragen
  (`→ Antwort: … (Meeting YYYY-MM-DD)`), Unbeantwortetes offen lassen und zeigen,
  neue Punkte sichtbar machen
- Meeting-Roh-Input wird als **Datei persistiert und bleibt als Beleg liegen**
  (Quelldokument, kein Status-Speicher — Analogie: Drop-Zone-Muster wie `docs-extract`)
- Eingabeweg: **Freitext direkt im Chat** als schneller Pfad („hier mein Dump: …")

**Nicht enthalten:**
- Keine Meeting-Agenda-Ansicht vorab (bleibt #25 / fach-agenda)
- Kein Anfassen von `## Progress`, Checkbox-Gates oder Statusfeldern (§6.2 Status-Neutralität)
- Kanonischer Ort der Antwort bleibt die Frage selbst — die Meeting-Datei ist Quelle/Beleg,
  nie zweiter Speicherort des Frage-Status

### Gewuenschtes Verhalten
- **Träger:** eigener Skill (Arbeitsname `/dtb:meeting-dump`) — dritter Verb-Schritt der
  Fachfragen-Kette (#13 Konvention → #26 Erfassung → **#24 Rückfluss**), kein Anbau an #13
- **Ablauf:** Dump in den Chat → Skill persistiert ihn als Beleg-Datei → zeigt
  **Abgleich-Vorschlag** als Tabelle (Antwort ↔ Frage, mit Feature/Datei und Konfidenz) →
  Freigabe (alle / Nummern / abbrechen) → erst dann abhaken + Antwort nachtragen
- **Bestätigungs-Muster:** Variante B von `open-question` (Ziel + formatierte Zeile zeigen,
  Freigabe abwarten), hier als **Liste von Zuordnungen** — Begründung: Abgleich ist
  Interpretationsarbeit, Fehlzuordnungen würden falsche Antworten als Beleg festschreiben
- **Rest-Input** (passt zu keiner offenen Frage): nur ausweisen als „Nicht zugeordnet"-Block
  mit Werkzeug-Hinweis (`/dtb:idea`, `/dtb:open-question <slug>`), NICHT aktiv weiterreichen —
  keine Duplikation der Erfassungs-Logik anderer Skills; Dump bleibt als Beleg liegen,
  nichts geht verloren (aktives Weiterreichen = mögliche Folge-Idee)

### Randfaelle

**Abgleich (Block 1 — entschieden):**
- Keine offenen `[Fach]`-Fragen im Projekt → kein Abbruch: Dump trotzdem als Beleg
  persistieren, ehrlich melden, kompletten Input als „Nicht zugeordnet" ausweisen
- Eine Aussage passt auf mehrere offene Fragen → beide Zuordnungen zeigen, als Konflikt
  markiert, Nutzer entscheidet per Freigabe (kein stilles Doppel-Abhaken)
- **Teilantwort:** Frage bleibt offen (`[ ]`), Zwischeninfo wird als eingerueckte Zeile
  nachgetragen: `→ Zwischenstand: … (Meeting YYYY-MM-DD)` — ⚠ bewusste **Erweiterung der
  §6.1-Grammatik** (zweite Fortsetzungszeilen-Form unter `[ ]`) → DERIVED_STATE_RULES.md
  §6.1 muss mitgezogen werden
- Frage schon `[x]` beantwortet, Meeting liefert abweichende Antwort → nicht ueberschreiben
  (Beleg!), als Konflikt ausweisen („beantwortet am …, Meeting sagt jetzt X"), Behandlung
  manuell (MVP: keine Antwort-Versionierung)

**Input (Block 2 — entschieden):**
- Leerer Aufruf → nachfragen statt abbrechen (Muster `open-question` Schritt 1)
- Widerspruch im Dump selbst (zwei Stellen, gleiche Frage, andere Antwort) → beide zeigen,
  Konflikt markieren, Nutzer waehlt
- Meeting-Datum: Skill fragt nach bzw. bietet heutiges Datum als Default an (Nachbereitung
  oft am Folgetag — stilles „heute" waere falsch)
- Markdown/Sonderzeichen im Dump → 1:1 uebernehmen, nichts escapen (wie `open-question`)

**Beleg-Datei (Block 3 — entschieden):**
- Ablage-Ort: `dtb-project/project-meetings/YYYY-MM-DD.md` (flach, Datum als Name;
  Rueckverfolgung `(Meeting YYYY-MM-DD)` ↔ Dateiname) — Alternativen verworfen:
  `project-requirements/input/` (semantisch falsch, docs-extract-Drop-Zone),
  `project-workflows/` (vermischt Beleg mit Workflow-Artefakten)
- Zwei Meetings am selben Tag → an Tagesdatei anhaengen (`## Besprechung 2 – HH:MM`,
  Muster Changelog-Session-Logs)
- Inhalt: nur Header (Datum, Erfassungszeitpunkt) + Roh-Dump unveraendert; Abgleich-Ergebnisse
  NICHT hineinschreiben (Antworten leben in den Features — sonst zweiter Speicherort)
- Doppel-Lauf mit identischem Dump → vor Anhaengen pruefen, warnen, nicht doppelt anhaengen

### Einschraenkungen
- **Status-Neutralitaet (§6.2, Invariante):** Skill schreibt nur `## Offene Punkte` +
  Beleg-Datei; nie `## Progress`, Statusfelder oder Eintrags-Reihenfolge (nur Checkbox
  flippen + Zeile einruecken; beantwortete Eintraege bleiben als Beleg stehen). Ein Meeting
  aendert den Feature-Status nie — der Skill bleibt komplett aus der Gate-Mechanik raus
- **Exakte Kanonform beim Scan:** nur `- [ ] [Fach] …` in `## Offene Punkte` matcht
  (kein Fuzzy auf der Lese-Seite, untagged Bullets ignoriert); `archive/` wird nicht
  gescannt (Antwort auf archivierte Frage → „Nicht zugeordnet"). Symmetrie-Garantie:
  Lese-Grammatik = Schreib-Grammatik, Single Source §6 (Wartungs-Hinweis-Muster)
- **Scan-Reichweite:** „liest, wo die §6-Schreiber schreiben" — aktuell
  `features/*/{discovery,spec}.md` (#13-MVP-Schnitt; Idee-Text nannte noch plan.md —
  vor dem Schnitt formuliert). Keine harte Dateiliste im Skill, Reichweite wandert mit
  der Konvention mit
- **Kit-Sync:** Klasse A automatisch (`skills/dtb-*/SKILL.md`-Muster).
  `allowed-tools: Read, Glob, Grep, Edit, Write` (Write fuer Beleg-Datei/Ordner —
  Unterschied zu open-question), `disable-model-invocation: true` (Capture-Werkzeug)
- **Seed-Skew (§6.1-Erweiterung, entschieden: hinnehmen):** `→ Zwischenstand:` aendert
  die Klasse-B-Seed-Datei `DERIVED_STATE_RULES.md` — Bestandsprojekte erben das nicht.
  Rein additiv, kein Lese-Skill bricht; Standard-Vermerk in der Regel-Datei
  („Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22").
  #22 bleibt eigenstaendig in der Triage (nicht als Abhaengigkeit vorgezogen)
- Fachliche Constraints: keine (Meeting-Inhalte bleiben lokal im Projekt)

### Integrationspunkte
- **Kanon-Update `DERIVED_STATE_RULES.md` §6 (Pflichtteil, gleicher Commit-Zug):**
  - §6.1: zweite Fortsetzungszeilen-Form ergaenzen — `→ Antwort:` nur unter `[x]`,
    `→ Zwischenstand:` nur unter `[ ]` (mehrere Zwischenstaende ueber die Zeit erlaubt,
    je Meeting einer; erst haken, wenn echte Antwort da). + Seed-Vermerk im Fussblock
  - §6.3: Satz „kein schreibender Konsument in diesem Feature" ersetzen — zwei Konsumenten:
    lesend die Agenda-Ansicht (#25, offen), schreibend der Rueckfluss `dtb:meeting-dump`
    (nur Checkbox-Flip + Fortsetzungszeile)
- **Wartungs-Hinweis-Kette:** `open-question`-Hinweis von „drei Schreiber" auf „vier Akteure"
  erweitern (drei Erzeuger + ein **Mutator** meeting-dump — legt keine neuen `[Fach]`-Fragen
  an, mutiert bestehende). Reziproken Gegen-Hinweis im neuen Skill setzen (Muster
  implement ↔ commit-and-push). `open-question` bleibt zentraler Kopplungs-Knoten
  (Hinweis nicht in feature-discover/-plan streuen)
- **Pipeline-Frontmatter (analog open-question):** `stage: capture`, `after: null`
  (eigener Einstieg; spaeter `after: dtb:fach-agenda` denkbar, wenn #25 existiert),
  `next: [dtb:workflow-next]`,
  `consumes: [workflow.config.yaml, features/*/spec.md, features/*/discovery.md]`,
  `produces: [features/*/spec.md, features/*/discovery.md, project-meetings/*.md]`.
  Bewusste Nebenwirkung: `project-meetings/` erscheint neu in pipeline-graph/workflow-status
  (gewollt — Beleg ist produziertes Artefakt, bricht nichts)
- **Kein Eligibility-Hard-Gate:** keine zwingende Eingabe (0 offene Fragen = definierter Pfad;
  laeuft config-los mit Fallback). Reiht sich bei open-question/idea/commit-and-push ein
  (weicher Redirect: leerer Aufruf → nachfragen). **Kein** neuer Eintrag in der
  Hard-Gate-Tabelle von `skills/CLAUDE.md`
- **Bewusst KEINE Integration:** project-init legt `project-meetings/` NICHT vorab an
  (Skill erstellt Ordner bei Bedarf — kein leerer Ordner je Projekt). Keine externen
  Abhaengigkeiten

---

## Abhaengigkeiten

- **Konflikte:** keine. **Ueberschneidungen:** keine.
- Ketten-Nachbarn grenzen #24 explizit aus und verweisen namentlich darauf:
  - fachfragen-erfassung (#13): „Antwort-Rueckfluss aus einem Meeting" unter „Nicht enthalten"
  - open-question (#26): Kette Format (#13) → Erfassung (#26) → Lese-Agenda (#25) →
    **Antwort-Rueckfluss (#24)** — #24 ist das vorgesehene naechste Glied
- Einziger Beruehrungspunkt: gemeinsame §6-Grammatik → als Pflicht-Update in
  „Integrationspunkte" (Punkt 1+2) verankert, keine Kollision
- #25 (fach-agenda) nicht gebaut → keine Gegenrichtungs-Abhaengigkeit, nur spaeterer
  `after:`-Anschluss

---

## Offene Punkte

- — keine — (Discovery abgeschlossen; alle Kategorien 3a-3e + Abhaengigkeits-Check +
  Name/Slug entschieden)

---

**Erstellt mit:** `/dtb:feature-discover`
