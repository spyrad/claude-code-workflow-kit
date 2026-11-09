# Discovery: Plan in einem Befehl
<!-- resume: done -->

**Erstellt:** 2026-11-09
**Idee-Referenz:** Inbox #178 — "Kette straffen (2/4): in der vollen Spur `dtb:feature-plan` und `dtb:impl-plan` mit einem Befehl nacheinander ausführen (spec.md, dann plan.md) — zwei Skills bleiben, keiner wird zusammengelegt."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-feature-plan/SKILL.md` | Kern: neuer Ausführungsschritt „impl-plan mitlaufen lassen" (Struktur-Check, Stopp-Weiche, Referenz-Ausführung), Backlog-Status je Ausgang, gemeinsamer Abschluss, Frontmatter (`next`, `consumes`, `produces`, `argument-hint`) |
| `skills/dtb-impl-plan/SKILL.md` | Nur Wartungs-Hinweise an den Anker-Sektionen: zweiter Referenz-Leser `dtb:feature-plan` neben `dtb:feature-fast` |
| `CLAUDE.md` | Skill-Lebenszyklus und Kategorie „Feature workflow" beschreiben feature-plan → impl-plan als zwei Befehle |
| `README.md` | Skill-Tabelle, Zeile `/dtb:feature-plan` |
| `skills/dtb-feature-discover/SKILL.md` | Abschlusszeile „Naechster Schritt: /dtb:feature-plan" — Hinweis, dass dieser Befehl bis plan.md führt |

---

## Anforderungen

### Scope
**Enthalten:**
- `dtb:feature-plan` führt nach dem Speichern von `spec.md` den Ablauf von `dtb:impl-plan` per Referenz aus: installierte `SKILL.md` lesen und anwenden, keine Kopie des Inhalts
- Stopp-Möglichkeit „nur spec.md" per Argument (`nur-spec`) bzw. ausdrücklichem Wunsch im Aufruftext
- Struktur-Check auf die genutzten Anker der impl-plan-Kopie vor der ersten Nutzung
- Backlog-Status, INBOX-Link und Abschlussmeldung passend zum tatsächlichen Ausgang (mit oder ohne plan.md)
- Frontmatter und Doku-Verweise nachziehen

**Nicht enthalten:**
- Zusammenlegen der beiden Skills — beide bleiben eigenständig aufrufbar
- `dtb:plan-review` mitlaufen lassen — bleibt eigener Schritt (frischer Blick)
- Umbau von `dtb:feature-start` / Abschlusszeilen Richtung `implement` (eigene Idee #179)
- Änderungen an `dtb:feature-fast` (bündelt schon, eigene Schiene)
- Umbau der Sichten, die bei „spec.md ohne plan.md" `/dtb:impl-plan` empfehlen (workflow-next, workflow-status, pane-start, project-health) — der Fall entsteht weiter durch „nur spec"

### Gewuenschtes Verhalten
- `/dtb:feature-plan {Name}` erzeugt `spec.md` und anschliessend `plan.md`, mit einer gemeinsamen Abschlussmeldung und dem nächsten Schritt `/dtb:plan-review {Name}`
- `/dtb:feature-plan {Name} nur-spec` verhält sich wie heute: nur `spec.md`, nächster Schritt `/dtb:impl-plan {Name}`
- Ohne Stopp-Angabe läuft impl-plan immer mit — es entsteht keine neue Rückfrage (per Veto-Vorlage bestätigt 2026-11-09)
- Mit laufen aus impl-plan: Lektionen-Prior (📚-Zeile), Eligibility-Gate (im selben Lauf erfüllt, daher still), Codebase-Research/Ist-Analyse, Planerstellung nach dem Template, Überschreib-Frage bei vorhandenem `plan.md`, Lektion-Kandidat-Vormerkung. Es entfallen die eigene Slug-Ermittlung (gleicher Slug) und die eigene Abschlussmeldung
- `plan.md` behält Inhalt und Fusszeile `**Erstellt mit:** /dtb:impl-plan` — ununterscheidbar von einem Einzel-Lauf

### Randfaelle
- impl-plan-Kopie weder global noch im Projekt gefunden → Installations-Hinweis (`/dtb:kit-sync`), `spec.md` bleibt gültig, Ende mit `→ Weiter mit: /dtb:impl-plan {Name}`
- Kopie vorhanden, Anker fehlt → Struktur-Drift-Meldung, kein Plan auf veralteter Basis, `spec.md` bleibt gültig, gleicher Weiter-Hinweis
- `plan.md` existiert schon → Überschreib-Frage von impl-plan gilt unverändert (bleibt beim Menschen)
- Keine `discovery.md` (feature-plan direkt aus dem Chat) → impl-plan-Scan mit Textzeilen-Bestätigung wie heute
- Verlinkter Worktree → Teil-Guard von feature-plan unverändert (INBOX/BACKLOG übersprungen); `plan.md` liegt im eigenen Change-Ordner und ist erlaubt
- Testordner-Slug (`zz-test-`, `abnahmeprobe-`) → kein BACKLOG-Eintrag wie heute

### Einschraenkungen
- Referenz, keine Kopie: die Regeln von impl-plan leben nur in dessen `SKILL.md` (Muster `dtb:feature-fast`)
- Beide Skills haben dieselben Werkzeuge (`Read, Write, Glob, Grep`) — kein `allowed-tools`-Nachzug nötig
- Frontmatter ist die maschinell gelesene Wahrheit (Lektion 44): `produces` und `consumes` im selben Zug nachziehen
- Struktur-Check vor der ersten Nutzung, nicht erst vor dem Schreiben (Lektion 89)

### Integrationspunkte
- `dtb:feature-fast` greppt in feature-plan auf `## Template fuer spec.md` und nutzt den Technical-Leak-Lint — beide Anker bleiben unverändert
- `dtb:impl-plan` trägt bereits Wartungs-Hinweise für `dtb:feature-fast`; der zweite Leser wird dort ergänzt
- `pipeline-graph`/`workflow-status` lesen `next:` aus dem Frontmatter

---

## Abhaengigkeiten

- Keine harten. Berührt sich mit #179 (feature-start überflüssig machen) nur in der Abschlusszeile von impl-plan, die hier nicht geändert wird

---

## Offene Punkte

- — keine —

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-09)
