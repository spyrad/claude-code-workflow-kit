# Discovery: Review-Härtung

**Erstellt:** 2026-07-08
**Idee-Referenz:** Inbox #3 — "Review-Härtung: Challenger-Pass (Widersprüche/Promise-Gaps) + ls/grep-Grounding in plan-review, Personas liefern Dimensions-Verdikte (PASS/WARN/FAIL → SOUND/REVISE/RETHINK); Severity×Impact-Doppelachse + Findings-Cap 10 + Fix-Optionen mit Tradeoff/Confidence + Resume-Marker für Triage-Wiederaufnahme in code-review (Vorbild: 10x-impl-review/plan-review)"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-plan-review/SKILL.md` | Bausteine 1–3: Challenger-Pass, Grounding, Dimensions-Verdikte. Challenge-Runde (Anti-Bias) existiert bereits seit Betriebs-Wächter (`4ee4a9a`) — wird ergänzt, nicht ersetzt |
| `skills/dtb-code-review/SKILL.md` | Bausteine 4–5: Severity×Impact-Doppelachse (ersetzt einachsige Prio 1–5), Findings-Cap 10, Fix-Optionen, Resume-Marker |
| `agents/architekt.md` | Verdikt-Zuordnung (Dimensionen im Skill, Agent bleibt rollenbeschreibend) |
| `agents/pragmatiker.md` | dito |
| `agents/senior-dev.md` | dito |
| `agents/betriebs-waechter.md` | Verdikt-Logik muss Fall „aktiviert/nicht aktiviert" berücksichtigen |
| `skills/dtb-lesson/SKILL.md` (indirekt) | Prior-Mechanik + Lektion-Kandidat-Vorschlag in beiden Review-Skills dürfen nicht brechen (keine Änderung an dtb-lesson selbst) |

Nicht betroffen (geprüft): `dtb-impl-plan` (PLAN-Format bleibt), `dtb-pipeline-graph` (nur bei Frontmatter-Änderung), `dtb-kit-sync` (Klasse-A-Muster deckt Änderungen automatisch ab).

---

## Anforderungen

### Scope

**Enthalten (5 Bausteine):**

*plan-review:*
1. **Challenger-Pass** — mechanische Konsistenz-Prüfung: Widersprüche zwischen Plan-Schritten, Promise-Gaps (Plan verspricht X, liefert es nie)
2. **ls/grep-Grounding** — Behauptungen des Plans über die Codebase (Dateien, Funktionen, Strukturen) werden per Glob/Grep verifiziert statt geglaubt
3. **Dimensions-Verdikte** — jeder Agent gibt PASS/WARN/FAIL pro Dimension; daraus deterministisch abgeleitetes Gesamt-Verdikt SOUND/REVISE/RETHINK

*code-review:*
4. **Findings-Härtung** — Severity×Impact-Doppelachse statt einachsiger Prio 1–5, Cap bei 10 Findings, Fix-Optionen mit Tradeoff + Confidence
5. **Resume-Marker** — Triage-Stand als kopierbarer Textblock am Report-Ende, damit ein abgebrochenes Review wiederaufgenommen werden kann

**Nicht enthalten:**
- Kein Umbau der Runden-Struktur von plan-review (4 Runden + Betriebs-Wächter-Logik Schritt 2c bleiben unangetastet)
- Kein automatisches Fixen — beide Reviews bleiben read-only, Empfehlungen bleiben Vorschläge
- Resume-Marker ist KEIN persistentes Pipeline-Artefakt (keine Datei, kein neues produces)
- Keine Änderung am Lektionen-Prior (Schritt 2b) oder an `dtb-lesson`

### Gewünschtes Verhalten

- **Verdikt-Platzierung:** Verdikte NUR in der Review-Zusammenfassung (Runden 1–4 bleiben reine Diskussion) — Verdikte sind das destillierte Ergebnis, nicht der Verlauf; frühe Verdikte würden Agenten vor der Challenge-Runde festnageln
- **Grounding still:** Checks laufen intern; nur Abweichungen werden gemeldet („⚠ Plan referenziert X — nicht gefunden"), bei Erfolg eine Zeile: `🔎 Grounding: N Referenzen geprüft, alle gefunden`
- **Resume-Marker:** kopierbarer Textblock am Report-Ende; beim nächsten Aufruf als Argument übergebbar
- **Etablierte UX-Muster weiterführen:** kompakte Ein-Zeilen-Hinweise (Muster `📚`/`🔧`), fixe Report-Templates mit Platzhaltern, Konsolen-Output statt Dateien

### Randfälle

- **Keine prüfbaren Referenzen** (z.B. Greenfield-Plan): Hinweiszeile `🔎 Grounding: keine prüfbaren Referenzen` — kein Fehler, kein Abbruch
- **Verdikt-Aggregation (feste Regel, deterministisch):** alle PASS → SOUND; ≥1 WARN, kein FAIL → REVISE; ≥1 FAIL → RETHINK. Ein einzelnes FAIL kann nicht durch PASS-Stimmen überstimmt werden
- **Findings-Cap-Überlauf:** Top 10 nach Severity×Impact zeigen + Zeile „N weitere Findings unterhalb des Caps (erneut ausführen nach Behebung)"
- **Resume-Marker-Verfall:** Marker enthält Commit-SHA des Review-Stands; bei Abweichung beim Wiederaufnehmen → Warnung + Frage, ob frisches Review

### Einschränkungen

- plan-review ist mit ~206 Zeilen bereits der größte Review-Skill — die 3 Bausteine dürfen ihn nicht bis zur Unlesbarkeit aufblähen
- `allowed-tools` reichen aus: plan-review hat Read/Glob/Grep (Grounding braucht nichts Neues), code-review hat zusätzlich Bash (git diff, Commit-SHA für Resume-Marker)
- Betriebs-Wächter-Aktivierung (Schritt 2c) und Lektionen-Prior (Schritt 2b) müssen unverändert funktionieren
- Beide Skills sind Klasse A → nach Abschluss `dtb:kit-sync`
- Keine fachlichen Constraints (keine Doku-Pflicht über die Skills hinaus, keine Rückwärtskompatibilität nötig — Pipeline leer)

### Integrationspunkte

- Verdikt-Dimensionen und Aggregations-Regel leben im **Skill** (`dtb-plan-review`); die Agenten-Dateien bleiben rollenbeschreibend (ggf. minimale Ergänzung der Verdikt-Pflicht)
- Betriebs-Wächter: liefert Verdikte nur wenn aktiviert; Aggregations-Regel arbeitet über die aktiven Agenten (3 oder 4)
- Nach Abschluss: `dtb:kit-sync` (globale Installation); `dtb:pipeline-graph` nur bei Frontmatter-Änderung (voraussichtlich nicht nötig)
- Externe Abhängigkeiten: keine — reines Markdown-Prompt-Kit. Vorbild `10x-impl-review`/`10x-plan-review` (Kurs-Repo `10x-devs-3.0`) dient als Inspiration, wird nicht eingebunden

---

## Abhängigkeiten

- Bestehende Features: 0 (Pipeline leer; DERIVED_STATE, KIT_SYNC, LESSON_LOOP archiviert)
- Konflikte: keine
- Berührung ohne Konflikt: **Betriebs-Wächter** (`4ee4a9a`, ohne FEATURE-Artefakt) hat plan-review zuletzt umgebaut — dieses Feature baut darauf auf; **LESSON_LOOP** hat den Prior verdrahtet — bleibt unangetastet

---

## Offene Punkte

- Zuschnitt der Verdikt-Dimensionen pro Agent (welche Dimensionen bewertet wer) — Detailfrage für `/dtb:feature-plan`
- Exaktes Format des Resume-Marker-Textblocks (Felder: Scope, Commit-SHA, offene Findings) — Detailfrage für den Plan

---

**Erstellt mit:** `/dtb:feature-discover`
