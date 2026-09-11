# Discovery: Output-Style „gezielt"
<!-- resume: done -->

**Erstellt:** 2026-08-07
**Idee-Referenz:** Inbox #40 — "Formulierung/Sprachstil von Claude anpassen: Ausgaben sparsam, fokussiert, nur das Noetige — Praezisierung bei Bedarf durch Nachhaken statt praeventiver Ausfuehrlichkeit"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `output-styles/` | **Neu** — Quellverzeichnis im Kit-Repo fuer die Style-Datei (versioniert, Review-faehig) |
| `skills/dtb-kit-sync/SKILL.md` | Klassen-Tabelle um `output-styles/*.md` als Klasse A erweitern (Verteilung nach `~/.claude/output-styles/`, Hash im Lock, Drei-Punkte-Drift) |
| `skills/CLAUDE.md` | Abschnitt `## Distribution (kit-sync)` Z. 214 listet die Klasse-A-Muster — muss die neue Klasse mitfuehren; ausserdem fehlt dort bis heute ein Output-/Stil-Abschnitt (Platz neben `## Language`, Z. 224) |
| `skills/dtb-project-health/SKILL.md` | Neuer Check „Style installiert, aber nicht aktiviert" (Randfall 2) |
| `CLAUDE.md` (Root) | Beschreibt das Distributionsmodell und die Artefakt-Klassen — zieht nach |

**Bewusst NICHT betroffen** (im Verlauf der Discovery ausgeschieden):
`settings.json` (Kit-Seed), `skills/dtb-project-init/SKILL.md`, ein `hooks/`-Verzeichnis — der
Hook-Weg entfiel mit der Entscheidung „global statt nur im Workflow". Ebenso die 39 `SKILL.md`
mit ihren Report-Laengen (Ebene a, s. u.).

---

## Anforderungen

### Scope

**Enthalten:**
- Eine **globale, workflow-uebergreifende** Stil-Anweisung fuer Claudes Fliesstext (Ebene b) —
  alles, was ausserhalb der Skill-Report-Vorlagen geschrieben wird: Erklaerungen, Begruendungen,
  Zwischenkommentare, Einschaetzungen
- Auslieferung als **Kit-Artefakt** (Klasse A) statt als lokale Config: Quelle im Repo, Verteilung
  via `dtb:kit-sync` nach `~/.claude/output-styles/` — versioniert, erreicht beide Maschinen
- **Ein-/ausschaltbar** ueber das `outputStyle`-Feld
- Erkennungsmerkmal (Nutzer-Formulierung 2026-08-07, „gezielt" statt „sparsam"):
  > Jeder Ausgabe muss auf einen Blick zu entnehmen sein: **worum es geht**, **was der Stand bzw.
  > das Problem ist**, und **welche Entscheidung verlangt wird**. Erklaerungen dazu kurz, knapp,
  > einfach — reduziert auf das Wichtigste, nicht weggelassen.
  Der Gegner ist **Vorwegnahme und Redundanz**, nicht Erklaerung. Struktur (Tabellen, Listen)
  bleibt ausdruecklich erlaubt, weil sie der Uebersicht dient

**Nicht enthalten:**
- **Ebene (a)** — die Report-Laengen der Skills vereinheitlichen (25 von 39 Skills tragen heute
  eine Vorgabe, mit sechs verschiedenen Zahlen: 12/15/40/60/60-80/80; 14 ohne, darunter
  `feature-discover`, `feature-plan`, `idea-review`, `docs-extract`). Eigener Zuschnitt
- **Subagents** — Output Styles wirken laut Doku nur in der Hauptkonversation; Sub-Agents laufen
  mit eigenem System-Prompt. `impl-review` und `plan-review` bleiben also unbeeinflusst
- Kein Eingriff in die Sprache (Deutsch bleibt), kein Kuerzen von Belegen, Zahlen oder Substanz
- Kein Schreibzugriff auf Zielprojekte — nichts landet in `dtb-project/` oder einer Projekt-`.claude/`

### Gewuenschtes Verhalten
- Wirkung erst nach `/clear` oder in einer neuen Session (System-Prompt wird bei Session-Start
  gelesen) — **vom Nutzer als in Ordnung bestaetigt**, keine Sofort-Wirkung noetig
- Kein bestehendes Kit-Muster als Vorlage — die Style-Datei wird frei formuliert (Nutzer-Entscheid)

### Randfaelle
1. **Aufgaben, die Ausfuehrlichkeit brauchen** (Analyse, Review, Fehlersuche): Die Style-Datei
   traegt eine Ausnahme-Klausel — *„wenn ausdruecklich um Analyse, Begruendung oder Vergleich
   gebeten wird, gilt die Beschraenkung nicht"*. Bewusst in der Datei statt per Umschalten, weil
   ein Wechsel ein `/clear` kostet und mitten in der Arbeit trifft
2. **Zweite Maschine:** `kit-sync` bringt die Datei, der Schalter (`outputStyle` in
   `~/.claude/settings.json`) reist **nicht** mit — die Datei laege inaktiv herum. Gegenmittel:
   `dtb:project-health` bekommt einen Check „Style installiert, aber nicht aktiviert".
   Ohne den waere es das #34-Muster (stiller Zwei-Maschinen-Drift)
3. **Projekt schlaegt User:** Traegt ein Projekt in `.claude/settings.local.json` einen eigenen
   `outputStyle`, gewinnt der gegen die globale Einstellung. Als bekannte Einschraenkung
   dokumentieren, **nicht** bekaempfen — das ist gewollte Settings-Praezedenz von Claude Code

### Einschraenkungen
- **Vorrang-Regel:** Gibt ein Skill ein Ausgabeformat vor, gilt das Format; der Stil wirkt nur auf
  den Text drumherum. Sonst beschneidet der Stil bewusst gesetzte Report-Strukturen
- **Laenge:** Obergrenze ~40 Zeilen. Die Datei geht in jeden System-Prompt jeder Session;
  Prompt-Caching mildert das erst nach der ersten Anfrage. Eine ausufernde Stil-Anweisung waere
  zudem inhaltlich unglaubwuerdig
- **`keep-coding-instructions: true` ist Pflicht** — Default ist `false`, ohne das Feld entfallen
  Claude Codes eingebaute Software-Engineering-Instruktionen komplett
- **Sprache der Datei: Deutsch** (Annahme 2026-08-07, nicht ausdruecklich bestaetigt) — Kit-Konvention
  fuer Bodies; die Antwortsprache steuert ohnehin das `language`-Setting

### Integrationspunkte
- **`kit-sync` bekommt die neue Klasse als Muster**, nicht als Einzeleintrag: `output-styles/*.md`
  → `~/.claude/output-styles/`. Analog zu `skills/dtb-*/SKILL.md` (`skills/CLAUDE.md` Z. 215:
  „a NEW skill is covered automatically by the pattern, no registration needed") — ein zweiter
  Style spaeter braucht dann keine Aenderung an `kit-sync`
- **`project-health`** bekommt den Check aus Randfall 2 („Style installiert, aber nicht aktiviert")
- **Praezedenz bewusst begrenzt (Nutzer-Entscheid 2026-08-07):** Dieses Feature beantwortet die
  Frage „Kit-Baustein oder lokale Config?" **nur fuer Output Styles**. Es ist ausdruecklich
  KEIN Praejudiz fuer **#41** (TTS, laeuft heute als ungetrackter Stop-Hook) oder **#45**
  (Hooks im Kit) — diese bleiben eigenstaendig zu entscheiden
- **#45 ist mit diesem Zuschnitt KEINE Vorbedingung mehr.** Der `UserPromptSubmit`-Hook war nur
  noetig, um „nur waehrend `/dtb:*`" zu erreichen; mit der Entscheidung fuer
  workflow-uebergreifende Geltung entfaellt die Bedingung und damit die Hook-Frage
- **Keine externen Abhaengigkeiten** ausser Claude Code selbst

---

## Verifizierte Mechanik (Quelle: offizielle Doku, abgerufen 2026-08-07)

| Punkt | Befund |
|-------|--------|
| Speicherorte | User: `~/.claude/output-styles/` · Projekt: `.claude/output-styles/` · Managed Policy |
| Format | Markdown mit Frontmatter (`name`, `description`, `keep-coding-instructions`, `force-for-plugin`) |
| Umschaltung | `/config` → *Output style*, **oder** `outputStyle`-Feld direkt in einer Settings-Datei |
| ⚠ `/output-style` | **Entfernt** — deprecated v2.1.73, removed v2.1.91. Nicht mehr verwenden |
| ⚠ Menue-Auswahl | `/config` speichert nach `.claude/settings.local.json` — **projektlokal**. Fuer globale Geltung muss `outputStyle` in `~/.claude/settings.json` stehen (einmal pro Maschine, von Hand) |
| Wirkung | Erst nach `/clear` bzw. neuer Session; gilt nur fuer die Hauptkonversation, nicht fuer Subagents |
| Token | Erhoeht Input-Tokens; Prompt-Caching senkt die Kosten ab der zweiten Anfrage einer Session |
| Plugins | Koennen Output Styles in einem `output-styles/`-Verzeichnis mitliefern (alternativer Verteilungsweg, hier nicht gewaehlt) |

**Zustand dieser Maschine (2026-08-07):** `~/.claude/output-styles/` existiert nicht,
`outputStyle` ist in `~/.claude/settings.json` nicht gesetzt, `~/.claude/CLAUDE.md` existiert nicht.

---

## Abhaengigkeiten

**Konflikte:** keine.

**Ueberschneidung (1):** `gitattributes-eol` (Task, offen) — dessen Renormalisierung aendert
Content-Hashes der Klasse-A-Dateien (`task.md` Z. 32) und traefe damit auch `output-styles/*.md`.
Entschaerft, weil `kit-sync` beim Hashing Zeilenenden normalisiert (`skills/CLAUDE.md` Z. 212);
die Reihenfolge beider Vorgaenge ist damit gleichgueltig.

**Struktureller Hinweis fuer `plan-review`:** Alle vier aktiven Features nutzen `kit-sync`
ausschliesslich als **Konsument** („Klasse-A-Muster erfasst den neuen Skill automatisch" —
`feature-fast/plan.md:192`, `meeting-agenda/plan.md:97`). Dieses Feature ist das **erste, das die
Klassen-Tabelle selbst erweitert**. Dafuer gibt es im Bestand keinen Praezedenzfall, entsprechend
sorgfaeltig ist die Spiegel-Kopplung zu pruefen: `kit-sync` (Tabelle + Lock-Schema),
`skills/CLAUDE.md` Z. 214 (Klasse-A-Muster) und Root-`CLAUDE.md` (Distributionsmodell) muessen
gemeinsam gezogen werden.

---

## Offene Punkte

- Sprache der Style-Datei: Deutsch angenommen, nicht ausdruecklich bestaetigt
- `kit-sync`: Verhalten bestehender Locks, die `output-styles/` noch nicht kennen (erwartet:
  Eintrag wird beim naechsten `sync` als neu erkannt und installiert — in `impl-plan` pruefen)

---

**Erstellt mit:** `/dtb:feature-discover`
