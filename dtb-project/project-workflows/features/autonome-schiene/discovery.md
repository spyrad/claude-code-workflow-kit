# Discovery: Autonome Schiene
<!-- resume: done -->

**Erstellt:** 2026-08-08
**Idee-Referenz:** Inbox #43 — "Autonome Schiene: Erkennung (ex-#49) + Ausfuehrung — leichtgewichtige Lane, die worker-taugliche Eintraege ohne die volle Kette (Discovery → Spec → Plan) erledigt"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-idea-review/SKILL.md | Dreier-Weiche bekaeme eine vierte Stufe "autonom" bzw. routet auf die neue Lane |
| skills/dtb-task/SKILL.md | Heutige Task-Lane: erfasst `task.md ## Schritte`, fuehrt aber nicht aus — die Lane setzt dort an |
| skills/dtb-implement/SKILL.md | Checkpoint-Kriterien / Verifikations-Gate = maschinelles Abbruch-/Erfolgskriterium des Workers |
| skills/CLAUDE.md | Governance-Konvention (read-only = modellaufrufbar, schreibend = nur Mensch) — hier muesste die Autonomie-Regel definiert werden |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | Single-Writer-Annahme; ein Worker, der `## Progress`/`## Schritte` abhakt, braucht eine geregelte Schreibrolle |
| skills/dtb-workflow-next/SKILL.md | Kandidat fuer Anzeige "autonom ausfuehrbar" bzw. Uebergabepunkt (Zuschnitt offen, s. 3a) |
| skills/dtb-workflow-checkpoint/SKILL.md | Rueckmeldung: wer schreibt Session-Log/Status nach einem autonomen Lauf? (Zuschnitt offen) |
| skills/dtb-autonome-schiene/SKILL.md | Der neue Skill selbst (Name/Slug provisorisch, Schritt 5) |

Referenzquellen (extern, KEINE Aenderungsziele — #32-Regel): Pocock-Skills-Repo
(https://github.com/mattpocock/skills) als Vorbild; Harness-Commands `/loop` (Intervall +
selbstgetaktet) und `/schedule` (Cloud-Agents) als Ausfuehrungs-Traeger-Kandidaten.

---

## Anforderungen

### Scope
**Enthalten:**
- Erkennungs-Seite (ex-#49): Urteil je INBOX-/Backlog-Eintrag — autonom ausfuehrbar ja / teilweise / nein, mit 1-Satz-Begruendung. Kriterien-Vorschlag: (1) Zielzustand mechanisch verifizierbar, (2) Scope geschlossen, (3) keine Fremdwirkung/Spiegel-Kopplung, (4) umkehrbar
- Ausfuehrungs-Seite: Worker arbeitet freigegebene Aufgaben ab (`task.md ## Schritte` bzw. definierte Schritte) und meldet mit gruenen Kriterien zur Abnahme — wahlweise einzeln ODER die gesamte vorgeschlagene Liste in der vorgeschlagenen Reihenfolge (Revision 3b: der 3a-Ausschluss "Listen-Durchlauf" ist aufgehoben)
- Parallel-Ausfuehrung, wo moeglich und gewuenscht (Nutzer-Entscheid 3b) — Gate: nur Eintraege, die laut Abhaengigkeits-Analyse unabhaengig sind und disjunkte Dateien anfassen; Isolation via Worktrees/Subagents
- Mensch gibt frei (vor dem Start) und nimmt ab (nach dem Lauf)

**Nicht enthalten:**
- Selbst committen/pushen — bleibt beim Menschen
- Status-/Anzeigefelder pflegen (Single-Writer-Annahme bleibt unangetastet)
- Start ohne menschliche Freigabe
- Discovery-/Spec-wuerdige Features — strikt nur Task-Lane-Material

### Gewuenschtes Verhalten
- **Erkennungs-Sicht:** scannt die INBOX (Ideen UND Tasks) und zeigt je Eintrag: Urteil
  (autonom ausfuehrbar ja/teilweise/nein), Abhaengigkeiten und eine empfohlene Reihenfolge
- **Nebenspalte "Vorab-Fragen":** fehlen einem Eintrag Kleinigkeiten zur vollstaendigen
  Autonomie (z.B. eine offene Scope-Entscheidung), stellt die Sicht pro Eintrag eine kurze
  Frage, die der Nutzer VOR der Ausfuehrung beantwortet
- **Freigabe-Wahl:** nach der Sicht fragt der Skill — einzelnen Task ausfuehren oder die
  gesamte vorgeschlagene Liste in der vorgeschlagenen Reihenfolge (inkl. paralleler
  Ausfuehrung unabhaengiger Eintraege)
- **Waehrend des Laufs:** Worker laufen im Hintergrund, der Nutzer arbeitet weiter,
  Meldung bei Abschluss
- **Bericht:** voller Bericht pro Task (was getan, was verifiziert, was aufgefallen) als
  **`worker-report.md` im jeweiligen Change-Ordner** — dritter Eintrag der status-neutralen
  Ordner-Datei-Familie (nach `review.md`, `fast-draft.md`); zaehlt NICHT fuer die
  Statusableitung. Im Chat nur kompakte Sammel-Zeilen mit Links (Status-Konvention).
  Preis: Deklaration in `DERIVED_STATE_RULES.md` = siebter Seed-Skew-Fall (#22)
- **Voraussetzung Ausfuehrung:** immer ein Change-Ordner mit definierten Schritten —
  eine INBOX-Idee ohne Ordner muss vorher durch `/dtb:task` (Nebenspalte weist darauf hin)

### Randfaelle
- **Kriterien werden nie gruen:** Deckelung ueber max. Versuche/Zeit; danach Abbruch mit
  Befund im Bericht ("so weit gekommen, daran gescheitert")
- **Ungeklaerte Entscheidung mitten im Lauf** (von den Vorab-Fragen nicht abgefangen):
  abbrechen und als "teilweise" zurueckmelden — kein Anhalten/Nachfragen, der
  Hintergrund-Charakter bleibt ungestoert
- **"teilweise"-Eintraege beim Listen-Lauf:** ueberspringen und am Ende gesammelt melden
- **Abnahme lehnt ab:** Ergebnis (Worktree/Diff) liegen lassen fuer einen zweiten Lauf
  mit Korrekturhinweis — nicht verwerfen
- **Kollision trotz Analyse** (zwei parallele Worker fassen dieselbe Datei an): zweiter
  Worker stoppt. Zentrale Dateien (v.a. `WORKFLOW_STATUS.md`) duerfen nur von einem
  Agenten gleichzeitig bespielt werden → Koordinations-/Locking-Mechanismus noetig
  (offener Punkt, s.u.)
- **Kein Eintrag tauglich:** melden UND je Eintrag begruenden, was zur Tauglichkeit
  fehlt (die Nebenspalte fuer alle)

### Einschraenkungen
- **Governance:** Der Skill ist schreibend → `disable-model-invocation: true`, nur der
  Mensch startet ihn. Autonomie beginnt nach der Freigabe und endet an der Abnahme —
  das Modell entscheidet nie selbst, DASS gearbeitet wird. Die Kit-Konvention
  "schreibend = nur Mensch" bleibt formal intakt (Delegation pro Lauf); als Regel auch
  in `skills/CLAUDE.md` festschreiben
- **Deckelung konfigurierbar:** Limits (max. Versuche, max. Zeit pro Task) in
  `workflow.config.yaml`, nicht fest im Skill. Default-Vorschlag fuer die Spec:
  3 Versuche / 30 Minuten pro Task (Zahlen vom Nutzer noch nicht bestaetigt)
- **Traeger-Degradation:** Fehlt ein Ausfuehrungs-Traeger (z.B. kein Git-Repo → keine
  Worktree-Isolation), degradiert die Lane auf sequenzielle Ausfuehrung — sie
  verweigert nicht

### Integrationspunkte
- **Dreier-Weiche (`idea-review`): unangetastet.** Die Erkennungs-Sicht der Lane ist der
  einzige Einstieg — keine vierte Stufe im Erstwurf (vermeidet Doppel-Urteil an zwei
  Stellen und einen Klasse-A-Eingriff). Beleg-getrieben nachruesten, falls sich manuelle
  Umleitungen haeufen (Empfehlung angenommen)
- **#33 (Triage-Sicht): Variante (b)** — die Erkennungs-Sicht wird so gebaut, dass #33
  spaeter als zweites Bewertungsraster andocken kann: EIN Scanner ueber die INBOX,
  mehrere Sichten. Kein Miterledigen von #33 in diesem Zuschnitt
- **`workflow-next` + `workflow-checkpoint`: im Erstwurf nicht anfassen.** Einstieg ist
  die Lane-Sicht, Ausgang die `worker-report.md`; eine "autonom ausfuehrbar"-Anzeige in
  `workflow-next` ist Folge-Zuschnitt
- **Externe Abhaengigkeiten:** nur Harness-Features (Subagents, Worktrees,
  Background-Tasks, ggf. `/loop`) — keine APIs/Services

---

## Abhaengigkeiten

- **Konflikte:** keine — kein aktives Vorhaben (4 Features "Fertig zum Testen",
  1 Aufgabe offen) arbeitet an unseren Aenderungszielen
- **`gitattributes-eol` (0/6):** geborener Erstlauf-Kandidat der Lane — ex-#49-Probe
  stufte ihn als "teilweise" ein (Schritt 1 ist Scope-Entscheidung → Testfall fuer die
  Vorab-Fragen-Nebenspalte)
- **`DERIVED_STATE_RULES.md`-Aenderung** (worker-report.md-Deklaration) = siebter
  Seed-Skew-Fall → Beleg fuer INBOX #22
- **INBOX #42** (parallele Sessions) bleibt offen, wird schmaler: die Lane liefert
  Parallel-Ausfuehrung von Tasks; #42 behaelt parallele Menschen-Sessions
- **`workflow.config.yaml`:** Limits landen in der Datei, deren Platzhalter-Befuellung
  ohnehin als offene Aufgabe im Status steht

---

## Offene Punkte

- Schreibkoordination bei parallelen Workern: Wie wird sichergestellt, dass zentrale
  Dateien (`WORKFLOW_STATUS.md`, INBOX, BACKLOG) nur von einem Agenten gleichzeitig
  geschrieben werden — Lock-Datei, Schreib-Queue, oder Worker schreiben zentrale Dateien
  gar nicht und nur der koordinierende Haupt-Agent aggregiert? (Nutzer 3c: "locken oder
  so — ueberdenken"; Scope-Ausschluss "Worker pflegen keine Statusfelder" loest das fuer
  Status, aber nicht fuer alle geteilten Ziele)

---

**Erstellt mit:** `/dtb:feature-discover`
