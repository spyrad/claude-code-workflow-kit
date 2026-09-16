# Discovery: feature-start schreibt keine Anzeigefelder mehr
<!-- resume: done -->

**Erstellt:** 2026-08-07
**Idee-Referenz:** Inbox #50 — „`dtb:feature-start` widerspricht dem Status-Kanon: Der Skill weist an, beim Start `In Arbeit` zu setzen — `DERIVED_STATE_RULES.md` §1.1 leitet bei vorhandenem `plan.md` mit 0 abgehakten Checkboxen aber `Geplant` ab"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-feature-start/SKILL.md` | Einzige Substanz-Datei: Schritt-4-Bloecke (Feature/Bug/Aufgabe) schreiben Anzeigefelder; Frontmatter (`description`, `produces`, `allowed-tools`), Ausgabe-Templates und „Wichtig"-Block spiegeln dieselbe Aussage |
| `skills/CLAUDE.md` | Doku-Spiegel: Z. 107 beschreibt `feature-start` als „nur Status-Updater" — nach der Aenderung falsch |

---

## Anforderungen

### Scope

**Enthalten:**
- Alle Schreibanweisungen auf **Anzeigefelder** aus `dtb:feature-start` entfernen — BACKLOG-Status (Feature Z. 96, Bug Z. 102, Aufgabe Z. 108) und `WORKFLOW_STATUS.md` (Z. 97/103/109)
- Frontmatter an die neue Wirkung anpassen: `description` (nennt heute „updating status to «In Arbeit»"), `produces`, `allowed-tools`
- Ausgabe-Templates (Z. 117/142/168 „Status: Geplant → In Arbeit") und „Wichtig"-Block (Z. 187 „Status-Update: BACKLOG.md und WORKFLOW_STATUS.md muessen aktualisiert werden") mitziehen
- Doku-Spiegel `skills/CLAUDE.md:107` korrigieren

**Nicht enthalten:**
- **Die Lese-Seite der Sektion „Laufende Arbeit"** — vier Skills adressieren eine Sektion, die niemand mehr erzeugt. Bewusst ausgeklammert (Nutzer-Entscheid 2026-08-07), separat als **Inbox #52** erfasst
- Die Progress-Nachruestung (Z. 94) — sie repariert eine fehlende Struktur, sie pflegt kein Anzeigefeld, und bleibt unveraendert
- Eligibility-Gate, Auswahl-Logik und Kontext-Anzeige des Skills
- Migration bestehender Projekte (siehe Einschraenkungen)

### Gewuenschtes Verhalten

- Ein Feature-, Bug- oder Aufgaben-Start **veraendert keine Statusanzeige** — er liest die Artefakte, zeigt den Kontext und verweist auf `/dtb:implement`
- Der abgeleitete Status bleibt nach dem Start unveraendert (`Geplant` / `Offen` / `Analysiert`) und wechselt erst mit dem ersten abgehakten Schritt auf `In Arbeit` — genau wie es `DERIVED_STATE_RULES.md:40` und §1.5 beschreiben
- Ein anschliessender `/dtb:workflow-resume` meldet **keinen** Feld-Konflikt mehr
- Schreibender Pfleger der Anzeigefelder ist allein `dtb:workflow-checkpoint` (§1.3)

### Randfaelle

- **Progress-Nachruestung:** Der Skill bietet bei Altbestand an, eine fehlende `## Progress`-Sektion nachzuruesten — das schreibt `plan.md`. Schreibrecht muss dafuer erhalten bleiben; nur `Write` (Neuanlage) entfaellt, `Edit` bleibt
- **Sichtbarkeitsluecke:** Zwischen Start und erstem Haekchen ist die begonnene Arbeit in BACKLOG und Statusdatei nicht als „laufend" erkennbar. Bewusst akzeptiert: genau diese Sichtbarkeit war die falsche Behauptung. Verwandt mit Inbox #44 (Zustand ohne Leseansicht)
- **Bug- und Aufgaben-Lane:** Beide schreiben denselben Fehler in die Artefaktdatei selbst (`bug.md`: `Analysiert` → `In Arbeit`; `task.md`: `Offen` → `In Arbeit`). Da ihr Status nach §1.5 aus der Checkliste abgeleitet wird, gilt dieselbe Regel — bei 0 abgehakten Schritten ist `In Arbeit` falsch
- **Bestandsprojekte mit bereits falsch gesetztem Feld:** Kein Reparaturlauf noetig — `workflow-checkpoint` synchronisiert Anzeigefelder ohnehin bei jedem Lauf (§1.3)

### Einschraenkungen

- Kein Seed-Skew (Inbox #22): `DERIVED_STATE_RULES.md` nennt `feature-start` an keiner Stelle (Grep 2026-08-07, 0 Treffer) — der Kanon bleibt unveraendert, Bestandsprojekte brauchen keinen neuen Seed
- `skills/dtb-feature-start/SKILL.md` ist ein Klasse-A-Artefakt: die Aenderung erreicht die installierten Kopien erst ueber Commit → Push → `/dtb:kit-sync sync` (Muster belegt durch Inbox #51, 2026-08-07)
- Der Skill bleibt gegen Modell-Initiative gesperrt, obwohl er seine Schreib-Wirkung verliert (siehe `spec.md` → Offene Punkte)

### Integrationspunkte

- **Vorgaenger** (`plan-review`, `debug-plan`) und **Nachfolger** (`implement`) bleiben unveraendert — die Pipeline-Kanten werden nicht angefasst
- `dtb:workflow-checkpoint` bleibt der einzige Schreiber der Anzeigefelder; sein Verhalten aendert sich nicht
- `dtb:workflow-resume` profitiert unmittelbar: sein §1.3-Konfliktbericht wird wieder aussagekraeftig, weil das Dauer-Rauschen entfaellt

---

## Abhaengigkeiten

- Keine. Der Zuschnitt beruehrt eine Substanz-Datei und einen Doku-Spiegel; kein anderer Change wartet darauf oder blockiert ihn.
- Beruehrungen ohne Abhaengigkeit: Inbox **#52** (Lese-Seite „Laufende Arbeit", hier ausgeklammert), **#44** (Sichtbarkeit begonnener Arbeit), **#35** (Zustandsaussagen ohne Pfleger — dieselbe Familie)

---

## Offene Punkte

- [ ] Soll `disable-model-invocation` auf `false` wechseln, sobald der Skill keine Anzeigefelder mehr schreibt? Die Kit-Konvention (read-only = modellaufrufbar) legt es nahe, die Rolle als bewusster Workflow-Schritt spricht dagegen. Vorlaeufig `true` (per Veto-Vorlage bestaetigt 2026-08-07)

---

**Erstellt mit:** `/dtb:feature-fast` (Fast-Track, Sammelvorlage bestaetigt 2026-08-07)
