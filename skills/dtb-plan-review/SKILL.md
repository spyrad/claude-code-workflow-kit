---
name: dtb:plan-review
description: >-
  Use when: "Plan Review", "Implementierungsplan reviewen", "Plan bewerten",
  "Plan pruefen". Conducts a structured review of an implementation plan
  with three agent perspectives (Architekt, Pragmatiker, Senior Dev).
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[Feature-Name]"
pipeline:
  stage: planning
  after: dtb:impl-plan
  next: dtb:feature-start
  consumes: [features/*/plan.md, features/*/spec.md, agents/*.md, project-rules/DERIVED_STATE_RULES.md, project-rules/lessons.md]
  produces: []
---

# Plan Review Discussion

Du fuehrst ein strukturiertes Review eines Implementierungsplans durch. Drei Agenten (Architekt, Pragmatiker und Senior Dev) diskutieren den Plan und stellen Damian als Product Owner gezielte Fragen. Bei Ops-/Security-Bezug kommt ein vierter Agent (Betriebs-Waechter) hinzu — Aktivierung siehe Schritt 2c.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Schritt 1: Plan und Feature-Spec laden

1. **Feature ermitteln:** Frage den Benutzer nach dem Feature-Namen/Slug, falls nicht aus dem Chat-Kontext erkennbar
2. **Plan lesen:** Lies `{config.paths.workflows}/features/{slug}/plan.md`
   - **Formal-Check `## Progress`:** Der Plan muss eine `## Progress`-Sektion haben —
     genau eine Checkbox-Zeile pro Schritt N.M, Format gemaess
     `{config.paths.rules}/DERIVED_STATE_RULES.md` §2. Fehlt die Sektion oder weicht
     die Nummerierung von den Plan-Schritten ab → als Finding in Runde 2 aufnehmen
     (der Umsetzungsstand waere sonst nicht ableitbar)
3. **Feature-Spec lesen:** Lies `{config.paths.workflows}/features/{slug}/spec.md` als zusaetzlichen Kontext

Falls Plan nicht gefunden:
```
Implementierungsplan nicht gefunden: features/{slug}/plan.md
Erstelle zuerst einen Implementierungsplan mit /dtb:impl-plan.
```

## Schritt 2: Agent-Definitionen laden

Lies die Agenten-Definitionen aus dem Projekt-Root:
- `agents/architekt.md`
- `agents/pragmatiker.md`
- `agents/senior-dev.md`
- `agents/betriebs-waechter.md` — nur laden, wenn in Schritt 2c aktiviert

Nimm diese Rollen fuer die Diskussion ein.

## Schritt 2b: Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) → diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `plan-review` oder `alle` enthaelt
- Die Agenten beruecksichtigen die passenden `Rule`-Aussagen in ihrer Diskussion still
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

- **Mindestens ein Trigger** → `agents/betriebs-waechter.md` laden; der Agent nimmt als
  vierte Stimme an allen Runden teil. Gib aus: `🔧 Betriebs-Waechter aktiviert: {Trigger-Grund}`
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

## Schritt 3: Diskussion fuehren

Fuehre die Diskussion in **4 Runden** basierend auf dem geladenen Implementierungsplan (mit Feature-Spec als Kontext):

### Runde 1 — Staerken des Implementierungsplans
Alle aktiven Agenten bewerten, was am Plan gut ist — jeweils aus ihrer Perspektive: Systemdesign (Architekt), Scope und Spec-Deckung (Pragmatiker), Umsetzbarkeit (Senior Dev), Betrieb & Haertung (Betriebs-Waechter, falls aktiviert).

### Runde 2 — Bedenken & Risiken
Alle aktiven Agenten identifizieren Probleme aus ihrer Perspektive: technische Risiken und Abhaengigkeiten (Architekt), Scope-Creep, Aufwand-Nutzen und Spec-Deckung — deckt der Plan die Feature-Spec vollstaendig ab, ohne darueber hinauszugehen (Pragmatiker), unrealistische Zeitschaetzungen und fehlende Implementierungsschritte (Senior Dev), und — falls aktiviert — Betriebs-, Deployment- und Sicherheitsrisiken (Betriebs-Waechter).
Befunde aus Grounding (2d) und Challenger-Pass (2e) werden hier von den zustaendigen Agenten
aufgegriffen und bewertet.

### Runde 3 — Challenge-Runde (Anti-Bias)
Alle aktiven Agenten wenden gezielt kritische Analysetechniken an:
- **Architekt:** Pre-Mortem — "Angenommen das Feature ist gescheitert. Was war die wahrscheinlichste Ursache?"
- **Pragmatiker:** Devil's Advocate — "Was spricht GEGEN diesen Plan? Welche einfachere Alternative wurde uebersehen?"
- **Senior Dev:** Unknown Unknowns — "Was wissen wir NICHT, das uns spaeter ueberraschen koennte?"
- **Betriebs-Waechter (falls aktiviert):** Adversarielles Day-2-Szenario — "Es ist 3 Uhr nachts und das System verhaelt sich falsch: sehen wir es und koennen wir es stoppen? Und wie wuerde ein Angreifer genau diese Aenderung ausnutzen?"

### Runde 4 — Fragen an Damian
Alle aktiven Agenten stellen gezielte Entscheidungsfragen an Damian. Die Fragen sollen konkret und entscheidungsrelevant sein — keine rhetorischen Fragen. Fragen koennen sich auf Erkenntnisse aus der Challenge-Runde beziehen.

## Schritt 4: Zusammenfassung mit Verdikt

Erstelle die Verdikt-Liste und konkrete Empfehlungen. Verdikte werden ERST JETZT vergeben —
nach Runde 3, nie innerhalb der Runden 1-4 (fruehe Verdikte nageln die Agenten vor der
Challenge-Runde fest). Jeder Agent bewertet NUR seine eigenen Dimensionen:

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

**Einspruchs-Regel:** Sieht ein Agent ein Problem in einer fremden Dimension, ergaenzt er
unter der Liste eine Zeile `Einspruch {Agent} zu {Dimension}: {1 Satz}`. Der zustaendige
Agent bestaetigt oder entkraeftet in einem Satz. Ein bestaetigter Einspruch zaehlt wie WARN
der Dimension — bei belegtem schwerwiegendem Fall wie FAIL.

**Gesamt-Verdikt (feste Regel — nie aufweichen, keine Zwischenstufen):**
- alle Dimensionen PASS → **SOUND**
- mindestens ein WARN, kein FAIL → **REVISE**
- mindestens ein FAIL → **RETHINK**

## Schritt 5: Anpassungen anbieten

Frage Damian ob Anpassungen am Implementierungsplan vorgenommen werden sollen.

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

[Falls Einsprueche: `Einspruch {Agent} zu {Dimension}: {1 Satz}` + Reaktion des zustaendigen Agenten (1 Satz)]

**Gesamt-Verdikt: SOUND / REVISE / RETHINK** — [1 Satz Herleitung ueber die feste Regel]

## Empfehlungen

1. [Konkrete Empfehlung]
2. [Konkrete Empfehlung]

---

Moechtest du Anpassungen am Implementierungsplan vornehmen? (Ja/Nein)
```

---

## Wichtig — Anweisungen fuer die Ausfuehrung

- **Rollen einhalten:** Jeder Agent argumentiert konsequent aus seiner Perspektive
- **Konkret bleiben:** Keine generischen Aussagen — immer Bezug auf den spezifischen Implementierungsplan
- **Verdikt-Disziplin:** Verdikte NUR in der Review-Zusammenfassung (nie in den Runden), nur PASS/WARN/FAIL
  (keine Zwischenstufen wie "WARN mit Tendenz PASS"), Gesamt-Verdikt strikt nach der festen Regel
- **Feature-Spec als Kontext:** Die Feature-Spec definiert das "Was/Warum" — der Plan das "Wie". Pruefe ob der Plan die Feature-Anforderungen vollstaendig abdeckt
- **Fragen muessen entscheidungsrelevant sein:** Nur Fragen stellen, deren Antwort den Plan tatsaechlich aendert
- **Max 3 Fragen pro Agent** in Runde 4 — Qualitaet vor Quantitaet
- **Deutsch:** Alle Texte auf Deutsch
- **Keine Datei-Erstellung:** Die Diskussion wird nur in der Konsole ausgegeben (Write dient
  ausschliesslich Plan-Anpassungen nach Zustimmung in Schritt 5)
- **Bei "Ja" zu Anpassungen:** Konkrete Aenderungen am Implementierungsplan vorschlagen und nach Bestaetigung umsetzen
