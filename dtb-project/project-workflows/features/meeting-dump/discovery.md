# Discovery: Meeting-Nachbereitung (Antwort-Rückfluss)
<!-- resume: 3b -->

**Erstellt:** 2026-07-20
**Idee-Referenz:** Inbox #24 — "Skill für Besprechungs-Nachbereitung: Punkte/Antworten/Input aus der letzten Projekt-Besprechung eingeben und gegen die offenen Fragen der Features prüfen. Abgleich Meeting-Ergebnisse ↔ offene Punkte in `features/*/{discovery,spec,plan}.md`; beantwortete Fragen zuordnen/nachtragen, unbeantwortete/neue Punkte sichtbar machen."
**Status:** In Bearbeitung

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-<neuer-slug>/SKILL.md | Neuer Skill (falls Träger = eigener Skill; Träger-Frage offen) |
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

**Beleg-Datei (Block 3 — VORSCHLAG, noch nicht bestaetigt):**
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
- [ausstehend — 3d]

### Integrationspunkte
- [ausstehend — 3e]

---

## Abhaengigkeiten

- [ausstehend — Schritt 4]

---

## Offene Punkte

- 3c Block 3 (Beleg-Datei): Vorschlag liegt vor (siehe Randfaelle), Bestaetigung des
  Ablage-Orts `project-meetings/` steht aus
- Kategorien 3d (Einschraenkungen) und 3e (Integrationspunkte) sowie Schritt 4
  (Abhaengigkeits-Check), Schritt 5 (Name/Slug final) noch offen

---

**Erstellt mit:** `/dtb:feature-discover`
