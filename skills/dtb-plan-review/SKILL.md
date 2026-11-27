---
name: dtb:plan-review
description: >-
  Use when: "Plan Review", "Implementierungsplan reviewen", "Plan bewerten",
  "Plan pruefen". Conducts a structured review of an implementation plan
  with three agent perspectives (Architekt, Pragmatiker, Senior Dev), each run
  as an isolated parallel subagent that never sees the other roles' findings.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent
argument-hint: "[Feature-Name]"
pipeline:
  stage: planning
  after: [dtb:impl-plan, dtb:feature-fast, dtb:feature-plan]
  next: [dtb:implement]
  consumes: [features/*/plan.md, features/*/spec.md, agents/*.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md, workflow.config.yaml]
  produces: [features/*/plan.md]
---

# Plan Review Discussion

Du fuehrst ein strukturiertes Review eines Implementierungsplans durch. Drei Rollen (Architekt, Pragmatiker und Senior Dev) reviewen den Plan — jede in einem eigenen, isolierten Subagenten, ohne die Befunde der anderen zu kennen (Schritt 3) — und stellen Damian als Product Owner gezielte Fragen. Du fuehrst Vorpruefungen und Zusammenfuehrung aus, nicht die Rollen selbst. Bei Ops-/Security-Bezug kommt eine vierte Rolle (Betriebs-Waechter) hinzu — Aktivierung siehe Schritt 2c.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

**Modell je Rolle (optional):** Lies den Block `plan_review.modelle` — Schluessel `architekt`,
`pragmatiker`, `senior-dev`, `betriebs-waechter`; Wert = ein Modellname, den das Agent-Werkzeug
fuer seinen Parameter `model` anbietet, oder `null`. Fehlt der Block oder der Schluessel, oder ist
der Wert `null` → die Rolle erbt das Modell der Session (kein Hinweis). Unbekannter Wert (vom
Agent-Werkzeug nicht angeboten) oder unbekannter Schluessel → erben und genau eine Zeile je Fall:
`⚠ plan_review.modelle.{schluessel}: „{wert}" unbekannt — Rolle erbt das Session-Modell`

## Schritt 1: Plan und Feature-Spec laden

1. **Feature ermitteln:** Frage den Benutzer nach dem Feature-Namen/Slug, falls nicht aus dem Chat-Kontext erkennbar
2. **Plan lesen:** Lies `{config.paths.workflows}/features/{slug}/plan.md`
   - **Formal-Check `## Progress`:** Der Plan muss eine `## Progress`-Sektion haben —
     genau eine Checkbox-Zeile pro Schritt N.M, Format gemaess
     `{config.paths.rules}/DERIVED_STATE_RULES.md` §2. Fehlt die Sektion oder weicht
     die Nummerierung von den Plan-Schritten ab → als Finding in Runde 2 aufnehmen
     (der Umsetzungsstand waere sonst nicht ableitbar)
3. **Feature-Spec lesen:** Lies `{config.paths.workflows}/features/{slug}/spec.md` als zusaetzlichen Kontext

**Eligibility-Gate (Fit-Check):** Fehlt `plan.md` → Hard-Gate greift (Konvention:
`skills/CLAUDE.md` → „Eligibility-Gates"). Gib den Meldeblock aus und arbeite NICHT weiter, bis
der Nutzer die Escape-Hatch bestaetigt:

```
⛔ plan-review braucht einen Implementierungsplan, der fehlt.
   Geprueft: features/{slug}/plan.md — nicht gefunden.
   → Erstelle ihn zuerst: /dtb:impl-plan {Feature-Name}   (Erzeuger; auch via /dtb:feature-plan oder /dtb:feature-fast)

   Fehlalarm (plan.md existiert doch) oder bewusst ohne fortfahren? „trotzdem fortfahren" bestaetigen.
```

Bei Bestaetigung: normal fortfahren. Sonst: hier stoppen (kein Review ohne Plan).

## Schritt 2: Agent-Definitionen laden

Lies die Agenten-Definitionen — bevorzugt aus der globalen Installation `~/.claude/agents/`,
mit Fallback auf den Projekt-Root `agents/`. Die Kit-Distribution installiert die Agenten global
(`dtb:kit-sync`); Zielprojekte haben i.d.R. keinen eigenen `agents/`-Ordner:
- `architekt.md`
- `pragmatiker.md`
- `senior-dev.md`
- `betriebs-waechter.md` — nur laden, wenn in Schritt 2c aktiviert

Aufloesung je Datei: zuerst `~/.claude/agents/{name}.md`, sonst `agents/{name}.md` (Projekt-Root).
Fehlt eine Rollen-Datei in **beiden** Quellen → melde
`⚠ Agenten-Definition {name}.md weder global (~/.claude/agents/) noch im Projekt (agents/) gefunden — /dtb:kit-sync ausfuehren`
und fahre mit den gefundenen Rollen fort (die 3 Kern-Agenten sind Minimum).

Halte den vollstaendigen Text jeder gefundenen Rollen-Datei bereit — er ist das Prompt-Material
der Rollen-Subagenten in Schritt 3. Du nimmst die Rollen NICHT selbst ein (einzige Ausnahme: der
Rueckfall in Schritt 3c).

## Schritt 2b: Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `plan-review` oder `alle` enthaelt
- Die Rollen lesen die Datei in Schritt 3 selbst (Pfad + diese Filterregel im Auftrag) und beruecksichtigen die passenden `Rule`-Aussagen still — du gibst sie NICHT als Text weiter und triffst keine Vorauswahl je Rolle (das wuerde jede Rolle durch deinen Kontext vorpraegen)
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei nach dem Filter behaltene Lektionen mit gegensaetzlicher `Rule` — z.B. „immer X" vs. „nie X" zum selben Gegenstand):
  beide zeigen und den Widerspruch melden — nicht selbst aufloesen

## Schritt 2c: Betriebs-Waechter-Relevanz pruefen

Pruefe anhand von Plan und Feature-Spec, ob der Plan mindestens einen dieser Trigger beruehrt:

- Deployment / Rollout / Infrastruktur-Aenderung
- Datenverarbeitung oder -speicherung (v.a. sensible/personenbezogene Daten, neues Logging)
- Externe Angriffsflaeche (oeffentliche Endpunkte, Input von aussen, Auth/Authz)
- Betriebskritischer Pfad / last- oder performance-relevant
- Secrets / Config / Berechtigungen

- **Mindestens ein Trigger** → `betriebs-waechter.md` laden (global `~/.claude/agents/` mit
  Projekt-Root-`agents/`-Fallback wie Schritt 2); die Rolle bekommt in Schritt 3
  einen eigenen, vierten Subagenten. Gib aus: `🔧 Betriebs-Waechter aktiviert: {Trigger-Grund}`
- **Kein Trigger** → Agent nicht laden, Ensemble bleibt bei drei Stimmen. Gib aus:
  `🔧 Betriebs-Waechter nicht aktiviert (kein Ops-/Security-Bezug im Plan)`

## Schritt 2d: Grounding (Codebase-Behauptungen verifizieren)

Extrahiere aus dem Plan alle eindeutig pruefbaren Codebase-Referenzen:
- Datei-Pfade (z.B. `skills/x/SKILL.md`, `agents/foo.md`)
- Benannte Funktionen/Sektionen in konkreten Dateien (z.B. "Schritt 2c in SKILL.md", "`## Progress` in plan.md")
- Struktur-Behauptungen ("Verzeichnis X enthaelt Y")

Nicht gierig extrahieren: Prosa ohne konkreten Datei-Bezug ist KEINE Referenz ("wir erweitern
das Review-Konzept" ist nichts Pruefbares). Verifiziere jede Referenz per Glob/Grep.

Ausgabe (genau eine Variante):
- Alle gefunden → `🔎 Grounding: {N} Referenzen geprueft, alle gefunden`
- Abweichungen → pro Abweichung eine Zeile `⚠ Plan referenziert {X} — nicht gefunden`, dazu
  fuer den Rest genau eine Zeile `🔎 Grounding: {M} weitere Referenzen geprueft, alle gefunden`
- Keine pruefbaren Referenzen → `🔎 Grounding: keine pruefbaren Referenzen` (kein Fehler, weiter)

Unsichere Checks (dynamische/implizite Referenzen, Mehrdeutigkeiten) nur als Hinweis ausgeben —
sie duerfen NIE ein FAIL-Verdikt treiben. Alle Abweichungen fliessen als Input in Runde 2.

## Schritt 2e: Challenger-Pass (mechanische Konsistenz)

Pruefe den Plan mechanisch auf Konsistenz — das ist KEINE Perspektiv-Kritik (die leistet
Runde 3), sondern Text-gegen-Text-Pruefung:

1. **Promise-Gaps:** Jede Zusage im Plan (Deliverables, Checkpoint-Kriterien, "wird ergaenzt"-
   Aussagen) muss einem Schritt N.M zuordenbar sein, der sie liefert. Zusage ohne liefernden
   Schritt = Promise-Gap
2. **Widersprueche:** Schritte, die sich gegenseitig aufheben, dieselbe Datei inkompatibel
   aendern oder gegensaetzliche Entscheidungen kodieren

Ausgabe: Kopfzeile `⚔ Challenger-Pass: {N} Befund(e)`, darunter nummerierte Liste (`1. {Befund}`);
keine Befunde → nur `⚔ Challenger-Pass: keine Widersprueche oder Promise-Gaps`.
Befunde fliessen als Input in Runde 2.

## Schritt 3: Rollen-Laeufe (isolierte Subagenten)

Jede aktive Rolle urteilt in einem **eigenen Subagenten** und sieht die Rueckgabe keiner anderen
Rolle. Grund: Spielt ein Modell alle Rollen im selben Kontext, hat die zweite Stimme die erste
schon gelesen, und die Perspektiven verschmelzen. Du fuehrst nur Vorarbeit (Schritte 0–2e) und
Zusammenfuehrung (3d, Schritt 4) aus — die vier Runden schreiben die Rollen.

**Rollen-Tabelle** (Runden-Fokus, Challenge-Technik und Dimensionen je Rolle):

| Rolle | Datei | Runde 1 — Staerken | Runde 2 — Bedenken & Risiken | Runde 3 — Challenge (Technik: Leitfrage) | Dimensionen |
|-------|-------|--------------------|------------------------------|------------------------------------------|-------------|
| 🏗️ Architekt | `architekt.md` | Systemdesign | technische Risiken und Abhaengigkeiten | Pre-Mortem: „Angenommen das Feature ist gescheitert. Was war die wahrscheinlichste Ursache?" | Technische Machbarkeit, Abhaengigkeiten |
| ⚡ Pragmatiker | `pragmatiker.md` | Scope und Spec-Deckung | Scope-Creep, Aufwand-Nutzen, Spec-Deckung — deckt der Plan die Feature-Spec vollstaendig ab, ohne darueber hinauszugehen | Devil's Advocate: „Was spricht GEGEN diesen Plan? Welche einfachere Alternative wurde uebersehen?" | Scope/MVP-Schnitt, Spec-Deckung |
| 💻 Senior Dev | `senior-dev.md` | Umsetzbarkeit | unrealistische Zeitschaetzungen und fehlende Implementierungsschritte | Unknown Unknowns: „Was wissen wir NICHT, das uns spaeter ueberraschen koennte?" | Reihenfolge der Phasen, Zeitschaetzungen, Teststrategie |
| 🔧 Betriebs-Waechter (nur falls aktiviert) | `betriebs-waechter.md` | Betrieb & Haertung | Betriebs-, Deployment- und Sicherheitsrisiken | Adversarielles Day-2-Szenario: „Es ist 3 Uhr nachts und das System verhaelt sich falsch: sehen wir es und koennen wir es stoppen? Und wie wuerde ein Angreifer genau diese Aenderung ausnutzen?" | Betrieb & Haertung |

### 3a: Dispatch

Starte je aktiver Rolle **einen** Sub-Agent (Typ `general-purpose`) — alle in **EINER**
Nachricht, damit sie parallel laufen. Parameter `model` = Wert aus Schritt 0; erbt die Rolle,
den Parameter weglassen. Plan und Spec liest der Subagent selbst — nicht in den Prompt kopieren.

Auftragsvorlage (je Rolle aus Rollen-Datei und Rollen-Tabelle fuellen):

```
Du bist die Rolle „{Rolle}" in einem Plan-Review. Deine Rollendefinition:

{vollstaendiger Text der Rollen-Datei aus Schritt 2}

Nur lesen — keine Datei schreiben oder aendern, keine Kommandos ausfuehren. Andere Rollen
reviewen denselben Plan getrennt von dir; ihre Befunde kennst du nicht, nimm sie nicht vorweg.

Lies:
- Implementierungsplan: {absoluter Pfad zu features/{slug}/plan.md}
- Feature-Spec: {absoluter Pfad zu features/{slug}/spec.md | „keine Spec vorhanden" — dann
  Spec-Deckung nur gegen die planinternen Zusagen pruefen}

Vorpruefungen des Skills (Input fuer deine Runde 2 — aufgreifen, soweit deine Perspektive
betroffen ist):
- Formal-Check `## Progress`: {ok | Befund aus Schritt 1}
- Grounding: {Ergebniszeile(n) aus Schritt 2d}
- Challenger-Pass: {Ergebnis aus Schritt 2e}

Lektionen (still beruecksichtigen): Lies {absoluter Pfad zu lessons.md} und beachte die
`Rule`-Spalte aller Zeilen, deren `Applies-to` `plan-review` oder `alle` enthaelt
{| „keine" — wenn Schritt 2b uebersprungen wurde}

Arbeite aus deiner Perspektive in vier Runden, konkret mit Bezug auf diesen Plan:
1. Staerken: {Runde-1-Fokus}
2. Bedenken & Risiken: {Runde-2-Fokus}
3. Challenge — {Technik}: {Leitfrage}
4. Fragen an Damian: hoechstens 3, nur Fragen, deren Antwort den Plan aendert

Erst NACH Runde 3 vergibst du Verdikte — nur fuer deine Dimensionen ({Dimensionen}), je
PASS (keine Bedenken) / WARN (Problem vorhanden, im Plan behebbar) / FAIL (nicht tragfaehig,
muss neu gedacht werden), keine Zwischenstufen. Ein Problem in einer fremden Dimension meldest
du als Einspruch, nie als Verdikt.

Rueckgabe exakt in diesem Format (Deutsch):
RUNDE 1: {Text}
RUNDE 2: {Text}
RUNDE 3: {Text}
RUNDE 4: {je Zeile eine Frage}
VERDIKT {Dimension}: {PASS|WARN|FAIL} — {1 Satz}    (genau eine Zeile je eigene Dimension)
EINSPRUCH {fremde Dimension}: {1 Satz}               (optional)
EMPFEHLUNG: {konkrete Plan-Aenderung}                (je WARN/FAIL mindestens eine)
```

### 3b: Warte-Regel

Die Subagenten laufen im Hintergrund und melden sich einzeln. Warte, bis **alle M** Rueckgaben
eingetroffen sind, bevor du zusammenfuehrst. Eine noch laufende Rolle wird
nie aus dem Hauptkontext gefuellt oder vorweggenommen — auch nicht teilweise. N in
`🤖 Subagenten: {N}/{M} Rollen isoliert` zaehlt nur Rollen, deren verwertbare Rueckgabe
tatsaechlich vom Subagenten kam.

### 3c: Rueckgabe-Pruefung und Rueckfall

Das Review bricht nie ab — ein Ausfall faellt sichtbar auf den bisherigen Ablauf zurueck:

- **Agent-Werkzeug nicht verfuegbar** (Aufruf abgelehnt oder nicht angeboten) → alle Rollen im
  Hauptkontext nach der Rollen-Tabelle (bisheriger Ablauf), N = 0, genau eine Zeile
  `⚠ Agent-Werkzeug nicht verfuegbar — alle Rollen im Hauptkontext (nicht isoliert)`
- **Einzelne Rueckgabe fehlgeschlagen oder unbrauchbar** — Fehlermeldung statt Ergebnis, eine
  eigene Dimension ohne `VERDIKT`-Zeile, ein Verdikt fuer eine fremde Dimension, ein Wert
  ausser PASS/WARN/FAIL → diese Rolle im Hauptkontext nachholen (Verdikt erst nach ihrer
  Runde 3), Zeile `⚠ Rolle {Rolle} im Hauptkontext ({Grund})`
- **Verwertbar trotz Formabweichung** (kein Rueckfall): identisch doppelte Zeilen (einmal
  uebernehmen) und eine abweichende Reihenfolge der Abschnitte. Widersprechen sich zwei
  `VERDIKT`-Zeilen derselben Dimension → unbrauchbar (Rueckfall wie oben)
- Eine nachgeholte Rolle zaehlt nicht in N

### 3d: Zusammenfuehrung

- `RUNDE`-Texte je Rolle inhaltlich unveraendert in die Runden-Abschnitte des Output-Formats
  setzen — du fuegst den Runden keine eigenen Befunde hinzu und streichst keine Aussage
- `VERDIKT`-Zeilen → Review-Zusammenfassung (Schritt 4); `EINSPRUCH`-Zeilen → Einspruchs-Regel
  (Schritt 4)
- `EMPFEHLUNG`-Zeilen aller Rollen → `## Empfehlungen`; gleiche Empfehlungen mehrerer Rollen
  erst hier zu einer zusammenfassen, Herkunft in Klammern (`(Architekt, Senior Dev)`)

## Schritt 4: Zusammenfassung mit Verdikt

Erstelle die Verdikt-Liste und die Empfehlungen aus den Rueckgaben (3d). Verdikte werden nie
innerhalb der Runden 1-4 vergeben (fruehe Verdikte nageln eine Rolle vor ihrer Challenge-Runde
fest): Jede Rolle vergibt sie in ihrem Subagenten erst nach ihrer eigenen Runde 3; fuer eine
nachgeholte Rolle (3c) gilt dasselbe im Hauptkontext. Fuer eine Rolle, die isoliert geliefert
hat, vergibst du kein Verdikt. Jede Rolle bewertet NUR ihre eigenen Dimensionen:

| Agent | Dimensionen |
|-------|-------------|
| Architekt | Technische Machbarkeit, Abhaengigkeiten |
| Pragmatiker | Scope/MVP-Schnitt, Spec-Deckung |
| Senior Dev | Reihenfolge der Phasen, Zeitschaetzungen, Teststrategie |
| Betriebs-Waechter (nur falls aktiviert) | Betrieb & Haertung |

**Verdikt-Semantik:** PASS = keine Bedenken; WARN = Problem vorhanden, im Plan behebbar;
FAIL = Dimension nicht tragfaehig, Plan muss in diesem Punkt neu gedacht werden.

Fehlt die Feature-Spec (Altbestand, Fixture): Dimension **Spec-Deckung** nur gegen die
planinternen Zusagen pruefen (Deliverables, Checkpoint-Kriterien) und in der Anmerkung
`keine Spec vorhanden` vermerken.

**Einspruchs-Regel:** Sieht eine Rolle ein Problem in einer fremden Dimension, liefert sie eine
`EINSPRUCH`-Zeile; uebernimm sie unter der Liste als `Einspruch {Rolle} zu {Dimension}: {1 Satz}`.
Die Reaktion schreibst du als Haupt-Skill in einem Satz, gekennzeichnet:
`Reaktion (Haupt-Skill, {zustaendige Rolle}): {bestaetigt|entkraeftet} — {1 Satz}`. Stuetze sie
auf die Rueckgabe der zustaendigen Rolle (deckt deren Runde 2 oder 3 den Punkt ab oder
widerlegt ihn?) — keine neue Argumentation in deren Namen. Ein bestaetigter Einspruch zaehlt
wie WARN der Dimension — bei belegtem schwerwiegendem Fall wie FAIL. Nennt eine
`EINSPRUCH`-Zeile keine Dimension aus der Tabelle oben, wird sie zu `Hinweis {Rolle}: {1 Satz}`
unter der Liste — ohne Reaktion und ohne Wirkung auf ein Verdikt.

**Gesamt-Verdikt (feste Regel — nie aufweichen, keine Zwischenstufen):**
- alle Dimensionen PASS → **SOUND**
- mindestens ein WARN, kein FAIL → **REVISE**
- mindestens ein FAIL → **RETHINK**

## Schritt 5: Anpassungen anbieten

Abhaengig vom Gesamt-Verdikt:

- **REVISE oder RETHINK → keine Ja/Nein-Frage.** Bei negativem Verdikt ist das „Ja" gesetzt
  (0 „Nein" in 26 realen Laeufen). Der Report endet mit der Anzeige-Zeile
  `→ Verdikt {REVISE|RETHINK}: direkt in die Finding-Runde` und es geht sofort weiter: die
  Empfehlungen einzeln vorschlagen, der Mensch nimmt je Empfehlung an, aendert ab oder lehnt
  ab. **Die Finding-Entscheidungen selbst bleiben einzeln beim Menschen** (sie legen Scope fest);
  Ablehnen oder Vertagen ist jederzeit moeglich und fuehrt in Schritt 6 zu „Findings offen".
- **SOUND → Frage bleibt:** „Moechtest du Anpassungen am Implementierungsplan vornehmen?
  (Ja/Nein)" — ohne WARN ist sie eine echte Wahl.

(Form-Kanon fuer Autoren: `skills/CLAUDE.md` → „Rueckfragen-Defaults (Veto-Form)", Zeile Z7.)

## Schritt 6: Kopf-Statusfeld setzen (Pfleger-Pflicht)

Dieser Skill ist der **einzige Pfleger** des `plan.md`-Kopf-Statusfelds
(Kanon: `{config.paths.rules}/DERIVED_STATE_RULES.md` §7). Der Schritt laeuft **immer** — auch
bei negativem Verdikt und auch dann, wenn in Schritt 5 keine Anpassung gewuenscht war. Ein
Review, das das Feld nicht anfasst, laesst es stillschweigend veralten; genau das ist der
Grund fuer die Pfleger-Regel.

**Still schreiben, nicht nachfragen:** Kein Bestaetigungs-Dialog — eine versionierte Zeile im
eigenen Arbeitsbaum ist trivial rueckholbar, und eine Pflicht-Interaktion an dieser Stelle
waere Reibung ohne Schutzwert. Die Aenderung wird stattdessen im Report ausgewiesen (unten).

### 6.1 Wert bestimmen (Wertematrix)

> **Wartungs-Hinweis (Format-Kopplung):** Diese Matrix ist woertlich gespiegelt in
> `DERIVED_STATE_RULES.md` §7.2. Die Kopie ist Absicht — die Regel-Datei ist Klasse-B-Seed und
> erreicht Bestandsprojekte nicht automatisch (INBOX #22), dieser Skill muss autark bleiben.
> Aenderst du die Matrix hier, ziehe §7.2 mit; der Gegen-Hinweis steht dort.

| Ausgang | Neuer Feldwert |
|---------|----------------|
| Gesamt-Verdikt SOUND | `Reviewed (plan-review {YYYY-MM-DD}: SOUND)` |
| REVISE, Findings in Schritt 5 vollstaendig eingearbeitet | `Reviewed (plan-review {YYYY-MM-DD}: REVISE → {N} WARNs behoben)` |
| REVISE, Findings offen (abgelehnt, vertagt oder nur teilweise uebernommen) | `Entwurf (plan-review {YYYY-MM-DD}: REVISE — Findings offen)` |
| Gesamt-Verdikt RETHINK | `Entwurf (plan-review {YYYY-MM-DD}: RETHINK)` |

**Harte „behoben"-Bedingung (binaer, kein Ermessen):** `Reviewed` nur, wenn **alle**
WARN-getriebenen Anpassungen tatsaechlich in `plan.md` geschrieben wurden. Teilannahme,
Vertagung oder Ablehnung ergeben `Entwurf (… Findings offen)`. Grund (asymmetrisches Risiko):
`Reviewed` schaltet in `dtb:workflow-next` „Start ausstehend" frei — ein zu frueh gesetztes
`Reviewed` schickt jemanden mit bekannten, unbehobenen Schwaechen in die Umsetzung; der
umgekehrte Fehler kostet nur einen weiteren, billigen Review-Lauf.

### 6.2 Zielzeile finden und schreiben (Randfaelle)

1. **Nur im Definitionsfenster suchen:** Die Zielzeile ist die erste `**Status:**`-Zeile
   **innerhalb der ersten 10 Zeilen** von `plan.md` (§7.1). `**Status:**`-Zeilen ausserhalb
   dieses Fensters bleiben **unangetastet** — sie sind kein Kopf-Statusfeld (schuetzt zitierte
   Bloecke, Template-Beispiele und Phasen-Tabellen im Fliesstext).
2. **Fehlt die Zeile im Fenster:** an der Kopfposition einfuegen — direkt unter
   `**Geschaetzte Dauer:**` bzw., falls es die Zeile nicht gibt, als letzte Zeile des
   Kopfblocks vor dem ersten `---`. Damit heilt der Pfleger nebenbei Plaene ohne Feld.
   **Fenster-Grenze (verbindlich):** Die eingefuegte Zeile muss selbst **innerhalb der ersten
   10 Zeilen** liegen. Laege die Kopfposition darunter (langer Kopfblock), stattdessen direkt
   nach der Titelzeile einfuegen — sonst waere die neue Zeile per §7.1 kein Kopf-Statusfeld,
   kein Leser saehe sie, und der naechste Lauf fuegte eine zweite ein.
3. **Altwerte normalisieren:** Traegt die Zeile einen abgeschafften Wert (Umsetzungs- oder
   Abschluss-Stufe) oder einen unbekannten Wert, wird sie durch den Wert aus 6.1 **ersetzt** —
   kein Anhaengen, keine zweite Statuszeile.
4. **Genau eine Zeile aendern** (Edit), sonst nichts am Plan.

### 6.3 Im Report ausweisen

Nach der Anpassungs-Runde aus Schritt 5 — und erst dann — wird genau eine zusaetzliche Zeile
ausgegeben: `📝 Kopf-Statusfeld → {neuer Wert}`. Sie steht **ausserhalb** des Output-Blocks
unten (dessen letzte Zeile die Anpassungs-Frage bzw. der Uebergang in die Finding-Runde ist), macht die stille
Aenderung sichtbar und belegt, dass der Pfleger gelaufen ist.

---

## Output-Format

Gib die Diskussion in folgendem Format aus:

```markdown
# Plan Review: [Feature-Name]
**Datum:** [YYYY-MM-DD]
**Implementierungsplan:** `features/{slug}/plan.md`
**Feature-Spec:** `features/{slug}/spec.md`

[📚-Zeile aus Schritt 2b, falls Lektionen beruecksichtigt]
[🔧-Zeile aus Schritt 2c]
🤖 Subagenten: {N}/{M} Rollen isoliert
[⚠-Zeilen aus Schritt 0 (Modellwerte) und Schritt 3c (Rueckfall), je Fall eine]
🔎 Grounding: [Ergebniszeile(n) aus Schritt 2d]
⚔ Challenger-Pass: [Ergebniszeile oder Kopfzeile + nummerierte Befunde aus Schritt 2e]

---

## Runde 1: Staerken des Implementierungsplans

**🏗️ Architekt:** "[Einschaetzung zu Systemdesign, technischen Entscheidungen, Abhaengigkeiten]"

**⚡ Pragmatiker:** "[Einschaetzung zu Scope, Ergebnisorientierung, Priorisierung]"

**💻 Senior Dev:** "[Einschaetzung zu Umsetzbarkeit, Schrittfolge, Zeitschaetzungen]"

**🔧 Betriebs-Waechter (falls aktiviert):** "[Einschaetzung zu Deployment, Observability, Haertung]"

---

## Runde 2: Bedenken & Risiken

**🏗️ Architekt:** "[Technische Risiken, Systemgrenzen, Abhaengigkeiten]"

**⚡ Pragmatiker:** "[Aufwand-Nutzen-Probleme, Scope-Creep, Spec-Deckung, Priorisierung]"

**💻 Senior Dev:** "[Unrealistische Zeitschaetzungen, fehlende Schritte, Teststrategie]"

**🔧 Betriebs-Waechter (falls aktiviert):** "[Betriebs-, Deployment- und Sicherheitsrisiken]"

---

## Runde 3: Challenge (Anti-Bias)

**🏗️ Architekt (Pre-Mortem):** "Angenommen dieses Feature ist gescheitert — [wahrscheinlichstes Szenario und Ursache]."

**⚡ Pragmatiker (Devil's Advocate):** "Gegen diesen Plan spricht: [staerkstes Gegenargument]. Alternative: [einfachere Loesung]."

**💻 Senior Dev (Unknown Unknowns):** "Was wir nicht wissen: [versteckte Risiken, fehlende Informationen, ungetestete Annahmen]."

**🔧 Betriebs-Waechter (Adversarielles Day-2-Szenario, falls aktiviert):** "3 Uhr nachts: [sehen/stoppen wir die Stoerung?]. Angreifer: [wie wird die Aenderung ausgenutzt?]."

---

## Runde 4: Fragen an Damian

**🏗️ Architekt:** "Damian, [konkrete technische Entscheidungsfrage]?"

**⚡ Pragmatiker:** "Damian, [konkrete Priorisierungs-/Scope-Frage]?"

**💻 Senior Dev:** "Damian, [konkrete Frage zu Umsetzung/Zeitrahmen/Teststrategie]?"

**🔧 Betriebs-Waechter (falls aktiviert):** "Damian, [konkrete Frage zu Deployment/Betrieb/Sicherheit]?"

---

## Review-Zusammenfassung

| Dimension | Zustaendig | Verdikt | Anmerkung |
|-----------|------------|---------|-----------|
| Technische Machbarkeit | 🏗️ Architekt | PASS/WARN/FAIL | [kurz] |
| Abhaengigkeiten | 🏗️ Architekt | PASS/WARN/FAIL | [kurz] |
| Scope / MVP-Schnitt | ⚡ Pragmatiker | PASS/WARN/FAIL | [kurz] |
| Spec-Deckung | ⚡ Pragmatiker | PASS/WARN/FAIL | [deckt der Plan die Feature-Spec vollstaendig ab?] |
| Reihenfolge der Phasen | 💻 Senior Dev | PASS/WARN/FAIL | [kurz] |
| Zeitschaetzungen | 💻 Senior Dev | PASS/WARN/FAIL | [kurz] |
| Teststrategie | 💻 Senior Dev | PASS/WARN/FAIL | [kurz] |
| Betrieb & Haertung (nur falls aktiviert) | 🔧 Betriebs-Waechter | PASS/WARN/FAIL | [Deployment, Observability, Angriffsflaeche] |

[Falls Einsprueche: `Einspruch {Rolle} zu {Dimension}: {1 Satz}` + `Reaktion (Haupt-Skill, {zustaendige Rolle}): {bestaetigt|entkraeftet} — {1 Satz}`]

**Gesamt-Verdikt: SOUND / REVISE / RETHINK** — [1 Satz Herleitung ueber die feste Regel]

## Empfehlungen

1. [Konkrete Empfehlung] ([Herkunft: Rolle(n)])
2. [Konkrete Empfehlung] ([Herkunft: Rolle(n)])

---

{SOUND:} Moechtest du Anpassungen am Implementierungsplan vornehmen? (Ja/Nein)
{REVISE/RETHINK:} → Verdikt {REVISE|RETHINK}: direkt in die Finding-Runde
```

Die Zeile `📝 Kopf-Statusfeld → {Wert}` gehoert bewusst **NICHT** in diesen Block: Der Feldwert
haengt am Ausgang von Schritt 5 (wurden die Findings eingearbeitet?) und ist erst nach der
Anpassungs-Runde bestimmbar. Der Block oben endet mit der noch unbeantworteten Frage (SOUND)
bzw. mit dem Uebergang in die noch nicht gelaufene Finding-Runde (REVISE/RETHINK); die
📝-Zeile folgt danach als eigene Ausgabe (Schritt 6.3). Sie hier einzusetzen wuerde den Wert
festlegen, bevor die Antwort vorliegt — und damit die harte „behoben"-Bedingung aus 6.1 aushebeln.

---

## Wichtig — Anweisungen fuer die Ausfuehrung

- **Isolation:** Jede Rolle urteilt in ihrem eigenen Subagenten (Schritt 3) und argumentiert
  konsequent aus ihrer Perspektive; keine Rolle sieht die Rueckgabe einer anderen. Du ordnest nur
  an und fuegst den Runden nichts hinzu — einzige Ausnahme ist der sichtbare Rueckfall (3c)
- **Konkret bleiben:** Keine generischen Aussagen — immer Bezug auf den spezifischen Implementierungsplan
- **Verdikt-Disziplin:** Verdikte NUR in der Review-Zusammenfassung (nie in den Runden), nur PASS/WARN/FAIL
  (keine Zwischenstufen wie "WARN mit Tendenz PASS"), Gesamt-Verdikt strikt nach der festen Regel
- **Feature-Spec als Kontext:** Die Feature-Spec definiert das "Was/Warum" — der Plan das "Wie". Pruefe ob der Plan die Feature-Anforderungen vollstaendig abdeckt
- **Fragen muessen entscheidungsrelevant sein:** Nur Fragen stellen, deren Antwort den Plan tatsaechlich aendert
- **Max 3 Fragen pro Agent** in Runde 4 — Qualitaet vor Quantitaet
- **Deutsch:** Alle Texte auf Deutsch
- **Keine Datei-Erstellung:** Die Diskussion wird nur in der Konsole ausgegeben. Geschrieben wird
  ausschliesslich in `features/{slug}/plan.md`, und nur an zwei Stellen: Plan-Anpassungen nach
  Zustimmung in Schritt 5 und das Kopf-Statusfeld in Schritt 6 (Pfleger-Pflicht, still).
  Die Rollen-Subagenten schreiben nie — geschrieben wird nur im Hauptkontext
- **Finding-Runde (REVISE/RETHINK direkt, SOUND nach „Ja"):** Konkrete Aenderungen am Implementierungsplan vorschlagen und nach Bestaetigung umsetzen — je Empfehlung einzeln
